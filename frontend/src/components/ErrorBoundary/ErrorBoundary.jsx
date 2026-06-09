/**
 * ErrorBoundary — catches uncaught React render errors at the root.
 *
 * On error:
 *   1. Captures the exception to Sentry (if VITE_SENTRY_DSN is set)
 *      and stashes the returned event ID so the user can quote it.
 *   2. Logs locally to console for dev visibility.
 *   3. Shows the shared branded <ErrorScreen> so users see the same
 *      polished UI regardless of which path crashed.
 *
 * NEVER let this component itself throw. The fallback path uses inline
 * fallback strings so a missing i18n provider doesn't escalate.
 */
import { Component } from 'react'
import ErrorScreen from '../ErrorScreen/ErrorScreen'

class ErrorBoundary extends Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null, eventId: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, errorInfo) {
    // Always log locally — Vercel function logs would have shown the
    // backend half but the frontend stack is harder to get without this.
    console.error('Error caught by boundary:', error, errorInfo)

    // Capture to Sentry async so we don't block the fallback render.
    // The dynamic import keeps Sentry out of the bundle until needed
    // AND means this works fine when Sentry isn't configured (the
    // import succeeds; init was a no-op so capture is also a no-op).
    import('@sentry/react').then(Sentry => {
      try {
        const eventId = Sentry.captureException(error, {
          contexts: { react: { componentStack: errorInfo?.componentStack } },
        })
        this.setState({ eventId })
      } catch { /* never let the error path throw */ }
    }).catch(() => {})
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorScreen
          variant="generic"
          eventId={this.state.eventId}
          showReload={true}
          showHome={true}
        />
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary
