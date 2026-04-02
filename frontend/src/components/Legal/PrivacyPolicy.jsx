import { FaTimes } from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import './Legal.css'

export default function PrivacyPolicy({ onClose }) {
  const { t } = useLanguage()

  const renderAnthropicLink = (text) => {
    const parts = text.split(/<a>(.*?)<\/a>/)
    return parts.map((part, i) =>
      i % 2 === 1 ? (
        <a key={i} href="https://www.anthropic.com/privacy" target="_blank" rel="noopener noreferrer">{part}</a>
      ) : (
        <span key={i}>{part}</span>
      )
    )
  }

  const renderList = (key) =>
    t(key).split('|').map((item, i) => <li key={i}>{item}</li>)

  const renderBoldList = (key) =>
    t(key).split('|').map((item, i) => {
      const dashIdx = item.indexOf(' — ')
      if (dashIdx !== -1) {
        return <li key={i}><strong>{item.slice(0, dashIdx)}</strong> — {item.slice(dashIdx + 3)}</li>
      }
      return <li key={i}>{item}</li>
    })

  const disclaimer = t('legal.translationDisclaimer')

  return (
    <div className="legal-overlay" onClick={onClose}>
      <div className="legal-modal" onClick={e => e.stopPropagation()}>
        <div className="legal-header">
          <div className="legal-logo">SY</div>
          <div>
            <h1 className="legal-title">{t('legal.privacyTitle')}</h1>
            <p className="legal-subtitle">{t('legal.privacySubtitle')}</p>
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
            <h2>{t('privacy.s1Title')}</h2>
            <p>{t('privacy.s1Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s2Title')}</h2>
            <h3>{t('privacy.s2aTitle')}</h3>
            <p>{t('privacy.s2aText')}</p>
            <h3>{t('privacy.s2bTitle')}</h3>
            <p>{t('privacy.s2bText')}</p>
            <h3>{t('privacy.s2cTitle')}</h3>
            <p>{t('privacy.s2cText')}</p>
            <h3>{t('privacy.s2dTitle')}</h3>
            <p>{renderAnthropicLink(t('privacy.s2dText'))}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s3Title')}</h2>
            <ul>{renderList('privacy.s3Items')}</ul>
            <p>{t('privacy.s3Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s4Title')}</h2>
            <p>{t('privacy.s4Intro')}</p>
            <ul>{renderBoldList('privacy.s4Items')}</ul>
            <p>{t('privacy.s4Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s5Title')}</h2>
            <p>{t('privacy.s5Text1')}</p>
            <p>{t('privacy.s5Text2')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s6Title')}</h2>
            <p>{t('privacy.s6Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s7Title')}</h2>
            <p>{t('privacy.s7Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s8Title')}</h2>
            <p>{t('privacy.s8Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s9Title')}</h2>
            <p>{t('privacy.s9Text')}</p>
          </section>
          <section className="legal-section">
            <h2>{t('privacy.s10Title')}</h2>
            <p>{t('privacy.s10Text')} <a href="mailto:symbolosadvsry@gmail.com">symbolosadvsry@gmail.com</a></p>
          </section>
        </div>
      </div>
    </div>
  )
}
