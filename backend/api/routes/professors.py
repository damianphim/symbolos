"""
backend/api/routes/professors.py  (updated — mcgill.courses blended ratings)

Professor rating endpoints. Now returns three rating fields:
  - rmp_rating      : RateMyProfessors (existing)
  - mc_rating       : mcgill.courses   (new, populated by scraper)
  - blended_rating  : weighted average by num_ratings (new)

The frontend ProfessorRating component shows all three when available,
or falls back gracefully to whichever sources exist.

Endpoints (unchanged URLs for backwards compatibility):
  GET /professors/rmp?name=<n>
  GET /professors/rmp-by-course?subject=ECON&catalog=208
  GET /professors/search?q=<n>
  GET /professors/rmp-bulk?courses=ECON208,COMP202
  POST /professors/rmp-bulk
"""

from fastapi import APIRouter, HTTPException, Query, status, Depends, Request
from typing import Optional, List
from pydantic import BaseModel
import logging
import re
from difflib import SequenceMatcher

from ..utils.supabase_client import get_supabase
from ..utils.cache import search_cache
from ..auth import get_current_user_id

router = APIRouter()
logger = logging.getLogger(__name__)

# ── Column selection ──────────────────────────────────────────────────────────

# Include new mc_* and blended_rating columns (graceful: NULL if not yet scraped)
_RMP_COLS = (
    'instructor, Course, course_name, '
    'rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again, '
    'mc_rating, mc_num_ratings, blended_rating'
)

_RMP_PROF_PREFIX   = "rmp_prof:"
_RMP_COURSE_PREFIX = "rmp_course:"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _name_similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def _normalize_name(name: str) -> str:
    name = re.sub(r'\b(dr|prof|professor|mr|mrs|ms)\b\.?', '', name, flags=re.IGNORECASE)
    return re.sub(r'\s+', ' ', name).strip().lower()


def _best_rmp_row(rows: list, target_name: str) -> dict | None:
    best_row, best_score = None, 0.0
    target_norm = _normalize_name(target_name)
    for row in rows:
        instr = row.get('instructor') or ''
        if not instr:
            continue
        # Require at least one rating source to be present
        if not row.get('rmp_rating') and not row.get('mc_rating') and not row.get('blended_rating'):
            continue
        score = _name_similarity(target_norm, _normalize_name(instr))
        if score > best_score:
            best_score = score
            best_row = row
    return best_row if best_score >= 0.60 else None


def _compute_blended(row: dict) -> Optional[float]:
    """
    Compute blended rating on-the-fly if the DB column isn't populated yet.
    Uses weighted average by num_ratings.
    """
    # Prefer pre-computed blended from DB
    if row.get('blended_rating'):
        return float(row['blended_rating'])

    rmp_r = row.get('rmp_rating')
    rmp_n = int(row.get('rmp_num_ratings') or 0)
    mc_r  = row.get('mc_rating')
    mc_n  = int(row.get('mc_num_ratings') or 0)

    # Normalize mc_rating if on 100-point scale
    if mc_r and float(mc_r) > 5:
        mc_r = float(mc_r) / 20.0

    if rmp_r and mc_r:
        total = rmp_n + mc_n
        if total == 0:
            return round((float(rmp_r) + float(mc_r)) / 2, 2)
        return round((float(rmp_r) * rmp_n + float(mc_r) * mc_n) / total, 2)

    return float(rmp_r) if rmp_r else (float(mc_r) if mc_r else None)


def _build_rmp_url(instructor: str) -> str | None:
    if not instructor:
        return None
    encoded = instructor.strip().replace(' ', '+')
    return f"https://www.ratemyprofessors.com/search/professors?q={encoded}&sid=U2Nob29sLTEyNDY="


def _format_professor(row: dict | None) -> dict | None:
    """Serialize a courses-table row into the professor rating payload."""
    if not row:
        return None

    instr = row.get('instructor') or ''
    parts = instr.split()
    first = ' '.join(parts[:-1]) if len(parts) > 1 else ''
    last  = parts[-1] if parts else instr

    rmp_r  = float(row['rmp_rating'])  if row.get('rmp_rating')  else None
    mc_r   = float(row['mc_rating'])   if row.get('mc_rating')   else None
    # Normalize mc if on 100-pt scale
    if mc_r and mc_r > 5:
        mc_r = round(mc_r / 20.0, 2)

    blended = _compute_blended(row)

    # Determine primary display rating: blended > rmp > mc
    display_rating = blended or rmp_r or mc_r

    return {
        # Identity
        'name':       instr,
        'first_name': first,
        'last_name':  last,

        # RMP data (original source)
        'rmp_rating':              rmp_r,
        'rmp_difficulty':          float(row['rmp_difficulty'])        if row.get('rmp_difficulty')        else None,
        'rmp_num_ratings':         int(row['rmp_num_ratings'])         if row.get('rmp_num_ratings')       else 0,
        'rmp_would_take_again':    float(row['rmp_would_take_again'])  if row.get('rmp_would_take_again')  else None,
        'rmp_url':                 _build_rmp_url(instr),

        # mcgill.courses data (new)
        'mc_rating':               mc_r,
        'mc_num_ratings':          int(row['mc_num_ratings'])          if row.get('mc_num_ratings')        else 0,
        'mc_url':                  f"https://mcgill.courses/instructor/{instr.replace(' ', '-')}",

        # Blended (best for display)
        'blended_rating':          blended,
        'avg_rating':              display_rating,  # kept for backwards compat

        # Metadata
        'rating_source': (
            'both'     if rmp_r and mc_r else
            'rmp_only' if rmp_r          else
            'mc_only'  if mc_r           else
            'none'
        ),
        'course':   row.get('Course'),
        'course_name': row.get('course_name'),
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/rmp", response_model=dict)
async def get_rmp_by_name(
    name: str = Query(..., min_length=2, max_length=100),
    subject: Optional[str] = Query(None, min_length=2, max_length=6),
    req: Request = None, _: str = Depends(get_current_user_id),
):
    """
    Look up combined RMP + mcgill.courses rating for a professor by name.
    Returns blended_rating in addition to the individual source ratings.
    """
    clean_name = name.strip()
    cache_key  = f"{_RMP_PROF_PREFIX}{subject or ''}:{clean_name.lower()}"
    cached = search_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        supabase = get_supabase()
        parts     = clean_name.split()
        last_name = parts[-1] if parts else clean_name

        qb = (
            supabase.from_('courses')
            .select(_RMP_COLS)
            .ilike('instructor', f'%{last_name}%')
        )
        if subject:
            qb = qb.like('Course', f'{subject.upper()}%')
        rows = qb.order('Course').limit(200).execute().data or []

        best = _best_rmp_row(rows, clean_name)

        # Fallback by first name
        if best is None and len(parts) > 1:
            qb2 = (
                supabase.from_('courses')
                .select(_RMP_COLS)
                .ilike('instructor', f'%{parts[0]}%')
            )
            if subject:
                qb2 = qb2.like('Course', f'{subject.upper()}%')
            rows2 = qb2.limit(200).execute().data or []
            best = _best_rmp_row(rows2, clean_name)

        if best is None:
            result = {'found': False, 'professor': None, 'match_score': 0.0}
        else:
            match_score = _name_similarity(
                _normalize_name(clean_name),
                _normalize_name(best.get('instructor') or '')
            )
            result = {
                'found':       True,
                'professor':   _format_professor(best),
                'match_score': round(match_score, 3),
            }

        search_cache.set(cache_key, result, ttl=600)
        return result

    except Exception as e:
        logger.exception(f"RMP lookup by name failed for '{name}': {e}")
        raise HTTPException(status_code=500, detail="Failed to look up professor rating")


@router.get("/rmp-by-course", response_model=dict)
async def get_rmp_by_course(
    subject: str = Query(..., min_length=2, max_length=6),
    catalog: str = Query(..., min_length=1, max_length=10),
    _: str = Depends(get_current_user_id),
):
    """
    Return all instructors (with blended RMP + mcgill.courses ratings)
    who have taught this course, sorted by blended_rating desc.
    """
    clean_subject = subject.strip().upper()
    clean_catalog = catalog.strip()
    course_code   = f"{clean_subject}{clean_catalog}"

    cache_key = f"{_RMP_COURSE_PREFIX}{course_code}"
    cached = search_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        supabase = get_supabase()

        response = (
            supabase.from_('courses')
            .select(_RMP_COLS + ', "Term Name"')
            .eq('Course', course_code)
            .execute()
        )
        rows = response.data or []

        # Deduplicate by instructor; keep best row (prefer highest blended, then rmp)
        seen: dict[str, dict] = {}
        for row in rows:
            instr = row.get('instructor') or ''
            if not instr:
                continue
            if instr not in seen:
                seen[instr] = row
            else:
                # Prefer row with any rating data
                existing_score = float(seen[instr].get('blended_rating') or seen[instr].get('rmp_rating') or 0)
                new_score      = float(row.get('blended_rating')         or row.get('rmp_rating')         or 0)
                if new_score > existing_score:
                    seen[instr] = row

        professors = [
            _format_professor(row)
            for row in seen.values()
            if row.get('rmp_rating') or row.get('mc_rating') or row.get('blended_rating')
        ]

        # Sort: blended first, then rmp-only, then mc-only
        professors.sort(key=lambda p: p['avg_rating'] or 0, reverse=True)

        result = {
            'course_code': f"{clean_subject} {clean_catalog}",
            'professors':  professors,
            'count':       len(professors),
        }
        search_cache.set(cache_key, result, ttl=600)
        return result

    except Exception as e:
        logger.exception(f"RMP by-course failed for {course_code}: {e}")
        raise HTTPException(status_code=500, detail="Failed to look up course professors")


@router.get("/search", response_model=dict)
async def search_professors(
    q: str = Query(..., min_length=2, max_length=80),
    subject: Optional[str] = Query(None, min_length=2, max_length=6),
    limit: int = Query(default=10, ge=1, le=50),
    _: str = Depends(get_current_user_id),
):
    """Search for professors by name. Returns blended ratings."""
    clean_q   = q.strip()
    cache_key = f"prof_search:{subject or ''}:{clean_q.lower()}:{limit}"
    cached    = search_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        supabase = get_supabase()
        qb = (
            supabase.from_('courses')
            .select(_RMP_COLS)
            .ilike('instructor', f'%{clean_q}%')
        )
        if subject:
            qb = qb.like('Course', f'{subject.upper()}%')
        rows = qb.order('instructor').limit(500).execute().data or []

        seen: dict[str, dict] = {}
        for row in rows:
            instr = row.get('instructor') or ''
            if not instr:
                continue
            existing  = float(seen[instr].get('blended_rating') or seen[instr].get('rmp_rating') or 0) if instr in seen else 0
            this_score = float(row.get('blended_rating') or row.get('rmp_rating') or 0)
            if instr not in seen or this_score > existing:
                seen[instr] = row

        professors = [_format_professor(row) for row in seen.values()]
        professors.sort(key=lambda p: (p['avg_rating'] or 0), reverse=True)
        professors = professors[:limit]

        result = {'professors': professors, 'count': len(professors), 'query': clean_q}
        search_cache.set(cache_key, result, ttl=300)
        return result

    except Exception as e:
        logger.exception(f"Professor search failed for '{q}': {e}")
        raise HTTPException(status_code=500, detail="Failed to search professors")


class BulkRmpRequest(BaseModel):
    codes: List[str]


@router.get("/rmp-bulk", response_model=dict)
async def get_rmp_bulk(courses: str = Query(...), _: str = Depends(get_current_user_id)):
    """Bulk blended rating lookup by course codes (GET version)."""
    return await _bulk_lookup(courses.split(','))


@router.post("/rmp-bulk", response_model=dict)
async def get_rmp_bulk_post(body: BulkRmpRequest, _: str = Depends(get_current_user_id)):
    """Bulk blended rating lookup by course codes (POST version)."""
    return await _bulk_lookup(body.codes)


async def _bulk_lookup(raw_codes: list[str]) -> dict:
    codes = [c.strip().upper().replace(' ', '') for c in raw_codes if c.strip()]
    if not codes:
        raise HTTPException(status_code=422, detail="No course codes provided")
    codes = codes[:60]

    cache_key = f"rmp_bulk:{'|'.join(sorted(codes))}"
    cached = search_cache.get(cache_key)
    if cached is not None:
        return cached

    try:
        supabase = get_supabase()
        or_filter = ','.join(f'Course.eq.{c}' for c in codes)
        rows = (
            supabase.from_('courses')
            .select(_RMP_COLS + ', "Term Name"')
            .or_(or_filter)
            .execute()
            .data or []
        )

        by_course: dict[str, list] = {}
        for row in rows:
            code = (row.get('Course') or '').upper()
            by_course.setdefault(code, []).append(row)

        ratings: dict = {}
        for code in codes:
            normalized = re.sub(r'^([A-Z]{2,6})(\d)', r'\1 \2', code)
            course_rows = by_course.get(code, [])
            best = max(
                (r for r in course_rows if r.get('blended_rating') or r.get('rmp_rating') or r.get('mc_rating')),
                key=lambda r: float(r.get('blended_rating') or r.get('rmp_rating') or r.get('mc_rating') or 0),
                default=None,
            )
            ratings[normalized] = _format_professor(best) if best else None

        result = {'ratings': ratings, 'courses_checked': len(codes)}
        search_cache.set(cache_key, result, ttl=600)
        return result

    except Exception as e:
        logger.exception(f"Bulk RMP lookup failed: {e}")
        raise HTTPException(status_code=500, detail="Bulk RMP lookup failed")
