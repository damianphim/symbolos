import { useState, useEffect, useCallback, useRef } from 'react'
import { useLanguage } from '../../../contexts/LanguageContext'
import {
  FaSync, FaChevronDown, FaChevronUp,
  FaBolt, FaArrowRight, FaGraduationCap,
  FaClipboardList, FaComments, FaCalendarAlt,
  FaChartBar, FaMapMarkedAlt, FaLightbulb,
  FaBookmark, FaRegBookmark, FaThumbtack,
  FaGripVertical, FaTrash, FaMapPin,
} from 'react-icons/fa'
import { CARD_CATEGORIES, CATEGORY_LABELS } from '../../../lib/cardsAPI'
import './AdvisorCards.css'

const CATEGORY_ICON_COMPONENTS = {
  deadlines:     FaCalendarAlt,
  degree:        FaGraduationCap,
  courses:       FaClipboardList,
  grades:        FaChartBar,
  planning:      FaMapMarkedAlt,
  opportunities: FaLightbulb,
  other:         FaComments,
}

const CARD_CONFIG = {
  urgent:   { accent: 'var(--card-urgent,   #ED1B2F)' },
  warning:  { accent: 'var(--card-warning,  #F59E0B)' },
  insight:  { accent: 'var(--card-insight,  #3B82F6)' },
  progress: { accent: 'var(--card-progress, #10B981)' },
}

// ── Thread messages scroller ──────────────────────────────────
function ThreadMessages({ thread, isThinking }) {
  const scrollRef = useRef(null)
  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [thread.length, isThinking])

  return (
    <div className="thread-messages" ref={scrollRef}>
      {thread.map((msg, i) => (
        <div
          key={i}
          className={`thread-message thread-message--${msg.role}`}
          // Preserve the language the user typed in, even if the UI language switches.
          // For assistant messages, lang is not stored (the AI responds in whatever
          // language was active at the time, which is already correct as rendered).
          lang={msg.role === 'user' && msg.lang ? msg.lang : undefined}
        >
          <p className="thread-text">{msg.content}</p>
        </div>
      ))}
      {isThinking && (
        <div className="thread-message thread-message--assistant">
          <p className="thread-text">
            <span className="thinking-dots"><span /><span /><span /></span>
          </p>
        </div>
      )}
    </div>
  )
}

// ── Auto-growing textarea chat bar ────────────────────────────
function CardChatBar({ onSend, isThinking, onFocus }) {
  const { t } = useLanguage()
  const [value, setValue] = useState('')
  const taRef = useRef(null)

  const adjustHeight = () => {
    const ta = taRef.current
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = Math.min(ta.scrollHeight, 120) + 'px'
  }

  const handleChange = (e) => {
    setValue(e.target.value)
    adjustHeight()
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      submit()
    }
  }

  const submit = () => {
    if (!value.trim() || isThinking) return
    onSend(value.trim())
    setValue('')
    if (taRef.current) taRef.current.style.height = 'auto'
  }

  return (
    <div className="card-chat-bar">
      <textarea
        ref={taRef}
        className="card-chat-bar__input"
        {...{ placeholder: t('brief.followUpPlaceholder') }}
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        onFocus={onFocus}
        disabled={isThinking}
        rows={1}
      />
      <button
        className="card-chat-bar__send"
        onClick={submit}
        disabled={isThinking || !value.trim()}
        type="button"
      >
        {isThinking
          ? <span className="thinking-dots small"><span /><span /><span /></span>
          : <FaArrowRight />}
      </button>
    </div>
  )
}

// Helper: translated category label
function catLabel(cat, t) {
  const map = {
    deadlines:     'brief.catDeadlines',
    degree:        'brief.catDegree',
    courses:       'brief.catCourses',
    grades:        'brief.catGrades',
    planning:      'brief.catPlanning',
    opportunities: 'brief.catOpportunities',
    other:         'brief.catOther',
  }
  return t(map[cat] || 'brief.catOther')
}

// ── Individual card ───────────────────────────────────────────
function AdvisorCard({
  card,
  thread = [],
  isThinking = false,
  isExpanded = false,
  isPinned = false,
  onSaveToggle,
  onPinToggle,
  onSend,
  onExpand,
  onCollapse,
  onDelete,
  dragHandleProps,
  isDragging,
}) {
  const { t } = useLanguage()
  const [saving, setSaving]       = useState(false)
  const [panelOpen, setPanelOpen] = useState(false)
  const cardRef = useRef(null)

  const config   = CARD_CONFIG[card.card_type || card.type] || CARD_CONFIG.insight
  const CardIcon = CATEGORY_ICON_COMPONENTS[card.category || 'other'] || FaComments
  const isSaved  = card.is_saved || false
  const isUser   = card.source === 'user'

  useEffect(() => {
    if (!isExpanded) return
    const handleClickOutside = (e) => {
      if (cardRef.current && !cardRef.current.contains(e.target)) {
        onCollapse(card.id)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isExpanded, card.id, onCollapse])

  const chips = card.actions || []

  // Sync with parent expanded state
  useEffect(() => { if (isExpanded) setPanelOpen(true) }, [isExpanded])

  // Auto-open only when a NEW message arrives (not on initial mount from localStorage)
  const prevThreadLen = useRef(thread.length)
  useEffect(() => {
    if (thread.length > prevThreadLen.current) setPanelOpen(true)
    prevThreadLen.current = thread.length
  }, [thread.length])

  const handleSave = async (e) => {
    e.stopPropagation()
    if (saving) return
    setSaving(true)
    try { await onSaveToggle(card.id, !isSaved) }
    finally { setSaving(false) }
  }

  const handlePin = (e) => {
    e.stopPropagation()
    onPinToggle(card, thread)
  }

  const togglePanel = () => {
    const next = !panelOpen
    setPanelOpen(next)
    if (next) {
      onExpand(card.id)
      setTimeout(() => cardRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 80)
    } else {
      onCollapse(card.id)
    }
  }

  const handleSend = (msg) => {
    if (!panelOpen) {
      setPanelOpen(true)
      onExpand(card.id)
    }
    onSend(msg)
  }

  return (
    <article
      data-card-id={card.id}
      className={[
        'advisor-card',
        `advisor-card--${card.card_type || card.type}`,
        isUser     ? 'advisor-card--user' : '',
        isSaved    ? 'advisor-card--saved' : '',
        isDragging ? 'advisor-card--dragging' : '',
        panelOpen  ? 'advisor-card--expanded' : '',
        isPinned   ? 'advisor-card--pinned' : '',
      ].filter(Boolean).join(' ')}
      style={{ '--card-accent': config.accent }}
      ref={cardRef}
    >
      {/* Drag handle */}
      <span className="advisor-card__drag-handle" {...dragHandleProps} {...{ title: t('brief.dragReorder') }}>
        <FaGripVertical />
      </span>

      {/* ── Header: icon | meta | save | trash ── */}
      <div className="advisor-card__header">
        <span className="advisor-card__icon"><CardIcon /></span>

        <div className="advisor-card__meta">
          <div className="advisor-card__meta-top">
            <span className="advisor-card__label">{card.label}</span>
            {isUser && <span className="advisor-card__user-badge">{t('brief.askedByYou')}</span>}
            {isSaved && (
              <span className="advisor-card__saved-badge">
                <FaThumbtack className="saved-badge__icon" /> {t('brief.savedBadge')}
              </span>
            )}
            {isPinned && (
              <span className="advisor-card__pinned-badge">
                <FaMapPin className="pinned-badge__icon" /> {t('brief.pinnedBadge')}
              </span>
            )}
          </div>
          <h3 className="advisor-card__title">{card.title}</h3>
        </div>

        {/* Trash, save, pin */}
        <div className="advisor-card__header-actions">
          <button
            className="advisor-card__delete"
            onClick={() => onDelete(card.id)}
            {...{ title: t('brief.deleteCard') }}
          >
            <FaTrash />
          </button>

          <button
            className={`advisor-card__save ${isSaved ? 'advisor-card__save--active' : ''}`}
            onClick={handleSave}
            disabled={saving}
            {...{ title: isSaved ? t('brief.removeBookmark') : t('brief.bookmark') }}
          >
            {isSaved ? <FaBookmark /> : <FaRegBookmark />}
          </button>

          <button
            className={`advisor-card__pin ${isPinned ? 'advisor-card__pin--active' : ''}`}
            onClick={handlePin}
            {...{ title: isPinned ? t('brief.unpin') : t('brief.pin') }}
          >
            <FaMapPin style={isPinned ? {} : { opacity: 0.45 }} />
          </button>
        </div>
      </div>

      {/* ── Body — always visible ── */}
      <p className="advisor-card__body">{card.body}</p>

      {/* ── Collapsible panel: chips + thread + chat bar + close toggle ── */}
      <div className={`advisor-card__panel ${panelOpen ? 'advisor-card__panel--open' : ''}`}>
        <div className="advisor-card__panel-inner">

          {/* Follow-up question chips */}
          {chips.length > 0 && (
            <div className="advisor-card__chips">
              {chips.map((chip, i) => (
                <button
                  key={i}
                  className="advisor-card__chip"
                  onClick={() => handleSend(chip)}
                  disabled={isThinking}
                >
                  <FaBolt className="chip-icon" />
                  {chip}
                </button>
              ))}
            </div>
          )}

          {thread.length > 0 && (
            <div className={`advisor-card__thread ${isExpanded ? '' : 'advisor-card__thread--preview'}`}>
              <div className="thread-divider" />
              {isExpanded ? (
                <ThreadMessages thread={thread} isThinking={isThinking} />
              ) : (
                <div className="advisor-card__thread-preview">
                  <div className={`thread-message thread-message--${thread[thread.length - 1].role}`}>
                    <p className="thread-text">
                      {thread[thread.length - 1].content.slice(0, 100)}
                      {thread[thread.length - 1].content.length > 100 ? '…' : ''}
                    </p>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Chat bar — always shown in open panel */}
          <div className="advisor-card__chat-bar-wrapper">
            <CardChatBar
              onSend={handleSend}
              isThinking={isThinking}
              onFocus={() => {
                if (!panelOpen) { setPanelOpen(true); onExpand(card.id) }
              }}
            />
          </div>

          {/* Close chevron */}
          <div className="advisor-card__toggle-row">
            <button
              className="advisor-card__toggle advisor-card__toggle--open"
              onClick={togglePanel}
              aria-label="Collapse"
            >
              <FaChevronUp />
            </button>
          </div>

        </div>
      </div>

      {/* ── Open chevron — always visible below the body when closed ── */}
      {!panelOpen && (
        <div className="advisor-card__toggle-row">
          <button
            className="advisor-card__toggle"
            onClick={togglePanel}
            aria-label="Expand"
          >
            <FaChevronDown />
          </button>
        </div>
      )}

      {/* Peek strip when collapsed but thread has messages */}
      {!panelOpen && thread.length > 0 && (
        <button className="advisor-card__thread-peek" onClick={togglePanel}>
          <span className={`thread-peek__role thread-peek__role--${thread[thread.length - 1].role}`}>
            {thread[thread.length - 1].role === 'user' ? t('brief.you') : t('brief.ai')}:
          </span>{' '}
          <span className="thread-peek__text">
            {thread[thread.length - 1].content.slice(0, 90)}
            {thread[thread.length - 1].content.length > 90 ? '…' : ''}
          </span>
        </button>
      )}
    </article>
  )
}

// ── Skeleton ──────────────────────────────────────────────────
function CardSkeleton() {
  return (
    <div className="advisor-card advisor-card--skeleton">
      <div className="skeleton-header">
        <div className="skeleton-circle" />
        <div className="skeleton-lines">
          <div className="skeleton-line skeleton-line--short" />
          <div className="skeleton-line skeleton-line--medium" />
        </div>
      </div>
      <div className="skeleton-line skeleton-line--long" />
      <div className="skeleton-line skeleton-line--medium" />
      <div className="skeleton-chips">
        <div className="skeleton-chip" /><div className="skeleton-chip" />
      </div>
    </div>
  )
}

// ── Drag-and-drop feed ────────────────────────────────────────
function DraggableFeed({
  cards, threadMap, thinkingCards, expandedCards,
  pinnedCardId, onSaveToggle, onPinToggle,
  onReorder, onSend, onExpand, onCollapse, onDelete,
}) {
  const [items, setItems]     = useState(cards)
  const [dragIdx, setDragIdx] = useState(null)
  const [overIdx, setOverIdx] = useState(null)
  const commitRef             = useRef(null)

  useEffect(() => { setItems(cards) }, [cards])

  const scrollAnimRef = useRef(null)

  const startAutoScroll = (e) => {
    const feed = document.querySelector('.advisor-cards-feed')
    if (!feed) return
    const cancelScroll = () => {
      cancelAnimationFrame(scrollAnimRef.current)
      scrollAnimRef.current = null
    }
    const ZONE = 80
    const SPEED = 12
    const tick = () => {
      const rect = feed.getBoundingClientRect()
      const y = e.clientY
      if (y - rect.top < ZONE) {
        feed.scrollTop -= SPEED
      } else if (rect.bottom - y < ZONE) {
        feed.scrollTop += SPEED
      } else {
        cancelScroll()
        return
      }
      scrollAnimRef.current = requestAnimationFrame(tick)
    }
    cancelScroll()
    scrollAnimRef.current = requestAnimationFrame(tick)
  }

  const handleDragStart = (idx) => (e) => {
    setDragIdx(idx)
    e.dataTransfer.effectAllowed = 'move'
    const ghost = document.createElement('div')
    ghost.style.cssText = 'position:absolute;top:-9999px'
    document.body.appendChild(ghost)
    e.dataTransfer.setDragImage(ghost, 0, 0)
    setTimeout(() => document.body.removeChild(ghost), 0)
  }

  const handleDragEnter = (idx) => () => {
    if (idx === dragIdx) return
    setOverIdx(idx)
    setItems(prev => {
      const next = [...prev]
      const [moved] = next.splice(dragIdx, 1)
      next.splice(idx, 0, moved)
      setDragIdx(idx)
      return next
    })
  }

  const handleDragEnd = () => {
    cancelAnimationFrame(scrollAnimRef.current)
    scrollAnimRef.current = null
    setDragIdx(null); setOverIdx(null)
    clearTimeout(commitRef.current)
    commitRef.current = setTimeout(() => {
      onReorder(items.map((card, i) => ({ id: card.id, sort_order: i })))
    }, 300)
  }

  return (
    <>
      {items.map((card, idx) => (
        <div
          key={card.id}
          className={`dnd-row ${dragIdx === idx ? 'dnd-row--dragging' : ''} ${overIdx === idx ? 'dnd-row--over' : ''}`}
          draggable
          onDragStart={handleDragStart(idx)}
          onDragEnter={handleDragEnter(idx)}
          onDragOver={e => { e.preventDefault(); startAutoScroll(e) }}
          onDragEnd={handleDragEnd}
        >
          <AdvisorCard
            card={card}
            thread={threadMap[card.id] || []}
            isThinking={thinkingCards.has(card.id)}
            isExpanded={expandedCards.has(card.id)}
            isPinned={card.id === pinnedCardId}
            onSaveToggle={onSaveToggle}
            onPinToggle={onPinToggle}
            onSend={(msg) => onSend(card.id, msg, card.title, card.body)}
            onExpand={onExpand}
            onCollapse={onCollapse}
            onDelete={onDelete}
            isDragging={dragIdx === idx}
            dragHandleProps={{
              onMouseDown: e => e.currentTarget.closest('[draggable]').setAttribute('draggable', true),
            }}
          />
        </div>
      ))}
    </>
  )
}

// ── Main export ───────────────────────────────────────────────
export default function AdvisorCards({
  userId = null,
  cards = [],
  isLoading = false,
  isGenerating = false,
  isAsking = false,
  generatedAt = null,
  onRefresh,
  onChipClick,
  onSaveToggle,
  onPinToggle,
  pinnedCardId = null,
  onReorder,
  onDeleteCard,
  freeformInput,
  setFreeformInput,
  onFreeformSubmit,
}) {
  const { t, language } = useLanguage()
  const [activeCategory, setActiveCategory] = useState('all')
  const [timeAgo, setTimeAgo] = useState('')

  const storageKey = userId ? `advisor_threads_${userId}` : 'advisor_threads'
  const deletedKey = userId ? `advisor_deleted_${userId}` : 'advisor_deleted'

  // ── Track locally-deleted card IDs so the count and feed stay in sync ──
  // Stored as { id: timestampMs } so entries older than 30 days are pruned automatically.
  const _DELETED_TTL_MS = 30 * 24 * 60 * 60 * 1000 // 30 days

  const [deletedIds, setDeletedIds] = useState(() => {
    try {
      const raw = JSON.parse(localStorage.getItem(deletedKey) || '{}')
      // Support legacy format (plain array) and new format (object with timestamps)
      if (Array.isArray(raw)) return new Set(raw)
      const now = Date.now()
      const pruned = Object.fromEntries(
        Object.entries(raw).filter(([, ts]) => now - ts < _DELETED_TTL_MS)
      )
      // Persist pruned version back immediately
      try { localStorage.setItem(deletedKey, JSON.stringify(pruned)) } catch {}
      return new Set(Object.keys(pruned))
    } catch { return new Set() }
  })

  // visibleCards is the source-of-truth for counts and the feed
  const visibleCards = cards.filter(c => !deletedIds.has(c.id))

  const [threadMap, setThreadMap] = useState(() => {
    try { return JSON.parse(localStorage.getItem(storageKey) || '{}') } catch { return {} }
  })
  const [thinkingCards, setThinking] = useState(new Set())
  const [expandedCards, setExpanded] = useState(new Set())

  useEffect(() => {
    try { localStorage.setItem(storageKey, JSON.stringify(threadMap)) } catch {}
  }, [threadMap, storageKey])

  const feedRef = useRef(null)
  const prevLen = useRef(visibleCards.length)

  useEffect(() => {
    if (visibleCards.length > prevLen.current && feedRef.current) {
      feedRef.current.scrollTo({ top: 0, behavior: 'smooth' })
    }
    prevLen.current = visibleCards.length
  }, [visibleCards.length])

  useEffect(() => {
    if (!generatedAt) return
    const update = () => {
      const diff = Math.floor((Date.now() - new Date(generatedAt).getTime()) / 60000)
      if (diff < 1)        setTimeAgo(t('brief.timeJustNow'))
      else if (diff === 1) setTimeAgo(t('brief.time1Min'))
      else if (diff < 60)  setTimeAgo(t('brief.timeMins').replace('{n}', diff))
      else                 setTimeAgo(t('brief.timeHours').replace('{n}', Math.floor(diff / 60)))
    }
    update()
    const interval = setInterval(update, 60000)
    return () => clearInterval(interval)
  }, [generatedAt, t])

  const handleSend = useCallback(async (cardId, message, cardTitle, cardBody) => {
    setExpanded(prev => new Set([...prev, cardId]))
    setThreadMap(prev => ({
      ...prev,
      [cardId]: [...(prev[cardId] || []), { role: 'user', content: message, lang: language }],
    }))
    setThinking(prev => new Set([...prev, cardId]))

    try {
      const reply = await onChipClick(cardId, message, cardTitle, cardBody)
      setThreadMap(prev => ({
        ...prev,
        [cardId]: [...(prev[cardId] || []), { role: 'assistant', content: reply }],
      }))
    } catch {
      setThreadMap(prev => ({
        ...prev,
        [cardId]: [...(prev[cardId] || []), { role: 'assistant', content: t('brief.errorSend') }],
      }))
    } finally {
      setThinking(prev => { const n = new Set(prev); n.delete(cardId); return n })
    }
  }, [onChipClick, t, language])

  const handleExpand   = useCallback((id) => setExpanded(prev => new Set([...prev, id])), [])
  const handleCollapse = useCallback((id) => setExpanded(prev => { const n = new Set(prev); n.delete(id); return n }), [])

  const handleDelete = useCallback((cardId) => {
    setExpanded(prev  => { const n = new Set(prev); n.delete(cardId); return n })
    setThreadMap(prev => { const n = { ...prev }; delete n[cardId]; return n })
    setThinking(prev  => { const n = new Set(prev); n.delete(cardId); return n })
    setDeletedIds(prev => {
      const n = new Set(prev)
      n.add(cardId)
      // Persist as { id: timestampMs } for TTL pruning on next load
      try {
        const raw = JSON.parse(localStorage.getItem(deletedKey) || '{}')
        const existing = Array.isArray(raw)
          ? Object.fromEntries([...raw].map(id => [id, 0]))
          : raw
        localStorage.setItem(deletedKey, JSON.stringify({ ...existing, [cardId]: Date.now() }))
      } catch {}
      return n
    })
    if (onDeleteCard) onDeleteCard(cardId)
  }, [onDeleteCard, deletedKey])

  const handlePinToggle = useCallback((card, thread) => {
    const isCurrentlyPinned = card.id === pinnedCardId
    if (onPinToggle) onPinToggle(isCurrentlyPinned ? null : card, isCurrentlyPinned ? [] : thread)
  }, [pinnedCardId, onPinToggle])

  const showSkeletons = isLoading || isGenerating

  // Counts are all based on visibleCards (deleted cards excluded)
  const categoryCounts = visibleCards.reduce((acc, card) => {
    const cat = card.category || 'other'
    acc[cat] = (acc[cat] || 0) + 1
    return acc
  }, {})

  const savedCards = visibleCards.filter(c => c.is_saved)

  const filteredCards =
    activeCategory === 'all'   ? visibleCards :
    activeCategory === 'saved' ? savedCards :
    visibleCards.filter(c => (c.category || 'other') === activeCategory)

  const activeCats = CARD_CATEGORIES.filter(cat => categoryCounts[cat])

  return (
    <div className="advisor-cards-root">

      {/* ── Header ── */}
      <header className="advisor-cards-header">
        <div className="advisor-cards-header__left">
          <h2 className="advisor-cards-header__title">{t('brief.title')}</h2>
          {generatedAt && !showSkeletons && (
            <span className="advisor-cards-header__timestamp">{t('brief.updated').replace('{time}', timeAgo)}</span>
          )}
        </div>
        <button
          className={`advisor-cards-refresh ${isGenerating ? 'spinning' : ''}`}
          onClick={onRefresh}
          disabled={isGenerating}
          {...{ title: t('brief.refresh') }}
        >
          <FaSync />
        </button>
      </header>

      {/* ── Category bar ── */}
      {!showSkeletons && (
        <nav className="category-bar">
          {/* All tab */}
          <button
            className={`category-tab ${activeCategory === 'all' ? 'active' : ''}`}
            onClick={() => setActiveCategory('all')}
          >
            <FaClipboardList className="category-tab__icon" />
            {t('brief.all')}
            <span className="category-tab__count">{visibleCards.length}</span>
          </button>

          {/* Per-category tabs — only shown if that category has cards */}
          {activeCats.map(cat => {
            const CatIcon = CATEGORY_ICON_COMPONENTS[cat] || FaComments
            return (
              <button
                key={cat}
                className={`category-tab ${activeCategory === cat ? 'active' : ''}`}
                onClick={() => setActiveCategory(cat)}
              >
                <CatIcon className="category-tab__icon" />
                {catLabel(cat, t)}
                {categoryCounts[cat] > 0 && (
                  <span className="category-tab__count">{categoryCounts[cat]}</span>
                )}
              </button>
            )
          })}

          {/* Saved tab */}
          <button
            className={`category-tab category-tab--saved ${activeCategory === 'saved' ? 'active' : ''}`}
            onClick={() => setActiveCategory('saved')}
          >
            <FaBookmark className="category-tab__icon" />
            {t('brief.saved')}
            {savedCards.length > 0 && (
              <span className="category-tab__count">{savedCards.length}</span>
            )}
          </button>
        </nav>
      )}



      {/* ── Card feed ── */}
      <div className="advisor-cards-feed" ref={feedRef}>
        {showSkeletons ? (
          <><CardSkeleton /><CardSkeleton /><CardSkeleton /></>
        ) : filteredCards.length === 0 && visibleCards.length === 0 ? (
          <div className="advisor-cards-empty">
            <FaGraduationCap className="empty-icon" />
            <p>{t('brief.preparing')}</p>
            <button className="btn-primary" onClick={onRefresh}>{t('brief.generateNow')}</button>
          </div>
        ) : filteredCards.length === 0 && activeCategory === 'saved' ? (
          <div className="advisor-cards-empty">
            <FaBookmark className="empty-icon" />
            <p>{t('brief.noSaved')}</p>
          </div>
        ) : filteredCards.length === 0 ? (
          <div className="advisor-cards-empty">
            {(() => { const I = CATEGORY_ICON_COMPONENTS[activeCategory] || FaComments; return <I className="empty-icon" /> })()}
            <p>{t('brief.noCards').replace('{category}', catLabel(activeCategory, t))}</p>
          </div>
        ) : (
          <DraggableFeed
            cards={filteredCards}
            threadMap={threadMap}
            thinkingCards={thinkingCards}
            expandedCards={expandedCards}
            pinnedCardId={pinnedCardId}
            onSaveToggle={onSaveToggle}
            onPinToggle={handlePinToggle}
            onReorder={onReorder}
            onSend={handleSend}
            onExpand={handleExpand}
            onCollapse={handleCollapse}
            onDelete={handleDelete}
          />
        )}
      </div>

      {/* ── Freeform input ── */}
      <form className="advisor-cards-freeform" onSubmit={onFreeformSubmit}>
        <input
          type="text"
          className="freeform-input"
          {...{ placeholder: t('brief.placeholder') }}
          value={freeformInput}
          onChange={e => setFreeformInput(e.target.value)}
          disabled={isAsking}
        />
        <button
          type="submit"
          className="freeform-send"
          disabled={isAsking || !freeformInput.trim()}
        >
          {isAsking
            ? <span className="thinking-dots small"><span /><span /><span /></span>
            : <FaArrowRight />}
        </button>
      </form>

    </div>
  )
}
