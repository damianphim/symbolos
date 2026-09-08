import { describe, it, expect, vi, afterEach } from 'vitest'
vi.mock('./supabase', () => ({supabase: {auth: {getSession: async () => ({data: {session: {access_token: 'test'}}})}}}))
import completedCoursesAPI from './completedCoursesAPI'
afterEach(() => vi.unstubAllGlobals())
describe('Completed courses pagination', () => {
  it('keeps older courses and normalizes codes across pages', async () => {
    const fetch = vi.fn()
      .mockResolvedValueOnce({ok: true, json: async () => ({completed_courses: [{course_code: 'MIMM211'}], next_cursor: 'older'})})
      .mockResolvedValueOnce({ok: true, json: async () => ({completed_courses: [{course_code: 'BIOL 111'}], next_cursor: null})})
    vi.stubGlobal('fetch', fetch)
    const result = await completedCoursesAPI.getCompleted('student')
    expect(result.completed_courses.map(c => c.course_code)).toEqual(['MIMM 211', 'BIOL 111'])
    expect(fetch.mock.calls[1][0]).toContain('cursor=older')
  })
})
