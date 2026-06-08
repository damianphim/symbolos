"""
pytest fixtures shared by the security smoke tests.

We don't talk to Supabase / Anthropic / Resend in CI. Every external
client is patched here so the tests run hermetically in <1s.
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import pytest

# Make `api.*` importable regardless of where pytest is invoked from.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


class FakeAuthAdmin:
    """Mimics supabase.auth.admin.get_user — returns a user object whose
    `email` attribute matches whatever the test sets up."""
    def __init__(self, email: str = "tester@mail.mcgill.ca"):
        self.email = email
        self.confirmed = True

    def get_user(self, user_id: str):
        user = SimpleNamespace(
            id=user_id,
            email=self.email,
            created_at="2025-01-01T00:00:00Z",
            last_sign_in_at="2025-06-01T00:00:00Z",
            email_confirmed_at="2025-01-01T00:00:00Z" if self.confirmed else None,
        )
        return SimpleNamespace(user=user)


class FakeTable:
    """Records every query and returns canned data."""
    def __init__(self, name: str, data: list[dict] | None = None):
        self._name = name
        self._data = data or []
        self._eq_filters: list[tuple[str, object]] = []
        self._in_filters: list[tuple[str, list]] = []

    def select(self, *args, **kwargs):
        return self

    def eq(self, col, val):
        self._eq_filters.append((col, val))
        return self

    def ilike(self, col, val):
        return self

    def or_(self, *args, **kwargs):
        """PostgREST-style OR expression. We don't parse it — the security
        tests still get protected by the application-layer Python filter
        we apply on top of the query, which is the defense-in-depth point."""
        return self

    def order(self, *args, **kwargs):
        return self

    def limit(self, n):
        return self

    def in_(self, col, vals):
        self._in_filters.append((col, vals))
        return self

    def single(self):
        return self

    def insert(self, row):
        self._data.append(row if isinstance(row, dict) else dict(row))
        return self

    def update(self, row):
        return self

    def delete(self):
        return self

    def execute(self):
        # Apply naive eq filtering for the tests that care
        rows = list(self._data)
        for col, val in self._eq_filters:
            rows = [r for r in rows if r.get(col) == val]
        return SimpleNamespace(data=rows, count=len(rows))


class FakeSupabase:
    """Stand-in for the supabase client. Tests can pre-seed tables via
    `.set_table('users', [...])`."""
    def __init__(self, auth_email: str = "tester@mail.mcgill.ca"):
        self._tables: dict[str, list[dict]] = {}
        self.auth = SimpleNamespace(admin=FakeAuthAdmin(email=auth_email))

    def set_table(self, name: str, rows: list[dict]) -> None:
        self._tables[name] = rows

    def table(self, name: str) -> FakeTable:
        return FakeTable(name, self._tables.setdefault(name, []))

    def rpc(self, *args, **kwargs):
        return SimpleNamespace(execute=lambda: SimpleNamespace(data=1))


@pytest.fixture
def fake_supabase(monkeypatch):
    sb = FakeSupabase()
    # Patch every importable get_supabase reference so all routes see the fake.
    import api.utils.supabase_client as supa
    monkeypatch.setattr(supa, "get_supabase", lambda: sb)
    monkeypatch.setattr(supa, "get_user_supabase", lambda jwt: sb)
    return sb


@pytest.fixture
def client(fake_supabase, monkeypatch):
    """A FastAPI TestClient with auth dependencies stubbed.

    Tests can override the authenticated user by setting
    `client.headers['X-Test-User']` and the test middleware below picks it up.
    """
    # Bypass JWT verification: a fake get_current_user_id reads a header.
    from fastapi import HTTPException
    from api import auth as auth_module

    async def _fake_get_user(request):
        uid = request.headers.get("x-test-user")
        if not uid:
            raise HTTPException(status_code=401, detail="Missing test auth header")
        return uid

    async def _fake_get_jwt(request):
        return request.headers.get("x-test-user", "")

    async def _fake_get_db(request):
        return fake_supabase

    monkeypatch.setattr(auth_module, "get_current_user_id", _fake_get_user)
    monkeypatch.setattr(auth_module, "get_current_jwt", _fake_get_jwt)
    monkeypatch.setattr(auth_module, "get_user_db", _fake_get_db)

    # And in routes that re-import them at module load — patch the references
    # already bound on those modules.
    from api.routes import clubs, users as users_route, verification as ver_route, forum
    for mod in (clubs, users_route, ver_route, forum):
        if hasattr(mod, "get_current_user_id"):
            monkeypatch.setattr(mod, "get_current_user_id", _fake_get_user)
        if hasattr(mod, "get_user_db"):
            monkeypatch.setattr(mod, "get_user_db", _fake_get_db)

    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)
