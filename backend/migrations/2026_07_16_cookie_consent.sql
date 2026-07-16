-- Cookie/analytics consent record (Quebec Law 25 accountability).
-- Stores the user's most recent analytics-cookie choice + when they made it,
-- so we can demonstrate valid, withdrawable consent. Idempotent.
alter table public.users add column if not exists cookie_consent    text;
alter table public.users add column if not exists cookie_consent_at  timestamptz;
