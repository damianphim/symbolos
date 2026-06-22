"""Joining/leaving clubs, a user's own club-scoped views, Join Requests,
and the calendar-sync feed (see CONTEXT.md — distinct from Subscription)."""
from fastapi import HTTPException, Request, Depends
from datetime import datetime, timedelta
import logging

from ...utils.supabase_client import get_supabase
from ...auth import get_current_user_id, require_self, get_user_db
from ._router import router
from .permissions import is_admin_user, is_club_owner_or_admin
from .schemas import JoinClubRequest, JoinRequestAction

logger = logging.getLogger(__name__)


@router.get("/join-requests/{club_id}")
async def get_join_requests(club_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Get pending Join Requests for a club. Owner or Managers can view."""
    try:
        supabase = get_supabase()
        if not is_club_owner_or_admin(club_id, current_user_id):
            raise HTTPException(status_code=403, detail="Only the club creator or admins can view join requests")

        result = (
            supabase.table("club_join_requests")
            .select("*")
            .eq("club_id", club_id)
            .eq("status", "pending")
            .order("created_at", desc=True)
            .execute()
        )
        return {"requests": result.data or [], "count": len(result.data or [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching join requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve join requests")


@router.post("/join-requests/{request_id}/action")
async def handle_join_request(request_id: str, body: JoinRequestAction, current_user_id: str = Depends(get_current_user_id)):
    """Approve or deny a Join Request."""
    if body.action not in ("approve", "deny"):
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'deny'")
    try:
        supabase = get_supabase()

        # Step 1: Get the request
        logger.info(f"[join-action] Looking up request {request_id}")
        req_result = supabase.table("club_join_requests").select("*").eq("id", request_id).execute()
        if not req_result.data:
            raise HTTPException(status_code=404, detail="Join request not found")
        join_req = req_result.data[0]
        logger.info(f"[join-action] Found request for club {join_req.get('club_id')} by user {join_req.get('user_id')}")

        # Step 2: Verify club ownership, per-club Manager, or global admin
        # NOTE: signature is is_club_owner_or_admin(club_id, user_id) — the
        # arguments were previously reversed here, which made this check
        # silently fail closed (no owner/admin could ever action a request).
        if not is_club_owner_or_admin(join_req["club_id"], current_user_id):
            raise HTTPException(status_code=403, detail="Only the club owner or admins can handle join requests")

        # Step 3: If approve, add to club
        if body.action == "approve":
            logger.info("[join-action] Approving — adding user to club")
            existing = supabase.table("user_clubs").select("user_id").eq("user_id", join_req["user_id"]).eq("club_id", join_req["club_id"]).execute()
            if not existing.data:
                supabase.table("user_clubs").insert({
                    "user_id": join_req["user_id"],
                    "club_id": join_req["club_id"],
                    "calendar_synced": True,
                }).execute()

        # Step 4: Delete the join request — Join Requests don't keep history
        # (unlike Club Submissions / Manager Invites; see CONTEXT.md)
        logger.info(f"[join-action] Deleting request {request_id}")
        supabase.table("club_join_requests").delete().eq("id", request_id).execute()

        logger.info(f"[join-action] Done — action={body.action}")
        return {"success": True, "status": "approved" if body.action == "approve" else "denied"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"[join-action] FAILED: {e}")
        raise HTTPException(status_code=500, detail="Failed to process join request")


@router.get("/user/{user_id}")
async def get_user_clubs(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Return all clubs a user has joined."""
    require_self(current_user_id, user_id)
    try:
        result = (
            user_sb.table("user_clubs")
            .select("*, clubs(*)")
            .eq("user_id", user_id)
            .execute()
        )
        clubs = []
        for row in (result.data or []):
            club_data = row.get("clubs") or {}
            club_data["calendar_synced"] = row.get("calendar_synced", False)
            club_data["joined_at"] = row.get("joined_at")
            club_data["user_club_id"] = row.get("id")
            clubs.append(club_data)
        return {"clubs": clubs, "count": len(clubs)}
    except Exception as e:
        logger.exception(f"Error fetching user clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user clubs")


@router.post("/user/{user_id}/join")
async def join_club(user_id: str, body: JoinClubRequest, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Join a public club directly, or create a Join Request for a private club."""
    require_self(current_user_id, user_id)

    # SEC FIX #2 / #5: McGill check + verified email.
    # The previous gate read users.email (user-editable), so anyone could
    # set their profile email to *@mail.mcgill.ca and join private clubs.
    # Now we trust ONLY auth.users.email — which the user proved control
    # of during Supabase Auth signup.
    from ...utils.verified_user import is_email_verified
    from ...utils.anomaly import record_action
    record_action(current_user_id, "club_join")
    try:
        supabase = get_supabase()
        if not is_admin_user(user_id):
            try:
                auth_user = supabase.auth.admin.get_user_by_id(user_id)
                auth_email = (getattr(auth_user.user, "email", None) or "").lower()
            except Exception:
                auth_email = ""
            if not auth_email.endswith("@mail.mcgill.ca"):
                raise HTTPException(status_code=403, detail="Only accounts with a @mail.mcgill.ca email can join clubs.")
            if not is_email_verified(user_id):
                raise HTTPException(status_code=403, detail={"code": "email_not_verified", "message": "Verify your email to join clubs."})

        # Check if club exists and whether it's private
        club_result = supabase.table("clubs").select("*").eq("id", body.club_id).execute()
        if not club_result.data:
            raise HTTPException(status_code=404, detail="Club not found")
        club = club_result.data[0]

        existing = (
            user_sb.table("user_clubs")
            .select("user_id")
            .eq("user_id", user_id)
            .eq("club_id", body.club_id)
            .execute()
        )
        if existing.data:
            raise HTTPException(status_code=409, detail="Already joined this club")

        if club.get("is_private"):
            # Check for existing pending request
            existing_req = (
                user_sb.table("club_join_requests")
                .select("id")
                .eq("user_id", user_id)
                .eq("club_id", body.club_id)
                .eq("status", "pending")
                .execute()
            )
            if existing_req.data:
                raise HTTPException(status_code=409, detail="You already have a pending request for this club")

            # Rate limit: max 3 applications per club per year
            one_year_ago = (datetime.utcnow() - timedelta(days=365)).isoformat()
            yearly_requests = (
                user_sb.table("club_join_requests")
                .select("id", count="exact")
                .eq("user_id", user_id)
                .eq("club_id", body.club_id)
                .gte("created_at", one_year_ago)
                .execute()
            )
            yearly_count = yearly_requests.count if yearly_requests.count is not None else len(yearly_requests.data or [])
            if yearly_count >= 3:
                raise HTTPException(status_code=429, detail="You can only apply to this club 3 times per year")

            # Use user-provided info from the join form
            requester_name = body.requester_name or "A student"
            requester_email = body.requester_email or ""
            requester_linkedin = body.requester_linkedin or ""

            # Create join request
            insert_data = {
                "user_id": user_id,
                "club_id": body.club_id,
                "status": "pending",
                "requester_name": requester_name,
            }
            # Add optional columns if provided (columns must exist in table)
            if requester_email:
                insert_data["requester_email"] = requester_email
            if requester_linkedin:
                insert_data["requester_linkedin"] = requester_linkedin

            user_sb.table("club_join_requests").insert(insert_data).execute()

            # Email club creator at milestone pending counts: 10, 20, 40, 60, 80, 100
            try:
                from .email import _send_join_request_email
                pending_count_result = (
                    supabase.table("club_join_requests")
                    .select("id", count="exact")
                    .eq("club_id", body.club_id)
                    .eq("status", "pending")
                    .execute()
                )
                pending_count = pending_count_result.count if pending_count_result.count is not None else len(pending_count_result.data or [])
                notify_milestones = {10, 20, 40, 60, 80, 100}
                if pending_count in notify_milestones:
                    creator_id = club.get("created_by")
                    if creator_id:
                        creator_result = supabase.table("users").select("email").eq("id", creator_id).execute()
                        if creator_result.data and creator_result.data[0].get("email"):
                            _send_join_request_email(
                                creator_email=creator_result.data[0]["email"],
                                club_name=club["name"],
                                requester_name=requester_name,
                                requester_email=requester_email,
                                requester_linkedin=requester_linkedin,
                            )
            except Exception as e:
                logger.warning(f"Failed to send join request email: {e}")

            return {"success": True, "status": "requested", "message": "Join request sent to club creator"}
        else:
            # Public club — join directly
            user_sb.table("user_clubs").insert({
                "user_id": user_id,
                "club_id": body.club_id,
                "calendar_synced": True,
            }).execute()
            return {"success": True, "status": "joined"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error joining club: {e}")
        raise HTTPException(status_code=500, detail="Failed to join club")


@router.get("/user/{user_id}/pending-requests")
async def get_user_pending_requests(user_id: str, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Get all club IDs where the user has a pending Join Request."""
    require_self(current_user_id, user_id)
    try:
        result = user_sb.table("club_join_requests").select("club_id").eq("user_id", user_id).eq("status", "pending").execute()
        club_ids = [r["club_id"] for r in (result.data or [])]
        return {"pending_club_ids": club_ids}
    except Exception as e:
        logger.exception(f"Error fetching pending requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch pending requests")


@router.get("/user/{user_id}/subscriptions")
async def get_user_subscriptions(user_id: str, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Get all club IDs the user is Subscribed to (see CONTEXT.md — distinct
    from Calendar Sync)."""
    require_self(current_user_id, user_id)
    try:
        result = user_sb.table("club_subscriptions").select("club_id").eq("user_id", user_id).execute()
        club_ids = [r["club_id"] for r in (result.data or [])]
        return {"subscribed_club_ids": club_ids}
    except Exception as e:
        logger.exception(f"Error fetching subscriptions: {e}")
        return {"subscribed_club_ids": []}


@router.delete("/user/{user_id}/leave/{club_id}")
async def leave_club(user_id: str, club_id: str, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Remove a club from the user's joined list."""
    require_self(current_user_id, user_id)
    try:
        user_sb.table("user_clubs").delete().eq("user_id", user_id).eq("club_id", club_id).execute()
        return {"success": True}
    except Exception as e:
        logger.exception(f"Error leaving club: {e}")
        raise HTTPException(status_code=500, detail="Failed to leave club")


@router.patch("/user/{user_id}/calendar/{club_id}")
async def toggle_calendar_sync(user_id: str, club_id: str, synced: bool, req: Request, current_user_id: str = Depends(get_current_user_id), user_sb = Depends(get_user_db)):
    """Toggle Calendar Sync for a club (see CONTEXT.md — distinct from Subscription)."""
    require_self(current_user_id, user_id)
    try:
        user_sb.table("user_clubs").update({"calendar_synced": synced}).eq("user_id", user_id).eq("club_id", club_id).execute()
        return {"success": True, "calendar_synced": synced}
    except Exception as e:
        logger.exception(f"Error toggling calendar sync: {e}")
        raise HTTPException(status_code=500, detail="Failed to update calendar sync")


@router.get("/events/subscribed")
async def get_subscribed_club_events(current_user_id: str = Depends(get_current_user_id)):
    """Get all club events from clubs the user has calendar_synced=true."""
    try:
        supabase = get_supabase()
        memberships = supabase.table("user_clubs").select("club_id").eq("user_id", current_user_id).eq("calendar_synced", True).execute()
        club_ids = [m["club_id"] for m in (memberships.data or [])]
        if not club_ids:
            return {"events": []}
        events = supabase.table("club_events").select("*, clubs(name, category)").in_("club_id", club_ids).order("date").execute()
        return {"events": events.data or []}
    except Exception as e:
        logger.exception(f"Error fetching subscribed club events: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch club events")


@router.get("/announcements/subscribed")
async def get_subscribed_club_announcements(current_user_id: str = Depends(get_current_user_id)):
    """Get all announcements from clubs the user has calendar_synced=true."""
    try:
        supabase = get_supabase()
        memberships = supabase.table("user_clubs").select("club_id").eq("user_id", current_user_id).eq("calendar_synced", True).execute()
        club_ids = [m["club_id"] for m in (memberships.data or [])]
        if not club_ids:
            return {"announcements": []}
        announcements = supabase.table("club_announcements").select("*, clubs(name, category)").in_("club_id", club_ids).order("created_at", desc=True).execute()
        return {"announcements": announcements.data or []}
    except Exception as e:
        logger.exception(f"Error fetching subscribed announcements: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch announcements")
