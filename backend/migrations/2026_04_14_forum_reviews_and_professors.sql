-- ════════════════════════════════════════════════════════════════════
-- Forum reviews + professor persistence
-- Run this in the Supabase SQL Editor.
-- ════════════════════════════════════════════════════════════════════

-- 1. Per-course professor info (year-over-year history is preserved by
--    having one row per (user, course, term, year) in *_courses tables).
ALTER TABLE completed_courses
  ADD COLUMN IF NOT EXISTS professor TEXT;

ALTER TABLE current_courses
  ADD COLUMN IF NOT EXISTS professor TEXT;

-- 2. Forum: review-specific columns. NULL means it's a plain discussion post.
--    review_target_type ∈ ('course', 'professor', NULL)
--    review_target_value = course code (e.g. "COMP 251") or professor name
--    rating              = 1–5 stars (NULL for non-review posts)
ALTER TABLE forum_posts
  ADD COLUMN IF NOT EXISTS rating SMALLINT
    CHECK (rating IS NULL OR (rating >= 1 AND rating <= 5));

ALTER TABLE forum_posts
  ADD COLUMN IF NOT EXISTS review_target_type TEXT
    CHECK (review_target_type IS NULL OR review_target_type IN ('course', 'professor'));

ALTER TABLE forum_posts
  ADD COLUMN IF NOT EXISTS review_target_value TEXT;

-- Indexes for fast lookup of "all reviews for COMP 251" etc.
CREATE INDEX IF NOT EXISTS idx_forum_posts_review_target
  ON forum_posts (review_target_type, review_target_value)
  WHERE review_target_type IS NOT NULL;

-- 3. Optional: drop the old strict category check constraint if it exists
--    so the API can write new category strings (course_review, professor_review,
--    app_feedback). If your schema didn't enforce category as a CHECK, this is
--    a no-op.
DO $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM pg_constraint
    WHERE conname = 'forum_posts_category_check'
  ) THEN
    EXECUTE 'ALTER TABLE forum_posts DROP CONSTRAINT forum_posts_category_check';
  END IF;
END $$;
