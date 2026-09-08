import { useEffect, useRef, useCallback } from 'react'
import { FaTimes } from 'react-icons/fa'
import './ui.css'

/**
 * Base modal wrapper, one overlay/panel/header implementation for the
 * app's simple dialogs (complex flows like EventModal and TranscriptUpload
 * keep their bespoke shells for now).
 *
 * Handles: Escape + overlay-click close, body scroll lock, Tab focus trap,
 * ARIA dialog roles. Content is `children`; put form action buttons inside
 * your form, or use the `footer` slot for non-form dialogs.
 */
export default function Modal({
  onClose,
  title,
  subtitle,
  icon,
  headerActions,
  accent,
  size = 'md',            // 'sm' | 'md' | 'lg'
  footer,
  className = '',
  children,
}) {
  const panelRef = useRef(null)

  // Escape close
  useEffect(() => {
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [onClose])

  // Body scroll lock
  useEffect(() => {
    const prev = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => { document.body.style.overflow = prev }
  }, [])

  // Focus the panel on mount so Tab starts inside the dialog
  useEffect(() => {
    panelRef.current?.focus()
  }, [])

  // Minimal focus trap: keep Tab cycling within the panel
  const trapTab = useCallback((e) => {
    if (e.key !== 'Tab' || !panelRef.current) return
    const focusables = panelRef.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    )
    if (!focusables.length) return
    const first = focusables[0]
    const last  = focusables[focusables.length - 1]
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus()
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus()
    }
  }, [])

  return (
    <div
      className="ui-modal-overlay"
      onMouseDown={(e) => { if (e.target === e.currentTarget) onClose() }}
    >
      <div
        className={`ui-modal ui-modal--${size} ${className}`}
        role="dialog"
        aria-modal="true"
        tabIndex={-1}
        ref={panelRef}
        onKeyDown={trapTab}
      >
        {accent && <div className="ui-modal__accent" style={{ background: accent }} />}

        <div className="ui-modal__header">
          {icon && <span className="ui-modal__icon">{icon}</span>}
          <div className="ui-modal__titles">
            <h2 className="ui-modal__title">{title}</h2>
            {subtitle && <p className="ui-modal__subtitle">{subtitle}</p>}
          </div>
          {headerActions}
          <button className="ui-modal__close" onClick={onClose} aria-label="Close">
            <FaTimes />
          </button>
        </div>

        <div className="ui-modal__body">{children}</div>

        {footer && <div className="ui-modal__footer">{footer}</div>}
      </div>
    </div>
  )
}
