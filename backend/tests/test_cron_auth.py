"""
/api/notifications/cron must be callable the way Vercel's scheduler calls it.

Incident: reminder emails never went out — April final-exam rows sat at
sent=false for six months and the new assessment backfill never ran. The
only trigger is vercel.json's `crons` entry, and Vercel cron (a) always
issues an HTTP GET and (b) can only send `Authorization: Bearer
<CRON_SECRET>`, never a custom X-Cron-Secret header. The route was
POST-only and read only X-Cron-Secret, so every scheduled run was rejected
(405, and 401 even if the method had matched) before doing any work.

These tests pin: both methods reach the handler, both header styles
authenticate, and bad/missing secrets are still rejected.
"""
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.routes import notifications
from api.routes.notifications import _cron_secret_ok

SECRET = "test-cron-secret-value"


@pytest.fixture(autouse=True)
def _configured_secret(monkeypatch):
    monkeypatch.setattr(notifications.settings, "CRON_SECRET", SECRET)


class TestCronSecretOk:
    def test_vercel_style_authorization_bearer(self):
        assert _cron_secret_ok(None, f"Bearer {SECRET}")

    def test_x_cron_secret_raw(self):
        assert _cron_secret_ok(SECRET, None)

    def test_x_cron_secret_with_bearer_prefix(self):
        assert _cron_secret_ok(f"Bearer {SECRET}", None)

    def test_wrong_secret_rejected(self):
        assert not _cron_secret_ok("nope", "Bearer also-nope")

    def test_missing_headers_rejected(self):
        assert not _cron_secret_ok(None, None)

    def test_empty_bearer_rejected(self):
        assert not _cron_secret_ok("", "Bearer ")

    def test_unconfigured_secret_never_authenticates(self, monkeypatch):
        monkeypatch.setattr(notifications.settings, "CRON_SECRET", "")
        assert not _cron_secret_ok("", "Bearer ")
        assert not _cron_secret_ok(None, None)


class TestCronEndpointMethodsAndAuth:
    """Rejection paths only — they return before any DB/email work, so these
    stay hermetic. (The success path is covered by the helper tests above
    plus the backfill tests.)"""

    def test_get_without_credentials_is_401_not_405(self):
        client = TestClient(app)
        resp = client.get("/api/notifications/cron")
        assert resp.status_code == 401  # reached the handler; 405 = the old bug

    def test_post_without_credentials_is_401(self):
        client = TestClient(app)
        assert client.post("/api/notifications/cron").status_code == 401

    def test_get_with_wrong_bearer_is_401(self):
        client = TestClient(app)
        resp = client.get("/api/notifications/cron", headers={"Authorization": "Bearer wrong"})
        assert resp.status_code == 401


class TestStaleReminderGuard:
    """Once the cron runs again it finds rows queued months ago for events
    that already happened (the April finals). They must be retired, not
    emailed with a negative 'days away' count."""

    def test_days_until_event(self):
        from datetime import date, timedelta
        from api.routes.notifications import _days_until_event
        assert _days_until_event((date.today() + timedelta(days=3)).isoformat()) == 3
        assert _days_until_event(date.today().isoformat()) == 0
        assert _days_until_event((date.today() - timedelta(days=170)).isoformat()) == -170

    def test_missing_or_garbage_date_is_none(self):
        from api.routes.notifications import _days_until_event
        assert _days_until_event(None) is None
        assert _days_until_event("") is None
        assert _days_until_event("not-a-date") is None
