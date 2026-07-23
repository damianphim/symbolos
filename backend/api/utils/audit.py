"""
Append-only audit log for sensitive data access.

Called on: transcript reads, data exports, admin profile views, and account
deletion. Records who accessed what and from where so that, if a user ever
reports unexpected data access, we can reconstruct the timeline.

Best-effort: a DB failure here MUST NOT break the calling endpoint.
Never log PII in the `resource` field — use IDs only.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Optional

from fastapi import Request

from .supabase_client import get_supabase

logger = logging.getLogger(__name__)


def log_access(
    user_id: Optional[str],
    action: str,
    resource: Optional[str] = None,
    req: Optional[Request] = None,
) -> None:
    """Write one append-only row to audit_log.

    action   — short label, e.g. 'transcript_read', 'data_export',
               'account_delete', 'admin_login', 'admin_view_feedback'
    resource — optional ID of the thing accessed, e.g. a user_id or table name
    req      — FastAPI Request, used to capture IP and User-Agent

    user_id may be None for actions with no single target user (e.g. an
    admin login, or an admin bulk-viewing a list) — the row is still
    written, just without the FK to auth.users. Do NOT pass a falsy
    placeholder to force a no-op; omit the call instead.
    """
    if not action:
        return

    ip = user_agent = None
    if req:
        forwarded = req.headers.get("x-forwarded-for")
        ip = (forwarded.split(",")[0].strip() if forwarded else None) or str(req.client.host) if req.client else None
        user_agent = req.headers.get("user-agent")

    try:
        get_supabase().table("audit_log").insert({
            "user_id":    user_id,
            "action":     action,
            "resource":   resource,
            "ip":         ip,
            "user_agent": user_agent,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }).execute()
    except Exception as exc:
        logger.debug("audit log DB failure: %s", type(exc).__name__)
