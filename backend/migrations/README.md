# Database migrations

Run these in the Supabase SQL Editor, in order.

| File | What it does |
|---|---|
| `2026_04_14_forum_reviews_and_professors.sql` | Adds `professor` to course tables, review fields to `forum_posts`, drops legacy category CHECK |
| `2026_04_14_club_logos_and_activity.sql` | Adds `clubs.logo_url`, creates the public `club-logos` storage bucket and RLS policies |
| `2026_04_14_scaling_indexes.sql` | Adds hot-path indexes (forum sort, user-scoped queries, notification cron) — safe to re-run |

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
