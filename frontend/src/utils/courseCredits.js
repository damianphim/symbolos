/**
 * McGill Course Credits Lookup
 * 
 * Most McGill courses are 3 credits, but some departments have different standards.
 * This utility provides accurate credit values for McGill courses.
 * 
 * NOTE: This is the SINGLE SOURCE OF TRUTH for course credit lookups.
 * Do NOT duplicate this logic elsewhere — always import from here.
 */

// ── Named constants (Fix #22: no more magic numbers) ──────────────────────
export const DEFAULT_CREDITS = 3
export const VALID_CREDIT_VALUES = [1, 2, 3, 4, 5, 6, 9, 12]

// Known course credit patterns at McGill
const COURSE_CREDIT_RULES = {
  // Specific courses with non-standard credits
  exact: {
    // 4-credit courses
    'MATH 140': 4,
    'MATH 141': 4,
    'MATH 150': 4,
    'MATH 151': 4,
    'PHYS 131': 4,
    'PHYS 142': 4,
    'CHEM 110': 4,
    'CHEM 120': 4,
    'BIOL 111': 4,
    'BIOL 112': 4,
    
    // 2-credit courses
    'COMP 202': 3, // Actually 3
    'COMP 250': 3, // Actually 3
    
    // 1-credit courses (labs, seminars)
    'CHEM 181': 1,
    'PHYS 181': 1,
    'BIOL 181': 1,
    
    // 6-credit courses (year-long)
    'CHEM 183': 6,
    'PHYS 183': 6,
  },
  
  // Pattern-based rules
  patterns: [
    // Lab courses (usually 1 credit)
    { pattern: /L\d{3}$/, credits: 1 },           // e.g., CHEM 213L
    { pattern: /\d{3}L$/, credits: 1 },           // e.g., PHYS 142L
    
    // Seminar courses (usually 1-2 credits)
    { pattern: /^[A-Z]{4}\s?\d{3}S$/, credits: 1 }, // e.g., COMP 400S
    
    // Independent study/research (variable, default 3)
    { pattern: /^[A-Z]{4}\s?[4-5]9\d$/, credits: 3 }, // e.g., COMP 499
    
    // Thesis courses (usually 6-12 credits)
    { pattern: /THES/, credits: 6 },
  ],
  
  // Department defaults (some departments have different standards)
  departments: {
    'MATH': 3,
    'COMP': 3,
    'PHYS': 3,
    'CHEM': 3,
    'BIOL': 3,
    'ECON': 3,
    'PSYC': 3,
    'MGMT': 3,
    'POLI': 3,
    'HIST': 3,
    'ENGL': 3,
    'FREN': 3,
  },
  
  // Special calculus courses are 4 credits
  calculus: ['MATH 140', 'MATH 141', 'MATH 150', 'MATH 151'],
  
  // Science lab courses with integrated lab (4 credits)
  integratedLabs: [
    'PHYS 131', 'PHYS 142',
    'CHEM 110', 'CHEM 120',
    'BIOL 111', 'BIOL 112'
  ]
}

/**
 * Get the credit value for a McGill course
 * @param {string} courseCode - Course code (e.g., "COMP 206" or "COMP206")
 * @returns {number} - Number of credits (default 3)
 */
export function getCourseCredits(courseCode) {
  // Normalize course code
  const normalizedCode = courseCode.replace(/\s+/g, ' ').trim().toUpperCase()
  
  // Check exact matches first
  if (COURSE_CREDIT_RULES.exact[normalizedCode]) {
    return COURSE_CREDIT_RULES.exact[normalizedCode]
  }
  
  // Check if it's a known calculus course (4 credits)
  if (COURSE_CREDIT_RULES.calculus.includes(normalizedCode)) {
    return 4
  }
  
  // Check if it's a science lab course (4 credits)
  if (COURSE_CREDIT_RULES.integratedLabs.includes(normalizedCode)) {
    return 4
  }
  
  // Check pattern-based rules
  for (const rule of COURSE_CREDIT_RULES.patterns) {
    if (rule.pattern.test(normalizedCode)) {
      return rule.credits
    }
  }
  
  // Default to 3 credits (standard at McGill)
  return DEFAULT_CREDITS
}

/**
 * Validate if a credit value is reasonable for McGill
 * @param {number} credits - Credit value to validate
 * @returns {boolean} - True if valid
 */
export function isValidCreditValue(credits) {
  return VALID_CREDIT_VALUES.includes(credits)
}

/**
 * Get common credit options for a course
 * @param {string} [courseCode=''] - Course code
 * @returns {Array<number>} - Array of common credit values
 */
export function getCommonCreditOptions(courseCode = '') {
  const detectedCredits = getCourseCredits(courseCode)
  
  const allOptions = [1, 2, 3, 4, 6, 12]
  
  // Move detected value to front
  return [
    detectedCredits,
    ...allOptions.filter(c => c !== detectedCredits)
  ]
}

/**
 * Format credits for display
 * @param {number} credits - Number of credits
 * @returns {string} - Formatted string
 */
export function formatCredits(credits) {
  if (!credits) return `${DEFAULT_CREDITS} credits`
  return `${credits} credit${credits !== 1 ? 's' : ''}`
}

/**
 * Batch lookup credits for multiple courses
 *
 * FIX #1: Renamed from `addCreditsToCoursesitsCourses` → `addCreditsToCourses`
 *
 * @param {Array<Object>} courses - Array of course objects with courseCode
 * @returns {Array<Object>} - Courses with credits added
 */
export function addCreditsToCourses(courses) {
  return courses.map(course => ({
    ...course,
    credits: course.credits || getCourseCredits(
      course.course_code || course.courseCode || `${course.subject} ${course.catalog}`,
      course.subject,
      course.catalog
    )
  }))
}

/**
 * Get special notes about course credits
 * @param {string} courseCode - Course code
 * @returns {string|null} - Note about credits or null
 */
export function getCreditNotes(courseCode) {
  const normalizedCode = courseCode.replace(/\s+/g, ' ').trim().toUpperCase()
  
  if (COURSE_CREDIT_RULES.calculus.includes(normalizedCode)) {
    return '4 credits (includes tutorial)'
  }
  
  if (COURSE_CREDIT_RULES.integratedLabs.includes(normalizedCode)) {
    return '4 credits (includes lab component)'
  }
  
  if (/L\d{3}$/.test(normalizedCode) || /\d{3}L$/.test(normalizedCode)) {
    return '1 credit (lab only)'
  }
  
  if (/THES/.test(normalizedCode)) {
    return 'Variable credits (thesis/research)'
  }
  
  return null
}

// Default export
export default {
  getCourseCredits,
  isValidCreditValue,
  getCommonCreditOptions,
  formatCredits,
  addCreditsToCourses,
  getCreditNotes
}