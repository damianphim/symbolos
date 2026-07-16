import { useEffect, useState } from 'react'
import { getConsent, CONSENT_EVENT } from '../lib/telemetry'

/**
 * Vercel Analytics is a non-essential cookie under Law 25, so we only mount it
 * while consent is granted — and UNMOUNT it the moment consent is withdrawn
 * (Law 25 / GDPR: revoking must be as easy as granting). We react to the
 * consent-change event in both directions.
 */
export default function ConsentedAnalytics() {
  const [accepted, setAccepted] = useState(getConsent() === 'accepted')

  useEffect(() => {
    const onConsent = () => setAccepted(getConsent() === 'accepted')
    window.addEventListener(CONSENT_EVENT, onConsent)
    return () => window.removeEventListener(CONSENT_EVENT, onConsent)
  }, [])

  const [Analytics, setAnalytics] = useState(null)
  useEffect(() => {
    if (accepted && !Analytics) {
      import('@vercel/analytics/react').then(m => setAnalytics(() => m.Analytics)).catch(() => {})
    }
  }, [accepted, Analytics])

  // Only render while consent is currently granted — withdrawal unmounts it.
  return accepted && Analytics ? <Analytics /> : null
}
