"""
pytest fixtures shared by the security smoke tests.

We don't talk to Supabase / Anthropic / Resend in CI. Every external
client is patched here so the tests run hermetically in <1s.

IMPORTANT: FastAPI captures dependency references at route-definition
time, so `monkeypatch.setattr(auth_module, ...)` does NOT override what
`Depends(get_current_user_id)` resolves to. The correct override is
`app.dependency_overrides[get_current_user_id] = fake_fn`, which we do
inside the `client` fixture below.
"""
from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

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
    def __init__(self, name: str, data):
        self._name = name
        self._data = data if data is not None else []
        self._eq_filters: list = []

    def select(self, *args, **kwargs):
        return self

    def eq(self, col, val):
        self._eq_filters.append((col, val))
        return self

    def ilike(self, col, val):
        return self

    def or_(self, *args, **kwargs):
        """PostgREST OR — no-op shim. The endpoints we test apply a
        Python-side filter as defense in depth, so the security
        assertions still hold even when this no-ops."""
        return self

    def order(self, *args, **kwargs):
        return self

    def limit(self, n):
        return self

    def in_(self, col, vals):
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
        rows = list(self._data)
        for col, val in self._eq_filters:
            rows = [r for r in rows if r.get(col) == val]
        return SimpleNamespace(data=rows, count=len(rows))


class FakeSupabase:
    """Stand-in for the supabase client. Tests can pre-seed tables via
    `.set_table('users', [...])`."""
    def __init__(self, auth_email: str = "tester@mail.mcgill.ca"):
        self._tables: dict = {}
        self.auth = SimpleNamespace(admin=FakeAuthAdmin(email=auth_email))

    def set_table(self, name: str, rows: list) -> None:
        self._tables[name] = rows

    def table(self, name: str) -> FakeTable:
        return FakeTable(name, self._tables.setdefault(name, []))

    def rpc(self, *args, **kwargs):
        return SimpleNamespace(execute=lambda: SimpleNamespace(data=1))


@pytest.fixture
def fake_supabase(monkeypatch):
    """Patch every importable get_supabase reference so all routes see
    the fake regardless of where they imported it from."""
    sb = FakeSupabase()
    # Patch at the canonical module location.
    import api.utils.supabase_client as supa
    monkeypatch.setattr(supa, "get_supabase", lambda: sb)
    monkeypatch.setattr(supa, "get_user_supabase", lambda jwt: sb)

    # Routes do `from ..utils.supabase_client import get_supabase` at
    # module load time, which BINDS the original function into their
    # own module namespace. We need to override THOSE bindings too.
    for module_path in (
        "api.routes.clubs",
        "api.routes.users",
        "api.routes.verification",
        "api.routes.forum",
        "api.routes.cards",
        "api.routes.chat",
        "api.routes.courses",
        "api.routes.webhooks",
        "api.utils.verified_user",
        "api.utils.llm_budget",
        "api.utils.anomaly",
        "api.main",
    ):
        try:
            mod = __import__(module_path, fromlist=["get_supabase"])
        except Exception:
            continue
        if hasattr(mod, "get_supabase"):
            monkeypatch.setattr(mod, "get_supabase", lambda: sb)
    return sb


@pytest.fixture
def client(fake_supabase, monkeypatch):
    """A FastAPI TestClient with auth dependencies overridden.

    Tests pass `X-Test-User: <id>` to identify themselves. No header
    means the unauthenticated case (expect 401).
    """
    from fastapi import HTTPException, Request
    from fastapi.testclient import TestClient
    from api.main import app
    from api.auth import get_current_user_id, get_current_jwt, get_user_db

    async def _fake_get_user(request: Request):
        uid = request.headers.get("x-test-user")
        if not uid:
            raise HTTPException(status_code=401, detail="Missing test auth header")
        return uid

    async def _fake_get_jwt(request: Request):
        return request.headers.get("x-test-user", "")

    async def _fake_get_db(request: Request):
        return fake_supabase

    # FastAPI overrides — the correct way to swap deps in tests.
    app.dependency_overrides[get_current_user_id] = _fake_get_user
    app.dependency_overrides[get_current_jwt]    = _fake_get_jwt
    app.dependency_overrides[get_user_db]        = _fake_get_db

    # Also override the email-verified gate so tests don't trip on it.
    from api.utils import verified_user as vu
    monkeypatch.setattr(vu, "is_email_verified", lambda _uid: True)
    # And the LLM budget gate.
    from api.utils import llm_budget as lb
    monkeypatch.setattr(lb, "check_and_record_llm_usage", lambda *a, **kw: None)

    tc = TestClient(app)
    try:
        yield tc
    finally:
        app.dependency_overrides.clear()
