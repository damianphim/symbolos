import { useEffect, useState } from 'react'
import { getConsent } from '../lib/telemetry'

/**
 * Vercel Analytics is a non-essential cookie under Law 25, so we only
 * mount it once the user has accepted the cookie banner. We watch the
 * consent value and mount lazily.
 */
export default function ConsentedAnalytics() {
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
