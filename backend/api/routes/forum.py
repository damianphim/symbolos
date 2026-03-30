"""
backend/api/routes/forum.py

Community forum endpoints — posts, replies, and per-user likes.

All endpoints are auth-protected via get_current_user_id().
Likes use a separate junction table so a user cannot like the same
post/reply twice (enforced at the DB level by a PRIMARY KEY constraint).

SECURITY FIX: Added _check_report_rate_limit() to report_post and report_reply.
              Without this, any authenticated user could flood the admin inbox
              by calling the report endpoint in a tight loop (5 rpm per user).

Endpoints:
  GET    /api/forum/posts                   – list posts (filter, sort, paginate)
  POST   /api/forum/posts                   – create a post
  DELETE /api/forum/posts/{post_id}         – delete own post
  GET    /api/forum/posts/{post_id}/replies – list replies for a post
  POST   /api/forum/posts/{post_id}/replies – add a reply
  DELETE /api/forum/replies/{reply_id}      – delete own reply
  POST   /api/forum/posts/{post_id}/like    – toggle like on a post
  POST   /api/forum/replies/{reply_id}/like – toggle like on a reply
  POST   /api/forum/posts/{post_id}/report  – report a post to admins
  POST   /api/forum/replies/{reply_id}/report – report a reply to admins
"""

from fastapi import APIRouter, HTTPException, status, Depends, Request, Query
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
import logging
from html import escape

from ..utils.supabase_client import get_supabase, with_retry
from ..auth import get_current_user_id
from ..exceptions import DatabaseException
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

VALID_CATEGORIES = {"courses", "study", "advice", "general", "planning"}
VALID_SORTS      = {"hot", "new", "top"}


# ── Pydantic models ────────────────────────────────────────────────────────────

class PostCreate(BaseModel):
    author:       str  = Field(..., min_length=1, max_length=80)
    avatar_color: str  = Field("#ed1b2f", max_length=20)
    category:     str  = Field("general", max_length=30)
    title:        str  = Field(..., min_length=1, max_length=120)
    body:         str  = Field(..., min_length=1, max_length=5000)
    tags:         List[str] = Field(default_factory=list)
    program_info: Optional[str] = Field(None, max_length=200)

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        if v not in VALID_CATEGORIES:
            raise ValueError(f"category must be one of {VALID_CATEGORIES}")
        return v

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: List[str]) -> List[str]:
        cleaned = [t.strip()[:50] for t in v if t.strip()]
        return cleaned[:8]   # max 8 tags


class ReplyCreate(BaseModel):
    author:       str = Field(..., min_length=1, max_length=80)
    avatar_color: str = Field("#ed1b2f", max_length=20)
    body:         str = Field(..., min_length=1, max_length=2000)
    program_info: Optional[str] = Field(None, max_length=200)


# ── Helper: fetch liked IDs for a user ────────────────────────────────────────

def _get_liked_post_ids(supabase, user_id: str, post_ids: List[str]) -> set:
    if not post_ids:
        return set()
    try:
        res = (
            supabase.table("forum_post_likes")
            .select("post_id")
            .eq("user_id", user_id)
            .in_("post_id", post_ids)
            .execute()
        )
        return {r["post_id"] for r in (res.data or [])}
    except Exception:
        return set()


def _get_liked_reply_ids(supabase, user_id: str, reply_ids: List[str]) -> set:
    if not reply_ids:
        return set()
    try:
        res = (
            supabase.table("forum_reply_likes")
            .select("reply_id")
            .eq("user_id", user_id)
            .in_("reply_id", reply_ids)
            .execute()
        )
        return {r["reply_id"] for r in (res.data or [])}
    except Exception:
        return set()


# ── Report rate-limit helper ───────────────────────────────────────────────────

def _check_report_rate_limit(user_id: str) -> None:
    """
    Allow at most 5 forum reports per user per minute.
    Prevents a malicious user from flooding the admin inbox.
    Fails open (allows through) if the rate limiter is unavailable.
    """
    try:
        from api.main import _limiter
        if not _limiter.is_allowed(f"forum_report:{user_id}", rpm=5):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many reports submitted. Please wait a moment before reporting again.",
            )
    except HTTPException:
        raise
    except Exception:
        # Rate limiter unavailable — fail open so reporting still works
        pass


# ── GET /posts ────────────────────────────────────────────────────────────────

@router.get("/posts", response_model=dict)
async def list_posts(
    req:      Request,
    category: Optional[str] = Query(None),
    sort:     str            = Query("hot"),
    search:   Optional[str] = Query(None),
    limit:    int            = Query(30, ge=1, le=100),
    offset:   int            = Query(0,  ge=0),
    current_user_id: str     = Depends(get_current_user_id),
):
    """
    List forum posts.

    - category: filter by category slug
    - sort: hot | new | top
    - search: full-text filter on title + body
    - limit/offset: pagination
    """
    if sort not in VALID_SORTS:
        sort = "hot"

    def _run():
        supabase = get_supabase()
        q = supabase.table("forum_posts").select(
            "id, user_id, author, avatar_color, category, title, body, tags, program_info, like_count, created_at"
        )

        if category and category != "all" and category in VALID_CATEGORIES:
            q = q.eq("category", category)

        if search:
            safe = search.strip()[:100].replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
            q = q.or_(f"title.ilike.%{safe}%,body.ilike.%{safe}%")

        if sort == "new":
            q = q.order("created_at", desc=True)
        elif sort == "top":
            q = q.order("like_count", desc=True).order("created_at", desc=True)
        else:  # hot: like_count + recency hybrid handled in Python below
            q = q.order("created_at", desc=True)

        q = q.limit(limit + offset)  # fetch enough for offset
        return q.execute().data or []

    try:
        posts = with_retry("forum_list_posts", _run)
    except Exception as e:
        logger.error(f"forum list_posts error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch posts")

    # Hot sort: score = like_count * 2 + recency_bonus (Python-side for simplicity)
    if sort == "hot":
        import time
        now = time.time()
        def _hot_score(p):
            try:
                from datetime import datetime, timezone
                ts = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00"))
                age_hours = (now - ts.timestamp()) / 3600
                return p["like_count"] * 2 + max(0, 48 - age_hours)
            except Exception:
                return p["like_count"]
        posts.sort(key=_hot_score, reverse=True)

    posts = posts[offset:offset + limit]

    # Attach reply counts
    post_ids = [p["id"] for p in posts]
    reply_counts: dict = {}
    if post_ids:
        try:
            supabase = get_supabase()
            rc_res = (
                supabase.table("forum_replies")
                .select("post_id")
                .in_("post_id", post_ids)
                .execute()
            )
            for r in (rc_res.data or []):
                pid = r["post_id"]
                reply_counts[pid] = reply_counts.get(pid, 0) + 1
        except Exception:
            pass

    # Attach per-user liked status
    liked_ids = _get_liked_post_ids(get_supabase(), current_user_id, post_ids)

    for p in posts:
        p["reply_count"] = reply_counts.get(p["id"], 0)
        p["liked"] = p["id"] in liked_ids

    return {"posts": posts, "total": len(posts)}


# ── POST /posts ───────────────────────────────────────────────────────────────

@router.post("/posts", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_post(
    payload: PostCreate,
    req:     Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Create a new forum post. Auth required."""
    def _run():
        supabase = get_supabase()
        data = {
            "user_id":      current_user_id,
            "author":       payload.author,
            "avatar_color": payload.avatar_color,
            "category":     payload.category,
            "title":        payload.title,
            "body":         payload.body,
            "tags":         payload.tags,
            "program_info": payload.program_info,
        }
        res = supabase.table("forum_posts").insert(data).execute()
        if not res.data:
            raise DatabaseException("create_post", "No data returned")
        return res.data[0]

    try:
        post = with_retry("forum_create_post", _run)
        post["reply_count"] = 0
        post["liked"] = False
        logger.info(f"Forum post created by {current_user_id}: {post['id']}")
        return {"post": post}
    except DatabaseException:
        raise HTTPException(status_code=500, detail="Failed to create post")
    except Exception as e:
        logger.exception(f"Unexpected error creating forum post: {e}")
        raise HTTPException(status_code=500, detail="Failed to create post")


# ── DELETE /posts/{post_id} ───────────────────────────────────────────────────

@router.delete("/posts/{post_id}", response_model=dict)
async def delete_post(
    post_id: str,
    req:     Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Delete own forum post."""
    try:
        supabase = get_supabase()
        existing = supabase.table("forum_posts").select("user_id").eq("id", post_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Post not found")
        if existing.data[0]["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Not your post")
        supabase.table("forum_posts").delete().eq("id", post_id).execute()
        return {"message": "Post deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error deleting forum post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete post")


# ── GET /posts/{post_id}/replies ──────────────────────────────────────────────

@router.get("/posts/{post_id}/replies", response_model=dict)
async def list_replies(
    post_id: str,
    req:     Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Fetch all replies for a post, oldest-first."""
    def _run():
        supabase = get_supabase()
        return (
            supabase.table("forum_replies")
            .select("id, post_id, user_id, author, avatar_color, body, program_info, like_count, created_at")
            .eq("post_id", post_id)
            .order("created_at", desc=False)
            .execute()
            .data or []
        )

    try:
        replies = with_retry("forum_list_replies", _run)
    except Exception as e:
        logger.error(f"forum list_replies error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch replies")

    # Attach per-user liked status
    reply_ids = [r["id"] for r in replies]
    liked_ids = _get_liked_reply_ids(get_supabase(), current_user_id, reply_ids)
    for r in replies:
        r["liked"] = r["id"] in liked_ids

    return {"replies": replies}


# ── POST /posts/{post_id}/replies ─────────────────────────────────────────────

@router.post("/posts/{post_id}/replies", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_reply(
    post_id: str,
    payload: ReplyCreate,
    req:     Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Add a reply to a post."""
    def _run():
        supabase = get_supabase()
        post_check = supabase.table("forum_posts").select("id").eq("id", post_id).execute()
        if not post_check.data:
            raise HTTPException(status_code=404, detail="Post not found")
        data = {
            "post_id":      post_id,
            "user_id":      current_user_id,
            "author":       payload.author,
            "avatar_color": payload.avatar_color,
            "body":         payload.body,
            "program_info": payload.program_info,
        }
        res = supabase.table("forum_replies").insert(data).execute()
        if not res.data:
            raise DatabaseException("create_reply", "No data returned")
        return res.data[0]

    try:
        reply = with_retry("forum_create_reply", _run)
        reply["liked"] = False
        logger.info(f"Forum reply created by {current_user_id} on post {post_id}")
        return {"reply": reply}
    except HTTPException:
        raise
    except DatabaseException:
        raise HTTPException(status_code=500, detail="Failed to create reply")
    except Exception as e:
        logger.exception(f"Unexpected error creating reply: {e}")
        raise HTTPException(status_code=500, detail="Failed to create reply")


# ── DELETE /replies/{reply_id} ────────────────────────────────────────────────

@router.delete("/replies/{reply_id}", response_model=dict)
async def delete_reply(
    reply_id: str,
    req:      Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Delete own reply."""
    try:
        supabase = get_supabase()
        existing = supabase.table("forum_replies").select("user_id").eq("id", reply_id).execute()
        if not existing.data:
            raise HTTPException(status_code=404, detail="Reply not found")
        if existing.data[0]["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Not your reply")
        supabase.table("forum_replies").delete().eq("id", reply_id).execute()
        return {"message": "Reply deleted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error deleting reply {reply_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete reply")


# ── POST /posts/{post_id}/like ────────────────────────────────────────────────

@router.post("/posts/{post_id}/like", response_model=dict)
async def toggle_post_like(
    post_id: str,
    req:     Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Toggle like on a post. Returns {liked: bool, like_count: int}."""
    try:
        supabase = get_supabase()

        existing = (
            supabase.table("forum_post_likes")
            .select("user_id")
            .eq("user_id", current_user_id)
            .eq("post_id", post_id)
            .execute()
        )
        already_liked = bool(existing.data)

        if already_liked:
            supabase.table("forum_post_likes").delete() \
                .eq("user_id", current_user_id).eq("post_id", post_id).execute()
            supabase.rpc("decrement_post_like", {"p_post_id": post_id}).execute()
        else:
            supabase.table("forum_post_likes").insert(
                {"user_id": current_user_id, "post_id": post_id}
            ).execute()
            supabase.rpc("increment_post_like", {"p_post_id": post_id}).execute()

        post_res = supabase.table("forum_posts").select("like_count").eq("id", post_id).execute()
        like_count = post_res.data[0]["like_count"] if post_res.data else 0

        return {"liked": not already_liked, "like_count": like_count}

    except Exception as e:
        logger.exception(f"Error toggling post like: {e}")
        raise HTTPException(status_code=500, detail="Failed to toggle like")


# ── POST /replies/{reply_id}/like ─────────────────────────────────────────────

@router.post("/replies/{reply_id}/like", response_model=dict)
async def toggle_reply_like(
    reply_id: str,
    req:      Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Toggle like on a reply."""
    try:
        supabase = get_supabase()

        existing = (
            supabase.table("forum_reply_likes")
            .select("user_id")
            .eq("user_id", current_user_id)
            .eq("reply_id", reply_id)
            .execute()
        )
        already_liked = bool(existing.data)

        if already_liked:
            supabase.table("forum_reply_likes").delete() \
                .eq("user_id", current_user_id).eq("reply_id", reply_id).execute()
            supabase.rpc("decrement_reply_like", {"p_reply_id": reply_id}).execute()
        else:
            supabase.table("forum_reply_likes").insert(
                {"user_id": current_user_id, "reply_id": reply_id}
            ).execute()
            supabase.rpc("increment_reply_like", {"p_reply_id": reply_id}).execute()

        reply_res = supabase.table("forum_replies").select("like_count").eq("id", reply_id).execute()
        like_count = reply_res.data[0]["like_count"] if reply_res.data else 0

        return {"liked": not already_liked, "like_count": like_count}

    except Exception as e:
        logger.exception(f"Error toggling reply like: {e}")
        raise HTTPException(status_code=500, detail="Failed to toggle like")


# ── Helpers: report email ──────────────────────────────────────────────────────

def _send_report_email(content_type: str, content_id: str, reporter_id: str,
                       author: str, preview: str):
    """Send a report notification email to all admin addresses."""
    if not settings.RESEND_API_KEY:
        return
    admin_emails = [e.strip() for e in settings.ADMIN_EMAILS.split(",") if e.strip()]
    if not admin_emails:
        return

    safe_type     = escape(content_type)
    safe_id       = escape(content_id)
    safe_author   = escape(author or "Unknown")
    safe_preview  = escape((preview or "")[:300])
    safe_reporter = escape(reporter_id)

    subject = f"🚩 Forum {safe_type} reported — Symbolos"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:32px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;">
        <tr><td style="background:#ED1B2F;border-radius:12px 12px 0 0;padding:20px 28px;">
          <span style="color:#fff;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;opacity:0.85;">Symbolos</span>
        </td></tr>
        <tr><td style="background:#ffffff;padding:28px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">
          <span style="display:inline-block;background:#fff7ed;color:#f97316;font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">Content Report</span>
          <h2 style="margin:16px 0 8px;font-size:20px;font-weight:700;color:#111827;">Forum {safe_type.capitalize()} Reported</h2>
          <p style="margin:0 0 20px;font-size:14px;color:#6b7280;">A forum {safe_type} has been flagged for review.</p>
          <table width="100%" cellpadding="0" cellspacing="0" style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:16px;margin-bottom:20px;">
            <tr><td style="padding:4px 0;font-size:13px;color:#374151;"><strong>Type:</strong> {safe_type.capitalize()}</td></tr>
            <tr><td style="padding:4px 0;font-size:13px;color:#374151;"><strong>Content ID:</strong> {safe_id}</td></tr>
            <tr><td style="padding:4px 0;font-size:13px;color:#374151;"><strong>Author:</strong> {safe_author}</td></tr>
            <tr><td style="padding:4px 0;font-size:13px;color:#374151;"><strong>Reported by:</strong> {safe_reporter}</td></tr>
            <tr><td style="padding:12px 0 4px;font-size:13px;color:#374151;"><strong>Content preview:</strong></td></tr>
            <tr><td style="padding:8px 12px;background:#fff;border:1px solid #e5e7eb;border-radius:6px;font-size:13px;color:#6b7280;font-style:italic;">{safe_preview}</td></tr>
          </table>
          <p style="margin:0;font-size:12px;color:#9ca3af;">Please review this content in the Symbolos admin panel.</p>
        </td></tr>
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;">
          <p style="margin:0;font-size:11px;color:#9ca3af;">Symbolos Admin Notification</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""

    try:
        import httpx
        httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json"},
            json={"from": "Symbolos <notifications@symbolos.ca>", "to": admin_emails,
                  "subject": subject, "html": html},
            timeout=8,
        )
    except Exception as exc:
        logger.warning(f"Failed to send report email: {exc}")


# ── POST /posts/{post_id}/report ───────────────────────────────────────────────

@router.post("/posts/{post_id}/report", response_model=dict)
async def report_post(
    post_id: str,
    req:     Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Flag a post for review. Sends an email to admins."""
    _check_report_rate_limit(current_user_id)
    try:
        supabase = get_supabase()
        post_res = supabase.table("forum_posts").select("user_id, author, title, body").eq("id", post_id).execute()
        if not post_res.data:
            raise HTTPException(status_code=404, detail="Post not found")
        p = post_res.data[0]
        if p["user_id"] == current_user_id:
            raise HTTPException(status_code=400, detail="You cannot report your own post")
        preview = f"{p.get('title', '')} — {p.get('body', '')}"
        _send_report_email("post", post_id, current_user_id, p.get("author", ""), preview)
        logger.info(f"Post {post_id} reported by {current_user_id}")
        return {"message": "Report submitted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error reporting post {post_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit report")


# ── POST /replies/{reply_id}/report ───────────────────────────────────────────

@router.post("/replies/{reply_id}/report", response_model=dict)
async def report_reply(
    reply_id: str,
    req:      Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """Flag a reply for review. Sends an email to admins."""
    _check_report_rate_limit(current_user_id)
    try:
        supabase = get_supabase()
        reply_res = supabase.table("forum_replies").select("user_id, author, body").eq("id", reply_id).execute()
        if not reply_res.data:
            raise HTTPException(status_code=404, detail="Reply not found")
        r = reply_res.data[0]
        if r["user_id"] == current_user_id:
            raise HTTPException(status_code=400, detail="You cannot report your own reply")
        _send_report_email("reply", reply_id, current_user_id, r.get("author", ""), r.get("body", ""))
        logger.info(f"Reply {reply_id} reported by {current_user_id}")
        return {"message": "Report submitted"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error reporting reply {reply_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit report")