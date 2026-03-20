"""
backend/api/routes/courses.py

EGRESS FIX (v2):

  Problem 1 — /subjects pulled 10,000 rows to extract ~150 prefixes in Python.
  Fix: query the `unique_subjects` Postgres VIEW instead (see
       sql/fix_egress_1_unique_subjects_view.sql).  ~150 tiny strings over
       the network instead of 10,000 rows.

  Problem 2 — /search fetched limit*20 raw section rows (up to 2,000) and
  collapsed them with _group_sections() in Python.
  Fix: call the `search_courses` Postgres RPC instead (see
       sql/fix_egress_2_search_courses_rpc.sql).  Postgres does the GROUP BY
       + AVG and returns exactly `limit` pre-aggregated rows.

  Problem 3 — In-memory SimpleCache is wiped on every Vercel cold start, so
  each new instance re-downloads the full datasets.
  Mitigation: the two SQL fixes above make cold-start fetches cheap (tiny
  payloads).  For a full fix, replace SimpleCache with an external store such
  as Upstash Redis (one line change in cache.py).

KEY REMINDER: Route order matters in FastAPI. /search and /subjects MUST be
declared before /{subject}/{catalog}, otherwise FastAPI matches "search" and
"subjects" as the {subject} path parameter and returns 404.
"""

from fastapi import APIRouter, HTTPException, Query, status, Depends, Request
from typing import Optional
import logging
import re

from ..config import settings
from ..utils.supabase_client import get_supabase
from ..exceptions import DatabaseException
from ..utils.cache import search_cache, subjects_cache
from ..auth import get_current_user_id

router = APIRouter()
logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────

_SUBJECTS_CACHE_KEY = "all_subjects"


# ── Helpers ────────────────────────────────────────────────────────────────────

def parse_course_code(course_code: str):
    """Parse 'COMP202' → ('COMP', '202').  Returns (None, None) on failure."""
    if not course_code:
        return None, None
    match = re.match(r'^([A-Z]+)(\d+[A-Z]?)$', course_code.upper())
    if match:
        return match.group(1), match.group(2)
    return None, None


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES — specific paths must come before wildcard /{subject}/{catalog}
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/search", response_model=dict)
async def search(
    query: Optional[str] = Query(None, min_length=1, max_length=100),
    subject: Optional[str] = Query(None, min_length=2, max_length=6),
    limit: int = Query(
        default=settings.DEFAULT_SEARCH_LIMIT,
        ge=1,
        le=settings.MAX_SEARCH_LIMIT,
    ),
    include_ratings: bool = Query(default=True),
    _: str = Depends(get_current_user_id),
):
    """
    Course search via the `search_courses` Postgres RPC.

    Intentionally public (no auth required) — the course catalogue is read-only
    public data. IP-based rate limiting is enforced by the global rate_limit_middleware
    in main.py (RATE_LIMIT_PER_MINUTE, default 100 req/min/IP).

    All grouping, averaging, and filtering now happen inside Postgres.
    The network payload is exactly `limit` pre-aggregated rows regardless
    of how many raw sections exist in the database.
    """
    try:
        supabase = get_supabase()
        clean_query   = query.strip()          if query   else None
        clean_subject = subject.strip().upper() if subject else None

        # Nothing to search
        if not clean_query and not clean_subject:
            return {"courses": [], "count": 0, "query": None, "subject": None,
                    "includes_ratings": True}

        cache_key = f"search:{clean_subject}:{clean_query}:{limit}"
        cached = search_cache.get(cache_key)
        if cached is not None:
            logger.debug(f"Cache hit: {cache_key}")
            return cached

        # ── Call the search_courses RPC ────────────────────────────────────────
        response = supabase.rpc(
            "search_courses",
            {
                "p_query":   clean_query,
                "p_subject": clean_subject,
                "p_limit":   limit,
            },
        ).execute()

        rows = response.data or []

        # Map RPC rows → response shape expected by the frontend
        result_courses = []
        for row in rows:
            course_obj = {
                "subject":      row.get("subject"),
                "catalog":      row.get("catalog"),
                "title":        row.get("title"),
                "average":      row.get("recent_average"),
                "average_year": row.get("recent_year"),
                "instructor":   row.get("instructor"),
                "num_sections": row.get("num_sections"),
            }
            if include_ratings:
                if row.get("rmp_rating"):
                    course_obj.update({
                        "rmp_rating":           row.get("rmp_rating"),
                        "rmp_difficulty":       row.get("rmp_difficulty"),
                        "rmp_num_ratings":      row.get("rmp_num_ratings"),
                        "rmp_would_take_again": row.get("rmp_would_take_again"),
                    })
                if row.get("mc_rating"):
                    course_obj["mc_rating"]      = row.get("mc_rating")
                    course_obj["mc_num_ratings"] = row.get("mc_num_ratings")
                if row.get("blended_rating"):
                    course_obj["blended_rating"] = row.get("blended_rating")
            result_courses.append(course_obj)

        logger.info(
            f"Course search (RPC): query='{clean_query}', "
            f"subject='{clean_subject}', results={len(result_courses)}"
        )

        result = {
            "courses":          result_courses,
            "count":            len(result_courses),
            "query":            clean_query,
            "subject":          clean_subject,
            "includes_ratings": include_ratings,
        }
        search_cache.set(cache_key, result, ttl=300)
        return result

    except DatabaseException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error in course search: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while searching courses",
        )


@router.get("/subjects", response_model=dict)
async def get_subjects(_: str = Depends(get_current_user_id)):
    """
    Return all unique subject codes via the `unique_subjects` Postgres VIEW.
    Cached in memory for 1 hour.

    Intentionally public — subject codes are read-only catalogue metadata.
    IP-based rate limiting applies via the global middleware in main.py.
    MUST be declared before /{subject}/{catalog} to avoid route shadowing.
    """
    cached = subjects_cache.get(_SUBJECTS_CACHE_KEY)
    if cached is not None:
        logger.debug("Returning cached subjects list")
        return cached

    try:
        supabase = get_supabase()
        response = supabase.from_("unique_subjects").select("subject").execute()
        subjects = sorted(
            row["subject"] for row in (response.data or []) if row.get("subject")
        )
        result = {"subjects": subjects, "count": len(subjects)}
        subjects_cache.set(_SUBJECTS_CACHE_KEY, result)
        logger.info(f"Retrieved and cached {len(subjects)} unique subjects")
        return result

    except DatabaseException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error getting subjects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving subjects",
        )


@router.get("/{subject}/{catalog}", response_model=dict)
async def get_course_details(
    subject: str,
    catalog: str,
    include_ratings: bool = Query(default=True),
    _: str = Depends(get_current_user_id),
):
    """
    Detailed info for a specific course — grade history, RMP + MC data, schedule.
    Uses the get_course_details RPC to return 1 aggregated row instead of
    fetching every historical section row (75+ rows for popular courses).
    MUST be declared after /search and /subjects.
    """
    try:
        supabase = get_supabase()

        if not subject or len(subject) < 2 or len(subject) > 6:
            raise HTTPException(status_code=400, detail="Invalid subject code")
        if not catalog or len(catalog) < 1 or len(catalog) > 10:
            raise HTTPException(status_code=400, detail="Invalid catalog number")

        clean_subject = subject.strip().upper()
        clean_catalog = catalog.strip()
        course_code   = f"{clean_subject}{clean_catalog}"

        # ── Single aggregated row from Postgres RPC ────────────────────────
        rpc_resp = supabase.rpc(
            "get_course_details", {"p_course_code": course_code}
        ).execute()

        data = rpc_resp.data or []
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Course {clean_subject} {clean_catalog} not found",
            )
        row = data[0]

        course_obj = {
            "subject":         clean_subject,
            "catalog":         clean_catalog,
            "title":           row.get("course_name") or "",
            "description":     row.get("description") or None,
            "credits":         row.get("credits") or None,
            "average":         row.get("recent_avg"),
            "overall_average": row.get("overall_avg"),
            "grade_trend":     row.get("grade_trend") or [],
            "instructors":     row.get("instructors") or [],
            "num_sections":    len(row.get("instructors") or []),
            "prerequisites":   row.get("prerequisites") or None,
            "corequisites":    row.get("corequisites") or None,
            "restrictions":    row.get("restrictions") or None,
        }

        if include_ratings:
            if row.get("rmp_rating"):
                course_obj.update({
                    "rmp_rating":           row.get("rmp_rating"),
                    "rmp_difficulty":       row.get("rmp_difficulty"),
                    "rmp_num_ratings":      row.get("rmp_num_ratings"),
                    "rmp_would_take_again": row.get("rmp_would_take_again"),
                })
            if row.get("mc_rating"):
                course_obj["mc_rating"]      = row.get("mc_rating")
                course_obj["mc_num_ratings"] = row.get("mc_num_ratings")
            if row.get("blended_rating"):
                course_obj["blended_rating"] = row.get("blended_rating")

        # ── Fetch schedule from mcgill_sections ────────────────────────────
        # mcgill_sections stores course_code with a space: "COMP 202"
        try:
            course_code_spaced = f"{clean_subject} {clean_catalog}"
            sched_resp = (
                supabase.from_("mcgill_sections")
                .select("crn, term, section_type, instructor, days, times, location")
                .eq("course_code", course_code_spaced)
                .order("term", desc=True)
                .execute()
            )
            schedule = sched_resp.data or []
            if schedule:
                course_obj["schedule"] = schedule
        except Exception as e:
            logger.warning(f"Failed to fetch schedule for {course_code}: {e}")

        return {"course": course_obj}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error getting course details for {subject}/{catalog}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving course details",
        )