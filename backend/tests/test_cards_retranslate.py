"""
Tests for _parse_cards_lenient() — the fallback used by /api/cards/retranslate/
when json.loads() fails on Claude's full card array.

Sentry: "Retranslate JSON parse error: Expecting ',' delimiter: line 21
column 56 (char 541)" — Claude occasionally drops a comma between two card
objects. The existing retry-once mechanism only helps if the retried call
comes back clean; when it doesn't, the old code raised and lost every card
in the batch over one bad delimiter. _parse_cards_lenient recovers whichever
individual card objects DO parse instead of failing the whole response.
"""
from __future__ import annotations

from api.routes.cards import _parse_cards_lenient


def test_recovers_all_cards_when_json_is_valid():
    raw = '[{"title": "A", "body": "one"}, {"title": "B", "body": "two"}]'
    assert _parse_cards_lenient(raw) == [
        {"title": "A", "body": "one"},
        {"title": "B", "body": "two"},
    ]


def test_recovers_remaining_cards_around_a_missing_comma():
    # No comma between the two objects — json.loads() on the whole array
    # would raise "Expecting ',' delimiter" here.
    raw = '[{"title": "A", "body": "one"} {"title": "B", "body": "two"}]'
    assert _parse_cards_lenient(raw) == [
        {"title": "A", "body": "one"},
        {"title": "B", "body": "two"},
    ]


def test_skips_only_the_individually_malformed_card():
    raw = '[{"title": "Good"}, {"title": "Bad" "missing_colon_comma": true}, {"title": "Also good"}]'
    assert _parse_cards_lenient(raw) == [{"title": "Good"}, {"title": "Also good"}]


def test_returns_empty_list_for_unrecoverable_garbage():
    assert _parse_cards_lenient("not json at all") == []


def test_handles_nested_objects_correctly():
    raw = '[{"title": "A", "actions": [{"label": "x"}]}]'
    assert _parse_cards_lenient(raw) == [{"title": "A", "actions": [{"label": "x"}]}]
