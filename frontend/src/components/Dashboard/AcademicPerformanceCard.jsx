import { summarizeGrades } from '../../utils/academicGrades'
import { useMemo, useState } from 'react'
import { FaChartBar, FaChartLine, FaBullseye, FaLightbulb } from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import { getCreditsRequired } from '../../utils/mcgillData'
import SectionHeader from '../ui/SectionHeader'
import GPATrendChart from './GPATrendChart'
import TargetGPACalculator from './TargetGPACalculator'
import './AcademicPerformanceCard.css'

/**
 * Academic Performance, current GPA, trend history, and the Target GPA
 * calculator merged into one card beside Degree Progress on the My Degree
 * tab. The trend chart and calculator share the space behind a segmented
 * toggle so the card stays the same height as its neighbour. Credit math
 * mirrors DegreeProgressTracker so the two cards agree.
 */
export default function AcademicPerformanceCard({ profile = {}, completedCourses = [] }) {
  const { t } = useLanguage()
  const [view, setView] = useState('trend')

  const { earnedCredits, totalRequired } = useMemo(() => {
    const courseCredits = completedCourses.reduce((sum, c) => sum + (c.credits || 3), 0)
    const advancedCredits = (profile?.advanced_standing || []).reduce((sum, c) => {
      if (c.counts_toward_degree === false) return sum
      return sum + (c.credits || 0)
    }, 0)
    return {
      earnedCredits: courseCredits + advancedCredits,
      totalRequired: getCreditsRequired(profile?.faculty, profile?.major, profile?.is_honours),
    }
  }, [completedCourses, profile])

  const enteredGrades = useMemo(() => summarizeGrades(completedCourses), [completedCourses])
  const currentGPA = enteredGrades.gpa ?? profile?.current_gpa
  const futureCredits = Math.max(0, totalRequired - earnedCredits)

  return (
    <div className="apc">
      <SectionHeader icon={<FaChartBar />} title={t('profile.academicPerformance')} />

      <div className="apc-hero">
        <span className="apc-hero-value">{currentGPA == null ? '--' : Number(currentGPA).toFixed(2)}</span>
        <div className="apc-hero-meta">
          <span className="apc-hero-label">{t(enteredGrades.gpa == null ? 'profile.currentGpa' : 'gpa.enteredGrades')}</span>
          <span className="apc-hero-sub">
            {Math.round(earnedCredits)} / {totalRequired} {t('courses.credits').toLowerCase()}
          </span>
        </div>
      </div>

      <div className="apc-toggle">
        <button
          className={`apc-toggle-btn ${view === 'trend' ? 'apc-toggle-btn--active' : ''}`}
          onClick={() => setView('trend')}
          aria-pressed={view === 'trend'}
        >
          <FaChartLine className="apc-toggle-icon" /> {t('gpa.trendTitle')}
        </button>
        <button
          className={`apc-toggle-btn ${view === 'target' ? 'apc-toggle-btn--active' : ''}`}
          onClick={() => setView('target')}
          aria-pressed={view === 'target'}
        >
          <FaBullseye className="apc-toggle-icon" /> {t('gpa.targetGpa')}
        </button>
      </div>

      <div className="apc-body">
        {view === 'trend' ? (
          <>
            <GPATrendChart completedCourses={completedCourses} currentGPA={currentGPA} />
            <p className="apc-tip">
              <FaLightbulb className="apc-tip-icon" />
              {t('profile.gpaTip')}
            </p>
          </>
        ) : (
          <TargetGPACalculator
            compact
            currentGPA={currentGPA}
            completedCredits={enteredGrades.credits}
            totalCreditsRequired={enteredGrades.credits + futureCredits}
          />
        )}
      </div>
    </div>
  )
}
