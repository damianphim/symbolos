"""
backend/api/routes/verification.py

Email verification via Resend — bypasses Supabase's rate-limited built-in mailer.
FIX: Updated email template to use correct brand color (#ED1B2F) and improved styling.

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

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
</head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:40px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">

        <!-- Header -->
        <tr><td style="background:linear-gradient(135deg,#ED1B2F 0%,#B01B2E 100%);border-radius:12px 12px 0 0;padding:24px 32px;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td>
                <span style="color:#fff;font-size:20px;font-weight:800;letter-spacing:-0.5px;">Symbolos</span>
              </td>
              <td align="right">
                <span style="color:rgba(255,255,255,0.7);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Email Verification</span>
              </td>
            </tr>
          </table>
        </td></tr>

        <!-- Body -->
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
            If you didn't create a Symbolos account, you can safely ignore this email — no action is needed.
          </p>
        </td></tr>

        <!-- Footer -->
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

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
            json={
                "from": "Symbolos <noreply@symbolos.ca>",
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