-- Adds a `subject` column to forum_posts (e.g. "COMP" from "COMP 202") so
-- the forum can filter reviews by subject without parsing review_target_value
-- on every query. Only ever set on course reviews; NULL for everything else.
ALTER TABLE forum_posts
  ADD COLUMN IF NOT EXISTS subject TEXT;

CREATE INDEX IF NOT EXISTS idx_forum_posts_subject
  ON forum_posts (subject)
  WHERE subject IS NOT NULL;

-- Backfill existing course reviews (professor_review's review_target_value
-- is a person's name, not a course code — leave those NULL).
-- Take only the LEADING letters so this matches the Python derivation in
-- forum.py (re.match(r"^([A-Za-z]+)")): "COMP 202D1" → "COMP", not "COMPD".
UPDATE forum_posts
SET subject = upper(substring(review_target_value from '^[A-Za-z]+'))
WHERE review_target_type = 'course'
  AND review_target_value IS NOT NULL
  AND subject IS NULL;

COMMENT ON COLUMN forum_posts.subject IS
  'Subject prefix (e.g. "COMP") extracted from review_target_value for course reviews. NULL for non-course posts.';
