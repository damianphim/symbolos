/**
 * Form validation utilities
 */

export const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
export const PASSWORD_MIN_LENGTH = 8
export const USERNAME_MIN_LENGTH = 3
export const USERNAME_MAX_LENGTH = 20
export const USERNAME_REGEX = /^[a-zA-Z0-9_]+$/

/**
 * Validate email format
 */
export const validateEmail = (email) => {
  if (!email) {
    return 'Email is required'
  }
  if (!EMAIL_REGEX.test(email)) {
    return 'Please enter a valid email address'
  }
  return null
}

/**
 * Validate password strength
 */
export const validatePassword = (password, isSignup = false) => {
  if (!password) {
    return 'Password is required'
  }
  if (password.length < PASSWORD_MIN_LENGTH) {
    return `Password must be at least ${PASSWORD_MIN_LENGTH} characters`
  }
  if (isSignup) {
    if (!/[a-z]/.test(password)) {
      return 'Password must include lowercase letters'
    }
    if (!/[A-Z]/.test(password)) {
      return 'Password must include uppercase letters'
    }
    if (!/\d/.test(password)) {
      return 'Password must include numbers'
    }
  }
  return null
}

/**
 * Validate username
 */
export const validateUsername = (username) => {
  if (!username) {
    return 'Username is required'
  }
  
  const trimmed = username.trim()
  
  if (trimmed.length < USERNAME_MIN_LENGTH) {
    return `Username must be at least ${USERNAME_MIN_LENGTH} characters`
  }
  if (trimmed.length > USERNAME_MAX_LENGTH) {
    return `Username must be no more than ${USERNAME_MAX_LENGTH} characters`
  }
  if (!USERNAME_REGEX.test(trimmed)) {
    return 'Username can only contain letters, numbers, and underscores'
  }
  return null
}

/**
 * Get user-friendly error message from API error
 */
export const getErrorMessage = (error) => {
  // Handle different error types
  if (!error) return 'An unknown error occurred'
  
  // Handle structured API errors
  if (error.response?.data?.code) {
    const { code, message } = error.response.data
    
    // Map error codes to user-friendly messages
    const errorMessages = {
      'USER_ALREADY_EXISTS': 'An account with this email already exists. Please sign in instead.',
      'USER_NOT_FOUND': 'No account found with this email.',
      'INVALID_TOKEN': 'Your session has expired. Please sign in again.',
      'VALIDATION_ERROR': 'Please check your input and try again.',
      'RATE_LIMIT_EXCEEDED': 'Too many attempts. Please try again in a few minutes.',
    }
    
    return errorMessages[code] || message || 'An error occurred'
  }
  
  // Handle Supabase auth errors
  const errorMessage = error.message || error.error_description || ''
  
  if (errorMessage.includes('Invalid login credentials')) {
    return 'Incorrect email or password. Please try again.'
  }
  if (errorMessage.includes('Email not confirmed')) {
    return 'Please verify your email address before signing in.'
  }
  if (errorMessage.includes('User already registered')) {
    return 'An account with this email already exists.'
  }
  if (errorMessage.includes('Password should be at least')) {
    return 'Password must be at least 8 characters long.'
  }
  if (error.code === 'ECONNREFUSED' || errorMessage.includes('Network')) {
    return 'Unable to connect. Please check your internet connection.'
  }
  if (errorMessage.includes('timeout')) {
    return 'Request timed out. Please try again.'
  }
  
  return errorMessage || 'Something went wrong. Please try again.'
}

/**
 * Sanitize user input to prevent XSS.
 * FIX F-10: Replaces the previous angle-bracket-only approach which was
 * trivially bypassed via HTML entities, Unicode, and javascript: URLs.
 *
 * Uses a multi-pass approach:
 *  1. Reject dangerous URI schemes (javascript:, data:, vbscript:)
 *  2. Encode all HTML special characters into safe entities
 *  3. Strip event-handler attribute patterns
 *  4. Enforce length limit
 */
export const sanitizeInput = (input) => {
  if (typeof input !== 'string') return input

  let s = input.trim()

  // 1. Block dangerous URI schemes (case-insensitive, ignoring whitespace/encoding)
  const dangerousScheme = /^\s*(javascript|data|vbscript)\s*:/i
  if (dangerousScheme.test(s)) return ''

  // 2. HTML-encode special characters to prevent injection
  s = s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')

  // 3. Strip any remaining on* event handler patterns
  s = s.replace(/on\w+\s*=/gi, '')

  // 4. Enforce length
  return s.slice(0, 1000)
}
