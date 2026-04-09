import React, { useState, useEffect, useMemo, useCallback } from 'react'
import {
  FaChevronLeft, FaChevronRight, FaPlus, FaTimes, FaBell,
  FaCalendarAlt, FaBullhorn, FaGraduationCap, FaUser, FaExternalLinkAlt, FaDownload,
  FaTrash, FaEdit, FaCheck, FaClipboardList, FaUsers, FaBook, FaLayerGroup, FaClock, FaExclamationTriangle,
  FaStar, FaBullseye, FaNewspaper, FaSearch, FaBellSlash
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import { useTimezone } from '../../contexts/TimezoneContext'
import useNotificationPrefs from '../../hooks/useNotificationPrefs'
import { scheduleNotification, queueExamNotification, deleteEvent as deleteEventAPI } from '../../services/notificationService'
import { lookupExam, formatExamTime } from '../../utils/examSchedule2026'
import currentCoursesAPI from '../../lib/currentCoursesAPI'
import { getEvents, saveEvent, deleteEvent as deleteEventDB, migrateLocalStorageEvents, expandRecurringEvents } from '../../lib/calendarAPI'
import clubsAPI from '../../lib/clubsAPI'
import newslettersAPI from '../../lib/newslettersAPI'

import {
  MCGILL_ACADEMIC_DATES, MONTHS_EN, MONTHS_FR, MONTHS_ZH,
  DAYS_EN, DAYS_FR, DAYS_ZH,
  L, getDaysInMonth, getFirstDayOfMonth, toDateStr, daysUntil,
  getClubEventStyle,
} from './CalendarTab/calendarConstants'
import { downloadICS, googleCalendarUrl } from './CalendarTab/calendarUtils'
import EventModal from './CalendarTab/EventModal'
import EventPopup from './CalendarTab/EventPopup'
import DayDrawer from './CalendarTab/DayDrawer'
import BulkDeleteModal from './CalendarTab/BulkDeleteModal'
import AnnouncementModal from './CalendarTab/AnnouncementModal'

import './CalendarTab.css'

export default function CalendarTab({ user, authFlags, clubEvents = [], managedClubs = [] }) {
  const { t, language } = useLanguage()
  const { getTodayStr, getNow } = useTimezone()
  const [notifPrefs] = useNotificationPrefs(user?.id, user?.email)

  const today = getNow()
  const MONTHS = language === 'zh' ? MONTHS_ZH : language === 'fr' ? MONTHS_FR : MONTHS_EN
  const DAYS   = language === 'zh' ? DAYS_ZH : language === 'fr' ? DAYS_FR   : DAYS_EN

  const typeConfig = {
    course:   { color: '#ed1b2f', bg: '#fef2f2', icon: <FaBook />,          label: t('calendar.classEvents') },
    academic: { color: '#1d4ed8', bg: '#eff6ff', icon: <FaGraduationCap />, label: t('calendar.academicDates') },
    exam:     { color: '#7c3aed', bg: '#f5f3ff', icon: <FaClipboardList />, label: L(language, 'Final Exams', 'Examens finaux', '期末考试') },
    personal: { color: '#059669', bg: '#ecfdf5', icon: <FaUser />,          label: t('calendar.personalEvents') },
    club:     { color: '#d97706', bg: '#fef3c7', icon: <FaUsers />,         label: L(language, 'Club Meeting', 'Réunion de club', '社团会议') },
    newsletter: { color: '#0891b2', bg: '#ecfeff', icon: <FaNewspaper />,   label: L(language, 'Newsletter', 'Infolettre', '通讯') },
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
    currentCoursesAPI.getCurrent(user.id).then(async data => {
      if (cancelled) return
      const courses = data?.current_courses || []
      const events = []
      courses.forEach((course, idx) => {
        const exam = lookupExam(course.course_code)
        if (!exam) return
        const timeStr = exam.start ? formatExamTime(exam.start) : ''
        const endStr  = exam.end   ? formatExamTime(exam.end)   : ''
        const campusLabel = exam.campus === 'D.T.' ? 'Downtown Campus'
                          : exam.campus === 'MAC'  ? 'MacDonald Campus' : ''
        const formatLabel = exam.type === 'ONLINE' ? '(Online)' : campusLabel ? `@ ${campusLabel}` : ''
        events.push({
          id: `exam-${course.course_code}-${idx}`,
          title: `${course.course_code} – Final Exam`,
          date: exam.date,
          time: timeStr,
          type: 'exam',
          category: 'Winter 2026 Finals',
          description: [course.course_title || exam.title, timeStr && endStr ? `${timeStr} – ${endStr}` : timeStr, formatLabel].filter(Boolean).join(' · '),
          readOnly: true,
          notifyEnabled: true,
          notifySameDay: notifPrefs.timing.sameDay,
          notify1Day:    notifPrefs.timing.oneDay,
          notify7Days:   notifPrefs.timing.oneWeek,
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
            await queueExamNotification(ev, user.id, user.email)
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

  const [view, setView]               = useState('calendar')
  const [currentYear, setCurrentYear] = useState(today.getFullYear())
  const [currentMonth, setCurrentMonth] = useState(today.getMonth())
  const [filter, setFilter]           = useState({ course: true, academic: true, exam: true, personal: true, club: true, newsletter: true })
  const [showModal, setShowModal]     = useState(false)
  const [editEvent, setEditEvent]     = useState(null)
  const [preselectedDate, setPreselectedDate] = useState(null)
  const [dayDrawer, setDayDrawer]     = useState(null)
  const [popupEvent, setPopupEvent]   = useState(null)
  const [notifSaved, setNotifSaved]   = useState(false)
  const [showExportMenu, setShowExportMenu] = useState(false)
  const [showGCalGuide, setShowGCalGuide] = useState(false)
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
      title:       ev.titleKey    ? t(ev.titleKey)    : ev.title    || '',
      category:    ev.categoryKey ? t(ev.categoryKey) : ev.category || '',
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
      try { await scheduleNotification(event, user.id, user.email) }
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
          <span>
            {language === 'zh'
              ? '⚠️ 部分课程缺少时间信息'
              : language === 'fr'
              ? "Certains cours n'ont pas d'heure. Cliquez sur \u00abAfficher/masquer des cours\u00bb pour les corriger."
              : 'Some classes are missing their time. Click "Show/Hide Classes" to fix them.'}
          </span>
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
              <FaCalendarAlt /> {t('calendar.calendarView')}
            </button>
            <button className={view === 'announcements' ? 'active' : ''} onClick={() => setView('announcements')}>
              <FaBullhorn /> {t('calendar.announcements')}
              {urgentEvents.length > 0 && <span className="cal-badge">{urgentEvents.length}</span>}
            </button>
            <button className={view === 'newsletters' ? 'active' : ''} onClick={() => setView('newsletters')}>
              <FaNewspaper /> {L(language, 'Newsletters', 'Infolettres', '通讯')}
            </button>
          </div>
          <div className="cal-export-wrap">
            <button className="cal-export-btn" onClick={() => setShowExportMenu(p => !p)}>
              <FaDownload size={13} /> {t('calendar.exportBtn')}
            </button>
            {showExportMenu && (
              <div className="cal-export-menu">
                <button className="cal-export-item" onClick={() => { downloadICS(filteredEvents, 'mcgill-calendar.ics'); setShowExportMenu(false) }}>
                  <FaDownload size={11} /> {t('calendar.exportICS')}
                </button>
                <button className="cal-export-item cal-export-item--google" onClick={() => { downloadICS(filteredEvents, 'mcgill-calendar.ics'); setShowGCalGuide(true); setShowExportMenu(false) }}>
                  <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
                  {t('calendar.exportGoogleHelp')}
                </button>
              </div>
            )}
          </div>
          <button className="cal-bulk-toggle-btn" onClick={() => setShowBulkDelete(true)} title={L(language, 'Manage events', 'Gérer les événements', '管理事件')}>
            <FaLayerGroup size={12} /> {L(language, 'Edit Events', 'Modifier les événements', '编辑事件')}
          </button>
          <button className="cal-add-btn" onClick={() => { setPreselectedDate(null); setEditEvent(null); setShowModal(true) }}>
            <FaPlus /> {t('calendar.addEventBtn')}
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="cal-filter-bar">
        {Object.entries(typeConfig).filter(([key]) => key !== 'newsletter' || isMcGillEmail).map(([key, cfg]) => (
          <button key={key}
            className={`cal-filter-chip ${filter[key] ? 'active' : ''}`}
            style={filter[key] ? { borderColor: cfg.color, background: cfg.bg, color: cfg.color } : {}}
            onClick={() => setFilter(f => ({ ...f, [key]: !f[key] }))}>
            {cfg.icon} {cfg.label}
          </button>
        ))}
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
          <div className="cal-month-nav">
            <button onClick={prevMonth}><FaChevronLeft /></button>
            <div className="cal-month-title">
              <h3>{MONTHS[currentMonth]} {currentYear}</h3>
              <button className="cal-today-btn" onClick={() => { setCurrentYear(today.getFullYear()); setCurrentMonth(today.getMonth()) }}>
                {t('calendar.todayBtn')}
              </button>
            </div>
            <button onClick={nextMonth}><FaChevronRight /></button>
          </div>
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
            ) : upcomingEvents.map(event => {
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
                })
                eventId = ev.id || ev.event?.id || null
              }
              await clubsAPI.createClubAnnouncement(data.clubId, {
                title: data.title,
                body: data.body,
                event_id: eventId,
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
        />
      )}

      {/* Google Calendar Import Guide */}
      {showGCalGuide && (
        <div className="modal-overlay cal-gcal-overlay" onClick={() => setShowGCalGuide(false)}>
          <div className="cal-gcal-modal" onClick={e => e.stopPropagation()}>
            <div className="cal-gcal-modal__header">
              <div className="cal-gcal-modal__icon">
                <svg width="28" height="28" viewBox="0 0 24 24" fill="white"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
              </div>
              <div>
                <h3 className="cal-gcal-modal__title">{t('calendar.exportGoogleHelp')}</h3>
                <p className="cal-gcal-modal__subtitle">{L(language, 'Your .ics file has been downloaded', 'Votre fichier .ics a été téléchargé', '您的.ics文件已下载')}</p>
              </div>
              <button className="cal-gcal-modal__close" onClick={() => setShowGCalGuide(false)}><FaTimes /></button>
            </div>
            <ol className="cal-gcal-steps">
              <li><span className="cal-gcal-step-num">1</span>{L(language, 'Open', 'Ouvrez', '打开')} <a href="https://calendar.google.com" target="_blank" rel="noopener noreferrer">calendar.google.com</a></li>
              <li><span className="cal-gcal-step-num">2</span>{L(language, 'Click the ⚙️ (Settings) icon → Settings', "Cliquez sur l'icône ⚙️ (Paramètres) → Paramètres", '点击⚙️（设置）图标 → 设置')}</li>
              <li><span className="cal-gcal-step-num">3</span>{L(language, 'Select "Import & export" from the sidebar', 'Sélectionnez "Importer et exporter" dans la barre latérale', '从侧边栏选择"导入与导出"')}</li>
              <li><span className="cal-gcal-step-num">4</span>{L(language, 'Click "Import" and choose the downloaded .ics file', "Cliquez sur \"Importer\" et choisissez le fichier .ics téléchargé", '点击"导入"并选择已下载的.ics文件')}</li>
              <li><span className="cal-gcal-step-num">5</span>{L(language, 'Select your calendar and click "Import"', "Sélectionnez votre calendrier et cliquez sur \"Importer\"", '选择您的日历并点击"导入"')}</li>
            </ol>
            <div className="cal-gcal-modal__actions">
              <a className="cal-gcal-modal__open-btn" href="https://calendar.google.com/calendar/r/settings/export" target="_blank" rel="noopener noreferrer">
                <FaExternalLinkAlt size={12} /> {L(language, 'Open Google Calendar', 'Ouvrir Google Agenda', '打开Google日历')}
              </a>
              <button className="cal-gcal-modal__done-btn" onClick={() => setShowGCalGuide(false)}>
                {L(language, 'Done', 'Terminé', '完成')}
              </button>
            </div>
          </div>
        </div>
      )}

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
