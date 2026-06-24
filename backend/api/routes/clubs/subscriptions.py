"""Club Subscriptions — a lightweight public interest signal, distinct from
Calendar Sync (see CONTEXT.md)."""
from fastapi import HTTPException, Depends
import logging

from ...utils.supabase_client import get_supabase
from ...auth import get_current_user_id, require_mcgill_email
from ._router import router

logger = logging.getLogger(__name__)


@router.post("/{club_id}/subscribe")
async def toggle_subscribe(club_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Toggle Subscription to a club's events/news. Returns the new state."""
    require_mcgill_email(current_user_id)
    try:
        supabase = get_supabase()
        # Verify club exists
        club_result = supabase.table("clubs").select("id").eq("id", club_id).execute()
        if not club_result.data:
            raise HTTPException(status_code=404, detail="Club not found")

        # Check current subscription
        existing = (
            supabase.table("club_subscriptions")
            .select("id")
            .eq("club_id", club_id)
            .eq("user_id", current_user_id)
            .execute()
        )
        if existing.data:
            # Unsubscribe
            supabase.table("club_subscriptions").delete().eq("club_id", club_id).eq("user_id", current_user_id).execute()
            return {"success": True, "is_subscribed": False}
        else:
            # Subscribe
            supabase.table("club_subscriptions").insert({
                "club_id": club_id,
                "user_id": current_user_id,
            }).execute()
            return {"success": True, "is_subscribed": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error toggling subscription: {e}")
        raise HTTPException(status_code=500, detail="Failed to toggle subscription")


@router.get("/{club_id}/subscribers")
async def get_subscribers_count(
    club_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    """Get the subscriber count for a club.

    SEC FIX #3: was unauthenticated. Now requires a logged-in user. The
    aggregate count itself is non-sensitive, but exposing this endpoint
    without auth let scrapers enumerate every club's popularity without
    even creating an account.
    """
    try:
        supabase = get_supabase()
        result = supabase.table("club_subscriptions").select("id", count="exact").eq("club_id", club_id).execute()
        count = result.count if result.count is not None else len(result.data or [])
        return {"count": count}
    except Exception as e:
        logger.exception(f"Error fetching subscribers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscribers")
