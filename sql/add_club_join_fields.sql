-- Add join_instructions and application_url columns to clubs table
-- join_instructions: free-text instructions for how to join the club
-- application_url: direct link to an external application form

ALTER TABLE clubs
  ADD COLUMN IF NOT EXISTS join_instructions TEXT,
  ADD COLUMN IF NOT EXISTS application_url TEXT;

-- Also add to club_submissions so these fields can be submitted during review
ALTER TABLE club_submissions
  ADD COLUMN IF NOT EXISTS join_instructions TEXT,
  ADD COLUMN IF NOT EXISTS application_url TEXT;
