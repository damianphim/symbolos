/**
 * consent.js — one entry point for changing cookie/analytics consent.
 *
 * Writes the choice locally (drives analytics on/off immediately) AND records
 * it server-side with a timestamp when the user is authenticated, so we can
 * demonstrate consent if ever asked (Quebec Law 25 accountability). The
 * server record is best-effort: pre-login (landing page) there's no session
 * to attach it to, and it must never block the UI.
 */
import { setConsent, getConsent } from './telemetry'
import { usersAPI } from './api'
import { supabase } from './supabase'

export { getConsent }

/** Record the current local consent value server-side, if logged in. */
export async function syncConsentToServer(value = getConsent()) {
  if (value !== 'accepted' && value !== 'declined') return
  try {
    const { data: { session } } = await supabase.auth.getSession()
    if (session?.user?.id) await usersAPI.recordConsent(session.user.id, value)
  } catch { /* best-effort — localStorage remains the working record */ }
}

/** Change consent: apply locally (analytics react immediately) + persist. */
export async function updateConsent(value) {
  setConsent(value)
  await syncConsentToServer(value)
}
