import './ui.css'

/**
 * Section title row with an optional right-aligned action slot
 * (link, button, or badge). Keeps card/section headers consistent.
 */
export default function SectionHeader({ icon, title, action, className = '', iconColor }) {
  return (
    <div className={`ui-section-header ${className}`}>
      <h2 className="ui-section-header__title">
        {icon && (
          <span
            className="ui-section-header__icon"
            style={iconColor ? { color: iconColor } : undefined}
          >
            {icon}
          </span>
        )}
        {title}
      </h2>
      {action && <div className="ui-section-header__action">{action}</div>}
    </div>
  )
}
