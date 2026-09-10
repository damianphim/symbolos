import { saveCourseCompletion } from '../lib/saveCourseCompletion'
/* eslint-disable react-refresh/only-export-components */
/**
 * DashboardDataContext
 *
 * Everything the dashboard *knows* and *does*, with none of how it looks.
 *
 * This was extracted verbatim out of Dashboard.jsx, which had grown into a
 * single component owning the data layer, the business logic AND the desktop
 * layout. The mobile shell needs the first two without the third, so they now
 * live here and Dashboard.jsx is purely the desktop view.
 *
 * What belongs here: user data (courses/favorites/cards), the loaders and
 * mutation handlers, course search, and cross-shell navigation intent
 * (activeTab + deep links).
 *
 * What does NOT belong here: anything only one shell has — the desktop
 * sidebar, the pinned-card right sidebar, the desktop onboarding tour.
 */
import {
  createContext, useContext, useState, useEffect, useCallback, useRef, useMemo,
} from 'react'
import { useAuth } from './AuthContext'
import { useLanguage } from './PreferencesContext'
import { coursesAPI, usersAPI } from '../lib/api'
import favoritesAPI from '../lib/favoritesAPI'
import completedCoursesAPI from '../lib/completedCoursesAPI'
import currentCoursesAPI from '../lib/currentCoursesAPI'
import cardsAPI from '../lib/cardsAPI'
import { PENDING_CARD_PREFIX, isPendingCardId } from '../lib/pendingCard'
import clubsAPI from '../lib/clubsAPI'
import { getCreditsRequired } from '../utils/mcgillData'
import { normalizeQuery, buildCorrectionCandidates } from '../utils/fuzzySearch'
import useUpcomingEvents from '../hooks/useUpcomingEvents'
import { readCache, writeCache, clearAllForUser } from '../lib/userDataCache'

const DashboardDataContext = createContext(null)

export function useDashboardData() {
  const ctx = useContext(DashboardDataContext)
  if (!ctx) throw new Error('useDashboardData must be used within a DashboardDataProvider')
  return ctx
}

export function DashboardDataProvider({ children }) {
  const { user, profile, signOut, updateProfile, refreshProfile, authFlags } = useAuth()
  const { t, language } = useLanguage()

  // Stable ref for current language — used inside useCallbacks without
  // adding `language` to their dependency arrays (which would cause
  // unnecessary re-creation and effect re-fires on every switch).
  const languageRef = useRef(language)
  useEffect(() => { languageRef.current = language }, [language])

  // ── Navigation ─────────────────────────────────────────
  // activeTab lives here rather than in a shell because both the desktop
  // sidebar and the mobile tab bar drive it, and deep links target it.
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

  // Deep link into the Brief: open a specific advisor card's chat (from Home).
  const [briefOpenCardId, setBriefOpenCardId] = useState(null)

  // Deep-link intents are exposed as setters rather than as ready-made
  // navigation helpers, because each shell composes them with its *own*
  // tab-change handler (the desktop one additionally collapses the sidebar).
  // Building them here would silently skip that side effect.

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
    document.title = tabNameKey ? `${t(tabNameKey)} · Symbolos` : 'Symbolos'
    return () => { document.title = 'Symbolos' }
  }, [activeTab, t])

  // ── Profile image ──────────────────────────────────────
  const [profileImage, setProfileImage] = useState(profile?.profile_image || null)
  const [isUploadingImage, setIsUploadingImage] = useState(false)
  const fileInputRef = useRef(null)

  // ── Transcript upload ──────────────────────────────────
  const [showTranscriptUpload, setShowTranscriptUpload] = useState(false)
  const [transcriptUploadTab, setTranscriptUploadTab] = useState('transcript')

  const openTranscriptUpload = useCallback(() => {
    setTranscriptUploadTab('transcript')
    setShowTranscriptUpload(true)
  }, [])
  const openSyllabusUpload = useCallback(() => {
    setTranscriptUploadTab('syllabus')
    setShowTranscriptUpload(true)
  }, [])

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

  // ── Tab change ─────────────────────────────────────────
  // Declared after the search state it resets: these setters are stable, but
  // referencing them above their useState calls trips react-hooks/immutability.
  // Shells may wrap this to add their own side effects (the desktop shell
  // closes its sidebar on narrow viewports).
  const handleTabChange = useCallback((tab) => {
    setActiveTab(tab)
    setSearchResults([])
    setSearchError(null)
    setSearchCorrection(null)
    setHasSearched(false)
  }, [])

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
  const completedCoursesMap = useMemo(() => new Set(completedCourses.map(c =>
    (c.course_code || `${c.subject} ${c.catalog}`).trim().toUpperCase().replace(/^([A-Z]+)(\d)/, '$1 $2')
  )), [completedCourses])
  const [currentCourses, setCurrentCourses]       = useState(_hydratedCurrent)
  const [currentCoursesMap, setCurrentCoursesMap] = useState(
    new Set((_hydratedCurrent || []).map(c => c.course_code))
  )

  // Self-reported degree-progress summary attached to chat/card requests so
  // the AI is grounded in actual requirement progress instead of just the
  // raw course list. A ref, not state: write-often/read-at-send-time,
  // doesn't need to trigger re-renders. Populated from two sources of
  // increasing detail: (1) the baseline total-credit effect below, which
  // runs as soon as profile/courses are loaded — always available; (2) if
  // the student visits Degree Planning this session, DegreePlanningView's
  // onProgressSummaryChange overwrites it with the fuller per-requirement-
  // block breakdown (same numbers it renders — see requirementMatch.js).
  const degreeProgressRef = useRef('')

  // Baseline total-credit progress, always available (no network fetch —
  // mirrors the same arithmetic DegreeProgressTracker shows on Home), so the
  // AI has SOME degree-progress signal even if the student never opens
  // Degree Planning this session. Skipped while Degree Planning ("favorites"
  // tab) is actually mounted — its onProgressSummaryChange callback is the
  // richer, per-requirement-block source of truth then, and since child
  // effects fire before parent effects in the same commit, running this
  // unconditionally could clobber that richer value with the coarser total.
  useEffect(() => {
    if (!profile || activeTab === 'favorites') return
    const completedCredits = completedCourses.reduce((sum, c) => sum + (c.credits || 3), 0)
    const advancedStandingCredits = (profile.advanced_standing || []).reduce(
      (sum, c) => (c.counts_toward_degree === false ? sum : sum + (c.credits || 0)), 0
    )
    const earned = completedCredits + advancedStandingCredits
    const total = getCreditsRequired(profile.faculty, profile.major, profile.is_honours)
    const pct = Math.min(100, Math.round((earned / total) * 100))
    degreeProgressRef.current = `Overall degree: ${pct}% complete (${earned}/${total} credits)`
  }, [profile, completedCourses, activeTab])

  // Computed here (not inside HomeTab) because the Sidebar's Calendar
  // badge needs the same urgentCount — avoids a second fetch of the feed.
  const {
    events: upcomingEvents,
    loading: upcomingEventsLoading,
    urgentCount: upcomingUrgentCount,
    hasCourseEvents: hasUpcomingCourseEvents,
    markUrgentSeen,
  } = useUpcomingEvents(user, currentCourses, { limit: 5 })

  // Opening Calendar dismisses the sidebar badge for whatever's currently
  // urgent — a new event entering the urgent window later still counts.
  useEffect(() => {
    if (activeTab === 'calendar') markUrgentSeen()
  }, [activeTab, markUrgentSeen])

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
      }, degreeProgressRef.current)
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

  // `threadHistory` is the thread up to but excluding `message` — callers own
  // the message list, so they pass it in rather than us re-deriving it. Without
  // it the follow-up loses all conversational context (see sendThreadMessage).
  const handleCardChipClick = useCallback(async (cardId, message, cardTitle, cardBody, threadHistory = null) => {
    if (!user?.id) return ''
    try {
      return await cardsAPI.sendThreadMessage(cardId, user.id, message, `${cardTitle}: ${cardBody}`, languageRef.current, degreeProgressRef.current, threadHistory)
    } catch (error) {
      console.error('Error in card thread:', error)
      return 'Something went wrong. Please try again.'
    }
  }, [user?.id])

  const handleCardSaveToggle = async (cardId, isSaved) => {
    // A placeholder card isn't in the database yet — saving it would 404.
    if (!user?.id || isPendingCardId(cardId)) return
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
    // Drop placeholders from the payload; the server has no row to reorder.
    order = (order || []).filter(o => !isPendingCardId(o?.id))
    if (!order.length) return
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

  const handleDeleteCard = async (cardId) => {
    setAdvisorCards(prev => prev.filter(c => c.id !== cardId))
    // Nothing to delete server-side for a placeholder — dropping it locally is
    // the whole operation.
    if (isPendingCardId(cardId)) return
    try { await cardsAPI.deleteCard(user.id, cardId) } catch (e) {
      console.warn('Failed to delete card from DB:', e)
    }
  }

  const handleFreeformSubmit = async (e) => {
    e.preventDefault()
    if (!freeformInput.trim() || isAsking || !user?.id) return
    const question = freeformInput.trim()
    setFreeformInput('')
    setIsAsking(true)

    // Show the question and open its chat immediately rather than after the
    // model replies. Asking used to clear the input and then sit silently for
    // several seconds before a collapsed card appeared at the top of the feed —
    // the student had no confirmation their question had registered, and what
    // they typed was on screen nowhere.
    //
    // The placeholder carries PENDING_CARD_PREFIX in its id; anything that
    // would call the API with a card id refuses to act on one (see
    // isPendingCardId) because that id does not exist server-side yet.
    const pendingId = `${PENDING_CARD_PREFIX}${Date.now()}`
    const pendingCard = {
      id: pendingId,
      source: 'user',
      card_type: 'insight',
      label: 'YOUR QUESTION',
      title: question,
      user_question: question,
      body: '',
      actions: [],
      category: 'other',
      is_saved: false,
      _pending: true,
    }
    setAdvisorCards(prev => [pendingCard, ...prev])
    setBriefOpenCardId(pendingId)

    try {
      const data = await cardsAPI.askCard(user.id, question, languageRef.current)
      if (data.card) {
        // Swap in the real card and keep the chat open on it — the id changes,
        // so the open-card pointer has to follow or the view would close.
        // _replacedPendingId lets the open views resolve through the swap in a
        // single render. Without it the id changes underneath them, the card
        // they are keyed to vanishes for one commit, and the mobile thread
        // unmounts and replays its slide-in animation mid-answer.
        setAdvisorCards(prev => prev.map(
          c => (c.id === pendingId ? { ...data.card, _replacedPendingId: pendingId } : c)
        ))
        setBriefOpenCardId(data.card.id)
      } else {
        setAdvisorCards(prev => prev.filter(c => c.id !== pendingId))
        setBriefOpenCardId(null)
      }
    } catch (error) {
      console.error('Error asking card:', error)
      // Roll the placeholder back and hand the student their text back rather
      // than losing it to a failed request.
      setAdvisorCards(prev => prev.filter(c => c.id !== pendingId))
      setBriefOpenCardId(null)
      setFreeformInput(question)
    } finally {
      setIsAsking(false)
    }
  }

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
      writeCache('completed', user.id, list)
    } catch (error) {
      console.error('Error loading completed courses:', error)
      setCompletedCourses([])
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
      let searchQueryValue = normalized
      if (codeMatch) {
        searchSubject = codeMatch[1]
        searchQueryValue = codeMatch[2]
      }

      const data = await coursesAPI.search(searchQueryValue, searchSubject, 50, searchTerm || null)
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

  // Apply immediately and prevent overlapping writes for the same course.
  const favoriteWrites = useRef(new Set())
  const handleToggleFavorite = async (course) => {
    if (!user?.id) return
    const courseCode = `${course.subject} ${course.catalog}`
    if (favoriteWrites.current.has(courseCode)) return
    favoriteWrites.current.add(courseCode)
    const previous = favorites.find(f => f.course_code === courseCode)
    const isFav = favoritesMap.has(courseCode)
    const item = { course_code: courseCode, course_title: course.title || course.course_title,
      subject: course.subject, catalog: course.catalog }
    const apply = (saved, row) => {
      setFavorites(prev => saved ? [row, ...prev.filter(f => f.course_code !== courseCode)] : prev.filter(f => f.course_code !== courseCode))
      setFavoritesMap(prev => { const next = new Set(prev); if (saved) next.add(courseCode); else next.delete(courseCode); return next })
    }
    apply(!isFav, item)
    try {
      if (isFav) await favoritesAPI.removeFavorite(user.id, courseCode)
      else await favoritesAPI.addFavorite(user.id, item)
    } catch (error) {
      apply(isFav, previous || item)
      alert(error.message || t('courses.saveFailed'))
    } finally {
      favoriteWrites.current.delete(courseCode)
    }
  }

  // ── Toggle completed ───────────────────────────────────
  const handleToggleCompleted = async (course) => {
    if (!user?.id) return
    const courseCode = `${course.subject} ${course.catalog}`
    const isComp = completedCoursesMap.has(courseCode)
    try {
      if (isComp) {
        const existing = completedCourses.find(c => c.course_code === courseCode)
        setCourseToComplete({ ...course, ...existing, course_code: courseCode, editing: true,
          transferCode: course.transferCode })
        setShowCompleteCourseModal(true)
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
      const response = await saveCourseCompletion({
        api: completedCoursesAPI, userId: user.id, course: courseData,
        editing: courseToComplete?.editing, transferCode: courseToComplete?.transferCode,
        standing: profile?.advanced_standing || [], updateProfile,
        onRollbackFailure: async () => {
          setCourseToComplete(prev => ({ ...prev, editing: true }))
          await loadCompletedCourses()
        },
      })
      const savedCourse = { ...completedCourses.find(c => c.course_code === courseData.course_code),
        ...courseData, ...response?.completed_course }
      const updatedCourses = [savedCourse, ...completedCourses.filter(c => c.course_code !== courseData.course_code)]
      setCompletedCourses(updatedCourses)
      writeCache('completed', user.id, updatedCourses)

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
      setShowCompleteCourseModal(false)
      setCourseToComplete(null)
    } catch (error) {
      console.error('Error adding completed course:', error)
      alert(error.message || t('courses.saveFailed'))
      throw error
    }
  }

  const handleRemoveCompleted = async () => {
    if (!user?.id || !courseToComplete?.editing) return
    await completedCoursesAPI.removeCompleted(user.id, courseToComplete.course_code)
    const remaining = completedCourses.filter(c => c.course_code !== courseToComplete.course_code)
    setCompletedCourses(remaining)
    writeCache('completed', user.id, remaining)
    setShowCompleteCourseModal(false)
    setCourseToComplete(null)
  }

  const cancelCompleteCourse = useCallback(() => {
    setShowCompleteCourseModal(false)
    setCourseToComplete(null)
  }, [])

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
      // Upload to Storage first — profile_image only accepts an https://
      // URL in our own bucket, never a raw base64 data: URI.
      const { profile_image } = await usersAPI.uploadProfileImage(user.id, file)
      const { error } = await updateProfile({ profile_image })
      if (error) throw error
    } catch (error) {
      console.error('Error uploading image:', error)
      alert('Failed to upload image. Please try again.')
    } finally {
      setIsUploadingImage(false)
      if (fileInputRef.current) fileInputRef.current.value = ''
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

  const value = {
    // auth passthrough — so shells don't need both hooks
    user, profile, authFlags, updateProfile,

    // navigation
    activeTab, setActiveTab, handleTabChange,
    coursesDeepLink, setCoursesDeepLink,
    briefOpenCardId, setBriefOpenCardId,

    // advisor cards
    advisorCards, cardsLoading, cardsGenerating, cardsGeneratedAt,
    freeformInput, setFreeformInput, isAsking,
    refreshAdvisorCards, handleCardSaveToggle, handleCardsReorder,
    handleCardChipClick, handleDeleteCard, handleFreeformSubmit,

    // courses & search
    searchQuery, setSearchQuery, searchResults, isSearching, searchError,
    searchCorrection, hasSearched, sortBy, setSortBy, searchTerm, setSearchTerm,
    availableTerms, handleCourseSearch, sortCourses,

    // user course data
    favorites, favoritesMap,
    completedCourses, completedCoursesMap,
    currentCourses, currentCoursesMap,
    isFavorited, isCompleted, isCurrent,
    handleToggleFavorite, handleToggleCompleted, handleToggleCurrent,

    // degree-progress summary (grounds AI card/chat requests)
    degreeProgressRef,

    // upcoming events
    upcomingEvents, upcomingEventsLoading, upcomingUrgentCount, hasUpcomingCourseEvents,

    // clubs
    clubCalendarEvents, setClubCalendarEvents, managedClubs,

    // mark-complete modal
    showCompleteCourseModal, courseToComplete, handleConfirmComplete, handleRemoveCompleted, cancelCompleteCourse,

    // transcript / syllabus upload
    showTranscriptUpload, transcriptUploadTab, setShowTranscriptUpload,
    openTranscriptUpload, openSyllabusUpload, handleTranscriptImportComplete,

    // profile image
    profileImage, isUploadingImage, fileInputRef, handleImageUpload, handleAvatarClick,

    // misc
    gpaToLetterGrade, handleSignOut,
  }

  return (
    <DashboardDataContext.Provider value={value}>
      {children}
    </DashboardDataContext.Provider>
  )
}
