-- ────────────────────────────────────────────────────────────────────────────
-- 2026-06-03 — Feedback inflow + webhook idempotency
--
-- 1. `feedback` table — backs POST /api/feedback. Every submission is
--    persisted here even if the email/Slack side fails, so nothing is lost.
-- 2. `seen_resend_events` — dedup table for the Resend webhook. Resend
--    retries on any non-2xx, so without this a momentarily-broken handler
--    could process the same bounce several times.
--
-- Idempotent — safe to re-run.
-- ────────────────────────────────────────────────────────────────────────────

-- ── 1. Feedback ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS feedback (
  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     uuid REFERENCES auth.users(id) ON DELETE SET NULL,
  user_email  text,
  kind        text NOT NULL DEFAULT 'general',
  message     text NOT NULL,
  course      text,
  page        text,
  status      text NOT NULL DEFAULT 'new',   -- new | triaged | done
  created_at  timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_feedback_status_created
  ON feedback (status, created_at DESC);

ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Users can insert their own feedback; nobody but the service role reads it.
DROP POLICY IF EXISTS "feedback_insert_own" ON feedback;
CREATE POLICY "feedback_insert_own"
  ON feedback FOR INSERT
  TO authenticated
  WITH CHECK (user_id = auth.uid());

-- No SELECT policy for anon/authenticated → only the service-role backend
-- (and the Supabase Studio admin) can read submissions.

-- ── 2. Resend webhook dedup ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS seen_resend_events (
  event_id    text PRIMARY KEY,
  seen_at     timestamptz NOT NULL DEFAULT now()
);

-- Auto-prune: we only need to remember an event long enough to outlast
-- Resend's retry window (hours). A periodic delete keeps the table small.
CREATE INDEX IF NOT EXISTS idx_seen_resend_events_seen_at
  ON seen_resend_events (seen_at);
