/**
 * frontend/src/lib/apiConfig.js
 *
 * Shared API configuration. All API clients should import BASE_URL
 * from here instead of duplicating the normalizeUrl logic.
 */
import { supabase } from './supabase'

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

/**
 * Authorization header for direct `fetch()` calls (transcript/syllabus upload,
 * degree requirements). Unlike the axios instance in api.js, these callers
 * don't get the request interceptor, so this must be robust on its own.
 *
 * Previously each caller did `getSession()` and returned `{}` when no token
 * was present — so an expired access token produced an unauthenticated request
 * and a cryptic backend 401 ("Missing or invalid Authorization header"). Here
 * we refresh when the token is missing or about to expire, and throw a clear,
 * user-facing message if we genuinely can't authenticate.
 */
export async function getAuthHeaders() {
  let { data: { session } } = await supabase.auth.getSession()
  // expires_at is unix seconds; refresh if missing or within 60s of expiry.
  const nearExpiry = session?.expires_at && (session.expires_at * 1000 - Date.now() < 60_000)
  if (!session?.access_token || nearExpiry) {
    const { data } = await supabase.auth.refreshSession()
    session = data?.session ?? session
  }
  if (!session?.access_token) {
    throw new Error('Your session has expired. Please sign in again.')
  }
  return { Authorization: `Bearer ${session.access_token}` }
}