import { useState } from 'react'
import {
  FaHeart, FaRegHeart, FaCheckCircle, FaStar, FaBook,
  FaUser, FaChartBar, FaFlag, FaChevronLeft, FaChevronRight,
  FaArrowLeft, FaTrophy, FaLayerGroup, FaExternalLinkAlt, FaCalendarAlt
, FaSearch } from 'react-icons/fa'
import { GrPowerCycle } from 'react-icons/gr'
import { MdOutlineRateReview } from 'react-icons/md'
import { useLanguage } from '../../contexts/LanguageContext'
import './CoursesTab.css'
import ProfSuggestionPopover from '../ProfSuggestion/ProfSuggestionPopover'

const PAGE_SIZE = 10

// ── RMP colour helpers ─────────────────────────────────────
const getRatingColor = (rating) => {
  if (!rating) return undefined
  if (rating >= 4.0) return '#22c55e'  // green  — excellent
  if (rating >= 3.5) return '#84cc16'  // lime   — good
  if (rating >= 3.0) return '#f59e0b'  // amber  — average
  return '#ef4444'                      // red    — poor
}

// Lower difficulty = better/easier = greener
const getDifficultyColor = (difficulty) => {
  if (!difficulty) return undefined
  if (difficulty <= 2.0) return '#22c55e'
  if (difficulty <= 3.0) return '#84cc16'
  if (difficulty <= 4.0) return '#f59e0b'
  return '#ef4444'
}

const getWouldTakeAgainColor = (percent) => {
  if (percent == null) return undefined
  if (percent >= 70) return '#22c55e'
  if (percent >= 50) return '#84cc16'
  if (percent >= 30) return '#f59e0b'
  return '#ef4444'
}

export default function CoursesTab({
  // Search
  searchQuery,
  setSearchQuery,
  searchResults,
  setSearchResults,
  isSearching,
  searchError,
  handleCourseSearch,
  // Detail
  selectedCourse,
  setSelectedCourse,
  handleCourseClick,
  // Sort
  sortBy,
  setSortBy,
  sortCourses,
  // Favorites / Completed / Current
  isFavorited,
  isCompleted,
  isCurrent,
  handleToggleFavorite,
  handleToggleCompleted,
  handleToggleCurrent,
  // Utility
  gpaToLetterGrade,
  // Fuzzy correction
  searchCorrection,
  onSearchWithCorrection,
  hasSearched,
}) {
  const { t, language } = useLanguage()

  const [openFlagCard, setOpenFlagCard] = useState(null)
  const [openFlagDetail, setOpenFlagDetail] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)

  const toggleFlagCard = (e, key) => {
    e.stopPropagation()
    setOpenFlagCard(prev => prev === key ? null : key)
  }

  const handleSortChange = (val) => {
    setSortBy(val)
    setCurrentPage(1)
  }

  const handleSearch = (e) => {
    setCurrentPage(1)
    handleCourseSearch(e)
  }

  const sortedResults = sortCourses(searchResults, sortBy)
  const totalPages    = Math.ceil(sortedResults.length / PAGE_SIZE)
  const pageStart     = (currentPage - 1) * PAGE_SIZE
  const pageEnd       = pageStart + PAGE_SIZE
  const pageResults   = sortedResults.slice(pageStart, pageEnd)

  const goToPage = (page) => {
    setCurrentPage(page)
    document.querySelector('.search-results')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  return (
    <div className="courses-container">
      <form className="search-section" onSubmit={handleSearch}>
        <input
          type="text"
          className="search-input"
          placeholder={t('courses.searchPlaceholder')}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button
          type="submit"
          className="btn btn-search"
          disabled={isSearching || !searchQuery.trim()}
        >
          {t('courses.search')}
        </button>
      </form>

      {searchError && <div className="error-banner">{searchError}</div>}

      {/* ── Fuzzy correction banner ── */}
      {searchCorrection && (
        <div className="search-correction-banner">
          <span>
            {language === 'fr' ? 'Vouliez-vous dire' : 'Did you mean'}
            {' '}
            <button
              className="search-correction-link"
              onClick={() => onSearchWithCorrection(searchCorrection.corrected)}
            >
              {searchCorrection.corrected}
            </button>
            {'? '}
            {language === 'fr'
              ? `Affichage des résultats pour "${searchCorrection.corrected}" (au lieu de "${searchCorrection.original}").`
              : `Showing results for "${searchCorrection.corrected}" instead of "${searchCorrection.original}".`}
          </span>
        </div>
      )}

      {/* ── VSB Banner ──────────────────────────────────────── */}
      <a
        href={`https://vsb.mcgill.ca/criteria.jsp?access=0&lang=${language === 'fr' ? 'fr' : 'en'}&tip=2&page=criteria&scratch=0&advice=0&legend=1&term=202601&sort=none&filters=iiiiiiiiii&bbs=&ds=&cams=OFF-CAMPUS_DISTANCE_DOWNTOWN_MACDONALD&locs=any&isrts=any&ses=any&pl=&pac=1`}
        target="_blank"
        rel="noreferrer"
        className="vsb-banner"
      >
        <div className="vsb-banner__left">
          <FaCalendarAlt className="vsb-banner__icon" />
          <div>
            <span className="vsb-banner__title">{t('courses.vsbLabel')}</span>
            <span className="vsb-banner__desc">{t('courses.vsbDesc')}</span>
          </div>
        </div>
        <FaExternalLinkAlt className="vsb-banner__arrow" />
      </a>

      {/* ── Search Results List ─────────────────────────────── */}
      {searchResults.length > 0 && !selectedCourse && (
        <div className="search-results">
          <div className="results-header-bar">
            <h3 className="results-header">
              {searchResults.length === 1
                ? t('courses.foundResults').replace('{count}', searchResults.length)
                : t('courses.foundResultsPlural').replace('{count}', searchResults.length)
              }
              {totalPages > 1 && (
                <span className="results-page-info">
                  — page {currentPage} of {totalPages}
                </span>
              )}
            </h3>
            <div className="sort-controls">
              <label htmlFor="sort-select" className="sort-label">{t('courses.sortBy')}</label>
              <select
                id="sort-select"
                className="sort-select"
                value={sortBy}
                onChange={(e) => handleSortChange(e.target.value)}
              >
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
              const cardKey    = `${course.subject}-${course.catalog}`
              const isFlagOpen = openFlagCard === cardKey

              const ratingColor      = getRatingColor(course.rmp_rating)
              const difficultyColor  = getDifficultyColor(course.rmp_difficulty)

              return (
                <div key={cardKey} className="course-card">
                  <div className="course-card-content" onClick={() => handleCourseClick(course)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      {course.average && (
                        <div className="course-average">
                          {course.average.toFixed(1)} GPA ({gpaToLetterGrade(course.average)})
                        </div>
                      )}
                    </div>
                    <h4 className="course-title">{course.title}</h4>

                    {course.instructor && (
                      <div className="course-instructor-section">
                        <div className="instructor-name"><FaUser /> {course.instructor}</div>
                        {course.rmp_rating && (
                          <div className="rmp-compact">
                            <div className="rmp-stat">
                              <span className="rmp-label" style={{ color: ratingColor }}>
                                <FaStar style={{ color: ratingColor }} />
                                {' '}{t('courses.rating')}:
                              </span>
                              <span className="rmp-value" style={{ color: ratingColor }}>
                                {course.rmp_rating.toFixed(1)}/5.0
                              </span>
                            </div>
                            {course.rmp_difficulty && (
                              <div className="rmp-stat">
                                <span className="rmp-label" style={{ color: difficultyColor }}>
                                  <MdOutlineRateReview style={{ color: difficultyColor }} />
                                  {' '}{t('courses.difficulty')}:
                                </span>
                                <span className="rmp-value" style={{ color: difficultyColor }}>
                                  {course.rmp_difficulty.toFixed(1)}/5.0
                                </span>
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Prof flag popover */}
                  <div className="prof-flag-wrapper">
                    <button
                      className={`prof-flag-btn ${isFlagOpen ? 'active' : ''}`}
                      onClick={(e) => toggleFlagCard(e, cardKey)}
                      data-tooltip="Report wrong professor"
                    >
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

                  {/* Action buttons */}
                  <div className="course-card-actions">
                    <button
                      className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`}
                      onClick={(e) => { e.stopPropagation(); handleToggleFavorite(course) }}
                      data-tooltip={isFavorited(course.subject, course.catalog) ? 'Remove saved' : 'Save course'}
                    >
                      {isFavorited(course.subject, course.catalog)
                        ? <FaHeart className="favorite-icon" />
                        : <FaRegHeart className="favorite-icon" />}
                    </button>
                    <button
                      className={`completed-btn ${isCompleted(course.subject, course.catalog) ? 'completed' : ''}`}
                      onClick={(e) => { e.stopPropagation(); handleToggleCompleted(course) }}
                      data-tooltip={isCompleted(course.subject, course.catalog) ? 'Mark incomplete' : 'Mark complete'}
                    >
                      <FaCheckCircle className="completed-icon" />
                    </button>
                    <button
                      className={`current-btn ${isCurrent(course.subject, course.catalog) ? 'current' : ''}`}
                      onClick={(e) => { e.stopPropagation(); handleToggleCurrent(course) }}
                      data-tooltip={isCurrent(course.subject, course.catalog) ? 'Remove from current' : 'Add to current'}
                    >
                      <FaBook className="current-icon" />
                    </button>
                  </div>
                </div>
              )
            })}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pagination">
              <button
                className="pagination-btn"
                onClick={() => goToPage(currentPage - 1)}
                disabled={currentPage === 1}
                aria-label="Previous page"
              >
                <FaChevronLeft />
              </button>

              <div className="pagination-pages">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => {
                  const isNearCurrent = Math.abs(page - currentPage) <= 1
                  const isEdge        = page === 1 || page === totalPages

                  if (!isNearCurrent && !isEdge) {
                    if (page === 2 || page === totalPages - 1) {
                      return <span key={page} className="pagination-ellipsis">…</span>
                    }
                    return null
                  }

                  return (
                    <button
                      key={page}
                      className={`pagination-page ${page === currentPage ? 'active' : ''}`}
                      onClick={() => goToPage(page)}
                    >
                      {page}
                    </button>
                  )
                })}
              </div>

              <button
                className="pagination-btn"
                onClick={() => goToPage(currentPage + 1)}
                disabled={currentPage === totalPages}
                aria-label="Next page"
              >
                <FaChevronRight />
              </button>
            </div>
          )}
        </div>
      )}

      {/* ── Course Detail View ──────────────────────────────── */}
      {selectedCourse && (
        <div className="course-details">

          {/* Back button */}
          <button
            className="btn-back"
            onClick={() => { setSelectedCourse(null); setOpenFlagDetail(false) }}
          >
            <FaArrowLeft /> {t('courses.backToResults')}
          </button>

          {/* Hero Card */}
          <div className="course-detail-hero">
            <div className="course-detail-hero-top">
              <div className="course-detail-code-block">
                <span className="course-detail-code">
                  {selectedCourse.subject} {selectedCourse.catalog}
                </span>
                <h2 className="course-detail-title">{selectedCourse.title}</h2>
              </div>

              {/* Action buttons */}
              <div className="course-detail-actions">
                <button
                  className={`course-detail-action-btn btn-save ${isFavorited(selectedCourse.subject, selectedCourse.catalog) ? 'active' : ''}`}
                  onClick={() => handleToggleFavorite(selectedCourse)}
                >
                  {isFavorited(selectedCourse.subject, selectedCourse.catalog)
                    ? <FaHeart /> : <FaRegHeart />}
                  {isFavorited(selectedCourse.subject, selectedCourse.catalog) ? 'Saved' : 'Save'}
                </button>
                <button
                  className={`course-detail-action-btn btn-done ${isCompleted(selectedCourse.subject, selectedCourse.catalog) ? 'active' : ''}`}
                  onClick={() => handleToggleCompleted(selectedCourse)}
                >
                  <FaCheckCircle />
                  {isCompleted(selectedCourse.subject, selectedCourse.catalog) ? 'Completed' : 'Done'}
                </button>
                <button
                  className={`course-detail-action-btn btn-current ${isCurrent(selectedCourse.subject, selectedCourse.catalog) ? 'active' : ''}`}
                  onClick={() => handleToggleCurrent(selectedCourse)}
                >
                  <FaBook />
                  {isCurrent(selectedCourse.subject, selectedCourse.catalog) ? 'Enrolled' : 'Enroll'}
                </button>
              </div>
            </div>

            {/* Stats row */}
            <div className="course-detail-stats">
              {selectedCourse.average && (
                <div className="course-detail-stat">
                  <FaTrophy className="course-detail-stat-icon" />
                  <span className="course-detail-stat-label">Recent GPA</span>
                  <span className="course-detail-stat-value gpa-value">
                    {parseFloat(selectedCourse.average).toFixed(2)}
                  </span>
                  <span className="course-detail-stat-sub">
                    ({gpaToLetterGrade(selectedCourse.average)})
                  </span>
                </div>
              )}
              {selectedCourse.overall_average && (
                <div className="course-detail-stat">
                  <FaChartBar className="course-detail-stat-icon" />
                  <span className="course-detail-stat-label">All-time Avg</span>
                  <span className="course-detail-stat-value">
                    {parseFloat(selectedCourse.overall_average).toFixed(2)}
                  </span>
                  <span className="course-detail-stat-sub">
                    ({gpaToLetterGrade(selectedCourse.overall_average)})
                  </span>
                </div>
              )}
              {selectedCourse.num_sections > 0 && (
                <div className="course-detail-stat">
                  <FaLayerGroup className="course-detail-stat-icon" />
                  <span className="course-detail-stat-label">Sections</span>
                  <span className="course-detail-stat-value">{selectedCourse.num_sections}</span>
                </div>
              )}
              {selectedCourse.rmp_rating && (
                <div className="course-detail-stat">
                  <FaStar
                    className="course-detail-stat-icon"
                    style={{ color: getRatingColor(selectedCourse.rmp_rating) }}
                  />
                  <span className="course-detail-stat-label">RMP Rating</span>
                  <span
                    className="course-detail-stat-value"
                    style={{ color: getRatingColor(selectedCourse.rmp_rating) }}
                  >
                    {selectedCourse.rmp_rating.toFixed(1)}
                  </span>
                  <span className="course-detail-stat-sub">/5.0</span>
                </div>
              )}
            </div>
          </div>

          {/* RMP Card */}
          {selectedCourse.rmp_rating && (
            <div className="course-detail-section">
              <div className="course-detail-section-header">
                <FaStar />
                <h3 className="course-detail-section-title">
                  {t('courses.professorRating')}
                </h3>
              </div>

              {selectedCourse.instructors?.[0] && (
                <div className="rmp-instructor-label">
                  <FaUser />
                  {selectedCourse.instructors[0]}
                </div>
              )}

              <div className="rmp-grid">
                <div className="rmp-grid-card">
                  <div className={`rmp-grid-value ${
                    selectedCourse.rmp_rating >= 4 ? 'good'
                    : selectedCourse.rmp_rating >= 3 ? 'ok'
                    : 'bad'
                  }`}>
                    {selectedCourse.rmp_rating.toFixed(1)}
                  </div>
                  <div className="rmp-grid-label">{t('courses.rating')}</div>
                </div>

                <div className="rmp-grid-card">
                  <div className={`rmp-grid-value ${
                    selectedCourse.rmp_difficulty <= 2.5 ? 'good'
                    : selectedCourse.rmp_difficulty <= 3.5 ? 'ok'
                    : 'bad'
                  }`}>
                    {selectedCourse.rmp_difficulty?.toFixed(1) ?? t('common.na')}
                  </div>
                  <div className="rmp-grid-label">{t('courses.difficulty')}</div>
                </div>

                <div className="rmp-grid-card">
                  <div className="rmp-grid-value">
                    {selectedCourse.rmp_num_ratings
                      ? Math.round(selectedCourse.rmp_num_ratings)
                      : t('common.na')}
                  </div>
                  <div className="rmp-grid-label">{t('courses.reviews')}</div>
                </div>

                <div className="rmp-grid-card">
                  <div className={`rmp-grid-value ${
                    selectedCourse.rmp_would_take_again >= 70 ? 'good'
                    : selectedCourse.rmp_would_take_again >= 50 ? 'ok'
                    : 'bad'
                  }`}>
                    {selectedCourse.rmp_would_take_again != null
                      ? `${Math.round(selectedCourse.rmp_would_take_again)}%`
                      : t('common.na')}
                  </div>
                  <div className="rmp-grid-label">{t('courses.wouldRetake')}</div>
                </div>
              </div>
            </div>
          )}

          {/* Grade Trend Card */}
          {selectedCourse.grade_trend?.length > 0 && (
            <div className="course-detail-section">
              <div className="course-detail-section-header">
                <FaChartBar />
                <h3 className="course-detail-section-title">Grade History</h3>
                <span className="course-detail-section-count">
                  {selectedCourse.grade_trend.length} year{selectedCourse.grade_trend.length !== 1 ? 's' : ''}
                </span>
              </div>
              <div className="grade-trend-list">
                {selectedCourse.grade_trend.map((entry, idx) => {
                  const gpa    = parseFloat(entry.average)
                  const barPct = Math.min(100, (gpa / 4.0) * 100)
                  return (
                    <div key={idx} className="grade-trend-row">
                      <span className="grade-trend-year">{entry.year}</span>
                      <div className="grade-trend-bar-wrap">
                        <div
                          className="grade-trend-bar"
                          style={{ width: `${barPct}%` }}
                        />
                      </div>
                      <span className="grade-trend-gpa">{gpa.toFixed(2)}</span>
                      <span className="grade-trend-letter">
                        {gpaToLetterGrade(gpa)}
                      </span>
                      <span className="grade-trend-sections">
                        {entry.sections} section{entry.sections !== 1 ? 's' : ''}
                      </span>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

        </div>
      )}

      {/* No results */}
      {!searchResults.length && !selectedCourse && !searchError && !isSearching && hasSearched && (
        <div className="placeholder-content placeholder-content--empty">
          <div className="placeholder-icon placeholder-icon--muted"><FaSearch /></div>
          <h3>{language === 'fr' ? 'Aucun résultat' : 'No results found'}</h3>
          <p>
            {language === 'fr'
              ? `Aucun cours trouvé pour "${searchQuery}". Essayez un code de cours (ex. COMP 202) ou un mot-clé du titre.`
              : `No courses found for "${searchQuery}". Try a course code (e.g. COMP 202) or a keyword from the title.`}
          </p>
        </div>
      )}

      {/* Initial placeholder */}
      {!searchResults.length && !selectedCourse && !searchError && !isSearching && !hasSearched && (
        <div className="placeholder-content">
          <div className="placeholder-icon"><FaBook /></div>
          <h3>{t('courses.explorerTitle')}</h3>
          <p>{t('courses.explorerDesc')}</p>
        </div>
      )}
    </div>
  )
}
