/**
 * useUpcomingEvents — lightweight "what's next" feed for the Home tab.
 *
 * Merges the user's calendar events (with weekly recurrences expanded)
 * and final exams for their current courses, then returns the next
 * `limit` upcoming entries sorted by date/time.
 *
 * Deliberately simpler than CalendarTab's pipeline (no club events,
 * newsletters, or historical exams) — Home only needs a glanceable
 * "Up Next" list. Cached via userDataCache for instant first paint.
 */
import { useState, useEffect, useCallback, useMemo } from 'react'
import { getEvents, expandRecurringEvents } from '../lib/calendarAPI'
import { lookupExams } from '../utils/examSchedule'
import { readCache, writeCache } from '../lib/userDataCache'

const CACHE_PREFIX = 'home_upcoming'
const URGENT_WINDOW_DAYS = 7
const SEEN_KEY_PREFIX = 'cal_urgent_seen'

// Which urgent events the sidebar badge has already been dismissed for.
// Per-device (localStorage), not per-item — an id here just means "counted
// at some point when the Calendar tab was opened", so it stays quiet even
// after re-fetches, but an id that later enters the urgent window for the
// first time (its date crosses into the 7-day cutoff) is still new and
// brings the badge back.
function readSeenIds(userId) {
  if (!userId) return new Set()
  try {
    const raw = localStorage.getItem(`${SEEN_KEY_PREFIX}_${userId}`)
    return raw ? new Set(JSON.parse(raw)) : new Set()
  } catch {
    return new Set()
  }
}

function writeSeenIds(userId, ids) {
  if (!userId) return
  try {
    localStorage.setItem(`${SEEN_KEY_PREFIX}_${userId}`, JSON.stringify([...ids]))
  } catch {
    // Private-browsing / storage-full — badge just won't persist across reloads.
  }
}

function todayIso() {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function buildFeed(userEvents, currentCourses) {
  const today = todayIso()

  const expanded = expandRecurringEvents(userEvents)
    .filter(ev => ev.date >= today)
    .map(ev => ({
      id: ev.id,
      title: ev.title,
      date: ev.date,
      time: ev.time || '',
      type: ev.type || 'personal',
      course_code: ev.course_code || '',
      location: ev.location || '',
    }))

  // Future final exams for current courses (student is presumably enrolled)
  const seen = new Set()
  const examEvents = []
  for (const course of currentCourses || []) {
    const code = course.course_code
    if (!code || seen.has(code)) continue
    seen.add(code)
    for (const exam of lookupExams(code)) {
      if (exam.date >= today) {
        examEvents.push({
          id: `exam-${code}-${exam.date}`,
          title: `${code} Final Exam`,
          date: exam.date,
          time: exam.start || '',
          type: 'exam',
          course_code: code,
          location: exam.campus || '',
        })
      }
    }
  }

  const all = [...expanded, ...examEvents].sort(
    (a, b) => a.date.localeCompare(b.date) || (a.time || '99').localeCompare(b.time || '99')
  )

  const urgentCutoff = new Date()
  urgentCutoff.setDate(urgentCutoff.getDate() + URGENT_WINDOW_DAYS)
  const cutoffIso = `${urgentCutoff.getFullYear()}-${String(urgentCutoff.getMonth() + 1).padStart(2, '0')}-${String(urgentCutoff.getDate()).padStart(2, '0')}`

  return {
    all,
    urgentIds: all.filter(ev => ev.date <= cutoffIso).map(ev => ev.id),
    // Setup-checklist signal: has the user imported a class schedule /
    // syllabus? (any calendar event tied to a course, past or future)
    hasCourseEvents: userEvents.some(ev => ev.course_code),
  }
}

export default function useUpcomingEvents(user, currentCourses, { limit = 5 } = {}) {
  const userId = user?.id

  const [feed, setFeed] = useState(() =>
    readCache(CACHE_PREFIX, userId, { all: [], urgentIds: [], hasCourseEvents: false })
  )
  const [loading, setLoading] = useState(() => feed.all.length === 0)
  const [seenIds, setSeenIds] = useState(() => readSeenIds(userId))

  useEffect(() => { setSeenIds(readSeenIds(userId)) }, [userId])

  useEffect(() => {
    if (!userId) return
    let cancelled = false
    getEvents(userId)
      .then(userEvents => {
        if (cancelled) return
        const next = buildFeed(userEvents, currentCourses)
        setFeed(next)
        writeCache(CACHE_PREFIX, userId, next)
      })
      .catch(() => {})
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
    // currentCourses is identified by length — Dashboard replaces the array
    // wholesale on import, and per-item edits don't affect exam lookup keys.
  }, [userId, currentCourses?.length]) // eslint-disable-line react-hooks/exhaustive-deps

  const urgentCount = useMemo(
    () => feed.urgentIds.filter(id => !seenIds.has(id)).length,
    [feed.urgentIds, seenIds]
  )

  // Dismisses the sidebar badge for every currently-urgent event. A new
  // event that enters the urgent window later (or a fresh id) still shows
  // up next time — this only quiets what's already been surfaced.
  const markUrgentSeen = useCallback(() => {
    if (!userId || feed.urgentIds.length === 0) return
    setSeenIds(prev => {
      const next = new Set(prev)
      let changed = false
      for (const id of feed.urgentIds) {
        if (!next.has(id)) { next.add(id); changed = true }
      }
      if (!changed) return prev
      writeSeenIds(userId, next)
      return next
    })
  }, [userId, feed.urgentIds])

  return {
    events: feed.all.slice(0, limit),
    urgentCount,
    hasCourseEvents: feed.hasCourseEvents,
    loading,
    markUrgentSeen,
  }
}
