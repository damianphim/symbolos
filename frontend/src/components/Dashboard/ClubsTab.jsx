import { useState, useEffect, useCallback, useMemo, useRef } from 'react'
import {
  FaSearch, FaUsers, FaHeart, FaCalendarAlt,
  FaPlus, FaTimes, FaExternalLinkAlt, FaChevronRight,
  FaEnvelope, FaCheck, FaBell, FaBullhorn, FaTrash,
  FaChevronDown, FaChevronLeft, FaStar, FaCog, FaCrown,
  FaBook, FaPalette, FaGraduationCap,
  FaLock, FaGlobe, FaEdit, FaUserPlus, FaUserCheck, FaUserTimes
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import clubsAPI from '../../lib/clubsAPI'
import './ClubsTab.css'

const CATEGORY_META = {
  'Academic':                { color: '#2563eb', bg: '#dbeafe', border: '#93c5fd', icon: <FaBook /> },
  'Engineering & Technology':{ color: '#7c3aed', bg: '#ede9fe', border: '#c4b5fd', icon: <FaStar /> },
  'Professional':            { color: '#0f766e', bg: '#ccfbf1', border: '#5eead4', icon: <FaStar /> },
  'Debate & Politics':       { color: '#b45309', bg: '#fef3c7', border: '#fcd34d', icon: <FaSearch /> },
  'Athletics & Recreation':  { color: '#16a34a', bg: '#dcfce7', border: '#86efac', icon: <FaUsers /> },
  'Arts & Culture':          { color: '#db2777', bg: '#fce7f3', border: '#f9a8d4', icon: <FaPalette /> },
  'Environment':             { color: '#15803d', bg: '#dcfce7', border: '#6ee7b7', icon: <FaHeart /> },
  'Health & Wellness':       { color: '#0284c7', bg: '#e0f2fe', border: '#7dd3fc', icon: <FaHeart /> },
  'Community Service':       { color: '#ea580c', bg: '#ffedd5', border: '#fdba74', icon: <FaHeart /> },
  'International':           { color: '#0891b2', bg: '#cffafe', border: '#67e8f9', icon: <FaSearch /> },
  'Science':                 { color: '#4f46e5', bg: '#e0e7ff', border: '#a5b4fc', icon: <FaBook /> },
  'Social':                  { color: '#dc2626', bg: '#fee2e2', border: '#fca5a5', icon: <FaUsers /> },
  'Spiritual & Religious':   { color: '#a16207', bg: '#fefce8', border: '#fde047', icon: <FaHeart /> },
  'Default':                 { color: 'var(--text-secondary)', bg: 'var(--bg-tertiary)', border: 'var(--border-secondary)', icon: <FaGraduationCap /> },
}

const CATEGORY_I18N_KEY = {
  'Academic':                'clubs.catAcademic',
  'Engineering & Technology':'clubs.catEngineering',
  'Professional':            'clubs.catProfessional',
  'Debate & Politics':       'clubs.catDebate',
  'Athletics & Recreation':  'clubs.catAthletics',
  'Arts & Culture':          'clubs.catArts',
  'Environment':             'clubs.catEnvironment',
  'Health & Wellness':       'clubs.catHealth',
  'Community Service':       'clubs.catCommunity',
  'International':           'clubs.catInternational',
  'Science':                 'clubs.catScience',
  'Social':                  'clubs.catSocial',
  'Spiritual & Religious':   'clubs.catSpiritual',
}

function getCat(category) {
  return CATEGORY_META[category] || CATEGORY_META.Default
}

function CategoryBadge({ category, size = 'sm', t }) {
  if (!category) return null
  const meta = getCat(category)
  const label = t ? (t(CATEGORY_I18N_KEY[category] || category) || category) : category
  return (
    <span className={`club-category-badge club-category-badge--${size}`}
      style={{ background: meta.bg, color: meta.color, borderColor: meta.border }}>
      <span className="club-category-badge__icon">{meta.icon}</span> {label}
    </span>
  )
}

function ClubAvatar({ name, category, size = 'md' }) {
  const meta = getCat(category)
  return (
    <div className={`club-avatar club-avatar--${size}`} style={{ background: meta.bg, color: meta.color }}>
      <span className="club-avatar__icon">{meta.icon}</span>
    </div>
  )
}

function JoinRequestModal({ club, onSubmit, onClose }) {
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [linkedin, setLinkedin] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!name.trim() || !email.trim()) return
    setSubmitting(true)
    try {
      await onSubmit({ requester_name: name.trim(), requester_email: email.trim(), requester_linkedin: linkedin.trim() || undefined })
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="club-drawer-overlay" onClick={onClose}>
      <div className="club-join-modal" onClick={e => e.stopPropagation()}>
        <div className="club-join-modal__header">
          <h3 style={{ margin: 0, fontSize: '18px' }}>Request to Join {club?.name}</h3>
          <button className="club-drawer__back" onClick={onClose}><FaTimes size={14} /></button>
        </div>
        <form onSubmit={handleSubmit} className="club-join-modal__form">
          <div className="club-join-modal__field">
            <label>Name <span style={{ color: '#dc2626' }}>*</span></label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder="Your full name" required />
          </div>
          <div className="club-join-modal__field">
            <label>Email <span style={{ color: '#dc2626' }}>*</span></label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder="Your email address" required />
          </div>
          <div className="club-join-modal__field">
            <label>LinkedIn <span style={{ color: '#9ca3af', fontWeight: 400, fontSize: '12px' }}>(optional)</span></label>
            <input type="url" value={linkedin} onChange={e => setLinkedin(e.target.value)} placeholder="https://linkedin.com/in/..." />
          </div>
          <button type="submit" className="club-action-btn club-action-btn--join" disabled={submitting || !name.trim() || !email.trim()} style={{ width: '100%', marginTop: '8px', justifyContent: 'center' }}>
            {submitting ? 'Sending...' : 'Submit Request'}
          </button>
        </form>
      </div>
    </div>
  )
}

function MembersSection({ clubId, clubOwnerId, meta, refreshKey }) {
  const [members, setMembers] = useState([])
  const [loading, setLoading] = useState(true)
  const [callerRole, setCallerRole] = useState('member')
  const [searchTerm, setSearchTerm] = useState('')

  const fetchMembers = useCallback(() => {
    setLoading(true)
    clubsAPI.getClubMembers(clubId)
      .then(d => {
        setMembers(d.members || [])
        setCallerRole(d.caller_role || 'member')
      })
      .finally(() => setLoading(false))
  }, [clubId])

  useEffect(() => { fetchMembers() }, [fetchMembers, refreshKey])

  const handleRemove = async (userId, name) => {
    if (!window.confirm(`Remove ${name || 'this member'} from the club?`)) return
    try {
      await clubsAPI.removeClubMember(clubId, userId)
      setMembers(prev => prev.filter(m => m.id !== userId))
    } catch (e) { alert(e.message) }
  }

  const handleSetRole = async (userId, newRole) => {
    const label = newRole === 'owner' ? 'Transfer ownership to this member? You will become an admin.' : null
    if (newRole === 'owner' && !window.confirm(label)) return
    try {
      const result = await clubsAPI.updateMemberRole(clubId, userId, newRole)
      // If ownership transferred, refresh entire list to get updated roles
      if (newRole === 'owner') { fetchMembers(); return }
      setMembers(prev => prev.map(m => m.id === userId ? { ...m, role: result.role } : m))
    } catch (e) { alert(e.message) }
  }

  if (loading) return <p style={{ fontSize: '13px', color: '#9ca3af', padding: '8px 0' }}>Loading members...</p>
  if (!members.length) return <p style={{ fontSize: '13px', color: '#9ca3af', padding: '8px 0' }}>No members yet.</p>

  const canManage = callerRole === 'owner' || callerRole === 'admin'
  const roleOrder = { owner: 0, admin: 1, member: 2 }
  const filteredMembers = members.filter(m => {
    if (!searchTerm) return true
    const q = searchTerm.toLowerCase()
    return (m.name || '').toLowerCase().includes(q) || (m.email || '').toLowerCase().includes(q)
  }).sort((a, b) => (roleOrder[a.role] ?? 2) - (roleOrder[b.role] ?? 2))

  return (
    <div className="club-members-list">
      {members.length > 5 && (
        <div className="club-members-search-wrap">
          <FaSearch size={11} style={{ color: 'var(--text-tertiary, #9ca3af)' }} />
          <input
            type="text"
            className="club-members-search"
            placeholder="Search members..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>
      )}
      <div className="club-members-count" style={{ fontSize: '11px', color: 'var(--text-tertiary, #9ca3af)', padding: '4px 0' }}>
        {filteredMembers.length} member{filteredMembers.length !== 1 ? 's' : ''}
        {searchTerm && ` matching "${searchTerm}"`}
      </div>
      {filteredMembers.map(m => {
        const isOwner = m.role === 'owner'
        const role = m.role || 'member'
        // Determine what actions caller can take on this member
        const canAffect = canManage && !isOwner && (
          callerRole === 'owner' || // owners can affect anyone except themselves
          (callerRole === 'admin') // admins can affect members and other admins
        )
        return (
          <div key={m.id} className="club-member-row">
            <div className="club-member-info">
              <span className="club-member-name">
                {m.name || 'Unknown'}
                <span className={`club-member-role-badge club-member-role-badge--${role}`}>
                  {role === 'owner' ? 'Owner' : role === 'admin' ? 'Admin' : 'Member'}
                </span>
              </span>
              {m.email && <span className="club-member-email">{m.email}</span>}
            </div>
            <div className="club-member-actions">
              {canAffect && (
                <>
                  {role === 'member' && (
                    <button className="club-member-role-toggle" onClick={() => handleSetRole(m.id, 'admin')} title="Promote to admin">
                      ↑ Admin
                    </button>
                  )}
                  {role === 'admin' && (
                    <button className="club-member-role-toggle club-member-role-toggle--demote" onClick={() => handleSetRole(m.id, 'member')} title="Demote to member">
                      ↓ Demote
                    </button>
                  )}
                  {callerRole === 'owner' && !isOwner && (
                    <button className="club-member-role-toggle" onClick={() => handleSetRole(m.id, 'owner')} title="Transfer ownership" style={{ color: '#b45309', fontSize: '11px' }}>
                      ♛ Owner
                    </button>
                  )}
                  <button className="club-member-remove" onClick={() => handleRemove(m.id, m.name)} title="Remove member">
                    <FaTimes size={10} />
                  </button>
                </>
              )}
            </div>
          </div>
        )
      })}
    </div>
  )
}

function ClubDetailDrawer({ club, liveClub, joined, calSynced, hasPendingRequest, onJoin, onLeave, onToggleCalendar, onClose, clubLoading, t, isAdmin, userId, isSubscribed, onToggleSubscribe }) {
  const [memberRefreshKey, setMemberRefreshKey] = useState(0)
  if (!club) return null
  const display = liveClub ? { ...club, ...liveClub } : club
  const meta = getCat(display.category)
  const isLoading = clubLoading[club.id] ?? false
  const isPrivate = display.is_private ?? false
  const canManage = isAdmin || display.created_by === userId

  return (
    <div className="club-drawer-overlay" onClick={onClose}>
      <aside className="club-drawer" onClick={e => e.stopPropagation()}>
        <div className="club-drawer__strip" style={{
          background: `linear-gradient(135deg, ${meta.color}18, ${meta.color}08)`,
          borderBottom: `3px solid ${meta.color}`
        }}>
          <button className="club-drawer__back" onClick={onClose}>
            <FaChevronLeft size={13} /> {t('clubs.back')}
          </button>
          <div className="club-drawer__strip-main">
            <ClubAvatar name={display.name} category={display.category} size="lg" />
            <div className="club-drawer__strip-text">
              <h2 className="club-drawer__name">{display.name}</h2>
              <div className="club-drawer__badges">
                <CategoryBadge category={display.category} size="md" t={t} />
                {isPrivate ? (
                  <span className="club-visibility-badge club-visibility-badge--private">
                    <FaLock size={9} /> {t('clubs.private')}
                  </span>
                ) : (
                  <span className="club-visibility-badge club-visibility-badge--public">
                    <FaGlobe size={9} /> {t('clubs.public')}
                  </span>
                )}
              </div>
            </div>
          </div>
          <div className="club-drawer__strip-actions" style={{ display: 'flex', gap: '8px' }}>
            {/* Subscribe button — toggle to get club updates */}
            <button
              className={`club-action-btn ${isSubscribed ? 'club-action-btn--subscribed' : 'club-action-btn--subscribe'}`}
              onClick={() => onToggleSubscribe(club.id)}
              disabled={isLoading}
              title={isSubscribed ? t('clubs.unsubscribeTooltip') : t('clubs.subscribeTooltip')}
            >
              {isSubscribed ? t('clubs.subscribed') : t('clubs.subscribe')}
            </button>
            {/* Join button — links to application_url if set, otherwise website_url */}
            {(display.application_url || display.website_url) ? (
              <a
                href={display.application_url || display.website_url}
                target="_blank"
                rel="noopener noreferrer"
                className="club-action-btn club-action-btn--join"
                style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
              >
                {t('clubs.joinClub')}
              </a>
            ) : (
              <button className="club-action-btn club-action-btn--join" disabled title={t('clubs.noWebsite')}>
                {t('clubs.joinClub')}
              </button>
            )}
          </div>
        </div>

        <div className="club-drawer__body">
          <div className="club-drawer__stats">
            {display.member_count != null && (
              <div className="club-drawer__stat">
                <FaUsers size={22} style={{ color: meta.color }} />
                <span className="club-drawer__stat-value">{display.member_count}</span>
                <span className="club-drawer__stat-label">{t('clubs.members')}</span>
              </div>
            )}
            {display.meeting_schedule && (
              <div className="club-drawer__stat">
                <FaCalendarAlt size={18} style={{ color: meta.color }} />
                <span className="club-drawer__stat-value" style={{ fontSize: '0.78rem', textAlign: 'center' }}>{display.meeting_schedule}</span>
                <span className="club-drawer__stat-label">{t('clubs.meets')}</span>
              </div>
            )}
            {display.location && (
              <div className="club-drawer__stat">
                <FaStar size={18} style={{ color: meta.color }} />
                <span className="club-drawer__stat-value" style={{ fontSize: '0.78rem', textAlign: 'center' }}>{display.location}</span>
                <span className="club-drawer__stat-label">{t('clubs.location')}</span>
              </div>
            )}
          </div>

          {display.description && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title"><FaCheck size={12} /> {t('clubs.about')}</h3>
              <p className="club-drawer__desc">{display.description}</p>
            </section>
          )}

          {display.join_instructions && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title"><FaUserPlus size={12} /> {t('clubs.howToJoin')}</h3>
              <p className="club-drawer__desc" style={{ whiteSpace: 'pre-line' }}>{display.join_instructions}</p>
              {display.application_url && (
                <a
                  className="club-drawer__link-btn"
                  href={display.application_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ marginTop: '8px', display: 'inline-flex' }}
                >
                  <FaExternalLinkAlt size={10} /> {t('clubs.applyNow')}
                </a>
              )}
            </section>
          )}

          {joined && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title"><FaCalendarAlt size={12} /> {t('clubs.calendarSync')}</h3>
              <div className="club-drawer__cal-row">
                <div className="club-drawer__cal-info">
                  <p>{t('clubs.calSyncDesc')}</p>
                  {display.meeting_schedule && (
                    <span className="club-drawer__cal-schedule"><FaCalendarAlt size={11} /> {display.meeting_schedule}</span>
                  )}
                </div>
                <button
                  className={`club-cal-toggle-btn ${calSynced ? 'active' : ''}`}
                  onClick={() => onToggleCalendar(club.id, !calSynced)}
                  style={calSynced ? { borderColor: meta.color, color: meta.color, background: meta.bg } : {}}
                >
                  {calSynced
                    ? <><FaBell size={12} /> {t('clubs.synced')}</>
                    : <><FaBell size={12} /> {t('clubs.notSynced')}</>}
                </button>
              </div>
            </section>
          )}

          {joined && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <FaUsers size={12} /> Members
                <button onClick={() => setMemberRefreshKey(k => k + 1)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--text-tertiary, #9ca3af)', fontSize: '11px', padding: '2px 6px' }} title="Refresh members">↻</button>
              </h3>
              <MembersSection clubId={club.id} clubOwnerId={display.created_by} meta={meta} refreshKey={memberRefreshKey} />
            </section>
          )}

          {(display.website_url || display.contact_email) && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title"><FaExternalLinkAlt size={11} /> {t('clubs.linksContact')}</h3>
              <div className="club-drawer__links">
                {display.website_url && (
                  <a className="club-drawer__link-btn" href={display.website_url} target="_blank" rel="noopener noreferrer">
                    <FaExternalLinkAlt size={10} /> {t('clubs.visitWebsite')}
                  </a>
                )}
                {display.contact_email && (
                  <a className="club-drawer__link-btn" href={`mailto:${display.contact_email}`}>
                    <FaEnvelope size={10} /> {display.contact_email}
                  </a>
                )}
              </div>
            </section>
          )}
        </div>
      </aside>
    </div>
  )
}

function ClubCard({ club, joined, calSynced, hasPendingRequest, isSubscribed, onJoin, onLeave, onToggleCalendar, onToggleSubscribe, onOpen, onDelete, onEdit, isAdmin, clubLoading, t }) {
  const meta = getCat(club.category)
  const [justJoined, setJustJoined] = useState(false)
  const isLoading = clubLoading[club.id] ?? false
  const isPrivate = club.is_private ?? false

  const handleJoin = async (e) => {
    e.stopPropagation()
    await onJoin(club.id)
    // Don't flash "joined" animation for private clubs (modal opens instead)
    if (!isPrivate) {
      setJustJoined(true)
      setTimeout(() => setJustJoined(false), 2500)
    }
  }

  return (
    <article className={`club-card ${joined ? 'club-card--joined' : ''}`} onClick={() => onOpen(club)}>
      <div className="club-card__accent" style={{ background: joined ? meta.color : meta.color, opacity: joined ? 1 : 0.5 }} />
      <div className="club-card__body">
        <div className="club-card__top">
          <ClubAvatar name={club.name} category={club.category} size="md" />
          <div className="club-card__info">
            <h3 className="club-card__name">{club.name}</h3>
            <div className="club-card__badges">
              <CategoryBadge category={club.category} t={t} />
              {isPrivate && (
                <span className="club-visibility-badge club-visibility-badge--private">
                  <FaLock size={9} /> {t('clubs.private')}
                </span>
              )}
            </div>
          </div>
        </div>
        {club.description && (
          <p className="club-card__desc">
            {club.description.length > 105 ? club.description.slice(0, 105) + '\u2026' : club.description}
          </p>
        )}
        <div className="club-card__meta-row">
          {club.member_count != null && (
            <span className="club-meta-chip"><FaUsers size={10} /> {club.member_count}</span>
          )}
          {club.meeting_schedule && (
            <span className="club-meta-chip"><FaCalendarAlt size={10} /> {club.meeting_schedule.length > 20 ? club.meeting_schedule.slice(0,20)+'\u2026' : club.meeting_schedule}</span>
          )}
          {club.location && (
            <span className="club-meta-chip"><FaStar size={10} /> {club.location}</span>
          )}
        </div>
      </div>
      <div className="club-card__footer" onClick={e => e.stopPropagation()}>
        {joined ? (
          <div className="club-card__footer-joined">
            <button
              className={`club-cal-chip ${calSynced ? 'active' : ''}`}
              onClick={() => onToggleCalendar(club.id, !calSynced)}
              style={calSynced ? { borderColor: meta.color, color: meta.color, background: meta.bg } : {}}
              title={calSynced ? t('clubs.calOn') : t('clubs.calOff')}
            >
              <FaCalendarAlt size={10} /> {calSynced ? t('clubs.calOn') : t('clubs.calOff')}
            </button>
            <button className="club-leave-chip" onClick={() => onLeave(club.id)} disabled={isLoading}>
              <FaTimes size={10} /> {t('clubs.leave')}
            </button>
          </div>
        ) : hasPendingRequest ? (
          <div>
            <button
              className="club-join-btn club-join-btn--applied"
              disabled
              style={{ background: meta.bg, borderColor: meta.color, color: meta.color, opacity: 0.85 }}
            >
              <FaCheck size={10} /> {t('clubs.requestedBtn')}
            </button>
            <p style={{ fontSize: '0.65rem', color: 'var(--text-tertiary)', margin: '4px 0 0', textAlign: 'center', lineHeight: 1.3 }}>
              {language === 'fr' ? 'En attente de réponse' : language === 'zh' ? '等待回复中' : 'Awaiting response'}
            </p>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '6px', width: '100%' }}>
            <button
              className={`club-join-btn ${isSubscribed ? 'club-join-btn--subscribed' : ''}`}
              onClick={(e) => { e.stopPropagation(); onToggleSubscribe(club.id) }}
              disabled={isLoading}
              style={{ flex: 1 }}
            >
              {isSubscribed ? t('clubs.subscribed') : t('clubs.subscribe')}
            </button>
            {(club.application_url || club.website_url) ? (
              <a
                href={club.application_url || club.website_url}
                target="_blank"
                rel="noopener noreferrer"
                className="club-join-btn"
                onClick={e => e.stopPropagation()}
                style={{ flex: 1, textDecoration: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}
              >
                {t('clubs.joinClub')}
              </a>
            ) : (
              <button className="club-join-btn" onClick={e => e.stopPropagation()} disabled style={{ flex: 1, opacity: 0.5 }}>
                {t('clubs.joinClub')}
              </button>
            )}
          </div>
        )}
        {isAdmin && (
          <>
            <button
              className="club-edit-btn"
              onClick={(e) => { e.stopPropagation(); onEdit(club) }}
              title="Edit club"
              style={{ padding: '4px 8px', fontSize: '11px', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--card-bg)', cursor: 'pointer' }}
            >
              <FaEdit size={10} />
            </button>
            <button
              className="club-delete-chip"
              onClick={(e) => { e.stopPropagation(); const v = window.prompt(`Type "delete" to permanently remove "${club.name}"`); if (v && v.toLowerCase().trim() === 'delete') onDelete(club.id) }}
              title="Delete club"
            >
              <FaTimes size={10} />
            </button>
          </>
        )}
        <button className="club-card__open-btn" onClick={() => onOpen(club)} title="View details">
          <FaChevronRight size={11} />
        </button>
      </div>
    </article>
  )
}

function MyClubRow({ club, calSynced, onLeave, onToggleCalendar, onOpen, onDelete, isAdmin, clubLoading, t }) {
  const meta = getCat(club.category)
  const isLoading = clubLoading[club.id] ?? false
  return (
    <div className="my-club-row" onClick={() => onOpen(club)}>
      <ClubAvatar name={club.name} category={club.category} size="sm" />
      <div className="my-club-row__info">
        <span className="my-club-row__name">{club.name}</span>
        <CategoryBadge category={club.category} t={t} />
      </div>
      <div className="my-club-row__right" onClick={e => e.stopPropagation()}>
        {club.meeting_schedule && (
          <span className="my-club-row__schedule"><FaCalendarAlt size={10} /> {club.meeting_schedule}</span>
        )}
        <button
          className={`club-cal-chip ${calSynced ? 'active' : ''}`}
          style={calSynced ? { borderColor: meta.color, color: meta.color, background: meta.bg } : {}}
          onClick={() => onToggleCalendar(club.id, !calSynced)}
          title={calSynced ? t('clubs.synced') : t('clubs.syncBtn')}
        >
          <FaCalendarAlt size={10} /> {calSynced ? t('clubs.synced') : t('clubs.syncBtn')}
        </button>
        <button className="club-leave-chip small" onClick={() => onLeave(club.id)} disabled={isLoading} title={t('clubs.leave')}>
          <FaTimes size={10} />
        </button>
        {isAdmin && (
          <button
            className="club-delete-chip"
            onClick={() => { const v = window.prompt(`Type "delete" to permanently remove "${club.name}"`); if (v && v.toLowerCase().trim() === 'delete') onDelete(club.id) }}
            title="Delete club"
          >
            <FaTimes size={10} />
          </button>
        )}
        <button className="club-card__open-btn" onClick={() => onOpen(club)}>
          <FaChevronRight size={11} />
        </button>
      </div>
    </div>
  )
}

function CreatedClubRow({ club, onEdit, onManage, onManageRequests, onOpen, pendingCount, t }) {
  const meta = getCat(club.category)
  return (
    <div className="my-club-row created-club-row" onClick={() => onOpen(club)} style={{ cursor: 'pointer' }}>
      <ClubAvatar name={club.name} category={club.category} size="sm" />
      <div className="my-club-row__info">
        <span className="my-club-row__name">{club.name}</span>
        <CategoryBadge category={club.category} t={t} />
        {club.is_private && (
          <span className="club-visibility-badge club-visibility-badge--private">
            <FaLock size={9} /> {t('clubs.private')}
          </span>
        )}
      </div>
      <div className="my-club-row__right" onClick={e => e.stopPropagation()}>
        {club.member_count != null && (
          <span className="my-club-row__schedule"><FaUsers size={10} /> {club.member_count} {t('clubs.members').toLowerCase()}</span>
        )}
        {club.is_private && (
          <button className="club-manage-requests-btn" onClick={() => onManageRequests(club)}>
            <FaUserPlus size={10} /> {t('clubs.requests')}
            {pendingCount > 0 && <span className="club-request-badge">{pendingCount}</span>}
          </button>
        )}
        <button className="club-edit-btn club-edit-btn--manage" onClick={() => onManage(club)}>
          <FaCog size={10} /> {t('clubs.manage.btn')}
        </button>
        <button className="club-card__open-btn" onClick={() => onOpen(club)}>
          <FaChevronRight size={11} />
        </button>
      </div>
    </div>
  )
}

function JoinRequestsModal({ club, onClose, onAction, t }) {
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(true)
  const [actionLoading, setActionLoading] = useState({})

  useEffect(() => {
    if (!club) return
    setLoading(true)
    clubsAPI.getJoinRequests(club.id)
      .then(data => setRequests(data.requests || []))
      .finally(() => setLoading(false))
  }, [club])

  const handleAction = async (reqId, action) => {
    setActionLoading(prev => ({ ...prev, [reqId]: true }))
    try {
      await clubsAPI.handleJoinRequest(reqId, action)
      setRequests(prev => prev.filter(r => r.id !== reqId))
      if (onAction) onAction()
    } catch { /* silent */ }
    finally { setActionLoading(prev => ({ ...prev, [reqId]: false })) }
  }

  return (
    <div className="clubs-modal-overlay" onClick={onClose}>
      <div className="clubs-modal" onClick={e => e.stopPropagation()}>
        <div className="clubs-modal__header">
          <div className="clubs-modal__header-left">
            <span className="clubs-modal__icon"><FaUserPlus size={22} /></span>
            <div>
              <h2>{t('clubs.joinRequestsTitle')}</h2>
              <p>{club?.name}</p>
            </div>
          </div>
          <button className="clubs-modal__close" onClick={onClose}><FaTimes /></button>
        </div>
        <div className="clubs-modal__body">
          {loading ? (
            <div className="clubs-loading" style={{ padding: '40px 20px' }}><div className="clubs-spinner" /></div>
          ) : requests.length === 0 ? (
            <div className="clubs-empty" style={{ padding: '40px 20px' }}>
              <FaUserCheck size={36} style={{ opacity: 0.2 }} />
              <h3>{t('clubs.noRequests')}</h3>
              <p>{t('clubs.noRequestsDesc')}</p>
            </div>
          ) : (
            <div className="join-requests-list">
              {requests.map(req => (
                <div key={req.id} className="join-request-row">
                  <div className="join-request-info">
                    <span className="join-request-name">{req.requester_name || 'Unknown'}</span>
                    {req.requester_email && <span className="join-request-email">{req.requester_email}</span>}
                    {req.requester_linkedin && (
                      <a className="join-request-linkedin" href={req.requester_linkedin} target="_blank" rel="noopener noreferrer">
                        LinkedIn Profile
                      </a>
                    )}
                    <span className="join-request-date">{new Date(req.created_at).toLocaleDateString()}</span>
                  </div>
                  <div className="join-request-actions">
                    <button
                      className="club-action-btn club-action-btn--join join-request-approve"
                      onClick={() => handleAction(req.id, 'approve')}
                      disabled={actionLoading[req.id]}
                    >
                      <FaUserCheck size={11} /> {t('clubs.approve')}
                    </button>
                    <button
                      className="club-action-btn club-action-btn--leave join-request-deny"
                      onClick={() => handleAction(req.id, 'deny')}
                      disabled={actionLoading[req.id]}
                    >
                      <FaUserTimes size={11} /> {t('clubs.deny')}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

// ── Club Management Dashboard ─────────────────────────────────────────────────
function ClubManageDashboard({ club, onClose, onSave, t, isAdmin }) {
  const [activeSection, setActiveSection] = useState('overview')
  const [managers, setManagers] = useState([])
  const [subscribers, setSubscribers] = useState({ count: 0 })
  const [newManagerEmail, setNewManagerEmail] = useState('')
  const [managerLoading, setManagerLoading] = useState(false)
  const [managerError, setManagerError] = useState('')
  const [managerSuccess, setManagerSuccess] = useState('')
  const [announcements, setAnnouncements] = useState([])
  const [events, setEvents] = useState([])
  const [annForm, setAnnForm] = useState({ title: '', body: '' })
  const [annSubmitting, setAnnSubmitting] = useState(false)
  const [eventForm, setEventForm] = useState({ title: '', description: '', event_date: '', location: '' })
  const [eventSubmitting, setEventSubmitting] = useState(false)
  const [editForm, setEditForm] = useState({
    name: club?.name || '', category: club?.category || '',
    description: club?.description || '', meeting_schedule: club?.meeting_schedule || '',
    website_url: club?.website_url || '', contact_email: club?.contact_email || '',
    location: club?.location || '', is_private: club?.is_private ?? false,
    executive_emails: club?.executive_emails || '',
    join_instructions: club?.join_instructions || '',
    application_url: club?.application_url || '',
  })
  const [editSubmitting, setEditSubmitting] = useState(false)
  const [editSuccess, setEditSuccess] = useState(false)
  const meta = getCat(club?.category)

  useEffect(() => {
    if (!club?.id) return
    clubsAPI.getClubManagers(club.id).then(d => setManagers(d.managers || []))
    clubsAPI.getClubEvents?.(club.id)?.then?.(d => setEvents(d.events || d || []))?.catch?.(() => {})
    clubsAPI.getClubAnnouncements?.(club.id)?.then?.(d => setAnnouncements(d.announcements || d || []))?.catch?.(() => {})
    fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000'}/api/clubs/${club.id}/subscribers`)
      .then(r => r.json()).then(d => setSubscribers(d)).catch(() => {})
  }, [club?.id])

  const handleAddManager = async () => {
    if (!newManagerEmail.trim()) return
    setManagerLoading(true)
    setManagerError('')
    setManagerSuccess('')
    try {
      const result = await clubsAPI.addClubManager(club.id, newManagerEmail.trim())
      setManagers(prev => [...prev, result.manager])
      setNewManagerEmail('')
      setManagerSuccess(t('clubs.manage.managerAdded'))
      setTimeout(() => setManagerSuccess(''), 3000)
    } catch (e) {
      setManagerError(e.message)
    } finally {
      setManagerLoading(false)
    }
  }

  const handleRemoveManager = async (userId, name) => {
    if (!window.confirm(t('clubs.manage.removeManagerConfirm').replace('{name}', name || ''))) return
    try {
      await clubsAPI.removeClubManager(club.id, userId)
      setManagers(prev => prev.filter(m => m.user_id !== userId))
    } catch (e) { setManagerError(e.message) }
  }

  const handleSaveEdit = async (e) => {
    e.preventDefault()
    setEditSubmitting(true)
    try {
      await onSave(club.id, editForm)
      setEditSuccess(true)
      setTimeout(() => setEditSuccess(false), 3000)
    } catch {}
    finally { setEditSubmitting(false) }
  }

  const handleCreateAnnouncement = async (e) => {
    e.preventDefault()
    if (!annForm.title.trim()) return
    setAnnSubmitting(true)
    try {
      await clubsAPI.createClubAnnouncement(club.id, annForm)
      setAnnForm({ title: '', body: '' })
      // Refresh announcements
      clubsAPI.getClubAnnouncements?.(club.id)?.then?.(d => setAnnouncements(d.announcements || d || []))?.catch?.(() => {})
    } catch {}
    finally { setAnnSubmitting(false) }
  }

  const handleDeleteAnnouncement = async (annId) => {
    try {
      await clubsAPI.deleteClubAnnouncement(club.id, annId)
      setAnnouncements(prev => prev.filter(a => a.id !== annId))
    } catch {}
  }

  const handleCreateEvent = async (e) => {
    e.preventDefault()
    if (!eventForm.title.trim() || !eventForm.event_date) return
    setEventSubmitting(true)
    try {
      await clubsAPI.createClubEvent(club.id, eventForm)
      setEventForm({ title: '', description: '', event_date: '', location: '' })
      clubsAPI.getClubEvents?.(club.id)?.then?.(d => setEvents(d.events || d || []))?.catch?.(() => {})
    } catch {}
    finally { setEventSubmitting(false) }
  }

  const handleDeleteEvent = async (eventId) => {
    try {
      await clubsAPI.deleteClubEvent(club.id, eventId)
      setEvents(prev => prev.filter(ev => ev.id !== eventId))
    } catch {}
  }

  const sections = [
    { key: 'overview', icon: <FaStar size={13} />, label: t('clubs.manage.overview') },
    { key: 'edit', icon: <FaEdit size={13} />, label: t('clubs.manage.editInfo') },
    { key: 'managers', icon: <FaCrown size={13} />, label: t('clubs.manage.managers') },
    { key: 'announcements', icon: <FaBullhorn size={13} />, label: t('clubs.manage.announcements') },
    { key: 'events', icon: <FaCalendarAlt size={13} />, label: t('clubs.manage.events') },
  ]

  if (!club) return null

  return (
    <div className="clubs-modal-overlay" onClick={onClose}>
      <div className="club-manage-dashboard" onClick={e => e.stopPropagation()}>
        {/* Header */}
        <div className="club-manage__header">
          <div className="club-manage__header-left">
            <ClubAvatar name={club.name} category={club.category} size="md" />
            <div>
              <h2 className="club-manage__title">{club.name}</h2>
              <p className="club-manage__subtitle">{t('clubs.manage.dashboardTitle')}</p>
            </div>
          </div>
          <button className="clubs-modal__close" onClick={onClose}><FaTimes /></button>
        </div>

        {/* Section tabs */}
        <div className="club-manage__tabs">
          {sections.map(s => (
            <button
              key={s.key}
              className={`club-manage__tab ${activeSection === s.key ? 'active' : ''}`}
              onClick={() => setActiveSection(s.key)}
            >
              {s.icon} {s.label}
            </button>
          ))}
        </div>

        {/* Section content */}
        <div className="club-manage__content">

          {/* ── Overview ── */}
          {activeSection === 'overview' && (
            <div className="club-manage__overview">
              <div className="club-manage__stats-grid">
                <div className="club-manage__stat-card">
                  <FaUsers size={20} style={{ color: meta.color }} />
                  <div className="club-manage__stat-val">{club.member_count ?? 0}</div>
                  <div className="club-manage__stat-label">{t('clubs.members')}</div>
                </div>
                <div className="club-manage__stat-card">
                  <FaBell size={20} style={{ color: '#2563eb' }} />
                  <div className="club-manage__stat-val">{subscribers.count ?? 0}</div>
                  <div className="club-manage__stat-label">{t('clubs.manage.subscribers')}</div>
                </div>
                <div className="club-manage__stat-card">
                  <FaCrown size={20} style={{ color: '#f59e0b' }} />
                  <div className="club-manage__stat-val">{managers.length}</div>
                  <div className="club-manage__stat-label">{t('clubs.manage.managers')}</div>
                </div>
                <div className="club-manage__stat-card">
                  <FaBullhorn size={20} style={{ color: '#8b5cf6' }} />
                  <div className="club-manage__stat-val">{announcements.length}</div>
                  <div className="club-manage__stat-label">{t('clubs.manage.announcements')}</div>
                </div>
              </div>
              <div className="club-manage__quick-info">
                <p><strong>{t('clubs.fieldCategory')}:</strong> {club.category || '—'}</p>
                <p><strong>{t('clubs.fieldEmail')}:</strong> {club.contact_email || '—'}</p>
                <p><strong>{t('clubs.fieldUrl')}:</strong> {club.website_url ? <a href={club.website_url} target="_blank" rel="noopener noreferrer">{club.website_url}</a> : '—'}</p>
                <p><strong>{t('clubs.fieldSchedule')}:</strong> {club.meeting_schedule || '—'}</p>
                <p><strong>{t('clubs.fieldVisibility')}:</strong> {club.is_private ? t('clubs.private') : t('clubs.visibilityPublic')}</p>
              </div>
            </div>
          )}

          {/* ── Edit Info ── */}
          {activeSection === 'edit' && (
            <form className="club-manage__edit-form" onSubmit={handleSaveEdit}>
              {editSuccess && <div className="club-manage__success"><FaCheck size={12} /> {t('clubs.manage.saved')}</div>}
              <div className="clubs-field">
                <label>{t('clubs.fieldName')} *</label>
                <input value={editForm.name} onChange={e => setEditForm(f => ({ ...f, name: e.target.value }))} />
              </div>
              <div className="clubs-field-row">
                <div className="clubs-field">
                  <label>{t('clubs.fieldCategory')}</label>
                  <select value={editForm.category} onChange={e => setEditForm(f => ({ ...f, category: e.target.value }))}>
                    <option value="">{t('clubs.fieldCategoryDefault')}</option>
                    {Object.keys(CATEGORY_META).filter(k => k !== 'Default').map(c => (
                      <option key={c} value={c}>{t(CATEGORY_I18N_KEY[c] || c) || c}</option>
                    ))}
                  </select>
                </div>
                <div className="clubs-field">
                  <label>{t('clubs.fieldLocation')}</label>
                  <input value={editForm.location} onChange={e => setEditForm(f => ({ ...f, location: e.target.value }))} />
                </div>
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldDesc')} *</label>
                <textarea value={editForm.description} onChange={e => setEditForm(f => ({ ...f, description: e.target.value }))} rows={3} />
              </div>
              <div className="clubs-field-row">
                <div className="clubs-field">
                  <label>{t('clubs.fieldSchedule')}</label>
                  <input value={editForm.meeting_schedule} onChange={e => setEditForm(f => ({ ...f, meeting_schedule: e.target.value }))} />
                </div>
                <div className="clubs-field">
                  <label>{t('clubs.fieldEmail')}</label>
                  <input value={editForm.contact_email} onChange={e => setEditForm(f => ({ ...f, contact_email: e.target.value }))} />
                </div>
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldUrl')}</label>
                <input value={editForm.website_url} onChange={e => setEditForm(f => ({ ...f, website_url: e.target.value }))} placeholder="https://..." />
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldApplicationUrl')}</label>
                <input value={editForm.application_url} onChange={e => setEditForm(f => ({ ...f, application_url: e.target.value }))} placeholder="https://..." />
                <span className="clubs-field-hint">{t('clubs.fieldApplicationUrlHint')}</span>
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldJoinInstructions')}</label>
                <textarea value={editForm.join_instructions} onChange={e => setEditForm(f => ({ ...f, join_instructions: e.target.value }))} rows={3} placeholder={t('clubs.fieldJoinInstructionsPlaceholder')} />
                <span className="clubs-field-hint">{t('clubs.fieldJoinInstructionsHint')}</span>
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldVisibility')}</label>
                <div className="clubs-visibility-toggle">
                  <button type="button" className={`clubs-visibility-option ${!editForm.is_private ? 'active' : ''}`} onClick={() => setEditForm(f => ({ ...f, is_private: false }))}>
                    <FaGlobe size={12} /> {t('clubs.visibilityPublic')}
                  </button>
                  <button type="button" className={`clubs-visibility-option ${editForm.is_private ? 'active' : ''}`} onClick={() => setEditForm(f => ({ ...f, is_private: true }))}>
                    <FaLock size={11} /> {t('clubs.visibilityPrivate')}
                  </button>
                </div>
              </div>
              <div className="clubs-modal__footer">
                <button type="submit" className="club-action-btn club-action-btn--join" disabled={editSubmitting}>
                  {editSubmitting ? <><span className="btn-spinner" /> {t('clubs.saving')}</> : <><FaCheck size={12} /> {t('clubs.saveChanges')}</>}
                </button>
              </div>
            </form>
          )}

          {/* ── Managers ── */}
          {activeSection === 'managers' && (
            <div className="club-manage__managers">
              <div className="club-manage__add-manager">
                <label>{t('clubs.manage.addManagerLabel')}</label>
                <div className="club-manage__add-row">
                  <input
                    type="email"
                    value={newManagerEmail}
                    onChange={e => setNewManagerEmail(e.target.value)}
                    placeholder={t('clubs.manage.addManagerPlaceholder')}
                    onKeyDown={e => e.key === 'Enter' && handleAddManager()}
                  />
                  <button className="club-action-btn club-action-btn--join" onClick={handleAddManager} disabled={managerLoading || !newManagerEmail.trim()}>
                    <FaUserPlus size={12} /> {t('clubs.manage.addBtn')}
                  </button>
                </div>
                {managerError && <p className="club-manage__error">{managerError}</p>}
                {managerSuccess && <p className="club-manage__success-text">{managerSuccess}</p>}
              </div>
              <div className="club-manage__manager-list">
                {managers.map((m, i) => (
                  <div key={m.user_id || i} className="club-manage__manager-row">
                    <div className="club-manage__manager-info">
                      <div className="club-manage__manager-avatar">
                        {m.role === 'owner' ? <FaCrown size={14} style={{ color: '#f59e0b' }} /> : <FaUserCheck size={14} />}
                      </div>
                      <div>
                        <span className="club-manage__manager-name">{m.name || m.email || 'Unknown'}</span>
                        <span className="club-manage__manager-role">{m.role === 'owner' ? t('clubs.manage.owner') : t('clubs.manage.manager')}</span>
                      </div>
                    </div>
                    {m.role !== 'owner' && (
                      <button className="club-manage__remove-btn" onClick={() => handleRemoveManager(m.user_id, m.name)} title={t('clubs.manage.removeManager')}>
                        <FaUserTimes size={12} />
                      </button>
                    )}
                  </div>
                ))}
                {managers.length === 0 && <p className="club-manage__empty">{t('clubs.manage.noManagers')}</p>}
              </div>
            </div>
          )}

          {/* ── Announcements ── */}
          {activeSection === 'announcements' && (
            <div className="club-manage__announcements">
              <form className="club-manage__ann-form" onSubmit={handleCreateAnnouncement}>
                <div className="clubs-field">
                  <label>{t('clubs.manage.annTitle')} *</label>
                  <input value={annForm.title} onChange={e => setAnnForm(f => ({ ...f, title: e.target.value }))} placeholder={t('clubs.manage.annTitlePlaceholder')} />
                </div>
                <div className="clubs-field">
                  <label>{t('clubs.manage.annBody')}</label>
                  <textarea value={annForm.body} onChange={e => setAnnForm(f => ({ ...f, body: e.target.value }))} rows={3} placeholder={t('clubs.manage.annBodyPlaceholder')} />
                </div>
                <button type="submit" className="club-action-btn club-action-btn--join" disabled={annSubmitting || !annForm.title.trim()}>
                  <FaBullhorn size={12} /> {annSubmitting ? t('clubs.saving') : t('clubs.manage.postAnnouncement')}
                </button>
              </form>
              <div className="club-manage__ann-list">
                {announcements.length === 0 && <p className="club-manage__empty">{t('clubs.manage.noAnnouncements')}</p>}
                {announcements.map((a, i) => (
                  <div key={a.id || i} className="club-manage__ann-item">
                    <div className="club-manage__ann-item-header">
                      <strong>{a.title}</strong>
                      <button className="club-manage__remove-btn" onClick={() => handleDeleteAnnouncement(a.id)}><FaTrash size={11} /></button>
                    </div>
                    {a.body && <p>{a.body}</p>}
                    {a.created_at && <span className="club-manage__ann-date">{new Date(a.created_at).toLocaleDateString()}</span>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ── Events ── */}
          {activeSection === 'events' && (
            <div className="club-manage__events">
              <form className="club-manage__event-form" onSubmit={handleCreateEvent}>
                <div className="clubs-field-row">
                  <div className="clubs-field" style={{ flex: 2 }}>
                    <label>{t('clubs.manage.eventTitle')} *</label>
                    <input value={eventForm.title} onChange={e => setEventForm(f => ({ ...f, title: e.target.value }))} placeholder={t('clubs.manage.eventTitlePlaceholder')} />
                  </div>
                  <div className="clubs-field" style={{ flex: 1 }}>
                    <label>{t('clubs.manage.eventDate')} *</label>
                    <input type="datetime-local" value={eventForm.event_date} onChange={e => setEventForm(f => ({ ...f, event_date: e.target.value }))} />
                  </div>
                </div>
                <div className="clubs-field-row">
                  <div className="clubs-field" style={{ flex: 2 }}>
                    <label>{t('clubs.manage.eventDesc')}</label>
                    <input value={eventForm.description} onChange={e => setEventForm(f => ({ ...f, description: e.target.value }))} placeholder={t('clubs.manage.eventDescPlaceholder')} />
                  </div>
                  <div className="clubs-field" style={{ flex: 1 }}>
                    <label>{t('clubs.fieldLocation')}</label>
                    <input value={eventForm.location} onChange={e => setEventForm(f => ({ ...f, location: e.target.value }))} placeholder="e.g. SSMU 302" />
                  </div>
                </div>
                <button type="submit" className="club-action-btn club-action-btn--join" disabled={eventSubmitting || !eventForm.title.trim() || !eventForm.event_date}>
                  <FaCalendarAlt size={12} /> {eventSubmitting ? t('clubs.saving') : t('clubs.manage.createEvent')}
                </button>
              </form>
              <div className="club-manage__event-list">
                {events.length === 0 && <p className="club-manage__empty">{t('clubs.manage.noEvents')}</p>}
                {events.map((ev, i) => (
                  <div key={ev.id || i} className="club-manage__event-item">
                    <div className="club-manage__event-item-header">
                      <strong>{ev.title}</strong>
                      <button className="club-manage__remove-btn" onClick={() => handleDeleteEvent(ev.id)}><FaTrash size={11} /></button>
                    </div>
                    <div className="club-manage__event-meta">
                      {ev.event_date && <span><FaCalendarAlt size={10} /> {new Date(ev.event_date).toLocaleString()}</span>}
                      {ev.location && <span>📍 {ev.location}</span>}
                    </div>
                    {ev.description && <p>{ev.description}</p>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}


function EditClubModal({ club, onClose, onSave, t }) {
  const [form, setForm] = useState({
    name: club?.name || '',
    category: club?.category || '',
    description: club?.description || '',
    meeting_schedule: club?.meeting_schedule || '',
    website_url: club?.website_url || '',
    contact_email: club?.contact_email || '',
    location: club?.location || '',
    is_private: club?.is_private ?? false,
    executive_emails: club?.executive_emails || '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [errors, setErrors] = useState({})
  const set = key => val => setForm(f => ({ ...f, [key]: val }))

  const validate = () => {
    const e = {}
    if (!form.name.trim()) e.name = t('clubs.required')
    if (!form.description.trim()) e.description = t('clubs.required')
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const handleSubmit = async (ev) => {
    ev.preventDefault()
    if (!validate()) return
    setSubmitting(true)
    try {
      await onSave(club.id, form)
      onClose()
    } catch { /* silent */ }
    finally { setSubmitting(false) }
  }

  return (
    <div className="clubs-modal-overlay" onClick={onClose}>
      <div className="clubs-modal" onClick={e => e.stopPropagation()}>
        <div className="clubs-modal__header">
          <div className="clubs-modal__header-left">
            <span className="clubs-modal__icon"><FaEdit size={22} /></span>
            <div>
              <h2>{t('clubs.editModalTitle')}</h2>
              <p>{t('clubs.editModalSub')}</p>
            </div>
          </div>
          <button className="clubs-modal__close" onClick={onClose}><FaTimes /></button>
        </div>
        <form className="clubs-modal__body" onSubmit={handleSubmit} noValidate>
          <div className={`clubs-field ${errors.name ? 'error' : ''}`}>
            <label>{t('clubs.fieldName')} <span className="req">*</span></label>
            <input value={form.name} onChange={e => set('name')(e.target.value)} placeholder={t('clubs.fieldNamePlaceholder')} />
            {errors.name && <span className="clubs-field-error">{errors.name}</span>}
          </div>
          <div className="clubs-field-row">
            <div className="clubs-field">
              <label>{t('clubs.fieldCategory')}</label>
              <select value={form.category} onChange={e => set('category')(e.target.value)}>
                <option value="">{t('clubs.fieldCategoryDefault')}</option>
                {Object.keys(CATEGORY_META).filter(k => k !== 'Default').map(c => (
                  <option key={c} value={c}>{t(CATEGORY_I18N_KEY[c] || c) || c}</option>
                ))}
              </select>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldLocation')}</label>
              <input value={form.location} onChange={e => set('location')(e.target.value)} placeholder={t('clubs.fieldLocationPlaceholder')} />
            </div>
          </div>
          <div className={`clubs-field ${errors.description ? 'error' : ''}`}>
            <label>{t('clubs.fieldDesc')} <span className="req">*</span></label>
            <textarea value={form.description} onChange={e => set('description')(e.target.value)} rows={3} placeholder={t('clubs.fieldDescPlaceholder')} />
            {errors.description && <span className="clubs-field-error">{errors.description}</span>}
          </div>
          <div className="clubs-field-row">
            <div className="clubs-field">
              <label>{t('clubs.fieldSchedule')}</label>
              <input value={form.meeting_schedule} onChange={e => set('meeting_schedule')(e.target.value)} placeholder={t('clubs.fieldSchedulePlaceholder')} />
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldEmail')}</label>
              <input type="email" value={form.contact_email} onChange={e => set('contact_email')(e.target.value)} placeholder="club@mail.mcgill.ca" />
            </div>
          </div>
          <div className="clubs-field">
            <label>{t('clubs.fieldUrl')}</label>
            <input type="url" value={form.website_url} onChange={e => set('website_url')(e.target.value)} placeholder="https://..." />
          </div>
          <div className="clubs-field">
            <label>{t('clubs.fieldExecEmails')}</label>
            <textarea value={form.executive_emails} onChange={e => set('executive_emails')(e.target.value)} rows={2} placeholder={t('clubs.fieldExecEmailsPlaceholder')} />
            <span className="clubs-field-hint">{t('clubs.fieldExecEmailsHint')}</span>
          </div>
          <div className="clubs-field">
            <label>{t('clubs.fieldVisibility')}</label>
            <div className="clubs-visibility-toggle">
              <button
                type="button"
                className={`clubs-visibility-option ${!form.is_private ? 'active' : ''}`}
                onClick={() => set('is_private')(false)}
              >
                <FaGlobe size={12} /> {t('clubs.visibilityPublic')}
              </button>
              <button
                type="button"
                className={`clubs-visibility-option ${form.is_private ? 'active' : ''}`}
                onClick={() => set('is_private')(true)}
              >
                <FaLock size={11} /> {t('clubs.visibilityPrivate')}
              </button>
            </div>
            <span className="clubs-field-hint">
              {form.is_private ? t('clubs.visibilityPrivateHint') : t('clubs.visibilityPublicHint')}
            </span>
          </div>
          <div className="clubs-modal__footer">
            <button type="button" className="club-action-btn club-action-btn--ghost" onClick={onClose}>{t('clubs.cancel')}</button>
            <button type="submit" className="club-action-btn club-action-btn--join" disabled={submitting}>
              {submitting
                ? <><span className="btn-spinner" /> {t('clubs.saving')}</>
                : <><FaCheck size={12} /> {t('clubs.saveChanges')}</>}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

function SubmitClubModal({ onClose, onSubmit, t }) {
  const [form, setForm] = useState({
    name: '', category: '', description: '', meeting_schedule: '',
    website_url: '', contact_email: '', location: '', is_private: false,
    executive_emails: '', join_instructions: '', application_url: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [done, setDone] = useState(false)
  const [errors, setErrors] = useState({})
  const set = key => val => setForm(f => ({ ...f, [key]: val }))

  const validate = () => {
    const e = {}
    if (!form.name.trim()) e.name = t('clubs.required')
    if (!form.description.trim()) e.description = t('clubs.required')
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const handleSubmit = async (ev) => {
    ev.preventDefault()
    if (!validate()) return
    setSubmitting(true)
    try { await onSubmit(form); setDone(true) }
    catch { /* silent */ }
    finally { setSubmitting(false) }
  }

  return (
    <div className="clubs-modal-overlay" onClick={onClose}>
      <div className="clubs-modal" onClick={e => e.stopPropagation()}>
        <div className="clubs-modal__header">
          <div className="clubs-modal__header-left">
            <span className="clubs-modal__icon"><FaGraduationCap size={22} /></span>
            <div>
              <h2>{t('clubs.requestModalTitle')}</h2>
              <p>{t('clubs.requestModalSub')}</p>
            </div>
          </div>
          <button className="clubs-modal__close" onClick={onClose}><FaTimes /></button>
        </div>
        {done ? (
          <div className="clubs-modal__success">
            <span className="clubs-modal__success-icon"><FaCheck size={28} /></span>
            <h3>{t('clubs.submitSuccess')}</h3>
            <p>{t('clubs.submitSuccessDesc')}</p>
            <button className="club-action-btn club-action-btn--join" onClick={onClose}>{t('clubs.done')}</button>
          </div>
        ) : (
          <form className="clubs-modal__body" onSubmit={handleSubmit} noValidate>
            <div className="clubs-mcgill-notice" style={{
              background: '#fef3c7', border: '1px solid #fcd34d', borderRadius: '8px',
              padding: '10px 14px', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '8px',
              fontSize: '13px', color: '#92400e', lineHeight: '1.4',
            }}>
              <FaEnvelope size={14} style={{ flexShrink: 0 }} />
              <span>{t('clubs.mcgillEmailRequired')}</span>
            </div>
            <div className={`clubs-field ${errors.name ? 'error' : ''}`}>
              <label>{t('clubs.fieldName')} <span className="req">*</span></label>
              <input value={form.name} onChange={e => set('name')(e.target.value)} placeholder={t('clubs.fieldNamePlaceholder')} />
              {errors.name && <span className="clubs-field-error">{errors.name}</span>}
            </div>
            <div className="clubs-field-row">
              <div className="clubs-field">
                <label>{t('clubs.fieldCategory')}</label>
                <select value={form.category} onChange={e => set('category')(e.target.value)}>
                  <option value="">{t('clubs.fieldCategoryDefault')}</option>
                  {Object.keys(CATEGORY_META).filter(k => k !== 'Default').map(c => (
                    <option key={c} value={c}>{t(CATEGORY_I18N_KEY[c] || c) || c}</option>
                  ))}
                </select>
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldLocation')}</label>
                <input value={form.location} onChange={e => set('location')(e.target.value)} placeholder={t('clubs.fieldLocationPlaceholder')} />
              </div>
            </div>
            <div className={`clubs-field ${errors.description ? 'error' : ''}`}>
              <label>{t('clubs.fieldDesc')} <span className="req">*</span></label>
              <textarea value={form.description} onChange={e => set('description')(e.target.value)} rows={3} placeholder={t('clubs.fieldDescPlaceholder')} />
              {errors.description && <span className="clubs-field-error">{errors.description}</span>}
            </div>
            <div className="clubs-field-row">
              <div className="clubs-field">
                <label>{t('clubs.fieldSchedule')}</label>
                <input value={form.meeting_schedule} onChange={e => set('meeting_schedule')(e.target.value)} placeholder={t('clubs.fieldSchedulePlaceholder')} />
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldEmail')}</label>
                <input type="email" value={form.contact_email} onChange={e => set('contact_email')(e.target.value)} placeholder="club@mail.mcgill.ca" />
              </div>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldUrl')}</label>
              <input type="url" value={form.website_url} onChange={e => set('website_url')(e.target.value)} placeholder="https://..." />
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldApplicationUrl')}</label>
              <input type="url" value={form.application_url} onChange={e => set('application_url')(e.target.value)} placeholder="https://..." />
              <span className="clubs-field-hint">{t('clubs.fieldApplicationUrlHint')}</span>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldJoinInstructions')}</label>
              <textarea value={form.join_instructions} onChange={e => set('join_instructions')(e.target.value)} rows={3} placeholder={t('clubs.fieldJoinInstructionsPlaceholder')} />
              <span className="clubs-field-hint">{t('clubs.fieldJoinInstructionsHint')}</span>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldExecEmails')}</label>
              <textarea value={form.executive_emails} onChange={e => set('executive_emails')(e.target.value)} rows={2} placeholder={t('clubs.fieldExecEmailsPlaceholder')} />
              <span className="clubs-field-hint">{t('clubs.fieldExecEmailsHint')}</span>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldVisibility')}</label>
              <div className="clubs-visibility-toggle">
                <button
                  type="button"
                  className={`clubs-visibility-option ${!form.is_private ? 'active' : ''}`}
                  onClick={() => set('is_private')(false)}
                >
                  <FaGlobe size={12} /> {t('clubs.visibilityPublic')}
                </button>
                <button
                  type="button"
                  className={`clubs-visibility-option ${form.is_private ? 'active' : ''}`}
                  onClick={() => set('is_private')(true)}
                >
                  <FaLock size={11} /> {t('clubs.visibilityPrivate')}
                </button>
              </div>
              <span className="clubs-field-hint">
                {form.is_private ? t('clubs.visibilityPrivateHint') : t('clubs.visibilityPublicHint')}
              </span>
            </div>
            <div className="clubs-modal__footer">
              <button type="button" className="club-action-btn club-action-btn--ghost" onClick={onClose}>{t('clubs.cancel')}</button>
              <button type="submit" className="club-action-btn club-action-btn--join" disabled={submitting}>
                {submitting
                  ? <><span className="btn-spinner" /> {t('clubs.submitting')}</>
                  : <><FaChevronRight size={12} /> {t('clubs.submitClub')}</>}
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  )
}

const PAGE_SIZE = 24

export default function ClubsTab({ user, authFlags, onClubEventsChange }) {
  const { t } = useLanguage()
  const isAdmin = authFlags?.is_admin ?? false
  const [activeView, setActiveView] = useState('explore')
  const [clubs, setClubs] = useState([])
  const [categories, setCategories] = useState([])
  const [myClubs, setMyClubs] = useState([])
  const [createdClubs, setCreatedClubs] = useState([])
  const [pendingCounts, setPendingCounts] = useState({})
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('')
  const [sortMode, setSortMode] = useState('default')
  const [loading, setLoading] = useState(false)
  const [myClubsLoading, setMyClubsLoading] = useState(false)
  const [error, setError] = useState(null)
  const [clubLoading, setClubLoading] = useState({})
  const setClubBusy = (clubId, busy) => setClubLoading(prev => ({ ...prev, [clubId]: busy }))
  const [page, setPage] = useState(1)
  const [hasMore, setHasMore] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [showSubmitModal, setShowSubmitModal] = useState(false)
  const [openClub, setOpenClub] = useState(null)
  const [editingClub, setEditingClub] = useState(null)
  const [managingClub, setManagingClub] = useState(null)
  const [managingRequestsClub, setManagingRequestsClub] = useState(null)
  const [joinToast, setJoinToast] = useState(null)
  const [joinRequestClub, setJoinRequestClub] = useState(null)
  const [pendingRequestClubIds, setPendingRequestClubIds] = useState(new Set())
  const [subscribedIds, setSubscribedIds] = useState(new Set())
  const debounceRef = useRef(null)
  const isMounted = useRef(true)

  useEffect(() => {
    isMounted.current = true
    return () => { isMounted.current = false }
  }, [])

  // Fetch user subscriptions on mount
  useEffect(() => {
    if (!user?.id) return
    clubsAPI.getUserSubscriptions(user.id).then(data => {
      if (isMounted.current) setSubscribedIds(new Set(data.subscribed_club_ids || []))
    }).catch(() => {})
  }, [user?.id])

  const joinedIds    = useMemo(() => new Set(myClubs.map(m => m.club?.id ?? m.id)), [myClubs])
  const calSyncedIds = useMemo(() => new Set(myClubs.filter(m => m.calendar_synced).map(m => m.club?.id ?? m.id)), [myClubs])

  const fetchClubs = useCallback(async (pageNum = 1) => {
    if (pageNum === 1) { setLoading(true); setError(null) }
    else setLoadingMore(true)
    try {
      const data = await clubsAPI.getClubs({
        search: debouncedSearch,
        category: selectedCategory,
        limit: PAGE_SIZE,
        offset: (pageNum - 1) * PAGE_SIZE,
      })
      const results = Array.isArray(data) ? data : data.clubs ?? []
      if (!isMounted.current) return
      if (pageNum === 1) setClubs(results)
      else setClubs(prev => [...prev, ...results])
      setHasMore(results.length === PAGE_SIZE)
      setPage(pageNum)
    } catch (e) {
      if (isMounted.current) setError(e.message)
    } finally {
      if (isMounted.current) { setLoading(false); setLoadingMore(false) }
    }
  }, [debouncedSearch, selectedCategory])

  const fetchMyClubs = useCallback(async () => {
    if (!user?.id) return
    setMyClubsLoading(true)
    try {
      const data = await clubsAPI.getUserClubs(user.id)
      const list = Array.isArray(data) ? data : data.clubs ?? []
      if (!isMounted.current) return
      setMyClubs(list)
      if (onClubEventsChange) onClubEventsChange(buildClubCalendarEvents(list))
    } catch { /* silent */ }
    finally { if (isMounted.current) setMyClubsLoading(false) }
  }, [user?.id, onClubEventsChange])

  const fetchCreatedClubs = useCallback(async () => {
    if (!user?.id) return
    try {
      // For admins, fetch ALL clubs so they can manage any club
      // For regular users, only their created clubs
      let list
      if (isAdmin) {
        const data = await clubsAPI.getClubs({ limit: 200 })
        list = Array.isArray(data) ? data : data.clubs ?? []
      } else {
        const data = await clubsAPI.getCreatedClubs(user.id)
        list = Array.isArray(data) ? data : data.clubs ?? []
      }
      if (!isMounted.current) return
      setCreatedClubs(isAdmin ? list : list)
      // Fetch pending counts for private clubs
      const counts = {}
      for (const club of list) {
        if (club.is_private) {
          try {
            const reqData = await clubsAPI.getJoinRequests(club.id)
            counts[club.id] = (reqData.requests || []).length
          } catch { counts[club.id] = 0 }
        }
      }
      if (isMounted.current) setPendingCounts(counts)
    } catch { /* silent */ }
  }, [user?.id, isAdmin])

  const fetchCategories = useCallback(async () => {
    try {
      const data = await clubsAPI.getCategories()
      if (isMounted.current) setCategories(Array.isArray(data) ? data : data.categories ?? [])
    } catch { /* silent */ }
  }, [])

  const fetchPendingRequests = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await clubsAPI.getUserPendingRequests(user.id)
      if (isMounted.current) setPendingRequestClubIds(new Set(data.pending_club_ids || []))
    } catch { /* silent */ }
  }, [user?.id])

  useEffect(() => { setPage(1); fetchClubs(1) }, [fetchClubs])
  useEffect(() => { fetchMyClubs() }, [fetchMyClubs])
  useEffect(() => { fetchCreatedClubs() }, [fetchCreatedClubs])
  useEffect(() => { fetchCategories() }, [fetchCategories])
  useEffect(() => { fetchPendingRequests() }, [fetchPendingRequests])

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      if (isMounted.current) setDebouncedSearch(search)
    }, 350)
    return () => clearTimeout(debounceRef.current)
  }, [search])

  const handleJoin = async (clubId, joinInfo) => {
    if (!user?.id) return
    // Only @mail.mcgill.ca emails can join clubs
    if (!user.email?.endsWith('@mail.mcgill.ca') && !authFlags?.is_admin) {
      setError('Only accounts with a @mail.mcgill.ca email can join clubs.')
      return
    }
    // For private clubs, show the join request modal first (unless joinInfo already provided)
    const club = clubs.find(c => c.id === clubId) || (openClub?.id === clubId ? openClub : null)
    if (club?.is_private && !joinInfo) {
      setJoinRequestClub(club)
      return
    }
    setClubBusy(clubId, true)
    try {
      const result = await clubsAPI.joinClub(user.id, clubId, joinInfo || {})
      if (result.status === 'requested') {
        setPendingRequestClubIds(prev => new Set([...prev, clubId]))
        // Force drawer re-render so "Applied" button shows immediately
        if (openClub?.id === clubId) setOpenClub(prev => prev ? { ...prev } : prev)
        // Also confirm from server to keep in sync
        fetchPendingRequests()
        setJoinToast(t('clubs.requestSentToast').replace('{name}', club?.name || 'club'))
      } else {
        await fetchMyClubs()
        setClubs(prev => prev.map(c => c.id === clubId ? { ...c, member_count: (c.member_count ?? 0) + 1 } : c))
        if (openClub?.id === clubId) setOpenClub(prev => prev ? { ...prev, member_count: (prev.member_count ?? 0) + 1 } : prev)
        if (club) setJoinToast(t('clubs.joinedToast').replace('{name}', club.name))
      }
      setTimeout(() => { if (isMounted.current) setJoinToast(null) }, 3000)
    } catch (e) { setError(e.message) }
    finally { setClubBusy(clubId, false) }
  }

  const handleJoinRequestSubmit = async (joinInfo) => {
    const clubId = joinRequestClub?.id
    setJoinRequestClub(null)
    if (clubId) await handleJoin(clubId, joinInfo)
  }

  const handleLeave = async (clubId) => {
    if (!user?.id) return
    setClubBusy(clubId, true)
    try {
      await clubsAPI.leaveClub(user.id, clubId)
      await fetchMyClubs()
      setClubs(prev => prev.map(c => c.id === clubId ? { ...c, member_count: Math.max(0, (c.member_count ?? 1) - 1) } : c))
      if (openClub?.id === clubId) setOpenClub(prev => prev ? { ...prev, member_count: Math.max(0, (prev.member_count ?? 1) - 1) } : prev)
    } catch (e) { setError(e.message) }
    finally { setClubBusy(clubId, false) }
  }

  const handleToggleSubscribe = async (clubId) => {
    setClubBusy(clubId, true)
    try {
      const result = await clubsAPI.toggleSubscription(clubId)
      if (isMounted.current) {
        setSubscribedIds(prev => {
          const next = new Set(prev)
          if (result.is_subscribed) next.add(clubId)
          else next.delete(clubId)
          return next
        })
        const club = clubs.find(c => c.id === clubId) || openClub
        setJoinToast(result.is_subscribed
          ? t('clubs.subscribedToast').replace('{name}', club?.name || '')
          : t('clubs.unsubscribedToast').replace('{name}', club?.name || ''))
        setTimeout(() => { if (isMounted.current) setJoinToast(null) }, 3000)
      }
    } catch (e) { setError(e.message) }
    finally { setClubBusy(clubId, false) }
  }

  const handleToggleCalendar = async (clubId, synced) => {
    setClubBusy(clubId, true)
    try {
      await clubsAPI.toggleCalendarSync(user.id, clubId, synced)
      await fetchMyClubs()
    } catch (e) { setError(e.message) }
    finally { setClubBusy(clubId, false) }
  }

  const handleDeleteClub = async (clubId) => {
    try {
      await clubsAPI.deleteClub(clubId)
      setClubs(prev => prev.filter(c => c.id !== clubId))
      setMyClubs(prev => prev.filter(m => (m.club?.id ?? m.id) !== clubId))
      setCreatedClubs(prev => prev.filter(c => c.id !== clubId))
      if (openClub?.id === clubId) setOpenClub(null)
      setJoinToast('Club deleted')
      setTimeout(() => setJoinToast(''), 2500)
    } catch (e) { setError(e.message) }
  }

  const handleSubmitClub = async (formData) => {
    await clubsAPI.submitClub({ ...formData, submitted_by: user?.id })
    setJoinToast(t('clubs.clubSubmittedToast'))
    setTimeout(() => { if (isMounted.current) setJoinToast(null) }, 4000)
  }

  const handleEditClub = async (clubId, formData) => {
    await clubsAPI.editClub(clubId, formData)
    await fetchCreatedClubs()
  }

  const displayClubs = useMemo(() => {
    let list = [...clubs]
    if (sortMode === 'members') list.sort((a, b) => (b.member_count ?? 0) - (a.member_count ?? 0))
    if (sortMode === 'name') list.sort((a, b) => (a.name ?? '').localeCompare(b.name ?? ''))
    return list
  }, [clubs, sortMode])

  const createdClubIds = useMemo(() => new Set(createdClubs.map(c => c.id)), [createdClubs])

  const resolvedMyClubs = useMemo(() =>
    myClubs.map(m => ({ club: m.club ?? m, calendar_synced: m.calendar_synced ?? false })).filter(m => m.club?.id && !createdClubIds.has(m.club.id)),
    [myClubs, createdClubIds]
  )

  const clubsById = useMemo(() => {
    const map = {}
    clubs.forEach(c => { map[c.id] = c })
    return map
  }, [clubs])

  const totalPendingRequests = useMemo(() =>
    Object.values(pendingCounts).reduce((sum, c) => sum + c, 0),
    [pendingCounts]
  )

  return (
    <div className="clubs-tab">
      {joinToast && <div className="clubs-toast"><FaCheck size={12} /> {joinToast}</div>}
      {joinRequestClub && (
        <JoinRequestModal
          club={joinRequestClub}
          onSubmit={handleJoinRequestSubmit}
          onClose={() => setJoinRequestClub(null)}
        />
      )}

      <div className="clubs-header">
        <div className="clubs-header__left">
          <div className="clubs-header__icon-wrap"><FaUsers size={26} /></div>
          <div>
            <h1 className="clubs-header__title">{t('clubs.title')}</h1>
            <p className="clubs-header__sub">{t('clubs.subtitle')}</p>
          </div>
        </div>
        <button className="clubs-submit-btn" onClick={() => setShowSubmitModal(true)}>
          <FaPlus size={11} /> {t('clubs.requestAddBtn')}
        </button>
      </div>

      <div className="clubs-tabs">
        <button className={`clubs-tab-btn ${activeView === 'explore' ? 'active' : ''}`} onClick={() => setActiveView('explore')}>
          <FaSearch size={15} /> {t('clubs.tabExplore')}
        </button>
        <button className={`clubs-tab-btn ${activeView === 'my-clubs' ? 'active' : ''}`} onClick={() => setActiveView('my-clubs')}>
          <FaHeart size={12} /> {t('clubs.tabMine')}
          {totalPendingRequests > 0 && (
            <span className="clubs-tab-notification">{totalPendingRequests}</span>
          )}
        </button>
      </div>

      {activeView === 'explore' && (
        <div className="clubs-explore">
          <div className="clubs-toolbar">
            <div className="clubs-search-wrap">
              <FaSearch className="clubs-search-icon" size={13} />
              <input
                className="clubs-search-input"
                type="text"
                placeholder={t('clubs.searchPlaceholder')}
                value={search}
                onChange={e => setSearch(e.target.value)}
              />
              {search && <button className="clubs-search-clear" onClick={() => setSearch('')}><FaTimes size={11} /></button>}
            </div>
            <div className="clubs-sort-wrap">
              <FaChevronDown size={11} />
              <select className="clubs-sort-select" value={sortMode} onChange={e => setSortMode(e.target.value)}>
                <option value="default">{t('clubs.sortDefault')}</option>
                <option value="members">{t('clubs.sortMembers')}</option>
                <option value="name">{t('clubs.sortName')}</option>
              </select>
            </div>
          </div>

          {categories.length > 0 && (
            <div className="clubs-filter-row">
              <div className="clubs-category-dropdown-wrap">
                <FaChevronDown size={11} className="clubs-category-dropdown-icon" />
                <select
                  className="clubs-category-dropdown"
                  value={selectedCategory}
                  onChange={e => setSelectedCategory(e.target.value)}
                >
                  <option value="">{t('clubs.filterAll')}</option>
                  {categories.map(cat => {
                    const label = t(CATEGORY_I18N_KEY[cat] || cat) || cat
                    return (
                      <option key={cat} value={cat}>{label}</option>
                    )
                  })}
                </select>
              </div>
            </div>
          )}

          {error && <div className="clubs-error">{error}<button onClick={() => setError(null)}><FaTimes size={11} /></button></div>}

          {loading ? (
            <div className="clubs-loading"><div className="clubs-spinner" /><p>{t('clubs.loading')}</p></div>
          ) : displayClubs.length === 0 ? (
            <div className="clubs-empty">
              <div className="clubs-empty__visual"><FaUsers size={52} /></div>
              <h3>{t('clubs.noClubsYet')}</h3>
              <p>{t('clubs.noClubsYetDesc')}</p>
              <button className="club-action-btn club-action-btn--join" onClick={() => setShowSubmitModal(true)}>
                <FaPlus size={11} /> {t('clubs.requestAddBtn')}
              </button>
            </div>
          ) : (
            <>
              <p className="clubs-results-label">
                <strong>{displayClubs.length}</strong> {displayClubs.length !== 1 ? t('clubs.results').replace('{count}','').trim() : t('clubs.result').replace('{count}','').trim()}
                {selectedCategory && <> {t('clubs.inCategory')} <em>{t(CATEGORY_I18N_KEY[selectedCategory] || selectedCategory) || selectedCategory}</em></>}
                {debouncedSearch && <> {t('clubs.matching')} "<em>{debouncedSearch}</em>"</>}
                {hasMore && <> {t('clubs.showingFirst').replace('{count}', displayClubs.length)}</>}
              </p>
              <div className="clubs-grid">
                {displayClubs.map(club => (
                  <ClubCard
                    key={club.id}
                    club={club}
                    joined={joinedIds.has(club.id)}
                    calSynced={calSyncedIds.has(club.id)}
                    hasPendingRequest={pendingRequestClubIds.has(club.id)}
                    isSubscribed={subscribedIds.has(club.id)}
                    onJoin={handleJoin}
                    onLeave={handleLeave}
                    onToggleCalendar={handleToggleCalendar}
                    onToggleSubscribe={handleToggleSubscribe}
                    onOpen={setOpenClub}
                    onDelete={handleDeleteClub}
                    onEdit={setEditingClub}
                    isAdmin={isAdmin}
                    clubLoading={clubLoading}
                    t={t}
                  />
                ))}
              </div>
              {hasMore && (
                <div className="clubs-load-more">
                  <button className="clubs-load-more__btn" onClick={() => fetchClubs(page + 1)} disabled={loadingMore}>
                    {loadingMore
                      ? <><span className="btn-spinner" style={{ borderTopColor: 'var(--accent-primary)' }} /> {t('clubs.loadingMore')}</>
                      : <><FaChevronDown size={11} /> {t('clubs.loadMore')}</>}
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {activeView === 'my-clubs' && (
        <div className="clubs-mine">
          {myClubsLoading ? (
            <div className="clubs-loading"><div className="clubs-spinner" /><p>{t('clubs.loadingMine')}</p></div>
          ) : (
            <>
              {/* Created Clubs Section */}
              {createdClubs.length > 0 && (
                <div className="clubs-mine__section">
                  <h3 className="clubs-mine__section-title">
                    <FaStar size={13} /> {isAdmin ? 'Manage Clubs' : t('clubs.createdByYou')}
                    <span className="clubs-mine__section-count">{createdClubs.length}</span>
                  </h3>
                  <div className="clubs-mine__list">
                    {createdClubs.map(club => (
                      <CreatedClubRow
                        key={club.id}
                        club={club}
                        onEdit={setEditingClub}
                        onManage={setManagingClub}
                        onManageRequests={setManagingRequestsClub}
                        onOpen={setOpenClub}
                        pendingCount={pendingCounts[club.id] || 0}
                        t={t}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Joined Clubs Section */}
              <div className="clubs-mine__section">
                <h3 className="clubs-mine__section-title">
                  <FaHeart size={13} /> {t('clubs.joinedClubs')}
                  {resolvedMyClubs.length > 0 && <span className="clubs-mine__section-count">{resolvedMyClubs.length}</span>}
                </h3>
                {resolvedMyClubs.length === 0 ? (
                  <div className="clubs-empty" style={{ padding: '40px 20px' }}>
                    <div className="clubs-empty__visual" style={{ opacity: 0.2 }}><FaHeart size={42} /></div>
                    <h3>{t('clubs.noJoined')}</h3>
                    <p>{t('clubs.noJoinedHint')}</p>
                    <button className="club-action-btn club-action-btn--join" onClick={() => setActiveView('explore')}>
                      <FaSearch size={13} /> {t('clubs.browseBtn')}
                    </button>
                  </div>
                ) : (
                  <div className="clubs-mine__list">
                    {resolvedMyClubs.map(({ club, calendar_synced }) => (
                      <MyClubRow
                        key={club.id}
                        club={club}
                        calSynced={calendar_synced}
                        onLeave={handleLeave}
                        onToggleCalendar={handleToggleCalendar}
                        onOpen={setOpenClub}
                        onDelete={handleDeleteClub}
                        isAdmin={isAdmin}
                        clubLoading={clubLoading}
                        t={t}
                      />
                    ))}
                  </div>
                )}
              </div>
            </>
          )}
        </div>
      )}

      {openClub && (
        <ClubDetailDrawer
          club={openClub}
          liveClub={clubsById[openClub.id]}
          joined={joinedIds.has(openClub.id)}
          calSynced={calSyncedIds.has(openClub.id)}
          hasPendingRequest={pendingRequestClubIds.has(openClub.id)}
          isSubscribed={subscribedIds.has(openClub.id)}
          onJoin={handleJoin}
          onLeave={handleLeave}
          onToggleCalendar={handleToggleCalendar}
          onToggleSubscribe={handleToggleSubscribe}
          onClose={() => setOpenClub(null)}
          clubLoading={clubLoading}
          t={t}
          isAdmin={isAdmin}
          userId={user?.id}
        />
      )}

      {showSubmitModal && (
        <SubmitClubModal onClose={() => setShowSubmitModal(false)} onSubmit={handleSubmitClub} t={t} />
      )}

      {editingClub && (
        <EditClubModal club={editingClub} onClose={() => setEditingClub(null)} onSave={handleEditClub} t={t} />
      )}

      {managingRequestsClub && (
        <JoinRequestsModal
          club={managingRequestsClub}
          onClose={() => setManagingRequestsClub(null)}
          onAction={() => { fetchCreatedClubs(); fetchMyClubs() }}
          t={t}
        />
      )}

      {managingClub && (
        <ClubManageDashboard
          club={managingClub}
          onClose={() => setManagingClub(null)}
          onSave={handleEditClub}
          t={t}
          isAdmin={isAdmin}
        />
      )}
    </div>
  )
}

export function buildClubCalendarEvents(myClubs) {
  const events = []
  const today = new Date()

  myClubs.forEach(membership => {
    const club = membership.club ?? membership
    if (!membership.calendar_synced) return
    if (!club?.name) return

    const schedule = (club.meeting_schedule || '').toLowerCase()
    if (!schedule || /\b(tbd|varies|tba|to be announced)\b/.test(schedule)) return

    const timeMatch = schedule.match(/(\d{1,2})(?::(\d{2}))?\s*(am|pm)/i)
    let timeStr = ''
    if (timeMatch) {
      let h = parseInt(timeMatch[1])
      const m = timeMatch[2] ?? '00'
      const ampm = timeMatch[3]?.toLowerCase()
      if (ampm === 'pm' && h < 12) h += 12
      if (ampm === 'am' && h === 12) h = 0
      timeStr = `${String(h).padStart(2, '0')}:${m}`
    }

    const DAY_MAP = { sunday: 0, monday: 1, tuesday: 2, wednesday: 3, thursday: 4, friday: 5, saturday: 6 }
    const foundDays = Object.entries(DAY_MAP)
      .filter(([name]) => schedule.includes(name))
      .map(([, idx]) => idx)
    if (foundDays.length === 0) return

    const isbiweekly = /bi[-\s]?weekly|every (other|2nd) week|alternate weeks?/.test(schedule)
    const weekStep = isbiweekly ? 2 : 1

    for (let week = 0; week < 8; week += weekStep) {
      foundDays.forEach(targetDay => {
        const d = new Date(today)
        const diff = (targetDay - d.getDay() + 7) % 7
        d.setDate(d.getDate() + diff + week * 7)
        const pad = n => String(n).padStart(2, '0')
        const dateStr = `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
        events.push({
          id: `club-${club.id}-${dateStr}`,
          title: `${club.name}`,
          date: dateStr,
          time: timeStr,
          type: 'club',
          category: club.category || 'Club',
          description: club.meeting_schedule || '',
          readOnly: true,
          clubId: club.id,
        })
      })
    }
  })

  return events
}
