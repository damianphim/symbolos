import { useState, useEffect, useRef, useCallback } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/LanguageContext'
import { chatAPI } from '../../lib/api'
import { FaRobot, FaChevronRight, FaArrowRight, FaTimes, FaChevronDown, FaChevronUp, FaThumbtack } from 'react-icons/fa'
import { MdPushPin, MdOutlinePushPin } from 'react-icons/md'
import './RightSidebar.css'

// ── Simple text renderer (bold + newlines) ────────────────────────────────────
function renderText(text) {
  // Split on **bold** and newlines
  const parts = text.split(/(\*\*[^*]+\*\*|\n)/g)
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>
    }
    if (part === '\n') return <br key={i} />
    return part
  })
}

// ── Load pinned messages from localStorage ────────────────────────────────────
function loadPinnedMessages() {
  try {
    const raw = localStorage.getItem('rsb_pinned_messages')
    return raw ? JSON.parse(raw) : []
  } catch {
    return []
  }
}

function savePinnedMessages(pins) {
  try {
    localStorage.setItem('rsb_pinned_messages', JSON.stringify(pins))
  } catch { /* quota exceeded — silently fail */ }
}

// ── Shared chat input bar ─────────────────────────────────────────────────────
function SidebarChatBar({ onSend, isThinking, placeholder }) {
  const { t } = useLanguage()
  const resolvedPlaceholder = placeholder ?? t('rsb.followUpPlaceholder')
  const [value, setValue] = useState('')
  const taRef = useRef(null)

  const adjustHeight = () => {
    const ta = taRef.current
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = Math.min(ta.scrollHeight, 100) + 'px'
  }

  const handleChange = (e) => { setValue(e.target.value); adjustHeight() }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); submit() }
  }

  const submit = () => {
    if (!value.trim() || isThinking) return
    onSend(value.trim())
    setValue('')
    if (taRef.current) taRef.current.style.height = 'auto'
  }

  return (
    <div className="rsb-chat-bar">
      <textarea
        ref={taRef}
        className="rsb-chat-bar__input"
        placeholder={resolvedPlaceholder}
        value={value}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        disabled={isThinking}
        rows={1}
      />
      <button
        className="rsb-chat-bar__send"
        onClick={submit}
        disabled={isThinking || !value.trim()}
        type="button"
      >
        {isThinking
          ? <span className="rsb-thinking-dots"><span /><span /><span /></span>
          : <FaArrowRight />}
      </button>
    </div>
  )
}

// ── Tab name helper ───────────────────────────────────────────────────────────
function getTabLabel(activeTab, t) {
  const tabKey = {
    courses: 'rsb.tab.courses',
    calendar: 'rsb.tab.calendar',
    favorites: 'rsb.tab.degree',
    profile: 'rsb.tab.profile',
    clubs: 'rsb.tab.clubs',
    forum: 'rsb.tab.forum',
  }[activeTab] || 'rsb.tab.default'
  return t(tabKey)
}

// ── Per-tab welcome message ───────────────────────────────────────────────────
function getWelcomeMessage(activeTab, t) {
  const key = {
    calendar: 'rsb.welcome.calendar',
    favorites: 'rsb.welcome.degree',
    clubs: 'rsb.welcome.clubs',
    courses: 'rsb.welcome.courses',
    profile: 'rsb.welcome.profile',
    forum: 'rsb.welcome.forum',
  }[activeTab] || 'rsb.welcome.default'
  return t(key)
}

// ── Main RightSidebar ─────────────────────────────────────────────────────────
export default function RightSidebar({
  isOpen,
  setIsOpen,
  pinnedCard,
  pinnedThread,
  pinnedIsThinking,
  onSend,
  onUnpin,
  activeTab,
}) {
  const { user } = useAuth()
  const { t, language } = useLanguage()
  const scrollRef = useRef(null)
  const navScrollRef = useRef(null)

  // ── Per-tab conversation persistence ────────────────────────────────────────
  // Keys: tab name, Values: { messages: [...], sessionId: string|null }
  const tabConversationsRef = useRef({})
  const prevTabRef = useRef(activeTab)

  // Nav assistant state
  const [navMessages, setNavMessages] = useState([])
  const [navThinking, setNavThinking] = useState(false)
  const [navSessionId, setNavSessionId] = useState(null)

  // Pinned messages state (persisted to localStorage)
  const [pinnedMessages, setPinnedMessages] = useState(loadPinnedMessages)
  const [pinnedSectionOpen, setPinnedSectionOpen] = useState(true)

  // Save pinned messages to localStorage whenever they change
  useEffect(() => {
    savePinnedMessages(pinnedMessages)
  }, [pinnedMessages])

  // Toggle pin on a message
  const togglePin = useCallback((msg) => {
    setPinnedMessages(prev => {
      const exists = prev.some(
        p => p.content === msg.content && p.role === msg.role && p.tab === msg.tab
      )
      if (exists) {
        return prev.filter(
          p => !(p.content === msg.content && p.role === msg.role && p.tab === msg.tab)
        )
      }
      return [...prev, { ...msg, tab: msg.tab || activeTab, pinnedAt: Date.now() }]
    })
  }, [activeTab])

  const isMessagePinned = useCallback((msg) => {
    return pinnedMessages.some(
      p => p.content === msg.content && p.role === msg.role
    )
  }, [pinnedMessages])

  // ── Tab switch: save current conversation, restore new tab's ───────────────
  useEffect(() => {
    const prevTab = prevTabRef.current
    if (prevTab !== activeTab) {
      // Save current conversation for the previous tab
      tabConversationsRef.current[prevTab] = {
        messages: navMessages,
        sessionId: navSessionId,
      }

      // Restore conversation for the new tab (or start fresh)
      const saved = tabConversationsRef.current[activeTab]
      if (saved && saved.messages.length > 0) {
        setNavMessages(saved.messages)
        setNavSessionId(saved.sessionId)
      } else {
        // Fresh welcome message for this tab
        setNavMessages([{
          role: 'assistant',
          content: getWelcomeMessage(activeTab, t),
        }])
        setNavSessionId(null)
      }
      prevTabRef.current = activeTab
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab])

  // Initial greeting when sidebar first opens and no messages exist
  useEffect(() => {
    if (!isOpen || pinnedCard) return
    if (navMessages.length === 0) {
      setNavMessages([{
        role: 'assistant',
        content: getWelcomeMessage(activeTab, t),
      }])
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, pinnedCard])

  // Re-translate the welcome message when language changes (only if it's the only message)
  useEffect(() => {
    if (navMessages.length === 1 && navMessages[0].role === 'assistant') {
      setNavMessages([{
        role: 'assistant',
        content: getWelcomeMessage(activeTab, t),
      }])
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [language])

  // Auto-scroll nav thread
  useEffect(() => {
    if (navScrollRef.current) {
      navScrollRef.current.scrollTop = navScrollRef.current.scrollHeight
    }
  }, [navMessages, navThinking])

  // Auto-scroll pinned thread
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [pinnedThread?.length, pinnedIsThinking])

  // Handle nav assistant message
  const handleNavSend = async (text) => {
    if (!user?.id) return
    setNavMessages(prev => [...prev, { role: 'user', content: text }])
    setNavThinking(true)
    try {
      const res = await chatAPI.sendMessage(user.id, text, navSessionId, activeTab)
      if (!navSessionId && res.session_id) setNavSessionId(res.session_id)
      setNavMessages(prev => [...prev, { role: 'assistant', content: res.response }])
    } catch {
      setNavMessages(prev => [...prev, { role: 'assistant', content: t('rsb.errorMsg') }])
    } finally {
      setNavThinking(false)
    }
  }

  // Draggable toggle button position
  const [buttonPos, setButtonPos] = useState(() => {
    const saved = localStorage.getItem('rightSidebarButtonPosition')
    return saved ? parseFloat(saved) : 50
  })
  const [isDragging, setIsDragging] = useState(false)

  useEffect(() => {
    localStorage.setItem('rightSidebarButtonPosition', buttonPos.toString())
  }, [buttonPos])

  useEffect(() => {
    if (!isDragging) return
    const onMove = (e) => {
      const y = e.touches ? e.touches[0].clientY : e.clientY
      const pct = Math.min(Math.max((y / window.innerHeight) * 100, 10), 90)
      setButtonPos(pct)
    }
    const onUp = () => setIsDragging(false)
    document.addEventListener('mousemove', onMove)
    document.addEventListener('mouseup', onUp)
    document.addEventListener('touchmove', onMove)
    document.addEventListener('touchend', onUp)
    return () => {
      document.removeEventListener('mousemove', onMove)
      document.removeEventListener('mouseup', onUp)
      document.removeEventListener('touchmove', onMove)
      document.removeEventListener('touchend', onUp)
    }
  }, [isDragging])

  const hasPinned = !!pinnedCard
  // When a card is pinned, the sidebar stays visible on every tab (including chat)
  // so the conversation is never interrupted by switching tabs
  const showSidebar = activeTab !== 'chat' || hasPinned
  const tabLabel = getTabLabel(activeTab, t)

  const suggestionKeys = {
    courses:       ['rsb.nav.courses.1','rsb.nav.courses.2','rsb.nav.courses.3'],
    calendar:      ['rsb.nav.calendar.1','rsb.nav.calendar.2','rsb.nav.calendar.3'],
    favorites:     ['rsb.nav.degree.1','rsb.nav.degree.2','rsb.nav.degree.3'],
    profile:       ['rsb.nav.profile.1','rsb.nav.profile.2','rsb.nav.profile.3'],
    clubs:         ['rsb.nav.clubs.1','rsb.nav.clubs.2','rsb.nav.clubs.3'],
    forum:         ['rsb.nav.forum.1','rsb.nav.forum.2','rsb.nav.forum.3'],
  }
  const suggestions = (suggestionKeys[activeTab] || ['rsb.nav.default.1','rsb.nav.default.2','rsb.nav.default.3']).map(k => t(k))

  // ── Render a message bubble ──────────────────────────────────────────────────
  const renderMessage = (msg, i) => {
    return (
      <div key={i} className={`rsb-msg rsb-msg--${msg.role}`}>
        <div className="rsb-msg__bubble-wrap">
          <p className="rsb-msg__text">{renderText(msg.content)}</p>
        </div>
      </div>
    )
  }

  // ── Pinned messages section ─────────────────────────────────────────────────
  const renderPinnedSection = () => {
    if (pinnedMessages.length === 0) return null
    return (
      <div className="rsb-pinned-section">
        <button
          className="rsb-pinned-section__toggle"
          onClick={() => setPinnedSectionOpen(prev => !prev)}
        >
          <FaThumbtack size={11} />
          <span>{t('rsb.pinnedMessages')} ({pinnedMessages.length})</span>
          {pinnedSectionOpen ? <FaChevronUp size={10} /> : <FaChevronDown size={10} />}
        </button>
        {pinnedSectionOpen && (
          <div className="rsb-pinned-section__list">
            {pinnedMessages.map((msg, i) => (
              <div key={i} className={`rsb-pinned-msg rsb-pinned-msg--${msg.role}`}>
                <p className="rsb-pinned-msg__text">{renderText(msg.content)}</p>
                <div className="rsb-pinned-msg__meta">
                  <span className="rsb-pinned-msg__tab">{msg.tab || '—'}</span>
                  <button
                    className="rsb-pin-btn rsb-pin-btn--active"
                    onClick={() => togglePin(msg)}
                    title={t('rsb.unpinMsg')}
                  >
                    <FaThumbtack size={9} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

  return (
    <>
      {/* Draggable tab — clean minimal strip */}
      {!isOpen && showSidebar && (
        <button
          className={`rsb-toggle ${isDragging ? 'rsb-toggle--dragging' : ''}`}
          style={{ top: `${buttonPos}%` }}
          onMouseDown={(e) => { setIsDragging(true); e.preventDefault() }}
          onTouchStart={() => setIsDragging(true)}
          onClick={() => { if (!isDragging) setIsOpen(true) }}
          title={t('rsb.openAssistant')}
          aria-label="Open assistant"
        >
          <FaChevronRight size={13} />
        </button>
      )}

      {/* Sidebar panel */}
      <aside className={`right-sidebar ${isOpen && showSidebar ? 'rsb--open' : 'rsb--closed'}`}>
        {isOpen && showSidebar && (
          <>
            {/* ── PINNED CARD MODE ── */}
            {hasPinned ? (
              <>
                <div className="rsb-header">
                  <div className="rsb-header__left">
                    <div className="rsb-logo-icon">
                      <MdPushPin size={18} />
                    </div>
                    <div className="rsb-header__text">
                      <span className="rsb-header__label">{t('rsb.pinnedChat')}</span>
                      <span className="rsb-header__title">{pinnedCard.title}</span>
                    </div>
                  </div>
                  <div className="rsb-header__actions">
                    <button className="rsb-unpin-btn" onClick={onUnpin} title={t('rsb.unpinCard')}>
                      <MdOutlinePushPin size={16} />
                    </button>
                    <button className="rsb-close-btn" onClick={() => setIsOpen(false)} title={t('rsb.closeSidebar')}>
                      <FaChevronRight size={14} />
                    </button>
                  </div>
                </div>

                <div className="rsb-thread" ref={scrollRef}>
                  {renderPinnedSection()}
                  {(!pinnedThread || pinnedThread.length === 0) ? (
                    <div className="rsb-thread__empty">
                      <FaRobot className="rsb-thread__empty-icon" />
                      <p>{t('rsb.noMessages')}</p>
                    </div>
                  ) : (
                    pinnedThread.map((msg, i) => renderMessage(msg, i))
                  )}
                  {pinnedIsThinking && (
                    <div className="rsb-msg rsb-msg--assistant">
                      <p className="rsb-msg__text">
                        <span className="rsb-thinking-dots"><span /><span /><span /></span>
                      </p>
                    </div>
                  )}
                </div>

                <div className="rsb-footer">
                  <SidebarChatBar onSend={onSend} isThinking={pinnedIsThinking} />
                  <div className="rsb-disclaimer">
                    {t('rsb.disclaimer')}
                  </div>
                </div>
              </>
            ) : (
              /* ── NAV ASSISTANT MODE ── */
              <>
                <div className="rsb-header rsb-header--nav">
                  <div className="rsb-header__left">
                    <div className="rsb-header__text">
                      <span className="rsb-header__label">{t('rsb.youreOn').replace('{tab}', tabLabel)}</span>
                      <span className="rsb-header__title">{t('rsb.askAnything')}</span>
                    </div>
                  </div>
                  <div className="rsb-header__actions">
                    <button className="rsb-close-btn" onClick={() => setIsOpen(false)} title={t('rsb.close')}>
                      <FaTimes size={14} />
                    </button>
                  </div>
                </div>

                {/* Messages */}
                <div className="rsb-thread" ref={navScrollRef}>
                  {navMessages.map((msg, i) => renderMessage(msg, i))}
                  {navThinking && (
                    <div className="rsb-msg rsb-msg--assistant">
                      <p className="rsb-msg__text">
                        <span className="rsb-thinking-dots"><span /><span /><span /></span>
                      </p>
                    </div>
                  )}
                </div>

                {/* Quick suggestion chips */}
                {navMessages.length <= 1 && !navThinking && (
                  <div className="rsb-suggestions">
                    {suggestions.map((s, i) => (
                      <button key={i} className="rsb-suggestion-chip" onClick={() => handleNavSend(s)}>
                        {s}
                      </button>
                    ))}
                  </div>
                )}

                <div className="rsb-footer">
                  <SidebarChatBar
                    onSend={handleNavSend}
                    isThinking={navThinking}
                    placeholder={t('rsb.navPlaceholder')}
                  />
                  <div className="rsb-disclaimer">
                    {t('rsb.disclaimer')}
                  </div>
                </div>
              </>
            )}
          </>
        )}
      </aside>
    </>
  )
}
