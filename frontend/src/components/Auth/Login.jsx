import { useState, useEffect, useRef } from 'react'
import { HiLightBulb } from 'react-icons/hi'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage, useTheme } from '../../contexts/PreferencesContext'
import { supabase } from '../../lib/supabase'
import {
  validateEmail,
  validatePassword,
  validateUsername,
} from '../../utils/validation'
import PrivacyPolicy from '../Legal/PrivacyPolicy'
import TermsOfService from '../Legal/TOS'
import AboutUs from '../Legal/AboutUs'
import { authAPI } from '../../lib/api'
import logoMark from '../../assets/loading-logo.png'
import './Auth.css'

function Login({ forceVerify = false, email: propEmail = '', userId: propUserId = '', onBack = null }) {
  // Restore verify screen if the component remounts mid-verification
  const storedVerify = (() => { try { return JSON.parse(sessionStorage.getItem('symbolos_verify') || 'null') } catch { return null } })()

  const [mode, setMode] = useState(forceVerify || storedVerify ? 'verify' : 'login') // 'login' | 'signup' | 'forgot' | 'reset' | 'verify'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [username, setUsername] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [animating, setAnimating] = useState(false)
  const [pendingEmail, setPendingEmail] = useState(propEmail || storedVerify?.email || '')
  const [pendingUserId, setPendingUserId] = useState(propUserId || storedVerify?.userId || '')
  // Message to surface *after* a mode transition (survives the mode-change effect's setMessage(''))
  const pendingMsgRef = useRef('')
  const [resendCooldown, setResendCooldown] = useState(0)
  const [resendLoading, setResendLoading] = useState(false)
  // 6-digit OTP entry on the verify screen. McGill inboxes (Microsoft 365)
  // run Safe Links, which auto-fetches the confirmation link seconds after
  // delivery — confirming the account before the user ever opens the email
  // (which often sits in Junk). A typed code can't be consumed by a scanner,
  // so this is the reliable path; link-click and polling remain as fallbacks.
  const [verifyCode, setVerifyCode] = useState('')
  const [verifyingCode, setVerifyingCode] = useState(false)
  const [legalModal, setLegalModal] = useState(null) // 'privacy' | 'terms' | 'about'
  const pollRef = useRef(null)

  const { signIn, signUp, resetPasswordForEmail, resendVerificationEmail, error: authError, clearError } = useAuth()
  const { t, language, setLanguage } = useLanguage()
  const { resolvedTheme, setTheme } = useTheme()
  const cycleTheme = () => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')

  const isLogin  = mode === 'login'
  const isSignup = mode === 'signup'
  const isForgot = mode === 'forgot'
  const isVerify = mode === 'verify'

  useEffect(() => {
    clearError()
    setErrors({})
    // If a message was queued to survive this mode transition, apply it now.
    if (pendingMsgRef.current) {
      setMessage(pendingMsgRef.current)
      pendingMsgRef.current = ''
    } else {
      setMessage('')
    }
  }, [mode, clearError])

  // Poll for verification completion when on the verify screen.
  // Two paths:
  //   A. Session present (autoconfirm ON or partial session): check
  //      session.user.email_confirmed_at and refresh so SIGNED_IN re-fires.
  //   B. No session (autoconfirm OFF — the common partner-configured case):
  //      call our unauthenticated /check-verified endpoint. When the phone's
  //      magic-link confirms the address in Supabase Auth, the backend sees
  //      email_confirmed_at and returns verified=true. We then auto-sign-in
  //      using the password still held in component state (typed during signup
  //      and never cleared on mode-switch). If the page was reloaded and the
  //      password is gone, we fall back to a "Verified — please sign in" state.
  useEffect(() => {
    if (mode !== 'verify') {
      if (pollRef.current) clearInterval(pollRef.current)
      return
    }

    const checkAndAdvance = async () => {
      try {
        // Path A: we already have a session on this device
        const { data: { session } } = await supabase.auth.getSession()
        if (session?.user?.email_confirmed_at) {
          clearInterval(pollRef.current)
          sessionStorage.removeItem('symbolos_verify')
          await supabase.auth.refreshSession()
          return
        }

        // Path B: no session — poll our unauthenticated endpoint
        if (!pendingUserId) return
        const { verified } = await authAPI.checkVerified(pendingUserId)
        if (!verified) return

        clearInterval(pollRef.current)
        sessionStorage.removeItem('symbolos_verify')

        if (password) {
          // Auto-sign-in using the credentials still in state
          const { error: signInErr } = await signIn(pendingEmail || email, password)
          if (signInErr) {
            // Sign-in failed — surface the login form so user can retry
            sessionStorage.removeItem('symbolos_verify')
            setMode('login')
          }
          // On success SIGNED_IN fires → AuthContext loads profile → app advances
        } else {
          // Page was reloaded; password is gone. Queue message to survive the
          // mode-change effect's setMessage(''), then fall back to login form.
          pendingMsgRef.current = t('auth.verifiedSignIn') || 'Email verified! Please sign in to continue.'
          setMode('login')
        }
      } catch { /* network errors are silent — next tick retries */ }
    }

    pollRef.current = setInterval(checkAndAdvance, 3000)
    return () => clearInterval(pollRef.current)
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [mode, pendingUserId])

  // Resend cooldown countdown
  useEffect(() => {
    if (resendCooldown <= 0) return
    const t = setTimeout(() => setResendCooldown(c => c - 1), 1000)
    return () => clearTimeout(t)
  }, [resendCooldown])

  const switchMode = (newMode) => {
    if (newMode === mode) return
    if (newMode !== 'verify') sessionStorage.removeItem('symbolos_verify')
    setAnimating(true)
    setTimeout(() => {
      setMode(newMode)
      setAnimating(false)
    }, 180)
  }

  const validateForm = () => {
    const newErrors = {}
    const emailError = validateEmail(email)
    if (emailError) newErrors.email = emailError
    if (!isForgot && !isVerify) {
      const passwordError = validatePassword(password, isSignup)
      if (passwordError) newErrors.password = passwordError
    }
    if (isSignup) {
      const usernameError = validateUsername(username)
      if (usernameError) newErrors.username = usernameError
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  // Verify the emailed 6-digit code. On success Supabase returns a session
  // and fires SIGNED_IN, so the app advances exactly like the link path.
  const handleVerifyCode = async (e) => {
    e?.preventDefault?.()
    const code = verifyCode.trim()
    if (!/^\d{6}$/.test(code) || verifyingCode) return
    setVerifyingCode(true)
    setErrors({})
    try {
      const { error } = await supabase.auth.verifyOtp({
        email: pendingEmail || email,
        token: code,
        type: 'signup',
      })
      if (error) throw error
      sessionStorage.removeItem('symbolos_verify')
      // SIGNED_IN fires → AuthContext loads the profile → app advances.
    } catch (err) {
      setErrors({ form: t('auth.codeInvalid') })
      console.warn('OTP verify failed:', err?.message)
    } finally {
      setVerifyingCode(false)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage('')
    setErrors({})
    if (!validateForm()) return
    setLoading(true)
    try {
      if (isForgot) {
        const { error } = await resetPasswordForEmail(email)
        if (error) setErrors({ form: error.message })
        else setMessage(t('auth.resetSent'))
        return
      }
      if (isLogin) {
        const { error } = await signIn(email, password)
        if (error) setErrors({ form: error.message })
      } else {
        const { data, error, needsEmailVerification } = await signUp(email, password, username.trim())
        if (error) setErrors({ form: error.message })
        else if (needsEmailVerification) {
          const uid = data?.user?.id || ''
          setPendingEmail(email)
          if (uid) setPendingUserId(uid)
          setResendCooldown(60)
          sessionStorage.setItem('symbolos_verify', JSON.stringify({ email, userId: uid }))
          // Mark this user for onboarding so ProfileSetup shows after they
          // verify and sign in (survives the cross-tab/cross-device flow).
          if (uid) localStorage.setItem('symbolos_pending_onboarding', uid)
          switchMode('verify')
        }
      }
    } catch (err) {
      setErrors({ form: err.message || t('auth.genericError') })
    } finally {
      setLoading(false)
    }
  }

  const passwordStrength = (pw) => {
    if (!pw) return { level: 0, label: '', color: '' }
    let score = 0
    if (pw.length >= 8) score++
    if (/[A-Z]/.test(pw)) score++
    if (/[a-z]/.test(pw)) score++
    if (/\d/.test(pw)) score++
    if (/[^A-Za-z0-9]/.test(pw)) score++
    if (score <= 2) return { level: score, label: t('auth.strengthWeak'), color: 'var(--error-primary)' }
    if (score <= 3) return { level: score, label: t('auth.strengthFair'), color: 'var(--warning-primary)' }
    if (score <= 4) return { level: score, label: t('auth.strengthGood'), color: 'var(--success-primary)' }
    return { level: score, label: t('auth.strengthStrong'), color: 'var(--success-hover)' }
  }

  const strength   = isSignup ? passwordStrength(password) : null
  const formError  = errors.form || authError?.message

  return (
    <div className="auth-page">
      {/* ── Legal modals ── */}
      {legalModal === 'privacy' && <PrivacyPolicy onClose={() => setLegalModal(null)} />}
      {legalModal === 'terms'   && <TermsOfService onClose={() => setLegalModal(null)} />}
      {legalModal === 'about'   && <AboutUs onClose={() => setLegalModal(null)} />}
      {/* ── Corner controls ── */}
      <div className="auth-corner-controls">
        {onBack && (
          <button
            className="auth-lang-btn"
            onClick={onBack}
            title="Back to landing page"
            style={{ paddingInline: '12px' }}
          >
            ← Home
          </button>
        )}
        <button
          className="auth-lang-btn"
          onClick={() => setLanguage(language === 'en' ? 'fr' : language === 'fr' ? 'zh' : 'en')}
          title={t('auth.langToggle')}
        >
          {language === 'en' ? 'FR' : language === 'fr' ? '中' : 'EN'}
        </button>
        <button
          className="auth-lang-btn"
          onClick={cycleTheme}
          title={resolvedTheme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          {resolvedTheme === 'dark' ? '☀' : '☽'}
        </button>
      </div>

      {/* ── Left branding panel ── */}
      <aside className="auth-branding">
        <div className="auth-branding-inner">
          <div className="auth-logo">
            <div className="auth-logo-mark">
              <img src={logoMark} alt="Symbolos" className="auth-logo-mark-img" />
            </div>
            <span className="auth-logo-name">Symbolos</span>
          </div>

          <div className="auth-branding-copy">
            <h1 className="auth-branding-headline">
              {t('auth.brandHeadline')}
            </h1>
            <p className="auth-branding-disclaimer">{t('legal.notAffiliatedShort')}</p>
          </div>

          <ul className="auth-feature-list">
            {[t('auth.feature1'), t('auth.feature2'), t('auth.feature3'), t('auth.feature4')].map(text => (
              <li key={text} className="auth-feature-item">
                <span className="auth-feature-bullet" aria-hidden="true">•</span>
                <span>{text}</span>
              </li>
            ))}
          </ul>
          {/* Legal links on branding panel (visible on desktop) */}
          <div className="auth-branding-legal">
            <button type="button" className="auth-branding-legal-link" onClick={() => setLegalModal('about')}>{t('legal.navAbout')}</button>
            <span className="auth-branding-legal-sep">·</span>
            <button type="button" className="auth-branding-legal-link" onClick={() => setLegalModal('privacy')}>{t('legal.navPrivacy')}</button>
            <span className="auth-branding-legal-sep">·</span>
            <button type="button" className="auth-branding-legal-link" onClick={() => setLegalModal('terms')}>{t('legal.navTerms')}</button>
          </div>
        </div>
      </aside>

      {/* ── Right form panel ── */}
      <main className="auth-form-panel">
        <div className={`auth-card ${animating ? 'auth-card--out' : 'auth-card--in'}`}>

          {/* Email verification screen */}
          {isVerify && (
            <div className="auth-verify-screen">
              <div className="auth-verify-icon">✉</div>
              <h2 className="auth-card-title">Verify your email to continue</h2>
              <p className="auth-card-subtitle">
                We sent a verification email to <strong>{pendingEmail}</strong>.<br />
                {t('auth.codeSubtitle')}
              </p>

              {/* 6-digit code entry — the reliable path (see verifyCode note) */}
              <form className="auth-verify-code-row" onSubmit={handleVerifyCode}>
                <input
                  className="auth-input auth-verify-code-input"
                  type="text"
                  inputMode="numeric"
                  autoComplete="one-time-code"
                  maxLength={6}
                  placeholder="123456"
                  value={verifyCode}
                  onChange={(e) => setVerifyCode(e.target.value.replace(/\D/g, ''))}
                  aria-label={t('auth.codeLabel')}
                />
                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={verifyCode.trim().length !== 6 || verifyingCode}
                >
                  {verifyingCode ? '…' : t('auth.codeVerifyBtn')}
                </button>
              </form>

              <p className="auth-verify-hint">This page will continue automatically once you verify.</p>
              <button
                className="btn btn-primary btn-full"
                style={{ marginTop: '20px' }}
                disabled={resendCooldown > 0 || resendLoading}
                onClick={async () => {
                  setResendLoading(true)
                  const { error } = await resendVerificationEmail(pendingEmail)
                  setResendLoading(false)
                  if (error) setErrors({ form: error.message })
                  else { setMessage('Verification email resent!'); setResendCooldown(60) }
                }}
              >
                {resendLoading ? 'Sending…' : resendCooldown > 0 ? `Resend email (${resendCooldown}s)` : 'Resend verification email'}
              </button>
              {message && <p className="auth-verify-success">{message}</p>}
              {errors.form && <p className="auth-error-msg" style={{ marginTop: '8px' }}>{errors.form}</p>}
              <button className="auth-back-btn" style={{ marginTop: '16px' }} onClick={() => switchMode('login')}>
                Back to sign in
              </button>
            </div>
          )}

          {/* Tabs — only for login/signup */}
          {!isForgot && !isVerify && (
            <div className="auth-tabs" role="tablist">
              <button
                role="tab"
                aria-selected={isLogin}
                className={`auth-tab ${isLogin ? 'auth-tab--active' : ''}`}
                onClick={() => switchMode('login')}
                disabled={loading}
              >
                {t('auth.tabSignIn')}
              </button>
              <button
                role="tab"
                aria-selected={isSignup}
                className={`auth-tab ${isSignup ? 'auth-tab--active' : ''}`}
                onClick={() => switchMode('signup')}
                disabled={loading}
              >
                {t('auth.tabCreate')}
              </button>
              <div className={`auth-tab-slider ${isSignup ? 'auth-tab-slider--right' : ''}`} />
            </div>
          )}

          {!isVerify && (
            <>
              <div className="auth-card-header">
                <h2 className="auth-card-title">
                  {isForgot ? t('auth.titleForgot') : isLogin ? t('auth.titleLogin') : t('auth.titleSignup')}
                </h2>
                <p className="auth-card-subtitle">
                  {isForgot ? t('auth.subForgot') : isLogin ? t('auth.subLogin') : t('auth.subSignup')}
                </p>
                {isLogin && (
                  <p className="auth-card-tip"><HiLightBulb />{t('auth.mcgillTip')}</p>
                )}
              </div>

              {formError && (
                <div className="auth-alert auth-alert--error" role="alert">
                  <span className="auth-alert-icon">!</span>
                  <span>{formError}</span>
                </div>
              )}

              {message && (
                <div className="auth-alert auth-alert--success" role="alert">
                  <span className="auth-alert-icon">✓</span>
                  <span>{message}</span>
                </div>
              )}

              <form onSubmit={handleSubmit} className="auth-form" noValidate>

                {isSignup && (
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="username">{t('auth.labelUsername')}</label>
                    <input
                      id="username"
                      type="text"
                      className={`auth-input ${errors.username ? 'auth-input--error' : ''}`}
                      placeholder="e.g. john_doe"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      autoComplete="username"
                      disabled={loading}
                    />
                    {errors.username && <p className="auth-error-msg">{errors.username}</p>}
                  </div>
                )}

                <div className="auth-field">
                  <label className="auth-label" htmlFor="email">{t('auth.labelEmail')}</label>
                  <input
                    id="email"
                    type="email"
                    className={`auth-input ${errors.email ? 'auth-input--error' : ''}`}
                    placeholder={t('auth.emailPlaceholder')}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoComplete="email"
                    disabled={loading}
                  />
                  {errors.email && <p className="auth-error-msg">{errors.email}</p>}
                </div>

                {!isForgot && (
                  <div className="auth-field">
                    <div className="auth-label-row">
                      <label className="auth-label" htmlFor="password">{t('auth.labelPassword')}</label>
                      {isLogin && (
                        <button
                          type="button"
                          className="auth-forgot-btn"
                          onClick={() => switchMode('forgot')}
                          disabled={loading}
                        >
                          {t('auth.forgotLink')}
                        </button>
                      )}
                    </div>
                    <div className="auth-input-wrap">
                      <input
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        className={`auth-input auth-input--has-icon ${errors.password ? 'auth-input--error' : ''}`}
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        autoComplete={isLogin ? 'current-password' : 'new-password'}
                        disabled={loading}
                      />
                      <button
                        type="button"
                        className="auth-pw-toggle"
                        onClick={() => setShowPassword(v => !v)}
                        aria-label={showPassword ? t('auth.hidePassword') : t('auth.showPassword')}
                        tabIndex={-1}
                      >
                        {showPassword ? (
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/>
                          </svg>
                        ) : (
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                          </svg>
                        )}
                      </button>
                    </div>
                    {errors.password && <p className="auth-error-msg">{errors.password}</p>}
                    {isSignup && !errors.password && (
                      <p className="auth-hint">{t('auth.passwordHint')}</p>
                    )}

                    {isSignup && password && (
                      <div className="auth-strength">
                        <div className="auth-strength-bar">
                          {[1, 2, 3, 4, 5].map((i) => (
                            <div
                              key={i}
                              className="auth-strength-seg"
                              style={{ background: i <= strength.level ? strength.color : 'var(--border-primary)' }}
                            />
                          ))}
                        </div>
                        <span className="auth-strength-label" style={{ color: strength.color }}>
                          {strength.label}
                        </span>
                      </div>
                    )}
                  </div>
                )}

                {/* Clickwrap notice (Law 25 / contract): completing signup
                    constitutes acceptance. Backend records version+timestamp. */}
                {!isLogin && !isForgot && (
                  <p className="auth-clickwrap">
                    {t('auth.clickwrapPre')}{' '}
                    <button type="button" className="auth-clickwrap-link" onClick={() => setLegalModal('terms')}>
                      {t('legal.navTerms')}
                    </button>
                    {' '}{t('auth.clickwrapAnd')}{' '}
                    <button type="button" className="auth-clickwrap-link" onClick={() => setLegalModal('privacy')}>
                      {t('legal.navPrivacy')}
                    </button>.
                  </p>
                )}

                <button type="submit" className="btn btn-primary btn-full" disabled={loading}>
                  {loading ? (
                    <span className="btn-loading">
                      <span className="spinner" />
                      {isForgot ? t('auth.loadingForgot') : isLogin ? t('auth.loadingLogin') : t('auth.loadingSignup')}
                    </span>
                  ) : (
                    isForgot ? t('auth.btnForgot') : isLogin ? t('auth.btnLogin') : t('auth.btnSignup')
                  )}
                </button>
              </form>

              <div className="auth-footer">
                {isForgot ? (
                  <button className="auth-back-btn" onClick={() => switchMode('login')}>
                    {t('auth.backToLogin')}
                  </button>
                ) : (
                  <p className="auth-toggle">
                    {isLogin ? t('auth.noAccount') : t('auth.hasAccount')}
                    {' '}
                    <button
                      type="button"
                      className="auth-toggle-btn"
                      onClick={() => switchMode(isLogin ? 'signup' : 'login')}
                      disabled={loading}
                    >
                      {isLogin ? t('auth.signUpLink') : t('auth.signInLink')}
                    </button>
                  </p>
                )}
              </div>
              {/* Legal links — shown on mobile (branding panel is hidden) */}
              <div className="auth-legal-links">
                <button type="button" className="auth-legal-link" onClick={() => setLegalModal('about')}>{t('legal.navAbout')}</button>
                <span className="auth-legal-sep">·</span>
                <button type="button" className="auth-legal-link" onClick={() => setLegalModal('privacy')}>{t('legal.navPrivacy')}</button>
                <span className="auth-legal-sep">·</span>
                <button type="button" className="auth-legal-link" onClick={() => setLegalModal('terms')}>{t('legal.navTerms')}</button>
              </div>
            </>
          )}

        </div>
      </main>
    </div>
  )
}

export default Login
