-- ════════════════════════════════════════════════════════════════════
-- Forum: merge course_review + professor_review into one review type
-- Run this in the Supabase SQL Editor.
-- ════════════════════════════════════════════════════════════════════

-- A review is now always a course review with an optional professor
-- attached, instead of two mutually-exclusive review types. The existing
-- `rating` column is kept as-is (it already means "how was the class
-- overall") and a second, independent rating dimension is added for
-- difficulty. Both are nullable so legacy course_review/professor_review
-- rows (which only ever set `rating`) keep working unmodified.
ALTER TABLE forum_posts
  ADD COLUMN IF NOT EXISTS difficulty_rating SMALLINT
    CHECK (difficulty_rating IS NULL OR (difficulty_rating >= 1 AND difficulty_rating <= 5));

ALTER TABLE forum_posts
  ADD COLUMN IF NOT EXISTS professor_name TEXT;

COMMENT ON COLUMN forum_posts.rating IS
  'Overall class rating, 1-5. For category=review this is required; NULL for non-review posts.';
COMMENT ON COLUMN forum_posts.difficulty_rating IS
  'Difficulty rating, 1-5, independent of the overall class rating. NULL for legacy course_review/professor_review posts and non-review posts.';
COMMENT ON COLUMN forum_posts.professor_name IS
  'Optional professor named in a course review. NULL if the reviewer didn''t specify one.';
