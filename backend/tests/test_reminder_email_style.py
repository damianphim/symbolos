"""
Calendar reminder emails must stay plain: one box with the reminder and a
link to the site. No emojis, no em/en dashes, no gradient or badge decoration.
"""
import re

import pytest

from api.routes.notifications import _build_html_email

# Emoji, pictographs, dingbats, arrows, variation selectors, and em/en dashes.
_BANNED = re.compile(
    "[–—←-⇿☀-➿⬀-⯿️"
    "\U0001f000-\U0001faff]"
)


@pytest.mark.parametrize("days", [0, 1, 3, 7])
@pytest.mark.parametrize("etype", ["exam", "quiz", "assignment", "midterm", "personal", "academic"])
def test_no_emojis_or_dashes(days, etype):
    subject, html = _build_html_email("MATH 323 Final Exam", "2026-12-10", etype, days)
    assert not _BANNED.search(subject), subject
    match = _BANNED.search(html)
    assert match is None, f"banned char {match.group()!r} in html"


def test_subjects_are_simple():
    assert _build_html_email("Quiz 2", "2026-10-10", "quiz", 0)[0] == "Today: Quiz 2"
    assert _build_html_email("Quiz 2", "2026-10-10", "quiz", 1)[0] == "Tomorrow: Quiz 2"
    assert _build_html_email("Quiz 2", "2026-10-10", "quiz", 7)[0] == "Quiz 2 in 7 days"


def test_contains_reminder_link_and_footer():
    _, html = _build_html_email("Quiz 2", "2026-10-10", "quiz", 7)
    assert "Quiz 2" in html
    assert "2026-10-10" in html
    assert 'href="https://symbolos.ca"' in html
    assert "gradient" not in html
    assert "Unsubscribe" in html or "unsubscribe" in html or "notification preferences" in html


def test_title_is_escaped():
    _, html = _build_html_email("<script>x</script>", "2026-10-10", "personal", 1)
    assert "<script>" not in html
