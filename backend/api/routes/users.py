"""
User management endpoints with improved error handling

SEC-001 FIX: Corrected table names in delete cascade and added missing tables.
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
# FIX #20/#26: Import field_validator and ConfigDict; remove old `validator`
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional, List
import logging
from urllib.parse import urlparse

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
from ..auth import get_current_user_id, require_self, get_user_db

router = APIRouter()
logger = logging.getLogger(__name__)


# FIX F-11: Typed sub-models replace raw dict fields
class AdvancedStandingItem(BaseModel):
    """A single AP/IB/transfer credit item."""
    course_code: str = Field(..., max_length=20)
    course_title: Optional[str] = Field(None, max_length=200)
    credits: float = Field(..., ge=0, le=20)


class NotificationPrefs(BaseModel):
    """User notification preferences."""
    email_enabled: bool = True
    sms_enabled: bool = False
    notify_1day: bool = True
    notify_7days: bool = True
    notify_same_day: bool = False


class UserCreate(BaseModel):
    """User creation schema"""
    id: str = Field(..., description="Supabase Auth user ID")
    email: EmailStr
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    major: Optional[str] = Field(None, max_length=100)
    # SEC-021: Constrained list size and item length (was unbounded)
    other_majors: Optional[List[str]] = Field(default_factory=list, max_length=10)
    minor: Optional[str] = Field(None, max_length=100)
    other_minors: Optional[List[str]] = Field(default_factory=list, max_length=10)
    concentration: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=1, le=10)
    interests: Optional[str] = Field(None, max_length=500)
    current_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    is_honours: Optional[bool] = Field(False, description="Whether the student is in an Honours program")
    advanced_standing: Optional[List[AdvancedStandingItem]] = Field(default_factory=list)

    # FIX #20: Replace deprecated Pydantic v1 @validator with Pydantic v2
    # @field_validator. The @classmethod decorator is required in v2.
    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v):
        if v and not str(v).replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

    # SEC-021: Validate individual item length in other_majors / other_minors
    @field_validator('other_majors', 'other_minors', mode='before')
    @classmethod
    def validate_string_list_items(cls, v):
        if v is None:
            return v
        for item in v:
            if not isinstance(item, str) or len(item) > 100:
                raise ValueError('Each item must be a string of at most 100 characters')
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
                "minor": None,
                "year": 2,
                "interests": "artificial intelligence, web development",
                "current_gpa": 3.5,
            }
        }
    )


class UserUpdate(BaseModel):
    """User update schema — only provided fields are changed"""
    username: Optional[str] = Field(None, min_length=3, max_length=20)
    major: Optional[str] = Field(None, max_length=100)
    other_majors: Optional[List[str]] = Field(None, max_length=10)  # SEC-021
    minor: Optional[str] = Field(None, max_length=100)
    other_minors: Optional[List[str]] = Field(None, max_length=10)  # SEC-021
    concentration: Optional[str] = Field(None, max_length=100)
    faculty: Optional[str] = Field(None, max_length=100)
    year: Optional[int] = Field(None, ge=0, le=10)
    interests: Optional[str] = Field(None, max_length=500)
    current_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    target_gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    is_honours: Optional[bool] = None
    profile_image: Optional[str] = None
    notification_prefs: Optional[NotificationPrefs] = None
    advanced_standing: Optional[List[AdvancedStandingItem]] = None

    # FIX F-06: Validate profile_image must be a valid https:// URL
    @field_validator('profile_image', mode='before')
    @classmethod
    def validate_profile_image(cls, v):
        if v is None:
            return v
        parsed = urlparse(str(v))
        if parsed.scheme != 'https':
            raise ValueError('profile_image must be a valid https:// URL')
        if not parsed.netloc:
            raise ValueError('profile_image must be a valid https:// URL')
        return str(v)

    @field_validator('username', mode='before')
    @classmethod
    def validate_username(cls, v):
        if v is None:
            return v
        if not str(v).replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v

    # SEC-021: Validate individual item length in other_majors / other_minors
    @field_validator('other_majors', 'other_minors', mode='before')
    @classmethod
    def validate_string_list_items(cls, v):
        if v is None:
            return v
        for item in v:
            if not isinstance(item, str) or len(item) > 100:
                raise ValueError('Each item must be a string of at most 100 characters')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "major": "Computer Science",
                "year": 3,
                "interests": "machine learning, data science"
            }
        }
    )


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_new_user(user: UserCreate, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Create a new user profile"""
    # FIX F-03: Ensure the authenticated user can only create their own profile
    require_self(current_user_id, user.id)

    try:
        # Check for existing email
        existing = get_user_by_email(user.email)
        if existing:
            if existing["id"] == user.id:
                return {"user": existing, "message": "User profile already exists"}
            raise UserAlreadyExistsException(user.email)

        user_data = user.model_dump(exclude_none=True)
        # Handle advanced_standing serialization
        if "advanced_standing" in user_data:
            user_data["advanced_standing"] = [
                item if isinstance(item, dict) else item.model_dump()
                for item in (user_data["advanced_standing"] or [])
            ]

        new_user = create_user_db(user_data)
        logger.info(f"New user created: {new_user.get('id')}")
        return {"user": new_user, "message": "User profile created successfully"}

    except UserAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": "user_already_exists", "message": "A user with this email already exists"}
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error creating user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )


@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
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
async def update_user(user_id: str, updates: UserUpdate, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    require_self(current_user_id, user_id)
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


# ──────────────────────────────────────────────────────────────────────────────
# SEC-001 FIX: Corrected table names and added missing tables.
#
# BEFORE (BROKEN):
#   "ai_cards"       → table doesn't exist (actual: "advisor_cards")
#   "chat_history"   → table doesn't exist (actual: "chat_messages")
#   missing:         → "favorites", "prof_suggestions" never deleted
#
# The `except: pass` pattern silently swallowed the wrong table name errors,
# so user data was never actually deleted from those tables.
# ──────────────────────────────────────────────────────────────────────────────

@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user_account(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    """Permanently delete a user's account. Users may only delete their own account."""
    require_self(current_user_id, user_id)
    try:
        supabase = get_supabase()

        # SEC-001 FIX: Correct table names and complete cascade.
        # Order: dependents first, then the user row itself.
        # Each tuple is (table_name, column_to_match).
        tables_to_clear = [
            ("advisor_cards",      "user_id"),   # was "ai_cards" (WRONG)
            ("chat_messages",      "user_id"),   # was "chat_history" (WRONG)
            ("favorites",          "user_id"),   # was MISSING
            ("prof_suggestions",   "user_id"),   # was MISSING
            ("user_clubs",         "user_id"),
            ("current_courses",    "user_id"),
            ("completed_courses",  "user_id"),
            ("calendar_events",    "user_id"),
            ("notification_queue", "user_id"),
        ]

        errors = []
        for table, column in tables_to_clear:
            try:
                supabase.table(table).delete().eq(column, user_id).execute()
            except Exception as e:
                # Log but continue — we still want to delete as much as possible
                errors.append(f"{table}: {e}")
                logger.warning(f"Failed to clear {table} for user {user_id}: {e}")

        # Delete the user profile row (uses "id" not "user_id")
        try:
            supabase.table("users").delete().eq("id", user_id).execute()
        except Exception as e:
            errors.append(f"users: {e}")
            logger.warning(f"Failed to delete user row for {user_id}: {e}")

        # Delete the Supabase Auth user (requires service role key)
        try:
            supabase.auth.admin.delete_user(user_id)
        except Exception as e:
            logger.warning(f"Could not delete auth user {user_id}: {e}")

        if errors:
            logger.error(f"Partial deletion for {user_id}. Failed tables: {errors}")

        logger.info(f"Account deleted: {user_id}")
        return {"message": "Account deleted successfully"}

    except Exception as e:
        logger.exception(f"Error deleting user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"code": "delete_failed", "message": "Failed to delete account"}
        )
