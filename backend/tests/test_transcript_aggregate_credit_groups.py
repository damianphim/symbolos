"""
_expand_advanced_standing_groups turns an aggregate-heading section (a
printed total with no per-course credit numbers) into concrete
advanced_standing rows with a deterministically even split — Python does the
division so it can't get 24 / 6 wrong the way an LLM guessing per-course
credits did (see Sentry SYMBOLOS-BACKEND-1C's underlying bug report).
"""
from api.routes.transcript import _expand_advanced_standing_groups


def test_even_split_matches_printed_total():
    extracted = {"student_info": {"advanced_standing_groups": [
        {"heading": "Advanced Placement Exams", "total_credits": 24,
         "course_codes": ["ECON 1XX", "ECON 1XX", "ENGL 1XX", "FRSL 211", "MATH 203", "PSYC 100"]},
    ]}}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 6
    assert sum(c["credits"] for c in standing) == 24
    assert all(c["credits"] == 4 for c in standing)
    assert [c["course_code"] for c in standing] == ["ECON 1XX", "ECON 1XX", "ENGL 1XX", "FRSL 211", "MATH 203", "PSYC 100"]
    # groups key must not survive into the persisted shape
    assert "advanced_standing_groups" not in extracted["student_info"]


def test_uneven_split_puts_remainder_on_first_courses_and_still_sums_exactly():
    extracted = {"student_info": {"advanced_standing_groups": [
        {"heading": "IB Credits", "total_credits": 25,
         "course_codes": ["A 1XX", "B 1XX", "C 1XX", "D 1XX", "E 1XX", "F 1XX"]},
    ]}}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert sum(c["credits"] for c in standing) == 25
    # 25 // 6 = 4 remainder 1 -> one course gets 5, the rest get 4
    credits = [c["credits"] for c in standing]
    assert credits.count(5) == 1
    assert credits.count(4) == 5


def test_preserves_existing_explicit_advanced_standing_entries():
    extracted = {"student_info": {
        "advanced_standing": [{"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3}],
        "advanced_standing_groups": [
            {"heading": "CEGEP", "total_credits": 6, "course_codes": ["X 1XX", "Y 1XX"]},
        ],
    }}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 3
    assert standing[0]["course_code"] == "BIOL 111"
    assert sum(c["credits"] for c in standing[1:]) == 6


def test_no_groups_is_a_no_op():
    extracted = {"student_info": {"advanced_standing": [
        {"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3},
    ]}}
    _expand_advanced_standing_groups(extracted)
    assert extracted["student_info"]["advanced_standing"] == [
        {"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3},
    ]


def test_missing_student_info_does_not_crash():
    extracted = {}
    _expand_advanced_standing_groups(extracted)  # should not raise
    assert extracted == {}


def test_malformed_group_is_skipped_not_crashed():
    extracted = {"student_info": {"advanced_standing_groups": [
        {"heading": "Bad total", "total_credits": "not-a-number", "course_codes": ["A 1XX"]},
        {"heading": "No courses", "total_credits": 6, "course_codes": []},
        {"heading": "Out of range", "total_credits": 999, "course_codes": ["A 1XX"]},
        {"heading": "Good one", "total_credits": 6, "course_codes": ["A 1XX", "B 1XX"]},
    ]}}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 2
    assert sum(c["credits"] for c in standing) == 6
