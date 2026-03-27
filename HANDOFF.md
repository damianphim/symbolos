# Symbolos Session Handoff — March 25, 2026

## Project Overview
**Symbolos** — Full-stack McGill student advisor platform
- **Frontend**: React 19 + Vite (port 5173)
- **Backend**: FastAPI (port 8000)
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Vercel

## Login Credentials (Test Account)
- Email: `alexander.duda@mail.mcgill.ca`
- Password: `Quebec12`

## How to Run Locally
```bash
# Backend (from project root):
cd /Users/alexanderduda/ai-advisor
env $(cat .env | grep -v '^#' | xargs) uvicorn api.main:app --reload --port 8000

# Frontend (from frontend/):
cd /Users/alexanderduda/ai-advisor/frontend
npm run dev
```

---

## PENDING TASKS (in priority order)

### 1. Club Buttons & Join System Enhancement
**User request**: "Make sure the club buttons work, and for join a club make sure the clubs creators have a section to include instructions for how to apply or join the club, or just a straight link to somewhere."

**Current state**:
- Subscribe button: toggles subscription (POST `/api/clubs/{id}/subscribe`) — working
- Join Club button: links to `website_url` if present, disabled otherwise — **needs enhancement**
- **MISSING**: No `join_instructions` or `application_url` field in clubs table
- **MISSING**: No way for club owners to write custom join instructions

**What needs to happen**:
1. Add `join_instructions TEXT` and `application_url TEXT` columns to `clubs` table (SQL migration)
2. Add these fields to `ClubSubmission` and `UpdateClubRequest` Pydantic models in `backend/api/routes/clubs.py`
3. Add these fields to the club submission form in `ClubsTab.jsx`
4. Add these fields to the Edit Info tab in `ClubManageDashboard` component
5. Display join instructions in `ClubDetailDrawer` when user clicks "Join Club"
6. If `application_url` is set, the "Join Club" button should link there instead of `website_url`

### 2. Club Management Dashboard — Verify & Polish
**User request**: "Have owners be able to manage their clubs in an easy interface, so that they can create events and announcements for subscribers."

**Current state**: `ClubManageDashboard` component EXISTS in ClubsTab.jsx (~line 55-300ish) with 5 tabs:
- Overview (stats)
- Edit Info
- Managers (add/remove by email)
- Announcements (create/delete)
- Events (create/delete)

**What needs to happen**:
- Test that all 5 tabs work end-to-end
- Verify events/announcements reach subscribers
- Add `join_instructions` and `application_url` to the Edit Info tab
- Ensure the "Manage" button (FaCog icon) on `CreatedClubRow` properly opens the dashboard

### 3. Add AI Disclaimers to Missing Locations
**User request**: "Make sure the double check message is at all points in the website where information is generated... better message than what I wrote, but keep it short and simple, no icons"

**Already has disclaimer**:
- `RightSidebar.jsx` (chat sidebar) — has `rsb.disclaimer` translation key
- `TranscriptUpload.jsx` — has AI accuracy warning (BUT still uses FaExclamationTriangle icon — REMOVE IT)

**MISSING disclaimer at these locations**:
1. `frontend/src/components/Dashboard/chat/AdvisorCards.jsx` (~794 lines) — Main AI briefing cards on Chat tab
2. `frontend/src/components/Dashboard/DegreePlanningView.jsx` (~1305 lines) — AI elective recommendations section (~line 450-478)
3. `frontend/src/components/Dashboard/DegreeRequirementsView.jsx` (~720 lines) — AI course recommendation badges (~line 675-683)

**How to implement**:
- Create a short, improved disclaimer message (no icons, no emojis)
- Something like: "Always verify AI-generated information with official McGill sources"
- Add as a small muted text below AI content in each location
- Use the `t('rsb.disclaimer')` translation key or create a shared one
- Remove `FaExclamationTriangle` icon from TranscriptUpload.jsx disclaimer

### 4. Review Emir's Requirements
**User request**: "Review what emir messaged me to make sure the website implements that properly"

**Emir's known requests** (from conversation history):
1. ✅ Transcript import fix (JSON endpoint avoids Vercel timeout)
2. ✅ Club submission confirmation toast
3. ✅ McGill email requirement for club submission
4. ✅ Sidebar chat improvements (tab-aware, pinning, site knowledge)
5. ✅ Card deduplication (W/F grades filtered when course later passed)
6. ✅ Professor recommendations in AI cards
7. ⚠️ Club management dashboard (exists but needs testing)
8. ⚠️ Multi-manager clubs (backend + frontend exist, needs testing)
9. ⚠️ Subscribe to club events (button exists, needs testing)
10. 🔲 Join instructions for clubs (not yet implemented — see Task 1)

### 5. Test Emir's Transcript Upload
- PDF location: `/Users/alexanderduda/Library/Mobile Documents/com~apple~CloudDocs/Emir UNOFFICIAL Transcript for ID.pdf`
- Test on the alexander.duda@mail.mcgill.ca account (do NOT delete the account)
- Upload via Degree Planning tab → Transcript Upload
- Verify parsed data looks correct
- Verify the AI accuracy warning appears before confirm

### 6. Full Bug Sweep
Test all additions made in recent sessions:
- [ ] Card language switching (EN/FR/ZH) — cards should match selected language
- [ ] Club Subscribe button toggles correctly with toast
- [ ] Club Join button links to website_url or application_url
- [ ] Club management dashboard (all 5 tabs)
- [ ] Club creation requires @mail.mcgill.ca email
- [ ] Sidebar chat: per-tab conversation persistence
- [ ] Sidebar chat: message pinning (localStorage)
- [ ] Sidebar chat: correct site knowledge answers
- [ ] Transcript upload + import (JSON endpoint)
- [ ] "Not affiliated with McGill" text above user profile in left sidebar
- [ ] Disclaimers at all AI content points
- [ ] No console errors

---

## KEY FILE LOCATIONS & LINE COUNTS

### Frontend
| File | Lines | Purpose |
|------|-------|---------|
| `frontend/src/components/Dashboard/ClubsTab.jsx` | 1915 | Club browsing, detail drawer, management dashboard |
| `frontend/src/components/Dashboard/ClubsTab.css` | ~800 | Club styles including management dashboard |
| `frontend/src/components/Dashboard/CalendarTab.jsx` | ~1300 | Calendar with club events integration |
| `frontend/src/components/Dashboard/chat/AdvisorCards.jsx` | 794 | AI briefing cards (NEEDS DISCLAIMER) |
| `frontend/src/components/Dashboard/DegreePlanningView.jsx` | 1305 | Degree planning + AI elective recs (NEEDS DISCLAIMER) |
| `frontend/src/components/Dashboard/DegreeRequirementsView.jsx` | 720 | Degree requirements + AI recs (NEEDS DISCLAIMER) |
| `frontend/src/components/Dashboard/RightSidebar.jsx` | 484 | Chat sidebar (has disclaimer) |
| `frontend/src/components/Dashboard/TranscriptUpload.jsx` | 401 | Transcript/syllabus upload (has disclaimer but REMOVE ICON) |
| `frontend/src/components/Dashboard/Settings.jsx` | 540 | User settings/profile |
| `frontend/src/components/Dashboard/Sidebar.jsx` | 195 | Left navigation sidebar |
| `frontend/src/lib/clubsAPI.js` | 300 | Club API client |
| `frontend/src/contexts/LanguageContext.jsx` | ~1200 | EN/FR/ZH translations |

### Backend
| File | Lines | Purpose |
|------|-------|---------|
| `backend/api/routes/clubs.py` | 1757 | All club endpoints |
| `backend/api/routes/cards.py` | ~400 | AI advisor cards |
| `backend/api/routes/chat.py` | ~300 | Chat with site knowledge |
| `backend/api/routes/transcript.py` | ~250 | Transcript parse + import |
| `backend/api/main.py` | ~100 | FastAPI app + router registration |

### SQL Migrations (already applied to Supabase)
| File | Purpose |
|------|---------|
| `sql/add_club_subscriptions.sql` | club_subscriptions + club_managers tables |
| `sql/add_is_honours.sql` | is_honours column |
| `sql/newsletter_tables.sql` | Newsletter system tables (planned, may not be applied yet) |

---

## ARCHITECTURE NOTES

### Auth Pattern
- Backend `/api/auth/flags` returns `{is_admin, is_mcgill_email}`
- `ADMIN_EMAILS` env var (set in Vercel) controls admin access
- Supabase JWT auth via `Authorization: Bearer <token>` header

### Club System Architecture
- **Public clubs**: Anyone can join directly
- **Private clubs**: Join request → owner approves/denies
- **Subscribe**: Get event/announcement notifications without joining
- **Managers**: Separate from members, managed via `club_managers` table
- **Events**: Appear on subscribers' calendars if calendar_synced
- **Announcements**: Email notifications to members via Resend API

### AI Card System
- Cards generated by Claude API based on student context (courses, profile, interests)
- Cached per-language in localStorage: `advisor_cards_{userId}_{lang}`
- Retranslation uses `system` parameter for language instruction
- `_deduplicate_completed()` filters W/F grades when course later passed

### Translation System
- `LanguageContext.jsx` has EN/FR/ZH translations
- `t('key.path')` function for lookups
- All UI text should use translation keys

---

## IMPORTANT CONTEXT
- User explicitly said: "only use react icons, but don't put icons for those buttons" (Subscribe/Join Club)
- User explicitly said: "no icons" for disclaimers
- User said to approach like a "senior software developer"
- The "Not affiliated with McGill University" notice is in the LEFT sidebar (Sidebar.jsx), above the user profile button
- Club submission requires @mail.mcgill.ca email (admins exempt)
- Newsletter system was planned (see plan file at `~/.claude/plans/lucky-swimming-adleman.md`) but may not be fully implemented yet

## ENV VARS
- `.env` file in project root has all backend secrets (Supabase, Claude API, Resend, etc.)
- Vercel has `ADMIN_EMAILS` set
