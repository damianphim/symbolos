# Symbolos Mobile — Phase 0 Audit

**Status:** read-only audit. No code changed. Not committed.
**Branch at time of audit:** `main` @ `8a7ce65` (clean)

---

## 0. Headline findings (read these first)

Five things materially change the plan as written:

1. **There is no router.** `react-router` is not a dependency. Navigation is `useState`
   in `App.jsx` (landing / login / dashboard) plus an `activeTab` string in
   `Dashboard.jsx`. Plan step 1.3 ("wire the router to select layout shell by
   viewport") has nothing to wire. See §4.
2. **`Dashboard.jsx` is both the data container and the desktop layout shell**
   (1085 lines; ~40 `useState`, all the course/favorite/card loaders and handlers).
   A `<MobileLayout>` cannot be swapped in beside it without duplicating that state.
   **This is the one blocking refactor.** See §5.
3. **Email verification is not Supabase's built-in flow.** It's a custom backend
   link, `{frontend_origin}/?verify_token=…&user_id=…` (`verification.py:219`).
   Password reset *is* Supabase (PKCE `?code=`). They need different deep-link
   handling. See §6.
4. **A 6-digit OTP verification path already exists** in `Login.jsx`
   (`supabase.auth.verifyOtp`, line 170) alongside a polling fallback. Signup
   verification can therefore work in the native app with **zero deep-link work**.
   This de-risks Phase 3 considerably. Password reset has no OTP equivalent.
5. **The `vercel.json` CSP does not apply to the native app** — there is no
   `<meta http-equiv="Content-Security-Policy">` in `index.html`, so the policy
   only exists as a Vercel response header. A Capacitor WebView loads from the
   local filesystem and never receives it. **Phase 3's "CSP breakage" risk is much
   smaller than the plan assumes.** CORS is the real problem instead. See §7.

---

## 1. CSS & breakpoint approach

Plain, hand-written CSS. One `.css` file co-located per component, imported
directly (`import './Dashboard.css'`). No Tailwind, no CSS modules, no
CSS-in-JS. Design tokens live in `theme.css` (561 lines) as CSS custom
properties; `index.css` holds resets and globals.

Breakpoints are **inconsistent** — 72 media queries across 8 distinct widths:

| Width | Count | Notes |
|---|---|---|
| 768px | 21 | de-facto primary |
| 640px | 15 | second most common |
| 480px | 13 | small-phone tier |
| 600px | 5 | |
| 900px | 4 | tablet-ish |
| 560px, 520px, 360px | 7 | one-offs |
| 760px, 700px, 1024px | 3 | one-offs |

JS-side, mobile is already checked twice, both at 768:
- `Dashboard.jsx:536` — `window.matchMedia('(max-width: 768px)')` for `--rsb-width`
- `Dashboard.jsx:695` — `window.innerWidth < 768` to auto-close the sidebar
- (`DegreeRequirementsView.jsx:497,513` disagrees at `< 760`)

**Recommendation:** `useViewport()` with **`max-width: 768px` = mobile**. It matches
both existing JS checks and the plurality of CSS. Do *not* mass-rewrite the other
breakpoints in Phase 1 — retune only the ones that visibly break, or the diff
becomes unreviewable against a live product.

---

## 2. Route / page inventory

"Routes" here means renderable top-level states, since there is no router.

### App shell (`App.jsx`)
| Screen | Trigger | Component |
|---|---|---|
| Landing | unauthenticated default | `Landing/LandingPage` |
| Login | `showLogin` state, `?signin`, `#signin`, `?verify_token` | `Auth/Login` (modes: login/signup/forgot/reset/verify) |
| Legal modals | `?show=privacy\|terms\|about` (Vercel rewrites `/privacy`, `/terms`) | `Legal/PrivacyPolicy`, `TOS`, `AboutUs` |
| Admin | `window.location.pathname === '/admin'` | `Admin/AdminSuggestions` |
| Loading / Error | auth state | `Loading`, `ErrorScreen`, `ErrorBoundary` |
| Dashboard | authenticated + verified | `Dashboard/Dashboard` |

### Dashboard tabs (`activeTab`, 8 entries, `Sidebar.jsx:16-25`)
`home` · `chat` (Brief) · `favorites` (Degree Planning) · `courses` · `calendar` ·
`clubs` · `forum` · `profile`

All except `home` and `chat` are `React.lazy`-loaded.

### Persistent overlays
`RightSidebar` (pinned-card chat) · `CourseDetailModal` · `TranscriptUpload` ·
`MarkCompleteModal` · `FeedbackModal` · `OnboardingTutorial` ·
calendar's `EventModal` / `DayDrawer` / `EventPopup` / `AnnouncementModal` / `BulkDeleteModal`

---

## 3. Per-page classification & effort

Levels per the plan: **(a)** responsive CSS · **(b)** adaptive Level 2 variant · **(c)** fine as-is.
Effort is relative (S/M/L/XL), assuming the §5 refactor has landed.

| Page / component | Size (jsx/css) | Class | Effort | Justification |
|---|---|---|---|---|
| **CalendarTab** | 1275 / 2612 | **(b)** | **XL** | A 7-column month grid is unusable at 360px. Needs a mobile agenda/list view. Also the worst logic/layout tangle: ~30 `useState` in one file, granularity + filters + 5 modals. Already has 6 media queries that are patching, not solving. |
| **ClubsTab** | 2453 / 2034 | **(b)** | **XL** | Largest component in the repo. Directory grid + detail + newsletters + management forms in one file. Needs decomposition before a variant is sane. |
| **DegreePlanningView** | 1680 / 1237 | **(b)** partial | **L** | 4 sub-tabs (`my_courses`/`requirements`/`study_abroad`/`advising`) in a horizontal bar — needs scroll or segmented control. `DegreeRequirementsView` is master-detail with its own `innerWidth < 760` sidebar toggle; that pattern needs a real push-navigation on mobile. Rest is (a). |
| **AdvisorCards** (Brief/chat) | 781 / 1005 | **(b)** | **L** | Card grid + drag-to-reorder + pin-to-right-sidebar. Drag-reorder and pinning are desktop metaphors. Mobile wants full-screen thread push. Only 2 media queries today. Plus keyboard-inset handling (§7.3). |
| **RightSidebar** | 442 / 579 | **(b)** | **M** | Already becomes an overlay drawer < 768. On mobile the pin concept should collapse into the Brief thread view rather than persist as a second surface. Partly *deleted* work, not added. |
| **CoursesView / CoursesTab** | — / 331 | **(a)** + partial (b) | **M** | Sub-tab bar + search + result cards. Has 768/640/480 queries. Result-card density and the sort/term filter row need work; structure is sound. |
| **Forum** | 710 / 903 | **(a)** | **M** | Already has 640/600 queries and a list-shaped layout that degrades acceptably. Mostly padding/typography. |
| **ProfileTab** + `Settings`, `EnhancedProfileForm`, `PersonalInfoCard`, `TargetGPACalculator`, `AcademicPerformanceCard`, `GPATrendChart` | ~2400 combined | **(a)** | **M** | Densest existing responsive coverage in the repo (1024/900/768/640/600/520/480/360). Form-heavy, already stacks. Charts need width audit. |
| **TranscriptUpload** | 438 / 664 | **(a)** + native check | **M** | Modal + drag-drop + polling. CSS is fine at 640. Real work is verifying the WebView file picker (§7.5), not layout. |
| **HomeTab** | 365 / — | **(a)** | **S–M** | Card grid, one 768 query. Straightforward stacking. |
| **Login / Auth** | 546 / 694 | **(a)** | **S** | Best-covered file (900/640/480/360). Needs keyboard-inset handling only. |
| **LandingPage** | — / 680 | **(a)** | **S** | Marketing page, already responsive at 820/560/360. Matters most — it's the r/mcgill funnel. |
| **CourseDetailModal** | 346 / 521 | **(a)**, (b) optional | **S** | Works at 600. A bottom-sheet variant would feel native but is polish, not blocker. |
| **Legal modals** | — / 200 | **(c)** | **S** | Fine at 520. |
| **AdminSuggestions** | — / 327 | **(c)** | — | Admin-only, desktop-only. Explicitly out of scope. |
| **OnboardingTutorial** | 340 / — | **(b)** | **M** | ⚠️ See §5.2 — this *breaks* under a mobile shell rather than merely looking wrong. |

---

## 4. Routing structure (and what it costs mobile)

State-based navigation, no URLs. Consequences:

- **No deep-link targets.** `symbolos.ca/calendar` does not exist. Phase 3
  deep links can only land on "the app", then set `activeTab` programmatically.
- **Android hardware back button has nothing to pop.** This is a Play Store
  review issue, not just a UX one — pressing back from any tab exits the app.
  Currently unimplemented in any form. **Not in the plan document; needs adding
  to Phase 3.**
- There is already an ad-hoc cross-component nav channel: `window.dispatchEvent`
  custom events (`open-transcript-upload`, `open-degree-planning`, `restart-tour`)
  listened for in `Dashboard.jsx:168-184`. Deep links can reuse this pattern.

**Recommendation:** do **not** add `react-router` in Phase 1. It would touch every
navigation call site in a live product for no mobile-layout benefit. Instead
introduce a small nav-stack state (`[{tab, params}]`) inside the extracted
dashboard provider, which gives both the mobile push/back pattern *and* an
Android back-button target. Revisit real routing only if App Links need to
land on specific screens (Phase 3+).

---

## 5. Tangled layout/logic — refactors required before mobile variants

### 5.1 `Dashboard.jsx` — the blocker

It currently owns, in one 1085-line component:
- **data**: favorites, completed, current courses (+ their `Set` maps), advisor
  cards, club events, managed clubs, search state, terms
- **logic**: `loadFavorites`, `loadCompletedCourses`, `loadCurrentCourses`,
  `loadAdvisorCards`, `refreshAdvisorCards`, the card language/retranslation
  effect (~90 lines), `handleCourseSearch` with fuzzy fallback, all
  toggle handlers, transcript import completion, avatar upload
- **layout**: `<Sidebar>` + `<main>` + the 8-way `activeTab` render switch + 6 overlays

Levels 2 and 3 both require the data half without the layout half.

**Required Phase 1 step 0:** extract the data/logic into
`useDashboardData()` (or a `DashboardDataProvider` context — preferable, since
the mobile shell will read it from nested screens). `Dashboard.jsx` becomes the
desktop *view* consuming it; `MobileLayout` becomes a second consumer. This is a
pure move-code refactor with no behavior change, and it is the single highest-risk
change in the whole project because it touches the file every authenticated user
loads. It should be its own commit, reviewed and tested alone, before any mobile
work starts — and it is **not parallelizable**, so no subagents until it lands.

### 5.2 `OnboardingTutorial.jsx` — breaks, not degrades

17 tour stops anchor via `document.querySelector('[data-tour="…"]')` +
`getBoundingClientRect()` (lines 167-169). Eight of those anchors —
`home`, `chat`, `courses`, `favorites`, `calendar`, `clubs`, `forum`, `profile` —
are **on the Sidebar nav buttons** (`Sidebar.jsx:132`). Under `<MobileLayout>`
there is no Sidebar, so `querySelector` returns `null` and the tour dies.

The mobile bottom tab bar must carry the same `data-tour` keys, and the deeper
in-page stops need re-verification per screen. Note the tour auto-shows for
accounts ≤3 days old (`Dashboard.jsx:120-132`) — i.e. exactly the new users a
store launch brings in. Treat as launch-blocking.

### 5.3 Lesser tangles
- `CalendarTab.jsx` — ~30 `useState` co-located with grid rendering; extract
  event-loading/filtering into a hook before writing the agenda view.
- `ClubsTab.jsx` — 2453 lines, needs splitting into list/detail/manage before
  a variant is maintainable.
- `DegreeRequirementsView.jsx` — master-detail selection state entangled with
  its own responsive sidebar toggle.

---

## 6. Supabase auth redirects (Phase 3 input)

Two **different** mechanisms, both currently origin-bound to the web app:

### 6.1 Signup / email verification — custom, not Supabase
- Backend builds `{frontend_origin}/?verify_token={token}&user_id={id}`
  (`verification.py:219`), where `frontend_origin` is chosen from
  `ALLOWED_ORIGINS`, preferring anything ending in `symbolos.ca`
  (`verification.py:78-80`).
- Frontend handles it in `App.jsx:64-88` (`handleVerifyToken` → `authAPI.verifyEmail`).
- **Also** `AuthContext.jsx:224-228` passes `emailRedirectTo: ${window.location.origin}/`
  to `supabase.auth.signUp`. In the native app that origin becomes
  `https://localhost` / `capacitor://localhost` — Supabase will reject it unless allowlisted.
- ✅ **Escape hatch:** `Login.jsx:165-180` already implements 6-digit OTP entry via
  `supabase.auth.verifyOtp`, plus a poll + window-focus refresh
  (`App.jsx:101-124`, `Login.jsx:69-110`). **Signup verification can ship on
  mobile with no deep link at all.** Recommend this for v1.

### 6.2 Password reset — Supabase PKCE
- `AuthContext.jsx:292-301`: `resetPasswordForEmail(email, { redirectTo: window.location.origin + '/' })`.
- Returns to `?code=`, which `onAuthStateChange` exchanges, firing
  `PASSWORD_RECOVERY` (`AuthContext.jsx:124-130`) → sets
  `symbolos_open_pw_change` → Dashboard opens on the profile tab
  (`Dashboard.jsx:66-68`).
- `AuthContext.jsx:179-207` deliberately skips `getSession()` when `?code=` is
  present to avoid racing the exchange. **Any deep-link handler must preserve
  this ordering** — feeding tokens in via `appUrlOpen` after the listener
  registers is compatible; doing it before is not.
- ⚠️ **No OTP fallback exists for reset.** This is the one flow that genuinely
  needs a deep link (or a new code-based reset path).

### 6.3 Recommendation
Hardcode both redirect origins to `https://symbolos.ca` (rather than
`window.location.origin`) and use **Android App Links** so the installed app
intercepts them, falling back to the web for everyone else. This avoids
allowlisting `https://localhost` in Supabase — which would otherwise be a
permanent open redirect target in a production project.

---

## 7. Native-integration risk review (Phase 2/3 input)

### 7.1 CORS — **will break every API call; must be fixed**
`backend/api/main.py:266-273` uses `allow_origins=settings.ALLOWED_ORIGINS`,
default `http://localhost:5173,https://ai-advisor-pi.vercel.app,https://symbolos.ca`
(`config.py:112`), with `allow_credentials=True`.

The native WebView's origin is `https://localhost` (Android, Capacitor default)
or `capacitor://localhost` (iOS). Neither is allowlisted → every request fails
preflight. `allow_credentials=True` also forbids the `"*"` wildcard shortcut.

**This is a required backend change and it is the only one.** Flagging per the
plan's instruction rather than making it.

### 7.2 CSP — **lower risk than the plan assumes**
The CSP exists *only* as a Vercel response header (`vercel.json:8`). There is no
`<meta http-equiv>` in `index.html`. A bundled Capacitor app is served from the
local WebView and never receives Vercel headers, so **the CSP does not apply
in-app** and cannot break it. The web app is unaffected by any mobile work.
Worth stating plainly given this repo's history — but no CSP change is needed.

### 7.3 Viewport / safe areas — already partly done
`index.html:5` already has `viewport-fit=cover`, the prerequisite for
`env(safe-area-inset-*)`. Good.

### 7.4 Build-time env var
`apiConfig.js:9-11` **throws** if `VITE_API_URL` is unset in a production build.
`npx cap sync` ships a `vite build` output, so `VITE_API_URL` must be present in
the local shell when building for native — otherwise the app hard-fails at
startup with no network error to diagnose.

### 7.5 File upload
`TranscriptUpload.jsx` / syllabus flows use a standard file input. Needs live
testing in the Android WebView; may need `@capacitor/filesystem` or a
`capacitor-file-picker` plugin if the native chooser misbehaves with PDFs.

### 7.6 Not in the plan, should be
- **Android hardware back button** (§4) — Play Store review risk.
- **Privacy policy URL** ✅ already exists: `symbolos.ca/privacy` via the
  `vercel.json:56` rewrite. Phase 5 prerequisite already satisfied.

---

## 8. Suggested sequencing (revision to Phase 1)

| # | Work | Parallel? |
|---|---|---|
| 0 | **Extract `DashboardDataProvider` from `Dashboard.jsx`** (§5.1) — no behavior change, own commit | ❌ blocking, solo |
| 1 | `useViewport()` @ 768px | ❌ |
| 2 | `<MobileLayout>` shell — bottom tabs, safe areas, nav stack, `data-tour` anchors (§5.2) | ❌ |
| 3 | Shell selection in `Dashboard` + back-stack wiring | ❌ |
| 4 | Level 1 CSS sweep: Landing, Login, Home, Forum, Profile cluster, Courses | ✅ subagents |
| 5 | Level 2 variants: Calendar (XL), Clubs (XL), Brief/AdvisorCards (L), DegreePlanning (L) | ✅ subagents, one per feature |
| 6 | RightSidebar collapse into Brief thread view | ✅ |

Bottom tab bar should carry **5 of the 8** tabs; the remaining 3 go into a "More"
sheet. Recommended primary five, based on the nav order and the tour's emphasis:
**Home · Brief · Courses · Calendar · Profile**, with Degree Planning, Clubs and
Forum under More. (Confirm — the plan guessed Advisor/Courses/Calendar/Forum/Profile,
which drops Home; Home is the default tab and the tour's first stop, so it should stay.)

---

## 9. Open questions for the developer

1. **Bottom-tab five** — confirm Home · Brief · Courses · Calendar · Profile, with
   Degree Planning / Clubs / Forum under "More"?
2. **§5.1 refactor** — approve extracting `Dashboard.jsx`'s data layer as a
   standalone, separately-reviewed commit before any mobile work?
3. **Password reset on native** (§6.2) — deep link, or add a code-based reset
   mirroring the existing signup OTP? The latter is more code but avoids App
   Links being on the critical path for launch.
4. **CORS change** (§7.1) — approve adding the Capacitor origins to
   `ALLOWED_ORIGINS`? Nothing works in-app without it.
5. **Calendar and Clubs are XL** and are the two genuine mobile rewrites. Is a
   reduced first version acceptable (Calendar = agenda list only, no month grid;
   Clubs = browse + detail, management deferred to desktop)?
6. **appId** — confirm `ca.symbolos.app`.
