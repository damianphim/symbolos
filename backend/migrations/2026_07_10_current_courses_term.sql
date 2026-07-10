-- Add term/year to current_courses so registered courses can be shown only
-- during their semester (Fall vs Winter vs Summer) instead of year-round.
-- Nullable: legacy rows keep NULL and the UI treats them as "term not set".

ALTER TABLE current_courses
  ADD COLUMN IF NOT EXISTS term text
    CHECK (term IN ('Fall', 'Winter', 'Summer')),
  ADD COLUMN IF NOT EXISTS year integer
    CHECK (year BETWEEN 2000 AND 2100);

COMMENT ON COLUMN current_courses.term IS
  'Semester the registration belongs to (Fall/Winter/Summer); NULL for legacy rows.';
COMMENT ON COLUMN current_courses.year IS
  'Calendar year of the term (e.g. 2026); NULL for legacy rows.';
