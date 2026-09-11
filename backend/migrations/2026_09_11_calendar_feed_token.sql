-- ────────────────────────────────────────────────────────────────────────────
-- 2026-09-11 — Personal calendar feed token
--
-- Lets a student subscribe their whole calendar in Apple Calendar / Google
-- Calendar / Outlook via a one-click "subscribe by URL" link, instead of
-- manually downloading and importing a .ics file every time. External
-- calendar apps can't send our normal auth headers, so the token itself
-- (a random, unguessable string embedded in the feed URL) is the auth —
-- looked up server-side to resolve back to a user, same pattern as
-- admin_approval.py's signed links. Revocable: regenerating the token
-- immediately invalidates any previously-shared URL.
--
-- Idempotent — safe to re-run.
-- ────────────────────────────────────────────────────────────────────────────

ALTER TABLE users ADD COLUMN IF NOT EXISTS calendar_feed_token text;

CREATE UNIQUE INDEX IF NOT EXISTS idx_users_calendar_feed_token
  ON users (calendar_feed_token)
  WHERE calendar_feed_token IS NOT NULL;
