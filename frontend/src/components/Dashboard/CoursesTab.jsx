import { useState } from 'react'
import {
  FaHeart, FaRegHeart, FaCheckCircle, FaStar, FaBook,
  FaUser, FaChartBar, FaFlag, FaChevronLeft, FaChevronRight,
  FaArrowLeft, FaTrophy, FaLayerGroup
} from 'react-icons/fa'
import { MdOutlineRateReview } from 'react-icons/md'
import { useLanguage } from '../../contexts/LanguageContext'
import './CoursesTab.css'
import ProfSuggestionPopover from '../ProfSuggestion/ProfSuggestionPopover'

const PAGE_SIZE = 10

const getRatingColor = (rating) => {
  if (!rating) return undefined
  if (rating >= 4.0) return '#22c55e'
  if (rating >= 3.5) return '#84cc16'
  if (rating >= 3.0) return '#f59e0b'
  return '#ef4444'
}

const getDifficultyColor = (difficulty) => {
  if (!difficulty) return undefined
  if (difficulty <= 2.0) return '#22c55e'
  if (difficulty <= 3.0) return '#84cc16'
  if (difficulty <= 4.0) return '#f59e0b'
  return '#ef4444'
}

const getBestRating = (course) =>
  course?.blended_rating ?? course?.rmp_rating ?? course?.mc_rating ?? null

const getTotalReviews = (course) => {
  if (!course) return null
  const total = (course.rmp_num_ratings ?? 0) + (course.mc_num_ratings ?? 0)
  return total > 0 ? total : null
}

const DAY_MAP = {
  M:'Mon', T:'Tue', W:'Wed', R:'Thu', F:'Fri', S:'Sat', U:'Sun',
  '1':'Mon','2':'Tue','3':'Wed','4':'Thu','5':'Fri','6':'Sat','7':'Sun',
}

export default function CoursesTab({
  searchQuery, setSearchQuery,
  searchResults, setSearchResults,
  isSearching, searchError,
  handleCourseSearch,
  selectedCourse, setSelectedCourse, handleCourseClick,
  sortBy, setSortBy, sortCourses,
  isFavorited, isCompleted, isCurrent,
  handleToggleFavorite, handleToggleCompleted, handleToggleCurrent,
  gpaToLetterGrade,
}) {
  const { t } = useLanguage()
  const [openFlagCard,   setOpenFlagCard]   = useState(null)
  const [openFlagDetail, setOpenFlagDetail] = useState(false)
  const [currentPage,    setCurrentPage]    = useState(1)

  const toggleFlagCard   = (e, key) => { e.stopPropagation(); setOpenFlagCard(p => p === key ? null : key) }
  const handleSortChange = (val)    => { setSortBy(val); setCurrentPage(1) }
  const handleSearch     = (e)      => { setCurrentPage(1); handleCourseSearch(e) }

  const sortedResults = sortCourses(searchResults, sortBy)
  const totalPages    = Math.ceil(sortedResults.length / PAGE_SIZE)
  const pageStart     = (currentPage - 1) * PAGE_SIZE
  const pageResults   = sortedResults.slice(pageStart, pageStart + PAGE_SIZE)

  const goToPage = (page) => {
    setCurrentPage(page)
    document.querySelector('.search-results')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <div className="courses-container">

      {/* ── Search bar ──────────────────────────────────────── */}
      <form className="search-section" onSubmit={handleSearch}>
        <input
          type="text"
          className="search-input"
          placeholder={t('courses.searchPlaceholder')}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="btn btn-search" disabled={isSearching || !searchQuery.trim()}>
          {t('courses.search')}
        </button>
      </form>

      {searchError && <div className="error-banner">{searchError}</div>}

      {/* ── Results list ────────────────────────────────────── */}
      {searchResults.length > 0 && !selectedCourse && (
        <div className="search-results">
          <div className="results-header-bar">
            <h3 className="results-header">
              {searchResults.length === 1
                ? t('courses.foundResults').replace('{count}', searchResults.length)
                : t('courses.foundResultsPlural').replace('{count}', searchResults.length)}
              {totalPages > 1 && (
                <span className="results-page-info"> — page {currentPage} of {totalPages}</span>
              )}
            </h3>
            <div className="sort-controls">
              <label htmlFor="sort-select" className="sort-label">{t('courses.sortBy')}</label>
              <select id="sort-select" className="sort-select" value={sortBy} onChange={(e) => handleSortChange(e.target.value)}>
                <option value="relevance">{t('courses.relevance')}</option>
                <option value="rating-high">{t('courses.sortRatingHigh')}</option>
                <option value="rating-low">{t('courses.sortRatingLow')}</option>
                <option value="name-az">{t('courses.sortNameAZ')}</option>
                <option value="name-za">{t('courses.sortNameZA')}</option>
                <option value="instructor-az">{t('courses.sortInstructorAZ')}</option>
                <option value="instructor-za">{t('courses.sortInstructorZA')}</option>
              </select>
            </div>
          </div>

          <div className="course-list">
            {pageResults.map((course) => {
              const cardKey     = `${course.subject}-${course.catalog}`
              const isFlagOpen  = openFlagCard === cardKey
              const rating      = getBestRating(course)
              const ratingColor = getRatingColor(rating)
              const diffColor   = getDifficultyColor(course.rmp_difficulty)

              return (
                <div key={cardKey} className="course-card">
                  <div className="course-card-content" onClick={() => handleCourseClick(course)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      {course.average != null && (
                        <div className="course-average">
                          {course.average.toFixed(1)} GPA ({gpaToLetterGrade(course.average)})
                        </div>
                      )}
                    </div>
                    <h4 className="course-title">{course.title}</h4>

                    {course.instructor && (
                      <div className="course-instructor-section">
                        <div className="instructor-name"><FaUser /> {course.instructor}</div>
                        {rating && (
                          <div className="rmp-compact">
                            <div className="rmp-stat">
                              <span className="rmp-label" style={{ color: ratingColor }}>
                                <FaStar style={{ color: ratingColor }} /> {t('courses.rating')}:
                              </span>
                              <span className="rmp-value" style={{ color: ratingColor }}>{rating.toFixed(1)}/5.0</span>
                            </div>
                            {course.rmp_difficulty && (
                              <div className="rmp-stat">
                                <span className="rmp-label" style={{ color: diffColor }}>
                                  <MdOutlineRateReview style={{ color: diffColor }} /> {t('courses.difficulty')}:
                                </span>
                                <span className="rmp-value" style={{ color: diffColor }}>{course.rmp_difficulty.toFixed(1)}/5.0</span>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  <div className="prof-flag-wrapper">
                    <button className={`prof-flag-btn ${isFlagOpen ? 'active' : ''}`} onClick={(e) => toggleFlagCard(e, cardKey)} data-tooltip="Report wrong professor">
                      <FaFlag />
                    </button>
                    {isFlagOpen && (
                      <ProfSuggestionPopover
                        courseSubject={course.subject}
                        courseCatalog={course.catalog}
                        currentInstructor={course.instructor}
                        onClose={() => setOpenFlagCard(null)}
                      />
                    )}
                  </div>

                  <div className="course-card-actions">
                    <button className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`} onClick={(e) => { e.stopPropagation(); handleToggleFavorite(course) }} data-tooltip={isFavorited(course.subject, course.catalog) ? 'Remove saved' : 'Save course'}>
                      {isFavorited(course.subject, course.catalog) ? <FaHeart className="favorite-icon" /> : <FaRegHeart className="favorite-icon" />}
                    </button>
                    <button className={`completed-btn ${isCompleted(course.subject, course.catalog) ? 'completed' : ''}`} onClick={(e) => { e.stopPropagation(); handleToggleCompleted(course) }} data-tooltip={isCompleted(course.subject, course.catalog) ? 'Mark incomplete' : 'Mark complete'}>
                      <FaCheckCircle className="completed-icon" />
                    </button>
                    <button className={`current-btn ${isCurrent(course.subject, course.catalog) ? 'current' : ''}`} onClick={(e) => { e.stopPropagation(); handleToggleCurrent(course) }} data-tooltip={isCurrent(course.subject, course.catalog) ? 'Remove from current' : 'Add to current'}>
                      <FaBook className="current-icon" />
                    </button>
                  </div>
                </div>
              )
            })}
          </div>

          {totalPages > 1 && (
            <div className="pagination">
              <button className="pagination-btn" onClick={() => goToPage(currentPage - 1)} disabled={currentPage === 1} aria-label="Previous page"><FaChevronLeft /></button>
              <div className="pagination-pages">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => {
                  const isNear = Math.abs(page - currentPage) <= 1
                  const isEdge = page === 1 || page === totalPages
                  if (!isNear && !isEdge) {
                    if (page === 2 || page === totalPages - 1) return <span key={page} className="pagination-ellipsis">…</span>
                    return null
                  }
                  return <button key={page} className={`pagination-page ${page === currentPage ? 'active' : ''}`} onClick={() => goToPage(page)}>{page}</button>
                })}
              </div>
              <button className="pagination-btn" onClick={() => goToPage(currentPage + 1)} disabled={currentPage === totalPages} aria-label="Next page"><FaChevronRight /></button>
            </div>
          )}
        </div>
      )}

      {/* ── Course detail ────────────────────────────────────── */}
      {selectedCourse && (() => {
        const rating       = getBestRating(selectedCourse)
        const totalReviews = getTotalReviews(selectedCourse)
        const ratingColor  = getRatingColor(rating)

        const byTerm = {}
        for (const s of selectedCourse.schedule || []) {
          const term = s.term || 'Unknown'
          if (!byTerm[term]) byTerm[term] = []
          byTerm[term].push(s)
        }
        const recentTerms = Object.keys(byTerm).sort((a, b) => b.localeCompare(a)).slice(0, 2)

        return (
          <div className="course-details">

            <button className="btn-back" onClick={() => { setSelectedCourse(null); setOpenFlagDetail(false) }}>
              <FaArrowLeft /> {t('courses.backToResults')}
            </button>

            {/* ── Hero ────────────────────────────────────────── */}
            <div className="course-detail-hero">
              <div className="course-detail-hero-top">
                <div className="course-detail-code-block">
                  <div className="course-detail-code-row">
                    <span className="course-detail-code">{selectedCourse.subject} {selectedCourse.catalog}</span>
                    {selectedCourse.credits != null && (
                      <span className="course-detail-credits">{selectedCourse.credits} cr</span>
                    )}
                  </div>
                  <h2 className="course-detail-title">{selectedCourse.title}</h2>
                  {selectedCourse.description && (
                    <p className="course-detail-description">{selectedCourse.description}</p>
                  )}
                </div>

                <div className="course-detail-actions">
                  <button className={`course-detail-action-btn btn-save ${isFavorited(selectedCourse.subject, selectedCourse.catalog) ? 'active' : ''}`} onClick={() => handleToggleFavorite(selectedCourse)}>
                    {isFavorited(selectedCourse.subject, selectedCourse.catalog) ? <FaHeart /> : <FaRegHeart />}
                    {isFavorited(selectedCourse.subject, selectedCourse.catalog) ? 'Saved' : 'Save'}
                  </button>
                  <button className={`course-detail-action-btn btn-done ${isCompleted(selectedCourse.subject, selectedCourse.catalog) ? 'active' : ''}`} onClick={() => handleToggleCompleted(selectedCourse)}>
                    <FaCheckCircle />
                    {isCompleted(selectedCourse.subject, selectedCourse.catalog) ? 'Completed' : 'Done'}
                  </button>
                  <button className={`course-detail-action-btn btn-current ${isCurrent(selectedCourse.subject, selectedCourse.catalog) ? 'active' : ''}`} onClick={() => handleToggleCurrent(selectedCourse)}>
                    <FaBook />
                    {isCurrent(selectedCourse.subject, selectedCourse.catalog) ? 'Enrolled' : 'Enroll'}
                  </button>
                </div>
              </div>

              <div className="course-detail-stats">
                {selectedCourse.average && (
                  <div className="course-detail-stat">
                    <FaTrophy className="course-detail-stat-icon" />
                    <span className="course-detail-stat-label">Recent GPA</span>
                    <span className="course-detail-stat-value gpa-value">{parseFloat(selectedCourse.average).toFixed(2)}</span>
                    <span className="course-detail-stat-sub">({gpaToLetterGrade(selectedCourse.average)})</span>
                  </div>
                )}
                {selectedCourse.overall_average && (
                  <div className="course-detail-stat">
                    <FaChartBar className="course-detail-stat-icon" />
                    <span className="course-detail-stat-label">All-time Avg</span>
                    <span className="course-detail-stat-value">{parseFloat(selectedCourse.overall_average).toFixed(2)}</span>
                    <span className="course-detail-stat-sub">({gpaToLetterGrade(selectedCourse.overall_average)})</span>
                  </div>
                )}
                {selectedCourse.num_sections > 0 && (
                  <div className="course-detail-stat">
                    <FaLayerGroup className="course-detail-stat-icon" />
                    <span className="course-detail-stat-label">Sections</span>
                    <span className="course-detail-stat-value">{selectedCourse.num_sections}</span>
                  </div>
                )}
                {rating && (
                  <div className="course-detail-stat">
                    <FaStar className="course-detail-stat-icon" style={{ color: ratingColor }} />
                    <span className="course-detail-stat-label">Prof Rating</span>
                    <span className="course-detail-stat-value" style={{ color: ratingColor }}>{rating.toFixed(1)}</span>
                    <span className="course-detail-stat-sub">/5.0</span>
                  </div>
                )}
              </div>
            </div>

            {/* ── Two-column body ──────────────────────────────── */}
            <div className="course-detail-body">

              {/* LEFT — schedule + grade history */}
              <div className="course-detail-col">

                {recentTerms.length > 0 && (
                  <div className="course-detail-section">
                    <div className="course-detail-section-header">
                      <FaLayerGroup />
                      <h3 className="course-detail-section-title">Sections</h3>
                      <span className="course-detail-section-count">{(selectedCourse.schedule || []).length} total</span>
                    </div>
                    {recentTerms.map(term => (
                      <div key={term} className="schedule-term-group">
                        <div className="schedule-term-label">{term}</div>
                        <div className="schedule-cards-grid">
                          {byTerm[term].map((s, idx) => (
                            <div key={idx} className="schedule-card">
                              <div className="schedule-card-header">
                                {s.section_type && (
                                  <span className={`schedule-type-badge type-${s.section_type.toLowerCase()}`}>{s.section_type}</span>
                                )}
                                {s.crn && <span className="schedule-crn">CRN {s.crn}</span>}
                              </div>
                              {s.instructor && (
                                <div className="schedule-card-row">
                                  <FaUser className="schedule-card-icon" />
                                  <span className="schedule-card-value">{s.instructor}</span>
                                </div>
                              )}
                              {s.days && (
                                <div className="schedule-card-row">
                                  <div className="schedule-day-pills">
                                    {s.days.split('').map((d, i) => (
                                      <span key={i} className="schedule-day-pill">{DAY_MAP[d] || d}</span>
                                    ))}
                                  </div>
                                  {s.times && <span className="schedule-time-value">{s.times}</span>}
                                </div>
                              )}
                              {s.location && (
                                <div className="schedule-card-row">
                                  <span className="schedule-location-value">📍 {s.location}</span>
                                </div>
                              )}
                            </div>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {selectedCourse.grade_trend?.length > 0 && (
                  <div className="course-detail-section">
                    <div className="course-detail-section-header">
                      <FaChartBar />
                      <h3 className="course-detail-section-title">Grade History</h3>
                      <span className="course-detail-section-count">{selectedCourse.grade_trend.length} years</span>
                    </div>
                    <div className="grade-trend-list">
                      {selectedCourse.grade_trend.map((entry, idx) => {
                        const gpa    = parseFloat(entry.average)
                        const barPct = Math.min(100, (gpa / 4.0) * 100)
                        return (
                          <div key={idx} className="grade-trend-row">
                            <span className="grade-trend-year">{entry.year}</span>
                            <div className="grade-trend-bar-wrap">
                              <div className="grade-trend-bar" style={{ width: `${barPct}%` }} />
                            </div>
                            <span className="grade-trend-gpa">{gpa.toFixed(2)}</span>
                            <span className="grade-trend-letter">{gpaToLetterGrade(gpa)}</span>
                            <span className="grade-trend-sections">{entry.sections} section{entry.sections !== 1 ? 's' : ''}</span>
                          </div>
                        )
                      })}
                    </div>
                  </div>
                )}
              </div>

              {/* RIGHT — rating + instructors */}
              <div className="course-detail-col">

                {rating && (
                  <div className="course-detail-section">
                    <div className="course-detail-section-header">
                      <FaStar />
                      <h3 className="course-detail-section-title">{t('courses.professorRating')}</h3>
                    </div>
                    {selectedCourse.instructors?.[0] && (
                      <div className="rmp-instructor-label">
                        <FaUser /> {selectedCourse.instructors[0]}
                      </div>
                    )}
                    <div className="rmp-grid">
                      <div className="rmp-grid-card">
                        <div className={`rmp-grid-value ${rating >= 4 ? 'good' : rating >= 3 ? 'ok' : 'bad'}`}>{rating.toFixed(1)}</div>
                        <div className="rmp-grid-label">{t('courses.rating')}</div>
                      </div>
                      {selectedCourse.rmp_difficulty != null && (
                        <div className="rmp-grid-card">
                          <div className={`rmp-grid-value ${selectedCourse.rmp_difficulty <= 2.5 ? 'good' : selectedCourse.rmp_difficulty <= 3.5 ? 'ok' : 'bad'}`}>{selectedCourse.rmp_difficulty.toFixed(1)}</div>
                          <div className="rmp-grid-label">{t('courses.difficulty')}</div>
                        </div>
                      )}
                      {selectedCourse.rmp_would_take_again != null && (
                        <div className="rmp-grid-card">
                          <div className={`rmp-grid-value ${selectedCourse.rmp_would_take_again >= 70 ? 'good' : selectedCourse.rmp_would_take_again >= 50 ? 'ok' : 'bad'}`}>{Math.round(selectedCourse.rmp_would_take_again)}%</div>
                          <div className="rmp-grid-label">{t('courses.wouldRetake')}</div>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {selectedCourse.instructors?.length > 0 && (
                  <div className="course-detail-section">
                    <div className="course-detail-section-header">
                      <FaUser />
                      <h3 className="course-detail-section-title">Instructors</h3>
                    </div>
                    <div className="instructors-list">
                      {selectedCourse.instructors.map((name, idx) => (
                        <div key={idx} className="instructor-chip">
                          <FaUser className="instructor-chip-icon" />
                          <span>{name}</span>
                          {idx === 0 && <span className="instructor-recent-badge">most recent</span>}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

              </div>
            </div>

          </div>
        )
      })()}

      {!searchResults.length && !selectedCourse && !searchError && !isSearching && (
        <div className="placeholder-content">
          <div className="placeholder-icon"><FaBook /></div>
          <h3>{t('courses.explorerTitle')}</h3>
          <p>{t('courses.explorerDesc')}</p>
        </div>
      )}
    </div>
  )
}