-- ============================================================
-- RLS (Row Level Security) policies for all user-scoped tables
-- ============================================================
-- Run this migration in the Supabase SQL editor or via supabase db push.
-- The anon/authenticated role is used by the user-scoped client (get_user_supabase).
-- The service_role key bypasses RLS entirely — used only for admin/cron operations.
--
-- IMPORTANT: Also add SUPABASE_ANON_KEY to your production environment variables.
-- IMPORTANT: After applying, revoke direct INSERT/UPDATE/DELETE from anon on the
--            courses table (read-only for students).
-- ============================================================


-- ── Helper: enable RLS on a table (idempotent) ───────────────────────────────
-- Just run ALTER TABLE ... ENABLE ROW LEVEL SECURITY; for each table below.


-- ============================================================
-- 1. users
-- ============================================================
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only read and write their own profile row.
DROP POLICY IF EXISTS "users_select_own"  ON users;
DROP POLICY IF EXISTS "users_insert_own"  ON users;
DROP POLICY IF EXISTS "users_update_own"  ON users;
DROP POLICY IF EXISTS "users_delete_own"  ON users;

CREATE POLICY "users_select_own"
  ON users FOR SELECT
  USING (id = auth.uid());

CREATE POLICY "users_insert_own"
  ON users FOR INSERT
  WITH CHECK (id = auth.uid());

CREATE POLICY "users_update_own"
  ON users FOR UPDATE
  USING (id = auth.uid())
  WITH CHECK (id = auth.uid());

CREATE POLICY "users_delete_own"
  ON users FOR DELETE
  USING (id = auth.uid());


-- ============================================================
-- 2. advisor_cards
-- ============================================================
ALTER TABLE advisor_cards ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "advisor_cards_select_own"  ON advisor_cards;
DROP POLICY IF EXISTS "advisor_cards_insert_own"  ON advisor_cards;
DROP POLICY IF EXISTS "advisor_cards_update_own"  ON advisor_cards;
DROP POLICY IF EXISTS "advisor_cards_delete_own"  ON advisor_cards;

CREATE POLICY "advisor_cards_select_own"
  ON advisor_cards FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "advisor_cards_insert_own"
  ON advisor_cards FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "advisor_cards_update_own"
  ON advisor_cards FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "advisor_cards_delete_own"
  ON advisor_cards FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 3. chat_messages
-- ============================================================
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "chat_messages_select_own"  ON chat_messages;
DROP POLICY IF EXISTS "chat_messages_insert_own"  ON chat_messages;
DROP POLICY IF EXISTS "chat_messages_update_own"  ON chat_messages;
DROP POLICY IF EXISTS "chat_messages_delete_own"  ON chat_messages;

CREATE POLICY "chat_messages_select_own"
  ON chat_messages FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "chat_messages_insert_own"
  ON chat_messages FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "chat_messages_update_own"
  ON chat_messages FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "chat_messages_delete_own"
  ON chat_messages FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 4. favorites
-- ============================================================
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "favorites_select_own"  ON favorites;
DROP POLICY IF EXISTS "favorites_insert_own"  ON favorites;
DROP POLICY IF EXISTS "favorites_update_own"  ON favorites;
DROP POLICY IF EXISTS "favorites_delete_own"  ON favorites;

CREATE POLICY "favorites_select_own"
  ON favorites FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "favorites_insert_own"
  ON favorites FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "favorites_update_own"
  ON favorites FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "favorites_delete_own"
  ON favorites FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 5. prof_suggestions
-- ============================================================
ALTER TABLE prof_suggestions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "prof_suggestions_select_own"    ON prof_suggestions;
DROP POLICY IF EXISTS "prof_suggestions_insert_own"    ON prof_suggestions;
DROP POLICY IF EXISTS "prof_suggestions_delete_own"    ON prof_suggestions;

-- Users can see and submit their own suggestions only.
-- Admins use service_role which bypasses RLS.
CREATE POLICY "prof_suggestions_select_own"
  ON prof_suggestions FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "prof_suggestions_insert_own"
  ON prof_suggestions FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "prof_suggestions_delete_own"
  ON prof_suggestions FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 6. user_clubs
-- ============================================================
ALTER TABLE user_clubs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "user_clubs_select_own"  ON user_clubs;
DROP POLICY IF EXISTS "user_clubs_insert_own"  ON user_clubs;
DROP POLICY IF EXISTS "user_clubs_update_own"  ON user_clubs;
DROP POLICY IF EXISTS "user_clubs_delete_own"  ON user_clubs;

CREATE POLICY "user_clubs_select_own"
  ON user_clubs FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "user_clubs_insert_own"
  ON user_clubs FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "user_clubs_update_own"
  ON user_clubs FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "user_clubs_delete_own"
  ON user_clubs FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 7. current_courses
-- ============================================================
ALTER TABLE current_courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "current_courses_select_own"  ON current_courses;
DROP POLICY IF EXISTS "current_courses_insert_own"  ON current_courses;
DROP POLICY IF EXISTS "current_courses_update_own"  ON current_courses;
DROP POLICY IF EXISTS "current_courses_delete_own"  ON current_courses;

CREATE POLICY "current_courses_select_own"
  ON current_courses FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "current_courses_insert_own"
  ON current_courses FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "current_courses_update_own"
  ON current_courses FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "current_courses_delete_own"
  ON current_courses FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 8. completed_courses
-- ============================================================
ALTER TABLE completed_courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "completed_courses_select_own"  ON completed_courses;
DROP POLICY IF EXISTS "completed_courses_insert_own"  ON completed_courses;
DROP POLICY IF EXISTS "completed_courses_update_own"  ON completed_courses;
DROP POLICY IF EXISTS "completed_courses_delete_own"  ON completed_courses;

CREATE POLICY "completed_courses_select_own"
  ON completed_courses FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "completed_courses_insert_own"
  ON completed_courses FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "completed_courses_update_own"
  ON completed_courses FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "completed_courses_delete_own"
  ON completed_courses FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 9. calendar_events
-- ============================================================
ALTER TABLE calendar_events ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "calendar_events_select_own"  ON calendar_events;
DROP POLICY IF EXISTS "calendar_events_insert_own"  ON calendar_events;
DROP POLICY IF EXISTS "calendar_events_update_own"  ON calendar_events;
DROP POLICY IF EXISTS "calendar_events_delete_own"  ON calendar_events;

CREATE POLICY "calendar_events_select_own"
  ON calendar_events FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "calendar_events_insert_own"
  ON calendar_events FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "calendar_events_update_own"
  ON calendar_events FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "calendar_events_delete_own"
  ON calendar_events FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 10. notification_queue
-- ============================================================
ALTER TABLE notification_queue ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "notification_queue_select_own"  ON notification_queue;
DROP POLICY IF EXISTS "notification_queue_insert_own"  ON notification_queue;
DROP POLICY IF EXISTS "notification_queue_update_own"  ON notification_queue;
DROP POLICY IF EXISTS "notification_queue_delete_own"  ON notification_queue;

CREATE POLICY "notification_queue_select_own"
  ON notification_queue FOR SELECT
  USING (user_id = auth.uid());

CREATE POLICY "notification_queue_insert_own"
  ON notification_queue FOR INSERT
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "notification_queue_update_own"
  ON notification_queue FOR UPDATE
  USING (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

CREATE POLICY "notification_queue_delete_own"
  ON notification_queue FOR DELETE
  USING (user_id = auth.uid());


-- ============================================================
-- 11. courses (read-only for authenticated users; no user_id column)
-- ============================================================
ALTER TABLE courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "courses_select_all"  ON courses;

-- All authenticated users can read the courses catalogue.
-- No INSERT/UPDATE/DELETE policies — only service_role (admin/cron) can write.
CREATE POLICY "courses_select_all"
  ON courses FOR SELECT
  TO authenticated
  USING (true);


-- ============================================================
-- 12. clubs (read-only for authenticated users)
-- ============================================================
ALTER TABLE clubs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "clubs_select_all"  ON clubs;

CREATE POLICY "clubs_select_all"
  ON clubs FOR SELECT
  TO authenticated
  USING (true);


-- ============================================================
-- Unique constraint: verification_tokens (prevents token collision)
-- ============================================================
-- Uncomment if not already applied:
-- ALTER TABLE verification_tokens
--   ADD CONSTRAINT verification_tokens_token_key UNIQUE (token);
