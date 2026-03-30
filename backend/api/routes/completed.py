"""
backend/api/routes/completed.py

"""
from fastapi import APIRouter, HTTPException, Query, status, Depends, Request
from typing import Optional, List
from pydantic import BaseModel, Field
import logging
import re
from datetime import datetime

from ..config import settings
from ..utils.supabase_client import get_supabase, get_user_by_id
from ..exceptions import DatabaseException, UserNotFoundException
from ..auth import get_current_user_id, require_self, get_user_db

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Named constants ────────────────────────────────────────────
VALID_TERMS = {"fall", "winter", "summer"}
VALID_GRADES = {
    # Standard letter grades
    "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F",
    # Pass/fail and satisfactory
    "P", "S", "U",
    # Administrative
    "W",   # Withdrew
    "L",   # Deferred
    "EX",  # Exemption/Exempt
    "IP",  # In Progress
    "CO",  # Complete
    "HH",  # High Honour
    "K",   # Incomplete
}
COURSE_CODE_PATTERN = re.compile(r"^[A-Z]{3,4}\s?\d{3}[A-Z]?\d?$", re.IGNORECASE)


def normalize_course_code(code: str) -> str:
    """Normalize course code to 'SUBJ NNN' format with single space."""
    code = code.strip().upper()
    # Insert space between letters and digits if missing: "COMP206" → "COMP 206"
    code = re.sub(r"([A-Z])(\d)", r"\1 \2", code)
    # Collapse multiple spaces
    code = re.sub(r"\s+", " ", code)
    return code


class CompletedCourse(BaseModel):
    """Completed course schema"""
    course_code: str = Field(..., min_length=1, max_length=20)
    course_title: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=2, max_length=4)
    catalog: str = Field(..., min_length=1, max_length=10)
    term: str = Field(..., min_length=1, max_length=20)
    year: int = Field(..., ge=2000, le=2100)
    grade: Optional[str] = Field(None, max_length=10)
    credits: int = Field(default=3, ge=0, le=12)


class CompletedCourseUpdate(BaseModel):
    """Update schema for completed course"""
    term: Optional[str] = Field(None, min_length=1, max_length=20)
    year: Optional[int] = Field(None, ge=2000, le=2100)
    grade: Optional[str] = Field(None, max_length=10)
    credits: Optional[int] = Field(None, ge=0, le=12)


# ── Validation helpers ──────────────────────────────────────────
def _validate_user_exists(user_id: str) -> None:
    """Raise 404 if user_id doesn't map to a real user."""
    try:
        get_user_by_id(user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found",
        )


def _validate_course_data(course: CompletedCourse) -> CompletedCourse:
    """Normalize and validate course fields beyond Pydantic basics."""
    # Normalize course_code
    course.course_code = normalize_course_code(course.course_code)

    # Validate term
    if course.term.lower() not in VALID_TERMS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid term '{course.term}'. Must be one of: Fall, Winter, Summer",
        )

    # Validate grade if provided
    if course.grade and course.grade.upper() not in VALID_GRADES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid grade '{course.grade}'. Must be one of: {', '.join(sorted(VALID_GRADES))}",
        )

    # Validate course_code format
    if not COURSE_CODE_PATTERN.match(course.course_code):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid course code format: '{course.course_code}'",
        )

    return course


async def _check_duplicate(user_id: str, course_code: str, user_sb) -> bool:
    """Return True if the user already has this course marked complete."""
    try:
        response = (
            user_sb.table("completed_courses")
            .select("id")
            .eq("user_id", user_id)
            .eq("course_code", course_code)
            .execute()
        )
        return bool(response.data)
    except Exception:
        return False


@router.get("/{user_id}", response_model=dict)
async def get_completed_courses(
    user_id: str,
    req: Request,
    current_user_id: str = Depends(get_current_user_id),
    user_sb = Depends(get_user_db),
    limit: int = Query(default=50, ge=1, le=200),
    cursor: Optional[str] = Query(None),
):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)

    try:
        query = (
            user_sb.table("completed_courses")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
        )

        if cursor:
            query = query.lt("created_at", cursor)

        query = query.limit(limit)
        response = query.execute()
        data = response.data or []

        next_cursor = data[-1]["created_at"] if data else None

        return {
            "completed_courses": data,
            "count": len(data),
            "next_cursor": next_cursor,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error getting completed courses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve completed courses",
        )


@router.post("/{user_id}", response_model=dict)
async def add_completed_course(user_id: str, course: CompletedCourse, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)
    course = _validate_course_data(course)

    if await _check_duplicate(user_id, course.course_code, user_sb):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Course {course.course_code} is already marked as completed",
        )

    try:
        data = {
            "user_id": user_id,
            "course_code": course.course_code,
            "course_title": course.course_title,
            "subject": course.subject.upper(),
            "catalog": course.catalog,
            "term": course.term.capitalize(),
            "year": course.year,
            "grade": course.grade.upper() if course.grade else None,
            "credits": course.credits,
        }

        response = user_sb.table("completed_courses").insert(data).execute()

        if not response.data:
            raise DatabaseException("add_completed", "No data returned")

        logger.info(f"Added completed course {course.course_code} for user {user_id}")
        return {
            "completed_course": response.data[0],
            "message": "Course marked as completed",
        }
    except HTTPException:
        raise
    except Exception as e:
        error_str = str(e)
        if "duplicate key" in error_str.lower() or "23505" in error_str:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Course already marked as completed",
            )
        logger.exception(f"Error adding completed course: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add completed course",
        )


@router.patch("/{user_id}/{course_code}", response_model=dict)
async def update_completed_course(
    user_id: str, course_code: str, updates: CompletedCourseUpdate,
    req: Request, current_user_id: str = Depends(get_current_user_id),
    user_sb = Depends(get_user_db),
):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)
    course_code = normalize_course_code(course_code)

    # Validate fields
    if updates.term and updates.term.lower() not in VALID_TERMS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid term '{updates.term}'",
        )
    if updates.grade and updates.grade.upper() not in VALID_GRADES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid grade '{updates.grade}'",
        )

    try:
        update_data = {
            k: v for k, v in updates.model_dump().items() if v is not None
        }

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update",
            )

        response = (
            user_sb.table("completed_courses")
            .update(update_data)
            .eq("user_id", user_id)
            .eq("course_code", course_code)
            .execute()
        )

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Completed course not found",
            )

        return {
            "completed_course": response.data[0],
            "message": "Course updated",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error updating completed course: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update completed course",
        )


@router.delete("/{user_id}/{course_code}", response_model=dict)
async def remove_completed_course(user_id: str, course_code: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)
    course_code = normalize_course_code(course_code)

    try:
        user_sb.table("completed_courses").delete().eq(
            "user_id", user_id
        ).eq("course_code", course_code).execute()

        logger.info(f"Removed completed course {course_code} for user {user_id}")
        return {"message": "Course removed", "course_code": course_code}
    except Exception as e:
        logger.exception(f"Error removing completed course: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove completed course",
        )
