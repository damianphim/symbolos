"""
backend/api/routes/transcript.py
Parse a McGill unofficial transcript PDF using Claude,
then bulk-import completed + current courses and update the user profile.
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Request
from typing import Optional
import anthropic
import asyncio
import base64
import logging
import re
import json

from ..utils.supabase_client import get_supabase, get_user_by_id, update_user
from ..exceptions import UserNotFoundException
from ..config import settings
from ..auth import get_current_user_id, require_self

# FIX F-07: PDF magic bytes — must appear at offset 0
PDF_MAGIC = b'%PDF'

router = APIRouter()
logger = logging.getLogger(__name__)

# ── Singleton async client (created once, reused across all requests) ─────────
_async_anthropic_client: Optional[anthropic.AsyncAnthropic] = None


def _get_async_client() -> anthropic.AsyncAnthropic:
    global _async_anthropic_client
    if _async_anthropic_client is None:
        _async_anthropic_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _async_anthropic_client


# ── Constants ─────────────────────────────────────────────────────────────────

VALID_TERMS = {"fall", "winter", "summer"}

VALID_GRADES = {
    "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F",
    "P", "S", "U",
    "W", "L", "EX", "IP", "CO", "HH", "K",
}

COURSE_CODE_PATTERN = re.compile(
    r"^[A-Z]{3,4}\s\d{3}([A-Z]\d?)?$",
    re.IGNORECASE,
)

# Retries for transient Anthropic API errors (e.g. 500 Internal Server Error)
_ANTHROPIC_MAX_RETRIES = 2
_ANTHROPIC_RETRY_BACKOFF = 1.5  # seconds; doubles each attempt


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize_course_code(code: str) -> str:
    code = code.strip().upper()
    code = re.sub(r"^([A-Z]{2,4})(\d)", r"\1 \2", code)
    code = re.sub(r"\s{2,}", " ", code)
    return code


# ── Extraction prompt ─────────────────────────────────────────────────────────

EXTRACTION_PROMPT = """You are parsing a McGill University unofficial transcript PDF.
Your job is to carefully read every section and return a single JSON object.
== STEP 1: Read the program header at the top of the transcript ==
Extract student_info fields:
  - major: the text after "Major Concentration" (e.g. "Computer Science")
  - minor: the text after "Minor Concentration" (e.g. "Science for Arts Students")
  - faculty: the degree name (e.g. "Arts", "Science", "Engineering")
  - year: the Year number shown (e.g. "Year 1" -> 1, "Year 2" -> 2) as an integer
  - cum_gpa: the CUMULATIVE GPA on the final summary line labelled "CUM GPA"
  - advanced_standing: ALL courses listed under "Credits/Exemptions" or
    "Advanced Placement Exams" — these are AP/IB/transfer credits. Capture every one.
== STEP 2: Completed courses ==
Include ANY course row that has a final grade — including:
  - Standard letter grades: A, A-, B+, B, B-, C+, C, C-, D, F
  - Pass/fail grades: P (Pass), S (Satisfactory), U (Unsatisfactory)
  - Administrative grades: W (Withdrew), L (Deferred), EX (Exempt), IP (In Progress),
    CO (Complete), HH (High Honour), K (Incomplete)
Pass/fail courses (P, S, U) DO count toward credit requirements even though they
don't affect GPA — include them. Do NOT include courses from Credits/Exemptions here.
== STEP 3: Current / in-progress courses ==
These are courses prefixed "RW" (registered or waitlisted) with NO grade yet.
IMPORTANT — multi-term courses:
  McGill uses suffixes like D1/D2 or J1/J2 for year-long courses split across two terms.
  If FRSL 207D1 appears in Fall with RW and no grade, it is STILL IN PROGRESS even though
  Winter shows FRSL 207D2 also with RW. Include BOTH D1 and D2 in current_courses.
  Always include every RW course from every term that has no grade.
Return ONLY this JSON — no markdown, no explanation:
{
  "student_info": {
    "major": "Computer Science",
    "minor": "Science for Arts Students",
    "faculty": "Arts",
    "year": 2,
    "cum_gpa": 3.39,
    "advanced_standing": [
      {"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3}
    ]
  },
  "completed_courses": [
    {
      "course_code": "COMP 206",
      "course_title": "Intro to Software Systems",
      "subject": "COMP",
      "catalog": "206",
      "term": "Fall",
      "year": 2024,
      "grade": "B-",
      "credits": 3
    }
  ],
  "current_courses": [
    {
      "course_code": "COMP 251",
      "course_title": "Algorithms and Data Structures",
      "subject": "COMP",
      "catalog": "251",
      "credits": 3
    }
  ]
}
Additional rules:
  - term must be exactly "Fall", "Winter", or "Summer"
  - year is the 4-digit calendar year the term occurred (e.g. 2024)
  - credits: use the numeric value on the transcript (typically 3 or 4)
  - catalog for multi-term courses includes the full suffix: "207D1", "207D2"
  - If a field is unknown, use null"""


# ── Claude extraction (with retry on transient 500s) ─────────────────────────

async def extract_transcript_data(pdf_bytes: bytes) -> dict:
    client = _get_async_client()
    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    last_exc: Exception = RuntimeError("unreachable")
    for attempt in range(_ANTHROPIC_MAX_RETRIES + 1):
        try:
            message = await client.messages.create(
                model=settings.CLAUDE_MODEL,
                max_tokens=4000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_b64,
                                },
                            },
                            {"type": "text", "text": EXTRACTION_PROMPT},
                        ],
                    }
                ],
            )
            break  # success — exit retry loop
        except anthropic.InternalServerError as e:
            last_exc = e
            if attempt < _ANTHROPIC_MAX_RETRIES:
                wait = _ANTHROPIC_RETRY_BACKOFF * (2 ** attempt)
                logger.warning(
                    f"Anthropic 500 on attempt {attempt + 1}, retrying in {wait:.1f}s … "
                    f"(request_id={getattr(e, 'request_id', 'unknown')})"
                )
                await asyncio.sleep(wait)
            else:
                logger.error(f"Anthropic 500 after {_ANTHROPIC_MAX_RETRIES + 1} attempts: {e}")
                raise
        except (anthropic.APIConnectionError, anthropic.APITimeoutError) as e:
            last_exc = e
            if attempt < _ANTHROPIC_MAX_RETRIES:
                wait = _ANTHROPIC_RETRY_BACKOFF * (2 ** attempt)
                logger.warning(f"Anthropic connection error on attempt {attempt + 1}, retrying in {wait:.1f}s … ({e})")
                await asyncio.sleep(wait)
            else:
                raise

    raw = message.content[0].text.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
    raw = re.sub(r"\s*```\s*$", "", raw, flags=re.MULTILINE)
    return json.loads(raw.strip())


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/parse/{user_id}")
async def parse_transcript(
    user_id: str,
    req: Request,
    current_user_id: str = Depends(get_current_user_id),
    file: UploadFile = File(...),
    dry_run: str = Form(default="false"),
):
    # FIX F-03: Ownership check
    require_self(current_user_id, user_id)
    is_dry_run = dry_run.lower() in ("true", "1", "yes")

    try:
        get_user_by_id(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")

    # FIX F-07: Reject non-.pdf filenames
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF files are accepted")

    # SEC-07: Reject oversized uploads before reading the full file into memory.
    # Content-Length is set by legitimate clients; large files without it are
    # also blocked once we read them below.
    MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    content_length = req.headers.get("content-length")
    if content_length and int(content_length) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="File too large (max 10MB)")

    pdf_bytes = await file.read()
    if len(pdf_bytes) > MAX_BYTES:
        raise HTTPException(status_code=422, detail="File too large (max 10MB)")

    # FIX F-07: Validate PDF magic bytes — reject any file disguised as a PDF
    if len(pdf_bytes) < 4 or pdf_bytes[:4] != PDF_MAGIC:
        raise HTTPException(status_code=422, detail="File does not appear to be a valid PDF")

    # SEC-025: Structural PDF validation — verify the file has a valid PDF trailer.
    # Magic bytes alone can be faked; a real PDF must contain a %%EOF marker and
    # at least one xref or startxref reference.
    tail = pdf_bytes[-1024:] if len(pdf_bytes) > 1024 else pdf_bytes
    if b"%%EOF" not in tail:
        raise HTTPException(status_code=422, detail="File does not appear to be a valid PDF")
    if b"startxref" not in tail and b"xref" not in pdf_bytes:
        raise HTTPException(status_code=422, detail="File does not appear to be a valid PDF")

    try:
        extracted = await extract_transcript_data(pdf_bytes)
    except json.JSONDecodeError as e:
        logger.error(f"Claude returned invalid JSON: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse transcript — Claude returned invalid data. Please try again.")
    except Exception as e:
        logger.exception(f"Transcript extraction failed: {e}")
        raise HTTPException(status_code=500, detail="Transcript extraction failed. Please try again.")

    # Normalize course codes
    for course in extracted.get("completed_courses", []):
        if course.get("course_code"):
            course["course_code"] = normalize_course_code(course["course_code"])
    for course in extracted.get("current_courses", []):
        if course.get("course_code"):
            course["course_code"] = normalize_course_code(course["course_code"])
    for course in (extracted.get("student_info") or {}).get("advanced_standing", []):
        if course.get("course_code"):
            course["course_code"] = normalize_course_code(course["course_code"])

    if is_dry_run:
        return {"parsed": extracted, "saved": False}

    # ── Persist ───────────────────────────────────────────────────────────────
    supabase = get_supabase()
    results = {
        "completed_added": 0,
        "completed_skipped": 0,
        "current_added": 0,
        "current_skipped": 0,
        "profile_updated": False,
    }

    # 1. Completed courses
    for course in extracted.get("completed_courses", []) or []:
        try:
            term = (course.get("term") or "").strip()
            if term.lower() not in VALID_TERMS:
                results["completed_skipped"] += 1
                continue

            grade = (course.get("grade") or "").strip().upper()
            if grade and grade not in VALID_GRADES:
                grade = None

            existing = supabase.table("completed_courses") \
                .select("id") \
                .eq("user_id", user_id) \
                .eq("course_code", course["course_code"]) \
                .execute()
            if existing.data:
                results["completed_skipped"] += 1
                continue

            row = {
                "user_id": user_id,
                "course_code": course["course_code"],
                "course_title": course.get("course_title"),
                "subject": course.get("subject", course["course_code"].split()[0]),
                "catalog": course.get("catalog", course["course_code"].split()[-1]),
                "term": term.capitalize(),
                "year": course.get("year"),
                "grade": grade or None,
                "credits": course.get("credits", 3),
            }
            supabase.table("completed_courses").insert(row).execute()
            results["completed_added"] += 1
        except Exception as e:
            logger.warning(f"Skipping completed course {course.get('course_code')}: {e}")
            results["completed_skipped"] += 1

    # 2. Current courses
    for course in extracted.get("current_courses", []) or []:
        try:
            existing = supabase.table("current_courses") \
                .select("id") \
                .eq("user_id", user_id) \
                .eq("course_code", course["course_code"]) \
                .execute()
            if existing.data:
                results["current_skipped"] += 1
                continue

            row = {
                "user_id": user_id,
                "course_code": course["course_code"],
                "course_title": course.get("course_title"),
                "subject": course.get("subject", course["course_code"].split()[0]),
                "catalog": course.get("catalog", course["course_code"].split()[-1]),
                "credits": course.get("credits", 3),
            }
            supabase.table("current_courses").insert(row).execute()
            results["current_added"] += 1
        except Exception as e:
            logger.warning(f"Skipping current course {course.get('course_code')}: {e}")
            results["current_skipped"] += 1

    # 3. Update user profile from student_info
    # SEC-022: Validate and bound Claude-extracted values before writing to DB.
    # This path bypasses the UserUpdate Pydantic model, so we must manually
    # enforce the same constraints here.
    student_info = extracted.get("student_info") or {}
    profile_updates = {}

    _str_field = lambda v, maxlen=100: str(v).strip()[:maxlen] if v else None
    if student_info.get("major"):
        profile_updates["major"] = _str_field(student_info["major"], 100)
    if student_info.get("minor"):
        profile_updates["minor"] = _str_field(student_info["minor"], 100)
    if student_info.get("faculty"):
        profile_updates["faculty"] = _str_field(student_info["faculty"], 100)
    if student_info.get("year"):
        try:
            year_val = int(student_info["year"])
            if 0 <= year_val <= 10:
                profile_updates["year"] = year_val
        except (ValueError, TypeError):
            pass  # skip invalid year from Claude
    if student_info.get("cum_gpa") is not None:
        try:
            gpa_val = float(student_info["cum_gpa"])
            if 0.0 <= gpa_val <= 4.0:
                profile_updates["current_gpa"] = round(gpa_val, 2)
        except (ValueError, TypeError):
            pass  # skip invalid GPA from Claude
    if student_info.get("advanced_standing"):
        # Validate each item has the expected shape and bounded values
        raw_standing = student_info["advanced_standing"]
        if isinstance(raw_standing, list):
            validated = []
            for item in raw_standing[:50]:  # cap at 50 items
                if isinstance(item, dict) and item.get("course_code"):
                    validated.append({
                        "course_code": str(item["course_code"]).strip()[:20],
                        "course_title": str(item.get("course_title", "")).strip()[:200],
                        "credits": min(max(float(item.get("credits", 3)), 0), 20),
                    })
            if validated:
                profile_updates["advanced_standing"] = validated

    if profile_updates:
        try:
            update_user(user_id, profile_updates)
            results["profile_updated"] = True
        except Exception as e:
            logger.warning(f"Profile update failed for {user_id}: {e}")

    logger.info(
        f"Transcript import complete for {user_id}: "
        f"+{results['completed_added']} completed, "
        f"+{results['current_added']} current, "
        f"profile_updated={results['profile_updated']}"
    )
    return {"results": results, "saved": True}
