"""
Elective recommendations via Claude AI

SEC-004 FIX: Replaced weak local _sanitize_field with shared sanitise module.
The old version lacked l33tspeak normalisation, unicode stripping, and had
fewer patterns — trivially bypassed with "1gn0re prev1ous" or zero-width chars.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import anthropic
import json
import re

from api.config import settings
from api.auth import get_current_user_id

# SEC-004 FIX: Use the shared, stronger sanitiser
from api.utils.sanitise import sanitise_user_message

router = APIRouter()

# ── Module-level singleton — created once, reused across all requests ─────────
_async_client: Optional[anthropic.AsyncAnthropic] = None


def _get_client() -> anthropic.AsyncAnthropic:
    global _async_client
    if _async_client is None:
        _async_client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _async_client


# SEC-004 FIX: Removed the local _INJECTION_PATTERNS and _sanitize_field().
# Now using sanitise_user_message() from the shared module which has:
#  - L33tspeak normalisation
#  - Unicode/zero-width character stripping
#  - 40+ patterns including French
#  - Consistent behaviour with chat.py


class ElectivesRequest(BaseModel):
    major:           Optional[str]       = Field(None, max_length=100)
    minor:           Optional[str]       = Field(None, max_length=100)
    concentration:   Optional[str]       = Field(None, max_length=100)
    year:            Optional[int]       = Field(None, ge=0, le=10)
    interests:       Optional[str]       = Field(None, max_length=500)
    # SEC-008 FIX: Added max_length per item (was only on the list)
    courses_taken:   Optional[List[str]] = Field(default_factory=list, max_length=200)
    exclude_courses: Optional[List[str]] = Field(default_factory=list, max_length=200)


@router.post("/recommend")
async def recommend_electives(
    req: ElectivesRequest,
    _: str = Depends(get_current_user_id),
):
    try:
        client = _get_client()

        # SEC-004 FIX: Use shared sanitiser for all user-controlled fields.
        # sanitise_user_message raises HTTP 400 on injection pattern match.
        def _safe(value: str, fallback: str = "Not set") -> str:
            if not value or not value.strip():
                return fallback
            sanitise_user_message(value)  # raises on injection match
            return value.strip()

        safe_major         = _safe(req.major or "", "Not set")
        safe_minor         = _safe(req.minor or "", "Not set")
        safe_concentration = _safe(req.concentration or "", "Not specified")
        safe_interests     = _safe(req.interests or "", "Not specified")

        # Sanitize and truncate individual course codes
        safe_courses_taken   = []
        for c in (req.courses_taken or []):
            sanitise_user_message(c)
            safe_courses_taken.append(c.strip()[:20])

        safe_exclude_courses = []
        for c in (req.exclude_courses or []):
            sanitise_user_message(c)
            safe_exclude_courses.append(c.strip()[:20])

        course_list  = ", ".join(safe_courses_taken)  if safe_courses_taken  else "None yet"
        exclude_str  = ", ".join(safe_exclude_courses) if safe_exclude_courses else "None"

        prompt = f"""You are an academic advisor at McGill University Faculty of Arts.

Student profile:
- Major: {safe_major}
- Minor: {safe_minor}
- Concentration: {safe_concentration}
- Year: {"U" + str(req.year) if req.year else "Not specified"}
- Interests: {safe_interests}
- Courses taken/taking: {course_list}

IMPORTANT — Do NOT recommend any of these required major/minor courses: {exclude_str}

Recommend exactly 8 ELECTIVE courses from McGill's course catalogue — courses outside the required program.
These should complement their interests, open new perspectives, or advance their career goals.
Mix of: breadth courses, upper-level courses in adjacent fields, interdisciplinary options.
Use real McGill course codes (COMP, MATH, PSYC, PHIL, ECON, HIST, POLI, SOCI, CLAS, LING, etc.)

Respond ONLY with valid JSON, no markdown, no explanation:
{{
  "theme": "one sentence about why these courses suit this student",
  "recommendations": [
    {{
      "subject": "COMP",
      "catalog": "396",
      "title": "Undergraduate Research Project",
      "credits": 3,
      "why": "one sentence why this suits this student specifically",
      "category": "one of: Breadth | Career | Advanced | Interdisciplinary | Interest"
    }}
  ]
}}"""

        message = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1200,
            messages=[{"role": "user", "content": prompt}]
        )

        raw = message.content[0].text.strip()
        raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
        raw = re.sub(r'\s*```\s*$', '', raw, flags=re.MULTILINE)
        parsed = json.loads(raw.strip())
        return {"success": True, "data": parsed}

    except HTTPException:
        raise
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to parse AI response. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")
