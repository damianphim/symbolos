/**
 * useScrollReveal, small IntersectionObserver hook that flips an element's
 * `data-revealed="true"` attribute once it enters the viewport, so CSS can
 * animate it in. One observer per element, disconnects after first reveal.
 *
 * Usage:
 *   const ref = useScrollReveal()
 *   <div ref={ref} className="reveal">...</div>
 *
 * Respects prefers-reduced-motion (instant reveal, no animation).
 */
import { useEffect, useRef } from 'react'

export default function useScrollReveal(options = {}) {
  const ref = useRef(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const prefersReduced = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
    if (prefersReduced) {
      el.setAttribute('data-revealed', 'true')
      return
    }

    if (!('IntersectionObserver' in window)) {
      el.setAttribute('data-revealed', 'true')
      return
    }

    const obs = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.setAttribute('data-revealed', 'true')
            obs.unobserve(entry.target)
          }
        })
      },
      {
        threshold: options.threshold ?? 0.15,
        rootMargin: options.rootMargin ?? '0px 0px -10% 0px',
      }
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [options.threshold, options.rootMargin])

  return ref
}
