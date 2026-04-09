import React, { useState } from 'react'
import { FaTimes, FaBell, FaCheck, FaTrash, FaGraduationCap, FaClipboardList, FaStar, FaBullseye } from 'react-icons/fa'
import { L, EVENT_TYPE_OPTIONS } from './calendarConstants'

// Re-export EVENT_TYPE_OPTIONS with icons attached (requires JSX context)
const EVENT_TYPE_OPTIONS_WITH_ICONS = [
  { ...EVENT_TYPE_OPTIONS[0], icon: <FaStar /> },
  { ...EVENT_TYPE_OPTIONS[1], icon: <FaGraduationCap /> },
  { ...EVENT_TYPE_OPTIONS[2], icon: <FaBullseye /> },
  { ...EVENT_TYPE_OPTIONS[3], icon: <FaClipboardList /> },
]

export default function EventModal({ event, onSave, onDelete, onClose, t, notifPrefs, user, language, managedClubs = [] }) {
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
    end_time:    event?.end_time    || '',
    location:    event?.location    || '',
    type:        event?.type        || 'personal',
    category:    event?.category    || '',
    description: event?.description || '',
    clubId:      event?.clubId      || (managedClubs[0]?.id || ''),
    recurrence:  event?.recurrence  || '',
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
  const selectedType = EVENT_TYPE_OPTIONS_WITH_ICONS.find(t => t.key === form.type) || EVENT_TYPE_OPTIONS_WITH_ICONS[0]

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.title.trim() || !form.date) return
    onSave({ ...form, id: event?.id || `user-${Date.now()}` })
  }

  const f = (key) => (val) => setForm(p => ({ ...p, [key]: val }))
  const toggle = (key) => setForm(p => ({ ...p, [key]: !p[key] }))

  return (
    <div className="cal-modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="cal-modal cal-modal-v2">
        <div className="cal-modal-accent" style={{ background: selectedType.color }} />

        <div className="cal-modal-header-v2">
          <div className="cal-modal-header-left">
            <span className="cal-modal-type-icon">{selectedType.icon}</span>
            <h3>{isEdit ? L(language, 'Edit Event', 'Modifier l\'événement', '编辑事件') : L(language, 'New Event', 'Nouvel événement', '新事件')}</h3>
          </div>
          <button className="cal-modal-close" onClick={onClose}><FaTimes /></button>
        </div>

        <form id="event-modal-form" className="cal-modal-body-v2" onSubmit={handleSubmit}>

          <div className="cal-v2-type-row">
            {EVENT_TYPE_OPTIONS_WITH_ICONS.filter(opt => opt.key !== 'club' || managedClubs.length > 0).map(opt => (
              <button key={opt.key} type="button"
                className={`cal-v2-type-card ${form.type === opt.key ? 'selected' : ''}`}
                style={form.type === opt.key ? { borderColor: opt.color, background: opt.bg, color: opt.color } : {}}
                onClick={() => f('type')(opt.key)}>
                <span className="cal-v2-type-icon" style={form.type === opt.key ? { color: opt.color } : {}}>{opt.icon}</span>
                <span className="cal-v2-type-label">{L(language, opt.labelEn, opt.labelFr, opt.labelZh)}</span>
                {form.type === opt.key && <span className="cal-v2-type-check" style={{ color: opt.color }}><FaCheck size={8} /></span>}
              </button>
            ))}
          </div>

          <div className="cal-v2-field">
            <label className="cal-v2-label">{L(language, 'Title', 'Titre', '标题')} <span className="cal-v2-required">*</span></label>
            <input
              className="cal-v2-input"
              type="text"
              value={form.title}
              onChange={e => f('title')(e.target.value)}
              placeholder={L(language, 'Event name…', 'Nom de l\'événement…', '事件名称…')}
              required
              autoFocus
            />
          </div>

          <div className="cal-v2-row">
            <div className="cal-v2-field cal-v2-field--date">
              <label className="cal-v2-label">{L(language, 'Date', 'Date', '日期')} <span className="cal-v2-required">*</span></label>
              <input className="cal-v2-input" type="date" value={form.date} onChange={e => f('date')(e.target.value)} required />
            </div>
            <div className="cal-v2-field cal-v2-field--time">
              <label className="cal-v2-label">{L(language, 'Start', 'Début', '开始')}</label>
              <input className="cal-v2-input" type="time" value={form.time} onChange={e => f('time')(e.target.value)} />
            </div>
            <div className="cal-v2-field cal-v2-field--time">
              <label className="cal-v2-label">{L(language, 'End', 'Fin', '结束')}</label>
              <input className="cal-v2-input" type="time" value={form.end_time} onChange={e => f('end_time')(e.target.value)} />
            </div>
          </div>

          <div className="cal-v2-field">
            <label className="cal-v2-label">{L(language, 'Location', 'Lieu', '地点')}</label>
            <input
              className="cal-v2-input"
              type="text"
              value={form.location}
              onChange={e => f('location')(e.target.value)}
              placeholder={L(language, 'Room, building…', 'Salle, bâtiment…', '教室、建筑…')}
            />
          </div>

          {form.type === 'club' && managedClubs.length > 0 && (
            <div className="cal-v2-field">
              <label className="cal-v2-label">{L(language, 'Club', 'Club', '社团')} <span className="cal-v2-required">*</span></label>
              <select className="cal-v2-input" value={form.clubId} onChange={e => f('clubId')(e.target.value)}>
                {managedClubs.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          )}

          {form.type === 'club' && (
            <div className="cal-v2-field">
              <label className="cal-v2-label">{L(language, 'Recurrence', 'Récurrence', '重复')}</label>
              <select className="cal-v2-input" value={form.recurrence} onChange={e => f('recurrence')(e.target.value)}>
                <option value="">{L(language, 'One-time event', 'Événement unique', '一次性事件')}</option>
                <option value="weekly_monday">Weekly Monday</option>
                <option value="weekly_tuesday">Weekly Tuesday</option>
                <option value="weekly_wednesday">Weekly Wednesday</option>
                <option value="weekly_thursday">Weekly Thursday</option>
                <option value="weekly_friday">Weekly Friday</option>
                <option value="weekly_saturday">Weekly Saturday</option>
                <option value="weekly_sunday">Weekly Sunday</option>
                <option value="biweekly_monday">Bi-weekly Monday</option>
                <option value="biweekly_tuesday">Bi-weekly Tuesday</option>
                <option value="biweekly_wednesday">Bi-weekly Wednesday</option>
                <option value="biweekly_thursday">Bi-weekly Thursday</option>
                <option value="biweekly_friday">Bi-weekly Friday</option>
              </select>
            </div>
          )}

          <div className="cal-v2-field">
            <label className="cal-v2-label">{L(language, 'Notes', 'Notes', '备注')}</label>
            <textarea
              className="cal-v2-input cal-v2-textarea"
              value={form.description}
              onChange={e => f('description')(e.target.value)}
              rows={2}
              placeholder={L(language, 'Optional details…', 'Détails optionnels…', '可选详情…')}
            />
          </div>

          <div className="cal-v2-notif-section">
            <div className="cal-v2-notif-header">
              <FaBell size={12} style={{ color: form.notifyEnabled ? '#ed1b2f' : 'var(--text-muted)' }} />
              <span>{L(language, 'Reminders', 'Rappels', '提醒')}</span>
              <button
                type="button"
                className={`cal-v2-notif-toggle ${form.notifyEnabled ? 'on' : 'off'}`}
                onClick={() => toggle('notifyEnabled')}
              >
                <span className="cal-v2-notif-toggle-knob" />
              </button>
            </div>
            {form.notifyEnabled && (
              <div className="cal-v2-timing-chips">
                {[
                  { key: 'notifySameDay', labelEn: 'Same day',  labelFr: 'Jour même',  labelZh: '当天' },
                  { key: 'notify1Day',    labelEn: '1 day before', labelFr: '1 jour avant', labelZh: '1天前' },
                  { key: 'notify7Days',   labelEn: '1 week before', labelFr: '1 semaine avant', labelZh: '1周前' },
                ].map(({ key, labelEn, labelFr, labelZh }) => (
                  <label key={key} className={`cal-v2-chip ${form[key] ? 'active' : ''}`}
                    style={form[key] ? { borderColor: selectedType.color, background: selectedType.bg, color: selectedType.color } : {}}>
                    <input type="checkbox" checked={form[key]} onChange={() => toggle(key)} />
                    {form[key] && <FaCheck size={8} />}
                    {L(language, labelEn, labelFr, labelZh)}
                  </label>
                ))}
              </div>
            )}
          </div>

        </form>

        <div className="cal-v2-footer">
          {isEdit && (
            <button type="button" className="cal-v2-btn-danger" onClick={() => onDelete(event.id)}>
              <FaTrash size={12} /> {L(language, 'Delete', 'Supprimer', '删除')}
            </button>
          )}
          <div className="cal-v2-actions-right">
            <button type="button" className="cal-v2-btn-ghost" onClick={onClose}>
              {L(language, 'Cancel', 'Annuler', '取消')}
            </button>
            <button type="submit" form="event-modal-form" className="cal-v2-btn-primary" style={{ background: selectedType.color }}>
              <FaCheck size={11} /> {isEdit ? L(language, 'Save', 'Enregistrer', '保存') : L(language, 'Add Event', 'Ajouter', '添加事件')}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
