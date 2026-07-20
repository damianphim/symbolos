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
  FaExclamationTriangle, FaExclamationCircle, FaChevronRight,
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import useViewport from '../../hooks/useViewport'
import { isCourseInActiveTerm } from '../../lib/termDates'
import DegreeProgressTracker from './DegreeProgressTracker'
import EmptyState from '../ui/EmptyState'
import Skeleton from '../ui/Skeleton'
import SectionHeader from '../ui/SectionHeader'
import Badge from '../ui/Badge'
import './HomeTab.css'

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
  advisorCards = [], cardsLoading = false, cardsGenerating = false,
  currentCourses = [], completedCourses = [],
  events = [], eventsLoading = false, hasCourseEvents = false,
  onTabChange, onViewCurrentCourses, onOpenBriefCard, onImportTranscript, onImportSyllabus,
}) {
  // Deep-link to My Courses → Current when available.
  const goToCurrentCourses = onViewCurrentCourses ?? (() => onTabChange('courses'))
  // Open a specific Brief card's chat; fall back to just switching tabs.
  const openBriefCard = (id) => (onOpenBriefCard ? onOpenBriefCard(id) : onTabChange('chat'))
  const { t, language } = useLanguage()
  // Mobile swaps the whole body for native grouped lists (see the mobile
  // return below). Switching on viewport, never on platform — mobile web gets
  // the same treatment as the native shell.
  const { isMobile } = useViewport()

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
  const resumeSetup = () => {
    setSetupDismissed(false)
    try { localStorage.removeItem(dismissKey) } catch { /* ignore */ }
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

  // Identical markup on both shells — only the surrounding body differs.
  const header = (
    <header className="home-header">
      <div>
        <h1 className="home-greeting">
          {greetName ? t('home.greeting').replace('{name}', greetName) : t('home.greetingNoName')}
        </h1>
        <p className="home-term">{t(currentTermKey()).replace('{year}', new Date().getFullYear())}</p>
      </div>
      {!setupComplete && (
        <button
          className="home-header__setup-badge"
          onClick={resumeSetup}
          title={setupDismissed ? t('setup.resume') : undefined}
        >
          <Badge variant="accent">{t('home.setupProgress').replace('{done}', doneCount).replace('{total}', steps.length)}</Badge>
        </button>
      )}
    </header>
  )

  // ══════════════════════════════════════════════════════════════
  // MOBILE (<= 768px)
  //
  // Home is the landing screen, so it sets the expectation for the whole app.
  // The desktop version is a grid of bordered cards floating on the page
  // background — the single most "website on a phone" shape there is. Here the
  // page is recessed (--m-bg-grouped, from the shell) and each section becomes
  // ONE raised .m-group whose rows are divided by hairlines, introduced by a
  // quiet .m-group-label sitting outside it.
  //
  // The exception is the Brief preview: an advisor card is a title + a
  // paragraph of prose, which is card-shaped content, not a list row. Those
  // stay cards — just flattened to native proportions (no border, softer
  // surface, roomier padding) rather than crammed into a row.
  //
  // `data-tour` anchors are deliberately absent: the tour only runs on the
  // desktop shell (its stops anchor to Sidebar buttons), so they stay on the
  // desktop path below.
  // ══════════════════════════════════════════════════════════════
  if (isMobile) {
    // Trailing navigation row that closes a group ("Open calendar", "View
     // all"). Being the last .m-row it inherits the group's bottom corners, so
     // the affordance lives inside the object it belongs to instead of
     // floating beside its heading the way the desktop header links do.
    const disclosure = (label, onClick) => (
      <button type="button" className="m-row m-row--tappable home-m-btn home-m-more" onClick={onClick}>
        <span className="home-m-more-label">{label}</span>
        <FaChevronRight className="home-m-chevron" />
      </button>
    )

    return (
      <div className="home-tab home-tab--mobile">
        {header}

        {/* ── Setup checklist ── */}
        {showSetup && (
          <section className="home-m-section">
            <div className="home-m-label-row">
              <span className="m-group-label">{t('setup.title')}</span>
              <button
                type="button"
                className="home-m-label-btn"
                onClick={dismissSetup}
                aria-label={t('setup.dismiss')}
              >
                <FaTimes />
              </button>
            </div>
            <ul className="m-group home-m-list">
              {steps.map(step => (
                <li key={step.key} className={`m-row home-m-step ${step.done ? 'is-done' : ''}`}>
                  <span className="home-setup__check">
                    {step.done ? <FaCheckCircle /> : <FaRegCircle />}
                  </span>
                  <div className="home-setup__text">
                    <span className="home-setup__step-title">{step.title}</span>
                    <span className="home-setup__step-sub">{step.sub}</span>
                  </div>
                  {!step.done && (
                    <button type="button" className="home-m-step-cta" onClick={step.onClick}>
                      {t('setup.start')}
                    </button>
                  )}
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* ── Up Next ── */}
        <section className="home-m-section">
          <div className="m-group-label">{t('home.upNext')}</div>
          <div className="m-group">
            {eventsLoading && events.length === 0 ? (
              [0, 1, 2].map(i => (
                <div key={i} className="m-row"><Skeleton height="1.25rem" /></div>
              ))
            ) : events.length > 0 ? (
              <>
                {events.map(ev => (
                  <button
                    key={ev.id}
                    type="button"
                    className="m-row m-row--tappable home-m-btn"
                    onClick={() => onTabChange('calendar')}
                  >
                    <span className="home-m-icon">{EVENT_ICONS[ev.type] || <FaCalendarAlt />}</span>
                    <span className="home-m-text">
                      <span className="home-m-title">{ev.title}</span>
                      <span className="home-m-sub">
                        {formatDate(ev.date)}{ev.time ? ` · ${ev.time}` : ''}
                      </span>
                    </span>
                    <Badge variant={daysUntil(ev.date) <= 7 ? 'warning' : 'default'}>
                      {countdown(ev.date)}
                    </Badge>
                  </button>
                ))}
                {disclosure(t('home.openCalendar'), () => onTabChange('calendar'))}
              </>
            ) : (
              <div className="home-m-empty">
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
              </div>
            )}
          </div>
        </section>

        {/* ── From your Brief — genuinely card-shaped, so it stays cards ── */}
        <section className="home-m-section">
          <div className="m-group-label">{t('home.fromYourBrief')}</div>
          {(cardsLoading && topCards.length === 0) || cardsGenerating ? (
            <div className="home-m-brief">
              {[0, 1].map(i => (
                <div key={i} className="home-m-brief-card">
                  <Skeleton width="55%" />
                  <Skeleton width="90%" />
                </div>
              ))}
            </div>
          ) : topCards.length > 0 ? (
            <div className="home-m-brief">
              {topCards.map(card => (
                <button
                  key={card.id}
                  type="button"
                  className="home-m-brief-card home-m-brief-card--tappable"
                  onClick={() => openBriefCard(card.id)}
                >
                  <span className="home-m-brief-top">
                    <span className="home-m-brief-icon">
                      {CARD_TYPE_ICONS[card.card_type] || <FaRegLightbulb />}
                    </span>
                    <span className="home-m-brief-title">{card.title}</span>
                    <FaChevronRight className="home-m-chevron" />
                  </span>
                  <span className="home-m-brief-body">{card.body}</span>
                </button>
              ))}
              <div className="m-group home-m-group--tight">
                {disclosure(t('home.viewAll'), () => onTabChange('chat'))}
              </div>
            </div>
          ) : (
            <div className="m-group">
              <div className="home-m-empty">
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
              </div>
            </div>
          )}
        </section>

        {/* ── Current courses ── */}
        <section className="home-m-section">
          <div className="m-group-label">{t('home.currentCourses')}</div>
          <div className="m-group">
            {activeCourses.length > 0 ? (
              <>
                {activeCourses.map(course => (
                  <button
                    key={course.course_code}
                    type="button"
                    className="m-row m-row--tappable home-m-btn"
                    onClick={goToCurrentCourses}
                  >
                    <span className="home-m-icon"><FaBook /></span>
                    <span className="home-m-text">
                      <span className="home-m-title">{course.course_code}</span>
                      {course.course_title && (
                        <span className="home-m-sub">{course.course_title}</span>
                      )}
                    </span>
                    <FaChevronRight className="home-m-chevron" />
                  </button>
                ))}
                {upcomingCount > 0 && disclosure(
                  t('home.coursesUpcomingSub').replace('{count}', String(upcomingCount)),
                  goToCurrentCourses,
                )}
                {disclosure(t('home.exploreCourses'), () => onTabChange('courses'))}
              </>
            ) : upcomingCount > 0 ? (
              <div className="home-m-empty">
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
              </div>
            ) : (
              <div className="home-m-empty">
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
              </div>
            )}
          </div>
        </section>

        {/* ── Degree progress ── */}
        <section className="home-m-section">
          <div className="m-group-label">{t('home.degreeProgress')}</div>
          <div className="m-group">
            <div className="home-m-degree">
              <DegreeProgressTracker completedCourses={completedCourses} profile={profile} compact />
            </div>
            {disclosure(t('home.viewDegreePlan'), () => onTabChange('favorites'))}
          </div>
        </section>

        {/* ── Quick actions ── */}
        <section className="home-m-section">
          <div className="m-group-label">{t('home.quickActions')}</div>
          <div className="m-group">
            {[
              { key: 'transcript', icon: <FaFileUpload />, label: t('home.actionTranscript'), onClick: onImportTranscript },
              { key: 'syllabus',   icon: <FaFilePdf />,    label: t('home.actionSyllabus'),   onClick: onImportSyllabus },
              { key: 'advisor',    icon: <FaComments />,   label: t('home.actionAdvisor'),    onClick: () => onTabChange('chat') },
              { key: 'event',      icon: <FaCalendarPlus />, label: t('home.actionEvent'),    onClick: () => onTabChange('calendar') },
            ].map(action => (
              <button
                key={action.key}
                type="button"
                className="m-row m-row--tappable home-m-btn"
                onClick={action.onClick}
              >
                <span className="home-m-icon">{action.icon}</span>
                <span className="home-m-text">
                  <span className="home-m-title">{action.label}</span>
                </span>
                <FaChevronRight className="home-m-chevron" />
              </button>
            ))}
          </div>
        </section>
      </div>
    )
  }

  return (
    <div className="home-tab">
      {/* ── Header ── */}
      {header}

      <div className="home-grid">
        {/* ── Main column ── */}
        <div className="home-main">
          {showSetup && (
            <section className="home-card home-setup" data-tour="home-setup">
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

          {/* Up Next */}
          <section className="home-card">
            <SectionHeader
              icon={<FaCalendarAlt />}
              iconColor="#ed1b2f"
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

          {/* From your Brief */}
          <section className="home-card">
            <SectionHeader
              icon={<FaRegLightbulb />}
              iconColor="#ed1b2f"
              title={t('home.fromYourBrief')}
              action={
                <button className="home-link" onClick={() => onTabChange('chat')}>
                  {t('home.viewAll')} <FaArrowRight />
                </button>
              }
            />
            {(cardsLoading && topCards.length === 0) || cardsGenerating ? (
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
                  <button key={card.id} className="home-brief__item" onClick={() => openBriefCard(card.id)}>
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
              iconColor="#ed1b2f"
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
          {/* Degree progress */}
          <section className="home-card">
            <SectionHeader
              icon={<FaChartLine />}
              iconColor="#ed1b2f"
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
