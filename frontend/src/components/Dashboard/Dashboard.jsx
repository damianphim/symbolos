import { useState, useEffect, lazy, Suspense } from 'react'
import { DashboardDataProvider, useDashboardData } from '../../contexts/DashboardDataContext'
import { CourseDetailProvider } from '../../contexts/CourseDetailContext'
import useViewport from '../../hooks/useViewport'
import DashboardTabContent from './DashboardTabContent'
import MobileLayout from './MobileLayout'
import RightSidebar from './RightSidebar'
import Sidebar from './Sidebar'
import CourseDetailModal from '../shared/CourseDetailModal'
import './Dashboard.css'

const TranscriptUpload   = lazy(() => import('./TranscriptUpload'))
const FeedbackModal      = lazy(() => import('./FeedbackModal'))
const MarkCompleteModal  = lazy(() => import('./MarkCompleteModal'))
const OnboardingTutorial = lazy(() => import('./OnboardingTutorial'))

/**
 * Desktop dashboard view.
 *
 * Owns only what is specific to *this* shell: the collapsible left sidebar,
 * the pinned-card right sidebar, and the onboarding tour (which anchors its
 * stops to Sidebar nav buttons via data-tour attributes, mobile ships its
 * own tutorial rather than reusing these anchors).
 *
 * All data and business logic comes from DashboardDataContext; the eight
 * screens themselves come from DashboardTabContent, shared with MobileLayout.
 */
function DesktopDashboard() {
  const {
    user, profile,
    activeTab, setActiveTab, handleTabChange: onTabChange,
    setCoursesDeepLink, setBriefOpenCardId,
    handleCardChipClick,
    favorites, profileImage,
    isFavorited, isCompleted, isCurrent,
    handleToggleFavorite, handleToggleCompleted, handleToggleCurrent,
    degreeProgressRef,
    upcomingUrgentCount,
    showCompleteCourseModal, courseToComplete, handleConfirmComplete, handleRemoveCompleted, cancelCompleteCourse,
    showTranscriptUpload, transcriptUploadTab, setShowTranscriptUpload,
    handleTranscriptImportComplete,
    handleSignOut,
  } = useDashboardData()

  // ── Layout ─────────────────────────────────────────────
  // Sidebar open/closed state, persisted across reloads but defaults to OPEN
  // on first visit so new users see the navigation rail.
  const [sidebarOpen, setSidebarOpen] = useState(() => {
    try {
      const stored = localStorage.getItem('sidebar_open')
      if (stored === null) return true   // first visit → open
      return stored === 'true'
    } catch {
      return true
    }
  })
  useEffect(() => {
    try { localStorage.setItem('sidebar_open', String(sidebarOpen)) } catch { /* ignore */ }
  }, [sidebarOpen])

  // Feedback modal is opened from the Sidebar, so its state lives with the
  // shell that renders that trigger.
  const [feedbackOpen, setFeedbackOpen] = useState(false)

  // Desktop-only side effect on tab change: collapse the sidebar on narrow
  // viewports so the content isn't hidden behind it.
  const handleTabChange = (tab) => {
    onTabChange(tab)
    if (window.innerWidth < 768) setSidebarOpen(false)
  }

  // Deep links from Home. These route through the local handleTabChange (not
  // the context's) so they collapse the sidebar exactly as before.
  const handleOpenBriefCard = (cardId) => {
    setBriefOpenCardId(cardId)
    handleTabChange('chat')
  }

  const openCurrentCourses = () => {
    setCoursesDeepLink({ subTab: 'my_courses', savedTab: 'current' })
    handleTabChange('courses')
  }

  const tourKey = `symbolos_tour_done_${user?.id}`
  // Only auto-show the walkthrough for genuinely new accounts (≤3 days old and
  // not yet completed) or returning users who've been away ≥30 days, never on
  // every login.
  const [showTutorial, setShowTutorial] = useState(() => {
    if (!user?.id) return false
    const DAY = 86400000, now = Date.now()
    const firstSeenKey = `symbolos_first_seen_${user.id}`
    if (!localStorage.getItem(firstSeenKey)) localStorage.setItem(firstSeenKey, String(now))
    const created = profile?.created_at ? new Date(profile.created_at).getTime() : NaN
    const createdMs = Number.isNaN(created) ? Number(localStorage.getItem(firstSeenKey)) : created
    const lastSeen = Number(localStorage.getItem(`symbolos_last_seen_${user.id}`)) || 0
    const done = !!localStorage.getItem(`symbolos_tour_done_${user.id}`)
    const accountAgeDays = (now - createdMs) / DAY
    const daysSinceSeen = lastSeen ? (now - lastSeen) / DAY : 0
    return (accountAgeDays <= 3 && !done) || (lastSeen > 0 && daysSinceSeen >= 30)
  })
  // Record this visit so we can detect a ≥30-day gap next time.
  useEffect(() => {
    if (user?.id) localStorage.setItem(`symbolos_last_seen_${user.id}`, String(Date.now()))
  }, [user?.id])
  // Keep sidebar expanded so data-tour targets are in the DOM during the walkthrough
  useEffect(() => {
    if (showTutorial) setSidebarOpen(true)
  }, [showTutorial])

  // Listen for `restart-tour` (fired by the "Replay tour" button in Settings)
  //, clear the completion flag and start the walkthrough over from Home.
  useEffect(() => {
    const handler = () => {
      try { localStorage.removeItem(tourKey) } catch { /* ignore */ }
      setActiveTab('home')
      setShowTutorial(true)
    }
    window.addEventListener('restart-tour', handler)
    return () => window.removeEventListener('restart-tour', handler)
  }, [tourKey, setActiveTab])

  // ── Right sidebar / pinned chat ─────────────────────────
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false)
  const [pinnedCard, setPinnedCard] = useState(null)
  const [pinnedThread, setPinnedThread] = useState([])
  const [pinnedIsThinking, setPinnedIsThinking] = useState(false)

  // ── Sync right sidebar width as CSS var ──────────────────
  // On phones the right sidebar overlays the content as a drawer
  // (see RightSidebar.css mobile rules), so it doesn't push layout
  // and --rsb-width should stay 0, otherwise the FeedbackModal
  // trigger button hides off-screen.
  useEffect(() => {
    const apply = () => {
      const isMobile = window.matchMedia('(max-width: 768px)').matches
      const visible = rightSidebarOpen && activeTab !== 'chat' && !isMobile
      document.body.style.setProperty('--rsb-width', visible ? '320px' : '0px')
    }
    apply()
    window.addEventListener('resize', apply)
    return () => {
      window.removeEventListener('resize', apply)
      document.body.style.setProperty('--rsb-width', '0px')
    }
  }, [rightSidebarOpen, activeTab])

  // ── Pinned card handler ───────────────────────────────────
  const handlePinToggle = (card, thread) => {
    if (!card) {
      setPinnedCard(null)
      setPinnedThread([])
      setRightSidebarOpen(false)
    } else {
      setPinnedCard(card)
      setPinnedThread(thread || [])
      setRightSidebarOpen(true)
    }
  }

  const handlePinnedSend = async (message) => {
    if (!user?.id || !pinnedCard) return
    // Snapshot before appending, the advisor needs the conversation so far to
    // resolve a short follow-up ("A") against what it just offered.
    const priorThread = pinnedThread
    setPinnedThread(prev => [...prev, { role: 'user', content: message }])
    setPinnedIsThinking(true)
    try {
      const reply = await handleCardChipClick(pinnedCard.id, message, pinnedCard.title, pinnedCard.body, priorThread)
      setPinnedThread(prev => [...prev, { role: 'assistant', content: reply }])
    } catch {
      setPinnedThread(prev => [...prev, { role: 'assistant', content: 'Something went wrong. Please try again.' }])
    } finally {
      setPinnedIsThinking(false)
    }
  }

  // ── Render ─────────────────────────────────────────────
  return (
    <>
    <div className="dashboard">
      <Sidebar
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        activeTab={activeTab}
        onTabChange={handleTabChange}
        favorites={favorites}
        profileImage={profileImage}
        user={user}
        profile={profile}
        onSignOut={handleSignOut}
        badges={{ calendar: upcomingUrgentCount > 0 ? upcomingUrgentCount : null }}
        onOpenFeedback={() => setFeedbackOpen(true)}
      />

      <main className="main-content">
        <button
          className="mobile-menu-btn-overlay"
          onClick={() => setSidebarOpen(true)}
          aria-label="Open menu"
        >☰</button>

        <div className="content-area">
          <DashboardTabContent
            onTabChange={handleTabChange}
            onOpenBriefCard={handleOpenBriefCard}
            onViewCurrentCourses={openCurrentCourses}
            onPinToggle={handlePinToggle}
            pinnedCardId={pinnedCard?.id || null}
          />
        </div>
      </main>

      {showCompleteCourseModal && courseToComplete && (
        <Suspense fallback={null}>
          <MarkCompleteModal
            course={courseToComplete}
            onConfirm={handleConfirmComplete}
            onRemove={handleRemoveCompleted}
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

      <RightSidebar
        isOpen={rightSidebarOpen}
        setIsOpen={setRightSidebarOpen}
        pinnedCard={pinnedCard}
        pinnedThread={pinnedThread}
        pinnedIsThinking={pinnedIsThinking}
        onSend={handlePinnedSend}
        onUnpin={() => handlePinToggle(null, [])}
        activeTab={activeTab}
        degreeProgressRef={degreeProgressRef}
      />

      <Suspense fallback={null}>
        <FeedbackModal userId={user?.id} userEmail={user?.email} open={feedbackOpen} onClose={() => setFeedbackOpen(false)} />
      </Suspense>

      {showTutorial && (
        <Suspense fallback={null}>
          <OnboardingTutorial
            onTabChange={setActiveTab}
            onComplete={() => {
              localStorage.setItem(tourKey, '1')
              setShowTutorial(false)
            }}
          />
        </Suspense>
      )}
    </div>

    <CourseDetailModal
      isFavorited={isFavorited}
      isCompleted={isCompleted}
      isCurrent={isCurrent}
      onToggleFavorite={handleToggleFavorite}
      onToggleCompleted={handleToggleCompleted}
      onToggleCurrent={handleToggleCurrent}
    />
    </>
  )
}

/**
 * Picks the layout shell by viewport width. Both shells sit inside the same
 * providers, so switching between them (rotating a tablet, dragging a desktop
 * window narrow) preserves all loaded data and the current tab, only the
 * presentation swaps.
 */
function DashboardShell() {
  const { isMobile } = useViewport()
  return isMobile ? <MobileLayout /> : <DesktopDashboard />
}

export default function Dashboard() {
  return (
    <DashboardDataProvider>
      <CourseDetailProvider>
        <DashboardShell />
      </CourseDetailProvider>
    </DashboardDataProvider>
  )
}
