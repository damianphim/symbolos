import { useState } from 'react'
import { FaHeart, FaRegHeart, FaCheckCircle, FaCheck, FaStar, FaBook, FaExternalLinkAlt, FaCalendarAlt } from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
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
  onCourseClick,
}) {
  const { t, language } = useLanguage()
  const [activeView, setActiveView] = useState('saved')

  const isCompleted = (subject, catalog) => completedCoursesMap.has(`${subject} ${catalog}`)
  const isCurrent   = (subject, catalog) => currentCoursesMap.has(`${subject} ${catalog}`)
  const isFavorited = (subject, catalog) => favoritesMap.has(`${subject}${catalog}`)

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
          <span className="tab-label">Current</span>
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

      {/* Saved Courses */}
      {activeView === 'saved' && (
        <div className="saved-courses-content">
          {favorites.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon"><FaStar /></div>
              <h3>No Saved Courses Yet</h3>
              <p>Save courses from the Course Explorer to see them here</p>
            </div>
          ) : (
            <div className="course-list">
              {favorites.map((course, idx) => (
                <div key={idx} className="course-card">
                  <div className="course-card-content" onClick={() => onCourseClick?.(course)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                    </div>
                    <h4 className="course-title">{course.course_title}</h4>
                  </div>
                  <div className="course-card-actions">
                    <button
                      className="favorite-btn favorited"
                      onClick={(e) => { e.stopPropagation(); onToggleFavorite?.({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      title="Remove from favorites"
                    >
                      <FaHeart className="favorite-icon" />
                    </button>
                    {onToggleCompleted && (
                      <button
                        className={`completed-btn ${isCompleted(course.subject, course.catalog) ? 'completed' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleCompleted({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isCompleted(course.subject, course.catalog) ? 'Mark as incomplete' : 'Mark as completed'}
                      >
                        <FaCheckCircle className="completed-icon" />
                      </button>
                    )}
                    {onToggleCurrent && (
                    <button
                      className={`current-btn ${isCurrent(course.subject, course.catalog) ? 'current' : ''}`}
                      onClick={(e) => { e.stopPropagation(); onToggleCurrent({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      disabled={isCompleted(course.subject, course.catalog) && !isCurrent(course.subject, course.catalog)}
                      title={
                        isCompleted(course.subject, course.catalog) && !isCurrent(course.subject, course.catalog)
                          ? 'Already in completed courses'
                          : isCurrent(course.subject, course.catalog)
                          ? 'Remove from current courses'
                          : 'Add to current courses'
                      }
                    >
                      <FaBook className="current-icon" />
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
              <h3>No Current Courses</h3>
              <p>Add courses you're enrolled in this semester from the Course Explorer</p>
            </div>
          ) : (
            <div className="course-list">
              {currentCourses.map((course, idx) => (
                <div key={idx} className="course-card">
                  <div className="course-card-content" onClick={() => onCourseClick?.(course)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      <div className="course-grade-badge" style={{ background: '#dbeafe', color: '#1d4ed8' }}>Current</div>
                    </div>
                    <h4 className="course-title">{course.course_title}</h4>
                    {course.credits && (
                      <div className="course-meta">
                        <span className="course-credits">{course.credits} credits</span>
                      </div>
                    )}
                  </div>
                  <div className="course-card-actions">
                    {onToggleFavorite && (
                      <button
                        className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleFavorite({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isFavorited(course.subject, course.catalog) ? 'Remove from favorites' : 'Add to favorites'}
                      >
                        {isFavorited(course.subject, course.catalog)
                          ? <FaHeart className="favorite-icon" />
                          : <FaRegHeart className="favorite-icon" />}
                      </button>
                    )}
                    {onToggleCompleted && (
                      <button
                        className={`completed-btn ${isCompleted(course.subject, course.catalog) ? 'completed' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleCompleted({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isCompleted(course.subject, course.catalog) ? 'Mark as incomplete' : 'Mark as completed'}
                      >
                        <FaCheckCircle className="completed-icon" />
                      </button>
                    )}
                    <button
                      className="current-btn current"
                      onClick={(e) => { e.stopPropagation(); onToggleCurrent?.({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      title="Remove from current courses"
                    >
                      <FaBook className="current-icon" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Completed Courses */}
      {activeView === 'completed' && (
        <div className="completed-courses-content">
          {completedCourses.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon"><FaCheck /></div>
              <h3>No Completed Courses Yet</h3>
              <p>Mark courses as completed to track your progress</p>
            </div>
          ) : (
            <div className="course-list">
              {completedCourses.map((course, idx) => (
                <div key={idx} className="course-card completed-course-card">
                  <div className="course-card-content" onClick={() => onCourseClick?.(course)}>
                    <div className="course-header">
                      <div className="course-code">{course.subject} {course.catalog}</div>
                      {course.grade && <div className="course-grade-badge">{course.grade}</div>}
                    </div>
                    <h4 className="course-title">{course.course_title}</h4>
                    {(course.term || course.year || course.credits) && (
                      <div className="course-meta">
                        {(course.term || course.year) && <span className="course-term">{course.term} {course.year}</span>}
                        {course.credits && <span className="course-credits"> • {course.credits} credits</span>}
                      </div>
                    )}
                  </div>
                  <div className="course-card-actions">
                    {onToggleFavorite && (
                      <button
                        className={`favorite-btn ${isFavorited(course.subject, course.catalog) ? 'favorited' : ''}`}
                        onClick={(e) => { e.stopPropagation(); onToggleFavorite({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                        title={isFavorited(course.subject, course.catalog) ? 'Remove from favorites' : 'Add to favorites'}
                      >
                        {isFavorited(course.subject, course.catalog)
                          ? <FaHeart className="favorite-icon" />
                          : <FaRegHeart className="favorite-icon" />}
                      </button>
                    )}
                    <button
                      className="completed-btn completed"
                      onClick={(e) => { e.stopPropagation(); onToggleCompleted?.({ subject: course.subject, catalog: course.catalog, title: course.course_title }) }}
                      title="Remove from completed"
                    >
                      <FaCheckCircle className="completed-icon" />
                    </button>
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
