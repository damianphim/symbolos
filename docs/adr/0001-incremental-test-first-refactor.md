# Refactor strategy: incremental, test-first, ship-alongside

The codebase (415 commits, ~7 months, two contributors) has grown several files mixing many concerns with almost no test coverage — e.g. `clubs.py` (2051 lines, 30+ endpoints spanning club CRUD, membership, admin moderation with HTML email-action views, and a cron cleanup job) and `ClubsTab.jsx` (2607 lines). We decided to refactor incrementally, module by module, interleaved with ongoing feature work, keeping `main` deployable at every commit — not a dedicated refactor-only block, not a full rewrite-and-migrate.

Before refactoring each module, we write characterization tests pinning down its *current* behavior, so the refactor is checked automatically rather than verified by hand. Backend tests use pytest and the existing `FakeSupabase`/`TestClient` harness in `backend/tests/conftest.py`, which already patches `get_supabase` for `clubs`, `cards`, `chat`, `forum`, etc. Frontend tests use Vitest + React Testing Library — new tooling, since the project had none — chosen because Vitest shares the existing Vite config/transform pipeline rather than needing a separate one (as Jest would).

Damian owns the refactor solo; Alex continues feature work elsewhere and isn't currently active in the codebase, so there's no file-ownership conflict right now. Project lifespan is uncertain but not ending soon, so the target is pragmatic modularity decided per-file (thin router/service split, sub-feature packages, etc. — whatever fits that file) rather than committing upfront to one layered architecture across the whole backend.

First target: `clubs.py` + `ClubsTab.jsx` — the worst offenders on each side, sharing one domain, with backend test fixtures already wired up.

## Considered Options

- **Manual QA instead of characterization tests** — rejected: no automated check that behavior survived a refactor, too risky for a live app with real users.
- **Big-bang rewrite** — rejected: highest upfront risk; the app must stay deployable throughout.
- **Dedicated refactor-only block, pausing feature work** — rejected: unnecessary since Alex isn't blocked by this work right now, and shipping features alongside the refactor keeps delivering value.
- **Jest for frontend tests** — rejected: would need its own transform/config setup separate from Vite, for no benefit over Vitest here.
