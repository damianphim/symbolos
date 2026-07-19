"""Club discovery and basic CRUD: list, starter suggestions, categories,
the clubs a user manages, editing, and deleting."""
from fastapi import HTTPException, Query, Response, Depends
from typing import Optional
import logging

from ...utils.supabase_client import get_supabase
from ...auth import get_current_user_id, require_self
from ._router import router
from .helpers import strip_club_pii, get_starter_names
from .permissions import is_admin_user, is_club_owner_or_admin
from .schemas import UpdateClubRequest

logger = logging.getLogger(__name__)


@router.get("")
async def list_clubs(
    response: Response,
    search: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
    current_user_id: str = Depends(get_current_user_id),
):
    """Return the public discovery view of verified, non-private clubs.

    SEC FIX #4 (HIGH):
      * Endpoint requires authentication (the McGill-only gate).
      * Private clubs are filtered out — there is NO branch in this
        response that exposes them. Managers see their private clubs
        via the dedicated /api/clubs/created/{user_id} endpoint, which
        is per-user and never edge-cached.
      * Per-club PII (contact_email, executive_emails, created_by,
        admin emails) is always stripped. Managers needing those fields
        for clubs they own use /api/clubs/created/{user_id} or
        /api/clubs/{club_id}/managers.

    PERF: because the response is now *identical for every authenticated
    user* (no per-user manager carve-out), we can safely public-cache it
    at the Vercel edge. 1-min TTL + 2-min stale-while-revalidate still
    cuts most Supabase reads on this endpoint under launch traffic, while
    keeping newly-approved clubs visible within a few minutes instead of
    up to an hour (a longer window here previously made an admin-approved
    club appear "missing" for anyone who'd already warmed the cache).

    Supabase RLS still mirrors this in case the anon key in the bundle
    is used to query the table directly — see
    backend/migrations/2026_06_01_sec_rls_clubs_pii.sql.

    !! IMPORTANT for future maintainers !!
    Vercel's edge cache ignores the Authorization header on cache keys,
    so once warm, this endpoint effectively serves to anyone, including
    requests with no auth header. The audit (finding #4) explicitly OK'd
    this once PII and private clubs were stripped at the data layer —
    they are. DO NOT add ANY of the following to this response, because
    the cache will leak it to non-McGill callers:
      * personal email addresses (contact_email, executive_emails, ...)
      * any field that could differ per-caller
      * private-club rows
      * draft / unverified clubs
      * anything you wouldn't write on a public flyer.
    """
    try:
        supabase = get_supabase()
        query = (
            supabase.table("clubs")
            .select("*")
            .eq("is_verified", True)
            # SEC: hard filter at the query level — private clubs MUST NOT
            # appear in the discovery response under any circumstance.
            .or_("is_private.is.null,is_private.eq.false")
            .order("name")
            .limit(limit)
        )
        if category:
            query = query.eq("category", category)
        if search:
            safe_search = search.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
            query = query.ilike("name", f"%{safe_search}%")
        result = query.execute()
        clubs = result.data or []

        # Defense-in-depth: even if the .or_() filter is dropped in a
        # future refactor, we re-filter private clubs in Python before
        # serialising. The smoke test (test_private_clubs_hidden) covers
        # this path specifically.
        clubs = [c for c in clubs if not c.get("is_private")]

        # Strip PII uniformly. Same response for everyone, so the edge can
        # cache one copy and serve it to every signed-in caller.
        visible = [strip_club_pii(c) for c in clubs]

        # Batched subscriber counts — single query for the whole page.
        ids = [c["id"] for c in visible if c.get("id")]
        sub_counts: dict = {}
        if ids:
            try:
                sub_rows = (supabase.table("club_subscriptions")
                            .select("club_id").in_("club_id", ids).execute().data or [])
                for r in sub_rows:
                    cid = r.get("club_id")
                    if cid:
                        sub_counts[cid] = sub_counts.get(cid, 0) + 1
            except Exception:
                pass
        for c in visible:
            c["subscriber_count"] = sub_counts.get(c.get("id"), 0)

        # `public` = shared cache (Vercel edge) may store this response.
        # `s-maxage=60` = edge keeps it 1 min; `max-age=30` = browsers
        # reuse briefly so a quick back-button doesn't refetch.
        # `stale-while-revalidate=120` = serve stale for up to 2 more
        # minutes while a background refresh runs — smooths spikes without
        # leaving a newly-approved club "missing" for very long.
        response.headers["Cache-Control"] = (
            "public, max-age=30, s-maxage=60, stale-while-revalidate=120"
        )
        return {"clubs": visible, "count": len(visible)}
    except Exception as e:
        logger.exception(f"Error listing clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve clubs")


@router.get("/starter")
async def get_starter_clubs(user_id: str, major: Optional[str] = None, current_user_id: str = Depends(get_current_user_id)):
    """Return personalised starter club suggestions based on major."""
    require_self(current_user_id, user_id)
    try:
        supabase = get_supabase()
        names = get_starter_names(major)
        result = supabase.table("clubs").select("*").eq("is_verified", True).execute()
        all_clubs = result.data or []
        names_lower = [n.lower() for n in names]
        matched = [c for c in all_clubs if c["name"].lower() in names_lower]
        joined_result = (
            supabase.table("user_clubs")
            .select("club_id")
            .eq("user_id", user_id)
            .execute()
        )
        joined_ids = {row["club_id"] for row in (joined_result.data or [])}
        for club in matched:
            club["is_joined"] = club["id"] in joined_ids
        return {"starter_clubs": matched}
    except Exception as e:
        logger.exception(f"Error fetching starter clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve starter clubs")


# ── STATIC routes must come before dynamic /{user_id} routes ─────────────────

@router.get("/categories")
async def get_categories(response: Response):
    """Return the distinct club categories. List is static so the edge
    can cache it aggressively."""
    response.headers["Cache-Control"] = "public, s-maxage=86400, max-age=3600"
    return {
        "categories": [
            "Academic", "Arts & Culture", "Athletics & Recreation",
            "Community Service", "Debate & Politics", "Engineering & Technology",
            "Environment", "Health & Wellness", "International", "Professional",
            "Science", "Social", "Spiritual & Religious",
        ]
    }


@router.get("/created/{user_id}")
async def get_created_clubs(user_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Return clubs the user can manage — owner OR invited Manager.
    (Endpoint name kept for backwards compat; semantics widened so invited
    Managers see their clubs in the My Clubs > Manage section.)"""
    require_self(current_user_id, user_id)
    try:
        supabase = get_supabase()

        # 1. Clubs the user CREATED (owner)
        owned = (
            supabase.table("clubs")
            .select("*")
            .eq("created_by", user_id)
            .execute().data or []
        )

        # 2. Clubs where they have role='admin' in user_clubs (a Manager —
        # see CONTEXT.md for why this column says "admin")
        admin_rows = (
            supabase.table("user_clubs")
            .select("club_id")
            .eq("user_id", user_id)
            .eq("role", "admin")
            .execute().data or []
        )
        admin_club_ids = [r["club_id"] for r in admin_rows if r.get("club_id")]
        admin_clubs = []
        if admin_club_ids:
            admin_clubs = (
                supabase.table("clubs")
                .select("*")
                .in_("id", admin_club_ids)
                .execute().data or []
            )

        # Merge, dedupe by id, preserve a clear marker so the frontend can tell
        # how the user can manage this club (mostly cosmetic — privileges are
        # the same on the backend either way).
        merged = {}
        for c in owned:
            c["_manage_role"] = "owner"
            merged[c["id"]] = c
        for c in admin_clubs:
            if c["id"] not in merged:
                c["_manage_role"] = "admin"
                merged[c["id"]] = c

        result = sorted(merged.values(), key=lambda c: (c.get("name") or "").lower())
        return {"clubs": result, "count": len(result)}
    except Exception as e:
        logger.exception(f"Error fetching managed clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve managed clubs")


@router.put("/edit/{club_id}")
async def edit_club(club_id: str, body: UpdateClubRequest, current_user_id: str = Depends(get_current_user_id)):
    """Update a club's info. Club owner or Managers can edit."""
    try:
        supabase = get_supabase()
        if not is_club_owner_or_admin(club_id, current_user_id):
            raise HTTPException(status_code=403, detail="Only the club owner or admins can edit this club")

        update_data = {k: v for k, v in body.dict().items() if v is not None}
        if not update_data:
            return {"success": True, "message": "No changes"}

        supabase.table("clubs").update(update_data).eq("id", club_id).execute()
        # Return updated club
        updated = supabase.table("clubs").select("*").eq("id", club_id).execute()
        return {"success": True, "club": (updated.data or [None])[0]}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error editing club: {e}")
        raise HTTPException(status_code=500, detail="Failed to update club")


@router.delete("/{club_id}")
async def delete_club(club_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Delete a club. Only platform admin users can delete any club."""
    if not is_admin_user(current_user_id):
        raise HTTPException(status_code=403, detail="Only admins can delete clubs")
    try:
        supabase = get_supabase()
        # Remove all user_clubs references first
        supabase.table("user_clubs").delete().eq("club_id", club_id).execute()
        # Delete the club
        supabase.table("clubs").delete().eq("id", club_id).execute()
        return {"success": True, "message": "Club deleted"}
    except Exception as e:
        logger.exception(f"Error deleting club: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete club")
