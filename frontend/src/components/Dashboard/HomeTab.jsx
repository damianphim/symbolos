/**
 * HomeTab — Canvas-LMS-style landing dashboard.
 *
 * Glanceable overview that ties the app together: a setup checklist for
 * new users (the empty states double as onboarding), the top advisor
 * cards, current courses, an "Up Next" deadline feed, and compact degree
 * progress. All data arrives via props from Dashboard — upcoming events
 * are computed once in Dashboard (via useUpcomingEvents) since the
 * Sidebar's Calendar badge needs the same feed.
 */
import { useMemo, useState } from 'react'
import {
  FaFileUpload, FaGraduationCap, FaFilePdf, FaComments, FaCalendarPlus,
  FaCheckCircle, FaRegCircle, FaArrowRight, FaTimes, FaRegLightbulb,
  FaBook, FaCalendarAlt, FaChartLine, FaClipboardList, FaFileAlt, FaPenAlt,
  FaExclamationTriangle, FaExclamationCircle,
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import { isCourseInActiveTerm } from '../../lib/termDates'
import DegreeProgressTracker from './DegreeProgressTracker'
import EmptyState from '../ui/EmptyState'
import Skeleton from '../ui/Skeleton'
import SectionHeader from '../ui/SectionHeader'
import Badge from '../ui/Badge'
import './HomeTab.css'

// Per-course accent palette built on the existing per-tab accents so course
// chips stay theme-aware (Canvas-style course color coding).
const COURSE_ACCENTS = [
  'var(--tab-courses-accent)',
  'var(--tab-calendar-accent)',
  'var(--tab-clubs-accent)',
  'var(--tab-forum-accent)',
  'var(--accent-primary)',
]

function courseAccent(code = '') {
  let h = 0
  for (let i = 0; i < code.length; i++) h = (h * 31 + code.charCodeAt(i)) >>> 0
  return COURSE_ACCENTS[h % COURSE_ACCENTS.length]
}

// Invariant: no raw emojis in the UI — react-icons only.
const EVENT_ICONS = {
  exam: <FaPenAlt />, midterm: <FaPenAlt />, assignment: <FaFileAlt />,
  quiz: <FaClipboardList />, academic: <FaGraduationCap />, personal: <FaCalendarAlt />,
}

// Advisor cards arrive with a backend-generated emoji in `card.icon`;
// map the card type to a react-icon instead of rendering the emoji.
const CARD_TYPE_ICONS = {
  urgent: <FaExclamationCircle />,
  warning: <FaExclamationTriangle />,
  insight: <FaRegLightbulb />,
}

const LOCALE_MAP = { en: 'en-CA', fr: 'fr-CA', zh: 'zh-CN' }

function daysUntil(dateStr) {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  const target = new Date(dateStr + 'T00:00:00')
  return Math.round((target - today) / 86400000)
}

function currentTermKey() {
  const m = new Date().getMonth()
  if (m <= 3) return 'home.termWinter'
  if (m <= 7) return 'home.termSummer'
  return 'home.termFall'
}

export default function HomeTab({
  user, profile,
  advisorCards = [], cardsLoading = false,
  currentCourses = [], completedCourses = [],
  events = [], eventsLoading = false, hasCourseEvents = false,
  onTabChange, onViewCurrentCourses, onImportTranscript, onImportSyllabus,
}) {
  // Deep-link to My Courses → Current when available.
  const goToCurrentCourses = onViewCurrentCourses ?? (() => onTabChange('courses'))
  const { t, language } = useLanguage()

  // Term-aware current courses: only show registrations for the semester we
  // are actually in (Fall vs Winter vs Summer); the rest are "upcoming".
  const activeCourses = useMemo(
    () => currentCourses.filter(c => isCourseInActiveTerm(c)),
    [currentCourses],
  )
  const upcomingCount = currentCourses.length - activeCourses.length

  // ── Setup checklist ────────────────────────────────────
  const dismissKey = `symbolos_setup_dismissed_${user?.id}`
  const [setupDismissed, setSetupDismissed] = useState(() => {
    try { return localStorage.getItem(dismissKey) === '1' } catch { return false }
  })
  const dismissSetup = () => {
    setSetupDismissed(true)
    try { localStorage.setItem(dismissKey, '1') } catch { /* ignore */ }
  }

  const steps = useMemo(() => [
    {
      key: 'transcript',
      done: completedCourses.length > 0,
      icon: <FaFileUpload />,
      title: t('setup.transcriptTitle'),
      sub: t('setup.transcriptSub'),
      onClick: onImportTranscript,
    },
    {
      key: 'program',
      done: !!profile?.major,
      icon: <FaGraduationCap />,
      title: t('setup.programTitle'),
      sub: t('setup.programSub'),
      onClick: () => onTabChange('profile'),
    },
    {
      key: 'syllabus',
      done: hasCourseEvents,
      icon: <FaFilePdf />,
      title: t('setup.syllabusTitle'),
      sub: t('setup.syllabusSub'),
      onClick: onImportSyllabus,
    },
  ], [completedCourses.length, profile?.major, hasCourseEvents, t, onImportTranscript, onImportSyllabus, onTabChange])

  const doneCount = steps.filter(s => s.done).length
  const setupComplete = doneCount === steps.length
  const showSetup = !setupComplete && !setupDismissed

  // ── Helpers ────────────────────────────────────────────
  const countdown = (dateStr) => {
    const d = daysUntil(dateStr)
    if (d <= 0) return t('home.today')
    if (d === 1) return t('calendar.tomorrow')
    return t('calendar.inXDays').replace('{n}', d)
  }
  const formatDate = (dateStr) =>
    new Date(dateStr + 'T00:00:00').toLocaleDateString(LOCALE_MAP[language] || 'en-CA', { month: 'short', day: 'numeric' })

  const topCards = advisorCards.slice(0, 3)
  const greetName = profile?.username || profile?.full_name || ''

  return (
    <div className="home-tab">
      {/* ── Header ── */}
      <header className="home-header">
        <div>
          <h1 className="home-greeting">
            {greetName ? t('home.greeting').replace('{name}', greetName) : t('home.greetingNoName')}
          </h1>
          <p className="home-term">{t(currentTermKey()).replace('{year}', new Date().getFullYear())}</p>
        </div>
        {!setupComplete && (
          <Badge variant="accent">{t('home.setupProgress').replace('{done}', doneCount).replace('{total}', steps.length)}</Badge>
        )}
      </header>

      <div className="home-grid">
        {/* ── Main column ── */}
        <div className="home-main">
          {showSetup && (
            <section className="home-card home-setup">
              <SectionHeader
                title={t('setup.title')}
                action={
                  <button className="home-setup__dismiss" onClick={dismissSetup} aria-label={t('setup.dismiss')} title={t('setup.dismiss')}>
                    <FaTimes />
                  </button>
                }
              />
              <ul className="home-setup__list">
                {steps.map(step => (
                  <li key={step.key} className={`home-setup__step ${step.done ? 'is-done' : ''}`}>
                    <span className="home-setup__check">
                      {step.done ? <FaCheckCircle /> : <FaRegCircle />}
                    </span>
                    <div className="home-setup__text">
                      <span className="home-setup__step-title">{step.title}</span>
                      <span className="home-setup__step-sub">{step.sub}</span>
                    </div>
                    {!step.done && (
                      <button className="home-setup__cta" onClick={step.onClick}>
                        {step.icon} {t('setup.start')}
                      </button>
                    )}
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* From your Brief */}
          <section className="home-card">
            <SectionHeader
              icon={<FaRegLightbulb />}
              title={t('home.fromYourBrief')}
              action={
                <button className="home-link" onClick={() => onTabChange('chat')}>
                  {t('home.viewAll')} <FaArrowRight />
                </button>
              }
            />
            {cardsLoading && topCards.length === 0 ? (
              <div className="home-brief__list">
                {[0, 1].map(i => (
                  <div key={i} className="home-brief__item">
                    <Skeleton circle height="2rem" />
                    <div className="home-brief__item-text">
                      <Skeleton width="55%" />
                      <Skeleton width="90%" />
                    </div>
                  </div>
                ))}
              </div>
            ) : topCards.length > 0 ? (
              <div className="home-brief__list">
                {topCards.map(card => (
                  <button key={card.id} className="home-brief__item" onClick={() => onTabChange('chat')}>
                    <span className="home-brief__icon">{CARD_TYPE_ICONS[card.card_type] || <FaRegLightbulb />}</span>
                    <div className="home-brief__item-text">
                      <span className="home-brief__title">{card.title}</span>
                      <span className="home-brief__body">{card.body}</span>
                    </div>
                  </button>
                ))}
              </div>
            ) : (
              <EmptyState
                icon={<FaRegLightbulb />}
                title={t('home.briefEmptyTitle')}
                subtitle={t('home.briefEmptySub')}
                action={
                  <button className="btn btn-secondary" onClick={() => onTabChange('chat')}>
                    {t('home.briefEmptyCta')}
                  </button>
                }
              />
            )}
          </section>

          {/* Current courses */}
          <section className="home-card">
            <SectionHeader
              icon={<FaBook />}
              title={t('home.currentCourses')}
              action={
                <button className="home-link" onClick={() => onTabChange('courses')}>
                  {t('home.exploreCourses')} <FaArrowRight />
                </button>
              }
            />
            {activeCourses.length > 0 ? (
              <div className="home-courses">
                {activeCourses.map(course => (
                  <button
                    key={course.course_code}
                    className="home-course-chip"
                    style={{ '--course-accent': courseAccent(course.course_code) }}
                    onClick={goToCurrentCourses}
                  >
                    <span className="home-course-chip__code">{course.course_code}</span>
                    {course.course_title && (
                      <span className="home-course-chip__title">{course.course_title}</span>
                    )}
                  </button>
                ))}
              </div>
            ) : upcomingCount > 0 ? (
              <EmptyState
                icon={<FaBook />}
                title={t('home.coursesNoneThisTerm')}
                subtitle={t('home.coursesUpcomingSub').replace('{count}', String(upcomingCount))}
                action={
                  <button className="btn btn-secondary" onClick={goToCurrentCourses}>
                    {t('home.coursesUpcomingCta')} <FaArrowRight />
                  </button>
                }
              />
            ) : (
              <EmptyState
                icon={<FaBook />}
                title={t('home.coursesEmptyTitle')}
                subtitle={t('home.coursesEmptySub')}
                action={
                  <button className="btn btn-secondary" onClick={onImportTranscript}>
                    <FaFileUpload /> {t('home.coursesEmptyCta')}
                  </button>
                }
              />
            )}
            {activeCourses.length > 0 && upcomingCount > 0 && (
              <button className="home-link" style={{ marginTop: 10 }} onClick={goToCurrentCourses}>
                {t('home.coursesUpcomingSub').replace('{count}', String(upcomingCount))} <FaArrowRight />
              </button>
            )}
          </section>
        </div>

        {/* ── Right column (Canvas "To Do") ── */}
        <div className="home-side">
          {/* Up Next */}
          <section className="home-card">
            <SectionHeader
              icon={<FaCalendarAlt />}
              title={t('home.upNext')}
              action={
                <button className="home-link" onClick={() => onTabChange('calendar')}>
                  {t('home.openCalendar')} <FaArrowRight />
                </button>
              }
            />
            {eventsLoading && events.length === 0 ? (
              <div className="home-upnext__list">
                {[0, 1, 2].map(i => <Skeleton key={i} height="2.25rem" />)}
              </div>
            ) : events.length > 0 ? (
              <ul className="home-upnext__list">
                {events.map(ev => (
                  <li key={ev.id} className="home-upnext__item">
                    <span className="home-upnext__emoji">{EVENT_ICONS[ev.type] || <FaCalendarAlt />}</span>
                    <div className="home-upnext__text">
                      <span className="home-upnext__title">{ev.title}</span>
                      <span className="home-upnext__meta">
                        {formatDate(ev.date)}{ev.time ? ` · ${ev.time}` : ''}
                      </span>
                    </div>
                    <Badge variant={daysUntil(ev.date) <= 7 ? 'warning' : 'default'}>
                      {countdown(ev.date)}
                    </Badge>
                  </li>
                ))}
              </ul>
            ) : (
              <EmptyState
                icon={<FaCalendarAlt />}
                title={t('home.upNextEmptyTitle')}
                subtitle={t('home.upNextEmptySub')}
                action={
                  <button className="btn btn-secondary" onClick={onImportSyllabus}>
                    <FaFilePdf /> {t('home.upNextEmptyCta')}
                  </button>
                }
              />
            )}
          </section>

          {/* Degree progress */}
          <section className="home-card">
            <SectionHeader
              icon={<FaChartLine />}
              title={t('home.degreeProgress')}
              action={
                <button className="home-link" onClick={() => onTabChange('favorites')}>
                  {t('home.viewDegreePlan')} <FaArrowRight />
                </button>
              }
            />
            <DegreeProgressTracker completedCourses={completedCourses} profile={profile} compact />
          </section>

          {/* Quick actions */}
          <section className="home-card">
            <SectionHeader title={t('home.quickActions')} />
            <div className="home-actions">
              <button className="home-action" onClick={onImportTranscript}>
                <FaFileUpload /> {t('home.actionTranscript')}
              </button>
              <button className="home-action" onClick={onImportSyllabus}>
                <FaFilePdf /> {t('home.actionSyllabus')}
              </button>
              <button className="home-action" onClick={() => onTabChange('chat')}>
                <FaComments /> {t('home.actionAdvisor')}
              </button>
              <button className="home-action" onClick={() => onTabChange('calendar')}>
                <FaCalendarPlus /> {t('home.actionEvent')}
              </button>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
