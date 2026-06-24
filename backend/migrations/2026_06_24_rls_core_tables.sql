-- ─────────────────────────────────────────────────────────────────────────────
-- 2026-06-24 — RLS for core user-data tables
--
-- The club/forum tables received RLS in earlier migrations. This migration
-- covers the remaining unprotected tables that hold personal user data:
-- users, chat_messages, advisor_cards, favorites, completed_courses,
-- current_courses, calendar_events, notification_queue, user_clubs,
-- newsletter_subscriptions, prof_suggestions, and service-role-only tables.
--
-- Reference/catalogue tables (courses, degree_programs, requirement_blocks,
-- requirement_courses) are also locked to read-only for authenticated users.
-- ─────────────────────────────────────────────────────────────────────────────


-- ── users ─────────────────────────────────────────────────────────────────────
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "users_select_own"  ON users;
DROP POLICY IF EXISTS "users_update_own"  ON users;
DROP POLICY IF EXISTS "users_insert_own"  ON users;

CREATE POLICY "users_select_own" ON users
FOR SELECT TO authenticated
USING (id = auth.uid());

CREATE POLICY "users_update_own" ON users
FOR UPDATE TO authenticated
USING (id = auth.uid())
WITH CHECK (id = auth.uid());

-- Insert is done by service_role on signup; authenticated row is created before
-- the user can authenticate, so no user-facing INSERT policy is needed.


-- ── chat_messages ─────────────────────────────────────────────────────────────
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "chat_messages_select_own" ON chat_messages;
DROP POLICY IF EXISTS "chat_messages_insert_own" ON chat_messages;
DROP POLICY IF EXISTS "chat_messages_delete_own" ON chat_messages;

CREATE POLICY "chat_messages_select_own" ON chat_messages
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "chat_messages_insert_own" ON chat_messages
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "chat_messages_delete_own" ON chat_messages
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── advisor_cards ─────────────────────────────────────────────────────────────
ALTER TABLE advisor_cards ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "advisor_cards_select_own" ON advisor_cards;
DROP POLICY IF EXISTS "advisor_cards_insert_own" ON advisor_cards;
DROP POLICY IF EXISTS "advisor_cards_update_own" ON advisor_cards;
DROP POLICY IF EXISTS "advisor_cards_delete_own" ON advisor_cards;

CREATE POLICY "advisor_cards_select_own" ON advisor_cards
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "advisor_cards_insert_own" ON advisor_cards
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "advisor_cards_update_own" ON advisor_cards
FOR UPDATE TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "advisor_cards_delete_own" ON advisor_cards
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── favorites ─────────────────────────────────────────────────────────────────
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "favorites_select_own" ON favorites;
DROP POLICY IF EXISTS "favorites_insert_own" ON favorites;
DROP POLICY IF EXISTS "favorites_delete_own" ON favorites;

CREATE POLICY "favorites_select_own" ON favorites
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "favorites_insert_own" ON favorites
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "favorites_delete_own" ON favorites
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── completed_courses ─────────────────────────────────────────────────────────
ALTER TABLE completed_courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "completed_courses_select_own" ON completed_courses;
DROP POLICY IF EXISTS "completed_courses_insert_own" ON completed_courses;
DROP POLICY IF EXISTS "completed_courses_update_own" ON completed_courses;
DROP POLICY IF EXISTS "completed_courses_delete_own" ON completed_courses;

CREATE POLICY "completed_courses_select_own" ON completed_courses
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "completed_courses_insert_own" ON completed_courses
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "completed_courses_update_own" ON completed_courses
FOR UPDATE TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "completed_courses_delete_own" ON completed_courses
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── current_courses ───────────────────────────────────────────────────────────
ALTER TABLE current_courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "current_courses_select_own" ON current_courses;
DROP POLICY IF EXISTS "current_courses_insert_own" ON current_courses;
DROP POLICY IF EXISTS "current_courses_update_own" ON current_courses;
DROP POLICY IF EXISTS "current_courses_delete_own" ON current_courses;

CREATE POLICY "current_courses_select_own" ON current_courses
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "current_courses_insert_own" ON current_courses
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "current_courses_update_own" ON current_courses
FOR UPDATE TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "current_courses_delete_own" ON current_courses
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── calendar_events ───────────────────────────────────────────────────────────
ALTER TABLE calendar_events ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "calendar_events_select_own" ON calendar_events;
DROP POLICY IF EXISTS "calendar_events_insert_own" ON calendar_events;
DROP POLICY IF EXISTS "calendar_events_update_own" ON calendar_events;
DROP POLICY IF EXISTS "calendar_events_delete_own" ON calendar_events;

CREATE POLICY "calendar_events_select_own" ON calendar_events
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "calendar_events_insert_own" ON calendar_events
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "calendar_events_update_own" ON calendar_events
FOR UPDATE TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "calendar_events_delete_own" ON calendar_events
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── notification_queue ────────────────────────────────────────────────────────
-- Service-role only: users never read/write this directly.
ALTER TABLE notification_queue ENABLE ROW LEVEL SECURITY;
-- No policies — service_role bypasses RLS; no authenticated access needed.


-- ── user_clubs ────────────────────────────────────────────────────────────────
ALTER TABLE user_clubs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "user_clubs_select" ON user_clubs;
DROP POLICY IF EXISTS "user_clubs_insert_own" ON user_clubs;
DROP POLICY IF EXISTS "user_clubs_update_manager" ON user_clubs;
DROP POLICY IF EXISTS "user_clubs_delete_own" ON user_clubs;

-- Members can see club membership (needed to display member counts / rosters)
CREATE POLICY "user_clubs_select" ON user_clubs
FOR SELECT TO authenticated
USING (
    user_id = auth.uid()
    OR EXISTS (
        SELECT 1 FROM club_managers cm
        WHERE cm.club_id = user_clubs.club_id AND cm.user_id = auth.uid()
    )
);

CREATE POLICY "user_clubs_insert_own" ON user_clubs
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

-- Managers can update roles within their club
CREATE POLICY "user_clubs_update_manager" ON user_clubs
FOR UPDATE TO authenticated
USING (
    user_id = auth.uid()
    OR EXISTS (
        SELECT 1 FROM club_managers cm
        WHERE cm.club_id = user_clubs.club_id AND cm.user_id = auth.uid()
    )
);

CREATE POLICY "user_clubs_delete_own" ON user_clubs
FOR DELETE TO authenticated
USING (
    user_id = auth.uid()
    OR EXISTS (
        SELECT 1 FROM club_managers cm
        WHERE cm.club_id = user_clubs.club_id AND cm.user_id = auth.uid()
    )
);


-- ── newsletter_subscriptions ──────────────────────────────────────────────────
ALTER TABLE newsletter_subscriptions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "newsletter_subscriptions_select_own" ON newsletter_subscriptions;
DROP POLICY IF EXISTS "newsletter_subscriptions_insert_own" ON newsletter_subscriptions;
DROP POLICY IF EXISTS "newsletter_subscriptions_update_own" ON newsletter_subscriptions;
DROP POLICY IF EXISTS "newsletter_subscriptions_delete_own" ON newsletter_subscriptions;

CREATE POLICY "newsletter_subscriptions_select_own" ON newsletter_subscriptions
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "newsletter_subscriptions_insert_own" ON newsletter_subscriptions
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());

CREATE POLICY "newsletter_subscriptions_update_own" ON newsletter_subscriptions
FOR UPDATE TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

CREATE POLICY "newsletter_subscriptions_delete_own" ON newsletter_subscriptions
FOR DELETE TO authenticated
USING (user_id = auth.uid());


-- ── newsletter_sources ────────────────────────────────────────────────────────
-- Read-only for authenticated users; writes are service_role/admin only.
ALTER TABLE newsletter_sources ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "newsletter_sources_select_authenticated" ON newsletter_sources;

CREATE POLICY "newsletter_sources_select_authenticated" ON newsletter_sources
FOR SELECT TO authenticated
USING (true);


-- ── prof_suggestions ──────────────────────────────────────────────────────────
ALTER TABLE prof_suggestions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "prof_suggestions_select_own"  ON prof_suggestions;
DROP POLICY IF EXISTS "prof_suggestions_insert_own"  ON prof_suggestions;

CREATE POLICY "prof_suggestions_select_own" ON prof_suggestions
FOR SELECT TO authenticated
USING (user_id = auth.uid());

CREATE POLICY "prof_suggestions_insert_own" ON prof_suggestions
FOR INSERT TO authenticated
WITH CHECK (user_id = auth.uid());


-- ── rate_limits ───────────────────────────────────────────────────────────────
-- Service-role only.
ALTER TABLE rate_limits ENABLE ROW LEVEL SECURITY;
-- No policies — service_role bypasses RLS.


-- ── seen_resend_events ────────────────────────────────────────────────────────
-- Service-role only (webhook idempotency).
ALTER TABLE seen_resend_events ENABLE ROW LEVEL SECURITY;
-- No policies — service_role bypasses RLS.


-- ── Read-only catalogue tables ────────────────────────────────────────────────
-- These are seeded reference data; no user should ever write to them directly.

ALTER TABLE courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "courses_select_authenticated" ON courses;
CREATE POLICY "courses_select_authenticated" ON courses
FOR SELECT TO authenticated
USING (true);

ALTER TABLE degree_programs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "degree_programs_select_authenticated" ON degree_programs;
CREATE POLICY "degree_programs_select_authenticated" ON degree_programs
FOR SELECT TO authenticated
USING (true);

ALTER TABLE requirement_blocks ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "requirement_blocks_select_authenticated" ON requirement_blocks;
CREATE POLICY "requirement_blocks_select_authenticated" ON requirement_blocks
FOR SELECT TO authenticated
USING (true);

ALTER TABLE requirement_courses ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "requirement_courses_select_authenticated" ON requirement_courses;
CREATE POLICY "requirement_courses_select_authenticated" ON requirement_courses
FOR SELECT TO authenticated
USING (true);
