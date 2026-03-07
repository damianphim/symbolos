/**
 * useNotificationPrefs.js
 *
 * Loads notification preferences from the users table in Supabase,
 * falls back to localStorage for instant reads, and keeps both in sync.
 *
 * The preferences are stored as a JSON column `notification_prefs` on the
 * users table. You'll need to add this column in Supabase:
 *
 *   ALTER TABLE users ADD COLUMN IF NOT EXISTS notification_prefs jsonb;
 *
 */
import { useState, useEffect, useCallback } from 'react'
import { usersAPI } from '../lib/api'

const STORAGE_KEY = 'mcgill_notification_prefs'

const DEFAULT_PREFS = {
  method: 'email',          // 'email' | 'sms' | 'both' | 'none'
  email: '',
  phone: '',
  timing: {
    sameDay: false,
    oneDay: true,
    oneWeek: true,
  },
  eventTypes: {
    exam:     true,          // final exams — auto-queued, opt-out here
    academic: true,
    union:    true,
    club:     true,
    personal: true,
  },
}

function mergeWithDefaults(stored) {
  if (!stored) return { ...DEFAULT_PREFS }
  return {
    ...DEFAULT_PREFS,
    ...stored,
    timing: { ...DEFAULT_PREFS.timing, ...(stored.timing || {}) },
    eventTypes: { ...DEFAULT_PREFS.eventTypes, ...(stored.eventTypes || {}) },
  }
}

function loadFromLocalStorage() {
  try {
    const stored = localStorage.getItem(STORAGE_KEY)
    return stored ? mergeWithDefaults(JSON.parse(stored)) : { ...DEFAULT_PREFS }
  } catch (_) {
    return { ...DEFAULT_PREFS }
  }
}

/**
 * @param {string|null} userId   - Supabase user id (null = not logged in)
 * @param {string|null} accountEmail - Account email to seed the email field
 */
export default function useNotificationPrefs(userId, accountEmail) {
  // Start with localStorage for instant render (no flash)
  const [prefs, setPrefsState] = useState(loadFromLocalStorage)
  const [syncing, setSyncing] = useState(false)

  // On mount (or when userId becomes available), load from Supabase
  useEffect(() => {
    if (!userId) return
    let cancelled = false

    async function loadFromSupabase() {
      try {
        const data = await usersAPI.getUser(userId)
        const remotePrefs = data?.user?.notification_prefs
        if (!cancelled && remotePrefs) {
          const merged = mergeWithDefaults(remotePrefs)
          setPrefsState(merged)
          localStorage.setItem(STORAGE_KEY, JSON.stringify(merged))
        }
      } catch (err) {
        // Non-fatal: just use whatever is in localStorage
        console.warn('Could not load notification prefs from Supabase:', err)
      }
    }

    loadFromSupabase()
    return () => { cancelled = true }
  }, [userId])

  // Seed email from account if not set
  useEffect(() => {
    if (accountEmail && !prefs.email) {
      setPrefsState(p => {
        const updated = { ...p, email: accountEmail }
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated))
        return updated
      })
    }
  }, [accountEmail]) // eslint-disable-line

  const setPrefs = useCallback(async (updater) => {
    setPrefsState(prev => {
      const next = typeof updater === 'function' ? updater(prev) : { ...prev, ...updater }
      // Always write to localStorage immediately for snappy UI
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next))

      // Persist to Supabase in the background
      if (userId) {
        setSyncing(true)
        usersAPI.updateUser(userId, { notification_prefs: next })
          .catch(err => console.warn('Failed to sync notification prefs:', err))
          .finally(() => setSyncing(false))
      }

      return next
    })
  }, [userId])

  return [prefs, setPrefs, syncing]
}
