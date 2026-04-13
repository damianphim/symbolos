import { useState, useEffect, useCallback, useRef } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { coursesAPI } from '../../lib/api'
import favoritesAPI from '../../lib/favoritesAPI'
import completedCoursesAPI from '../../lib/completedCoursesAPI'
import currentCoursesAPI from '../../lib/currentCoursesAPI'
import { getCourseCredits } from '../../utils/courseCredits'
import { normalizeQuery, buildCorrectionCandidates } from '../../utils/fuzzySearch'
import { useLanguage } from '../../contexts/LanguageContext'
import cardsAPI from '../../lib/cardsAPI'
import AdvisorCards from './chat/AdvisorCards'
import FeedbackModal from './FeedbackModal'
import ClubsTab from './ClubsTab'
import RightSidebar from './RightSidebar'
import CoursesView from './CoursesView'

import Sidebar from './Sidebar'
import ProfileTab from './ProfileTab'
import DegreePlanningView from './DegreePlanningView'
import Forum from '../Forum/Forum'
import MarkCompleteModal from './MarkCompleteModal'
import CalendarTab from './CalendarTab'
import clubsAPI from '../../lib/clubsAPI'
import TranscriptUpload from './TranscriptUpload'

import OnboardingTutorial from './OnboardingTutorial'
import { CourseDetailProvider } from '../../contexts/CourseDetailContext'
import CourseDetailModal from '../shared/CourseDetailModal'
import './Dashboard.css'

export default function Dashboard() {
  const { user, profile, signOut, updateProfile, refreshProfile, authFlags } = useAuth()
  const { t, language } = useLanguage()

  // Stable ref for current language — used inside useCallbacks without
  // adding `language` to their dependency arrays (which would cause
  // unnecessary re-creation and effect re-fires on every switch).
  const languageRef = useRef(language)
  languageRef.current = language

  // ── Layout ─────────────────────────────────────────────
  const [activeTab, setActiveTab] = useState(() =>
    localStorage.getItem('symbolos_open_pw_change') ? 'profile' : 'chat'
  )

  const [sidebarOpen, setSidebarOpen] = useState(true)

  // ── Dynamic browser tab title ────────────────────────
  useEffect(() => {
    const tabNameKey = {
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
  const [selectedCourse, setSelectedCourse] = useState(null)
  const [isLoadingCourse, setIsLoadingCourse] = useState(false)
  const [sortBy, setSortBy] = useState('relevance')

  // ── Favorites & completed ──────────────────────────────
  const [favorites, setFavorites] = useState([])
  const [favoritesMap, setFavoritesMap] = useState(new Set())
  const [completedCourses, setCompletedCourses] = useState([])
  const [completedCoursesMap, setCompletedCoursesMap] = useState(new Set())
  const [currentCourses, setCurrentCourses] = useState([])
  const [currentCoursesMap, setCurrentCoursesMap] = useState(new Set())

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
    try {
      setCardsGenerating(true)
      const usedLang = lang || languageRef.current
      const data = await cardsAPI.generateCards(user.id, force, usedLang)
      const cards = data.cards || []
      setAdvisorCards(cards)
      setCardsGeneratedAt(data.generated_at || null)
      // Only cache + mark language when backend confirms it (cards_language !== null)
      const confirmedLang = data.cards_language
      if (confirmedLang) {
        _cacheCards(cards, data.generated_at, confirmedLang)
        try { localStorage.setItem(`cards_language_${user.id}`, confirmedLang) } catch {}
      }
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
      setCardsLoading(true)

      // Try localStorage cache first for instant display
      const cached = _getCachedCards()
      if (cached && cached.cards?.length > 0) {
        setAdvisorCards(cached.cards)
        setCardsGeneratedAt(cached.generatedAt || null)
      }

      // Always fetch from server to get latest
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
              try { localStorage.setItem(`cards_language_${user.id}`, retranslated.cards_language || currentLang) } catch {}
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
        // Server cards match current language — display and cache them
        setAdvisorCards(cards)
        setCardsGeneratedAt(data.generated_at || null)
        if (serverLang) {
          _cacheCards(cards, data.generated_at, serverLang)
          try { localStorage.setItem(`cards_language_${user.id}`, serverLang) } catch {}
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
  useEffect(() => {
    const visible = rightSidebarOpen && activeTab !== 'chat'
    document.body.style.setProperty('--rsb-width', visible ? '320px' : '0px')
    return () => document.body.style.setProperty('--rsb-width', '0px')
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
        try { localStorage.setItem(`cards_language_${user.id}`, confirmedLang) } catch {}
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
  const loadFavorites = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await favoritesAPI.getFavorites(user.id)
      setFavorites(data.favorites || [])
      // FIX: normalize stored course_code to "SUBJ CAT" format for consistent lookup
      setFavoritesMap(new Set((data.favorites || []).map(f => {
        const code = f.course_code || ''
        // If stored without space (e.g. "COMP202"), insert it
        return code.replace(/^([A-Za-z]+)(\d)/, '$1 $2')
      })))
    } catch (error) {
      console.error('Error loading favorites:', error)
    }
  }, [user?.id])

  const loadCompletedCourses = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await completedCoursesAPI.getCompleted(user.id)
      setCompletedCourses(data.completed_courses || [])
      setCompletedCoursesMap(new Set((data.completed_courses || []).map(c => c.course_code)))
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
      setCurrentCourses(data.current_courses || [])
      setCurrentCoursesMap(new Set((data.current_courses || []).map(c => c.course_code)))
    } catch (error) {
      console.error('Error loading current courses:', error)
      setCurrentCourses([])
      setCurrentCoursesMap(new Set())
    }
  }, [user?.id])

  // ── Tab change ─────────────────────────────────────────
  const handleTabChange = (tab) => {
    setActiveTab(tab)
    setSelectedCourse(null)
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
    setSelectedCourse(null)
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

      const data = await coursesAPI.search(searchQuery, searchSubject, 50)
      let courses = data.courses || data || []
      if (!Array.isArray(courses)) courses = []

      // Zero results — try fuzzy correction
      if (courses.length === 0) {
        const candidates = buildCorrectionCandidates(rawQuery)
        for (const candidate of candidates) {
          const corrCode = candidate.query.match(/^([A-Z]{2,6})\s+(\d{3}[A-Z]?)$/)
          const retrySub = corrCode ? corrCode[1] : null
          const retryQ   = corrCode ? corrCode[2] : candidate.query
          const retry = await coursesAPI.search(retryQ, retrySub, 50)
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

  const handleCourseClick = async (course) => {
    setIsLoadingCourse(true)
    try {
      const data = await coursesAPI.getDetails(course.subject, course.catalog)
      setSelectedCourse(data.course || data)
    } catch (error) {
      console.error('Error loading course details:', error)
      setSearchError('Failed to load course details.')
    } finally {
      setIsLoadingCourse(false)
    }
  }

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
    try { await signOut() }
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
      />

      <main className="main-content">
        <button
          className="mobile-menu-btn-overlay"
          onClick={() => setSidebarOpen(true)}
          aria-label="Open menu"
        >☰</button>

        <div className="content-area">

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
            <ClubsTab
              key="clubs-tab-v2"
              user={user}
              profile={profile}
              authFlags={authFlags}
              onClubEventsChange={setClubCalendarEvents}
            />
          )}

          {activeTab === 'courses' && (
            <CoursesView
              favorites={favorites}
              completedCourses={completedCourses}
              completedCoursesMap={completedCoursesMap}
              currentCourses={currentCourses}
              currentCoursesMap={currentCoursesMap}
              favoritesMap={favoritesMap}
              onToggleFavorite={handleToggleFavorite}
              onToggleCompleted={handleToggleCompleted}
              onToggleCurrent={handleToggleCurrent}
              onCourseClick={handleCourseClick}
              searchQuery={searchQuery}
              setSearchQuery={setSearchQuery}
              searchResults={searchResults}
              setSearchResults={setSearchResults}
              isSearching={isSearching}
              searchError={searchError}
              searchCorrection={searchCorrection}
              onSearchWithCorrection={(q) => { setSearchQuery(q); handleCourseSearch(null, q) }}
              hasSearched={hasSearched}
              selectedCourse={selectedCourse}
              setSelectedCourse={setSelectedCourse}
              isLoadingCourse={isLoadingCourse}
              sortBy={sortBy}
              setSortBy={setSortBy}
              sortCourses={sortCourses}
              isFavorited={isFavorited}
              isCompleted={isCompleted}
              isCurrent={isCurrent}
              handleCourseSearch={handleCourseSearch}
              handleCourseClick={handleCourseClick}
              handleToggleFavorite={handleToggleFavorite}
              handleToggleCompleted={handleToggleCompleted}
              handleToggleCurrent={handleToggleCurrent}
              gpaToLetterGrade={gpaToLetterGrade}
            />
          )}

          {activeTab === 'favorites' && (
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
          )}

          {activeTab === 'forum' && <Forum />}

          {activeTab === 'calendar' && (
            <CalendarTab user={user} authFlags={authFlags} clubEvents={clubCalendarEvents} managedClubs={managedClubs} />
          )}

          {activeTab === 'profile' && (
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
          )}
        </div>
      </main>

      {showCompleteCourseModal && courseToComplete && (
        <MarkCompleteModal
          course={courseToComplete}
          onConfirm={handleConfirmComplete}
          onCancel={() => {
            setShowCompleteCourseModal(false)
            setCourseToComplete(null)
          }}
        />
      )}

      {showTranscriptUpload && (
        <TranscriptUpload
          userId={user?.id}
          defaultTab={transcriptUploadTab}
          onClose={() => setShowTranscriptUpload(false)}
          onImportComplete={handleTranscriptImportComplete}
        />
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

      <FeedbackModal userId={user?.id} userEmail={user?.email} />

      {showTutorial && (
        <OnboardingTutorial
          onComplete={() => {
            localStorage.setItem(tourKey, '1')
            setShowTutorial(false)
          }}
        />
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
