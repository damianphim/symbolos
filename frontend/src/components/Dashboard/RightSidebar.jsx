import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../../contexts/AuthContext'
import { chatAPI } from '../../lib/api'
import { FaRobot, FaChevronRight, FaArrowRight, FaTimes, FaCommentDots } from 'react-icons/fa'
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

// ── Shared chat input bar ─────────────────────────────────────────────────────
function SidebarChatBar({ onSend, isThinking, placeholder = 'Ask a follow-up…' }) {
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
        placeholder={placeholder}
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

// ── Nav assistant quick-action chips ─────────────────────────────────────────
const NAV_SUGGESTIONS = {
  courses:       ['How do I search for a course?', 'What do the GPA badges mean?', 'How do I mark a course complete?'],
  calendar:      ['How do I add an event?', 'How do I upload a syllabus?', 'Where are my final exam dates?'],
  degree:        ['How does degree progress work?', 'What is a complementary course?', 'How do I add a minor?'],
  profile:       ['How do I upload my transcript?', 'How do I add transfer credits?', 'How do I change my major?'],
  'study-abroad':['How do exchanges work at McGill?', 'Which programs are in Europe?', 'How do credits transfer?'],
  chat:          ['What can you help me with?', 'Tell me about my degree progress', 'Recommend courses for next semester'],
}

const DEFAULT_SUGGESTIONS = ['What can you help me with?', 'How do I plan my degree?', 'Show me my course options']

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
  const scrollRef = useRef(null)
  const navScrollRef = useRef(null)

  // Nav assistant state
  const [navMessages, setNavMessages] = useState([])
  const [navThinking, setNavThinking] = useState(false)
  const [navSessionId, setNavSessionId] = useState(null)

  // Greeting message when the sidebar opens without a pinned card
  useEffect(() => {
    if (!isOpen || pinnedCard) return
    if (navMessages.length === 0) {
      const tabLabel = {
        courses: 'Courses', calendar: 'Calendar', degree: 'Degree Planning',
        profile: 'Profile', 'study-abroad': 'Study Abroad', chat: 'Chat',
      }[activeTab] || 'the dashboard'
      setNavMessages([{
        role: 'assistant',
        content: `Hi! I'm your academic advisor. You're on ${tabLabel} — ask me anything or tap a suggestion below.`,
      }])
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isOpen, pinnedCard, activeTab])

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
      setNavMessages(prev => [...prev, { role: 'assistant', content: '❌ Something went wrong. Please try again.' }])
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
  // Show sidebar on all non-chat tabs (both pinned and nav-assistant modes)
  const showSidebar = activeTab !== 'chat'
  const suggestions = NAV_SUGGESTIONS[activeTab] || DEFAULT_SUGGESTIONS

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
          title="Open assistant"
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
                      <span className="rsb-header__label">Pinned Chat</span>
                      <span className="rsb-header__title">{pinnedCard.title}</span>
                    </div>
                  </div>
                  <div className="rsb-header__actions">
                    <button className="rsb-unpin-btn" onClick={onUnpin} title="Unpin card">
                      <MdOutlinePushPin size={16} />
                    </button>
                    <button className="rsb-close-btn" onClick={() => setIsOpen(false)} title="Close sidebar">
                      <FaChevronRight size={14} />
                    </button>
                  </div>
                </div>

                <div className="rsb-thread" ref={scrollRef}>
                  {(!pinnedThread || pinnedThread.length === 0) ? (
                    <div className="rsb-thread__empty">
                      <FaRobot className="rsb-thread__empty-icon" />
                      <p>No messages yet. Ask a follow-up below to continue the conversation.</p>
                    </div>
                  ) : (
                    pinnedThread.map((msg, i) => (
                      <div key={i} className={`rsb-msg rsb-msg--${msg.role}`}>
                        <p className="rsb-msg__text">{renderText(msg.content)}</p>
                      </div>
                    ))
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
                </div>
              </>
            ) : (
              /* ── NAV ASSISTANT MODE ── */
              <>
                <div className="rsb-header rsb-header--nav">
                  <div className="rsb-header__left">
                    <div className="rsb-header__text">
                      <span className="rsb-header__label">Website Assistant</span>
                      <span className="rsb-header__title">Ask me anything</span>
                    </div>
                  </div>
                  <button className="rsb-close-btn" onClick={() => setIsOpen(false)} title="Close">
                    <FaTimes size={14} />
                  </button>
                </div>

                {/* Messages */}
                <div className="rsb-thread" ref={navScrollRef}>
                  {navMessages.map((msg, i) => (
                    <div key={i} className={`rsb-msg rsb-msg--${msg.role}`}>
                      <p className="rsb-msg__text">{renderText(msg.content)}</p>
                    </div>
                  ))}
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
                    placeholder="Ask me about courses, planning, or how to navigate…"
                  />
                </div>
              </>
            )}
          </>
        )}
      </aside>
    </>
  )
}
