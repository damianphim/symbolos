import { StrictMode, useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import CookieConsent from './components/CookieConsent/CookieConsent'
import { initTelemetry, getConsent } from './lib/telemetry'

// Boot strictly-necessary telemetry (Sentry) immediately; consent-gated
// analytics (PostHog) only start if the user previously accepted.
initTelemetry()

/**
 * Vercel Analytics is a non-essential cookie under Law 25, so we only
 * mount it once the user has accepted the cookie banner. We watch the
 * consent value and mount lazily.
 */
function ConsentedAnalytics() {
  const [accepted, setAccepted] = useState(getConsent() === 'accepted')
  useEffect(() => {
    if (accepted) return
    // Poll briefly for the consent flag flipping (cheap; the banner
    // writes localStorage synchronously on click). Stops once accepted.
    const id = setInterval(() => {
      if (getConsent() === 'accepted') {
        setAccepted(true)
        clearInterval(id)
      }
    }, 1000)
    return () => clearInterval(id)
  }, [accepted])

  const [Analytics, setAnalytics] = useState(null)
  useEffect(() => {
    if (accepted && !Analytics) {
      import('@vercel/analytics/react').then(m => setAnalytics(() => m.Analytics)).catch(() => {})
    }
  }, [accepted, Analytics])

  return Analytics ? <Analytics /> : null
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <ConsentedAnalytics />
    <CookieConsent />
  </StrictMode>,
)
