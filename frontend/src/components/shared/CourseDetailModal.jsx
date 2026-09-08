import { useEffect, useState } from 'react'
import {
  FaHeart, FaRegHeart, FaCheckCircle, FaBook, FaUser, FaChartBar,
  FaStar, FaTrophy, FaLayerGroup, FaExclamationCircle, FaTimes, FaExternalLinkAlt,
  FaFlag, FaCalendarAlt, FaMapMarkerAlt,
} from 'react-icons/fa'
import { useCourseDetail } from '../../contexts/CourseDetailContext'
import { useLanguage } from '../../contexts/PreferencesContext'
import { getBestRating } from '../../utils/courseRatings'
import ProfSuggestionPopover from '../ProfSuggestion/ProfSuggestionPopover'
import './CourseDetailModal.css'

const DAY_MAP = {
  M:'Mon', T:'Tue', W:'Wed', R:'Thu', F:'Fri', S:'Sat', U:'Sun',
  '1':'Mon','2':'Tue','3':'Wed','4':'Thu','5':'Fri','6':'Sat','7':'Sun',
}

const gpaToLetter = (gpa) => {
  if (!gpa) return ''
  const n = parseFloat(gpa)
  if (n >= 3.85) return 'A'
  if (n >= 3.5)  return 'A-'
  if (n >= 3.15) return 'B+'
  if (n >= 2.85) return 'B'
  if (n >= 2.5)  return 'B-'
  if (n >= 2.15) return 'C+'
  if (n >= 1.85) return 'C'
  if (n >= 1.5)  return 'C-'
  if (n >= 1.15) return 'D+'
  if (n >= 0.85) return 'D'
  return 'F'
}

export default function CourseDetailModal({
  isFavorited, isCompleted, isCurrent,
  onToggleFavorite, onToggleCompleted, onToggleCurrent,
}) {
  const { course, loading, error, closeCourse } = useCourseDetail()
  const { t } = useLanguage()
  // "Professor outdated?" flag popover (moved here from the old inline
  // detail view in CoursesTab so both entry points get it).
  const [flagOpen, setFlagOpen] = useState(false)

  // Close on Escape
  useEffect(() => {
    if (!course) return
    const onKey = (e) => { if (e.key === 'Escape') closeCourse() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [course, closeCourse])

  // Reset the flag popover whenever a different course is shown
  useEffect(() => { setFlagOpen(false) }, [course?.subject, course?.catalog])

  // Lock body scroll while open
  useEffect(() => {
    if (course) {
      document.body.style.overflow = 'hidden'
    } else {
      document.body.style.overflow = ''
    }
    return () => { document.body.style.overflow = '' }
  }, [course])

  if (!course) return null

  const isLoading = course._loading || loading
  const rating  = getBestRating(course)

  const byTerm = {}
  for (const s of course.schedule || []) {
    const term = s.term || 'Unknown'
    if (!byTerm[term]) byTerm[term] = []
    byTerm[term].push(s)
  }
  const recentTerms = (() => {
    const top2 = Object.keys(byTerm).sort((a, b) => b.localeCompare(a)).slice(0, 2)
    if (course.term && byTerm[course.term] && !top2.includes(course.term)) {
      return [course.term, ...top2]
    }
    return top2
  })()

  const subj = course.subject
  const cat  = course.catalog

  return (
    <div className="cdm-backdrop" onMouseDown={closeCourse}>
      <div className="cdm-panel" onMouseDown={(e) => e.stopPropagation()}>

        <button className="cdm-close" onClick={closeCourse} aria-label="Close">
          <FaTimes />
        </button>

        {isLoading ? (
          <div className="cdm-skeleton">
            <div className="cdm-skeleton-code" />
            <div className="cdm-skeleton-title" />
            <div className="cdm-skeleton-desc" />
            <div className="cdm-skeleton-desc short" />
          </div>
        ) : error ? (
          <div className="cdm-error">{error}</div>
        ) : (
          <>
            {/* ── Hero ─────────────────────────────────────── */}
            <div className="cdm-hero">
              <div className="cdm-hero-top">
                <div className="cdm-code-block">
                  <div className="cdm-code-row">
                    <span className="cdm-code">{subj} {cat}</span>
                    {course.credits != null && (
                      <span className="cdm-credits">{course.credits} cr</span>
                    )}
                  </div>
                  <h2 className="cdm-title">{course.title}</h2>
                  {course.description && (
                    <p className="cdm-description">{course.description}</p>
                  )}
                </div>

                <div className="cdm-actions">
                  <button
                    className={`cdm-action-btn btn-save ${isFavorited?.(subj, cat) ? 'active' : ''}`}
                    onClick={() => onToggleFavorite?.(course)}
                  >
                    {isFavorited?.(subj, cat) ? <FaHeart /> : <FaRegHeart />}
                    {isFavorited?.(subj, cat) ? t('courses.detailSaved') : t('courses.detailSave')}
                  </button>
                  <button
                    className={`cdm-action-btn btn-done ${isCompleted?.(subj, cat) ? 'active' : ''}`}
                    onClick={() => { closeCourse(); onToggleCompleted?.(course) }}
                  >
                    <FaCheckCircle />
                    {isCompleted?.(subj, cat) ? t('courses.detailCompleted') : t('courses.detailDone')}
                  </button>
                  <button
                    className={`cdm-action-btn btn-current ${isCurrent?.(subj, cat) ? 'active' : ''}`}
                    onClick={() => onToggleCurrent?.(course)}
                  >
                    <FaBook />
                    {isCurrent?.(subj, cat) ? t('courses.detailEnrolled') : t('courses.detailEnroll')}
                  </button>
                  <a
                    className="cdm-action-btn btn-vsb"
                    href={`https://vsb.mcgill.ca/criteria.jsp?access=0&lang=en&tip=2&page=criteria&scratch=0&advice=0&legend=1&term=202601&sort=none&filters=iiiiiiiiii&bbs=&ds=&cams=OFF-CAMPUS_DISTANCE_DOWNTOWN_MACDONALD&locs=any&isrts=any&ses=any&pl=&pac=1&CourseData_0_0=${subj}-${cat}&rq_0_0=null`}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    <FaExternalLinkAlt /> VSB
                  </a>
                </div>
              </div>

              <div className="cdm-stats">
                {course.term_average != null && (
                  <div className="cdm-stat cdm-stat--term">
                    <FaCalendarAlt className="cdm-stat-icon" />
                    <span className="cdm-stat-label">{t('courses.termAvgLabel').replace('{term}', course.term)}</span>
                    <span className="cdm-stat-value gpa-value">{parseFloat(course.term_average).toFixed(2)}</span>
                    <span className="cdm-stat-sub">({gpaToLetter(course.term_average)})</span>
                  </div>
                )}
                {course.average && (
                  <div className="cdm-stat">
                    <FaTrophy className="cdm-stat-icon" />
                    <span className="cdm-stat-label">{t('courses.recentGpa')}</span>
                    <span className="cdm-stat-value gpa-value">{parseFloat(course.average).toFixed(2)}</span>
                    <span className="cdm-stat-sub">({gpaToLetter(course.average)})</span>
                  </div>
                )}
                {course.overall_average && (
                  <div className="cdm-stat">
                    <FaChartBar className="cdm-stat-icon" />
                    <span className="cdm-stat-label">{t('courses.allTimeAvg')}</span>
                    <span className="cdm-stat-value">{parseFloat(course.overall_average).toFixed(2)}</span>
                    <span className="cdm-stat-sub">({gpaToLetter(course.overall_average)})</span>
                  </div>
                )}
              </div>
            </div>

            {/* ── Body ─────────────────────────────────────── */}
            <div className="cdm-body">

              {/* LEFT */}
              <div className="cdm-col">

                {recentTerms.length > 0 && (
                  <div className="cdm-section">
                    <div className="cdm-section-header">
                      <FaLayerGroup />
                      <h3>{t('courses.sections')}</h3>
                      <span className="cdm-section-count">{t('courses.nTotal').replace('{n}', (course.schedule || []).length)}</span>
                    </div>
                    {recentTerms.map(term => (
                      <div key={term} className="cdm-term-group">
                        <div className="cdm-term-label">{term}</div>
                        <div className="cdm-schedule-grid">
                          {byTerm[term].map((s, idx) => (
                            <div key={idx} className="cdm-schedule-card">
                              <div className="cdm-schedule-card-header">
                                {s.section_type && (
                                  <span className={`cdm-type-badge type-${s.section_type.toLowerCase()}`}>{s.section_type}</span>
                                )}
                                {s.crn && <span className="cdm-crn">CRN {s.crn}</span>}
                              </div>
                              {s.instructor && (
                                <div className="cdm-schedule-row">
                                  <FaUser className="cdm-schedule-icon" />
                                  <span>{s.instructor}</span>
                                </div>
                              )}
                              {s.days && (
                                <div className="cdm-schedule-row">
                                  <div className="cdm-day-pills">
                                    {s.days.split('').map((d, i) => (
                                      <span key={i} className="cdm-day-pill">{DAY_MAP[d] || d}</span>
                                    ))}
                                  </div>
                                  {s.times && <span className="cdm-time">{s.times}</span>}
                                </div>
                              )}
                              {s.location && (
                                <div className="cdm-schedule-row">
                                  <FaMapMarkerAlt className="cdm-schedule-icon" />
                                  <span>{s.location}</span>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {course.grade_trend?.length > 0 && (
                  <div className="cdm-section">
                    <div className="cdm-section-header">
                      <FaChartBar />
                      <h3>{t('courses.gradeHistory')}</h3>
                      <span className="cdm-section-count">{t('courses.nYears').replace('{n}', course.grade_trend.length)}</span>
                    </div>
                    <div className="cdm-grade-list">
                      {course.grade_trend.map((entry, idx) => {
                        const gpa    = parseFloat(entry.average)
                        const barPct = Math.min(100, (gpa / 4.0) * 100)
                        return (
                          <div key={idx} className="cdm-grade-row">
                            <span className="cdm-grade-year">{entry.year}</span>
                            <div className="cdm-grade-bar-wrap">
                              <div className="cdm-grade-bar" style={{ width: `${barPct}%` }} />
                            </div>
                            <span className="cdm-grade-gpa">{gpa.toFixed(2)}</span>
                            <span className="cdm-grade-letter">{gpaToLetter(gpa)}</span>
                            <span className="cdm-grade-sections">{entry.sections}s</span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>

              {/* RIGHT */}
              <div className="cdm-col">

                {rating != null && (
                  <div className="cdm-section">
                    <div className="cdm-section-header">
                      <FaStar />
                      <h3>{t('courses.professorRating')}</h3>
                    </div>
                    <div className="cdm-rating-grid">
                      <div className="cdm-rating-card">
                        <div className={`cdm-rating-val ${rating >= 4 ? 'good' : rating >= 3 ? 'ok' : 'bad'}`}>{rating.toFixed(1)}</div>
                        <div className="cdm-rating-label">{t('courses.rating')}</div>
                      </div>
                      {course.rmp_difficulty != null && (
                        <div className="cdm-rating-card">
                          <div className={`cdm-rating-val ${course.rmp_difficulty <= 2.5 ? 'good' : course.rmp_difficulty <= 3.5 ? 'ok' : 'bad'}`}>{course.rmp_difficulty.toFixed(1)}</div>
                          <div className="cdm-rating-label">{t('courses.difficulty')}</div>
                        </div>
                      )}
                      {course.rmp_would_take_again != null && (
                        <div className="cdm-rating-card">
                          <div className={`cdm-rating-val ${course.rmp_would_take_again >= 70 ? 'good' : course.rmp_would_take_again >= 50 ? 'ok' : 'bad'}`}>{Math.round(course.rmp_would_take_again)}%</div>
                          <div className="cdm-rating-label">{t('courses.wouldRetake')}</div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {course.instructors?.length > 0 && (
                  <div className="cdm-section">
                    <div className="cdm-section-header">
                      <FaUser />
                      <h3>{t('courses.instructorsTitle')}</h3>
                      <span className="cdm-flag-wrapper">
                        <button
                          className={`cdm-flag-btn ${flagOpen ? 'active' : ''}`}
                          onClick={() => setFlagOpen(o => !o)}
                          title={t('courses.flagProf')}
                          aria-label={t('courses.flagProf')}
                        >
                          <FaFlag />
                        </button>
                        {flagOpen && (
                          <ProfSuggestionPopover
                            courseCode={`${subj} ${cat}`}
                            currentInstructor={course.instructors[0] || course.instructor || null}
                            onClose={() => setFlagOpen(false)}
                          />
                        )}
                      </span>
                    </div>
                    <div className="cdm-instructors">
                      {course.instructors.map((name, idx) => (
                        <div key={idx} className="cdm-instructor-chip">
                          <FaUser className="cdm-instructor-icon" />
                          <span>{name}</span>
                          {idx === 0 && <span className="cdm-instructor-badge">{t('courses.mostRecent')}</span>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {(course.prerequisites || course.corequisites || course.restrictions) && (
                  <div className="cdm-section">
                    <div className="cdm-section-header">
                      <FaExclamationCircle />
                      <h3>{t('courses.requirementsTitle')}</h3>
                    </div>
                    <div className="cdm-reqs">
                      {course.prerequisites && (
                        <div className="cdm-req-item">
                          <span className="cdm-req-label">{t('courses.prerequisites')}</span>
                          <span className="cdm-req-text">{course.prerequisites}</span>
                        </div>
                      )}
                      {course.corequisites && (
                        <div className="cdm-req-item">
                          <span className="cdm-req-label">{t('courses.corequisites')}</span>
                          <span className="cdm-req-text">{course.corequisites}</span>
                        </div>
                      )}
                      {course.restrictions && (
                        <div className="cdm-req-item">
                          <span className="cdm-req-label">{t('courses.restrictions')}</span>
                          <span className="cdm-req-text">{course.restrictions}</span>
                        </div>
                      )}
                    </div>
                  </div>
                )}

              </div>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
