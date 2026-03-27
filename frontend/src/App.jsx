import React, { useState, useEffect, useCallback } from 'react'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { ThemeProvider } from './contexts/ThemeContext'
import { LanguageProvider } from './contexts/LanguageContext'
import { TimezoneProvider } from './contexts/TimezoneContext'
import Login from './components/Auth/Login'
import Dashboard from './components/Dashboard/Dashboard'
import ProfileSetup from './components/ProfileSetup/ProfileSetup'
import Loading from './components/Loading/Loading'
import ErrorBoundary from './components/ErrorBoundary/ErrorBoundary'
import { authAPI } from './lib/api'
import './theme.css'
import './App.css'
import AdminSuggestions from './components/Admin/AdminSuggestions'

function AppContent() {
  const { user, profile, loading, error, needsOnboarding, refreshProfile } = useAuth()
  const [verifying, setVerifying] = useState(false)
  const [verifyError, setVerifyError] = useState('')

  // Enforce 2-second minimum loading screen
  const [minLoadDone, setMinLoadDone] = useState(false)
  useEffect(() => {
    const t = setTimeout(() => setMinLoadDone(true), 2000)
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
      <div className="error-screen">
        <h2>Verification failed</h2>
        <p>{verifyError}</p>
        <button onClick={() => { setVerifyError(''); window.location.replace('/') }}>Back to sign in</button>
      </div>
    )
  }

  if (error?.type === 'AUTH_INIT_FAILED') {
    return (
      <div className="error-screen">
        <h2>Unable to initialize authentication</h2>
        <p>Please refresh the page or check your internet connection.</p>
        <button onClick={() => window.location.reload()}>Reload Page</button>
      </div>
    )
  }

  if (user && window.location.pathname === '/admin') return <AdminSuggestions />

  if (user && needsOnboarding) return <ProfileSetup />

  // Signed in but email not verified → show Login in verify mode
  if (user && profile && profile.email_verified === false) return <Login forceVerify email={profile.email} userId={user.id} />

  if (user && profile) return <Dashboard />

  if (user && !profile && !error) return <Loading />

  return <Login />
}

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <LanguageProvider>
          <TimezoneProvider>
            <AuthProvider>
              <AppContent />
            </AuthProvider>
          </TimezoneProvider>
        </LanguageProvider>
      </ThemeProvider>
    </ErrorBoundary>
  )
}

export default App
