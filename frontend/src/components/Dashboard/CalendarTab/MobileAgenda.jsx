import React from 'react'
import { FaPlus, FaChevronRight } from 'react-icons/fa'
import { toDateStr } from './calendarConstants'

/**
 * Mobile-only replacement for the 7-column month grid / week grid.
 *
 * A 7-column grid is unreadable at 360px, so on phones the same period
 * (whatever `dates` the caller passes — a month or a week) is rendered as a
 * chronological list grouped by day. The caller keeps ownership of the period
 * itself, so the existing month/week toggle and the prev/next nav keep working
 * unchanged; only the rendering of the period swaps.
 *
 * Days with no events are dropped so the list stays scannable, except today,
 * which is always shown as an anchor.
 */

const byTime = (a, b) => (a.time || '99:99').localeCompare(b.time || '99:99')

export default function MobileAgenda({
  dates,
  eventsByDate,
  todayStr,
  pinnedDateStr,
  MONTHS,
  DAYS,
  onSelectEvent,
  onOpenDay,
  onAddOnDate,
  typeConfig,
  getEventStyle,
  t,
}) {
  const groups = dates
    .map(date => {
      const dateStr = toDateStr(date.getFullYear(), date.getMonth(), date.getDate())
      return {
        date,
        dateStr,
        events: (eventsByDate[dateStr] || []).slice().sort(byTime),
      }
    })
    // Empty days are dropped to keep the list scannable, except today (always an
    // anchor) and any explicitly pinned day — e.g. the day selected in the month
    // grid, which must stay visible even with no events so its add button is
    // reachable.
    .filter(g => g.events.length > 0 || g.dateStr === todayStr || g.dateStr === pinnedDateStr)

  if (groups.length === 0) {
    return (
      <div className="cal-agenda cal-agenda--empty">
        <p>{t('cal.noEventsInRange')}</p>
        <button className="cal-agenda__empty-add" onClick={() => onAddOnDate(dates[0])}>
          <FaPlus size={11} /> {t('calendar.addEvent')}
        </button>
      </div>
    )
  }

  return (
    <div className="cal-agenda">
      {groups.map(({ date, dateStr, events }) => {
        const isToday = dateStr === todayStr
        return (
          <section key={dateStr} className={`cal-agenda-day ${isToday ? 'is-today' : ''}`}>
            <div className="cal-agenda-day__header">
              <button
                type="button"
                className="cal-agenda-day__label"
                onClick={() => onOpenDay(date)}
              >
                <span className="cal-agenda-day__num">{date.getDate()}</span>
                <span className="cal-agenda-day__meta">
                  <span className="cal-agenda-day__weekday">{DAYS[date.getDay()]}</span>
                  <span className="cal-agenda-day__month">{MONTHS[date.getMonth()]}</span>
                </span>
                {isToday && <span className="cal-agenda-day__today">{t('calendar.today')}</span>}
              </button>
              <button
                type="button"
                className="cal-agenda-day__add"
                onClick={() => onAddOnDate(date)}
                aria-label={t('calendar.addEvent')}
                title={t('calendar.addEvent')}
              >
                <FaPlus size={11} />
              </button>
            </div>

            {events.length === 0 ? (
              <p className="cal-agenda-day__empty">{t('cal.noEventsToday')}</p>
            ) : (
              <ul className="cal-agenda-day__list">
                {events.map(e => {
                  const style = getEventStyle(e, typeConfig)
                  return (
                    <li key={e.id}>
                      {/* The event type is carried by a colour dot rather than
                          by tinting the whole row. A tinted, separately
                          bordered row is card chrome: it makes each event a
                          floating box, and it forces hardcoded dark text
                          because the tint is light in both themes. A dot
                          leaves the row on the group surface, so it inherits
                          theme colours and reads as one list. */}
                      <button
                        type="button"
                        className="cal-agenda-event"
                        onClick={() => onSelectEvent(e)}
                      >
                        <span
                          className="cal-agenda-event__dot"
                          style={{ background: style.color }}
                          aria-hidden="true"
                        />
                        <span className="cal-agenda-event__time">
                          {e.time
                            ? `${e.time}${e.end_time ? `–${e.end_time}` : ''}`
                            : t('cal.allDay')}
                        </span>
                        <span className="cal-agenda-event__body">
                          <span className="cal-agenda-event__title">{e.title}</span>
                          {e.category && (
                            <span className="cal-agenda-event__cat">{e.category}</span>
                          )}
                        </span>
                        <FaChevronRight className="cal-agenda-event__chev" size={10} />
                      </button>
                    </li>
                  )
                })}
              </ul>
            )}
          </section>
        )
      })}
    </div>
  )
}
