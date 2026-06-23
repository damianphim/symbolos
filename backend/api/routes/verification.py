"""
Email verification via Resend — bypasses Supabase's rate-limited built-in mailer.

Endpoints:
  POST /api/auth/send-verification  — generate token, store in DB, send Resend email
  POST /api/auth/verify-email       — validate token, mark email_verified = true

SEC FIX #1 (CRITICAL): the previous version trusted the request body for
user_id, email, and redirect_url. That meant anyone could mail
"verify your Symbolos account" links from noreply@symbolos.ca to any
recipient, pointing at any URL, with a valid token bound to any account.
The fix:

  * /send-verification now derives user_id from the Bearer JWT and pulls
    the address straight from auth.users (the verified Supabase identity).
    The request body is empty.
  * redirect_url is hard-allowlisted to the production / staging frontend
    origins from config.ALLOWED_ORIGINS — never user-controlled.
  * Per-user throttle (1 email per 60s, 6 per day) on top of the global
    IP-tier rate limit so a logged-in attacker can't spam the mailer.
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Tuple

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.auth import get_current_user_id
from api.config import settings
from api.utils.supabase_client import get_supabase, with_retry

router = APIRouter()
logger = logging.getLogger(__name__)

TOKEN_TTL_HOURS = 24

# Per-user throttle: at most one verification mail every 60 seconds, and at
# most 6 over a rolling day. Tracked in the `rate_limits` table keyed by
# "verify_send:<user_id>".
_SEND_MIN_INTERVAL_SECONDS = 60
_SEND_DAILY_MAX = 6


class VerifyEmailRequest(BaseModel):
    user_id: str
    token: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _allowed_redirect_origins() -> list[str]:
    """Production + staging frontend origins. Never trust client input."""
    raw = settings.ALLOWED_ORIGINS
    if isinstance(raw, str):
        items = [o.strip() for o in raw.split(",") if o.strip()]
    else:
        items = [str(o).strip() for o in (raw or []) if str(o).strip()]
    # Drop localhost in production builds — a phishing landing on
    # localhost is harmless, but we shouldn't be mailing it either.
    if settings.ENVIRONMENT == "production":
        items = [o for o in items if not o.startswith("http://localhost")]
    return items


def _primary_frontend_origin() -> str:
    """First allowed origin = the canonical frontend URL we mail."""
    origins = _allowed_redirect_origins()
    if not origins:
        raise HTTPException(status_code=500, detail="No frontend origin configured")
    # Prefer the apex domain if present (symbolos.ca > vercel preview).
    for o in origins:
        if o.endswith("symbolos.ca"):
            return o
    return origins[0]


def _check_send_throttle(user_id: str) -> None:
    """1/min + 6/day per-user. Uses the rate_limits table so the counter is
    shared across all serverless instances."""
    sb = get_supabase()
    now = datetime.now(timezone.utc)

    # 1-per-60s gate: stored in the user's row as last_verification_sent_at.
    try:
        row = (
            sb.table("users")
            .select("last_verification_sent_at")
            .eq("id", user_id)
            .single()
            .execute()
        )
        last = (row.data or {}).get("last_verification_sent_at")
        if last:
            try:
                last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
                if (now - last_dt).total_seconds() < _SEND_MIN_INTERVAL_SECONDS:
                    raise HTTPException(
                        status_code=429,
                        detail="Please wait a minute before requesting another verification email.",
                    )
            except ValueError:
                pass  # malformed timestamp — ignore, let the day-counter catch abuse
    except HTTPException:
        raise
    except Exception:
        pass  # column may not exist yet on a fresh DB

    # Day-counter via rate_limits table (24h bucket).
    bucket = now.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    key = f"verify_send:{user_id}"
    try:
        read = (
            sb.table("rate_limits")
            .select("count")
            .eq("key", key)
            .eq("window_start", bucket)
            .execute()
        )
        if read.data and (read.data[0].get("count") or 0) >= _SEND_DAILY_MAX:
            raise HTTPException(
                status_code=429,
                detail="Daily verification-email limit reached. Try again tomorrow.",
            )
        if read.data:
            sb.table("rate_limits").update({
                "count": (read.data[0].get("count") or 0) + 1,
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
        logger.warning("verify_send rate_limit DB failure: %s", type(exc).__name__)
        # Fail open on DB outage — the per-user 60s gate + the global IP
        # limiter are still in force.


def _resolve_auth_email(user_id: str) -> str:
    """Pull the verified email straight from auth.users — NOT the
    user-editable profile column."""
    sb = get_supabase()
    try:
        u = sb.auth.admin.get_user_by_id(user_id)
        email = (getattr(u.user, "email", None) or "").strip()
        if not email:
            raise HTTPException(status_code=400, detail="No email on file for this account")
        return email
    except HTTPException:
        raise
    except Exception as exc:
        logger.warning("auth.admin.get_user failed for %s: %s", user_id, type(exc).__name__)
        raise HTTPException(status_code=500, detail="Could not resolve account email")


def _hash_token(token: str) -> str:
    """HMAC-SHA256 of the token using ADMIN_SECRET. Storing only the hash
    means a DB leak does not yield usable verification links."""
    return hmac.new(
        settings.ADMIN_SECRET.encode("utf-8"),
        token.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/send-verification")
async def send_verification(
    current_user_id: str = Depends(get_current_user_id),
):
    """Re-send the verification email for the *currently authenticated* user.

    Body is empty — every field that used to be client-supplied (user_id,
    email, redirect_url) is now server-derived. See module docstring for
    the threat model that motivated this rewrite.
    """
    if not settings.RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="Email service not configured")

    _check_send_throttle(current_user_id)

    email = _resolve_auth_email(current_user_id)
    frontend_origin = _primary_frontend_origin()

    # Use a cryptographically random token (was uuid.uuid4, which is fine,
    # but secrets.token_urlsafe is the conventional choice and gives 256
    # bits without dashes).
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS)).isoformat()

    def _store():
        # We store the HASH not the raw token. The raw token only ever
        # exists in the outgoing email and the user's clicked link.
        get_supabase().table("users").update({
            "verification_token": token_hash,
            "verification_token_expires_at": expires_at,
            "email_verified": False,
            "last_verification_sent_at": datetime.now(timezone.utc).isoformat(),
        }).eq("id", current_user_id).execute()

    with_retry("store_verification_token", _store)

    # Build the verify URL from a server-controlled origin only.
    verify_url = f"{frontend_origin}/?verify_token={token}&user_id={current_user_id}"

    html = _verification_html(verify_url)

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
            json={
                "from": "Symbolos <noreply@symbolos.ca>",
                "to": [email],
                "subject": "Verify your Symbolos account",
                "html": html,
            },
            timeout=10,
        )
        if resp.status_code not in (200, 201):
            logger.error("Resend error %s", resp.status_code)
            raise HTTPException(status_code=502, detail="Failed to send verification email")

    logger.info("Verification email sent to user %s", current_user_id)
    return {"ok": True}


@router.get("/check-verified/{user_id}")
async def check_verified(user_id: str):
    """Unauthenticated poll used by the verify screen on the original signup
    tab.  When Supabase autoconfirm is OFF the tab has no session, so we
    cannot use any authenticated endpoint.  This returns whether the address
    has been confirmed via either Supabase's own magic-link or our custom
    Resend token, and syncs our users.email_verified column as a side-effect.

    Information-disclosure risk is low: the response is a boolean, the
    user_id is a UUID (not guessable), and this is rate-limited by the
    existing IP-level FastAPI middleware.
    """
    sb = get_supabase()
    verified = False

    # 1. Check Supabase Auth — set by partner's magic-link flow.
    try:
        u = sb.auth.admin.get_user_by_id(user_id)
        if u.user and getattr(u.user, "email_confirmed_at", None):
            verified = True
    except Exception:
        pass

    # 2. Fall back to our own column (set by /verify-email Resend flow).
    if not verified:
        try:
            row = (
                sb.table("users")
                .select("email_verified")
                .eq("id", user_id)
                .single()
                .execute()
            )
            verified = bool((row.data or {}).get("email_verified"))
        except Exception:
            pass

    # Sync our column so authenticated profile fetches also see the flag.
    if verified:
        try:
            sb.table("users").update({"email_verified": True}).eq("id", user_id).execute()
        except Exception:
            pass

    return {"verified": verified}


@router.post("/verify-email")
async def verify_email(req: VerifyEmailRequest):
    """Consume a verification token. Unauthenticated (the click comes from
    an email link before the user is signed in). Constant-time compare on
    the HMAC of the supplied token vs. the stored hash."""
    def _fetch():
        return get_supabase().table("users").select(
            "verification_token, verification_token_expires_at"
        ).eq("id", req.user_id).execute()

    result = with_retry("fetch_verification_token", _fetch)

    if not result.data:
        # Generic message — don't tell an attacker which user_ids exist.
        raise HTTPException(status_code=400, detail="Invalid or already-used verification link")

    row = result.data[0]
    stored_hash = (row.get("verification_token") or "")
    supplied_hash = _hash_token(req.token or "")

    if not stored_hash or not hmac.compare_digest(stored_hash, supplied_hash):
        raise HTTPException(status_code=400, detail="Invalid or already-used verification link")

    expires_str = row.get("verification_token_expires_at")
    if expires_str:
        try:
            expires_at = datetime.fromisoformat(expires_str.replace("Z", "+00:00"))
            if expires_at < datetime.now(timezone.utc):
                raise HTTPException(
                    status_code=400,
                    detail="Verification link has expired. Please request a new one.",
                )
        except ValueError:
            raise HTTPException(status_code=400, detail="Verification link is malformed.")

    def _confirm():
        get_supabase().table("users").update({
            "email_verified": True,
            "verification_token": None,
            "verification_token_expires_at": None,
        }).eq("id", req.user_id).execute()

    with_retry("confirm_email", _confirm)
    logger.info("Email verified for user %s", req.user_id)
    return {"ok": True}


# ── Email HTML — unchanged design, factored out for readability ───────────────

def _verification_html(verify_url: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:40px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">
        <tr><td style="background:linear-gradient(135deg,#ED1B2F 0%,#B01B2E 100%);border-radius:12px 12px 0 0;padding:24px 32px;">
          <table width="100%" cellpadding="0" cellspacing="0"><tr>
            <td><span style="color:#fff;font-size:20px;font-weight:800;letter-spacing:-0.5px;">Symbolos</span></td>
            <td align="right"><span style="color:rgba(255,255,255,0.7);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Email Verification</span></td>
          </tr></table>
        </td></tr>
        <tr><td style="background:#ffffff;padding:36px 32px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">
          <h1 style="font-size:22px;font-weight:700;color:#111827;margin:0 0 12px;">Verify your email address</h1>
          <p style="font-size:15px;color:#4b5563;margin:0 0 8px;line-height:1.65;">
            Thanks for signing up for Symbolos — your AI-powered McGill academic advisor.
          </p>
          <p style="font-size:15px;color:#4b5563;margin:0 0 28px;line-height:1.65;">
            Click the button below to confirm your email address and activate your account.
          </p>
          <div style="text-align:center;margin-bottom:28px;">
            <a href="{verify_url}"
               style="display:inline-block;background:linear-gradient(135deg,#ED1B2F 0%,#B01B2E 100%);
                      color:#ffffff;padding:14px 36px;border-radius:8px;
                      text-decoration:none;font-weight:700;font-size:15px;
                      letter-spacing:0.01em;box-shadow:0 2px 8px rgba(237,27,47,0.3);">
              Verify email address →
            </a>
          </div>
          <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:14px 16px;margin-bottom:24px;">
            <p style="font-size:12px;color:#6b7280;margin:0;line-height:1.6;">
              🔒 This link expires in <strong>{TOKEN_TTL_HOURS} hours</strong> and can only be used once.<br>
              If the button doesn't work, copy and paste this URL into your browser:<br>
              <span style="word-break:break-all;color:#ED1B2F;font-size:11px;">{verify_url}</span>
            </p>
          </div>
          <p style="font-size:13px;color:#9ca3af;margin:0;line-height:1.6;">
            If you didn't request this email, you can safely ignore it — no action is needed.
          </p>
        </td></tr>
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 32px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.7;">
            Symbolos · Not affiliated with McGill University<br>
            <a href="https://symbolos.ca/privacy" style="color:#9ca3af;">Privacy Policy</a>
            &nbsp;·&nbsp;
            <a href="https://symbolos.ca/terms" style="color:#9ca3af;">Terms of Service</a>
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""
