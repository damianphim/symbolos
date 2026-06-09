import React, { useState, useEffect, useCallback } from 'react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { PreferencesProvider } from './contexts/PreferencesContext'
import Login from './components/Auth/Login'
import LandingPage from './components/Landing/LandingPage'
import PrivacyPolicy from './components/Legal/PrivacyPolicy'
import TermsOfService from './components/Legal/TOS'
import AboutUs from './components/Legal/AboutUs'
import Dashboard from './components/Dashboard/Dashboard'
import ProfileSetup from './components/ProfileSetup/ProfileSetup'
import Loading from './components/Loading/Loading'
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'
import ErrorScreen from './components/ErrorScreen/ErrorScreen'
import { authAPI } from './lib/api'
import './theme.css'
import './App.css'
import AdminSuggestions from './components/Admin/AdminSuggestions'

function AppContent() {
  const { user, profile, loading, error, needsOnboarding, refreshProfile } = useAuth()
  const [verifying, setVerifying] = useState(false)
  const [verifyError, setVerifyError] = useState('')

  // SEC FIX (audit #11): the verification email links to /privacy and /terms.
  // The Vercel rewrite turns those into /?show=privacy and /?show=terms;
  // here we open the corresponding legal modal so the URLs don't 404.
  const _initialLegal = (() => {
    if (typeof window === 'undefined') return null
    const p = new URLSearchParams(window.location.search)
    const show = p.get('show')
    if (show === 'privacy' || show === 'terms' || show === 'about') return show
    return null
  })()
  const [legalModal, setLegalModal] = useState(_initialLegal)

  // Unauthenticated users see the marketing landing page first. They can click
  // "Sign in" anywhere on it to swap to the login form. We honor URL hints
  // (?signin or hash #signin) and the verification-flow path so the legacy
  // direct-to-login links keep working.
  const _initialShowLogin = (() => {
    if (typeof window === 'undefined') return false
    const p = new URLSearchParams(window.location.search)
    return p.has('signin') || p.has('verify_token') || window.location.hash === '#signin'
  })()
  const [showLogin, setShowLogin] = useState(_initialShowLogin)

  // Brief flash-prevention only — render as soon as auth resolves (no
  // artificial 2s minimum, that was costing every user 2s on first paint).
  const [minLoadDone, setMinLoadDone] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setMinLoadDone(true), 250)
    return () => clearTimeout(t)
  }, [])

  // Handle ?verify_token=xxx&user_id=xxx — sent by the verification email link
  const handleVerifyToken = useCallback(async () => {
    const params = new URLSearchParams(window.location.search)
    const token = params.get('verify_token')
    const userId = params.get('user_id')
    if (!token || !userId) return

    // Clear params from URL immediately so reloads don't re-trigger
    window.history.replaceState({}, '', window.location.pathname)

    setVerifying(true)
    try {
      await authAPI.verifyEmail(userId, token)
      await refreshProfile()
      try {
        const { track, Events } = await import('./lib/telemetry')
        track(Events.EmailVerified)
      } catch {}
    } catch (err) {
      setVerifyError(err?.response?.data?.detail || 'Verification failed. The link may have expired.')
    } finally {
      setVerifying(false)
    }
  }, [refreshProfile])

  useEffect(() => { handleVerifyToken() }, [handleVerifyToken])

  if (loading || !minLoadDone || verifying) return <Loading />

  if (verifyError) {
    return (
      <ErrorScreen
        variant="verifyFailed"
        customMessage={verifyError}
        showReload={false}
        showSignIn={true}
        showHome={false}
        onSignIn={() => { setVerifyError(''); window.location.replace('/') }}
      />
    )
  }

  if (error?.type === 'AUTH_INIT_FAILED') {
    return (
      <ErrorScreen
        variant="authFailed"
        showReload={true}
        showHome={false}
      />
    )
  }

  if (user && window.location.pathname === '/admin') return <AdminSuggestions />

  if (user && needsOnboarding) return <ProfileSetup />

  // Signed in but email not verified → show Login in verify mode
  if (user && profile && profile.email_verified === false) return <Login forceVerify email={profile.email} userId={user.id} />

  if (user && profile) return <Dashboard />

  if (user && !profile && !error) return <Loading />

  // SEC FIX (audit #11): /privacy and /terms get rewritten to /?show=...
  // and we render the corresponding legal modal over the landing page so
  // verification-email footer links actually work.
  const _closeLegal = () => {
    setLegalModal(null)
    try {
      const url = new URL(window.location.href)
      url.searchParams.delete('show')
      window.history.replaceState({}, '', url.toString())
    } catch {}
  }

  // Unauthenticated: show landing first; click "Sign in" → show Login.
  const main = showLogin
    ? <Login onBack={() => setShowLogin(false)} />
    : <LandingPage onSignIn={() => setShowLogin(true)} />

  return (
    <>
      {main}
      {legalModal === 'privacy' && <PrivacyPolicy onClose={_closeLegal} />}
      {legalModal === 'terms'   && <TermsOfService onClose={_closeLegal} />}
      {legalModal === 'about'   && <AboutUs onClose={_closeLegal} />}
    </>
  )
}

function App() {
  return (
    <ErrorBoundary>
      <PreferencesProvider>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </PreferencesProvider>
    </ErrorBoundary>
  )
}

export default App
