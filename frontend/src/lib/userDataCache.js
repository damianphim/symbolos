/**
 * userDataCache.js — tiny SWR-style localStorage cache for per-user data.
 *
 * Pattern at call sites:
 *   1. useState with a hydrator that reads from cache (instant first paint)
 *   2. fire the existing fetch in useEffect
 *   3. when fetch returns, write back to cache
 *
 * Cache entries are namespaced by user_id so signing in as a different user
 * doesn't show the previous user's data, and have a 24h TTL by default so
 * stale data is eventually refreshed even if a fetch silently fails.
 */

const DEFAULT_TTL_MS = 24 * 60 * 60 * 1000  // 24 hours

function _key(prefix, userId) {
  return `udc_${prefix}_${userId || 'anon'}`
}

export function readCache(prefix, userId, fallback = null, ttlMs = DEFAULT_TTL_MS) {
  if (!userId) return fallback
  try {
    const raw = localStorage.getItem(_key(prefix, userId))
    if (!raw) return fallback
    const { data, ts } = JSON.parse(raw)
    if (typeof ts !== 'number') return fallback
    if (Date.now() - ts > ttlMs) return fallback
    return data === undefined ? fallback : data
  } catch {
    return fallback
  }
}

export function writeCache(prefix, userId, data) {
  if (!userId) return
  try {
    localStorage.setItem(_key(prefix, userId), JSON.stringify({ data, ts: Date.now() }))
  } catch {
    // Quota exceeded or storage disabled — silently ignore
  }
}

export function clearCache(prefix, userId) {
  if (!userId) return
  try { localStorage.removeItem(_key(prefix, userId)) } catch { /* Cache removal is best effort when browser storage is unavailable. */ }
}

/**
 * Bulk-clear every udc_* entry for a user. Call from signOut.
 */
export function clearAllForUser(userId) {
  if (!userId) return
  try {
    const suffix = `_${userId}`
    const toRemove = []
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i)
      if (k && k.startsWith('udc_') && k.endsWith(suffix)) toRemove.push(k)
    }
    toRemove.forEach(k => localStorage.removeItem(k))
  } catch { /* Cache removal is best effort when browser storage is unavailable. */ }
}
