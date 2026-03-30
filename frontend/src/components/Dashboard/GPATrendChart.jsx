import { useMemo } from 'react'
import { FaChartBar } from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import './GPATrendChart.css'

export default function GPATrendChart({ completedCourses, currentGPA }) {
  const { t } = useLanguage()
  
  // Calculate GPA per semester from completed courses
  const semesterData = useMemo(() => {
    if (!completedCourses || completedCourses.length === 0) {
      // If no completed courses but there's a current GPA, show just that
      if (currentGPA) {
        return [{
          label: t('gpa.currentGpaLabel'),
          shortLabel: t('gpa.current'),
          semesterNumber: 1,
          gpa: parseFloat(currentGPA).toFixed(2),
          courses: 0,
          isCurrent: true
        }]
      }
      return []
    }

    // Group courses by semester
    const semesterMap = new Map()
    
    completedCourses.forEach(course => {
      if (!course.term || !course.year) return
      
      // Skip courses without grades (add/drop)
      if (!course.grade) return
      
      const semesterKey = `${course.term} ${course.year}`
      
      if (!semesterMap.has(semesterKey)) {
        semesterMap.set(semesterKey, {
          term: course.term,
          year: course.year,
          courses: [],
          sortKey: getSortKey(course.term, course.year)
        })
      }
      
      semesterMap.get(semesterKey).courses.push(course)
    })

    // Sort semesters chronologically
    const sortedSemesters = Array.from(semesterMap.values())
      .sort((a, b) => a.sortKey - b.sortKey)

    // Calculate CUMULATIVE GPA for each semester
    let cumulativeTotalPoints = 0
    let cumulativeTotalCredits = 0
    
    const semesters = sortedSemesters.map((semester, idx) => {
      // Add this semester's courses to cumulative totals
      semester.courses.forEach(course => {
        const gradePoints = getGradePoints(course.grade)
        const credits = course.credits || 3
        
        if (gradePoints !== null) {
          cumulativeTotalPoints += gradePoints * credits
          cumulativeTotalCredits += credits
        }
      })
      
      // Calculate cumulative GPA up to this point
      const cumulativeGPA = cumulativeTotalCredits > 0 
        ? (cumulativeTotalPoints / cumulativeTotalCredits).toFixed(2) 
        : '0.00'
      
      return {
        label: `${semester.term} ${semester.year}`,
        shortLabel: `${semester.term} '${semester.year.toString().slice(-2)}`,
        semesterNumber: idx + 1,
        gpa: cumulativeGPA,
        courses: semester.courses.length,
        totalCourses: cumulativeTotalCredits / 3, // Approximate total courses
        isCurrent: false
      }
    })

    // Add current GPA as the last point if provided
    if (currentGPA && semesters.length > 0) {
      const currentGPAValue = parseFloat(currentGPA)
      
      // Always add current GPA as the final point
      semesters.push({
        label: t('gpa.currentGpaLabel'),
        shortLabel: t('gpa.current'),
        semesterNumber: semesters.length + 1,
        gpa: currentGPAValue.toFixed(2),
        courses: 0,
        isCurrent: true
      })
    }

    return semesters
  }, [completedCourses, currentGPA, t])

  // Convert letter grade to grade points
  function getGradePoints(grade) {
    if (!grade) return null
    
    const gradeMap = {
      'A': 4.0, 'A-': 3.7,
      'B+': 3.3, 'B': 3.0, 'B-': 2.7,
      'C+': 2.3, 'C': 2.0, 'C-': 1.7,
      'D': 1.0, 'F': 0.0,
      'S': null, 'U': null
    }
    
    return gradeMap[grade] ?? null
  }

  function getSortKey(term, year) {
    const termOrder = { 'Fall': 0, 'Winter': 1, 'Summer': 2 }
    return year * 10 + (termOrder[term] ?? 0)
  }

  if (semesterData.length === 0) {
    return (
      <div className="gpa-trend-empty">
        <p><FaChartBar style={{ marginRight: '6px', verticalAlign: 'middle', color: 'var(--accent-primary, #ED1B2F)' }} />{t('gpa.addGradesPrompt')}</p>
      </div>
    )
  }

  const maxGPA = Math.max(...semesterData.map(s => parseFloat(s.gpa)), 4.0)
  const minGPA = Math.min(...semesterData.map(s => s.gpa).filter(g => g !== null), 0)
  const range = maxGPA - minGPA

  return (
    <div className="gpa-trend-chart">
      <div className="chart-header">
        <h3 className="chart-title">{t('gpa.trendTitle')}</h3>
        <span className="chart-subtitle">
          {semesterData.length} {semesterData.length === 1 ? t('gpa.semester') : t('gpa.semesters')}
        </span>
      </div>
      
      <div className="chart-container">
        {/* Y-axis labels */}
        <div className="y-axis">
          <span className="y-label">4.0</span>
          <span className="y-label">3.0</span>
          <span className="y-label">2.0</span>
          <span className="y-label">1.0</span>
          <span className="y-label">0.0</span>
        </div>

        {/* Chart area */}
        <div className="chart-area">
          {/* Grid lines */}
          <div className="grid-lines">
            <div className="grid-line"></div>
            <div className="grid-line"></div>
            <div className="grid-line"></div>
            <div className="grid-line"></div>
          </div>

          {/* Data points and line */}
          <svg className="chart-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
            {/* Draw line connecting points */}
            {semesterData.length > 1 && (
              <polyline
                className="trend-line"
                points={semesterData
                  .map((semester, idx) => {
                    const x = (idx / (semesterData.length - 1)) * 100
                    const y = 100 - ((parseFloat(semester.gpa) - minGPA) / range * 100)
                    return `${x},${y}`
                  })
                  .join(' ')}
              />
            )}

            {/* Draw area under line */}
            {semesterData.length > 1 && (
              <polygon
                className="trend-area"
                points={[
                  ...semesterData.map((semester, idx) => {
                    const x = (idx / (semesterData.length - 1)) * 100
                    const y = 100 - ((parseFloat(semester.gpa) - minGPA) / range * 100)
                    return `${x},${y}`
                  }),
                  `100,100`,
                  `0,100`
                ].join(' ')}
              />
            )}
          </svg>

          {/* Data points */}
          <div className="data-points">
            {semesterData.map((semester, idx) => {
              const x = (idx / (semesterData.length - 1)) * 100
              const y = 100 - ((parseFloat(semester.gpa) - minGPA) / range * 100)
              
              return (
                <div
                  key={idx}
                  className={`data-point ${semester.isCurrent ? 'current-point' : ''}`}
                  style={{
                    left: `${x}%`,
                    top: `${y}%`
                  }}
                  title={semester.isCurrent 
                    ? `${semester.label}: ${semester.gpa} GPA` 
                    : `${semester.label}: ${semester.gpa} GPA (${semester.courses} ${t('gpa.courses')})`
                  }
                >
                  <div className="point-circle"></div>
                  <div className="point-label">{semester.gpa}</div>
                </div>
              )
            })}
          </div>
        </div>
      </div>

      {/* X-axis labels */}
      <div className="x-axis">
        {semesterData.map((semester, idx) => (
          <div key={idx} className="x-label-group">
            <span className="x-label-main">{semester.shortLabel}</span>
            <span className="x-label-sub">{t('gpa.semesterShort')} {semester.semesterNumber}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
