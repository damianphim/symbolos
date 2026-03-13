import { useState, useEffect, useMemo } from 'react'
import { useLanguage } from '../../contexts/LanguageContext'
import { supabase } from '../../lib/supabase'
import {
  FaGraduationCap, FaChevronDown, FaChevronUp, FaChevronRight,
  FaCheckCircle, FaCircle, FaStar, FaSearch,
  FaLightbulb, FaExternalLinkAlt, FaTimes
} from 'react-icons/fa'
import './DegreeRequirementsView.css'

// Fix double /api/api bug — strip trailing /api from env var
const rawBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const API_BASE = rawBase.replace(/\/api\/?$/, '')

/** Returns Authorization header object with the current Supabase Bearer token. */
async function getAuthHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  if (!session?.access_token) return {}
  return { Authorization: `Bearer ${session.access_token}` }
}

const TYPE_LABELS = {
  major:         'Major',
  minor:         'Minor',
  honours:       'Honours',
  joint_honours: 'Joint Honours',
  beng:          'B.Eng.',
  bge:           'B.G.E.',
  bscarch:       'B.Sc.(Arch.)',
  concentration: 'Concentration',
  core:          'Core',
  required:      'Core',
  diploma:       'Diploma',
}
const TYPE_COLORS = {
  major:         '#dc2626',
  minor:         '#ca8a04',
  honours:       '#2563eb',
  joint_honours: '#0f766e',
  beng:          '#dc2626',
  bge:           '#0891b2',
  bscarch:       '#d97706',
  concentration: '#7c3aed',
  core:          '#0f766e',
  required:      '#0f766e',
  diploma:       '#059669',
}
const TYPE_BG = {
  major:         '#fef2f2',
  minor:         '#fefce8',
  honours:       '#eff6ff',
  joint_honours: '#f0fdfa',
  beng:          '#fef2f2',
  bge:           '#ecfeff',
  bscarch:       '#fffbeb',
  concentration: '#faf5ff',
  core:          '#f0fdfa',
  required:      '#f0fdfa',
  diploma:       '#ecfdf5',
}

// Normalize short faculty names (as stored in profile) to full faculty strings
const FACULTY_MAP = {
  'Arts':                        'Faculty of Arts',
  'Science':                     'Faculty of Science',
  'Engineering':                 'Faculty of Engineering',
  'Agriculture':                 'Faculty of Agricultural and Environmental Sciences',
  'Education':                   'Faculty of Education',
  'Law':                         'Faculty of Law',
  'Management':                  'Desautels Faculty of Management',
  'Medicine':                    'Faculty of Medicine and Health Sciences',
  'Music':                       'Schulich School of Music',
  'Nursing':                     'Ingram School of Nursing',
  'Bachelor of Arts and Science': 'Faculty of Arts & Science',
}

function normalizeFaculty(f) {
  return FACULTY_MAP[f] || f || ''
}

function matchCourse(req, userCourses) {
  if (!req.catalog) return null
  const key = `${req.subject} ${req.catalog}`.toUpperCase()
  return userCourses.find(c => {
    const cKey = `${c.subject || ''} ${c.catalog || ''}`.toUpperCase()
    return cKey === key
  }) || null
}

function normalizeCode(code) {
  return (code || '').toUpperCase()
    .replace(/([A-Z])(\d)/g, '$1 $2')  // COMP202 → COMP 202
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

export default function DegreeRequirementsView({ completedCourses = [], currentCourses = [], profile = {} }) {
  const { t, language } = useLanguage()
  const [programs, setPrograms]           = useState([])
  const [selectedKey, setSelectedKey]     = useState(null)
  const [programDetail, setProgramDetail] = useState(null)
  const [loading, setLoading]             = useState(false)
  const [seeding, setSeeding]             = useState(false)
  const [seedDone, setSeedDone]           = useState(false)
  const [error, setError]                 = useState(null)
  const [detailError, setDetailError]     = useState(null)
  const [search, setSearch]               = useState('')
  const [typeFilter, setTypeFilter]       = useState('all')
  const [openBlocks, setOpenBlocks]       = useState({})
  const [showAllCourses, setShowAllCourses] = useState({})
  const [showRecommended, setShowRecommended] = useState(false)
  const [sidebarOpen, setSidebarOpen]     = useState(true)
  const [facultyFilter, setFacultyFilter] = useState(normalizeFaculty(profile?.faculty))

  const advStanding = profile?.advanced_standing || []
  const transferCredits = advStanding.reduce((s, c) => s + (c.credits || 0), 0)
  const foundationWaived = transferCredits >= 24 &&
    (profile?.faculty === 'Faculty of Arts' || profile?.faculty === 'Bachelor of Arts and Science')
  const [collapsedGroups, setCollapsedGroups] = useState({})
  const toggleGroup = (key) => setCollapsedGroups(prev => ({ ...prev, [key]: !prev[key] }))

  const allUserCourses = useMemo(
    () => [...completedCourses, ...currentCourses],
    [completedCourses, currentCourses]
  )

  // Sync faculty filter when profile loads/changes (only if user hasn't manually changed it)
  useEffect(() => {
    if (profile?.faculty) {
      setFacultyFilter(normalizeFaculty(profile.faculty))
    }
  }, [profile?.faculty])

  useEffect(() => {
    const isBaScFilter = facultyFilter === 'Faculty of Arts & Science'
    if (isBaScFilter) {
      // B.A. & Sc.: fetch interfaculty + all Arts + all Science programs
      getAuthHeaders().then(headers =>
        Promise.all([
          fetch(`${API_BASE}/api/degree-requirements/programs?faculty=${encodeURIComponent('Faculty of Arts & Science')}`, { headers }).then(r => r.json()),
          fetch(`${API_BASE}/api/degree-requirements/programs?faculty=${encodeURIComponent('Faculty of Arts')}`, { headers }).then(r => r.json()),
          fetch(`${API_BASE}/api/degree-requirements/programs?faculty=${encodeURIComponent('Faculty of Science')}`, { headers }).then(r => r.json()),
        ])
      )
        .then(([basc, arts, sci]) => {
          const all = [
            ...(Array.isArray(basc) ? basc : []),
            ...(Array.isArray(arts) ? arts : []),
            ...(Array.isArray(sci)  ? sci  : []),
          ]
          setPrograms(all)
        })
        .catch(() => setError('Could not load programs. Try loading requirements first.'))
    } else {
      const fParam = facultyFilter ? `?faculty=${encodeURIComponent(facultyFilter)}` : ''
      getAuthHeaders().then(headers =>
        fetch(`${API_BASE}/api/degree-requirements/programs${fParam}`, { headers })
          .then(r => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`)
            return r.json()
          })
          .then(data => { if (Array.isArray(data)) setPrograms(data) })
          .catch(() => setError('Could not load programs. Try loading requirements first.'))
      )
    }
  }, [seedDone, facultyFilter])

  useEffect(() => {
    if (!selectedKey) return
    setLoading(true)
    setProgramDetail(null)
    setOpenBlocks({})
    setShowAllCourses({})
    setDetailError(null)
    getAuthHeaders().then(headers =>
      fetch(`${API_BASE}/api/degree-requirements/programs/${selectedKey}`, { headers })
        .then(r => {
          if (r.status === 404) {
            setDetailError('not_found')
            return null
          }
          if (!r.ok) {
            setDetailError('error')
            return null
          }
          return r.json()
        })
        .then(data => {
          if (data) {
            setProgramDetail(data)
            const initial = {}
            data.blocks?.forEach((b, i) => { if (i < 2) initial[b.id] = true })
            setOpenBlocks(initial)
          }
        })
        .catch(() => setDetailError('error'))
        .finally(() => setLoading(false))
    )
  }, [selectedKey])

  const handleSeed = async () => {
    setSeeding(true)
    setError(null)
    try {
      // Map faculty filter to seed param
      const seedFacultyMap = {
        'Faculty of Arts':                  'arts',
        'Faculty of Science':               'science',
        'Faculty of Arts & Science':        'arts_science',
        'Faculty of Engineering':           'engineering',
        'Desautels Faculty of Management':  'management',
        'Faculty of Agricultural and Environmental Sciences': 'aes',
        'Faculty of Dental Medicine and Oral Health Sciences': 'dentistry',
        'Faculty of Medicine and Health Sciences': 'medicine',
        'Schulich School of Music': 'music',
        'Ingram School of Nursing': 'nursing',
        'School of Physical and Occupational Therapy': 'spot',
      }
      const seedParam = seedFacultyMap[facultyFilter] || null

      // Check if programs already exist for THIS faculty
      const checkUrl = facultyFilter
        ? `${API_BASE}/api/degree-requirements/programs?faculty=${encodeURIComponent(facultyFilter)}`
        : `${API_BASE}/api/degree-requirements/programs`
      const headers = await getAuthHeaders()
      const checkRes = await fetch(checkUrl, { headers })
      if (checkRes.ok) {
        const existing = await checkRes.json()
        if (Array.isArray(existing) && existing.length > 0) {
          setSeedDone(v => !v)
          return
        }
      }

      // Seed for the specific faculty
      const seedUrl = seedParam
        ? `${API_BASE}/api/degree-requirements/seed?faculty=${seedParam}`
        : `${API_BASE}/api/degree-requirements/seed`
      const res = await fetch(seedUrl, { method: 'POST', headers })
      const data = await res.json()
      if (data.success) setSeedDone(v => !v)
      else setError('Load failed: ' + JSON.stringify(data.detail || data))
    } catch {
      setError('Load request failed. Is the backend running?')
    } finally {
      setSeeding(false)
    }
  }

  const filteredPrograms = useMemo(() => programs.filter(p => {
    const matchSearch = p.name.toLowerCase().includes(search.toLowerCase())
    const matchType   = typeFilter === 'all' || p.program_type === typeFilter
    return matchSearch && matchType
  }), [programs, search, typeFilter])

  const progress = useMemo(() => {
    if (!programDetail) return null
    let required = 0, completed = 0
    programDetail.blocks?.forEach(block => {
      block.courses?.forEach(c => {
        if (c.is_required) {
          required += parseFloat(c.credits || 3)
          const transferCountsMajor = matchTransfer(c, advStanding, { requireMajorCredit: true })
          if (transferCountsMajor || (!matchTransfer(c, advStanding) && matchCourse(c, allUserCourses)))
            completed += parseFloat(c.credits || 3)
        }
      })
    })
    return { required, completed, pct: required > 0 ? Math.round((completed / required) * 100) : 0 }
  }, [programDetail, allUserCourses, advStanding])

  const toggleBlock   = id => setOpenBlocks(p => ({ ...p, [id]: !p[id] }))
  const toggleShowAll = id => setShowAllCourses(p => ({ ...p, [id]: !p[id] }))

  return (
    <div className="drv-root">

      {/* Sidebar */}
      <aside className={`drv-sidebar ${sidebarOpen ? 'drv-sidebar--open' : ''}`}>
        <div className="drv-sidebar-header">
          <FaGraduationCap className="drv-sidebar-icon" />
          <span>Programs</span>
          <button className="drv-sidebar-close" onClick={() => setSidebarOpen(false)}><FaTimes /></button>
        </div>

        <div className="drv-faculty-select-wrap">
          <select
            className="drv-faculty-select"
            value={facultyFilter}
            onChange={e => { setFacultyFilter(e.target.value); setSelectedKey(null); setProgramDetail(null); setDetailError(null); setTypeFilter('all') }}
          >
            <option value="">All Faculties</option>
            <option value="Faculty of Agricultural and Environmental Sciences">Agricultural &amp; Environmental Sciences</option>
            <option value="Faculty of Arts">Faculty of Arts</option>
            <option value="Faculty of Arts &amp; Science">Bachelor of Arts &amp; Science</option>
            <option value="Faculty of Dental Medicine and Oral Health Sciences">Dental Medicine &amp; Oral Health Sciences</option>
            <option value="Faculty of Education">Faculty of Education</option>
            <option value="Faculty of Engineering">Faculty of Engineering</option>
            <option value="School of Environment">Environment</option>
            <option value="Faculty of Law">Faculty of Law</option>
            <option value="Desautels Faculty of Management">Management (Desautels)</option>
            <option value="Faculty of Medicine and Health Sciences">Medicine &amp; Health Sciences</option>
            <option value="Schulich School of Music">Schulich School of Music</option>
            <option value="Ingram School of Nursing">Nursing</option>
            <option value="School of Physical and Occupational Therapy">Physical &amp; Occupational Therapy</option>
            <option value="Faculty of Science">Faculty of Science</option>
          </select>
        </div>

        <div className="drv-sidebar-search">
          <FaSearch className="drv-search-icon" />
          <input
            value={search}
            onChange={e => setSearch(e.target.value)}
            placeholder="Search programs…"
            className="drv-search-input"
          />
        </div>

        <div className="drv-type-filters">
          {(
            facultyFilter.toLowerCase().includes('engineering')
              ? ['all', 'beng', 'bge', 'bscarch', 'minor']
              : facultyFilter.toLowerCase().includes('management') || facultyFilter.toLowerCase().includes('desautels')
                ? ['all', 'core', 'major', 'concentration', 'honours']
                : facultyFilter === 'School of Environment'
                  ? ['all', 'major', 'minor', 'diploma']
                  : facultyFilter === 'Faculty of Law'
                  ? ['all', 'major']
                  : facultyFilter === 'Faculty of Agricultural and Environmental Sciences'
                  ? ['all', 'major', 'honours', 'beng', 'minor', 'diploma']
                  : facultyFilter === 'Faculty of Dental Medicine and Oral Health Sciences'
                  ? ['all', 'major', 'diploma']
                  : facultyFilter === 'Faculty of Medicine and Health Sciences'
                  ? ['all', 'major', 'diploma']
                  : facultyFilter === 'Schulich School of Music'
                  ? ['all', 'major', 'minor']
                  : facultyFilter === 'Ingram School of Nursing'
                  ? ['all', 'major']
                  : facultyFilter === 'School of Physical and Occupational Therapy'
                  ? ['all', 'major']
                  : ['all', 'major', 'minor', 'honours']
          ).map(t => {
            const isActive = typeFilter === t
            const color = TYPE_COLORS[t]
            const bg    = TYPE_BG[t]
            return (
              <button
                key={t}
                className={`drv-type-chip ${isActive ? 'drv-type-chip--active' : ''}`}
                onClick={() => setTypeFilter(t)}
                style={t !== 'all' ? {
                  borderColor: isActive ? color : `${color}55`,
                  background:  isActive ? color : (typeFilter === 'all' ? bg : 'transparent'),
                  color:       isActive ? '#fff' : color,
                } : {}}
              >
                {t !== 'all' && (
                  <span style={{
                    display: 'inline-block', width: 7, height: 7, borderRadius: '50%',
                    background: isActive ? '#ffffff99' : color,
                    marginRight: 5, verticalAlign: 'middle',
                  }} />
                )}
                {t === 'all' ? 'All' : (TYPE_LABELS[t] || t)}
              </button>
            )
          })}
        </div>

        {programs.length === 0 && (
          <button className="drv-seed-btn" onClick={handleSeed} disabled={seeding}>
            {seeding ? 'Loading…' : `Load ${facultyFilter ? facultyFilter.replace('Faculty of ', '') : 'All'} Requirements`}
          </button>
        )}

        <div className="drv-program-list">
          {filteredPrograms.length === 0 && programs.length > 0 && (
            <div className="drv-empty-search">No programs match.</div>
          )}
          {facultyFilter === 'Faculty of Arts & Science' ? (
            (() => {
              const groups = [
                { label: 'Interfaculty Programs', faculty: 'Faculty of Arts & Science' },
                { label: 'Arts Concentrations',   faculty: 'Faculty of Arts' },
                { label: 'Science Concentrations', faculty: 'Faculty of Science' },
              ]
              return groups.map(({ label, faculty }) => {
                const groupProgs = filteredPrograms.filter(p => p.faculty === faculty)
                if (groupProgs.length === 0) return null
                const isCollapsed = !!collapsedGroups[faculty]
                return (
                  <div key={faculty}>
                    <button
                      onClick={() => toggleGroup(faculty)}
                      style={{
                        width: '100%', background: 'none', border: 'none', cursor: 'pointer',
                        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                        padding: '10px 12px 6px', gap: '6px',
                      }}
                    >
                      <span style={{ fontSize: '10px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.08em', color: '#6b7280' }}>{label}</span>
                      <span style={{ fontSize: '10px', color: '#9ca3af', transform: isCollapsed ? 'rotate(-90deg)' : 'rotate(0deg)', transition: 'transform 0.2s', display: 'inline-block' }}>▾</span>
                    </button>
                    {!isCollapsed && groupProgs.map(prog => (
                      <button
                        key={prog.program_key}
                        className={`drv-program-item ${selectedKey === prog.program_key ? 'drv-program-item--active' : ''}`}
                        onClick={() => { setSelectedKey(prog.program_key); setDetailError(null); if (window.innerWidth < 760) setSidebarOpen(false) }}
                      >
                        <span className="drv-type-dot" style={{ background: TYPE_COLORS[prog.program_type] }} />
                        <span className="drv-program-name">{prog.name}</span>
                        <span className="drv-program-credits">{prog.total_credits}cr</span>
                      </button>
                    ))}
                  </div>
                )
              })
            })()
          ) : (
            filteredPrograms.map(prog => (
              <button
                key={prog.program_key}
                className={`drv-program-item ${selectedKey === prog.program_key ? 'drv-program-item--active' : ''}`}
                onClick={() => { setSelectedKey(prog.program_key); setDetailError(null); if (window.innerWidth < 760) setSidebarOpen(false) }}
              >
                <span className="drv-type-dot" style={{ background: TYPE_COLORS[prog.program_type] }} />
                <span className="drv-program-name">{prog.name}</span>
                <span className="drv-program-credits">{prog.total_credits}cr</span>
              </button>
            ))
          )}
        </div>
      </aside>

      {/* Main */}
      <main className="drv-main">
        <button className="drv-open-sidebar" onClick={() => setSidebarOpen(true)}>
          ☰ Browse Programs
        </button>

        {error && (
          <div className="drv-error">
            {error}
            {programs.length === 0 && (
              <button className="drv-seed-btn drv-seed-btn--inline" onClick={handleSeed} disabled={seeding}>
                {seeding ? 'Loading…' : `Load ${facultyFilter ? facultyFilter.replace('Faculty of ', '') : 'All'} Requirements`}
              </button>
            )}
          </div>
        )}

        {!selectedKey && !loading && (
          <div className="drv-welcome">
            <div className="drv-welcome-icon-wrap"><FaGraduationCap /></div>
            <h2>{t('dp.welcomeTitle')}</h2>
            <p>{t('dp.welcomeDesc')}</p>
            {programs.length > 0 && (
              <p className="drv-welcome-count">
                {programs.length === 1
                  ? t('dp.programAvailable').replace('{count}', programs.length)
                  : t('dp.programsAvailable').replace('{count}', programs.length)}
              </p>
            )}
            {programs.length === 0 && (
              <button className="drv-seed-btn" onClick={handleSeed} disabled={seeding}>
                {seeding ? t('dp.loading') : t('dp.loadBtn')}
              </button>
            )}
          </div>
        )}

        {loading && (
          <div className="drv-loading">
            <div className="drv-spinner" />
            <span>{t('dp.loadingSpinner')}</span>
          </div>
        )}

        {!loading && selectedKey && detailError === 'not_found' && !programDetail && (
          <div className="drv-welcome">
            <div className="drv-welcome-icon-wrap" style={{ opacity: 0.5 }}><FaGraduationCap /></div>
            <h2>{t('dp.notFoundTitle')}</h2>
            <p style={{ color: 'var(--text-secondary, #6b7280)' }}>
              {t('dp.notFoundDesc')}
            </p>
            <p style={{ color: 'var(--text-tertiary, #9ca3af)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
              {t('dp.notFoundHint')}
            </p>
          </div>
        )}

        {!loading && selectedKey && detailError === 'error' && !programDetail && (
          <div className="drv-error">
            {t('dp.loadError')}
          </div>
        )}

        {/* Foundation year waived banner */}
        {foundationWaived && selectedKey && (
          <div className="drv-foundation-waived-banner">
            <span>✓</span>
            <span>
              <strong style={{ color: 'var(--text-primary)' }}>{t('dp.foundationWaived')}</strong> — {t('dp.foundationWaivedDesc').replace('{count}', transferCredits)}
              {transferCredits < 30 ? ` ${t('dp.foundationWaivedNote')}` : ''}.
            </span>
          </div>
        )}

        {programDetail && !loading && (
          <div className="drv-detail">
            <div className="drv-detail-header">
              <div className="drv-detail-header-left">
                <span
                  className="drv-detail-type-badge"
                  style={{
                    background: TYPE_BG[programDetail.program_type],
                    color: TYPE_COLORS[programDetail.program_type],
                    border: `1px solid ${TYPE_COLORS[programDetail.program_type]}33`
                  }}
                >
                  {TYPE_LABELS[programDetail.program_type]}
                </span>
                <h1 className="drv-detail-title">{programDetail.name}</h1>
                {programDetail.description && (
                  <p className="drv-detail-desc">{programDetail.description}</p>
                )}
              </div>
              <div className="drv-detail-meta">
                <div className="drv-meta-card">
                  <span className="drv-meta-label">{language === 'zh' ? '学分：' : language === 'fr' ? 'Crédits :' : 'Credits:'}</span>
                  <span className="drv-meta-val">{programDetail.total_credits}</span>
                </div>
                {progress && progress.required > 0 && (
                  <div className="drv-meta-card drv-meta-card--green">
                    <span className="drv-meta-label">{language === 'zh' ? '已完成必修：' : language === 'fr' ? 'Requis complété :' : 'Required done:'}</span>
                    <span className="drv-meta-val">{progress.pct}%</span>
                  </div>
                )}
                {programDetail.ecalendar_url && (
                  <a
                    href={language === 'fr'
                      ? programDetail.ecalendar_url.replace('/en/', '/fr/')
                      : programDetail.ecalendar_url}
                    target="_blank"
                    rel="noreferrer"
                    className="drv-ecal-link"
                  >
                    {language === 'zh' ? 'eCalendar' : language === 'fr' ? 'eCalendrier' : 'eCalendar'} <FaExternalLinkAlt />
                  </a>
                )}
              </div>
            </div>

            {progress && progress.required > 0 && (
              <div className="drv-progress-wrap">
                <div className="drv-progress-track">
                  <div className="drv-progress-fill" style={{ width: `${progress.pct}%` }} />
                </div>
                <span className="drv-progress-label">
                  {progress.completed}/{progress.required} required credits completed
                </span>
              </div>
            )}

            <div className="drv-controls">
              <button
                className={`drv-rec-toggle ${showRecommended ? 'drv-rec-toggle--active' : ''}`}
                onClick={() => setShowRecommended(v => !v)}
              >
                <FaLightbulb /> {showRecommended ? 'All Courses' : 'Recommended Only'}
              </button>
            </div>

            <div className="drv-blocks">
              {programDetail.blocks?.map(block => {
                const isOpen  = openBlocks[block.id]
                const showAll = showAllCourses[block.id]
                const courses = showRecommended
                  ? block.courses?.filter(c => c.recommended)
                  : block.courses

                const PREVIEW = 5
                const visible      = showAll ? courses : courses?.slice(0, PREVIEW)
                const required     = block.courses?.filter(c => c.is_required) || []
                const completedReq = required.filter(c =>
                  matchTransfer(c, advStanding) || matchCourse(c, allUserCourses)
                )
                const blockDone    = required.length > 0 && completedReq.length === required.length

                return (
                  <div key={block.id} className={`drv-block ${blockDone ? 'drv-block--done' : ''}`}>
                    <button className="drv-block-header" onClick={() => toggleBlock(block.id)}>
                      <div className="drv-block-header-left">
                        <span className="drv-chevron">
                          {isOpen ? <FaChevronDown /> : <FaChevronRight />}
                        </span>
                        <div>
                          <span className="drv-block-title">{block.title}</span>
                          {block.credits_needed && (
                            <span className="drv-block-credits"> · {block.credits_needed}cr needed</span>
                          )}
                        </div>
                      </div>
                      <div className="drv-block-header-right">
                        {required.length > 0 && (
                          <span className={`drv-block-pill ${blockDone ? 'drv-block-pill--done' : ''}`}>
                            {blockDone ? '✓ Complete' : `${completedReq.length}/${required.length} req`}
                          </span>
                        )}
                        <span className="drv-block-count">{block.courses?.length}</span>
                      </div>
                    </button>

                    {isOpen && (
                      <div className="drv-block-body">
                        {(block.notes || block.min_level || block.max_credits_200 || block.min_credits_400) && (
                          <div className="drv-block-info">
                            {block.notes && <span>{block.notes}</span>}
                            {block.min_level && <span>Min level: {block.min_level}+</span>}
                            {block.max_credits_200 && <span>Max {block.max_credits_200}cr at 200-level</span>}
                            {block.min_credits_400 && <span>Min {block.min_credits_400}cr at 400/500-level</span>}
                          </div>
                        )}

                        <div className="drv-course-list">
                          {visible?.map(course => {
                            const isTransfer = matchTransfer(course, advStanding)
                            const isCompleted = isTransfer || completedCourses.some(c =>
                              `${c.subject} ${c.catalog}`.toUpperCase() ===
                              `${course.subject} ${course.catalog}`.toUpperCase()
                            )
                            const isCurrent = !isTransfer && currentCourses.some(c =>
                              `${c.subject} ${c.catalog}`.toUpperCase() ===
                              `${course.subject} ${course.catalog}`.toUpperCase()
                            )

                            return (
                              <div
                                key={course.id}
                                className={[
                                  'drv-course-row',
                                  course.is_required ? 'drv-course-row--required' : '',
                                  isCompleted        ? 'drv-course-row--done'     : '',
                                  isCurrent          ? 'drv-course-row--current'  : '',
                                ].filter(Boolean).join(' ')}
                              >
                                <div className="drv-course-status">
                                  {isCompleted
                                    ? <FaCheckCircle className="drv-status-icon drv-status-icon--done" />
                                    : isCurrent
                                      ? <FaCircle className="drv-status-icon drv-status-icon--current" />
                                      : <FaCircle className="drv-status-icon drv-status-icon--empty" />
                                  }
                                </div>

                                <div className="drv-course-info">
                                  <div className="drv-course-top">
                                    <span className={`drv-course-code ${!course.catalog ? 'drv-course-code--wildcard' : ''}`}>
                                      {course.subject} {course.catalog || '•••'}
                                    </span>
                                    <span className="drv-course-title">{course.title}</span>
                                    <div className="drv-course-badges">
                                      {course.is_required && <span className="drv-badge drv-badge--required">Required</span>}
                                      {course.recommended && <span className="drv-badge drv-badge--rec"><FaStar /> Rec</span>}
                                    </div>
                                  </div>
                                  {course.recommended && course.recommendation_reason && (
                                    <p className="drv-rec-reason">
                                      <FaLightbulb className="drv-rec-icon" />
                                      {course.recommendation_reason}
                                    </p>
                                  )}
                                </div>

                                <div className="drv-course-right">
                                  <span className="drv-course-credits">{course.credits}cr</span>
                                  {isCompleted && isTransfer   && <span className="drv-tag drv-tag--transfer">↩ Transfer</span>}
                                  {isCompleted && !isTransfer  && <span className="drv-tag drv-tag--done">✓ Done</span>}
                                  {isCurrent && !isCompleted   && <span className="drv-tag drv-tag--cur">Taking</span>}
                                </div>
                              </div>
                            )
                          })}
                        </div>

                        {courses && courses.length > PREVIEW && (
                          <button className="drv-show-more" onClick={() => toggleShowAll(block.id)}>
                            {showAll
                              ? <><FaChevronUp /> Show less</>
                              : <><FaChevronDown /> Show {courses.length - PREVIEW} more</>
                            }
                          </button>
                        )}

                        {showRecommended && (!courses || courses.length === 0) && (
                          <p className="drv-no-rec">No recommended courses in this block.</p>
                        )}
                      </div>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
