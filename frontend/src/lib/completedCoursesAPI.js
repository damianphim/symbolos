import { BASE_URL } from './apiConfig'
import { supabase } from './supabase'

async function authHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
}

export const completedCoursesAPI = {
  async getCompleted(userId) {
    const headers = await authHeaders()
    const courses = []
    let cursor = null
    const seen = new Set()
    do {
      const params = new URLSearchParams({ limit: '200' })
      if (cursor) params.set('cursor', cursor)
      const response = await fetch(`${BASE_URL}/api/completed/${userId}?${params}`, { headers })
      if (!response.ok) throw new Error('Failed to fetch completed courses')
      const data = await response.json()
      courses.push(...(data.completed_courses || []).map(course => {
        const code = (course.course_code || `${course.subject} ${course.catalog}`).trim().toUpperCase().replace(/^([A-Z]+)(\d)/, '$1 $2')
        const [subject, catalog] = code.split(/\s+/)
        return { ...course, course_code: code, subject: course.subject || subject, catalog: course.catalog || catalog }
      }))
      cursor = data.next_cursor
      if (!data.completed_courses?.length || !cursor || seen.has(cursor)) break
      seen.add(cursor)
    } while (cursor)
    return { completed_courses: courses, count: courses.length }

  },

  async addCompleted(userId, courseData) {
    const response = await fetch(`${BASE_URL}/api/completed/${userId}`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({
        course_code: courseData.course_code,
        course_title: courseData.course_title,
        subject: courseData.subject,
        catalog: courseData.catalog,
        term: courseData.term,
        year: courseData.year,
        grade: courseData.grade || null,
        credits: courseData.credits || 3,
      }),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to add completed course')
    }
    return response.json()
  },

  async updateCompleted(userId, courseCode, updates) {
    const response = await fetch(`${BASE_URL}/api/completed/${userId}/${encodeURIComponent(courseCode)}`, {
      method: 'PATCH',
      headers: await authHeaders(),
      body: JSON.stringify(updates),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to update completed course')
    }
    return response.json()
  },

  async removeCompleted(userId, courseCode) {
    const response = await fetch(`${BASE_URL}/api/completed/${userId}/${encodeURIComponent(courseCode)}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to remove completed course')
    return response.json()
  },
}

export default completedCoursesAPI
