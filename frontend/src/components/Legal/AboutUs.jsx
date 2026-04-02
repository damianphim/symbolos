import {
  FaTimes, FaGraduationCap, FaRobot, FaChartBar,
  FaCalendarAlt, FaBuilding, FaGlobe, FaEnvelope,
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import './Legal.css'

export default function AboutUs({ onClose }) {
  const { t } = useLanguage()

  const disclaimer = t('legal.translationDisclaimer')

  return (
    <div className="legal-overlay" onClick={onClose}>
      <div className="legal-modal" onClick={e => e.stopPropagation()}>
        <div className="legal-header">
          <div className="legal-logo">SY</div>
          <div>
            <h1 className="legal-title">{t('legal.aboutTitle')}</h1>
            <p className="legal-subtitle">{t('legal.aboutSubtitle')}</p>
          </div>
          {onClose && (
            <button className="legal-close" onClick={onClose} aria-label="Close">
              <FaTimes />
            </button>
          )}
        </div>
        <div className="legal-body">
          {disclaimer && (
            <div className="legal-translation-banner">{disclaimer}</div>
          )}
          <div className="legal-disclaimer-banner">
            <strong>{t('legal.notAffiliated')}</strong> {t('legal.aboutNotAffiliatedDesc')}
          </div>
          <section className="legal-section about-mission">
            <div className="about-logo-large">
              <svg width="48" height="48" viewBox="0 0 28 28" fill="none">
                <circle cx="14" cy="14" r="5" fill="#ED1B2F" opacity="0.95"/>
                <circle cx="14" cy="14" r="11" stroke="#ED1B2F" strokeWidth="1.5" opacity="0.35"/>
                <circle cx="14" cy="14" r="7" stroke="#ED1B2F" strokeWidth="1" opacity="0.6"/>
              </svg>
            </div>
            <h2>{t('about.missionTitle')}</h2>
            <p>{t('about.missionText1')}</p>
            <p>{t('about.missionText2')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('about.featuresTitle')}</h2>
            <div className="about-features-grid">
              <div className="about-feature">
                <span className="about-feature-icon"><FaGraduationCap /></span>
                <div>
                  <strong>{t('about.featureDegree')}</strong>
                  <p>{t('about.featureDegreeDesc')}</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon"><FaRobot /></span>
                <div>
                  <strong>{t('about.featureAI')}</strong>
                  <p>{t('about.featureAIDesc')}</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon"><FaChartBar /></span>
                <div>
                  <strong>{t('about.featureGrades')}</strong>
                  <p>{t('about.featureGradesDesc')}</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon"><FaCalendarAlt /></span>
                <div>
                  <strong>{t('about.featureCalendar')}</strong>
                  <p>{t('about.featureCalendarDesc')}</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon"><FaBuilding /></span>
                <div>
                  <strong>{t('about.featureClubs')}</strong>
                  <p>{t('about.featureClubsDesc')}</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon"><FaGlobe /></span>
                <div>
                  <strong>{t('about.featureMultilingual')}</strong>
                  <p>{t('about.featureMultilingualDesc')}</p>
                </div>
              </div>
            </div>
          </section>
          <section className="legal-section">
            <h2>{t('about.builtByTitle')}</h2>
            <p>{t('about.builtByText1')}</p>
            <p>{t('about.builtByText2')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('about.techTitle')}</h2>
            <p>{t('about.techText')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('about.disclaimerTitle')}</h2>
            <div className="legal-warning-box">
              {t('about.disclaimerText')}
            </div>
          </section>
          <section className="legal-section">
            <h2>{t('about.contactTitle')}</h2>
            <p>{t('about.contactText')}</p>
            <p style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <FaEnvelope style={{ color: 'var(--accent-primary, #ED1B2F)', flexShrink: 0 }} />
              <a href="mailto:symbolosadvsry@gmail.com">symbolosadvsry@gmail.com</a>
            </p>
            <p>{t('about.contactFeedback')}</p>
          </section>
        </div>
      </div>
    </div>
  )
}
