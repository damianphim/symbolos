import { useState, useEffect } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/LanguageContext'
import { useTheme } from '../../contexts/ThemeContext'
import {
  validateEmail,
  validatePassword,
  validateUsername,
} from '../../utils/validation'
import './Auth.css'

function Login() {
  const [mode, setMode] = useState('login') // 'login' | 'signup' | 'forgot'
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [username, setUsername] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [animating, setAnimating] = useState(false)

  const { signIn, signUp, error: authError, clearError } = useAuth()
  const { t, language, setLanguage } = useLanguage()
  const { resolvedTheme, setTheme } = useTheme()
  const cycleTheme = () => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')

  const isLogin = mode === 'login'
  const isSignup = mode === 'signup'
  const isForgot = mode === 'forgot'

  useEffect(() => {
    clearError()
    setErrors({})
    setMessage('')
  }, [mode, clearError])

  const switchMode = (newMode) => {
    if (newMode === mode) return
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
    if (!isForgot) {
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

  const handleSubmit = async (e) => {
    e.preventDefault()
    setMessage('')
    setErrors({})
    if (!validateForm()) return
    setLoading(true)
    try {
      if (isForgot) {
        setMessage(t('auth.resetSent'))
        return
      }
      if (isLogin) {
        const { error } = await signIn(email, password)
        if (error) setErrors({ form: error.message })
      } else {
        const { error } = await signUp(email, password, username.trim())
        if (error) setErrors({ form: error.message })
        else setMessage(t('auth.accountCreated'))
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

  const strength = isSignup ? passwordStrength(password) : null
  const formError = errors.form || authError?.message

  return (
    <div className="auth-page">
      {/* ── Corner controls ── */}
      <div className="auth-corner-controls">
        <button
          className="auth-lang-btn"
          onClick={() => setLanguage(language === 'en' ? 'fr' : 'en')}
          title={t('auth.langToggle')}
        >
          {language === 'en' ? 'FR' : 'EN'}
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
              <svg width="26" height="26" viewBox="0 0 28 28" fill="none">
                <circle cx="14" cy="14" r="5" fill="white" opacity="0.95"/>
                <circle cx="14" cy="14" r="11" stroke="white" strokeWidth="1.5" opacity="0.35"/>
                <circle cx="14" cy="14" r="7" stroke="white" strokeWidth="1" opacity="0.6"/>
              </svg>
            </div>
            <span className="auth-logo-name">Symbolos</span>
          </div>

          <div className="auth-branding-copy">
            <h1 className="auth-branding-headline">
              {t('auth.brandHeadline')}
            </h1>
            <p className="auth-branding-sub">
              {t('auth.brandSub')}
            </p>
          </div>

          <ul className="auth-feature-list">
            {[
              t('auth.feature1'),
              t('auth.feature2'),
              t('auth.feature3'),
              t('auth.feature4'),
            ].map((text) => (
              <li key={text} className="auth-feature-item">
                <span className="auth-feature-dot" />
                <span>{text}</span>
              </li>
            ))}
          </ul>
        </div>
      </aside>

      {/* ── Right form panel ── */}
      <main className="auth-form-panel">
        <div className={`auth-card ${animating ? 'auth-card--out' : 'auth-card--in'}`}>

          {!isForgot && (
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

          <div className="auth-card-header">
            <h2 className="auth-card-title">
              {isForgot ? t('auth.titleForgot') : isLogin ? t('auth.titleLogin') : t('auth.titleSignup')}
            </h2>
            <p className="auth-card-subtitle">
              {isForgot ? t('auth.subForgot') : isLogin ? t('auth.subLogin') : t('auth.subSignup')}
            </p>
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
                placeholder="you@mail.mcgill.ca"
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

        </div>
      </main>
    </div>
  )
}

export default Login
