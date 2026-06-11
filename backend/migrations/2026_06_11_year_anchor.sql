-- ────────────────────────────────────────────────────────────────────────────
-- 2026-06-11 — Academic-year auto-advance anchor
--
-- A student's year of study (U0–U3 = year 0–3) was set once and never moved.
-- This adds `year_anchor`: the Fall calendar year of the academic year in
-- which `year` was last set/advanced. The daily cron compares it to the
-- current academic year and bumps `year` each September, so the planner
-- stays accurate without the student editing it.
--
-- Academic year convention: the Fall calendar year. Sept 2025–Aug 2026 = 2025.
--
-- Backfill: existing rows are anchored to the CURRENT academic year so the
-- next September advance is correct and nobody jumps multiple years at once.
-- Idempotent — safe to re-run.
-- ────────────────────────────────────────────────────────────────────────────

ALTER TABLE users ADD COLUMN IF NOT EXISTS year_anchor int;

-- Current academic year = Fall calendar year (month >= 9 → this year, else last).
UPDATE users
SET year_anchor = CASE
  WHEN EXTRACT(MONTH FROM now()) >= 9 THEN EXTRACT(YEAR FROM now())::int
  ELSE EXTRACT(YEAR FROM now())::int - 1
END
WHERE year_anchor IS NULL AND year IS NOT NULL;
