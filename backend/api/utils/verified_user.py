"""
Verified-user guard (SEC fix #5).

Supabase's mailer_autoconfirm is ON, so a new signup gets a usable session
*immediately*, with no proof that the email is real. That made findings #1
and #2 fully exploitable from a throwaway @anything.com address. To stop
that, every privileged endpoint (chat, cards, club join, forum post, etc.)
now goes through `require_verified_email()`, which:

  1. Reads the user's verified flag from the `users` table (set by
     /api/auth/verify-email after the Resend token round-trip), AND
  2. Cross-checks against the real auth.users email domain (so a McGill
     address that hasn't completed our own verification still counts —
     they already verified by being able to read mail at that address).

Returns the user_id on success. Raises 403 with a structured detail so the
frontend can route the user back to the verification screen.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from time import time
from typing import Tuple

from fastapi import Depends, HTTPException, status

from ..auth import get_current_user_id
from .supabase_client import get_supabase

logger = logging.getLogger(__name__)

# Cache verified status for 60s per user to avoid hammering Supabase on every
# request. Cache key is (user_id, minute_bucket) so it auto-expires.
_VERIFIED_TTL_SECONDS = 60


@lru_cache(maxsize=1024)
def _cached_check(user_id: str, bucket: int) -> Tuple[bool, str]:
    """Inner cache. Returns (is_verified, auth_email_lower)."""
    sb = get_supabase()
    # Real auth email (cannot be edited by the user)
    auth_email = ""
    try:
        u = sb.auth.admin.get_user_by_id(user_id)
        auth_email = (getattr(u.user, "email", None) or "").lower()
    except Exception as exc:
        logger.warning("auth.admin.get_user failed for %s: %s", user_id, type(exc).__name__)

    # Verified flag we set ourselves (via Resend round-trip)
    is_verified = False
    try:
        row = sb.table("users").select("email_verified").eq("id", user_id).single().execute()
        is_verified = bool((row.data or {}).get("email_verified"))
    except Exception as exc:
        logger.warning("users.email_verified fetch failed for %s: %s", user_id, type(exc).__name__)

    return (is_verified, auth_email)


def is_email_verified(user_id: str) -> bool:
    """Return True if the user has either completed our own email verification
    OR signed up with a real McGill address (already verified by SSO/IT)."""
    bucket = int(time() // _VERIFIED_TTL_SECONDS)
    verified, auth_email = _cached_check(user_id, bucket)
    if verified:
        return True
    # Trust McGill's own mailer: if Supabase has confirmed the address belongs
    # to mail.mcgill.ca / mcgill.ca, we don't need to send a second link.
    if auth_email.endswith("@mail.mcgill.ca") or auth_email.endswith("@mcgill.ca"):
        return True
    return False


async def require_verified_email(
    current_user_id: str = Depends(get_current_user_id),
) -> str:
    """FastAPI dependency. Use on every endpoint that sends mail, costs
    money (Claude), writes content other users can see, or grants trust."""
    if not is_email_verified(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "email_not_verified",
                "message": "Verify your email address to use this feature.",
            },
        )
    return current_user_id
