import React, { useState } from 'react'
import { FaTimes, FaCheck, FaBullhorn, FaCalendarAlt } from 'react-icons/fa'
import { L } from './calendarConstants'

export default function AnnouncementModal({ clubs, onSave, onClose, language }) {
  const [form, setForm] = useState({ title: '', body: '', clubId: clubs[0]?.id || '', attachEvent: false, eventDate: '', eventTime: '', eventEndTime: '', eventLocation: '' })
  const handleSubmit = (e) => {
    e.preventDefault()
    if (!form.title.trim() || !form.body.trim() || !form.clubId) return
    if (form.attachEvent && !form.eventDate) return
    onSave(form)
  }
  return (
    <div className="cal-modal-overlay" onClick={e => e.target === e.currentTarget && onClose()}>
      <div className="cal-modal cal-modal-v2" style={{ maxWidth: '460px' }}>
        <div className="cal-modal-accent" style={{ background: '#d97706' }} />
        <div className="cal-modal-header-v2">
          <div className="cal-modal-header-left">
            <span className="cal-modal-type-icon"><FaBullhorn /></span>
            <h3>{L(language, 'Post Announcement', 'Publier une annonce', '发布公告')}</h3>
          </div>
          <button className="cal-modal-close" onClick={onClose}><FaTimes /></button>
        </div>
        <form className="cal-modal-body-v2" onSubmit={handleSubmit}>
          <div className="cal-v2-field">
            <label className="cal-v2-label">{L(language, 'Club', 'Club', '社团')}</label>
            <select className="cal-v2-input" value={form.clubId} onChange={e => setForm(p => ({ ...p, clubId: e.target.value }))}>
              {clubs.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>
          <div className="cal-v2-field">
            <label className="cal-v2-label">{L(language, 'Title', 'Titre', '标题')} <span className="cal-v2-required">*</span></label>
            <input className="cal-v2-input" value={form.title} onChange={e => setForm(p => ({ ...p, title: e.target.value }))} placeholder={L(language, 'Announcement title…', 'Titre de l\'annonce…', '公告标题…')} required autoFocus />
          </div>
          <div className="cal-v2-field">
            <label className="cal-v2-label">{L(language, 'Message', 'Message', '消息')} <span className="cal-v2-required">*</span></label>
            <textarea className="cal-v2-input cal-v2-textarea" rows={4} value={form.body} onChange={e => setForm(p => ({ ...p, body: e.target.value }))} placeholder={L(language, 'Write your announcement…', 'Rédigez votre annonce…', '写下你的公告…')} required />
          </div>
          <div className="cal-v2-field">
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer', fontSize: '13px', fontWeight: 600, color: 'var(--text-secondary)' }}>
              <input type="checkbox" checked={form.attachEvent} onChange={e => setForm(p => ({ ...p, attachEvent: e.target.checked }))} style={{ accentColor: '#d97706' }} />
              <FaCalendarAlt size={12} style={{ color: '#d97706' }} />
              {L(language, 'Attach an event', 'Joindre un événement', '附加活动')}
            </label>
          </div>
          {form.attachEvent && (
            <>
              <div className="cal-v2-field">
                <label className="cal-v2-label">{L(language, 'Event Date', 'Date', '日期')} <span className="cal-v2-required">*</span></label>
                <input className="cal-v2-input" type="date" value={form.eventDate} onChange={e => setForm(p => ({ ...p, eventDate: e.target.value }))} required />
              </div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <div className="cal-v2-field" style={{ flex: 1 }}>
                  <label className="cal-v2-label">{L(language, 'Start', 'Début', '开始')}</label>
                  <input className="cal-v2-input" type="time" value={form.eventTime} onChange={e => setForm(p => ({ ...p, eventTime: e.target.value }))} />
                </div>
                <div className="cal-v2-field" style={{ flex: 1 }}>
                  <label className="cal-v2-label">{L(language, 'End', 'Fin', '结束')}</label>
                  <input className="cal-v2-input" type="time" value={form.eventEndTime} onChange={e => setForm(p => ({ ...p, eventEndTime: e.target.value }))} />
                </div>
              </div>
              <div className="cal-v2-field">
                <label className="cal-v2-label">{L(language, 'Location', 'Lieu', '地点')}</label>
                <input className="cal-v2-input" value={form.eventLocation} onChange={e => setForm(p => ({ ...p, eventLocation: e.target.value }))} placeholder={L(language, 'e.g. SSMU Ballroom', 'ex. Salle de bal SSMU', '例如 SSMU舞厅')} />
              </div>
            </>
          )}
          <div className="cal-v2-footer">
            <div className="cal-v2-actions-right">
              <button type="button" className="cal-v2-btn-ghost" onClick={onClose}>{L(language, 'Cancel', 'Annuler', '取消')}</button>
              <button type="submit" className="cal-v2-btn-primary" style={{ background: '#d97706' }}><FaCheck size={11} /> {L(language, 'Post', 'Publier', '发布')}</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  )
}
