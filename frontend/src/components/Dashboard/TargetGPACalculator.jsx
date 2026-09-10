import { useState, useMemo } from 'react'
import { useLanguage } from '../../contexts/PreferencesContext'
import { FaBullseye, FaLightbulb, FaBan, FaSmile, FaFire } from 'react-icons/fa'
import { FaDumbbell } from 'react-icons/fa6'
import { FaBook } from 'react-icons/fa'
import { HiMiniSparkles } from "react-icons/hi2";
import './TargetGPACalculator.css'

export default function TargetGPACalculator({ currentGPA, completedCredits, totalCreditsRequired = 120, compact = false }) {
  const { t } = useLanguage()
  const [targetGPA, setTargetGPA] = useState('')
  const [horizon, setHorizon] = useState('degree')
  const [scopeCredits, setScopeCredits] = useState('15')
  const [scopeCompleted, setScopeCompleted] = useState('0')
  const [scopeGPA, setScopeGPA] = useState('0')
  const scoped = horizon !== 'degree'
  const baselineGPA = scoped ? scopeGPA : currentGPA
  const baselineCredits = scoped ? scopeCompleted : completedCredits
  const horizonCredits = scoped ? Number(scopeCredits) : totalCreditsRequired

  const [showResult, setShowResult] = useState(false)

  const calculation = useMemo(() => {
    if (baselineGPA == null || baselineGPA === '' || targetGPA === '' || baselineCredits == null || baselineCredits === '') return null

    const current = parseFloat(baselineGPA)
    const target = parseFloat(targetGPA)
    const completed = parseFloat(baselineCredits)
    const remaining = Math.max(0, horizonCredits - completed)

    if (![current, target, completed, horizonCredits].every(Number.isFinite)) return null
    if (target < 0 || target > 4.0) return { error: 'Target GPA must be between 0.0 and 4.0' }
    if (current < 0 || current > 4.0) return { error: 'Current GPA must be between 0.0 and 4.0' }
    if (completed < 0) return { error: 'Completed credits cannot be negative' }
    if (remaining <= 0) return { error: 'You have already completed all required credits' }

    const requiredGPA = (target * horizonCredits - current * completed) / remaining

    if (requiredGPA > 4.0) {
      return {
        isAchievable: false,
        requiredGPA: requiredGPA.toFixed(2),
        message: `${t('gpa.impossibleMessage')} ${((current * completed + 4.0 * remaining) / horizonCredits).toFixed(2)}`
      }
    }

    if (requiredGPA < 0) {
      return {
        isAchievable: true,
        requiredGPA: '0.00',
        targetGPA: target.toFixed(2), remainingCredits: remaining, scenarios: [],
        message: t('gpa.alreadyExceeded').replace('{current}', current.toFixed(2)).replace('{target}', target.toFixed(2))
      }
    }

    const scenarios = [
      { label: t('gpa.scenarioConservative'), gpa: 3.0, finalGPA: ((current * completed + 3.0 * remaining) / horizonCredits).toFixed(2) },
      { label: t('gpa.scenarioStrong'),       gpa: 3.7, finalGPA: ((current * completed + 3.7 * remaining) / horizonCredits).toFixed(2) },
      { label: t('gpa.scenarioPerfect'),      gpa: 4.0, finalGPA: ((current * completed + 4.0 * remaining) / horizonCredits).toFixed(2) }
    ]

    return {
      isAchievable: true,
      requiredGPA: requiredGPA.toFixed(2),
      remainingCredits: remaining,
      completedCredits: completed,
      currentGPA: current.toFixed(2),
      targetGPA: target.toFixed(2),
      scenarios,
      difficulty: getDifficulty(requiredGPA)
    }
  }, [baselineGPA, targetGPA, baselineCredits, horizonCredits, t])

  function getDifficulty(requiredGPA) {
    if (requiredGPA <= 2.5) return { level: t('gpa.difficultyEasy'),           color: '#10b981', emoji: <FaSmile    className="difficulty-emoji" /> }
    if (requiredGPA <= 3.0) return { level: t('gpa.difficultyModerate'),        color: '#3b82f6', emoji: <FaDumbbell className="difficulty-emoji" /> }
    if (requiredGPA <= 3.5) return { level: t('gpa.difficultyChallenging'),     color: '#f59e0b', emoji: <FaBook     className="difficulty-emoji" /> }
    if (requiredGPA <= 3.8) return { level: t('gpa.difficultyDifficult'),       color: '#ef4444', emoji: <FaFire     className="difficulty-emoji" /> }
    return                   { level: t('gpa.difficultyVeryDifficult'), color: '#dc2626', emoji: <FaBullseye className="difficulty-emoji" /> }
  }

  const handleCalculate = () => {
    if (calculation) setShowResult(true)
  }

  const handleReset = () => {
    setTargetGPA('')
    setShowResult(false)
  }

  function getLetterGrade(gpa) {
    if (gpa >= 3.85) return 'A (Excellent)'
    if (gpa >= 3.5)  return 'A- to A (Very Good)'
    if (gpa >= 3.15) return 'B+ (Good)'
    if (gpa >= 2.85) return 'B (Satisfactory)'
    if (gpa >= 2.5)  return 'B- to B (Acceptable)'
    if (gpa >= 2.15) return 'C+ (Below Average)'
    if (gpa >= 1.85) return 'C (Minimal Pass)'
    return 'Below C (Needs Improvement)'
  }

  function getTips(requiredGPA) {
    const tips = []
    if (requiredGPA >= 3.7) {
      tips.push('Focus on your strongest subjects for higher grades')
      tips.push('Consider taking fewer courses per semester to maintain quality')
      tips.push('Form study groups with high-performing classmates')
      tips.push('Attend all office hours and seek help early')
    } else if (requiredGPA >= 3.3) {
      tips.push('Maintain consistent study habits throughout the semester')
      tips.push('Start assignments early to allow time for revisions')
      tips.push('Attend review sessions before exams')
    } else if (requiredGPA >= 2.7) {
      tips.push('Stay on top of coursework and avoid falling behind')
      tips.push('Review material regularly, not just before exams')
      tips.push('Take advantage of tutoring resources')
    } else {
      tips.push('You have a comfortable cushion - maintain good habits')
      tips.push('Consider challenging yourself with interesting electives')
      tips.push('Focus on learning, not just grades')
    }
    return tips
  }

  return (
    <div className={`target-gpa-calculator${compact ? ' target-gpa-calculator--compact' : ''}`}>
      <div className="calculator-header">
        {/* In compact mode the surrounding card's toggle already names this
            section, so only the one-line subtitle is kept */}
        {!compact && (
          <h3 className="calculator-title">
            <FaBullseye className="calculator-icon" /> {t('gpa.targetGpa')} {t('common.calculator')}
          </h3>
        )}
        <p className="calculator-subtitle">{t('gpa.calculatorSubtitle')}</p>
      </div>

      <div className="calculator-body">
        {/* Current Stats, hidden in compact mode, where the surrounding
            Academic Performance card already shows GPA and credit totals */}
        {!compact && (
          <div className="current-stats">
            <div className="stat-box">
              <span className="stat-label">{t('gpa.currentGpa')}</span>
              <span className="stat-value">{currentGPA ?? '--'}</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">{t('gpa.creditsCompleted')}</span>
              <span className="stat-value">{Math.round(completedCredits || 0)}</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">{t('gpa.creditsRemaining')}</span>
              <span className="stat-value">{Math.max(0, totalCreditsRequired - Math.round(completedCredits || 0))}</span>
            </div>
          </div>
        )}

        <label className="input-label">
          <span>{t('gpa.horizon')}</span>
          <select value={horizon} onChange={e => {
            const next = e.target.value
            setHorizon(next)
            setScopeCredits(next === 'year' ? '30' : '15')
            setShowResult(false)
          }}>
            {['degree', 'term', 'year', 'custom'].map(scope => <option key={scope} value={scope}>{t(`gpa.horizon.${scope}`)}</option>)}
          </select>
        </label>
        {scoped && <fieldset>
          <legend>{t('gpa.scopeHint')}</legend>
          {[
            ['gpa.scopeTotal', scopeCredits, setScopeCredits, 300, 0.5],
            ['gpa.scopeCompleted', scopeCompleted, setScopeCompleted, 300, 0.5],
            ['gpa.scopeGpa', scopeGPA, setScopeGPA, 4, 0.01],
          ].map(([key, value, setter, max, step]) => <label className="input-label" key={key}>
            <span>{t(key)}</span>
            <input type="number" min="0" max={max} step={step} value={value} onChange={e => { setter(e.target.value); setShowResult(false) }} />
          </label>)}
        </fieldset>}
        {/* Input Section */}
        <div className="input-section">
          <label className="input-label">
            <span className="label-text">{t('gpa.targetGpa')}</span>
            <input
              type="number"
              min="0"
              max="4.0"
              step="0.01"
              placeholder="e.g., 3.5"
              value={targetGPA}
              onChange={(e) => { setTargetGPA(e.target.value); setShowResult(false) }}
              className="gpa-input"
            />
          </label>
          <button
            onClick={handleCalculate}
            disabled={!calculation}
            className="calculate-btn"
          >
            {t('gpa.calculateRequired')}
          </button>
        </div>

        {/* Results */}
        {showResult && calculation && (
          <div className="results-section">
            {calculation.error ? (
              <div className="error-message">
                <span className="error-icon"><FaLightbulb className="error-icon" /></span>
                <p>{calculation.error}</p>
              </div>
            ) : calculation.isAchievable ? (
              <>
                <div className="main-result">
                  <div className="result-header">
                    <span className="result-label">{t('gpa.requiredGpa')}</span>
                    {calculation.difficulty && (
                      <span className="difficulty-badge" style={{ backgroundColor: calculation.difficulty.color }}>
                        {calculation.difficulty.emoji} {calculation.difficulty.level}
                      </span>
                    )}
                  </div>
                  <div className="result-value">{calculation.requiredGPA}</div>
                  {calculation.message && <p>{calculation.message}</p>}
                  <div className="result-details">
                    {t('gpa.toReach')} <strong>{calculation.targetGPA}</strong> {t('gpa.withRemaining')} <strong>{calculation.remainingCredits}</strong> {t('gpa.creditsRemaining')}
                  </div>
                </div>

                <div className="grade-equivalent">
                  <span className="grade-label">{t('gpa.equivalentGrade')}</span>
                  <span className="grade-value">{getLetterGrade(parseFloat(calculation.requiredGPA))}</span>
                </div>

                <div className="scenarios-section">
                  <h4 className="scenarios-title">
                    <HiMiniSparkles className="scenarios-icon" /> {t('gpa.whatIfScenarios')}
                  </h4>
                  <div className="scenarios-list">
                    {(calculation.scenarios || []).map((scenario, idx) => (
                      <div key={idx} className="scenario-item">
                        <div className="scenario-header">
                          <span className="scenario-label">{scenario.label}</span>
                          <span className="scenario-gpa">{scenario.gpa.toFixed(1)}</span>
                        </div>
                        <div className="scenario-result">
                          {t('gpa.finalGpa')}: <strong>{scenario.finalGPA}</strong>
                          {parseFloat(scenario.finalGPA) >= parseFloat(calculation.targetGPA)
                            ? <span className="check-icon">✓</span>
                            : <span className="cross-icon">✗</span>
                          }
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {!compact && (
                  <div className="tips-section">
                    <h4 className="tips-title">
                      <FaLightbulb className="tips-icon" /> {t('gpa.tipsToReach')}
                    </h4>
                    <ul className="tips-list">
                      {getTips(parseFloat(calculation.requiredGPA)).map((tip, idx) => (
                        <li key={idx}>{tip}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <button onClick={handleReset} className="reset-btn">
                  {t('gpa.calculateAnother')}
                </button>
              </>
            ) : (
              <div className="impossible-result">
                <span className="impossible-icon"><FaBan className="impossible-icon" /></span>
                <h4>{t('gpa.notAchievable')}</h4>
                <p>{calculation.message}</p>
                <button onClick={handleReset} className="reset-btn">
                  {t('gpa.tryDifferent')}
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
