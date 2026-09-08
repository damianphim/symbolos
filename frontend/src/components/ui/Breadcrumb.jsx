import './ui.css'

/**
 * Presentational breadcrumb trail. `items` is an ordered array of
 * { key, label, onClick }, the last item renders as plain (current)
 * text, every earlier item is a clickable link back to that level.
 */
export default function Breadcrumb({ items, className = '' }) {
  return (
    <nav className={`ui-breadcrumb ${className}`} aria-label="Breadcrumb">
      {items.map((item, i) => {
        const isLast = i === items.length - 1
        return (
          <span key={item.key ?? i} className="ui-breadcrumb__segment">
            {i > 0 && <span className="ui-breadcrumb__sep">/</span>}
            {isLast ? (
              <span className="ui-breadcrumb__current">{item.label}</span>
            ) : (
              <button type="button" className="ui-breadcrumb__link" onClick={item.onClick}>
                {item.label}
              </button>
            )}
          </span>
        )
      })}
    </nav>
  )
}
