"""
_generate_ics produces the .ics content served by the personal calendar feed
(GET /api/notifications/feed/{token}.ics), which Apple/Google/Outlook fetch
directly — it must be well-formed RFC 5545, mirroring the frontend's
generateICS() in calendarUtils.js so the one-time download and the live
subscription produce equivalent output.
"""
from api.routes.notifications import _generate_ics, _ics_escape, _ics_datetime


def test_timed_event_has_utc_datetime_start_and_end():
    ics = _generate_ics([
        {"id": "1", "title": "COMP 202 Lecture", "date": "2026-09-15", "time": "10:00"},
    ])
    assert "DTSTART:20260915T100000Z" in ics
    assert "DTEND:20260915T110000Z" in ics  # defaults to +1h when no end_time
    assert "SUMMARY:COMP 202 Lecture" in ics


def test_explicit_end_time_is_used_over_default():
    ics = _generate_ics([
        {"id": "1", "title": "Exam", "date": "2026-12-10", "time": "09:00", "end_time": "11:30"},
    ])
    assert "DTSTART:20261210T090000Z" in ics
    assert "DTEND:20261210T113000Z" in ics


def test_all_day_event_uses_date_value_not_datetime():
    ics = _generate_ics([{"id": "1", "title": "Registration opens", "date": "2026-11-01"}])
    assert "DTSTART;VALUE=DATE:20261101" in ics
    assert "DTEND;VALUE=DATE:20261101" in ics
    assert "DTSTART:2026" not in ics  # no bare timed DTSTART


def test_special_characters_are_escaped():
    escaped = _ics_escape("Meeting; agenda, notes\nline two")
    assert escaped == "Meeting\\; agenda\\, notes\\nline two"


def test_valid_calendar_envelope():
    ics = _generate_ics([{"id": "1", "title": "Test", "date": "2026-01-01"}])
    assert ics.startswith("BEGIN:VCALENDAR")
    assert ics.endswith("END:VCALENDAR")
    assert "VERSION:2.0" in ics
    assert ics.count("BEGIN:VEVENT") == 1
    assert ics.count("END:VEVENT") == 1


def test_multiple_events_and_optional_fields():
    ics = _generate_ics([
        {"id": "1", "title": "A", "date": "2026-01-01", "description": "desc", "location": "Loc", "category": "exam"},
        {"id": "2", "title": "B", "date": "2026-01-02"},
    ])
    assert ics.count("BEGIN:VEVENT") == 2
    assert "DESCRIPTION:desc" in ics
    assert "LOCATION:Loc" in ics
    assert "CATEGORIES:exam" in ics


def test_event_missing_date_is_skipped_not_crashed():
    ics = _generate_ics([
        {"id": "1", "title": "No date"},
        {"id": "2", "title": "Has date", "date": "2026-01-01"},
    ])
    assert ics.count("BEGIN:VEVENT") == 1
    assert "Has date" in ics


def test_empty_events_list_still_produces_valid_empty_calendar():
    ics = _generate_ics([])
    assert "BEGIN:VCALENDAR" in ics
    assert "END:VCALENDAR" in ics
    assert "BEGIN:VEVENT" not in ics


def test_ics_datetime_pads_single_digit_components():
    assert _ics_datetime("2026-1-5", "9:5") == "20260105T090500"
    assert _ics_datetime("2026-01-05", None) == "20260105"
