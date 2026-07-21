-- ════════════════════════════════════════════════════════════════════
-- clubs: cached AI translations of the free-text detail fields
-- Run this in the Supabase SQL Editor.
--
-- The club detail drawer can now show description / meeting_schedule /
-- join_instructions in the viewer's language (FR/ZH). Translations are
-- produced on demand by a single Haiku call the first time a club is opened
-- in a given language, then cached in these columns so we never re-translate
-- (or re-bill) on subsequent views. `name` is intentionally NOT translated —
-- club names are proper nouns / acronyms.
--
-- When an owner edits one of the source fields (see edit_club in
-- discovery.py), the matching _fr/_zh columns are set back to NULL so the
-- stale translation is regenerated on next view.
-- ════════════════════════════════════════════════════════════════════

ALTER TABLE clubs
  ADD COLUMN IF NOT EXISTS description_fr        TEXT,
  ADD COLUMN IF NOT EXISTS description_zh        TEXT,
  ADD COLUMN IF NOT EXISTS meeting_schedule_fr   TEXT,
  ADD COLUMN IF NOT EXISTS meeting_schedule_zh   TEXT,
  ADD COLUMN IF NOT EXISTS join_instructions_fr  TEXT,
  ADD COLUMN IF NOT EXISTS join_instructions_zh  TEXT;
