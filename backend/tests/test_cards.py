"""
Tests for backend/api/routes/cards.py bug fixes:

1. PATCH /api/cards/{user_id}/reorder — Sentry: `null value in column
   "sort_order" of relation "advisor_cards" violates not-null constraint`,
   27 events, ongoing 4 weeks (every reorder attempt). The frontend always
   sends {id, sort_order} (AdvisorCards.jsx), which CardOrder.resolved_position
   correctly resolves to an int, but the RPC payload only ever included a
   "position" key — if the reorder_advisor_cards RPC (defined in Supabase,
   not in this repo) reads "sort_order" from each payload item to fill the
   sort_order column, that key was simply never present, writing NULL
   every time.

2. save_cards() — Sentry: `insert or update on table "advisor_cards"
   violates foreign key constraint "advisor_cards_user_id_fkey"` on
   POST /api/cards/stream/{user_id}. Streamed card generation can run for
   tens of seconds; if the account is deleted mid-stream, user_id no
   longer exists by the time save_cards persists the generated cards.
"""
from __future__ import annotations

from types import SimpleNamespace

import pytest
from postgrest.exceptions import APIError

from tests.conftest import auth
from api.routes.cards import save_cards


def test_reorder_sends_both_position_and_sort_order_keys(client, fake_supabase):
    fake_supabase.set_table("users", [{"id": "user-1", "email": "tester@mail.mcgill.ca"}])

    captured = {}

    def _rpc(name, params, *args, **kwargs):
        captured["name"] = name
        captured["params"] = params
        return SimpleNamespace(execute=lambda: SimpleNamespace(data=1))

    fake_supabase.rpc = _rpc

    resp = client.patch(
        "/api/cards/user-1/reorder",
        json={"order": [{"id": "card-1", "sort_order": 0}, {"id": "card-2", "sort_order": 1}]},
        headers=auth("user-1"),
    )
    assert resp.status_code == 200
    assert resp.json() == {"reordered": 2}

    assert captured["name"] == "reorder_advisor_cards"
    payload = captured["params"]["payload"]
    assert payload == [
        {"id": "card-1", "position": 0, "sort_order": 0},
        {"id": "card-2", "position": 1, "sort_order": 1},
    ]


def test_reorder_resolves_position_field_too(client, fake_supabase):
    """Older/other callers sending 'position' instead of 'sort_order' still work."""
    fake_supabase.set_table("users", [{"id": "user-1", "email": "tester@mail.mcgill.ca"}])

    captured = {}

    def _rpc(name, params, *args, **kwargs):
        captured["params"] = params
        return SimpleNamespace(execute=lambda: SimpleNamespace(data=1))

    fake_supabase.rpc = _rpc

    resp = client.patch(
        "/api/cards/user-1/reorder",
        json={"order": [{"id": "card-1", "position": 3}]},
        headers=auth("user-1"),
    )
    assert resp.status_code == 200
    assert captured["params"]["payload"] == [{"id": "card-1", "position": 3, "sort_order": 3}]


# ── save_cards: FK violation from a mid-stream account deletion ────────────

class _RaisingTable:
    """Stands in for supabase.table("advisor_cards") — delete() is a no-op,
    insert().execute() raises the given error."""
    def __init__(self, error):
        self._error = error
        self._is_insert = False
    def delete(self): return self
    def eq(self, *a, **kw): return self
    def insert(self, rows):
        self._is_insert = True
        return self
    def execute(self):
        if self._is_insert and self._error is not None:
            raise self._error
        return SimpleNamespace(data=[])


def test_save_cards_swallows_fk_violation_from_deleted_user(fake_supabase, monkeypatch):
    error = APIError({"code": "23503", "message": "FK violation", "details": None, "hint": None})
    monkeypatch.setattr(fake_supabase, "table", lambda name: _RaisingTable(error))

    # Should not raise — the user is gone, nothing left to persist for.
    save_cards("deleted-user", [{"title": "t", "body": "b", "type": "insight"}])


def test_save_cards_reraises_other_db_errors(fake_supabase, monkeypatch):
    error = APIError({"code": "42P01", "message": "undefined_table", "details": None, "hint": None})
    monkeypatch.setattr(fake_supabase, "table", lambda name: _RaisingTable(error))

    with pytest.raises(APIError):
        save_cards("user-1", [{"title": "t", "body": "b", "type": "insight"}])
