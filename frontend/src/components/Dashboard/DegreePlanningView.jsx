import React, { useState, useEffect, useMemo, useRef } from 'react'
import {
  FaHeart, FaRegHeart, FaCheckCircle, FaStar, FaBook,
  FaBullseye, FaFileUpload, FaChevronDown, FaChevronUp,
  FaGraduationCap, FaListAlt, FaLightbulb, FaExternalLinkAlt,
  FaChevronRight, FaCircle, FaBolt, FaPlane, FaInfoCircle
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import { supabase } from '../../lib/supabase'
import DegreeProgressTracker from './DegreeProgressTracker'
import DegreeRequirementsView from './DegreeRequirementsView'
import StudyAbroadView from './StudyAbroadView'
import AdvisingResourcesView from './AdvisingResourcesView'
import './DegreePlanningView.css'

// Fix double /api/api bug
const rawBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_BASE = rawBase.replace(/\/api\/?$/, '')

/** Returns Authorization header with the current Supabase Bearer token. */
async function getAuthHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) return {}
  return { Authorization: `Bearer ${session.access_token}` }
}

// Map profile major/minor names to program_keys
function toProgramKey(name, type = 'major', faculty = '') {
  if (!name) return null
  // Normalize: strip trailing degree designators like "(B.A.)", "(B.Sc.)", "(Honours)"
  name = name.replace(/\s*\([^)]+\)\s*$/, '').trim() || name
  const fl = faculty.toLowerCase()
  const isSci = fl.includes('science') && !fl.includes('arts & science') && !fl.includes('arts and science')
  const isBasc = fl.includes('arts & science') || fl.includes('arts and science')
  const isEng  = fl.includes('engineering')
  const isEnv  = fl.includes('environment') || fl.includes('bieler')
  const isLaw  = fl.includes('faculty of law') || fl === 'law'
  const isAes  = fl.includes('agricultural and environmental') || fl.includes('agri-env') || fl === 'aes'
  const isDentistry = fl.includes('dental medicine') || fl.includes('dentistry')

  // Faculty of Law – BCL/JD (single program regardless of major name stored)
  if (isLaw) {
    return 'law_bcl_jd'
  }

  // Faculty of Dental Medicine and Oral Health Sciences
  if (isDentistry) {
    const dentMap = {
      'Doctor of Dental Medicine (D.M.D.) – Four-Year Program': 'dmd_dentistry',
      'Dental Preparatory Year (Dent-P)': 'dentp_bsc',
    }
    if (dentMap[name]) return dentMap[name]
    return 'dmd_dentistry'
  }

  // Faculty of Agricultural and Environmental Sciences
  if (isAes) {
    const aesMap = {
      'Environmental Biology':                   'envbio_bsc_agenvsc',
      'Environmental Biology (Honours)':         'envbio_honours_bsc_agenvsc',
      'Agricultural Economics':                  'agec_bsc_agenvsc',
      'Life Sciences (Biological and Agricultural)': 'lifesci_bsc_agenvsc',
      'Bioresource Engineering':                 'bree_beng',
    }
    if (aesMap[name]) return aesMap[name]
    if (type === 'honours') return 'envbio_honours_bsc_agenvsc'
  }

  // Bieler School of Environment B.A. programs
  if (isEnv) {
    const envMap = {
      'Ecological Determinants of Health in Society': 'environment_ecological_determinants_ba',
      'Economics and the Earth\'s Environment': 'environment_economics_earth_ba',
      'Environment and Development': 'environment_development_ba',
    }
    if (envMap[name]) return envMap[name]
    if (type === 'minor') return 'environment_minor_ba'
    if (type === 'diploma') return 'environment_diploma'
  }

  // B.A. & Sc. interfaculty programs
  if (isBasc) {
    const bascMap = {
      'Cognitive Science': 'cogs_interfaculty',
      'Cognitive Science (Honours)': 'cogs_honours',
      'Sustainability, Science and Society': 'sss_interfaculty',
      'Sustainability, Science and Society (Honours)': 'sss_honours',
      'Environment': 'environment_interfaculty',
      'Environment (Honours)': 'environment_honours',
    }
    if (bascMap[name]) return `${bascMap[name]}_basc`
    // Fall through to arts/science maps for multi-track
  }

  // Science programs use _bsc suffix
  if (isSci) {
    const sciMap = {
      'Computer Science': 'cs',
      'Software Engineering': 'software_engineering',
      'Mathematics': 'mathematics',
      'Statistics': 'statistics',
      'Applied Mathematics': 'applied_mathematics',
      'Physics': 'physics',
      'Biology': 'biology',
      'Chemistry': 'chemistry',
      'Biochemistry': 'biochemistry',
      'Neuroscience': 'neuroscience',
      'Physiology': 'physiology',
      'Microbiology and Immunology': 'micro_immuno',
      'Earth and Planetary Sciences': 'earth_planetary',
      'Atmospheric and Oceanic Sciences': 'atmos_oceanic',
      'Environmental Science': 'environmental_science',
      'Geography': 'geography_sci',
    }
    const slug = sciMap[name] || name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '')
    return `${slug}_${type}_bsc`
  }

  // Management (Desautels) programs
  if (fl.includes('management') || fl.includes('desautels')) {
    const mgmtSlugMap = {
      'Accounting': 'accounting',
      'Finance': 'finance',
      'Marketing': 'marketing',
      'Business Analytics': 'business_analytics',
      'Strategic Management': 'strategic_management',
      'Information Technology Management': 'it_management',
      'Organizational Behaviour and Human Resources': 'ob_hr',
      'International Management': 'intl_management',
      'Managing for Sustainability': 'managing_sustainability',
      'Retail Management': 'retail_management',
      'Economics for Management Students': 'economics_management',
      'Mathematics and Statistics for Management': 'math_stats_management',
      'Investment Management': 'investment_management',
    }
    const slug = mgmtSlugMap[name] || name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '')
    if (type === 'honours') return `${slug}_honours_bcom`
    if (type === 'concentration') return `${slug}_concentration_bcom`
    return `${slug}_major_bcom`
  }

  const map = {
    'Anthropology': 'anthropology',
    'Art History': 'art_history',
    'Economics': 'economics',
    'Political Science': 'political_science',
    'Psychology': 'psychology',
    'Sociology': 'sociology',
    'Linguistics': 'linguistics',
    'History': 'history',
    'Philosophy': 'philosophy',
    'English': 'english_literature',
    'English Literature': 'english_literature',
    'Communication Studies': 'communication_studies',
    'International Development Studies': 'intl_development',
    'International Development': 'intl_development',
    'Gender, Sexuality, Feminist and Social Justice Studies': 'gsfsj',
    'Canadian Studies': 'canadian_studies',
    'Classical Studies': 'classics',
    'Classics': 'classics',
    'Jewish Studies': 'jewish_studies',
    'East Asian Studies': 'east_asian_studies',
    'Geography': 'geography',
    'Computer Science': 'computer_science_arts',
    'Supplemental Computer Science': 'supplemental_computer_science',
    'German Studies': 'german_studies',
    'Hispanic Studies': 'hispanic_studies',
    'Italian Studies': 'italian_studies',
    'Religious Studies': 'religious_studies',
    'African Studies': 'african_studies',
    'Information Studies': 'information_studies',
    'Latin American and Caribbean Studies': 'latin_american_caribbean',
    'Liberal Arts': 'liberal_arts',
    'French': 'french',
    'French Language and Literature': 'french',
    'Cognitive Science': 'cognitive_science',
    'European Literature and Culture': 'european_lit_culture',
    'World Islamic and Middle East Studies': 'world_islamic_middle_east',
    // Science for Arts
    'Science for Arts Students': 'science_for_arts_students',
    'Science for Arts': 'science_for_arts_students',
    // Engineering programs
    'Software Engineering': 'software_engineering_coop',
    'Computer Engineering': 'computer_engineering',
    'Electrical Engineering': 'electrical_engineering',
    'Mechanical Engineering': 'mechanical_engineering',
    'Civil Engineering': 'civil_engineering',
    'Chemical Engineering': 'chemical_engineering',
    'Bioengineering': 'bioengineering',
    'Mining Engineering': 'mining_engineering',
    'Materials Engineering': 'materials_engineering_coop',
  }
  const slug = map[name] || name.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '')
  return `${slug}_${type}`
}

function matchCourse(req, userCourses) {
  if (!req.catalog) return null
  const key = `${req.subject} ${req.catalog}`.toUpperCase()
  return userCourses.find(c =>
    `${c.subject || ''} ${c.catalog || ''}`.toUpperCase() === key
  ) || null
}

// Transfer credits show as done but do NOT count toward credits
function normalizeCode(code) {
  return (code || '').toUpperCase()
    .replace(/([A-Z])(\d)/g, '$1 $2')  // COMP202 -> COMP 202
    .replace(/\s+/g, ' ')
    .trim()
}
function matchTransfer(req, advancedStanding = [], { requireMajorCredit = false } = {}) {
  if (!req.catalog) return false
  const key = normalizeCode(`${req.subject} ${req.catalog}`)
  return advancedStanding.some(t => {
    if (normalizeCode(t.course_code) !== key) return false
    if (requireMajorCredit) return !!t.counts_toward_major
    return true
  })
}

// ── Accordion ─────────────────────────────────────────────────────────────────
function AccordionCard({ icon, title, count, accentColor, defaultOpen = true, children }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className={`dp-accordion ${open ? 'dp-accordion--open' : ''}`}>
      <button className="dp-accordion-header" onClick={() => setOpen(o => !o)}>
        <div className="dp-accordion-left">
          <span className="dp-accordion-icon" style={{ color: accentColor }}>{icon}</span>
          <span className="dp-accordion-title">{title}</span>
          {count != null && count > 0 && (
            <span className="dp-accordion-badge" style={{ background: accentColor }}>{count}</span>
          )}
        </div>
        <span className="dp-accordion-chevron">{open ? <FaChevronUp /> : <FaChevronDown />}</span>
      </button>
      {open && <div className="dp-accordion-body">{children}</div>}
    </div>
  )
}

function EmptyState({ icon, title, subtitle }) {
  return (
    <div className="dp-empty">
      <span className="dp-empty-icon">{icon}</span>
      <p className="dp-empty-title">{title}</p>
      <p className="dp-empty-sub">{subtitle}</p>
    </div>
  )
}

function CourseRow({ course, onClick, actions }) {
  return (
    <div className="dp-course-row">
      <div className="dp-course-info" onClick={onClick}>
        <span className="dp-course-code">{course.subject} {course.catalog}</span>
        <span className="dp-course-title">{course.course_title || course.title}</span>
        {(course.term || course.year || course.credits) && (
          <span className="dp-course-meta">
            {course.term && course.year ? `${course.term} ${course.year}` : ''}
            {course.credits ? ` · ${course.credits} cr` : ''}
          </span>
        )}
      </div>
      <div className="dp-course-actions">{actions}</div>
    </div>
  )
}


// ── Electives Panel ────────────────────────────────────────────────────────────
function ElectivesPanel({ profile, completedCourses, currentCourses, programData, minorData, allProgramData, courseAllocations, assignCourse }) {
  const { t } = useLanguage()
  const [recs, setRecs]           = useState(null)
  const [recsLoading, setRecsLoading] = useState(false)
  const [recsError, setRecsError] = useState(null)
  const [showRecs, setShowRecs]   = useState(false)
  const hasLoaded                 = useRef(false)
  const [assignedNote, setAssignedNote] = useState(null) // show warning when user assigns an elective

  // Build a set of ALL course codes that count toward ANY major or minor
  const requiredCodes = useMemo(() => {
    const codes = new Set()
    allProgramData.forEach(prog => {
      prog?.blocks?.forEach(b => b.courses?.forEach(c => {
        if (c.catalog) codes.add(`${c.subject} ${c.catalog}`.toUpperCase())
      }))
    })
    return codes
  }, [allProgramData])

  // Wildcard blocks: any PSYC 300+ etc. — user courses matching these aren't electives
  const wildcardBlocks = useMemo(() => {
    const blocks = []
    allProgramData.forEach(prog => {
      prog?.blocks?.forEach(b => {
        if ((b.courses?.some(c => !c.catalog)) || b.min_level) {
          blocks.push({
            subjects: new Set(b.courses?.map(c => c.subject?.toUpperCase()).filter(Boolean)),
            minLevel: b.min_level || 0,
          })
        }
      })
    })
    return blocks
  }, [allProgramData])

  const handleAssign = (courseKey, programKey) => {
    assignCourse(courseKey, programKey || null)
    if (programKey) {
      setAssignedNote(courseKey)
      setTimeout(() => setAssignedNote(null), 4000)
    }
  }

  // Find courses the user has taken that don't go toward any major/minor
  const electiveCourses = useMemo(() => {
    const advancedStanding = profile?.advanced_standing || []
    const allTaken = [
      ...completedCourses.map(c => ({ ...c, _source: 'completed' })),
      ...currentCourses.map(c => ({ ...c, _source: 'current' })),
      ...advancedStanding.filter(t => t.course_code).map(t => {
        const parts = t.course_code.trim().split(/\s+/)
        return {
          subject: parts[0] || '',
          catalog: parts.slice(1).join(' ') || '',
          course_title: t.course_title || t.title || '',
          credits: t.credits || 3,
          _source: 'transfer',
          _raw: t,
        }
      }),
    ]
    return allTaken.filter(c => {
      if (!c.subject || !c.catalog) return false
      const key = `${c.subject} ${c.catalog}`.toUpperCase()
      if (requiredCodes.has(key)) return false
      if (courseAllocations[key]) return false // manually assigned to a program
      // Check wildcard blocks
      for (const wb of wildcardBlocks) {
        if (!wb.subjects.has(c.subject?.toUpperCase())) continue
        if (wb.minLevel > 0) {
          const lvl = parseInt(c.catalog)
          if (isNaN(lvl) || lvl < wb.minLevel) continue
        }
        return false // matches a wildcard block → not an elective
      }
      return true
    })
  }, [completedCourses, currentCourses, profile, requiredCodes, wildcardBlocks, courseAllocations])

  const _recsRateLimited = () => {
    if (authFlags?.is_admin) return false // admins unlimited
    const key = 'elective_recs_timestamps'
    const now = Date.now()
    const weekAgo = now - 7 * 24 * 60 * 60 * 1000
    try {
      const stamps = JSON.parse(localStorage.getItem(key) || '[]').filter(t => t > weekAgo)
      if (stamps.length >= 2) return true // max 2 per week
      stamps.push(now)
      localStorage.setItem(key, JSON.stringify(stamps))
      return false
    } catch { return false }
  }

  const generateRecs = async (skipRateLimit = false) => {
    if (!skipRateLimit && _recsRateLimited()) {
      setRecsError('You can refresh elective suggestions up to 2 times per week. Try again later.')
      return
    }
    setRecsLoading(true)
    setRecsError(null)
    try {
      const advancedStanding = profile?.advanced_standing || []
      const allCourses = [...completedCourses, ...currentCourses]
      const coursesTaken = [
        ...allCourses
          .filter(c => c.subject && c.catalog)
          .map(c => `${c.subject} ${c.catalog}`.trim()),
        ...advancedStanding
          .filter(t => t.course_code)
          .map(t => t.course_code.trim()),
      ].filter(Boolean)

      const excludeCourses = Array.from(requiredCodes)

      const { data: { session } } = await supabase.auth.getSession()
      const token = session?.access_token
      if (!token) throw new Error('Not authenticated')

      const res = await fetch(`${API_BASE}/api/electives/recommend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          major:           profile?.major        || null,
          minor:           profile?.minor        || null,
          concentration:   profile?.concentration|| null,
          year:            (profile?.year >= 0 && profile?.year <= 10) ? profile.year : null,
          interests:       profile?.interests    || null,
          courses_taken:   coursesTaken,
          exclude_courses: excludeCourses,
        })
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
      if (!data.success) throw new Error(data.detail || 'Failed')
      setRecs(data.data)
    } catch(e) {
      setRecsError('Could not generate recommendations. Try again.')
    } finally {
      setRecsLoading(false)
    }
  }

  const handleShowRecs = () => {
    setShowRecs(true)
    if (!hasLoaded.current) {
      hasLoaded.current = true
      generateRecs(true) // initial load doesn't count toward rate limit
    }
  }

  const profileKey = `${profile?.major}|${profile?.minor}|${profile?.interests}`
  const prevProfileKey = useRef(profileKey)
  useEffect(() => {
    if (!hasLoaded.current) return
    if (prevProfileKey.current === profileKey) return
    prevProfileKey.current = profileKey
    generateRecs(true) // profile change doesn't count toward rate limit
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profileKey])

  const CATEGORY_COLORS = {
    'Breadth':           { bg: '#eff6ff', color: '#1d4ed8' },
    'Career':            { bg: '#f0fdf4', color: '#15803d' },
    'Advanced':          { bg: '#faf5ff', color: '#7c3aed' },
    'Interdisciplinary': { bg: '#fff7ed', color: '#c2410c' },
    'Interest':          { bg: '#fef9c3', color: '#92400e' },
  }

  const SOURCE_LABELS = { completed: 'Done', current: 'Taking', transfer: 'Transfer' }
  const SOURCE_COLORS = {
    completed: { bg: '#f0fdf4', color: '#15803d' },
    current:   { bg: '#eff6ff', color: '#1d4ed8' },
    transfer:  { bg: '#fef9c3', color: '#92400e' },
  }

  return (
    <div className="dp-electives">
      {/* ── AI Recommendations ──────────────────────────── */}
      <div className="dp-electives-recs-section">
        <div className="dp-electives-recs-header">
          <span className="dp-electives-spark">✦</span>
          <div>
            <h3 className="dp-electives-title">Recommended Electives</h3>
            <p className="dp-electives-sub">
              AI picks for {[profile?.major, profile?.minor].filter(Boolean).join(' + ')}
              {profile?.interests ? ` · ${profile.interests}` : ''}
            </p>
          </div>
          {showRecs ? (
            <button className="dp-electives-refresh" onClick={generateRecs} disabled={recsLoading}>
              {recsLoading ? '...' : '↻'}
            </button>
          ) : (
            <button className="dp-electives-refresh dp-electives-refresh--generate" onClick={handleShowRecs}>
              Generate ✦
            </button>
          )}
        </div>

        {showRecs && recsLoading && (
          <div className="dp-electives-loading">
            <div className="dp-req-spinner" />
            <span>{t('dp.generatingRecs')}</span>
          </div>
        )}

        {showRecs && recsError && !recsLoading && (
          <div className="dp-electives-error">
            {recsError}
            <button onClick={generateRecs}>{t('dp.retry')}</button>
          </div>
        )}

        {showRecs && recs && !recsLoading && (
          <>
            {recs.theme && (
              <p className="dp-electives-theme">💡 {recs.theme}</p>
            )}
            <div className="dp-electives-grid">
              {recs.recommendations?.map((c, i) => {
                const alreadyTaken = [...completedCourses, ...currentCourses].some(uc =>
                  `${uc.subject} ${uc.catalog}`.toUpperCase() === `${c.subject} ${c.catalog}`.toUpperCase()
                )
                const catStyle = CATEGORY_COLORS[c.category] || CATEGORY_COLORS['Breadth']
                return (
                  <div key={i} className={`dp-elective-card ${alreadyTaken ? 'dp-elective-card--taken' : ''}`}>
                    <div className="dp-elective-top">
                      <span className="dp-elective-code">{c.subject} {c.catalog}</span>
                      <span className="dp-elective-cat" style={{ background: catStyle.bg, color: catStyle.color }}>
                        {c.category}
                      </span>
                      {alreadyTaken && <span className="dp-elective-taken">✓ {t('dp.statusTaking')}</span>}
                    </div>
                    <p className="dp-elective-title">{c.title}</p>
                    <p className="dp-elective-why">{c.why}</p>
                    <span className="dp-elective-credits">{c.credits} cr</span>
                  </div>
                )
              })}
            </div>
            <p className="rsb-disclaimer">{t('rsb.disclaimer')}</p>
          </>
        )}

        {!showRecs && (
          <div className="dp-electives-recs-prompt">
            <p>Get personalized elective suggestions based on your program and interests.</p>
          </div>
        )}
      </div>

      {/* ── Taken Electives ─────────────────────────────── */}
      <div className="dp-electives-header">
        <div className="dp-electives-title-row">
          <span className="dp-electives-spark">📚</span>
          <div>
            <h3 className="dp-electives-title">My Elective Courses</h3>
            <p className="dp-electives-sub">
              Courses you've taken that don't count toward{' '}
              {[profile?.major, profile?.minor].filter(Boolean).join(' or ') || 'your program'}
            </p>
          </div>
        </div>
        <span className="dp-electives-badge">{electiveCourses.length}</span>
      </div>

      {electiveCourses.length === 0 ? (
        <div className="dp-electives-empty">
          <span style={{ fontSize: '2rem', opacity: 0.3 }}>🎓</span>
          <p>No elective courses found yet.</p>
          <p style={{ fontSize: '0.8rem', opacity: 0.6 }}>
            Courses you complete outside your major &amp; minor requirements will appear here.
          </p>
        </div>
      ) : (
        <div className="dp-electives-grid">
          {electiveCourses.map((c, i) => {
            const srcStyle = SOURCE_COLORS[c._source] || SOURCE_COLORS.completed
            return (
              <div key={i} className="dp-elective-card dp-elective-card--taken">
                <div className="dp-elective-top">
                  <span className="dp-elective-code">{c.subject} {c.catalog}</span>
                  <span
                    className="dp-elective-cat"
                    style={{ background: srcStyle.bg, color: srcStyle.color }}
                  >
                    {SOURCE_LABELS[c._source] || 'Done'}
                  </span>
                </div>
                <p className="dp-elective-title">{c.course_title || c.title || '—'}</p>
                <div className="dp-elective-assign">
                  <select
                    className="dp-elective-assign-select"
                    value={courseAllocations[`${c.subject} ${c.catalog}`.toUpperCase()] || ''}
                    onChange={e => handleAssign(`${c.subject} ${c.catalog}`.toUpperCase(), e.target.value)}
                  >
                    <option value="">Count toward...</option>
                    {allProgramData.map(prog => prog && (
                      <option key={prog.program_key} value={prog.program_key}>
                        {prog.name?.replace(/\s*[–-]\s*(Major|Minor|Honours|Concentration).*/, '') || prog.program_key}
                      </option>
                    ))}
                  </select>
                  {assignedNote === `${c.subject} ${c.catalog}`.toUpperCase() && (
                    <p className="dp-elective-assign-note">⚠ Double-check with your academic advisor whether this course actually counts toward this program.</p>
                  )}
                </div>
                {c.credits && <span className="dp-elective-credits">{c.credits} cr</span>}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

// ── My Program Requirements card ──────────────────────────────────────────────
function ProgramSection({ prog, completedCourses, currentCourses, advStanding, openBlocks, setOpenBlocks, courseAllocations = {}, assignCourse, overlapKeys = new Set(), allProgramData = [] }) {
  const { t } = useLanguage()
  if (!prog) return null

  const progKey = prog.program_key

  // Progress: two-phase — exact listed courses then wildcard blocks (min_level / null catalog)
  const totalCredits = prog.total_credits || 36
  let earnedCredits = 0
  const seenDbKeys   = new Set() // DB course keys already scanned
  const seenUserKeys = new Set() // user course keys already counted (avoid double-count)

  // Phase 1: exact course matches (transfer excluded from credit total)
  prog.blocks?.forEach(b => b.courses?.forEach(c => {
    if (!c.catalog) return
    const key = `${c.subject} ${c.catalog}`.toUpperCase()
    if (seenDbKeys.has(key)) return
    seenDbKeys.add(key)
    if (matchTransfer(c, advStanding)) return
    // If overlapping course allocated to a different program, skip it
    if (overlapKeys.has(key) && courseAllocations[key] && courseAllocations[key] !== progKey) return
    const inCompleted = completedCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key)
    const inCurrent   = currentCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key)
    if (inCompleted || inCurrent) {
      // Use actual earned credits from user record (more accurate than seeded value)
      const uc = [...completedCourses, ...currentCourses].find(u => `${u.subject} ${u.catalog}`.toUpperCase() === key)
      earnedCredits += parseFloat(uc?.credits || c.credits || 3)
      seenUserKeys.add(key)
    }
  }))

  // Phase 2: wildcard blocks — blocks with min_level or null-catalog entries
  // Count any matching user course not already counted above
  prog.blocks?.forEach(b => {
    const hasWildcard = (b.courses?.some(c => !c.catalog)) || b.min_level
    if (!hasWildcard) return
    const blockSubjects = new Set(b.courses?.map(c => c.subject?.toUpperCase()).filter(Boolean))
    const minLevel = b.min_level || 0
    for (const uc of [...completedCourses, ...currentCourses]) {
      const ucKey = `${uc.subject} ${uc.catalog}`.toUpperCase()
      if (seenDbKeys.has(ucKey) || seenUserKeys.has(ucKey)) continue
      if (!blockSubjects.has(uc.subject?.toUpperCase())) continue
      if (minLevel > 0) { const lvl = parseInt(uc.catalog); if (isNaN(lvl) || lvl < minLevel) continue }
      // If overlapping course allocated to a different program, skip it
      if (overlapKeys.has(ucKey) && courseAllocations[ucKey] && courseAllocations[ucKey] !== progKey) continue
      earnedCredits += parseFloat(uc.credits || 3)
      seenUserKeys.add(ucKey)
    }
  })

  const pct = Math.min(100, Math.round((earnedCredits / totalCredits) * 100))

  return (
    <div className="dp-prog-section">
      {/* Progress bar */}
      <div className="dp-prog-bar-wrap">
        <div className="dp-prog-bar-track">
          <div className="dp-prog-bar-fill" style={{ width: `${pct}%` }} />
        </div>
        <span className="dp-prog-bar-label">{t('dp.creditsOf').replace('{earned}', earnedCredits).replace('{total}', totalCredits)}</span>
      </div>

      {/* Blocks */}
      {prog.blocks?.map(block => {
        const isOpen = openBlocks[block.id]
        // For block progress: count matched courses (any, not just is_required) + wildcard matches
        const blockCourses = block.courses?.filter(c => c.catalog) || []
        const exactMatched = blockCourses.filter(c => {
          const key = `${c.subject} ${c.catalog}`.toUpperCase()
          // Transfer credits count as "done" for block completion (course is met)
          if (matchTransfer(c, advStanding)) return true
          return completedCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key) ||
                 currentCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key)
        })
        const exactKeys = new Set(blockCourses.map(c => `${c.subject} ${c.catalog}`.toUpperCase()))
        const creditsNeeded = block.credits_needed || 0
        let creditsEarned = exactMatched.reduce((s, c) => s + parseFloat(c.credits || 3), 0)

        // Wildcard: blocks with null-catalog entries or min_level count matching user courses
        const hasWildcard = (block.courses?.some(c => !c.catalog)) || block.min_level
        if (hasWildcard && creditsEarned < creditsNeeded) {
          const blockSubjects = new Set(block.courses?.map(c => c.subject?.toUpperCase()).filter(Boolean))
          const minLevel = block.min_level || 0
          for (const uc of [...completedCourses, ...currentCourses]) {
            if (creditsEarned >= creditsNeeded) break
            const ucKey = `${uc.subject} ${uc.catalog}`.toUpperCase()
            if (exactKeys.has(ucKey)) continue
            if (!blockSubjects.has(uc.subject?.toUpperCase())) continue
            if (minLevel > 0) { const lvl = parseInt(uc.catalog); if (isNaN(lvl) || lvl < minLevel) continue }
            creditsEarned += parseFloat(uc.credits || 3)
          }
        }
        const blockMatched = exactMatched
        const blockDone = creditsNeeded > 0 && creditsEarned >= creditsNeeded

        return (
          <div key={block.id} className={`dp-req-block ${blockDone ? 'dp-req-block--done' : ''}`}>
            <button
              className="dp-req-block-header"
              onClick={() => setOpenBlocks(p => ({ ...p, [block.id]: !p[block.id] }))}
            >
              <div className="dp-req-block-left">
                <span className="dp-req-block-chevron">{isOpen ? <FaChevronDown /> : <FaChevronRight />}</span>
                <span className="dp-req-block-name">{block.title}</span>
                {block.credits_needed && <span className="dp-req-block-cr">{block.credits_needed}cr</span>}
              </div>
              <div className="dp-req-block-right">
                <span className={`dp-req-pill ${blockDone ? 'dp-req-pill--done' : ''}`}>
                  {blockDone ? '✓ Done' : `${creditsEarned}/${creditsNeeded}cr`}
                </span>
              </div>
            </button>

            {isOpen && (
              <div className="dp-req-block-courses">
                {block.notes && <p className="dp-req-block-note">{block.notes}</p>}
                {block.courses?.map(c => {
                  const key = `${c.subject} ${c.catalog}`.toUpperCase()
                  const isTransfer = matchTransfer(c, advStanding)
                  const done = isTransfer || completedCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key)
                  const taking = !done && currentCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key)
                  const isOverlap = c.catalog && overlapKeys.has(key) && (done || taking)
                  const allocatedTo = isOverlap ? (courseAllocations[key] || null) : null
                  const allocatedElsewhere = isOverlap && allocatedTo && allocatedTo !== progKey
                  const otherProgName = allocatedElsewhere
                    ? (allProgramData.find(p => p?.program_key === allocatedTo)?.name?.replace(/\s*[–-]\s*(Major|Minor|Honours|Concentration).*/, '') || allocatedTo)
                    : null
                  return (
                    <div key={c.id} className={`dp-req-course ${done && !allocatedElsewhere ? 'dp-req-course--done' : ''} ${taking && !allocatedElsewhere ? 'dp-req-course--taking' : ''} ${allocatedElsewhere ? 'dp-req-course--conflict' : ''}`}>
                      {done && !allocatedElsewhere
                        ? <FaCheckCircle className="dp-req-course-icon dp-req-course-icon--done" />
                        : taking && !allocatedElsewhere
                          ? <FaCircle className="dp-req-course-icon dp-req-course-icon--taking" />
                          : <FaCircle className="dp-req-course-icon dp-req-course-icon--empty" />
                      }
                      <div className="dp-req-course-main">
                        <div className="dp-req-course-row">
                          <span className="dp-req-course-code">{c.subject} {c.catalog || '•••'}</span>
                          <span className="dp-req-course-title">{c.title}</span>
                          {done && isTransfer  && <span className="dp-req-transfer-tag">{t('dp.statusTransfer')} · {t('dp.transferExempt')}</span>}
                          {done && !isTransfer && !allocatedElsewhere && <span className="dp-req-done-tag">{t('dp.statusDone')}</span>}
                          {taking && !allocatedElsewhere && <span className="dp-req-taking-tag">{t('dp.statusTaking')}</span>}
                          {allocatedElsewhere && <span className="dp-req-conflict-tag">Counted toward {otherProgName}</span>}
                        </div>
                        {isOverlap && assignCourse && (
                          <div className="dp-req-overlap-assign">
                            <span className="dp-req-overlap-label">⚠ Overlaps with another program —</span>
                            <select
                              className="dp-req-overlap-select"
                              value={allocatedTo || ''}
                              onChange={e => assignCourse(key, e.target.value || null)}
                            >
                              <option value="">Count toward all (unassigned)</option>
                              {allProgramData.filter(Boolean).map(p => (
                                <option key={p.program_key} value={p.program_key}>
                                  Count toward {p.name?.replace(/\s*[–-]\s*(Major|Minor|Honours|Concentration).*/, '') || p.program_key} only
                                </option>
                              ))}
                            </select>
                          </div>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

function MyProgramCard({ profile, completedCourses, currentCourses }) {
  const { t } = useLanguage()
  const [programData, setProgramData]         = useState(null)
  const [minorData, setMinorData]             = useState(null)
  const [sciData, setSciData]                 = useState(null)
  const [coreData, setCoreData]               = useState(null)
  const [concentrationData, setConcentrationData] = useState(null)
  // Additional majors/minors: keyed maps  { programKey → data }
  const [extraMajorsData, setExtraMajorsData] = useState({})
  const [extraMinorsData, setExtraMinorsData] = useState({})
  const [loading, setLoading]                 = useState(false)
  const [seeding, setSeeding]                 = useState(false)
  const [openBlocks, setOpenBlocks]           = useState({})
  const [activeTab, setActiveTab]             = useState('major')
  const [loadFailed, setLoadFailed]           = useState(false)
  const [unavailable, setUnavailable]         = useState({ major: false, minor: false, core: false, concentration: false })

  // Course allocations — lifted from ElectivesPanel so ProgramSection can also use them
  const [courseAllocations, setCourseAllocations] = useState(() => {
    try { return JSON.parse(localStorage.getItem('dp_course_allocations') || '{}') } catch { return {} }
  })
  const assignCourse = (courseKey, programKey) => {
    const next = programKey ? { ...courseAllocations, [courseKey]: programKey } : (() => {
      const c = { ...courseAllocations }; delete c[courseKey]; return c
    })()
    setCourseAllocations(next)
    localStorage.setItem('dp_course_allocations', JSON.stringify(next))
  }

  const advStanding = profile?.advanced_standing || []

  const isBasc          = profile?.faculty === 'Bachelor of Arts and Science'
  const bascStream      = isBasc ? (profile?.concentration || 'Interfaculty') : null
  const bascIsMultiTrack = bascStream === 'Multi-track' || bascStream === 'Joint Honours'

  const isMgmt = !isBasc && (
    profile?.faculty === 'Management' ||
    (profile?.faculty || '').toLowerCase().includes('management') ||
    (profile?.faculty || '').toLowerCase().includes('desautels')
  )

  // Foundation year waived if Arts or B.A. & Sc. with 24+ transfer credits
  const transferCredits = advStanding.reduce((s, c) => s + (c.credits || 0), 0)
  const foundationWaived = transferCredits >= 24 &&
    (profile?.faculty === 'Faculty of Arts' || isBasc)

  const majorKey = toProgramKey(
    profile?.major,
    'major',
    isBasc && !bascIsMultiTrack ? 'Faculty of Arts & Science' : (profile?.faculty || '')
  )
  const sciKey = isBasc && bascIsMultiTrack
    ? toProgramKey(profile?.other_majors?.[0], 'major', 'Faculty of Science')
    : null
  const minorKey = !isMgmt ? toProgramKey(profile?.minor, 'minor', profile?.faculty || '') : null
  // Management-specific keys
  const coreKey          = isMgmt ? 'bcom_core' : null
  const concentrationKey = isMgmt && profile?.concentration
    ? toProgramKey(profile.concentration, 'concentration', profile?.faculty || '')
    : null

  // Extra majors: other_majors[] excluding the BASC science slot (already handled by sciKey)
  const extraMajorsList = useMemo(() => {
    if (!profile?.other_majors?.length) return []
    return profile.other_majors
      .filter(m => m && !(isBasc && bascIsMultiTrack)) // BASC multi-track already uses sciKey
      .map(name => ({
        name,
        key: toProgramKey(name, 'major', profile?.faculty || ''),
      }))
      .filter(({ key }) => key && key !== majorKey)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile?.other_majors?.join(','), majorKey, isBasc, bascIsMultiTrack])

  // Extra minors: other_minors[] excluding the primary minor
  const extraMinorsList = useMemo(() => {
    if (!profile?.other_minors?.length) return []
    return profile.other_minors
      .filter(m => m)
      .map(name => ({
        name,
        key: toProgramKey(name, 'minor', profile?.faculty || ''),
      }))
      .filter(({ key }) => key && key !== minorKey)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile?.other_minors?.join(','), minorKey])

  const fetchProgram = async (key, setter) => {
    if (!key) return 'skip'
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${API_BASE}/api/degree-requirements/programs/${key}`, {
        cache: 'no-store',
        headers,
      })
      if (res.status === 404) {
        return 'not_found'
      }
      if (!res.ok) return 'error'
      const data = await res.json()
      setter(data)
      setOpenBlocks(prev => {
        const init = { ...prev }
        data.blocks?.forEach((b, i) => { if (i < 2) init[b.id] = true })
        return init
      })
      return 'ok'
    } catch {
      return 'error'
    }
  }

  const fetchedRef = React.useRef(false)

  useEffect(() => {
    if (!profile) return
    if (!majorKey && !minorKey && !sciKey && extraMajorsList.length === 0 && extraMinorsList.length === 0) return
    setLoading(true)
    setLoadFailed(false)
    setProgramData(null)
    setMinorData(null)
    setSciData(null)
    setExtraMajorsData({})
    setExtraMinorsData({})
    setUnavailable({ major: false, minor: false })
    fetchedRef.current = true

    // Fetch extra majors
    const extraMajorFetches = extraMajorsList.map(({ name, key }) =>
      fetchProgram(key, data => setExtraMajorsData(prev => ({ ...prev, [key]: data })))
        .then(result => ({ key, name, result }))
    )
    // Fetch extra minors
    const extraMinorFetches = extraMinorsList.map(({ name, key }) =>
      fetchProgram(key, data => setExtraMinorsData(prev => ({ ...prev, [key]: data })))
        .then(result => ({ key, name, result }))
    )

    Promise.all([
      fetchProgram(majorKey, setProgramData),
      fetchProgram(minorKey, setMinorData),
      fetchProgram(sciKey, setSciData),
      fetchProgram(coreKey, setCoreData),
      fetchProgram(concentrationKey, setConcentrationData),
      ...extraMajorFetches,
      ...extraMinorFetches,
    ]).then(([majorResult, minorResult, , coreResult, concResult]) => {
      setUnavailable({
        major:         majorResult === 'not_found',
        minor:         minorResult === 'not_found',
        core:          coreResult  === 'not_found',
        concentration: concResult  === 'not_found',
      })
    }).finally(() => setLoading(false))
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [majorKey, minorKey, sciKey, coreKey, concentrationKey,
      extraMajorsList.map(x=>x.key).join(','),
      extraMinorsList.map(x=>x.key).join(','),
      !!profile, profile?.concentration])

  const allCourseKeys = useMemo(
    () => [...completedCourses, ...currentCourses].map(c => `${c.subject} ${c.catalog}`).join(','),
    [completedCourses, currentCourses]
  )

  const handleSeed = async () => {
    setSeeding(true)
    try {
      const headers = await getAuthHeaders()
      const res = await fetch(`${API_BASE}/api/degree-requirements/seed`, { method: 'POST', headers })
      const data = await res.json()
      if (data.success) {
        const extraMajorFetches = extraMajorsList.map(({ name, key }) =>
          fetchProgram(key, d => setExtraMajorsData(prev => ({ ...prev, [key]: d })))
        )
        const extraMinorFetches = extraMinorsList.map(({ name, key }) =>
          fetchProgram(key, d => setExtraMinorsData(prev => ({ ...prev, [key]: d })))
        )
        const [majorResult, minorResult, , coreResult, concResult] = await Promise.all([
          fetchProgram(majorKey, setProgramData),
          fetchProgram(minorKey, setMinorData),
          fetchProgram(sciKey, setSciData),
          fetchProgram(coreKey, setCoreData),
          fetchProgram(concentrationKey, setConcentrationData),
          ...extraMajorFetches,
          ...extraMinorFetches,
        ])
        setUnavailable({
          major:         majorResult === 'not_found',
          minor:         minorResult === 'not_found',
          core:          coreResult  === 'not_found',
          concentration: concResult  === 'not_found',
        })
      }
    } catch {}
    finally { setSeeding(false) }
  }

  const hasSomething = profile?.major || profile?.minor ||
    profile?.other_majors?.length > 0 || profile?.other_minors?.length > 0 ||
    (isBasc && profile?.other_majors?.length > 0) ||
    isMgmt
  if (!hasSomething) return null

  const hasMajor         = !!programData
  const hasMinor         = !!minorData
  const hasCore          = !!coreData
  const hasConcentration = !!concentrationData
  const hasExtraMajors   = Object.keys(extraMajorsData).length > 0
  const hasExtraMinors   = Object.keys(extraMinorsData).length > 0
  const hasAny           = hasMajor || hasMinor || hasCore || hasConcentration || hasExtraMajors || hasExtraMinors

  const tabs = []
  if (isMgmt) {
    tabs.push({ id: 'core', label: 'BCom Core', data: coreData, unavailable: unavailable.core })
    if (profile?.major) tabs.push({ id: 'major', label: profile.major, data: programData, unavailable: unavailable.major })
    if (profile?.concentration) tabs.push({ id: 'concentration', label: profile.concentration, data: concentrationData, unavailable: unavailable.concentration })
  } else {
    let majorLabel
    if (isBasc && bascIsMultiTrack) {
      majorLabel = profile?.major ? `${profile.major} (Arts)` : null
    } else {
      majorLabel = profile?.major || null
    }
    if (majorLabel) tabs.push({ id: 'major', label: majorLabel, data: programData, unavailable: unavailable.major })
    if (isBasc && bascIsMultiTrack && profile?.other_majors?.[0]) {
      tabs.push({ id: 'sci', label: `${profile.other_majors[0]} (Science)`, data: sciData, unavailable: false })
    }
    // Additional majors (non-BASC)
    if (!isBasc || !bascIsMultiTrack) {
      extraMajorsList.forEach(({ name, key }) => {
        tabs.push({ id: `extra_major_${key}`, label: name, data: extraMajorsData[key] || null, unavailable: !extraMajorsData[key], type: 'major' })
      })
    }
    // Primary minor
    if (profile?.minor) tabs.push({ id: 'minor', label: profile.minor, data: minorData, unavailable: unavailable.minor })
    // Additional minors
    extraMinorsList.forEach(({ name, key }) => {
      tabs.push({ id: `extra_minor_${key}`, label: name, data: extraMinorsData[key] || null, unavailable: !extraMinorsData[key], type: 'minor' })
    })
  }
  const currentTab = tabs.find(t => t.id === activeTab) || tabs[0]
  const currentTabData = currentTab?.data
  const currentTabUnavailable = currentTab?.unavailable

  // All programs array and overlap detection
  const allProgramDataArray = useMemo(() => [
    programData, minorData, sciData, coreData, concentrationData,
    ...Object.values(extraMajorsData), ...Object.values(extraMinorsData),
  ].filter(Boolean), [programData, minorData, sciData, coreData, concentrationData, extraMajorsData, extraMinorsData])

  // overlapKeys: course keys that appear in 2+ programs
  const overlapKeys = useMemo(() => {
    const counts = new Map()
    allProgramDataArray.forEach(prog => {
      prog.blocks?.forEach(b => b.courses?.forEach(c => {
        if (!c.catalog) return
        const key = `${c.subject} ${c.catalog}`.toUpperCase()
        counts.set(key, (counts.get(key) || 0) + 1)
      }))
    })
    return new Set([...counts.entries()].filter(([, n]) => n > 1).map(([k]) => k))
  }, [allProgramDataArray])

  const calcRingProgress = (prog) => {
    if (!prog) return { pct: 0, earned: 0, total: prog?.total_credits || 36 }
    const progKey = prog.program_key
    const total = prog.total_credits || 36
    let earned = 0
    const seenDb   = new Set()
    const seenUser = new Set()

    // Phase 1: exact matches (transfer excluded)
    prog.blocks?.forEach(b => b.courses?.forEach(c => {
      if (!c.catalog) return
      const key = `${c.subject} ${c.catalog}`.toUpperCase()
      if (seenDb.has(key)) return
      seenDb.add(key)
      if (matchTransfer(c, advStanding)) return
      if (overlapKeys.has(key) && courseAllocations[key] && courseAllocations[key] !== progKey) return
      const matched = completedCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key) ||
                      currentCourses.some(uc => `${uc.subject} ${uc.catalog}`.toUpperCase() === key)
      if (matched) {
        const uc = [...completedCourses, ...currentCourses].find(u => `${u.subject} ${u.catalog}`.toUpperCase() === key)
        earned += parseFloat(uc?.credits || c.credits || 3)
        seenUser.add(key)
      }
    }))

    // Phase 2: wildcard blocks
    prog.blocks?.forEach(b => {
      const hasWildcard = (b.courses?.some(c => !c.catalog)) || b.min_level
      if (!hasWildcard) return
      const blockSubjects = new Set(b.courses?.map(c => c.subject?.toUpperCase()).filter(Boolean))
      const minLevel = b.min_level || 0
      for (const uc of [...completedCourses, ...currentCourses]) {
        const ucKey = `${uc.subject} ${uc.catalog}`.toUpperCase()
        if (seenDb.has(ucKey) || seenUser.has(ucKey)) continue
        if (!blockSubjects.has(uc.subject?.toUpperCase())) continue
        if (minLevel > 0) { const lvl = parseInt(uc.catalog); if (isNaN(lvl) || lvl < minLevel) continue }
        if (overlapKeys.has(ucKey) && courseAllocations[ucKey] && courseAllocations[ucKey] !== progKey) continue
        earned += parseFloat(uc.credits || 3)
        seenUser.add(ucKey)
      }
    })

    return { pct: Math.min(100, Math.round((earned / total) * 100)), earned, total }
  }

  const majorRing         = calcRingProgress(programData)
  const minorRing         = calcRingProgress(minorData)
  const coreRing          = calcRingProgress(coreData)
  const concentrationRing = calcRingProgress(concentrationData)

  return (
    <div className="dp-req-card">
      <div className="dp-req-card-header">
        <span className="dp-req-card-icon"><FaListAlt /></span>
        <div>
          <h2 className="dp-req-card-title">{t('dp.myProgramRequirements')}</h2>
          <p className="dp-req-card-sub">
            {isMgmt
              ? ['BCom Core', profile?.major, profile?.concentration, ...(profile?.other_majors || []), ...(profile?.other_minors || [])].filter(Boolean).join(' · ')
              : [
                  profile?.major,
                  ...((!isBasc || !bascIsMultiTrack) ? (profile?.other_majors || []) : []),
                  profile?.minor,
                  ...(profile?.other_minors || []),
                ].filter(Boolean).join(' · ')
            }
          </p>
        </div>
      </div>

      {loading && (
        <div className="dp-req-loading"><div className="dp-req-spinner" /> {t('dp.loadingRequirements')}</div>
      )}

      {!loading && !hasAny && !unavailable.major && !unavailable.minor && (
        <div className="dp-req-empty">
          <p>{t('dp.requirementsNotLoaded')}</p>
          <button className="dp-req-seed-btn" onClick={handleSeed} disabled={seeding}>
            <FaBolt /> {seeding ? t('dp.loading') : t('dp.loadRequirements')}
          </button>
        </div>
      )}

      {!loading && !hasAny && (unavailable.major || unavailable.minor) && (
        <div className="dp-req-empty">
          <p style={{ color: 'var(--text-secondary, #6b7280)', fontSize: '0.9rem' }}>
            Detailed requirements for{' '}
            {[
              unavailable.major && profile?.major,
              unavailable.minor && profile?.minor,
            ].filter(Boolean).join(' and ')}{' '}
            are not yet available. We're working on adding more programs!
          </p>
          <p style={{ color: 'var(--text-tertiary, #9ca3af)', fontSize: '0.8rem', marginTop: '0.25rem' }}>
            {t('dp.browseDegreeReqs')}
          </p>
        </div>
      )}

      {!loading && hasAny && (
        <div className="dp-req-body">

          {/* Progress rings */}
          <div className="dp-req-progress-row">
            {isMgmt ? (
              <>
                {hasCore && (
                  <div className="dp-req-progress-item">
                    <div className="dp-req-ring">
                      <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                        <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                        <circle cx="18" cy="18" r="15.9"
                          className="dp-req-ring-fill dp-req-ring-fill--minor"
                          strokeDasharray={`${coreRing.pct} ${100 - coreRing.pct}`}
                          strokeDashoffset="25"
                        />
                      </svg>
                      <span className="dp-req-ring-label">{coreRing.pct}%</span>
                    </div>
                    <div className="dp-req-prog-text">
                      <span className="dp-req-prog-name">{t('dp.ringCore')}</span>
                      <span className="dp-req-prog-detail">{coreRing.earned}/{coreRing.total} {t('dp.credits')}</span>
                    </div>
                  </div>
                )}
                {hasMajor && (
                  <div className="dp-req-progress-item">
                    <div className="dp-req-ring">
                      <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                        <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                        <circle cx="18" cy="18" r="15.9"
                          className="dp-req-ring-fill dp-req-ring-fill--major"
                          strokeDasharray={`${majorRing.pct} ${100 - majorRing.pct}`}
                          strokeDashoffset="25"
                        />
                      </svg>
                      <span className="dp-req-ring-label">{majorRing.pct}%</span>
                    </div>
                    <div className="dp-req-prog-text">
                      <span className="dp-req-prog-name">{t('dp.ringMajor')}</span>
                      <span className="dp-req-prog-detail">{majorRing.earned}/{majorRing.total} {t('dp.credits')}</span>
                    </div>
                  </div>
                )}
                {hasConcentration && (
                  <div className="dp-req-progress-item">
                    <div className="dp-req-ring">
                      <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                        <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                        <circle cx="18" cy="18" r="15.9"
                          className="dp-req-ring-fill" style={{ stroke: '#7c3aed' }}
                          strokeDasharray={`${concentrationRing.pct} ${100 - concentrationRing.pct}`}
                          strokeDashoffset="25"
                        />
                      </svg>
                      <span className="dp-req-ring-label">{concentrationRing.pct}%</span>
                    </div>
                    <div className="dp-req-prog-text">
                      <span className="dp-req-prog-name">{t('dp.ringConcentration')}</span>
                      <span className="dp-req-prog-detail">{concentrationRing.earned}/{concentrationRing.total} {t('dp.credits')}</span>
                    </div>
                  </div>
                )}
              </>
            ) : (
              <>
                {hasMajor && (
                  <div className="dp-req-progress-item">
                    <div className="dp-req-ring">
                      <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                        <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                        <circle cx="18" cy="18" r="15.9"
                          className="dp-req-ring-fill dp-req-ring-fill--major"
                          strokeDasharray={`${majorRing.pct} ${100 - majorRing.pct}`}
                          strokeDashoffset="25"
                        />
                      </svg>
                      <span className="dp-req-ring-label">{majorRing.pct}%</span>
                    </div>
                    <div className="dp-req-prog-text">
                      <span className="dp-req-prog-name">{profile?.major || t('dp.ringMajor')}</span>
                      <span className="dp-req-prog-detail">{majorRing.earned}/{majorRing.total} {t('dp.credits')}</span>
                    </div>
                  </div>
                )}
                {/* Extra majors rings */}
                {extraMajorsList.map(({ name, key }) => {
                  const data = extraMajorsData[key]
                  if (!data) return null
                  const ring = calcRingProgress(data)
                  return (
                    <div key={key} className="dp-req-progress-item">
                      <div className="dp-req-ring">
                        <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                          <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                          <circle cx="18" cy="18" r="15.9"
                            className="dp-req-ring-fill dp-req-ring-fill--major"
                            strokeDasharray={`${ring.pct} ${100 - ring.pct}`}
                            strokeDashoffset="25"
                          />
                        </svg>
                        <span className="dp-req-ring-label">{ring.pct}%</span>
                      </div>
                      <div className="dp-req-prog-text">
                        <span className="dp-req-prog-name">{name}</span>
                        <span className="dp-req-prog-detail">{ring.earned}/{ring.total} {t('dp.credits')}</span>
                      </div>
                    </div>
                  )
                })}
                {hasMinor && (
                  <div className="dp-req-progress-item">
                    <div className="dp-req-ring">
                      <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                        <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                        <circle cx="18" cy="18" r="15.9"
                          className="dp-req-ring-fill dp-req-ring-fill--minor"
                          strokeDasharray={`${minorRing.pct} ${100 - minorRing.pct}`}
                          strokeDashoffset="25"
                        />
                      </svg>
                      <span className="dp-req-ring-label">{minorRing.pct}%</span>
                    </div>
                    <div className="dp-req-prog-text">
                      <span className="dp-req-prog-name">{profile?.minor || t('dp.ringMinor')}</span>
                      <span className="dp-req-prog-detail">{minorRing.earned}/{minorRing.total} {t('dp.credits')}</span>
                    </div>
                  </div>
                )}
                {/* Extra minors rings */}
                {extraMinorsList.map(({ name, key }) => {
                  const data = extraMinorsData[key]
                  if (!data) return null
                  const ring = calcRingProgress(data)
                  return (
                    <div key={key} className="dp-req-progress-item">
                      <div className="dp-req-ring">
                        <svg viewBox="0 0 36 36" className="dp-req-ring-svg">
                          <circle cx="18" cy="18" r="15.9" className="dp-req-ring-bg" />
                          <circle cx="18" cy="18" r="15.9"
                            className="dp-req-ring-fill dp-req-ring-fill--minor"
                            strokeDasharray={`${ring.pct} ${100 - ring.pct}`}
                            strokeDashoffset="25"
                          />
                        </svg>
                        <span className="dp-req-ring-label">{ring.pct}%</span>
                      </div>
                      <div className="dp-req-prog-text">
                        <span className="dp-req-prog-name">{name}</span>
                        <span className="dp-req-prog-detail">{ring.earned}/{ring.total} {t('dp.credits')}</span>
                      </div>
                    </div>
                  )
                })}
              </>
            )}
          </div>

          {/* Tab switcher */}
          <div className="dp-prog-tabs">
            {tabs.map(tab => (
              <button
                key={tab.id}
                className={`dp-prog-tab ${activeTab === tab.id ? 'dp-prog-tab--active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.id === 'core'
                  ? t('dp.tabCore').replace('{label}', tab.label)
                  : tab.id === 'concentration'
                  ? t('dp.tabConcentration').replace('{label}', tab.label)
                  : tab.id === 'sci'
                  ? t('dp.tabScience').replace('{label}', tab.label)
                  : tab.id === 'minor' || tab.id.startsWith('extra_minor_')
                  ? t('dp.tabMinor').replace('{label}', tab.label)
                  : t('dp.tabMajor').replace('{label}', tab.label)
                }
                {tab.unavailable && !tab.data && (
                  <span style={{ fontSize: '0.7rem', opacity: 0.6, marginLeft: '0.25rem' }}>{t('dp.na')}</span>
                )}
              </button>
            ))}
            <button
              className={`dp-prog-tab ${activeTab === 'electives' ? 'dp-prog-tab--active dp-prog-tab--electives' : ''}`}
              onClick={() => setActiveTab('electives')}
            >
              ✦ Electives
            </button>
          </div>

          {/* Foundation year waived banner */}
          {foundationWaived && (
            <div className="drv-foundation-waived-banner">
              <span>✓</span>
              <span>
                <strong style={{ color: 'var(--text-primary)' }}>{t('dp.foundationWaived')}</strong> — {t('dp.foundationWaivedDesc').replace('{count}', transferCredits)}
                {transferCredits < 30 ? t('dp.foundationWaivedNote') : ''}.
              </span>
            </div>
          )}

          {/* Active program blocks */}
          {activeTab !== 'electives' && currentTabData && (
            <ProgramSection
              prog={currentTabData}
              completedCourses={completedCourses}
              currentCourses={currentCourses}
              advStanding={advStanding}
              openBlocks={openBlocks}
              setOpenBlocks={setOpenBlocks}
              courseAllocations={courseAllocations}
              assignCourse={assignCourse}
              overlapKeys={overlapKeys}
              allProgramData={allProgramDataArray}
            />
          )}

          {/* Unavailable tab message */}
          {activeTab !== 'electives' && !currentTabData && currentTabUnavailable && (
            <div className="dp-req-empty" style={{ padding: '1.5rem', textAlign: 'center' }}>
              <p style={{ color: 'var(--text-secondary, #6b7280)', fontSize: '0.9rem', margin: 0 }}>
                {t('dp.notAvailableShort').replace('{program}', currentTab?.label ?? '')}
              </p>
              <p style={{ color: 'var(--text-tertiary, #9ca3af)', fontSize: '0.8rem', marginTop: '0.5rem' }}>
                {t('dp.checkDegreeReqs')}
              </p>
            </div>
          )}

          {/* Electives tab — always mounted to preserve state, hidden when inactive */}
          <div style={{ display: activeTab === 'electives' ? 'block' : 'none' }}>
            <ElectivesPanel
              profile={profile}
              completedCourses={completedCourses}
              currentCourses={currentCourses}
              programData={programData}
              minorData={minorData}
              allProgramData={allProgramDataArray}
              courseAllocations={courseAllocations}
              assignCourse={assignCourse}
            />
          </div>
        </div>
      )}
    </div>
  )
}

// ── Main component ─────────────────────────────────────────────────────────────
export default function DegreePlanningView({
  favorites = [],
  completedCourses = [],
  currentCourses = [],
  completedCoursesMap = new Set(),
  currentCoursesMap = new Set(),
  favoritesMap = new Set(),
  profile = {},
  onToggleFavorite,
  onToggleCompleted,
  onToggleCurrent,
  onCourseClick,
  onImportTranscript,
  onImportSyllabus,
  authFlags,
}) {
  const { t } = useLanguage()
  const [subTab, setSubTab] = useState('my_courses')

  const isCompleted = (s, c) => completedCoursesMap.has(`${s} ${c}`)
  const isCurrent   = (s, c) => currentCoursesMap.has(`${s} ${c}`)
  const isFavorited = (s, c) => favoritesMap.has(`${s}${c}`)

  return (
    <div className="dp-view">

      {/* ── Sub-tabs ──────────────────────────────────────── */}
      <div className="dp-subtab-bar">
        <button
          className={`dp-subtab-btn ${subTab === 'my_courses' ? 'dp-subtab-btn--active' : ''}`}
          onClick={() => setSubTab('my_courses')}
        >
          <FaGraduationCap className="dp-subtab-icon" />
          <span>{t('dp.myDegree')}</span>
          {(favorites.length + completedCourses.length + currentCourses.length) > 0 && (
            <span className="dp-subtab-count">
              {favorites.length + completedCourses.length + currentCourses.length}
            </span>
          )}
        </button>
        <button
          className={`dp-subtab-btn ${subTab === 'requirements' ? 'dp-subtab-btn--active' : ''}`}
          onClick={() => setSubTab('requirements')}
        >
          <FaListAlt className="dp-subtab-icon" />
          <span>{t('dp.degreeRequirements')}</span>
        </button>
        <button
          className={`dp-subtab-btn ${subTab === 'study_abroad' ? 'dp-subtab-btn--active' : ''}`}
          onClick={() => setSubTab('study_abroad')}
        >
          <FaPlane className="dp-subtab-icon" />
          <span>{t('dp.studyAbroad')}</span>
        </button>
        <button
          className={`dp-subtab-btn ${subTab === 'advising' ? 'dp-subtab-btn--active' : ''}`}
          onClick={() => setSubTab('advising')}
        >
          <FaInfoCircle className="dp-subtab-icon" />
          <span>{t('dp.advisingResources')}</span>
        </button>
      </div>

      {/* ── Degree Requirements tab ───────────────────────── */}
      {subTab === 'requirements' && (
        <div className="dp-req-tab-wrap">
          <DegreeRequirementsView
            completedCourses={completedCourses}
            currentCourses={currentCourses}
            profile={profile}
          />
        </div>
      )}

      {/* ── Study Abroad tab ──────────────────────────────── */}
      {subTab === 'study_abroad' && (
        <div className="dp-sa-tab-wrap">
          <StudyAbroadView profile={profile} />
        </div>
      )}

      {/* ── Advising Resources tab ────────────────────────── */}
      {subTab === 'advising' && (
        <div className="dp-sa-tab-wrap">
          <AdvisingResourcesView profile={profile} />
        </div>
      )}

      {/* ── My Degree tab ─────────────────────────────────── */}
      {subTab === 'my_courses' && (
        <>
          {/* Degree Progress */}
          <div className="dp-section-card">
            <div className="dp-section-header">
              <span className="dp-section-icon"><FaBullseye /></span>
              <h2 className="dp-section-title">{t('profile.degreeProgress')}</h2>
              <div className="dp-import-btns">
                {onImportTranscript && (
                  <button className="dp-import-btn" onClick={onImportTranscript}>
                    <FaFileUpload /> {t('dp.transcript')}
                  </button>
                )}
                {onImportSyllabus && (
                  <button className="dp-import-btn dp-import-btn--secondary" onClick={onImportSyllabus}>
                    <FaBook /> {t('dp.syllabuses')}
                  </button>
                )}
              </div>
            </div>
            <DegreeProgressTracker completedCourses={completedCourses} profile={profile} />
          </div>

          {/* My Program Requirements card */}
          <MyProgramCard
            profile={profile}
            completedCourses={completedCourses}
            currentCourses={currentCourses}
          />
        </>
      )}
    </div>
  )
}
