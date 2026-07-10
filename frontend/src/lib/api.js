import axios from 'axios'
import { supabase } from './supabase'

const API_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.PROD
    ? (() => { throw new Error('VITE_API_URL must be set in production') })()
    : 'http://localhost:8000/api'
)

// Create axios instance with configuration
const api = axios.create({
  baseURL: API_URL,
  timeout: 30000, // 30 seconds
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - add auth token
api.interceptors.request.use(
  async (config) => {
    try {
      const { data: { session } } = await supabase.auth.getSession()
      if (session?.access_token) {
        config.headers.Authorization = `Bearer ${session.access_token}`
      }
    } catch (error) {
      console.error('Error getting session for API request:', error)
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor - handle errors
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Handle network errors
    if (!error.response) {
      console.error('Network error:', error.message)
      return Promise.reject({
        message: 'Unable to connect to server. Please check your internet connection.',
        code: 'NETWORK_ERROR'
      })
    }

    // Handle 401 Unauthorized - refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      
      try {
        const { data: { session }, error: refreshError } = await supabase.auth.refreshSession()
        
        if (refreshError || !session) {
          // Refresh failed, sign out user
          await supabase.auth.signOut()
          window.location.href = '/'
          return Promise.reject(error)
        }
        
        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${session.access_token}`
        return api(originalRequest)
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError)
        await supabase.auth.signOut()
        window.location.href = '/'
        return Promise.reject(error)
      }
    }

    // Handle specific HTTP errors
    if (error.response?.status === 429) {
      return Promise.reject({
        message: 'Too many requests. Please wait a moment and try again.',
        code: 'RATE_LIMIT_EXCEEDED',
        response: error.response
      })
    }

    if (error.response?.status >= 500) {
      return Promise.reject({
        message: 'Server error. Please try again later.',
        code: 'SERVER_ERROR',
        response: error.response
      })
    }

    // Return structured error
    return Promise.reject({
      message: error.response?.data?.message || error.message || 'An error occurred',
      code: error.response?.data?.code || 'UNKNOWN_ERROR',
      response: error.response
    })
  }
)

// Chat API with session support
export const chatAPI = {
  async sendMessage(userId, message, sessionId = null, currentTab = null) {
    const stored = localStorage.getItem('language')
    const language = ['en', 'fr', 'zh'].includes(stored) ? stored : 'en'
    try {
      const response = await api.post('/chat/send', {
        user_id: userId,
        message: message,
        session_id: sessionId,
        current_tab: currentTab,
        language,
      })
      return response.data
    } catch (error) {
      console.error('Send message error:', error)
      throw error
    }
  },

  async getHistory(userId, sessionId = null, limit = 50) {
    try {
      const params = { limit }
      if (sessionId) {
        params.session_id = sessionId
      }
      const response = await api.get(`/chat/history/${userId}`, { params })
      return response.data
    } catch (error) {
      console.error('Get history error:', error)
      throw error
    }
  },

  async getSessions(userId, limit = 20) {
    try {
      const response = await api.get(`/chat/sessions/${userId}`, {
        params: { limit }
      })
      return response.data
    } catch (error) {
      console.error('Get sessions error:', error)
      throw error
    }
  },

  async deleteSession(userId, sessionId) {
    try {
      await api.delete(`/chat/session/${userId}/${sessionId}`)
    } catch (error) {
      console.error('Delete session error:', error)
      throw error
    }
  },

  async clearHistory(userId) {
    try {
      await api.delete(`/chat/history/${userId}`)
    } catch (error) {
      console.error('Clear history error:', error)
      throw error
    }
  }
}

// Courses API
export const coursesAPI = {
  search: async (query = '', subject = null, limit = 50, term = null) => {
    try {
      const params = {}
      if (query) params.query = query
      if (subject) params.subject = subject
      if (term) params.term = term
      params.limit = limit

      const response = await api.get('/courses/search', { params })
      return response.data
    } catch (error) {
      console.error('Course search error:', error)
      throw error
    }
  },

  getTerms: async () => {
    try {
      const response = await api.get('/courses/terms')
      return response.data
    } catch (error) {
      console.error('Course terms error:', error)
      return { terms: [] }
    }
  },

  getDetails: async (subject, catalog) => {
    try {
      const response = await api.get(`/courses/${subject}/${catalog}`)
      return response.data
    } catch (error) {
      console.error('Course details error:', error)
      throw error
    }
  },
  
  getSubjects: async () => {
    try {
      const response = await api.get('/courses/subjects')
      return response.data
    } catch (error) {
      console.error('Subjects error:', error)
      throw error
    }
  },
}

// Users API
export const usersAPI = {
  createUser: async (userData) => {
    try {
      const response = await api.post('/users/', userData)
      return response.data
    } catch (error) {
      console.error('User creation error:', error)
      throw error
    }
  },
  
  getUser: async (userId) => {
    try {
      const response = await api.get(`/users/${userId}`)
      return response.data
    } catch (error) {
      console.error('Get user error:', error)
      throw error
    }
  },
  
  updateUser: async (userId, updates) => {
    try {
      // FIX: Removed verbose debug console.log statements that were
      // logging full request payloads and responses in production
      const response = await api.patch(`/users/${userId}`, updates)
      return response.data
    } catch (error) {
      console.error('Update user error:', error)
      throw error
    }
  },

  /**
   * Quebec Law 25 / GDPR data portability.
   * Returns the full personal-data dump for the authenticated user.
   * Backend: backend/api/routes/users.py → export_user_data
   */
  exportData: async (userId) => {
    const response = await api.get(`/users/${userId}/export`)
    return response.data
  },

  // ── Degree-planning course allocations ───────────────────────────────────
  // Which program a student counts a given course toward. Server-persisted
  // so it follows them across devices.
  getCourseAllocations: async (userId) => {
    const response = await api.get(`/users/${userId}/course-allocations`)
    return response.data?.allocations || {}
  },
  setCourseAllocation: async (userId, courseCode, programKey) => {
    const response = await api.put(`/users/${userId}/course-allocations`, {
      course_code: courseCode, program_key: programKey,
    })
    return response.data
  },
  deleteCourseAllocation: async (userId, courseCode) => {
    const response = await api.delete(
      `/users/${userId}/course-allocations/${encodeURIComponent(courseCode)}`
    )
    return response.data
  },
}

// Auth flags API
export const authAPI = {
  async getFlags() {
    try {
      const response = await api.get('/auth/flags')
      return response.data
    } catch {
      return { is_admin: false, is_mcgill_email: false }
    }
  },
  /**
   * Re-send the verification email for the *currently authenticated* user.
   * SEC FIX #1: the body is empty — backend derives user_id+email from the
   * JWT and uses a server-side allowlisted redirect URL. We no longer pass
   * those fields client-side because they were the attack vector that let
   * any caller send "verify your Symbolos account" mail from our domain
   * to any recipient with any redirect.
   */
  async sendVerification() {
    const response = await api.post('/auth/send-verification', {})
    return response.data
  },
  async verifyEmail(userId, token) {
    const response = await api.post('/auth/verify-email', { user_id: userId, token })
    return response.data
  },
  async checkVerified(userId) {
    const response = await api.get(`/auth/check-verified/${encodeURIComponent(userId)}`)
    return response.data
  },
}

export default api
