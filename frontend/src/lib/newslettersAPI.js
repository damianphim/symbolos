/**
 * frontend/src/lib/newslettersAPI.js
 *
 * API client for newsletter sources, subscriptions, and events.
 */
import { BASE_URL } from './apiConfig'
import { supabase } from './supabase'

async function authHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
}

const newslettersAPI = {
  // ── Sources ───────────────────────────────────────────────────────────────

  async getSources({ category, search } = {}) {
    try {
      const params = new URLSearchParams()
      if (category) params.set('category', category)
      if (search) params.set('search', search)
      const res = await fetch(`${BASE_URL}/api/newsletters/sources?${params}`, {
        headers: await authHeaders(),
      })
      if (res.ok) return res.json()
    } catch (_) {}
    return []
  },

  async getCategories() {
    try {
      const res = await fetch(`${BASE_URL}/api/newsletters/sources/categories`, {
        headers: await authHeaders(),
      })
      if (res.ok) {
        const data = await res.json()
        return data.categories || []
      }
    } catch (_) {}
    return []
  },

  // ── Subscriptions ─────────────────────────────────────────────────────────

  async getSubscriptions() {
    try {
      const res = await fetch(`${BASE_URL}/api/newsletters/subscriptions`, {
        headers: await authHeaders(),
      })
      if (res.ok) {
        const data = await res.json()
        return data.subscriptions || []
      }
    } catch (_) {}
    return []
  },

  async subscribe(sourceId, calendarSync = true) {
    const res = await fetch(`${BASE_URL}/api/newsletters/subscriptions`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ source_id: sourceId, calendar_sync: calendarSync }),
    })
    if (!res.ok) throw new Error('Failed to subscribe')
    return res.json()
  },

  async updateSubscription(sourceId, updates = {}) {
    const body = {}
    if (updates.calendarSync !== undefined) body.calendar_sync = updates.calendarSync
    if (updates.emailMuted !== undefined) body.email_muted = updates.emailMuted
    const res = await fetch(`${BASE_URL}/api/newsletters/subscriptions/${sourceId}`, {
      method: 'PATCH',
      headers: await authHeaders(),
      body: JSON.stringify(body),
    })
    if (!res.ok) throw new Error('Failed to update subscription')
    return res.json()
  },

  async unsubscribe(sourceId) {
    const res = await fetch(`${BASE_URL}/api/newsletters/subscriptions/${sourceId}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to unsubscribe')
    return res.json()
  },

  // ── Events (calendar-synced newsletter events) ────────────────────────────

  async getEvents() {
    try {
      const res = await fetch(`${BASE_URL}/api/newsletters/events`, {
        headers: await authHeaders(),
      })
      if (res.ok) {
        const data = await res.json()
        return data.events || []
      }
    } catch (_) {}
    return []
  },
}

export default newslettersAPI
