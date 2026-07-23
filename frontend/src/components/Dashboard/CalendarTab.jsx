import React, { useState, useEffect, useMemo, useCallback } from 'react'
import {
  FaChevronLeft, FaChevronRight, FaPlus, FaTimes, FaBell,
  FaCalendarAlt, FaBullhorn, FaGraduationCap, FaUser, FaExternalLinkAlt, FaDownload,
  FaTrash, FaEdit, FaCheck, FaClipboardList, FaUsers, FaBook, FaLayerGroup, FaClock, FaExclamationTriangle,
  FaStar, FaBullseye, FaNewspaper, FaSearch, FaBellSlash, FaEllipsisH, FaTag,
  FaApple, FaWindows, FaFilter, FaChevronDown
} from 'react-icons/fa'
import { useLanguage, useTimezone } from '../../contexts/PreferencesContext'
import useViewport from '../../hooks/useViewport'
import useNotificationPrefs from '../../hooks/useNotificationPrefs'
import { scheduleNotification, queueExamNotification, deleteEvent as deleteEventAPI } from '../../services/notificationService'
import { lookupExams, formatExamTime } from '../../utils/examSchedule'
import currentCoursesAPI from '../../lib/currentCoursesAPI'
import completedCoursesAPI from '../../lib/completedCoursesAPI'
import { getEvents, saveEvent, deleteEvent as deleteEventDB, migrateLocalStorageEvents, expandRecurringEvents } from '../../lib/calendarAPI'
import clubsAPI from '../../lib/clubsAPI'
import newslettersAPI from '../../lib/newslettersAPI'

import {
  MCGILL_ACADEMIC_DATES, MONTHS_EN, MONTHS_FR, MONTHS_ZH,
  DAYS_EN, DAYS_FR, DAYS_ZH,
  L, getDaysInMonth, getFirstDayOfMonth, toDateStr, daysUntil,
  getClubEventStyle, getCustomEventTypes, saveCustomEventTypes,
} from './CalendarTab/calendarConstants'
import { downloadICS } from './CalendarTab/calendarUtils'
import EventModal from './CalendarTab/EventModal'
import EventPopup from './CalendarTab/EventPopup'
import DayDrawer from './CalendarTab/DayDrawer'
import MobileAgenda from './CalendarTab/MobileAgenda'
import MobileMonthGrid from './CalendarTab/MobileMonthGrid'
import MobileWeekStrip from './CalendarTab/MobileWeekStrip'
import BulkDeleteModal from './CalendarTab/BulkDeleteModal'
import AnnouncementModal from './CalendarTab/AnnouncementModal'

import './CalendarTab.css'

export default function CalendarTab({ user, authFlags, clubEvents = [], managedClubs = [] }) {
  const { t, language } = useLanguage()
  const { getTodayStr, getNow } = useTimezone()
  const { isMobile } = useViewport()
  const [notifPrefs] = useNotificationPrefs(user?.id, user?.email)

  const today = getNow()
  const MONTHS = language === 'zh' ? MONTHS_ZH : language === 'fr' ? MONTHS_FR : MONTHS_EN
  const DAYS   = language === 'zh' ? DAYS_ZH : language === 'fr' ? DAYS_FR   : DAYS_EN

  const [customTypes, setCustomTypes] = useState(() => getCustomEventTypes(user?.id))

  useEffect(() => {
    setCustomTypes(getCustomEventTypes(user?.id))
  }, [user?.id])

  const handleAddCustomType = useCallback((newType) => {
    setCustomTypes(prev => {
      const updated = [...prev, newType]
      saveCustomEventTypes(user?.id, updated)
      return updated
    })
  }, [user?.id])

  const typeConfig = {
    course:   { color: '#ed1b2f', bg: '#fef2f2', icon: <FaBook />,          label: t('calendar.classEvents') },
    academic: { color: '#1d4ed8', bg: '#eff6ff', icon: <FaGraduationCap />, label: t('calendar.academicDates') },
    exam:     { color: '#7c3aed', bg: '#f5f3ff', icon: <FaClipboardList />, label: L(language, 'Final Exams', 'Examens finaux', '期末考试') },
    personal: { color: '#059669', bg: '#ecfdf5', icon: <FaUser />,          label: t('calendar.personalEvents') },
    club:     { color: '#d97706', bg: '#fef3c7', icon: <FaUsers />,         label: L(language, 'Club Meeting', 'Réunion de club', '社团会议') },
    newsletter: { color: '#0891b2', bg: '#ecfeff', icon: <FaNewspaper />,   label: L(language, 'Newsletter', 'Infolettre', '通讯') },
    ...Object.fromEntries(customTypes.map(ct => [ct.key, { color: ct.color, bg: ct.bg, icon: <FaTag />, label: ct.label }])),
  }

  const getEventStyle = useCallback((event, cfg) => {
    if (event.type === 'club') {
      const clubStyle = getClubEventStyle(event)
      return { ...clubStyle, icon: <FaUsers />, label: L(language, 'Club Meeting', 'Réunion de club', '社团会议') }
    }
    return cfg[event.type] || cfg.personal
  }, [language])

  const [examEvents, setExamEvents] = useState([])
  const [userEvents, setUserEvents]       = useState([])
  const [isLoadingEvents, setIsLoadingEvents] = useState(true)
  const [serverClubEvents, setServerClubEvents] = useState([])
  const [clubAnnouncements, setClubAnnouncements] = useState([])
  const [showAnnouncementModal, setShowAnnouncementModal] = useState(false)
  const [newsletterEvents, setNewsletterEvents] = useState([])

  // ── Newsletter subscription state ─────────────────────────────
  const [nlSources, setNlSources] = useState([])
  const [nlSearch, setNlSearch] = useState('')
  const [nlLoading, setNlLoading] = useState(false)
  const [nlExpanded, setNlExpanded] = useState(false)

  const isMcGillEmail = authFlags?.is_mcgill_email ?? false

  useEffect(() => {
    if (!user?.id || !isMcGillEmail) return
    let cancelled = false
    setNlLoading(true)
    newslettersAPI.getSources().then(data => {
      if (!cancelled) setNlSources(Array.isArray(data) ? data : [])
    }).catch(() => {}).finally(() => { if (!cancelled) setNlLoading(false) })
    return () => { cancelled = true }
  }, [user?.id, isMcGillEmail])

  const handleNlToggle = async (source) => {
    const prev = [...nlSources]
    const wasSubscribed = source.subscribed
    setNlSources(s => s.map(src => src.id === source.id ? { ...src, subscribed: !src.subscribed, email_muted: false } : src))
    try {
      if (wasSubscribed) {
        await newslettersAPI.unsubscribe(source.id)
      } else {
        await newslettersAPI.subscribe(source.id, true)
        if (source.url && window.confirm(
          language === 'fr'
            ? `Voulez-vous aussi recevoir les emails de ${source.name} ? Cela ouvrira leur page d'inscription.`
            : language === 'zh'
            ? `您还想直接收到 ${source.name} 的邮件吗？这将打开他们的注册页面。`
            : `Would you also like to receive emails directly from ${source.name}? This will open their signup page.`
        )) {
          window.open(source.url, '_blank', 'noopener')
        }
      }
    } catch { setNlSources(prev) }
  }

  const handleNlMuteToggle = async (source) => {
    const prev = [...nlSources]
    const newMuted = !source.email_muted
    setNlSources(s => s.map(src => src.id === source.id ? { ...src, email_muted: newMuted } : src))
    try {
      await newslettersAPI.updateSubscription(source.id, { emailMuted: newMuted })
    } catch { setNlSources(prev) }
  }

  const filteredNlSources = nlSearch
    ? nlSources.filter(s => s.name.toLowerCase().includes(nlSearch.toLowerCase()) || s.category.toLowerCase().includes(nlSearch.toLowerCase()))
    : nlSources

  useEffect(() => {
    if (!user?.id || !isMcGillEmail) return
    let cancelled = false
    newslettersAPI.getEvents().then(events => {
      if (cancelled) return
      setNewsletterEvents(events.map(ev => ({
        id: `nl-${ev.id}`,
        title: ev.title,
        date: ev.date,
        time: ev.time || null,
        end_time: ev.end_time || null,
        type: 'newsletter',
        category: ev.source_name || 'Newsletter',
        description: ev.description || '',
        location: ev.location || '',
        link: ev.link || '',
      })))
    }).catch(() => {})
    return () => { cancelled = true }
  }, [user?.id])

  useEffect(() => {
    if (!user?.id) return
    let cancelled = false
    // Pull BOTH current and completed courses — past exams stay in the
    // calendar as a permanent history record even after the term ends and
    // courses move from "current" → "completed".
    Promise.all([
      currentCoursesAPI.getCurrent(user.id).catch(() => ({})),
      completedCoursesAPI.getCompleted(user.id).catch(() => ({})),
    ]).then(async ([curData, compData]) => {
      if (cancelled) return
      const currentCourses   = curData?.current_courses    || []
      const completedCourses = compData?.completed_courses || []

      // Dedupe by course_code — if a course is somehow in both lists,
      // current wins (it's the most recent enrollment).
      const seen = new Set()
      const allCourses = []
      for (const c of currentCourses) {
        if (c.course_code && !seen.has(c.course_code)) {
          seen.add(c.course_code); allCourses.push({ ...c, _historical: false })
        }
      }
      for (const c of completedCourses) {
        if (c.course_code && !seen.has(c.course_code)) {
          seen.add(c.course_code); allCourses.push({ ...c, _historical: true })
        }
      }

      const events = []
      const todayStr = new Date().toISOString().split('T')[0]

      // "When did the user actually start using Symbolos?" — use account
      // created_at, NOT per-course created_at. Re-importing a transcript
      // moves courses from current → completed with a fresh per-row
      // timestamp, which is misleading. The account creation date is the
      // real signal for "was this user on Symbolos at the time of the exam?"
      const userCreatedAt = user?.created_at ? user.created_at.slice(0, 10) : null

      allCourses.forEach((course, idx) => {
        // lookupExams returns EVERY matching exam across all loaded terms.
        const matches = lookupExams(course.course_code)

        // Filter:
        //  1. Term/year must match the course's recorded term/year so a
        //     Winter 2026 exam never shows up for a course taken in Winter
        //     2025 (and vice versa). Current courses (no term/year) get
        //     all future exams — student is presumably enrolled.
        //  2. For HISTORICAL courses, the USER ACCOUNT must have existed on
        //     or before the exam date. Accounts created after the exam can't
        //     have had a real calendar history for that exam, so we skip it.
        const relevant = matches.filter(exam => {
          if (course._historical) {
            // Term/year exact match required for completed courses
            if (!course.term || !course.year) return false
            if (course.term !== exam.term)   return false
            if (Number(course.year) !== exam.year) return false
            // Account must have predated the exam date
            if (userCreatedAt && userCreatedAt > exam.date) return false
            return true
          } else {
            // Current course — show all future-or-today exams
            return exam.date >= todayStr
          }
        })

        relevant.forEach((exam, mIdx) => {
          const timeStr = exam.start ? formatExamTime(exam.start) : ''
          const endStr  = exam.end   ? formatExamTime(exam.end)   : ''
          const campusLabel = exam.campus === 'D.T.' ? 'Downtown Campus'
                            : exam.campus === 'MAC'  ? 'MacDonald Campus' : ''
          const formatLabel = exam.type === 'ONLINE' ? '(Online)' : campusLabel ? `@ ${campusLabel}` : ''
          const isPast = exam.date < todayStr
          events.push({
            id: `exam-${course.course_code}-${idx}-${mIdx}`,
            title: `${course.course_code} – Final Exam`,
            date: exam.date,
            time: timeStr,
            type: 'exam',
            category: exam.termLabel || (isPast ? 'Past Final Exam' : 'Final Exam'),
            description: [course.course_title || exam.title, timeStr && endStr ? `${timeStr} – ${endStr}` : timeStr, formatLabel].filter(Boolean).join(' · '),
            readOnly: true,
            notifyEnabled: !isPast,
            notifySameDay: notifPrefs.timing.sameDay,
            notify1Day:    notifPrefs.timing.oneDay,
            notify7Days:   notifPrefs.timing.oneWeek,
          })
        })
      })
      setExamEvents(events)

      if (
        !cancelled &&
        notifPrefs.method !== 'none' &&
        notifPrefs.eventTypes?.exam !== false &&
        user?.email &&
        events.length > 0
      ) {
        const today = new Date().toISOString().split('T')[0]
        for (const ev of events) {
          if (cancelled) break
          if (ev.date < today) continue
          try {
            await queueExamNotification(ev, user.id, user.email, notifPrefs)
          } catch (err) {
            console.warn(`Could not queue notification for ${ev.title}:`, err)
          }
        }
      }
    }).catch(() => {})
    return () => { cancelled = true }
  }, [user?.id, notifPrefs.method, notifPrefs.eventTypes?.exam, notifPrefs.timing.sameDay, notifPrefs.timing.oneDay, notifPrefs.timing.oneWeek])

  useEffect(() => {
    if (!user?.id) return
    let cancelled = false
    const load = async () => {
      try {
        await migrateLocalStorageEvents(user.id)
        if (cancelled) return
        const rawEvents = await getEvents(user.id)
        if (!cancelled) setUserEvents(expandRecurringEvents(rawEvents))
      } catch (err) {
        console.error('Failed to load calendar events from Supabase:', err)
        try {
          const local = JSON.parse(localStorage.getItem('mcgill_calendar_events') || '[]')
          if (!cancelled) setUserEvents(local)
        } catch { /* ignore */ }
      } finally {
        if (!cancelled) setIsLoadingEvents(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [user?.id])

  useEffect(() => {
    if (!user?.id) return
    let cancelled = false
    async function loadClubData() {
      try {
        const [evRes, annRes] = await Promise.all([
          clubsAPI.getSubscribedClubEvents(),
          clubsAPI.getSubscribedClubAnnouncements(),
        ])
        if (cancelled) return
        const shaped = (evRes.events || []).map(ev => ({
          id: `sclub-${ev.id}`,
          _serverId: ev.id,
          title: ev.title,
          date: ev.date,
          time: ev.time || '',
          end_time: ev.end_time || '',
          type: 'club',
          category: ev.clubs?.name || '',
          description: ev.description || '',
          location: ev.location || '',
          clubId: ev.club_id,
          recurrence: ev.recurrence || null,
          readOnly: false,
        }))
        const expanded = expandRecurringEvents(shaped)
        setServerClubEvents(expanded)
        setClubAnnouncements(annRes.announcements || [])
      } catch (err) {
        console.error('Failed to load club events/announcements:', err)
      }
    }
    loadClubData()
    return () => { cancelled = true }
  }, [user?.id])

  const refreshClubData = useCallback(async () => {
    if (!user?.id) return
    try {
      const [evRes, annRes] = await Promise.all([
        clubsAPI.getSubscribedClubEvents(),
        clubsAPI.getSubscribedClubAnnouncements(),
      ])
      const shaped = (evRes.events || []).map(ev => ({
        id: `sclub-${ev.id}`,
        _serverId: ev.id,
        title: ev.title,
        date: ev.date,
        time: ev.time || '',
        end_time: ev.end_time || '',
        type: 'club',
        category: ev.clubs?.name || '',
        description: ev.description || '',
        location: ev.location || '',
        clubId: ev.club_id,
        recurrence: ev.recurrence || null,
        readOnly: false,
      }))
      setServerClubEvents(expandRecurringEvents(shaped))
      setClubAnnouncements(annRes.announcements || [])
    } catch (err) { console.error('Failed to refresh club data:', err) }
  }, [user?.id])

  const formatDate = useCallback((dateStr) => {
    const [y, m, d] = dateStr.split('-')
    return `${MONTHS[parseInt(m) - 1]} ${parseInt(d)}, ${y}`
  }, [MONTHS])

  // "Jul 6 – Jul 12, 2026" (or "Jul 30 – Aug 5, 2026" across a month boundary)
  const formatWeekRange = (start, end) => {
    const sameMonth = start.getMonth() === end.getMonth() && start.getFullYear() === end.getFullYear()
    const startLabel = `${MONTHS[start.getMonth()].slice(0, 3)} ${start.getDate()}`
    const endLabel = sameMonth
      ? `${end.getDate()}, ${end.getFullYear()}`
      : `${MONTHS[end.getMonth()].slice(0, 3)} ${end.getDate()}, ${end.getFullYear()}`
    return `${startLabel} – ${endLabel}`
  }

  const [view, setView]               = useState('calendar')
  const [currentYear, setCurrentYear] = useState(today.getFullYear())
  const [currentMonth, setCurrentMonth] = useState(today.getMonth())
  // Day highlighted in the mobile month grid; its events show in the agenda
  // below. Kept inside the visible month by the effect further down so paging
  // months always lands on a day that's actually on screen.
  const [selectedDate, setSelectedDate] = useState(today)
  // Calendar granularity — 'month' (existing grid) or 'week' (full agenda per
  // day, so users can see clearly what's due in the next 7 days).
  const [calGranularity, setCalGranularity] = useState('month')
  const startOfWeek = (d) => { const s = new Date(d); s.setHours(0, 0, 0, 0); s.setDate(s.getDate() - s.getDay()); return s }
  const [weekStart, setWeekStart] = useState(() => startOfWeek(today))
  const switchToWeek = () => {
    const isCurrentRealMonth = currentYear === today.getFullYear() && currentMonth === today.getMonth()
    const anchor = isCurrentRealMonth ? today : new Date(currentYear, currentMonth, 1)
    setWeekStart(startOfWeek(anchor))
    setCalGranularity('week')
  }
  const switchToMonth = () => {
    setCurrentYear(weekStart.getFullYear())
    setCurrentMonth(weekStart.getMonth())
    setCalGranularity('month')
  }
  const prevWeek = () => setWeekStart(d => { const n = new Date(d); n.setDate(n.getDate() - 7); return n })
  const nextWeek = () => setWeekStart(d => { const n = new Date(d); n.setDate(n.getDate() + 7); return n })
  const weekDates = Array.from({ length: 7 }, (_, i) => { const d = new Date(weekStart); d.setDate(d.getDate() + i); return d })
  const [filter, setFilter]           = useState({ course: true, academic: true, exam: true, personal: true, club: true, newsletter: true })
  const [showModal, setShowModal]     = useState(false)
  const [editEvent, setEditEvent]     = useState(null)
  const [preselectedDate, setPreselectedDate] = useState(null)
  const [dayDrawer, setDayDrawer]     = useState(null)
  const [popupEvent, setPopupEvent]   = useState(null)
  const [notifSaved, setNotifSaved]   = useState(false)
  const [showMoreMenu, setShowMoreMenu] = useState(false)
  const [showGCalGuide, setShowGCalGuide] = useState(false)
  const [guideProvider, setGuideProvider] = useState('google')
  const [showBulkDelete, setShowBulkDelete] = useState(false)
  const [hiddenSlotKeys, setHiddenSlotKeys] = useState(() => {
    try {
      const stored = localStorage.getItem(`hiddenSlots_${user?.id}`)
      return stored ? new Set(JSON.parse(stored)) : new Set()
    } catch { return new Set() }
  })

  useEffect(() => {
    try {
      localStorage.setItem(`hiddenSlots_${user?.id}`, JSON.stringify([...hiddenSlotKeys]))
    } catch { /* ignore */ }
  }, [hiddenSlotKeys, user?.id])

  const [mutedClubIds, setMutedClubIds] = useState(() => {
    try {
      const stored = localStorage.getItem(`mutedClubs_${user?.id}`)
      return stored ? new Set(JSON.parse(stored)) : new Set()
    } catch { return new Set() }
  })
  useEffect(() => {
    if (!user?.id) return
    try {
      localStorage.setItem(`mutedClubs_${user?.id}`, JSON.stringify([...mutedClubIds]))
    } catch { /* silent */ }
  }, [mutedClubIds, user?.id])

  const [hiddenEventIds, setHiddenEventIds] = useState(() => {
    try {
      const stored = localStorage.getItem(`hiddenEvents_${user?.id}`)
      return stored ? new Set(JSON.parse(stored)) : new Set()
    } catch { return new Set() }
  })
  useEffect(() => {
    if (!user?.id) return
    try {
      localStorage.setItem(`hiddenEvents_${user?.id}`, JSON.stringify([...hiddenEventIds]))
    } catch { /* silent */ }
  }, [hiddenEventIds, user?.id])

  const allEvents = useMemo(() => {
    const tEvent = (ev) => ({
      ...ev,
      title:       ev.titleKey    ? t(ev.titleKey)    : ev.titleEn    ? L(language, ev.titleEn, ev.titleFr, ev.titleZh)    : ev.title    || '',
      category:    ev.categoryKey ? t(ev.categoryKey) : ev.categoryEn ? L(language, ev.categoryEn, ev.categoryFr, ev.categoryZh) : ev.category || '',
      description: ev.descKey     ? t(ev.descKey)     : ev.description || '',
    })
    const retypedUser = userEvents.map(ev =>
      ev.course_code && ev.recurrence ? { ...tEvent(ev), type: 'course' } : tEvent(ev)
    )
    return [
      ...MCGILL_ACADEMIC_DATES.map(tEvent),
      ...examEvents,
      ...retypedUser,
      ...clubEvents,
      ...serverClubEvents,
      ...newsletterEvents.map(tEvent),
    ]
  }, [userEvents, examEvents, clubEvents, serverClubEvents, newsletterEvents, language, t])

  const filteredEvents = useMemo(() =>
    allEvents.filter(e => {
      if (filter[e.type] === false) return false
      if (e.course_code && e.recurrence) {
        const key = `${e.course_code}::${e.recurrence}::${e.time || ''}`
        if (hiddenSlotKeys.has(key)) return false
      }
      if (e.type === 'club' && e.clubId && mutedClubIds.has(e.clubId)) return false
      if (hiddenEventIds.has(e.id)) return false
      return true
    }),
    [allEvents, filter, hiddenSlotKeys, mutedClubIds, hiddenEventIds]
  )

  // Per-type counts from the full (unfiltered) event universe — used to fold
  // chips for types the student has no events of behind "+N more", so the
  // filter bar doesn't force everyone to scan six chips up front.
  const eventCountsByType = useMemo(() => {
    const counts = {}
    allEvents.forEach(e => { counts[e.type] = (counts[e.type] || 0) + 1 })
    return counts
  }, [allEvents])
  const [showAllFilterChips, setShowAllFilterChips] = useState(false)
  // Phones get the chip row behind a compact disclosure — six chips wrap into
  // three rows at 360px and push the calendar itself below the fold.
  const [showMobileFilters, setShowMobileFilters] = useState(false)
  const mutedFilterCount = Object.values(filter).filter(v => v === false).length

  const eventsByDate = useMemo(() => {
    const map = {}
    filteredEvents.forEach(e => {
      if (!map[e.date]) map[e.date] = []
      map[e.date].push(e)
    })
    return map
  }, [filteredEvents])

  const userEventIds = useMemo(() => new Set(userEvents.map(e => e.id)), [userEvents])

  const prevMonth = () => {
    if (currentMonth === 0) { setCurrentMonth(11); setCurrentYear(y => y - 1) }
    else setCurrentMonth(m => m - 1)
  }
  const nextMonth = () => {
    if (currentMonth === 11) { setCurrentMonth(0); setCurrentYear(y => y + 1) }
    else setCurrentMonth(m => m + 1)
  }

  const daysInMonth = getDaysInMonth(currentYear, currentMonth)
  const firstDay = getFirstDayOfMonth(currentYear, currentMonth)
  const cells = []
  for (let i = 0; i < firstDay; i++) cells.push(null)
  for (let d = 1; d <= daysInMonth; d++) cells.push(d)

  // Keep the mobile month grid's selected day on a date that's actually in the
  // month being shown. Paging to another month jumps to today if it's that
  // month, else the 1st — never leaves a stale day from the previous month.
  // (today is omitted from deps: getNow() returns a fresh Date each render, and
  // we only need to react to the visible month/granularity changing.)
  useEffect(() => {
    if (calGranularity !== 'month') return
    const inMonth = selectedDate.getFullYear() === currentYear && selectedDate.getMonth() === currentMonth
    if (inMonth) return
    const isCurrentMonth = today.getFullYear() === currentYear && today.getMonth() === currentMonth
    setSelectedDate(isCurrentMonth ? today : new Date(currentYear, currentMonth, 1))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentYear, currentMonth, calGranularity])

  // Same idea for the week strip: keep the selected day inside the visible
  // week. Paging weeks (or switching to week granularity) lands on today when
  // it's in view, else the first day of the week.
  useEffect(() => {
    if (calGranularity !== 'week') return
    const selStr = toDateStr(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate())
    const weekStrs = weekDates.map(d => toDateStr(d.getFullYear(), d.getMonth(), d.getDate()))
    if (weekStrs.includes(selStr)) return
    const todayIdx = weekStrs.indexOf(getTodayStr())
    setSelectedDate(todayIdx >= 0 ? weekDates[todayIdx] : weekDates[0])
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [weekStart, calGranularity])

  const to24h = (t) => {
    if (!t) return null
    if (/^\d{2}:\d{2}$/.test(t)) return t
    if (/^\d{1,2}:\d{2}$/.test(t) && !t.includes('AM') && !t.includes('PM'))
      return t.padStart(5, '0')
    const m = t.match(/^(\d{1,2}):(\d{2})\s*(AM|PM)$/i)
    if (m) {
      let h = parseInt(m[1], 10)
      const min = m[2]
      const period = m[3].toUpperCase()
      if (period === 'PM' && h !== 12) h += 12
      if (period === 'AM' && h === 12) h = 0
      return `${String(h).padStart(2, '0')}:${min}`
    }
    return t
  }

  const handleSaveEvent = async (event) => {
    if (event.type === 'club' && event.clubId) {
      setShowModal(false); setEditEvent(null); setPreselectedDate(null)
      try {
        await clubsAPI.createClubEvent(event.clubId, {
          title: event.title,
          description: event.description || '',
          date: event.date,
          time: to24h(event.time),
          end_time: to24h(event.end_time),
          location: event.location || null,
          recurrence: event.recurrence || null,
        })
        await refreshClubData()
      } catch (err) {
        console.error('Failed to create club event:', err)
      }
      return
    }

    const isEdit = event.id && userEvents.some(e => e.id === event.id)
    const tempId = event.id || `user-${Date.now()}`
    if (isEdit) {
      setUserEvents(prev => prev.map(e => e.id === event.id ? event : e))
    } else {
      const newEvent = { ...event, id: tempId }
      setUserEvents(prev => [...prev, newEvent])
      event = newEvent
    }

    setShowModal(false); setEditEvent(null); setPreselectedDate(null)

    try {
      const saved = await saveEvent(event, user.id)
      if (!isEdit && saved.id && saved.id !== tempId) {
        setUserEvents(prev => prev.map(e => e.id === tempId ? { ...e, id: saved.id } : e))
        event = { ...event, id: saved.id }
      }
    } catch (err) {
      console.error('Failed to save event to Supabase:', err)
      if (isEdit) {
        setUserEvents(prev => prev.map(e => e.id === event.id ? editEvent : e))
      } else {
        setUserEvents(prev => prev.filter(e => e.id !== tempId))
      }
      return
    }

    if (event.notifyEnabled) {
      // Pass the user's notification prefs so method (email/sms/both/none),
      // phone, and event-type opt-outs are all honored on the backend.
      try { await scheduleNotification(event, user.id, user.email, notifPrefs) }
      catch (err) { console.error('Failed to schedule notification:', err) }
      setNotifSaved(true)
      setTimeout(() => setNotifSaved(false), 3000)
    }
  }

  const handleDeleteEvent = async (id) => {
    const deleted = userEvents.find(e => e.id === id)
    setUserEvents(prev => prev.filter(e => e.id !== id))
    setShowModal(false); setEditEvent(null); setPopupEvent(null); setDayDrawer(null)

    try {
      await deleteEventDB(id, user.id)
    } catch (err) {
      console.error('Failed to delete event from Supabase:', err)
      if (deleted) setUserEvents(prev => [...prev, deleted])
    }

    if (user?.id && id && !id.startsWith('user-')) {
      try { await deleteEventAPI(id, user.id) }
      catch (err) { console.error('Failed to delete event from notification backend:', err) }
    }
  }

  const handleBulkHide = (slotKeys, action) => {
    if (action === 'unhide') {
      setHiddenSlotKeys(prev => {
        const next = new Set(prev)
        slotKeys.forEach(k => next.delete(k))
        return next
      })
    } else {
      setHiddenSlotKeys(prev => new Set([...prev, ...slotKeys]))
    }
  }

  const handleBulkUnhideAll = () => {
    setHiddenSlotKeys(new Set())
  }

  const handleEditSlot = async (anchorEv, { recurrence, time, end_time }) => {
    const oldKey = `${anchorEv.course_code}::${anchorEv.recurrence}::${anchorEv.time || ''}`
    const newKey = `${anchorEv.course_code}::${recurrence}::${time || ''}`
    const updatedAnchor = {
      ...anchorEv,
      recurrence,
      time,
      end_time,
      _isRecurringOccurrence: false,
      _anchorId: undefined,
    }
    const reexpanded = expandRecurringEvents([updatedAnchor])
    setUserEvents(prev => {
      const rest = prev.filter(e => e.id !== anchorEv.id && e._anchorId !== anchorEv.id)
      return [...rest, ...reexpanded]
    })
    if (hiddenSlotKeys.has(oldKey)) {
      setHiddenSlotKeys(prev => {
        const s = new Set(prev); s.delete(oldKey); s.add(newKey); return s
      })
    }
    try { await saveEvent(updatedAnchor, user.id) }
    catch (err) { console.error('Failed to save slot edit:', err) }
  }

  const handleDayClick = (day) => {
    if (!day) return
    const dateStr = toDateStr(currentYear, currentMonth, day)
    const eventsOnDay = eventsByDate[dateStr] || []
    if (eventsOnDay.length > 0) {
      setDayDrawer({ date: dateStr, events: eventsOnDay })
    } else {
      setPreselectedDate(dateStr); setEditEvent(null); setShowModal(true)
    }
  }

  // Same as handleDayClick but for the week view, which works with Date
  // objects directly since a week can straddle a month/year boundary.
  const handleWeekDayAdd = (date) => {
    const dateStr = toDateStr(date.getFullYear(), date.getMonth(), date.getDate())
    setPreselectedDate(dateStr); setEditEvent(null); setShowModal(true)
  }

  // Mobile agenda: tapping a day heading keeps the desktop month-grid
  // behaviour (drawer when the day has events, add-event otherwise) so the
  // DayDrawer stays reachable without a month grid to click.
  const handleAgendaDayClick = (date) => {
    const dateStr = toDateStr(date.getFullYear(), date.getMonth(), date.getDate())
    const eventsOnDay = eventsByDate[dateStr] || []
    if (eventsOnDay.length > 0) {
      setDayDrawer({ date: dateStr, events: eventsOnDay })
    } else {
      setPreselectedDate(dateStr); setEditEvent(null); setShowModal(true)
    }
  }

  const handleAddFromDrawer = () => {
    const date = dayDrawer?.date
    setDayDrawer(null)
    setPreselectedDate(date); setEditEvent(null); setShowModal(true)
  }

  const handleEditFromDrawer = (event) => {
    setDayDrawer(null)
    setEditEvent(event); setShowModal(true)
  }

  const upcomingEvents = useMemo(() => {
    const todayStr = getTodayStr()
    return [...filteredEvents]
      .filter(e => e.date >= todayStr)
      .sort((a, b) => a.date.localeCompare(b.date))
      .slice(0, 30)
  }, [filteredEvents, getTodayStr])

  const urgentEvents = upcomingEvents.filter(e => daysUntil(e.date) <= 7)

  // Announcements list shows 5 at a time — urgentEvents above stays computed
  // from the full upcomingEvents so the "N events in 7 days" banner and any
  // badge counts stay accurate regardless of how much is expanded on screen.
  const [showAllUpcoming, setShowAllUpcoming] = useState(false)
  const displayedUpcoming = showAllUpcoming ? upcomingEvents : upcomingEvents.slice(0, 5)

  const countdownLabel = (days) => {
    if (days === 0) return L(language, '🔴 Today!', "🔴 Aujourd'hui!", '🔴 今天！')
    if (days === 1) return `⚠️ ${t('calendar.tomorrow')}`
    if (days <= 7)  return `⚠️ ${t('calendar.inXDays').replace('{n}', days)}`
    return t('calendar.inXDays').replace('{n}', days)
  }

  return (
    <div className="cal-container">
      {/* Missing-time banner */}
      {userEvents.some(e => e.recurrence && e.course_code && !e._isRecurringOccurrence && !e.time) && (
        <div className="cal-missing-time-banner">
          <FaExclamationTriangle className="cal-missing-icon" />
          <span>{L(language, 'Some classes are missing their time.', "Certaines classes n'ont pas d'heure.", '部分课程缺少时间信息')}</span>
          <button className="cal-missing-fix-btn" onClick={() => setShowBulkDelete(true)}>
            {L(language, 'Fix now', 'Corriger', '立即修复')}
          </button>
        </div>
      )}

      {/* Header */}
      <div className="cal-header">
        <div className="cal-header-left">
          <FaCalendarAlt className="cal-header-icon" />
          <div>
            <h2 className="cal-title">{t('nav.calendar')}</h2>
            <p className="cal-subtitle">{t('calendar.subtitle')}</p>
          </div>
        </div>
        <div className="cal-header-right">
          {notifSaved && (
            <div className="cal-notif-toast"><FaBell /> {t('calendar.remindersSet')}</div>
          )}
          <div className="cal-view-toggle">
            <button className={view === 'calendar' ? 'active' : ''} onClick={() => setView('calendar')}>
              <FaCalendarAlt /> <span>{t('calendar.calendarView')}</span>
            </button>
            <button className={view === 'announcements' ? 'active' : ''} onClick={() => setView('announcements')}>
              <FaBullhorn /> <span>{t('calendar.announcements')}</span>
              {urgentEvents.length > 0 && <span className="cal-badge">{urgentEvents.length}</span>}
            </button>
            <button className={view === 'newsletters' ? 'active' : ''} onClick={() => setView('newsletters')}>
              <FaNewspaper /> <span>{L(language, 'Newsletters', 'Infolettres', '通讯')}</span>
            </button>
          </div>
          <div className="cal-export-wrap">
            <button
              className="cal-export-btn cal-more-btn"
              onClick={() => setShowMoreMenu(p => !p)}
              aria-label={L(language, 'More options', "Plus d'options", '更多选项')}
              title={L(language, 'More options', "Plus d'options", '更多选项')}
            >
              <FaEllipsisH size={13} />
            </button>
            {showMoreMenu && (
              <div className="cal-export-menu">
                <button className="cal-export-item" onClick={() => { downloadICS(filteredEvents, 'mcgill-calendar.ics'); setShowMoreMenu(false) }}>
                  <FaDownload size={11} /> {t('calendar.exportICS')}
                </button>
                <button className="cal-export-item cal-export-item--google" onClick={() => { downloadICS(filteredEvents, 'mcgill-calendar.ics'); setGuideProvider('google'); setShowGCalGuide(true); setShowMoreMenu(false) }}>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
                  {t('calendar.exportGoogleHelp')}
                </button>
                <button className="cal-export-item cal-export-item--apple" onClick={() => { downloadICS(filteredEvents, 'mcgill-calendar.ics'); setGuideProvider('apple'); setShowGCalGuide(true); setShowMoreMenu(false) }}>
                  <FaApple size={13} />
                  {t('calendar.exportAppleHelp')}
                </button>
                <button className="cal-export-item cal-export-item--outlook" onClick={() => { downloadICS(filteredEvents, 'mcgill-calendar.ics'); setGuideProvider('outlook'); setShowGCalGuide(true); setShowMoreMenu(false) }}>
                  <FaWindows size={12} />
                  {t('calendar.exportOutlookHelp')}
                </button>
                <button className="cal-export-item" onClick={() => { setShowBulkDelete(true); setShowMoreMenu(false) }}>
                  <FaLayerGroup size={11} /> {L(language, 'Edit Events', 'Modifier les événements', '编辑事件')}
                </button>
              </div>
            )}
          </div>
          <button className="cal-add-btn" data-tour="calendar-add" onClick={() => { setPreselectedDate(null); setEditEvent(null); setShowModal(true) }}>
            <FaPlus /> <span>{t('calendar.addEventBtn')}</span>
          </button>
        </div>
      </div>

      {/* Mobile: chip row folds behind a compact disclosure */}
      {isMobile && (
        <button
          className={`cal-filter-toggle ${showMobileFilters ? 'is-open' : ''}`}
          onClick={() => setShowMobileFilters(p => !p)}
          aria-expanded={showMobileFilters}
        >
          <FaFilter size={11} />
          <span>{t('cal.filters')}</span>
          {mutedFilterCount > 0 && (
            <span className="cal-filter-toggle__count">{mutedFilterCount}</span>
          )}
          <FaChevronDown size={10} className="cal-filter-toggle__chev" />
        </button>
      )}

      {/* Filter Bar — chips for types with zero events fold behind "+N more" */}
      <div className={`cal-filter-bar${isMobile && !showMobileFilters ? ' cal-filter-bar--collapsed' : ''}`}>
        {(() => {
          const visibleTypes = Object.entries(typeConfig).filter(([key]) => key !== 'newsletter' || isMcGillEmail)
          const withEvents = visibleTypes.filter(([key]) => (eventCountsByType[key] || 0) > 0)
          const withoutEvents = visibleTypes.filter(([key]) => (eventCountsByType[key] || 0) === 0)
          const shown = showAllFilterChips ? visibleTypes : withEvents
          return (
            <>
              {shown.map(([key, cfg]) => (
                <button key={key}
                  className={`cal-filter-chip ${filter[key] ? 'active' : ''}`}
                  style={filter[key] ? { borderColor: cfg.color, background: cfg.bg, color: cfg.color } : {}}
                  onClick={() => setFilter(f => ({ ...f, [key]: !f[key] }))}>
                  {cfg.icon} {cfg.label}
                </button>
              ))}
              {!showAllFilterChips && withoutEvents.length > 0 && (
                <button className="cal-filter-chip cal-filter-chip--more" onClick={() => setShowAllFilterChips(true)}>
                  +{withoutEvents.length} {L(language, 'more', 'de plus', '更多')}
                </button>
              )}
            </>
          )
        })()}
      </div>

      {isLoadingEvents && (
        <div className="cal-loading">
          <div className="cal-loading-spinner" />
          <span>Loading your events…</span>
        </div>
      )}

      {/* Calendar View */}
      {view === 'calendar' && !isLoadingEvents && (
        <div className="cal-body">
          <div className="cal-granularity-toggle">
            <button className={calGranularity === 'month' ? 'active' : ''} onClick={switchToMonth}>
              {t('calendar.monthView')}
            </button>
            <button className={calGranularity === 'week' ? 'active' : ''} onClick={switchToWeek}>
              {t('calendar.weekView')}
            </button>
          </div>

          {calGranularity === 'month' ? (
            <>
              <div className="cal-month-nav">
                <button onClick={prevMonth}><FaChevronLeft /></button>
                <div className="cal-month-title">
                  <h3>{MONTHS[currentMonth]} {currentYear}</h3>
                  <button className="cal-today-btn" onClick={() => { setCurrentYear(today.getFullYear()); setCurrentMonth(today.getMonth()); setSelectedDate(today) }}>
                    {t('calendar.todayBtn')}
                  </button>
                </div>
                <button onClick={nextMonth}><FaChevronRight /></button>
              </div>
              {isMobile ? (
                <>
                  {/* Compact month grid so the whole month is visible and any
                      day is reachable; the selected day's events render below. */}
                  <MobileMonthGrid
                    cells={cells}
                    year={currentYear}
                    month={currentMonth}
                    DAYS={DAYS}
                    eventsByDate={eventsByDate}
                    selectedStr={toDateStr(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate())}
                    todayStr={getTodayStr()}
                    onSelectDay={(day) => setSelectedDate(new Date(currentYear, currentMonth, day))}
                    typeConfig={typeConfig} getEventStyle={getEventStyle}
                  />
                  <MobileAgenda
                    dates={[selectedDate]}
                    eventsByDate={eventsByDate}
                    todayStr={getTodayStr()}
                    pinnedDateStr={toDateStr(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate())}
                    MONTHS={MONTHS} DAYS={DAYS}
                    onSelectEvent={setPopupEvent}
                    onOpenDay={handleAgendaDayClick}
                    onAddOnDate={handleWeekDayAdd}
                    typeConfig={typeConfig} getEventStyle={getEventStyle}
                    t={t}
                  />
                </>
              ) : (
              <>
              <div className="cal-grid-header">
                {DAYS.map(d => <div key={d} className="cal-grid-day-label">{d}</div>)}
              </div>
              <div className="cal-grid">
                {cells.map((day, idx) => {
                  if (!day) return <div key={`empty-${idx}`} className="cal-cell cal-cell-empty" />
                  const dateStr = toDateStr(currentYear, currentMonth, day)
                  const eventsOnDay = eventsByDate[dateStr] || []
                  const isToday = dateStr === getTodayStr()
                  return (
                    <div key={dateStr}
                      className={`cal-cell ${isToday ? 'cal-cell-today' : ''} ${eventsOnDay.length > 0 ? 'cal-cell-has-events' : ''}`}
                      onClick={() => handleDayClick(day)}>
                      <span className={`cal-cell-number ${isToday ? 'today' : ''}`}>{day}</span>
                      <div className="cal-cell-events">
                        {eventsOnDay.slice(0, 3).map(e => {
                          const style = getEventStyle(e, typeConfig)
                          return (
                            <div key={e.id} className="cal-event-dot" style={{ background: style.color, color: '#fff' }} title={e.title}>
                              {(() => {
                                const t = e.title
                                const courseMatch = t.match(/^([A-Z]{2,6})\s*(\d{3}[A-Z]?)\s+(.+)$/)
                                if (courseMatch) {
                                  const type = courseMatch[3]
                                  const abbr = type.startsWith('Lecture') ? 'Lec' : type.startsWith('Tutorial') ? 'Tut' : type.startsWith('Lab') ? 'Lab' : type.slice(0,3)
                                  return `${courseMatch[1]}${courseMatch[2]} ${abbr}`
                                }
                                return t.length > 13 ? t.slice(0, 12) + '…' : t
                              })()}
                            </div>
                          )
                        })}
                        {eventsOnDay.length > 3 && (
                          <div className="cal-event-more">+{eventsOnDay.length - 3} {t('cal.moreDots')}</div>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
              </>
              )}
            </>
          ) : (
            <>
              <div className="cal-month-nav">
                <button onClick={prevWeek}><FaChevronLeft /></button>
                <div className="cal-month-title">
                  <h3>
                    {formatWeekRange(weekDates[0], weekDates[6])}
                  </h3>
                  <button className="cal-today-btn" onClick={() => { setWeekStart(startOfWeek(today)); setSelectedDate(today) }}>
                    {t('calendar.todayBtn')}
                  </button>
                </div>
                <button onClick={nextWeek}><FaChevronRight /></button>
              </div>
              {isMobile ? (
                <>
                  {/* Week strip so all 7 days are visible and tappable; the
                      selected day's events render below (mirrors month view). */}
                  <MobileWeekStrip
                    weekDates={weekDates}
                    DAYS={DAYS}
                    eventsByDate={eventsByDate}
                    selectedStr={toDateStr(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate())}
                    todayStr={getTodayStr()}
                    onSelectDay={setSelectedDate}
                    typeConfig={typeConfig} getEventStyle={getEventStyle}
                  />
                  <MobileAgenda
                    dates={[selectedDate]}
                    eventsByDate={eventsByDate}
                    todayStr={getTodayStr()}
                    pinnedDateStr={toDateStr(selectedDate.getFullYear(), selectedDate.getMonth(), selectedDate.getDate())}
                    MONTHS={MONTHS} DAYS={DAYS}
                    onSelectEvent={setPopupEvent}
                    onOpenDay={handleAgendaDayClick}
                    onAddOnDate={handleWeekDayAdd}
                    typeConfig={typeConfig} getEventStyle={getEventStyle}
                    t={t}
                  />
                </>
              ) : (
              <div className="cal-week-grid">
                {weekDates.map(date => {
                  const dateStr = toDateStr(date.getFullYear(), date.getMonth(), date.getDate())
                  const eventsOnDay = (eventsByDate[dateStr] || []).slice().sort((a, b) => (a.time || '99:99').localeCompare(b.time || '99:99'))
                  const isToday = dateStr === getTodayStr()
                  return (
                    <div key={dateStr} className={`cal-week-col ${isToday ? 'cal-week-col-today' : ''}`}>
                      <div className="cal-week-col-header">
                        <span className="cal-week-col-day">{DAYS[date.getDay()]}</span>
                        <span className={`cal-week-col-num ${isToday ? 'today' : ''}`}>{date.getDate()}</span>
                      </div>
                      <div className="cal-week-col-events">
                        {eventsOnDay.map(e => {
                          const style = getEventStyle(e, typeConfig)
                          return (
                            <div
                              key={e.id}
                              className="cal-week-event"
                              style={{ borderLeftColor: style.color, background: style.bg }}
                              onClick={() => setPopupEvent(e)}
                            >
                              {e.time && <span className="cal-week-event-time">{e.time}</span>}
                              <span className="cal-week-event-title">{e.title}</span>
                            </div>
                          )
                        })}
                        <button className="cal-week-add-btn" onClick={() => handleWeekDayAdd(date)}>
                          <FaPlus size={10} />
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
              )}
            </>
          )}

          <div className="cal-legend">
            {Object.entries(typeConfig).filter(([key]) => key !== 'newsletter' || isMcGillEmail).map(([key, cfg]) => (
              <div key={key} className="cal-legend-item">
                <span className="cal-legend-dot" style={{ background: cfg.color }} />
                {cfg.label}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Announcements View */}
      {view === 'announcements' && !isLoadingEvents && (
        <div className="cal-announcements">
          {urgentEvents.length > 0 && (
            <div className="cal-urgent-banner">
              <FaBell />
              <strong>{urgentEvents.length} {urgentEvents.length === 1 ? t('calendar.event') : t('calendar.events')} {t('calendar.upcomingIn7')}</strong>
            </div>
          )}
          <div className="cal-announce-list">
            {upcomingEvents.length === 0 ? (
              <div className="cal-empty-state">
                <FaCalendarAlt size={40} />
                <p>{t('calendar.noUpcoming')}</p>
              </div>
            ) : displayedUpcoming.map(event => {
              const style = getEventStyle(event, typeConfig)
              const days = daysUntil(event.date)
              const isUrgent = days <= 7 && days >= 0
              return (
                <div key={event.id}
                  className={`cal-announce-card ${isUrgent ? 'urgent' : ''}`}
                  style={{ borderLeftColor: style.color }}
                  onClick={() => setPopupEvent(event)}>
                  <div className="cal-announce-card-left">
                    <div className="cal-announce-type" style={{ color: style.color, background: style.bg }}>
                      {style.icon} {style.label}
                    </div>
                    <h4>{event.title}</h4>
                    {event.category && <span className="cal-announce-category">{event.category}</span>}
                    {event.description && <p className="cal-announce-desc">{event.description}</p>}
                  </div>
                  <div className="cal-announce-card-right">
                    <div className="cal-announce-date">{formatDate(event.date)}</div>
                    <div className="cal-announce-countdown" style={{ color: days === 0 ? '#ef4444' : isUrgent ? '#f59e0b' : style.color }}>
                      {countdownLabel(days)}
                    </div>
                    {event.notifyEnabled && (
                      <div className="cal-announce-notif"><FaBell size={10} /> {t('calendar.remindersSet')}</div>
                    )}
                  </div>
                </div>
              )
            })}
          </div>

          {!showAllUpcoming && upcomingEvents.length > displayedUpcoming.length && (
            <button className="cal-show-more-btn" onClick={() => setShowAllUpcoming(true)}>
              {L(language, 'Show more', 'Afficher plus', '显示更多')} ({upcomingEvents.length - displayedUpcoming.length})
            </button>
          )}

          {clubAnnouncements.length > 0 && (
            <>
              <h3 style={{ margin: '24px 0 12px', fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FaBullhorn size={13} style={{ color: '#d97706' }} /> {L(language, 'Club Announcements', 'Annonces de club', '社团公告')}
              </h3>
              <div className="cal-announce-list">
                {clubAnnouncements.map(ann => (
                  <div key={ann.id} className="cal-announce-card" style={{ borderLeftColor: '#d97706' }}>
                    <div className="cal-announce-card-left">
                      <div className="cal-announce-type" style={{ color: '#d97706', background: '#fef3c7' }}>
                        <FaBullhorn /> {ann.clubs?.name || 'Club'}
                      </div>
                      <h4>{ann.title}</h4>
                      <p className="cal-announce-desc">{ann.body}</p>
                    </div>
                    <div className="cal-announce-card-right">
                      <div className="cal-announce-date">{formatDate(ann.date)}</div>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}

          {managedClubs.length > 0 && (
            <button
              className="cal-v2-btn-primary"
              style={{ background: '#d97706', marginTop: '16px', display: 'flex', alignItems: 'center', gap: '6px', padding: '10px 20px', border: 'none', borderRadius: '8px', color: '#fff', fontWeight: 600, cursor: 'pointer' }}
              onClick={() => setShowAnnouncementModal(true)}
            >
              <FaBullhorn size={12} /> {L(language, 'Post Announcement', 'Publier une annonce', '发布公告')}
            </button>
          )}
        </div>
      )}

      {/* Newsletters View */}
      {view === 'newsletters' && (
        <div className="cal-announcements">
          {isMcGillEmail && (
            <div style={{ marginBottom: 24, background: 'var(--bg-secondary)', borderRadius: 12, border: '1px solid var(--border-primary)' }}>
              <div style={{ padding: '14px 16px', borderBottom: '1px solid var(--border-primary)', display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 12 }}>
                <h3 style={{ margin: 0, fontSize: '14px', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <FaNewspaper size={13} style={{ color: '#0891b2' }} />
                  {L(language, 'Newsletter Subscriptions', 'Abonnements aux infolettres', '通讯订阅')}
                </h3>
                {nlExpanded && nlSources.length > 3 && (
                  <div style={{ position: 'relative', flexShrink: 0 }}>
                    <FaSearch size={11} style={{ position: 'absolute', left: 8, top: '50%', transform: 'translateY(-50%)', color: '#999', pointerEvents: 'none' }} />
                    <input
                      type="text"
                      placeholder={L(language, 'Search…', 'Rechercher…', '搜索…')}
                      value={nlSearch}
                      onChange={e => setNlSearch(e.target.value)}
                      style={{ paddingLeft: 24, paddingRight: nlSearch ? 24 : 8, paddingTop: 5, paddingBottom: 5, fontSize: '12px', border: '1px solid var(--border-primary)', borderRadius: 6, background: 'var(--bg-primary)', color: 'var(--text-primary)', width: 140 }}
                    />
                    {nlSearch && (
                      <button onClick={() => setNlSearch('')} style={{ position: 'absolute', right: 6, top: '50%', transform: 'translateY(-50%)', background: 'none', border: 'none', cursor: 'pointer', color: '#999', padding: 0, lineHeight: 1 }}>
                        <FaTimes size={11} />
                      </button>
                    )}
                  </div>
                )}
              </div>
              {nlLoading ? (
                <p style={{ textAlign: 'center', padding: '14px', fontSize: '13px', color: 'var(--text-tertiary)' }}>
                  {L(language, 'Loading…', 'Chargement…', '加载中…')}
                </p>
              ) : filteredNlSources.length === 0 ? (
                <p style={{ textAlign: 'center', padding: '14px', fontSize: '13px', color: 'var(--text-tertiary)' }}>
                  {nlSearch
                    ? L(language, 'No results', 'Aucun résultat', '无结果')
                    : L(language, 'No newsletters available yet', 'Aucune infolettre disponible', '暂无通讯')}
                </p>
              ) : (
                <>
                  <div style={nlExpanded ? { maxHeight: 280, overflowY: 'auto' } : {}}>
                    {(nlExpanded || nlSearch ? filteredNlSources : filteredNlSources.slice(0, 3)).map(src => (
                      <div key={src.id} style={{ display: 'flex', alignItems: 'center', gap: 10, padding: '10px 16px', borderBottom: '1px solid var(--border-primary)' }}>
                        <div style={{ flex: 1, minWidth: 0 }}>
                          <div style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: 6 }}>
                            {src.logo_url && <img src={src.logo_url} alt="" style={{ width: 16, height: 16, borderRadius: 3 }} />}
                            {src.name}
                          </div>
                          <div style={{ fontSize: '11px', color: 'var(--text-tertiary)', marginTop: 2 }}>
                            {src.category}
                            {src.subscribed && !src.email_muted && <> &middot; <FaCalendarAlt size={9} style={{ verticalAlign: 'middle' }} /> {L(language, 'Calendar + emails', 'Calendrier + emails', '日历 + 邮件')}</>}
                            {src.subscribed && src.email_muted && <> &middot; <FaCalendarAlt size={9} style={{ verticalAlign: 'middle' }} /> {L(language, 'Calendar only', 'Calendrier uniquement', '仅日历')}</>}
                          </div>
                        </div>
                        <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexShrink: 0 }}>
                          {src.subscribed && (
                            <button
                              onClick={() => handleNlMuteToggle(src)}
                              title={src.email_muted ? L(language, 'Unmute emails', 'Réactiver emails', '取消静音') : L(language, 'Mute emails', 'Muet emails', '静音邮件')}
                              style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '4px 8px', fontSize: '11px', border: '1px solid var(--border-primary)', borderRadius: 6, background: src.email_muted ? 'var(--bg-tertiary)' : 'none', color: 'var(--text-tertiary)', cursor: 'pointer', opacity: src.email_muted ? 1 : 0.6 }}
                            >
                              <FaBellSlash size={10} />
                              {src.email_muted ? L(language, 'Muted', 'Muet', '已静音') : L(language, 'Mute', 'Muet', '静音')}
                            </button>
                          )}
                          <button
                            onClick={() => handleNlToggle(src)}
                            style={{ display: 'flex', alignItems: 'center', gap: 4, padding: '5px 10px', fontSize: '12px', border: '1px solid', borderColor: src.subscribed ? '#0891b2' : 'var(--border-primary)', borderRadius: 6, background: src.subscribed ? '#ecfeff' : 'none', color: src.subscribed ? '#0891b2' : 'var(--text-secondary)', cursor: 'pointer', minWidth: 88, justifyContent: 'center', fontWeight: 600 }}
                          >
                            {src.subscribed
                              ? <><FaCheck size={9} /> {L(language, 'Subscribed', 'Abonné', '已订阅')}</>
                              : L(language, 'Subscribe', "S'abonner", '订阅')}
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                  {!nlSearch && filteredNlSources.length > 3 && (
                    <button
                      onClick={() => setNlExpanded(p => !p)}
                      style={{ width: '100%', padding: '8px 16px', fontSize: '12px', background: 'none', border: 'none', borderTop: '1px solid var(--border-primary)', color: '#0891b2', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, fontWeight: 600 }}
                    >
                      {nlExpanded
                        ? L(language, '↑ Show less', '↑ Voir moins', '↑ 收起')
                        : L(language, `+ ${filteredNlSources.length - 3} more`, `+ ${filteredNlSources.length - 3} de plus`, `+ ${filteredNlSources.length - 3} 个`)}
                    </button>
                  )}
                </>
              )}
            </div>
          )}

          <h3 style={{ margin: '0 0 16px', fontSize: '15px', fontWeight: 600, color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FaCalendarAlt size={13} style={{ color: '#0891b2' }} /> {L(language, 'Upcoming Events', 'Événements à venir', '即将举行的活动')}
          </h3>
          {newsletterEvents.length === 0 ? (
            <div className="cal-empty-state">
              <FaNewspaper size={40} />
              <p>{L(language, 'No newsletter events yet. Subscribe above to see events here.', 'Aucun événement. Abonnez-vous ci-dessus pour voir les événements.', '暂无活动。在上方订阅通讯以查看活动。')}</p>
            </div>
          ) : (
            <div className="cal-announce-list">
              {newsletterEvents.map(event => {
                const days = daysUntil(event.date)
                return (
                  <div key={event.id} className="cal-announce-card" style={{ borderLeftColor: '#0891b2' }}
                    onClick={() => setPopupEvent(event)}>
                    <div className="cal-announce-card-left">
                      <div className="cal-announce-type" style={{ color: '#0891b2', background: '#ecfeff' }}>
                        <FaNewspaper /> {L(language, 'Newsletter', 'Infolettre', '通讯')}
                      </div>
                      <h4>{event.title}</h4>
                      {event.description && <p className="cal-announce-desc">{event.description}</p>}
                    </div>
                    <div className="cal-announce-card-right">
                      <div className="cal-announce-date">{formatDate(event.date)}</div>
                      <div className="cal-announce-countdown">{countdownLabel(days)}</div>
                    </div>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}

      {/* Announcement Modal */}
      {showAnnouncementModal && (
        <AnnouncementModal
          clubs={managedClubs}
          onSave={async (data) => {
            try {
              let eventId = null
              if (data.attachEvent) {
                const ev = await clubsAPI.createClubEvent(data.clubId, {
                  title: data.title,
                  date: data.eventDate,
                  time: data.eventTime || null,
                  end_time: data.eventEndTime || null,
                  location: data.eventLocation || null,
                  join_link: data.join_link || null,
                })
                eventId = ev.id || ev.event?.id || null
              }
              await clubsAPI.createClubAnnouncement(data.clubId, {
                title: data.title,
                body: data.body,
                event_id: eventId,
                join_link: data.join_link || null,
              })
              await refreshClubData()
            } catch (err) { console.error('Failed to create announcement:', err) }
            setShowAnnouncementModal(false)
          }}
          onClose={() => setShowAnnouncementModal(false)}
          language={language}
        />
      )}

      {/* Day Events Drawer */}
      {dayDrawer && (
        <DayDrawer
          date={dayDrawer.date}
          events={dayDrawer.events}
          onClose={() => setDayDrawer(null)}
          onAddEvent={handleAddFromDrawer}
          onEditEvent={handleEditFromDrawer}
          onSelectEvent={setPopupEvent}
          t={t} language={language} formatDate={formatDate}
          typeConfig={typeConfig} getEventStyle={getEventStyle}
          userEventIds={userEventIds}
        />
      )}

      {/* Single Event Popup */}
      {popupEvent && (
        <div className="cal-popup-overlay" onClick={() => setPopupEvent(null)}>
          <EventPopup
            event={popupEvent}
            onClose={() => setPopupEvent(null)}
            canEdit={userEventIds.has(popupEvent.id)}
            onEdit={() => { setEditEvent(popupEvent); setPopupEvent(null); setShowModal(true) }}
            onHide={() => {
              const ev = popupEvent
              if (ev.course_code && ev.recurrence) {
                const key = `${ev.course_code}::${ev.recurrence}::${ev.time || ''}`
                setHiddenSlotKeys(prev => new Set([...prev, key]))
              } else {
                setHiddenEventIds(prev => new Set([...prev, ev.id]))
              }
              setPopupEvent(null)
            }}
            t={t} language={language} formatDate={formatDate}
            typeConfig={typeConfig} getEventStyle={getEventStyle}
          />
        </div>
      )}

      {/* Add/Edit Modal */}
      {showModal && (
        <EventModal
          event={editEvent ? editEvent : preselectedDate ? { date: preselectedDate } : null}
          onSave={handleSaveEvent}
          onDelete={handleDeleteEvent}
          onClose={() => { setShowModal(false); setEditEvent(null); setPreselectedDate(null) }}
          t={t} notifPrefs={notifPrefs} user={user} language={language}
          managedClubs={managedClubs}
          customTypes={customTypes} onAddCustomType={handleAddCustomType}
        />
      )}

      {/* Calendar Import Guide (Google / Apple / Outlook) */}
      {showGCalGuide && (() => {
        const guides = {
          google: {
            accent: '#1a73e8',
            icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="white"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>,
            title: t('calendar.exportGoogleHelp'),
            steps: [
              <>{L(language, 'Open', 'Ouvrez', '打开')} <a href="https://calendar.google.com" target="_blank" rel="noopener noreferrer">calendar.google.com</a></>,
              L(language, 'Click the Settings icon → Settings', "Cliquez sur l'icône Paramètres → Paramètres", '点击设置图标 → 设置'),
              L(language, 'Select "Import & export" from the sidebar', 'Sélectionnez "Importer et exporter" dans la barre latérale', '从侧边栏选择"导入与导出"'),
              L(language, 'Click "Import" and choose the downloaded .ics file', "Cliquez sur \"Importer\" et choisissez le fichier .ics téléchargé", '点击"导入"并选择已下载的.ics文件'),
              L(language, 'Select your calendar and click "Import"', "Sélectionnez votre calendrier et cliquez sur \"Importer\"", '选择您的日历并点击"导入"'),
            ],
            openHref: 'https://calendar.google.com/calendar/r/settings/export',
            openLabel: L(language, 'Open Google Calendar', 'Ouvrir Google Agenda', '打开Google日历'),
          },
          apple: {
            accent: '#000000',
            icon: <FaApple size={22} color="white" />,
            title: t('calendar.exportAppleHelp'),
            steps: [
              L(language, 'On a Mac: double-click the downloaded .ics file to open it in Calendar', 'Sur Mac : double-cliquez sur le fichier .ics téléchargé pour l\'ouvrir dans Calendrier', '在Mac上：双击下载的.ics文件以在日历中打开'),
              L(language, 'On iPhone/iPad: open the file from Downloads and tap it', 'Sur iPhone/iPad : ouvrez le fichier depuis Téléchargements et appuyez dessus', '在iPhone/iPad上：从"下载"中打开该文件并点击'),
              L(language, 'Choose which calendar to add the events to', 'Choisissez le calendrier où ajouter les événements', '选择要添加事件的日历'),
              L(language, 'Tap or click "Add" / "OK" to finish importing', 'Appuyez ou cliquez sur "Ajouter" / "OK" pour terminer l\'importation', '点击"添加"/"好"以完成导入'),
            ],
          },
          outlook: {
            accent: '#0078d4',
            icon: <FaWindows size={20} color="white" />,
            title: t('calendar.exportOutlookHelp'),
            steps: [
              <>{L(language, 'On the web: go to', 'Sur le web : allez sur', '在网页上：访问')} <a href="https://outlook.live.com/calendar/0/addcalendar" target="_blank" rel="noopener noreferrer">outlook.live.com</a></>,
              L(language, 'Click "Add calendar" → "Upload from file"', 'Cliquez sur "Ajouter un calendrier" → "Importer un fichier"', '点击"添加日历" → "从文件上传"'),
              L(language, 'Desktop app: File → Open & Export → Import/Export instead', 'Application de bureau : Fichier → Ouvrir et exporter → Importer/Exporter', '桌面应用：文件 → 打开和导出 → 导入/导出'),
              L(language, 'Select the downloaded .ics file and follow the prompts', 'Sélectionnez le fichier .ics téléchargé et suivez les instructions', '选择已下载的.ics文件并按照提示操作'),
            ],
            openHref: 'https://outlook.live.com/calendar/0/addcalendar',
            openLabel: L(language, 'Open Outlook', 'Ouvrir Outlook', '打开Outlook'),
          },
        }
        const current = guides[guideProvider]
        return (
          <div className="modal-overlay cal-gcal-overlay" onClick={() => setShowGCalGuide(false)}>
            <div className="cal-gcal-modal" onClick={e => e.stopPropagation()}>
              <div className="cal-guide-tabs">
                {Object.keys(guides).map(key => (
                  <button
                    key={key}
                    className={`cal-guide-tab ${guideProvider === key ? 'active' : ''}`}
                    style={guideProvider === key ? { color: guides[key].accent, borderColor: guides[key].accent } : {}}
                    onClick={() => setGuideProvider(key)}
                  >
                    {key === 'google' ? 'Google' : key === 'apple' ? 'Apple' : 'Outlook'}
                  </button>
                ))}
              </div>
              <div className="cal-gcal-modal__header">
                <div className="cal-gcal-modal__icon" style={{ background: current.accent }}>
                  {current.icon}
                </div>
                <div>
                  <h3 className="cal-gcal-modal__title">{current.title}</h3>
                  <p className="cal-gcal-modal__subtitle">{L(language, 'Your .ics file has been downloaded', 'Votre fichier .ics a été téléchargé', '您的.ics文件已下载')}</p>
                </div>
                <button className="cal-gcal-modal__close" onClick={() => setShowGCalGuide(false)}><FaTimes /></button>
              </div>
              <ol className="cal-gcal-steps">
                {current.steps.map((step, i) => (
                  <li key={i}><span className="cal-gcal-step-num">{i + 1}</span>{step}</li>
                ))}
              </ol>
              <div className="cal-gcal-modal__actions">
                {current.openHref && (
                  <a className="cal-gcal-modal__open-btn" style={{ background: current.accent }} href={current.openHref} target="_blank" rel="noopener noreferrer">
                    <FaExternalLinkAlt size={12} /> {current.openLabel}
                  </a>
                )}
                <button className="cal-gcal-modal__done-btn" onClick={() => setShowGCalGuide(false)}>
                  {L(language, 'Done', 'Terminé', '完成')}
                </button>
              </div>
            </div>
          </div>
        )
      })()}

      {/* Bulk Delete Modal */}
      {showBulkDelete && (
        <BulkDeleteModal
          userEvents={userEvents}
          allEvents={allEvents}
          onHide={handleBulkHide}
          hiddenSlotKeys={hiddenSlotKeys}
          onUnhideAll={() => { handleBulkUnhideAll(); setHiddenEventIds(new Set()); setMutedClubIds(new Set()) }}
          onClose={() => setShowBulkDelete(false)}
          language={language}
          onEditSlot={handleEditSlot}
          serverClubEvents={serverClubEvents}
          mutedClubIds={mutedClubIds}
          onToggleMuteClub={(clubId) => setMutedClubIds(prev => {
            const next = new Set(prev)
            if (next.has(clubId)) next.delete(clubId)
            else next.add(clubId)
            return next
          })}
          hiddenEventIds={hiddenEventIds}
          onToggleHideEvent={(eventId) => setHiddenEventIds(prev => {
            const next = new Set(prev)
            if (next.has(eventId)) next.delete(eventId)
            else next.add(eventId)
            return next
          })}
          typeConfig={typeConfig}
          getEventStyle={getEventStyle}
        />
      )}
    </div>
  )
}
