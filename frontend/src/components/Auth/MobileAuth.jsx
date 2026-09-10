import { FaChevronLeft, FaSun, FaMoon, FaRegEnvelope } from 'react-icons/fa'
import { useLanguage, useTheme } from '../../contexts/PreferencesContext'
import PrivacyPolicy from '../Legal/PrivacyPolicy'
import TermsOfService from '../Legal/TOS'
import AboutUs from '../Legal/AboutUs'
import logoMark from '../../assets/logo-mark.png'
import './MobileAuth.css'

/**
 * Mobile presentation of the auth flow (<=768px, viewport-gated, mobile web
 * gets this too, not just the installed app).
 *
 * Pure presentation. Every piece of state and every handler is owned by
 * Login.jsx and passed in; this file must never call supabase, validate, or
 * decide what a mode does. Splitting it out rather than branching inside
 * Login's JSX is deliberate: the desktop tree then stays literally untouched,
 * which is the one thing that must not regress on a live product.
 *
 * Continues MobileWelcome.jsx, same system font stack, same 50px/12px button
 * geometry, same spacing rhythm, so signing up doesn't feel like a hand-off
 * to a website.
 */
export default function MobileAuth({
  mode,
  email, setEmail,
  password, setPassword,
  username, setUsername,
  showPassword, setShowPassword,
  errors, loading, message, formError, strength,
  handleSubmit, switchMode, animating,
  verifyCode, setVerifyCode, handleVerifyCode, verifyingCode,
  resetCode, setResetCode, newPassword, setNewPassword, handleResetPassword, resettingPassword,
  pendingEmail, resendCooldown, resendLoading, handleResend,
  legalModal, setLegalModal,
  onBack,
}) {
  const { t, language, setLanguage } = useLanguage()
  const { resolvedTheme, setTheme } = useTheme()

  // t() returns the key itself when a translation is missing, which would put
  // a raw "auth.foo" on screen. Fall back to copy until the locale files land.
  const tr = (key, fallback) => {
    const value = t(key)
    return value === key ? fallback : value
  }

  const isLogin  = mode === 'login'
  const isSignup = mode === 'signup'
  const isForgot = mode === 'forgot'
  const isVerify = mode === 'verify'
  const isReset  = mode === 'reset'

  // Leading chevron replaces the browser-style "← Back" link. forgot/verify
  // are pushed states within auth, so they pop back to sign-in; on the root
  // login/signup screen the only thing behind us is whatever opened Login.
  const back = isForgot || isVerify || isReset
    ? () => switchMode('login')
    : onBack

  const title = isVerify ? t('auth.titleVerify')
    : isReset  ? t('auth.titleReset')
    : isForgot ? t('auth.titleForgot')
    : isLogin  ? t('auth.titleLogin')
    : t('auth.titleSignup')

  const subtitle = isReset ? t('auth.subReset')
    : isForgot ? t('auth.subForgot')
    : isLogin ? t('auth.subLogin')
    : t('auth.subSignup')

  return (
    <div className="ma-root">
      {legalModal === 'privacy' && <PrivacyPolicy onClose={() => setLegalModal(null)} />}
      {legalModal === 'terms'   && <TermsOfService onClose={() => setLegalModal(null)} />}
      {legalModal === 'about'   && <AboutUs onClose={() => setLegalModal(null)} />}

      {/* Not a title bar, the screen title lives in the content. This strip
          only carries navigation and the two global toggles. */}
      <div className="ma-nav">
        {back ? (
          <button type="button" className="ma-nav-back" onClick={back} aria-label={tr('auth.back', 'Back')}>
            <FaChevronLeft size={17} />
          </button>
        ) : <span className="ma-nav-spacer" />}

        <div className="ma-nav-actions">
          <button
            type="button"
            className="ma-nav-btn"
            onClick={() => setLanguage(language === 'en' ? 'fr' : language === 'fr' ? 'zh' : 'en')}
            aria-label={t('auth.langToggle')}
          >
            {language === 'en' ? 'FR' : language === 'fr' ? '中' : 'EN'}
          </button>
          <button
            type="button"
            className="ma-nav-btn"
            onClick={() => setTheme(resolvedTheme === 'dark' ? 'light' : 'dark')}
            aria-label={resolvedTheme === 'dark' ? 'Light mode' : 'Dark mode'}
          >
            {resolvedTheme === 'dark' ? <FaSun size={14} /> : <FaMoon size={14} />}
          </button>
        </div>
      </div>

      {/* The single scroller for the screen. The submit button sits in normal
          flow at the end of it (never position:fixed, a fixed footer renders
          *behind* the iOS keyboard), and .ma-scroll carries enough bottom
          padding + scroll-padding that the browser's focus scroll can always
          lift the active field and the button clear of the keyboard. */}
      <div className="ma-scroll">
        <div className={`ma-content ${animating ? 'ma-content--out' : 'ma-content--in'}`}>

          <header className="ma-header">
            <img src={logoMark} alt="" className="ma-logo" />
            <h1 className="ma-title">{title}</h1>
            {isVerify ? (
              <p className="ma-subtitle">
                {tr('auth.verifySentTo', 'We sent a verification email to')}{' '}
                <strong className="ma-verify-email">{pendingEmail}</strong>
                <br />
                {t('auth.codeSubtitle')}
              </p>
            ) : (
              <p className="ma-subtitle">{subtitle}</p>
            )}
          </header>

          {isVerify ? (
            <>
              <form className="ma-form" onSubmit={handleVerifyCode}>
                <div className="ma-field">
                  <label className="ma-label" htmlFor="ma-code">{t('auth.codeLabel')}</label>
                  <input
                    id="ma-code"
                    className="ma-input ma-code-input"
                    type="text"
                    inputMode="numeric"
                    autoComplete="one-time-code"
                    maxLength={6}
                    placeholder="123456"
                    value={verifyCode}
                    onChange={(e) => setVerifyCode(e.target.value.replace(/\D/g, ''))}
                    aria-label={t('auth.codeLabel')}
                  />
                </div>

                <button
                  type="submit"
                  className="ma-btn ma-btn--primary"
                  disabled={verifyCode.trim().length !== 6 || verifyingCode}
                >
                  {verifyingCode
                    ? <span className="ma-spinner" aria-hidden="true" />
                    : t('auth.codeVerifyBtn')}
                </button>
              </form>

              {errors.form && <p className="ma-alert ma-alert--error" role="alert">{errors.form}</p>}
              {message && <p className="ma-alert ma-alert--success" role="status">{message}</p>}

              <p className="ma-note">
                <FaRegEnvelope size={12} aria-hidden="true" />
                {tr('auth.verifyAuto', 'This page will continue automatically once you verify.')}
              </p>

              <div className="ma-secondary">
                <button
                  type="button"
                  className="ma-textbtn"
                  disabled={resendCooldown > 0 || resendLoading}
                  onClick={handleResend}
                >
                  {resendLoading
                    ? tr('auth.resendSending', 'Sending…')
                    : resendCooldown > 0
                      ? `${tr('auth.resendCooldown', 'Resend email')} (${resendCooldown}s)`
                      : tr('auth.resendBtn', 'Resend verification email')}
                </button>
              </div>
            </>
          ) : isReset ? (
            <>
              <form className="ma-form" onSubmit={handleResetPassword}>
                <div className="ma-field">
                  <label className="ma-label" htmlFor="ma-reset-code">{t('auth.codeLabel')}</label>
                  <input
                    id="ma-reset-code"
                    className="ma-input ma-code-input"
                    type="text"
                    inputMode="numeric"
                    autoComplete="one-time-code"
                    maxLength={6}
                    placeholder="123456"
                    value={resetCode}
                    onChange={(e) => setResetCode(e.target.value.replace(/\D/g, ''))}
                    disabled={resettingPassword}
                  />
                </div>
                <div className="ma-field">
                  <label className="ma-label" htmlFor="ma-new-password">{t('auth.labelNewPassword')}</label>
                  <input
                    id="ma-new-password"
                    type="password"
                    className={`ma-input ${errors.password ? 'ma-input--error' : ''}`}
                    placeholder="••••••••"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    autoComplete="new-password"
                    disabled={resettingPassword}
                  />
                  {errors.password && <p className="ma-error">{errors.password}</p>}
                </div>

                <button
                  type="submit"
                  className="ma-btn ma-btn--primary"
                  disabled={resetCode.trim().length !== 6 || !newPassword || resettingPassword}
                >
                  {resettingPassword
                    ? <span className="ma-spinner" aria-hidden="true" />
                    : t('auth.btnReset')}
                </button>
              </form>

              {errors.form && <p className="ma-alert ma-alert--error" role="alert">{errors.form}</p>}
              {message && <p className="ma-alert ma-alert--success" role="status">{message}</p>}
            </>
          ) : (
            <>
              {formError && <p className="ma-alert ma-alert--error" role="alert">{formError}</p>}
              {message && <p className="ma-alert ma-alert--success" role="status">{message}</p>}

              <form onSubmit={handleSubmit} className="ma-form" noValidate>
                {isSignup && (
                  <div className="ma-field">
                    <label className="ma-label" htmlFor="ma-username">{t('auth.labelUsername')}</label>
                    <input
                      id="ma-username"
                      type="text"
                      className={`ma-input ${errors.username ? 'ma-input--error' : ''}`}
                      placeholder="e.g. john_doe"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      autoComplete="username"
                      autoCapitalize="none"
                      autoCorrect="off"
                      disabled={loading}
                    />
                    {errors.username && <p className="ma-error">{errors.username}</p>}
                  </div>
                )}

                <div className="ma-field">
                  <label className="ma-label" htmlFor="ma-email">{t('auth.labelEmail')}</label>
                  <input
                    id="ma-email"
                    type="email"
                    className={`ma-input ${errors.email ? 'ma-input--error' : ''}`}
                    placeholder={t('auth.emailPlaceholder')}
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    autoComplete="email"
                    autoCapitalize="none"
                    autoCorrect="off"
                    inputMode="email"
                    disabled={loading}
                  />
                  {errors.email && <p className="ma-error">{errors.email}</p>}
                </div>

                {!isForgot && (
                  <div className="ma-field">
                    <label className="ma-label" htmlFor="ma-password">{t('auth.labelPassword')}</label>
                    <div className="ma-input-wrap">
                      <input
                        id="ma-password"
                        type={showPassword ? 'text' : 'password'}
                        className={`ma-input ma-input--has-icon ${errors.password ? 'ma-input--error' : ''}`}
                        placeholder="••••••••"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        autoComplete={isLogin ? 'current-password' : 'new-password'}
                        disabled={loading}
                      />
                      <button
                        type="button"
                        className="ma-pw-toggle"
                        onClick={() => setShowPassword(v => !v)}
                        aria-label={showPassword ? t('auth.hidePassword') : t('auth.showPassword')}
                        tabIndex={-1}
                      >
                        {showPassword ? (
                          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/><line x1="1" y1="1" x2="23" y2="23"/>
                          </svg>
                        ) : (
                          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>
                          </svg>
                        )}
                      </button>
                    </div>
                    {errors.password && <p className="ma-error">{errors.password}</p>}
                    {isSignup && !errors.password && <p className="ma-hint">{t('auth.passwordHint')}</p>}

                    {isSignup && password && (
                      <div className="ma-strength">
                        <div className="ma-strength-bar">
                          {[1, 2, 3, 4, 5].map((i) => (
                            <div
                              key={i}
                              className="ma-strength-seg"
                              style={{ background: i <= strength.level ? strength.color : 'var(--border-primary)' }}
                            />
                          ))}
                        </div>
                        <span className="ma-strength-label" style={{ color: strength.color }}>
                          {strength.label}
                        </span>
                      </div>
                    )}
                  </div>
                )}

                {isLogin && (
                  <div className="ma-forgot-row">
                    <button
                      type="button"
                      className="ma-textbtn"
                      onClick={() => switchMode('forgot')}
                      disabled={loading}
                    >
                      {t('auth.forgotLink')}
                    </button>
                  </div>
                )}

                {!isLogin && !isForgot && (
                  <p className="ma-clickwrap">
                    {t('auth.clickwrapPre')}{' '}
                    <button type="button" className="ma-inline-link" onClick={() => setLegalModal('terms')}>
                      {t('legal.navTerms')}
                    </button>
                    {' '}{t('auth.clickwrapAnd')}{' '}
                    <button type="button" className="ma-inline-link" onClick={() => setLegalModal('privacy')}>
                      {t('legal.navPrivacy')}
                    </button>.
                  </p>
                )}

                <button type="submit" className="ma-btn ma-btn--primary" disabled={loading}>
                  {loading ? (
                    <>
                      <span className="ma-spinner" aria-hidden="true" />
                      {isForgot ? t('auth.loadingForgot') : isLogin ? t('auth.loadingLogin') : t('auth.loadingSignup')}
                    </>
                  ) : (
                    isForgot ? t('auth.btnForgot') : isLogin ? t('auth.btnLogin') : t('auth.btnSignup')
                  )}
                </button>
              </form>

              {!isForgot && (
                <div className="ma-secondary">
                  <span className="ma-secondary-label">
                    {isLogin ? t('auth.noAccount') : t('auth.hasAccount')}
                  </span>
                  <button
                    type="button"
                    className="ma-textbtn ma-textbtn--accent"
                    onClick={() => switchMode(isLogin ? 'signup' : 'login')}
                    disabled={loading}
                  >
                    {isLogin ? t('auth.signUpLink') : t('auth.signInLink')}
                  </button>
                </div>
              )}
            </>
          )}

          <div className="ma-legal">
            <button type="button" className="ma-legal-link" onClick={() => setLegalModal('about')}>{t('legal.navAbout')}</button>
            <span className="ma-legal-sep">·</span>
            <button type="button" className="ma-legal-link" onClick={() => setLegalModal('privacy')}>{t('legal.navPrivacy')}</button>
            <span className="ma-legal-sep">·</span>
            <button type="button" className="ma-legal-link" onClick={() => setLegalModal('terms')}>{t('legal.navTerms')}</button>
          </div>
        </div>
      </div>
    </div>
  )
}
