# Symbolos — McGill AI Advisor

## Stack
- **Frontend**: React + Vite (`frontend/src/`)
- **Backend**: FastAPI + Python (`backend/api/`)
- **DB**: Supabase (PostgreSQL + auth)
- **AI**: Anthropic Claude Haiku (`claude-haiku-4-5-20251001`)
- **Deploy**: Vercel (frontend + backend as serverless functions)

## Backend structure
```
backend/api/
├── main.py              # FastAPI app, router registration
├── config.py            # Settings (env vars via pydantic-settings)
├── auth.py              # JWT auth, get_current_user_id, require_self
├── routes/
│   ├── chat.py          # /api/chat — main student chat, build_system_context()
│   ├── cards.py         # /api/cards — AI advisor card generation & threads
│   ├── courses.py       # /api/courses — search, details
│   ├── transcript.py    # /api/transcript — PDF upload → course import
│   ├── syllabus.py      # /api/syllabus — PDF upload → calendar events
│   ├── degree_requirements.py  # /api/degree-requirements — progress tracking
│   └── ...              # clubs, forum, calendar, users, notifications, etc.
├── seeds/               # Degree requirement data per faculty (seed DB)
│   ├── science_degree_requirements.py
│   ├── arts_degree_requirements.py
│   └── ... (one file per faculty)
├── prompts/             # Static prompt content loaded once at startup
│   ├── site_knowledge.md
│   ├── mcgill_advising.md
│   └── tab_guidance/    # One .md per tab (chat/calendar/courses/etc.)
└── utils/
    ├── supabase_client.py  # DB helpers (get_user_by_id, save_message, etc.)
    ├── sanitise.py         # Input sanitisation (injection/XSS prevention)
    ├── lang.py             # Shared lang_instruction() for FR/ZH/EN
    └── cache.py            # Utility cache helpers
```

## Frontend structure
```
frontend/src/
├── components/Dashboard/   # Main app tabs (ChatTab, CoursesTab, CalendarTab, etc.)
├── components/Auth/        # Login
├── lib/                    # API clients (api.js, cardsAPI.js, favoritesAPI.js, etc.)
├── contexts/               # AuthContext, LanguageContext, ThemeContext, TimezoneContext
└── hooks/                  # useNotificationPrefs, useUpcomingEvents
```

## Key patterns
- **Auth**: JWT via Supabase. Every route uses `Depends(get_current_user_id)` + `require_self()`.
- **AI context**: `build_system_context()` in `chat.py` — base student data cached 5min per user, static prompts loaded from `prompts/` at startup.
- **Seed format**: Each seed file returns a list of program dicts with `blocks` → `{block_type, credits_needed, courses: [{course_code, credits, title}]}`.
- **Reseed**: `POST /api/degree-requirements/seed?faculty=<name>` with `Authorization: Bearer <CRON_SECRET>`.
- **History**: `settings.CHAT_CONTEXT_MESSAGES` (default 6) controls how many turns are sent to Claude.

## Env vars (backend)
`ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_ANON_KEY`, `CRON_SECRET`, `ADMIN_SECRET`, `ADMIN_EMAILS`, `INNGEST_EVENT_KEY`, `INNGEST_SIGNING_KEY` (last two required in production only — get both from the Inngest Cloud dashboard for this app; without them every transcript/syllabus background job fails signature validation)

## Common tasks
- **Edit AI prompts**: edit files in `backend/api/prompts/` → restart server
- **Fix degree requirements**: edit `backend/api/seeds/<faculty>_degree_requirements.py` → reseed
- **Add a route**: create `backend/api/routes/<name>.py` → register in `main.py`
- **Change Claude model**: set `CLAUDE_MODEL` / `CLAUDE_CARDS_MODEL` in env or `config.py`

## Feature map (what each part of the site is for)
- **Home** — daily dashboard: AI "Brief" cards, current courses (active term only), Up Next deadlines, degree progress, quick actions.
- **Brief / Chat** — AI advisor cards generated per-user from their academic data (`cards.py`); freeform Q&A grounded in student context (`chat.py`).
- **Courses** — search McGill catalogue with grade history + RateMyProfessor; "My Courses" = saved / current (grouped by term) / completed.
- **Degree Planning** — seed-driven requirement blocks per program, progress tracking, AI recommendations.
- **Calendar** — events from syllabus import + manual entry + club events.
- **Transcript import** — PDF → Claude extraction → preview → import (async Inngest job). Populates completed/current courses, GPA, program.
- **Syllabus import** — PDF(s) → Claude → calendar events (async Inngest job).
- **Clubs / Forum** — student club directory + newsletters; course/prof discussion.
- **Profile** — settings, language, notifications, data deletion.

## Engineering invariants (apply to every change)
- **Security**: every new route takes `Depends(get_current_user_id)` + `require_self()`. Sanitize user input (`utils/sanitise.py`). Bound/validate all Claude-extracted values before persisting. New tables need RLS.
- **PII**: never store or output student IDs, permanent codes, or other government identifiers. Transcripts are redacted **before** the Claude call — text is extracted locally (pypdf) and `26\d{7}` / `[A-Z]{4}\d{8}` patterns stripped (`transcript.py _redact_transcript_text`), then the redacted **text** is sent (never the raw PDF). Scanned/no-text PDFs are **refused** (`UnreadableTranscriptError`), never sent un-redacted. `_scrub_pii` on the model output is the defense-in-depth backstop. Keep all three working.
- **i18n**: every user-facing string goes through `t()` with keys added to **all three** of `locales/en.js`, `fr.js`, `zh.js`. Never hardcode UI text.
- **No emojis in UI**: use `react-icons` components only. Backend-generated emoji (e.g. advisor-card `icon`) must be mapped to a react-icon before rendering.
- **Term-awareness**: `current_courses` rows carry `term`/`year`; UI filters by active term via `frontend/src/lib/termDates.js`. Rows with NULL term are legacy and always shown.
- **External calls**: wrap outbound HTTP (Resend, Slack, Inngest send) in try/except with a clean 5xx + friendly message — never leak raw tracebacks. Distinguish transient (connection/timeout/429/5xx → "try again") from permanent errors in user-facing messages.
- **Async jobs**: transcript/syllabus parsing returns `202 {job_id}`; frontends must poll `/api/jobs/{id}` (see `pollJob` in `ProfileSetup.jsx` / `TranscriptUpload.jsx`).
- **Local dev**: full stack = `backend` (uvicorn :8000) + `inngest` (dev server :8288) + `frontend` (:5173) — all in `.claude/launch.json`. Without Inngest, uploads 503.

## Agent skills

### Issue tracker

Issues are tracked as GitHub Issues on `damianphim/symbolos` (via the `gh` CLI). External PRs are not pulled into triage. See `docs/agents/issue-tracker.md`.

### Triage labels

Default label vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `CONTEXT.md` + `docs/adr/` at the repo root. See `docs/agents/domain.md`.
