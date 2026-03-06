import { useState } from 'react'
import { FaStar, FaSearch } from 'react-icons/fa'
import SavedCoursesView from './SavedCoursesView'
import CoursesTab from './CoursesTab'
import './DegreePlanningView.css'
import './CoursesView.css'

export default function CoursesView({
  // SavedCoursesView props
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
  // CoursesTab props
  searchQuery,
  setSearchQuery,
  searchResults,
  setSearchResults,
  isSearching,
  searchError,
  selectedCourse,
  setSelectedCourse,
  isLoadingCourse,
  sortBy,
  setSortBy,
  sortCourses,
  isFavorited,
  isCompleted,
  isCurrent,
  handleCourseSearch,
  handleCourseClick,
  handleToggleFavorite,
  handleToggleCompleted,
  handleToggleCurrent,
  gpaToLetterGrade,
  searchCorrection,
  onSearchWithCorrection,
  hasSearched,
  defaultSubTab = 'course_search',
}) {
  const [subTab, setSubTab] = useState(defaultSubTab)

  const totalMyCourses =
    favorites.length + completedCourses.length + currentCourses.length

  return (
    <div className="courses-view">
      {/* ── Sub-tab bar ── */}
      <div className="dp-subtab-bar">
        <button
          className={`dp-subtab-btn ${subTab === 'my_courses' ? 'dp-subtab-btn--active' : ''}`}
          onClick={() => setSubTab('my_courses')}
        >
          <FaStar className="dp-subtab-icon" />
          <span>My Courses</span>
          {totalMyCourses > 0 && (
            <span className="dp-subtab-count">{totalMyCourses}</span>
          )}
        </button>

        <button
          className={`dp-subtab-btn ${subTab === 'course_search' ? 'dp-subtab-btn--active' : ''}`}
          onClick={() => setSubTab('course_search')}
        >
          <FaSearch className="dp-subtab-icon" />
          <span>Course Search</span>
        </button>
      </div>

      {/* ── My Courses — unmount when not active ── */}
      {subTab === 'my_courses' && (
        <div className="courses-my-panel">
          <SavedCoursesView
            favorites={favorites}
            completedCourses={completedCourses}
            currentCourses={currentCourses}
            completedCoursesMap={completedCoursesMap}
            currentCoursesMap={currentCoursesMap}
            favoritesMap={favoritesMap}
            onToggleFavorite={onToggleFavorite}
            onToggleCompleted={onToggleCompleted}
            onToggleCurrent={onToggleCurrent}
            onCourseClick={onCourseClick}
          />
        </div>
      )}

      {/* ── Course Search — always mounted to preserve search state ── */}
      <div
        className="courses-search-panel"
        style={{ display: subTab === 'course_search' ? 'block' : 'none' }}
      >
        <CoursesTab
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          searchResults={searchResults}
          setSearchResults={setSearchResults}
          isSearching={isSearching}
          searchError={searchError}
          selectedCourse={selectedCourse}
          setSelectedCourse={setSelectedCourse}
          isLoadingCourse={isLoadingCourse}
          sortBy={sortBy}
          setSortBy={setSortBy}
          sortCourses={sortCourses}
          isFavorited={isFavorited}
          isCompleted={isCompleted}
          isCurrent={isCurrent}
          handleCourseSearch={handleCourseSearch}
          handleCourseClick={handleCourseClick}
          searchCorrection={searchCorrection}
          onSearchWithCorrection={onSearchWithCorrection}
          hasSearched={hasSearched}
          handleToggleFavorite={handleToggleFavorite}
          handleToggleCompleted={handleToggleCompleted}
          handleToggleCurrent={handleToggleCurrent}
          gpaToLetterGrade={gpaToLetterGrade}
        />
      </div>
    </div>
  )
}
