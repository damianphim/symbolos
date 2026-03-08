"""
Elective recommendations via Claude AI
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import json
import re

from api.config import settings

router = APIRouter()


class ElectivesRequest(BaseModel):
    major: Optional[str] = None
    minor: Optional[str] = None
    concentration: Optional[str] = None
    year: Optional[int] = None
    interests: Optional[str] = None
    courses_taken: Optional[List[str]] = []
    exclude_courses: Optional[List[str]] = []


@router.post("/recommend")
async def recommend_electives(req: ElectivesRequest):
    try:
        # FIX: Use AsyncAnthropic to avoid blocking the event loop
        client = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)

        course_list = ", ".join(req.courses_taken) if req.courses_taken else "None yet"

        exclude_str = ", ".join(req.exclude_courses) if req.exclude_courses else "None"
        prompt = f"""You are an academic advisor at McGill University Faculty of Arts.

Student profile:
- Major: {req.major or 'Not set'}
- Minor: {req.minor or 'Not set'}
- Concentration: {req.concentration or 'Not specified'}
- Year: {"U" + str(req.year) if req.year else "Not specified"}
- Interests: {req.interests or 'Not specified'}
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

        # FIX: Use await with the async client
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

    except json.JSONDecodeError as e:
        raise HTTPException(status_code=500, detail="Failed to parse AI response. Please try again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")
