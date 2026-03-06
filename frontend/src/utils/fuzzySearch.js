/**
 * Fuzzy course search correction utilities.
 *
 * Strategy:
 *  1. Normalize spacing — "COMP202" or "comp 202" → "COMP 202"
 *  2. Extract subject + catalog parts if recognisable
 *  3. If zero results come back, compute Levenshtein distance between the
 *     typed subject and every known McGill subject code, then retry with
 *     the closest match (≤ 2 edits away).
 *  4. For free-text queries (e.g. "introdcution to programming") run a
 *     simple token-level fuzzy match against known title fragments.
 */

// ── All active McGill subject prefixes ──────────────────────────────────────
export const KNOWN_SUBJECTS = [
  'ACCT','ANAT','ANTH','ARAB','ARBC','ARCG','ARCH','ARTH','ARTS',
  'ATOC','BIOL','BIOC','BMDE','BREE','CANS','CATH','CCOM','CDNS',
  'CHEM','CHIN','CHEE','CIVE','CLCV','CLAS','COMM','COMP','CONS',
  'DENT','DEWA','DNTP','DRSL','EARS','EAST','ECSE','EDEC','EDPE',
  'EDSL','EDUC','ENGL','ENGR','ENVB','ENVI','EPSC','ESYS','EXMD',
  'FINE','FREN','GEOG','GEOL','GERM','GKIR','GLAM','HIST','HLTH',
  'HRPD','HURO','IBUS','IDFT','INTD','IPHA','ISLA','ITAL','ITSN',
  'JRNL','KORE','LARC','LATI','LATN','LAWS','LING','LSCI','MASC',
  'MATH','MDPH','MGSC','MIMM','MNGT','MUSC','NASC','NEUR','NSCI',
  'NUTR','OCCU','OFFS','PHAR','PHGY','PHIL','PHYS','PLNT','POLI',
  'PORT','PSYC','PTOT','RELG','RELI','RUSS','SLIS','SLPG','SOCI',
  'SPAN','SPCH','SURG','SWRK','THEA','THEO','TURK','URBS','VETS',
  'WILD','WMST','YIDD',
]

// ── Levenshtein distance (capped at maxD for speed) ─────────────────────────
function levenshtein(a, b, maxD = 3) {
  if (Math.abs(a.length - b.length) > maxD) return maxD + 1
  const dp = Array.from({ length: a.length + 1 }, (_, i) => i)
  for (let j = 1; j <= b.length; j++) {
    let prev = j
    for (let i = 1; i <= a.length; i++) {
      const temp = dp[i - 1] + (a[i - 1] !== b[j - 1] ? 1 : 0)
      dp[i - 1] = prev
      prev = Math.min(prev + 1, dp[i] + 1, temp)
    }
    dp[a.length] = prev
    if (Math.min(...dp) > maxD) return maxD + 1
  }
  return dp[a.length]
}

// ── Closest known subject (returns null if nothing within maxD edits) ────────
export function closestSubject(typed, maxD = 2) {
  const upper = typed.toUpperCase().replace(/[^A-Z]/g, '')
  if (upper.length < 2) return null
  let best = null, bestD = maxD + 1
  for (const s of KNOWN_SUBJECTS) {
    const d = levenshtein(upper, s, maxD)
    if (d < bestD) { bestD = d; best = s }
  }
  return bestD <= maxD ? best : null
}

// ── Normalise a raw user query ───────────────────────────────────────────────
// "comp202" → "COMP 202"
// "comp  202" → "COMP 202"
// "COMP202L" → "COMP 202"  (strip section letter if any)
const COURSE_CODE_RE = /^([A-Za-z]{2,6})\s*(\d{3}[A-Za-z]?)$/

export function normalizeQuery(raw) {
  const trimmed = raw.trim()
  const m = trimmed.match(COURSE_CODE_RE)
  if (m) {
    // Strip trailing letter suffix from catalog (e.g. 202L → 202)
    const catalog = m[2].replace(/[A-Za-z]+$/, '')
    return `${m[1].toUpperCase()} ${catalog}`
  }
  // Collapse multiple spaces
  return trimmed.replace(/\s+/g, ' ')
}

// ── Build correction candidates from a zero-result query ────────────────────
export function buildCorrectionCandidates(raw) {
  const normalized = normalizeQuery(raw)
  const parts = normalized.split(' ')

  // Might be a course code like "CMOP 202"
  if (parts.length >= 2 && /^\d{3}$/.test(parts[parts.length - 1])) {
    const subjectPart = parts.slice(0, -1).join('')
    const catalog     = parts[parts.length - 1]
    const corrected   = closestSubject(subjectPart)
    if (corrected && corrected !== subjectPart.toUpperCase()) {
      return [{ query: `${corrected} ${catalog}`, note: `${corrected} ${catalog}` }]
    }
  }

  // Single token that looks like a malformed code e.g. "CMOP202"
  const m = raw.trim().match(/^([A-Za-z]{2,6})(\d{3})$/)
  if (m) {
    const corrected = closestSubject(m[1])
    if (corrected) return [{ query: `${corrected} ${m[2]}`, note: `${corrected} ${m[2]}` }]
  }

  return []
}
