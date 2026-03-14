/**
 * frontend/src/lib/apiConfig.js
 *
 * Shared API configuration. All API clients should import BASE_URL
 * from here instead of duplicating the normalizeUrl logic.
 */

const API_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.PROD
    ? (() => { throw new Error('VITE_API_URL must be set in production') })()
    : 'http://localhost:8000'
)

/**
 * Normalize the API URL:
 * - Remove trailing slash
 * - Remove /api suffix (we add it back per-request)
 */
const normalizeUrl = (url) => {
  let normalized = url.replace(/\/$/, '')
  if (normalized.endsWith('/api')) {
    normalized = normalized.slice(0, -4)
  }
  return normalized
}

export const BASE_URL = normalizeUrl(API_URL)
export const API_BASE = `${BASE_URL}/api`