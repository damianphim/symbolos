import './ui.css'

/**
 * Section title row with an optional right-aligned action slot
 * (link, button, or badge). Keeps card/section headers consistent.
 */
export default function SectionHeader({ title, action, className = '' }) {
  return (
    <div className={`ui-section-header ${className}`}>
      <h2 className="ui-section-header__title">
        {title}
      </h2>
      {action && <div className="ui-section-header__action">{action}</div>}
    </div>
  )
}
