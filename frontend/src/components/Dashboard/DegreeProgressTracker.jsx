import { useMemo } from 'react'
import { useLanguage } from '../../contexts/LanguageContext'
import { getCreditsRequired } from '../../utils/mcgillData'
import { FaBook, FaBolt, FaCheck, FaBullseye, FaRegCircle, FaGraduationCap, FaLightbulb, FaFlag } from 'react-icons/fa'
import { GiPartyPopper } from 'react-icons/gi'
import { LuBicepsFlexed } from 'react-icons/lu'
import './DegreeProgressTracker.css'

export default function DegreeProgressTracker({ completedCourses = [], profile = {} }) {
  const { t } = useLanguage()
  
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

  return (
    <div className="degree-progress-tracker">
      {/* Progress Bar */}
      <div className="progress-section">
        <div className="progress-header">
          <h3 className="progress-title">{t('degree.completion')}</h3>
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

      {/* Milestones */}
      <div className="milestones">
        {[
          { pct: 0.25, icon: <FaFlag />,          labelKey: 'degree.milestone25' },
          { pct: 0.5,  icon: <GiPartyPopper />,   labelKey: 'degree.milestone50' },
          { pct: 0.75, icon: <LuBicepsFlexed />,  labelKey: 'degree.milestone75' },
          { pct: 1,    icon: <FaGraduationCap />, labelKey: 'degree.milestone100' },
        ].map(({ pct, icon, labelKey }) => {
          const threshold = pct === 1 ? stats.totalRequired : Math.round(stats.totalRequired * pct)
          const done = stats.totalEarnedCredits >= threshold
          return (
            <div key={pct} className={`milestone ${done ? 'completed' : ''}`}>
              <div className="milestone-marker">
                {done
                  ? <FaCheck className="milestone-check" />
                  : <FaRegCircle className="milestone-circle" />}
              </div>
              <div className="milestone-text">
                <span className="milestone-credits">{threshold} {t('courses.credits').toLowerCase()}</span>
                <span className="milestone-label">
                  <span className="milestone-icon-inline">{icon}</span>
                  {t(labelKey)}
                </span>
              </div>
            </div>
          )
        })}
      </div>

      {stats.advancedStandingCredits > 0 && (
        <div className="info-note">
          <span className="info-icon"><FaLightbulb /></span>
          <span>{t('degree.creditsHeadStart').replace('{count}', Math.round(stats.advancedStandingCredits))}</span>
        </div>
      )}
    </div>
  )
}
