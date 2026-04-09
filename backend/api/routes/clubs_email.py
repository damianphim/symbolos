"""
clubs_email.py — Email notification helpers for the clubs feature.
Imported by clubs.py — kept separate to reduce file size.
"""
from typing import Optional
import logging
from html import escape

from ..config import settings

logger = logging.getLogger(__name__)

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

    # Get emails from users table
    emails = []
    for uid in user_ids:
        try:
            profile = supabase.table("users").select("email").eq("id", uid).execute()
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


def _notify_club_members_announcement(supabase, club_id: str, club_name: str, title: str, body_text: str, event=None):
    """Email all members of a club about a new announcement, optionally with an attached event."""
    if not settings.RESEND_API_KEY:
        return

    members = supabase.table("user_clubs").select("user_id").eq("club_id", club_id).execute()
    if not members.data:
        return

    emails = []
    for m in members.data:
        try:
            profile = supabase.table("users").select("email").eq("id", m["user_id"]).execute()
            if profile.data and profile.data[0].get("email"):
                emails.append(profile.data[0]["email"])
        except Exception:
            continue

    if not emails:
        return

    safe_name = escape(club_name)
    safe_title = escape(title)
    safe_body = escape(body_text[:500]).replace("\n", "<br/>")

    # Build optional event details block
    event_block = ""
    if event:
        ev_title = escape(event.get("title", ""))
        ev_date = escape(event.get("date", "TBA"))
        ev_time = escape(event.get("time") or "TBA")
        ev_loc = escape(event.get("location") or "TBA")
        event_block = f"""
          <div style="margin:16px 0;padding:1px 0;">
            <div style="margin-bottom:4px;"><span style="display:inline-block;background:#fef3c7;color:#92400e;font-size:10px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:3px 8px;border-radius:12px;">Event</span></div>
            <table width="100%" cellpadding="0" cellspacing="0" style="background:#f9fafb;padding:12px;border-radius:8px;">
              <tr><td style="padding:4px 0;font-size:13px;color:#6b7280;width:80px;">Event</td><td style="padding:4px 0;font-size:14px;color:#111827;font-weight:600;">{ev_title}</td></tr>
              <tr><td style="padding:4px 0;font-size:13px;color:#6b7280;">Date</td><td style="padding:4px 0;font-size:14px;color:#111827;">{ev_date}</td></tr>
              <tr><td style="padding:4px 0;font-size:13px;color:#6b7280;">Time</td><td style="padding:4px 0;font-size:14px;color:#111827;">{ev_time}</td></tr>
              <tr><td style="padding:4px 0;font-size:13px;color:#6b7280;">Location</td><td style="padding:4px 0;font-size:14px;color:#111827;">{ev_loc}</td></tr>
            </table>
          </div>"""

    subject = f"📢 {safe_title} — {safe_name}"
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
            <span style="display:inline-block;background:#ede9fe;color:#7c3aed;font-size:11px;font-weight:700;letter-spacing:0.06em;text-transform:uppercase;padding:4px 10px;border-radius:20px;">Announcement</span>
          </div>
          <h1 style="margin:0 0 8px;font-size:22px;font-weight:700;color:#111827;line-height:1.3;">{safe_title}</h1>
          <p style="margin:0 0 16px;font-size:14px;color:#6b7280;">From <strong>{safe_name}</strong></p>
          <p style="margin:0 0 16px;font-size:14px;color:#374151;line-height:1.6;">{safe_body}</p>
          {event_block}
          <div style="text-align:center;margin-top:20px;">
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
            logger.warning(f"Resend error for announcement notification: {resp.status_code} {resp.text}")
        else:
            logger.info(f"Announcement notification sent to {len(emails)} members of {club_name}")
    except Exception as e:
        logger.exception(f"Failed to send announcement notification: {e}")


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
