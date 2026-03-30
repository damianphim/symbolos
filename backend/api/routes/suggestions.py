"""
backend/api/routes/suggestions.py
Professor name suggestion/correction system.
Users can flag incorrect professor names; submissions go to a pending queue
for admin review before any data is updated.
"""
from fastapi import APIRouter, HTTPException, Header, status, Depends, Request
from pydantic import BaseModel, Field
from typing import Optional, List
import logging

from ..utils.supabase_client import get_supabase, get_user_by_id
from ..exceptions import DatabaseException, UserNotFoundException
from ..auth import get_current_user_id, require_self, get_user_db
from .admin import verify_admin_token

router = APIRouter()
logger = logging.getLogger(__name__)


class ProfSuggestion(BaseModel):
    user_id: str
    course_code: str = Field(..., min_length=1, max_length=20)
    current_name: Optional[str] = Field(None, max_length=200)
    suggested_name: str = Field(..., min_length=2, max_length=200)


class SuggestionReview(BaseModel):
    status: str = Field(..., pattern="^(approved|rejected)$")


# ── Auth helper for admin endpoints ──────────────────────────────────────────
# Uses the signed admin session token issued by /api/admin/verify.
# This is separate from CRON_SECRET so a leaked admin session cannot trigger
# automated cron jobs (and vice versa).
def _verify_admin_token_header(x_cron_secret: Optional[str]) -> None:
    """
    Verify the admin session token sent in the X-Cron-Secret header.
    The header name is kept for frontend compatibility; the value is now a
    short-lived signed token issued by /api/admin/verify, not the raw CRON_SECRET.
    """
    if not x_cron_secret or not verify_admin_token(x_cron_secret):
        raise HTTPException(status_code=401, detail="Invalid or missing admin token")


# ── Submit a suggestion ────────────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED)
async def submit_suggestion(
    suggestion: ProfSuggestion,
    req: Request,
    current_user_id: str = Depends(get_current_user_id),
    user_sb=Depends(get_user_db),
):
    """Submit a professor name correction. Auth required; user can only submit for themselves."""
    require_self(current_user_id, suggestion.user_id)
    try:
        # Verify user exists
        try:
            get_user_by_id(suggestion.user_id)
        except UserNotFoundException:
            raise HTTPException(status_code=404, detail="User not found")

        # Prevent duplicate pending suggestions from same user for same course
        existing = (
            user_sb.table("prof_suggestions")
            .select("id")
            .eq("user_id", suggestion.user_id)
            .eq("course_code", suggestion.course_code.upper())
            .eq("status", "pending")
            .execute()
        )
        if existing.data:
            raise HTTPException(
                status_code=409,
                detail="You already have a pending suggestion for this course."
            )

        data = {
            "user_id": suggestion.user_id,
            "course_code": suggestion.course_code.upper(),
            "current_name": suggestion.current_name,
            "suggested_name": suggestion.suggested_name.strip(),
            "status": "pending",
        }

        response = user_sb.table("prof_suggestions").insert(data).execute()

        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to save suggestion")

        logger.info(
            f"Prof suggestion submitted: {suggestion.course_code} → '{suggestion.suggested_name}' "
            f"by user {suggestion.user_id}"
        )

        return {"message": "Suggestion submitted successfully. Thank you!", "id": response.data[0]["id"]}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error submitting suggestion: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit suggestion")


# ── Admin: list all pending suggestions ───────────────────────
@router.get("/admin/pending", response_model=dict)
async def get_pending_suggestions(x_cron_secret: Optional[str] = Header(None)):
    """Admin endpoint — list all pending suggestions. Protected by CRON_SECRET."""
    _verify_admin_token_header(x_cron_secret)

    try:
        supabase = get_supabase()
        response = (
            supabase.table("prof_suggestions")
            .select("*")
            .eq("status", "pending")
            .order("created_at", desc=False)
            .execute()
        )
        return {"suggestions": response.data or [], "count": len(response.data or [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching pending suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch suggestions")


# ── Admin: approve or reject a suggestion ─────────────────────
@router.patch("/admin/{suggestion_id}", response_model=dict)
async def review_suggestion(
    suggestion_id: str,
    review: SuggestionReview,
    x_cron_secret: Optional[str] = Header(None),
):
    """
    Admin endpoint — approve or reject a pending suggestion.
    If approved, updates the instructor name in the courses table.
    Protected by CRON_SECRET.
    """
    _verify_admin_token_header(x_cron_secret)

    try:
        supabase = get_supabase()

        # Fetch the suggestion
        result = (
            supabase.table("prof_suggestions")
            .select("*")
            .eq("id", suggestion_id)
            .execute()
        )
        if not result.data:
            raise HTTPException(status_code=404, detail="Suggestion not found")

        suggestion = result.data[0]

        if suggestion["status"] != "pending":
            raise HTTPException(status_code=409, detail="Suggestion has already been reviewed")

        # Update suggestion status
        supabase.table("prof_suggestions").update({"status": review.status}).eq("id", suggestion_id).execute()

        # If approved, update the instructor in the courses table
        if review.status == "approved":
            supabase.table("courses").update(
                {"instructor": suggestion["suggested_name"]}
            ).eq("Course", suggestion["course_code"]).execute()

            logger.info(
                f"Suggestion {suggestion_id} approved — updated instructor for "
                f"{suggestion['course_code']} to '{suggestion['suggested_name']}'"
            )

        return {"message": f"Suggestion {review.status} successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error reviewing suggestion: {e}")
        raise HTTPException(status_code=500, detail="Failed to review suggestion")


# ── Admin: list all suggestions (all statuses) ────────────────
@router.get("/admin/all", response_model=dict)
async def get_all_suggestions(x_cron_secret: Optional[str] = Header(None)):
    """Admin endpoint — list all suggestions regardless of status. Protected by CRON_SECRET."""
    _verify_admin_token_header(x_cron_secret)

    try:
        supabase = get_supabase()
        response = (
            supabase.table("prof_suggestions")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )
        return {"suggestions": response.data or [], "count": len(response.data or [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching all suggestions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch suggestions")
