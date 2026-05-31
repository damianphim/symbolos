import { useState, useEffect, useRef, useCallback } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/PreferencesContext'
import forumAPI from '../../lib/forumAPI'
import {
  FaComments, FaThumbsUp, FaReply, FaSearch, FaFire,
  FaClock, FaStar, FaRegStar, FaPlus, FaTimes, FaChevronDown,
  FaChevronUp, FaBookOpen, FaUsers, FaChalkboardTeacher,
  FaBullhorn, FaCog, FaPaperPlane, FaSpinner,
  FaTag, FaTrash, FaFlag,
} from 'react-icons/fa'
import './Forum.css'

// ─────────────────────────────────────────────────────────────────────
// Top-level sections in the forum (post-2026-04 redesign).
//   - reviews       → groups course_review + professor_review (sub-tabs)
//   - clubs         → discussions about clubs
//   - general       → general non-academic discussion
//   - app_feedback  → feedback about Symbolos itself
// ─────────────────────────────────────────────────────────────────────
const SECTIONS = [
  { key: 'reviews',      label: 'Reviews',     icon: <FaStar />,              color: '#f59e0b' },
  { key: 'clubs',        label: 'Clubs',       icon: <FaUsers />,             color: '#10b981' },
  { key: 'general',      label: 'General',     icon: <FaBullhorn />,          color: '#8b5cf6' },
  { key: 'app_feedback', label: 'App Feedback', icon: <FaCog />,              color: '#3b82f6' },
]

const REVIEW_SUBTABS = [
  { key: 'course_review',    label: 'Courses',    icon: <FaBookOpen />,           color: '#3b82f6' },
  { key: 'professor_review', label: 'Professors', icon: <FaChalkboardTeacher />, color: '#ed1b2f' },
]

function getSortOptions(t) {
  return [
    { key: 'hot', label: t('forum.sortHot'), icon: <FaFire /> },
    { key: 'new', label: t('forum.sortNew'), icon: <FaClock /> },
    { key: 'top', label: t('forum.sortTop'), icon: <FaStar /> },
  ]
}

// Map an API post category → the section key it belongs to.
function categoryToSection(cat) {
  if (cat === 'course_review' || cat === 'professor_review') return 'reviews'
  if (cat === 'clubs') return 'clubs'
  if (cat === 'app_feedback') return 'app_feedback'
  return 'general'  // includes legacy: general/courses/study/advice/planning
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

// ── Star rating widget ───────────────────────────────────────────
function StarPicker({ value, onChange, size = 22 }) {
  return (
    <div className="forum-stars forum-stars--picker" role="radiogroup">
      {[1, 2, 3, 4, 5].map(n => (
        <button
          key={n}
          type="button"
          className={`forum-star ${n <= value ? 'forum-star--on' : ''}`}
          onClick={() => onChange(n)}
          aria-label={`${n} star${n === 1 ? '' : 's'}`}
        >
          {n <= value ? <FaStar size={size} /> : <FaRegStar size={size} />}
        </button>
      ))}
    </div>
  )
}

function StarDisplay({ rating, size = 14 }) {
  if (rating == null) return null
  return (
    <span className="forum-stars">
      {[1, 2, 3, 4, 5].map(n => (
        n <= rating
          ? <FaStar key={n} size={size} className="forum-star forum-star--on" />
          : <FaRegStar key={n} size={size} className="forum-star" />
      ))}
    </span>
  )
}

// ── New Post Modal ───────────────────────────────────────────────
function NewPostModal({ onClose, onSubmit, isSubmitting, initialSection, initialReviewSubtab }) {
  const { t } = useLanguage()
  const [section, setSection] = useState(initialSection || 'general')
  const [reviewKind, setReviewKind] = useState(initialReviewSubtab || 'course_review')

  // Review-specific state
  const [target, setTarget] = useState('')         // course code or professor name
  const [rating, setRating] = useState(0)
  const [instructors, setInstructors] = useState({ courses: [], professors: [] })
  const [instructorsLoaded, setInstructorsLoaded] = useState(false)

  // Common
  const [title, setTitle] = useState('')
  const [body,  setBody]  = useState('')
  const [tags,  setTags]  = useState('')
  // For free-typed professor (not in dropdown)
  const [customProf, setCustomProf] = useState('')

  const isReview = section === 'reviews'
  const reviewCategory = reviewKind  // 'course_review' | 'professor_review'

  // Fetch user's instructors when entering reviews tab
  useEffect(() => {
    if (!isReview || instructorsLoaded) return
    forumAPI.getMyInstructors()
      .then(data => { setInstructors(data); setInstructorsLoaded(true) })
      .catch(() => setInstructorsLoaded(true))
  }, [isReview, instructorsLoaded])

  const effectiveTarget = reviewCategory === 'professor_review'
    ? (target === '__custom__' ? customProf.trim() : target)
    : target

  const canSubmit = (() => {
    if (!title.trim() || !body.trim() || isSubmitting) return false
    if (isReview) {
      if (!rating) return false
      if (!effectiveTarget) return false
    }
    return true
  })()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!canSubmit) return

    const category = isReview ? reviewCategory : section
    const payload = {
      title: title.trim(),
      body: body.trim(),
      category,
      tags: tags.split(',').map(s => s.trim()).filter(Boolean),
    }
    if (isReview) {
      payload.rating = rating
      payload.review_target_type = reviewCategory === 'course_review' ? 'course' : 'professor'
      payload.review_target_value = effectiveTarget
    }
    onSubmit(payload)
  }

  // Auto-fill title when reviewing a known target
  useEffect(() => {
    if (!isReview) return
    if (effectiveTarget && !title.trim()) {
      if (reviewCategory === 'course_review') {
        const c = instructors.courses?.find(x => x.course_code === effectiveTarget)
        setTitle(c?.course_title ? `${effectiveTarget} — ${c.course_title}` : `${effectiveTarget} review`)
      } else {
        setTitle(`${effectiveTarget} review`)
      }
    }
  }, [effectiveTarget, isReview, reviewCategory])  // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="forum-modal-overlay" onClick={onClose}>
      <div className="forum-modal" onClick={e => e.stopPropagation()}>
        <div className="forum-modal__header">
          <h2 className="forum-modal__title">New post</h2>
          <button className="forum-modal__close" onClick={onClose}><FaTimes /></button>
        </div>
        <form className="forum-modal__body" onSubmit={handleSubmit}>

          {/* Section picker */}
          <div className="forum-modal__field">
            <label className="forum-modal__label">Section</label>
            <div className="forum-modal__cat-grid">
              {SECTIONS.map(s => (
                <button key={s.key} type="button"
                  className={`forum-modal__cat-btn ${section === s.key ? 'active' : ''}`}
                  style={{ '--cat-color': s.color }}
                  onClick={() => setSection(s.key)}>
                  {s.icon} {s.label}
                </button>
              ))}
            </div>
          </div>

          {/* Reviews: sub-tab + target picker + rating */}
          {isReview && (
            <>
              <div className="forum-modal__field">
                <label className="forum-modal__label">Review type</label>
                <div className="forum-modal__cat-grid forum-modal__cat-grid--2">
                  {REVIEW_SUBTABS.map(s => (
                    <button key={s.key} type="button"
                      className={`forum-modal__cat-btn ${reviewKind === s.key ? 'active' : ''}`}
                      style={{ '--cat-color': s.color }}
                      onClick={() => { setReviewKind(s.key); setTarget('') }}>
                      {s.icon} {s.label}
                    </button>
                  ))}
                </div>
              </div>

              {reviewCategory === 'course_review' ? (
                <div className="forum-modal__field">
                  <label className="forum-modal__label">Pick a course from your transcript</label>
                  <select className="forum-modal__input"
                    value={target} onChange={e => setTarget(e.target.value)}>
                    <option value="">— choose a course —</option>
                    {(instructors.courses || []).map(c => (
                      <option key={c.course_code} value={c.course_code}>
                        {c.course_code}{c.course_title ? ` — ${c.course_title}` : ''}
                      </option>
                    ))}
                  </select>
                  {!instructorsLoaded && <span className="forum-modal__hint">Loading your courses…</span>}
                  {instructorsLoaded && (instructors.courses || []).length === 0 && (
                    <span className="forum-modal__hint">No courses yet — import your transcript to enable course reviews.</span>
                  )}
                </div>
              ) : (
                <div className="forum-modal__field">
                  <label className="forum-modal__label">Pick a professor you've had</label>
                  <select className="forum-modal__input"
                    value={target} onChange={e => setTarget(e.target.value)}>
                    <option value="">— choose a professor —</option>
                    {(instructors.professors || []).map(p => (
                      <option key={p.name} value={p.name}>
                        {p.name}{p.courses?.length ? ` (${p.courses.map(c => c.course_code).join(', ')})` : ''}
                      </option>
                    ))}
                    <option value="__custom__">+ Type a different name…</option>
                  </select>
                  {target === '__custom__' && (
                    <input className="forum-modal__input" style={{ marginTop: 8 }}
                      placeholder="Professor name (e.g. Joseph Vybihal)"
                      value={customProf} onChange={e => setCustomProf(e.target.value)}
                      maxLength={120} />
                  )}
                  {!instructorsLoaded && <span className="forum-modal__hint">Loading your professors…</span>}
                  {instructorsLoaded && (instructors.professors || []).length === 0 && target !== '__custom__' && (
                    <span className="forum-modal__hint">
                      No professors saved yet — pick "Type a different name" above, or add professor names to your completed courses in Degree Planning.
                    </span>
                  )}
                </div>
              )}

              <div className="forum-modal__field">
                <label className="forum-modal__label">Rating <span style={{ color: '#ef4444' }}>*</span></label>
                <StarPicker value={rating} onChange={setRating} />
              </div>
            </>
          )}

          {/* Title */}
          <div className="forum-modal__field">
            <label className="forum-modal__label">{isReview ? 'Headline' : 'Title'}</label>
            <input className="forum-modal__input"
              placeholder={isReview ? 'Quick summary of your review' : 'What\'s on your mind?'}
              value={title} onChange={e => setTitle(e.target.value)} maxLength={120} required />
            <span className="forum-modal__char">{title.length}/120</span>
          </div>

          {/* Body */}
          <div className="forum-modal__field">
            <label className="forum-modal__label">{isReview ? 'Your review' : 'Details'}</label>
            <textarea className="forum-modal__textarea"
              placeholder={isReview
                ? 'What did you like? What was hard? Was the workload manageable? Was the prof helpful?'
                : 'Share details, ask questions, or start a discussion…'}
              value={body} onChange={e => setBody(e.target.value)} rows={5} required />
          </div>

          {/* Tags */}
          <div className="forum-modal__field">
            <label className="forum-modal__label">
              Tags <span className="forum-modal__optional">(optional, comma-separated)</span>
            </label>
            <input className="forum-modal__input"
              placeholder="easy, exam-heavy, fair-grading…"
              value={tags} onChange={e => setTags(e.target.value)} />
          </div>

          <div className="forum-modal__footer">
            <button type="button" className="forum-btn forum-btn--ghost" onClick={onClose}>{t('forum.cancel')}</button>
            <button type="submit" className="forum-btn forum-btn--primary" disabled={!canSubmit}>
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

  const [expanded, setExpanded]           = useState(false)
  const [replies, setReplies]             = useState([])
  const [repliesLoaded, setRepliesLoaded] = useState(false)
  const [loadingReplies, setLoadingReplies] = useState(false)
  const [showReplyBox, setShowReplyBox]   = useState(false)
  const [isReplying, setIsReplying]       = useState(false)
  const [likeCount, setLikeCount]         = useState(post.like_count ?? 0)
  const [liked, setLiked]                 = useState(post.liked ?? false)

  const isOwn = post.user_id === currentUserId
  const isReview = post.category === 'course_review' || post.category === 'professor_review'

  // Build a section badge for the post
  const section = SECTIONS.find(s => s.key === categoryToSection(post.category)) || SECTIONS[2]
  const reviewSub = isReview ? REVIEW_SUBTABS.find(r => r.key === post.category) : null
  const badge = reviewSub || section

  const handleToggleExpand = async () => {
    const next = !expanded
    setExpanded(next)
    if (next && !repliesLoaded) {
      setLoadingReplies(true)
      try {
        const data = await forumAPI.getReplies(post.id)
        setReplies(data.replies || [])
        setRepliesLoaded(true)
      } catch { /* silent */ }
      finally { setLoadingReplies(false) }
    }
  }

  const handleLike = async () => {
    const wasLiked = liked
    setLiked(!wasLiked)
    setLikeCount(c => wasLiked ? c - 1 : c + 1)
    try {
      const res = await onLike(post.id)
      setLiked(res.liked); setLikeCount(res.like_count)
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
      setReplies(prev => prev.map(r => r.id === replyId ? { ...r, liked: res.liked, like_count: res.like_count } : r))
    } catch {
      setReplies(prev => prev.map(r =>
        r.id === replyId ? { ...r, liked: !r.liked, like_count: r.liked ? r.like_count - 1 : r.like_count + 1 } : r
      ))
    }
  }

  const handleAddReply = async (text) => {
    setIsReplying(true)
    try {
      const res = await forumAPI.createReply(post.id, { author: myName, avatar_color: myColor, body: text, program_info: myProgramInfo || null })
      setReplies(prev => [...prev, { ...res.reply, liked: false }])
      setRepliesLoaded(true); setExpanded(true); setShowReplyBox(false)
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
    try { await forumAPI.reportPost(post.id); alert(t('forum.reportSuccess')) }
    catch { alert(t('forum.reportError')) }
  }

  const handleReportReply = async (replyId) => {
    if (!window.confirm(t('forum.confirmReportReply'))) return
    try { await forumAPI.reportReply(replyId); alert(t('forum.reportSuccess')) }
    catch { alert(t('forum.reportError')) }
  }

  const replyCount = repliesLoaded ? replies.length : (post.reply_count ?? 0)

  return (
    <article className={`forum-post-card ${isReview ? 'forum-post-card--review' : ''}`}>
      <div className="forum-post-card__header">
        <Avatar letter={post.author} color={post.avatar_color} size={36} />
        <div className="forum-post-card__meta">
          <span className="forum-post-card__author">{post.author}</span>
          {post.program_info && <span className="forum-post-card__program">{post.program_info}</span>}
          <span className="forum-post-card__dot">·</span>
          <span className="forum-post-card__time">{timeAgo(post.created_at, t)}</span>
        </div>
        <div className="forum-post-card__cat-badge" style={{ '--cat-color': badge.color }}>
          {badge.icon} {badge.label}
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

      {/* Review header strip */}
      {isReview && (
        <div className="forum-review-strip">
          <span className="forum-review-strip__target">
            {post.category === 'course_review' ? <FaBookOpen /> : <FaChalkboardTeacher />}
            {post.review_target_value}
          </span>
          <StarDisplay rating={post.rating} size={14} />
        </div>
      )}

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

  const SORT_OPTIONS = getSortOptions(t)

  const [posts, setPosts]             = useState([])
  const [loading, setLoading]         = useState(true)
  const [error, setError]             = useState(null)
  // Top-level section: reviews | clubs | general | app_feedback
  const [activeSection, setActiveSection] = useState('reviews')
  // Within Reviews: course_review | professor_review
  const [reviewSubtab, setReviewSubtab] = useState('course_review')
  const [sortMode, setSortMode]       = useState('hot')
  const [search, setSearch]           = useState('')
  const [debouncedSearch, setDebouncedSearch] = useState('')
  const [showNewPost, setShowNewPost] = useState(false)
  const [isPosting, setIsPosting]     = useState(false)
  const debounceRef = useRef(null)

  const myName   = profile?.username || user?.email?.split('@')[0] || 'student'
  const myColor  = '#ed1b2f'
  const myUserId = user?.id

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

  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => setDebouncedSearch(search), 350)
    return () => clearTimeout(debounceRef.current)
  }, [search])

  // Which API category to request for the active section
  const apiCategory = activeSection === 'reviews' ? reviewSubtab : activeSection

  const fetchPosts = useCallback(async () => {
    setLoading(true); setError(null)
    try {
      const data = await forumAPI.getPosts({
        category: apiCategory,
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
  }, [apiCategory, sortMode, debouncedSearch, t])

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

  const handleCreatePost = async (postData) => {
    setIsPosting(true)
    try {
      const data = await forumAPI.createPost({
        ...postData,
        author: myAuthor,
        avatar_color: myColor,
        program_info: myProgramInfo || null,
      })
      // If the new post matches the current view, prepend it
      const matchesView = data.post.category === apiCategory
      if (matchesView) {
        setPosts(prev => [{ ...data.post, reply_count: 0, liked: false }, ...prev])
      }
      setShowNewPost(false)
    } catch (err) {
      console.error('Create post failed:', err)
      alert(err.message || 'Failed to create post')
    }
    finally { setIsPosting(false) }
  }

  const sectionMeta = SECTIONS.find(s => s.key === activeSection) || SECTIONS[0]

  return (
    <div className="forum-root">
      {/* Header */}
      <div className="forum-header">
        <div className="forum-header__left">
          <div className="forum-header__icon"><FaComments size={22} /></div>
          <div>
            <h1 className="forum-header__title">Community</h1>
            <p className="forum-header__sub">Reviews · Clubs · Discussion · Feedback</p>
          </div>
        </div>
        <button className="forum-new-btn" onClick={() => setShowNewPost(true)}>
          <FaPlus size={12} /> {t('forum.newPostBtn')}
        </button>
      </div>

      {/* Section tabs */}
      <div className="forum-section-bar">
        {SECTIONS.map(s => (
          <button key={s.key}
            className={`forum-section-btn ${activeSection === s.key ? 'active' : ''}`}
            style={{ '--cat-color': s.color }}
            onClick={() => setActiveSection(s.key)}>
            {s.icon} <span>{s.label}</span>
          </button>
        ))}
      </div>

      {/* Reviews sub-tabs */}
      {activeSection === 'reviews' && (
        <>
          <div className="forum-subtab-bar">
            {REVIEW_SUBTABS.map(s => (
              <button key={s.key}
                className={`forum-subtab-btn ${reviewSubtab === s.key ? 'active' : ''}`}
                style={{ '--cat-color': s.color }}
                onClick={() => setReviewSubtab(s.key)}>
                {s.icon} <span>{s.label}</span>
              </button>
            ))}
          </div>

          {/* Link-out banner: send users to mcgill.courses for broader review coverage */}
          <a
            className="forum-linkout-banner"
            href="https://mcgill.courses"
            target="_blank"
            rel="noopener noreferrer"
          >
            <FaBookOpen className="forum-linkout-banner__icon" />
            <span className="forum-linkout-banner__text">
              <strong>Want more reviews?</strong> Browse student-written course & professor reviews on <u>mcgill.courses</u> ↗
            </span>
          </a>
        </>
      )}

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
          {sectionMeta.icon}
          <p>
            {debouncedSearch
              ? t('forum.noPostsFiltered')
              : activeSection === 'reviews'
                ? `No ${reviewSubtab === 'course_review' ? 'course' : 'professor'} reviews yet — be the first!`
                : activeSection === 'clubs'
                  ? 'No club discussions yet.'
                  : activeSection === 'app_feedback'
                    ? 'No app feedback yet — share what could be better.'
                    : t('forum.noPostsYet')}
          </p>
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
        <NewPostModal
          onClose={() => setShowNewPost(false)}
          onSubmit={handleCreatePost}
          isSubmitting={isPosting}
          initialSection={activeSection}
          initialReviewSubtab={reviewSubtab}
        />
      )}
    </div>
  )
}
