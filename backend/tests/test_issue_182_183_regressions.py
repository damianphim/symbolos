import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest


def test_aggregate_cegep_and_u0_survive_import(monkeypatch, fake_supabase):
    from api.routes import transcript
    profile_updates = []
    monkeypatch.setattr(transcript, 'update_user', lambda uid, values: profile_updates.append(values))
    extracted = {
        'student_info': {'year': 0, 'advanced_standing': [
            {'course_code': 'CEGEP', 'course_title': 'CEGEP advanced standing', 'credits': 30},
            {'course_code': 'ECON 1XX', 'course_title': '', 'credits': 3},
            {'course_code': 'ECON 1XX', 'course_title': '', 'credits': 3},
        ]},
        'completed_courses': [{'course_code': 'BIOL 111', 'subject': 'BIOL', 'catalog': '111',
                               'course_title': 'Biology', 'term': 'Fall', 'year': 2025, 'grade': 'A', 'credits': 3}],
    }
    transcript._dedupe_extracted(extracted)
    result = transcript._persist_transcript_data('student', extracted, user_sb=fake_supabase)
    assert result['completed_added'] == 1
    assert profile_updates[0]['year'] == 0
    assert [c['credits'] for c in profile_updates[0]['advanced_standing']] == [30, 3, 3]


@pytest.mark.parametrize('invalid', ['invalid', float('nan'), float('inf'), -1, 61])
def test_import_rejects_invalid_standing_credits(monkeypatch, fake_supabase, invalid):
    from api.routes import transcript
    updates = []
    monkeypatch.setattr(transcript, 'update_user', lambda uid, values: updates.append(values))
    transcript._persist_transcript_data('student', {'student_info': {'advanced_standing': [
        {'course_code': 'CEGEP', 'credits': invalid}
    ]}}, user_sb=fake_supabase)
    assert not updates


@pytest.mark.asyncio
async def test_search_matches_subject_prefix_and_department_name(monkeypatch):
    from api.routes import courses
    monkeypatch.setattr(courses, 'get_subjects', AsyncMock(return_value={'subjects': ['MIMM', 'MATH']}))
    monkeypatch.setattr(courses.search_cache, 'get', lambda key: None)
    monkeypatch.setattr(courses.search_cache, 'set', lambda *args, **kwargs: None)
    calls = []
    def rpc(name, params):
        calls.append(params)
        rows = [{'subject': 'MIMM', 'catalog': '211', 'title': 'Microbiology'}] if params['p_subject'] == 'MIMM' else []
        return SimpleNamespace(execute=lambda: SimpleNamespace(data=rows))
    monkeypatch.setattr(courses, 'get_supabase', lambda: SimpleNamespace(rpc=rpc))
    for query in ['MIM', 'Microbiology and Immunology']:
        # Call the endpoint directly: the query and response values are explicit.
        result = await courses.search(query=query, subject=None, limit=50, include_ratings=True, term=None)
        assert json.loads(result.body)['courses'][0]['subject'] == 'MIMM'
        assert 'public' in result.headers['cache-control']
    assert any(call['p_query'] is None and call['p_subject'] == 'MIMM' for call in calls)


def test_completed_grade_can_be_cleared_without_losing_term(client, fake_supabase):
    fake_supabase.set_table('users', [{'id': 'user-1'}])
    fake_supabase.set_table('completed_courses', [{
        'user_id': 'user-1', 'course_code': 'MIMM 211', 'grade': 'B', 'term': 'Fall', 'year': 2025,
    }])
    response = client.patch('/api/completed/user-1/MIMM%20211', json={'grade': None}, headers={'Authorization': 'Bearer user-1'})
    assert response.status_code == 200
    course = response.json()['completed_course']
    assert course['grade'] is None
    assert course['term'] == 'Fall'
