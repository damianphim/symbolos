-- Add is_honours column to users table
-- Run this in Supabase SQL Editor

ALTER TABLE users ADD COLUMN IF NOT EXISTS is_honours BOOLEAN DEFAULT false;

-- Update RLS policy if needed (should already be covered by existing policies)
COMMENT ON COLUMN users.is_honours IS 'Whether the student is enrolled in an Honours program variant of their major';
