"""
Per-user LLM budget gate (SEC fix #7).

The auditor pointed out that /api/chat/send happily returns model output to
any signed-up account with no per-user cap. The existing RATE_LIMIT_PER_MINUTE
limits burst, but at 25 req/min an attacker can still rack up ~36k requests
per day, which is real money on Claude.

This helper enforces a coarser-grained daily request counter per user, stored
in the existing `rate_limits` table (sliding-window rows we already prune).
Default: 200 chat-class requests + 40 card-class generations per day. Admins
exempt. The numbers are deliberately generous — a real student plowing
through assignment week will rarely hit 50/day.

Tunable via env: LLM_BUDGET_CHAT_PER_DAY, LLM_BUDGET_CARDS_PER_DAY.
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone

from fastapi import HTTPException, status

from ..config import settings

logger = logging.getLogger(__name__)


def _budget_for(kind: str) -> int:
    if kind == "chat":
        return int(os.getenv("LLM_BUDGET_CHAT_PER_DAY", "200"))
    if kind == "cards":
        return int(os.getenv("LLM_BUDGET_CARDS_PER_DAY", "40"))
    if kind == "electives":
        return int(os.getenv("LLM_BUDGET_ELECTIVES_PER_DAY", "20"))
    if kind == "transcript":
        return int(os.getenv("LLM_BUDGET_TRANSCRIPT_PER_DAY", "8"))
    return int(os.getenv("LLM_BUDGET_DEFAULT_PER_DAY", "100"))


def _is_admin_user(user_id: str) -> bool:
    """Look up if user is in ADMIN_EMAILS by auth email."""
    try:
        from .supabase_client import get_supabase
        sb = get_supabase()
        u = sb.auth.admin.get_user_by_id(user_id)
        email = (getattr(u.user, "email", None) or "").lower()
        admin_emails = {e.strip().lower() for e in settings.ADMIN_EMAILS.split(",") if e.strip()}
        return email in admin_emails
    except Exception:
        return False


def check_and_record_llm_usage(user_id: str, kind: str = "chat") -> None:
    """Block the request with 429 if this user has spent their daily budget
    for this LLM-call class. Otherwise record one unit of usage.

    The counter rolls over at UTC midnight. Admins are exempt.
    """
    if _is_admin_user(user_id):
        return
    limit = _budget_for(kind)
    now = datetime.now(timezone.utc)
    bucket = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    key = f"llm_budget:{kind}:{user_id}"

    try:
        from .supabase_client import get_supabase
        sb = get_supabase()
        read = (
            sb.table("rate_limits")
            .select("count")
            .eq("key", key)
            .eq("window_start", bucket)
            .execute()
        )
        if read.data:
            count = (read.data[0].get("count") or 0)
            if count >= limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail={
                        "code": "llm_budget_exceeded",
                        "message": (
                            f"Daily {kind} limit reached ({limit}/day). "
                            "The counter resets at midnight UTC."
                        ),
                    },
                )
            sb.table("rate_limits").update({
                "count": count + 1,
                "updated_at": now.isoformat(),
            }).eq("key", key).eq("window_start", bucket).execute()
        else:
            sb.table("rate_limits").insert({
                "key": key,
                "window_start": bucket,
                "count": 1,
                "updated_at": now.isoformat(),
            }).execute()
    except HTTPException:
        raise
    except Exception as exc:
        # Fail open on DB outage — losing a few tracked calls is acceptable;
        # blocking every user because the limiter is broken is not. The
        # global IP rate limiter is still in force.
        logger.warning("llm_budget DB failure: %s", type(exc).__name__)
