import { useState, useRef, useEffect } from 'react'
import { FaFlag, FaCheck, FaTimes } from 'react-icons/fa'
import { useAuth } from '../../contexts/AuthContext'
import { supabase } from '../../lib/supabase'
import './ProfSuggestionPopover.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const normalizeUrl = (url) => {
  let n = url.replace(/\/$/, '')
  if (n.endsWith('/api')) n = n.slice(0, -4)
  return n
}
const BASE_URL = normalizeUrl(API_URL)

export default function ProfSuggestionPopover({ courseCode, currentInstructor, onClose }) {
  const { user } = useAuth()
  const [suggestedName, setSuggestedName] = useState('')
  const [status, setStatus] = useState('idle') // idle | submitting | success | error | duplicate
  const popoverRef = useRef(null)
  const inputRef = useRef(null)

  // Focus input on open
  useEffect(() => {
    setTimeout(() => inputRef.current?.focus(), 50)
  }, [])

  // Close on outside click
  useEffect(() => {
    const handleClick = (e) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target)) {
        onClose()
      }
    }
    document.addEventListener('mousedown', handleClick)
    return () => document.removeEventListener('mousedown', handleClick)
  }, [onClose])

  // Close on Escape
  useEffect(() => {
    const handleKey = (e) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', handleKey)
    return () => document.removeEventListener('keydown', handleKey)
  }, [onClose])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!suggestedName.trim() || !user?.id) return

    setStatus('submitting')
    try {
      const { data: { session } } = await supabase.auth.getSession()
      const authHeader = session?.access_token
        ? { Authorization: `Bearer ${session.access_token}` }
        : {}
      const response = await fetch(`${BASE_URL}/api/suggestions/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...authHeader },
        body: JSON.stringify({
          user_id: user.id,
          course_code: courseCode,
          current_name: currentInstructor || null,
          suggested_name: suggestedName.trim(),
        }),
      })

      if (response.status === 409) {
        setStatus('duplicate')
        return
      }
      if (!response.ok) throw new Error('Failed to submit')

      setStatus('success')
      setTimeout(() => onClose(), 1800)
    } catch {
      setStatus('error')
    }
  }

  return (
    <div className="prof-popover" ref={popoverRef} onClick={(e) => e.stopPropagation()}>
      <div className="prof-popover-header">
        <FaFlag className="prof-popover-flag" />
        <span>Suggest a correction</span>
        <button className="prof-popover-close" onClick={onClose}><FaTimes /></button>
      </div>

      {status === 'success' ? (
        <div className="prof-popover-success">
          <FaCheck /> Thanks! We'll review your suggestion.
        </div>
      ) : status === 'duplicate' ? (
        <div className="prof-popover-duplicate">
          You've already submitted a suggestion for this course.
          <button className="prof-popover-dismiss" onClick={onClose}>Dismiss</button>
        </div>
      ) : (
        <>
          <p className="prof-popover-desc">
            Think the professor listed for <strong>{courseCode}</strong> is wrong?
            Let us know who actually teaches it — we'll verify and update.
          </p>

          {currentInstructor && (
            <div className="prof-popover-current">
              Currently listed: <span>{currentInstructor}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <input
              ref={inputRef}
              className="prof-popover-input"
              type="text"
              placeholder="Correct professor name"
              value={suggestedName}
              onChange={(e) => setSuggestedName(e.target.value)}
              maxLength={200}
              disabled={status === 'submitting'}
            />
            {status === 'error' && (
              <p className="prof-popover-error">Something went wrong. Please try again.</p>
            )}
            <div className="prof-popover-actions">
              <button type="button" className="prof-popover-cancel" onClick={onClose}>
                Cancel
              </button>
              <button
                type="submit"
                className="prof-popover-submit"
                disabled={!suggestedName.trim() || status === 'submitting'}
              >
                {status === 'submitting' ? 'Submitting…' : 'Submit'}
              </button>
            </div>
          </form>
        </>
      )}
    </div>
  )
}
