"""
backend/api/routes/notifications.py

FIX: Updated _build_html_email() to use Symbolos brand color (#ED1B2F)
     consistently instead of the generic blue/grey palette.
     Also fixes the cron guard to accept both secret formats.

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

NOTIFICATIONS_ENABLED = True


class CalendarEventIn(BaseModel):
    id: Optional[str] = None
    client_id: Optional[str] = Field(None, max_length=200)
    user_id: str
    title: str             = Field(..., min_length=1, max_length=200)
    date: str              = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    time: Optional[str]    = Field(None, pattern=r"^\d{2}:\d{2}$")
    end_time: Optional[str] = Field(None, pattern=r"^\d{2}:\d{2}$")
    type: str              = Field("personal", max_length=50)
    category: Optional[str]    = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    notify_enabled: bool = True
    notify_email: bool = True
    notify_sms: bool = False
    notify_email_addr: Optional[EmailStr] = None
    notify_phone: Optional[str] = Field(None, max_length=20)
    notify_same_day: bool = False
    notify_1day: bool = True
    notify_7days: bool = True
    course_code: Optional[str] = Field(None, max_length=20)

    @field_validator("notify_phone", mode="before")
    @classmethod
    def validate_phone(cls, v):
        if v is None or v == "":
            return None
        import re
        if not re.match(r"^\+[1-9]\d{6,14}$", str(v)):
            raise ValueError("notify_phone must be in E.164 format (e.g. +15145551234)")
        return str(v)

    @field_validator("date", mode="before")
    @classmethod
    def validate_date(cls, v: str) -> str:
        try:
            date.fromisoformat(v)
        except ValueError:
            raise ValueError(f"Invalid date: {v}")
        return v


class EventDeleteRequest(BaseModel):
    user_id: str


# ── Email builder ─────────────────────────────────────────────────────────────

def _type_meta(event_type: str) -> dict:
    meta = {
        "exam":       {"emoji": "📝", "label": "Exam",       "color": "#DC2626"},
        "quiz":       {"emoji": "📋", "label": "Quiz",       "color": "#D97706"},
        "assignment": {"emoji": "📄", "label": "Assignment", "color": "#2563EB"},
        "midterm":    {"emoji": "📝", "label": "Midterm",    "color": "#DC2626"},
        "personal":   {"emoji": "📅", "label": "Event",      "color": "#6B7280"},
        "academic":   {"emoji": "🎓", "label": "Academic",   "color": "#ED1B2F"},
    }
    return meta.get(event_type, meta["personal"])


def _build_html_email(event_title: str, event_date: str, event_type: str, days_before: int) -> tuple[str, str]:
    """Build a branded HTML email for a calendar reminder. Returns (subject, html)."""
    m = _type_meta(event_type)
    safe_title = escape(event_title)
    safe_date  = escape(event_date)

    if days_before == 0:
        timing_text = "is <strong>TODAY</strong>"
        subject = f"{m['emoji']} Today: {event_title}"
        urgency_color = "#DC2626"
    elif days_before == 1:
        timing_text = "is <strong>TOMORROW</strong>"
        subject = f"{m['emoji']} Tomorrow: {event_title}"
        urgency_color = "#D97706"
    else:
        timing_text = f"is in <strong>{days_before} days</strong>"
        subject = f"{m['emoji']} Reminder: {event_title} — {days_before} days away"
        urgency_color = "#ED1B2F"

    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width,initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:40px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">

        <!-- Header -->
        <tr><td style="background:linear-gradient(135deg,#ED1B2F 0%,#B01B2E 100%);border-radius:12px 12px 0 0;padding:20px 28px;">
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td><span style="color:#fff;font-size:18px;font-weight:800;">Symbolos</span></td>
              <td align="right"><span style="color:rgba(255,255,255,0.75);font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Academic Reminder</span></td>
            </tr>
          </table>
        </td></tr>

        <!-- Body -->
        <tr><td style="background:#ffffff;padding:32px 28px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">

          <!-- Event type badge -->
          <div style="margin-bottom:20px;">
            <span style="display:inline-block;background:{m['color']}18;color:{m['color']};
                         font-size:11px;font-weight:700;text-transform:uppercase;
                         letter-spacing:0.08em;padding:4px 12px;border-radius:20px;">
              {m['emoji']} {m['label']}
            </span>
          </div>

          <h1 style="font-size:22px;font-weight:700;color:#111827;margin:0 0 8px;line-height:1.3;">
            {safe_title}
          </h1>
          <p style="font-size:16px;color:{urgency_color};font-weight:600;margin:0 0 20px;">
            {timing_text} — {safe_date}
          </p>

          <div style="background:#f9fafb;border:1px solid #e5e7eb;border-left:4px solid {m['color']};
                      border-radius:0 8px 8px 0;padding:14px 18px;margin-bottom:24px;">
            <p style="font-size:14px;color:#374151;margin:0;line-height:1.6;">
              This is your scheduled reminder from Symbolos. Good luck! 🍀
            </p>
          </div>

          <div style="text-align:center;">
            <a href="https://symbolos.ca"
               style="display:inline-block;background:linear-gradient(135deg,#ED1B2F 0%,#B01B2E 100%);
                      color:#fff;padding:12px 28px;border-radius:8px;text-decoration:none;
                      font-weight:600;font-size:14px;">
              Open Symbolos →
            </a>
          </div>

        </td></tr>

        <!-- Footer -->
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.7;">
            Symbolos · Not affiliated with McGill University<br>
            You're receiving this because you set a reminder in your Symbolos calendar.<br>
            <a href="https://symbolos.ca" style="color:#ED1B2F;text-decoration:none;">Manage reminders</a>
          </p>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>"""
    return subject, html


# ── Email / SMS senders ───────────────────────────────────────────────────────

def _send_email(to: str, event_title: str, event_date: str, event_type: str, days_before: int) -> bool:
    """Send reminder email via Resend. Returns True on success."""
    if not NOTIFICATIONS_ENABLED:
        logger.info(f"[NOTIFICATIONS DISABLED] Would send email to {to} for '{event_title}'")
        return True

    try:
        subject, html = _build_html_email(event_title, event_date, event_type, days_before)

        resend.api_key = settings.RESEND_API_KEY
        resend.Emails.send({
            "from": "Symbolos <notifications@symbolos.ca>",
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
            body = f"{meta['emoji']} McGill Reminder: '{event_title}' is TODAY ({event_date}). Good luck!"
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

    supabase = get_supabase()

    # Upsert by client_id if provided (idempotent)
    existing_id = None
    if event.client_id:
        existing = (
            supabase.table("calendar_events")
            .select("id")
            .eq("user_id", event.user_id)
            .eq("client_id", event.client_id)
            .execute()
        )
        if existing.data:
            existing_id = existing.data[0]["id"]

    event_row = {
        "user_id":          event.user_id,
        "client_id":        event.client_id,
        "title":            event.title,
        "date":             event.date,
        "time":             event.time,
        "end_time":         event.end_time,
        "type":             event.type,
        "category":         event.category,
        "description":      event.description,
        "notify_enabled":   event.notify_enabled,
        "notify_email":     event.notify_email,
        "notify_sms":       event.notify_sms,
        "notify_email_addr": str(event.notify_email_addr) if event.notify_email_addr else None,
        "notify_phone":     event.notify_phone,
        "notify_same_day":  event.notify_same_day,
        "notify_1day":      event.notify_1day,
        "notify_7days":     event.notify_7days,
        "course_code":      event.course_code,
    }

    if existing_id:
        result = supabase.table("calendar_events").update(event_row).eq("id", existing_id).execute()
        saved_id = existing_id
    else:
        result = supabase.table("calendar_events").insert(event_row).execute()
        saved_id = result.data[0]["id"] if result.data else None

    if not saved_id:
        raise HTTPException(status_code=500, detail="Failed to save event")

    # Queue notifications
    if event.notify_enabled and saved_id:
        _queue_notifications(supabase, saved_id, event)

    return {"ok": True, "event_id": saved_id}


def _queue_notifications(supabase, event_id: str, event: CalendarEventIn):
    """Delete old queued notifications for this event and re-queue."""
    try:
        supabase.table("notification_queue").delete().eq("event_id", event_id).eq("sent", False).execute()

        today_str = date.today().isoformat()
        if not event.date or event.date < today_str:
            return

        ev_date = date.fromisoformat(event.date)
        email_addr = str(event.notify_email_addr) if event.notify_email_addr else None
        rows = []

        offsets = []
        if event.notify_7days:  offsets.append(7)
        if event.notify_1day:   offsets.append(1)
        if event.notify_same_day: offsets.append(0)

        for days_before in offsets:
            send_on = ev_date - timedelta(days=days_before)
            if send_on < date.today():
                continue
            if event.notify_email and email_addr:
                rows.append({
                    "user_id":     event.user_id,
                    "event_id":    event_id,
                    "event_title": event.title,
                    "event_date":  event.date,
                    "event_type":  event.type,
                    "send_on":     send_on.isoformat(),
                    "method":      "email",
                    "email":       email_addr,
                    "phone":       None,
                    "sent":        False,
                })
            if event.notify_sms and event.notify_phone:
                rows.append({
                    "user_id":     event.user_id,
                    "event_id":    event_id,
                    "event_title": event.title,
                    "event_date":  event.date,
                    "event_type":  event.type,
                    "send_on":     send_on.isoformat(),
                    "method":      "sms",
                    "email":       None,
                    "phone":       event.notify_phone,
                    "sent":        False,
                })

        if rows:
            supabase.table("notification_queue").insert(rows).execute()
            logger.info(f"Queued {len(rows)} notifications for event {event_id}")
    except Exception as e:
        logger.error(f"Failed to queue notifications for event {event_id}: {e}")


@router.delete("/{event_id}")
async def delete_event(event_id: str, body: EventDeleteRequest, current_user_id: str = Depends(get_current_user_id)):
    """Remove a calendar event and its queued notifications."""
    require_self(current_user_id, body.user_id)
    supabase = get_supabase()
    supabase.table("notification_queue").delete().eq("event_id", event_id).execute()
    supabase.table("calendar_events").delete().eq("id", event_id).eq("user_id", body.user_id).execute()
    return {"ok": True}


@router.get("/events")
async def list_events(user_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Return all calendar events for a user."""
    require_self(current_user_id, user_id)
    supabase = get_supabase()
    result = supabase.table("calendar_events").select("*").eq("user_id", user_id).order("date").execute()
    return {"events": result.data or []}


@router.post("/cron")
async def run_cron(request: Request, x_cron_secret: Optional[str] = Header(None)):
    """
    Daily cron job — send all due notifications.
    Protected by CRON_SECRET header.
    FIX: Accept both 'Bearer <secret>' and raw '<secret>' formats.
    """
    # Normalise: strip "Bearer " prefix if present
    raw_secret = x_cron_secret or ""
    secret = raw_secret.removeprefix("Bearer ").strip()

    if not hmac.compare_digest(secret, settings.CRON_SECRET):
        raise HTTPException(status_code=401, detail="Unauthorized")

    supabase = get_supabase()
    today = date.today().isoformat()

    due = (
        supabase.table("notification_queue")
        .select("*")
        .lte("send_on", today)
        .eq("sent", False)
        .execute()
    )

    sent_count = 0
    fail_count = 0

    for row in (due.data or []):
        method = row.get("method", "email")
        ok = False
        try:
            if method == "email" and row.get("email"):
                ok = _send_email(
                    row["email"], row["event_title"], row["event_date"],
                    row.get("event_type", "personal"),
                    (date.fromisoformat(row["event_date"]) - date.today()).days
                )
            elif method == "sms" and row.get("phone"):
                ok = _send_sms(
                    row["phone"], row["event_title"], row["event_date"],
                    row.get("event_type", "personal"),
                    (date.fromisoformat(row["event_date"]) - date.today()).days
                )
        except Exception as e:
            logger.error(f"Notification send error for row {row.get('id')}: {e}")

        if ok:
            supabase.table("notification_queue").update({"sent": True}).eq("id", row["id"]).execute()
            sent_count += 1
        else:
            fail_count += 1

    logger.info(f"Cron: {sent_count} sent, {fail_count} failed")
    return {"ok": True, "sent": sent_count, "failed": fail_count}