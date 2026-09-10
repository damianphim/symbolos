"""
Transcript import 422'd for every double-major/double-minor student.

The extraction prompt asks Claude for student_info.major/minor as a single
string (e.g. "Computer Science"), but a student with two concurrent majors
or minors reasonably gets Claude to return a list of them instead
(["Economics", "International Development Studies"]). The parse/preview
step doesn't validate against a strict schema, so it always "succeeded" —
but POST /api/transcript/import/{user_id} deserializes the body into
ImportRequest, whose _StudentInfo.major/minor were typed `str | None`,
so FastAPI rejected the confirm-import request outright before any
application code ran. The student saw a generic "Something went wrong"
with no record of it anywhere, since import isn't tracked as a job.

Same class of bug as SYMBOLOS-BACKEND-1B (syllabus instructor list) —
never trust an LLM's output to match the requested schema exactly.
"""
from __future__ import annotations

from api.routes.transcript import ImportRequest, _StudentInfo


class TestDoubleMajorMinorImport:
    def test_list_major_and_minor_join_into_a_string(self):
        info = _StudentInfo(
            major=["Economics", "International Development Studies"],
            minor=["Mathematics", "Hispanic Studies"],
        )
        assert info.major == "Economics / International Development Studies"
        assert info.minor == "Mathematics / Hispanic Studies"

    def test_single_major_string_is_unaffected(self):
        info = _StudentInfo(major="Computer Science", minor="Science for Arts Students")
        assert info.major == "Computer Science"
        assert info.minor == "Science for Arts Students"

    def test_empty_major_list_becomes_none(self):
        info = _StudentInfo(major=[], minor=None)
        assert info.major is None
        assert info.minor is None

    def test_full_import_request_with_double_major_validates(self):
        """Regression: this exact shape 422'd before the fix."""
        body = {
            "student_info": {
                "major": ["Economics", "International Development Studies"],
                "minor": ["Mathematics", "Hispanic Studies"],
                "faculty": "Arts",
                "year": 3,
                "cum_gpa": 3.07,
            },
            "completed_courses": [
                {"course_code": "ECON 230D1", "course_title": "Microeconomic Theory", "grade": "B+", "credits": 3}
            ],
            "current_courses": [],
        }
        req = ImportRequest(**body)
        assert req.student_info.major == "Economics / International Development Studies"
        assert req.student_info.minor == "Mathematics / Hispanic Studies"
