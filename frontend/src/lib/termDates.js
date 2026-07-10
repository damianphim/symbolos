// McGill term windows, per https://www.mcgill.ca/importantdates/key-dates
// (e.g. Fall 2026: classes Aug 31 – Dec 4, exams end Dec 22;
//  Winter 2027: classes Jan 5 – Apr 14, exams end Apr 30).
// Boundaries below are slightly padded so they hold year-over-year without
// needing an annual data update:
//   Fall:   Aug 25 – Dec 31
//   Winter: Jan 1  – Apr 30
//   Summer: May 1  – Aug 24

/** Returns { term: 'Fall'|'Winter'|'Summer', year } for a given date (default: today). */
export function getActiveTerm(date = new Date()) {
  const m = date.getMonth() + 1 // 1-12
  const d = date.getDate()
  const y = date.getFullYear()
  if (m <= 4) return { term: 'Winter', year: y }
  if (m < 8 || (m === 8 && d < 25)) return { term: 'Summer', year: y }
  return { term: 'Fall', year: y }
}

/**
 * True when a course row belongs to the active term.
 * Rows without term/year (legacy data) count as active so nothing the user
 * added before the migration silently disappears.
 */
export function isCourseInActiveTerm(course, date = new Date()) {
  if (!course?.term || !course?.year) return true
  const active = getActiveTerm(date)
  return course.term === active.term && Number(course.year) === active.year
}

/** Sort key: terms in chronological order within an academic year. */
const TERM_ORDER = { Winter: 0, Summer: 1, Fall: 2 }

/**
 * Groups course rows by "<Term> <Year>" (legacy rows under 'Term not set'),
 * ordered chronologically, with the active term first when present.
 * Returns [{ key, term, year, isActive, courses }].
 */
export function groupCoursesByTerm(courses, date = new Date()) {
  const active = getActiveTerm(date)
  const groups = new Map()
  for (const c of courses || []) {
    const hasTerm = c?.term && c?.year
    const key = hasTerm ? `${c.term} ${c.year}` : 'Term not set'
    if (!groups.has(key)) {
      groups.set(key, {
        key,
        term: hasTerm ? c.term : null,
        year: hasTerm ? Number(c.year) : null,
        isActive: hasTerm
          ? c.term === active.term && Number(c.year) === active.year
          : true, // legacy rows are treated as active
        courses: [],
      })
    }
    groups.get(key).courses.push(c)
  }
  return [...groups.values()].sort((a, b) => {
    if (a.isActive !== b.isActive) return a.isActive ? -1 : 1
    if (a.year !== b.year) return (a.year ?? 0) - (b.year ?? 0)
    return (TERM_ORDER[a.term] ?? 3) - (TERM_ORDER[b.term] ?? 3)
  })
}
