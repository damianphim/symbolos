"""
backend/api/routes/notifications.py

Handles:
  POST /api/notifications/schedule  – save event + queue notifications
  DELETE /api/notifications/{event_id} – remove event + queue
  GET  /api/notifications/events    – list user's calendar events
  POST /api/notifications/cron      – daily cron: send due notifications (service key protected)

SEC-007: Added E.164 pattern validation to notify_phone field.
"""

import hmac
from fastapi import APIRouter, HTTPException, Header, Depends, Request
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
import logging
from html import escape
from datetime import date, timedelta
import resend
from ..config import settings
from ..utils.supabase_client import get_supabase
from ..auth import get_current_user_id, require_self

router = APIRouter()
logger = logging.getLogger(__name__)

# ── Feature flag ─────────────────────────────────────────────────────────────
NOTIFICATIONS_ENABLED = True


# ── Pydantic schemas ─────────────────────────────────────────────────────────

class CalendarEventIn(BaseModel):
    id: Optional[str] = None
    client_id: Optional[str] = Field(None, max_length=200)  # stable id for idempotency (e.g. "exam-COMP251-0")
    user_id: str
    title: str             = Field(..., min_length=1, max_length=200)
    date: str              = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")  # ISO "YYYY-MM-DD"
    time: Optional[str]    = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    type: str              = Field("personal", max_length=50)
    category: Optional[str]    = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    notify_enabled: bool = True
    notify_email: bool = True
    notify_sms: bool = False
    notify_email_addr: Optional[EmailStr] = None   # was Optional[str] — now validated
    # SEC-007: E.164 phone validation (moved to field_validator below to
    # handle null/empty strings cleanly — Field(pattern=) fires even on None
    # in some Pydantic v2 JSON deserialization paths).
    notify_phone: Optional[str] = Field(None, max_length=20)
    notify_same_day: bool = False
    notify_1day: bool = True
    notify_7days: bool = True

    @field_validator("notify_phone", mode="before")
    @classmethod
    def validate_phone(cls, v):
        """SEC-007: Validate E.164 format, but allow null (most callers don't use SMS)."""
        if v is None or v == "":
            return None
        import re
        if not re.match(r"^\+[1-9]\d{6,14}$", str(v)):
            raise ValueError("notify_phone must be in E.164 format (e.g. +15145551234)")
        return str(v)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v: str) -> str:
        """Ensure date is a real calendar date, not just a pattern match."""
        from datetime import date as _date
        try:
            _date.fromisoformat(str(v))
        except ValueError:
            raise ValueError("date must be a valid calendar date in YYYY-MM-DD format")
        return str(v)


# ── Email templates ──────────────────────────────────────────────────────────

# Emoji + color per event type
_TYPE_META = {
    "exam":     {"emoji": "📝", "label": "Final Exam",        "color": "#7c3aed", "bg": "#f5f3ff"},
    "academic": {"emoji": "📅", "label": "Academic Deadline", "color": "#1d4ed8", "bg": "#eff6ff"},
    "course":   {"emoji": "📚", "label": "Class",             "color": "#ed1b2f", "bg": "#fef2f2"},
    "personal": {"emoji": "⭐", "label": "Event",             "color": "#059669", "bg": "#ecfdf5"},
    "club":     {"emoji": "🎯", "label": "Club Meeting",      "color": "#d97706", "bg": "#fef3c7"},
}

def _type_meta(event_type: str) -> dict:
    return _TYPE_META.get(event_type, _TYPE_META["personal"])


def _countdown_phrase(days_before: int) -> str:
    if days_before == 0:
        return "is <strong>today</strong>"
    if days_before == 1:
        return "is <strong>tomorrow</strong>"
    return f"is coming up in <strong>{days_before} days</strong>"


def _format_date_nice(iso: str) -> str:
    """'2026-04-15' → 'Wednesday, April 15, 2026'"""
    try:
        d = date.fromisoformat(iso)
        return d.strftime("%A, %B %-d, %Y")
    except Exception:
        return iso


def _build_html_email(
    event_title: str,
    event_date: str,
    event_type: str,
    days_before: int,
) -> tuple[str, str]:
    """Returns (subject, html_body)."""
    # Escape all user-controlled fields before interpolating into HTML
    safe_title = escape(event_title)
    safe_date = escape(event_date)

    meta = _type_meta(event_type)
    emoji = meta["emoji"]
    label = meta["label"]
    color = meta["color"]
    bg    = meta["bg"]
    countdown = _countdown_phrase(days_before)
    nice_date = _format_date_nice(safe_date)

    if days_before == 0:
        subject = f"{emoji} Today: {safe_title}"
    elif days_before == 1:
        subject = f"{emoji} Tomorrow: {safe_title}"
    else:
        subject = f"{emoji} In {days_before} days: {safe_title}"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{subject}</title>
</head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:32px 16px;">
    <tr>
      <td align="center">
        <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">

          <!-- Header -->
          <tr>
            <td style="background:#ED1B2F;border-radius:12px 12px 0 0;padding:20px 28px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td>
                    <span style="color:#fff;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;opacity:0.85;">McGill AI Advisor</span>
                  </td>
                  <td align="right">
                    <span style="font-size:22px;">{emoji}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="background:#ffffff;padding:28px 28px 20px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">

              <!-- Type badge -->
              <div style="margin-bottom:16px;">
                <span style="display:inline-block;background:{bg};color:{color};font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">{label}</span>
              </div>

              <!-- Title -->
              <h1 style="margin:0 0 10px;font-size:22px;font-weight:700;color:#111827;line-height:1.3;">{safe_title}</h1>

              <!-- Countdown -->
              <p style="margin:0 0 20px;font-size:16px;color:#374151;line-height:1.5;">
                Your {label.lower()} {countdown}.
              </p>

              <!-- Date card -->
              <table cellpadding="0" cellspacing="0" style="background:{bg};border:1px solid {color}22;border-radius:10px;padding:14px 18px;margin-bottom:24px;width:100%;">
                <tr>
                  <td>
                    <div style="font-size:11px;font-weight:600;color:{color};text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">Date</div>
                    <div style="font-size:15px;font-weight:600;color:#111827;">{nice_date}</div>
                  </td>
                </tr>
              </table>

              <!-- CTA -->
              <div style="text-align:center;margin-bottom:8px;">
                <a href="https://symbolos.ca" style="display:inline-block;background:#ED1B2F;color:#fff;font-size:14px;font-weight:600;text-decoration:none;padding:12px 28px;border-radius:8px;">View Calendar →</a>
              </div>

            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;text-align:center;">
              <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.6;">
                You're receiving this because you enabled reminders in McGill AI Advisor.<br/>
                <a href="https://symbolos.ca" style="color:#9ca3af;">Manage notifications</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""

    return subject, html


# ── Helpers ──────────────────────────────────────────────────────────────────

def _build_notification_rows(event_db_id: str, user_id: str, event: CalendarEventIn) -> list:
    """Return rows to insert into notification_queue based on timing flags."""
    event_date = date.fromisoformat(event.date)
    today = date.today()
    rows = []

    method = "both" if (event.notify_email and event.notify_sms) \
             else "sms" if event.notify_sms \
             else "email"

    offsets = []
    if event.notify_7days:
        offsets.append(7)
    if event.notify_1day:
        offsets.append(1)
    if event.notify_same_day:
        offsets.append(0)

    for days_before in offsets:
        send_on = event_date - timedelta(days=days_before)
        if send_on >= today:
            rows.append({
                "user_id":     user_id,
                "event_id":    event_db_id,
                "event_title": event.title,
                "event_date":  event.date,
                "event_type":  event.type,
                "send_on":     send_on.isoformat(),
                "method":      method,
                "email":       event.notify_email_addr,
                "phone":       event.notify_phone,
                "sent":        False,
            })
    return rows


def _send_email(to: str, event_title: str, event_date: str, event_type: str, days_before: int) -> bool:
    """Send reminder email via Resend. Returns True on success."""
    if not NOTIFICATIONS_ENABLED:
        logger.info(f"[NOTIFICATIONS DISABLED] Would send email to {to} for '{event_title}'")
        return True

    try:
        subject, html = _build_html_email(event_title, event_date, event_type, days_before)

        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            "from": "McGill AI Advisor <reminders@symbolos.ca>",
            "to": [to],
            "subject": subject,
            "html": html,
        })
        logger.info(f"Email sent to {to}: {subject}")
        return True
    except Exception as e:
        logger.error(f"Resend error: {e}")
        return False


def _send_sms(to: str, event_title: str, event_date: str, event_type: str, days_before: int) -> bool:
    """Send reminder SMS via Twilio. Returns True on success."""
    if not NOTIFICATIONS_ENABLED:
        logger.info(f"[NOTIFICATIONS DISABLED] Would send SMS to {to} for '{event_title}'")
        return True

    try:
        from twilio.rest import Client
        meta = _type_meta(event_type)
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        if days_before == 0:
            body = f"{meta['emoji']} McGill Reminder: '{event_title}' is TODAY ({event_date})."
        elif days_before == 1:
            body = f"{meta['emoji']} McGill Reminder: '{event_title}' is TOMORROW ({event_date})."
        else:
            body = f"{meta['emoji']} McGill Reminder: '{event_title}' is in {days_before} days ({event_date})."

        client.messages.create(body=body, from_=settings.TWILIO_FROM_NUMBER, to=to)
        return True
    except Exception as e:
        logger.error(f"Twilio error: {e}")
        return False


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/schedule")
async def schedule_event(event: CalendarEventIn, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Save a calendar event and queue its notifications."""
    require_self(current_user_id, event.user_id)

    try:
        supabase = get_supabase()

        event_row = {
            "user_id":          event.user_id,
            "title":            event.title,
            "date":             event.date,
            "time":             event.time,
            "type":             event.type,
            "category":         event.category,
            "description":      event.description,
            "notify_enabled":   event.notify_enabled,
            "notify_email":     event.notify_email,
            "notify_sms":       event.notify_sms,
            "notify_email_addr": event.notify_email_addr,
            "notify_phone":     event.notify_phone,
            "notify_same_day":  event.notify_same_day,
            "notify_1day":      event.notify_1day,
            "notify_7days":     event.notify_7days,
        }

        result = supabase.table("calendar_events").insert(event_row).execute()
        db_event_id = result.data[0]["id"]

        supabase.table("notification_queue") \
            .delete() \
            .eq("user_id", event.user_id) \
            .eq("event_id", db_event_id) \
            .execute()

        notif_rows = []
        if event.notify_enabled:
            notif_rows = _build_notification_rows(db_event_id, event.user_id, event)
            if notif_rows:
                supabase.table("notification_queue").insert(notif_rows).execute()

        return {"success": True, "event_id": db_event_id, "queued": len(notif_rows)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"schedule_event error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.post("/queue-exam")
async def queue_exam_notification(event: CalendarEventIn, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """
    Idempotent: queue notifications for a read-only exam event.
    Does NOT create a calendar_events row.
    Uses client_id to deduplicate — safe to call on every page load.
    """
    require_self(current_user_id, event.user_id)

    if not event.notify_enabled or not event.notify_email_addr:
        return {"success": True, "queued": 0, "skipped": True}

    try:
        supabase = get_supabase()

        # Idempotency: skip if unsent rows already exist for this key
        idempotency_key = event.client_id or f"{event.user_id}:{event.title}:{event.date}"
        existing = supabase.table("notification_queue") \
            .select("id") \
            .eq("user_id", event.user_id) \
            .eq("idempotency_key", idempotency_key) \
            .eq("sent", False) \
            .execute()

        if existing.data:
            logger.debug(f"Exam notification already queued: {idempotency_key}")
            return {"success": True, "queued": 0, "already_queued": True}

        # Build rows (no calendar_events row — pass None for event_id since the
        # column is UUID-typed and exam events have no calendar_events record)
        notif_rows = _build_notification_rows(None, event.user_id, event)
        for row in notif_rows:
            row["idempotency_key"] = idempotency_key

        if notif_rows:
            supabase.table("notification_queue").insert(notif_rows).execute()
            logger.info(f"Queued {len(notif_rows)} exam notification(s): {event.title}")

        return {"success": True, "queued": len(notif_rows)}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"queue_exam error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.get("/events/{user_id}")
async def get_user_events(user_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Return all calendar events for a user."""
    require_self(current_user_id, user_id)

    try:
        supabase = get_supabase()
        result = supabase.table("calendar_events") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("date") \
            .execute()
        return {"events": result.data}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"get_user_events error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.delete("/events/{event_id}")
async def delete_event(event_id: str, user_id: str, request: Request, current_user_id: str = Depends(get_current_user_id)):
    """Delete a calendar event and its queued notifications."""
    require_self(current_user_id, user_id)

    try:
        supabase = get_supabase()
        # Scope by user_id to prevent IDOR — a user cannot delete another user's notifications
        supabase.table("notification_queue").delete().eq("event_id", event_id).eq("user_id", user_id).execute()
        supabase.table("calendar_events").delete() \
            .eq("id", event_id).eq("user_id", user_id).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"delete_event error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.post("/cron")
async def run_notification_cron(request: Request):
    """
    Called daily by Vercel Cron at 12:00 UTC.
    Vercel sends the CRON_SECRET as: Authorization: Bearer <secret>
    Protected — rejects any request without the correct secret.
    """
    if not settings.CRON_SECRET:
        raise HTTPException(status_code=500, detail="CRON_SECRET not configured")

    # Vercel cron sends Authorization: Bearer <CRON_SECRET>
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(token or "", settings.CRON_SECRET):
        raise HTTPException(status_code=401, detail="Invalid cron secret")

    today = date.today().isoformat()
    supabase = get_supabase()

    rows = supabase.table("notification_queue") \
        .select("*") \
        .lte("send_on", today) \
        .eq("sent", False) \
        .execute().data

    sent_count = 0
    failed_ids = []

    for row in rows:
        event_date  = row["event_date"]
        event_type  = row.get("event_type", "personal")
        days_before = (
            date.fromisoformat(event_date) - date.fromisoformat(row["send_on"])
        ).days
        ok = True

        if row["method"] in ("email", "both") and row.get("email"):
            ok &= _send_email(row["email"], row["event_title"], event_date, event_type, days_before)

        if row["method"] in ("sms", "both") and row.get("phone"):
            ok &= _send_sms(row["phone"], row["event_title"], event_date, event_type, days_before)

        if ok:
            supabase.table("notification_queue").update(
                {"sent": True, "sent_at": date.today().isoformat()}
            ).eq("id", row["id"]).execute()
            sent_count += 1
        else:
            failed_ids.append(row["id"])

    logger.info(f"Cron: enabled={NOTIFICATIONS_ENABLED}, sent={sent_count}, failed={len(failed_ids)}")
    return {
        "sent": sent_count,
        "failed": len(failed_ids),
        "failed_ids": failed_ids,
        "notifications_enabled": NOTIFICATIONS_ENABLED,
    }
