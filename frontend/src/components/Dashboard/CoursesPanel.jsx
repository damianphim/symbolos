import { useState } from 'react'
import { normalizeQuery, buildCorrectionCandidates } from '../../utils/fuzzySearch'
import coursesAPI           from '../../lib/professorsAPI'
import ProfessorRating     from '../ProfessorRating/ProfessorRating'
import { gpaToLetterGrade } from '../../utils/gpaUtils'
import { FaChartBar, FaBook } from 'react-icons/fa'
import './CoursesPanel.css'

export default function CoursesPanel() {
  const [searchQuery,    setSearchQuery]    = useState('')
  const [searchResults,  setSearchResults]  = useState([])
  const [isSearching,    setIsSearching]    = useState(false)
  const [searchError,    setSearchError]    = useState(null)
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [isLoadingCourse,setIsLoadingCourse]= useState(false)
  const [correction, setCorrection] = useState(null)

  // ── search ────────────────────────────────────────────────────────
  const doSearch = async (rawQuery) => {
    setIsSearching(true)
    setSearchError(null)
    setCorrection(null)
    setSelectedCourse(null)
    try {
      const normalized = normalizeQuery(rawQuery)
      const data = await coursesAPI.search(normalized, null, 100)
      const courses = data.courses || data || []

      if (Array.isArray(courses) && courses.length > 0) {
        setSearchResults(courses)
        return
      }

      // Zero results — try fuzzy correction
      const candidates = buildCorrectionCandidates(rawQuery)
      for (const candidate of candidates) {
        const retry = await coursesAPI.search(candidate.query, null, 100)
        const list = retry.courses || retry || []
        if (Array.isArray(list) && list.length > 0) {
          setCorrection({ original: rawQuery, corrected: candidate.note })
          setSearchResults(list)
          return
        }
      }

      setSearchResults([])
      setSearchError('No courses found matching your search.')
    } catch (err) {
      console.error('Course search error:', err)
      setSearchError('Failed to search courses. Please try again.')
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!searchQuery.trim()) return
    doSearch(searchQuery)
  }

  // ── detail ────────────────────────────────────────────────────────
  const handleCourseClick = async (course) => {
    setIsLoadingCourse(true)
    setSelectedCourse(null)
    try {
      const data = await coursesAPI.getDetails(course.subject, course.catalog)
      setSelectedCourse(data.course)
    } catch (err) {
      console.error('Error loading course details:', err)
      setSearchError('Failed to load course details.')
    } finally {
      setIsLoadingCourse(false)
    }
  }

  // ── render ────────────────────────────────────────────────────────
  return (
    <div className="courses-container">
      <form className="search-section" onSubmit={handleSearch}>
        <input
          type="text"
          className="search-input"
          placeholder="Search for courses (e.g., COMP 202, Introduction to Programming)..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="btn btn-search" disabled={isSearching || !searchQuery.trim()}>
          Search
        </button>
      </form>

      {searchError && <div className="error-banner">{searchError}</div>}
      {correction && (
        <div className="search-correction-banner">
          Did you mean{' '}
          <button className="search-correction-link" onClick={() => { setSearchQuery(correction.corrected); doSearch(correction.corrected) }}>
            {correction.corrected}
          </button>?
          {' '}Showing results for "{correction.corrected}".
        </div>
      )}

      {/* Result list */}
      {searchResults.length > 0 && !selectedCourse && (
        <div className="search-results">
          <h3 className="results-header">
            Found {searchResults.length} course{searchResults.length !== 1 ? 's' : ''}
          </h3>
          <div className="course-list">
            {searchResults.map(course => (
              <div
                key={`${course.subject}-${course.catalog}`}
                className="course-card"
                onClick={() => handleCourseClick(course)}
              >
                <div className="course-header">
                  <div className="course-code">{course.subject} {course.catalog}</div>
                  {course.average && (
                    <div className="course-average">
                      {course.average.toFixed(1)} GPA ({gpaToLetterGrade(course.average)})
                    </div>
                  )}
                </div>
                <h4 className="course-title">{course.title}</h4>
                {course.sections && (
                  <div className="course-meta">
                    <FaChartBar className="meta-icon" /> {course.sections.length} section{course.sections.length !== 1 ? 's' : ''} available
                  </div>
                )}
              </div>
            ))}
          </div>
          <button className="btn-back" onClick={() => { setSearchResults([]); setSearchQuery('') }}>
            ← New Search
          </button>
        </div>
      )}

      {/* Detail view */}
      {selectedCourse && (
        <div className="course-details">
          <button className="btn-back" onClick={() => setSelectedCourse(null)}>← Back to Results</button>

          <div className="course-details-header">
            <h2 className="course-details-title">
              {selectedCourse.subject} {selectedCourse.catalog}: {selectedCourse.title}
            </h2>
            {selectedCourse.average_grade && (
              <div className="course-stat-badge">
                 {selectedCourse.average_grade} GPA ({gpaToLetterGrade(selectedCourse.average_grade)})
              </div>
            )}
          </div>

          <div className="course-sections">
            <h3 className="sections-header">Sections ({selectedCourse.num_sections})</h3>
            {selectedCourse.sections.map((section, idx) => (
              <div key={idx} className="section-card">
                <div className="section-info">
                  <div className="section-header">
                    <span className="section-term">{section.term || 'N/A'}</span>
                    {section.average && (
                      <span className="section-average">
                        {section.average} GPA ({gpaToLetterGrade(section.average)})
                      </span>
                    )}
                  </div>
                  {section.instructor && section.instructor !== 'TBA' && (
                    <div className="section-instructor">
                      <strong>Instructor:</strong> {section.instructor}
                    </div>
                  )}
                </div>
                {section.professor_rating && <ProfessorRating rating={section.professor_rating} />}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty / placeholder */}
      {!searchResults.length && !selectedCourse && !searchError && !isSearching && (
        <div className="placeholder-content">
          <div className="placeholder-icon"><FaBook /></div>
          <h3>Course Explorer with Professor Ratings</h3>
          <p>Search through McGill courses with historical grade data and live RateMyProfessor ratings.</p>
        </div>
      )}
    </div>
  )
}
