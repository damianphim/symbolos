import { useState, useEffect, useLayoutEffect, useCallback, useMemo, useRef } from 'react'
import { FaRocket, FaLightbulb } from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'

// Full tour: walks every tab in the sidebar, plus one deeper stop per tab
// highlighting its main sub-navigation. The 8 top-level stops reuse the
// data-tour="<key>" anchors already on every Sidebar nav button; the deeper
// stops target a data-tour attribute added to that tab's own markup.
const buildSteps = (t) => [
  {
    id: 'welcome',
    target: null,
    tab: null,
    title: t('tour.welcomeTitle'),
    description: t('tour.welcomeDesc'),
    tip: null,
  },
  {
    id: 'home',
    target: '[data-tour="home"]',
    tab: 'home',
    title: t('tour.homeTitle'),
    description: t('tour.homeDesc'),
    tip: t('tour.homeTip'),
  },
  {
    id: 'home-setup',
    target: '[data-tour="home-setup"]',
    tab: 'home',
    title: t('tour.homeSetupTitle'),
    description: t('tour.homeSetupDesc'),
    tip: null,
  },
  {
    id: 'chat',
    target: '[data-tour="chat"]',
    tab: 'chat',
    title: t('tour.briefTitle'),
    description: t('tour.briefDesc'),
    tip: t('tour.briefTip'),
  },
  {
    id: 'chat-categories',
    target: '[data-tour="chat-categories"]',
    tab: 'chat',
    title: t('tour.chatCategoriesTitle'),
    description: t('tour.chatCategoriesDesc'),
    tip: null,
  },
  {
    id: 'chat-freeform',
    target: '[data-tour="chat-freeform"]',
    tab: 'chat',
    title: t('tour.chatFreeformTitle'),
    description: t('tour.chatFreeformDesc'),
    tip: null,
  },
  {
    id: 'courses',
    target: '[data-tour="courses"]',
    tab: 'courses',
    title: t('tour.coursesTitle'),
    description: t('tour.coursesDesc'),
    tip: null,
  },
  {
    id: 'courses-mycourses',
    target: '[data-tour="courses-mycourses"]',
    tab: 'courses',
    title: t('tour.coursesMyCoursesTitle'),
    description: t('tour.coursesMyCoursesDesc'),
    tip: null,
  },
  {
    id: 'favorites',
    target: '[data-tour="favorites"]',
    tab: 'favorites',
    title: t('tour.degreeTitle'),
    description: t('tour.degreeDesc'),
    tip: t('tour.degreeTip'),
  },
  {
    id: 'degree-subtabs',
    target: '[data-tour="degree-subtabs"]',
    tab: 'favorites',
    title: t('tour.degreeSubtabsTitle'),
    description: t('tour.degreeSubtabsDesc'),
    tip: null,
  },
  {
    id: 'calendar',
    target: '[data-tour="calendar"]',
    tab: 'calendar',
    title: t('tour.calendarTitle'),
    description: t('tour.calendarDesc'),
    tip: null,
  },
  {
    id: 'calendar-add',
    target: '[data-tour="calendar-add"]',
    tab: 'calendar',
    title: t('tour.calendarAddTitle'),
    description: t('tour.calendarAddDesc'),
    tip: null,
  },
  {
    id: 'clubs',
    target: '[data-tour="clubs"]',
    tab: 'clubs',
    title: t('tour.clubsTitle'),
    description: t('tour.clubsDesc'),
    tip: null,
  },
  {
    id: 'clubs-tabs',
    target: '[data-tour="clubs-tabs"]',
    tab: 'clubs',
    title: t('tour.clubsTabsTitle'),
    description: t('tour.clubsTabsDesc'),
    tip: null,
  },
  {
    id: 'forum',
    target: '[data-tour="forum"]',
    tab: 'forum',
    title: t('tour.forumTitle'),
    description: t('tour.forumDesc'),
    tip: null,
  },
  {
    id: 'forum-sections',
    target: '[data-tour="forum-sections"]',
    tab: 'forum',
    title: t('tour.forumSectionsTitle'),
    description: t('tour.forumSectionsDesc'),
    tip: null,
  },
  {
    id: 'profile',
    target: '[data-tour="profile"]',
    tab: 'profile',
    title: t('tour.profileTitle'),
    description: t('tour.profileDesc'),
    tip: null,
  },
]

const PAD = 10
const TOOLTIP_W = 300

export default function OnboardingTutorial({ onComplete, onTabChange }) {
  const { t } = useLanguage()
  const [step, setStep] = useState(0)
  const [rect, setRect] = useState(null)
  const [visible, setVisible] = useState(false)
  const [arrowOffset, setArrowOffset] = useState(50)
  const [tooltipTop, setTooltipTop] = useState(null)
  const tooltipRef = useRef(null)

  const STEPS = useMemo(() => buildSteps(t), [t])
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

  // Several stops target elements inside lazily-loaded tabs (ClubsTab,
  // CalendarTab, Forum, ...) — a single 120ms re-check isn't always enough
  // to catch the chunk fetch + mount on a slow connection, so poll a few
  // times with backoff instead of just once.
  useLayoutEffect(() => {
    measure()
    const delays = [50, 150, 300, 600, 1000]
    const timers = delays.map(d => setTimeout(measure, d))
    return () => timers.forEach(clearTimeout)
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
    if (onTabChange) onTabChange('home')
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
          background: 'var(--tour-bg)',
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
              borderRight: '7px solid var(--tour-bg)',
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
              background: i === step ? '#ed1b2f' : i < step ? 'rgba(237,27,47,0.4)' : 'var(--tour-track)',
              transition: 'all 0.3s ease',
            }} />
          ))}
          <span style={{ marginLeft: 'auto', fontSize: '0.7rem', color: 'var(--tour-text-muted)', fontVariantNumeric: 'tabular-nums' }}>
            {step + 1}/{STEPS.length}
          </span>
        </div>

        <h3 style={{ color: 'var(--tour-text)', fontSize: '1.05rem', fontWeight: 700, margin: '0 0 8px', letterSpacing: '-0.01em', lineHeight: 1.25 }}>
          {current.title}
        </h3>
        <p style={{ color: 'var(--tour-text-muted)', fontSize: '0.855rem', lineHeight: 1.65, margin: '0 0 10px' }}>
          {current.description}
        </p>

        {current.tip && (
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start', padding: '8px 10px', borderRadius: 7, background: 'rgba(237,27,47,0.07)', border: '1px solid rgba(237,27,47,0.14)', marginBottom: 12 }}>
            <FaLightbulb size={11} style={{ color: '#f59e0b', flexShrink: 0, marginTop: 2 }} />
            <span style={{ color: 'var(--tour-text-muted)', fontSize: '0.785rem', fontStyle: 'italic', lineHeight: 1.5 }}>{current.tip}</span>
          </div>
        )}

        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: current.tip ? 4 : 12 }}>
          {!isLast && (
            <button
              onClick={finish}
              style={{ background: 'none', border: 'none', color: 'var(--tour-text-subtle)', fontSize: '0.76rem', cursor: 'pointer', padding: '4px 0', fontFamily: 'inherit', lineHeight: 1, textDecoration: 'underline', textUnderlineOffset: 2 }}
            >
              {t('tour.skip')}
            </button>
          )}
          <div style={{ display: 'flex', gap: 8, marginLeft: 'auto' }}>
            {!isFirst && (
              <button
                onClick={() => advance('back')}
                style={{ background: 'var(--tour-surface)', border: '1px solid var(--tour-border)', color: 'var(--tour-text-muted)', fontSize: '0.8rem', fontWeight: 500, padding: '6px 14px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit' }}
              >
                ← {t('tour.back')}
              </button>
            )}
            {!isLast ? (
              <button
                onClick={() => advance('fwd')}
                style={{ background: '#ed1b2f', border: 'none', color: '#fff', fontSize: '0.8rem', fontWeight: 600, padding: '6px 16px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit', boxShadow: '0 3px 10px rgba(237,27,47,0.35)' }}
              >
                {isFirst ? `${t('tour.start')} →` : `${t('tour.next')} →`}
              </button>
            ) : (
              <button
                onClick={finish}
                style={{ background: '#ed1b2f', border: 'none', color: '#fff', fontSize: '0.82rem', fontWeight: 600, padding: '7px 16px', borderRadius: 8, cursor: 'pointer', fontFamily: 'inherit', display: 'flex', alignItems: 'center', gap: 6, boxShadow: '0 3px 10px rgba(237,27,47,0.35)' }}
              >
                <FaRocket size={12} /> {t('tour.finish')}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
