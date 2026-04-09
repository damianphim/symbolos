import React from 'react'
import { FaTimes, FaBell, FaCalendarAlt, FaEdit, FaExternalLinkAlt } from 'react-icons/fa'
import { L, daysUntil } from './calendarConstants'
import { googleCalendarUrl } from './calendarUtils'
import { EyeOffIcon } from './BulkDeleteModal'

export default function EventPopup({ event, onClose, onEdit, canEdit, onHide, t, language, formatDate, typeConfig, getEventStyle }) {
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
          {event.time && ` ${L(language, 'at', 'à', '于')} ${event.time}${event.end_time ? `–${event.end_time}` : ''}`}
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
      <div className="cal-event-popup-actions">
        {canEdit && (
          <button className="cal-event-popup-edit" onClick={onEdit}>
            <FaEdit /> {t('calendar.editEvent')}
          </button>
        )}
        <button className="cal-event-popup-hide" onClick={onHide}>
          <EyeOffIcon /> {L(language, 'Hide from calendar', 'Masquer du calendrier', '从日历隐藏')}
        </button>
      </div>
    </div>
  )
}
