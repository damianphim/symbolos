import { FaTimes, FaExclamationTriangle } from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import './Legal.css'

export default function TermsOfService({ onClose }) {
  const { t } = useLanguage()

  const renderList = (key) =>
    t(key).split('|').map((item, i) => <li key={i}>{item}</li>)

  const disclaimer = t('legal.translationDisclaimer')

  return (
    <div className="legal-overlay" onClick={onClose}>
      <div className="legal-modal" onClick={e => e.stopPropagation()}>
        <div className="legal-header">
          <div className="legal-logo">SY</div>
          <div>
            <h1 className="legal-title">{t('legal.tosTitle')}</h1>
            <p className="legal-subtitle">{t('legal.tosSubtitle')}</p>
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
            <strong>{t('legal.notAffiliated')}</strong> {t('legal.notAffiliatedDesc')}
          </div>
          <section className="legal-section">
            <h2>{t('tos.s1Title')}</h2>
            <p>{t('tos.s1Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s2Title')}</h2>
            <p>{t('tos.s2Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s3Title')}</h2>
            <p>{t('tos.s3Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s4Title')}</h2>
            <ul>{renderList('tos.s4Items')}</ul>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s5Title')}</h2>
            <p>{t('tos.s5Intro')}</p>
            <ul>{renderList('tos.s5Items')}</ul>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s6Title')}</h2>
            <div className="legal-warning-box" style={{ display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
              <FaExclamationTriangle style={{ flexShrink: 0, marginTop: '2px', color: '#b45309' }} />
              <span><strong>{t('tos.s6Warning').split(':')[0]}:</strong>{t('tos.s6Warning').slice(t('tos.s6Warning').indexOf(':') + 1)}</span>
            </div>
            <ul>{renderList('tos.s6Items')}</ul>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s7Title')}</h2>
            <p>{t('tos.s7Text1')}</p>
            <p>{t('tos.s7Text2')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s8Title')}</h2>
            <p>{t('tos.s8Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s9Title')}</h2>
            <p>{t('tos.s9Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s10Title')}</h2>
            <p>{t('tos.s10Text1')}</p>
            <p>{t('tos.s10Text2')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s11Title')}</h2>
            <p>{t('tos.s11Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s12Title')}</h2>
            <p>{t('tos.s12Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s13Title')}</h2>
            <p>{t('tos.s13Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('tos.s14Title')}</h2>
            <p>{t('tos.s14Text')} <a href="mailto:symbolosadvsry@gmail.com">symbolosadvsry@gmail.com</a></p>
          </section>
        </div>
      </div>
    </div>
  )
}
