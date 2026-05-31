/**
 * examSchedule.js — multi-term final-exam schedule registry.
 *
 * To add a new term:
 *   1. Drop in a new file, e.g. `examSchedule_dec2026.js`, exporting an
 *      array shaped like APRIL_2026_EXAMS.
 *   2. Import it here and add an entry to TERMS below with a label.
 * That's it — no other code needs to change. Historical schedules stay
 * forever so past exams remain in users' calendar history.
 */
import { APRIL_2026_EXAMS } from './examSchedule2026'

// ── Term registry ──────────────────────────────────────────────────
// term:  one of 'Winter' | 'Summer' | 'Fall' (must match the value stored
//        in completed_courses.term so we can match a user's course to the
//        correct term's exam).
// year:  4-digit calendar year the exams happen in.
// label: human-readable string the calendar uses as the event category.
// exams: the array of exam entries (one per course-section).
const TERMS = [
  { term: 'Winter', year: 2026, label: 'Winter 2026 Finals', exams: APRIL_2026_EXAMS },
  // Add future terms here, e.g.:
  // { term: 'Fall',   year: 2026, label: 'Fall 2026 Finals',   exams: DEC_2026_EXAMS },
]

// Build a multimap: normalized course code → list of exam entries
// Each entry carries its term + year + termLabel so the caller can filter
// to only the matches that apply to a given course.
const _multimap = (() => {
  const m = new Map()
  for (const { term, year, label, exams } of TERMS) {
    for (const exam of exams) {
      const key = exam.code.trim().toUpperCase()
      if (!m.has(key)) m.set(key, [])
      m.get(key).push({ ...exam, term, year, termLabel: label })
    }
  }
  return m
})()

// Normalize a course code string for lookup
function _normalize(courseCode) {
  if (!courseCode) return null
  let norm = courseCode.trim().toUpperCase().replace(/\s+/g, ' ')
  norm = norm.replace(/^([A-Z]{2,4})(\d)/, '$1 $2')
  return norm
}

// Variants we try when normalizing didn't match directly
function _variants(norm) {
  const out = [norm]
  const withoutD = norm.replace(/\s?D\d$/, '').trim()
  if (withoutD !== norm) out.push(withoutD)
  const withoutSection = norm.replace(/\s+\d{3}$/, '').trim()
  if (withoutSection !== norm) out.push(withoutSection)
  const withoutBoth = withoutD.replace(/\s?D\d$/, '').replace(/\s+\d{3}$/, '').trim()
  if (withoutBoth !== norm) out.push(withoutBoth)
  return out
}

/**
 * Return ALL matching exam entries for a course code across every term.
 * Used by the calendar to generate one event per (course, exam) so a
 * student who took COMP 251 in two different years sees both exams in
 * their permanent calendar history.
 */
export function lookupExams(courseCode) {
  const norm = _normalize(courseCode)
  if (!norm) return []
  for (const variant of _variants(norm)) {
    if (_multimap.has(variant)) return _multimap.get(variant)
  }
  return []
}

/**
 * Return ONE exam entry for a course code:
 *   - the soonest future exam, if any exist
 *   - otherwise the most recent past exam
 * Use when the caller only wants a single "best" match.
 */
export function lookupExam(courseCode) {
  const all = lookupExams(courseCode)
  if (all.length === 0) return null

  const today = new Date().toISOString().split('T')[0]
  const future = all.filter(e => e.date >= today).sort((a, b) => a.date.localeCompare(b.date))
  if (future.length > 0) return future[0]

  const past = [...all].sort((a, b) => b.date.localeCompare(a.date))
  return past[0]
}

/** Format start time as 12-hour clock e.g. "2:00 PM" */
export function formatExamTime(time24) {
  if (!time24) return ''
  const [h, m] = time24.split(':').map(Number)
  const ampm = h >= 12 ? 'PM' : 'AM'
  const hour = h % 12 || 12
  return `${hour}:${String(m).padStart(2, '0')} ${ampm}`
}
