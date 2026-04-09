import React from 'react'
import { FaTimes, FaPlus, FaChevronRight, FaEdit } from 'react-icons/fa'

export default function DayDrawer({ date, events, onClose, onAddEvent, onEditEvent, onSelectEvent, t, language, formatDate, typeConfig, getEventStyle, userEventIds }) {
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
            return (
              <div key={event.id} className="cal-day-drawer__item" style={{ borderLeftColor: style.color, cursor: 'pointer' }}
                onClick={() => onSelectEvent(event)}>
                <div className="cal-day-drawer__item-header">
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
                    <FaChevronRight size={11} style={{ color: 'var(--text-tertiary, #9ca3af)' }} />
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
