"""
_expand_advanced_standing_groups turns an aggregate-heading section (a
printed total with no per-course credit numbers) into concrete
advanced_standing rows. Known codes (AP especially, via
AP_COURSE_CREDIT_LOOKUP) get their exact McGill credit value; only the
remainder is split evenly across codes with no known value — a plain even
split gets individual AP courses wrong even when the total happens to match
(see Sentry SYMBOLOS-BACKEND-1C's underlying bug report, and the live-test
regression: an even split of this exact 24-credit block gave 4 credits to
every course, but the real values are 3, 3, 6, 6, 3, 3).
"""
from api.routes.transcript import _expand_advanced_standing_groups


def test_real_world_ap_block_matches_exact_per_course_values():
    """The exact "Advanced Placement Exams - 24 credits" block from a real
    Minerva transcript that exposed the even-split bug live."""
    extracted = {"student_info": {"advanced_standing_groups": [
        {"heading": "Advanced Placement Exams", "total_credits": 24,
         "course_codes": ["ECON 1XX", "ECON 1XX", "ENGL 1XX", "FRSL 211", "MATH 203", "PSYC 100"]},
    ]}}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 6
    assert sum(c["credits"] for c in standing) == 24
    credits_by_code = [(c["course_code"], c["credits"]) for c in standing]
    assert credits_by_code == [
        ("ECON 1XX", 3), ("ECON 1XX", 3), ("ENGL 1XX", 6),
        ("FRSL 211", 6), ("MATH 203", 3), ("PSYC 100", 3),
    ]
    # groups key must not survive into the persisted shape
    assert "advanced_standing_groups" not in extracted["student_info"]


def test_unknown_codes_split_only_the_remainder_after_known_codes_claim_theirs():
    # ECON 1XX is known (3cr); the two made-up codes split whatever's left.
    extracted = {"student_info": {"advanced_standing_groups": [
        {"heading": "Mixed", "total_credits": 13,
         "course_codes": ["ECON 1XX", "ZZZZ 1XX", "YYYY 1XX"]},
    ]}}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    by_code = {c["course_code"]: c["credits"] for c in standing}
    assert by_code["ECON 1XX"] == 3
    assert by_code["ZZZZ 1XX"] + by_code["YYYY 1XX"] == 10
    assert sum(c["credits"] for c in standing) == 13


def test_all_unknown_codes_fall_back_to_even_split_of_full_total():
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


def test_known_codes_total_exceeding_printed_total_leaves_unknowns_at_zero():
    # If known-code credits alone already reach (or exceed) the printed
    # total, remaining is clamped to 0 rather than going negative.
    extracted = {"student_info": {"advanced_standing_groups": [
        {"heading": "Odd", "total_credits": 3,
         "course_codes": ["ENGL 1XX", "ZZZZ 1XX"]},  # ENGL 1XX alone is 6cr
    ]}}
    _expand_advanced_standing_groups(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    by_code = {c["course_code"]: c["credits"] for c in standing}
    assert by_code["ENGL 1XX"] == 6
    assert by_code["ZZZZ 1XX"] == 0


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
