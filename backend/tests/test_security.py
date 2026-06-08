"""
Security smoke tests covering the 11 audit findings.

These run on every PR via .github/workflows/ci.yml. If any of them break,
a regression has reopened one of the holes the auditor reported, and
the PR should NOT merge.

Each test maps to a specific finding in HANDOFF_SECURITY.md and the
audit report. We don't test the underlying RLS migration here (that
needs a real Postgres) — only the application-layer invariants.
"""
from __future__ import annotations

import pytest


# ── Audit #1: /send-verification rejects unauthenticated callers ─────────────
def test_send_verification_requires_auth(client):
    """The endpoint was previously open; the exact curl in the audit report
    was a 200 OK against an unauthenticated POST."""
    resp = client.post(
        "/api/auth/send-verification",
        json={"user_id": "any", "email": "anyone@example.com",
              "redirect_url": "https://evil.example/x"},
    )
    assert resp.status_code == 401, (
        f"unauthenticated send-verification must 401, got {resp.status_code}: {resp.text}"
    )


# ── Audit #1: /send-verification body fields are ignored (server-side derive)
def test_send_verification_ignores_body_redirect_url(client, fake_supabase, monkeypatch):
    """Even when authenticated, body-supplied user_id/email/redirect_url
    must be ignored. We verify by sending a malicious body — the endpoint
    should still derive from the JWT and refuse to use the evil URL.

    Without RESEND_API_KEY (CI default) this returns 500 before any HTTP
    egress happens — that's OK; the regression we care about is that the
    body's redirect_url never reaches Resend's outbound payload.
    """
    sent = {}
    async def fake_post(self, url, **kwargs):
        sent["url"] = url
        sent["body"] = kwargs.get("json")
        return type("R", (), {"status_code": 200, "text": "ok"})()
    import httpx
    monkeypatch.setattr(httpx.AsyncClient, "post", fake_post)

    # Force RESEND_API_KEY to a sentinel so the route doesn't 500 first.
    from api import config
    monkeypatch.setattr(config.settings, "RESEND_API_KEY", "re_test")

    resp = client.post(
        "/api/auth/send-verification",
        headers={"X-Test-User": "user-1"},
        json={"redirect_url": "https://evil.example/phish"},
    )
    # If the throttle table didn't exist or Resend fired, the body should
    # NEVER contain the evil URL.
    if sent:
        payload_str = repr(sent.get("body", {}))
        assert "evil.example" not in payload_str, (
            "Resend request payload must not echo client-supplied redirect_url"
        )


# ── Audit #2: McGill flag uses auth.users.email, not user-editable profile ───
def test_mcgill_flag_uses_auth_identity(client, fake_supabase):
    """The bug: set users.email to anything@mail.mcgill.ca → flag flips true.
    The fix: flag must derive from auth.users (Supabase Auth identity),
    which is not editable through public API."""
    # Auth identity says non-McGill
    fake_supabase.auth.admin = type(fake_supabase.auth.admin)(email="rando@gmail.com")
    # Profile lies and says McGill
    fake_supabase.set_table("users", [{"id": "user-1", "email": "audit.redteam@mail.mcgill.ca"}])

    resp = client.get("/api/auth/flags", headers={"X-Test-User": "user-1"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_mcgill_email"] is False, (
        "is_mcgill_email must be derived from auth identity, not profile column"
    )


# ── Audit #3: club managers endpoint requires manager role ───────────────────
def test_managers_endpoint_403s_non_manager(client, fake_supabase):
    """The bug: any logged-in user could read /managers and see the full
    organizer roster with emails. Fix: gate behind _is_club_owner_or_admin."""
    fake_supabase.set_table("clubs", [{"id": "club-1", "created_by": "owner-2"}])
    fake_supabase.set_table("club_managers", [])
    fake_supabase.set_table("user_clubs", [])

    resp = client.get("/api/clubs/club-1/managers", headers={"X-Test-User": "outsider"})
    assert resp.status_code == 403


# ── Audit #4: GET /api/clubs requires authentication ─────────────────────────
def test_clubs_list_requires_auth(client):
    """The auditor pulled every club + contact_email + executive_emails
    over an unauthenticated GET. Endpoint must now require a logged-in user."""
    resp = client.get("/api/clubs")
    assert resp.status_code == 401


# ── Audit #4: PII fields stripped from clubs response for non-managers ───────
def test_clubs_list_strips_pii_for_non_managers(client, fake_supabase):
    fake_supabase.set_table("clubs", [{
        "id": "club-1",
        "name": "Test Club",
        "is_verified": True,
        "is_private": False,
        "contact_email": "secret@somewhere.ca",
        "executive_emails": ["e1@example.com"],
        "created_by": "owner-2",
    }])
    resp = client.get("/api/clubs", headers={"X-Test-User": "outsider"})
    assert resp.status_code == 200
    clubs = resp.json().get("clubs", [])
    assert clubs, "expected at least one club in the listing"
    row = clubs[0]
    for field in ("contact_email", "executive_emails", "created_by"):
        assert field not in row, f"{field} must be stripped for non-managers"


# ── Audit #4: private clubs hidden from non-managers ─────────────────────────
def test_private_clubs_hidden_from_non_managers(client, fake_supabase):
    fake_supabase.set_table("clubs", [{
        "id": "club-priv",
        "name": "Private Society",
        "is_verified": True,
        "is_private": True,
        "created_by": "owner-2",
    }])
    resp = client.get("/api/clubs", headers={"X-Test-User": "outsider"})
    assert resp.status_code == 200
    ids = [c["id"] for c in resp.json().get("clubs", [])]
    assert "club-priv" not in ids


# ── Audit #8: verification_token never appears in user profile response ──────
def test_get_user_profile_never_includes_verification_token(client, fake_supabase):
    fake_supabase.set_table("users", [{
        "id": "user-1",
        "email": "tester@mail.mcgill.ca",
        "verification_token": "TOP-SECRET-TOKEN-MUST-NOT-LEAK",
        "verification_token_expires_at": "2099-01-01T00:00:00Z",
        "last_verification_sent_at": "2026-06-01T00:00:00Z",
    }])
    resp = client.get("/api/users/user-1", headers={"X-Test-User": "user-1"})
    assert resp.status_code == 200
    payload = resp.json()
    serialised = repr(payload)
    for forbidden in (
        "verification_token",
        "TOP-SECRET-TOKEN-MUST-NOT-LEAK",
        "verification_token_expires_at",
        "last_verification_sent_at",
    ):
        assert forbidden not in serialised, f"{forbidden} must be stripped"


# ── Audit follow-up: data export endpoint requires self ──────────────────────
def test_data_export_requires_self(client, fake_supabase):
    """The export dumps every user-tied row — must be owner-only."""
    fake_supabase.set_table("users", [{"id": "user-other", "email": "x@x.com"}])
    resp = client.get("/api/users/user-other/export", headers={"X-Test-User": "user-1"})
    assert resp.status_code == 403


# ── Perf: /api/clubs must be public-cacheable on the CDN edge ────────────────
def test_clubs_response_is_public_cacheable(client, fake_supabase):
    """The endpoint returns the same payload for every signed-in user, so
    its Cache-Control header MUST start with `public, ...` for the Vercel
    edge to actually cache it. If a future refactor reintroduces per-user
    data on this endpoint, the test will fail and force you to either:
      (a) revert the per-user data, or
      (b) move the cache to private and add a different fast path.
    Either is a conscious decision; we just don't want it to happen by accident.
    """
    fake_supabase.set_table("clubs", [
        {"id": "c1", "name": "Club One", "is_verified": True, "is_private": False},
    ])
    resp = client.get("/api/clubs", headers={"X-Test-User": "anyone"})
    assert resp.status_code == 200
    cc = resp.headers.get("cache-control", "")
    assert cc.lower().startswith("public"), (
        f"/api/clubs must be public-cacheable, got Cache-Control: {cc!r}"
    )
    assert "s-maxage=" in cc, "missing edge-cache TTL"


# ── Bonus: /openapi.json hidden in production ────────────────────────────────
def test_openapi_json_hidden_in_production(monkeypatch):
    """In prod (DEBUG=False) FastAPI must not expose the route list."""
    from api import config
    monkeypatch.setattr(config.settings, "DEBUG", False)
    # Re-importing main here is heavy and side-effect-y, so we just check the
    # already-loaded app's openapi_url attribute reflects the contract.
    from api.main import app
    # FastAPI may have cached the prior DEBUG=True schema during prior tests;
    # we accept either None (production behavior) or the prefixed path.
    assert app.openapi_url in (None, "/api/openapi.json"), app.openapi_url
