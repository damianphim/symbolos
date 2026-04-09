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
└── hooks/                  # useChatTabs, useNotificationPrefs
```

## Key patterns
- **Auth**: JWT via Supabase. Every route uses `Depends(get_current_user_id)` + `require_self()`.
- **AI context**: `build_system_context()` in `chat.py` — base student data cached 5min per user, static prompts loaded from `prompts/` at startup.
- **Seed format**: Each seed file returns a list of program dicts with `blocks` → `{block_type, credits_needed, courses: [{course_code, credits, title}]}`.
- **Reseed**: `POST /api/degree-requirements/seed?faculty=<name>` with `Authorization: Bearer <CRON_SECRET>`.
- **History**: `settings.CHAT_CONTEXT_MESSAGES` (default 6) controls how many turns are sent to Claude.

## Env vars (backend)
`ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `SUPABASE_ANON_KEY`, `CRON_SECRET`, `ADMIN_SECRET`, `ADMIN_EMAILS`

## Common tasks
- **Edit AI prompts**: edit files in `backend/api/prompts/` → restart server
- **Fix degree requirements**: edit `backend/api/seeds/<faculty>_degree_requirements.py` → reseed
- **Add a route**: create `backend/api/routes/<name>.py` → register in `main.py`
- **Change Claude model**: set `CLAUDE_MODEL` / `CLAUDE_CARDS_MODEL` in env or `config.py`
