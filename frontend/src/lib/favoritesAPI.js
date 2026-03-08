import { BASE_URL } from './apiConfig'
import { supabase } from './supabase'

async function authHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
}

export const favoritesAPI = {
  async getFavorites(userId) {
    const response = await fetch(`${BASE_URL}/api/favorites/${userId}`, {
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch favorites')
    return response.json()
  },

  async addFavorite(userId, courseData) {
    const response = await fetch(`${BASE_URL}/api/favorites/${userId}`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({
        course_code: courseData.course_code,
        course_title: courseData.course_title,
        subject: courseData.subject,
        catalog: courseData.catalog,
      }),
    })
    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.detail || 'Failed to add favorite')
    }
    return response.json()
  },

  async removeFavorite(userId, courseCode) {
    const response = await fetch(`${BASE_URL}/api/favorites/${userId}/${courseCode}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to remove favorite')
    return response.json()
  },

  async checkFavorite(userId, courseCode) {
    const response = await fetch(`${BASE_URL}/api/favorites/${userId}/check/${courseCode}`, {
      headers: await authHeaders(),
    })
    if (!response.ok) return { is_favorited: false }
    return response.json()
  },
}

export default favoritesAPI
