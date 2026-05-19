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
 * Resolve which channels to use from notification prefs.
 *   method ∈ 'email' | 'sms' | 'both' | 'none'
 * Returns { notify_email, notify_sms, email, phone } honoring the user's choice.
 */
function _resolveChannels(notifPrefs, fallbackEmail) {
  const method = (notifPrefs?.method) || 'email'
  const email  = (notifPrefs?.email  || fallbackEmail || '').trim() || null
  const phone  = (notifPrefs?.phone  || '').trim() || null
  return {
    notify_email: (method === 'email' || method === 'both') && !!email,
    notify_sms:   (method === 'sms'   || method === 'both') && !!phone,
    email,
    phone,
  }
}

/**
 * Should we even schedule a notification for this event?
 * Honors:
 *   - method !== 'none'
 *   - per-event-type opt-out (eventTypes[event.type] !== false)
 *   - at least one channel actually has credentials (email or phone)
 */
function _shouldSchedule(event, notifPrefs, channels) {
  if (event.notifyEnabled === false) return false
  if ((notifPrefs?.method) === 'none') return false

  const type = event.type || 'personal'
  const typePref = notifPrefs?.eventTypes
  if (typePref && typePref[type] === false) return false

  return channels.notify_email || channels.notify_sms
}

/**
 * Save an event to Supabase and queue its notifications.
 * notifPrefs is the user's preferences from useNotificationPrefs().
 */
export async function scheduleNotification(event, userId, userEmail, notifPrefs = null) {
  const channels = _resolveChannels(notifPrefs, userEmail)
  const willSchedule = _shouldSchedule(event, notifPrefs, channels)

  const payload = {
    user_id:          userId,
    title:            event.title,
    date:             event.date,
    time:             event.time        || null,
    type:             event.type        || 'personal',
    category:         event.category    || null,
    description:      event.description || null,
    // notify_enabled gates whether the backend writes any rows into
    // notification_queue. Honor the user's preference here.
    notify_enabled:   willSchedule,
    notify_email:     channels.notify_email,
    notify_sms:       channels.notify_sms,
    notify_email_addr: channels.email,
    notify_phone:     channels.phone,
    notify_same_day:  event.notifySameDay ?? false,
    notify_1day:      event.notify1Day   ?? true,
    notify_7days:     event.notify7Days  ?? true,
    method:           (notifPrefs?.method) || 'email',
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

export async function queueExamNotification(event, userId, userEmail, notifPrefs = null) {
  const channels = _resolveChannels(notifPrefs, userEmail)
  // Caller (CalendarTab effect) already guards on method !== 'none' and the
  // 'exam' event-type opt-out, but double-check here so this is safe to call
  // standalone too.
  const willSchedule =
    (notifPrefs?.method) !== 'none'
    && notifPrefs?.eventTypes?.exam !== false
    && (channels.notify_email || channels.notify_sms)

  const payload = {
    client_id:        event.id,
    user_id:          userId,
    title:            event.title,
    date:             event.date,
    time:             to24h(event.time),
    type:             'exam',
    category:         event.category    || null,
    description:      event.description || null,
    notify_enabled:   willSchedule,
    notify_email:     channels.notify_email,
    notify_sms:       channels.notify_sms,
    notify_email_addr: channels.email,
    notify_phone:     channels.phone,
    notify_same_day:  event.notifySameDay ?? false,
    notify_1day:      event.notify1Day   ?? true,
    notify_7days:     event.notify7Days  ?? true,
  }

  const res = await fetch(`${BASE}/api/notifications/schedule`, {
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
  const res = await fetch(`${BASE}/api/notifications/events?user_id=${encodeURIComponent(userId)}`, {
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
  const res = await fetch(`${BASE}/api/notifications/${eventId}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json', ...(await _authHeader()) },
    body: JSON.stringify({ user_id: userId }),
  })
  if (!res.ok) throw new Error('Failed to delete event')
  return res.json()
}
