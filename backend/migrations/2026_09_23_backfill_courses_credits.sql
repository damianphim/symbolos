-- ────────────────────────────────────────────────────────────────────────────
-- 2026-09-23 — Backfill courses.credits from mcgill_sections
--
-- courses.credits was never populated (0 of 11,768 rows had a value) —
-- whatever process originally loaded the `courses` table never wrote this
-- column. Separately, mcgill_sections DOES have real credit data (14,624 of
-- 31,836 rows) parsed by backend/scripts/import_sections.py from live
-- Banner listings. That script only ever wrote to mcgill_sections, never to
-- courses, so the two tables silently diverged on this one column.
--
-- mcgill_sections.course_code has a space ("COMP 202"); courses."Course"
-- doesn't ("COMP202") — the join strips it to match.
--
-- This only fills NULLs. It never overwrites an existing value, and running
-- it twice is a no-op the second time.
-- ────────────────────────────────────────────────────────────────────────────

-- ── STEP 1 — preview: how many rows would this actually change? ──────────
-- Run this first. If the count looks reasonable, proceed to the UPDATE below.

SELECT COUNT(*) AS would_update
FROM courses c
JOIN (
  SELECT DISTINCT ON (REPLACE(course_code, ' ', ''))
    REPLACE(course_code, ' ', '') AS course_code_norm,
    credits
  FROM mcgill_sections
  WHERE credits IS NOT NULL
  ORDER BY REPLACE(course_code, ' ', ''), credits
) sub ON c."Course" = sub.course_code_norm
WHERE c.credits IS NULL;

-- ── STEP 2 — the actual backfill ──────────────────────────────────────────

UPDATE courses c
SET credits = sub.credits
FROM (
  SELECT DISTINCT ON (REPLACE(course_code, ' ', ''))
    REPLACE(course_code, ' ', '') AS course_code_norm,
    credits
  FROM mcgill_sections
  WHERE credits IS NOT NULL
  ORDER BY REPLACE(course_code, ' ', ''), credits
) sub
WHERE c."Course" = sub.course_code_norm
  AND c.credits IS NULL;

-- ── STEP 3 — verify coverage improved ─────────────────────────────────────

SELECT
  COUNT(*)                                          AS total_rows,
  COUNT(credits)                                     AS rows_with_credits,
  ROUND(100.0 * COUNT(credits) / COUNT(*), 1)        AS pct_populated
FROM courses;
