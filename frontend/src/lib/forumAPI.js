import { BASE_URL } from './apiConfig'
import { supabase } from './supabase'

async function authHeaders() {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  return { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }
}

const forumAPI = {
  // ── Posts ────────────────────────────────────────────────────────

  async getPosts({ category, sort = 'hot', search, limit = 30, offset = 0 } = {}) {
    const params = new URLSearchParams()
    if (category && category !== 'all') params.set('category', category)
    if (sort)   params.set('sort', sort)
    if (search) params.set('search', search)
    params.set('limit', limit)
    params.set('offset', offset)

    const res = await fetch(`${BASE_URL}/api/forum/posts?${params}`, {
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to fetch posts')
    return res.json()
  },

  async createPost({ author, avatar_color, category, title, body, tags }) {
    const res = await fetch(`${BASE_URL}/api/forum/posts`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ author, avatar_color, category, title, body, tags }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to create post')
    }
    return res.json()
  },

  async deletePost(postId) {
    const res = await fetch(`${BASE_URL}/api/forum/posts/${postId}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to delete post')
    return res.json()
  },

  // ── Replies ──────────────────────────────────────────────────────

  async getReplies(postId) {
    const res = await fetch(`${BASE_URL}/api/forum/posts/${postId}/replies`, {
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to fetch replies')
    return res.json()
  },

  async createReply(postId, { author, avatar_color, body }) {
    const res = await fetch(`${BASE_URL}/api/forum/posts/${postId}/replies`, {
      method: 'POST',
      headers: await authHeaders(),
      body: JSON.stringify({ author, avatar_color, body }),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to create reply')
    }
    return res.json()
  },

  async deleteReply(replyId) {
    const res = await fetch(`${BASE_URL}/api/forum/replies/${replyId}`, {
      method: 'DELETE',
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to delete reply')
    return res.json()
  },

  // ── Likes ────────────────────────────────────────────────────────

  async togglePostLike(postId) {
    const res = await fetch(`${BASE_URL}/api/forum/posts/${postId}/like`, {
      method: 'POST',
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to toggle like')
    return res.json()
  },

  async toggleReplyLike(replyId) {
    const res = await fetch(`${BASE_URL}/api/forum/replies/${replyId}/like`, {
      method: 'POST',
      headers: await authHeaders(),
    })
    if (!res.ok) throw new Error('Failed to toggle like')
    return res.json()
  },
}

export default forumAPI
