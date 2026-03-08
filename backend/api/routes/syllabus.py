"""
backend/api/routes/syllabus.py

Parse one or more McGill syllabus PDFs using Claude.
Extracts course metadata, schedule, assessments, and instructor info,
then populates calendar_events and enriches current_courses.

"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Request
from typing import List, Optional
import anthropic
import base64
import logging
import json
import re
from datetime import date, datetime, timedelta  # FIX #2: import timedelta directly

from difflib import SequenceMatcher

from ..utils.supabase_client import get_supabase, get_user_by_id
from ..exceptions import UserNotFoundException
from ..config import settings
from ..auth import get_current_user_id, require_self

# FIX F-07: PDF magic bytes
PDF_MAGIC = b'%PDF'
from ..exceptions import UserNotFoundException
from ..config import settings


# ── RMP helper ────────────────────────────────────────────────────────────────

def _lookup_rmp(supabase, instructor_name: str, course_code: str | None) -> dict | None:
    """
    Look up Rate My Professors data for `instructor_name` from the courses table.
    Returns a dict with rmp_* fields, or None if no match found.
    """
    if not instructor_name:
        return None

    try:
        parts     = instructor_name.strip().split()
        last_name = parts[-1] if parts else instructor_name

        # Build query — filter by subject prefix if course_code provided
        qb = (
            supabase.from_("courses")
            .select("instructor, rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again, rmp_url, Course")
            .ilike("instructor", f"%{last_name}%")
            .not_.is_("rmp_rating", "null")
        )
        if course_code:
            subject = course_code.split()[0].upper() if " " in course_code else course_code[:4].upper()
            qb = qb.like("Course", f"{subject}%")

        rows = qb.limit(100).execute().data or []

        if not rows and len(parts) > 1:
            # Fallback: search by first name
            qb2 = (
                supabase.from_("courses")
                .select("instructor, rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again, rmp_url, Course")
                .ilike("instructor", f"%{parts[0]}%")
                .not_.is_("rmp_rating", "null")
            )
            rows = qb2.limit(100).execute().data or []

        if not rows:
            return None

        # Fuzzy match
        target = instructor_name.lower()
        best_row  = None
        best_score = 0.0
        for row in rows:
            instr = (row.get("instructor") or "").lower()
            score = SequenceMatcher(None, target, instr).ratio()
            if score > best_score:
                best_score = score
                best_row   = row

        if best_score < 0.55 or best_row is None:
            return None

        return {
            "name":                    best_row.get("instructor"),
            "rmp_rating":              best_row.get("rmp_rating"),
            "rmp_difficulty":          best_row.get("rmp_difficulty"),
            "rmp_num_ratings":         best_row.get("rmp_num_ratings"),
            "rmp_would_take_again":    best_row.get("rmp_would_take_again"),
            "rmp_url":                 best_row.get("rmp_url"),
            "match_score":             round(best_score, 3),
        }

    except Exception as e:
        logger.warning(f"RMP lookup failed for '{instructor_name}': {e}")
        return None

router = APIRouter()
logger = logging.getLogger(__name__)

# FIX #9: Module-level AsyncAnthropic singleton — created once, reused across all requests.
_async_anthropic_client: anthropic.AsyncAnthropic | None = None


def _get_async_client() -> anthropic.AsyncAnthropic:
    global _async_anthropic_client
    if _async_anthropic_client is None:
        _async_anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _async_anthropic_client


# ── Extraction prompt ──────────────────────────────────────────────────────────

SYLLABUS_EXTRACTION_PROMPT = """You are parsing a McGill University course syllabus PDF.
Extract ALL available information and return a single JSON object with this exact structure.
If a field is not present in the syllabus, use null.

{
  "course_code": "COMP 251",
  "course_title": "Algorithms and Data Structures",
  "credits": 3,
  "term": "Winter",
  "year": 2026,
  "section": "001",
  "crn": "12345",
  "department": "School of Computer Science",
  "faculty": "Science",

  "instructor": {
    "name": "David Becerra",
    "email": "david.becerra@mcgill.ca",
    "office": "MC 123",
    "office_hours": [
      { "day": "Tuesday", "start_time": "14:00", "end_time": "15:00", "location": "MC 123" }
    ]
  },

  "tas": [
    { "name": "Jane Doe", "email": "jane.doe@mcgill.ca" }
  ],

  "course_email": "comp251.cs@mcgill.ca",

  "schedule": [
    {
      "day": "Tuesday",
      "start_time": "10:05",
      "end_time": "11:25",
      "location": "BURN 1B24",
      "type": "Lecture"
    },
    {
      "day": "Thursday",
      "start_time": "10:05",
      "end_time": "11:25",
      "location": "BURN 1B24",
      "type": "Lecture"
    }
  ],

  "assessments": [
    {
      "title": "Assignment 1",
      "type": "assignment",
      "weight": 7,
      "due_date": "2026-02-01",
      "description": "Data structures programming assignment"
    },
    {
      "title": "Midterm 1",
      "type": "midterm",
      "weight": 22,
      "date": "2026-02-10",
      "time": "18:00",
      "location": "ENGMC 204",
      "description": "Covers Data Structures"
    },
    {
      "title": "Final Exam",
      "type": "final",
      "weight": 33,
      "date": null,
      "description": "Graph Theory + all topics"
    }
  ],

  "textbooks": [
    { "title": "Introduction to Algorithms", "authors": "Cormen et al.", "edition": "3rd", "required": true }
  ],

  "prerequisites": ["COMP 250", "MATH 240"],
  "restrictions": ["Not open to students who have taken COMP 252"],

  "policies": {
    "late_penalty": "5% per day",
    "late_max_days": 7,
    "attendance": null,
    "technology": "Laptop allowed, no social media",
    "communication": "Use course email comp251.cs@mcgill.ca"
  },

  "description": "Brief 1-2 sentence course description.",
  "learning_outcomes": ["Analyze algorithm correctness", "Design efficient algorithms"],
  "course_url": null,
  "platform": "myCourses"
}

IMPORTANT RULES:
- For schedule entries, use 24-hour time format (HH:MM).
- For dates, use ISO format YYYY-MM-DD. If only a range is given (e.g. Feb 9-13), use the first date.
- If the syllabus lists multiple sections with different schedules, include ALL schedule entries.
- assessment "type" must be one of: assignment, quiz, midterm, final, project, lab, participation, other
- Return ONLY the JSON object, no markdown, no explanation.
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def _strip_json_fences(raw: str) -> str:
    raw = re.sub(r"^\s*```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$", "", raw, flags=re.MULTILINE)
    return raw.strip()


def normalize_course_code(code: str) -> str:
    """Ensure course code has a space between subject and number: 'COMP251' → 'COMP 251'."""
    code = code.strip().upper()
    code = re.sub(r"^([A-Z]{2,4})(\d)", r"\1 \2", code)
    code = re.sub(r"\s{2,}", " ", code)
    return code


# FIX #1: Declare as async and use AsyncAnthropic + await so the Claude API call
# doesn't block FastAPI's event loop during the ~5–15 second extraction.
# FIX #9: Use the module-level singleton client instead of creating one per call.
async def _extract_syllabus_data(pdf_bytes: bytes) -> dict:
    client = _get_async_client()
    b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    msg = await client.messages.create(  # FIX #1: await the async call
        model=settings.CLAUDE_MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": SYLLABUS_EXTRACTION_PROMPT,
                    },
                ],
            }
        ],
    )

    raw = msg.content[0].text
    raw = _strip_json_fences(raw)
    return json.loads(raw)


def _normalize_time(t: Optional[str]) -> Optional[str]:
    """Normalise any time string to 24-hour HH:MM format."""
    if not t:
        return None
    t = t.strip()
    # FIX #4: The original regex replaced am/pm with itself (no-op).
    # Correct fix: collapse any whitespace immediately before am/pm so that
    # "10:05 AM" becomes "10:05AM", which then matches the "%I:%M%p" strptime
    # format and gets converted to proper 24-hour "10:05" / "22:05" output.
    t = re.sub(r'\s+(am|pm)$', r'\1', t, flags=re.IGNORECASE)
    try:
        for fmt in ("%H:%M", "%I:%M %p", "%I:%M%p", "%I%p"):
            try:
                return datetime.strptime(t, fmt).strftime("%H:%M")
            except ValueError:
                continue
    except Exception:
        pass
    return t


def _day_abbrev(day: str) -> str:
    mapping = {
        "monday": "Mon", "tuesday": "Tue", "wednesday": "Wed",
        "thursday": "Thu", "friday": "Fri", "saturday": "Sat", "sunday": "Sun",
    }
    return mapping.get(day.lower(), day[:3].capitalize())


def _next_weekday_date(day_name: str, term: str, year: int) -> Optional[str]:
    """
    Return the ISO date string of the first upcoming occurrence of `day_name`
    within the given term's approximate start window.
    Winter: Jan 5, Summer: May 1, Fall: Sep 1

    FIX #2: Use the already-imported timedelta instead of __import__("datetime").
    FIX #3: If the computed date is already in the past (e.g. mid-semester upload),
            advance by one week so the calendar event lands in the future.
    """
    if not day_name:
        return None

    term_starts = {
        "winter": date(year, 1, 5),
        "summer": date(year, 5, 1),
        "fall":   date(year, 9, 1),
    }
    day_numbers = {
        "monday": 0, "tuesday": 1, "wednesday": 2,
        "thursday": 3, "friday": 4, "saturday": 5, "sunday": 6,
    }

    start = term_starts.get(term.lower(), date(year, 1, 5))
    target = day_numbers.get(day_name.lower())
    if target is None:
        return None

    days_ahead = (target - start.weekday()) % 7
    result_date = start + timedelta(days=days_ahead)  # FIX #2: direct timedelta

    # FIX #3: If the computed date is already past (mid-semester upload),
    # advance by one week so the anchor event appears in the future.
    today = date.today()
    if result_date < today:
        result_date += timedelta(weeks=1)

    return result_date.isoformat()


# ── Route ──────────────────────────────────────────────────────────────────────

@router.post("/parse/{user_id}")
async def parse_syllabuses(
    user_id: str,
    req: Request,
    current_user_id: str = Depends(get_current_user_id),
    files: List[UploadFile] = File(...),
    dry_run: str = Form(default="false"),
):
    # FIX F-03: Ownership check
    require_self(current_user_id, user_id)
    is_dry_run = dry_run.lower() in ("true", "1", "yes")

    try:
        get_user_by_id(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")

    if not files:
        raise HTTPException(status_code=422, detail="No files provided")

    MAX_SYLLABUS_FILES = 5
    if len(files) > MAX_SYLLABUS_FILES:
        raise HTTPException(
            status_code=422,
            detail=f"Too many files. Maximum {MAX_SYLLABUS_FILES} syllabuses per upload.",
        )

    supabase = get_supabase()
    all_results = []

    for upload in files:
        if not upload.filename.lower().endswith(".pdf"):
            all_results.append({
                "filename": upload.filename,
                "success": False,
                "error": "Only PDF files are accepted",
            })
            continue

        # F-06: Check Content-Length header before reading to avoid allocating
        # memory for oversized uploads (header is advisory, full read still authoritative).
        cl = upload.headers.get("content-length") if hasattr(upload, "headers") else None
        if cl:
            try:
                if int(cl) > 15 * 1024 * 1024:
                    all_results.append({
                        "filename": upload.filename,
                        "success": False,
                        "error": "File too large (max 15MB)",
                    })
                    continue
            except (ValueError, TypeError):
                pass  # malformed header — let the authoritative size check below decide

        pdf_bytes = await upload.read()
        if len(pdf_bytes) > 15 * 1024 * 1024:
            all_results.append({
                "filename": upload.filename,
                "success": False,
                "error": "File too large (max 15MB)",
            })
            continue

        # FIX F-07: Validate magic bytes before sending to Claude
        if len(pdf_bytes) < 4 or pdf_bytes[:4] != PDF_MAGIC:
            all_results.append({
                "filename": upload.filename,
                "success": False,
                "error": "File does not appear to be a valid PDF",
            })
            continue

        try:
            extracted = await _extract_syllabus_data(pdf_bytes)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON from Claude for {upload.filename}: {e}")
            all_results.append({
                "filename": upload.filename,
                "success": False,
                "error": "Failed to parse syllabus — Claude returned invalid data.",
            })
            continue
        except Exception as e:
            logger.exception(f"Extraction failed for {upload.filename}: {e}")
            all_results.append({
                "filename": upload.filename,
                "success": False,
                "error": "Extraction failed. Please try again.",
            })
            continue

        if is_dry_run:
            all_results.append({
                "filename": upload.filename,
                "success": True,
                "parsed": extracted,
                "saved": False,
            })
            continue

        # ── Persist ──────────────────────────────────────────────────────────
        result = {
            "filename": upload.filename,
            "success": True,
            "saved": True,
            "course_code": extracted.get("course_code"),
            "course_title": extracted.get("course_title"),
            "section": extracted.get("section"),
            "term": extracted.get("term"),
            "year": extracted.get("year"),
            "instructor_name": extracted.get("instructor", {}).get("name"),
            "instructor_email": extracted.get("instructor", {}).get("email"),
            "schedule": extracted.get("schedule") or [],
            "calendar_events_added": 0,
            "current_course_updated": False,
            "rmp_data": None,  # populated below after DB interaction
        }

        # FIX #6: Normalize the course code so "COMP251" → "COMP 251" before
        # any DB lookups. Without this, the current_courses update silently
        # finds 0 rows when Claude omits the space.
        raw_code = extracted.get("course_code") or ""
        course_code = normalize_course_code(raw_code) if raw_code else ""
        result["course_code"] = course_code or None

        course_title = extracted.get("course_title") or course_code
        term = extracted.get("term") or "Winter"
        year = extracted.get("year") or date.today().year
        instructor = extracted.get("instructor") or {}
        schedule_slots = extracted.get("schedule") or []
        assessments = extracted.get("assessments") or []

        # ── RMP lookup by professor name ──────────────────────────────────────
        instr_name = instructor.get("name")
        if instr_name:
            try:
                from difflib import SequenceMatcher
                import re as _re

                def _norm_name(n):
                    n = _re.sub(r'\b(dr|prof|professor|mr|mrs|ms)\b\.?', '', n or '', flags=_re.IGNORECASE)
                    return _re.sub(r'\s+', ' ', n).strip().lower()

                parts = instr_name.split()
                last_name = parts[-1] if parts else instr_name
                subject_hint = course_code.split()[0] if course_code and " " in course_code else None

                rmp_qb = supabase.from_("courses").select(
                    'instructor, rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again, rmp_url'
                ).ilike("instructor", f"%{last_name}%").not_.is_("rmp_rating", "null")
                if subject_hint:
                    rmp_qb = rmp_qb.like("Course", f"{subject_hint}%")
                rmp_rows = (rmp_qb.limit(100).execute().data) or []

                best_row, best_score = None, 0.0
                for rrow in rmp_rows:
                    if not rrow.get("rmp_rating"):
                        continue
                    score = SequenceMatcher(None, _norm_name(instr_name), _norm_name(rrow.get("instructor") or "")).ratio()
                    if score > best_score:
                        best_score, best_row = score, rrow

                if best_row and best_score >= 0.60:
                    result["rmp_data"] = {
                        "avg_rating":               best_row.get("rmp_rating"),
                        "avg_difficulty":           best_row.get("rmp_difficulty"),
                        "num_ratings":              int(best_row.get("rmp_num_ratings") or 0),
                        "would_take_again_percent": (
                            round(float(best_row["rmp_would_take_again"]))
                            if best_row.get("rmp_would_take_again") is not None else None
                        ),
                        "rmp_url": best_row.get("rmp_url"),
                        "match_score": round(best_score, 3),
                    }
            except Exception as rmp_err:
                logger.warning(f"RMP lookup failed for '{instr_name}': {rmp_err}")

        # ── 1. Enrich current_courses row ─────────────────────────────────────
        if course_code:
            try:
                if schedule_slots:
                    day_parts = []
                    seen: set = set()
                    for slot in schedule_slots:
                        d = _day_abbrev(slot.get("day", ""))
                        if d not in seen:
                            day_parts.append(d)
                            seen.add(d)
                    days_str = "/".join(day_parts)
                    first = schedule_slots[0]
                    time_str = f"{first.get('start_time', '')}–{first.get('end_time', '')}"
                    loc_str = first.get("location") or ""
                    schedule_str = f"{days_str} {time_str} {loc_str}".strip()
                else:
                    schedule_str = None

                updates: dict = {}
                if instructor.get("name"):
                    updates["professor"] = instructor["name"]
                if schedule_str:
                    updates["schedule"] = schedule_str
                if instructor.get("email"):
                    updates["professor_email"] = instructor["email"]
                if instructor.get("office"):
                    updates["professor_office"] = instructor["office"]
                if schedule_slots and schedule_slots[0].get("location"):
                    updates["room"] = schedule_slots[0]["location"]

                if updates:
                    res = supabase.table("current_courses") \
                        .update(updates) \
                        .eq("user_id", user_id) \
                        .eq("course_code", course_code) \
                        .execute()
                    if res.data:
                        result["current_course_updated"] = True
            except Exception as e:
                logger.warning(f"Could not update current_courses for {course_code}: {e}")

        # FIX #8: Delete existing syllabus-generated calendar events for this
        # course before inserting new ones. Prevents duplicates when a student
        # re-uploads the same (or updated) syllabus.
        if course_code:
            try:
                supabase.table("calendar_events") \
                    .delete() \
                    .eq("user_id", user_id) \
                    .eq("course_code", course_code) \
                    .eq("type", "academic") \
                    .execute()
            except Exception as e:
                logger.warning(f"Could not clear existing events for {course_code}: {e}")

        # FIX #5: Collect all rows to insert, then do one bulk INSERT per table
        # instead of an individual INSERT per event (was O(n) round-trips).
        calendar_rows: list[dict] = []

        # ── 2. Build recurring lecture slot rows ───────────────────────────────
        for slot in schedule_slots:
            day = slot.get("day", "")
            start_time = _normalize_time(slot.get("start_time"))
            end_time = _normalize_time(slot.get("end_time"))
            location = slot.get("location") or ""
            slot_type = slot.get("type") or "Lecture"
            slot_date = _next_weekday_date(day, term, year)
            if not slot_date:
                continue

            calendar_rows.append({
                "user_id": user_id,
                "title": f"{course_code} {slot_type}",
                "date": slot_date,
                "time": start_time,
                "end_time": end_time,
                "type": "academic",
                "category": course_code,
                "description": (
                    f"{course_title}\n"
                    f"Every {day} {start_time}–{end_time}\n"
                    f"Location: {location}\n"
                    f"Instructor: {instructor.get('name') or 'TBD'}"
                ),
                "location": location or None,
                "course_code": course_code,
                "recurrence": f"weekly_{day.lower()}",
                "notify_enabled": False,
                "notify_email": False,
                "notify_sms": False,
                "notify_email_addr": None,
                "notify_phone": None,
                "notify_same_day": False,
                "notify_1day": False,
                "notify_7days": False,
            })

        # ── 3. Build assessment rows ───────────────────────────────────────────
        for assessment in assessments:
            event_date = assessment.get("date") or assessment.get("due_date")
            if not event_date:
                continue  # skip undated finals — they'll be set later

            a_type = assessment.get("type", "other")
            a_title = assessment.get("title") or a_type.capitalize()
            a_time = _normalize_time(assessment.get("time"))
            a_location = assessment.get("location") or ""
            a_weight = assessment.get("weight")

            is_exam = a_type in ("midterm", "final", "quiz")
            weight_str = f" ({a_weight}%)" if a_weight else ""
            desc_parts = [f"{course_code} — {a_title}{weight_str}"]
            if assessment.get("description"):
                desc_parts.append(assessment["description"])
            if a_location:
                desc_parts.append(f"Location: {a_location}")

            calendar_rows.append({
                "user_id": user_id,
                "title": f"{course_code} — {a_title}",
                "date": event_date,
                "time": a_time,
                "type": "academic",
                "category": f"{course_code} · {'Exam' if is_exam else 'Assignment'}",
                "description": "\n".join(desc_parts),
                "location": a_location or None,
                "course_code": course_code,
                "notify_enabled": is_exam,
                "notify_email": is_exam,
                "notify_sms": False,
                "notify_email_addr": None,
                "notify_phone": None,
                "notify_same_day": False,
                "notify_1day": is_exam,
                "notify_7days": is_exam,
            })

        # ── 4. Build office hours rows ─────────────────────────────────────────
        # Office hours use type="personal" so they are NOT wiped by the academic
        # dedup delete above and are tracked separately.
        oh_rows: list[dict] = []
        for oh in (instructor.get("office_hours") or []):
            oh_date = _next_weekday_date(oh.get("day", ""), term, year)
            if not oh_date:
                continue
            oh_rows.append({
                "user_id": user_id,
                "title": f"{course_code} Office Hours — {instructor.get('name') or 'Instructor'}",
                "date": oh_date,
                "time": _normalize_time(oh.get("start_time")),
                "end_time": _normalize_time(oh.get("end_time")),
                "type": "personal",
                "category": course_code,
                "description": (
                    f"Office hours for {course_code}\n"
                    f"Instructor: {instructor.get('name') or 'TBD'}\n"
                    f"Location: {oh.get('location') or instructor.get('office') or 'TBD'}\n"
                    f"Every {oh.get('day')} {oh.get('start_time')}–{oh.get('end_time')}"
                ),
                "location": oh.get("location") or instructor.get("office") or None,
                "course_code": course_code,
                "recurrence": f"weekly_{oh.get('day', '').lower()}",
                "notify_enabled": False,
                "notify_email": False,
                "notify_sms": False,
                "notify_email_addr": None,
                "notify_phone": None,
                "notify_same_day": False,
                "notify_1day": False,
                "notify_7days": False,
            })

        # FIX #5: Single bulk INSERT for academic events, another for office hours.
        if calendar_rows:
            try:
                supabase.table("calendar_events").insert(calendar_rows).execute()
                result["calendar_events_added"] += len(calendar_rows)
            except Exception as e:
                logger.warning(f"Bulk insert of academic events failed for {course_code}: {e}")
                # Row-by-row fallback so partial success is still possible
                for row in calendar_rows:
                    try:
                        supabase.table("calendar_events").insert(row).execute()
                        result["calendar_events_added"] += 1
                    except Exception as row_err:
                        logger.warning(f"Could not save event '{row.get('title')}': {row_err}")

        if oh_rows:
            try:
                supabase.table("calendar_events").insert(oh_rows).execute()
                result["calendar_events_added"] += len(oh_rows)
            except Exception as e:
                logger.warning(f"Bulk insert of office hours failed for {course_code}: {e}")
                for row in oh_rows:
                    try:
                        supabase.table("calendar_events").insert(row).execute()
                        result["calendar_events_added"] += 1
                    except Exception as row_err:
                        logger.warning(f"Could not save office hours row: {row_err}")

        logger.info(
            f"Syllabus import for user {user_id}, course {course_code}: "
            f"{result['calendar_events_added']} events added, "
            f"current_course_updated={result['current_course_updated']}"
        )

        # ── 5. Lookup RMP data for extracted professor ─────────────────────────
        if instructor.get("name") and course_code:
            try:
                # Extract subject from course_code (e.g. "COMP 251" → "COMP")
                subj_match = re.match(r'^([A-Z]{2,6})', course_code.replace(' ', ''))
                subject_code = subj_match.group(1) if subj_match else None

                # Query courses table for this instructor
                last_name = instructor["name"].split()[-1] if instructor["name"].split() else instructor["name"]
                rmp_query = (
                    supabase.from_("courses")
                    .select("instructor, rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again, rmp_url")
                    .ilike("instructor", f"%{last_name}%")
                    .not_.is_("rmp_rating", "null")
                )
                if subject_code:
                    rmp_query = rmp_query.like("Course", f"{subject_code}%")
                rmp_query = rmp_query.limit(20)
                rmp_rows = rmp_query.execute().data or []

                # Find best match
                if rmp_rows:
                    instr_norm = instructor["name"].lower()
                    best_row = None
                    best_score = 0.0
                    for row in rmp_rows:
                        row_instr = (row.get("instructor") or "").lower()
                        # Compute rough similarity: check if all parts of last_name appear
                        if last_name.lower() in row_instr:
                            # Simple token overlap score
                            parts_match = sum(
                                1 for p in instr_norm.split()
                                if p in row_instr
                            )
                            score = parts_match / max(len(instr_norm.split()), 1)
                            if score > best_score and row.get("rmp_rating", 0):
                                best_score = score
                                best_row = row

                    if best_row and best_score >= 0.4:
                        rmp_would_take = best_row.get("rmp_would_take_again")
                        result["rmp_data"] = {
                            "instructor_name": best_row.get("instructor"),
                            "avg_rating": best_row.get("rmp_rating"),
                            "avg_difficulty": best_row.get("rmp_difficulty"),
                            "num_ratings": int(best_row.get("rmp_num_ratings") or 0),
                            "would_take_again_percent": (
                                round(float(rmp_would_take)) if rmp_would_take is not None else None
                            ),
                            "rmp_url": best_row.get("rmp_url"),
                            "match_score": round(best_score, 2),
                        }
            except Exception as rmp_err:
                logger.warning(f"RMP lookup failed for {instructor.get('name')}: {rmp_err}")

        all_results.append(result)

    return {
        "results": all_results,
        "total_files": len(files),
        "total_events_added": sum(r.get("calendar_events_added", 0) for r in all_results if r.get("success")),
        "total_courses_updated": sum(1 for r in all_results if r.get("current_course_updated")),
    }
