-- ────────────────────────────────────────────────────────────────────────────
-- 2026-06-11 — Lock year_anchor to backend-only writes
--
-- year_anchor is a SYSTEM-managed field: the backend sets it whenever a
-- student's `year` is set, and the September cron advances it. A user must
-- never write it directly (via the anon key in the JS bundle hitting
-- PostgREST), because a forged low anchor would make the cron over-advance
-- their year of study. The API already drops the field (UserUpdate ignores
-- unknown keys), so this closes the direct-PostgREST path too.
--
-- Mirrors the column revokes from 2026_06_01 (verification_token) and
-- 2026_06_02 (email_bounced). The service-role backend bypasses these grants.
--
-- Idempotent — safe to re-run.
-- ────────────────────────────────────────────────────────────────────────────

DO $$
BEGIN
  -- Revoke direct UPDATE on the system-managed degree-progression columns.
  -- `year` stays user-writable (it's their year of study, set through the
  -- profile form), but year_anchor must only ever be set by the backend.
  BEGIN
    REVOKE UPDATE (year_anchor) ON users FROM anon, authenticated;
  EXCEPTION WHEN undefined_column THEN
    -- Column not present yet (run 2026_06_11_year_anchor.sql first) — no-op.
    NULL;
  END;
END $$;
