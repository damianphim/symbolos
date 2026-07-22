/**
 * LandingPage.jsx
 *
 * Apple-style scroll-driven landing page shown to unauthenticated users.
 * Each section fades + slides up as it enters the viewport (IntersectionObserver
 * via useScrollReveal). Sticky top nav keeps the "Sign in" CTA one click away.
 *
 * SCREENSHOTS expected at frontend/src/assets/landing/, one per
 * section × language × theme: `{prefix}-{langToken}-{light|dark}.{ext}`
 *   - brief-{english|french|mand}-{light|dark}  — Advisor cards / Brief tab
 *   - deg-{eng|fr|mand}-{light|dark}            — Degree Planning
 *   - cal-{eng|fr|mand}-{light|dark}            — Calendar grid with exam dots
 *   - club-{eng|fr|mand}-{light|dark}           — Clubs directory / detail
 *
 * <ThemedScreenshot prefix="brief" .../> picks the file matching the visitor's
 * current language + resolved theme (light/dark, "auto" included) live, and
 * re-picks on the fly if they switch either. Falls back to a legacy static
 * `{prefix}.png` (no lang/theme suffix) for backwards compat, then to a
 * styled "Screenshot placeholder" so the page never breaks if a variant
 * is missing.
 */
import { useEffect, useState, useMemo } from 'react'
import { HiChevronDown } from 'react-icons/hi'
import { FaSun, FaMoon, FaPalette } from 'react-icons/fa'
import logoMark from '../../assets/loading-logo.png'
import mcgillSkyline from '../../assets/landing/mcgill-skyline.jpg'
import PrivacyPolicy from '../Legal/PrivacyPolicy'
import TermsOfService from '../Legal/TOS'
import AboutUs from '../Legal/AboutUs'
import { useLanguage, useTheme } from '../../contexts/PreferencesContext'
import useScrollReveal from './useScrollReveal'
import './LandingPage.css'

// Vite's import.meta.glob — bundles whichever screenshots actually exist in
// frontend/src/assets/landing/ at build time, no errors if some are missing.
// Drop files in that folder and restart dev/redeploy to pick them up.
const _shots = import.meta.glob('../../assets/landing/*.{png,jpg,jpeg,webp}', { eager: true, query: '?url', import: 'default' })
const _findShot = (basename) => {
  const match = Object.entries(_shots).find(([path]) => path.split('/').pop().startsWith(basename + '.'))
  return match ? match[1] : null
}

// Screenshot filenames use inconsistent language tokens across sections
// (brief: "english"/"french"; calendar/club/deg: "eng"/"fr") — try every
// known token for the language rather than hardcoding one per prefix.
const _LANG_TOKENS = { en: ['english', 'eng'], fr: ['french', 'fr'], zh: ['mand', 'zh', 'chinese'] }

function _resolveShot(prefix, language, resolvedTheme) {
  for (const token of _LANG_TOKENS[language] || _LANG_TOKENS.en) {
    const match = _findShot(`${prefix}-${token}-${resolvedTheme}`)
    if (match) return match
  }
  return _findShot(prefix) // legacy static fallback (no lang/theme suffix)
}

function ThemedScreenshot({ prefix, alt, caption }) {
  const { language } = useLanguage()
  const { resolvedTheme } = useTheme()
  const src = useMemo(() => _resolveShot(prefix, language, resolvedTheme), [prefix, language, resolvedTheme])

  if (!src) {
    return (
      <div className="landing-shot landing-shot--placeholder" aria-label={alt}>
        <div className="landing-shot__placeholder-inner">
          <div className="landing-shot__placeholder-dot" />
          <div className="landing-shot__placeholder-dot" />
          <div className="landing-shot__placeholder-dot" />
        </div>
        <p className="landing-shot__placeholder-text">{alt}</p>
      </div>
    )
  }
  return (
    <div className="landing-shot">
      <img src={src} alt={alt} loading="lazy" />
      {caption && <p className="landing-shot__caption">{caption}</p>}
    </div>
  )
}

function Reveal({ children, delay = 0, as: Tag = 'div', className = '', ...rest }) {
  const ref = useScrollReveal()
  return (
    <Tag
      ref={ref}
      className={`reveal ${className}`}
      style={delay ? { '--reveal-delay': `${delay}ms` } : undefined}
      {...rest}
    >
      {children}
    </Tag>
  )
}

export default function LandingPage({ onSignIn }) {
  const { t, language, setLanguage } = useLanguage()
  const { theme, setTheme } = useTheme()
  const [legalModal, setLegalModal] = useState(null) // 'privacy' | 'terms' | 'about'
  const cycleTheme = () => setTheme(theme === 'light' ? 'dark' : theme === 'dark' ? 'auto' : 'light')

  // Mark the element so [data-landing] CSS hooks (full-bleed scroll layout,
  // dark-mode overrides) can target it. The landing page follows whatever
  // theme the visitor has picked (or their system preference), same as the
  // rest of the app — it no longer forces light mode.
  useEffect(() => {
    const html = document.documentElement
    html.setAttribute('data-landing', 'true')
    return () => html.removeAttribute('data-landing')
  }, [])


  return (
    <div className="landing-root">
      <div className="landing-controls">
        <button
          className="landing-theme-btn"
          onClick={cycleTheme}
          title={t('sidebar.colorTheme')}
        >
          {theme === 'dark' ? <FaMoon /> : theme === 'auto' ? <FaPalette /> : <FaSun />}
        </button>
        <button
          className="landing-lang-btn"
          onClick={() => setLanguage(language === 'en' ? 'fr' : language === 'fr' ? 'zh' : 'en')}
          title={t('auth.langToggle')}
        >
          {language === 'en' ? 'FR' : language === 'fr' ? '中' : 'EN'}
        </button>
      </div>

      {/* ── 1. Hero ──────────────────────────────────────────────── */}
      <section className="landing-section landing-hero" id="top">
        <div className="landing-section__inner landing-hero__inner">
          <Reveal as="h1" className="landing-hero__headline">
            {t('landing.heroHeadline1')}<br />
            <span className="landing-hero__accent">{t('landing.heroHeadline2')}</span>
          </Reveal>
          <Reveal delay={120} as="p" className="landing-hero__sub">
            {t('landing.heroSub')}
          </Reveal>
          <Reveal delay={240} className="landing-hero__cta-row">
            <button className="landing-btn landing-btn--primary" onClick={onSignIn}>
              {t('landing.ctaSignIn')}
            </button>
          </Reveal>
          <Reveal delay={400} className="landing-hero__hint">
            {t('landing.heroHint')}
          </Reveal>
        </div>
        <button
          type="button"
          className="landing-hero__scroll-btn"
          onClick={() => document.getElementById('brief')?.scrollIntoView({ behavior: 'smooth' })}
          aria-label={t('landing.scrollDown')}
        >
          <HiChevronDown />
        </button>
      </section>

      {/* ── 2. Brief ─────────────────────────────────────────────── */}
      <section className="landing-section landing-section--alt" id="brief">
        <div className="landing-section__inner landing-feature">
          <Reveal className="landing-feature__copy">
            <span className="landing-eyebrow landing-eyebrow--chat">{t('landing.briefEyebrow')}</span>
            <p className="landing-feature__text">{t('landing.briefText')}</p>
            <ul className="landing-feature__bullets">
              <li>{t('landing.briefB1')}</li>
              <li>{t('landing.briefB2')}</li>
              <li>{t('landing.briefB3')}</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual">
            <ThemedScreenshot prefix="brief" alt={t('landing.briefAlt')} />
          </Reveal>
        </div>
      </section>

      {/* ── 3. Courses & degree ──────────────────────────────────── */}
      <section className="landing-section" id="degree">
        <div className="landing-section__inner landing-feature landing-feature--reverse">
          <Reveal className="landing-feature__copy">
            <span className="landing-eyebrow landing-eyebrow--degree">{t('landing.degreeEyebrow')}</span>
            <p className="landing-feature__text">{t('landing.degreeText')}</p>
            <ul className="landing-feature__bullets">
              <li>{t('landing.degreeB1')}</li>
              <li>{t('landing.degreeB2')}</li>
              <li>{t('landing.degreeB3')}</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual">
            <ThemedScreenshot prefix="deg" alt={t('landing.degreeAlt1')} />
          </Reveal>
        </div>
      </section>

      {/* ── 4. Calendar ──────────────────────────────────────────── */}
      <section className="landing-section landing-section--alt" id="calendar">
        <div className="landing-section__inner landing-feature">
          <Reveal className="landing-feature__copy">
            <span className="landing-eyebrow landing-eyebrow--calendar">{t('landing.calEyebrow')}</span>
            <p className="landing-feature__text">{t('landing.calText')}</p>
            <ul className="landing-feature__bullets">
              <li>{t('landing.calB1')}</li>
              <li>{t('landing.calB2')}</li>
              <li>{t('landing.calB3')}</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual">
            <ThemedScreenshot prefix="cal" alt={t('landing.calAlt')} />
          </Reveal>
        </div>
      </section>

      {/* ── 5. Clubs ─────────────────────────────────────────────── */}
      <section className="landing-section" id="clubs">
        <div className="landing-section__inner landing-feature landing-feature--reverse">
          <Reveal className="landing-feature__copy">
            <span className="landing-eyebrow landing-eyebrow--clubs">{t('landing.clubsEyebrow')}</span>
            <p className="landing-feature__text">{t('landing.clubsText')}</p>
            <ul className="landing-feature__bullets">
              <li>{t('landing.clubsB1')}</li>
              <li>{t('landing.clubsB2')}</li>
              <li>{t('landing.clubsB3')}</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual">
            <ThemedScreenshot prefix="club" alt={t('landing.clubsAlt1')} />
          </Reveal>
        </div>
      </section>

      {/* ── 6. Forum ─────────────────────────────────────────────── */}
      <section className="landing-section landing-section--alt" id="forum">
        <div className="landing-section__inner landing-forum">
          <Reveal>
            <span className="landing-eyebrow landing-eyebrow--forum">{t('landing.forumEyebrow')}</span>
          </Reveal>
          <div className="landing-forum__grid">
            <Reveal className="landing-forum__card" delay={80}>
              <span className="landing-forum__pill">{t('landing.forumPill1')}</span>
              <h3>{t('landing.forumH1')}</h3>
              <p>{t('landing.forumP1')}</p>
            </Reveal>
            <Reveal className="landing-forum__card" delay={160}>
              <span className="landing-forum__pill">{t('landing.forumPill2')}</span>
              <h3>{t('landing.forumH2')}</h3>
              <p>{t('landing.forumP2')}</p>
            </Reveal>
            <Reveal className="landing-forum__card" delay={240}>
              <span className="landing-forum__pill">{t('landing.forumPill3')}</span>
              <h3>{t('landing.forumH3')}</h3>
              <p>{t('landing.forumP3')}</p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ── 7. Privacy strip ─────────────────────────────────────── */}
      <section className="landing-section landing-privacy" id="privacy">
        <div className="landing-section__inner">
          <Reveal as="h2" className="landing-privacy__title">
            {t('landing.privacyTitle')}
          </Reveal>
          <div className="landing-privacy__grid">
            <Reveal className="landing-privacy__card">
              <h3>{t('landing.privacyH1')}</h3>
              <p>{t('landing.privacyP1')}</p>
            </Reveal>
            <Reveal delay={80} className="landing-privacy__card">
              <h3>{t('landing.privacyH2')}</h3>
              <p>{t('landing.privacyP2')}</p>
            </Reveal>
            <Reveal delay={160} className="landing-privacy__card">
              <h3>{t('landing.privacyH3')}</h3>
              <p>{t('landing.privacyP3')}</p>
            </Reveal>
            <Reveal delay={240} className="landing-privacy__card">
              <h3>{t('landing.privacyH4')}</h3>
              <p>{t('landing.privacyP4')}</p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ── 8. Big CTA ───────────────────────────────────────────── */}
      <section
        className="landing-section landing-cta"
        id="cta"
        style={{ backgroundImage: `url(${mcgillSkyline})` }}
      >
        <div className="landing-section__inner landing-cta__inner">
          <Reveal as="h2" className="landing-cta__title">
            {t('landing.ctaTitle1')}<br />{t('landing.ctaTitle2')}
          </Reveal>
          <Reveal delay={120} as="p" className="landing-cta__sub">
            {t('landing.ctaSub')}
          </Reveal>
          <Reveal delay={240}>
            <button className="landing-btn landing-btn--primary landing-btn--xl" onClick={onSignIn}>
              {t('landing.ctaSignIn')}
            </button>
          </Reveal>
        </div>
      </section>

      {/* ── 9. Footer ────────────────────────────────────────────── */}
      <footer className="landing-footer">
        <div className="landing-section__inner landing-footer__inner">
          <div className="landing-footer__brand">
            <img src={logoMark} alt="Symbolos" className="landing-footer__logo" />
            <span>{t('landing.footerBrand')}</span>
          </div>
          <div className="landing-footer__links">
            <button type="button" className="landing-footer__legal-btn" onClick={() => setLegalModal('privacy')}>{t('legal.navPrivacy')}</button>
            <button type="button" className="landing-footer__legal-btn" onClick={() => setLegalModal('terms')}>{t('legal.navTerms')}</button>
            <button type="button" className="landing-footer__legal-btn" onClick={() => setLegalModal('about')}>{t('legal.navAbout')}</button>
          </div>
        </div>
        <p className="landing-footer__copy">
          © {new Date().getFullYear()} Symbolos · {t('landing.footerCopy')}
        </p>
      </footer>

      {legalModal === 'privacy' && <PrivacyPolicy onClose={() => setLegalModal(null)} />}
      {legalModal === 'terms'   && <TermsOfService onClose={() => setLegalModal(null)} />}
      {legalModal === 'about'   && <AboutUs onClose={() => setLegalModal(null)} />}
    </div>
  )
}
