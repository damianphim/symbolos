-- ────────────────────────────────────────────────────────────────────────────
-- 2026-06-10 — Terms / Privacy acceptance record
--
-- Stores when each user agreed to the legal terms and which version they
-- agreed to. Recorded at profile creation (POST /api/users). Gives a
-- defensible record under Quebec Law 25 / contract law.
--
-- Bump settings.LEGAL_POLICY_VERSION when the policies materially change;
-- you can then find users on an old version with:
--   SELECT id, email FROM users WHERE tos_version <> '<new-version>';
-- and prompt them to re-accept.
--
-- Idempotent — safe to re-run.
-- ────────────────────────────────────────────────────────────────────────────

ALTER TABLE users ADD COLUMN IF NOT EXISTS tos_accepted_at timestamptz;
ALTER TABLE users ADD COLUMN IF NOT EXISTS tos_version text;

-- Backfill existing accounts: they accepted whatever was live when they
-- signed up. We don't know the exact timestamp, so mark the version as
-- 'legacy-pre-2026-06-10' (distinguishable from versioned acceptances) and
-- use now() as an approximate stamp. Uses a guarded UPDATE so it works
-- whether or not the table has a created_at column.
UPDATE users
SET tos_accepted_at = COALESCE(tos_accepted_at, now()),
    tos_version     = COALESCE(tos_version, 'legacy-pre-2026-06-10')
WHERE tos_accepted_at IS NULL;
