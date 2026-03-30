"""
Favorites endpoints for managing user's favorited courses
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from typing import List
from pydantic import BaseModel
import logging

from ..utils.supabase_client import get_supabase
from ..exceptions import DatabaseException
from ..auth import get_current_user_id, require_self, get_user_db

router = APIRouter()
logger = logging.getLogger(__name__)


class FavoriteRequest(BaseModel):
    """Request to add a favorite"""
    course_code: str
    course_title: str
    subject: str
    catalog: str


class FavoriteResponse(BaseModel):
    """Favorite course response"""
    id: int
    course_code: str
    course_title: str
    subject: str
    catalog: str
    created_at: str


@router.get("/{user_id}", response_model=dict)
async def get_user_favorites(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
    """
    Get all favorited courses for a user
    
    - **user_id**: User's UUID
    
    Returns list of favorited courses with details
    """
    try:
        result = (
            user_sb.table("favorites")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
        favorites = result.data or []
        logger.info(f"Retrieved {len(favorites)} favorites for user {user_id}")
        return {
            "favorites": favorites,
            "count": len(favorites)
        }
    except Exception as e:
        logger.exception(f"Unexpected error getting favorites: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve favorites"
        )


@router.post("/{user_id}", response_model=dict)
async def add_user_favorite(user_id: str, favorite: FavoriteRequest, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
    """
    Add a course to user's favorites
    
    - **user_id**: User's UUID
    - **favorite**: Course information to favorite
    
    Returns the created favorite
    """
    try:
        favorite_data = {
            "user_id": user_id,
            "course_code": favorite.course_code,
            "course_title": favorite.course_title,
            "subject": favorite.subject,
            "catalog": favorite.catalog,
        }
        response = user_sb.table("favorites").insert(favorite_data).execute()
        if not response.data:
            raise DatabaseException("add_favorite", "No data returned from insert")
        logger.info(f"Added favorite {favorite.course_code} for user {user_id}")
        return {
            "favorite": response.data[0],
            "message": "Course added to favorites"
        }
    except DatabaseException as e:
        error_msg = str(e)
        if "already in favorites" in error_msg:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Course is already in favorites"
            )
        logger.error(f"Database error adding favorite: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add favorite"
        )
    except Exception as e:
        error_str = str(e)
        if "duplicate key" in error_str.lower() or "23505" in error_str:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Course is already in favorites"
            )
        logger.exception(f"Unexpected error adding favorite: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.delete("/{user_id}/{course_code}", response_model=dict)
async def remove_user_favorite(user_id: str, course_code: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
    """
    Remove a course from user's favorites
    
    - **user_id**: User's UUID
    - **course_code**: Course code to unfavorite (e.g., "COMP206")
    
    Returns success message
    """
    try:
        user_sb.table("favorites").delete().eq("user_id", user_id).eq("course_code", course_code).execute()
        logger.info(f"Removed favorite {course_code} for user {user_id}")
        return {
            "message": "Course removed from favorites",
            "course_code": course_code
        }
    except Exception as e:
        logger.exception(f"Unexpected error removing favorite: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove favorite"
        )


@router.get("/{user_id}/check/{course_code}", response_model=dict)
async def check_favorite_status(user_id: str, course_code: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
    """
    Check if a course is favorited by user
    
    - **user_id**: User's UUID
    - **course_code**: Course code to check (e.g., "COMP206")
    
    Returns whether the course is favorited
    """
    try:
        response = (
            user_sb.table("favorites")
            .select("id")
            .eq("user_id", user_id)
            .eq("course_code", course_code)
            .execute()
        )
        favorited = len(response.data) > 0 if response.data else False
        return {
            "is_favorited": favorited,
            "course_code": course_code
        }
    except Exception as e:
        logger.exception(f"Error checking favorite status: {e}")
        return {
            "is_favorited": False,
            "course_code": course_code
        }
