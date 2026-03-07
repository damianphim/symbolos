/**
 * frontend/src/lib/calendarAPI.js
 *
 * Supabase-backed calendar event persistence.
 * Also exports expandRecurringEvents() to inflate weekly recurrences
 * from the stored anchor row into full-term occurrences.
 */

import { supabase } from './supabase'

const TABLE = 'calendar_events'

// ── Term boundary constants ────────────────────────────────────────────────────
// Classes-end dates (not exam-period end).  Recurring lecture slots stop here.
const TERM_ENDS = {
  fall_2025:   '2025-12-03',
  winter_2026: '2026-04-14',
  summer_2025: '2025-08-14',
  summer_2026: '2026-08-13',
}

// No-class holidays that should be skipped when generating occurrences.
const NO_CLASS_DATES = new Set([
  // Fall 2025
  '2025-09-01', // Labour Day
  '2025-10-13', // Thanksgiving
  '2025-10-14', '2025-10-15', '2025-10-16', '2025-10-17', // Fall Reading Break
  // Winter 2026
  '2026-03-02', '2026-03-03', '2026-03-04', '2026-03-05', '2026-03-06', // Winter Reading Break
  '2026-04-03', // Good Friday
  '2026-04-06', // Easter Monday
])

// Day-name → JS getDay() index
const DAY_INDEX = {
  sunday: 0, monday: 1, tuesday: 2, wednesday: 3,
  thursday: 4, friday: 5, saturday: 6,
}

// ── Column mapping ─────────────────────────────────────────────────────────────

function toDb(event, userId) {
  const row = {
    user_id:         userId,
    title:           event.title,
    date:            event.date,
    time:            event.time    || null,
    end_time:        event.end_time  || null,
    type:            event.type    || 'personal',
    category:        event.category || null,
    description:     event.description || null,
    location:        event.location   || null,
    course_code:     event.course_code || null,
    recurrence:      event.recurrence  || null,
    notify_enabled:  event.notifyEnabled  ?? false,
    notify_same_day: event.notifySameDay  ?? false,
    notify_1day:     event.notify1Day     ?? false,
    notify_7days:    event.notify7Days    ?? false,
  }
  // Only include id if it's already a real UUID (existing row).
  // New events get id like "user-1234567890" which is not a valid UUID —
  // omitting it lets Supabase generate one, avoiding a type-mismatch failure.
  if (event.id && !event.id.startsWith('user-')) {
    row.id = event.id
  }
  return row
}

function fromDb(row) {
  return {
    id:            row.id,
    title:         row.title,
    date:          row.date,
    time:          row.time     || '',
    end_time:      row.end_time || '',
    type:          row.type,
    category:      row.category    || '',
    description:   row.description || '',
    location:      row.location    || '',
    course_code:   row.course_code || '',
    recurrence:    row.recurrence  || null,
    notifyEnabled: row.notify_enabled,
    notifySameDay: row.notify_same_day,
    notify1Day:    row.notify_1day,
    notify7Days:   row.notify_7days,
  }
}

// ── Recurring event expansion ──────────────────────────────────────────────────

/**
 * Given an array of raw calendar events (already fromDb-mapped),
 * expand any weekly recurring events across their term.
 *
 * For each event with recurrence like "weekly_tuesday":
 *   - start from the stored anchor date
 *   - generate one occurrence every 7 days
 *   - stop at the term-end date for the event's term (derived from category)
 *   - skip no-class holidays
 *   - give each occurrence a stable synthetic ID: `{id}_occ_{YYYY-MM-DD}`
 *
 * Non-recurring events are returned unchanged.
 *
 * @param {Object[]} events — fromDb-mapped event objects
 * @returns {Object[]} flat array with recurring events fully expanded
 */
export function expandRecurringEvents(events) {
  const result = []

  for (const ev of events) {
    if (!ev.recurrence || !ev.recurrence.startsWith('weekly_')) {
      result.push(ev)
      continue
    }

    // Determine which day-of-week this recurs on
    const dayName = ev.recurrence.replace('weekly_', '') // e.g. "tuesday"
    const targetDow = DAY_INDEX[dayName]
    if (targetDow === undefined) {
      result.push(ev)
      continue
    }

    // Pick term end based on category (course_code stored in category column)
    // and anchor date
    const anchor = new Date(ev.date + 'T00:00:00')
    const termEnd = _guessTermEnd(ev.date)
    if (!termEnd) {
      result.push(ev)
      continue
    }
    const endDate = new Date(termEnd + 'T00:00:00')

    // Generate occurrences
    let cur = new Date(anchor)
    // Ensure we start on the correct day of week
    while (cur.getDay() !== targetDow) {
      cur.setDate(cur.getDate() + 1)
    }

    while (cur <= endDate) {
      const dateStr = _toIso(cur)
      if (!NO_CLASS_DATES.has(dateStr)) {
        const isAnchor = dateStr === ev.date
        result.push({
          ...ev,
          id:   isAnchor ? ev.id : `${ev.id}_occ_${dateStr}`,
          date: dateStr,
          // Mark non-anchor occurrences so they can't be individually edited/deleted
          _isRecurringOccurrence: !isAnchor,
          _anchorId: ev.id,
        })
      }
      cur.setDate(cur.getDate() + 7)
    }
  }

  return result
}

function _toIso(d) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function _guessTermEnd(anchorDate) {
  if (!anchorDate) return null
  const [year, month] = anchorDate.split('-').map(Number)
  // Fall: Aug–Dec
  if (year === 2025 && month >= 8) return TERM_ENDS.fall_2025
  // Winter: Jan–Apr
  if (year === 2026 && month >= 1 && month <= 4) return TERM_ENDS.winter_2026
  // Summer 2025
  if (year === 2025 && month >= 5 && month <= 8) return TERM_ENDS.summer_2025
  // Summer 2026
  if (year === 2026 && month >= 5) return TERM_ENDS.summer_2026
  return null
}

// ── CRUD ───────────────────────────────────────────────────────────────────────

/**
 * Fetch all stored events for a user (anchor rows only — no expansion yet).
 * Caller should pass through expandRecurringEvents() for display.
 */
export async function getEvents(userId) {
  const { data, error } = await supabase
    .from(TABLE)
    .select('*')
    .eq('user_id', userId)
    .order('date', { ascending: true })

  if (error) throw error
  return (data || []).map(fromDb)
}

/**
 * Upsert a single event. Returns the saved event object.
 */
export async function saveEvent(event, userId) {
  const row = toDb(event, userId)

  const { data, error } = await supabase
    .from(TABLE)
    .upsert(row, { onConflict: 'id' })
    .select()
    .single()

  if (error) throw error
  return fromDb(data)
}

/**
 * Delete a single event by ID.
 */
export async function deleteEvent(eventId, userId) {
  const { error } = await supabase
    .from(TABLE)
    .delete()
    .eq('id', eventId)
    .eq('user_id', userId)

  if (error) throw error
}

/**
 * Migrate existing localStorage events into Supabase.
 * Call once after login. Idempotent.
 */
export async function migrateLocalStorageEvents(userId) {
  const LS_KEY = 'mcgill_calendar_events'
  let localEvents = []
  try {
    localEvents = JSON.parse(localStorage.getItem(LS_KEY) || '[]')
  } catch {
    return
  }

  if (localEvents.length === 0) return

  const rows = localEvents.map(e => toDb(e, userId))

  const { error } = await supabase
    .from(TABLE)
    .upsert(rows, { onConflict: 'id' })

  if (error) {
    console.error('Failed to migrate localStorage events:', error)
    return
  }

  localStorage.removeItem(LS_KEY)
  console.info(`Migrated ${localEvents.length} calendar events from localStorage to Supabase`)
}
