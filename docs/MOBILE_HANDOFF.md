# Symbolos Mobile — Developer Handoff

**Branch:** `mobile-app` (18 commits ahead of `main`, pushed)
**Status:** web-side work complete and verified by build + tests. **Nothing has run on a real device or simulator.**
**Written:** 2026-07-20

You have a Mac. That is the thing this project has been blocked on. Almost everything in §6 needs one.

---

## 1. What this is

The Symbolos web frontend, wrapped in Capacitor as a native app, with a mobile-specific UI layer. **One codebase** — no second frontend. Only the *view* layer forks; API clients, contexts, hooks and Supabase session handling are shared.

**Decision: iOS-only for publishing.** 61% of users are iOS, 6% Android — ~91% of identified mobile. The Android project is still generated and committed because it costs nothing to keep and gives a free local debug target on Windows, but it is **not** being published. That drops the Google Play $25 fee and Google's 12-tester/14-day closed-testing requirement off the critical path entirely.

---

## 2. Getting it running

### Prerequisites

- **Node ≥ 20.12.** Non-negotiable — see §7.1, this will waste an hour if you miss it.
- Xcode + Command Line Tools.
- CocoaPods is **not** required. Capacitor 8 uses Swift Package Manager.

### First run

```bash
git fetch origin
git checkout mobile-app
cd frontend
npm install

# REQUIRED. apiConfig.js throws if this is missing in a production build,
# and `cap sync` copies whatever is in dist/ — so forgetting it produces an
# app that fails at startup with no useful error. See §7.2.
VITE_API_URL=https://ai-advisor-backend-seven.vercel.app npm run build

npx cap sync ios
npx cap open ios     # opens Xcode
```

In Xcode: select a simulator or your device, press Run. Bundle identifier is already `ca.symbolos.app`.

### After every frontend change

```bash
VITE_API_URL=... npm run build && npx cap sync ios
```

The app ships bundled assets — it does **not** load symbolos.ca at runtime. Without `cap sync` you are testing a stale build. Rationale in `docs/adr/0003-capacitor-bundled-web-assets.md`.

---

## 3. Architecture you should not accidentally undo

### 3.1 Viewport vs platform — the important one

| Helper | Question | Drives |
|---|---|---|
| `useViewport()` (`hooks/useViewport.js`) | is this screen phone-sized? (≤768px) | **all layout** |
| `isNativeApp()` (`lib/platform.js`) | are we inside the installed app? | landing skip, deep links, push, status bar |

Layout switches on **viewport**, never platform, so mobile *web* visitors get the same UI as app users. A lot of traffic arrives from r/mcgill on phones and must not get a desktop layout crammed onto a phone.

Using `isNativeApp()` for a layout decision would silently hand mobile web visitors the desktop experience. There is currently exactly **one** legitimate use: skipping the marketing landing page inside the app.

### 3.2 The shell split

```
Dashboard.jsx
├── DashboardDataProvider      all data + business logic (contexts/DashboardDataContext.jsx)
└── DashboardShell             picks by viewport
    ├── MobileLayout           bottom tab bar, full-screen pages
    └── DesktopDashboard       sidebar, right sidebar, onboarding tour
        └── both render DashboardTabContent  (the 8 screens, shared)
```

`Dashboard.jsx` used to be 1085 lines owning data *and* layout. It was split so a mobile shell could consume the data without duplicating it. **Don't put data or fetching back into either shell.**

**Bottom tabs:** Home · Brief · Degree Planning · Calendar · Profile. Courses, Clubs and Forum live in the "More" sheet. There is a test asserting the secondary three stay out of the bar.

### 3.3 Desktop must not change

Every mobile change is inside `@media (max-width: 768px)` or gated on `isMobile`. Some screens (`HomeTab`, `Login`) return an entirely separate mobile tree, which is a stronger guarantee. `MobileAuth` deliberately touches no `Auth.css` rule at all.

**This is the single easiest thing to break.** symbolos.ca has real users on desktop right now.

### 3.4 Native styling primitives

`components/Dashboard/MobileLayout.css` defines `.m-group`, `.m-row`, `.m-group-label`, `.m-push-enter/exit` and `--m-*` tokens. Screens style themselves from these. They are scoped to `.mobile-shell`, so **they do not resolve on the auth screens**, which define their own equivalents locally.

If you add a screen, use the primitives. See §8.1 — there is known drift because three agents built screens in parallel before some primitives existed.

---

## 4. Project invariants (from CLAUDE.md — still apply)

- **i18n:** every user-facing string goes through `t()`, with keys in **all three** of `locales/en.js`, `fr.js`, `zh.js`. A key present in one and missing in another renders the raw key string to users. `t()` does not fall back to English.
- **No emojis in UI.** `react-icons` only. Backend-generated advisor-card `icon` values must be mapped to a react-icon before rendering.
- **Security:** every new route takes `Depends(get_current_user_id)` + `require_self()`. New tables need RLS.
- **PII:** transcripts are redacted *before* the Claude call; scanned PDFs are refused, never sent un-redacted. Keep all three layers working.
- **Never commit** `.env` files, keys, keystores or signing credentials. `.gitignore` already covers Android/iOS signing material and build output.

---

## 5. Environment gotchas that will cost you time

### 5.1 Node version
The repo's default Node here is **v19.9.0**. Vitest dies at startup with:
```
SyntaxError: The requested module 'node:util' does not provide an export named 'styleText'
```
`styleText` landed in Node 20.12. Use Node ≥ 20.12 (verified on v24.17.0). Three separate agents hit this and each initially thought they'd broken the suite. **Adding `.nvmrc` or a `package.json` `engines` field is a worthwhile 5-minute fix.**

### 5.2 `VITE_API_URL`
Throws if missing in a production build. Symptom of forgetting it: app launches to a blank screen with no useful error.

### 5.3 CORS
`ALLOWED_ORIGINS` is set as an **environment variable in the backend Vercel project** — the value in `backend/api/config.py` is only a default and is ignored in production. Currently allowed:

```
http://localhost:5173
https://ai-advisor-pi.vercel.app
https://symbolos.ca
capacitor://localhost
https://localhost
https://ai-advisor-git-mobile-app-damianphims-projects.vercel.app
```

⚠️ **`capacitor://localhost` is still rejected in production.** The env var lists it, but the deployed backend runs the *old* origin validator which only accepts `http`/`https` schemes and silently discards anything else. The fix is on this branch (`backend/api/config.py`) and takes effect when it merges. **Until then the iOS app cannot reach the API.** This is the first thing to check if every request fails in the simulator.

Android's origin is `https://localhost`, which *is* allowed today — so Android works before the merge and iOS doesn't.

### 5.4 Preview deployments
Branch alias: `https://ai-advisor-git-mobile-app-damianphims-projects.vercel.app`

Auto-updates on every push. Do **not** use the per-deployment hash URLs (`ai-advisor-7v557es6i-…`) — they change every deploy and aren't allowlisted for CORS.

Vercel **Deployment Protection** is on, so the preview requires a Vercel login. You'll need access to the team.

`?native=1` on a preview forces the native code path in a browser so you can see app-only screens. Hard-gated on hostname — inert on symbolos.ca. `?native=0` clears it.

---

## 6. What has never been tested — your job

Everything below was written against the spec and verified only by `npm run build` and `npm run test`. **No pixel has been seen on a device.** This is the highest-value part of the handoff.

### 6.1 Never run natively at all
- [ ] App launches, splash → welcome screen
- [ ] Safe-area insets under a real notch / Dynamic Island (top *and* bottom)
- [ ] Status bar style and colour against the app background
- [ ] Keyboard: chat composer, all five auth screens. CSS-only handling today — `@capacitor/keyboard` is **not** installed (Phase 3)
- [ ] **Transcript / syllabus PDF upload through the WebView file picker.** Highest-risk unknown. May need `@capacitor/filesystem` or a file-picker plugin
- [ ] Back-swipe gesture behaviour
- [ ] Deep links — not implemented at all yet (Phase 3)

### 6.2 Visual, reasoned but never seen
- [ ] Calendar agenda: sticky day headers under scroll (depends on `.mobile-content` being the *only* scroller — do not add a nested one)
- [ ] Brief: card → thread push transition, and the thread overlay's z-index against the tab bar (thread is 150, bar is 100, More sheet is 130)
- [ ] Degree Requirements: list → detail push
- [ ] 360px width (iPhone SE) across every screen
- [ ] Dark mode across every new mobile surface
- [ ] **French and Chinese.** A French label overflowing every phone was a real bug found here — English-only testing masks a whole class of layout failure

### 6.3 Full regression, in-app
signup → email verify (use the **6-digit OTP**, not the link — see §8.3) → login → chat with advisor → transcript upload → course explorer → calendar → forum → account deletion.

### 6.4 Regression the other way
Desktop web and mobile web on this branch. Nothing may break for existing users. This is the one that matters most commercially.

---

## 7. Remaining work (Phase 3)

Not started, all code-side:

1. **Deep links** for Supabase auth. Email verification can ship without them (OTP path, §8.3). Password reset genuinely needs them *or* the code-based reset in §8.2.
2. **`@capacitor/status-bar`** — style/colour.
3. **`@capacitor/keyboard`** — proper inset handling, replacing the CSS-only approach.
4. **Code-based password reset** (decided, not built). Mirrors the signup OTP so App Links stay off the launch critical path.
5. **Push notifications** — explicitly deferred, do not build now.

---

## 8. Known issues and follow-ups

Accumulated during the work. None are blockers; all are real.

### 8.1 Mobile primitive drift
Three screens were built in parallel before some primitives existed, so a disclosure chevron, a press-feedback treatment, a group-gap value and a segmented control were each reinvented 2–4 times with slightly different values. Consolidating into `MobileLayout.css` and refactoring screens onto them is the single best cleanup for perceived polish.

### 8.2 `mode='reset'` in `Login.jsx` is dead code
Nothing sets it. Real recovery goes `PASSWORD_RECOVERY` → `symbolos_open_pw_change` → Settings modal, never reaching `Login`. It currently renders as a degenerate signup form on both desktop and mobile. This is where the code-based reset (§7.4) should probably live.

### 8.3 Email verification relies on the OTP path
McGill inboxes run Microsoft 365 Safe Links, which auto-fetches emailed confirmation links seconds after delivery — consuming them before the student clicks. The **6-digit typed code** is the reliable path; link-click and polling are fallbacks. Don't "simplify" it away. It's also why the app can ship without deep links.

### 8.4 CSS leakage in Courses
`CoursesTab.css` declares unscoped `.course-card`, `.course-header`, `.course-title`, `.course-code`, `.vsb-banner`, `.empty-state`. Because `CoursesView` keeps the search panel mounted (`display:none`) so search state survives, those rules are live on the My Courses screen and were overriding its scoped styles. Fixed on mobile; **still wrong on desktop** (right-aligned action pills + a double divider, contradicting that file's own comment). `.empty-state` also collides globally with `ProfileTab.css`.

### 8.5 Remaining i18n gaps
- `Forum.jsx` `SECTIONS[].label` is a hardcoded English array literal — forum tab names render in English for FR/ZH users, visibly and to screen readers.
- `zh.js` is missing ~18 keys, `fr.js` 1 (mostly `clubs.*` around the manage dashboard). Pre-existing.
- `ClubsTab.jsx` references `clubs.manage.joinLink`, which exists in **no** locale file — renders the raw key today.
- `auth.resendSuccess` exists but isn't wired (the string lives in a handler shared with desktop).
- Some French/Chinese translations of McGill credential names (`B.G.E.`, `B.Sc.(Arch.)`) were left as the English abbreviation; `Honours` → `Spécialisation` is a guess. Worth a native check.

### 8.6 Accessibility
Fixed: forum section tabs, modal close, search clear, delete/report now have accessible names.
Outstanding: `RatingPicker` stars announce bare "1".."5" with an unnamed radiogroup; like buttons' accessible name is just the number.

### 8.7 Tooling
`npm run lint` fails — `@eslint/js` isn't installed. `npx eslint --format json` works.

---

## 9. Store prerequisites (iOS)

- [ ] **Apple Developer Program — $99/year.** Enrolment has lead time; start it early.
- [ ] Screenshots (needs a running app), app icon, description
- [ ] App Privacy labels
- [ ] Age rating questionnaire
- [x] Privacy policy URL — `symbolos.ca/privacy` exists
- [x] In-app account deletion — Apple **requires** it for apps with account creation; already built
- [x] Sign in with Apple — only required if offering third-party social login. Supabase email/password, so exempt

**Two review risks:**

- **Guideline 4.2 "minimum functionality"** — wrapped web apps get rejected as "just a website." This is why the app ships bundled assets rather than loading symbolos.ca, and why native integrations should be done properly rather than minimally.
- **McGill branding.** Both stores scrutinise apps implying institutional affiliation, Apple more so. The "Not affiliated with McGill University" disclaimer exists in-app — **put it in the store listing description too.** Worst case is a rejection demanding written permission from the university.

Going iOS-only means a rejection blocks you completely; there's no Android release to fall back on.

---

## 10. Rules of engagement

- **Never push to `main` without Damian's explicit approval.** Vercel auto-deploys `main` to production on every push. Real users.
- Work on `mobile-app` or a branch off it.
- Never commit secrets, keystores or `.env` files.
- Run `npm run test` (59 tests) and `npm run build` before pushing.
- If you change a Capacitor config or add a plugin, run `npx cap sync` and commit the native project changes.
