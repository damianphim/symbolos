-- Supabase advisor: "View is defined with the SECURITY DEFINER property".
-- A SECURITY DEFINER view runs with the view creator's privileges/RLS instead
-- of the querying user's, which can bypass row-level security on the underlying
-- tables. Switch these read-only catalogue views to SECURITY INVOKER so they
-- respect the caller's permissions.
--
-- Safe for this app: both views are queried only by the backend service role
-- (courses.py /subjects reads unique_subjects; instructor_ratings feeds the
-- search RPCs). Neither is read by the anon/authenticated client, so enforcing
-- the caller's RLS changes no behavior. Postgres 15+ (Supabase) supports the
-- security_invoker view option.

ALTER VIEW public.unique_subjects    SET (security_invoker = on);
ALTER VIEW public.instructor_ratings SET (security_invoker = on);
