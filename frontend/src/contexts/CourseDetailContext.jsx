import { createContext, useContext, useState, useCallback } from 'react'
import { coursesAPI } from '../lib/api'

const CourseDetailContext = createContext(null)

export function CourseDetailProvider({ children }) {
  const [course,    setCourse]    = useState(null)   // full course data object
  const [loading,   setLoading]   = useState(false)
  const [error,     setError]     = useState(null)

  const openCourse = useCallback(async (subject, catalog) => {
    if (!subject || !catalog) return
    setLoading(true)
    setError(null)
    setCourse({ subject, catalog, _loading: true })   // open modal immediately with skeleton
    try {
      const data = await coursesAPI.getDetails(subject, catalog)
      setCourse(data.course || data)
    } catch (err) {
      console.error('CourseDetailModal fetch error:', err)
      setError('Failed to load course details.')
      setCourse(null)
    } finally {
      setLoading(false)
    }
  }, [])

  const closeCourse = useCallback(() => {
    setCourse(null)
    setError(null)
  }, [])

  return (
    <CourseDetailContext.Provider value={{ course, loading, error, openCourse, closeCourse }}>
      {children}
    </CourseDetailContext.Provider>
  )
}

export const useCourseDetail = () => {
  const ctx = useContext(CourseDetailContext)
  if (!ctx) throw new Error('useCourseDetail must be used within CourseDetailProvider')
  return ctx
}
