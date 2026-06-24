"""
Background job status helpers (Supabase-backed).

All writes use the service-role client so they bypass RLS.
Users can read their own rows via the anon/auth client (see RLS policy).
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Optional

from .supabase_client import get_supabase

logger = logging.getLogger(__name__)


def create_job(job_id: str, user_id: str, kind: str, dry_run: bool = False) -> None:
    get_supabase().table("jobs").insert({
        "id":         job_id,
        "user_id":    user_id,
        "kind":       kind,
        "status":     "pending",
        "dry_run":    dry_run,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }).execute()


def update_job(
    job_id: str,
    status: str,
    result: Optional[Any] = None,
    error: Optional[str] = None,
) -> None:
    patch: dict = {
        "status":     status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if result is not None:
        patch["result"] = result
    if error is not None:
        patch["error"] = error[:2000]  # cap so it fits comfortably in the column
    try:
        get_supabase().table("jobs").update(patch).eq("id", job_id).execute()
    except Exception as exc:
        logger.warning("jobs update failed job=%s status=%s: %s", job_id, status, exc)


def get_job(job_id: str, user_id: str) -> Optional[dict]:
    """Return the job row or None if not found / not owned by user_id."""
    row = (
        get_supabase()
        .table("jobs")
        .select("id, user_id, kind, status, dry_run, result, error, created_at, updated_at")
        .eq("id", job_id)
        .eq("user_id", user_id)
        .execute()
    )
    return row.data[0] if row.data else None
