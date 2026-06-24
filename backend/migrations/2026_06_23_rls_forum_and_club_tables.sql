-- ────────────────────────────────────────────────────────────────────────────
-- 2026-06-23 — RLS for forum, club sub-tables, and other uncovered tables
--
-- The Supabase anon key is public (embedded in the JS bundle).  Any table
-- without RLS can be read/written directly via PostgREST, bypassing the
-- backend's auth, sanitisation, and business logic.
--
-- Tables covered here (all were missing RLS):
--   club_managers, club_subscriptions, club_join_requests,
--   club_manager_requests, club_events, club_announcements,
--   club_submissions, forum_posts, forum_replies,
--   forum_post_likes, forum_reply_likes
--
-- Tables intentionally left without user-scoped RLS:
--   rate_limits, seen_resend_events   — server-side only (service_role)
--   degree_programs, requirement_blocks, requirement_courses — read-only seed
-- ────────────────────────────────────────────────────────────────────────────


-- ══════════════════════════════════════════════════════════════════════════════
-- CLUB SUB-TABLES
-- ══════════════════════════════════════════════════════════════════════════════

-- ── club_managers ─────────────────────────────────────────────────────────────
-- Managers can see/manage their own rows; club owners see all rows for their club.
ALTER TABLE club_managers ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_managers_select" ON club_managers;
DROP POLICY IF EXISTS "club_managers_insert" ON club_managers;
DROP POLICY IF EXISTS "club_managers_delete" ON club_managers;

CREATE POLICY "club_managers_select"
ON club_managers FOR SELECT
TO authenticated
USING (
  user_id = auth.uid()                    -- own manager row
  OR is_club_manager(club_id)             -- club owner/admin can see all managers
);

CREATE POLICY "club_managers_insert"
ON club_managers FOR INSERT
TO authenticated
WITH CHECK (is_club_manager(club_id));

CREATE POLICY "club_managers_delete"
ON club_managers FOR DELETE
TO authenticated
USING (is_club_manager(club_id));


-- ── club_subscriptions ────────────────────────────────────────────────────────
ALTER TABLE club_subscriptions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_subscriptions_select_own" ON club_subscriptions;
DROP POLICY IF EXISTS "club_subscriptions_insert_own" ON club_subscriptions;
DROP POLICY IF EXISTS "club_subscriptions_delete_own" ON club_subscriptions;

CREATE POLICY "club_subscriptions_select_own"
ON club_subscriptions FOR SELECT
TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "club_subscriptions_insert_own"
ON club_subscriptions FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "club_subscriptions_delete_own"
ON club_subscriptions FOR DELETE
TO authenticated
USING (user_id = auth.uid());


-- ── club_join_requests ────────────────────────────────────────────────────────
ALTER TABLE club_join_requests ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_join_requests_select" ON club_join_requests;
DROP POLICY IF EXISTS "club_join_requests_insert" ON club_join_requests;
DROP POLICY IF EXISTS "club_join_requests_delete" ON club_join_requests;

CREATE POLICY "club_join_requests_select"
ON club_join_requests FOR SELECT
TO authenticated
USING (
  user_id = auth.uid()
  OR is_club_manager(club_id)
);

CREATE POLICY "club_join_requests_insert"
ON club_join_requests FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "club_join_requests_delete"
ON club_join_requests FOR DELETE
TO authenticated
USING (user_id = auth.uid() OR is_club_manager(club_id));


-- ── club_manager_requests ─────────────────────────────────────────────────────
ALTER TABLE club_manager_requests ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_manager_requests_select" ON club_manager_requests;
DROP POLICY IF EXISTS "club_manager_requests_insert" ON club_manager_requests;
DROP POLICY IF EXISTS "club_manager_requests_delete" ON club_manager_requests;

CREATE POLICY "club_manager_requests_select"
ON club_manager_requests FOR SELECT
TO authenticated
USING (
  user_id = auth.uid()
  OR is_club_manager(club_id)
);

CREATE POLICY "club_manager_requests_insert"
ON club_manager_requests FOR INSERT
TO authenticated
WITH CHECK (is_club_manager(club_id));

CREATE POLICY "club_manager_requests_delete"
ON club_manager_requests FOR DELETE
TO authenticated
USING (is_club_manager(club_id));


-- ── club_events ───────────────────────────────────────────────────────────────
-- Public events are visible to all authenticated users; private-club events
-- are only visible to members and managers.
ALTER TABLE club_events ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_events_select" ON club_events;
DROP POLICY IF EXISTS "club_events_insert" ON club_events;
DROP POLICY IF EXISTS "club_events_update" ON club_events;
DROP POLICY IF EXISTS "club_events_delete" ON club_events;

CREATE POLICY "club_events_select"
ON club_events FOR SELECT
TO authenticated
USING (
  -- Event belongs to a public verified club, OR caller is a member/manager
  EXISTS (
    SELECT 1 FROM clubs c
    WHERE c.id = club_id
      AND c.is_verified = true
      AND COALESCE(c.is_private, false) = false
  )
  OR is_club_manager(club_id)
  OR EXISTS (
    SELECT 1 FROM user_clubs uc
    WHERE uc.club_id = club_events.club_id AND uc.user_id = auth.uid()
  )
);

CREATE POLICY "club_events_insert"
ON club_events FOR INSERT
TO authenticated
WITH CHECK (is_club_manager(club_id));

CREATE POLICY "club_events_update"
ON club_events FOR UPDATE
TO authenticated
USING (is_club_manager(club_id))
WITH CHECK (is_club_manager(club_id));

CREATE POLICY "club_events_delete"
ON club_events FOR DELETE
TO authenticated
USING (is_club_manager(club_id));


-- ── club_announcements ────────────────────────────────────────────────────────
ALTER TABLE club_announcements ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_announcements_select" ON club_announcements;
DROP POLICY IF EXISTS "club_announcements_insert" ON club_announcements;
DROP POLICY IF EXISTS "club_announcements_update" ON club_announcements;
DROP POLICY IF EXISTS "club_announcements_delete" ON club_announcements;

CREATE POLICY "club_announcements_select"
ON club_announcements FOR SELECT
TO authenticated
USING (
  EXISTS (
    SELECT 1 FROM clubs c
    WHERE c.id = club_id
      AND c.is_verified = true
      AND COALESCE(c.is_private, false) = false
  )
  OR is_club_manager(club_id)
  OR EXISTS (
    SELECT 1 FROM user_clubs uc
    WHERE uc.club_id = club_announcements.club_id AND uc.user_id = auth.uid()
  )
);

CREATE POLICY "club_announcements_insert"
ON club_announcements FOR INSERT
TO authenticated
WITH CHECK (is_club_manager(club_id));

CREATE POLICY "club_announcements_update"
ON club_announcements FOR UPDATE
TO authenticated
USING (is_club_manager(club_id))
WITH CHECK (is_club_manager(club_id));

CREATE POLICY "club_announcements_delete"
ON club_announcements FOR DELETE
TO authenticated
USING (is_club_manager(club_id));


-- ── club_submissions ──────────────────────────────────────────────────────────
-- Admin-reviewed pending clubs: submitter sees their own row; admins use service_role.
ALTER TABLE club_submissions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "club_submissions_select_own" ON club_submissions;
DROP POLICY IF EXISTS "club_submissions_insert_own" ON club_submissions;

CREATE POLICY "club_submissions_select_own"
ON club_submissions FOR SELECT
TO authenticated
USING (submitted_by = auth.uid());

CREATE POLICY "club_submissions_insert_own"
ON club_submissions FOR INSERT
TO authenticated
WITH CHECK (submitted_by = auth.uid());


-- ══════════════════════════════════════════════════════════════════════════════
-- FORUM TABLES
-- ══════════════════════════════════════════════════════════════════════════════

-- ── forum_posts ───────────────────────────────────────────────────────────────
-- All authenticated users can read. Authors can update/delete their own posts.
-- Anon role gets no access (no anonymous forum reads via the bundle key).
ALTER TABLE forum_posts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "forum_posts_select_auth" ON forum_posts;
DROP POLICY IF EXISTS "forum_posts_insert_own"  ON forum_posts;
DROP POLICY IF EXISTS "forum_posts_update_own"  ON forum_posts;
DROP POLICY IF EXISTS "forum_posts_delete_own"  ON forum_posts;

CREATE POLICY "forum_posts_select_auth"
ON forum_posts FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "forum_posts_insert_own"
ON forum_posts FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "forum_posts_update_own"
ON forum_posts FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "forum_posts_delete_own"
ON forum_posts FOR DELETE
TO authenticated
USING (user_id = auth.uid());


-- ── forum_replies ─────────────────────────────────────────────────────────────
ALTER TABLE forum_replies ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "forum_replies_select_auth" ON forum_replies;
DROP POLICY IF EXISTS "forum_replies_insert_own"  ON forum_replies;
DROP POLICY IF EXISTS "forum_replies_update_own"  ON forum_replies;
DROP POLICY IF EXISTS "forum_replies_delete_own"  ON forum_replies;

CREATE POLICY "forum_replies_select_auth"
ON forum_replies FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "forum_replies_insert_own"
ON forum_replies FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "forum_replies_update_own"
ON forum_replies FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "forum_replies_delete_own"
ON forum_replies FOR DELETE
TO authenticated
USING (user_id = auth.uid());


-- ── forum_post_likes ──────────────────────────────────────────────────────────
ALTER TABLE forum_post_likes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "forum_post_likes_select_auth" ON forum_post_likes;
DROP POLICY IF EXISTS "forum_post_likes_insert_own"  ON forum_post_likes;
DROP POLICY IF EXISTS "forum_post_likes_delete_own"  ON forum_post_likes;

CREATE POLICY "forum_post_likes_select_auth"
ON forum_post_likes FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "forum_post_likes_insert_own"
ON forum_post_likes FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "forum_post_likes_delete_own"
ON forum_post_likes FOR DELETE
TO authenticated
USING (user_id = auth.uid());


-- ── forum_reply_likes ─────────────────────────────────────────────────────────
ALTER TABLE forum_reply_likes ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "forum_reply_likes_select_auth" ON forum_reply_likes;
DROP POLICY IF EXISTS "forum_reply_likes_insert_own"  ON forum_reply_likes;
DROP POLICY IF EXISTS "forum_reply_likes_delete_own"  ON forum_reply_likes;

CREATE POLICY "forum_reply_likes_select_auth"
ON forum_reply_likes FOR SELECT
TO authenticated
USING (true);

CREATE POLICY "forum_reply_likes_insert_own"
ON forum_reply_likes FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "forum_reply_likes_delete_own"
ON forum_reply_likes FOR DELETE
TO authenticated
USING (user_id = auth.uid());
