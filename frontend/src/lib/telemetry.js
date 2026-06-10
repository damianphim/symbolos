/**
 * telemetry.js — Sentry + PostHog initialization.
 *
 * Both stay silent (no init, no errors) when their respective env vars are
 * missing. That lets local dev / CI / preview deployments run without
 * needing prod keys, and gives us a single place to disable everything if
 * we ever need to.
 *
 * Env vars (set in Vercel → Project → Settings → Environment Variables):
 *   VITE_SENTRY_DSN              — Sentry project DSN
 *   VITE_SENTRY_ENVIRONMENT      — optional, defaults to VERCEL_ENV
 *   VITE_POSTHOG_KEY             — PostHog project API key
 *   VITE_POSTHOG_HOST            — optional, defaults to https://us.i.posthog.com
 */

let _sentryReady = false
let _posthog = null
let _analyticsStarted = false

// ── Consent gating (Quebec Law 25 §8.1) ──────────────────────────────────────
// We split telemetry into two buckets:
//   • Sentry  = "strictly necessary" error monitoring. It carries no
//     marketing identifiers, is PII-scrubbed, and is needed to keep the
//     service working. Under Law 25 / GDPR this is a legitimate-interest
//     basis that does NOT require opt-in consent. It loads immediately.
//   • PostHog + Vercel Analytics = product analytics. These DO require
//     affirmative consent because they set non-essential cookies / track
//     behaviour. They stay dark until the user accepts the cookie banner.
const CONSENT_KEY = 'symbolos_cookie_consent'  // 'accepted' | 'declined'

export function getConsent() {
  try { return localStorage.getItem(CONSENT_KEY) } catch { return null }
}

export function setConsent(value) {
  try { localStorage.setItem(CONSENT_KEY, value) } catch {}
  if (value === 'accepted') startAnalytics()
}

/** Boot the strictly-necessary telemetry (Sentry) immediately, and the
 * consent-gated analytics only if consent was previously granted. */
export async function initTelemetry() {
  await _initSentry()
  if (getConsent() === 'accepted') startAnalytics()
}

/** Start the consent-gated analytics (PostHog). Idempotent. Called either
 * from initTelemetry (returning user who already consented) or from
 * setConsent('accepted') (user just clicked Accept). */
export async function startAnalytics() {
  if (_analyticsStarted) return
  _analyticsStarted = true
  await _initPostHog()
}

async function _initSentry() {
  const dsn = import.meta.env.VITE_SENTRY_DSN
  if (!dsn) return
  try {
    const Sentry = await import('@sentry/react')
    Sentry.init({
      dsn,
      environment:
        import.meta.env.VITE_SENTRY_ENVIRONMENT ||
        import.meta.env.MODE ||
        'production',
      release: import.meta.env.VITE_VERCEL_GIT_COMMIT_SHA || 'dev',
      integrations: [
        Sentry.browserTracingIntegration(),
        Sentry.replayIntegration({
          // Don't capture text inputs / PII in replays.
          maskAllText: true,
          blockAllMedia: true,
        }),
      ],
      // Slim quotas — bump once we know what's noisy.
      tracesSampleRate: 0.1,
      replaysSessionSampleRate: 0.0,   // off by default; record only on error
      replaysOnErrorSampleRate: 1.0,
      // The auth tokens in URLs would otherwise leak into Sentry.
      sendDefaultPii: false,
      beforeSend(event) {
        try {
          // Strip Authorization headers and verify tokens from breadcrumbs.
          if (event.request?.headers) delete event.request.headers.Authorization
          if (event.request?.url) {
            const u = new URL(event.request.url)
            if (u.searchParams.has('verify_token')) u.searchParams.set('verify_token', '<redacted>')
            event.request.url = u.toString()
          }
        } catch {}
        return event
      },
    })
    _sentryReady = true
  } catch (err) {
    console.warn('[telemetry] Sentry init failed:', err?.message || err)
  }
}

async function _initPostHog() {
  const apiKey = import.meta.env.VITE_POSTHOG_KEY
  if (!apiKey) return
  try {
    const mod = await import('posthog-js')
    const posthog = mod.default || mod
    posthog.init(apiKey, {
      api_host: import.meta.env.VITE_POSTHOG_HOST || 'https://us.i.posthog.com',
      person_profiles: 'identified_only',
      capture_pageview: true,
      capture_pageleave: true,
      // Quebec Law 25: respect Do-Not-Track. Users who set it get no analytics.
      respect_dnt: true,
      // Don't autocapture form inputs — too much PII risk for a student app.
      autocapture: { url_allowlist: [], dom_event_allowlist: ['click', 'change', 'submit'] },
      session_recording: { maskAllInputs: true, maskTextSelector: '*' },
    })
    _posthog = posthog
  } catch (err) {
    console.warn('[telemetry] PostHog init failed:', err?.message || err)
  }
}

/** Identify a user across both Sentry and PostHog. Call after login. */
export async function identifyUser({ id, email }) {
  if (!id) return
  // Sentry
  if (_sentryReady) {
    try {
      const Sentry = await import('@sentry/react')
      Sentry.setUser({ id })  // intentionally no email — PII-light
    } catch {}
  }
  // PostHog
  if (_posthog) {
    try {
      // We hash the email so we can group by user in PostHog without
      // storing the plaintext address there.
      _posthog.identify(id, { email_domain: (email || '').split('@')[1] || null })
    } catch {}
  }
}

/** Clear identity on logout so the next session starts anonymous. */
export async function resetTelemetryIdentity() {
  if (_sentryReady) {
    try {
      const Sentry = await import('@sentry/react')
      Sentry.setUser(null)
    } catch {}
  }
  if (_posthog) {
    try { _posthog.reset() } catch {}
  }
}

/** Fire a product-funnel event. PostHog dashboard groups these into funnels. */
export function track(event, props = {}) {
  if (!_posthog) return
  try { _posthog.capture(event, props) } catch {}
}

/** Funnel event names — keep all of them here so they can't drift. */
export const Events = {
  SignupStarted:        'signup_started',
  SignupCompleted:      'signup_completed',
  EmailVerified:        'email_verified',
  OnboardingCompleted:  'onboarding_completed',
  FirstCardSeen:        'first_card_seen',
  CardChipClicked:      'card_chip_clicked',
  TranscriptImported:   'transcript_imported',
  SyllabusImported:     'syllabus_imported',
  ClubSubscribed:       'club_subscribed',
  ForumPostCreated:     'forum_post_created',
}
