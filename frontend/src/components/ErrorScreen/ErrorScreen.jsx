/**
 * ErrorScreen — single source of truth for fatal / blocking error UIs.
 *
 * Used by:
 *   - ErrorBoundary: caught React render errors
 *   - App.jsx:       auth init failure, email verification failure
 *
 * Visual: cream-on-light theme (matches landing page), Symbolos logo,
 * McGill red accent, mobile-first responsive. Mirrors the
 * post-mortem-friendly ID surfacing from Sentry so support requests
 * land with the actionable info.
 *
 * Falls back gracefully if i18n / Sentry / logo asset aren't available
 * — this is the screen users see when *the app is broken*, so it
 * must not itself throw.
 */
import { useEffect, useMemo, useState } from 'react'
import {
  FaExclamationTriangle, FaSync, FaHome, FaSignInAlt,
  FaSignOutAlt, FaEnvelope, FaInfoCircle,
} from 'react-icons/fa'
import logoMark from '../../assets/loading-logo.png'
import './ErrorScreen.css'

const SUPPORT_EMAIL = 'symbolosadvsry@gmail.com'
const STATUS_URL    = 'https://status.symbolos.ca'

// Map of error variants → (title key, body key) used to pull copy from
// the i18n table. If translations aren't loaded we fall back to the
// inline default string so the user is never staring at "error.screen.title".
const VARIANTS = {
  generic: {
    title: ['error.screen.title.generic',      'Something went wrong'],
    body:  ['error.screen.body.generic',       'A glitch on our side stopped this page from loading. Your data is safe — nothing was changed.'],
  },
  verifyFailed: {
    title: ['error.screen.title.verifyFailed', "Verification didn't work"],
    body:  ['error.screen.body.verifyFailed',  "The verification link didn't work. It may have expired or already been used."],
  },
  authFailed: {
    title: ['error.screen.title.authFailed',   "Couldn't sign you in"],
    body:  ['error.screen.body.authFailed',    "We couldn't talk to the authentication service. This is usually a flaky internet connection."],
  },
  network: {
    title: ['error.screen.title.network',      "You're offline"],
    body:  ['error.screen.body.network',       "Looks like your connection dropped. Once you're back online, this page should load."],
  },
}

/** Lazy-imported i18n hook — guarded so this component still renders if
 * the LanguageContext isn't mounted (e.g. the error happened inside the
 * provider itself). */
function useSafeTranslate() {
  const [t, setT] = useState(() => (k, fb) => fb || k)
  useEffect(() => {
    let alive = true
    import('../../contexts/PreferencesContext').then(mod => {
      try {
        const ctxT = mod?.useLanguage?.()?.t
        if (alive && typeof ctxT === 'function') setT(() => ctxT)
      } catch { /* outside provider — keep fallback */ }
    }).catch(() => {})
    return () => { alive = false }
  }, [])
  return t
}

export default function ErrorScreen({
  variant = 'generic',
  customMessage,        // Override the body text (e.g. backend error detail)
  eventId,              // Sentry event id, if captured
  showHome = true,
  showReload = true,
  showSignIn = false,
  showSignOut = false,
  onSignOut,
  onSignIn,
  onHome,
}) {
  const t = useSafeTranslate()
  const v = VARIANTS[variant] || VARIANTS.generic

  const title = t(v.title[0], v.title[1])
  const body  = customMessage || t(v.body[0], v.body[1])

  // Browser online/offline → switch the variant title/body live.
  const [offline, setOffline] = useState(
    typeof navigator !== 'undefined' && navigator.onLine === false
  )
  useEffect(() => {
    const on  = () => setOffline(false)
    const off = () => setOffline(true)
    window.addEventListener('online',  on)
    window.addEventListener('offline', off)
    return () => {
      window.removeEventListener('online',  on)
      window.removeEventListener('offline', off)
    }
  }, [])

  const effectiveTitle = offline
    ? t('error.screen.title.network', VARIANTS.network.title[1])
    : title
  const effectiveBody = offline
    ? t('error.screen.body.network',  VARIANTS.network.body[1])
    : body

  const mailto = useMemo(() => {
    const subject = encodeURIComponent(`Symbolos error — ${variant}`)
    const ref = eventId ? `\n\nReference: ${eventId}` : ''
    const where = typeof window !== 'undefined' ? window.location.href : ''
    const body  = encodeURIComponent(
      `Hi Symbolos team,\n\nI hit this error while using the site.\n\n` +
      `What I was doing: \n\nWhere: ${where}${ref}\n\nThanks.`
    )
    return `mailto:${SUPPORT_EMAIL}?subject=${subject}&body=${body}`
  }, [variant, eventId])

  return (
    <div className="err-screen">
      <div className="err-screen__card" role="alert">
        <img src={logoMark} alt="Symbolos" className="err-screen__logo" />

        <div className="err-screen__icon" aria-hidden="true">
          <FaExclamationTriangle />
        </div>

        <h1 className="err-screen__title">{effectiveTitle}</h1>
        <p className="err-screen__body">{effectiveBody}</p>

        <div className="err-screen__actions">
          {showReload && (
            <button
              className="err-screen__btn err-screen__btn--primary"
              onClick={() => window.location.reload()}
            >
              <FaSync /> {t('error.screen.action.reload', 'Reload page')}
            </button>
          )}
          {showHome && (
            <button
              className="err-screen__btn err-screen__btn--ghost"
              onClick={onHome || (() => { window.location.href = '/' })}
            >
              <FaHome /> {t('error.screen.action.home', 'Go home')}
            </button>
          )}
          {showSignIn && (
            <button
              className="err-screen__btn err-screen__btn--ghost"
              onClick={onSignIn || (() => { window.location.replace('/?signin') })}
            >
              <FaSignInAlt /> {t('error.screen.action.signin', 'Back to sign in')}
            </button>
          )}
          {showSignOut && onSignOut && (
            <button
              className="err-screen__btn err-screen__btn--ghost"
              onClick={onSignOut}
            >
              <FaSignOutAlt /> {t('error.screen.action.signOut', 'Sign out')}
            </button>
          )}
        </div>

        {eventId && (
          <div className="err-screen__ref">
            <code className="err-screen__ref-code">
              {t('error.screen.eventId', 'Reference: {id}').replace('{id}', eventId)}
            </code>
            <p className="err-screen__ref-hint">
              <FaInfoCircle size={11} />
              {' '}
              {t(
                'error.screen.eventIdHint',
                'Include this reference if you contact us — it helps us find the issue in our logs.'
              )}
            </p>
          </div>
        )}

        <div className="err-screen__footer">
          <a href={mailto} className="err-screen__link">
            <FaEnvelope size={11} />
            {' '}
            {t('error.screen.action.contact', 'Email support')}
          </a>
          <span className="err-screen__sep">·</span>
          <a
            href={STATUS_URL}
            target="_blank"
            rel="noopener noreferrer"
            className="err-screen__link"
          >
            {t('error.screen.status', 'Check status page')}
          </a>
        </div>
      </div>
    </div>
  )
}
