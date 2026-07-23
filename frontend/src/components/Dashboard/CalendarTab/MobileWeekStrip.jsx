import React from 'react'
import { toDateStr } from './calendarConstants'

/**
 * Horizontal week selector for phones — the week-granularity counterpart to
 * MobileMonthGrid. Seven day cells (weekday letter, date, event dots), today
 * ringed and the selected day filled. Tapping a day selects it; the caller
 * renders that day's events in the agenda below (strip + agenda, mirroring the
 * month view). Works with Date objects (same shape as weekDates) so a week can
 * straddle a month boundary without special-casing.
 */
export default function MobileWeekStrip({
  weekDates,
  DAYS,
  eventsByDate,
  selectedStr,
  todayStr,
  onSelectDay,
  typeConfig,
  getEventStyle,
}) {
  return (
    <div className="cal-wstrip">
      {weekDates.map(date => {
        const dateStr = toDateStr(date.getFullYear(), date.getMonth(), date.getDate())
        const dayEvents = eventsByDate[dateStr] || []
        const isToday = dateStr === todayStr
        const isSelected = dateStr === selectedStr
        return (
          <button
            key={dateStr}
            type="button"
            className={`cal-wstrip__cell${isToday ? ' is-today' : ''}${isSelected ? ' is-selected' : ''}`}
            onClick={() => onSelectDay(date)}
            aria-pressed={isSelected}
            aria-current={isToday ? 'date' : undefined}
          >
            <span className="cal-wstrip__weekday">{DAYS[date.getDay()].slice(0, 1)}</span>
            <span className="cal-wstrip__num">{date.getDate()}</span>
            {/* Always rendered (empty when no events) so every cell reserves the
                same dot-row height and the numbers stay aligned across the row. */}
            <span className="cal-wstrip__dots" aria-hidden="true">
              {dayEvents.slice(0, 3).map(e => {
                const style = getEventStyle(e, typeConfig)
                return (
                  <span
                    key={e.id}
                    className="cal-wstrip__dot"
                    style={{ background: style.color }}
                  />
                )
              })}
            </span>
          </button>
        )
      })}
    </div>
  )
}
