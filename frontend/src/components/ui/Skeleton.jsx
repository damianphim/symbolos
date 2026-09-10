import './ui.css'

/**
 * Shimmering placeholder block. Compose several to sketch the shape of
 * loading content (see CardSkeleton in chat/AdvisorCards.jsx for the
 * pattern this generalises).
 */
export default function Skeleton({ width = '100%', height = '0.875rem', radius = '6px', circle = false, className = '', style }) {
  return (
    <div
      className={`ui-skeleton ${className}`}
      aria-hidden="true"
      style={{
        width: circle ? height : width,
        height,
        borderRadius: circle ? '50%' : radius,
        ...style,
      }}
    />
  )
}

/** Stack of shimmer lines, the last one shorter, quick text placeholder. */
export function SkeletonLines({ lines = 3, className = '' }) {
  return (
    <div className={`ui-skeleton-lines ${className}`} aria-hidden="true">
      {Array.from({ length: lines }, (_, i) => (
        <Skeleton key={i} width={i === lines - 1 ? '60%' : '100%'} />
      ))}
    </div>
  )
}
