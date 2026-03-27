"""
Email verification via Resend — bypasses Supabase's rate-limited built-in mailer.

Endpoints:
  POST /api/auth/send-verification  — generate token, store in DB, send Resend email
  POST /api/auth/verify-email       — validate token, mark email_verified = true
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import uuid
import httpx
from datetime import datetime, timezone, timedelta
import logging

from api.config import settings
from api.utils.supabase_client import get_supabase, with_retry

router = APIRouter()
logger = logging.getLogger(__name__)

TOKEN_TTL_HOURS = 24


class SendVerificationRequest(BaseModel):
    user_id: str
    email: EmailStr
    redirect_url: str  # window.location.origin from the frontend


class VerifyEmailRequest(BaseModel):
    user_id: str
    token: str


@router.post("/send-verification")
async def send_verification(req: SendVerificationRequest):
    if not settings.RESEND_API_KEY:
        raise HTTPException(status_code=500, detail="Email service not configured")

    token = str(uuid.uuid4())
    expires_at = (datetime.now(timezone.utc) + timedelta(hours=TOKEN_TTL_HOURS)).isoformat()

    def _store():
        get_supabase().table("users").update({
            "verification_token": token,
            "verification_token_expires_at": expires_at,
            "email_verified": False,
        }).eq("id", req.user_id).execute()

    with_retry("store_verification_token", _store)

    verify_url = f"{req.redirect_url}?verify_token={token}&user_id={req.user_id}"

    html = f"""
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;max-width:480px;margin:0 auto;padding:40px 24px;background:#fff">
  <div style="margin-bottom:28px">
    <span style="font-size:22px;font-weight:700;color:#0f172a">Symbolos</span>
  </div>
  <h1 style="font-size:20px;font-weight:700;color:#0f172a;margin:0 0 10px">Verify your email address</h1>
  <p style="font-size:15px;color:#475569;margin:0 0 28px;line-height:1.6">
    Click the button below to confirm your email and activate your Symbolos account.
  </p>
  <a href="{verify_url}"
     style="display:inline-block;background:#e05c5c;color:#ffffff;padding:13px 30px;
            border-radius:8px;text-decoration:none;font-weight:600;font-size:15px">
    Verify email address
  </a>
  <p style="font-size:12px;color:#94a3b8;margin:28px 0 0;line-height:1.6">
    This link expires in {TOKEN_TTL_HOURS} hours.<br>
    If you didn't create a Symbolos account, you can safely ignore this email.
  </p>
  <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0">
  <p style="font-size:11px;color:#cbd5e1;margin:0">Not affiliated with McGill University</p>
</div>
"""

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
            json={
                "from": "Symbolos <onboarding@resend.dev>",
                "to": [req.email],
                "subject": "Verify your Symbolos account",
                "html": html,
            },
            timeout=10,
        )
        if resp.status_code not in (200, 201):
            logger.error(f"Resend error {resp.status_code}: {resp.text}")
            raise HTTPException(status_code=502, detail="Failed to send verification email")

    logger.info(f"Verification email sent to {req.email}")
    return {"ok": True}


@router.post("/verify-email")
async def verify_email(req: VerifyEmailRequest):
    def _fetch():
        return get_supabase().table("users").select(
            "verification_token, verification_token_expires_at"
        ).eq("id", req.user_id).execute()

    result = with_retry("fetch_verification_token", _fetch)

    if not result.data:
        raise HTTPException(status_code=404, detail="User not found")

    row = result.data[0]

    if row.get("verification_token") != req.token:
        raise HTTPException(status_code=400, detail="Invalid or already-used verification link")

    expires_str = row.get("verification_token_expires_at")
    if expires_str:
        expires_at = datetime.fromisoformat(expires_str.replace("Z", "+00:00"))
        if expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=400,
                detail="Verification link has expired. Please request a new one."
            )

    def _confirm():
        get_supabase().table("users").update({
            "email_verified": True,
            "verification_token": None,
            "verification_token_expires_at": None,
        }).eq("id", req.user_id).execute()

    with_retry("confirm_email", _confirm)
    logger.info(f"Email verified for user {req.user_id}")
    return {"ok": True}
