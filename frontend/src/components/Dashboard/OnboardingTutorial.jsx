import { useState, useEffect, useLayoutEffect, useCallback, useRef } from 'react'
import { FaRocket, FaLightbulb } from 'react-icons/fa'

const STEPS = [
  {
    id: 'welcome',
    target: null,
    tab: null,
    title: 'Welcome to Symbolos',
    description: "Your McGill AI Academic Advisor. Let's take a 30-second tour of everything you can do.",
    tip: null,
  },
  {
    id: 'chat',
    target: '[data-tour="chat"]',
    tab: 'chat',
    title: 'Academic Brief',
    description: 'Your personalized daily briefing. Get AI-generated cards with course recommendations, degree insights, and academic tips tailored to your profile.',
    tip: 'Ask anything — "What courses should I take for a COMP major in U1?"',
  },
  {
    id: 'favorites',
    target: '[data-tour="favorites"]',
    tab: 'favorites',
    title: 'Degree Planning',
    description: "Visualize your entire degree at a glance. See which requirements you've completed, what's in progress, and what's left — including transfer credits and electives.",
    tip: 'Completed courses automatically update your degree progress.',
  },
  {
    id: 'courses',
    target: '[data-tour="courses"]',
    tab: 'courses',
    title: 'Explore Courses',
    description: 'Search all McGill courses by code or keyword. See descriptions, credit values, and save courses for future semesters.',
    tip: 'Search "COMP 202" or just type "algorithms" to find relevant courses.',
  },
  {
    id: 'calendar',
    target: '[data-tour="calendar"]',
    tab: 'calendar',
    title: 'Calendar',
    description: "Stay on top of your semester. Final exam schedules are automatically loaded from McGill's official data. Add personal events and set email reminders.",
    tip: 'Your final exam schedule is always pre-populated each term.',
  },
  {
    id: 'clubs',
    target: '[data-tour="clubs"]',
    tab: 'clubs',
    title: 'Student Clubs',
    description: 'Explore hundreds of McGill student clubs. Join clubs, get notified about events, and connect with students who share your interests.',
    tip: 'Club events automatically appear in your calendar once you join.',
  },
  {
    id: 'forum',
    target: '[data-tour="forum"]',
    tab: 'forum',
    title: 'Community Forum',
    description: 'Ask questions, share advice, and connect with fellow McGill students. Browse posts by category and contribute to the community.',
    tip: 'Post anonymously or publicly — your choice.',
  },
  {
    id: 'profile',
    target: '[data-tour="profile"]',
    tab: 'profile',
    title: 'Your Profile',
    description: 'Set your faculty, program, and year so Symbolos can give you the most relevant advice. Switch between light/dark mode and languages at any time.',
    tip: 'The more you fill out your profile, the smarter your advisor gets.',
  },
  {
    id: 'done',
    target: null,
    tab: null,
    title: "You're All Set!",
    description: "Your McGill academic journey starts now. Head to Academic Brief to see your personalized cards, or jump to Degree Planning to check your progress.",
    tip: null,
  },
]

const PAD = 10
const TOOLTIP_W = 300

export default function OnboardingTutorial({ onComplete, onTabChange }) {
  const [step, setStep] = useState(0)
  const [rect, setRect] = useState(null)
  const [visible, setVisible] = useState(false)
  const [arrowOffset, setArrowOffset] = useState(50)
  const [tooltipTop, setTooltipTop] = useState(null)
  const tooltipRef = useRef(null)

  const current = STEPS[step]
  const isFirst = step === 0
  const isLast  = step === STEPS.length - 1

  const measure = useCallback(() => {
    if (!current.target) { setRect(null); return }
    const el = document.querySelector(current.target)
    if (!el) { setRect(null); return }
    const r = el.getBoundingClientRect()
    setRect({ top: r.top, left: r.left, width: r.width, height: r.height, right: r.right, bottom: r.bottom })
  }, [current.target])

  useLayoutEffect(() => {
    measure()
    const t = setTimeout(measure, 120)
    return () => clearTimeout(t)
  }, [measure, step])

  useEffect(() => {
    window.addEventListener('resize', measure)
    return () => window.removeEventListener('resize', measure)
  }, [measure])

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 60)
    return () => clearTimeout(t)
  }, [])

  // Compute tooltip position and arrow offset after layout (reads ref safely in effect)
  useEffect(() => {
    if (!tooltipRef.current) return
    const tipH = tooltipRef.current.offsetHeight || 240
    if (rect) {
      const targetCenterY = rect.top + rect.height / 2
      const top = Math.max(16, Math.min(targetCenterY - tipH / 2, window.innerHeight - tipH - 16))
      setTooltipTop(top)
      setArrowOffset(Math.max(10, Math.min(targetCenterY - top, tipH - 10)))
    } else {
      setTooltipTop(null)
    }
  }, [rect, step])

  const advance = (dir) => {
    const nextIdx = step + (dir === 'fwd' ? 1 : -1)
    const next = STEPS[nextIdx]
    if (next?.tab && onTabChange) onTabChange(next.tab)
    setStep(nextIdx)
  }

  const finish = () => {
    if (onTabChange) onTabChange('chat')
    setVisible(false)
    setTimeout(() => onComplete?.(), 350)
  }

  const hasTarget = !!rect

  return (
    <div
      style={{
        position: 'fixed', inset: 0, zIndex: 9999,
        pointerEvents: visible ? 'all' : 'none',
        opacity: visible ? 1 : 0,
        transition: 'opacity 0.35s ease',
      }}
    >
      {/* ── Spotlight overlay ── */}
      {hasTarget ? (
        <>
          <div style={{ position: 'fixed', top: 0, left: 0, right: 0, height: Math.max(0, rect.top - PAD), background: 'rgba(0,0,0,0.72)' }} />
          <div style={{ position: 'fixed', top: Math.max(0, rect.top - PAD), left: 0, width: Math.max(0, rect.left - PAD), height: rect.height + PAD * 2, background: 'rgba(0,0,0,0.72)' }} />
          <div style={{ position: 'fixed', top: Math.max(0, rect.top - PAD), left: rect.right + PAD, right: 0, height: rect.height + PAD * 2, background: 'rgba(0,0,0,0.72)' }} />
          <div style={{ position: 'fixed', top: rect.bottom + PAD, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.72)' }} />
          {/* Glow ring */}
          <div style={{
            position: 'fixed',
            top: rect.top - PAD, left: rect.left - PAD,
            width: rect.width + PAD * 2, height: rect.height + PAD * 2,
            borderRadius: 10,
            border: '2px solid #ed1b2f',
            boxShadow: '0 0 0 1px rgba(237,27,47,0.2), 0 0 24px rgba(237,27,47,0.35)',
            pointerEvents: 'none',
          }} />
        </>
      ) : (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.72)', backdropFilter: 'blur(4px)', WebkitBackdropFilter: 'blur(4px)' }} />
      )}

      {/* ── Tooltip card ── */}
      <div
        ref={tooltipRef}
        style={{
          position: 'fixed',
          ...(hasTarget && tooltipTop !== null
            ? { top: tooltipTop, left: rect.right + PAD + 18, width: TOOLTIP_W }
            : { top: '50%', left: '50%', transform: 'translate(-50%,-50%)', width: 420, maxWidth: 'calc(100vw - 32px)' }
          ),
          background: '#0f0d1a',
          border: '1px solid rgba(237,27,47,0.22)',
          borderRadius: 14,
          padding: '20px 22px',
          boxShadow: '0 12px 48px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.03)',
        }}
      >
        {/* Arrow (only for spotlight steps) */}
        {hasTarget && (
          <>
            <div style={{
              position: 'absolute', left: -8, top: arrowOffset,
              width: 0, height: 0,
              borderTop: '8px solid transparent', borderBottom: '8px solid transparent',
              borderRight: '8px solid rgba(237,27,47,0.22)',
              transform: 'translateY(-50%)',
            }} />
            <div style={{
              position: 'absolute', left: -6, top: arrowOffset,
              width: 0, height: 0,
              borderTop: '7px solid transparent', borderBottom: '7px solid transparent',
              borderRight: '7px solid #0f0d1a',
              transform: 'translateY(-50%)',
            }} />
          </>
        )}

        {/* Progress dots */}
        <div style={{ display: 'flex', gap: 4, marginBottom: 14, alignItems: 'center' }}>
          {STEPS.map((_, i) => (
            <div key={i} style={{
              height: 5, borderRadius: 3,
              width: i === step ? 14 : 5,
              background: i === step ? '#ed1b2f' : i < step ? 'rgba(237,27,47,0.4)' : 'rgba(255,255,255,0.12)',
              transition: 'all 0.3s ease',
            }} />
          ))}
          <span style={{ marginLeft: 'auto', fontSize: '0.7rem', color: 'rgba(255,255,255,0.2)', fontVariantNumeric: 'tabular-nums' }}>
            {step + 1}/{STEPS.length}
          </span>
        </div>

        <h3 style={{ color: '#fff', fontSize: '1.05rem', fontWeight: 700, margin: '0 0 8px', letterSpacing: '-0.01em', lineHeight: 1.25 }}>
          {current.title}
        </h3>
        <p style={{ color: 'rgba(255,255,255,0.6)', fontSize: '0.855rem', lineHeight: 1.65, margin: '0 0 10px' }}>
          {current.description}
        </p>

        {current.tip && (
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '8px 10px', borderRadius: 7, background: 'rgba(237,27,47,0.07)', border: '1px solid rgba(237,27,47,0.14)', marginBottom: 12 }}>
            <FaLightbulb size={11} style={{ color: '#f59e0b', flexShrink: 0, marginTop: 2 }} />
            <span style={{ color: 'rgba(255,255,255,0.45)', fontSize: '0.785rem', fontStyle: 'italic', lineHeight: 1.5 }}>{current.tip}</span>
          </div>
        )}

        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: current.tip ? 4 : 12 }}>
          {!isLast && (
            <button
              onClick={finish}
              style={{ background: 'none', border: 'none', color: 'rgba(255,255,255,0.25)', fontSize: '0.76rem', cursor: 'pointer', padding: '4px 0', fontFamily: 'inherit', lineHeight: 1 }}
            >
              Skip
            </button>
          )}
          <div style={{ display: 'flex', gap: 8, marginLeft: 'auto' }}>
            {!isFirst && !isLast && (
              <button
                onClick={() => advance('back')}
                style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', color: 'rgba(255,255,255,0.5)', fontSize: '0.8rem', fontWeight: 500, padding: '6px 14px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit' }}
              >
                ← Back
              </button>
            )}
            {!isLast ? (
              <button
                onClick={() => advance('fwd')}
                style={{ background: '#ed1b2f', border: 'none', color: '#fff', fontSize: '0.8rem', fontWeight: 600, padding: '6px 16px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit', boxShadow: '0 3px 10px rgba(237,27,47,0.35)' }}
              >
                {isFirst ? 'Start Tour →' : 'Next →'}
              </button>
            ) : (
              <button
                onClick={finish}
                style={{ background: '#ed1b2f', border: 'none', color: '#fff', fontSize: '0.82rem', fontWeight: 600, padding: '7px 16px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit', display: 'flex', alignItems: 'center', gap: 6, boxShadow: '0 3px 10px rgba(237,27,47,0.35)' }}
              >
                <FaRocket size={12} /> Go to Dashboard
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
