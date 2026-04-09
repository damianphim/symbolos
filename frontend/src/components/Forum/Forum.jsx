import { useState, useEffect, useRef, useCallback } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/LanguageContext'
import forumAPI from '../../lib/forumAPI'
import {
  FaComments, FaThumbsUp, FaReply, FaSearch, FaFire,
  FaClock, FaStar, FaPlus, FaTimes, FaChevronDown,
  FaChevronUp, FaBookOpen, FaUsers, FaLightbulb,
  FaBullhorn, FaGraduationCap, FaPaperPlane, FaSpinner,
  FaTag, FaTrash, FaFlag,
} from 'react-icons/fa'
import './Forum.css'

// ── Category / sort helpers (call with t inside components) ───────
function getCategories(t) {
  return [
    { key: 'all',      label: t('forum.catAll'),      icon: <FaComments />,      color: '#ed1b2f' },
    { key: 'courses',  label: t('forum.catCourses'),   icon: <FaBookOpen />,      color: '#3b82f6' },
    { key: 'study',    label: t('forum.catStudy'),     icon: <FaUsers />,         color: '#10b981' },
    { key: 'advice',   label: t('forum.catAdvice'),    icon: <FaLightbulb />,     color: '#f59e0b' },
    { key: 'general',  label: t('forum.catGeneral'),   icon: <FaBullhorn />,      color: '#8b5cf6' },
    { key: 'planning', label: t('forum.catPlanning'),  icon: <FaGraduationCap />, color: '#ed1b2f' },
  ]
}

function getSortOptions(t) {
  return [
    { key: 'hot', label: t('forum.sortHot'), icon: <FaFire /> },
    { key: 'new', label: t('forum.sortNew'), icon: <FaClock /> },
    { key: 'top', label: t('forum.sortTop'), icon: <FaStar /> },
  ]
}

// ── Utility ──────────────────────────────────────────────────────
function timeAgo(ts, t) {
  const diff = Date.now() - new Date(ts).getTime()
  const m = Math.floor(diff / 60000)
  if (m < 1) return t('forum.timeJustNow')
  if (m < 60) return `${m}${t('forum.timeMin')}`
  const h = Math.floor(m / 60)
  if (h < 24) return `${h}${t('forum.timeHour')}`
  return `${Math.floor(h / 24)}${t('forum.timeDay')}`
}

function Avatar({ letter, color, size = 32 }) {
  return (
    <div style={{
      width: size, height: size, borderRadius: '50%',
      background: color || '#ed1b2f', color: '#fff',
      display: 'flex', alignItems: 'center', justifyContent: 'center',
      fontSize: size * 0.4, fontWeight: 700, flexShrink: 0,
    }}>
      {(letter || '?')[0].toUpperCase()}
    </div>
  )
}

// ── New Post Modal ────────────────────────────────────────────────
function NewPostModal({ onClose, onSubmit, isSubmitting }) {
  const { t } = useLanguage()
  const CATEGORIES = getCategories(t)
  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [category, setCategory] = useState('general')
  const [tags, setTags] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!title.trim() || !body.trim()) return
    onSubmit({
      title: title.trim(), body: body.trim(), category,
      tags: tags.split(',').map(tag => tag.trim()).filter(Boolean),
    })
  }

  return (
    <div className="forum-modal-overlay" onClick={onClose}>
      <div className="forum-modal" onClick={e => e.stopPropagation()}>
        <div className="forum-modal__header">
          <h2 className="forum-modal__title">{t('forum.modalCreateTitle')}</h2>
          <button className="forum-modal__close" onClick={onClose}><FaTimes /></button>
        </div>
        <form className="forum-modal__body" onSubmit={handleSubmit}>
          <div className="forum-modal__field">
            <label className="forum-modal__label">{t('forum.modalCategory')}</label>
            <div className="forum-modal__cat-grid">
              {CATEGORIES.filter(c => c.key !== 'all').map(cat => (
                <button key={cat.key} type="button"
                  className={`forum-modal__cat-btn ${category === cat.key ? 'active' : ''}`}
                  style={{ '--cat-color': cat.color }}
                  onClick={() => setCategory(cat.key)}
                >
                  {cat.icon} {cat.label}
                </button>
              ))}
            </div>
          </div>
          <div className="forum-modal__field">
            <label className="forum-modal__label">{t('forum.modalTitleLabel')}</label>
            <input className="forum-modal__input" placeholder={t('forum.modalTitlePlaceholder')}
              value={title} onChange={e => setTitle(e.target.value)} maxLength={120} required autoFocus />
            <span className="forum-modal__char">{title.length}/120</span>
          </div>
          <div className="forum-modal__field">
            <label className="forum-modal__label">{t('forum.modalBodyLabel')}</label>
            <textarea className="forum-modal__textarea" placeholder={t('forum.modalBodyPlaceholder')}
              value={body} onChange={e => setBody(e.target.value)} rows={5} required />
          </div>
          <div className="forum-modal__field">
            <label className="forum-modal__label">
              {t('forum.modalTagsLabel')} <span className="forum-modal__optional">{t('forum.modalTagsOptional')}</span>
            </label>
            <input className="forum-modal__input" placeholder={t('forum.modalTagsPlaceholder')}
              value={tags} onChange={e => setTags(e.target.value)} />
          </div>
          <div className="forum-modal__footer">
            <button type="button" className="forum-btn forum-btn--ghost" onClick={onClose}>{t('forum.cancel')}</button>
            <button type="submit" className="forum-btn forum-btn--primary"
              disabled={isSubmitting || !title.trim() || !body.trim()}>
              {isSubmitting ? <><FaSpinner className="forum-spin" /> {t('forum.posting')}</> : <><FaPaperPlane /> {t('forum.post')}</>}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// ── Reply Box ─────────────────────────────────────────────────────
function ReplyBox({ onSubmit, isSubmitting, onCancel }) {
  const { t } = useLanguage()
  const [text, setText] = useState('')
  const handleSubmit = (e) => {
    e.preventDefault()
    if (!text.trim()) return
    onSubmit(text.trim())
    setText('')
  }
  return (
    <form className="forum-reply-box" onSubmit={handleSubmit}>
      <textarea className="forum-reply-box__input" placeholder={t('forum.replyPlaceholder')}
        value={text} onChange={e => setText(e.target.value)} rows={3} autoFocus />
      <div className="forum-reply-box__actions">
        <button type="button" className="forum-btn forum-btn--ghost forum-btn--sm" onClick={onCancel}>{t('forum.cancel')}</button>
        <button type="submit" className="forum-btn forum-btn--primary forum-btn--sm"
          disabled={isSubmitting || !text.trim()}>
          {isSubmitting ? <FaSpinner className="forum-spin" /> : <FaPaperPlane />}
          {isSubmitting ? t('forum.posting') : t('forum.replyBtn')}
        </button>
      </div>
    </form>
  )
}

// ── Post Card ─────────────────────────────────────────────────────
function PostCard({ post, currentUserId, myName, myColor, myProgramInfo, onLike, onDelete, onReplyAdded }) {
  const { t } = useLanguage()
  const CATEGORIES = getCategories(t)

  const [expanded, setExpanded]           = useState(false)
  const [replies, setReplies]             = useState([])
  const [repliesLoaded, setRepliesLoaded] = useState(false)
  const [loadingReplies, setLoadingReplies] = useState(false)
  const [showReplyBox, setShowReplyBox]   = useState(false)
  const [isReplying, setIsReplying]       = useState(false)
  const [likeCount, setLikeCount]         = useState(post.like_count ?? 0)
  const [liked, setLiked]                 = useState(post.liked ?? false)

  const cat   = CATEGORIES.find(c => c.key === post.category) || CATEGORIES[1]
  const isOwn = post.user_id === currentUserId

  const handleToggleExpand = async () => {
    const next = !expanded
    setExpanded(next)
    if (next && !repliesLoaded) {
      setLoadingReplies(true)
      try {
        const data = await forumAPI.getReplies(post.id)
        setReplies(data.replies || [])
        setRepliesLoaded(true)
      } catch { /* fail silently */ }
      finally { setLoadingReplies(false) }
    }
  }

  const handleLike = async () => {
    const wasLiked = liked
    setLiked(!wasLiked)
    setLikeCount(c => wasLiked ? c - 1 : c + 1)
    try {
      const res = await onLike(post.id)
      setLiked(res.liked)
      setLikeCount(res.like_count)
    } catch {
      setLiked(wasLiked)
      setLikeCount(c => wasLiked ? c + 1 : c - 1)
    }
  }

  const handleReplyLike = async (replyId) => {
    setReplies(prev => prev.map(r =>
      r.id === replyId
        ? { ...r, liked: !r.liked, like_count: r.liked ? r.like_count - 1 : r.like_count + 1 }
        : r
    ))
    try {
      const res = await forumAPI.toggleReplyLike(replyId)
      setReplies(prev => prev.map(r =>
        r.id === replyId ? { ...r, liked: res.liked, like_count: res.like_count } : r
      ))
    } catch {
      setReplies(prev => prev.map(r =>
        r.id === replyId
          ? { ...r, liked: !r.liked, like_count: r.liked ? r.like_count - 1 : r.like_count + 1 }
          : r
      ))
    }
  }

  const handleAddReply = async (text) => {
    setIsReplying(true)
    try {
      const res = await forumAPI.createReply(post.id, { author: myName, avatar_color: myColor, body: text, program_info: myProgramInfo || null })
      setReplies(prev => [...prev, { ...res.reply, liked: false }])
      setRepliesLoaded(true)
      setExpanded(true)
      setShowReplyBox(false)
      if (onReplyAdded) onReplyAdded(post.id)
    } catch (err) { console.error('Reply failed:', err) }
    finally { setIsReplying(false) }
  }

  const handleDeleteReply = async (replyId) => {
    try {
      await forumAPI.deleteReply(replyId)
      setReplies(prev => prev.filter(r => r.id !== replyId))
    } catch (err) { console.error('Delete reply failed:', err) }
  }

  const handleReportPost = async () => {
    if (!window.confirm(t('forum.confirmReportPost'))) return
    try {
      await forumAPI.reportPost(post.id)
      alert(t('forum.reportSuccess'))
    } catch { alert(t('forum.reportError')) }
  }

  const handleReportReply = async (replyId) => {
    if (!window.confirm(t('forum.confirmReportReply'))) return
    try {
      await forumAPI.reportReply(replyId)
      alert(t('forum.reportSuccess'))
    } catch { alert(t('forum.reportError')) }
  }

  const replyCount = repliesLoaded ? replies.length : (post.reply_count ?? 0)

  return (
    <article className="forum-post-card">
      {/* Header */}
      <div className="forum-post-card__header">
        <Avatar letter={post.author} color={post.avatar_color} size={36} />
        <div className="forum-post-card__meta">
          <span className="forum-post-card__author">{post.author}</span>
          {post.program_info && <span className="forum-post-card__program">{post.program_info}</span>}
          <span className="forum-post-card__dot">·</span>
          <span className="forum-post-card__time">{timeAgo(post.created_at, t)}</span>
        </div>
        <div className="forum-post-card__cat-badge" style={{ '--cat-color': cat.color }}>
          {cat.icon} {cat.label}
        </div>
        {isOwn ? (
          <button className="forum-action-btn forum-action-btn--sm forum-action-btn--danger"
            onClick={() => onDelete(post.id)} title={t('forum.deletePost')}>
            <FaTrash />
          </button>
        ) : (
          <button className="forum-action-btn forum-action-btn--sm forum-action-btn--report"
            onClick={handleReportPost} title={t('forum.reportPost')}>
            <FaFlag />
          </button>
        )}
      </div>

      {/* Body */}
      <div className="forum-post-card__body">
        <h3 className="forum-post-card__title">{post.title}</h3>
        <p className="forum-post-card__text">{post.body}</p>
        {post.tags?.length > 0 && (
          <div className="forum-post-card__tags">
            {post.tags.map(tag => (
              <span key={tag} className="forum-post-card__tag"><FaTag size={9} /> {tag}</span>
            ))}
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="forum-post-card__actions">
        <button className={`forum-action-btn ${liked ? 'forum-action-btn--liked' : ''}`} onClick={handleLike}>
          <FaThumbsUp /> {likeCount}
        </button>
        <button className={`forum-action-btn ${expanded ? 'forum-action-btn--active' : ''}`} onClick={handleToggleExpand}>
          <FaComments /> {replyCount} {replyCount === 1 ? t('forum.replySingular') : t('forum.replyPlural')}
          {replyCount > 0 && (expanded ? <FaChevronUp size={10} /> : <FaChevronDown size={10} />)}
        </button>
        <button className="forum-action-btn" onClick={() => setShowReplyBox(v => !v)}>
          <FaReply /> {t('forum.replyBtn')}
        </button>
      </div>

      {/* Replies */}
      {expanded && (
        <div className="forum-replies">
          {loadingReplies && (
            <div className="forum-replies__loading"><FaSpinner className="forum-spin" /> {t('forum.loadingReplies')}</div>
          )}
          {replies.map(reply => (
            <div key={reply.id} className="forum-reply">
              <Avatar letter={reply.author} color={reply.avatar_color} size={28} />
              <div className="forum-reply__content">
                <div className="forum-reply__meta">
                  <span className="forum-reply__author">{reply.author}</span>
                  {reply.program_info && <span className="forum-post-card__program">{reply.program_info}</span>}
                  <span className="forum-reply__time">{timeAgo(reply.created_at, t)}</span>
                </div>
                <p className="forum-reply__text">{reply.body}</p>
                <div className="forum-reply__actions">
                  <button
                    className={`forum-action-btn forum-action-btn--sm ${reply.liked ? 'forum-action-btn--liked' : ''}`}
                    onClick={() => handleReplyLike(reply.id)}>
                    <FaThumbsUp /> {reply.like_count ?? 0}
                  </button>
                  {reply.user_id === currentUserId ? (
                    <button className="forum-action-btn forum-action-btn--sm forum-action-btn--danger"
                      onClick={() => handleDeleteReply(reply.id)} title={t('forum.deleteReply')}>
                      <FaTrash />
                    </button>
                  ) : (
                    <button className="forum-action-btn forum-action-btn--sm forum-action-btn--report"
                      onClick={() => handleReportReply(reply.id)} title={t('forum.reportReply')}>
                      <FaFlag />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Reply box */}
      {showReplyBox && (
        <div className="forum-post-card__reply-area">
          <ReplyBox onSubmit={handleAddReply} isSubmitting={isReplying} onCancel={() => setShowReplyBox(false)} />
        </div>
      )}
    </article>
  )
}

// ── Main ──────────────────────────────────────────────────────────
export default function Forum() {
  const { user, profile } = useAuth()
  const { t } = useLanguage()

  const CATEGORIES   = getCategories(t)
  const SORT_OPTIONS = getSortOptions(t)

  const [posts, setPosts]             = useState([])
  const [loading, setLoading]         = useState(true)
  const [error, setError]             = useState(null)
  const [activeCategory, setActiveCategory] = useState('all')
  const [sortMode, setSortMode]       = useState('hot')
  const [search, setSearch]           = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [showNewPost, setShowNewPost] = useState(false)
  const [isPosting, setIsPosting]     = useState(false)
  const debounceRef = useRef(null)

  const myName   = profile?.username || user?.email?.split('@')[0] || 'student'
  const myColor  = '#ed1b2f'
  const myUserId = user?.id

  // Privacy settings (read from localStorage, same keys Settings.jsx writes)
  const isPublic     = (localStorage.getItem('profileVisibility') || 'private') === 'public'
  const shareProgram = JSON.parse(localStorage.getItem('shareProgress') ?? 'false')
  const myAuthor     = isPublic ? myName : 'Anonymous'
  const myProgramInfo = shareProgram && profile
    ? (() => {
        const majors = [profile.major, ...(profile.other_majors || [])].filter(Boolean)
        const minors = [profile.minor, ...(profile.other_minors || [])].filter(Boolean)
        const parts = [
          profile.year ? `U${profile.year}` : null,
          profile.faculty || null,
          ...majors,
          ...minors.map(m => `${m} (minor)`),
        ].filter(Boolean)
        return parts.length ? parts.join(' · ') : null
      })()
    : null

  // Debounce search input
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => setDebouncedSearch(search), 350)
    return () => clearTimeout(debounceRef.current)
  }, [search])

  // Fetch posts whenever filters change
  const fetchPosts = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await forumAPI.getPosts({
        category: activeCategory !== 'all' ? activeCategory : undefined,
        sort: sortMode,
        search: debouncedSearch || undefined,
        limit: 50,
      })
      setPosts(data.posts || [])
    } catch (err) {
      console.error('Forum fetch error:', err)
      setError(t('forum.loadError'))
    } finally {
      setLoading(false)
    }
  }, [activeCategory, sortMode, debouncedSearch, t])

  useEffect(() => { fetchPosts() }, [fetchPosts])

  const handleLike = useCallback((postId) => forumAPI.togglePostLike(postId), [])

  const handleDelete = useCallback(async (postId) => {
    if (!window.confirm(t('forum.confirmDeletePost'))) return
    try {
      await forumAPI.deletePost(postId)
      setPosts(prev => prev.filter(p => p.id !== postId))
    } catch (err) { console.error('Delete failed:', err) }
  }, [t])

  const handleReplyAdded = useCallback((postId) => {
    setPosts(prev => prev.map(p =>
      p.id === postId ? { ...p, reply_count: (p.reply_count ?? 0) + 1 } : p
    ))
  }, [])

  const handleCreatePost = async ({ title, body, category, tags }) => {
    setIsPosting(true)
    try {
      const data = await forumAPI.createPost({ author: myAuthor, avatar_color: myColor, category, title, body, tags, program_info: myProgramInfo || null })
      setPosts(prev => [{ ...data.post, reply_count: 0, liked: false }, ...prev])
      setShowNewPost(false)
    } catch (err) { console.error('Create post failed:', err) }
    finally { setIsPosting(false) }
  }

  const catCounts = CATEGORIES.reduce((acc, cat) => {
    acc[cat.key] = cat.key === 'all' ? posts.length : posts.filter(p => p.category === cat.key).length
    return acc
  }, {})

  return (
    <div className="forum-root">
      {/* Header */}
      <div className="forum-header">
        <div className="forum-header__left">
          <div className="forum-header__icon"><FaComments size={22} /></div>
          <div>
            <h1 className="forum-header__title">{t('forum.header')}</h1>
            <p className="forum-header__sub">{t('forum.subheader')}</p>
          </div>
        </div>
        <button className="forum-new-btn" onClick={() => setShowNewPost(true)}>
          <FaPlus size={12} /> {t('forum.newPostBtn')}
        </button>
      </div>

      {/* Toolbar */}
      <div className="forum-toolbar">
        <div className="forum-search-wrap">
          <FaSearch className="forum-search-ico" />
          <input className="forum-search" placeholder={t('forum.searchPlaceholder')}
            value={search} onChange={e => setSearch(e.target.value)} />
          {search && <button className="forum-search-clear" onClick={() => setSearch('')}><FaTimes size={11} /></button>}
        </div>
        <div className="forum-sort">
          {SORT_OPTIONS.map(s => (
            <button key={s.key} className={`forum-sort-btn ${sortMode === s.key ? 'active' : ''}`}
              onClick={() => setSortMode(s.key)}>
              {s.icon} {s.label}
            </button>
          ))}
        </div>
      </div>

      {/* Category chips */}
      <div className="forum-cats">
        {CATEGORIES.map(cat => (
          <button key={cat.key}
            className={`forum-cat-btn ${activeCategory === cat.key ? 'active' : ''}`}
            style={{ '--cat-color': cat.color }}
            onClick={() => setActiveCategory(cat.key)}>
            <span className="forum-cat-btn__icon">{cat.icon}</span>
            {cat.label}
            <span className="forum-cat-btn__count">{catCounts[cat.key] ?? 0}</span>
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div className="forum-loading-bar"><FaSpinner className="forum-spin" /> {t('forum.loadingPosts')}</div>
      ) : error ? (
        <div className="forum-error-bar">
          {error}
          <button className="forum-btn forum-btn--ghost forum-btn--sm" onClick={fetchPosts}>{t('forum.retry')}</button>
        </div>
      ) : posts.length === 0 ? (
        <div className="forum-empty">
          <FaComments size={32} />
          <p>{debouncedSearch || activeCategory !== 'all' ? t('forum.noPostsFiltered') : t('forum.noPostsYet')}</p>
          <button className="forum-btn forum-btn--primary" onClick={() => setShowNewPost(true)}>
            <FaPlus /> {t('forum.createPostBtn')}
          </button>
        </div>
      ) : (
        <div className="forum-posts">
          {posts.map(post => (
            <PostCard key={post.id} post={post}
              currentUserId={myUserId} myName={myAuthor} myColor={myColor}
              myProgramInfo={myProgramInfo}
              onLike={handleLike} onDelete={handleDelete} onReplyAdded={handleReplyAdded} />
          ))}
        </div>
      )}

      {showNewPost && (
        <NewPostModal onClose={() => setShowNewPost(false)} onSubmit={handleCreatePost} isSubmitting={isPosting} />
      )}
    </div>
  )
}
