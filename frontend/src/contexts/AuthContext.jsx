/* eslint-disable react-refresh/only-export-components */
import { createContext, useContext, useEffect, useState, useCallback, useRef } from 'react'
import { supabase } from '../lib/supabase'
import api, { usersAPI, authAPI } from '../lib/api'

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
  const [needsOnboarding, setNeedsOnboarding]       = useState(false)
  const [needsPasswordReset, setNeedsPasswordReset] = useState(false)
  const [authFlags, setAuthFlags]                   = useState({ is_admin: false, is_mcgill_email: false })

  const mountedRef         = useRef(true)
  const loadingProfile     = useRef(false)
  const justSignedUp       = useRef(false)
  const justUpdatedProfile = useRef(false)
  const loadedForUserId    = useRef(null)

  const loadProfile = useCallback(async (userId) => {
    if (!mountedRef.current) return

    if (loadingProfile.current) {
      return
    }

    if (loadedForUserId.current === userId && profile !== null) {
      return
    }

    loadingProfile.current = true

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
          // Pre-seed the token so the axios interceptor doesn't race on cold load
          if (session?.access_token) {
            api.defaults.headers.common['Authorization'] = `Bearer ${session.access_token}`
          }
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

        // Don't update user state during the brief sign-in that happens
        // inside signUp() before we call signOut() to enforce email verification.
        if (justSignedUp.current) return

        setUser(session?.user ?? null)

        if (event === 'PASSWORD_RECOVERY') {
          // User clicked a password-reset link — signal the UI to show the reset form
          if (session?.access_token) {
            api.defaults.headers.common['Authorization'] = `Bearer ${session.access_token}`
          }
          // Store recovery flag so Login.jsx can switch to 'reset' mode
          if (mountedRef.current) setNeedsPasswordReset(true)
          return
        }

        if (event === 'SIGNED_IN' && session?.user) {
          // Pre-seed the token immediately on sign-in
          if (session?.access_token) {
            api.defaults.headers.common['Authorization'] = `Bearer ${session.access_token}`
          }
          if (justSignedUp.current) {
            justSignedUp.current = false
            return
          }
          if (justUpdatedProfile.current) {
            justUpdatedProfile.current = false
            return
          }

          // If this is the first login after email verification, restore onboarding.
          // The flag was stored in signUp() and survives the redirect from the email link.
          const pendingId = localStorage.getItem('symbolos_pending_onboarding')
          if (pendingId && pendingId === session.user.id) {
            localStorage.removeItem('symbolos_pending_onboarding')
            if (mountedRef.current) setNeedsOnboarding(true)
          }

          // Non-blocking — fire in background so login feels instant
          loadProfile(session.user.id)
        }

        if (event === 'SIGNED_OUT') {
          delete api.defaults.headers.common['Authorization']
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

      const redirectTo = `${window.location.origin}/`
      const { data, error: signUpError } = await supabase.auth.signUp({
        email,
        password,
        options: { emailRedirectTo: redirectTo },
      })
      if (signUpError) throw signUpError
      if (!data.user) throw new Error('Signup failed: no user returned')
      if (data.user.identities && data.user.identities.length === 0) throw new Error('EMAIL_ALREADY_EXISTS')

      // Create the profile row (email_verified defaults to false in the DB)
      try {
        await usersAPI.createUser({ id: data.user.id, email, username: username?.trim() || null })
      } catch (profileError) {
        const status = profileError.response?.status
        const code   = profileError.response?.data?.code
        if (status !== 409 && code !== 'user_already_exists') {
          console.error('Profile creation error:', profileError)
        }
      }

      // Send verification email via Resend (bypasses Supabase rate limits)
      try {
        await authAPI.sendVerification(data.user.id, email)
      } catch (emailError) {
        console.error('Failed to send verification email:', emailError)
        // Non-fatal — user can resend from the verify screen
      }

      justSignedUp.current = false

      return { data, error: null, needsEmailVerification: true }
    } catch (err) {
      justSignedUp.current = false
      setError({ type: 'SIGNUP_FAILED', message: friendlyAuthError(err) })
      return { data: null, error: { message: friendlyAuthError(err) } }
    }
  }

  // ── resendVerificationEmail ───────────────────────────────────────────────
  const resendVerificationEmail = async (email) => {
    try {
      if (!user?.id) throw new Error('No user session')
      await authAPI.sendVerification(user.id, email)
      return { error: null }
    } catch (err) {
      return { error: { message: err?.response?.data?.detail || err.message || 'Failed to send email' } }
    }
  }

  // ── resetPasswordForEmail ─────────────────────────────────────────────────
  const resetPasswordForEmail = async (email) => {
    try {
      const redirectTo = `${window.location.origin}/`
      const { error } = await supabase.auth.resetPasswordForEmail(email, { redirectTo })
      if (error) throw error
      return { error: null }
    } catch (err) {
      return { error: { message: friendlyAuthError(err) } }
    }
  }

  // ── updatePassword ────────────────────────────────────────────────────────
  const updatePassword = async (newPassword) => {
    try {
      const { error } = await supabase.auth.updateUser({ password: newPassword })
      if (error) throw error
      return { error: null }
    } catch (err) {
      return { error: { message: friendlyAuthError(err) } }
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
    try {
      await api.delete(`/users/${user.id}`)
    } catch (err) {
      const detail = err.response?.data?.detail
      throw new Error(detail?.message || detail || 'Failed to delete account')
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

  // Fetch auth flags (admin, mcgill email) from backend when user is set
  useEffect(() => {
    if (!user?.id) { setAuthFlags({ is_admin: false, is_mcgill_email: false }); return }
    authAPI.getFlags().then(flags => {
      if (mountedRef.current) setAuthFlags(flags)
    })
  }, [user?.id])

  const clearError = useCallback(() => setError(null), [])

  const refreshProfile = useCallback(async () => {
    if (!user?.id) return
    loadedForUserId.current = null
    loadingProfile.current = false
    await loadProfile(user.id)
  }, [user?.id, loadProfile])

  const clearPasswordReset = useCallback(() => setNeedsPasswordReset(false), [])

  const value = { user, profile, loading, error, needsOnboarding, needsPasswordReset, authFlags, signUp, signIn, signOut, deleteAccount, updateProfile, refreshProfile, completeOnboarding, clearError, clearPasswordReset, resetPasswordForEmail, resendVerificationEmail, updatePassword }
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
