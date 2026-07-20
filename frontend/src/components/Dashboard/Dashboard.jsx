import { useState, useEffect, lazy, Suspense } from 'react'
import { DashboardDataProvider, useDashboardData } from '../../contexts/DashboardDataContext'
import AdvisorCards from './chat/AdvisorCards'
import HomeTab from './HomeTab'
import RightSidebar from './RightSidebar'
import CoursesView from './CoursesView'

import Sidebar from './Sidebar'

// Code-split everything that isn't on the default landing screen. Home is
// the default tab and ships in the main bundle (Brief/Chat stays static too
// since Home links straight into it); secondary tabs and modals only
// download when the user navigates to them.
const ClubsTab          = lazy(() => import('./ClubsTab'))
const ProfileTab        = lazy(() => import('./ProfileTab'))
const DegreePlanningView = lazy(() => import('./DegreePlanningView'))
const Forum             = lazy(() => import('../Forum/Forum'))
const CalendarTab       = lazy(() => import('./CalendarTab'))
const TranscriptUpload  = lazy(() => import('./TranscriptUpload'))
const FeedbackModal     = lazy(() => import('./FeedbackModal'))
const MarkCompleteModal = lazy(() => import('./MarkCompleteModal'))
const OnboardingTutorial = lazy(() => import('./OnboardingTutorial'))

import { CourseDetailProvider } from '../../contexts/CourseDetailContext'
import CourseDetailModal from '../shared/CourseDetailModal'
import './Dashboard.css'

// Tiny inline spinner used as Suspense fallback for lazy tabs
function TabLoader() {
  return (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      minHeight: '40vh', color: 'var(--text-secondary)',
    }}>
      <div style={{
        width: 28, height: 28, border: '3px solid var(--border-color)',
        borderTopColor: 'var(--accent-primary, #ed1b2f)', borderRadius: '50%',
        animation: 'spin 0.7s linear infinite',
      }} />
    </div>
  )
}

/**
 * Desktop dashboard view.
 *
 * Owns only what is specific to *this* shell: the collapsible left sidebar,
 * the pinned-card right sidebar, and the desktop onboarding tour (which
 * anchors its tour stops to Sidebar nav buttons via data-tour attributes —
 * mobile ships its own tutorial rather than reusing these anchors).
 *
 * All data and business logic comes from DashboardDataContext.
 */
function DesktopDashboard() {
  const {
    user, profile, authFlags, updateProfile,
    activeTab, setActiveTab, handleTabChange: onTabChange,
    coursesDeepLink, setCoursesDeepLink,
    briefOpenCardId, setBriefOpenCardId,

    advisorCards, cardsLoading, cardsGenerating, cardsGeneratedAt,
    freeformInput, setFreeformInput, isAsking,
    refreshAdvisorCards, handleCardSaveToggle, handleCardsReorder,
    handleCardChipClick, handleDeleteCard, handleFreeformSubmit,

    searchQuery, setSearchQuery, searchResults, isSearching, searchError,
    searchCorrection, hasSearched, sortBy, setSortBy, searchTerm, setSearchTerm,
    availableTerms, handleCourseSearch, sortCourses,

    favorites, favoritesMap,
    completedCourses, completedCoursesMap,
    currentCourses, currentCoursesMap,
    isFavorited, isCompleted, isCurrent,
    handleToggleFavorite, handleToggleCompleted, handleToggleCurrent,

    upcomingEvents, upcomingEventsLoading, upcomingUrgentCount, hasUpcomingCourseEvents,

    clubCalendarEvents, setClubCalendarEvents, managedClubs,

    showCompleteCourseModal, courseToComplete, handleConfirmComplete, cancelCompleteCourse,

    showTranscriptUpload, transcriptUploadTab, setShowTranscriptUpload,
    openTranscriptUpload, openSyllabusUpload, handleTranscriptImportComplete,

    profileImage, isUploadingImage, fileInputRef, handleImageUpload, handleAvatarClick,

    gpaToLetterGrade, handleSignOut,
  } = useDashboardData()

  // ── Layout ─────────────────────────────────────────────
  // Sidebar open/closed state — persisted across reloads but defaults to OPEN
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
  // not yet completed) or returning users who've been away ≥30 days — never on
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
  // — clear the completion flag and start the walkthrough over from Home.
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
  // and --rsb-width should stay 0 — otherwise the FeedbackModal
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
    setPinnedThread(prev => [...prev, { role: 'user', content: message }])
    setPinnedIsThinking(true)
    try {
      const reply = await handleCardChipClick(pinnedCard.id, message, pinnedCard.title, pinnedCard.body)
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
      />

      <main className="main-content">
        <button
          className="mobile-menu-btn-overlay"
          onClick={() => setSidebarOpen(true)}
          aria-label="Open menu"
        >☰</button>

        <div className="content-area">

          {activeTab === 'home' && (
            <HomeTab
              user={user}
              profile={profile}
              advisorCards={advisorCards}
              cardsLoading={cardsLoading}
              cardsGenerating={cardsGenerating}
              currentCourses={currentCourses}
              completedCourses={completedCourses}
              events={upcomingEvents}
              eventsLoading={upcomingEventsLoading}
              hasCourseEvents={hasUpcomingCourseEvents}
              onTabChange={handleTabChange}
              onViewCurrentCourses={openCurrentCourses}
              onOpenBriefCard={handleOpenBriefCard}
              onImportTranscript={openTranscriptUpload}
              onImportSyllabus={openSyllabusUpload}
            />
          )}

          {activeTab === 'chat' && (
            <AdvisorCards
              userId={user?.id}
              cards={advisorCards}
              isLoading={cardsLoading}
              isGenerating={cardsGenerating}
              isAsking={isAsking}
              generatedAt={cardsGeneratedAt}
              onRefresh={() => refreshAdvisorCards(true)}
              onSaveToggle={handleCardSaveToggle}
              onPinToggle={handlePinToggle}
              pinnedCardId={pinnedCard?.id || null}
              onReorder={handleCardsReorder}
              onChipClick={handleCardChipClick}
              onFollowUp={handleCardChipClick}
              onDeleteCard={handleDeleteCard}
              freeformInput={freeformInput}
              setFreeformInput={setFreeformInput}
              onFreeformSubmit={handleFreeformSubmit}
              openCardId={briefOpenCardId}
              onOpenedCard={() => setBriefOpenCardId(null)}
            />
          )}

          {activeTab === 'clubs' && (
            <Suspense fallback={<TabLoader />}>
              <ClubsTab
                key="clubs-tab-v2"
                user={user}
                profile={profile}
                authFlags={authFlags}
                onClubEventsChange={setClubCalendarEvents}
              />
            </Suspense>
          )}

          {activeTab === 'courses' && (
            <CoursesView
              defaultSubTab={coursesDeepLink?.subTab ?? 'course_search'}
              defaultSavedTab={coursesDeepLink?.savedTab ?? 'saved'}
              favorites={favorites}
              completedCourses={completedCourses}
              completedCoursesMap={completedCoursesMap}
              currentCourses={currentCourses}
              currentCoursesMap={currentCoursesMap}
              favoritesMap={favoritesMap}
              onToggleFavorite={handleToggleFavorite}
              onToggleCompleted={handleToggleCompleted}
              onToggleCurrent={handleToggleCurrent}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              searchResults={searchResults}
              isSearching={isSearching}
              searchError={searchError}
              searchCorrection={searchCorrection}
              hasSearched={hasSearched}
              sortBy={sortBy}
              setSortBy={setSortBy}
              sortCourses={sortCourses}
              searchTerm={searchTerm}
              setSearchTerm={setSearchTerm}
              availableTerms={availableTerms}
              isFavorited={isFavorited}
              isCompleted={isCompleted}
              isCurrent={isCurrent}
              handleCourseSearch={handleCourseSearch}
              handleToggleFavorite={handleToggleFavorite}
              handleToggleCompleted={handleToggleCompleted}
              handleToggleCurrent={handleToggleCurrent}
              gpaToLetterGrade={gpaToLetterGrade}
            />
          )}

          {activeTab === 'favorites' && (
            <Suspense fallback={<TabLoader />}>
              <DegreePlanningView
                favorites={favorites}
                completedCourses={completedCourses}
                completedCoursesMap={completedCoursesMap}
                currentCourses={currentCourses}
                currentCoursesMap={currentCoursesMap}
                favoritesMap={favoritesMap}
                profile={profile}
                authFlags={authFlags}
                onToggleFavorite={handleToggleFavorite}
                onToggleCompleted={handleToggleCompleted}
                onToggleCurrent={handleToggleCurrent}
                onImportTranscript={openTranscriptUpload}
                onImportSyllabus={openSyllabusUpload}
                onCourseClick={undefined}
              />
            </Suspense>
          )}

          {activeTab === 'forum' && (
            <Suspense fallback={<TabLoader />}>
              <Forum />
            </Suspense>
          )}

          {activeTab === 'calendar' && (
            <Suspense fallback={<TabLoader />}>
              <CalendarTab user={user} authFlags={authFlags} clubEvents={clubCalendarEvents} managedClubs={managedClubs} />
            </Suspense>
          )}

          {activeTab === 'profile' && (
            <Suspense fallback={<TabLoader />}>
              <ProfileTab
                user={user}
                profile={profile}
                updateProfile={updateProfile}
                signOut={handleSignOut}
                profileImage={profileImage}
                isUploadingImage={isUploadingImage}
                fileInputRef={fileInputRef}
                handleImageUpload={handleImageUpload}
                handleAvatarClick={handleAvatarClick}
                completedCourses={completedCourses}
                favorites={favorites}
                chatHistory={[]}
                onImportTranscript={openTranscriptUpload}
              />
            </Suspense>
          )}
        </div>
      </main>

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

      <RightSidebar
        isOpen={rightSidebarOpen}
        setIsOpen={setRightSidebarOpen}
        pinnedCard={pinnedCard}
        pinnedThread={pinnedThread}
        pinnedIsThinking={pinnedIsThinking}
        onSend={handlePinnedSend}
        onUnpin={() => handlePinToggle(null, [])}
        activeTab={activeTab}
      />

      <Suspense fallback={null}>
        <FeedbackModal userId={user?.id} userEmail={user?.email} />
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
 * Composition root. Providers wrap the view so that a future <MobileLayout>
 * can be selected here, consuming the exact same data layer.
 */
export default function Dashboard() {
  return (
    <DashboardDataProvider>
      <CourseDetailProvider>
        <DesktopDashboard />
      </CourseDetailProvider>
    </DashboardDataProvider>
  )
}
