"""
_expand_ap_exams resolves each printed AP subject to its exact McGill
course(s)/credits via AP_CREDIT_TABLE (scraped from
mcgill.ca/transfercredit/prospective/ap), instead of an even split — the
real per-subject values aren't uniform (e.g. the same "24 credits" block is
Macroeconomics=3, Microeconomics=3, English Literature=6, French=6,
Statistics=3, Psychology=3, not 4 each).
"""
from api.routes.transcript import _expand_ap_exams


def test_real_world_24_credit_block_matches_exact_per_subject_values():
    extracted = {"student_info": {"ap_exams": [
        "Macroeconomics", "Microeconomics", "English Literature and Composition",
        "French Language and Culture", "Statistics", "Psychology",
    ]}}
    _expand_ap_exams(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert sum(c["credits"] for c in standing) == 24
    by_code = {}
    for c in standing:
        by_code.setdefault(c["course_code"], []).append(c["credits"])
    assert by_code["ECON 1XX"] == [3, 3]
    assert by_code["ENGL 1XX"] == [6]
    assert by_code["FRSL 211"] == [6]
    assert by_code["MATH 203"] == [3]
    assert by_code["PSYC 100"] == [3]
    # ap_exams must not survive into the persisted shape
    assert "ap_exams" not in extracted["student_info"]


def test_multi_course_subject_splits_into_separate_rows():
    extracted = {"student_info": {"ap_exams": ["Biology"]}}
    _expand_ap_exams(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 2
    codes = {c["course_code"]: c["credits"] for c in standing}
    assert codes == {"BIOL 111": 3, "BIOL 112": 3}


def test_zero_credit_subject_is_recognized_and_adds_nothing():
    extracted = {"student_info": {"ap_exams": ["Precalculus"]}}
    _expand_ap_exams(extracted)
    assert extracted["student_info"]["advanced_standing"] == []


def test_ap_prefix_and_case_are_normalized():
    extracted = {"student_info": {"ap_exams": ["AP Psychology", "  statistics  "]}}
    _expand_ap_exams(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    codes = sorted(c["course_code"] for c in standing)
    assert codes == ["MATH 203", "PSYC 100"]


def test_unrecognized_subject_is_skipped_not_crashed():
    extracted = {"student_info": {"ap_exams": ["Not A Real AP Subject", "Psychology"]}}
    _expand_ap_exams(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 1
    assert standing[0]["course_code"] == "PSYC 100"


def test_preserves_existing_advanced_standing_entries():
    extracted = {"student_info": {
        "advanced_standing": [{"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3}],
        "ap_exams": ["Statistics"],
    }}
    _expand_ap_exams(extracted)
    standing = extracted["student_info"]["advanced_standing"]
    assert len(standing) == 2
    assert standing[0]["course_code"] == "BIOL 111"
    assert standing[1]["course_code"] == "MATH 203"


def test_no_ap_exams_is_a_no_op():
    extracted = {"student_info": {"advanced_standing": [
        {"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3},
    ]}}
    _expand_ap_exams(extracted)
    assert extracted["student_info"]["advanced_standing"] == [
        {"course_code": "BIOL 111", "course_title": "Biology 1", "credits": 3},
    ]


def test_missing_student_info_does_not_crash():
    extracted = {}
    _expand_ap_exams(extracted)
    assert extracted == {}
