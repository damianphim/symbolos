import React from 'react'
import { toDateStr } from './calendarConstants'

/**
 * Compact, tappable month grid for phones.
 *
 * The mobile agenda (MobileAgenda) hides every day without events, so with a
 * light schedule it collapses to essentially "today" and there is no calendar
 * to scan or to reach an arbitrary date from. This restores the month view the
 * desktop grid gives, but readable at 360px: day numbers with small event dots
 * rather than event text crammed into cells. Tapping a day selects it; the
 * caller renders that day's events below (grid + agenda, the iOS/Google phone
 * pattern).
 */
export default function MobileMonthGrid({
  cells,
  year,
  month,
  DAYS,
  eventsByDate,
  selectedStr,
  todayStr,
  onSelectDay,
  typeConfig,
  getEventStyle,
}) {
  return (
    <div className="cal-mgrid">
      <div className="cal-mgrid__weekdays">
        {DAYS.map((d, i) => (
          <span key={i} className="cal-mgrid__weekday">{d.slice(0, 1)}</span>
        ))}
      </div>
      <div className="cal-mgrid__grid">
        {cells.map((day, idx) => {
          if (!day) return <span key={`empty-${idx}`} className="cal-mgrid__cell cal-mgrid__cell--empty" />
          const dateStr = toDateStr(year, month, day)
          const dayEvents = eventsByDate[dateStr] || []
          const isToday = dateStr === todayStr
          const isSelected = dateStr === selectedStr
          return (
            <button
              key={dateStr}
              type="button"
              className={`cal-mgrid__cell${isToday ? ' is-today' : ''}${isSelected ? ' is-selected' : ''}`}
              onClick={() => onSelectDay(day)}
              aria-pressed={isSelected}
              aria-current={isToday ? 'date' : undefined}
            >
              <span className="cal-mgrid__num">{day}</span>
              {dayEvents.length > 0 && (
                <span className="cal-mgrid__dots" aria-hidden="true">
                  {dayEvents.slice(0, 3).map(e => {
                    const style = getEventStyle(e, typeConfig)
                    return (
                      <span
                        key={e.id}
                        className="cal-mgrid__dot"
                        style={{ background: style.color }}
                      />
                    )
                  })}
                </span>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
