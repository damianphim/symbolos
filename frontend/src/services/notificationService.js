/**
 * notificationService.js
 * Talks to /api/notifications/* on the backend.
 * All mutating/private endpoints now send the Supabase JWT for auth.
 */

import { supabase } from '../lib/supabase'

const BASE = (import.meta.env.VITE_API_URL || (
  import.meta.env.PROD
    ? (() => { throw new Error('VITE_API_URL must be set in production') })()
    : 'http://localhost:8000'
)).replace(/\/api\/?$/, '')

/** Get the current user's Bearer token from Supabase session. */
async function _authHeader() {
  const { data } = await supabase.auth.getSession()
  const token = data?.session?.access_token
  if (!token) throw new Error('Not authenticated')
  return { Authorization: `Bearer ${token}` }
}

/**
 * Save an event to Supabase and queue its notifications.
 */
export async function scheduleNotification(event, userId, userEmail) {
  const payload = {
    user_id:          userId,
    title:            event.title,
    date:             event.date,
    time:             event.time        || null,
    type:             event.type        || 'personal',
    category:         event.category    || null,
    description:      event.description || null,
    notify_enabled:   event.notifyEnabled ?? true,
    notify_email:     true,
    notify_sms:       false,
    notify_email_addr: userEmail,
    notify_phone:     null,
    notify_same_day:  event.notifySameDay ?? false,
    notify_1day:      event.notify1Day   ?? true,
    notify_7days:     event.notify7Days  ?? true,
    method:           'email',
  }

  const res = await fetch(`${BASE}/api/notifications/schedule`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(await _authHeader()) },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Failed to schedule notification')
  }

  return res.json()
}

/**
 * Idempotently queue notifications for a read-only exam event.
 * Does NOT create a calendar_events row — safe to call on every load.
 */
function to24h(timeStr) {
  if (!timeStr) return null
  // Already HH:MM 24h format
  if (/^\d{2}:\d{2}$/.test(timeStr)) return timeStr
  // Parse "2:00 PM", "12:30 AM", etc.
  const m = timeStr.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i)
  if (!m) return null
  let h = parseInt(m[1], 10)
  const min = m[2]
  const period = m[3].toUpperCase()
  if (period === 'PM' && h !== 12) h += 12
  if (period === 'AM' && h === 12) h = 0
  return `${String(h).padStart(2, '0')}:${min}`
}

export async function queueExamNotification(event, userId, userEmail) {
  const payload = {
    client_id:        event.id,           // e.g. "exam-COMP251-0" — used for dedup
    user_id:          userId,
    title:            event.title,
    date:             event.date,
    time:             to24h(event.time),
    type:             'exam',
    category:         event.category    || null,
    description:      event.description || null,
    notify_enabled:   true,
    notify_email:     true,
    notify_sms:       false,
    notify_email_addr: userEmail,
    notify_phone:     null,
    notify_same_day:  event.notifySameDay ?? false,
    notify_1day:      event.notify1Day   ?? true,
    notify_7days:     event.notify7Days  ?? true,
  }

  const res = await fetch(`${BASE}/api/notifications/queue-exam`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(await _authHeader()) },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || 'Failed to queue exam notification')
  }

  return res.json()
}

/**
 * Fetch all calendar events for a user from Supabase.
 */
export async function getUserEvents(userId) {
  const res = await fetch(`${BASE}/api/notifications/events/${userId}`, {
    headers: await _authHeader(),
  })
  if (!res.ok) throw new Error('Failed to fetch events')
  const data = await res.json()
  return data.events || []
}

/**
 * Delete an event (cascade removes its notification_queue rows).
 */
export async function deleteEvent(eventId, userId) {
  const res = await fetch(`${BASE}/api/notifications/events/${eventId}?user_id=${userId}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json', ...(await _authHeader()) },
  })
  if (!res.ok) throw new Error('Failed to delete event')
  return res.json()
}
