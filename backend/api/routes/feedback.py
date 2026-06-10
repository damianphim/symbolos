"""
Customer feedback inflow.

  POST /api/feedback — user-submitted feedback / bug report / missing course.

Previously the FeedbackModal only opened a `mailto:` link, which:
  * Fails silently if the user has no mail client configured (most
    students on a Chromebook / web-only setup).
  * Gives us no record.

This endpoint:
  1. Stores the feedback row (so nothing is ever lost).
  2. Emails the admin inbox via Resend (so we actually see it).
  3. Optionally posts to a Slack channel if SLACK_WEBHOOK_URL is set.

All three are best-effort and independent — a Slack outage doesn't stop
the email, a Resend outage doesn't stop the DB write.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from html import escape
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ..auth import get_current_user_id
from ..config import settings
from ..utils.supabase_client import get_supabase

router = APIRouter()
logger = logging.getLogger(__name__)

ADMIN_INBOX = os.getenv("SUPPORT_EMAIL", "symbolosadvsry@gmail.com")


class FeedbackIn(BaseModel):
    kind: str = Field("general", max_length=40)       # general | bug | missing-course
    message: str = Field(..., min_length=1, max_length=4000)
    course: Optional[str] = Field(None, max_length=40)
    page: Optional[str] = Field(None, max_length=300)  # where they were


@router.post("")
async def submit_feedback(
    body: FeedbackIn,
    current_user_id: str = Depends(get_current_user_id),
):
    sb = get_supabase()

    # Resolve the user's email for the reply-to (best effort).
    user_email = "unknown"
    try:
        u = sb.auth.admin.get_user(current_user_id)
        user_email = (getattr(u.user, "email", None) or "unknown")
    except Exception:
        pass

    safe_msg = escape(body.message.strip())
    safe_course = escape(body.course.strip()) if body.course else None
    safe_page = escape(body.page.strip()) if body.page else None

    # ── 1. Persist ────────────────────────────────────────────────────────────
    row = {
        "user_id":   current_user_id,
        "user_email": user_email,
        "kind":      body.kind,
        "message":   body.message.strip(),
        "course":    body.course.strip() if body.course else None,
        "page":      body.page.strip() if body.page else None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status":    "new",
    }
    try:
        sb.table("feedback").insert(row).execute()
    except Exception as exc:
        # Table may not exist yet — log and keep going so the email still fires.
        logger.warning("feedback insert failed: %s", type(exc).__name__)

    # ── 2. Email the admin inbox ──────────────────────────────────────────────
    if settings.RESEND_API_KEY:
        subject = f"[Symbolos feedback] {body.kind}" + (f" — {safe_course}" if safe_course else "")
        html = (
            f"<h2 style='font-family:sans-serif'>New {escape(body.kind)} feedback</h2>"
            f"<p style='font-family:sans-serif'><strong>From:</strong> {escape(user_email)}<br>"
            f"<strong>User ID:</strong> {escape(current_user_id)}<br>"
            + (f"<strong>Course:</strong> {safe_course}<br>" if safe_course else "")
            + (f"<strong>Page:</strong> {safe_page}<br>" if safe_page else "")
            + "</p>"
            f"<div style='font-family:sans-serif;white-space:pre-wrap;border-left:3px solid #ED1B2F;"
            f"padding-left:12px;color:#374151'>{safe_msg}</div>"
        )
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
                    json={
                        "from": "Symbolos <noreply@symbolos.ca>",
                        "to": [ADMIN_INBOX],
                        "reply_to": user_email if "@" in user_email else None,
                        "subject": subject,
                        "html": html,
                    },
                    timeout=10,
                )
        except Exception as exc:
            logger.warning("feedback email failed: %s", type(exc).__name__)

    # ── 3. Slack (optional) ───────────────────────────────────────────────────
    slack = os.getenv("SLACK_WEBHOOK_URL", "").strip()
    if slack:
        text = (
            f":speech_balloon: *{body.kind}* from `{user_email}`"
            + (f" · course `{body.course}`" if body.course else "")
            + (f" · page `{body.page}`" if body.page else "")
            + f"\n> {body.message.strip()[:500]}"
        )
        try:
            async with httpx.AsyncClient() as client:
                await client.post(slack, json={"text": text}, timeout=5)
        except Exception as exc:
            logger.debug("slack feedback post failed: %s", type(exc).__name__)

    return {"ok": True}
