import './Legal.css'

export default function AboutUs({ onClose }) {
  return (
    <div className="legal-overlay" onClick={onClose}>
      <div className="legal-modal" onClick={e => e.stopPropagation()}>
        <div className="legal-header">
          <div className="legal-logo">SY</div>
          <div>
            <h1 className="legal-title">About Symbolos</h1>
            <p className="legal-subtitle">Independent student academic advisor</p>
          </div>
          {onClose && (
            <button className="legal-close" onClick={onClose} aria-label="Close">✕</button>
          )}
        </div>

        <div className="legal-body">
          <div className="legal-disclaimer-banner">
            <strong>Not affiliated with McGill University.</strong> Symbolos is an independent student-built tool and is not endorsed by or connected to McGill University.
          </div>

          <section className="legal-section about-mission">
            <div className="about-logo-large">
              <svg width="48" height="48" viewBox="0 0 28 28" fill="none">
                <circle cx="14" cy="14" r="5" fill="#ED1B2F" opacity="0.95"/>
                <circle cx="14" cy="14" r="11" stroke="#ED1B2F" strokeWidth="1.5" opacity="0.35"/>
                <circle cx="14" cy="14" r="7" stroke="#ED1B2F" strokeWidth="1" opacity="0.6"/>
              </svg>
            </div>
            <h2>Our Mission</h2>
            <p>Navigating a McGill degree can be complex — hundreds of courses, shifting requirements, waitlists, prerequisites, grade curves, and advising queues that stretch for weeks. Symbolos exists to make that process clearer, faster, and less stressful.</p>
            <p>We built Symbolos because we've lived the frustration ourselves. We wanted a tool that actually understands your degree, remembers your history, and gives you specific, actionable advice — not generic links to the eCalendar.</p>
          </section>

          <section className="legal-section">
            <h2>What Symbolos Does</h2>
            <div className="about-features-grid">
              <div className="about-feature">
                <span className="about-feature-icon">🎓</span>
                <div>
                  <strong>Degree Planning</strong>
                  <p>Track your progress toward graduation, visualize completed requirements, and identify gaps — with support for dozens of McGill programs.</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon">🤖</span>
                <div>
                  <strong>AI Academic Advisor</strong>
                  <p>Powered by Anthropic's Claude, our advisor knows your courses, grades, interests, and degree requirements to give personalized, context-aware guidance.</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon">📊</span>
                <div>
                  <strong>Historical Grade Data</strong>
                  <p>Browse crowdsourced class average data across thousands of McGill course sections, so you can make informed decisions about your workload.</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon">📅</span>
                <div>
                  <strong>Smart Calendar</strong>
                  <p>Auto-detect final exam dates, import syllabus deadlines, and set email or SMS reminders so nothing slips through the cracks.</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon">🏛️</span>
                <div>
                  <strong>Clubs & Community</strong>
                  <p>Discover student clubs, subscribe to events, and connect with fellow students in the community forum.</p>
                </div>
              </div>
              <div className="about-feature">
                <span className="about-feature-icon">🌍</span>
                <div>
                  <strong>Multilingual</strong>
                  <p>Full support for English, French, and Mandarin — because McGill is a global university.</p>
                </div>
              </div>
            </div>
          </section>

          <section className="legal-section">
            <h2>Built by Students</h2>
            <p>Symbolos was created by McGill students who wanted better tools for navigating their academic journey. It is a passion project, not a commercial product.</p>
            <p>The grade data powering our course explorer is crowdsourced from the McGill community — thank you to every student who has contributed.</p>
          </section>

          <section className="legal-section">
            <h2>Technology</h2>
            <p>Symbolos is built with React and FastAPI, backed by Supabase (PostgreSQL), and powered by Anthropic's Claude API for AI features. It is deployed on Vercel.</p>
          </section>

          <section className="legal-section">
            <h2>Important Disclaimer</h2>
            <div className="legal-warning-box">
              Symbolos is <strong>not an official McGill tool</strong>. Always verify academic requirements, course information, and deadlines through official McGill channels: the eCalendar, Minerva, and your departmental advisor. AI-generated advice may contain errors.
            </div>
          </section>

          <section className="legal-section">
            <h2>Contact Us</h2>
            <p>Feedback, bug reports, or questions? We'd love to hear from you.</p>
            <p>📧 <a href="mailto:hello@symbolos.ca">hello@symbolos.ca</a></p>
            <p>You can also use the <strong>Feedback</strong> button in the app at any time.</p>
          </section>
        </div>
      </div>
    </div>
  )
}