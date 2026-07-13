/**
 * CookieConsent — Quebec Law 25 §8.1 affirmative-consent banner.
 *
 * Non-essential cookies (PostHog product analytics, Vercel Analytics)
 * must not run until the user explicitly accepts. Strictly-necessary
 * cookies (auth session, theme, language, the consent choice itself)
 * always run — they're exempt.
 *
 * Behaviour:
 *   • First visit, no stored choice → banner shows.
 *   • Accept → analytics boot immediately, banner hides forever.
 *   • Decline → analytics never boot, banner hides (re-openable from
 *     the Privacy modal's "Cookie settings" if we add one later).
 *   • Respects Do-Not-Track: if the browser signals DNT, we treat it as
 *     an implicit decline and don't even show the banner.
 */
import { useEffect, useState } from 'react'
import { FaCookieBite } from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import { getConsent, setConsent } from '../../lib/telemetry'
import './CookieConsent.css'

function dntEnabled() {
  if (typeof navigator === 'undefined') return false
  const v = navigator.doNotTrack || window.doNotTrack || navigator.msDoNotTrack
  return v === '1' || v === 'yes'
}

export default function CookieConsent() {
  const { t } = useLanguage()
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    // Already chose, or DNT set → never show.
    if (getConsent()) return
    if (dntEnabled()) {
      setConsent('declined')
      return
    }
    // Small delay so it doesn't fight the first paint / loading screen.
    const t = setTimeout(() => setVisible(true), 800)
    return () => clearTimeout(t)
  }, [])

  if (!visible) return null

  const accept = () => { setConsent('accepted'); setVisible(false) }
  const decline = () => { setConsent('declined'); setVisible(false) }

  return (
    <div className="cookie-consent" role="dialog" aria-live="polite" aria-label={t('cookie.ariaLabel')}>
      <div className="cookie-consent__inner">
        <div className="cookie-consent__icon" aria-hidden="true">
          <FaCookieBite />
        </div>
        <div className="cookie-consent__text">
          <p className="cookie-consent__title">{t('cookie.title')}</p>
          <p className="cookie-consent__body">
            {t('cookie.body')}
          </p>
        </div>
        <div className="cookie-consent__actions">
          <button className="cookie-consent__btn cookie-consent__btn--ghost" onClick={decline}>
            {t('cookie.essentialOnly')}
          </button>
          <button className="cookie-consent__btn cookie-consent__btn--primary" onClick={accept}>
            {t('cookie.acceptAll')}
          </button>
        </div>
      </div>
    </div>
  )
}
