"""
Tests for the forum "review" category unification (2026-07): course_review
and professor_review used to be two separate review types; a review post is
now always a course review with an optional professor attached, plus two
independent rating dimensions (overall `rating` and `difficulty_rating`).

Legacy course_review/professor_review posts must keep validating and
rendering the old way, and must still show up in the merged "review" feed.
"""
from __future__ import annotations

import pytest

from tests.conftest import auth


@pytest.fixture(autouse=True)
def no_resend(monkeypatch):
    from api import config
    monkeypatch.setattr(config.settings, "RESEND_API_KEY", "")


def _base_payload(**overrides):
    payload = {
        "author": "Some Student",
        "avatar_color": "#ed1b2f",
        "category": "review",
        "title": "Great course",
        "body": "Really enjoyed it.",
        "tags": [],
    }
    payload.update(overrides)
    return payload


# ── create_post: unified "review" category ────────────────────────────────

def test_create_review_requires_rating_and_difficulty(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(review_target_value="COMP 202", rating=4),  # no difficulty_rating
        headers=auth("user-1"),
    )
    assert resp.status_code == 422


def test_create_review_requires_course_code(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(rating=4, difficulty_rating=3),  # no review_target_value
        headers=auth("user-1"),
    )
    assert resp.status_code == 422


def test_create_review_professor_is_optional(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(review_target_value="COMP 202", rating=4, difficulty_rating=3),
        headers=auth("user-1"),
    )
    assert resp.status_code == 201
    post = resp.json()["post"]
    assert post["review_target_type"] == "course"
    assert post["review_target_value"] == "COMP 202"
    assert post["professor_name"] is None
    assert post["rating"] == 4
    assert post["difficulty_rating"] == 3


def test_create_review_with_professor_name(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(
            review_target_value="COMP 202", rating=5, difficulty_rating=2,
            professor_name="Joseph Vybihal",
        ),
        headers=auth("user-1"),
    )
    assert resp.status_code == 201
    post = resp.json()["post"]
    assert post["professor_name"] == "Joseph Vybihal"


def test_non_review_post_clears_review_fields(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(
            category="general", rating=5, difficulty_rating=2,
            review_target_value="COMP 202", professor_name="Someone",
        ),
        headers=auth("user-1"),
    )
    assert resp.status_code == 201
    post = resp.json()["post"]
    assert post["rating"] is None
    assert post["difficulty_rating"] is None
    assert post["review_target_value"] is None
    assert post["professor_name"] is None


# ── Legacy course_review/professor_review still validate the old way ──────

def test_legacy_course_review_still_works(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(category="course_review", review_target_value="COMP 202", rating=4),
        headers=auth("user-1"),
    )
    assert resp.status_code == 201
    post = resp.json()["post"]
    assert post["review_target_type"] == "course"
    assert post["difficulty_rating"] is None   # legacy posts never set this
    assert post["professor_name"] is None


def test_legacy_professor_review_still_works(client, fake_supabase):
    resp = client.post(
        "/api/forum/posts",
        json=_base_payload(category="professor_review", review_target_value="Joseph Vybihal", rating=5),
        headers=auth("user-1"),
    )
    assert resp.status_code == 201
    post = resp.json()["post"]
    assert post["review_target_type"] == "professor"


# ── list_posts: the merged "review" feed includes legacy categories ────────

def test_review_feed_includes_legacy_categories(client, fake_supabase):
    fake_supabase.set_table("forum_posts", [
        {"id": "p1", "user_id": "u1", "author": "A", "avatar_color": "#ed1b2f",
         "category": "review", "title": "New-style review", "body": "b", "tags": [],
         "program_info": None, "rating": 4, "difficulty_rating": 3,
         "review_target_type": "course", "review_target_value": "COMP 202",
         "professor_name": None, "like_count": 0, "created_at": "2026-07-01T00:00:00Z"},
        {"id": "p2", "user_id": "u1", "author": "A", "avatar_color": "#ed1b2f",
         "category": "course_review", "title": "Old-style course review", "body": "b", "tags": [],
         "program_info": None, "rating": 3, "difficulty_rating": None,
         "review_target_type": "course", "review_target_value": "MATH 133",
         "professor_name": None, "like_count": 0, "created_at": "2026-06-01T00:00:00Z"},
        {"id": "p3", "user_id": "u1", "author": "A", "avatar_color": "#ed1b2f",
         "category": "professor_review", "title": "Old-style prof review", "body": "b", "tags": [],
         "program_info": None, "rating": 5, "difficulty_rating": None,
         "review_target_type": "professor", "review_target_value": "Some Prof",
         "professor_name": None, "like_count": 0, "created_at": "2026-05-01T00:00:00Z"},
        {"id": "p4", "user_id": "u1", "author": "A", "avatar_color": "#ed1b2f",
         "category": "general", "title": "Not a review", "body": "b", "tags": [],
         "program_info": None, "rating": None, "difficulty_rating": None,
         "review_target_type": None, "review_target_value": None,
         "professor_name": None, "like_count": 0, "created_at": "2026-05-02T00:00:00Z"},
    ])

    resp = client.get("/api/forum/posts", params={"category": "review", "sort": "new"}, headers=auth("user-1"))
    assert resp.status_code == 200
    ids = {p["id"] for p in resp.json()["posts"]}
    assert ids == {"p1", "p2", "p3"}
    assert "p4" not in ids


# ── reviews_summary: professor lookups merge legacy + new shapes ──────────

def test_reviews_summary_professor_merges_legacy_and_named(client, fake_supabase):
    fake_supabase.set_table("forum_posts", [
        # Legacy: professor WAS the review target
        {"id": "p1", "review_target_type": "professor", "review_target_value": "Joseph Vybihal",
         "professor_name": None, "rating": 4, "difficulty_rating": None},
        # Unified: professor named on a course review
        {"id": "p2", "review_target_type": "course", "review_target_value": "COMP 202",
         "professor_name": "Joseph Vybihal", "rating": 2, "difficulty_rating": 5},
    ])

    resp = client.get(
        "/api/forum/reviews/summary",
        params={"target_type": "professor", "target_value": "Joseph Vybihal"},
        headers=auth("user-1"),
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["rating_count"] == 2
    assert data["avg_rating"] == 3.0
    assert data["avg_difficulty"] == 5.0
