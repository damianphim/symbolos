import { useState, useEffect, useCallback, useMemo, useRef } from 'react'
import {
  FaSearch, FaUsers, FaHeart, FaCalendarAlt,
  FaPlus, FaTimes, FaExternalLinkAlt, FaChevronRight, FaChevronLeft,
  FaEnvelope, FaCheck, FaBell, FaBullhorn, FaTrash,
  FaChevronDown, FaStar, FaCog, FaCrown,
  FaBook, FaPalette, FaGraduationCap,
  FaLock, FaGlobe, FaEdit, FaUserPlus, FaUserCheck, FaUserTimes,
  FaExclamationTriangle, FaFire, FaGem, FaMapMarkerAlt,
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/PreferencesContext'
import { useAuth } from '../../contexts/AuthContext'
import useViewport from '../../hooks/useViewport'
import clubsAPI from '../../lib/clubsAPI'
import { readCache, writeCache } from '../../lib/userDataCache'
import Breadcrumb from '../ui/Breadcrumb'
import './ClubsTab.css'

// Every category uses the same neutral gray — no per-category color, and no
// red (red is reserved for active/hover states elsewhere in the UI). The
// category is still distinguished by its icon + label.
const catVars = () => ({
  color:  'var(--text-secondary)',
  bg:     'var(--bg-tertiary)',
  border: 'var(--border-secondary)',
})

const CATEGORY_META = {
  'Academic':                { ...catVars('academic'),      icon: <FaBook /> },
  'Engineering & Technology':{ ...catVars('engineering'),   icon: <FaStar /> },
  'Professional':            { ...catVars('professional'),  icon: <FaStar /> },
  'Debate & Politics':       { ...catVars('debate'),        icon: <FaSearch /> },
  'Athletics & Recreation':  { ...catVars('athletics'),     icon: <FaUsers /> },
  'Arts & Culture':          { ...catVars('arts'),          icon: <FaPalette /> },
  'Environment':             { ...catVars('environment'),   icon: <FaHeart /> },
  'Health & Wellness':       { ...catVars('health'),        icon: <FaHeart /> },
  'Community Service':       { ...catVars('community'),     icon: <FaHeart /> },
  'International':           { ...catVars('international'), icon: <FaSearch /> },
  'Science':                 { ...catVars('science'),       icon: <FaBook /> },
  'Social':                  { ...catVars('social'),        icon: <FaUsers /> },
  'Spiritual & Religious':   { ...catVars('spiritual'),     icon: <FaHeart /> },
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

function ClubAvatar({ name, category, size = 'md', calSynced = false, logoUrl = null, editable = false, onEditClick = null }) {
  const meta = getCat(category)
  const initials = (name || '?').trim().split(/\s+/).slice(0, 2).map(w => w[0]?.toUpperCase()).join('') || '?'
  const dim = { sm: 28, md: 44, lg: 64 }[size] ?? 44

  // Always stop click from bubbling up to the card (so clicking the avatar
  // never opens the detail drawer). Belt-and-braces: stop both mousedown and
  // click at React and native event levels. Only owners get the file picker.
  const swallow = (e) => {
    e.stopPropagation()
    // The native stopImmediatePropagation blocks any other listeners on the
    // same DOM element from also firing (defensive — useful if any portal
    // attaches its own native click listener).
    e.nativeEvent?.stopImmediatePropagation?.()
  }
  const handleClick = (e) => {
    swallow(e)
    if (editable && onEditClick) onEditClick()
  }

  return (
    <div
      className={`club-avatar club-avatar--${size} ${editable ? 'club-avatar--editable' : ''}`}
      onClick={handleClick}
      onMouseDown={swallow}
      onPointerDown={swallow}
      title={editable ? 'Click to change logo' : undefined}
      style={{
        width: dim, height: dim, borderRadius: 10,
        background: logoUrl ? 'transparent' : meta.bg,
        color: meta.color, border: `1px solid ${meta.border}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontSize: dim * 0.36, fontWeight: 700, position: 'relative', flexShrink: 0,
        overflow: 'hidden', cursor: editable ? 'pointer' : undefined,
      }}
    >
      {logoUrl ? (
        <img
          src={logoUrl}
          alt={name || 'Club logo'}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
          onError={(e) => { e.currentTarget.style.display = 'none'; e.currentTarget.parentElement.appendChild(document.createTextNode(initials)) }}
        />
      ) : initials}
      {calSynced && (
        <span className="club-avatar__cal-badge" title="In your calendar">
          <FaCalendarAlt size={9} />
        </span>
      )}
      {editable && (
        <span className="club-avatar__edit-overlay" aria-hidden>
          <FaEdit size={Math.max(10, dim * 0.28)} />
        </span>
      )}
    </div>
  )
}

// Skeleton placeholder used while the club grid is loading — visually matches a real card
function ClubCardSkeleton() {
  return (
    <div className="club-card club-card--skeleton" aria-hidden>
      <div className="club-card__body">
        <div className="club-card__top">
          <div className="club-skel club-skel--avatar" />
          <div style={{ flex: 1 }}>
            <div className="club-skel club-skel--title" />
            <div className="club-skel club-skel--badge" />
          </div>
        </div>
        <div className="club-skel club-skel--line" />
        <div className="club-skel club-skel--line" style={{ width: '70%' }} />
        <div className="club-skel club-skel--meta" />
      </div>
      <div className="club-card__footer">
        <div className="club-skel club-skel--btn" />
      </div>
    </div>
  )
}

function JoinRequestModal({ club, onSubmit, onClose }) {
  const { t } = useLanguage()
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
          <h3 style={{ margin: 0, fontSize: '18px' }}>{t('clubs.requestToJoin')} {club?.name}</h3>
          <button className="club-drawer__back" onClick={onClose}><FaTimes size={14} /></button>
        </div>
        <form onSubmit={handleSubmit} className="club-join-modal__form">
          <div className="club-join-modal__field">
            <label>{t('clubs.joinName')} <span style={{ color: 'var(--error-primary)' }}>*</span></label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} placeholder={t('clubs.joinNamePlaceholder')} required />
          </div>
          <div className="club-join-modal__field">
            <label>{t('clubs.joinEmail')} <span style={{ color: 'var(--error-primary)' }}>*</span></label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} placeholder={t('clubs.joinEmailPlaceholder')} required />
          </div>
          <div className="club-join-modal__field">
            <label>{t('clubs.joinLinkedIn')} <span style={{ color: 'var(--text-muted)', fontWeight: 400, fontSize: '12px' }}>{t('clubs.joinOptional')}</span></label>
            <input type="url" value={linkedin} onChange={e => setLinkedin(e.target.value)} placeholder={t('clubs.joinLinkedInPlaceholder')} />
          </div>
          <button type="submit" className="club-action-btn club-action-btn--join" disabled={submitting || !name.trim() || !email.trim()} style={{ width: '100%', marginTop: '8px', justifyContent: 'center' }}>
            {submitting ? t('clubs.joinSending') : t('clubs.joinSubmit')}
          </button>
        </form>
      </div>
    </div>
  )
}

function MembersSection({ clubId, refreshKey }) {
  const { t } = useLanguage()
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
    if (!window.confirm(t('clubs.confirmRemoveMember').replace('{name}', name || t('clubs.roleMember')))) return
    try {
      await clubsAPI.removeClubMember(clubId, userId)
      setMembers(prev => prev.filter(m => m.id !== userId))
    } catch (e) { alert(e.message) }
  }

  const handleSetRole = async (userId, newRole) => {
    if (newRole === 'owner' && !window.confirm(t('clubs.confirmTransferOwnership'))) return
    try {
      const result = await clubsAPI.updateMemberRole(clubId, userId, newRole)
      // If ownership transferred, refresh entire list to get updated roles
      if (newRole === 'owner') { fetchMembers(); return }
      setMembers(prev => prev.map(m => m.id === userId ? { ...m, role: result.role } : m))
    } catch (e) { alert(e.message) }
  }

  if (loading) return <p style={{ fontSize: '13px', color: 'var(--text-muted)', padding: '8px 0' }}>{t('clubs.membersLoading')}</p>
  if (!members.length) return <p style={{ fontSize: '13px', color: 'var(--text-muted)', padding: '8px 0' }}>{t('clubs.membersNone')}</p>

  const canManage = callerRole === 'owner' || callerRole === 'admin'
  const roleOrder = { owner: 0, admin: 1, member: 2 }
  // Discovery-only site — clubs have an owner and execs (admins), no regular
  // members. Hide any stray role='member' rows from older data.
  const filteredMembers = members
    .filter(m => m.role === 'owner' || m.role === 'admin')
    .filter(m => {
      if (!searchTerm) return true
      const q = searchTerm.toLowerCase()
      return (m.name || '').toLowerCase().includes(q) || (canManage && (m.email || '').toLowerCase().includes(q))
    })
    .sort((a, b) => (roleOrder[a.role] ?? 2) - (roleOrder[b.role] ?? 2))

  return (
    <div className="club-members-list">
      {members.length > 5 && (
        <div className="club-members-search-wrap">
          <FaSearch size={11} style={{ color: 'var(--text-tertiary, #9ca3af)' }} />
          <input
            type="text"
            className="club-members-search"
            placeholder={t('clubs.membersSearch')}
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </div>
      )}
      <div className="club-members-count" style={{ fontSize: '11px', color: 'var(--text-tertiary, #9ca3af)', padding: '4px 0' }}>
        {filteredMembers.length} {filteredMembers.length !== 1 ? t('clubs.membersPlural') : t('clubs.membersSingular')}
        {searchTerm && ` ${t('clubs.membersMatching')} "${searchTerm}"`}
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
                {m.name || t('clubs.roleUnknown')}
                <span className={`club-member-role-badge club-member-role-badge--${role}`}>
                  {role === 'owner' ? t('clubs.roleOwner') : role === 'admin' ? t('clubs.roleAdmin') : t('clubs.roleMember')}
                </span>
              </span>
              {canManage && m.email && <span className="club-member-email">{m.email}</span>}
            </div>
            <div className="club-member-actions">
              {canAffect && (
                <>
                  {role === 'member' && (
                    <button className="club-member-role-toggle" onClick={() => handleSetRole(m.id, 'admin')} title={t('clubs.promoteToAdmin')}>
                      ↑ {t('clubs.roleAdmin')}
                    </button>
                  )}
                  {role === 'admin' && (
                    <button className="club-member-role-toggle club-member-role-toggle--demote" onClick={() => handleSetRole(m.id, 'member')} title={t('clubs.demoteToMember')}>
                      ↓ {t('clubs.demoteToMember')}
                    </button>
                  )}
                  {callerRole === 'owner' && !isOwner && (
                    <button className="club-member-role-toggle" onClick={() => handleSetRole(m.id, 'owner')} title={t('clubs.transferOwnership')} style={{ color: '#b45309', fontSize: '11px' }}>
                      ♛ {t('clubs.roleOwner')}
                    </button>
                  )}
                  <button className="club-member-remove" onClick={() => handleRemove(m.id, m.name)} title={t('clubs.removeMember')}>
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

function ClubDetailDrawer({ club, liveClub, joined, calSynced, onToggleCalendar, onClose, clubLoading, t, isAdmin, userId, isSubscribed, onToggleSubscribe, onLogoChanged, isMcGill, onManage }) {
  const [memberRefreshKey, setMemberRefreshKey] = useState(0)
  const [activity, setActivity] = useState(null)        // #11 — recent announcements/events
  const [logoOptimistic, setLogoOptimistic] = useState(null)
  const [logoBusy, setLogoBusy] = useState(false)
  const drawerLogoInputRef = useRef(null)
  const instructionsRef = useRef(null)
  const { isMobile } = useViewport()

  // On mobile this drawer is a full-screen detail view pushed on top of the
  // browse list, so it should slide in from the trailing edge and back out
  // the same way — direction is what makes "deeper" and "back" legible
  // without a breadcrumb. Popping needs the exit animation to finish before
  // the parent unmounts us, hence the local closing state; desktop keeps its
  // existing instant close and its own drawer-slide animation.
  const POP_MS = 200
  const [closing, setClosing] = useState(false)
  const handleClose = useCallback(() => {
    if (!isMobile) { onClose(); return }
    if (closing) return
    setClosing(true)
    setTimeout(onClose, POP_MS)
  }, [isMobile, closing, onClose])

  useEffect(() => {
    if (!club?.id) return
    setLogoOptimistic(null)
    clubsAPI.getClubActivity(club.id, { limit: 4 }).then(setActivity).catch(() => setActivity({ items: [] }))
  }, [club?.id])

  if (!club) return null
  const display = liveClub ? { ...club, ...liveClub } : club
  const meta = getCat(display.category)
  const isLoading = clubLoading[club.id] ?? false
  const isOwnerOrAdmin = isAdmin || (userId && display.created_by === userId)
  const displayLogo = logoOptimistic || display.logo_url

  const handleDrawerLogoPick = () => drawerLogoInputRef.current?.click()
  const handleDrawerLogoFile = async (e) => {
    const file = e.target.files?.[0]
    e.target.value = ''
    if (!file) return
    setLogoBusy(true)
    try {
      const { logo_url } = await clubsAPI.uploadClubLogo(display.id, file)
      setLogoOptimistic(logo_url)
      onLogoChanged?.(display.id, logo_url)
    } catch (err) {
      alert(err.message || 'Upload failed')
    } finally {
      setLogoBusy(false)
    }
  }
  const isPrivate = display.is_private ?? false
  const canManage = isAdmin || display.created_by === userId

  return (
    <div
      className={`club-drawer-overlay${closing ? ' club-drawer-overlay--closing' : ''}`}
      onClick={handleClose}
    >
      <aside
        className={`club-drawer${isMobile ? (closing ? ' m-push-exit' : ' m-push-enter') : ''}`}
        onClick={e => e.stopPropagation()}
      >
        <div className="club-drawer__strip" style={{
          background: `linear-gradient(135deg, ${meta.bg}, transparent)`,
          borderBottom: `3px solid ${meta.color}`
        }}>
          {/* On mobile the drawer becomes a full-screen sheet, so no overlay
              is left to tap — the close button beside the breadcrumb is the
              way out. On desktop the wrapper is `display: contents` and the
              button `display: none`, so the breadcrumb stays the direct flex
              child it has always been and nothing about the layout changes. */}
          <div className="club-drawer__strip-top">
            <Breadcrumb
              className="club-drawer__breadcrumb"
              items={[
                { key: 'clubs', label: t('nav.clubs'), onClick: handleClose },
                { key: 'club', label: display.name },
              ]}
            />
            <button
              type="button"
              className="club-drawer__mobile-close"
              onClick={handleClose}
              aria-label={t('clubs.back')}
              title={t('clubs.back')}
            >
              {/* A back-chevron, not an X: this view was pushed, so the way
                  out is "back", and the icon should agree with the direction
                  the sheet animates. */}
              <FaChevronLeft size={16} />
            </button>
          </div>
          <div className="club-drawer__strip-main">
            <ClubAvatar
              name={display.name}
              category={display.category}
              size="lg"
              // Hide "in your calendar" badge for owners — redundant alongside
              // the owner crown / Manage controls. Still useful for joined-but-
              // not-owned clubs.
              calSynced={calSynced && !(userId && display.created_by === userId)}
              logoUrl={displayLogo}
              editable={isOwnerOrAdmin && !logoBusy}
              onEditClick={handleDrawerLogoPick}
            />
            {isOwnerOrAdmin && (
              <input
                ref={drawerLogoInputRef}
                type="file"
                accept="image/png,image/jpeg,image/webp,image/svg+xml"
                hidden
                onChange={handleDrawerLogoFile}
              />
            )}
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
            {/* Subscribe and Join buttons — hidden for owners/managers */}
            {canManage ? (
              onManage ? (
                <button className="club-action-btn club-action-btn--subscribed" onClick={() => onManage(display)}>
                  <FaCog size={11} /> {t('clubs.manage.manageBtn') || 'Manage club'}
                </button>
              ) : (
                <span className="club-action-btn club-action-btn--subscribed" style={{ cursor: 'default', opacity: 0.75 }}>
                  ✓ {t('clubs.manage.owner') || 'Manager'}
                </span>
              )
            ) : isMcGill ? (
              <>
                <button
                  className={`club-action-btn ${isSubscribed ? 'club-action-btn--subscribed' : 'club-action-btn--subscribe'}`}
                  onClick={() => onToggleSubscribe(club.id)}
                  disabled={isLoading}
                  title={isSubscribed ? t('clubs.unsubscribeTooltip') : t('clubs.subscribeTooltip')}
                >
                  {isSubscribed ? t('clubs.subscribed') : t('clubs.subscribe')}
                </button>
                {/* Join button — application_url first, then join_instructions */}
                {display.application_url ? (
                  <a
                    href={display.application_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="club-action-btn club-action-btn--join"
                    style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '6px' }}
                  >
                    {t('clubs.joinClub')}
                  </a>
                ) : display.join_instructions ? (
                  <button
                    className="club-action-btn club-action-btn--join"
                    onClick={() => instructionsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })}
                  >
                    {t('clubs.joinClub')}
                  </button>
                ) : (
                  <button className="club-action-btn club-action-btn--join" disabled title={t('clubs.noJoinInfo')}>
                    {t('clubs.joinClub')}
                  </button>
                )}
              </>
            ) : (
              <span className="club-action-btn club-action-btn--locked" title="McGill email required">
                <FaLock size={11} /> McGill only
              </span>
            )}
          </div>
        </div>

        <div className="club-drawer__body">
          {/* #10 Four-chip quick-action row at the top of the body */}
          <div className="club-drawer__quick-actions">
            {canManage ? null : isMcGill ? (
              <>
                {display.application_url ? (
                  <a
                    href={display.application_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="club-drawer__chip club-drawer__chip--primary"
                    style={{ background: meta.color }}
                  >
                    <FaUserPlus size={11} /> {joined ? t('clubs.joined') || 'Joined' : t('clubs.joinClub')}
                  </a>
                ) : (
                  <button
                    className="club-drawer__chip club-drawer__chip--primary"
                    style={{ background: meta.color }}
                    onClick={() => display.join_instructions && instructionsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })}
                    disabled={!display.join_instructions}
                  >
                    <FaUserPlus size={11} /> {joined ? t('clubs.joined') || 'Joined' : t('clubs.joinClub')}
                  </button>
                )}
                {joined && (
                  <button
                    className={`club-drawer__chip ${calSynced ? 'club-drawer__chip--active' : ''}`}
                    onClick={() => onToggleCalendar(club.id, !calSynced)}
                    style={calSynced ? { borderColor: meta.color, color: meta.color } : {}}
                  >
                    <FaCalendarAlt size={11} /> {calSynced ? t('clubs.calOn') : t('clubs.calOff')}
                  </button>
                )}
                <button
                  className={`club-drawer__chip ${isSubscribed ? 'club-drawer__chip--active' : ''}`}
                  onClick={() => onToggleSubscribe(club.id)}
                  style={isSubscribed ? { borderColor: meta.color, color: meta.color } : {}}
                  title={isSubscribed ? t('clubs.unsubscribeTooltip') : t('clubs.subscribeTooltip')}
                >
                  <FaBell size={11} /> {isSubscribed ? t('clubs.subscribed') : t('clubs.notifyMe') || 'Notify me'}
                </button>
              </>
            ) : (
              <span className="club-drawer__chip" style={{ opacity: 0.6, cursor: 'default', pointerEvents: 'none' }} title="McGill email required">
                <FaLock size={11} /> McGill email required to join or subscribe
              </span>
            )}
          </div>

          <div className="club-drawer__stats">
            {display.subscriber_count != null && (
              <div className="club-drawer__stat">
                <FaBell size={20} style={{ color: meta.color }} />
                <span className="club-drawer__stat-value">{display.subscriber_count}</span>
                <span className="club-drawer__stat-label">{t('clubs.subscribers') || 'Subscribers'}</span>
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

          {/* #11 Recent activity — shows the club is alive */}
          {activity && activity.items && activity.items.length > 0 && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title">
                <FaBullhorn size={11} /> {t('clubs.recentActivity') || 'Recent activity'}
              </h3>
              <div className="club-drawer__activity-list">
                {activity.items.map(item => (
                  <div key={`${item.type}-${item.id}`} className="club-drawer__activity-item">
                    <span
                      className="club-drawer__activity-badge"
                      style={{ background: item.type === 'event' ? meta.color : '#8b5cf6' }}
                    >
                      {item.type === 'event' ? <FaCalendarAlt size={9} /> : <FaBullhorn size={9} />}
                      {item.type === 'event' ? 'Event' : 'Update'}
                    </span>
                    <div className="club-drawer__activity-content">
                      <div className="club-drawer__activity-title">{item.title}</div>
                      {item.body && <div className="club-drawer__activity-body">{item.body}</div>}
                      <div className="club-drawer__activity-meta">
                        {item.timestamp && new Date(item.timestamp).toLocaleDateString(undefined, { month: 'short', day: 'numeric', year: 'numeric' })}
                        {item.location && <> · {item.location}</>}
                        {item.join_link && <> · <a href={item.join_link} target="_blank" rel="noopener noreferrer" style={{ color: '#1d4ed8' }}>Join</a></>}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {display.description && (
            <section className="club-drawer__section">
              <h3 className="club-drawer__section-title"><FaCheck size={12} /> {t('clubs.about')}</h3>
              <p className="club-drawer__desc">{display.description}</p>
            </section>
          )}

          {display.join_instructions && (
            <section ref={instructionsRef} className="club-drawer__section">
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

function ClubCard({ club, joined, calSynced, isSubscribed, onLeave, onToggleCalendar, onToggleSubscribe, onOpen, onDelete, onEdit, onManage, onLogoChanged, isAdmin, clubLoading, t, userId, isFeatured = false, isMcGill = false }) {
  const meta = getCat(club.category)
  const isLoading = clubLoading[club.id] ?? false
  // Owner or admin both get full manage privileges — invited managers are
  // surfaced via the _manage_role flag the /created endpoint now returns.
  const isOwner   = userId && club.created_by === userId
  const isManager = isOwner || club._manage_role === 'admin'

  // Logo quick-upload (owners only) — click the avatar to swap the picture
  const [logoOptimistic, setLogoOptimistic] = useState(null)
  const [logoBusy, setLogoBusy] = useState(false)
  const logoInputRef = useRef(null)
  const displayLogoUrl = logoOptimistic || club.logo_url

  const handleLogoPick = () => logoInputRef.current?.click()

  const handleLogoFile = async (e) => {
    const file = e.target.files?.[0]
    e.target.value = '' // reset so re-picking same file fires onChange
    if (!file) return
    setLogoBusy(true)
    try {
      const { logo_url } = await clubsAPI.uploadClubLogo(club.id, file)
      setLogoOptimistic(logo_url)
      onLogoChanged?.(club.id, logo_url)
    } catch (err) {
      alert(err.message || 'Upload failed')
    } finally {
      setLogoBusy(false)
    }
  }

  return (
    <article
      className={`club-card ${joined ? 'club-card--joined' : ''} ${isFeatured ? 'club-card--featured' : ''}`}
      onClick={() => onOpen(club)}
    >
      {isFeatured && (
        <div className="club-card__featured-badge" style={{ background: meta.color }}>
          <FaFire size={8} /> {t('clubs.featuredBadge') || 'Trending'}
        </div>
      )}
      {isManager && (
        <input
          ref={logoInputRef}
          type="file"
          accept="image/png,image/jpeg,image/webp,image/svg+xml"
          hidden
          onChange={handleLogoFile}
        />
      )}
      <div className="club-card__body">
        <div className="club-card__top">
          <ClubAvatar
            name={club.name}
            category={club.category}
            size="md"
            // Hide the "in your calendar" badge on clubs you MANAGE — managers
            // already get the crown / Manage controls, so the cal dot is
            // redundant noise on those cards.
            calSynced={calSynced && !isManager}
            logoUrl={displayLogoUrl}
            editable={isManager && !logoBusy}
            onEditClick={handleLogoPick}
          />
          <div className="club-card__info">
            <h3 className="club-card__name">{club.name}</h3>
            <div className="club-card__badges">
              <CategoryBadge category={club.category} t={t} />
            </div>
          </div>
        </div>
        {club.description && (
          <p className="club-card__desc club-card__desc--clamped">{club.description}</p>
        )}
        {(club.subscriber_count != null || club.meeting_schedule || club.location) && (
          <div className="club-card__meta-line">
            {club.subscriber_count != null && (
              <span title={t('clubs.subscribers') || 'Subscribers'}><FaBell size={9} /> {club.subscriber_count}</span>
            )}
            {club.meeting_schedule && (
              <>
                <span className="club-card__meta-sep">\u00b7</span>
                <span><FaCalendarAlt size={9} /> {club.meeting_schedule.length > 18 ? club.meeting_schedule.slice(0,18) + '\u2026' : club.meeting_schedule}</span>
              </>
            )}
            {club.location && (
              <>
                <span className="club-card__meta-sep">\u00b7</span>
                <span><FaStar size={9} /> {club.location}</span>
              </>
            )}
          </div>
        )}
      </div>
      <div className="club-card__footer" onClick={e => e.stopPropagation()}>
        {isManager ? (
          <div className="club-card__footer-joined">
            <button
              className="club-manage-btn"
              onClick={() => onManage?.(club)}
              title={t('clubs.manageClub') || 'Manage club'}
            >
              <FaCog size={11} /> {t('clubs.manageBtnShort') || 'Manage'}
            </button>
            <span className="club-card__owner-pill">
              <FaCrown size={9} /> {isOwner ? t('clubs.managerBadge') : (t('clubs.adminBadge') || 'Admin')}
            </span>
          </div>
        ) : joined ? (
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
        ) : (
          // Discovery-only: small bell-icon Subscribe toggle alongside a
          // primary Join Club button. Subscribe pulls events into the
          // user's calendar; Join links OUT to the club's external apply
          // URL or scrolls the drawer to their join_instructions.
          <div className="club-card__cta-row">
            {isMcGill ? (
              <>
                <button
                  className={`club-bell-toggle ${isSubscribed ? 'club-bell-toggle--on' : ''}`}
                  onClick={(e) => { e.stopPropagation(); onToggleSubscribe(club.id) }}
                  disabled={isLoading}
                  title={isSubscribed ? (t('clubs.subscribed') || 'Subscribed') : (t('clubs.subscribe') || 'Subscribe')}
                  aria-label={isSubscribed ? 'Unsubscribe from updates' : 'Subscribe for updates'}
                >
                  <FaBell size={12} />
                </button>
                {club.application_url ? (
                  <a
                    href={club.application_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="club-join-btn club-join-btn--primary"
                    onClick={e => e.stopPropagation()}
                  >
                    {t('clubs.joinClub')}
                  </a>
                ) : club.join_instructions ? (
                  <button
                    className="club-join-btn club-join-btn--primary"
                    onClick={e => { e.stopPropagation(); onOpen(club) }}
                  >
                    {t('clubs.joinClub')}
                  </button>
                ) : (
                  <button className="club-join-btn club-join-btn--primary" disabled title={t('clubs.noJoinInfo')}>
                    {t('clubs.joinClub')}
                  </button>
                )}
              </>
            ) : (
              <span
                className="club-join-btn club-join-btn--locked"
                title="McGill email required"
                onClick={e => e.stopPropagation()}
              >
                <FaLock size={10} /> McGill only
              </span>
            )}
          </div>
        )}
        {isAdmin && !isOwner && (
          <>
            <button
              className="club-edit-btn"
              onClick={(e) => { e.stopPropagation(); onEdit(club) }}
              title={t('clubs.editClub')}
              style={{ padding: '4px 8px', fontSize: '11px', borderRadius: '6px', border: '1px solid var(--border)', background: 'var(--card-bg)', cursor: 'pointer' }}
            >
              <FaEdit size={10} />
            </button>
            <button
              className="club-delete-chip"
              onClick={(e) => { e.stopPropagation(); const v = window.prompt(`${t('clubs.confirmDeleteClub')} "${club.name}"`); if (v && v.toLowerCase().trim() === 'delete') onDelete(club.id) }}
              title={t('clubs.deleteClub')}
            >
              <FaTimes size={10} />
            </button>
          </>
        )}
        <button className="club-card__open-btn" onClick={() => onOpen(club)} title={t('clubs.viewDetails')}>
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
      <ClubAvatar name={club.name} category={club.category} size="sm" logoUrl={club.logo_url} />
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
            onClick={() => { const v = window.prompt(`${t('clubs.confirmDeleteClub')} "${club.name}"`); if (v && v.toLowerCase().trim() === 'delete') onDelete(club.id) }}
            title={t('clubs.deleteClub')}
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

function CreatedClubRow({ club, onManage, onOpen, t }) {
  return (
    <div className="my-club-row created-club-row" onClick={() => onOpen(club)} style={{ cursor: 'pointer' }}>
      <ClubAvatar name={club.name} category={club.category} size="sm" logoUrl={club.logo_url} />
      <div className="my-club-row__info">
        <span className="my-club-row__name">{club.name}</span>
        <CategoryBadge category={club.category} t={t} />
      </div>
      <div className="my-club-row__right" onClick={e => e.stopPropagation()}>
        {club.subscriber_count != null && (
          <span className="my-club-row__schedule"><FaBell size={10} /> {club.subscriber_count} {(t('clubs.subscribers') || 'Subscribers').toLowerCase()}</span>
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
                    <span className="join-request-name">{req.requester_name || t('clubs.roleUnknown')}</span>
                    {req.requester_email && <span className="join-request-email">{req.requester_email}</span>}
                    {req.requester_linkedin && (
                      <a className="join-request-linkedin" href={req.requester_linkedin} target="_blank" rel="noopener noreferrer">
                        {t('clubs.linkedInProfile')}
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
function ClubManageDashboard({ club, onClose, onSave, onDelete, isAdmin, t }) {
  const [activeSection, setActiveSection] = useState('overview')
  const [managers, setManagers] = useState([])
  const [subscribers, setSubscribers] = useState({ count: 0 })
  const [newManagerEmail, setNewManagerEmail] = useState('')
  const [managerLoading, setManagerLoading] = useState(false)
  const [managerError, setManagerError] = useState('')
  const [managerSuccess, setManagerSuccess] = useState('')
  const [announcements, setAnnouncements] = useState([])
  const [events, setEvents] = useState([])
  const [annForm, setAnnForm] = useState({ title: '', body: '', join_link: '' })
  const [annSubmitting, setAnnSubmitting] = useState(false)
  const [eventForm, setEventForm] = useState({ title: '', description: '', event_date: '', location: '', join_link: '' })
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
  const [editError, setEditError] = useState('')

  // Logo upload state
  const [logoUrl, setLogoUrl] = useState(club?.logo_url || null)
  const [logoUploading, setLogoUploading] = useState(false)
  const [logoError, setLogoError] = useState('')
  const logoFileRef = useRef(null)

  const handleLogoFile = async (file) => {
    if (!file) return
    setLogoError(''); setLogoUploading(true)
    try {
      const { logo_url } = await clubsAPI.uploadClubLogo(club.id, file)
      setLogoUrl(logo_url)
    } catch (e) {
      setLogoError(e.message || 'Upload failed')
    } finally {
      setLogoUploading(false)
    }
  }
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
      // Send a manager-invite REQUEST; the target user accepts/denies from
      // their own Clubs tab. They become an admin only on accept.
      await clubsAPI.createManagerRequest(club.id, newManagerEmail.trim())
      setNewManagerEmail('')
      setManagerSuccess(t('clubs.manage.managerInviteSent') || 'Invite sent, they will see it in their Clubs tab.')
      setTimeout(() => setManagerSuccess(''), 4000)
    } catch (e) {
      setManagerError(e.message)
    } finally {
      setManagerLoading(false)
    }
  }

  const handleSaveEdit = async (e) => {
    e.preventDefault()
    if (!editForm.application_url?.trim() && !editForm.join_instructions?.trim()) {
      setEditError(t('clubs.joinRequiredError') || 'Please fill in either the Application URL or How to Join instructions.')
      return
    }
    setEditError('')
    setEditSubmitting(true)
    try {
      await onSave(club.id, editForm)
      setEditSuccess(true)
      setTimeout(() => setEditSuccess(false), 3000)
    } catch (err) {
      setEditError(err?.message || 'Failed to save changes.')
    } finally { setEditSubmitting(false) }
  }

  const handleCreateAnnouncement = async (e) => {
    e.preventDefault()
    if (!annForm.title.trim()) return
    setAnnSubmitting(true)
    try {
      await clubsAPI.createClubAnnouncement(club.id, annForm)
      setAnnForm({ title: '', body: '', join_link: '' })
      // Refresh announcements
      clubsAPI.getClubAnnouncements?.(club.id)?.then?.(d => setAnnouncements(d.announcements || d || []))?.catch?.(() => {})
    } catch { /* ignore */ }
    finally { setAnnSubmitting(false) }
  }

  const handleDeleteAnnouncement = async (annId) => {
    try {
      await clubsAPI.deleteClubAnnouncement(club.id, annId)
      setAnnouncements(prev => prev.filter(a => a.id !== annId))
    } catch { /* ignore */ }
  }

  const handleCreateEvent = async (e) => {
    e.preventDefault()
    if (!eventForm.title.trim() || !eventForm.event_date) return
    setEventSubmitting(true)
    try {
      await clubsAPI.createClubEvent(club.id, eventForm)
      setEventForm({ title: '', description: '', event_date: '', location: '', join_link: '' })
      clubsAPI.getClubEvents?.(club.id)?.then?.(d => setEvents(d.events || d || []))?.catch?.(() => {})
    } catch { /* ignore */ }
    finally { setEventSubmitting(false) }
  }

  const handleDeleteEvent = async (eventId) => {
    try {
      await clubsAPI.deleteClubEvent(club.id, eventId)
      setEvents(prev => prev.filter(ev => ev.id !== eventId))
    } catch { /* ignore */ }
  }

  const sections = [
    { key: 'overview', icon: <FaStar size={13} />, label: t('clubs.manage.overview') },
    { key: 'edit', icon: <FaEdit size={13} />, label: t('clubs.manage.editInfo') },
    // Execs tab — clubs have an owner and admins (no regular members on this
    // site, which is discovery-only).
    { key: 'members', icon: <FaUsers size={13} />, label: t('clubs.manage.execs') },
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
            <ClubAvatar name={club.name} category={club.category} size="md" logoUrl={club.logo_url} />
            <div>
              <h2 className="club-manage__title">{club.name}</h2>
              <p className="club-manage__subtitle">{t('clubs.manage.dashboardTitle')}</p>
            </div>
          </div>
          <div className="club-manage__header-right">
            {isAdmin && (
              <button
                className="club-manage__delete-btn"
                onClick={() => {
                  const v = window.prompt(`${t('clubs.confirmDeleteClub')} "${club.name}"`)
                  if (v && v.toLowerCase().trim() === 'delete') { onDelete(club.id); onClose() }
                }}
                title={t('clubs.deleteClub')}
              >
                <FaTrash size={11} /> {t('clubs.deleteClub')}
              </button>
            )}
            <button className="clubs-modal__close" onClick={onClose}><FaTimes /></button>
          </div>
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
                  <FaBell size={20} style={{ color: meta.color }} />
                  <div className="club-manage__stat-val">{subscribers.count ?? club.subscriber_count ?? 0}</div>
                  <div className="club-manage__stat-label">{t('clubs.subscribers') || 'Subscribers'}</div>
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
                <p><strong>{t('clubs.fieldCategory')}:</strong> {club.category || '-'}</p>
                <p><strong>{t('clubs.fieldEmail')}:</strong> {club.contact_email || '-'}</p>
                <p><strong>{t('clubs.fieldUrl')}:</strong> {club.website_url ? <a href={club.website_url} target="_blank" rel="noopener noreferrer">{club.website_url}</a> : '-'}</p>
                <p><strong>{t('clubs.fieldSchedule')}:</strong> {club.meeting_schedule || '-'}</p>
                <p><strong>{t('clubs.fieldVisibility')}:</strong> {club.is_private ? t('clubs.private') : t('clubs.visibilityPublic')}</p>
              </div>
            </div>
          )}

          {/* ── Edit Info ── */}
          {activeSection === 'edit' && (
            <form className="club-manage__edit-form" onSubmit={handleSaveEdit}>
              {editSuccess && <div className="club-manage__success"><FaCheck size={12} /> {t('clubs.manage.saved')}</div>}

              {/* Logo upload */}
              <div className="clubs-field">
                <label>{t('clubs.fieldLogo') || 'Club logo'}</label>
                <div className="club-logo-uploader">
                  <ClubAvatar name={editForm.name || club?.name} category={editForm.category || club?.category} size="lg" logoUrl={logoUrl} />
                  <div className="club-logo-uploader__actions">
                    <input
                      ref={logoFileRef}
                      type="file"
                      accept="image/png,image/jpeg,image/webp,image/svg+xml"
                      hidden
                      onChange={e => handleLogoFile(e.target.files?.[0])}
                    />
                    <button
                      type="button"
                      className="clubs-modal__btn clubs-modal__btn--secondary"
                      onClick={() => logoFileRef.current?.click()}
                      disabled={logoUploading}
                    >
                      {logoUploading
                        ? <><div className="btn-spinner" /> {t('clubs.uploading') || 'Uploading…'}</>
                        : logoUrl
                          ? (t('clubs.changeLogo') || 'Change logo')
                          : (t('clubs.uploadLogo') || 'Upload logo')}
                    </button>
                    {logoUrl && (
                      <button
                        type="button"
                        className="clubs-modal__btn clubs-modal__btn--ghost"
                        onClick={async () => {
                          setLogoUrl(null)
                          try { await clubsAPI.editClub(club.id, { logo_url: '' }) } catch { /* ignore */ }
                        }}
                        disabled={logoUploading}
                      >
                        <FaTrash size={11} /> {t('clubs.removeLogo') || 'Remove'}
                      </button>
                    )}
                    <p className="club-logo-uploader__hint">
                      {t('clubs.logoHint') || 'Square image, under 2 MB. PNG, JPG, WebP, or SVG.'}
                    </p>
                    {logoError && <p className="club-logo-uploader__err"><FaExclamationTriangle size={11} /> {logoError}</p>}
                  </div>
                </div>
              </div>

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
              <div className="clubs-join-required-note">
                <FaExclamationTriangle style={{ marginRight: '4px', verticalAlign: 'middle', flexShrink: 0 }} /><strong>{t('clubs.joinRequiredLabel')}</strong> {t('clubs.joinRequiredNote')}
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldApplicationUrl')}</label>
                <input value={editForm.application_url} onChange={e => { setEditForm(f => ({ ...f, application_url: e.target.value })); setEditError('') }} placeholder="https://..." />
                <span className="clubs-field-hint">{t('clubs.fieldApplicationUrlHint')}</span>
              </div>
              <div className="clubs-field">
                <label>{t('clubs.fieldJoinInstructions')}</label>
                <textarea value={editForm.join_instructions} onChange={e => { setEditForm(f => ({ ...f, join_instructions: e.target.value })); setEditError('') }} rows={3} placeholder={t('clubs.fieldJoinInstructionsPlaceholder')} />
                <span className="clubs-field-hint">{t('clubs.fieldJoinInstructionsHint')}</span>
              </div>
              {editError && <div className="clubs-edit-error">{editError}</div>}
              <div className="clubs-field">
                <label>{t('clubs.fieldExecutiveEmails')}</label>
                <input value={editForm.executive_emails} onChange={e => setEditForm(f => ({ ...f, executive_emails: e.target.value }))} placeholder="exec1@mail.mcgill.ca, exec2@mail.mcgill.ca" />
                <span className="clubs-field-hint">{t('clubs.fieldExecutiveEmailsHint')}</span>
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

          {/* ── Members (replaces the old separate Managers tab) ── */}
          {activeSection === 'members' && (
            <div className="club-manage__members">
              {/* Promote a McGill email straight to admin — kept from old
                  Managers tab. Owner/admin can still demote later from the list. */}
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

              {/* Unified member list — MembersSection already sorts owners
                  first, then admins, then members; and renders promote /
                  demote / remove inline for callers with the right role. */}
              <MembersSection
                clubId={club.id}
                clubOwnerId={club.created_by}
                meta={meta}
                refreshKey={managerLoading ? 1 : 0}
              />
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
                <div className="clubs-field">
                  <label>{t('clubs.manage.joinLink') || 'Join Link'}</label>
                  <input type="url" value={annForm.join_link} onChange={e => setAnnForm(f => ({ ...f, join_link: e.target.value }))} placeholder="Zoom, Teams, or other link…" />
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
                    {a.join_link && <p><a href={a.join_link} target="_blank" rel="noopener noreferrer" style={{ color: '#1d4ed8', fontSize: '13px' }}>Join Link</a></p>}
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
                <div className="clubs-field">
                  <label>{t('clubs.manage.joinLink') || 'Join Link'}</label>
                  <input type="url" value={eventForm.join_link} onChange={e => setEventForm(f => ({ ...f, join_link: e.target.value }))} placeholder="Zoom, Teams, or other link…" />
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
                      {ev.location && <span><FaMapMarkerAlt size={10} /> {ev.location}</span>}
                    </div>
                    {ev.description && <p>{ev.description}</p>}
                    {ev.join_link && <p><a href={ev.join_link} target="_blank" rel="noopener noreferrer" style={{ color: '#1d4ed8', fontSize: '13px' }}>Join Link</a></p>}
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
    if (!form.application_url.trim() && !form.join_instructions.trim() && !form.website_url.trim()) {
      e.joinMethod = t('clubs.joinMethodRequired') || 'Please provide at least one: Application URL, Join Instructions, or Website URL so members know how to join.'
    }
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
            <div className="clubs-join-required-note">
              <FaExclamationTriangle style={{ marginRight: '4px', verticalAlign: 'middle', flexShrink: 0 }} /><strong>{t('clubs.joinRequiredLabel')}</strong> {t('clubs.joinRequiredNote')}
            </div>
            {errors.joinMethod && (
              <div style={{ background: '#fef2f2', border: '1px solid #fca5a5', borderRadius: '8px', padding: '10px 14px', fontSize: '13px', color: '#b91c1c', display: 'flex', alignItems: 'flex-start', gap: '8px' }}>
                <FaExclamationTriangle style={{ flexShrink: 0 }} />
                <span>{errors.joinMethod}</span>
              </div>
            )}
            <div className={`clubs-field ${errors.joinMethod ? 'error' : ''}`}>
              <label>{t('clubs.fieldApplicationUrl')}</label>
              <input type="url" value={form.application_url} onChange={e => set('application_url')(e.target.value)} placeholder="https://..." />
              <span className="clubs-field-hint">{t('clubs.fieldApplicationUrlHint')}</span>
            </div>
            <div className={`clubs-field ${errors.joinMethod ? 'error' : ''}`}>
              <label>{t('clubs.fieldJoinInstructions')}</label>
              <textarea value={form.join_instructions} onChange={e => set('join_instructions')(e.target.value)} rows={3} placeholder={t('clubs.fieldJoinInstructionsPlaceholder')} />
              <span className="clubs-field-hint">{t('clubs.fieldJoinInstructionsHint')}</span>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldExecEmails')} <span style={{ color: 'var(--accent-primary)' }}>*</span></label>
              <textarea value={form.executive_emails} onChange={e => set('executive_emails')(e.target.value)} rows={2} placeholder={t('clubs.fieldExecEmailsPlaceholder')} />
              <span className="clubs-field-hint">{t('clubs.fieldExecEmailsHint')}</span>
            </div>
            <div className="clubs-field">
              <label>{t('clubs.fieldVisibility')}</label>
              <div className="clubs-visibility-toggle">
                <button type="button" className={`clubs-visibility-option ${!form.is_private ? 'active' : ''}`} onClick={() => set('is_private')(false)}>
                  <FaGlobe size={12} /> {t('clubs.visibilityPublic')}
                </button>
                <button type="button" className={`clubs-visibility-option ${form.is_private ? 'active' : ''}`} onClick={() => set('is_private')(true)}>
                  <FaLock size={11} /> {t('clubs.visibilityPrivate')}
                </button>
              </div>
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
  const { t, language } = useLanguage()
  const { profile } = useAuth()
  const isAdmin   = authFlags?.is_admin        ?? false
  const isMcGill  = authFlags?.is_mcgill_email ?? false
  const [activeView, setActiveView] = useState('explore')
  const [clubs, setClubs] = useState([])
  // SWR-style hydrate from cache for instant first paint
  const [myClubs, setMyClubs]         = useState(() => readCache('my_clubs', user?.id, []))
  const [createdClubs, setCreatedClubs] = useState(() => readCache('created_clubs', user?.id, []))
  const [pendingCounts, setPendingCounts] = useState({})
  const [search, setSearch] = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [sortMode, setSortMode] = useState('default')
  const [categoryFilter, setCategoryFilter] = useState('')
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
  const [subscribedIds, setSubscribedIds] = useState(() => new Set(readCache('subscriptions', user?.id, [])))
  const debounceRef = useRef(null)
  const isMounted = useRef(true)

  useEffect(() => {
    isMounted.current = true
    return () => { isMounted.current = false }
  }, [])

  // Fetch user subscriptions on mount (cache for instant subsequent renders)
  useEffect(() => {
    if (!user?.id) return
    clubsAPI.getUserSubscriptions(user.id).then(data => {
      const ids = data.subscribed_club_ids || []
      if (isMounted.current) setSubscribedIds(new Set(ids))
      writeCache('subscriptions', user.id, ids)
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
        category: categoryFilter || undefined,
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
  }, [debouncedSearch, categoryFilter])

  const fetchMyClubs = useCallback(async () => {
    if (!user?.id) return
    // Only show the spinner if we don't already have cached data on screen
    if (myClubs.length === 0) setMyClubsLoading(true)
    try {
      const data = await clubsAPI.getUserClubs(user.id)
      const list = Array.isArray(data) ? data : data.clubs ?? []
      if (!isMounted.current) return
      setMyClubs(list)
      writeCache('my_clubs', user.id, list)
      if (onClubEventsChange) onClubEventsChange(buildClubCalendarEvents(list))
    } catch { /* silent */ }
    finally { if (isMounted.current) setMyClubsLoading(false) }
  }, [user?.id, onClubEventsChange, myClubs.length])

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
      writeCache('created_clubs', user.id, list)
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

  const fetchPendingRequests = useCallback(async () => {
    if (!user?.id) return
    try {
      const data = await clubsAPI.getUserPendingRequests(user.id)
      if (isMounted.current) setPendingRequestClubIds(new Set(data.pending_club_ids || []))
    } catch { /* silent */ }
  }, [user?.id])

  // Manager-invite inbox — invitations sent to me, awaiting my response
  const [managerInvites, setManagerInvites] = useState([])
  const fetchManagerInvites = useCallback(async () => {
    try {
      const data = await clubsAPI.getIncomingManagerRequests()
      if (isMounted.current) setManagerInvites(data.requests || [])
    } catch { /* silent */ }
  }, [])

  const respondToInvite = useCallback(async (inviteId, action) => {
    // Optimistic: hide the invite immediately
    setManagerInvites(prev => prev.filter(r => r.id !== inviteId))
    try {
      await clubsAPI.respondToManagerRequest(inviteId, action)
      if (action === 'accept') {
        // Pull fresh my-clubs / created-clubs so the new admin role shows up
        fetchMyClubs()
        fetchCreatedClubs()
      }
    } catch (e) {
      alert(e.message || 'Failed')
      fetchManagerInvites()  // reload on failure to recover state
    }
  }, [fetchMyClubs, fetchCreatedClubs, fetchManagerInvites])

  useEffect(() => { setPage(1); fetchClubs(1) }, [fetchClubs])
  useEffect(() => { fetchMyClubs() }, [fetchMyClubs])
  useEffect(() => { fetchCreatedClubs() }, [fetchCreatedClubs])
  useEffect(() => { fetchPendingRequests() }, [fetchPendingRequests])
  useEffect(() => { fetchManagerInvites() }, [fetchManagerInvites])

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
    if (!isMcGill) {
      setError('Only McGill email addresses (@mcgill.ca or @mail.mcgill.ca) can join clubs.')
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
      setClubs(prev => prev.map(c => c.id === clubId ? { ...c, subscriber_count: Math.max(0, (c.subscriber_count ?? 1) - 1) } : c))
      if (openClub?.id === clubId) setOpenClub(prev => prev ? { ...prev, subscriber_count: Math.max(0, (prev.subscriber_count ?? 1) - 1) } : prev)
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
    const result = await clubsAPI.editClub(clubId, formData)
    const updated = result?.club
    if (updated) {
      setClubs(prev => prev.map(c => c.id === clubId ? { ...c, ...updated } : c))
    }
    await fetchCreatedClubs()
  }

  // Fired after a successful logo upload from a card or the drawer — patch
  // the loaded clubs in place so other parts of the UI reflect the new URL
  // without a full refetch.
  const handleLogoChanged = useCallback((clubId, newLogoUrl) => {
    setClubs(prev => prev.map(c => c.id === clubId ? { ...c, logo_url: newLogoUrl } : c))
    setCreatedClubs(prev => prev.map(c => c.id === clubId ? { ...c, logo_url: newLogoUrl } : c))
    setMyClubs(prev => prev.map(m => {
      const cl = m.club ?? m
      if (cl.id !== clubId) return m
      return m.club ? { ...m, club: { ...m.club, logo_url: newLogoUrl } } : { ...m, logo_url: newLogoUrl }
    }))
  }, [])

  const displayClubs = useMemo(() => {
    let list = [...clubs]
    if (sortMode === 'members') list.sort((a, b) => (b.subscriber_count ?? 0) - (a.subscriber_count ?? 0))
    if (sortMode === 'name') list.sort((a, b) => (a.name ?? '').localeCompare(b.name ?? ''))
    return list
  }, [clubs, sortMode])

  // #2/#3 — Curated rows computed from the loaded page of clubs.
  // Trending = top 5 by subscriber_count; For You = clubs in categories that
  // loosely match the user's major/faculty keywords.
  const trendingClubs = useMemo(() => {
    if (clubs.length < 4) return []
    return [...clubs]
      .filter(c => c.subscriber_count != null && c.subscriber_count >= 1)
      .sort((a, b) => (b.subscriber_count ?? 0) - (a.subscriber_count ?? 0))
      .slice(0, 5)
  }, [clubs])

  // Heuristic mapping from program keywords → club categories that overlap
  const CATEGORY_HINTS = {
    'Engineering & Technology': ['engineering', 'computer', 'software', 'mechanical', 'electrical'],
    'Science':                  ['science', 'physics', 'chemistry', 'biology', 'math'],
    'Academic':                 ['arts', 'humanities', 'literature', 'history'],
    'Health & Wellness':        ['nursing', 'medicine', 'dentistry', 'physiology', 'kinesiology'],
    'Debate & Politics':        ['political', 'politics', 'international'],
    'Arts & Culture':           ['music', 'art', 'theatre', 'film'],
    'Environment':              ['environment', 'sustainability', 'geography'],
    'Athletics & Recreation':   ['kinesiology', 'physical education'],
  }

  const forYouClubs = useMemo(() => {
    if (clubs.length < 4) return []
    const blob = `${profile?.major || ''} ${profile?.faculty || ''} ${profile?.minor || ''}`.toLowerCase()
    if (!blob.trim()) return []
    const matchingCategories = new Set()
    for (const [cat, hints] of Object.entries(CATEGORY_HINTS)) {
      if (hints.some(h => blob.includes(h))) matchingCategories.add(cat)
    }
    if (!matchingCategories.size) return []
    return clubs
      .filter(c => matchingCategories.has(c.category))
      .slice(0, 5)
  }, [clubs, profile?.major, profile?.faculty, profile?.minor])

  const forYouLabel = useMemo(() => {
    if (profile?.major) return `${t('clubs.basedOn') || 'Based on'} ${profile.major}`
    if (profile?.faculty) return `${t('clubs.basedOn') || 'Based on'} ${profile.faculty}`
    return t('clubs.pickedForYou') || 'Picked for you'
  }, [profile?.major, profile?.faculty, t])

  // #4 — Clubs the user subscribes to but hasn't joined or created
  const watchingClubs = useMemo(() => {
    const joined = new Set([...joinedIds])
    const created = new Set(createdClubs.map(c => c.id))
    return clubs.filter(c => subscribedIds.has(c.id) && !joined.has(c.id) && !created.has(c.id))
  }, [clubs, subscribedIds, joinedIds, createdClubs])

  const clubsById = useMemo(() => {
    const map = {}
    clubs.forEach(c => { map[c.id] = c })
    return map
  }, [clubs])

  const totalPendingRequests = useMemo(() =>
    // Sum of join requests pending on clubs the user manages
    Object.values(pendingCounts).reduce((sum, c) => sum + c, 0)
    // ...plus manager invites pending for the current user themselves
    + managerInvites.length,
    [pendingCounts, managerInvites.length]
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

      <div className="clubs-tabs" data-tour="clubs-tabs">
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
          {/* #1 — Search + sort on one row, more compact */}
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
              <select className="clubs-sort-select" value={categoryFilter} onChange={e => setCategoryFilter(e.target.value)}>
                <option value="">{t('clubs.filterTypeAll')}</option>
                {Object.keys(CATEGORY_META).filter(k => k !== 'Default').map(c => (
                  <option key={c} value={c}>{t(CATEGORY_I18N_KEY[c] || c) || c}</option>
                ))}
              </select>
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

          {error && <div className="clubs-error">{error}<button onClick={() => setError(null)}><FaTimes size={11} /></button></div>}

          {/* #2/#3 — Curated rows visible only when not actively searching */}
          {!loading && !debouncedSearch && trendingClubs.length > 0 && (
            <div className="clubs-curated-row">
              <div className="clubs-curated-row__header">
                <h3 className="clubs-curated-row__title"><FaFire size={13} style={{ color: '#f59e0b' }} /> {t('clubs.trendingTitle') || 'Trending this week'}</h3>
                <span className="clubs-curated-row__sub">{t('clubs.trendingHint') || 'Most popular on Symbolos'}</span>
              </div>
              <div className="clubs-curated-row__strip">
                {trendingClubs.map(club => (
                  <ClubCard
                    key={`trend-${club.id}`}
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
                    onManage={setManagingClub}
                    onLogoChanged={handleLogoChanged}
                    isFeatured
                    isAdmin={isAdmin}
                    isMcGill={isMcGill}
                    clubLoading={clubLoading}
                    userId={user?.id}
                    language={language}
                    t={t}
                  />
                ))}
              </div>
            </div>
          )}

          {!loading && !debouncedSearch && forYouClubs.length > 0 && (
            <div className="clubs-curated-row">
              <div className="clubs-curated-row__header">
                <h3 className="clubs-curated-row__title"><FaGem size={12} style={{ color: 'var(--accent-primary)' }} /> {t('clubs.forYouTitle') || 'For you'}</h3>
                <span className="clubs-curated-row__sub">{forYouLabel}</span>
              </div>
              <div className="clubs-curated-row__strip">
                {forYouClubs.map(club => (
                  <ClubCard
                    key={`fy-${club.id}`}
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
                    onManage={setManagingClub}
                    onLogoChanged={handleLogoChanged}
                    isAdmin={isAdmin}
                    isMcGill={isMcGill}
                    clubLoading={clubLoading}
                    userId={user?.id}
                    language={language}
                    t={t}
                  />
                ))}
              </div>
            </div>
          )}

          {loading ? (
            // #13 Skeleton placeholders instead of spinner
            <div className="clubs-grid">
              {Array.from({ length: 6 }).map((_, i) => <ClubCardSkeleton key={`skel-${i}`} />)}
            </div>
          ) : displayClubs.length === 0 ? (
            // #14 Better empty state with actionable suggestions
            <div className="clubs-empty">
              <div className="clubs-empty__visual"><FaUsers size={52} /></div>
              <h3>{debouncedSearch ? (t('clubs.noClubsFound') || 'No clubs match those filters') : t('clubs.noClubsYet')}</h3>
              <p>
                {debouncedSearch
                  ? (t('clubs.tryClearSearch') || 'Try a different search term.')
                  : t('clubs.noClubsYetDesc')}
              </p>
              <div className="clubs-empty__actions">
                {debouncedSearch && (
                  <button
                    className="club-action-btn club-action-btn--subscribe"
                    onClick={() => setSearch('')}
                  >
                    <FaTimes size={11} /> {t('clubs.clearFilters') || 'Clear filters'}
                  </button>
                )}
                <button className="club-action-btn club-action-btn--join" onClick={() => setShowSubmitModal(true)}>
                  <FaPlus size={11} /> {t('clubs.requestAddBtn')}
                </button>
              </div>
            </div>
          ) : (
            <>
              <p className="clubs-results-label">
                <strong>{displayClubs.length}</strong> {displayClubs.length !== 1 ? t('clubs.results').replace('{count}','').trim() : t('clubs.result').replace('{count}','').trim()}
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
                    onManage={setManagingClub}
                    onLogoChanged={handleLogoChanged}
                    language={language}
                    onToggleCalendar={handleToggleCalendar}
                    onToggleSubscribe={handleToggleSubscribe}
                    onOpen={setOpenClub}
                    onDelete={handleDeleteClub}
                    onEdit={setEditingClub}
                    isAdmin={isAdmin}
                    isMcGill={isMcGill}
                    clubLoading={clubLoading}
                    userId={user?.id}
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
          {/* Manager-invite inbox — pinned at the top so users see it instantly */}
          {managerInvites.length > 0 && (
            <div className="clubs-mine__section clubs-invite-inbox">
              <h3 className="clubs-mine__section-title">
                <FaBell size={13} /> {t('clubs.managerInvitesTitle') || 'Manager invitations'}
                <span className="clubs-mine__section-count">{managerInvites.length}</span>
              </h3>
              <div className="clubs-invite-list">
                {managerInvites.map(inv => {
                  const clubName = inv?.clubs?.name || 'a club'
                  const requester = inv.requested_by_name || 'A manager'
                  return (
                    <div key={inv.id} className="clubs-invite-row">
                      <div className="clubs-invite-row__avatar">
                        <ClubAvatar
                          name={clubName}
                          category={inv?.clubs?.category}
                          size="sm"
                          logoUrl={inv?.clubs?.logo_url}
                        />
                      </div>
                      <div className="clubs-invite-row__body">
                        <p className="clubs-invite-row__text">
                          <strong>{requester}</strong> {t('clubs.invitedYouTo') || 'invited you to manage'} <strong>{clubName}</strong>
                        </p>
                        {inv.message && <p className="clubs-invite-row__msg">"{inv.message}"</p>}
                      </div>
                      <div className="clubs-invite-row__actions">
                        <button
                          className="club-action-btn club-action-btn--join"
                          onClick={() => respondToInvite(inv.id, 'accept')}
                        >
                          <FaCheck size={10} /> {t('clubs.accept') || 'Accept'}
                        </button>
                        <button
                          className="club-action-btn club-action-btn--subscribe"
                          onClick={() => respondToInvite(inv.id, 'deny')}
                        >
                          <FaTimes size={10} /> {t('clubs.deny') || 'Deny'}
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {myClubsLoading ? (
            <div className="clubs-loading"><div className="clubs-spinner" /><p>{t('clubs.loadingMine')}</p></div>
          ) : (
            <>
              {/* Created Clubs Section */}
              {createdClubs.length > 0 && (
                <div className="clubs-mine__section">
                  <h3 className="clubs-mine__section-title">
                    <FaStar size={13} /> {isAdmin ? t('clubs.manageClubs') : t('clubs.createdByYou')}
                    <span className="clubs-mine__section-count">{createdClubs.length}</span>
                  </h3>
                  <div className="clubs-mine__list">
                    {createdClubs.map(club => (
                      <CreatedClubRow
                        key={club.id}
                        club={club}
                        onEdit={setEditingClub}
                        onManage={setManagingClub}
                    onLogoChanged={handleLogoChanged}
                        onManageRequests={setManagingRequestsClub}
                        onOpen={setOpenClub}
                        pendingCount={pendingCounts[club.id] || 0}
                        t={t}
                      />
                    ))}
                  </div>
                </div>
              )}

              {/* Joined Clubs section removed — discovery-only site, no
                  "joining" concept. Subscriptions live in the Watching section
                  below. */}

              {/* #4 — Subscribed / Watching section (clubs you follow but haven't joined) */}
              {watchingClubs.length > 0 && (
                <div className="clubs-mine__section">
                  <h3 className="clubs-mine__section-title">
                    <FaBell size={12} /> {t('clubs.watchingClubs') || 'Watching'}
                    <span className="clubs-mine__section-count">{watchingClubs.length}</span>
                  </h3>
                  <div className="clubs-grid clubs-grid--mine-watching">
                    {watchingClubs.map(club => (
                      <ClubCard
                        key={`watch-${club.id}`}
                        club={club}
                        joined={false}
                        calSynced={false}
                        hasPendingRequest={pendingRequestClubIds.has(club.id)}
                        isSubscribed={true}
                        onJoin={handleJoin}
                        onLeave={handleLeave}
                        onToggleCalendar={handleToggleCalendar}
                        onToggleSubscribe={handleToggleSubscribe}
                        onOpen={setOpenClub}
                        onDelete={handleDeleteClub}
                        onEdit={setEditingClub}
                        onManage={setManagingClub}
                    onLogoChanged={handleLogoChanged}
                        isAdmin={isAdmin}
                    isMcGill={isMcGill}
                        clubLoading={clubLoading}
                        userId={user?.id}
                        language={language}
                        t={t}
                      />
                    ))}
                  </div>
                </div>
              )}
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
          onLogoChanged={handleLogoChanged}
          clubLoading={clubLoading}
          t={t}
          isAdmin={isAdmin}
          userId={user?.id}
          isMcGill={isMcGill}
          onManage={(clubToManage) => { setOpenClub(null); setManagingClub(clubToManage) }}
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
          onDelete={handleDeleteClub}
          t={t}
          isAdmin={isAdmin}
        />
      )}
    </div>
  )
}

// eslint-disable-next-line react-refresh/only-export-components -- pure helper, also imported by tests
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
