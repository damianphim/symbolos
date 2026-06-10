"""
Inbound webhooks from third-party providers.

  POST /api/webhooks/resend  — bounce / complaint / delivery events.

Why we want this:
  * If a user's verification mail bounces (hard-fail), they will be stuck
    on the verify screen forever. We mark their account so the frontend
    can show a "fix your address" prompt instead of "check your inbox".
  * Spam complaints are an early signal of compromised list hygiene or
    a confused user — surface them in Sentry so we notice.
  * Soft bounces / temp failures we just count, no action.

Verification:
  Resend signs every webhook with a shared secret via the Svix-Signature
  header (Resend uses Svix under the hood). We compute HMAC-SHA256 over
  `<id>.<timestamp>.<raw_body>` and compare in constant time. Reject
  anything that fails so attackers can't poison the bounce list to
  suspend competitor accounts.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import os
import time
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request

from ..utils.supabase_client import get_supabase

router = APIRouter()
logger = logging.getLogger(__name__)


def _verify_svix(req: Request, body: bytes) -> bool:
    """Verify a Svix-style webhook signature.

    Resend → Webhooks → settings → "Signing Secret" looks like `whsec_…`.
    Set it as RESEND_WEBHOOK_SECRET in Vercel env. If it isn't set we
    refuse to process the webhook in production (fail-closed) and warn
    in dev so the developer sees what's missing.
    """
    secret = os.getenv("RESEND_WEBHOOK_SECRET", "").strip()
    if not secret:
        env = os.getenv("VERCEL_ENV") or os.getenv("ENVIRONMENT", "development")
        if env == "production":
            return False
        logger.warning("RESEND_WEBHOOK_SECRET not set — accepting unsigned webhook (dev only)")
        return True

    svix_id = req.headers.get("svix-id", "")
    svix_ts = req.headers.get("svix-timestamp", "")
    svix_sig_header = req.headers.get("svix-signature", "")
    if not (svix_id and svix_ts and svix_sig_header):
        return False

    # Replay window — Resend's timestamps are unix seconds. Drop anything
    # older than 5 minutes to limit replay even if a key leaks briefly.
    try:
        if abs(time.time() - int(svix_ts)) > 300:
            return False
    except ValueError:
        return False

    # The secret is base64-encoded after the `whsec_` prefix.
    try:
        key_bytes = base64.b64decode(secret.removeprefix("whsec_"))
    except Exception:
        return False

    signed_payload = f"{svix_id}.{svix_ts}.".encode() + body
    expected = base64.b64encode(
        hmac.new(key_bytes, signed_payload, hashlib.sha256).digest()
    ).decode()

    # Header format: "v1,<sig> v1,<sig2>" — multiple signatures supported
    # for rotation. Any matching one is enough.
    for sig in svix_sig_header.split():
        try:
            _, candidate = sig.split(",", 1)
        except ValueError:
            continue
        if hmac.compare_digest(candidate, expected):
            return True
    return False


def _flag_bounced(email: str, reason: str) -> None:
    """Mark every Symbolos profile with this email so the frontend can
    surface a 'your email bounced — update it' prompt. No-op if the
    address isn't ours."""
    if not email:
        return
    try:
        sb = get_supabase()
        sb.table("users").update({
            "email_bounced":     True,
            "email_bounced_at":  datetime.now(timezone.utc).isoformat(),
            "email_bounce_reason": reason[:200],
        }).eq("email", email.lower()).execute()
    except Exception as exc:
        # The columns may not exist on a fresh DB — log and continue so
        # the webhook still returns 200 (Resend retries on non-2xx).
        logger.warning("flag_bounced DB failure: %s", type(exc).__name__)


@router.post("/resend")
async def resend_webhook(req: Request):
    """Handle bounce / complaint / delivery events from Resend.

    Resend event types (https://resend.com/docs/dashboard/webhooks/event-types):
      email.sent / email.delivered           → metric, no action
      email.delivery_delayed                 → metric only
      email.bounced                          → if hard, flag the user
      email.complained                       → flag + Sentry breadcrumb
      email.opened / email.clicked           → ignored for now (PII)
    """
    body = await req.body()
    if not _verify_svix(req, body):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")

    try:
        payload = (await req.json()) or {}
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    # ── Idempotency ───────────────────────────────────────────────────────────
    # Resend retries on any non-2xx, so the same event can arrive multiple
    # times. Dedup on the Svix message id (stable across retries of the same
    # delivery). If we've seen it, ack with 200 and do nothing.
    event_id = req.headers.get("svix-id") or payload.get("id")
    if event_id:
        try:
            sb = get_supabase()
            existing = (
                sb.table("seen_resend_events")
                .select("event_id").eq("event_id", event_id).execute()
            )
            if existing.data:
                logger.info("Resend webhook %s already processed — skipping", event_id)
                return {"ok": True, "deduped": True}
            sb.table("seen_resend_events").insert({"event_id": event_id}).execute()
        except Exception as exc:
            # If the dedup table is unavailable, fail open — better to risk a
            # double-process (which is idempotent anyway: flagging a user
            # bounced twice is harmless) than to drop the event.
            logger.warning("webhook dedup check failed: %s", type(exc).__name__)

    event_type = (payload.get("type") or "").lower()
    data = payload.get("data") or {}
    # Resend nests the recipient under data.to (list)
    recipient = ""
    to = data.get("to")
    if isinstance(to, list) and to:
        recipient = str(to[0])
    elif isinstance(to, str):
        recipient = to

    if event_type == "email.bounced":
        bounce = data.get("bounce") or {}
        bounce_type = (bounce.get("type") or "").lower()  # "hard" | "soft"
        if bounce_type == "hard":
            reason = bounce.get("subType") or bounce.get("message") or "hard bounce"
            _flag_bounced(recipient, reason)
            logger.warning("Resend HARD bounce: %s — %s", recipient, reason)
        else:
            logger.info("Resend soft bounce (ignored): %s", recipient)

    elif event_type == "email.complained":
        # Spam complaint — same treatment as hard bounce, this address is
        # not safe to mail again.
        _flag_bounced(recipient, "spam complaint")
        logger.warning("Resend SPAM complaint: %s", recipient)
        # Capture as a Sentry breadcrumb if Sentry is configured so we get
        # alerted to surge complaints.
        try:
            import sentry_sdk
            sentry_sdk.capture_message(
                f"Resend spam complaint: {recipient}", level="warning"
            )
        except Exception:
            pass

    else:
        # Sent / delivered / opened / clicked / etc. — counted by Resend's
        # own dashboard, we don't need to mirror.
        logger.debug("Resend webhook event %s ignored", event_type)

    return {"ok": True}
