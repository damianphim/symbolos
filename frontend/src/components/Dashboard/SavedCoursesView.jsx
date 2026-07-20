import { useState } from 'react'
import { FaHeart, FaRegHeart, FaCheckCircle, FaCheck, FaStar, FaBook, FaExternalLinkAlt, FaCalendarAlt } from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import { useCourseDetail } from '../../contexts/CourseDetailContext'
import { groupCoursesByTerm } from '../../lib/termDates'
import './SavedCoursesView.css'

export default function SavedCoursesView({
  favorites = [],
  completedCourses = [],
  currentCourses = [],
  completedCoursesMap = new Set(),
  currentCoursesMap = new Set(),
  favoritesMap = new Set(),
  onToggleFavorite,
  onToggleCompleted,
  onToggleCurrent,
  defaultTab = 'saved',
}) {
  const { t, language } = useLanguage()
  const { openCourse } = useCourseDetail()
  const [activeView, setActiveView] = useState(defaultTab)

  const isCompleted = (subject, catalog) => completedCoursesMap.has(`${subject} ${catalog}`)
  const isCurrent   = (subject, catalog) => currentCoursesMap.has(`${subject} ${catalog}`)
  const isFavorited = (subject, catalog) => favoritesMap.has(`${subject} ${catalog}`)

  return (
    <div className="saved-courses-view">
      {/* Tab Navigation */}
      <div className="saved-tabs">
        <button
          className={`saved-tab ${activeView === 'saved' ? 'active' : ''}`}
          onClick={() => setActiveView('saved')}
        >
          <span className="tab-icon"><FaStar /></span>
          <span className="tab-label">{t('saved.savedCourses')}</span>
          {favorites.length > 0 && <span className="tab-count">{favorites.length}</span>}
        </button>

        <button
          className={`saved-tab ${activeView === 'current' ? 'active' : ''}`}
          onClick={() => setActiveView('current')}
        >
          <span className="tab-icon"><FaBook /></span>
          <span className="tab-label">{t('saved.pillCurrent')}</span>
          {currentCourses.length > 0 && <span className="tab-count">{currentCourses.length}</span>}
        </button>

        <button
          className={`saved-tab ${activeView === 'completed' ? 'active' : ''}`}
          onClick={() => setActiveView('completed')}
        >
          <span className="tab-icon"><FaCheck /></span>
          <span className="tab-label">{t('saved.completed')}</span>
          {completedCourses.length > 0 && <span className="tab-count">{completedCourses.length}</span>}
        </button>
      </div>

      {/* ── VSB Banner ──────────────────────────────────────── */}
      <a
        href={`https://vsb.mcgill.ca/criteria.jsp?access=0&lang=${language === 'fr' ? 'fr' : 'en'}&tip=2&page=criteria&scratch=0&advice=0&legend=1&term=202601&sort=none&filters=iiiiiiiiii&bbs=&ds=&cams=OFF-CAMPUS_DISTANCE_DOWNTOWN_MACDONALD&locs=any&isrts=any&ses=any&pl=&pac=1`}
        target="_blank"
        rel="noreferrer"
        className="vsb-banner m-group m-row m-row--tappable"
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

      {/* Saved Courses */}
      {activeView === 'saved' && (
        <div className="saved-courses-content">
          {favorites.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon"><FaStar /></div>
              <h3>{t('saved.noSavedCourses')}</h3>
              <p>{t('saved.noSavedCoursesDesc')}</p>
            </div>
          ) : (
            <div className="course-list m-group">
              {favorites.map((course, idx) => (
                <div key={idx} className="course-card m-row m-row--tappable">
                  <div className="course-card-content" onClick={() => openCourse(course.subject, course.catalog)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                    </div>
                    <h4 className="course-title">{course.course_title}</h4>
                  </div>
                  <div className="course-card-actions">
                    <button
                      className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`}
                      onClick={(e) => { e.stopPropagation(); onToggleFavorite?.({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      title={isFavorited(course.subject, course.catalog) ? t('courses.removeFromSaved') : t('courses.addToSaved')}
                    >
                      <FaHeart className="favorite-icon" /> <span className="action-pill-label">{t('saved.pillSaved')}</span>
                    </button>
                    {onToggleCompleted && (
                      <button
                        className={`completed-btn ${isCompleted(course.subject, course.catalog) ? 'completed' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleCompleted({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isCompleted(course.subject, course.catalog) ? t('saved.tipMarkIncomplete') : t('courses.markCompleted')}
                      >
                        <FaCheckCircle className="completed-icon" /> <span className="action-pill-label">{t('saved.completed')}</span>
                      </button>
                    )}
                    {onToggleCurrent && (
                    <button
                      className={`current-btn ${isCurrent(course.subject, course.catalog) ? 'current' : ''}`}
                      onClick={(e) => { e.stopPropagation(); onToggleCurrent({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      disabled={isCompleted(course.subject, course.catalog) && !isCurrent(course.subject, course.catalog)}
                      title={
                        isCompleted(course.subject, course.catalog) && !isCurrent(course.subject, course.catalog)
                          ? t('saved.tipAlreadyCompleted')
                          : isCurrent(course.subject, course.catalog)
                          ? t('saved.tipRemoveCurrent')
                          : t('saved.tipAddCurrent')
                      }
                    >
                      <FaBook className="current-icon" /> <span className="action-pill-label">{t('saved.pillCurrent')}</span>
                    </button>
                  )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Current Courses */}
      {activeView === 'current' && (
        <div className="saved-courses-content">
          {currentCourses.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon"><FaBook /></div>
              <h3>{t('saved.noCurrentCourses')}</h3>
              <p>{t('saved.noCurrentCoursesDesc')}</p>
            </div>
          ) : (
            groupCoursesByTerm(currentCourses).map(group => (
            <div key={group.key} className="course-list" style={{ marginBottom: 18 }}>
              <div className="term-group-header" style={{
                display: 'flex', alignItems: 'center', gap: 8,
                margin: '4px 2px 10px', fontWeight: 700, fontSize: 14,
                gridColumn: '1 / -1',
              }}>
                <FaCalendarAlt style={{ opacity: 0.6 }} />
                <span>{group.key === 'Term not set' ? t('saved.termNotSet') : group.key}</span>
                <span style={{
                  fontSize: 11, fontWeight: 600, padding: '2px 8px', borderRadius: 999,
                  background: group.isActive ? '#dcfce7' : '#f1f5f9',
                  color: group.isActive ? '#15803d' : '#64748b',
                }}>
                  {group.isActive ? t('saved.currentTerm') : t('saved.upcoming')}
                </span>
              </div>
              {/* The term header must stay a direct child of the auto-fill grid
                  on desktop (it relies on `grid-column: 1 / -1`), so the cards
                  get their own wrapper instead of the header being lifted out.
                  `.saved-term-group` is `display: contents` on desktop — the
                  grid sees the cards exactly as before — and becomes the
                  raised `.m-group` surface only inside `.mobile-shell`. */}
              <div className="saved-term-group m-group">
              {group.courses.map((course, idx) => (
                <div key={idx} className="course-card m-row m-row--tappable">
                  <div className="course-card-content" onClick={() => openCourse(course.subject, course.catalog)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      {group.isActive ? (
                        <div className="course-grade-badge" style={{ background: '#dbeafe', color: '#1d4ed8' }}>{t('saved.pillCurrent')}</div>
                      ) : (
                        <div className="course-grade-badge" style={{ background: '#f1f5f9', color: '#64748b' }}>{t('saved.upcoming')}</div>
                      )}
                    </div>
                    <h4 className="course-title">{course.course_title}</h4>
                    {course.credits && (
                      <div className="course-meta">
                        <span className="course-credits">{t('saved.creditsCount').replace('{n}', course.credits)}</span>
                      </div>
                    )}
                  </div>
                  <div className="course-card-actions">
                    {onToggleFavorite && (
                      <button
                        className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleFavorite({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isFavorited(course.subject, course.catalog) ? t('courses.removeFromSaved') : t('courses.addToSaved')}
                      >
                        {isFavorited(course.subject, course.catalog)
                          ? <FaHeart className="favorite-icon" />
                          : <FaRegHeart className="favorite-icon" />}
                        {' '}<span className="action-pill-label">{t('saved.pillSaved')}</span>
                      </button>
                    )}
                    {onToggleCompleted && (
                      <button
                        className={`completed-btn ${isCompleted(course.subject, course.catalog) ? 'completed' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleCompleted({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isCompleted(course.subject, course.catalog) ? t('saved.tipMarkIncomplete') : t('courses.markCompleted')}
                      >
                        <FaCheckCircle className="completed-icon" /> <span className="action-pill-label">{t('saved.completed')}</span>
                      </button>
                    )}
                    <button
                      className={`current-btn ${isCurrent(course.subject, course.catalog) ? 'current' : ''}`}
                      onClick={(e) => { e.stopPropagation(); onToggleCurrent?.({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      title={t('saved.tipRemoveCurrent')}
                    >
                      <FaBook className="current-icon" /> <span className="action-pill-label">{t('saved.pillCurrent')}</span>
                    </button>
                  </div>
                </div>
              ))}
              </div>
            </div>
            ))
          )}
        </div>
      )}

      {/* Completed Courses */}
      {activeView === 'completed' && (
        <div className="completed-courses-content">
          {completedCourses.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon"><FaCheck /></div>
              <h3>{t('saved.noCompletedCourses')}</h3>
              <p>{t('saved.noCompletedCoursesDesc')}</p>
            </div>
          ) : (
            <div className="course-list m-group">
              {completedCourses.map((course, idx) => (
                <div key={idx} className="course-card completed-course-card m-row m-row--tappable">
                  <div className="course-card-content" onClick={() => openCourse(course.subject, course.catalog, course.term && course.year ? `${course.term} ${course.year}` : undefined)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      {course.grade && <div className="course-grade-badge">{course.grade}</div>}
                    </div>
                    <h4 className="course-title">{course.course_title}</h4>
                    {(course.term || course.year || course.credits) && (
                      <div className="course-meta">
                        {(course.term || course.year) && <span className="course-term">{course.term} {course.year}</span>}
                        {course.credits && <span className="course-credits"> • {t('saved.creditsCount').replace('{n}', course.credits)}</span>}
                      </div>
                    )}
                  </div>
                  <div className="course-card-actions">
                    {onToggleFavorite && (
                      <button
                        className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleFavorite({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isFavorited(course.subject, course.catalog) ? t('courses.removeFromSaved') : t('courses.addToSaved')}
                      >
                        {isFavorited(course.subject, course.catalog)
                          ? <FaHeart className="favorite-icon" />
                          : <FaRegHeart className="favorite-icon" />}
                        {' '}<span className="action-pill-label">{t('saved.pillSaved')}</span>
                      </button>
                    )}
                    <button
                      className="completed-btn completed"
                      onClick={(e) => { e.stopPropagation(); onToggleCompleted?.({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      title={t('saved.tipRemoveCompleted')}
                    >
                      <FaCheckCircle className="completed-icon" /> <span className="action-pill-label">{t('saved.completed')}</span>
                    </button>
                    {onToggleCurrent && (
                      <button
                        className={`current-btn ${isCurrent(course.subject, course.catalog) ? 'current' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleCurrent({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isCurrent(course.subject, course.catalog) ? t('saved.tipRemoveCurrent') : t('saved.tipMarkCurrent')}
                      >
                        <FaBook className="current-icon" /> <span className="action-pill-label">{t('saved.pillCurrent')}</span>
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
