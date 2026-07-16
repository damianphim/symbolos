/**
 * requirementMatch.js — shared course ↔ requirement matching.
 *
 * The bug this fixes: some degree-requirement blocks store a single
 * "wildcard placeholder" course instead of listing every eligible course.
 * e.g. the Anthropology Minor's "200-level ANTH Courses" block contains one
 * row: { subject:"ANTH", catalog:"200", title:"Any 200-level Anthropology
 * course" }. A student who took ANTH 209 got no credit because the old
 * matcher did an exact `"ANTH 209" === "ANTH 200"` comparison.
 *
 * wildcardBand() detects these placeholders from their title (and round-
 * hundred catalog) and returns the subject + catalog range they stand for,
 * so any course in that band matches. Applies to every program, so a
 * wildcard block in any faculty's requirements now resolves correctly.
 *
 * Patterns handled:
 *   "Any 200-level Anthropology course"      → ANTH 200–299
 *   "Any 300-level X course"                 → X   300–399
 *   "Any upper-level GERM course (300+)"     → GERM 300+
 *   "Any upper-level LING course"            → LING 300+
 *   round-hundred placeholder catalog (200)  → subject 200–299
 */

/** If `req` is a wildcard placeholder, return {subject, min, max}; else null. */
export function wildcardBand(req) {
  if (!req) return null
  const title = (req.title || '').toLowerCase()
  const looksWild = /\bany\b/.test(title) && /level/.test(title)
  if (!looksWild) return null

  const subject = (req.subject || '').toUpperCase()
  if (!subject) return null

  // "300+" / "(300+)" → open-ended from that level.
  let m = title.match(/(\d{3})\s*\+/)
  if (m) return { subject, min: parseInt(m[1], 10), max: Infinity }

  // "NNN-level" → that single hundred band.
  m = title.match(/(\d{3})\s*-?\s*level/)
  if (m) {
    const lvl = parseInt(m[1], 10)
    return { subject, min: lvl, max: lvl + 99 }
  }

  // "upper-level" with no explicit number → conventionally 300+.
  if (/upper[\s-]*level/.test(title)) return { subject, min: 300, max: Infinity }

  // Fallback: a round-hundred placeholder catalog (e.g. "200").
  const cat = parseInt(req.catalog, 10)
  if (!Number.isNaN(cat) && cat % 100 === 0) {
    return { subject, min: cat, max: cat + 99 }
  }
  return null
}

function keyOf(c) {
  return `${c?.subject || ''} ${c?.catalog || ''}`.toUpperCase()
}

/**
 * Every course code that appears as a real (non-wildcard) requirement row
 * anywhere in a program's blocks. Pass this as `excludeKeys` to matchCourse /
 * blockWildcardMatches to stop a wildcard/complementary block (e.g. "any
 * COMP 300+ course") from double-counting a course that already satisfies a
 * more specific requirement elsewhere in the SAME program (e.g. a Group D
 * requirement naming that exact course) — one course can't count toward two
 * different requirement categories at once.
 */
export function explicitlyClaimedCourseKeys(blocks = []) {
  const claimed = new Set()
  for (const block of blocks || []) {
    for (const c of block?.courses || []) {
      if (!c?.catalog || wildcardBand(c)) continue
      claimed.add(keyOf(c))
    }
  }
  return claimed
}

/**
 * Find the user course that satisfies requirement `req`, or null.
 * Handles both exact codes and wildcard-band placeholders.
 *
 * `excludeKeys` (optional): a Set of course keys to skip when resolving a
 * *wildcard* match — see explicitlyClaimedCourseKeys(). Exact-code matches
 * are never excluded, since a row explicitly naming a course is always
 * allowed to claim it.
 */
export function matchCourse(req, userCourses = [], excludeKeys = null) {
  const band = wildcardBand(req)
  if (band) {
    return userCourses.find(c => {
      if (excludeKeys && excludeKeys.has(keyOf(c))) return false
      if ((c.subject || '').toUpperCase() !== band.subject) return false
      const cat = parseInt(c.catalog, 10)
      return !Number.isNaN(cat) && cat >= band.min && cat <= band.max
    }) || null
  }

  if (!req.catalog) return null
  const key = `${req.subject} ${req.catalog}`.toUpperCase()
  return userCourses.find(c =>
    `${c.subject || ''} ${c.catalog || ''}`.toUpperCase() === key
  ) || null
}

/**
 * Return the user courses that satisfy a block's *wildcard* portion —
 * placeholder courses ("Any 200-level X course"), null-catalog entries, or
 * a block-level min_level. Does NOT apply any credit cap or de-dup against
 * exact matches; callers handle that bookkeeping (seen sets, overlap
 * allocation, per-block credit limits) themselves.
 *
 * `excludeKeys` (optional): a Set of course keys to never return — pass
 * explicitlyClaimedCourseKeys(programBlocks) so this block's wildcard slot
 * can't double-count a course a different block already claims by name.
 *
 * Used by all three progress computations (the program ring, the per-program
 * progress bar, and per-block credit counting) so they can't drift apart.
 */
export function blockWildcardMatches(block, userCourses = [], excludeKeys = null) {
  const bands = (block?.courses || []).map(c => wildcardBand(c)).filter(Boolean)
  const minLevel = block?.min_level || 0
  const legacyApplies = (block?.courses || []).some(c => !c.catalog) || minLevel > 0
  if (!legacyApplies && bands.length === 0) return []

  const blockSubjects = new Set(
    (block?.courses || []).map(c => (c.subject || '').toUpperCase()).filter(Boolean)
  )

  const out = []
  for (const uc of userCourses) {
    if (excludeKeys && excludeKeys.has(keyOf(uc))) continue
    const ucSubj = (uc.subject || '').toUpperCase()
    const ucLvl = parseInt(uc.catalog, 10)
    const inBand = bands.some(b =>
      b.subject === ucSubj && !Number.isNaN(ucLvl) && ucLvl >= b.min && ucLvl <= b.max)
    let inLegacy = legacyApplies && blockSubjects.has(ucSubj)
    if (inLegacy && minLevel > 0 && (Number.isNaN(ucLvl) || ucLvl < minLevel)) inLegacy = false
    if (inBand || inLegacy) out.push(uc)
  }
  return out
}
