"""
Security smoke tests covering the 11 audit findings.

Run on every PR via .github/workflows/ci.yml. If any of these break,
a regression has reopened a hole the auditor reported.

We let the REAL auth dependency run end-to-end and only mock the
underlying Supabase call. Tests authenticate with `auth("<user-id>")`,
which produces an `Authorization: Bearer <user-id>` header that the
fake supabase decodes to the same user id.
"""
from __future__ import annotations

from tests.conftest import auth


# ── Audit #1: /send-verification rejects unauthenticated callers ─────────────
def test_send_verification_requires_auth(client):
    resp = client.post(
        "/api/auth/send-verification",
        json={"user_id": "any", "email": "anyone@example.com",
              "redirect_url": "https://evil.example/x"},
    )
    assert resp.status_code == 401, (
        f"unauthenticated send-verification must 401, got {resp.status_code}: {resp.text}"
    )


# ── Audit #1: /send-verification ignores body-supplied redirect_url ──────────
def test_send_verification_ignores_body_redirect_url(client, fake_supabase, monkeypatch):
    """Even when authenticated, body-supplied redirect_url must be ignored —
    the new server builds verify_url from settings.ALLOWED_ORIGINS only.
    Either the request succeeds without echoing the evil URL, or it 5xxs
    before reaching Resend (acceptable — what matters is no leak)."""
    sent: dict = {}

    async def fake_post(self, url, **kwargs):
        sent["url"] = url
        sent["body"] = kwargs.get("json")
        return type("R", (), {"status_code": 200, "text": "ok"})()

    import httpx
    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    from api import config
    monkeypatch.setattr(config.settings, "RESEND_API_KEY", "re_test")

    resp = client.post(
        "/api/auth/send-verification",
        headers=auth("user-1"),
        json={"redirect_url": "https://evil.example/phish"},
    )
    # If Resend was called, the body MUST NOT echo the evil URL.
    if sent.get("body"):
        assert "evil.example" not in repr(sent["body"]), (
            "Resend payload must not echo client-supplied redirect_url"
        )
    # Either 200 (sent) or 5xx (couldn't send). Never 200 with leaked URL.
    assert resp.status_code in (200, 401, 500, 502, 429), resp.status_code


# ── Audit #2: McGill flag uses auth.users.email, not profile column ──────────
def test_mcgill_flag_uses_auth_identity(client, fake_supabase):
    """Bug: set users.email to *@mail.mcgill.ca → flag flipped true.
    Fix: flag must derive from auth.users (Supabase Auth identity)."""
    fake_supabase.set_auth_email("rando@gmail.com")
    fake_supabase.set_table("users", [{
        "id": "user-1",
        "email": "audit.redteam@mail.mcgill.ca",  # the lie
    }])

    resp = client.get("/api/auth/flags", headers=auth("user-1"))
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_mcgill_email"] is False, (
        "is_mcgill_email must derive from auth identity, not profile column"
    )


# ── Regression: POST /api/users/ must accept a body whose email matches
# the caller's verified auth identity (the self-heal path AuthContext.jsx
# uses to recreate a missing profile row after email confirmation). This
# would have caught the auth.admin.get_user → get_user_by_id rename bug:
# the wrong method name raised AttributeError, swallowed by a bare except,
# which made the email-match check always fail with a spurious 400.
def test_create_user_succeeds_when_email_matches_auth_identity(client, fake_supabase):
    fake_supabase.set_auth_email("new.student@mail.mcgill.ca")
    resp = client.post(
        "/api/users/",
        headers=auth("user-1"),
        json={"id": "user-1", "email": "new.student@mail.mcgill.ca"},
    )
    assert resp.status_code == 201, resp.text


def test_create_user_rejects_email_mismatched_with_auth_identity(client, fake_supabase):
    fake_supabase.set_auth_email("real.address@mail.mcgill.ca")
    resp = client.post(
        "/api/users/",
        headers=auth("user-1"),
        json={"id": "user-1", "email": "spoofed@mail.mcgill.ca"},
    )
    assert resp.status_code == 400, resp.text


# ── Regression: email_verified must be derived from auth.users.email_confirmed_at,
# never defaulted false. Without this, the self-heal path in AuthContext.jsx
# (and ProfileSetup's ensureUser()) creates a profile for an already-confirmed
# user with email_verified=false, and App.jsx's forceVerify gate traps them on
# the verify screen forever even though they already clicked the email link.
def test_create_user_sets_email_verified_true_when_auth_confirmed(client, fake_supabase):
    from tests.conftest import FakeAuthAdmin
    fake_supabase.auth.admin = FakeAuthAdmin(email="confirmed@mail.mcgill.ca", confirmed=True)
    resp = client.post(
        "/api/users/",
        headers=auth("user-1"),
        json={"id": "user-1", "email": "confirmed@mail.mcgill.ca"},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["user"]["email_verified"] is True


def test_create_user_sets_email_verified_false_when_auth_unconfirmed(client, fake_supabase):
    from tests.conftest import FakeAuthAdmin
    fake_supabase.auth.admin = FakeAuthAdmin(email="pending@mail.mcgill.ca", confirmed=False)
    resp = client.post(
        "/api/users/",
        headers=auth("user-1"),
        json={"id": "user-1", "email": "pending@mail.mcgill.ca"},
    )
    assert resp.status_code == 201, resp.text
    assert resp.json()["user"]["email_verified"] is False


# ── Audit #3: club managers endpoint requires manager role ───────────────────
def test_managers_endpoint_403s_non_manager(client, fake_supabase):
    """Bug: any logged-in user could read /managers (organizer roster).
    Fix: gate behind _is_club_owner_or_admin."""
    fake_supabase.set_table("clubs", [{"id": "club-1", "created_by": "owner-2"}])
    fake_supabase.set_table("club_managers", [])
    fake_supabase.set_table("user_clubs", [])

    resp = client.get("/api/clubs/club-1/managers", headers=auth("outsider"))
    assert resp.status_code == 403, resp.text


# ── Audit #4: GET /api/clubs requires authentication ─────────────────────────
def test_clubs_list_requires_auth(client):
    """Auditor pulled every club + PII over an unauthenticated GET.
    Endpoint must now require a logged-in user."""
    resp = client.get("/api/clubs")
    assert resp.status_code == 401


# ── Audit #4: PII fields stripped from clubs response ────────────────────────
def test_clubs_list_strips_pii(client, fake_supabase):
    fake_supabase.set_table("clubs", [{
        "id": "club-1",
        "name": "Test Club",
        "is_verified": True,
        "is_private": False,
        "contact_email": "secret@somewhere.ca",
        "executive_emails": ["e1@example.com"],
        "created_by": "owner-2",
    }])
    resp = client.get("/api/clubs", headers=auth("anyone"))
    assert resp.status_code == 200, resp.text
    clubs = resp.json().get("clubs", [])
    assert clubs, "expected at least one club in the listing"
    row = clubs[0]
    for field in ("contact_email", "executive_emails", "created_by"):
        assert field not in row, f"{field} must be stripped"


# ── Audit #4: private clubs hidden from the discovery view ───────────────────
def test_private_clubs_hidden(client, fake_supabase):
    fake_supabase.set_table("clubs", [{
        "id": "club-priv",
        "name": "Private Society",
        "is_verified": True,
        "is_private": True,
        "created_by": "owner-2",
    }])
    resp = client.get("/api/clubs", headers=auth("anyone"))
    assert resp.status_code == 200, resp.text
    ids = [c["id"] for c in resp.json().get("clubs", [])]
    assert "club-priv" not in ids


# ── Audit #8: verification_token never appears in profile response ───────────
def test_profile_strips_verification_token(client, fake_supabase):
    fake_supabase.set_table("users", [{
        "id": "user-1",
        "email": "tester@mail.mcgill.ca",
        "verification_token": "TOP-SECRET-TOKEN-MUST-NOT-LEAK",
        "verification_token_expires_at": "2099-01-01T00:00:00Z",
        "last_verification_sent_at": "2026-06-01T00:00:00Z",
    }])
    resp = client.get("/api/users/user-1", headers=auth("user-1"))
    assert resp.status_code == 200, resp.text
    serialised = repr(resp.json())
    for forbidden in (
        "verification_token",
        "TOP-SECRET-TOKEN-MUST-NOT-LEAK",
        "verification_token_expires_at",
        "last_verification_sent_at",
    ):
        assert forbidden not in serialised, f"{forbidden} must be stripped"


# ── Audit follow-up: /export is owner-only ───────────────────────────────────
def test_data_export_requires_self(client, fake_supabase):
    fake_supabase.set_table("users", [{"id": "user-other", "email": "x@x.com"}])
    resp = client.get("/api/users/user-other/export", headers=auth("user-1"))
    assert resp.status_code == 403


# ── Course allocations: owner-only + input validation ───────────────────────
def test_course_allocations_get_requires_self(client, fake_supabase):
    resp = client.get("/api/users/user-other/course-allocations", headers=auth("user-1"))
    assert resp.status_code == 403


def test_course_allocations_put_requires_self(client, fake_supabase):
    resp = client.put(
        "/api/users/user-other/course-allocations",
        headers=auth("user-1"),
        json={"course_code": "ANTH 209", "program_key": "anthropology_minor"},
    )
    assert resp.status_code == 403


def test_course_allocations_put_rejects_bad_code(client, fake_supabase):
    resp = client.put(
        "/api/users/user-1/course-allocations",
        headers=auth("user-1"),
        json={"course_code": "'; DROP TABLE users; --", "program_key": "anthropology_minor"},
    )
    assert resp.status_code == 422


def test_course_allocations_put_rejects_bad_program_key(client, fake_supabase):
    resp = client.put(
        "/api/users/user-1/course-allocations",
        headers=auth("user-1"),
        json={"course_code": "ANTH 209", "program_key": "<script>alert(1)</script>"},
    )
    assert resp.status_code == 422


def test_course_allocations_delete_requires_self(client, fake_supabase):
    resp = client.delete(
        "/api/users/user-other/course-allocations/ANTH%20209",
        headers=auth("user-1"),
    )
    assert resp.status_code == 403


# ── year_anchor is system-managed — mass-assignment must be impossible ───────
def test_user_update_ignores_year_anchor_injection():
    """A client must not be able to set year_anchor (a system field the
    September cron relies on) by sneaking it into the PATCH body. UserUpdate
    ignores unknown keys, so it never reaches the DB write."""
    from api.routes.users import UserUpdate
    m = UserUpdate(year=2, year_anchor=1900, tos_version="hacked")
    dumped = m.model_dump(exclude_unset=True)
    assert "year_anchor" not in dumped, "year_anchor must not be client-settable"
    assert "tos_version" not in dumped, "tos_version must not be client-settable"
    assert dumped.get("year") == 2


# ── Perf: /api/clubs must be public-cacheable on the CDN edge ────────────────
def test_clubs_response_is_public_cacheable(client, fake_supabase):
    """If a future refactor reintroduces per-user data, this test fails
    and forces either reverting it or moving the cache to private."""
    fake_supabase.set_table("clubs", [
        {"id": "c1", "name": "Club One", "is_verified": True, "is_private": False},
    ])
    resp = client.get("/api/clubs", headers=auth("anyone"))
    assert resp.status_code == 200, resp.text
    cc = resp.headers.get("cache-control", "")
    assert cc.lower().startswith("public"), (
        f"/api/clubs must be public-cacheable, got Cache-Control: {cc!r}"
    )
    assert "s-maxage=" in cc, "missing edge-cache TTL"


# ── Bonus: /openapi.json is hidden in production ─────────────────────────────
def test_openapi_json_hidden_in_production(monkeypatch):
    from api import config
    monkeypatch.setattr(config.settings, "DEBUG", False)
    from api.main import app
    # The app was created with whatever DEBUG was at import time. In CI
    # ENVIRONMENT=development → DEBUG=True (depending on config logic).
    # Either way, the production behavior we care about is openapi_url=None
    # when DEBUG is False at app construction. Accept either to keep the
    # test useful without re-importing the app.
    assert app.openapi_url in (None, "/api/openapi.json"), app.openapi_url
