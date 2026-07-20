import { useState, useEffect, useCallback, useRef } from 'react'
import { useLanguage } from '../../../contexts/PreferencesContext'
import {
  FaSync, FaChevronDown, FaChevronUp,
  FaChevronLeft, FaChevronRight,
  FaBolt, FaArrowRight, FaGraduationCap,
  FaClipboardList, FaComments, FaCalendarAlt,
  FaChartBar, FaMapMarkedAlt, FaLightbulb,
  FaBookmark, FaRegBookmark, FaThumbtack,
  FaGripVertical, FaTrash, FaMapPin,
} from 'react-icons/fa'
import { CARD_CATEGORIES, CATEGORY_LABELS } from '../../../lib/cardsAPI'
import useViewport from '../../../hooks/useViewport'
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

// ── Thread messages scroller ──────────────────────────────────
// `className` / `leading` exist for the mobile full-screen thread, where this
// element becomes the page's only scroller and carries the card summary +
// starter chips above the transcript. Both default to the desktop behaviour.
function ThreadMessages({ thread, isThinking, className = '', leading = null }) {
  const scrollRef = useRef(null)
  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [thread.length, isThinking])

  return (
    <div className={`thread-messages${className ? ` ${className}` : ''}`} ref={scrollRef}>
      {leading}
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

// ── Follow-up chips ───────────────────────────────────────────
// Shared by the desktop inline panel and the mobile full-screen thread so the
// typed-action map below only ever exists in one place. Renders exactly the
// markup the desktop panel used before this was extracted.
function CardChips({ chips, isThinking, onSend }) {
  if (!chips.length) return null
  return (
    <div className="advisor-card__chips">
      {chips.map((chip, i) => {
        const chipLabel = typeof chip === 'string' ? chip : (chip?.label ?? '')
        const chipType  = typeof chip === 'object' ? chip?.type : null
        // Typed actions short-circuit the normal chat-send flow.
        // Keep this list in sync with Dashboard's window listeners.
        const TYPED_ACTIONS = {
          open_transcript_upload: 'open-transcript-upload',
          open_degree_planning:   'open-degree-planning',
        }
        const dispatchEvent = TYPED_ACTIONS[chipType]
        const handleChipClick = () => {
          if (dispatchEvent) {
            window.dispatchEvent(new CustomEvent(dispatchEvent))
            return
          }
          onSend(chipLabel)
        }
        return (
          <button
            key={i}
            className="advisor-card__chip"
            onClick={handleChipClick}
            disabled={isThinking && !dispatchEvent}
          >
            <FaBolt className="chip-icon" />
            {chipLabel}
          </button>
        )
      })}
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

  const CardIcon = CATEGORY_ICON_COMPONENTS[card.category || 'other'] || FaComments
  const isSaved  = card.is_saved || false
  const isUser   = card.source === 'user'

  useEffect(() => {
    if (!isExpanded) return
    const handleClickOutside = (e) => {
      if (e.target.closest('.sidebar')) return
      if (cardRef.current && !cardRef.current.contains(e.target)) {
        onCollapse(card.id)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [isExpanded, card.id, onCollapse])

  const chips = card.actions || []

  // Sync with parent expanded state (two-way): the parent can both open this
  // card and collapse it — so opening one card from Home closes the others,
  // and click-outside actually closes the panel.
  useEffect(() => { setPanelOpen(isExpanded) }, [isExpanded])

  // Auto-open only when a NEW message arrives (not on initial mount from localStorage).
  // Also register in the parent's expanded set so open state is fully tracked
  // (lets a Home deep-link collapse this card too).
  const prevThreadLen = useRef(thread.length)
  useEffect(() => {
    if (thread.length > prevThreadLen.current) { setPanelOpen(true); onExpand(card.id) }
    prevThreadLen.current = thread.length
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [thread.length])

  const handleSave = async (e) => {
    e.stopPropagation()
    if (saving) return
    setSaving(true)
    try { await onSaveToggle(card.id, !isSaved) }
    finally { setSaving(false) }
  }

  // `onPinToggle` is undefined in shells with no right sidebar to pin into
  // (MobileLayout), so the button is not rendered at all there — this guard is
  // belt-and-braces for any other shell that omits the prop.
  const canPin = typeof onPinToggle === 'function'

  const handlePin = (e) => {
    e.stopPropagation()
    if (!canPin) return
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
      style={{
        // During streaming, each card gets an explicit stagger delay so they
        // visually appear one by one. After persisted (id present), clear it.
        ...(card._streamIdx !== undefined && !card.id
          ? { animationDelay: `${card._streamIdx * 0.18}s` }
          : {}),
      }}
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

          {canPin && (
            <button
              className={`advisor-card__pin ${isPinned ? 'advisor-card__pin--active' : ''}`}
              onClick={handlePin}
              {...{ title: isPinned ? t('brief.unpin') : t('brief.pin') }}
            >
              <FaMapPin style={isPinned ? {} : { opacity: 0.45 }} />
            </button>
          )}
        </div>
      </div>

      {/* ── Body — always visible ── */}
      <p className="advisor-card__body">{card.body}</p>

      {/* ── Collapsible panel: chips + thread + chat bar + close toggle ── */}
      <div className={`advisor-card__panel ${panelOpen ? 'advisor-card__panel--open' : ''}`}>
        <div className="advisor-card__panel-inner">

          {/* Follow-up question chips */}
          <CardChips chips={chips} isThinking={isThinking} onSend={handleSend} />

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

// ══════════════════════════════════════════════════════════════
// MOBILE (<= 768px)
//
// The desktop card is a self-contained inline chat: it expands in place, can
// be dragged to reorder, and can be pinned into the right sidebar. None of
// those three metaphors survive a phone — there is no sidebar to pin into,
// HTML5 drag events never fire from touch, and an inline expanding thread
// fights the page scroller for the small amount of vertical space there is.
//
// So mobile gets a list -> detail push instead: a compact, whole-card-tappable
// summary in the feed, and a full-screen thread view with a back control. The
// desktop components below are left exactly as they were.
// ══════════════════════════════════════════════════════════════

// ── Mobile: compact card in the list ──────────────────────────
function MobileAdvisorCard({ card, thread = [], isThinking = false, onOpen, onSaveToggle, onDelete }) {
  const { t } = useLanguage()
  const [saving, setSaving] = useState(false)

  const CardIcon = CATEGORY_ICON_COMPONENTS[card.category || 'other'] || FaComments
  const isSaved  = card.is_saved || false
  const isUser   = card.source === 'user'
  const last     = thread.length > 0 ? thread[thread.length - 1] : null

  const handleSave = async (e) => {
    e.stopPropagation()
    if (saving) return
    setSaving(true)
    try { await onSaveToggle(card.id, !isSaved) }
    finally { setSaving(false) }
  }

  const handleDelete = (e) => {
    e.stopPropagation()
    onDelete(card.id)
  }

  const open = () => onOpen(card.id)

  const countKey = thread.length === 1 ? 'brief.msgs' : 'brief.msgsPlural'

  return (
    /* The whole card is tappable, but it deliberately is NOT role="button":
       it already contains buttons, and nesting button roles breaks assistive
       tech. The footer row below is a real <button>, so keyboard and screen
       reader users get an explicit, focusable way in. */
    <article
      data-card-id={card.id}
      onClick={open}
      className={[
        'advisor-card',
        'advisor-card--mobile',
        `advisor-card--${card.card_type || card.type}`,
        isUser  ? 'advisor-card--user' : '',
        isSaved ? 'advisor-card--saved' : '',
      ].filter(Boolean).join(' ')}
      style={{
        ...(card._streamIdx !== undefined && !card.id
          ? { animationDelay: `${card._streamIdx * 0.18}s` }
          : {}),
      }}
    >
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
          </div>
          <h3 className="advisor-card__title">{card.title}</h3>
        </div>

        {/* No pin button: there is no right sidebar on mobile to pin into. */}
        <div className="advisor-card__header-actions">
          <button
            className={`advisor-card__save ${isSaved ? 'advisor-card__save--active' : ''}`}
            onClick={handleSave}
            disabled={saving}
            {...{ 'aria-label': isSaved ? t('brief.removeBookmark') : t('brief.bookmark') }}
          >
            {isSaved ? <FaBookmark /> : <FaRegBookmark />}
          </button>

          <button
            className="advisor-card__delete"
            onClick={handleDelete}
            {...{ 'aria-label': t('brief.deleteCard') }}
          >
            <FaTrash />
          </button>
        </div>
      </div>

      <p className="advisor-card__body">{card.body}</p>

      <button
        type="button"
        className="advisor-card__mobile-open"
        onClick={(e) => { e.stopPropagation(); open() }}
      >
        <span className="advisor-card__mobile-open-label">
          {isThinking
            ? <span className="thinking-dots small"><span /><span /><span /></span>
            : last
              ? (
                <>
                  <span className={`thread-peek__role thread-peek__role--${last.role}`}>
                    {last.role === 'user' ? t('brief.you') : t('brief.ai')}:
                  </span>{' '}
                  <span className="thread-peek__text">{last.content}</span>
                </>
              )
              : t('cards.openThread')}
        </span>
        {thread.length > 0 && (
          <span className="advisor-card__mobile-count">
            {t(countKey).replace('{n}', thread.length)}
          </span>
        )}
        <FaChevronRight className="advisor-card__mobile-chevron" />
      </button>
    </article>
  )
}

// ── Mobile: full-screen thread push view ──────────────────────
// Deliberately covers the fixed bottom tab bar (z-index 100). A detail view
// that only sat above it would leave the composer wedged between a keyboard
// and a nav rail; covering it gives the thread the whole screen, and the back
// control is the single, obvious way out.
function MobileCardThread({ card, thread, isThinking, onSend, onClose, onSaveToggle }) {
  const { t } = useLanguage()
  const [saving, setSaving] = useState(false)

  const CardIcon = CATEGORY_ICON_COMPONENTS[card.category || 'other'] || FaComments
  const isSaved  = card.is_saved || false
  const chips    = card.actions || []

  // Escape closes the view. Android's back gesture surfaces as Escape in some
  // WebView configurations, matching how MobileLayout closes its More sheet.
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  const handleSave = async () => {
    if (saving) return
    setSaving(true)
    try { await onSaveToggle(card.id, !isSaved) }
    finally { setSaving(false) }
  }

  return (
    <div
      className="mobile-card-thread"
      role="dialog"
      aria-modal="true"
      aria-label={card.title}
    >
      <header className="mobile-card-thread__bar">
        <button
          className="mobile-card-thread__back"
          onClick={onClose}
          {...{ 'aria-label': t('cards.back') }}
        >
          <FaChevronLeft />
        </button>

        <div className="mobile-card-thread__heading">
          <span className="advisor-card__label">{card.label}</span>
          <h2 className="mobile-card-thread__title">{card.title}</h2>
        </div>

        <button
          className={`advisor-card__save ${isSaved ? 'advisor-card__save--active' : ''}`}
          onClick={handleSave}
          disabled={saving}
          {...{ 'aria-label': isSaved ? t('brief.removeBookmark') : t('brief.bookmark') }}
        >
          {isSaved ? <FaBookmark /> : <FaRegBookmark />}
        </button>
      </header>

      {/* The transcript is the only scroller in this view; the card summary and
          starter chips ride along at the top of it rather than eating fixed
          height above it. */}
      <ThreadMessages
        thread={thread}
        isThinking={isThinking}
        className="thread-messages--fill"
        leading={
          <div className="mobile-card-thread__intro">
            <span className="advisor-card__icon"><CardIcon /></span>
            <p className="advisor-card__body">{card.body}</p>
            <CardChips chips={chips} isThinking={isThinking} onSend={onSend} />
          </div>
        }
      />

      <div className="mobile-card-thread__composer">
        <CardChatBar onSend={onSend} isThinking={isThinking} />
      </div>
    </div>
  )
}

// ── Mobile: plain (non-reorderable) feed ──────────────────────
function MobileFeed({ cards, threadMap, thinkingCards, onOpen, onSaveToggle, onDelete }) {
  return (
    <>
      {cards.map(card => (
        <MobileAdvisorCard
          key={card.id}
          card={card}
          thread={threadMap[card.id] || []}
          isThinking={thinkingCards.has(card.id)}
          onOpen={onOpen}
          onSaveToggle={onSaveToggle}
          onDelete={onDelete}
        />
      ))}
    </>
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
          data-card-id={card.id}
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
  openCardId = null,
  onOpenedCard,
}) {
  const { t, language } = useLanguage()
  const { isMobile } = useViewport()
  const [activeCategory, setActiveCategory] = useState('all')
  const [timeAgo, setTimeAgo] = useState('')
  // Mobile only: which card's thread is showing as a full-screen push view.
  const [mobileThreadId, setMobileThreadId] = useState(null)

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
      try { localStorage.setItem(deletedKey, JSON.stringify(pruned)) } catch { /* ignore */ }
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
    try { localStorage.setItem(storageKey, JSON.stringify(threadMap)) } catch { /* ignore */ }
  }, [threadMap, storageKey])

  // Deep link from Home: open ONLY the requested card's chat (collapsing any
  // others that were open) and scroll to it.
  useEffect(() => {
    if (!openCardId || !cards.some(c => c.id === openCardId)) return
    // On mobile the equivalent of "open this card's chat" is pushing its
    // full-screen thread, not expanding a panel somewhere down the feed.
    if (isMobile) {
      setMobileThreadId(openCardId)
      onOpenedCard?.()
      return
    }
    setExpanded(new Set([openCardId]))
    requestAnimationFrame(() => {
      const el = document.querySelector(`[data-card-id="${openCardId}"]`)
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    })
    onOpenedCard?.()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [openCardId, cards, isMobile])

  // Crossing the breakpoint mid-session (rotation, desktop resize) must not
  // leave a full-screen mobile overlay hanging over the desktop layout.
  useEffect(() => {
    if (!isMobile) setMobileThreadId(null)
  }, [isMobile])

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
      } catch { /* ignore */ }
      return n
    })
    if (onDeleteCard) onDeleteCard(cardId)
  }, [onDeleteCard, deletedKey])

  const handlePinToggle = useCallback((card, thread) => {
    const isCurrentlyPinned = card.id === pinnedCardId
    if (onPinToggle) onPinToggle(isCurrentlyPinned ? null : card, isCurrentlyPinned ? [] : thread)
  }, [pinnedCardId, onPinToggle])

  const showSkeletons = isLoading || isGenerating

  // Auto-open the top card's chat panel so it's immediately obvious that
  // cards are chats, not static tips. Fires once per tab visit — this
  // component remounts every time the user switches to the Brief tab
  // (Dashboard conditionally renders it), so the guard just prevents it
  // from re-firing on every re-render within a single visit.
  // Skipped on mobile: there is no inline panel to open, and auto-pushing a
  // full-screen thread on arrival would hide the card list the user came for.
  const autoExpandedRef = useRef(false)
  useEffect(() => {
    if (isMobile || autoExpandedRef.current || showSkeletons) return
    // If Home deep-linked a specific card, let that effect own the expansion —
    // don't also open the top card (which would leave two cards open).
    if (openCardId) { autoExpandedRef.current = true; return }
    const topCard = visibleCards[0]
    if (!topCard) return
    autoExpandedRef.current = true
    setExpanded(prev => new Set([...prev, topCard.id]))
  }, [showSkeletons, visibleCards, openCardId, isMobile])

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

  // Resolved from visibleCards so a refresh or a delete that drops the card
  // also dismisses the thread instead of stranding a stale overlay.
  const mobileThreadCard = mobileThreadId
    ? visibleCards.find(c => c.id === mobileThreadId) || null
    : null

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
        <nav className="category-bar" data-tour="chat-categories">
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
        ) : isMobile ? (
          /* Reordering is intentionally absent here — see MobileFeed's note. */
          <MobileFeed
            cards={filteredCards}
            threadMap={threadMap}
            thinkingCards={thinkingCards}
            onOpen={setMobileThreadId}
            onSaveToggle={onSaveToggle}
            onDelete={handleDelete}
          />
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
      <form className="advisor-cards-freeform" onSubmit={onFreeformSubmit} data-tour="chat-freeform">
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

      <p className="rsb-disclaimer">{t('rsb.disclaimer')}</p>

      {isMobile && mobileThreadCard && (
        <MobileCardThread
          card={mobileThreadCard}
          thread={threadMap[mobileThreadCard.id] || []}
          isThinking={thinkingCards.has(mobileThreadCard.id)}
          onSend={(msg) => handleSend(mobileThreadCard.id, msg, mobileThreadCard.title, mobileThreadCard.body)}
          onClose={() => setMobileThreadId(null)}
          onSaveToggle={onSaveToggle}
        />
      )}

    </div>
  )
}
