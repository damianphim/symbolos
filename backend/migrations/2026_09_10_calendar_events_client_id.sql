-- ────────────────────────────────────────────────────────────────────────────
-- 2026-09-10 — calendar_events.client_id column
--
-- backend/api/routes/notifications.py has referenced client_id since March
-- (a stable, frontend-generated id like "exam-COMP251-0" used to upsert
-- calendar events idempotently instead of duplicating them on retry), but
-- the column was never actually created in the database — every insert that
-- carried a client_id has been failing with Postgres error 42703 (column
-- does not exist). Low-traffic code paths (e.g. the registration-reminder
-- card) meant this went unnoticed for months; see Sentry SYMBOLOS-BACKEND-1C.
--
-- Idempotent — safe to re-run.
-- ────────────────────────────────────────────────────────────────────────────

ALTER TABLE calendar_events ADD COLUMN IF NOT EXISTS client_id varchar(200);

CREATE INDEX IF NOT EXISTS idx_calendar_events_user_client
  ON calendar_events (user_id, client_id)
  WHERE client_id IS NOT NULL;
