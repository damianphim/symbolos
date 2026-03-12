import { useState, useEffect } from 'react'
import {
  FaGraduationCap,
  FaLightbulb,
  FaListAlt,
  FaBook,
  FaCalendarAlt,
  FaUserCog,
  FaRocket,
  FaCommentDots,
} from 'react-icons/fa'

const STEPS = [
  {
    id: 'welcome',
    Icon: FaGraduationCap,
    iconColor: '#ed1b2f',
    title: 'Welcome to Symbolos',
    subtitle: 'Your McGill AI Academic Advisor',
    description:
      'Symbolos helps you navigate every part of your McGill journey — from choosing courses to tracking your degree, all in one place.',
    highlight: null,
    tip: null,
  },
  {
    id: 'chat',
    Icon: FaLightbulb,
    iconColor: '#f59e0b',
    title: 'Academic Brief',
    subtitle: 'Academic Brief tab',
    description:
      'Your personalized daily briefing. Get AI-generated cards with course recommendations, degree insights, and academic tips tailored to your profile.',
    highlight: 'chat',
    tip: 'Ask anything: "What courses should I take for a COMP major in U1?"',
  },
  {
    id: 'degree',
    Icon: FaListAlt,
    iconColor: '#10b981',
    title: 'Degree Planning',
    subtitle: 'Degree Planning tab',
    description:
      "Visualize your entire degree at a glance. See which requirements you've completed, what's in progress, and what's left — including transfer credits.",
    highlight: 'favorites',
    tip: 'Completed courses automatically update your degree progress.',
  },
  {
    id: 'courses',
    Icon: FaBook,
    iconColor: '#6366f1',
    title: 'Explore Courses',
    subtitle: 'Courses tab',
    description:
      "Search all McGill courses by code or keyword. See descriptions, credit values, and save courses you're interested in for future semesters.",
    highlight: 'courses',
    tip: 'Search "COMP 202" or just type "algorithms" to find relevant courses.',
  },
  {
    id: 'calendar',
    Icon: FaCalendarAlt,
    iconColor: '#3b82f6',
    title: 'Manage Your Calendar',
    subtitle: 'Calendar tab',
    description:
      "Stay on top of your semester. Final exam schedules are automatically loaded from McGill's official data. Add personal events and set email reminders.",
    highlight: 'calendar',
    tip: 'Your final exam schedule is always pre-populated each term.',
  },
  {
    id: 'profile',
    Icon: FaUserCog,
    iconColor: '#ec4899',
    title: 'Personalize Your Experience',
    subtitle: 'Profile & Settings',
    description:
      'Set your faculty, program, and year so Symbolos can give you the most relevant advice. Switch between light/dark mode and English/French at any time.',
    highlight: 'profile',
    tip: 'The more you fill out your profile, the smarter your advisor gets.',
  },
  {
    id: 'ready',
    Icon: FaRocket,
    iconColor: '#ed1b2f',
    title: "You're All Set!",
    subtitle: "Let's get started",
    description:
      'Your McGill academic journey starts now. Head to Academic Brief to see your personalized cards, or explore Courses to start planning your semester.',
    highlight: null,
    tip: null,
  },
]

const NAV_LABELS = {
  chat: 'Academic Brief',
  favorites: 'Degree Planning',
  courses: 'Courses',
  calendar: 'Calendar',
  profile: 'Profile',
}

export default function OnboardingTutorial({ onComplete }) {
  const [step, setStep] = useState(0)
  const [animating, setAnimating] = useState(false)
  const [direction, setDirection] = useState('forward')
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 80)
    return () => clearTimeout(t)
  }, [])

  const current = STEPS[step]
  const isFirst = step === 0
  const isLast = step === STEPS.length - 1
  const progressPct = ((step + 1) / STEPS.length) * 100

  const go = (dir) => {
    if (animating) return
    setDirection(dir)
    setAnimating(true)
    setTimeout(() => {
      setStep(s => dir === 'forward' ? s + 1 : s - 1)
      setAnimating(false)
    }, 220)
  }

  const handleComplete = () => {
    setVisible(false)
    setTimeout(() => onComplete?.(), 400)
  }

  const { Icon, iconColor } = current

  return (
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:wght@300;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

        .ot-overlay {
          position: fixed;
          inset: 0;
          z-index: 9999;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
          background: rgba(10, 8, 20, 0.75);
          backdrop-filter: blur(6px);
          -webkit-backdrop-filter: blur(6px);
          transition: opacity 0.4s ease;
          opacity: 0;
        }
        .ot-overlay.ot-visible { opacity: 1; }

        .ot-card {
          position: relative;
          width: 100%;
          max-width: 500px;
          background: #0f0d1a;
          border: 1px solid rgba(237, 27, 47, 0.22);
          border-radius: 20px;
          overflow: hidden;
          box-shadow:
            0 0 0 1px rgba(255,255,255,0.04),
            0 40px 80px rgba(0,0,0,0.65),
            0 0 60px rgba(237, 27, 47, 0.07);
          font-family: 'DM Sans', sans-serif;
        }

        .ot-card::before {
          content: '';
          position: absolute;
          top: 0; left: 0; right: 0;
          height: 3px;
          background: linear-gradient(90deg, transparent, #ed1b2f 40%, #ff7070 60%, transparent);
          z-index: 2;
        }

        .ot-card::after {
          content: '';
          position: absolute;
          inset: 0;
          background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.025) 1px, transparent 0);
          background-size: 28px 28px;
          pointer-events: none;
        }

        .ot-progress {
          position: absolute;
          top: 3px; left: 0;
          height: 2px;
          width: 100%;
          background: rgba(255,255,255,0.06);
          z-index: 3;
        }
        .ot-progress-fill {
          height: 100%;
          background: linear-gradient(90deg, #ed1b2f, #ff8a8a);
          transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
          border-radius: 0 2px 2px 0;
        }

        .ot-body {
          position: relative;
          z-index: 1;
          padding: 2.2rem 2.4rem 1.8rem;
        }

        .ot-step-row {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 1.6rem;
        }
        .ot-dots { display: flex; gap: 5px; }
        .ot-dot {
          width: 5px; height: 5px;
          border-radius: 50%;
          background: rgba(255,255,255,0.15);
          transition: all 0.3s ease;
        }
        .ot-dot.ot-dot-active {
          background: #ed1b2f;
          width: 18px;
          border-radius: 3px;
        }
        .ot-dot.ot-dot-done { background: rgba(237, 27, 47, 0.35); }
        .ot-step-label {
          font-size: 11px;
          font-weight: 500;
          color: rgba(255,255,255,0.25);
          letter-spacing: 0.08em;
          text-transform: uppercase;
          margin-left: auto;
        }

        .ot-content { transition: opacity 0.22s ease, transform 0.22s ease; }
        .ot-content.ot-slide-fwd { opacity: 0; transform: translateX(16px); }
        .ot-content.ot-slide-back { opacity: 0; transform: translateX(-16px); }

        .ot-icon-wrap {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 56px;
          height: 56px;
          border-radius: 14px;
          margin-bottom: 1.1rem;
        }

        .ot-title {
          font-family: 'Fraunces', serif;
          font-size: 1.65rem;
          font-weight: 600;
          color: #ffffff;
          line-height: 1.2;
          margin: 0 0 0.3rem;
          letter-spacing: -0.02em;
        }
        .ot-subtitle {
          font-size: 0.75rem;
          font-weight: 500;
          color: #ed1b2f;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          margin-bottom: 1rem;
          opacity: 0.9;
        }
        .ot-description {
          font-size: 0.95rem;
          font-weight: 300;
          color: rgba(255,255,255,0.65);
          line-height: 1.72;
          margin-bottom: 1.2rem;
        }

        .ot-nav-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.45rem;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 7px;
          padding: 0.45rem 0.8rem;
          margin-bottom: 1.2rem;
        }
        .ot-nav-dot {
          width: 6px; height: 6px;
          border-radius: 50%;
          background: #ed1b2f;
          box-shadow: 0 0 6px #ed1b2f;
          flex-shrink: 0;
        }
        .ot-nav-text { font-size: 0.78rem; color: rgba(255,255,255,0.4); }
        .ot-nav-name { font-size: 0.78rem; font-weight: 500; color: rgba(255,255,255,0.78); }

        .ot-tip {
          background: rgba(237, 27, 47, 0.07);
          border: 1px solid rgba(237, 27, 47, 0.18);
          border-left: 3px solid #ed1b2f;
          border-radius: 8px;
          padding: 0.7rem 1rem;
          margin-bottom: 1.3rem;
          display: flex;
          align-items: flex-start;
          gap: 0.55rem;
        }
        .ot-tip-icon { flex-shrink: 0; margin-top: 1px; color: #f59e0b; }
        .ot-tip-text {
          font-size: 0.83rem;
          color: rgba(255,255,255,0.55);
          font-style: italic;
          line-height: 1.5;
        }

        .ot-actions {
          display: flex;
          align-items: center;
          margin-top: 0.4rem;
        }
        .ot-btn-skip {
          background: none; border: none;
          color: rgba(255,255,255,0.25);
          font-family: 'DM Sans', sans-serif;
          font-size: 0.8rem;
          cursor: pointer;
          padding: 0.5rem 0;
          transition: color 0.2s;
        }
        .ot-btn-skip:hover { color: rgba(255,255,255,0.5); }

        .ot-btn-group { display: flex; gap: 0.55rem; margin-left: auto; }

        .ot-btn-back {
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.1);
          color: rgba(255,255,255,0.55);
          font-family: 'DM Sans', sans-serif;
          font-size: 0.86rem; font-weight: 500;
          padding: 0.58rem 1.1rem;
          border-radius: 9px; cursor: pointer;
          transition: all 0.18s ease;
        }
        .ot-btn-back:hover {
          background: rgba(255,255,255,0.09);
          color: rgba(255,255,255,0.8);
        }

        .ot-btn-next {
          background: #ed1b2f; border: none; color: #fff;
          font-family: 'DM Sans', sans-serif;
          font-size: 0.86rem; font-weight: 600;
          padding: 0.58rem 1.4rem;
          border-radius: 9px; cursor: pointer;
          transition: all 0.18s ease;
          display: flex; align-items: center; gap: 0.4rem;
          box-shadow: 0 4px 14px rgba(237, 27, 47, 0.32);
        }
        .ot-btn-next:hover {
          background: #d01929;
          box-shadow: 0 4px 20px rgba(237, 27, 47, 0.48);
          transform: translateY(-1px);
        }
        .ot-btn-next:active { transform: translateY(0); }

        .ot-btn-finish {
          background: linear-gradient(135deg, #ed1b2f, #c0142b);
          border: none; color: #fff;
          font-family: 'DM Sans', sans-serif;
          font-size: 0.9rem; font-weight: 600;
          padding: 0.65rem 1.8rem;
          border-radius: 9px; cursor: pointer;
          transition: all 0.18s ease;
          display: flex; align-items: center; gap: 0.5rem;
          box-shadow: 0 4px 20px rgba(237, 27, 47, 0.38);
        }
        .ot-btn-finish:hover {
          transform: translateY(-1px);
          box-shadow: 0 6px 28px rgba(237, 27, 47, 0.52);
        }
        .ot-feedback-callout {
          display: flex;
          align-items: flex-start;
          gap: 8px;
          margin-top: 14px;
          padding: 10px 13px;
          border-radius: 8px;
          background: var(--bg-tertiary, #f0f4ff);
          border: 1px solid var(--border-color, #dde3f0);
          font-size: 12.5px;
          color: var(--text-secondary, #555e7a);
          line-height: 1.5;
        }
        .ot-feedback-callout strong {
          color: var(--text-primary, #1a1f2e);
        }
        .ot-feedback-icon {
          flex-shrink: 0;
          margin-top: 2px;
          color: var(--accent, #6366f1);
        }
      `}</style>

      <div className={`ot-overlay${visible ? ' ot-visible' : ''}`}>
        <div className="ot-card">
          <div className="ot-progress">
            <div className="ot-progress-fill" style={{ width: `${progressPct}%` }} />
          </div>

          <div className="ot-body">
            <div className="ot-step-row">
              <div className="ot-dots">
                {STEPS.map((_, i) => (
                  <div
                    key={i}
                    className={`ot-dot${i === step ? ' ot-dot-active' : i < step ? ' ot-dot-done' : ''}`}
                  />
                ))}
              </div>
              <span className="ot-step-label">{step + 1} / {STEPS.length}</span>
            </div>

            <div
              className={`ot-content${
                animating
                  ? direction === 'forward' ? ' ot-slide-fwd' : ' ot-slide-back'
                  : ''
              }`}
            >
              {/* React Icon block */}
              <div
                className="ot-icon-wrap"
                style={{
                  background: `${iconColor}18`,
                  border: `1px solid ${iconColor}33`,
                  boxShadow: `0 4px 20px ${iconColor}22`,
                }}
              >
                <Icon size={26} color={iconColor} />
              </div>

              <h2 className="ot-title">{current.title}</h2>
              {current.subtitle && <div className="ot-subtitle">{current.subtitle}</div>}
              <p className="ot-description">{current.description}</p>

              {current.highlight && NAV_LABELS[current.highlight] && (
                <div className="ot-nav-badge">
                  <div className="ot-nav-dot" />
                  <span className="ot-nav-text">Find it in&nbsp;</span>
                  <span className="ot-nav-name">{NAV_LABELS[current.highlight]}</span>
                </div>
              )}

              {current.tip && (
                <div className="ot-tip">
                  <FaLightbulb size={13} className="ot-tip-icon" color="#f59e0b" />
                  <span className="ot-tip-text">{current.tip}</span>
                </div>
              )}
            </div>

            {isLast && (
              <div className="ot-feedback-callout">
                <FaCommentDots size={14} className="ot-feedback-icon" />
                <span>
                  Got feedback? Hit the <strong>Feedback</strong> button anytime — your suggestions help us keep improving.
                </span>
              </div>
            )}

            <div className="ot-actions">
              {!isLast ? (
                <button className="ot-btn-skip" onClick={handleComplete}>Skip tour</button>
              ) : <div />}
              <div className="ot-btn-group">
                {!isFirst && !isLast && (
                  <button className="ot-btn-back" onClick={() => go('back')}>← Back</button>
                )}
                {!isLast ? (
                  <button className="ot-btn-next" onClick={() => go('forward')}>
                    {isFirst ? 'Start Tour' : 'Next'} →
                  </button>
                ) : (
                  <button className="ot-btn-finish" onClick={handleComplete}>
                    <FaRocket size={14} />
                    Go to Dashboard
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}
