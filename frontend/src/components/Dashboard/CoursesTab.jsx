import { useState } from 'react'
import {
  FaHeart, FaRegHeart, FaCheckCircle, FaStar, FaBook,
  FaUser, FaChevronLeft, FaChevronRight, FaCalendarAlt,
  FaExternalLinkAlt, FaInfoCircle, FaSearch,
} from 'react-icons/fa'
import { MdOutlineRateReview } from 'react-icons/md'
import { useLanguage } from '../../contexts/PreferencesContext'
import { useCourseDetail } from '../../contexts/CourseDetailContext'
import {
  getRatingColor, getDifficultyColor, getBestRating, getTotalReviews,
} from '../../utils/courseRatings'
import Skeleton from '../ui/Skeleton'
import EmptyState from '../ui/EmptyState'
import './CoursesTab.css'

const PAGE_SIZE = 10

export default function CoursesTab({
  searchQuery, setSearchQuery,
  searchResults,
  isSearching, searchError,
  handleCourseSearch,
  sortBy, setSortBy, sortCourses,
  searchTerm, setSearchTerm, availableTerms = [],
  isFavorited, isCompleted, isCurrent,
  handleToggleFavorite, handleToggleCompleted, handleToggleCurrent,
  gpaToLetterGrade,
  searchCorrection, hasSearched,
}) {
  const { t, language } = useLanguage()
  // Detail viewing goes through the shared CourseDetailModal (mounted once in
  // Dashboard) — same overlay the My Courses tab uses, so both entry points
  // share one detail UI.
  const { openCourse } = useCourseDetail()
  const [currentPage, setCurrentPage] = useState(1)

  const handleSortChange = (val) => { setSortBy(val); setCurrentPage(1) }
  const handleSearch     = (e)   => { setCurrentPage(1); handleCourseSearch(e) }

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

      {/* ── Filters (always visible) ────────────────────────── */}
      <div className="courses-filter-bar">
        {availableTerms.length > 0 && setSearchTerm && (
          <div className="filter-group">
            <label htmlFor="term-select" className="sort-label">{t('courses.semester')}</label>
            <select
              id="term-select"
              className="sort-select"
              value={searchTerm || ''}
              onChange={(e) => { setCurrentPage(1); setSearchTerm(e.target.value) }}
            >
              <option value="">{t('courses.allSemesters')}</option>
              {availableTerms.map(tm => <option key={tm} value={tm}>{tm}</option>)}
            </select>
          </div>
        )}
        <div className="filter-group">
          <label htmlFor="sort-select" className="sort-label">{t('courses.sortBy')}</label>
          <select id="sort-select" className="sort-select" value={sortBy} onChange={(e) => handleSortChange(e.target.value)}>
            <option value="relevance">{t('courses.relevance')}</option>
            <option value="rating-high">{t('courses.sortRatingHigh')}</option>
            <option value="rating-low">{t('courses.sortRatingLow')}</option>
            <option value="number">{t('courses.sortNumber')}</option>
            <option value="grade-high">{t('courses.sortGradeHigh')}</option>
          </select>
        </div>
      </div>

      {/* ── VSB Banner ──────────────────────────────────────── */}
      <a
        href={`https://vsb.mcgill.ca/criteria.jsp?access=0&lang=${language === 'fr' ? 'fr' : 'en'}&tip=2&page=criteria&scratch=0&advice=0&legend=1&term=202601&sort=none&filters=iiiiiiiiii&bbs=&ds=&cams=OFF-CAMPUS_DISTANCE_DOWNTOWN_MACDONALD&locs=any&isrts=any&ses=any&pl=&pac=1`}
        target="_blank"
        rel="noopener noreferrer"
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

      {searchError && <div className="error-banner">{searchError}</div>}

      {/* ── Loading skeletons ───────────────────────────────── */}
      {isSearching && (
        <div className="course-list">
          {[0, 1, 2, 3].map(i => (
            <div key={i} className="course-card course-card--skeleton">
              <Skeleton width="8rem" height="1.1rem" />
              <Skeleton width="60%" height="1rem" />
              <Skeleton width="40%" height="0.85rem" />
            </div>
          ))}
        </div>
      )}

      {/* ── Results list ────────────────────────────────────── */}
      {searchResults.length > 0 && !isSearching && (
        <div className="search-results">
          {/* Typo-correction notice — Dashboard already auto-applied the
              corrected query; this just tells the user what happened. */}
          {searchCorrection && (
            <div className="search-correction-banner">
              <FaInfoCircle />
              <span>
                {t('courses.correctionPrefix')}{' '}
                <strong>{searchCorrection.corrected}</strong>{' '}
                {t('courses.correctionSuffix').replace('{original}', searchCorrection.original)}
              </span>
            </div>
          )}

          <div className="results-header-bar">
            <h3 className="results-header">
              {searchResults.length === 1
                ? t('courses.foundResults').replace('{count}', searchResults.length)
                : t('courses.foundResultsPlural').replace('{count}', searchResults.length)}
              {totalPages > 1 && (
                <span className="results-page-info">, page {currentPage} of {totalPages}</span>
              )}
            </h3>
          </div>

          <div className="course-list">
            {pageResults.map((course) => {
              const cardKey     = `${course.subject}-${course.catalog}`
              const rating      = getBestRating(course)
              const reviews     = getTotalReviews(course)
              const ratingColor = getRatingColor(rating)
              const diffColor   = getDifficultyColor(course.rmp_difficulty)

              return (
                <div key={cardKey} className="course-card">
                  <div className="course-card-content" onClick={() => openCourse(course.subject, course.catalog)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      {course.average != null && (
                        <div className="course-average">
                          {course.average.toFixed(1)} GPA ({gpaToLetterGrade(course.average)})
                        </div>
                      )}
                    </div>
                    <h4 className="course-title">{course.title}</h4>

                    {course.term_instructor && (
                      <div className="course-term-prof">
                        <FaUser /> {searchTerm}: <strong>{course.term_instructor}</strong>
                        {course.prof_historical_avg != null ? (
                          <span className="term-prof-avg">
                            {' · '}{t('courses.profHistAvg')}: {course.prof_historical_avg.toFixed(1)} ({gpaToLetterGrade(course.prof_historical_avg)}
                            {course.prof_historical_n ? `, ${course.prof_historical_n}` : ''})
                          </span>
                        ) : (
                          <span className="term-prof-avg term-prof-avg--none">{' · '}{t('courses.profNoHist')}</span>
                        )}
                      </div>
                    )}

                    {course.instructor && (
                      <div className="course-instructor-section">
                        <div className="instructor-name"><FaUser /> {course.instructor}</div>
                        {rating && (
                          <div className="rmp-compact">
                            <div className="rmp-stat" title={reviews ? t('courses.ratingsCount').replace('{n}', reviews) : undefined}>
                              <span className="rmp-label" style={{ color: ratingColor }}>
                                <FaStar style={{ color: ratingColor }} /> {t('courses.rating')}:
                              </span>
                              <span className="rmp-value" style={{ color: ratingColor }}>{rating.toFixed(1)}/5.0</span>
                              {reviews && <span className="rmp-reviews">· {reviews}</span>}
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

      {/* ── No results ──────────────────────────────────────── */}
      {hasSearched && !isSearching && !searchError && searchResults.length === 0 && (
        <EmptyState
          icon={<FaSearch />}
          title={t('courses.noResultsTitle')}
          subtitle={t('courses.noResultsDesc')}
        />
      )}

      {/* ── Pre-search placeholder ──────────────────────────── */}
      {!hasSearched && !searchError && !isSearching && (
        <div className="placeholder-content">
          <div className="placeholder-icon"><FaBook /></div>
          <h3>{t('courses.explorerTitle')}</h3>
          <p>{t('courses.explorerDesc')}</p>
        </div>
      )}
    </div>
  )
}
