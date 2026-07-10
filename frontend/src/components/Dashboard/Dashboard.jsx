import { useState, useEffect, useCallback, useRef, lazy, Suspense } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { coursesAPI } from '../../lib/api'
import favoritesAPI from '../../lib/favoritesAPI'
import completedCoursesAPI from '../../lib/completedCoursesAPI'
import currentCoursesAPI from '../../lib/currentCoursesAPI'
import { getCourseCredits as _getCourseCredits } from '../../utils/courseCredits'
import { normalizeQuery, buildCorrectionCandidates } from '../../utils/fuzzySearch'
import { useLanguage } from '../../contexts/PreferencesContext'
import cardsAPI from '../../lib/cardsAPI'
import AdvisorCards from './chat/AdvisorCards'
import HomeTab from './HomeTab'
import useUpcomingEvents from '../../hooks/useUpcomingEvents'
import RightSidebar from './RightSidebar'
import CoursesView from './CoursesView'

import Sidebar from './Sidebar'
import clubsAPI from '../../lib/clubsAPI'
import { readCache, writeCache, clearAllForUser } from '../../lib/userDataCache'

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

export default function Dashboard() {
  const { user, profile, signOut, updateProfile, refreshProfile, authFlags } = useAuth()
  const { t, language } = useLanguage()

  // Stable ref for current language — used inside useCallbacks without
  // adding `language` to their dependency arrays (which would cause
  // unnecessary re-creation and effect re-fires on every switch).
  const languageRef = useRef(language)
  useEffect(() => { languageRef.current = language }, [language])

  // ── Layout ─────────────────────────────────────────────
  const [activeTab, setActiveTab] = useState(() =>
    localStorage.getItem('symbolos_open_pw_change') ? 'profile' : 'home'
  )

  // Deep link into the Courses tab (e.g. Home → "View upcoming courses"
  // lands on My Courses → Current). Cleared when leaving the tab so a normal
  // visit gets the default view again.
  const [coursesDeepLink, setCoursesDeepLink] = useState(null)
  useEffect(() => {
    if (activeTab !== 'courses') setCoursesDeepLink(null)
  }, [activeTab])

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

  // ── Dynamic browser tab title ────────────────────────
  useEffect(() => {
    const tabNameKey = {
      home:      'nav.home',
      chat:      'nav.chat',
      favorites: 'nav.degreePlanning',
      courses:   'nav.courses',
      calendar:  'nav.calendar',
      clubs:     'nav.clubs',
      forum:     'nav.forum',
      profile:   'nav.profile',
    }[activeTab]
    document.title = tabNameKey ? `${t(tabNameKey)} — Symbolos` : 'Symbolos'
    return () => { document.title = 'Symbolos' }
  }, [activeTab, t])

  const tourKey = `symbolos_tour_done_${user?.id}`
  const [showTutorial, setShowTutorial] = useState(
    () => !!user?.id && !localStorage.getItem(`symbolos_tour_done_${user?.id}`)
  )
  // Keep sidebar expanded so data-tour targets are in the DOM during the walkthrough
  useEffect(() => {
    if (showTutorial) setSidebarOpen(true)
  }, [showTutorial])
  const [profileImage, setProfileImage] = useState(profile?.profile_image || null)
  const [isUploadingImage, setIsUploadingImage] = useState(false)
  const fileInputRef = useRef(null)

  // ── Right sidebar / pinned chat ─────────────────────────
  const [rightSidebarOpen, setRightSidebarOpen] = useState(false)
  const [pinnedCard, setPinnedCard] = useState(null)
  const [pinnedThread, setPinnedThread] = useState([])
  const [pinnedIsThinking, setPinnedIsThinking] = useState(false)

  // ── Transcript upload ──────────────────────────────────
  const [showTranscriptUpload, setShowTranscriptUpload] = useState(false)
  const [transcriptUploadTab, setTranscriptUploadTab] = useState('transcript')

  // Listen for `open-transcript-upload` custom event fired by reminder card chips
  useEffect(() => {
    const handler = () => {
      setTranscriptUploadTab('transcript')
      setShowTranscriptUpload(true)
    }
    window.addEventListener('open-transcript-upload', handler)
    return () => window.removeEventListener('open-transcript-upload', handler)
  }, [])

  // Listen for `open-degree-planning` custom event fired by the
  // course-registration reminder card chip — jumps the user to the
  // Degree Planning tab so they can plan next term.
  useEffect(() => {
    const handler = () => setActiveTab('favorites')   // 'favorites' tab = Degree Planning
    window.addEventListener('open-degree-planning', handler)
    return () => window.removeEventListener('open-degree-planning', handler)
  }, [])

  // ── Advisor cards ──────────────────────────────────────
  const [advisorCards, setAdvisorCards] = useState([])
  const [cardsLoading, setCardsLoading] = useState(false)
  const [cardsGenerating, setCardsGenerating] = useState(false)
  const [cardsGeneratedAt, setCardsGeneratedAt] = useState(null)
  const [freeformInput, setFreeformInput] = useState('')
  const [isAsking, setIsAsking] = useState(false)

  const isLoadingCardsRef    = useRef(false)
  const isGeneratingCardsRef = useRef(false)

  // ── Club calendar events ───────────────────────────────
  const [clubCalendarEvents, setClubCalendarEvents] = useState([])
  const [managedClubs, setManagedClubs] = useState([])

  // ── Course search ──────────────────────────────────────
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [isSearching, setIsSearching] = useState(false)
  const [searchError, setSearchError] = useState(null)
  const [searchCorrection, setSearchCorrection] = useState(null) // { original, corrected }
  const [hasSearched, setHasSearched] = useState(false)
  const [sortBy, setSortBy] = useState('relevance')
  const [searchTerm, setSearchTerm] = useState('')      // semester filter, '' = all
  const [availableTerms, setAvailableTerms] = useState([])

  // ── Favorites & completed ──────────────────────────────
  // SWR-style: hydrate user-data state from localStorage so the UI paints
  // instantly on every visit, then revalidate in the background.
  const _hydratedFavorites = readCache('favorites', user?.id, [])
  const _hydratedCompleted = readCache('completed', user?.id, [])
  const _hydratedCurrent   = readCache('current',   user?.id, [])

  const [favorites, setFavorites]                 = useState(_hydratedFavorites)
  const [favoritesMap, setFavoritesMap]           = useState(
    new Set((_hydratedFavorites || []).map(f => (f.course_code || '').replace(/^([A-Za-z]+)(\d)/, '$1 $2')))
  )
  const [completedCourses, setCompletedCourses]   = useState(_hydratedCompleted)
  const [completedCoursesMap, setCompletedCoursesMap] = useState(
    new Set((_hydratedCompleted || []).map(c => c.course_code))
  )
  const [currentCourses, setCurrentCourses]       = useState(_hydratedCurrent)
  const [currentCoursesMap, setCurrentCoursesMap] = useState(
    new Set((_hydratedCurrent || []).map(c => c.course_code))
  )

  // Computed once here (not inside HomeTab) because the Sidebar's Calendar
  // badge needs the same urgentCount — avoids a second fetch of the feed.
  const {
    events: upcomingEvents,
    loading: upcomingEventsLoading,
    urgentCount: upcomingUrgentCount,
    hasCourseEvents: hasUpcomingCourseEvents,
  } = useUpcomingEvents(user, currentCourses, { limit: 5 })

  // ── Mark Complete modal ────────────────────────────────
  const [showCompleteCourseModal, setShowCompleteCourseModal] = useState(false)
  const [courseToComplete, setCourseToComplete] = useState(null)

  // ── Utilities ──────────────────────────────────────────
  const gpaToLetterGrade = (gpa) => {
    if (!gpa) return ''
    const n = parseFloat(gpa)
    if (n >= 3.85) return 'A'
    if (n >= 3.7)  return 'A-'
    if (n >= 3.3)  return 'B+'
    if (n >= 3.0)  return 'B'
    if (n >= 2.7)  return 'B-'
    if (n >= 2.3)  return 'C+'
    if (n >= 2.0)  return 'C'
    if (n >= 1.0)  return 'D'
    return 'F'
  }

  const sortCourses = (courses, sortType) => {
    const sorted = [...courses]
    switch (sortType) {
      case 'rating-high':   return sorted.sort((a, b) => (b.rmp_rating || 0) - (a.rmp_rating || 0))
      case 'rating-low':    return sorted.sort((a, b) => (a.rmp_rating || 0) - (b.rmp_rating || 0))
      case 'name-az':       return sorted.sort((a, b) => `${a.subject} ${a.catalog}`.localeCompare(`${b.subject} ${b.catalog}`))
      case 'name-za':       return sorted.sort((a, b) => `${b.subject} ${b.catalog}`.localeCompare(`${a.subject} ${a.catalog}`))
      case 'instructor-az': return sorted.sort((a, b) => (a.instructor || 'ZZZ').localeCompare(b.instructor || 'ZZZ'))
      case 'instructor-za': return sorted.sort((a, b) => (b.instructor || '').localeCompare(a.instructor || ''))
      case 'number':        return sorted.sort((a, b) => (parseInt(a.catalog, 10) || 0) - (parseInt(b.catalog, 10) || 0))
      // Highest average grade with the semester's specific professor,
      // historically. Courses where we know that prof's history rank first
      // (by that average); the rest fall to the bottom, ordered by the
      // course's own recent average.
      case 'grade-high':    return sorted.sort((a, b) => {
                                    const av = a.prof_historical_avg, bv = b.prof_historical_avg
                                    if (av != null && bv != null) return bv - av
                                    if (av != null) return -1
                                    if (bv != null) return 1
                                    return (b.average ?? -1) - (a.average ?? -1)
                                  })
      default: return sorted
    }
  }

  // FIX: all three maps use the same key format: "SUBJECT CATALOG" (with space)
  const isFavorited = (subject, catalog) => favoritesMap.has(`${subject} ${catalog}`)
  const isCompleted = (subject, catalog) => completedCoursesMap.has(`${subject} ${catalog}`)
  const isCurrent   = (subject, catalog) => currentCoursesMap.has(`${subject} ${catalog}`)

  // ── Advisor card handlers ──────────────────────────────

  // ── Helpers: localStorage card cache (per-language) ────────────
  const _cacheCards = useCallback((cards, generatedAt, lang = null) => {
    if (!user?.id) return
    const usedLang = lang || languageRef.current || 'en'
    try {
      localStorage.setItem(`advisor_cards_${user.id}_${usedLang}`, JSON.stringify({ cards, generatedAt, ts: Date.now() }))
    } catch { /* quota exceeded — ignore */ }
  }, [user?.id])

  const _getCachedCards = useCallback((lang = null) => {
    if (!user?.id) return null
    const usedLang = lang || languageRef.current || 'en'
    try {
      const raw = localStorage.getItem(`advisor_cards_${user.id}_${usedLang}`)
      if (raw) {
        const parsed = JSON.parse(raw)
        // Cache valid for 6 hours
        if (Date.now() - parsed.ts < 6 * 3600000) return parsed
      }
      return null
    } catch { return null }
  }, [user?.id])

  // Rate limit: 2 manual card refreshes per week (admins unlimited)
  const _cardsRateLimited = useCallback(() => {
    if (authFlags?.is_admin) return false
    const key = 'cards_refresh_timestamps'
    const now = Date.now()
    const weekAgo = now - 7 * 24 * 60 * 60 * 1000
    try {
      const stamps = JSON.parse(localStorage.getItem(key) || '[]').filter(t => t > weekAgo)
      if (stamps.length >= 2) return true
      stamps.push(now)
      localStorage.setItem(key, JSON.stringify(stamps))
      return false
    } catch { return false }
  }, [authFlags?.is_admin])

  const refreshAdvisorCards = useCallback(async (force = true, lang = null, skipRateLimit = false) => {
    if (!user?.id) return
    if (isGeneratingCardsRef.current) return
    // Rate limit manual refreshes (force=true means user clicked refresh)
    if (force && !skipRateLimit && _cardsRateLimited()) {
      alert('You can refresh your academic brief up to 2 times per week. Try again later!')
      return
    }
    isGeneratingCardsRef.current = true
    setCardsGenerating(true)
    // Clear existing AI cards so the skeleton/stream-in feels fresh
    setAdvisorCards(prev => prev.filter(c => c.source !== 'ai'))

    const usedLang = lang || languageRef.current
    let streamIdx = 0

    try {
      await cardsAPI.generateCardsStream(user.id, force, usedLang, {
        onCard: (card) => {
          const idx = streamIdx++
          // Tag with _streamIdx so we can identify un-persisted stream cards in prev
          const tagged = { ...card, _streamIdx: idx }
          setAdvisorCards(prev => {
            // Keep user-sourced cards + already-streamed cards (tagged), then append new one
            const base = prev.filter(c => c.source === 'user' || c._streamIdx !== undefined)
            return [...base, tagged]
          })
        },
        onDone: (event) => {
          const confirmedLang = event.language
          if (confirmedLang) {
            // Fetch persisted cards from server to replace tagged stream cards with real DB rows
            cardsAPI.getCards(user.id).then(data => {
              const cards = data.cards || []
              setAdvisorCards(cards)
              setCardsGeneratedAt(data.generated_at || null)
              _cacheCards(cards, data.generated_at, confirmedLang)
              try { localStorage.setItem(`cards_language_${user.id}`, confirmedLang) } catch { /* ignore */ }
            }).catch(() => {})
          }
        },
        onError: (detail) => {
          console.error('Card stream error:', detail)
        },
      })
    } catch (error) {
      console.error('Error generating advisor cards:', error)
    } finally {
      setCardsGenerating(false)
      isGeneratingCardsRef.current = false
    }
  }, [user?.id, _cacheCards, _cardsRateLimited])

  const loadAdvisorCards = useCallback(async () => {
    if (!user?.id) return
    if (isLoadingCardsRef.current) return
    isLoadingCardsRef.current = true
    try {
      // SWR pattern: if cache is hit, paint instantly and DO NOT show the
      // loading spinner — that was making cached visits feel slow because
      // the UI flashed loading state even though cards were already there.
      const cached = _getCachedCards()
      const cacheHit = cached && cached.cards?.length > 0

      if (cacheHit) {
        setAdvisorCards(cached.cards)
        setCardsGeneratedAt(cached.generatedAt || null)
        // Skip the background revalidate entirely if cache is fresh
        // (< 5 min). The user can hit Refresh to force a regenerate.
        const ageMs = cached.ts ? Date.now() - cached.ts : Infinity
        if (ageMs < 5 * 60 * 1000) {
          isLoadingCardsRef.current = false
          return
        }
      } else {
        // No cache → only NOW show the loading state
        setCardsLoading(true)
      }

      // Background revalidate (cache miss OR cache stale)
      const data = await cardsAPI.getCards(user.id)
      const cards = data.cards || []
      const currentLang = languageRef.current

      // serverLang comes directly from the backend (stored in Supabase user metadata).
      // This is always accurate — no localStorage guessing needed.
      const serverLang = data.cards_language ?? null

      const aiCards = cards.filter(c => c.source === 'ai')
      // Retranslate if: we have AI cards AND (server lang unknown OR doesn't match UI lang)
      const needsRetranslation = aiCards.length > 0 && serverLang !== currentLang

      if (needsRetranslation && !isGeneratingCardsRef.current) {
        // Cache server cards under their known language for cheap future switching
        if (serverLang) _cacheCards(cards, data.generated_at, serverLang)

        // Check if we have a cached translation for the current language
        const cachedTranslation = _getCachedCards(currentLang)
        if (cachedTranslation?.cards?.length) {
          setAdvisorCards(cachedTranslation.cards)
          setCardsGeneratedAt(cachedTranslation.generatedAt || null)
        } else {
          setAdvisorCards([])
          try {
            const retranslated = await cardsAPI.retranslateCards(user.id, currentLang)
            if (retranslated?.cards?.length) {
              setAdvisorCards(retranslated.cards)
              _cacheCards(retranslated.cards, retranslated.generated_at, currentLang)
              // retranslated.cards_language is confirmed by backend
              try { localStorage.setItem(`cards_language_${user.id}`, retranslated.cards_language || currentLang) } catch { /* ignore */ }
            } else {
              await refreshAdvisorCards(true, currentLang, true)
            }
          } catch (err) {
            console.error('Retranslation failed, trying full regeneration:', err)
            try {
              await refreshAdvisorCards(true, currentLang, true)
            } catch {
              setAdvisorCards(cards)
            }
          }
        }
      } else if (cards.length > 0) {
        // Server cards match current language — display and cache them.
        // If the cached set already matches by id, skip setAdvisorCards to
        // avoid a re-render that replays the entry-slide animation.
        const sameAsCached = cacheHit
          && cached.cards.length === cards.length
          && cached.cards.every((c, i) => c.id === cards[i]?.id)
        if (!sameAsCached) {
          setAdvisorCards(cards)
          setCardsGeneratedAt(data.generated_at || null)
        }
        if (serverLang) {
          _cacheCards(cards, data.generated_at, serverLang)
          try { localStorage.setItem(`cards_language_${user.id}`, serverLang) } catch { /* ignore */ }
        }
      } else if (!isGeneratingCardsRef.current) {
        await refreshAdvisorCards(false)
      }
    } catch (error) {
      console.error('Error loading advisor cards:', error)
    } finally {
      setCardsLoading(false)
      isLoadingCardsRef.current = false
    }
  }, [user?.id, refreshAdvisorCards, _getCachedCards, _cacheCards])

  const handleCardChipClick = async (cardId, message, cardTitle, cardBody) => {
    if (!user?.id) return ''
    try {
      return await cardsAPI.sendThreadMessage(cardId, user.id, message, `${cardTitle}: ${cardBody}`, languageRef.current)
    } catch (error) {
      console.error('Error in card thread:', error)
      return 'Something went wrong. Please try again.'
    }
  }

  const handleCardSaveToggle = async (cardId, isSaved) => {
    if (!user?.id) return
    try {
      const updated = await cardsAPI.saveCard(cardId, isSaved)
      setAdvisorCards(prev =>
        prev.map(c => c.id === cardId ? { ...c, is_saved: updated.is_saved } : c)
      )
    } catch (error) {
      console.error('Error toggling card save:', error)
    }
  }

  const handleCardsReorder = async (order) => {
    if (!user?.id) return
    try {
      await cardsAPI.reorderCards(user.id, order)
      setAdvisorCards(prev => {
        const orderMap = Object.fromEntries(order.map(o => [o.id, o.sort_order]))
        return [...prev]
          .map(c => orderMap[c.id] !== undefined ? { ...c, sort_order: orderMap[c.id] } : c)
          .sort((a, b) => (a.sort_order ?? 0) - (b.sort_order ?? 0))
      })
    } catch (error) {
      console.error('Error reordering cards:', error)
    }
  }

  const handleFreeformSubmit = async (e) => {
    e.preventDefault()
    if (!freeformInput.trim() || isAsking || !user?.id) return
    const question = freeformInput.trim()
    setFreeformInput('')
    setIsAsking(true)
    try {
      const data = await cardsAPI.askCard(user.id, question, languageRef.current)
      if (data.card) {
        setAdvisorCards(prev => [data.card, ...prev])
      }
    } catch (error) {
      console.error('Error asking card:', error)
    } finally {
      setIsAsking(false)
    }
  }

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

  // ── Fetch managed clubs (for calendar event/announcement creation) ──
  useEffect(() => {
    if (!user?.id) return
    async function load() {
      try {
        if (authFlags?.is_admin) {
          const res = await clubsAPI.getClubs({ limit: 200 })
          setManagedClubs(res.clubs || [])
        } else {
          const res = await clubsAPI.getCreatedClubs(user.id)
          setManagedClubs(res.clubs || [])
        }
      } catch { setManagedClubs([]) }
    }
    load()
  }, [user?.id, authFlags?.is_admin])

  // ── Language switch: retranslate cards (no full regeneration) ────
  // On mount: loadAdvisorCards already handles language mismatch.
  // On actual switch: retranslate existing cards, don't burn a generation.
  const prevLanguageRef = useRef(null)
  useEffect(() => {
    const isMount = prevLanguageRef.current === null
    const switched = !isMount && prevLanguageRef.current !== language
    prevLanguageRef.current = language

    if (isMount || !switched || !user?.id) return

    // Check if we have a cached translation for the new language
    const cached = _getCachedCards(language)
    if (cached?.cards?.length) {
      // Instant switch from cache — no API call, no tokens burned
      setAdvisorCards(cached.cards)
      setCardsGeneratedAt(cached.generatedAt || null)
      // DON'T update cards_language_ here — server still has the old language.
      // cards_language_ must only reflect what the server actually stores.
      return
    }

    // No cache for this language — call API to retranslate (costs tokens once)
    // Only update cards_language AFTER successful retranslation
    setCardsGenerating(true)
    cardsAPI.retranslateCards(user.id, language).then(data => {
      if (data?.cards?.length) {
        setAdvisorCards(data.cards)
        setCardsGeneratedAt(data.generated_at || null)
        const confirmedLang = data.cards_language || language
        _cacheCards(data.cards, data.generated_at, confirmedLang)
        try { localStorage.setItem(`cards_language_${user.id}`, confirmedLang) } catch { /* ignore */ }
      } else {
        // Empty response — fall back to full regeneration (force=true to bypass "fresh" check)
        return refreshAdvisorCards(true, language, true)
      }
    }).catch(() => {
      // Retranslation failed — fall back to full regeneration
      return refreshAdvisorCards(true, language, true).catch(() => {})
    }).finally(() => {
      setCardsGenerating(false)
    })
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [language])

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

  // ── Data loaders ───────────────────────────────────────
  // Each loader updates state AND writes to the userDataCache so subsequent
  // visits paint from cache before the network call returns.
  const loadFavorites = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await favoritesAPI.getFavorites(user.id)
      const list = data.favorites || []
      setFavorites(list)
      // FIX: normalize stored course_code to "SUBJ CAT" format for consistent lookup
      setFavoritesMap(new Set(list.map(f => {
        const code = f.course_code || ''
        // If stored without space (e.g. "COMP202"), insert it
        return code.replace(/^([A-Za-z]+)(\d)/, '$1 $2')
      })))
      writeCache('favorites', user.id, list)
    } catch (error) {
      console.error('Error loading favorites:', error)
    }
  }, [user?.id])

  const loadCompletedCourses = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await completedCoursesAPI.getCompleted(user.id)
      const list = data.completed_courses || []
      setCompletedCourses(list)
      setCompletedCoursesMap(new Set(list.map(c => c.course_code)))
      writeCache('completed', user.id, list)
    } catch (error) {
      console.error('Error loading completed courses:', error)
      setCompletedCourses([])
      setCompletedCoursesMap(new Set())
    }
  }, [user?.id])

  const loadCurrentCourses = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await currentCoursesAPI.getCurrent(user.id)
      const list = data.current_courses || []
      setCurrentCourses(list)
      setCurrentCoursesMap(new Set(list.map(c => c.course_code)))
      writeCache('current', user.id, list)
    } catch (error) {
      console.error('Error loading current courses:', error)
      setCurrentCourses([])
      setCurrentCoursesMap(new Set())
    }
  }, [user?.id])

  // ── Tab change ─────────────────────────────────────────
  const handleTabChange = (tab) => {
    setActiveTab(tab)
    setSearchResults([])
    setSearchError(null)
    setSearchCorrection(null)
    setHasSearched(false)
    if (window.innerWidth < 768) setSidebarOpen(false)
  }

  // ── Course search ──────────────────────────────────────
  const handleCourseSearch = async (e, overrideQuery) => {
    if (e?.preventDefault) e.preventDefault()
    const rawQuery = overrideQuery || searchQuery
    if (!rawQuery.trim() || isSearching) return
    setIsSearching(true)
    setSearchError(null)
    setSearchCorrection(null)
    setHasSearched(true)
    try {
      const normalized = normalizeQuery(rawQuery)

      // If normalized looks like "COMP 202", split into subject + catalog params
      // so the RPC receives them separately instead of as a full-text query
      const codeMatch = normalized.match(/^([A-Z]{2,6})\s+(\d{3}[A-Z]?)$/)
      let searchSubject = null
      let searchQuery   = normalized
      if (codeMatch) {
        searchSubject = codeMatch[1]
        searchQuery   = codeMatch[2]
      }

      const data = await coursesAPI.search(searchQuery, searchSubject, 50, searchTerm || null)
      let courses = data.courses || data || []
      if (!Array.isArray(courses)) courses = []

      // Zero results — try fuzzy correction
      if (courses.length === 0) {
        const candidates = buildCorrectionCandidates(rawQuery)
        for (const candidate of candidates) {
          const corrCode = candidate.query.match(/^([A-Z]{2,6})\s+(\d{3}[A-Z]?)$/)
          const retrySub = corrCode ? corrCode[1] : null
          const retryQ   = corrCode ? corrCode[2] : candidate.query
          const retry = await coursesAPI.search(retryQ, retrySub, 50, searchTerm || null)
          const retryList = retry.courses || retry || []
          if (Array.isArray(retryList) && retryList.length > 0) {
            setSearchCorrection({ original: rawQuery, corrected: candidate.note })
            setSearchResults(retryList)
            return
          }
        }
      }

      setSearchResults(courses)
      if (courses.length === 0) setSearchError(null) // CoursesTab shows its own empty state
    } catch (error) {
      console.error('Error searching courses:', error)
      setSearchError('Failed to search courses. Please try again.')
      setSearchResults([])
    } finally {
      setIsSearching(false)
    }
  }

  // Load the list of semesters we have section data for (for the filter).
  useEffect(() => {
    coursesAPI.getTerms().then(d => setAvailableTerms(d?.terms || [])).catch(() => {})
  }, [])

  // Re-run the current search whenever the semester filter changes.
  useEffect(() => {
    if (hasSearched && searchQuery.trim()) handleCourseSearch()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchTerm])

  // ── Toggle favorite ────────────────────────────────────
  const handleToggleFavorite = async (course) => {
    if (!user?.id) return
    // FIX: use space-separated key to match isFavorited and favoritesMap
    const courseCode = `${course.subject} ${course.catalog}`
    const isFav = favoritesMap.has(courseCode)
    try {
      if (isFav) {
        await favoritesAPI.removeFavorite(user.id, courseCode)
        setFavorites(prev => prev.filter(f => f.course_code !== courseCode))
        setFavoritesMap(prev => { const s = new Set(prev); s.delete(courseCode); return s })
      } else {
        await favoritesAPI.addFavorite(user.id, {
          course_code: courseCode,
          course_title: course.title,
          subject: course.subject,
          catalog: course.catalog,
        })
        setFavorites(prev => [
          { course_code: courseCode, course_title: course.title, subject: course.subject, catalog: course.catalog },
          ...prev,
        ])
        setFavoritesMap(prev => new Set([...prev, courseCode]))
      }
    } catch (error) {
      console.error('Error toggling favorite:', error)
      alert(error.message || 'Failed to update favorites')
    }
  }

  // ── Toggle completed ───────────────────────────────────
  const handleToggleCompleted = async (course) => {
    if (!user?.id) return
    const courseCode = `${course.subject} ${course.catalog}`
    const isComp = completedCoursesMap.has(courseCode)
    try {
      if (isComp) {
        await completedCoursesAPI.removeCompleted(user.id, courseCode)
        setCompletedCourses(prev => prev.filter(c => c.course_code !== courseCode))
        setCompletedCoursesMap(prev => { const s = new Set(prev); s.delete(courseCode); return s })
      } else {
        setCourseToComplete(course)
        setShowCompleteCourseModal(true)
      }
    } catch (error) {
      console.error('Error toggling completed course:', error)
      alert(error.message || 'Failed to update completed courses')
    }
  }

  const handleConfirmComplete = async (courseData) => {
    if (!user?.id) return
    try {
      await completedCoursesAPI.addCompleted(user.id, courseData)
      setCompletedCourses(prev => [courseData, ...prev])
      setCompletedCoursesMap(prev => new Set([...prev, courseData.course_code]))

      // Auto-remove from current if enrolled
      if (currentCoursesMap.has(courseData.course_code)) {
        try {
          await currentCoursesAPI.removeCurrent(user.id, courseData.course_code)
          setCurrentCourses(prev => prev.filter(c => c.course_code !== courseData.course_code))
          setCurrentCoursesMap(prev => { const s = new Set(prev); s.delete(courseData.course_code); return s })
        } catch (e) {
          console.warn('Could not auto-remove from current:', e)
        }
      }
    } catch (error) {
      console.error('Error adding completed course:', error)
      alert(error.message || 'Failed to add completed course')
    } finally {
      setShowCompleteCourseModal(false)
      setCourseToComplete(null)
    }
  }

  // ── Toggle current ─────────────────────────────────────
  const handleToggleCurrent = async (course) => {
    if (!user?.id) return
    const courseCode = `${course.subject} ${course.catalog}`
    const enrolled = currentCoursesMap.has(courseCode)
    try {
      if (enrolled) {
        await currentCoursesAPI.removeCurrent(user.id, courseCode)
        setCurrentCourses(prev => prev.filter(c => c.course_code !== courseCode))
        setCurrentCoursesMap(prev => { const s = new Set(prev); s.delete(courseCode); return s })
      } else {
        const courseData = {
          course_code: courseCode,
          course_title: course.title || course.course_title || '',
          subject: course.subject,
          catalog: course.catalog,
          credits: course.credits || 3,
        }
        await currentCoursesAPI.addCurrent(user.id, courseData)
        setCurrentCourses(prev => [courseData, ...prev])
        setCurrentCoursesMap(prev => new Set([...prev, courseCode]))

        // Auto-remove from completed if previously marked done
        if (completedCoursesMap.has(courseCode)) {
          try {
            await completedCoursesAPI.removeCompleted(user.id, courseCode)
            setCompletedCourses(prev => prev.filter(c => c.course_code !== courseCode))
            setCompletedCoursesMap(prev => { const s = new Set(prev); s.delete(courseCode); return s })
          } catch (e) {
            console.warn('Could not auto-remove from completed:', e)
          }
        }
      }
    } catch (error) {
      console.error('Error toggling current course:', error)
      alert(error.message || 'Failed to update current courses')
    }
  }

  // ── Sign out ───────────────────────────────────────────
  const handleSignOut = async () => {
    try {
      // Clear cached user data so the next user doesn't see this user's info
      if (user?.id) clearAllForUser(user.id)
      await signOut()
    }
    catch (error) { console.error('Error signing out:', error) }
  }

  // ── Profile image ──────────────────────────────────────
  const handleAvatarClick = () => fileInputRef.current?.click()

  const handleImageUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    if (!file.type.startsWith('image/')) { alert('Please select an image file'); return }
    if (file.size > 5 * 1024 * 1024) { alert('Image size must be less than 5MB'); return }
    setIsUploadingImage(true)
    try {
      const reader = new FileReader()
      reader.onloadend = async () => {
        await updateProfile({ profile_image: reader.result })
        setProfileImage(reader.result)
      }
      reader.readAsDataURL(file)
    } catch (error) {
      console.error('Error uploading image:', error)
      alert('Failed to upload image. Please try again.')
    } finally {
      setIsUploadingImage(false)
    }
  }

  // ── Transcript import complete ─────────────────────────
  const handleTranscriptImportComplete = () => {
    setShowTranscriptUpload(false)
    loadCompletedCourses()
    loadCurrentCourses()
    refreshProfile()
    refreshAdvisorCards(true, null, true) // skip rate limit after transcript import
  }

  // ── Effects ────────────────────────────────────────────
  useEffect(() => {
    if (user?.id) {
      loadFavorites()
      loadCompletedCourses()
      loadCurrentCourses()
      loadAdvisorCards()
    }
  }, [user?.id, loadFavorites, loadCompletedCourses, loadCurrentCourses, loadAdvisorCards])

  useEffect(() => {
    setProfileImage(profile?.profile_image || null)
  }, [profile?.profile_image])

  // ── Render ─────────────────────────────────────────────
  return (
    <CourseDetailProvider>
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
              currentCourses={currentCourses}
              completedCourses={completedCourses}
              events={upcomingEvents}
              eventsLoading={upcomingEventsLoading}
              hasCourseEvents={hasUpcomingCourseEvents}
              onTabChange={handleTabChange}
              onViewCurrentCourses={() => {
                setCoursesDeepLink({ subTab: 'my_courses', savedTab: 'current' })
                handleTabChange('courses')
              }}
              onImportTranscript={() => { setTranscriptUploadTab('transcript'); setShowTranscriptUpload(true) }}
              onImportSyllabus={() => { setTranscriptUploadTab('syllabus'); setShowTranscriptUpload(true) }}
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
              onDeleteCard={async (cardId) => {
                setAdvisorCards(prev => prev.filter(c => c.id !== cardId))
                try { await cardsAPI.deleteCard(user.id, cardId) } catch (e) {
                  console.warn('Failed to delete card from DB:', e)
                }
              }}
              freeformInput={freeformInput}
              setFreeformInput={setFreeformInput}
              onFreeformSubmit={handleFreeformSubmit}
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
                onImportTranscript={() => { setTranscriptUploadTab('transcript'); setShowTranscriptUpload(true) }}
                onImportSyllabus={() => { setTranscriptUploadTab('syllabus'); setShowTranscriptUpload(true) }}
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
                onImportTranscript={() => { setTranscriptUploadTab('transcript'); setShowTranscriptUpload(true) }}
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
            onCancel={() => {
              setShowCompleteCourseModal(false)
              setCourseToComplete(null)
            }}
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
    </CourseDetailProvider>
  )
}
