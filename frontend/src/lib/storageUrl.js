/**
 * storageUrl.js — serve public storage objects from our own origin.
 *
 * Why: Supabase's storage CDN serves objects without
 * X-Content-Type-Options: nosniff, and application code cannot add response
 * headers to that origin. Routing through /storage/* (a Vercel rewrite in
 * frontend/vercel.json) means the site's own header block applies instead.
 *
 * Deliberately conservative — it only rewrites when the result is definitely
 * usable, and returns the original Supabase URL otherwise:
 *
 *   - https only. The backend validator (validate_profile_image in
 *     routes/users.py) requires an https URL on an allowlisted host, so a
 *     http://localhost origin would be rejected on save. Local dev therefore
 *     keeps using the absolute Supabase URL and behaves exactly as before.
 *
 *   - Web only. Capacitor runs from capacitor://localhost, where the Vercel
 *     rewrite doesn't exist at all, so native keeps the absolute URL too.
 *
 * Existing rows hold absolute Supabase URLs and keep working; the validator
 * accepts both shapes on purpose, so this migrates gradually rather than
 * breaking every avatar written before the proxy existed.
 */

const PUBLIC_MARKER = '/storage/v1/object/public/'

/** True when the current origin actually serves the /storage/* rewrite. */
function canProxy() {
  if (typeof window === 'undefined' || !window.location) return false
  return window.location.protocol === 'https:'
}

/**
 * Convert a Supabase public object URL into a same-origin proxy URL.
 * Returns the input unchanged when proxying isn't applicable.
 */
export function toProxiedStorageUrl(publicUrl) {
  if (!publicUrl || !canProxy()) return publicUrl
  const idx = publicUrl.indexOf(PUBLIC_MARKER)
  if (idx === -1) return publicUrl
  const objectPath = publicUrl.slice(idx + PUBLIC_MARKER.length)
  return `${window.location.origin}/storage/${objectPath}`
}
