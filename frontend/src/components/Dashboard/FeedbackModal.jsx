/**
 * FeedbackModal.jsx
 *
 * A feedback modal styled to match the existing ProfSuggestionPopover.
 * Two modes:
 *   - General feedback (free text, submitted to your backend or mailto)
 *   - Missing course (course code + optional note)
 *
 * Controlled by the parent, the trigger lives in Sidebar.jsx (mini-rail
 * pill + full-sidebar popup item), not in this component:
 *
 *   const [feedbackOpen, setFeedbackOpen] = useState(false)
 *   <Sidebar onOpenFeedback={() => setFeedbackOpen(true)} ... />
 *   <FeedbackModal open={feedbackOpen} onClose={() => setFeedbackOpen(false)} />
 */

import { useState, useRef, useEffect } from 'react'
import { FaFlag, FaCheck, FaCommentAlt, FaSearch } from 'react-icons/fa'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/PreferencesContext'
import Modal from '../ui/Modal'
import './FeedbackModal.css'

export default function FeedbackModal({ open, onClose }) {
  const { user } = useAuth()
  const { t } = useLanguage()
  const [mode, setMode]     = useState(null) // null | 'general' | 'missing-course'
  const [text, setText]     = useState('')
  const [course, setCourse] = useState('')
  const [status, setStatus] = useState('idle') // idle | submitting | success | error | duplicate
  const inputRef = useRef(null)

  // Focus first input when mode is selected
  // (overlay-click + Escape close are handled by the shared Modal)
  useEffect(() => {
    if (mode) setTimeout(() => inputRef.current?.focus(), 50)
  }, [mode])

  const close = () => {
    onClose()
    setMode(null)
    setText('')
    setCourse('')
    setStatus('idle')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const missingCourse = mode === 'missing-course'
    if (missingCourse && !course.trim()) return
    if (!missingCourse && !text.trim()) return

    setStatus('submitting')

    // Primary path: POST to the backend, which persists the feedback,
    // emails the admin inbox via Resend, and optionally pings Slack.
    // This works even when the user has no mail client configured.
    try {
      const { default: api } = await import('../../lib/api')
      await api.post('/feedback', {
        kind: missingCourse ? 'missing-course' : 'general',
        message: text.trim() || `(missing course request: ${course.trim()})`,
        course: missingCourse ? course.trim() : undefined,
        page: window.location.pathname,
      })
      setStatus('success')
      setTimeout(() => close(), 2000)
      return
    } catch (err) {
      console.warn('Feedback POST failed, falling back to mailto:', err)
    }

    // Fallback: mailto (covers the case where the backend is unreachable).
    const subject = encodeURIComponent(
      missingCourse
        ? `[Symbolos] Missing Course: ${course.trim()}`
        : '[Symbolos] Feedback'
    )
    const body = encodeURIComponent(
      missingCourse
        ? `Missing course: ${course.trim()}\nNote: ${text.trim()}\nUser: ${user?.email || 'anonymous'}`
        : `${text.trim()}\n\nUser: ${user?.email || 'anonymous'}`
    )
    window.open(`mailto:symbolosadvsry@gmail.com?subject=${subject}&body=${body}`)
    setStatus('success')
    setTimeout(() => close(), 2000)
  }

  return (
    <>
      {/* Overlay + Modal */}
      {open && (
        <Modal onClose={close} title={t('fb.title')} icon={<FaFlag />} size="sm">
            {/* Mode selection */}
            {!mode && status === 'idle' && (
              <div className="feedback-mode-select">
                <p className="feedback-modal-desc">{t('fb.modePrompt')}</p>
                <button className="feedback-mode-btn" onClick={() => setMode('general')}>
                  <FaCommentAlt className="feedback-mode-icon" />
                  <div>
                    <strong>{t('fb.modeGeneral')}</strong>
                    <span>{t('fb.modeGeneralSub')}</span>
                  </div>
                </button>
                <button className="feedback-mode-btn" onClick={() => setMode('missing-course')}>
                  <FaSearch className="feedback-mode-icon" />
                  <div>
                    <strong>{t('fb.modeMissing')}</strong>
                    <span>{t('fb.modeMissingSub')}</span>
                  </div>
                </button>
              </div>
            )}

            {/* General feedback form */}
            {mode === 'general' && status === 'idle' && (
              <form className="feedback-form" onSubmit={handleSubmit}>
                <p className="feedback-modal-desc">{t('fb.generalDesc')}</p>
                <textarea
                  ref={inputRef}
                  className="feedback-textarea"
                  placeholder={t('fb.generalPlaceholder')}
                  value={text}
                  onChange={e => setText(e.target.value)}
                  maxLength={1000}
                  rows={4}
                  disabled={status === 'submitting'}
                />
                <div className="feedback-form-actions">
                  <button type="button" className="feedback-cancel-btn" onClick={() => setMode(null)}>{t('fb.back')}</button>
                  <button
                    type="submit"
                    className="feedback-submit-btn"
                    disabled={!text.trim() || status === 'submitting'}
                  >
                    {status === 'submitting' ? t('fb.sending') : t('fb.send')}
                  </button>
                </div>
              </form>
            )}

            {/* Missing course form */}
            {mode === 'missing-course' && status === 'idle' && (
              <form className="feedback-form" onSubmit={handleSubmit}>
                <p className="feedback-modal-desc">{t('fb.missingDesc')}</p>
                <input
                  ref={inputRef}
                  className="feedback-input"
                  type="text"
                  placeholder={t('fb.missingPlaceholder')}
                  value={course}
                  onChange={e => setCourse(e.target.value)}
                  maxLength={50}
                  disabled={status === 'submitting'}
                />
                <textarea
                  className="feedback-textarea feedback-textarea--short"
                  placeholder={t('fb.missingExtra')}
                  value={text}
                  onChange={e => setText(e.target.value)}
                  maxLength={300}
                  rows={2}
                  disabled={status === 'submitting'}
                />
                <div className="feedback-form-actions">
                  <button type="button" className="feedback-cancel-btn" onClick={() => setMode(null)}>{t('fb.back')}</button>
                  <button
                    type="submit"
                    className="feedback-submit-btn"
                    disabled={!course.trim() || status === 'submitting'}
                  >
                    {status === 'submitting' ? t('fb.sending') : t('fb.submit')}
                  </button>
                </div>
              </form>
            )}

            {/* Success */}
            {status === 'success' && (
              <div className="feedback-success">
                <FaCheck /> {t('fb.success')}
              </div>
            )}

            {/* Duplicate */}
            {status === 'duplicate' && (
              <div className="feedback-duplicate">
                {t('fb.duplicate')}
                <button className="feedback-cancel-btn" onClick={close}>{t('fb.close')}</button>
              </div>
            )}
        </Modal>
      )}
    </>
  )
}
