/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react'
import { supabase } from '../lib/supabase'
import { usersAPI } from '../lib/api'

const AuthContext = createContext({})

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser]                       = useState(null)
  const [profile, setProfile]                 = useState(null)
  const [loading, setLoading]                 = useState(true)
  const [error, setError]                     = useState(null)
  // True only for brand-new signups — keeps App.jsx on ProfileSetup
  // even though a minimal profile already exists in the DB.
  // Cleared by completeOnboarding() when the user finishes or skips.
  const [needsOnboarding, setNeedsOnboarding] = useState(false)

  const mountedRef         = useRef(true)
  const loadingProfile     = useRef(false)
  const justSignedUp       = useRef(false)
  const justUpdatedProfile = useRef(false)
  const loadedForUserId    = useRef(null)

  const loadProfile = useCallback(async (userId) => {
    if (!mountedRef.current) return

    if (loadingProfile.current) {
      console.log('Skipping loadProfile — already in progress')
      return
    }

    if (loadedForUserId.current === userId && profile !== null) {
      console.log('Skipping loadProfile — profile already loaded for this user')
      return
    }

    loadingProfile.current = true
    console.log('Loading profile for:', userId)

    try {
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Profile load timeout')), 15000)
      )

      const { user: userProfile } = await Promise.race([
        usersAPI.getUser(userId),
        timeoutPromise,
      ])

      if (mountedRef.current) {
        setProfile(userProfile)
        loadedForUserId.current = userId
        setError(null)
      }
    } catch (err) {
      console.error('Error loading profile:', err)

      if (mountedRef.current) {
        if (err.message === 'Profile load timeout') {
          if (!profile) {
            setError({ type: 'PROFILE_LOAD_TIMEOUT', message: 'Profile load timed out. Please check your connection and refresh.' })
          }
        } else if (err.response?.status === 404) {
          setProfile(null)
          loadedForUserId.current = null
          if (!justSignedUp.current) {
            setError({ type: 'PROFILE_NOT_FOUND', message: 'Profile not found.' })
          }
        } else {
          if (!profile) {
            setError({ type: 'PROFILE_LOAD_FAILED', message: 'Unable to load profile. Please refresh.' })
          }
        }
      }
    } finally {
      loadingProfile.current = false
      console.log('loadProfile finished')
    }
  }, [profile])

  useEffect(() => {
    mountedRef.current = true
    let authSubscription = null

    const initialize = async () => {
      try {
        const { data: { session }, error: sessionError } = await supabase.auth.getSession()
        if (sessionError) throw sessionError

        if (mountedRef.current) {
          setUser(session?.user ?? null)
          // Non-blocking — don't await so loading state clears fast
          if (session?.user) loadProfile(session.user.id)
        }
      } catch (err) {
        console.error('Auth initialization error:', err)
        if (mountedRef.current) setError({ type: 'AUTH_INIT_FAILED', message: 'Unable to initialize authentication' })
      } finally {
        if (mountedRef.current) setLoading(false)
      }
    }

    initialize()

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      async (event, session) => {
        if (!mountedRef.current) return

        setUser(session?.user ?? null)

        if (event === 'SIGNED_IN' && session?.user) {
          if (justSignedUp.current) {
            console.log('Skipping profile load — just signed up')
            justSignedUp.current = false
            return
          }
          if (justUpdatedProfile.current) {
            console.log('Skipping profile load — just updated profile')
            justUpdatedProfile.current = false
            return
          }
          // Non-blocking — fire in background so login feels instant
          loadProfile(session.user.id)
        }

        if (event === 'SIGNED_OUT') {
          setProfile(null)
          setError(null)
          setNeedsOnboarding(false)
          loadedForUserId.current = null
        }
      }
    )

    authSubscription = subscription

    return () => {
      mountedRef.current = false
      authSubscription?.unsubscribe()
    }
  }, [loadProfile])

  // ── signUp ──────────────────────────────────────────────────────────────
  const signUp = async (email, password, username) => {
    try {
      setError(null)

      // Must be set BEFORE supabase.auth.signUp() — Supabase fires SIGNED_IN
      // synchronously inside signUp, before it returns.
      justSignedUp.current = true

      const { data, error: signUpError } = await supabase.auth.signUp({ email, password })
      if (signUpError) throw signUpError
      if (!data.user) throw new Error('Signup failed: no user returned')
      if (data.user.identities && data.user.identities.length === 0) throw new Error('EMAIL_ALREADY_EXISTS')

      try {
        await usersAPI.createUser({ id: data.user.id, email, username: username?.trim() || null })
        console.log('Minimal profile record created')
      } catch (profileError) {
        const status = profileError.response?.status
        const code   = profileError.response?.data?.code
        if (status !== 409 && code !== 'user_already_exists') {
          console.error('Profile creation error:', profileError)
          // Don't throw — user auth succeeded, ProfileSetup will retry via updateUser
        }
      }

      if (mountedRef.current) {
        setUser(data.user)
        loadedForUserId.current = data.user.id
        justSignedUp.current = false
        setNeedsOnboarding(true)
      }

      return { data, error: null }
    } catch (err) {
      justSignedUp.current = false
      setError({ type: 'SIGNUP_FAILED', message: friendlyAuthError(err) })
      return { data: null, error: { message: friendlyAuthError(err) } }
    }
  }

  // ── signIn ──────────────────────────────────────────────────────────────
  const signIn = async (email, password) => {
    try {
      setError(null)
      loadedForUserId.current = null
      const { data, error: signInError } = await supabase.auth.signInWithPassword({ email, password })
      if (signInError) throw signInError
      return { data, error: null }
    } catch (err) {
      setError({ type: 'SIGNIN_FAILED', message: friendlyAuthError(err) })
      return { data: null, error: { message: friendlyAuthError(err) } }
    }
  }


  // ── deleteAccount ────────────────────────────────────────────────────────
  const deleteAccount = async () => {
    if (!user?.id) throw new Error('No user logged in')
    const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const BASE_URL = API_URL.replace(/\/api\/?$/, '').replace(/\/$/, '')
    const res = await fetch(`${BASE_URL}/api/users/${user.id}`, { method: 'DELETE' })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      throw new Error(data.detail?.message || 'Failed to delete account')
    }
    await supabase.auth.signOut()
    setUser(null)
    setProfile(null)
  }

  // ── signOut ─────────────────────────────────────────────────────────────
  const signOut = async () => {
    try {
      setError(null)
      const { error: signOutError } = await supabase.auth.signOut()
      if (signOutError) throw signOutError
      setUser(null)
      setProfile(null)
      setNeedsOnboarding(false)
      loadedForUserId.current = null
      return { error: null }
    } catch (err) {
      setError({ type: 'SIGNOUT_FAILED', message: err.message })
      return { error: err }
    }
  }

  // ── updateProfile ────────────────────────────────────────────────────────
  const updateProfile = async (updates) => {
    if (!user) throw new Error('No user logged in')
    try {
      setError(null)
      const { user: updatedUser } = await usersAPI.updateUser(user.id, updates)
      if (mountedRef.current) {
        justUpdatedProfile.current = true
        setProfile(updatedUser)
        loadedForUserId.current = user.id
        setTimeout(() => { justUpdatedProfile.current = false }, 1000)
      }
      return { data: updatedUser, error: null }
    } catch (err) {
      setError({ type: 'PROFILE_UPDATE_FAILED', message: 'Failed to update profile' })
      return { data: null, error: err }
    }
  }

  // ── completeOnboarding ───────────────────────────────────────────────────
  // Called by ProfileSetup when the user finishes or skips.
  // Fetches the latest profile from DB then clears needsOnboarding.
  const completeOnboarding = useCallback(async () => {
    if (!user?.id) return
    loadedForUserId.current = null
    loadingProfile.current = false
    await loadProfile(user.id)
    if (mountedRef.current) setNeedsOnboarding(false)
  }, [user?.id, loadProfile])

  const clearError = useCallback(() => setError(null), [])

  const value = { user, profile, loading, error, needsOnboarding, signUp, signIn, signOut, deleteAccount, updateProfile, completeOnboarding, clearError }
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// ── Translate raw Supabase / network errors into readable strings ─────────────
function friendlyAuthError(err) {
  const msg  = err?.message || err?.error_description || ''
  const code = err?.code || ''

  if (msg === 'EMAIL_ALREADY_EXISTS' || msg.includes('User already registered') || msg.includes('already been registered'))
    return 'An account with this email already exists. Please sign in instead.'
  if (msg.includes('Invalid login credentials') || code === 'invalid_credentials')
    return 'Incorrect email or password. Please try again.'
  if (msg.includes('Email not confirmed'))
    return 'Please verify your email address before signing in.'
  if (msg.includes('Password should be at least'))
    return 'Password must be at least 8 characters long.'
  if (msg.includes('rate limit') || msg.includes('too many requests') || code === 'over_request_rate_limit')
    return 'Too many attempts. Please wait a few minutes and try again.'
  if (code === 'NETWORK_ERROR' || msg.includes('Unable to connect') || msg.includes('Network'))
    return 'Unable to connect. Please check your internet connection.'
  if (msg.includes('timeout'))
    return 'Request timed out. Please try again.'
  return msg || 'Something went wrong. Please try again.'
}
