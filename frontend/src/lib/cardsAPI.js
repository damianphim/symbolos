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

  /**
   * Streaming card generation via SSE.
   * Calls onCard(card, index) for each card as it arrives.
   * Calls onDone({ count, language, fresh?, rate_limited? }) when complete.
   * Calls onError(detail) on failure.
   */
  async generateCardsStream(userId, force = false, language = null, { onCard, onDone, onError } = {}) {
    const response = await fetch(`${BASE_URL}/api/cards/stream/${userId}`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ force, language: language || getLang() }),
    })
    if (!response.ok) {
      onError?.('Failed to start card generation')
      return
    }

    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let buffer = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() // keep incomplete last line
        for (const line of lines) {
          if (!line.startsWith('data: ')) continue
          try {
            const event = JSON.parse(line.slice(6))
            if (event.type === 'card') {
              onCard?.(event.card, event.index)
              // Give the browser a full frame to paint the new card before the next one
              await new Promise(r => requestAnimationFrame(r))
            } else if (event.type === 'done') {
              onDone?.(event)
            } else if (event.type === 'error') {
              onError?.(event.detail)
            }
          } catch { /* ignore malformed SSE lines */ }
        }
      }
    } finally {
      reader.releaseLock()
    }
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

  async deleteCard(userId, cardId) {
    const response = await fetch(`${BASE_URL}/api/cards/${userId}/${cardId}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!response.ok) throw new Error('Failed to delete card')
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
