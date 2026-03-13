import { BASE_URL } from './apiConfig'
import { supabase } from './supabase'

async function authHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
}

export const CARD_CATEGORIES = [
  'deadlines', 'degree', 'courses', 'grades', 'planning', 'opportunities', 'other',
]

export const CATEGORY_LABELS = {
  deadlines: 'Deadlines', degree: 'Degree', courses: 'Courses',
  grades: 'Grades', planning: 'Planning', opportunities: 'Opportunities', other: 'Other',
}

export const CATEGORY_ICONS = {
  deadlines: '📅', degree: '🎓', courses: '📚',
  grades: '📊', planning: '🗺️', opportunities: '✨', other: '💬',
}

// FIX: getLang is now only a fallback. All public methods accept an explicit
// `language` parameter so the caller (Dashboard) can pass the React context
// value directly, avoiding any race with localStorage writes.
function getLang() {
  const stored = localStorage.getItem('language')
  return ['en', 'fr', 'zh'].includes(stored) ? stored : 'en'
}

const cardsAPI = {
  async getCards(userId) {
    const response = await fetch(`${BASE_URL}/api/cards/${userId}`, {
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to fetch advisor cards')
    return response.json()
  },

  async generateCards(userId, force = false, language = null) {
    const response = await fetch(`${BASE_URL}/api/cards/generate/${userId}`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ force, language: language || getLang() }),
    })
    if (!response.ok) throw new Error('Failed to generate advisor cards')
    return response.json()
  },

  async retranslateCards(userId, language = null) {
    const response = await fetch(`${BASE_URL}/api/cards/retranslate/${userId}`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ language: language || getLang() }),
    })
    if (!response.ok) throw new Error('Failed to retranslate cards')
    return response.json()
  },

  async askCard(userId, question, language = null) {
    const response = await fetch(`${BASE_URL}/api/cards/ask/${userId}`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ user_id: userId, question, language: language || getLang() }),
    })
    if (!response.ok) throw new Error('Failed to generate card from question')
    return response.json()
  },

  async sendThreadMessage(cardId, userId, message, cardContext, language = null) {
    const response = await fetch(`${BASE_URL}/api/cards/${cardId}/thread`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ user_id: userId, message, card_context: cardContext, language: language || getLang() }),
    })
    if (!response.ok) throw new Error('Failed to send thread message')
    const data = await response.json()
    return data.response
  },

  async clearCards(userId) {
    const response = await fetch(`${BASE_URL}/api/cards/${userId}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to clear advisor cards')
  },

  async saveCard(cardId, isSaved) {
    const response = await fetch(`${BASE_URL}/api/cards/${cardId}/save`, {
      method: 'PATCH',
      headers: await authHeaders(),
      body: JSON.stringify({ is_saved: isSaved }),
    })
    if (!response.ok) throw new Error('Failed to update card saved state')
    return response.json()
  },

  async reorderCards(userId, order) {
    const response = await fetch(`${BASE_URL}/api/cards/${userId}/reorder`, {
      method: 'PATCH',
      headers: await authHeaders(),
      body: JSON.stringify({ order }),
    })
    if (!response.ok) throw new Error('Failed to reorder cards')
    return response.json()
  },
}

export default cardsAPI
