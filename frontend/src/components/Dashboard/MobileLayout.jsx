import { useState, useEffect, lazy, Suspense } from 'react'
import {
  FaHome, FaRegLightbulb, FaGraduationCap, FaCalendarAlt, FaUser,
  FaBook, FaUsers, FaComments, FaEllipsisH, FaCog, FaPalette,
  FaSignOutAlt, FaInfoCircle, FaShieldAlt, FaFileAlt, FaSun, FaMoon,
  FaCommentDots,
} from 'react-icons/fa'
import { MdLanguage } from 'react-icons/md'
import { useDashboardData } from '../../contexts/DashboardDataContext'
import { useTheme, useLanguage } from '../../contexts/PreferencesContext'
import DashboardTabContent from './DashboardTabContent'
import CourseDetailModal from '../shared/CourseDetailModal'
import PrivacyPolicy from '../Legal/PrivacyPolicy'
import TermsOfService from '../Legal/TOS'
import AboutUs from '../Legal/AboutUs'
import './MobileLayout.css'

const TranscriptUpload  = lazy(() => import('./TranscriptUpload'))
const FeedbackModal     = lazy(() => import('./FeedbackModal'))
const MarkCompleteModal = lazy(() => import('./MarkCompleteModal'))

// Five primary destinations. The desktop sidebar carries all eight, but a
// bottom bar has roughly five thumb-width slots before targets get too small
// to hit reliably — so the long tail moves into the More sheet rather than
// making the bar scroll horizontally (scrolled-off tabs are effectively
// undiscoverable).
const PRIMARY_TABS = (t) => [
  { key: 'home',      icon: <FaHome />,          label: t('nav.home') },
  { key: 'chat',      icon: <FaRegLightbulb />,  label: t('nav.chat') },
  { key: 'favorites', icon: <FaGraduationCap />, label: t('nav.degreePlanning') },
  { key: 'calendar',  icon: <FaCalendarAlt />,   label: t('nav.calendar') },
  { key: 'profile',   icon: <FaUser />,          label: t('nav.profile') },
]

const MORE_TABS = (t) => [
  { key: 'courses', icon: <FaBook />,     label: t('nav.courses') },
  { key: 'clubs',   icon: <FaUsers />,    label: t('nav.clubs') },
  { key: 'forum',   icon: <FaComments />, label: t('nav.forum') },
]

/**
 * Mobile layout shell.
 *
 * Full-screen pages with a bottom tab bar, selected by viewport width (not by
 * native platform) so mobile web visitors get the same UI as app users.
 *
 * Intentionally does NOT render the desktop Sidebar or the pinned-card
 * RightSidebar: pinning is a two-column metaphor with nowhere to go on a
 * phone. The onboarding tour is also omitted — its stops anchor to Sidebar
 * nav buttons, so mobile ships its own tutorial instead.
 */
export default function MobileLayout() {
  const {
    user, profile,
    activeTab, handleTabChange,
    setCoursesDeepLink, setBriefOpenCardId,
    upcomingUrgentCount,
    showCompleteCourseModal, courseToComplete, handleConfirmComplete, cancelCompleteCourse,
    showTranscriptUpload, transcriptUploadTab, setShowTranscriptUpload,
    handleTranscriptImportComplete,
    isFavorited, isCompleted, isCurrent,
    handleToggleFavorite, handleToggleCompleted, handleToggleCurrent,
    handleSignOut,
  } = useDashboardData()

  const { t, language, setLanguage } = useLanguage()
  const { theme, setTheme } = useTheme()

  const [moreOpen, setMoreOpen] = useState(false)
  const [feedbackOpen, setFeedbackOpen] = useState(false)
  const [legalModal, setLegalModal] = useState(null) // 'privacy' | 'terms' | 'about'

  const primary = PRIMARY_TABS(t)
  const more    = MORE_TABS(t)
  const activeIsInMore = more.some(m => m.key === activeTab)

  // Scroll a newly-opened page back to the top. Without this, moving from a
  // scrolled Home into Calendar lands mid-page.
  useEffect(() => {
    const el = document.querySelector('.mobile-content')
    if (el) el.scrollTop = 0
  }, [activeTab])

  // Close the More sheet on Escape (external keyboards, and Android's back
  // gesture surfaces as Escape in some WebView configurations).
  useEffect(() => {
    if (!moreOpen) return
    const onKey = (e) => { if (e.key === 'Escape') setMoreOpen(false) }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [moreOpen])

  const go = (tab) => {
    handleTabChange(tab)
    setMoreOpen(false)
  }

  const onOpenBriefCard = (cardId) => {
    setBriefOpenCardId(cardId)
    go('chat')
  }

  const onViewCurrentCourses = () => {
    setCoursesDeepLink({ subTab: 'my_courses', savedTab: 'current' })
    go('courses')
  }

  const cycleTheme = () => setTheme(theme === 'light' ? 'dark' : theme === 'dark' ? 'auto' : 'light')
  const nextLanguage = () => setLanguage(language === 'en' ? 'fr' : language === 'fr' ? 'zh' : 'en')

  const themeLabel = theme === 'light' ? t('settings.light')
    : theme === 'dark' ? t('settings.dark')
    : t('settings.auto')

  return (
    <div className="mobile-shell">
      {legalModal === 'privacy' && <PrivacyPolicy onClose={() => setLegalModal(null)} />}
      {legalModal === 'terms'   && <TermsOfService onClose={() => setLegalModal(null)} />}
      {legalModal === 'about'   && <AboutUs onClose={() => setLegalModal(null)} />}

      {/* No top bar. A persistent header that only repeats the active tab's
          name is web chrome, not app chrome — the tab bar already says where
          you are, and the header cost ~52px of vertical space on every
          screen. Screens that need a title render their own, in content,
          where it can scroll away. */}
      <main className="mobile-content">
        <DashboardTabContent
          onTabChange={go}
          onOpenBriefCard={onOpenBriefCard}
          onViewCurrentCourses={onViewCurrentCourses}
          onPinToggle={undefined}
          pinnedCardId={null}
        />
      </main>

      {/* ── Bottom tab bar ── */}
      <nav className="mobile-tabbar" aria-label={t('nav.home')}>
        {primary.map(({ key, icon, label }) => (
          <button
            key={key}
            className={`mobile-tab ${activeTab === key ? 'mobile-tab--active' : ''}`}
            onClick={() => go(key)}
            aria-current={activeTab === key ? 'page' : undefined}
            aria-label={label}
          >
            <span className="mobile-tab-icon">
              {icon}
              {key === 'calendar' && upcomingUrgentCount > 0 && (
                <span className="mobile-tab-badge">
                  {upcomingUrgentCount > 9 ? '9+' : upcomingUrgentCount}
                </span>
              )}
            </span>
            <span className="mobile-tab-label">{label}</span>
          </button>
        ))}

        <button
          className={`mobile-tab ${activeIsInMore ? 'mobile-tab--active' : ''}`}
          onClick={() => setMoreOpen(true)}
          aria-label={t('nav.more')}
          aria-expanded={moreOpen}
        >
          <span className="mobile-tab-icon"><FaEllipsisH /></span>
          <span className="mobile-tab-label">{t('nav.more')}</span>
        </button>
      </nav>

      {/* ── More sheet ── */}
      {moreOpen && (
        <>
          <div className="mobile-sheet-overlay" onClick={() => setMoreOpen(false)} />
          <div className="mobile-sheet" role="dialog" aria-modal="true" aria-label={t('nav.more')}>
            <div className="mobile-sheet-handle" />

            <div className="mobile-sheet-user">
              <div className="mobile-sheet-avatar">
                {profile?.profile_image
                  ? <img src={profile.profile_image} alt="" />
                  : (user?.email?.[0]?.toUpperCase() || '?')}
              </div>
              <div className="mobile-sheet-userinfo">
                <div className="mobile-sheet-username">{profile?.username || t('common.user')}</div>
                <div className="mobile-sheet-useremail">{user?.email}</div>
              </div>
            </div>

            <div className="mobile-sheet-grid">
              {more.map(({ key, icon, label }) => (
                <button
                  key={key}
                  className={`mobile-sheet-item ${activeTab === key ? 'mobile-sheet-item--active' : ''}`}
                  onClick={() => go(key)}
                >
                  <span className="mobile-sheet-icon">{icon}</span>
                  <span>{label}</span>
                </button>
              ))}
            </div>

            <div className="mobile-sheet-divider" />

            <button className="mobile-sheet-row" onClick={() => { setMoreOpen(false); go('profile') }}>
              <span className="mobile-sheet-icon"><FaCog /></span>
              <span>{t('sidebar.settings')}</span>
            </button>
            <button className="mobile-sheet-row" onClick={nextLanguage}>
              <span className="mobile-sheet-icon"><MdLanguage /></span>
              <span>{language === 'en' ? 'Français' : language === 'fr' ? '中文' : 'English'}</span>
            </button>
            <button className="mobile-sheet-row" onClick={cycleTheme}>
              <span className="mobile-sheet-icon">
                {theme === 'dark' ? <FaMoon /> : theme === 'auto' ? <FaPalette /> : <FaSun />}
              </span>
              <span>{t('sidebar.colorTheme')}: {themeLabel}</span>
            </button>
            <button className="mobile-sheet-row" onClick={() => { setMoreOpen(false); setFeedbackOpen(true) }}>
              <span className="mobile-sheet-icon"><FaCommentDots /></span>
              <span>{t('fb.button')}</span>
            </button>

            <div className="mobile-sheet-divider" />

            <button className="mobile-sheet-row" onClick={() => { setMoreOpen(false); setLegalModal('about') }}>
              <span className="mobile-sheet-icon"><FaInfoCircle /></span>
              <span>{t('sidebar.aboutSymbolos')}</span>
            </button>
            <button className="mobile-sheet-row" onClick={() => { setMoreOpen(false); setLegalModal('privacy') }}>
              <span className="mobile-sheet-icon"><FaShieldAlt /></span>
              <span>{t('sidebar.privacyPolicy')}</span>
            </button>
            <button className="mobile-sheet-row" onClick={() => { setMoreOpen(false); setLegalModal('terms') }}>
              <span className="mobile-sheet-icon"><FaFileAlt /></span>
              <span>{t('sidebar.termsOfService')}</span>
            </button>

            <div className="mobile-sheet-divider" />

            <button
              className="mobile-sheet-row mobile-sheet-row--danger"
              onClick={() => { setMoreOpen(false); handleSignOut() }}
            >
              <span className="mobile-sheet-icon"><FaSignOutAlt /></span>
              <span>{t('sidebar.logOut')}</span>
            </button>

            <div className="mobile-sheet-footer">{t('rsb.notAffiliated')}</div>
          </div>
        </>
      )}

      {showCompleteCourseModal && courseToComplete && (
        <Suspense fallback={null}>
          <MarkCompleteModal
            course={courseToComplete}
            onConfirm={handleConfirmComplete}
            onCancel={cancelCompleteCourse}
          />
        </Suspense>
      )}

      {showTranscriptUpload && (
        <Suspense fallback={null}>
          <TranscriptUpload
            userId={user?.id}
            defaultTab={transcriptUploadTab}
            onClose={() => setShowTranscriptUpload(false)}
            onImportComplete={handleTranscriptImportComplete}
          />
        </Suspense>
      )}

      <Suspense fallback={null}>
        <FeedbackModal
          userId={user?.id}
          userEmail={user?.email}
          open={feedbackOpen}
          onClose={() => setFeedbackOpen(false)}
        />
      </Suspense>

      <CourseDetailModal
        isFavorited={isFavorited}
        isCompleted={isCompleted}
        isCurrent={isCurrent}
        onToggleFavorite={handleToggleFavorite}
        onToggleCompleted={handleToggleCompleted}
        onToggleCurrent={handleToggleCurrent}
      />
    </div>
  )
}
