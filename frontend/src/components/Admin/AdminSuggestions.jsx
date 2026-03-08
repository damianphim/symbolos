import { useState, useEffect } from 'react'
import { FaCheck, FaTimes, FaFlag, FaClock } from 'react-icons/fa'
import { BASE_URL } from '../../lib/apiConfig'
import './AdminSuggestions.css'

// FIX F-04: Admin authentication is now performed server-side.
// The VITE_ADMIN_PASSWORD env var has been removed — the password is
// verified by the backend and never embedded in the JS bundle.

export default function AdminSuggestions() {
  const [authed, setAuthed] = useState(false)
  const [password, setPassword] = useState('')
  const [adminToken, setAdminToken] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [filter, setFilter] = useState('pending') // pending | all
  const [actionLoading, setActionLoading] = useState(null)
  const [error, setError] = useState(null)
  const [loginLoading, setLoginLoading] = useState(false)

  const login = async (e) => {
    e.preventDefault()
    setLoginLoading(true)
    setError(null)
    try {
      // FIX F-04: Verify password server-side; never compare client-side
      const res = await fetch(`${BASE_URL}/api/admin/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ secret: password }),
      })
      if (!res.ok) {
        setError('Incorrect password')
        return
      }
      const data = await res.json()
      setAdminToken(data.token)
      setAuthed(true)
    } catch {
      setError('Could not connect to server')
    } finally {
      setLoginLoading(false)
    }
  }

  const fetchSuggestions = async () => {
    try {
      const endpoint = filter === 'pending' ? '/api/suggestions/admin/pending' : '/api/suggestions/admin/all'
      const res = await fetch(`${BASE_URL}${endpoint}`, {
        headers: { 'X-Cron-Secret': adminToken },
      })
      if (!res.ok) {
        if (res.status === 401) {
          setError('Authentication failed. Check your admin credentials.')
          return
        }
        throw new Error()
      }
      const data = await res.json()
      setSuggestions(data.suggestions || [])
    } catch {
      setError('Failed to load suggestions')
    }
  }

  useEffect(() => {
    if (authed) fetchSuggestions()
  }, [authed, filter]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleReview = async (id, status) => {
    setActionLoading(id)
    try {
      const res = await fetch(`${BASE_URL}/api/suggestions/admin/${id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'X-Cron-Secret': adminToken,
        },
        body: JSON.stringify({ status }),
      })
      if (!res.ok) throw new Error()
      // Remove from list if filtering by pending
      if (filter === 'pending') {
        setSuggestions((prev) => prev.filter((s) => s.id !== id))
      } else {
        setSuggestions((prev) => prev.map((s) => s.id === id ? { ...s, status } : s))
      }
    } catch {
      setError('Failed to update suggestion')
    } finally {
      setActionLoading(null)
    }
  }

  if (!authed) {
    return (
      <div className="admin-login">
        <h2><FaFlag /> Admin — Prof Suggestions</h2>
        <form onSubmit={login}>
          <input
            type="password"
            placeholder="Admin password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="admin-input"
          />
          {error && <p className="admin-error">{error}</p>}
          <button type="submit" className="admin-btn-primary" disabled={loginLoading}>
            {loginLoading ? 'Verifying...' : 'Enter'}
          </button>
        </form>
      </div>
    )
  }

  const statusBadge = (s) => {
    if (s === 'pending') return <span className="badge badge-pending"><FaClock /> Pending</span>
    if (s === 'approved') return <span className="badge badge-approved"><FaCheck /> Approved</span>
    return <span className="badge badge-rejected"><FaTimes /> Rejected</span>
  }

  return (
    <div className="admin-page">
      <div className="admin-header">
        <h2><FaFlag /> Professor Suggestions</h2>
        <div className="admin-filter">
          <button
            className={`filter-btn ${filter === 'pending' ? 'active' : ''}`}
            onClick={() => setFilter('pending')}
          >
            Pending
          </button>
          <button
            className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
            onClick={() => setFilter('all')}
          >
            All
          </button>
        </div>
      </div>

      {error && <div className="admin-error-banner">{error}</div>}

      {suggestions.length === 0 ? (
        <div className="admin-empty">No {filter === 'pending' ? 'pending' : ''} suggestions.</div>
      ) : (
        <div className="suggestions-list">
          {suggestions.map((s) => (
            <div key={s.id} className={`suggestion-card ${s.status}`}>
              <div className="suggestion-info">
                <div className="suggestion-course">{s.course_code}</div>
                <div className="suggestion-names">
                  <span className="name-label">Current:</span>
                  <span className="name-value current">{s.current_name || '—'}</span>
                  <span className="name-arrow">→</span>
                  <span className="name-label">Suggested:</span>
                  <span className="name-value suggested">{s.suggested_name}</span>
                </div>
                <div className="suggestion-meta">
                  {statusBadge(s.status)} &nbsp;·&nbsp;
                  {new Date(s.created_at).toLocaleDateString()} &nbsp;·&nbsp;
                  <span className="user-id">User: {s.user_id?.slice(0, 8)}…</span>
                </div>
              </div>

              {s.status === 'pending' && (
                <div className="suggestion-actions">
                  <button
                    className="action-btn approve"
                    disabled={actionLoading === s.id}
                    onClick={() => handleReview(s.id, 'approved')}
                  >
                    <FaCheck /> Approve
                  </button>
                  <button
                    className="action-btn reject"
                    disabled={actionLoading === s.id}
                    onClick={() => handleReview(s.id, 'rejected')}
                  >
                    <FaTimes /> Reject
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
