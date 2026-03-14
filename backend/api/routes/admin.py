"""
backend/api/routes/admin.py

Backend admin authentication endpoint.
- Uses constant-time comparison (hmac.compare_digest) to prevent timing attacks.
- Separate ADMIN_SECRET from CRON_SECRET — login no longer leaks CRON_SECRET (F-03).
  Instead, a short-lived signed admin session token is issued (15-minute expiry).
- Brute-force protection is now Supabase-backed (F-05) so the 5-attempt limit
  is shared across all serverless instances. Falls back to in-memory on DB error.
"""
import hashlib
import hmac
import logging
import time
from collections import defaultdict
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request, status
from pydantic import BaseModel

from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# ── Admin session token ───────────────────────────────────────────────────────
# Format: "admin:<exp_unix_timestamp>:<hmac_sha256_hex>"
# Signed with ADMIN_SECRET so the server can verify without storing sessions.

_ADMIN_TOKEN_TTL = 900  # 15 minutes (reduced from 1 hour for security)

# ── Token revocation list ─────────────────────────────────────────────────────
# In-memory set of revoked token signatures. Cleared on cold start, which is
# acceptable because tokens are short-lived (15 min) and worst case a revoked
# token survives until its natural expiry.
_revoked_tokens: set[str] = set()


def _issue_admin_token() -> str:
    """Issue a short-lived signed admin session token."""
    exp = int(time.time()) + _ADMIN_TOKEN_TTL
    payload = f"admin:{exp}"
    sig = hmac.new(
        settings.ADMIN_SECRET.encode(),
        payload.encode(),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}:{sig}"


def revoke_admin_token(token: str) -> None:
    """Add a token's signature to the revocation set."""
    parts = token.split(":")
    if len(parts) == 3:
        _revoked_tokens.add(parts[2])


def verify_admin_token(token: str) -> bool:
    """
    Verify a previously issued admin session token.
    Returns False if the token is malformed, expired, revoked, or has an invalid signature.
    """
    try:
        parts = token.split(":")
        if len(parts) != 3 or parts[0] != "admin":
            return False
        exp = int(parts[1])
        if time.time() > exp:
            # Lazily clean up expired entries from the revocation set
            _revoked_tokens.discard(parts[2])
            return False
        # Check revocation list before expensive HMAC
        if parts[2] in _revoked_tokens:
            return False
        payload = f"admin:{exp}"
        expected_sig = hmac.new(
            settings.ADMIN_SECRET.encode(),
            payload.encode(),
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(parts[2], expected_sig)
    except Exception:
        return False


# ── Brute-force protection (Supabase-backed, F-05) ────────────────────────────
# Attempts are stored in the same `rate_limits` table used by the main rate
# limiter so the counter is shared across all serverless instances.
# Falls back to an in-memory dict if Supabase is unavailable.

_ADMIN_RATE_LIMIT = 5    # max attempts per IP per window
_ADMIN_RATE_WINDOW = 60  # seconds

# In-memory fallback (used only when Supabase is down)
_fallback_attempts: dict[str, list[float]] = defaultdict(list)


def _check_admin_rate_limit(ip: str) -> None:
    """
    Block the request if this IP has exceeded the admin login attempt limit.
    Uses Supabase for shared state across instances; falls back to in-memory.
    Raises HTTP 429 if the limit is exceeded.
    """
    key = f"admin_login:{ip}"
    now = time.time()
    window_start_ts = now - _ADMIN_RATE_WINDOW

    # ── Try Supabase-backed check ─────────────────────────────────────────────
    try:
        from ..utils.supabase_client import get_supabase
        supabase = get_supabase()
        window_iso = datetime.now(timezone.utc).replace(second=0, microsecond=0).isoformat()

        try:
            result = supabase.rpc(
                "increment_rate_limit",
                {"p_key": key, "p_window": window_iso},
            ).execute()
            attempt_count = result.data
        except Exception:
            # RPC not available — two-step fallback (same as main rate limiter)
            read = (
                supabase.table("rate_limits")
                .select("count")
                .eq("key", key)
                .eq("window_start", window_iso)
                .execute()
            )
            if read.data:
                attempt_count = read.data[0]["count"] + 1
                supabase.table("rate_limits").update({
                    "count": attempt_count,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }).eq("key", key).eq("window_start", window_iso).execute()
            else:
                attempt_count = 1
                supabase.table("rate_limits").insert({
                    "key": key,
                    "window_start": window_iso,
                    "count": 1,
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }).execute()

        if attempt_count > _ADMIN_RATE_LIMIT:
            logger.warning(f"Admin brute-force lockout (Supabase) for IP: {ip}")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many login attempts. Please wait 60 seconds.",
            )
        return  # Supabase check passed

    except HTTPException:
        raise
    except Exception as e:
        logger.warning(f"Admin rate-limit DB error, falling back to in-memory: {e}")

    # ── In-memory fallback ────────────────────────────────────────────────────
    attempts = _fallback_attempts[ip]
    _fallback_attempts[ip] = [t for t in attempts if t > window_start_ts]
    if len(_fallback_attempts[ip]) >= _ADMIN_RATE_LIMIT:
        logger.warning(f"Admin brute-force lockout (in-memory fallback) for IP: {ip}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please wait 60 seconds.",
        )
    _fallback_attempts[ip].append(now)


# ── Request schema ────────────────────────────────────────────────────────────

class AdminLoginRequest(BaseModel):
    secret: str


# ── Route ─────────────────────────────────────────────────────────────────────

@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_admin(request: AdminLoginRequest, req: Request):
    """
    Verify the admin secret and issue a short-lived signed session token.

    - Authenticates with ADMIN_SECRET only (CRON_SECRET is never returned).
    - Issues a 15-minute signed token the frontend uses for subsequent admin calls.
    - Constant-time comparison prevents timing attacks.
    - Rate-limited to 5 attempts/minute per IP, Supabase-backed and shared
      across all serverless instances (falls back to in-memory if DB is down).
    """
    forwarded_for = req.headers.get("x-forwarded-for")
    if forwarded_for:
        # Use the rightmost entry — appended by Vercel's infrastructure,
        # not spoofable by the client (see main.py _get_client_ip for details).
        parts = [p.strip() for p in forwarded_for.split(",") if p.strip()]
        client_ip = parts[-1] if parts else "unknown"
    else:
        client_ip = req.client.host if req.client else "unknown"
    _check_admin_rate_limit(client_ip)

    admin_secret = settings.ADMIN_SECRET
    if not admin_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin access not configured",
        )

    if not hmac.compare_digest(request.secret, admin_secret):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    logger.info(f"Admin access granted from {client_ip}")
    # Return a scoped, time-limited admin session token — NOT the CRON_SECRET.
    return {
        "token": _issue_admin_token(),
        "expires_in": _ADMIN_TOKEN_TTL,
    }
