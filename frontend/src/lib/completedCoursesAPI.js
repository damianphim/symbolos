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
    const response = await fetch(`${BASE_URL}/api/completed/${userId}`, {
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch completed courses')
    return response.json()
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
