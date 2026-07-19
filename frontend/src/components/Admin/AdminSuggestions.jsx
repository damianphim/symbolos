import { useState, useEffect } from 'react'
import { FaCheck, FaTimes, FaFlag, FaClock, FaChartBar, FaUsers, FaComments, FaUpload } from 'react-icons/fa'
import { BASE_URL } from '../../lib/apiConfig'
import './AdminSuggestions.css'

export default function AdminSuggestions() {
  const [authed, setAuthed] = useState(false)
  const [password, setPassword] = useState('')
  const [adminToken, setAdminToken] = useState('')
  const [tab, setTab] = useState('stats') // stats | suggestions
  const [suggestions, setSuggestions] = useState([])
  const [filter, setFilter] = useState('pending')
  const [actionLoading, setActionLoading] = useState(null)
  const [error, setError] = useState(null)
  const [loginLoading, setLoginLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [statsLoading, setStatsLoading] = useState(false)
  const [feedback, setFeedback] = useState([])
  const [feedbackLoading, setFeedbackLoading] = useState(false)

  const login = async (e) => {
    e.preventDefault()
    setLoginLoading(true)
    setError(null)
    try {
      const res = await fetch(`${BASE_URL}/api/admin/verify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ secret: password }),
      })
      if (!res.ok) { setError('Incorrect password'); return }
      const data = await res.json()
      setAdminToken(data.token)
      setAuthed(true)
    } catch {
      setError('Could not connect to server')
    } finally {
      setLoginLoading(false)
    }
  }

  const fetchStats = async () => {
    setStatsLoading(true)
    try {
      const res = await fetch(`${BASE_URL}/api/admin/stats`, {
        headers: { 'X-Cron-Secret': adminToken },
      })
      if (!res.ok) throw new Error()
      setStats(await res.json())
    } catch {
      setError('Failed to load stats')
    } finally {
      setStatsLoading(false)
    }
  }

  const fetchSuggestions = async () => {
    try {
      const endpoint = filter === 'pending' ? '/api/suggestions/admin/pending' : '/api/suggestions/admin/all'
      const res = await fetch(`${BASE_URL}${endpoint}`, {
        headers: { 'X-Cron-Secret': adminToken },
      })
      if (!res.ok) {
        if (res.status === 401) { setError('Authentication failed.'); return }
        throw new Error()
      }
      setSuggestions((await res.json()).suggestions || [])
    } catch {
      setError('Failed to load suggestions')
    }
  }

  const fetchFeedback = async () => {
    setFeedbackLoading(true)
    try {
      const res = await fetch(`${BASE_URL}/api/feedback/admin`, {
        headers: { 'X-Cron-Secret': adminToken },
      })
      if (res.ok) setFeedback((await res.json()).items || [])
    } catch {
      // feedback admin endpoint may not exist yet — silent
    } finally {
      setFeedbackLoading(false)
    }
  }

  useEffect(() => {
    if (!authed) return
    if (tab === 'stats') fetchStats()
    if (tab === 'suggestions') fetchSuggestions()
    if (tab === 'feedback') fetchFeedback()
  }, [authed, tab, filter]) // eslint-disable-line react-hooks/exhaustive-deps

  const handleReview = async (id, status) => {
    setActionLoading(id)
    try {
      const res = await fetch(`${BASE_URL}/api/suggestions/admin/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json', 'X-Cron-Secret': adminToken },
        body: JSON.stringify({ status }),
      })
      if (!res.ok) throw new Error()
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
        <h2><FaFlag /> Admin Panel</h2>
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

  const StatCard = ({ icon, label, value, sub }) => (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-body">
        <div className="stat-value">{value ?? '-'}</div>
        <div className="stat-label">{label}</div>
        {sub && <div className="stat-sub">{sub}</div>}
      </div>
    </div>
  )

  return (
    <div className="admin-page">
      {error && <div className="admin-error-banner">{error}</div>}

      <div className="admin-header">
        <h2><FaFlag /> Admin Panel</h2>
        <div className="admin-tabs">
          <button className={`filter-btn ${tab === 'stats' ? 'active' : ''}`} onClick={() => setTab('stats')}>
            <FaChartBar /> Stats
          </button>
          <button className={`filter-btn ${tab === 'suggestions' ? 'active' : ''}`} onClick={() => setTab('suggestions')}>
            <FaCheck /> Suggestions
          </button>
          <button className={`filter-btn ${tab === 'feedback' ? 'active' : ''}`} onClick={() => setTab('feedback')}>
            Feedback
          </button>
        </div>
      </div>

      {tab === 'stats' && (
        statsLoading ? <div className="admin-empty">Loading…</div> : stats ? (
          <div className="stats-dashboard">
            <div className="stats-section-label">Users</div>
            <div className="stats-grid">
              <StatCard icon={<FaUsers />} label="Total users" value={stats.users.total} />
              <StatCard icon={<FaUsers />} label="New this week" value={stats.users.new_7d} sub={`${stats.users.new_30d} this month`} />
              <StatCard icon={<FaUsers />} label="Active (7d)" value={stats.users.active_7d} sub="sent ≥1 message" />
            </div>

            <div className="stats-section-label">Messages</div>
            <div className="stats-grid">
              <StatCard icon={<FaComments />} label="Total messages" value={stats.messages.total} />
              <StatCard icon={<FaComments />} label="Messages (7d)" value={stats.messages.last_7d} sub={`${stats.messages.last_30d} in 30d`} />
              <StatCard icon={<FaComments />} label="Avg / active user" value={stats.messages.avg_per_active_user} sub="past 7 days" />
            </div>

            <div className="stats-section-label">Features</div>
            <div className="stats-grid">
              <StatCard icon={<FaUpload />} label="Transcript uploads" value={stats.features.transcript_uploads} />
              <StatCard icon={<FaChartBar />} label="Advisor cards" value={stats.features.advisor_cards} />
              <StatCard icon={<FaComments />} label="Forum posts" value={stats.features.forum_posts} />
              <StatCard icon={<FaUsers />} label="Club joins" value={stats.features.club_joins} />
              <StatCard icon={<FaFlag />} label="Feedback" value={stats.features.feedback_total} sub={`${stats.features.feedback_7d} this week`} />
            </div>
          </div>
        ) : null
      )}

      {tab === 'suggestions' && (
        <>
          <div className="admin-filter">
            <button className={`filter-btn ${filter === 'pending' ? 'active' : ''}`} onClick={() => setFilter('pending')}>Pending</button>
            <button className={`filter-btn ${filter === 'all' ? 'active' : ''}`} onClick={() => setFilter('all')}>All</button>
          </div>
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
                      <span className="name-value current">{s.current_name || '-'}</span>
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
                      <button className="action-btn approve" disabled={actionLoading === s.id} onClick={() => handleReview(s.id, 'approved')}>
                        <FaCheck /> Approve
                      </button>
                      <button className="action-btn reject" disabled={actionLoading === s.id} onClick={() => handleReview(s.id, 'rejected')}>
                        <FaTimes /> Reject
                      </button>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </>
      )}

      {tab === 'feedback' && (
        feedbackLoading ? <div className="admin-empty">Loading…</div> :
        feedback.length === 0 ? (
          <div className="admin-empty">No feedback yet.</div>
        ) : (
          <div className="suggestions-list">
            {feedback.map((f) => (
              <div key={f.id} className="suggestion-card pending">
                <div className="suggestion-info">
                  <div className="suggestion-course">{f.kind} {f.course ? `· ${f.course}` : ''}</div>
                  <div className="suggestion-names" style={{ display: 'block', whiteSpace: 'pre-wrap' }}>{f.message}</div>
                  <div className="suggestion-meta">
                    {new Date(f.created_at).toLocaleDateString()} &nbsp;·&nbsp;
                    <span className="user-id">{f.user_email || f.user_id?.slice(0, 8) + '…'}</span>
                    {f.page && <> &nbsp;·&nbsp; {f.page}</>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      )}
    </div>
  )
}
