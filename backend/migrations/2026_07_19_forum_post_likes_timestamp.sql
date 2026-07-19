-- Semester-aware forum ranking needs to know WHEN each like landed (to
-- compute "upvotes since the semester ended" and recent like velocity),
-- not just that it exists. forum_post_likes is a pure junction table today
-- with no timestamp column.
ALTER TABLE forum_post_likes
  ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ NOT NULL DEFAULT now();

COMMENT ON COLUMN forum_post_likes.created_at IS
  'When the like was created. Existing rows backfill to now() at migration time — their exact historical like time is unrecoverable, so the ranking algorithm treats them as recent, which is a safe default (only pushes them toward "keeps pace" longer, never suppresses them incorrectly).';
