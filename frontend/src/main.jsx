import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import ConsentedAnalytics from './components/ConsentedAnalytics.jsx'
import { initTelemetry } from './lib/telemetry'

// Boot strictly-necessary telemetry (Sentry) immediately; consent-gated
// analytics (PostHog) only start if the user previously accepted.
initTelemetry()

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <ConsentedAnalytics />
  </StrictMode>,
)
