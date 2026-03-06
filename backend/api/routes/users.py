"""
User management endpoints with improved error handling
"""
from fastapi import APIRouter, HTTPException, status
# FIX #20/#26: Import field_validator and ConfigDict; remove old `validator`
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
import logging

from api.utils.supabase_client import (
    get_user_by_id,
    get_user_by_email,
    create_user as create_user_db,
    update_user as update_user_db,
    get_supabase
)
from api.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    DatabaseException
)
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


class UserCreate(BaseModel):
    """User creation schema"""
    id: str = Field(..., description="Supabase Auth user ID")
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    major: Optional[str] = Field(None, max_length=100)
    other_majors: Optional[List[str]] = Field(default_factory=list)
    minor: Optional[str] = Field(None, max_length=100)
    other_minors: Optional[List[str]] = Field(default_factory=list)
    concentration: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1, le=10)
    interests: Optional[str] = Field(None, max_length=500)
    current_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    advanced_standing: Optional[List[dict]] = Field(default_factory=list)

    # FIX #20: Replace deprecated Pydantic v1 @validator with Pydantic v2
    # @field_validator. The @classmethod decorator is required in v2.
    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v):
        if v and not str(v).replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

    # FIX #26: Replace deprecated Pydantic v1 `class Config` / `schema_extra`
    # with Pydantic v2 `model_config` / `json_schema_extra`.
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "student@mail.mcgill.ca",
                "username": "mcgill_student",
                "major": "Computer Science",
                "other_majors": ["Mathematics"],
                "minor": "Economics",
                "other_minors": [],
                "concentration": "AI/ML",
                "year": 3,
                "interests": "Machine Learning, Web Development",
                "current_gpa": 3.5,
                "advanced_standing": [
                    {"course_code": "MATH 140", "course_title": "Calculus I", "credits": 3}
                ]
            }
        }
    )


class UserUpdate(BaseModel):
    """User update schema - handles null values for clearing fields"""
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    major: Optional[str] = Field(None, max_length=100)
    other_majors: Optional[List[str]] = None
    minor: Optional[str] = Field(None, max_length=100)
    other_minors: Optional[List[str]] = None
    concentration: Optional[str] = Field(None, max_length=100)
    faculty: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=0, le=10)
    interests: Optional[str] = Field(None, max_length=500)
    current_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    advanced_standing: Optional[List[dict]] = None
    notification_prefs: Optional[dict] = None
    profile_image: Optional[str] = None

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v):
        if v and not str(v).replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v


class UserResponse(BaseModel):
    """User response schema"""
    id: str
    email: str
    username: Optional[str] = None
    major: Optional[str] = None
    other_majors: Optional[List[str]] = None
    minor: Optional[str] = None
    other_minors: Optional[List[str]] = None
    concentration: Optional[str] = None
    faculty: Optional[str] = None
    year: Optional[int] = None
    interests: Optional[str] = None
    current_gpa: Optional[float] = None
    advanced_standing: Optional[List[dict]] = None
    created_at: Optional[str] = None


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate):
    """Create a new user profile"""
    try:
        logger.info(f"=== CREATE USER REQUEST ===")
        logger.info(f"User ID: {user.id}")
        logger.info(f"Email: {user.email}")
        logger.info(f"Username: {user.username}")

        # Check if profile exists by ID (not email!)
        try:
            existing = get_user_by_id(user.id)
            logger.warning(f"User profile already exists: {user.id}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "user_already_exists",
                    "message": "User profile already exists for this ID"
                }
            )
        except UserNotFoundException:
            logger.info(f"User profile doesn't exist yet, creating...")
            pass

        # Create user
        user_data = user.model_dump(exclude_none=True)
        created_user = create_user_db(user_data)

        logger.info(f"✓ User profile created successfully: {created_user['id']}")
        return {
            "user": created_user,
            "message": "User profile created successfully"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"✗ Unexpected error creating user")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "internal_error",
                "message": "Failed to create user profile"
            }
        )


@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str):
    """
    Get user profile by ID

    - **user_id**: The user's unique identifier
    """
    try:
        user = get_user_by_id(user_id)
        return {"user": user}
    except UserNotFoundException as e:
        logger.warning(f"User not found: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "user_not_found",
                "message": "User not found"
            }
        )
    except Exception as e:
        logger.exception(f"Unexpected error getting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.patch("/{user_id}", response_model=dict)
async def update_user(user_id: str, updates: UserUpdate):
    """
    Update user profile

    - **user_id**: The user's unique identifier
    - **updates**: Fields to update (only provided fields are changed)
    """
    try:
        get_user_by_id(user_id)

        # Use model_dump (Pydantic v2) — include fields explicitly set to None
        # so callers can clear optional fields
        update_data = updates.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        updated_user = update_user_db(user_id, update_data)
        logger.info(f"User profile updated: {user_id}")

        return {
            "user": updated_user,
            "message": "User profile updated successfully"
        }

    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": "user_not_found", "message": "User not found"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error updating user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_account(user_id: str):
    """
    Permanently delete a user's account and all associated data.
    Deletes: user data rows, then the Supabase Auth user.
    """
    try:
        supabase = get_supabase()

        # Delete user data from all tables (cascade-order)
        tables_to_clear = [
            "user_clubs",
            "user_current_courses",
            "user_completed_courses",
            "user_events",
            "notifications",
            "ai_cards",
            "users",
        ]
        for table in tables_to_clear:
            try:
                supabase.table(table).delete().eq("user_id", user_id).execute()
            except Exception:
                # Some tables may not exist or column may differ — continue
                pass

        # Also try `id` column for the users table specifically
        try:
            supabase.table("users").delete().eq("id", user_id).execute()
        except Exception:
            pass

        # Delete the Supabase Auth user (requires service role key)
        try:
            supabase.auth.admin.delete_user(user_id)
        except Exception as e:
            logger.warning(f"Could not delete auth user {user_id}: {e}")

        logger.info(f"Account deleted: {user_id}")
        return {"message": "Account deleted successfully"}

    except Exception as e:
        logger.exception(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "delete_failed", "message": "Failed to delete account"}
        )
