/**
 * LandingPage.jsx
 *
 * Apple-style scroll-driven landing page shown to unauthenticated users.
 * Each section fades + slides up as it enters the viewport (IntersectionObserver
 * via useScrollReveal). Sticky top nav keeps the "Sign in" CTA one click away.
 *
 * SCREENSHOTS expected at frontend/src/assets/landing/ (drop them here as PNGs):
 *   - brief.png      — Advisor cards / Brief tab
 *   - degree1.png    — Degree Planning overview (first of two side-by-side shots)
 *   - degree2.png    — Degree Requirements detail (second of two)
 *   - calendar.png   — Calendar grid with exam dots
 *   - clubs1.png     — Clubs directory (first of two side-by-side shots)
 *   - clubs2.png     — Club detail / drawer / manage (second of two)
 *
 * Missing screenshots gracefully render as a styled "Screenshot placeholder"
 * so the page never breaks if you haven't dropped them yet.
 */
import { useEffect } from 'react'
import logoMark from '../../assets/loading-logo.png'
import useScrollReveal from './useScrollReveal'
import './LandingPage.css'

// Vite's import.meta.glob — bundles whichever screenshots actually exist in
// frontend/src/assets/landing/ at build time, no errors if some are missing.
// Drop a file in that folder (named e.g. brief.png), restart dev/redeploy, and
// it picks up automatically.
const _shots = import.meta.glob('../../assets/landing/*.{png,jpg,jpeg,webp}', { eager: true, query: '?url', import: 'default' })
const _findShot = (basename) => {
  const match = Object.entries(_shots).find(([path]) => path.split('/').pop().startsWith(basename + '.'))
  return match ? match[1] : null
}
const brief    = _findShot('brief')
const degree1  = _findShot('degree1') || _findShot('degree')   // backwards compat
const degree2  = _findShot('degree2')
const calendar = _findShot('calendar')
const clubs1   = _findShot('clubs1') || _findShot('clubs')     // backwards compat
const clubs2   = _findShot('clubs2')

function Screenshot({ src, alt, caption }) {
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
  // ── Force LIGHT theme while the landing is mounted ────────────────────
  // The landing page is designed around a cream/light palette and the dark
  // variant looks broken (low contrast, wrong accents, dark scrollbars).
  // Override the user's theme preference on <html> for the duration of the
  // page, then restore it on unmount so the rest of the app still respects
  // whatever the user picked in Settings.
  useEffect(() => {
    const html = document.documentElement
    const previous = html.getAttribute('data-theme')
    html.setAttribute('data-theme', 'light')
    // Also mark the element so any [data-landing] CSS hooks can target it
    html.setAttribute('data-landing', 'true')
    return () => {
      if (previous) html.setAttribute('data-theme', previous)
      else html.removeAttribute('data-theme')
      html.removeAttribute('data-landing')
    }
  }, [])


  return (
    <div className="landing-root">

      {/* ── 1. Hero ──────────────────────────────────────────────── */}
      <section className="landing-section landing-hero" id="top">
        <div className="landing-hero__bg" aria-hidden />
        <div className="landing-section__inner landing-hero__inner">
          <Reveal as="h1" className="landing-hero__headline">
            The McGill student planner.<br />
            <span className="landing-hero__accent">All in one place.</span>
          </Reveal>
          <Reveal delay={120} as="p" className="landing-hero__sub">
            Your personal AI advisor, degree progress, course planner, calendar,
            club directory, and student forum, built by McGill students, for
            McGill students.
          </Reveal>
          <Reveal delay={240} className="landing-hero__cta-row">
            <button className="landing-btn landing-btn--primary" onClick={onSignIn}>
              Sign in with your McGill email
            </button>
            <a href="#brief" className="landing-btn landing-btn--ghost">
              See what's inside ↓
            </a>
          </Reveal>
          <Reveal delay={400} className="landing-hero__hint">
            Free, McGill-only, no tracking, your data stays yours.
          </Reveal>
        </div>
      </section>

      {/* ── 2. Brief ─────────────────────────────────────────────── */}
      <section className="landing-section landing-section--alt" id="brief">
        <div className="landing-section__inner landing-feature">
          <Reveal className="landing-feature__copy" style={{'--section-color': '#ed1b2f'}}>
            <span className="landing-eyebrow landing-eyebrow--chat">YOUR BRIEF</span>
            <h2 className="landing-feature__title">A personal AI academic advisor.</h2>
            <p className="landing-feature__text">
              Open the app and read a briefing built from your transcript,
              schedule, and goals. Eight cards every week: deadlines, gaps in
              your degree, recommended professors, opportunities you'd otherwise
              miss. Ask follow-up questions on any card in plain English.
            </p>
            <ul className="landing-feature__bullets">
              <li>Cards stream in card-by-card, no waiting screen</li>
              <li>Tap any card to chat with the advisor about it</li>
              <li>Pin the ones that matter, dismiss the rest</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual">
            <Screenshot src={brief} alt="Advisor brief: eight cards covering deadlines, degree progress, and opportunities" />
          </Reveal>
        </div>
      </section>

      {/* ── 3. Courses & degree ──────────────────────────────────── */}
      <section className="landing-section" id="degree">
        <div className="landing-section__inner landing-feature landing-feature--reverse">
          <Reveal className="landing-feature__copy" style={{'--section-color': '#059669'}}>
            <span className="landing-eyebrow landing-eyebrow--degree">DEGREE PROGRESS</span>
            <h2 className="landing-feature__title">Every requirement, every credit.</h2>
            <p className="landing-feature__text">
              Upload your unofficial transcript and your major's requirements
              fill in automatically. See exactly which courses count, which
              blocks are done, and which electives you still need. No more
              mental accounting.
            </p>
            <ul className="landing-feature__bullets">
              <li>Auto-detects which transcript courses fill each requirement</li>
              <li>AI elective recommendations based on your interests</li>
              <li>Built-in support for joint, honours, and B.A. & Sc. programs</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual landing-feature__visual--double">
            <Screenshot src={degree1} alt="Degree progress overview with credit totals and milestone bar" />
            <Screenshot src={degree2} alt="Degree requirements view showing each block of courses" />
          </Reveal>
        </div>
      </section>

      {/* ── 4. Calendar ──────────────────────────────────────────── */}
      <section className="landing-section landing-section--alt" id="calendar">
        <div className="landing-section__inner landing-feature">
          <Reveal className="landing-feature__copy" style={{'--section-color': '#059669'}}>
            <span className="landing-eyebrow landing-eyebrow--calendar">CALENDAR & REMINDERS</span>
            <h2 className="landing-feature__title">Never miss a deadline.</h2>
            <p className="landing-feature__text">
              Final exam dates auto-populate from McGill's schedule. Drop a
              syllabus PDF and assignments, midterms, and lecture times all
              land in your calendar. Pick what you want emails about and we
              send them on the right day.
            </p>
            <ul className="landing-feature__bullets">
              <li>Final exams auto-loaded for your registered courses</li>
              <li>Syllabus PDF → calendar in seconds</li>
              <li>Reminder emails 1 day and 7 days out, opt out anytime</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual">
            <Screenshot src={calendar} alt="Calendar grid with exam dates and assignment deadlines" />
          </Reveal>
        </div>
      </section>

      {/* ── 5. Clubs ─────────────────────────────────────────────── */}
      <section className="landing-section" id="clubs">
        <div className="landing-section__inner landing-feature landing-feature--reverse">
          <Reveal className="landing-feature__copy" style={{'--section-color': '#7c3aed'}}>
            <span className="landing-eyebrow landing-eyebrow--clubs">CLUBS</span>
            <h2 className="landing-feature__title">Discover McGill clubs without the hunt.</h2>
            <p className="landing-feature__text">
              Every verified McGill club in one searchable directory. Subscribe
              to follow updates and pull club events into your calendar. When
              you're ready to join, the apply link takes you straight to the
              club's own form.
            </p>
            <ul className="landing-feature__bullets">
              <li>Filter by category, faculty, or what you've already taken</li>
              <li>Subscribe for announcements + auto-add events to your calendar</li>
              <li>Run a club? Claim its page, post events, manage your exec team</li>
            </ul>
          </Reveal>
          <Reveal delay={120} className="landing-feature__visual landing-feature__visual--double">
            <Screenshot src={clubs1} alt="Clubs directory with category pills and club cards" />
            <Screenshot src={clubs2} alt="Club detail drawer with subscribe and join buttons" />
          </Reveal>
        </div>
      </section>

      {/* ── 6. Forum ─────────────────────────────────────────────── */}
      <section className="landing-section landing-section--alt" id="forum">
        <div className="landing-section__inner landing-forum">
          <Reveal>
            <span className="landing-eyebrow landing-eyebrow--forum">FORUM</span>
            <h2 className="landing-feature__title">Three places to talk to other McGill students.</h2>
            <p className="landing-feature__text landing-forum__lead">
              A focused, McGill-only forum split into three sections so
              conversations stay on topic.
            </p>
          </Reveal>
          <div className="landing-forum__grid">
            <Reveal className="landing-forum__card" delay={80}>
              <span className="landing-forum__pill">Courses</span>
              <h3>Talk about your classes.</h3>
              <p>Compare profs, swap notes on what to expect, ask "is this course actually as hard as people say?".</p>
            </Reveal>
            <Reveal className="landing-forum__card" delay={160}>
              <span className="landing-forum__pill">The site</span>
              <h3>Feedback on Symbolos.</h3>
              <p>Spot a bug? Want a feature? Post it here. Built features get prioritized by what students actually ask for.</p>
            </Reveal>
            <Reveal className="landing-forum__card" delay={240}>
              <span className="landing-forum__pill">General</span>
              <h3>Everything else.</h3>
              <p>Apartment hunts, study spots, the latest on union elections. Anything McGill students would want to discuss.</p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ── 7. Privacy strip ─────────────────────────────────────── */}
      <section className="landing-section landing-privacy" id="privacy">
        <div className="landing-section__inner">
          <Reveal as="h2" className="landing-privacy__title">
            McGill-only. Your data stays yours.
          </Reveal>
          <div className="landing-privacy__grid">
            <Reveal className="landing-privacy__card">
              <h3>McGill emails only</h3>
              <p>Accounts gated to @mail.mcgill.ca and @mcgill.ca. No outside spam, no anonymous posters.</p>
            </Reveal>
            <Reveal delay={80} className="landing-privacy__card">
              <h3>Hosted in Canada / US</h3>
              <p>Database on Supabase, files on Vercel, both compliant with Canadian privacy law.</p>
            </Reveal>
            <Reveal delay={160} className="landing-privacy__card">
              <h3>Delete anytime</h3>
              <p>One button in Settings wipes your account and all data. No retention, no recovery period.</p>
            </Reveal>
            <Reveal delay={240} className="landing-privacy__card">
              <h3>Free, forever</h3>
              <p>No paywall, no tracking pixels, no ad network. Built by a McGill student because nothing like this existed.</p>
            </Reveal>
          </div>
        </div>
      </section>

      {/* ── 8. Big CTA ───────────────────────────────────────────── */}
      <section className="landing-section landing-cta" id="cta">
        <div className="landing-section__inner landing-cta__inner">
          <Reveal as="h2" className="landing-cta__title">
            Built by McGill students.<br />Free for every McGill student.
          </Reveal>
          <Reveal delay={120} as="p" className="landing-cta__sub">
            Sign in with your McGill email and the brief is ready in seconds.
          </Reveal>
          <Reveal delay={240}>
            <button className="landing-btn landing-btn--primary landing-btn--xl" onClick={onSignIn}>
              Sign in with your McGill email
            </button>
          </Reveal>
        </div>
      </section>

      {/* ── 9. Footer ────────────────────────────────────────────── */}
      <footer className="landing-footer">
        <div className="landing-section__inner landing-footer__inner">
          <div className="landing-footer__brand">
            <img src={logoMark} alt="Symbolos" className="landing-footer__logo" />
            <span>Symbolos · McGill student planner</span>
          </div>
          <div className="landing-footer__links">
            <a href="#brief">Brief</a>
            <a href="#degree">Degree</a>
            <a href="#calendar">Calendar</a>
            <a href="#clubs">Clubs</a>
            <a href="#forum">Forum</a>
            <a href="#privacy">Privacy</a>
            <button className="landing-footer__signin" onClick={onSignIn}>Sign in</button>
          </div>
        </div>
        <p className="landing-footer__copy">
          © {new Date().getFullYear()} Symbolos · Not affiliated with McGill University ·
          Built independently by a McGill student.
        </p>
      </footer>
    </div>
  )
}
