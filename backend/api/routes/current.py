"""
backend/api/routes/current.py
Current (in-progress) courses for a user.
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import Optional
from pydantic import BaseModel, Field
import logging
import re

from ..utils.supabase_client import get_supabase, get_user_by_id
from ..exceptions import DatabaseException, UserNotFoundException
from ..auth import get_current_user_id, require_self

router = APIRouter()
logger = logging.getLogger(__name__)

COURSE_CODE_PATTERN = re.compile(r"^[A-Z]{3,4}\s?\d{3}[A-Z]?\d?$", re.IGNORECASE)


def normalize_course_code(code: str) -> str:
    code = code.strip().upper()
    code = re.sub(r"([A-Z])(\d)", r"\1 \2", code)
    code = re.sub(r"\s+", " ", code)
    return code


def _validate_user_exists(user_id: str) -> None:
    try:
        get_user_by_id(user_id)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


class CurrentCourse(BaseModel):
    course_code: str = Field(..., min_length=1, max_length=20)
    course_title: str = Field(..., min_length=1, max_length=200)
    subject: str = Field(..., min_length=2, max_length=4)
    catalog: str = Field(..., min_length=1, max_length=10)
    credits: int = Field(default=3, ge=0, le=12)


@router.get("/{user_id}")
async def get_current_courses(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)
    try:
        supabase = get_supabase()
        response = (
            supabase.table("current_courses")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        return {"current_courses": response.data or [], "count": len(response.data or [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error getting current courses: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve current courses")


@router.post("/{user_id}")
async def add_current_course(user_id: str, course: CurrentCourse, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)
    course.course_code = normalize_course_code(course.course_code)

    if not COURSE_CODE_PATTERN.match(course.course_code):
        raise HTTPException(status_code=422, detail=f"Invalid course code format: '{course.course_code}'")

    # Check duplicate
    try:
        supabase = get_supabase()
        existing = (
            supabase.table("current_courses")
            .select("id")
            .eq("user_id", user_id)
            .eq("course_code", course.course_code)
            .execute()
        )
        if existing.data:
            raise HTTPException(status_code=409, detail=f"Course {course.course_code} is already in current courses")

        data = {
            "user_id": user_id,
            "course_code": course.course_code,
            "course_title": course.course_title,
            "subject": course.subject.upper(),
            "catalog": course.catalog,
            "credits": course.credits,
        }
        response = supabase.table("current_courses").insert(data).execute()
        if not response.data:
            raise DatabaseException("add_current", "No data returned")

        return {"current_course": response.data[0], "message": "Course added to current courses"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error adding current course: {e}")
        raise HTTPException(status_code=500, detail="Failed to add current course")


@router.delete("/{user_id}/{course_code}")
async def remove_current_course(user_id: str, course_code: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    _validate_user_exists(user_id)
    course_code = normalize_course_code(course_code)
    try:
        supabase = get_supabase()
        supabase.table("current_courses").delete().eq("user_id", user_id).eq("course_code", course_code).execute()
        return {"message": "Course removed", "course_code": course_code}
    except Exception as e:
        logger.exception(f"Error removing current course: {e}")
        raise HTTPException(status_code=500, detail="Failed to remove current course")
