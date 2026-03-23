// frontend/src/lib/clubsAPI.js
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const normalizeUrl = (url) => {
  let n = url.replace(/\/$/, '')
  if (n.endsWith('/api')) n = n.slice(0, -4)
  return n
}
const BASE_URL = normalizeUrl(API_URL)

import { supabase } from './supabase'

async function authHeaders(json = true) {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  const h = { Authorization: `Bearer ${token}` }
  if (json) h['Content-Type'] = 'application/json'
  return h
}


const clubsAPI = {
  async getClubs({ search, category, limit = 50, offset = 0 } = {}) {
    try {
      const params = new URLSearchParams()
      if (search) params.set('search', search)
      if (category) params.set('category', category)
      if (limit) params.set('limit', String(limit))
      const res = await fetch(`${BASE_URL}/api/clubs?${params}`, { headers: await authHeaders() })
      if (!res.ok) throw new Error('Failed to fetch clubs')
      return await res.json()
    } catch (e) {
      console.error('getClubs error:', e)
      return { clubs: [], count: 0 }
    }
  },

  async getStarterClubs(userId, major) {
    try {
      const params = new URLSearchParams({ user_id: userId })
      if (major) params.set('major', major)
      const res = await fetch(`${BASE_URL}/api/clubs/starter?${params}`, { headers: await authHeaders() })
      if (res.ok) {
        const data = await res.json()
        if (data.starter_clubs && data.starter_clubs.length > 0) return data
      }
    } catch (_) {}
    return { starter_clubs: [] }
  },

  async getUserClubs(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { clubs: [], count: 0 }
  },

  async getCreatedClubs(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/created/${userId}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { clubs: [], count: 0 }
  },

  async joinClub(userId, clubId, { requester_name, requester_email, requester_linkedin } = {}) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/join`, {
        method: 'POST',
        headers: await authHeaders(),
        body: JSON.stringify({ club_id: clubId, requester_name, requester_email, requester_linkedin }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || 'Failed to join club')
      }
      return res.json()
    } catch (e) {
      if (e.message && (e.message.includes('Failed to join') || e.message.includes('Already') || e.message.includes('pending'))) throw e
      return { success: true }
    }
  },

  async leaveClub(userId, clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/leave/${clubId}`, { method: 'DELETE', headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { success: true }
  },

  async getUserPendingRequests(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/pending-requests`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { pending_club_ids: [] }
  },

  async toggleCalendarSync(userId, clubId, synced) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/calendar/${clubId}?synced=${synced}`, { method: 'PATCH', headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { success: true, calendar_synced: synced }
  },

  async submitClub(data) {
    const res = await fetch(`${BASE_URL}/api/clubs/submit`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to submit club')
    }
    return res.json()
  },

  async editClub(clubId, data) {
    const res = await fetch(`${BASE_URL}/api/clubs/edit/${clubId}`, {
      method: 'PUT',
      headers: await authHeaders(),
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to update club')
    }
    return res.json()
  },

  async getJoinRequests(clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/join-requests/${clubId}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { requests: [], count: 0 }
  },

  async handleJoinRequest(requestId, action) {
    const res = await fetch(`${BASE_URL}/api/clubs/join-requests/${requestId}/action`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ action }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to process request')
    }
    return res.json()
  },

  async deleteClub(clubId) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to delete club')
    }
    return res.json()
  },

  // ── Club Members ────────────────────────────────────────────────────────
  async getClubMembers(clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/members`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { members: [], count: 0 }
  },

  async removeClubMember(clubId, memberUserId) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/members/${memberUserId}`, {
      method: 'DELETE', headers: await authHeaders(),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to remove member') }
    return res.json()
  },

  async updateMemberRole(clubId, memberUserId, role) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/members/${memberUserId}/role`, {
      method: 'PATCH', headers: await authHeaders(),
      body: JSON.stringify({ role }),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to update role') }
    return res.json()
  },

  // ── Club Events ──────────────────────────────────────────────────────────
  async getSubscribedClubEvents() {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/events/subscribed`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { events: [] }
  },

  async createClubEvent(clubId, data) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/events`, {
      method: 'POST', headers: await authHeaders(), body: JSON.stringify(data),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to create event') }
    return res.json()
  },

  async deleteClubEvent(clubId, eventId) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/events/${eventId}`, {
      method: 'DELETE', headers: await authHeaders(),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to delete event') }
    return res.json()
  },

  // ── Club Announcements ──────────────────────────────────────────────────
  async getSubscribedClubAnnouncements() {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/announcements/subscribed`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { announcements: [] }
  },

  async createClubAnnouncement(clubId, data) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/announcements`, {
      method: 'POST', headers: await authHeaders(), body: JSON.stringify(data),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to create announcement') }
    return res.json()
  },

  async deleteClubAnnouncement(clubId, annId) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/announcements/${annId}`, {
      method: 'DELETE', headers: await authHeaders(),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to delete announcement') }
    return res.json()
  },

  async getCategories() {
    return {
      categories: [
        'Academic', 'Arts & Culture', 'Athletics & Recreation',
        'Community Service', 'Debate & Politics', 'Engineering & Technology',
        'Environment', 'Health & Wellness', 'International', 'Professional',
        'Science', 'Social', 'Spiritual & Religious',
      ]
    }
  },

}

export default clubsAPI
