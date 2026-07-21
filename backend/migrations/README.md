# Database migrations

Run these in the Supabase SQL Editor, in order.

| File | What it does |
|---|---|
| `2026_04_14_forum_reviews_and_professors.sql` | Adds `professor` to course tables, review fields to `forum_posts`, drops legacy category CHECK |
| `2026_04_14_club_logos_and_activity.sql` | Adds `clubs.logo_url`, creates the public `club-logos` storage bucket and RLS policies |
| `2026_04_14_scaling_indexes.sql` | Adds hot-path indexes (forum sort, user-scoped queries, notification cron) — safe to re-run |
| `2026_04_14_security_tighten_logo_policies.sql` | **SEC FIX**: replaces the over-permissive club-logos RLS so only the club owner can upload/update/delete their own logo (paired with the `logo_url` validator added in code) |
| `2026_05_18_backfill_username_from_email.sql` | Sets `username` to the first name derived from McGill email for any existing user with NULL/empty username (e.g. `first.last@mail.mcgill.ca` → `First`) |
| `2026_05_18_club_manager_requests.sql` | New `club_manager_requests` table for the manager-invite flow — owners/admins request other Symbolos users to become managers, target accepts/denies from their Clubs tab |
| `2026_05_18_club_logo_admin_upload.sql` | Widens the club-logos storage RLS so invited admins (not just the owner) can upload/update/delete their club's logo |
| `2026_05_21_add_join_link.sql` | Adds `join_link` column to clubs |
| `2026_06_01_sec_rls_clubs_pii.sql` | **SEC FIX**: RLS on `clubs` (hide private clubs from anon/non-members); revoke verification_token columns from anon/auth roles |
| `2026_06_02_email_bounce_columns.sql` | Adds email bounce/complaint tracking columns to `users` |
| `2026_06_03_feedback_and_webhook_dedup.sql` | Adds `feedback` table and `seen_resend_events` idempotency table |
| `2026_06_10_tos_acceptance.sql` | Adds `tos_accepted_at` and `tos_version` columns to `users` |
| `2026_06_11_course_allocations.sql` | New `course_allocations` table with RLS for degree-planning course→program choices |
| `2026_06_11_year_anchor.sql` | Adds `year_anchor` column to users for cohort-relative year calculation |
| `2026_06_23_rls_forum_and_club_tables.sql` | **SEC FIX**: RLS on 11 previously unprotected tables — `club_managers`, `club_subscriptions`, `club_join_requests`, `club_manager_requests`, `club_events`, `club_announcements`, `club_submissions`, `forum_posts`, `forum_replies`, `forum_post_likes`, `forum_reply_likes` |
| `2026_06_23_audit_log.sql` | New `audit_log` table — append-only record of sensitive data access (transcript uploads, data exports, account deletions). Users can read their own rows; backend writes via service_role only. |
| `2026_07_16_cookie_consent.sql` | Adds `cookie_consent` + `cookie_consent_at` to `users` — server-side record of the analytics-cookie consent choice (Law 25 accountability). Code degrades gracefully if not yet applied. |
| `2026_07_19_forum_unified_reviews.sql` | Adds `difficulty_rating` + `professor_name` to `forum_posts` — merges course_review/professor_review into one review type (course + optional professor + two independent rating dimensions). Legacy rows unaffected. |
| `2026_07_19_forum_post_likes_timestamp.sql` | Adds `created_at` to `forum_post_likes` — the semester-aware ranking algorithm needs to know when each like landed, not just that it exists. Existing rows backfill to `now()`. |
| `2026_07_19_forum_subject_filter.sql` | Adds `subject` to `forum_posts` (e.g. "COMP" extracted from a course review's `review_target_value`) + backfills existing course reviews, so the forum can filter/search by subject without re-parsing course codes on every query. |
| `2026_07_20_profile_images_bucket.sql` | Creates the public `profile-images` storage bucket + per-user RLS (upload/update/delete scoped to `{user_id}/...`), so profile photo uploads actually persist — the frontend previously sent a raw base64 data URI which the `profile_image` https-only validator always rejected. |
| `2026_07_20_clubs_private_visible.sql` | **Product change**: private clubs are now discoverable in Explore/Trending like public ones — "private" means join-by-application only, not hidden. Updates the `2026_06_01_sec_rls_clubs_pii.sql` RLS to drop the `is_private = false` condition, keeping only `is_verified = true`. |
| `2026_07_20_advisor_cards_advice_category.sql` | **Bug fix**: adds `"advice"` to `advisor_cards_category_check` — the new proactive-milestone card category was added in code but never in the DB constraint, so every "advice" card 500'd on insert (Sentry `23514`). |
| `2026_07_21_clubs_translation_cache.sql` | Adds `description_{fr,zh}`, `meeting_schedule_{fr,zh}`, `join_instructions_{fr,zh}` to `clubs` — cache for on-demand AI translations of a club's detail fields, filled the first time a club is opened in FR/ZH and cleared when the owner edits the source field. |

All migrations are idempotent (`IF NOT EXISTS`, `ON CONFLICT DO NOTHING`, `DO $$ ... END $$` guards) so re-running them is a no-op.

---

## Supabase connection pooler — N/A for this stack

The Supabase pooler (port 6543, Pro plan) only applies to **direct Postgres
connections** (asyncpg, psycopg2, raw psql). This backend uses `supabase-py`'s
`create_client()`, which talks to Supabase via **PostgREST** — and PostgREST
manages its own internal pool on Supabase's side. **Do not change `SUPABASE_URL`
to the pooler URL** — it'll break PostgREST routing.

The pooler becomes relevant only if you later move hot-path reads onto
`asyncpg` directly (real persistent pool, lower per-query overhead). Good
candidates if/when you do that:
- `forum.py` post list queries
- `cards.py::_fetch_student_context_parallel`
- `clubs.py` list/category fetches

---

## Scaling roadmap (where we are)

Already shipped (Tier 1 + parts of Tier 2):

- ✅ Tiered rate limits per endpoint (general 100 / chat 50 / Claude-heavy 30 rpm per IP, halved per user)
- ✅ Index migration for hot-path queries
- ✅ Anthropic prompt caching on `chat.py` (system block marked `ephemeral`)
- ✅ Anthropic prompt caching on `cards.py` (stream + generate + retranslate)
- ✅ Both models on Haiku 4.5 (no tier change needed)

Still TODO (revisit at ~5–10k users):

- Async-ify the remaining sync Supabase calls in `transcript.py`, `electives.py`, and `forum.py` (wrap with `asyncio.to_thread`)
- Move long-running PDF parsing off Vercel (Inngest, Trigger.dev, or Supabase Edge Functions)
- Real connection pool with `asyncpg` once we leave Vercel for a long-lived host
