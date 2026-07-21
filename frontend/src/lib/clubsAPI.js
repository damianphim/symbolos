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
  async getClubs({ search, category, limit = 50, offset = 0, lang } = {}) {
    try {
      const params = new URLSearchParams()
      if (search) params.set('search', search)
      if (category) params.set('category', category)
      if (limit) params.set('limit', String(limit))
      if (offset) params.set('offset', String(offset))
      if (lang) params.set('lang', lang)
      const res = await fetch(`${BASE_URL}/api/clubs?${params}`, { headers: await authHeaders() })
      if (!res.ok) throw new Error('Failed to fetch clubs')
      return await res.json()
    } catch (e) {
      console.error('getClubs error:', e)
      return { clubs: [], count: 0 }
    }
  },

  async getStarterClubs(userId, major, lang) {
    try {
      const params = new URLSearchParams({ user_id: userId })
      if (major) params.set('major', major)
      if (lang) params.set('lang', lang)
      const res = await fetch(`${BASE_URL}/api/clubs/starter?${params}`, { headers: await authHeaders() })
      if (res.ok) {
        const data = await res.json()
        if (data.starter_clubs && data.starter_clubs.length > 0) return data
      }
    } catch { /* ignore */ }
    return { starter_clubs: [] }
  },

  async getUserClubs(userId, lang) {
    try {
      const params = lang ? `?lang=${encodeURIComponent(lang)}` : ''
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}${params}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { clubs: [], count: 0 }
  },

  async getCreatedClubs(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/created/${userId}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
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
    } catch { /* ignore */ }
    return { success: true }
  },

  async getUserPendingRequests(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/pending-requests`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { pending_club_ids: [] }
  },

  async toggleCalendarSync(userId, clubId, synced) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/calendar/${clubId}?synced=${synced}`, { method: 'PATCH', headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
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
    } catch { /* ignore */ }
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
    } catch { /* ignore */ }
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
    } catch { /* ignore */ }
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
    } catch { /* ignore */ }
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

  // ── Club Subscriptions ─────────────────────────────────────────────────────
  async toggleSubscription(clubId) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/subscribe`, {
      method: 'POST', headers: await authHeaders(),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to toggle subscription') }
    return res.json()
  },

  async getUserSubscriptions(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/subscriptions`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { subscribed_club_ids: [] }
  },

  // ── Manager-invite requests ──────────────────────────────────────────────
  async createManagerRequest(clubId, email, message = null) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/manager-requests`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ email, message }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to send invite')
    }
    return res.json()
  },

  async getIncomingManagerRequests() {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/manager-requests/incoming`, {
        headers: await authHeaders(),
      })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { requests: [], count: 0 }
  },

  async respondToManagerRequest(requestId, action) {
    const res = await fetch(`${BASE_URL}/api/clubs/manager-requests/${requestId}/action`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ action }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to respond to invite')
    }
    return res.json()
  },

  // ── Activity feed + faculty stats (drawer enrichment) ─────────────────────
  async getClubActivity(clubId, { limit = 5 } = {}) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/activity?limit=${limit}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { items: [], count: 0 }
  },

  // AI-translated detail fields (description / meeting_schedule /
  // join_instructions) for a non-English viewer. Cached server-side, so this
  // is one Haiku call per club per language, ever. Returns {} on any failure
  // so the caller just falls back to the original (English) text.
  async getClubTranslation(clubId, lang) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/translation?lang=${encodeURIComponent(lang)}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return {}
  },

  async getClubFacultyStats(clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/faculty-stats`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { your_faculty: null, your_faculty_count: 0, by_faculty: [], total: 0 }
  },

  // ── Logo upload — direct to Supabase Storage, then PATCH the club row ─────
  async uploadClubLogo(clubId, file) {
    // Lazy-import the supabase client to avoid circular imports
    const { supabase } = await import('./supabase')
    if (!file) throw new Error('No file selected')
    if (!file.type?.startsWith('image/')) throw new Error('File must be an image')
    if (file.size > 2 * 1024 * 1024) throw new Error('Image must be under 2 MB')

    // Path: club-logos/{club_id}/logo.{ext} — overwrite previous logo
    const ext = (file.name.split('.').pop() || 'png').toLowerCase().replace(/[^a-z0-9]/g, '')
    const path = `${clubId}/logo.${ext || 'png'}`
    const { error: upErr } = await supabase.storage
      .from('club-logos')
      .upload(path, file, { upsert: true, contentType: file.type })
    if (upErr) throw new Error(upErr.message || 'Upload failed')

    const { data: urlData } = supabase.storage.from('club-logos').getPublicUrl(path)
    // Cache-bust so the new logo shows immediately
    const publicUrl = `${urlData.publicUrl}?v=${Date.now()}`

    // Persist the URL on the club row via the existing PUT endpoint
    await this.editClub(clubId, { logo_url: publicUrl })
    return { logo_url: publicUrl }
  },

  // ── Club Managers ──────────────────────────────────────────────────────────
  async getClubManagers(clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/managers`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch { /* ignore */ }
    return { managers: [], count: 0 }
  },

  async removeClubManager(clubId, managerUserId) {
    const res = await fetch(`${BASE_URL}/api/clubs/${clubId}/managers/${managerUserId}`, {
      method: 'DELETE', headers: await authHeaders(),
    })
    if (!res.ok) { const err = await res.json().catch(() => ({})); throw new Error(err.detail || 'Failed to remove manager') }
    return res.json()
  },

}

export default clubsAPI
