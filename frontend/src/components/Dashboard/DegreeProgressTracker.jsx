import { useMemo, useState } from 'react'
import { useLanguage } from '../../contexts/PreferencesContext'
import { getCreditsRequired } from '../../utils/mcgillData'
import {
  FaBook, FaBolt, FaCheck, FaBullseye,
  FaLightbulb, FaTimes, FaChevronDown, FaChevronUp,
} from 'react-icons/fa'
import './DegreeProgressTracker.css'

// `compact` renders only the progress bar + credit totals (used on Home);
// the full layout with breakdown/milestones stays the Degree Planning default.
export default function DegreeProgressTracker({ completedCourses = [], profile = {}, compact = false }) {
  const { t } = useLanguage()

  // Dismissible "head start" tip — remembers the choice across visits.
  const [headStartDismissed, setHeadStartDismissed] = useState(
    () => { try { return localStorage.getItem('dp_dismiss_headstart') === '1' } catch { return false } }
  )
  const dismissHeadStart = () => {
    setHeadStartDismissed(true)
    try { localStorage.setItem('dp_dismiss_headstart', '1') } catch { /* ignore */ }
  }

  // Breakdown + milestones are secondary detail — collapsed by default so
  // the card leads with just the bar and totals.
  const [detailsOpen, setDetailsOpen] = useState(false)

  const stats = useMemo(() => {
    // Calculate completed course credits
    const completedCredits = completedCourses.reduce((sum, course) => {
      return sum + (course.credits || 3) // Default to 3 if not specified
    }, 0)

    // Calculate advanced standing credits (only entries with counts_toward_degree not explicitly false)
    const advancedStandingCredits = (profile?.advanced_standing || []).reduce((sum, course) => {
      if (course.counts_toward_degree === false) return sum
      return sum + (course.credits || 0)
    }, 0)

    // Total earned credits
    const totalEarnedCredits = completedCredits + advancedStandingCredits

    // Get credit requirements from the single source of truth
    const TOTAL_CREDITS_REQUIRED = getCreditsRequired(
      profile?.faculty,
      profile?.major,
      profile?.is_honours
    )
    
    const remainingCredits = Math.max(0, TOTAL_CREDITS_REQUIRED - totalEarnedCredits)
    const progressPercentage = Math.min(100, (totalEarnedCredits / TOTAL_CREDITS_REQUIRED) * 100)

    return {
      completedCredits,
      advancedStandingCredits,
      totalEarnedCredits,
      totalRequired: TOTAL_CREDITS_REQUIRED,
      remainingCredits,
      progressPercentage,
      completedCourseCount: completedCourses.length,
      advancedStandingCourseCount: (profile?.advanced_standing || []).length
    }
  }, [completedCourses, profile])

  const progressSection = (
    <div className="progress-section">
      <div className="progress-header">
        <span className="progress-percentage">{Math.round(stats.progressPercentage)}%</span>
      </div>
      <div className="progress-bar-container">
        <div
          className="progress-bar-fill"
          style={{ width: `${stats.progressPercentage}%` }}
        >
          <div className="progress-bar-shine"></div>
        </div>
      </div>
      <div className="progress-labels">
        <span className="progress-label">{Math.round(stats.totalEarnedCredits)} {t('degree.creditsEarned')}</span>
        <span className="progress-label">{stats.totalRequired} {t('degree.creditsRequired')}</span>
      </div>
    </div>
  )

  if (compact) {
    return (
      <div className="degree-progress-tracker degree-progress-tracker--compact">
        {progressSection}
        {stats.remainingCredits > 0 && (
          <p className="degree-progress-tracker__remaining-hint">
            {Math.round(stats.remainingCredits)} {t('courses.credits').toLowerCase()} {t('degree.remaining').toLowerCase()}
          </p>
        )}
      </div>
    )
  }

  return (
    <div className="degree-progress-tracker">
      {progressSection}

      <button
        className="progress-details-toggle"
        onClick={() => setDetailsOpen(o => !o)}
        aria-expanded={detailsOpen}
      >
        {detailsOpen ? <FaChevronUp /> : <FaChevronDown />}
        {detailsOpen ? t('degree.hideDetails') : t('degree.showDetails')}
      </button>

      {detailsOpen && (
        <>
      {/* Credit Breakdown */}
      <div className="credits-breakdown">
        <div className="credit-item">
          <div className="credit-icon"><FaBook /></div>
          <div className="credit-details">
            <div className="credit-label">{t('degree.completedCourses')}</div>
            <div className="credit-value">
              <span>{stats.completedCourseCount} {t('nav.courses')}</span>
            </div>
          </div>
        </div>

        {stats.advancedStandingCredits > 0 && (
          <div className="credit-item highlight">
            <div className="credit-icon"><FaBolt /></div>
            <div className="credit-details">
              <div className="credit-label">{t('degree.advancedStanding')}</div>
              <div className="credit-value">
                {Math.round(stats.advancedStandingCredits)} {t('courses.credits').toLowerCase()}

              </div>
            </div>
          </div>
        )}

        <div className="credit-item total">
          <div className="credit-icon"><FaCheck /></div>
          <div className="credit-details">
            <div className="credit-label">{t('degree.totalEarned')}</div>
            <div className="credit-value">{Math.round(stats.totalEarnedCredits)} {t('courses.credits').toLowerCase()}</div>
          </div>
        </div>

        <div className="credit-item remaining">
          <div className="credit-icon"><FaBullseye /></div>
          <div className="credit-details">
            <div className="credit-label">{t('degree.remaining')}</div>
            <div className="credit-value">{Math.round(stats.remainingCredits)} {t('courses.credits').toLowerCase()}</div>
          </div>
        </div>
      </div>

        </>
      )}

      {stats.advancedStandingCredits > 0 && !headStartDismissed && (
        <div className="info-note">
          <span className="info-icon"><FaLightbulb /></span>
          <span>{t('degree.creditsHeadStart').replace('{count}', Math.round(stats.advancedStandingCredits))}</span>
          <button className="info-note-close" onClick={dismissHeadStart} aria-label="Dismiss" title="Dismiss">
            <FaTimes />
          </button>
        </div>
      )}
    </div>
  )
}
