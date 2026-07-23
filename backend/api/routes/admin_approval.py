"""
admin_approval.py — TEMPORARY manual account-approval flow.

Context: McGill's Microsoft 365 tenant is silently holding our verification
emails (SPF/DKIM/DMARC all pass, mail-tester 10/10 — it's their filter, not
us; McGill IT ticket filed 2026-07-13). Until that's resolved, new McGill
students can't self-verify, so we approve accounts by hand:

  1. Right after signup the frontend calls POST /api/admin-approval/notify.
  2. We email the platform admin (APPROVAL_NOTIFY_EMAIL) the new address and a
     one-click approve link signed with ADMIN_SECRET.
  3. Admin opens the link → a page showing the account + a "confirm" link →
     GET /approve/confirm actually confirms the account (email_confirm) so the
     student can log in.

Design notes:
  * The backend origin runs a strict CSP (default-src 'none'), so these pages
    are plain HTML — no forms, inline styles, or scripts (all would be blocked).
  * Approval is a *two-step* GET: the emailed link only shows a review page; a
    second link on that page performs the confirm. A link-prefetcher (the exact
    thing that broke self-verification) follows the emailed link at most, so it
    lands on the harmless review page and never approves.
  * Every link is HMAC-signed with ADMIN_SECRET and expires in 14 days.

REMOVE this route, its main.py registration, and the frontend notify() call
once verification-email delivery is fixed.
"""
from __future__ import annotations

import hashlib
import hmac
import html
import logging
import time

import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from api.config import settings
from api.utils.supabase_client import get_supabase
from api.utils.audit import log_access

router = APIRouter()
logger = logging.getLogger(__name__)

# Approve links stay valid for 14 days — long enough for the admin to get to
# them, short enough that a leaked link doesn't live forever.
_APPROVAL_TTL_SECONDS = 14 * 24 * 3600


class NotifyRequest(BaseModel):
    user_id: str


# ── Signed token (HMAC over user_id + expiry) ───────────────────────────────

def _sign(user_id: str, expiry: int) -> str:
    msg = f"{user_id}:{expiry}".encode()
    return hmac.new(settings.ADMIN_SECRET.encode(), msg, hashlib.sha256).hexdigest()


def _make_token(user_id: str) -> str:
    expiry = int(time.time()) + _APPROVAL_TTL_SECONDS
    return f"{expiry}.{_sign(user_id, expiry)}"


def _verify_token(user_id: str, token: str) -> bool:
    try:
        expiry_str, sig = token.split(".", 1)
        expiry = int(expiry_str)
    except (ValueError, AttributeError):
        return False
    if expiry < int(time.time()):
        return False
    return hmac.compare_digest(sig, _sign(user_id, expiry))


# ── Supabase auth admin helpers (service role) ──────────────────────────────

def _get_auth_user(user_id: str) -> dict | None:
    """Fetch an auth.users record via the admin API. None if not found."""
    try:
        resp = httpx.get(
            f"{settings.SUPABASE_URL}/auth/v1/admin/users/{user_id}",
            headers={
                "apikey": settings.SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
            },
            timeout=10,
        )
    except httpx.HTTPError as exc:
        logger.error("Supabase admin fetch failed: %s", type(exc).__name__)
        raise HTTPException(status_code=502, detail="Upstream error")
    if resp.status_code == 404:
        return None
    if resp.status_code != 200:
        logger.error("Supabase admin fetch error %s", resp.status_code)
        raise HTTPException(status_code=502, detail="Upstream error")
    return resp.json()


def _confirm_auth_user(user_id: str) -> None:
    """Mark the account's email confirmed so the student can log in."""
    try:
        resp = httpx.put(
            f"{settings.SUPABASE_URL}/auth/v1/admin/users/{user_id}",
            headers={
                "apikey": settings.SUPABASE_SERVICE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
                "Content-Type": "application/json",
            },
            json={"email_confirm": True},
            timeout=10,
        )
    except httpx.HTTPError as exc:
        logger.error("Supabase confirm failed: %s", type(exc).__name__)
        raise HTTPException(status_code=502, detail="Upstream error")
    if resp.status_code not in (200, 201):
        logger.error("Supabase confirm error %s", resp.status_code)
        raise HTTPException(status_code=502, detail="Upstream error")
    # Best-effort: sync our own users.email_verified flag too.
    try:
        get_supabase().table("users").update({"email_verified": True}).eq("id", user_id).execute()
    except Exception:  # noqa: BLE001 — flag sync is non-critical
        logger.warning("email_verified flag sync failed for %s", user_id)


# ── Minimal HTML (no forms/styles/scripts — strict backend CSP) ─────────────

def _page(title: str, body_html: str) -> HTMLResponse:
    return HTMLResponse(
        f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title></head><body><main>{body_html}</main></body></html>"""
    )


def _notify_html(email: str, review_url: str, created_at: str) -> str:
    safe_email = html.escape(email)
    safe_created = html.escape(created_at)
    return f"""\
<div style="font-family:system-ui,sans-serif;max-width:480px;margin:auto">
  <h2>New Symbolos signup awaiting approval</h2>
  <p>A new account needs manual approval (McGill mail-filter workaround):</p>
  <p><strong>Email:</strong> {safe_email}<br>
     <strong>Created:</strong> {safe_created}</p>
  <p style="margin-top:24px">
    <a href="{review_url}" style="background:#ed1b2f;color:#fff;padding:12px 24px;
       border-radius:8px;text-decoration:none;font-weight:600">Review this signup</a>
  </p>
  <p style="color:#666;font-size:13px;margin-top:20px">
    Only approve if you recognise this as a real McGill student. Opening the link
    shows a review page; approval happens on a second click there.
  </p>
</div>"""


# ── Endpoints ───────────────────────────────────────────────────────────────

@router.post("/notify")
async def notify_signup(body: NotifyRequest):
    """Called by the frontend right after signup. Emails the admin a review
    link. Unauthenticated (the new user has no confirmed session yet) but safe:
    it only ever emails the fixed admin address, and it no-ops for unknown or
    already-confirmed accounts so it can't be used to spam or to probe."""
    user = _get_auth_user(body.user_id)
    if not user:
        # Unknown id — silently succeed so this can't be used to enumerate.
        return {"ok": True}
    if user.get("email_confirmed_at"):
        return {"ok": True}  # already approved/confirmed

    email = user.get("email") or ""
    created_at = (user.get("created_at") or "")[:19].replace("T", " ") + " UTC"
    token = _make_token(body.user_id)
    review_url = (
        f"{settings.API_BASE_URL}{settings.API_PREFIX}/admin-approval/approve"
        f"?user_id={body.user_id}&token={token}"
    )

    if not settings.RESEND_API_KEY:
        logger.warning("Approval notify skipped — RESEND_API_KEY unset")
        return {"ok": True}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "https://api.resend.com/emails",
                headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}"},
                json={
                    "from": "Symbolos <noreply@symbolos.ca>",
                    "to": [settings.APPROVAL_NOTIFY_EMAIL],
                    "subject": f"Approve Symbolos signup: {email}",
                    "html": _notify_html(email, review_url, created_at),
                },
                timeout=10,
            )
    except httpx.HTTPError as exc:
        logger.error("Approval notify send failed: %s", type(exc).__name__)
        return {"ok": True}  # never fail signup over a notification hiccup
    if resp.status_code not in (200, 201):
        logger.error("Approval notify Resend error %s", resp.status_code)
    return {"ok": True}


@router.get("/approve", response_class=HTMLResponse)
async def approve_review(user_id: str, token: str):
    """Review page (step 1). Shows the account and a link that performs the
    actual confirm. A prefetcher following the emailed link lands here and
    changes nothing."""
    if not _verify_token(user_id, token):
        return _page("Invalid link", "<h2>Link invalid or expired</h2>"
                     "<p>Ask the student to sign up again for a fresh request.</p>")
    user = _get_auth_user(user_id)
    if not user:
        return _page("Not found", "<h2>Account not found</h2>")
    if user.get("email_confirmed_at"):
        return _page("Already approved",
                     f"<h2>Already approved</h2><p>{html.escape(user.get('email',''))} can already log in.</p>")

    confirm_url = (
        f"{settings.API_PREFIX}/admin-approval/approve/confirm"
        f"?user_id={html.escape(user_id)}&token={html.escape(token)}"
    )
    return _page("Approve account",
                 f"<h2>Approve this account?</h2>"
                 f"<p><strong>{html.escape(user.get('email',''))}</strong></p>"
                 f"<p>Only approve if this is a real McGill student.</p>"
                 f'<p><a href="{confirm_url}">Yes — approve and let them in</a></p>')


@router.get("/approve/confirm", response_class=HTMLResponse)
async def approve_confirm(user_id: str, token: str, req: Request):
    """Confirm step (step 2). Reached only from the review page's link."""
    if not _verify_token(user_id, token):
        return _page("Invalid link", "<h2>Link invalid or expired</h2>")
    user = _get_auth_user(user_id)
    if not user:
        return _page("Not found", "<h2>Account not found</h2>")
    if not user.get("email_confirmed_at"):
        _confirm_auth_user(user_id)
        logger.info("Manually approved account %s", user_id)
        log_access(user_id=user_id, action="admin_account_approve", req=req)
    return _page("Approved",
                 f"<h2>Approved</h2><p>{html.escape(user.get('email',''))} can now log in.</p>")
