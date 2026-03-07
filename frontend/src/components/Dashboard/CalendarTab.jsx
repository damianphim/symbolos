import React, { useState, useEffect, useMemo, useCallback } from 'react'
import {
  FaChevronLeft, FaChevronRight, FaPlus, FaTimes, FaBell,
  FaCalendarAlt, FaBullhorn, FaGraduationCap, FaUser, FaExternalLinkAlt, FaDownload,
  FaTrash, FaEdit, FaCheck, FaClipboardList, FaUsers, FaBook, FaLayerGroup, FaClock, FaExclamationTriangle,
  FaChevronDown, FaChevronUp
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import { useTimezone } from '../../contexts/TimezoneContext'
import useNotificationPrefs from '../../hooks/useNotificationPrefs'
import { scheduleNotification, queueExamNotification, deleteEvent as deleteEventAPI } from '../../services/notificationService'
import { lookupExam, formatExamTime } from '../../utils/examSchedule2026'
import currentCoursesAPI from '../../lib/currentCoursesAPI'
// FIX #16: Import Supabase calendar API instead of reading/writing localStorage
import { getEvents, saveEvent, deleteEvent as deleteEventDB, migrateLocalStorageEvents, expandRecurringEvents } from '../../lib/calendarAPI'
import './CalendarTab.css'

// ── McGill Academic Dates 2025–26 ────────────────────────────────
const MCGILL_ACADEMIC_DATES = [
  { id: 'f-01', title: 'Deadline to Register (avoid penalty)',         date: '2025-08-14', type: 'academic', category: 'Fall 2025' },
  { id: 'f-02', title: 'Fall Classes Begin',                           date: '2025-08-27', type: 'academic', category: 'Fall 2025' },
  { id: 'f-03', title: 'Labour Day (no classes)',                      date: '2025-09-01', type: 'academic', category: 'Fall 2025' },
  { id: 'f-04', title: 'Deadline to Cancel Registration',              date: '2025-08-31', type: 'academic', category: 'Fall 2025' },
  { id: 'f-05', title: 'Add/Drop Deadline',                            date: '2025-09-09', type: 'academic', category: 'Fall 2025' },
  { id: 'f-06', title: 'Withdrawal with Refund Deadline',              date: '2025-09-16', type: 'academic', category: 'Fall 2025' },
  { id: 'f-07', title: 'Thanksgiving (no classes)',                    date: '2025-10-13', type: 'academic', category: 'Fall 2025' },
  { id: 'f-08', title: 'Fall Reading Break Begins',                    date: '2025-10-14', type: 'academic', category: 'Fall 2025' },
  { id: 'f-09', title: 'Fall Reading Break Ends',                      date: '2025-10-17', type: 'academic', category: 'Fall 2025' },
  { id: 'f-10', title: 'Withdrawal WITHOUT Refund Deadline',           date: '2025-10-28', type: 'academic', category: 'Fall 2025' },
  { id: 'f-11', title: 'Fall Classes End / Makeup Day (Monday sched)', date: '2025-12-03', type: 'academic', category: 'Fall 2025' },
  { id: 'f-12', title: 'Study Day',                                    date: '2025-12-04', type: 'academic', category: 'Fall 2025' },
  { id: 'f-13', title: 'Fall Exams Begin',                             date: '2025-12-05', type: 'academic', category: 'Fall 2025' },
  { id: 'f-14', title: 'Holiday Break Begins (offices closed)',        date: '2025-12-25', type: 'academic', category: 'Fall 2025' },
  { id: 'f-15', title: 'Fall Exams End',                               date: '2025-12-19', type: 'academic', category: 'Fall 2025' },
  { id: 'w-01', title: 'Deadline to Cancel Registration',              date: '2025-12-31', type: 'academic', category: 'Winter 2026' },
  { id: 'w-02', title: 'Holiday Break Ends',                           date: '2026-01-02', type: 'academic', category: 'Winter 2026' },
  { id: 'w-03', title: 'Winter Classes Begin',                         date: '2026-01-05', type: 'academic', category: 'Winter 2026' },
  { id: 'w-04', title: 'Add/Drop Deadline',                            date: '2026-01-20', type: 'academic', category: 'Winter 2026' },
  { id: 'w-05', title: 'Withdrawal with Refund Deadline',              date: '2026-01-27', type: 'academic', category: 'Winter 2026' },
  { id: 'w-06', title: 'Winter Reading Break Begins',                  date: '2026-03-02', type: 'academic', category: 'Winter 2026' },
  { id: 'w-07', title: 'Winter Reading Break Ends',                    date: '2026-03-06', type: 'academic', category: 'Winter 2026' },
  { id: 'w-08', title: 'Withdrawal WITHOUT Refund Deadline',           date: '2026-03-10', type: 'academic', category: 'Winter 2026' },
  { id: 'w-09', title: 'Good Friday (no classes)',                     date: '2026-04-03', type: 'academic', category: 'Winter 2026' },
  { id: 'w-10', title: 'Easter Monday (no classes)',                   date: '2026-04-06', type: 'academic', category: 'Winter 2026' },
  { id: 'w-11', title: 'Winter Classes End / Makeup Day (Friday sched)', date: '2026-04-14', type: 'academic', category: 'Winter 2026' },
  { id: 'w-12', title: 'Study Day',                                    date: '2026-04-15', type: 'academic', category: 'Winter 2026' },
  { id: 'w-13', title: 'Winter Exams Begin',                           date: '2026-04-16', type: 'academic', category: 'Winter 2026' },
  { id: 'w-14', title: 'Winter Exams End',                             date: '2026-04-30', type: 'academic', category: 'Winter 2026' },
]

const CLUB_CATEGORY_COLORS = {
  'Academic':                 { color: '#2563eb', bg: '#dbeafe' },
  'Engineering & Technology': { color: '#7c3aed', bg: '#ede9fe' },
  'Professional':             { color: '#0f766e', bg: '#ccfbf1' },
  'Debate & Politics':        { color: '#b45309', bg: '#fef3c7' },
  'Athletics & Recreation':   { color: '#16a34a', bg: '#dcfce7' },
  'Arts & Culture':           { color: '#db2777', bg: '#fce7f3' },
  'Environment':              { color: '#15803d', bg: '#dcfce7' },
  'Health & Wellness':        { color: '#0284c7', bg: '#e0f2fe' },
  'Community Service':        { color: '#ea580c', bg: '#ffedd5' },
  'International':            { color: '#0891b2', bg: '#cffafe' },
  'Science':                  { color: '#4f46e5', bg: '#e0e7ff' },
  'Social':                   { color: '#dc2626', bg: '#fee2e2' },
  'Spiritual & Religious':    { color: '#a16207', bg: '#fefce8' },
}

function getClubEventStyle(event) {
  if (event.category && CLUB_CATEGORY_COLORS[event.category]) {
    return CLUB_CATEGORY_COLORS[event.category]
  }
  return { color: '#d97706', bg: '#fef3c7' }
}

const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December']
const MONTHS_FR = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
const DAYS_EN = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
const DAYS_FR = ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam']

function getDaysInMonth(year, month) { return new Date(year, month + 1, 0).getDate() }
function getFirstDayOfMonth(year, month) { return new Date(year, month, 1).getDay() }
function toDateStr(year, month, day) {
  return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
}
function daysUntil(dateStr) {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  return Math.round((new Date(dateStr + 'T00:00:00') - today) / 86400000)
}

// ── Event Modal ───────────────────────────────────────────────────
function EventModal({ event, onSave, onDelete, onClose, t, notifPrefs, user }) {
  const today = new Date().toLocaleDateString('en-CA', {
    timeZone: localStorage.getItem('timezone') || Intl.DateTimeFormat().resolvedOptions().timeZone
  })

  const defaultNotif = () => ({
    notifyEnabled: notifPrefs.method !== 'none',
    notifySameDay: notifPrefs.timing.sameDay,
    notify1Day:    notifPrefs.timing.oneDay,
    notify7Days:   notifPrefs.timing.oneWeek,
  })

  const [form, setForm] = useState(() => ({
    title:       event?.title       || '',
    date:        event?.date        || today,
    time:        event?.time        || '',
    type:        event?.type        || 'personal',
    category:    event?.category    || '',
    description: event?.description || '',
    ...(event?.id && !event?.titleKey
      ? {
          notifyEnabled: event.notifyEnabled ?? true,
          notifySameDay: event.notifySameDay ?? false,
          notify1Day:    event.notify1Day    ?? true,
          notify7Days:   event.notify7Days   ?? true,
        }
      : defaultNotif()
    ),
  }))

  const isEdit = !!event?.id && !event?.titleKey
  const typeConfig = {
    personal: { color: '#059669', bg: '#ecfdf5', label: t('calendar.personalEvents') },
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.title.trim() || !form.date) return
    onSave({ ...form, id: event?.id || `user-${Date.now()}` })
  }

  const f = (key) => (val) => setForm(p => ({ ...p, [key]: val }))
  const toggle = (key) => setForm(p => ({ ...p, [key]: !p[key] }))

  return (
    <div className="cal-modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="cal-modal">
        <div className="cal-modal-header">
          <h3>{isEdit ? t('calendar.editEventTitle') : t('calendar.addEventTitle')}</h3>
          <button className="cal-modal-close" onClick={onClose}><FaTimes /></button>
        </div>
        <form className="cal-modal-body" onSubmit={handleSubmit}>
          <div className="cal-field">
            <label>{t('calendar.eventTitle')} *</label>
            <input type="text" value={form.title} onChange={e => f('title')(e.target.value)} placeholder={t('calendar.eventTitlePlaceholder')} required />
          </div>
          <div className="cal-field-row">
            <div className="cal-field">
              <label>{t('calendar.date')} *</label>
              <input type="date" value={form.date} onChange={e => f('date')(e.target.value)} required />
            </div>
            <div className="cal-field">
              <label>{t('calendar.time')}</label>
              <input type="time" value={form.time} onChange={e => f('time')(e.target.value)} />
            </div>
          </div>
          <div className="cal-field">
            <label>{t('calendar.eventType')}</label>
            <div className="cal-type-grid">
              {Object.entries(typeConfig).map(([key, cfg]) => (
                <button key={key} type="button"
                  className={`cal-type-btn ${form.type === key ? 'selected' : ''}`}
                  style={form.type === key ? { borderColor: cfg.color, background: cfg.bg, color: cfg.color } : {}}
                  onClick={() => f('type')(key)}>
                  {cfg.label}
                </button>
              ))}
            </div>
          </div>
          <div className="cal-field">
            <label>{t('calendar.groupCategory')}</label>
            <input type="text" value={form.category} onChange={e => f('category')(e.target.value)} placeholder={t('calendar.groupPlaceholder')} />
          </div>
          <div className="cal-field">
            <label>{t('calendar.description')}</label>
            <textarea value={form.description} onChange={e => f('description')(e.target.value)} rows={2} placeholder={t('calendar.descPlaceholder')} />
          </div>
          <div className="cal-section-divider"><FaBell /> {t('calendar.reminders')}</div>
          <div className="cal-field">
            <label className="cal-checkbox-label cal-notif-master">
              <input type="checkbox" checked={form.notifyEnabled} onChange={() => toggle('notifyEnabled')} />
              <span className={`cal-notif-toggle ${form.notifyEnabled ? 'on' : 'off'}`}>
                {form.notifyEnabled ? t('calendar.notifOn') : t('calendar.notifOff')}
              </span>
              {t('calendar.enableNotifications')}
            </label>
          </div>
          {form.notifyEnabled && (
            <div className="cal-field">
              <label>{t('calendar.whenToRemind')}</label>
              <div className="cal-notify-row cal-notify-wrap">
                {[
                  { key: 'notifySameDay', label: t('calendar.remindSameDay') },
                  { key: 'notify1Day',    label: t('calendar.remind1Day') },
                  { key: 'notify7Days',   label: t('calendar.remind7Days') },
                ].map(({ key, label }) => (
                  <label key={key} className={`cal-timing-chip ${form[key] ? 'active' : ''}`}>
                    <input type="checkbox" checked={form[key]} onChange={() => toggle(key)} />
                    {form[key] && <FaCheck size={9} />} {label}
                  </label>
                ))}
              </div>
            </div>
          )}
          <div className="cal-modal-actions">
            {isEdit && (
              <button type="button" className="cal-btn-danger" onClick={() => onDelete(event.id)}>
                <FaTrash /> {t('calendar.delete')}
              </button>
            )}
            <div className="cal-modal-actions-right">
              <button type="button" className="cal-btn-secondary" onClick={onClose}>{t('calendar.cancel')}</button>
              <button type="submit" className="cal-btn-primary">
                <FaCheck /> {isEdit ? t('calendar.saveChanges') : t('calendar.addEvent')}
              </button>
            </div>
          </div>
        </form>
      </div>

    </div>
  )
}

// ── Single Event Popup ────────────────────────────────────────────
function EventPopup({ event, onClose, onEdit, canEdit, t, language, formatDate, typeConfig, getEventStyle }) {
  const style = getEventStyle(event, typeConfig)
  const days = daysUntil(event.date)
  const countdownText = days < 0
    ? `${Math.abs(days)}${t('calendar.daysAgo')}`
    : days === 0 ? t('calendar.today2')
    : `${t('calendar.inDays')} ${days}${t('calendar.inDaysSuffix')}`

  return (
    <div className="cal-event-popup">
      <div className="cal-event-popup-header" style={{ borderColor: style.color }}>
        <div className="cal-event-popup-type" style={{ color: style.color, background: style.bg }}>
          {style.icon} {style.label}
        </div>
        <button className="cal-event-popup-close" onClick={onClose}><FaTimes /></button>
      </div>
      <div className="cal-event-popup-body">
        <h4>{event.title}</h4>
        {event.category && <div className="cal-event-popup-cat">{event.category}</div>}
        <div className="cal-event-popup-date">
          <FaCalendarAlt />
          {formatDate(event.date)}
          {event.time && ` ${language === 'fr' ? 'à' : 'at'} ${event.time}${event.end_time ? `–${event.end_time}` : ''}`}
          <span className="cal-event-popup-countdown" style={{ color: days < 0 ? '#9ca3af' : days <= 7 ? '#f59e0b' : style.color }}>
            {countdownText}
          </span>
        </div>
        {event.location && (
          <div className="cal-event-popup-location">📍 {event.location}</div>
        )}
        {event.description && <p className="cal-event-popup-desc">{event.description}</p>}
        {event.notifyEnabled && (
          <div className="cal-event-popup-notif">
            <FaBell size={11} />
            {[
              event.notifySameDay && t('calendar.remindSameDay'),
              event.notify1Day    && t('calendar.remind1Day'),
              event.notify7Days   && t('calendar.remind7Days'),
            ].filter(Boolean).join(', ')}
          </div>
        )}
      </div>
      <div className="cal-event-popup-gcal">
        <a
          className="cal-event-popup-gcal-btn"
          href={googleCalendarUrl(event)}
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaExternalLinkAlt size={10} /> {t('calendar.addToGoogle')}
        </a>
      </div>
      {canEdit && (
        <button className="cal-event-popup-edit" onClick={onEdit}>
          <FaEdit /> {t('calendar.editEvent')}
        </button>
      )}

    </div>
  )
}

// ── Day Events Drawer ─────────────────────────────────────────────
function DayDrawer({ date, events, onClose, onAddEvent, onEditEvent, onSelectEvent, t, language, formatDate, typeConfig, getEventStyle, userEventIds }) {
  const [expanded, setExpanded] = useState(null)

  return (
    <div className="cal-day-drawer-overlay" onClick={onClose}>
      <div className="cal-day-drawer" onClick={e => e.stopPropagation()}>
        <div className="cal-day-drawer__header">
          <div className="cal-day-drawer__title">
            <span className="cal-day-drawer__date">{formatDate(date)}</span>
            <span className="cal-day-drawer__count">{events.length} event{events.length !== 1 ? 's' : ''}</span>
          </div>
          <div className="cal-day-drawer__actions">
            <button className="cal-day-drawer__add-btn" onClick={onAddEvent}>
              <FaPlus size={11} /> {t('calendar.addEvent')}
            </button>
            <button className="cal-day-drawer__close" onClick={onClose}><FaTimes /></button>
          </div>
        </div>
        <div className="cal-day-drawer__list">
          {events.map(event => {
            const style = getEventStyle(event, typeConfig)
            const isEditable = userEventIds.has(event.id)
            const isExpanded = expanded === event.id
            return (
              <div key={event.id} className="cal-day-drawer__item" style={{ borderLeftColor: style.color }}>
                <div className="cal-day-drawer__item-header" onClick={() => setExpanded(isExpanded ? null : event.id)}>
                  <div className="cal-day-drawer__item-left">
                    <span className="cal-day-drawer__item-type" style={{ color: style.color, background: style.bg }}>
                      {style.icon} {style.label}
                    </span>
                    <span className="cal-day-drawer__item-title">{event.title}</span>
                  </div>
                  <div className="cal-day-drawer__item-right">
                    {event.time && (
                      <span className="cal-day-drawer__item-time">
                        {event.time}{event.end_time ? `–${event.end_time}` : ''}
                      </span>
                    )}
                    {isEditable && !event._isRecurringOccurrence && (
                      <button className="cal-day-drawer__edit-btn" onClick={e => { e.stopPropagation(); onEditEvent(event) }}>
                        <FaEdit size={11} />
                      </button>
                    )}
                    {isExpanded ? <FaChevronUp size={11} /> : <FaChevronDown size={11} />}
                  </div>
                </div>
                {isExpanded && (
                  <div className="cal-day-drawer__item-body">
                    {event.location && (
                      <div className="cal-day-drawer__item-location">
                        📍 {event.location}
                      </div>
                    )}
                    {event.category && <div className="cal-day-drawer__item-cat">{event.category}</div>}
                    {event.description && <p className="cal-day-drawer__item-desc">{event.description}</p>}
                    {event.notifyEnabled && (
                      <div className="cal-event-popup-notif">
                        <FaBell size={10} />
                        {[
                          event.notifySameDay && t('calendar.remindSameDay'),
                          event.notify1Day    && t('calendar.remind1Day'),
                          event.notify7Days   && t('calendar.remind7Days'),
                        ].filter(Boolean).join(', ')}
                      </div>
                    )}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      </div>

    </div>
  )
}

// ── Main ──────────────────────────────────────────────────────────


// ── Bulk Delete Modal ─────────────────────────────────────────────
const DAY_OPTIONS = [
  { value: 'weekly_monday',    label: 'Monday' },
  { value: 'weekly_tuesday',   label: 'Tuesday' },
  { value: 'weekly_wednesday', label: 'Wednesday' },
  { value: 'weekly_thursday',  label: 'Thursday' },
  { value: 'weekly_friday',    label: 'Friday' },
]
const DAY_LABELS = {
  weekly_monday:'Mon', weekly_tuesday:'Tue', weekly_wednesday:'Wed',
  weekly_thursday:'Thu', weekly_friday:'Fri', weekly_saturday:'Sat', weekly_sunday:'Sun'
}

function SlotRow({ ev, isHidden, isSelected, onToggle, onSave, language }) {
  const [editing, setEditing] = React.useState(false)
  const [day,      setDay]      = React.useState(ev.recurrence || '')
  const [timeStart,setTimeStart]= React.useState(ev.time || '')
  const [timeEnd,  setTimeEnd]  = React.useState(ev.end_time || '')
  const [saving,   setSaving]   = React.useState(false)

  const missingTime = !ev.time

  const handleSave = async () => {
    setSaving(true)
    try {
      await onSave(ev, { recurrence: day, time: timeStart, end_time: timeEnd })
      setEditing(false)
    } finally {
      setSaving(false)
    }
  }

  const slotLabel = ev.title.replace(ev.course_code || '', '').trim() || 'Slot'
  const dayLabel  = DAY_LABELS[ev.recurrence] || ev.recurrence?.replace('weekly_','') || '?'
  const hasEnd = ev.end_time && String(ev.end_time).trim()
  const timeLabel = ev.time ? (hasEnd ? ` ${ev.time}–${ev.end_time}` : ` ${ev.time}`) : ''

  if (editing) {
    return (
      <div className="cal-bulk-slot cal-bulk-slot--editing" onClick={e => e.stopPropagation()}>
        <select className="cal-bulk-edit-select" value={day} onChange={e => setDay(e.target.value)}>
          {DAY_OPTIONS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
        </select>
        <input
          className="cal-bulk-edit-time"
          type="time"
          value={timeStart}
          onChange={e => setTimeStart(e.target.value)}
          placeholder="HH:MM"
        />
        <span className="cal-bulk-edit-sep">–</span>
        <input
          className="cal-bulk-edit-time"
          type="time"
          value={timeEnd}
          onChange={e => setTimeEnd(e.target.value)}
          placeholder="HH:MM"
        />
        <button className="cal-bulk-edit-save" onClick={handleSave} disabled={saving}>
          {saving ? '…' : <FaCheck size={11}/>}
        </button>
        <button className="cal-bulk-edit-cancel" onClick={() => setEditing(false)}>
          <FaTimes size={11}/>
        </button>
      </div>
    )
  }

  return (
    <div
      className={`cal-bulk-slot${isHidden ? ' cal-bulk-slot--hidden' : ''}${missingTime ? ' cal-bulk-slot--missing' : ''}`}
      onClick={onToggle}
    >
      <input type="checkbox" readOnly checked={isSelected} className="cal-bulk-check" onClick={e => e.stopPropagation()} onChange={() => {}} />
      <span className="cal-bulk-slot__day">{dayLabel}</span>
      <span className="cal-bulk-slot__label">{slotLabel}{timeLabel}</span>
      {missingTime && <span className="cal-bulk-slot__badge cal-bulk-slot__badge--warn"><FaClock size={9}/> {language === 'fr' ? 'heure manquante' : 'no time'}</span>}
      {isHidden && !missingTime && <span className="cal-bulk-slot__badge">{language === 'fr' ? 'masqué' : 'hidden'}</span>}
      <button
        className="cal-bulk-slot__edit-btn"
        title={language === 'fr' ? 'Modifier' : 'Edit'}
        onClick={e => { e.stopPropagation(); setEditing(true) }}
      >
        <FaEdit size={10}/> {language === 'fr' ? 'Modifier' : 'Edit'}
      </button>
    </div>
  )
}

function BulkDeleteModal({ userEvents, onHide, hiddenSlotKeys, onUnhideAll, onClose, language, onEditSlot }) {
  const [selected, setSelected] = React.useState(new Set())

  const groups = React.useMemo(() => {
    const anchors = userEvents.filter(e => e.recurrence && e.course_code && !e._isRecurringOccurrence)
    const map = {}
    for (const ev of anchors) {
      const cc = ev.course_code || ev.category || 'Other'
      if (!map[cc]) map[cc] = {}
      const rec = ev.recurrence || 'no-recurrence'
      if (!map[cc][rec]) map[cc][rec] = []
      map[cc][rec].push(ev)
    }
    return map
  }, [userEvents])

  const slotKey = (ev) => `${ev.course_code}::${ev.recurrence}`

  const toggleKey = (key) => setSelected(prev => {
    const s = new Set(prev); s.has(key) ? s.delete(key) : s.add(key); return s
  })
  const toggleGroup = (keys) => {
    const allOn = keys.every(k => selected.has(k))
    setSelected(prev => {
      const s = new Set(prev)
      allOn ? keys.forEach(k => s.delete(k)) : keys.forEach(k => s.add(k))
      return s
    })
  }

  const hasAnything = Object.keys(groups).length > 0

  return (
    <div className="modal-overlay cal-bulk-overlay" onClick={onClose}>
      <div className="cal-bulk-modal" onClick={e => e.stopPropagation()}>
        <div className="cal-bulk-modal__header">
          <h3>{language === 'fr' ? 'Gérer les cours du calendrier' : 'Manage Calendar Classes'}</h3>
          <button className="cal-bulk-modal__close" onClick={onClose}><FaTimes /></button>
        </div>

        {!hasAnything ? (
          <p className="cal-bulk-empty">{language === 'fr' ? 'Aucun cours récurrent trouvé.' : 'No recurring class slots found.'}</p>
        ) : (
          <div className="cal-bulk-list">
            {Object.entries(groups).sort(([a],[b]) => a.localeCompare(b)).map(([courseCode, days]) => {
              const allEvs  = Object.values(days).flat()
              const allKeys = allEvs.map(slotKey)
              const allSelected = allKeys.every(k => selected.has(k))
              const hasMissing = allEvs.some(e => !e.time)
              return (
                <div key={courseCode} className="cal-bulk-course">
                  <div className="cal-bulk-course__header" onClick={() => toggleGroup(allKeys)}>
                    <input type="checkbox" readOnly checked={allSelected} className="cal-bulk-check" onChange={() => {}} />
                    <span className="cal-bulk-course__name">{courseCode}</span>
                    {hasMissing && <span className="cal-bulk-course__warn"><FaExclamationTriangle size={10}/></span>}
                    <span className="cal-bulk-course__count">{allKeys.length} slot{allKeys.length !== 1 ? 's' : ''}</span>
                  </div>
                  <div className="cal-bulk-slots">
                    {Object.entries(days).sort(([a],[b]) => a.localeCompare(b)).map(([rec, evs]) =>
                      evs.map(ev => (
                        <SlotRow
                          key={`${slotKey(ev)}-${ev.time}-${ev.recurrence}`}
                          ev={ev}
                          isHidden={hiddenSlotKeys?.has(slotKey(ev))}
                          isSelected={selected.has(slotKey(ev))}
                          onToggle={() => toggleKey(slotKey(ev))}
                          onSave={onEditSlot}
                          language={language}
                        />
                      ))
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}

        <div className="cal-bulk-modal__footer">
          <span className="cal-bulk-count">
            {(hiddenSlotKeys?.size || 0) > 0 && (
              <button className="cal-bulk-unhide-btn" onClick={onUnhideAll}>
                {language === 'fr' ? `Afficher tout (${hiddenSlotKeys?.size || 0} masqué)` : `Show all (${hiddenSlotKeys?.size || 0} hidden)`}
              </button>
            )}
          </span>
          <button className="cal-bulk-cancel-btn" onClick={onClose}>
            {language === 'fr' ? 'Fermer' : 'Close'}
          </button>
          <button
            className="cal-bulk-delete-confirm-btn"
            disabled={selected.size === 0}
            onClick={() => onHide([...selected])}
          >
            <FaLayerGroup size={11} />
            {language === 'fr' ? `Masquer (${selected.size || 0})` : `Hide (${selected.size || 0})`}
          </button>
        </div>
      </div>
    </div>
  )
}

// ── Google Calendar / ICS utilities ──────────────────────────────

function toICSDate(dateStr, timeStr) {
  // dateStr: "2026-03-15", timeStr: "14:30" (optional)
  const [y, m, d] = dateStr.split('-')
  if (timeStr) {
    const [h, min] = timeStr.split(':')
    return `${y}${m.padStart(2,'0')}${d.padStart(2,'0')}T${h.padStart(2,'0')}${(min||'00').padStart(2,'0')}00`
  }
  return `${y}${m.padStart(2,'0')}${d.padStart(2,'0')}`
}

function toICSDateUTC(dateStr, timeStr) {
  const local = toICSDate(dateStr, timeStr)
  return timeStr ? local + 'Z' : local
}

function escapeICS(str) {
  return (str || '').replace(/[\\,;]/g, c => '\\' + c).replace(/\n/g, '\\n')
}

function generateICS(events) {
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Symbolos//McGill Advisor//EN',
    'CALSCALE:GREGORIAN',
    'METHOD:PUBLISH',
    'X-WR-CALNAME:McGill Academic Calendar',
  ]

  events.forEach((ev, i) => {
    const dtstart = toICSDateUTC(ev.date, ev.time)
    const dtend = ev.end_time
      ? toICSDateUTC(ev.date, ev.end_time)
      : ev.time
        ? toICSDateUTC(ev.date, ev.time)  // same time = 1hr block handled below
        : dtstart

    lines.push('BEGIN:VEVENT')
    lines.push(`UID:symbolos-${ev.id || i}-${ev.date}@mcgill.symbolos.ca`)
    lines.push(`DTSTAMP:${toICSDateUTC(new Date().toISOString().split('T')[0], new Date().toTimeString().slice(0,5))}`)

    if (ev.time) {
      lines.push(`DTSTART:${dtstart}`)
      // If no end time, default to 1 hour later
      if (!ev.end_time) {
        const [h, min] = ev.time.split(':').map(Number)
        const endHour = String(h + 1).padStart(2,'0')
        lines.push(`DTEND:${toICSDateUTC(ev.date, endHour + ':' + String(min).padStart(2,'0'))}`)
      } else {
        lines.push(`DTEND:${toICSDateUTC(ev.date, ev.end_time)}`)
      }
    } else {
      // All-day event
      lines.push(`DTSTART;VALUE=DATE:${dtstart}`)
      lines.push(`DTEND;VALUE=DATE:${dtstart}`)
    }

    lines.push(`SUMMARY:${escapeICS(ev.title)}`)
    if (ev.description) lines.push(`DESCRIPTION:${escapeICS(ev.description)}`)
    if (ev.location)    lines.push(`LOCATION:${escapeICS(ev.location)}`)
    if (ev.category)    lines.push(`CATEGORIES:${escapeICS(ev.category)}`)
    lines.push('END:VEVENT')
  })

  lines.push('END:VCALENDAR')
  return lines.join('\r\n')
}

function downloadICS(events, filename = 'mcgill-calendar.ics') {
  const content = generateICS(events)
  const blob = new Blob([content], { type: 'text/calendar;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const a = Object.assign(document.createElement('a'), { href: url, download: filename })
  document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url)
}

function googleCalendarUrl(event) {
  const fmt = (s) => encodeURIComponent(s || '')
  const dtstart = toICSDate(event.date, event.time)
  let dates
  if (event.time) {
    const [h, min] = event.time.split(':').map(Number)
    const endHour = event.end_time
      ? event.end_time.split(':').map(Number)
      : [h + 1, min]
    const dtend = toICSDate(event.date, endHour[0] + ':' + String(endHour[1] || 0).padStart(2,'0'))
    dates = `${dtstart}/${dtend}`
  } else {
    dates = `${dtstart}/${dtstart}`
  }
  return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${fmt(event.title)}&dates=${dates}&details=${fmt(event.description)}&location=${fmt(event.location)}`
}

export default function CalendarTab({ user, clubEvents = [] }) {
  const { t, language } = useLanguage()
  const { getTodayStr, getNow } = useTimezone()
  const [notifPrefs] = useNotificationPrefs(user?.id, user?.email)

  const today = getNow()
  const MONTHS = language === 'fr' ? MONTHS_FR : MONTHS_EN
  const DAYS   = language === 'fr' ? DAYS_FR   : DAYS_EN

  const typeConfig = {
    course:   { color: '#ed1b2f', bg: '#fef2f2', icon: <FaBook />,          label: t('calendar.classEvents') },
    academic: { color: '#1d4ed8', bg: '#eff6ff', icon: <FaGraduationCap />, label: t('calendar.academicDates') },
    exam:     { color: '#7c3aed', bg: '#f5f3ff', icon: <FaClipboardList />, label: language === 'fr' ? 'Examens finaux' : 'Final Exams' },
    personal: { color: '#059669', bg: '#ecfdf5', icon: <FaUser />,          label: t('calendar.personalEvents') },
    club:     { color: '#d97706', bg: '#fef3c7', icon: <FaUsers />,         label: language === 'fr' ? 'Réunion de club' : 'Club Meeting' },
  }

  const getEventStyle = useCallback((event, cfg) => {
    if (event.type === 'club') {
      const clubStyle = getClubEventStyle(event)
      return { ...clubStyle, icon: <FaUsers />, label: language === 'fr' ? 'Réunion de club' : 'Club Meeting' }
    }
    return cfg[event.type] || cfg.personal
  }, [language])

  const [examEvents, setExamEvents] = useState([])

  // FIX #16: userEvents now lives in Supabase, not localStorage.
  // isLoadingEvents shows a spinner while the initial fetch is in flight.
  const [userEvents, setUserEvents]       = useState([])
  const [isLoadingEvents, setIsLoadingEvents] = useState(true)

  // ── Load exam schedule from current courses ─────────────────────
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
          // notification fields
          notifyEnabled: true,
          notifySameDay: notifPrefs.timing.sameDay,
          notify1Day:    notifPrefs.timing.oneDay,
          notify7Days:   notifPrefs.timing.oneWeek,
        })
      })
      setExamEvents(events)

      // ── Auto-queue exam notifications (opt-out via Settings) ────
      // Skip entirely if user disabled notifications or turned off exam type
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
          // Only queue future exams
          if (ev.date < today) continue
          try {
            await queueExamNotification(ev, user.id, user.email)
          } catch (err) {
            // Non-fatal — exam still shows on calendar
            console.warn(`Could not queue notification for ${ev.title}:`, err)
          }
        }
      }
    }).catch(() => {})
    return () => { cancelled = true }
  }, [user?.id, notifPrefs.method, notifPrefs.eventTypes?.exam, notifPrefs.timing.sameDay, notifPrefs.timing.oneDay, notifPrefs.timing.oneWeek])

  // ── FIX #16: Load user events from Supabase on mount ───────────
  useEffect(() => {
    if (!user?.id) return
    let cancelled = false

    const load = async () => {
      try {
        // Migrate any events still in localStorage before the first fetch.
        // migrateLocalStorageEvents is idempotent — safe to call on every login.
        await migrateLocalStorageEvents(user.id)

        if (cancelled) return
        const rawEvents = await getEvents(user.id)
        if (!cancelled) setUserEvents(expandRecurringEvents(rawEvents))
      } catch (err) {
        console.error('Failed to load calendar events from Supabase:', err)
        // Fallback: try reading from localStorage so the user sees their data
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

  const formatDate = useCallback((dateStr) => {
    const [y, m, d] = dateStr.split('-')
    return `${MONTHS[parseInt(m) - 1]} ${parseInt(d)}, ${y}`
  }, [MONTHS])

  const [view, setView]               = useState('calendar')
  const [currentYear, setCurrentYear] = useState(today.getFullYear())
  const [currentMonth, setCurrentMonth] = useState(today.getMonth())
  const [filter, setFilter]           = useState({ course: true, academic: true, exam: true, personal: true, club: true })
  const [showModal, setShowModal]     = useState(false)
  const [editEvent, setEditEvent]     = useState(null)
  const [preselectedDate, setPreselectedDate] = useState(null)
  const [dayDrawer, setDayDrawer]     = useState(null)
  const [popupEvent, setPopupEvent]   = useState(null)
  const [notifSaved, setNotifSaved]   = useState(false)
  const [showExportMenu, setShowExportMenu] = useState(false)
  const [showGCalGuide, setShowGCalGuide] = useState(false)
  const [showBulkDelete, setShowBulkDelete] = useState(false)
  const [hiddenSlotKeys, setHiddenSlotKeys] = useState(new Set())

  // FIX #19: tEvent defined inside useMemo so it always captures the current
  // translation function. language is a real dependency — no eslint-disable needed.
  const allEvents = useMemo(() => {
    const tEvent = (ev) => ({
      ...ev,
      title:       ev.titleKey    ? t(ev.titleKey)    : ev.title    || '',
      category:    ev.categoryKey ? t(ev.categoryKey) : ev.category || '',
      description: ev.descKey     ? t(ev.descKey)     : ev.description || '',
    })
    // Events from syllabus have course_code set — give them type 'course' (red)
    const retypedUser = userEvents.map(ev =>
      ev.course_code && ev.recurrence ? { ...tEvent(ev), type: 'course' } : tEvent(ev)
    )
    return [
      ...MCGILL_ACADEMIC_DATES.map(tEvent),
      ...examEvents,
      ...retypedUser,
      ...clubEvents,
    ]
  }, [userEvents, examEvents, clubEvents, language, t])

  const filteredEvents = useMemo(() =>
    allEvents.filter(e => {
      if (filter[e.type] === false) return false
      if (e.course_code && e.recurrence) {
        const key = `${e.course_code}::${e.recurrence}`
        if (hiddenSlotKeys.has(key)) return false
      }
      return true
    }),
    [allEvents, filter, hiddenSlotKeys]
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

  // ── FIX #16: Save handler writes to Supabase ────────────────────
  const handleSaveEvent = async (event) => {
    const isEdit = event.id && userEvents.some(e => e.id === event.id)

    // Optimistic update — patch local state immediately so UI feels instant
    const tempId = event.id || `user-${Date.now()}`
    if (isEdit) {
      setUserEvents(prev => prev.map(e => e.id === event.id ? event : e))
    } else {
      const newEvent = { ...event, id: tempId }
      setUserEvents(prev => [...prev, newEvent])
      event = newEvent
    }

    setShowModal(false); setEditEvent(null); setPreselectedDate(null)

    // Persist to Supabase in the background
    try {
      const saved = await saveEvent(event, user.id)
      // Replace the temp id with the real UUID Supabase assigned
      if (!isEdit && saved.id && saved.id !== tempId) {
        setUserEvents(prev => prev.map(e => e.id === tempId ? { ...e, id: saved.id } : e))
        event = { ...event, id: saved.id }
      }
    } catch (err) {
      console.error('Failed to save event to Supabase:', err)
      // Revert optimistic update on failure
      if (isEdit) {
        setUserEvents(prev => prev.map(e => e.id === event.id ? editEvent : e))
      } else {
        setUserEvents(prev => prev.filter(e => e.id !== tempId))
      }
      return  // Don't try to schedule notifications if save failed
    }

    // Schedule notification if requested
    if (event.notifyEnabled) {
      try { await scheduleNotification(event, user.id, user.email) }
      catch (err) { console.error('Failed to schedule notification:', err) }
      setNotifSaved(true)
      setTimeout(() => setNotifSaved(false), 3000)
    }
  }

  // ── FIX #16: Delete handler removes from Supabase ──────────────
  const handleDeleteEvent = async (id) => {
    const deleted = userEvents.find(e => e.id === id)
    setUserEvents(prev => prev.filter(e => e.id !== id))
    setShowModal(false); setEditEvent(null); setPopupEvent(null); setDayDrawer(null)

    try {
      await deleteEventDB(id, user.id)
    } catch (err) {
      console.error('Failed to delete event from Supabase:', err)
      // Revert optimistic delete on failure
      if (deleted) setUserEvents(prev => [...prev, deleted])
    }

    // Also clean up any backend notification record
    if (user?.id && id && !id.startsWith('user-')) {
      try { await deleteEventAPI(id, user.id) }
      catch (err) { console.error('Failed to delete event from notification backend:', err) }
    }
  }


  // ── Bulk delete: remove all recurring slots for a given anchor event ──
  const handleBulkHide = (slotKeys) => {
    setHiddenSlotKeys(prev => new Set([...prev, ...slotKeys]))
    setShowBulkDelete(false)
  }

  const handleBulkUnhideAll = () => {
    setHiddenSlotKeys(new Set())
  }

  // Edit a slot's day/time — updates anchor + all occurrences in state + Supabase
  const handleEditSlot = async (anchorEv, { recurrence, time, end_time }) => {
    const oldKey = `${anchorEv.course_code}::${anchorEv.recurrence}`
    const newKey = `${anchorEv.course_code}::${recurrence}`

    // Strip _isRecurringOccurrence/_anchorId so expandRecurringEvents treats it as a fresh anchor
    const updatedAnchor = {
      ...anchorEv,
      recurrence,
      time,
      end_time,
      _isRecurringOccurrence: false,
      _anchorId: undefined,
    }

    // Re-expand the updated anchor into full weekly occurrences
    const reexpanded = expandRecurringEvents([updatedAnchor])

    setUserEvents(prev => {
      // Remove old anchor + all its occurrences
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
    if (days === 0) return language === 'fr' ? "🔴 Aujourd'hui!" : '🔴 Today!'
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
            {language === 'fr'
              ? "Certains cours n'ont pas d'heure. Cliquez sur \u00abAfficher/masquer des cours\u00bb pour les corriger."
              : 'Some classes are missing their time. Click "Show/Hide Classes" to fix them.'}
          </span>
          <button className="cal-missing-fix-btn" onClick={() => setShowBulkDelete(true)}>
            {language === 'fr' ? 'Corriger' : 'Fix now'}
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
          <button className="cal-bulk-toggle-btn" onClick={() => setShowBulkDelete(true)} title={language === 'fr' ? 'Supprimer des cours en masse' : 'Bulk delete classes'}>
            <FaLayerGroup size={12} /> {language === 'fr' ? 'Modifier les cours' : 'Edit Classes'}
          </button>
          <button className="cal-add-btn" onClick={() => { setPreselectedDate(null); setEditEvent(null); setShowModal(true) }}>
            <FaPlus /> {t('calendar.addEventBtn')}
          </button>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="cal-filter-bar">
        {Object.entries(typeConfig).map(([key, cfg]) => (
          <button key={key}
            className={`cal-filter-chip ${filter[key] ? 'active' : ''}`}
            style={filter[key] ? { borderColor: cfg.color, background: cfg.bg, color: cfg.color } : {}}
            onClick={() => setFilter(f => ({ ...f, [key]: !f[key] }))}>
            {cfg.icon} {cfg.label}
          </button>
        ))}
      </div>

      {/* FIX #16: Loading state while fetching from Supabase */}
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
                            // "COMP 251 Lecture" → "COMP251 Lec"  "Winter Reading Break" → "Winter Rdg…"
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
            {Object.entries(typeConfig).map(([key, cfg]) => (
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
        </div>
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

      {/* Single Event Popup (announcements view) */}
      {popupEvent && (
        <div className="cal-popup-overlay" onClick={() => setPopupEvent(null)}>
          <EventPopup
            event={popupEvent}
            onClose={() => setPopupEvent(null)}
            canEdit={userEventIds.has(popupEvent.id)}
            onEdit={() => { setEditEvent(popupEvent); setPopupEvent(null); setShowModal(true) }}
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
          t={t} notifPrefs={notifPrefs} user={user}
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
                <p className="cal-gcal-modal__subtitle">{language === 'fr' ? 'Votre fichier .ics a été téléchargé' : 'Your .ics file has been downloaded'}</p>
              </div>
              <button className="cal-gcal-modal__close" onClick={() => setShowGCalGuide(false)}><FaTimes /></button>
            </div>
            <ol className="cal-gcal-steps">
              <li><span className="cal-gcal-step-num">1</span>{language === 'fr' ? 'Ouvrez' : 'Open'} <a href="https://calendar.google.com" target="_blank" rel="noopener noreferrer">calendar.google.com</a></li>
              <li><span className="cal-gcal-step-num">2</span>{language === 'fr' ? "Cliquez sur l'icône ⚙️ (Paramètres) → Paramètres" : 'Click the ⚙️ (Settings) icon → Settings'}</li>
              <li><span className="cal-gcal-step-num">3</span>{language === 'fr' ? 'Sélectionnez "Importer et exporter" dans la barre latérale' : 'Select "Import & export" from the sidebar'}</li>
              <li><span className="cal-gcal-step-num">4</span>{language === 'fr' ? "Cliquez sur \"Importer\" et choisissez le fichier .ics téléchargé" : 'Click "Import" and choose the downloaded .ics file'}</li>
              <li><span className="cal-gcal-step-num">5</span>{language === 'fr' ? "Sélectionnez votre calendrier et cliquez sur \"Importer\"" : 'Select your calendar and click "Import"'}</li>
            </ol>
            <div className="cal-gcal-modal__actions">
              <a className="cal-gcal-modal__open-btn" href="https://calendar.google.com/calendar/r/settings/export" target="_blank" rel="noopener noreferrer">
                <FaExternalLinkAlt size={12} /> {language === 'fr' ? 'Ouvrir Google Agenda' : 'Open Google Calendar'}
              </a>
              <button className="cal-gcal-modal__done-btn" onClick={() => setShowGCalGuide(false)}>
                {language === 'fr' ? 'Terminé' : 'Done'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Bulk Delete Modal */}
      {showBulkDelete && (
        <BulkDeleteModal
          userEvents={userEvents}
          onHide={handleBulkHide}
          hiddenSlotKeys={hiddenSlotKeys}
          onUnhideAll={handleBulkUnhideAll}
          onClose={() => setShowBulkDelete(false)}
          language={language}
          onEditSlot={handleEditSlot}
        />
      )}
    </div>
  )
}
