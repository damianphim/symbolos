import React from 'react'
import { FaTimes, FaCheck, FaEdit, FaClock, FaCalendarAlt, FaLayerGroup } from 'react-icons/fa'
import { L } from './calendarConstants'

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

export function EyeIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  )
}

export function EyeOffIcon() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
      <line x1="1" y1="1" x2="23" y2="23"/>
    </svg>
  )
}

function SlotRow({ ev, isHidden, onToggleHide, onSave, language }) {
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
  const timeLabel = ev.time ? (hasEnd ? `${ev.time}–${ev.end_time}` : ev.time) : null

  if (editing) {
    return (
      <div className="slot-row slot-row--editing" onClick={e => e.stopPropagation()}>
        <div className="slot-row-edit-fields">
          <select className="slot-edit-select" value={day} onChange={e => setDay(e.target.value)}>
            {DAY_OPTIONS.map(d => <option key={d.value} value={d.value}>{d.label}</option>)}
          </select>
          <div className="slot-edit-time-pair">
            <input className="slot-edit-time" type="time" value={timeStart} onChange={e => setTimeStart(e.target.value)} />
            <span className="slot-edit-sep">→</span>
            <input className="slot-edit-time" type="time" value={timeEnd} onChange={e => setTimeEnd(e.target.value)} />
          </div>
        </div>
        <div className="slot-row-edit-actions">
          <button className="slot-edit-save" onClick={handleSave} disabled={saving}>
            {saving ? '…' : <><FaCheck size={10}/> {L(language, 'Save', 'OK', '保存')}</>}
          </button>
          <button className="slot-edit-cancel" onClick={() => setEditing(false)}>
            <FaTimes size={10}/>
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className={`slot-row ${isHidden ? 'slot-row--hidden' : ''}`}>
      <div className="slot-row-main">
        <span className="slot-day-pill">{dayLabel}</span>
        <div className="slot-info">
          <span className="slot-label">{slotLabel}</span>
          {timeLabel
            ? <span className="slot-time">{timeLabel}</span>
            : <span className="slot-time slot-time--missing"><FaClock size={9}/> {L(language, 'no time set', 'heure manquante', '未设时间')}</span>
          }
        </div>
      </div>
      <div className="slot-row-actions">
        <button
          className="slot-action-btn slot-edit-btn"
          title={L(language, 'Edit time', 'Modifier', '编辑时间')}
          onClick={e => { e.stopPropagation(); setEditing(true) }}
        >
          <FaEdit size={11}/>
        </button>
        <button
          className={`slot-action-btn slot-eye-btn ${isHidden ? 'slot-eye-btn--hidden' : ''}`}
          title={isHidden ? L(language, 'Show on calendar', 'Afficher', '在日历上显示') : L(language, 'Hide from calendar', 'Masquer', '从日历隐藏')}
          onClick={e => { e.stopPropagation(); onToggleHide() }}
        >
          {isHidden ? <EyeOffIcon /> : <EyeIcon />}
        </button>
      </div>
    </div>
  )
}

export default function BulkDeleteModal({ userEvents, allEvents = [], onHide, hiddenSlotKeys, onUnhideAll, onClose, language, onEditSlot, serverClubEvents = [], mutedClubIds, onToggleMuteClub, hiddenEventIds, onToggleHideEvent, typeConfig = {}, getEventStyle }) {
  const classGroups = React.useMemo(() => {
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

  const eventsByType = React.useMemo(() => {
    const map = {}
    for (const ev of allEvents) {
      if (ev.course_code && ev.recurrence && ev._isRecurringOccurrence) continue
      if (ev.course_code && ev.recurrence) continue
      const type = ev.type || 'personal'
      if (!map[type]) map[type] = []
      map[type].push(ev)
    }
    for (const type in map) {
      map[type].sort((a, b) => (a.date || '').localeCompare(b.date || ''))
    }
    return map
  }, [allEvents])

  const slotKey = (ev) => `${ev.course_code}::${ev.recurrence}::${ev.time || ''}`
  const totalHidden = (hiddenSlotKeys?.size || 0) + (hiddenEventIds?.size || 0) + (mutedClubIds?.size || 0)

  const getCourseStats = (evs) => {
    const keys = evs.map(slotKey)
    const hidden = keys.filter(k => hiddenSlotKeys?.has(k)).length
    return { total: keys.length, hidden, visible: keys.length - hidden }
  }

  const hideAllForCourse = (evs) => {
    const keys = evs.map(slotKey)
    const allHidden = keys.every(k => hiddenSlotKeys?.has(k))
    if (allHidden) onHide(keys, 'unhide')
    else onHide(keys.filter(k => !hiddenSlotKeys?.has(k)), 'hide')
  }

  const typeOrder = ['course', 'academic', 'exam', 'personal', 'club']

  return (
    <div className="cal-bulk-overlay" onClick={onClose}>
      <div className="mgr-modal" onClick={e => e.stopPropagation()}>

        <div className="mgr-header">
          <div className="mgr-header-left">
            <FaLayerGroup size={15} style={{ color: '#ed1b2f' }} />
            <div>
              <h3 className="mgr-title">{L(language, 'Manage Events', 'Gérer les événements', '管理事件')}</h3>
              {totalHidden > 0 && (
                <p className="mgr-subtitle">
                  {L(language, `${totalHidden} item${totalHidden !== 1 ? 's' : ''} hidden`, `${totalHidden} élément${totalHidden !== 1 ? 's' : ''} masqué${totalHidden !== 1 ? 's' : ''}`, `${totalHidden}项已隐藏`)}
                </p>
              )}
            </div>
          </div>
          <div className="mgr-header-right">
            {totalHidden > 0 && (
              <button className="mgr-show-all-btn" onClick={onUnhideAll}>
                <EyeIcon /> {L(language, 'Show all', 'Tout afficher', '全部显示')}
              </button>
            )}
            <button className="mgr-close" onClick={onClose}><FaTimes /></button>
          </div>
        </div>

        <div className="mgr-legend">
          <span className="mgr-legend-item mgr-legend-visible"><EyeIcon /> {L(language, 'Visible', 'Visible', '可见')}</span>
          <span className="mgr-legend-item mgr-legend-hidden"><EyeOffIcon /> {L(language, 'Hidden', 'Masqué', '已隐藏')}</span>
          <span className="mgr-legend-sep" />
          <span className="mgr-legend-hint">{L(language, 'Click 👁 to toggle visibility', 'Cliquez 👁 pour basculer', '点击👁切换可见性')}</span>
        </div>

        <div className="mgr-list" style={{ maxHeight: '60vh', overflowY: 'auto' }}>
          {Object.keys(classGroups).length > 0 && (
            <div style={{ marginBottom: 12 }}>
              <div style={{ padding: '8px 12px', fontSize: '12px', fontWeight: 700, color: typeConfig.course?.color || '#ed1b2f', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                {typeConfig.course?.icon} {L(language, 'Recurring Classes', 'Cours récurrents', '循环课程')}
              </div>
              {Object.entries(classGroups).sort(([a],[b]) => a.localeCompare(b)).map(([courseCode, days]) => {
                const allEvs = Object.values(days).flat()
                const stats = getCourseStats(allEvs)
                const allHidden = stats.hidden === stats.total
                return (
                  <div key={courseCode} className="mgr-course">
                    <div className="mgr-course-header">
                      <div className="mgr-course-header-left">
                        <span className="mgr-course-code">{courseCode}</span>
                        <span className="mgr-course-stats">
                          {stats.hidden > 0
                            ? <span className="mgr-course-stats--partial">{stats.visible}/{stats.total} {L(language, 'visible', 'visible', '可见')}</span>
                            : <span className="mgr-course-stats--all">{L(language, 'All visible', 'Tout visible', '全部可见')}</span>
                          }
                        </span>
                      </div>
                      <button
                        className={`mgr-course-toggle ${allHidden ? 'mgr-course-toggle--hidden' : ''}`}
                        onClick={() => hideAllForCourse(allEvs)}
                      >
                        {allHidden ? <EyeOffIcon /> : <EyeIcon />}
                        <span>{allHidden ? L(language, 'Show all', 'Afficher tout', '全部显示') : L(language, 'Hide all', 'Masquer tout', '全部隐藏')}</span>
                      </button>
                    </div>
                    <div className="mgr-slots">
                      {Object.entries(days).sort(([a],[b]) => a.localeCompare(b)).map(([rec, evs]) =>
                        evs.map(ev => (
                          <SlotRow
                            key={`${slotKey(ev)}-${ev.time}-${ev.recurrence}`}
                            ev={ev}
                            isHidden={hiddenSlotKeys?.has(slotKey(ev))}
                            onToggleHide={() => {
                              const key = slotKey(ev)
                              onHide([key], hiddenSlotKeys?.has(key) ? 'unhide' : 'hide')
                            }}
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

          {typeOrder.filter(type => eventsByType[type]?.length > 0).map(type => {
            const events = eventsByType[type]
            const cfg = typeConfig[type] || typeConfig.personal || { color: '#059669', bg: '#ecfdf5', label: type }
            if (type === 'club') {
              const clubMap = {}
              events.forEach(ev => {
                const cid = ev.clubId || 'unknown'
                if (!clubMap[cid]) clubMap[cid] = { name: ev.category || 'Club', events: [] }
                clubMap[cid].events.push(ev)
              })
              return (
                <div key={type} style={{ marginBottom: 12 }}>
                  <div style={{ padding: '8px 12px', fontSize: '12px', fontWeight: 700, color: cfg.color, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    {cfg.icon} {cfg.label}
                  </div>
                  {Object.entries(clubMap).map(([clubId, { name, events: clubEvs }]) => {
                    const isMuted = mutedClubIds?.has(clubId)
                    return (
                      <div key={clubId} className="mgr-course">
                        <div className="mgr-course-header">
                          <div className="mgr-course-header-left">
                            <span className="mgr-course-code">{name}</span>
                          </div>
                          <button
                            className={`mgr-course-toggle ${isMuted ? 'mgr-course-toggle--hidden' : ''}`}
                            onClick={() => onToggleMuteClub(clubId)}
                          >
                            {isMuted ? <EyeOffIcon /> : <EyeIcon />}
                            <span>{isMuted ? L(language, 'Show all', 'Afficher tout', '全部显示') : L(language, 'Hide all', 'Masquer tout', '全部隐藏')}</span>
                          </button>
                        </div>
                        <div className="mgr-slots">
                          {clubEvs.map(ev => {
                            const isHidden = hiddenEventIds?.has(ev.id) || isMuted
                            const dateObj = ev.date ? new Date(ev.date + 'T00:00:00') : null
                            const shortDate = dateObj ? dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : ''
                            const hasEnd = ev.end_time && String(ev.end_time).trim()
                            const timeLabel = ev.time ? (hasEnd ? `${ev.time}–${ev.end_time}` : ev.time) : null
                            return (
                              <div key={ev.id} className={`slot-row ${isHidden ? 'slot-row--hidden' : ''}`}>
                                <div className="slot-row-main">
                                  <span className="slot-day-pill">{shortDate}</span>
                                  <div className="slot-info">
                                    <span className="slot-label">{ev.title}</span>
                                    {timeLabel && <span className="slot-time">{timeLabel}</span>}
                                  </div>
                                </div>
                                <div className="slot-row-actions">
                                  <button
                                    className={`slot-action-btn slot-eye-btn ${isHidden ? 'slot-eye-btn--hidden' : ''}`}
                                    onClick={e => { e.stopPropagation(); onToggleHideEvent(ev.id) }}
                                    disabled={isMuted}
                                  >
                                    {isHidden ? <EyeOffIcon /> : <EyeIcon />}
                                  </button>
                                </div>
                              </div>
                            )
                          })}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )
            }

            return (
              <div key={type} style={{ marginBottom: 12 }}>
                <div style={{ padding: '8px 12px', fontSize: '12px', fontWeight: 700, color: cfg.color, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                  {cfg.icon} {cfg.label}
                </div>
                <div className="mgr-slots">
                  {events.map(ev => {
                    const isHidden = hiddenEventIds?.has(ev.id)
                    const dateObj = ev.date ? new Date(ev.date + 'T00:00:00') : null
                    const shortDate = dateObj ? dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : ''
                    const hasEnd = ev.end_time && String(ev.end_time).trim()
                    const timeLabel = ev.time ? (hasEnd ? `${ev.time}–${ev.end_time}` : ev.time) : null
                    return (
                      <div key={ev.id} className={`slot-row ${isHidden ? 'slot-row--hidden' : ''}`}>
                        <div className="slot-row-main">
                          <span className="slot-day-pill">{shortDate}</span>
                          <div className="slot-info">
                            <span className="slot-label">{ev.title}</span>
                            {timeLabel && <span className="slot-time">{timeLabel}</span>}
                          </div>
                        </div>
                        <div className="slot-row-actions">
                          <button
                            className={`slot-action-btn slot-eye-btn ${isHidden ? 'slot-eye-btn--hidden' : ''}`}
                            onClick={e => { e.stopPropagation(); onToggleHideEvent(ev.id) }}
                          >
                            {isHidden ? <EyeOffIcon /> : <EyeIcon />}
                          </button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )
          })}

          {Object.keys(classGroups).length === 0 && Object.keys(eventsByType).length === 0 && (
            <div className="mgr-empty">
              <span style={{ fontSize: '2rem' }}><FaCalendarAlt /></span>
              <p>{L(language, 'No events found.', 'Aucun événement trouvé.', '未找到事件。')}</p>
            </div>
          )}
        </div>

        <div className="mgr-footer">
          <button className="mgr-done-btn" onClick={onClose}>
            {L(language, 'Done', 'Terminé', '完成')}
          </button>
        </div>
      </div>
    </div>
  )
}
