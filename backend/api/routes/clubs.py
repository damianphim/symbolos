"""
backend/api/routes/clubs.py

Clubs endpoints — browse verified McGill clubs, get starter suggestions
based on user major/year, join/leave clubs, submit new clubs for review,
manage join requests for private clubs, and edit clubs you created.
"""
from fastapi import APIRouter, HTTPException, Query, status, Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, EmailStr, Field, AnyHttpUrl, field_validator
from typing import Optional, List
import logging
import secrets
import time
from datetime import datetime, timedelta, timezone
from html import escape

from ..utils.supabase_client import get_supabase
from ..exceptions import DatabaseException
from ..auth import get_current_user_id, require_self
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Hardcoded starter clubs seeded by major keywords ─────────────────────────
MAJOR_CLUB_MAP = {
    "computer science": ["McGill AI Society", "HackMcGill", "McGill Robotics", "McGill Cybersecurity Club"],
    "software":         ["HackMcGill", "McGill AI Society", "McGill Cybersecurity Club"],
    "engineering":      ["McGill Robotics", "McGill Engineering Students' Society", "Formula SAE McGill"],
    "mathematics":      ["McGill Mathematics & Statistics Society", "McGill AI Society"],
    "physics":          ["McGill Physics Society", "McGill Astronomy Society"],
    "biology":          ["McGill Biology Society", "McGill Pre-Med Society", "McGill Genetics Society"],
    "chemistry":        ["McGill Chemistry Society", "McGill Pre-Med Society"],
    "medicine":         ["McGill Pre-Med Society", "McGill Medical Ethics Society"],
    "business":         ["McGill Finance Association", "McGill Management Consulting Group", "McGill Marketing Association"],
    "management":       ["McGill Finance Association", "McGill Management Consulting Group", "McGill Entrepreneurship Society"],
    "economics":        ["McGill Economics Students' Association", "McGill Finance Association"],
    "law":              ["McGill Law Students' Association", "McGill Moot Court Society", "McGill International Law Society"],
    "arts":             ["McGill Arts Undergraduate Society", "McGill Debate Society", "Le Moyne Literary Review"],
    "psychology":       ["McGill Psychology Student Association", "McGill Mental Health Awareness Club"],
    "philosophy":       ["McGill Philosophy Society", "McGill Debate Society"],
    "music":            ["McGill Music Students' Association", "McGill Jazz Orchestra"],
    "political":        ["McGill Model UN", "McGill Debate Society", "McGill International Relations Council"],
    "environment":      ["McGill Sustainability Association", "McGill Outdoors Club"],
    "architecture":     ["McGill Architecture Students' Association"],
    "nursing":          ["McGill Nursing Students' Society"],
    "education":        ["McGill Education Student Society"],
}

DEFAULT_STARTERS = [
    "McGill Debate Society",
    "McGill Model UN",
    "HackMcGill",
    "McGill AI Society",
    "McGill Outdoors Club",
]


# ── Pydantic models ───────────────────────────────────────────────────────────

class ClubSubmission(BaseModel):
    name:             str            = Field(..., min_length=2, max_length=100)
    description:      str            = Field(..., min_length=2, max_length=1000)
    category:         Optional[str]  = Field(None, max_length=60)
    contact_email:    Optional[str]  = Field(None, max_length=200)
    website_url:      Optional[str]  = None
    meeting_schedule: Optional[str]  = Field(None, max_length=300)
    location:         Optional[str]  = Field(None, max_length=200)
    is_private:       bool           = False
    submitted_by:     Optional[str]  = None
    executive_emails: str             = Field(..., min_length=2, max_length=500)


class JoinClubRequest(BaseModel):
    club_id: str
    requester_name: Optional[str] = None
    requester_email: Optional[str] = None
    requester_linkedin: Optional[str] = None


class UpdateClubRequest(BaseModel):
    name:             Optional[str]  = Field(None, min_length=2, max_length=100)
    description:      Optional[str]  = Field(None, max_length=1000)
    category:         Optional[str]  = Field(None, max_length=60)
    contact_email:    Optional[str]  = Field(None, max_length=200)
    website_url:      Optional[str]  = None
    meeting_schedule: Optional[str]  = Field(None, max_length=300)
    location:         Optional[str]  = Field(None, max_length=200)
    is_private:       Optional[bool] = None


class JoinRequestAction(BaseModel):
    action: str  # "approve" or "deny"


def _convert_to_24h(v: Optional[str]) -> Optional[str]:
    """Convert time strings like '2:00 PM' to '14:00' (HH:MM 24h format)."""
    if not v:
        return None
    import re
    v = v.strip()
    # Already HH:MM 24h format
    if re.match(r'^\d{2}:\d{2}$', v):
        return v
    # Handle "H:MM" without AM/PM (e.g. "2:00")
    if re.match(r'^\d{1,2}:\d{2}$', v) and 'AM' not in v.upper() and 'PM' not in v.upper():
        return v.zfill(5)
    # Handle 12h format like "2:00 PM" or "12:30 AM"
    m = re.match(r'^(\d{1,2}):(\d{2})\s*(AM|PM)$', v, re.IGNORECASE)
    if m:
        h = int(m.group(1))
        mins = m.group(2)
        period = m.group(3).upper()
        if period == 'PM' and h != 12:
            h += 12
        if period == 'AM' and h == 12:
            h = 0
        return f"{h:02d}:{mins}"
    return v  # fallback


class ClubEventCreate(BaseModel):
    title:       str            = Field(..., min_length=1, max_length=200)
    description: Optional[str]  = Field(None, max_length=1000)
    date:        str            = Field(...)  # YYYY-MM-DD
    time:        Optional[str]  = None        # HH:MM (auto-converts 12h format)
    end_time:    Optional[str]  = None        # HH:MM (auto-converts 12h format)
    location:    Optional[str]  = Field(None, max_length=200)
    recurrence:  Optional[str]  = None        # null, 'weekly_monday', 'biweekly_tuesday', etc.

    @field_validator('time', 'end_time', mode='before')
    @classmethod
    def normalize_time(cls, v):
        return _convert_to_24h(v)


class ClubAnnouncementCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    body:  str = Field(..., min_length=1, max_length=2000)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_starter_names(major: Optional[str]) -> List[str]:
    """Return a list of club names relevant to the user's major."""
    if not major:
        return DEFAULT_STARTERS
    major_lower = major.lower()
    for keyword, names in MAJOR_CLUB_MAP.items():
        if keyword in major_lower:
            return names
    return DEFAULT_STARTERS


def _send_join_request_email(creator_email: str, club_name: str, requester_name: str, requester_email: str = "", requester_linkedin: str = ""):
    """Send an email to the club creator when someone requests to join."""
    try:
        if not settings.RESEND_API_KEY:
            logger.warning("RESEND_API_KEY not set — skipping join request email")
            return

        safe_club = escape(club_name)
        safe_name = escape(requester_name or "A student")
        safe_email = escape(requester_email or "Not provided")
        safe_linkedin = escape(requester_linkedin or "")

        linkedin_row = ""
        if safe_linkedin:
            linkedin_row = f'<tr><td style="padding:6px 0;font-size:13px;color:#6b7280;width:90px;">LinkedIn</td><td style="padding:6px 0;font-size:14px;color:#111827;"><a href="{safe_linkedin}" style="color:#2563eb;text-decoration:none;">{safe_linkedin}</a></td></tr>'

        subject = f"New Join Request: {safe_club}"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:32px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">
        <tr><td style="background:#ED1B2F;border-radius:12px 12px 0 0;padding:20px 28px;">
          <span style="color:#fff;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;opacity:0.85;">Symbolos</span>
        </td></tr>
        <tr><td style="background:#ffffff;padding:28px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">
          <div style="margin-bottom:16px;">
            <span style="display:inline-block;background:#fef3c7;color:#92400e;font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">Join Request</span>
          </div>
          <h1 style="margin:0 0 10px;font-size:22px;font-weight:700;color:#111827;line-height:1.3;">{safe_club}</h1>
          <p style="margin:0 0 16px;font-size:16px;color:#374151;line-height:1.5;">
            Someone has requested to join your club.
          </p>
          <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:20px;background:#f9fafb;padding:12px;border-radius:8px;">
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;width:90px;">Name</td><td style="padding:6px 0;font-size:14px;color:#111827;font-weight:600;">{safe_name}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Email</td><td style="padding:6px 0;font-size:14px;color:#111827;">{safe_email}</td></tr>
            {linkedin_row}
          </table>
          <p style="margin:0 0 20px;font-size:14px;color:#6b7280;">
            Log in to your Symbolos dashboard to approve or deny this request.
          </p>
          <div style="text-align:center;">
            <a href="https://symbolos.ca" style="display:inline-block;background:#ED1B2F;color:#fff;font-size:14px;font-weight:600;text-decoration:none;padding:12px 28px;border-radius:8px;">Review Request</a>
          </div>
        </td></tr>
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.6;">
            You're receiving this because you are the creator of {safe_club} on Symbolos.
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>"""

        import httpx
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json"},
            json={"from": "Symbolos <notifications@symbolos.ca>", "to": [creator_email], "subject": subject, "html": html},
            timeout=10,
        )
        if resp.status_code >= 400:
            logger.warning(f"Resend API error for join request: {resp.status_code} {resp.text}")
        else:
            logger.info(f"Join request email sent to {creator_email} for club {club_name}")
    except Exception as e:
        logger.exception(f"Failed to send join request email: {e}")


def _notify_club_members_new_event(supabase, club_id: str, club_name: str, title: str, date: str, time: str = None, location: str = None, description: str = None):
    """Email all members of a club about a new event."""
    if not settings.RESEND_API_KEY:
        return

    # Get all member user IDs
    members = supabase.table("user_clubs").select("user_id").eq("club_id", club_id).execute()
    if not members.data:
        return

    user_ids = [m["user_id"] for m in members.data]

    # Get emails from auth — try profiles table
    emails = []
    for uid in user_ids:
        try:
            profile = supabase.table("profiles").select("email").eq("id", uid).execute()
            if profile.data and profile.data[0].get("email"):
                emails.append(profile.data[0]["email"])
        except Exception:
            continue

    if not emails:
        return

    safe_name = escape(club_name)
    safe_title = escape(title)
    safe_desc = escape((description or "")[:300])
    safe_loc = escape(location or "TBA")
    time_str = time or "TBA"

    subject = f"New Event: {safe_title} — {safe_name}"
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:32px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">
        <tr><td style="background:#ED1B2F;border-radius:12px 12px 0 0;padding:20px 28px;">
          <span style="color:#fff;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;opacity:0.85;">Symbolos</span>
        </td></tr>
        <tr><td style="background:#ffffff;padding:28px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">
          <div style="margin-bottom:16px;">
            <span style="display:inline-block;background:#dbeafe;color:#1d4ed8;font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">New Event</span>
          </div>
          <h1 style="margin:0 0 8px;font-size:22px;font-weight:700;color:#111827;line-height:1.3;">{safe_title}</h1>
          <p style="margin:0 0 16px;font-size:14px;color:#6b7280;">Posted by <strong>{safe_name}</strong></p>
          <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:16px;background:#f9fafb;padding:12px;border-radius:8px;">
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;width:80px;">Date</td><td style="padding:6px 0;font-size:14px;color:#111827;font-weight:600;">{escape(date)}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Time</td><td style="padding:6px 0;font-size:14px;color:#111827;">{escape(time_str)}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Location</td><td style="padding:6px 0;font-size:14px;color:#111827;">{safe_loc}</td></tr>
          </table>
          {"<p style='margin:0 0 20px;font-size:14px;color:#374151;line-height:1.6;'>" + safe_desc + "</p>" if safe_desc else ""}
          <div style="text-align:center;">
            <a href="https://symbolos.ca" style="display:inline-block;background:#ED1B2F;color:#fff;font-size:14px;font-weight:600;text-decoration:none;padding:12px 28px;border-radius:8px;">View on Symbolos</a>
          </div>
        </td></tr>
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.6;">
            You're receiving this because you are a member of {safe_name} on Symbolos.
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>"""

    try:
        import httpx
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json"},
            json={"from": "Symbolos <notifications@symbolos.ca>", "to": emails, "subject": subject, "html": html},
            timeout=10,
        )
        if resp.status_code >= 400:
            logger.warning(f"Resend error for event notification: {resp.status_code} {resp.text}")
        else:
            logger.info(f"Event notification sent to {len(emails)} members of {club_name}")
    except Exception as e:
        logger.exception(f"Failed to send event notification: {e}")


# ── DB-stored action tokens for email-based club approval ────────────────────
_ACTION_TOKEN_TTL_DAYS = 7


def _generate_action_tokens(submission_id: str):
    """Generate random tokens for approve/reject and store them in the DB."""
    approve_token = secrets.token_urlsafe(32)
    reject_token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(timezone.utc) + timedelta(days=_ACTION_TOKEN_TTL_DAYS)).isoformat()

    logger.info(f"Generating action tokens for submission {submission_id}")
    supabase = get_supabase()
    supabase.table("club_submissions").update({
        "approve_token": approve_token,
        "reject_token": reject_token,
        "token_expires_at": expires_at,
    }).eq("id", submission_id).execute()
    logger.info(f"Action tokens stored for submission {submission_id}")

    return approve_token, reject_token


def _verify_action_token(token: str):
    """Look up a token in the DB. Returns (submission_id, action) or (None, None)."""
    try:
        supabase = get_supabase()
        # Check approve tokens
        result = supabase.table("club_submissions").select("id, token_expires_at, status").eq("approve_token", token).execute()
        if result.data:
            row = result.data[0]
            expires = row.get("token_expires_at", "")
            if expires and datetime.fromisoformat(expires) < datetime.now(timezone.utc):
                logger.warning(f"Approve token expired for submission {row['id']}")
                return None, None
            return row["id"], "approved"

        # Check reject tokens
        result = supabase.table("club_submissions").select("id, token_expires_at, status").eq("reject_token", token).execute()
        if result.data:
            row = result.data[0]
            expires = row.get("token_expires_at", "")
            if expires and datetime.fromisoformat(expires) < datetime.now(timezone.utc):
                logger.warning(f"Reject token expired for submission {row['id']}")
                return None, None
            return row["id"], "rejected"

        logger.warning(f"Token not found in DB: {token[:20]}...")
        return None, None
    except Exception as e:
        logger.exception(f"Token verification error: {e}")
        return None, None


def _send_admin_club_email(submission: dict):
    """Send an approval/rejection email to admin emails when a club is submitted."""
    if not settings.RESEND_API_KEY:
        raise Exception("RESEND_API_KEY not set")

    admin_emails = [e.strip() for e in settings.ADMIN_EMAILS.split(",") if e.strip()]
    if not admin_emails:
        raise Exception("No ADMIN_EMAILS configured")

    safe_name = escape(submission.get("name", "Unknown"))
    safe_desc = escape(submission.get("description", "")[:200])
    category = escape(submission.get("category", "Social"))
    visibility = "Private" if submission.get("is_private") else "Public"
    location = escape(submission.get("location", "") or "Not specified")
    schedule = escape(submission.get("meeting_schedule", "") or "Not specified")
    contact = escape(submission.get("contact_email", "") or "Not provided")
    exec_emails = escape(submission.get("executive_emails", "") or "Not provided")
    sub_id = submission.get("id", "")

    # Use tokens already stored on the submission
    approve_token = submission.get("approve_token", "")
    reject_token = submission.get("reject_token", "")
    if not approve_token or not reject_token:
        raise Exception(f"No tokens on submission {sub_id}: approve={bool(approve_token)} reject={bool(reject_token)}")

    try:
        # Links go directly to the backend API endpoint which returns an HTML result page
        base = settings.API_BASE_URL.rstrip("/")
        approve_url = f"{base}/api/clubs/admin/action?token={approve_token}"
        reject_url = f"{base}/api/clubs/admin/action?token={reject_token}"

        subject = f"New Club Submission: {safe_name}"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:32px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">
        <tr><td style="background:#ED1B2F;border-radius:12px 12px 0 0;padding:20px 28px;">
          <span style="color:#fff;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;opacity:0.85;">Symbolos</span>
        </td></tr>
        <tr><td style="background:#ffffff;padding:28px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">
          <div style="margin-bottom:16px;">
            <span style="display:inline-block;background:#fef3c7;color:#92400e;font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">New Club Submission</span>
          </div>
          <h1 style="margin:0 0 16px;font-size:22px;font-weight:700;color:#111827;line-height:1.3;">{safe_name}</h1>
          <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:16px;">
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;width:100px;">Category</td><td style="padding:6px 0;font-size:14px;color:#111827;font-weight:600;">{category}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Visibility</td><td style="padding:6px 0;font-size:14px;color:#111827;font-weight:600;">{visibility}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Location</td><td style="padding:6px 0;font-size:14px;color:#111827;">{location}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Schedule</td><td style="padding:6px 0;font-size:14px;color:#111827;">{schedule}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Contact</td><td style="padding:6px 0;font-size:14px;color:#111827;">{contact}</td></tr>
            <tr><td style="padding:6px 0;font-size:13px;color:#6b7280;">Exec Emails</td><td style="padding:6px 0;font-size:14px;color:#111827;font-weight:600;">{exec_emails}</td></tr>
          </table>
          <p style="margin:0 0 20px;font-size:14px;color:#374151;line-height:1.6;background:#f9fafb;padding:12px;border-radius:8px;">{safe_desc}</p>
          <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
              <td width="48%" style="padding-right:8px;">
                <a href="{approve_url}" style="display:block;text-align:center;background:#16a34a;color:#fff;font-size:15px;font-weight:700;text-decoration:none;padding:14px 20px;border-radius:8px;">Approve</a>
              </td>
              <td width="48%" style="padding-left:8px;">
                <a href="{reject_url}" style="display:block;text-align:center;background:#dc2626;color:#fff;font-size:15px;font-weight:700;text-decoration:none;padding:14px 20px;border-radius:8px;">Reject</a>
              </td>
            </tr>
          </table>
        </td></tr>
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.6;">
            This link expires in 7 days. You're receiving this because you are an admin of Symbolos.
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>"""

        import httpx
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {settings.RESEND_API_KEY}", "Content-Type": "application/json"},
            json={"from": "Symbolos <notifications@symbolos.ca>", "to": admin_emails, "subject": subject, "html": html},
            timeout=10,
        )
        resp_data = resp.json()
        logger.info(f"Resend API response for club {submission.get('name')}: status={resp.status_code} body={resp_data}")
        if resp.status_code >= 400:
            raise Exception(f"Resend API error {resp.status_code}: {resp_data}")
        # Store response for debugging
        submission["_resend_response"] = {"status": resp.status_code, "body": resp_data}
    except Exception as e:
        logger.exception(f"Failed to send admin club email: {e}")
        raise


def _send_submitter_notification_email(contact_email: str, club_name: str, status: str):
    """Notify the club submitter about their submission being approved or rejected."""
    try:
        import resend
        if not settings.RESEND_API_KEY or not contact_email:
            return

        resend.api_key = settings.RESEND_API_KEY
        safe_name = escape(club_name)
        is_approved = status == "approved"
        badge_bg = "#dcfce7" if is_approved else "#fee2e2"
        badge_color = "#166534" if is_approved else "#dc2626"
        badge_text = "Approved" if is_approved else "Rejected"
        message = (
            f"Your club <strong>{safe_name}</strong> has been approved and is now live on Symbolos! Students can find and join your club."
            if is_approved else
            f"Unfortunately, your club submission <strong>{safe_name}</strong> was not approved at this time. You can resubmit with updated information."
        )

        subject = f"Club {'Approved' if is_approved else 'Not Approved'}: {safe_name}"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5;padding:32px 16px;">
    <tr><td align="center">
      <table width="100%" cellpadding="0" cellspacing="0" style="max-width:520px;">
        <tr><td style="background:#ED1B2F;border-radius:12px 12px 0 0;padding:20px 28px;">
          <span style="color:#fff;font-size:13px;font-weight:600;letter-spacing:0.08em;text-transform:uppercase;opacity:0.85;">Symbolos</span>
        </td></tr>
        <tr><td style="background:#ffffff;padding:28px;border-left:1px solid #e4e4e7;border-right:1px solid #e4e4e7;">
          <div style="margin-bottom:16px;">
            <span style="display:inline-block;background:{badge_bg};color:{badge_color};font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">{badge_text}</span>
          </div>
          <h1 style="margin:0 0 16px;font-size:22px;font-weight:700;color:#111827;line-height:1.3;">{safe_name}</h1>
          <p style="margin:0 0 20px;font-size:15px;color:#374151;line-height:1.6;">{message}</p>
          {'<div style="text-align:center;"><a href="https://symbolos.ca" style="display:inline-block;background:#ED1B2F;color:#fff;font-size:14px;font-weight:600;text-decoration:none;padding:12px 28px;border-radius:8px;">Go to Dashboard</a></div>' if is_approved else ''}
        </td></tr>
        <tr><td style="background:#f9fafb;border:1px solid #e4e4e7;border-top:none;border-radius:0 0 12px 12px;padding:16px 28px;text-align:center;">
          <p style="margin:0;font-size:11px;color:#9ca3af;line-height:1.6;">Symbolos &mdash; symbolos.ca</p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body></html>"""

        resend.Emails.send({
            "from": "Symbolos <notifications@symbolos.ca>",
            "to": [contact_email],
            "subject": subject,
            "html": html,
        })
        logger.info(f"Submitter notification email sent to {contact_email} for club {club_name} ({status})")
    except Exception as e:
        logger.exception(f"Failed to send submitter notification email: {e}")


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("")
async def list_clubs(
    search: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = Query(default=50, ge=1, le=200),
):
    """Return all verified clubs, optionally filtered."""
    try:
        supabase = get_supabase()
        query = (
            supabase.table("clubs")
            .select("*")
            .eq("is_verified", True)
            .order("name")
            .limit(limit)
        )
        if category:
            query = query.eq("category", category)
        if search:
            safe_search = search.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
            query = query.ilike("name", f"%{safe_search}%")
        result = query.execute()
        return {"clubs": result.data or [], "count": len(result.data or [])}
    except Exception as e:
        logger.exception(f"Error listing clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve clubs")


@router.get("/starter")
async def get_starter_clubs(user_id: str, major: Optional[str] = None, current_user_id: str = Depends(get_current_user_id)):
    """Return personalised starter club suggestions based on major."""
    require_self(current_user_id, user_id)
    try:
        supabase = get_supabase()
        names = _get_starter_names(major)
        result = supabase.table("clubs").select("*").eq("is_verified", True).execute()
        all_clubs = result.data or []
        names_lower = [n.lower() for n in names]
        matched = [c for c in all_clubs if c["name"].lower() in names_lower]
        joined_result = (
            supabase.table("user_clubs")
            .select("club_id")
            .eq("user_id", user_id)
            .execute()
        )
        joined_ids = {row["club_id"] for row in (joined_result.data or [])}
        for club in matched:
            club["is_joined"] = club["id"] in joined_ids
        return {"starter_clubs": matched}
    except Exception as e:
        logger.exception(f"Error fetching starter clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve starter clubs")


# ── STATIC routes must come before dynamic /{user_id} routes ─────────────────

@router.get("/categories")
async def get_categories():
    """Return the distinct club categories."""
    return {
        "categories": [
            "Academic", "Arts & Culture", "Athletics & Recreation",
            "Community Service", "Debate & Politics", "Engineering & Technology",
            "Environment", "Health & Wellness", "International", "Professional",
            "Science", "Social", "Spiritual & Religious",
        ]
    }


@router.get("/created/{user_id}")
async def get_created_clubs(user_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Return clubs created by this user."""
    require_self(current_user_id, user_id)
    try:
        supabase = get_supabase()
        result = (
            supabase.table("clubs")
            .select("*")
            .eq("created_by", user_id)
            .order("name")
            .execute()
        )
        return {"clubs": result.data or [], "count": len(result.data or [])}
    except Exception as e:
        logger.exception(f"Error fetching created clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve created clubs")


@router.put("/edit/{club_id}")
async def edit_club(club_id: str, body: UpdateClubRequest, current_user_id: str = Depends(get_current_user_id)):
    """Update a club's info. Club owner or admins can edit."""
    try:
        supabase = get_supabase()
        if not _is_club_owner_or_admin(club_id, current_user_id):
            raise HTTPException(status_code=403, detail="Only the club owner or admins can edit this club")

        update_data = {k: v for k, v in body.dict().items() if v is not None}
        if not update_data:
            return {"success": True, "message": "No changes"}

        supabase.table("clubs").update(update_data).eq("id", club_id).execute()
        # Return updated club
        updated = supabase.table("clubs").select("*").eq("id", club_id).execute()
        return {"success": True, "club": (updated.data or [None])[0]}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error editing club: {e}")
        raise HTTPException(status_code=500, detail="Failed to update club")


@router.get("/join-requests/{club_id}")
async def get_join_requests(club_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Get pending join requests for a club. Only the creator can view."""
    try:
        supabase = get_supabase()
        # Verify ownership
        club_result = supabase.table("clubs").select("created_by").eq("id", club_id).execute()
        if not club_result.data:
            raise HTTPException(status_code=404, detail="Club not found")
        if club_result.data[0].get("created_by") != current_user_id:
            raise HTTPException(status_code=403, detail="Only the club creator can view join requests")

        result = (
            supabase.table("club_join_requests")
            .select("*")
            .eq("club_id", club_id)
            .eq("status", "pending")
            .order("created_at", desc=True)
            .execute()
        )
        return {"requests": result.data or [], "count": len(result.data or [])}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error fetching join requests: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve join requests")


@router.post("/join-requests/{request_id}/action")
async def handle_join_request(request_id: str, body: JoinRequestAction, current_user_id: str = Depends(get_current_user_id)):
    """Approve or deny a join request."""
    if body.action not in ("approve", "deny"):
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'deny'")
    try:
        supabase = get_supabase()
        # Get the request
        req_result = supabase.table("club_join_requests").select("*").eq("id", request_id).execute()
        if not req_result.data:
            raise HTTPException(status_code=404, detail="Join request not found")
        join_req = req_result.data[0]

        # Verify club ownership or admin
        if not _is_club_owner_or_admin(join_req["club_id"], current_user_id):
            raise HTTPException(status_code=403, detail="Only the club creator or admins can handle join requests")

        # Update request status
        new_status = "approved" if body.action == "approve" else "denied"
        supabase.table("club_join_requests").update({"status": new_status}).eq("id", request_id).execute()

        # If approved, add user to club
        if body.action == "approve":
            # Check not already joined
            existing = (
                supabase.table("user_clubs")
                .select("user_id")
                .eq("user_id", join_req["user_id"])
                .eq("club_id", join_req["club_id"])
                .execute()
            )
            if not existing.data:
                supabase.table("user_clubs").insert({
                    "user_id": join_req["user_id"],
                    "club_id": join_req["club_id"],
                    "calendar_synced": False,
                }).execute()

        return {"success": True, "status": new_status}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error handling join request: {e}")
        raise HTTPException(status_code=500, detail="Failed to process join request")


@router.get("/user/{user_id}")
async def get_user_clubs(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Return all clubs a user has joined."""
    try:
        supabase = get_supabase()
        result = (
            supabase.table("user_clubs")
            .select("*, clubs(*)")
            .eq("user_id", user_id)
            .execute()
        )
        clubs = []
        for row in (result.data or []):
            club_data = row.get("clubs") or {}
            club_data["calendar_synced"] = row.get("calendar_synced", False)
            club_data["joined_at"] = row.get("joined_at")
            club_data["user_club_id"] = row.get("id")
            clubs.append(club_data)
        return {"clubs": clubs, "count": len(clubs)}
    except Exception as e:
        logger.exception(f"Error fetching user clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user clubs")


@router.post("/user/{user_id}/join")
async def join_club(user_id: str, body: JoinClubRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Join a public club directly, or create a join request for a private club."""
    try:
        supabase = get_supabase()

        # Check if club exists and whether it's private
        club_result = supabase.table("clubs").select("*").eq("id", body.club_id).execute()
        if not club_result.data:
            raise HTTPException(status_code=404, detail="Club not found")
        club = club_result.data[0]

        existing = (
            supabase.table("user_clubs")
            .select("user_id")
            .eq("user_id", user_id)
            .eq("club_id", body.club_id)
            .execute()
        )
        if existing.data:
            raise HTTPException(status_code=409, detail="Already joined this club")

        if club.get("is_private"):
            # Check for existing pending request
            existing_req = (
                supabase.table("club_join_requests")
                .select("id")
                .eq("user_id", user_id)
                .eq("club_id", body.club_id)
                .eq("status", "pending")
                .execute()
            )
            if existing_req.data:
                raise HTTPException(status_code=409, detail="You already have a pending request for this club")

            # Use user-provided info from the join form
            requester_name = body.requester_name or "A student"
            requester_email = body.requester_email or ""
            requester_linkedin = body.requester_linkedin or ""

            # Create join request
            insert_data = {
                "user_id": user_id,
                "club_id": body.club_id,
                "status": "pending",
                "requester_name": requester_name,
            }
            # Add optional columns if provided (columns must exist in table)
            if requester_email:
                insert_data["requester_email"] = requester_email
            if requester_linkedin:
                insert_data["requester_linkedin"] = requester_linkedin

            supabase.table("club_join_requests").insert(insert_data).execute()

            # Send email to club creator (non-blocking — don't fail the join if email fails)
            try:
                creator_id = club.get("created_by")
                if creator_id:
                    creator_result = supabase.table("profiles").select("email").eq("id", creator_id).execute()
                    if creator_result.data and creator_result.data[0].get("email"):
                        _send_join_request_email(
                            creator_email=creator_result.data[0]["email"],
                            club_name=club["name"],
                            requester_name=requester_name,
                            requester_email=requester_email,
                            requester_linkedin=requester_linkedin,
                        )
            except Exception as e:
                logger.warning(f"Failed to send join request email: {e}")

            return {"success": True, "status": "requested", "message": "Join request sent to club creator"}
        else:
            # Public club — join directly
            supabase.table("user_clubs").insert({
                "user_id": user_id,
                "club_id": body.club_id,
                "calendar_synced": False,
            }).execute()
            return {"success": True, "status": "joined"}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error joining club: {e}")
        raise HTTPException(status_code=500, detail="Failed to join club")


@router.delete("/user/{user_id}/leave/{club_id}")
async def leave_club(user_id: str, club_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Remove a club from the user's joined list."""
    try:
        supabase = get_supabase()
        supabase.table("user_clubs").delete().eq("user_id", user_id).eq("club_id", club_id).execute()
        return {"success": True}
    except Exception as e:
        logger.exception(f"Error leaving club: {e}")
        raise HTTPException(status_code=500, detail="Failed to leave club")


@router.patch("/user/{user_id}/calendar/{club_id}")
async def toggle_calendar_sync(user_id: str, club_id: str, synced: bool, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Toggle calendar sync for a club."""
    try:
        supabase = get_supabase()
        supabase.table("user_clubs").update({"calendar_synced": synced}).eq("user_id", user_id).eq("club_id", club_id).execute()
        return {"success": True, "calendar_synced": synced}
    except Exception as e:
        logger.exception(f"Error toggling calendar sync: {e}")
        raise HTTPException(status_code=500, detail="Failed to update calendar sync")


@router.post("/submit")
async def submit_club(submission: ClubSubmission, current_user_id: str = Depends(get_current_user_id)):
    """Submit a new club for admin review."""
    try:
        supabase = get_supabase()
        insert_result = supabase.table("club_submissions").insert({
            "name": submission.name,
            "description": submission.description,
            "category": submission.category or "Social",
            "contact_email": submission.contact_email,
            "website_url": submission.website_url,
            "meeting_schedule": submission.meeting_schedule,
            "location": submission.location,
            "is_private": submission.is_private,
            "submitted_by": submission.submitted_by or current_user_id,
            "executive_emails": submission.executive_emails,
            "status": "pending",
        }).execute()

        # Generate tokens and send approval email to admins
        email_sent = False
        email_error = None
        token_generated = False
        if insert_result.data:
            sub_id = insert_result.data[0].get("id", "")
            # Generate tokens directly here so we can track failures
            try:
                _generate_action_tokens(sub_id)
                token_generated = True
            except Exception as token_err:
                email_error = f"Token generation failed: {token_err}"
                logger.exception(f"Failed to generate action tokens: {token_err}")

            resend_debug = None
            if token_generated:
                try:
                    # Re-fetch the submission with tokens
                    updated = supabase.table("club_submissions").select("*").eq("id", sub_id).execute()
                    if updated.data:
                        sub_data = updated.data[0]
                        _send_admin_club_email(sub_data)
                        email_sent = True
                        resend_debug = sub_data.get("_resend_response")
                except Exception as email_err:
                    email_error = f"Email send failed: {email_err}"
                    logger.exception(f"Failed to send admin email: {email_err}")

        return {"success": True, "email_sent": email_sent, "token_generated": token_generated, "email_error": email_error, "resend_debug": resend_debug, "admin_emails": settings.ADMIN_EMAILS, "version": "v5", "message": "Club submission received. We'll review it shortly!"}
    except Exception as e:
        logger.exception(f"Error submitting club: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit club")


ADMIN_USER_IDS = {
    "82e6f229-ce80-47a8-a63c-f099b03dfc73",  # aduda2469@gmail.com
    "65ad96d2-1704-4ff2-b661-42626f153fe8",  # dphimister24@gmail.com
}


def _is_admin_user(user_id: str) -> bool:
    """Check if the authenticated user is an admin."""
    return user_id in ADMIN_USER_IDS


def _is_club_owner_or_admin(club_id: str, user_id: str) -> bool:
    """Check if user is the club creator OR a global admin."""
    if _is_admin_user(user_id):
        return True
    supabase = get_supabase()
    club = supabase.table("clubs").select("created_by").eq("id", club_id).execute()
    if club.data and club.data[0].get("created_by") == user_id:
        return True
    return False


# ── Club Events ──────────────────────────────────────────────────────────────

# NOTE: Static paths MUST come before /{club_id} dynamic paths to avoid route conflicts

@router.get("/events/subscribed")
async def get_subscribed_club_events(current_user_id: str = Depends(get_current_user_id)):
    """Get all club events from clubs the user has calendar_synced=true."""
    try:
        supabase = get_supabase()
        memberships = supabase.table("user_clubs").select("club_id").eq("user_id", current_user_id).eq("calendar_synced", True).execute()
        club_ids = [m["club_id"] for m in (memberships.data or [])]
        if not club_ids:
            return {"events": []}
        events = supabase.table("club_events").select("*, clubs(name, category)").in_("club_id", club_ids).order("date").execute()
        return {"events": events.data or []}
    except Exception as e:
        logger.exception(f"Error fetching subscribed club events: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch club events")


@router.get("/announcements/subscribed")
async def get_subscribed_club_announcements(current_user_id: str = Depends(get_current_user_id)):
    """Get all announcements from clubs the user has calendar_synced=true."""
    try:
        supabase = get_supabase()
        memberships = supabase.table("user_clubs").select("club_id").eq("user_id", current_user_id).eq("calendar_synced", True).execute()
        club_ids = [m["club_id"] for m in (memberships.data or [])]
        if not club_ids:
            return {"announcements": []}
        announcements = supabase.table("club_announcements").select("*, clubs(name, category)").in_("club_id", club_ids).order("created_at", desc=True).execute()
        return {"announcements": announcements.data or []}
    except Exception as e:
        logger.exception(f"Error fetching subscribed announcements: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch announcements")


@router.post("/{club_id}/events")
async def create_club_event(club_id: str, body: ClubEventCreate, current_user_id: str = Depends(get_current_user_id)):
    """Create a club event. Only club owner or admins can create."""
    if not _is_club_owner_or_admin(club_id, current_user_id):
        raise HTTPException(status_code=403, detail="Only club owner or admins can create events")
    try:
        supabase = get_supabase()
        result = supabase.table("club_events").insert({
            "club_id": club_id,
            "title": body.title,
            "description": body.description,
            "date": body.date,
            "time": body.time,
            "end_time": body.end_time,
            "location": body.location,
            "recurrence": body.recurrence,
            "created_by": current_user_id,
        }).execute()

        # Email all club members about the new event (non-blocking)
        try:
            club_result = supabase.table("clubs").select("name").eq("id", club_id).execute()
            club_name = club_result.data[0]["name"] if club_result.data else "Your Club"
            _notify_club_members_new_event(
                supabase, club_id, club_name,
                title=body.title, date=body.date, time=body.time,
                location=body.location, description=body.description,
            )
        except Exception as e:
            logger.warning(f"Failed to send event notification emails: {e}")

        return {"success": True, "event": result.data[0] if result.data else None}
    except Exception as e:
        logger.exception(f"Error creating club event: {e}")
        raise HTTPException(status_code=500, detail="Failed to create event")


@router.delete("/{club_id}/events/{event_id}")
async def delete_club_event(club_id: str, event_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Delete a club event. Only club owner or admins can delete."""
    if not _is_club_owner_or_admin(club_id, current_user_id):
        raise HTTPException(status_code=403, detail="Only club owner or admins can delete events")
    try:
        supabase = get_supabase()
        supabase.table("club_events").delete().eq("id", event_id).eq("club_id", club_id).execute()
        return {"success": True}
    except Exception as e:
        logger.exception(f"Error deleting club event: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete event")


# ── Club Announcements ──────────────────────────────────────────────────────

@router.post("/{club_id}/announcements")
async def create_club_announcement(club_id: str, body: ClubAnnouncementCreate, current_user_id: str = Depends(get_current_user_id)):
    """Create a club announcement. Only club owner or admins can create."""
    if not _is_club_owner_or_admin(club_id, current_user_id):
        raise HTTPException(status_code=403, detail="Only club owner or admins can create announcements")
    try:
        supabase = get_supabase()
        result = supabase.table("club_announcements").insert({
            "club_id": club_id,
            "title": body.title,
            "body": body.body,
            "created_by": current_user_id,
        }).execute()
        return {"success": True, "announcement": result.data[0] if result.data else None}
    except Exception as e:
        logger.exception(f"Error creating club announcement: {e}")
        raise HTTPException(status_code=500, detail="Failed to create announcement")


@router.delete("/{club_id}/announcements/{ann_id}")
async def delete_club_announcement(club_id: str, ann_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Delete a club announcement. Only club owner or admins can delete."""
    if not _is_club_owner_or_admin(club_id, current_user_id):
        raise HTTPException(status_code=403, detail="Only club owner or admins can delete announcements")
    try:
        supabase = get_supabase()
        supabase.table("club_announcements").delete().eq("id", ann_id).eq("club_id", club_id).execute()
        return {"success": True}
    except Exception as e:
        logger.exception(f"Error deleting club announcement: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete announcement")


@router.delete("/{club_id}")
async def delete_club(club_id: str, current_user_id: str = Depends(get_current_user_id)):
    """Delete a club. Only admin users can delete any club."""
    if not _is_admin_user(current_user_id):
        raise HTTPException(status_code=403, detail="Only admins can delete clubs")
    try:
        supabase = get_supabase()
        # Remove all user_clubs references first
        supabase.table("user_clubs").delete().eq("club_id", club_id).execute()
        # Delete the club
        supabase.table("clubs").delete().eq("id", club_id).execute()
        return {"success": True, "message": "Club deleted"}
    except Exception as e:
        logger.exception(f"Error deleting club: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete club")


# ── Admin endpoints ──────────────────────────────────────────────────────────

def _verify_admin_token(req: Request):
    """Verify admin token from X-Cron-Secret header."""
    from .admin import verify_admin_token
    token = req.headers.get("x-cron-secret", "")
    if not verify_admin_token(token):
        raise HTTPException(status_code=401, detail="Invalid admin token")


@router.get("/admin/submissions")
async def admin_list_submissions(req: Request, status_filter: Optional[str] = "pending"):
    """List club submissions for admin review."""
    _verify_admin_token(req)
    try:
        supabase = get_supabase()
        query = supabase.table("club_submissions").select("*").order("created_at", desc=True)
        if status_filter and status_filter != "all":
            query = query.eq("status", status_filter)
        result = query.execute()
        return {"submissions": result.data or []}
    except Exception as e:
        logger.exception(f"Error listing submissions: {e}")
        raise HTTPException(status_code=500, detail="Failed to list submissions")


@router.patch("/admin/submissions/{submission_id}")
async def admin_review_submission(submission_id: str, req: Request):
    """Approve or reject a club submission. On approve, create the club."""
    _verify_admin_token(req)
    try:
        body = await req.json()
        new_status = body.get("status")
        if new_status not in ("approved", "rejected"):
            raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")

        supabase = get_supabase()

        # Get the submission
        sub_result = supabase.table("club_submissions").select("*").eq("id", submission_id).execute()
        if not sub_result.data:
            raise HTTPException(status_code=404, detail="Submission not found")
        submission = sub_result.data[0]

        # Update status
        supabase.table("club_submissions").update({"status": new_status}).eq("id", submission_id).execute()

        # If approved, create the actual club
        if new_status == "approved":
            supabase.table("clubs").insert({
                "name": submission["name"],
                "description": submission["description"],
                "category": submission.get("category") or "Social",
                "contact_email": submission.get("contact_email"),
                "website_url": submission.get("website_url"),
                "meeting_schedule": submission.get("meeting_schedule"),
                "location": submission.get("location"),
                "is_private": submission.get("is_private", False),
                "is_verified": True,
                "created_by": submission.get("submitted_by"),
                "executive_emails": submission.get("executive_emails"),
                "member_count": 0,
            }).execute()

        return {"success": True, "status": new_status}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error reviewing submission: {e}")
        raise HTTPException(status_code=500, detail="Failed to review submission")


# ── Email-based club approval (no auth required — token IS the auth) ─────────

def _action_result_html(title: str, message: str, is_success: bool) -> str:
    """Generate a simple HTML result page for the email action."""
    bg = "#dcfce7" if is_success else "#fee2e2"
    color = "#166534" if is_success else "#dc2626"
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{escape(title)}</title></head>
<body style="margin:0;padding:0;background:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;display:flex;align-items:center;justify-content:center;min-height:100vh;">
  <div style="max-width:440px;width:100%;margin:40px auto;padding:32px;background:#fff;border-radius:12px;box-shadow:0 4px 16px rgba(0,0,0,0.08);text-align:center;">
    <div style="display:inline-block;background:{bg};color:{color};font-size:12px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:5px 12px;border-radius:20px;margin-bottom:16px;">{escape(title)}</div>
    <p style="margin:0;font-size:16px;color:#374151;line-height:1.6;">{message}</p>
    <a href="https://symbolos.ca" style="display:inline-block;margin-top:20px;background:#ED1B2F;color:#fff;font-size:14px;font-weight:600;text-decoration:none;padding:10px 24px;border-radius:8px;">Go to Symbolos</a>
  </div>
</body></html>"""


@router.get("/admin/action")
async def admin_email_action(token: str):
    """
    Process an approve/reject action from an email link.
    No auth required — the HMAC-signed token is the credential.
    Returns an HTML page with the result.
    """
    logger.info(f"Admin action called with token: {token[:60]}...")
    submission_id, action = _verify_action_token(token)
    if not submission_id:
        return HTMLResponse(_action_result_html(
            "Link Expired",
            "This link has expired or is invalid. Please check your email for a newer link.",
            False,
        ))

    try:
        supabase = get_supabase()

        # Get the submission
        sub_result = supabase.table("club_submissions").select("*").eq("id", submission_id).execute()
        if not sub_result.data:
            return HTMLResponse(_action_result_html(
                "Not Found",
                "This club submission was not found. It may have been deleted.",
                False,
            ))

        submission = sub_result.data[0]

        # Check if already processed
        if submission.get("status") != "pending":
            current = submission["status"].capitalize()
            return HTMLResponse(_action_result_html(
                "Already Processed",
                f"This club submission has already been <strong>{current}</strong>.",
                False,
            ))

        # If approved, create the actual club BEFORE updating status
        if action == "approved":
            club_data = {
                "name": submission["name"],
                "description": submission["description"],
                "category": submission.get("category") or "Social",
                "contact_email": submission.get("contact_email"),
                "website_url": submission.get("website_url"),
                "meeting_schedule": submission.get("meeting_schedule"),
                "location": submission.get("location"),
                "is_private": submission.get("is_private", False),
                "is_verified": True,
                "created_by": submission.get("submitted_by"),
            }
            if submission.get("executive_emails"):
                club_data["executive_emails"] = submission["executive_emails"]
            logger.info(f"Inserting club: {club_data}")
            supabase.table("clubs").insert(club_data).execute()
            logger.info(f"Club inserted successfully: {submission['name']}")

        # Update status only after successful club creation
        supabase.table("club_submissions").update({"status": action}).eq("id", submission_id).execute()

        # Notify the submitter (non-critical)
        contact_email = submission.get("contact_email")
        if contact_email:
            try:
                _send_submitter_notification_email(contact_email, submission["name"], action)
            except Exception as email_err:
                logger.exception(f"Failed to send submitter notification: {email_err}")

        if action == "approved":
            return HTMLResponse(_action_result_html(
                "Club Approved",
                f"<strong>{escape(submission['name'])}</strong> has been approved and is now live on Symbolos!",
                True,
            ))
        else:
            return HTMLResponse(_action_result_html(
                "Club Rejected",
                f"<strong>{escape(submission['name'])}</strong> has been rejected.",
                True,
            ))

    except Exception as e:
        logger.exception(f"Error processing email action: {e}")
        return HTMLResponse(_action_result_html(
            "Error",
            "Something went wrong processing this action. Please try again.",
            False,
        ))
