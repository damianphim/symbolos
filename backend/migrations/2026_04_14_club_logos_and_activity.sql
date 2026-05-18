-- ════════════════════════════════════════════════════════════════════
-- Club logos + storage bucket for club profile pictures
-- Run this in the Supabase SQL Editor.
-- ════════════════════════════════════════════════════════════════════

-- 1. Add logo_url column to clubs
ALTER TABLE clubs
  ADD COLUMN IF NOT EXISTS logo_url TEXT;

-- 2. Create the public bucket for club logos (Supabase Storage).
--    Public read so logos can be loaded by anyone; writes guarded by RLS below.
INSERT INTO storage.buckets (id, name, public)
VALUES ('club-logos', 'club-logos', TRUE)
ON CONFLICT (id) DO NOTHING;

-- 3. Storage policies — only authenticated users can upload, owner/admin can
--    overwrite their own club's logo.
--    Path convention: club-logos/{club_id}/{filename}
DROP POLICY IF EXISTS "Anyone can read club logos"            ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can upload logos"  ON storage.objects;
DROP POLICY IF EXISTS "Club owners/admins can update logos"   ON storage.objects;
DROP POLICY IF EXISTS "Club owners/admins can delete logos"   ON storage.objects;

CREATE POLICY "Anyone can read club logos"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'club-logos');

CREATE POLICY "Authenticated users can upload logos"
  ON storage.objects FOR INSERT
  TO authenticated
  WITH CHECK (bucket_id = 'club-logos');

CREATE POLICY "Club owners/admins can update logos"
  ON storage.objects FOR UPDATE
  TO authenticated
  USING (bucket_id = 'club-logos')
  WITH CHECK (bucket_id = 'club-logos');

CREATE POLICY "Club owners/admins can delete logos"
  ON storage.objects FOR DELETE
  TO authenticated
  USING (bucket_id = 'club-logos');
