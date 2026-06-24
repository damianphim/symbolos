-- ────────────────────────────────────────────────────────────────────────────
-- 2026-06-24 — Background jobs table + job-uploads storage bucket
--
-- Transcript and syllabus PDF processing now runs as an Inngest background
-- job. The upload endpoint stores the PDF in Supabase Storage, creates a
-- job row here, then returns 202 immediately. The frontend polls
-- GET /api/jobs/{id} for status. When the job completes, the result is
-- stored in the `result` column and the PDF is cleaned up from storage.
-- ────────────────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS jobs (
    id          uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id     uuid        REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
    kind        text        NOT NULL,                -- 'transcript' | 'syllabus'
    status      text        NOT NULL DEFAULT 'pending',  -- pending | processing | done | failed
    dry_run     boolean     NOT NULL DEFAULT false,
    result      jsonb,
    error       text,
    created_at  timestamptz DEFAULT now() NOT NULL,
    updated_at  timestamptz DEFAULT now() NOT NULL,
    CONSTRAINT jobs_status_check CHECK (status IN ('pending','processing','done','failed')),
    CONSTRAINT jobs_kind_check   CHECK (kind   IN ('transcript','syllabus'))
);

CREATE INDEX IF NOT EXISTS jobs_user_id_idx    ON jobs (user_id);
CREATE INDEX IF NOT EXISTS jobs_status_idx     ON jobs (status);
CREATE INDEX IF NOT EXISTS jobs_created_at_idx ON jobs (created_at DESC);

ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

-- Users can read their own jobs (for status polling)
DROP POLICY IF EXISTS "jobs_select_own" ON jobs;
CREATE POLICY "jobs_select_own"
ON jobs FOR SELECT
TO authenticated
USING (user_id = auth.uid());

-- No user-initiated writes — backend uses service_role only


-- ── Supabase Storage bucket for temporary PDF uploads ────────────────────────
-- Private bucket — no public access. PDFs are deleted once the job completes.
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'job-uploads',
    'job-uploads',
    false,
    15728640,   -- 15 MB max
    ARRAY['application/pdf']
)
ON CONFLICT (id) DO NOTHING;

-- Only the service role can read/write job uploads (no user-facing storage policy)
