/**
 * Characterization tests for ClubsTab.jsx, written before refactoring it
 * (see docs/adr/0001-incremental-test-first-refactor.md). These pin down
 * CURRENT behavior, including some that's dead code rather than intended
 * design — see the "dead join flow" tests below.
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ClubsTab, { buildClubCalendarEvents } from './ClubsTab'

vi.mock('../../lib/clubsAPI', () => ({
  default: {
    getClubs: vi.fn(),
    getStarterClubs: vi.fn(),
    getUserClubs: vi.fn(),
    getCreatedClubs: vi.fn(),
    joinClub: vi.fn(),
    leaveClub: vi.fn(),
    getUserPendingRequests: vi.fn(),
    toggleCalendarSync: vi.fn(),
    submitClub: vi.fn(),
    editClub: vi.fn(),
    getJoinRequests: vi.fn(),
    handleJoinRequest: vi.fn(),
    deleteClub: vi.fn(),
    getClubMembers: vi.fn(),
    removeClubMember: vi.fn(),
    updateMemberRole: vi.fn(),
    getSubscribedClubEvents: vi.fn(),
    createClubEvent: vi.fn(),
    deleteClubEvent: vi.fn(),
    getSubscribedClubAnnouncements: vi.fn(),
    createClubAnnouncement: vi.fn(),
    deleteClubAnnouncement: vi.fn(),
    getCategories: vi.fn(),
    toggleSubscription: vi.fn(),
    getUserSubscriptions: vi.fn(),
    createManagerRequest: vi.fn(),
    getIncomingManagerRequests: vi.fn(),
    respondToManagerRequest: vi.fn(),
    getClubActivity: vi.fn(),
    getClubFacultyStats: vi.fn(),
    uploadClubLogo: vi.fn(),
    getClubManagers: vi.fn(),
    removeClubManager: vi.fn(),
  },
}))

vi.mock('../../contexts/AuthContext', () => ({
  useAuth: vi.fn(),
}))

vi.mock('../../contexts/PreferencesContext', () => ({
  useLanguage: vi.fn(),
}))

import clubsAPI from '../../lib/clubsAPI'
import { useAuth } from '../../contexts/AuthContext'
import { useLanguage } from '../../contexts/PreferencesContext'

const USER = { id: 'user-1', email: 'student@mail.mcgill.ca' }

function makeClub(overrides = {}) {
  return {
    id: 'club-1',
    name: 'HackMcGill',
    category: 'Engineering & Technology',
    description: 'A hackathon club.',
    is_private: false,
    created_by: 'owner-1',
    ...overrides,
  }
}

function setDefaultMocks() {
  clubsAPI.getClubs.mockResolvedValue({ clubs: [], count: 0 })
  clubsAPI.getUserClubs.mockResolvedValue({ clubs: [], count: 0 })
  clubsAPI.getCreatedClubs.mockResolvedValue({ clubs: [], count: 0 })
  clubsAPI.getCategories.mockResolvedValue({ categories: [] })
  clubsAPI.getUserPendingRequests.mockResolvedValue({ pending_club_ids: [] })
  clubsAPI.getIncomingManagerRequests.mockResolvedValue({ requests: [], count: 0 })
  clubsAPI.getUserSubscriptions.mockResolvedValue({ subscribed_club_ids: [] })
  clubsAPI.getClubActivity.mockResolvedValue({ items: [], count: 0 })
  clubsAPI.getClubFacultyStats.mockResolvedValue({ your_faculty: null, your_faculty_count: 0, by_faculty: [], total: 0 })
  clubsAPI.getJoinRequests.mockResolvedValue({ requests: [], count: 0 })
  clubsAPI.getClubManagers.mockResolvedValue({ managers: [], count: 0 })
  clubsAPI.getClubMembers.mockResolvedValue({ members: [], count: 0 })
}

beforeEach(() => {
  vi.clearAllMocks()
  setDefaultMocks()
  useAuth.mockReturnValue({ profile: {} })
  useLanguage.mockReturnValue({ t: (key) => key, language: 'en' })
  // ClubManageDashboard does one raw `fetch` (subscriber count) outside
  // clubsAPI — stub it so tests don't attempt a real network call.
  global.fetch = vi.fn().mockResolvedValue({ ok: false, json: async () => ({}) })
})

afterEach(() => {
  vi.restoreAllMocks()
})

function renderTab(props = {}) {
  return render(<ClubsTab user={USER} authFlags={{ is_admin: false, is_mcgill_email: true }} {...props} />)
}

// ── buildClubCalendarEvents (pure function) ───────────────────────────────────

describe('buildClubCalendarEvents', () => {
  it('skips memberships that are not calendar_synced', () => {
    const events = buildClubCalendarEvents([
      { calendar_synced: false, club: { id: 'c1', name: 'Club', meeting_schedule: 'Mondays at 5pm' } },
    ])
    expect(events).toEqual([])
  })

  it('skips clubs with TBD/varies schedules', () => {
    const events = buildClubCalendarEvents([
      { calendar_synced: true, club: { id: 'c1', name: 'Club', meeting_schedule: 'TBD' } },
    ])
    expect(events).toEqual([])
  })

  it('skips schedules with no recognizable day of week', () => {
    const events = buildClubCalendarEvents([
      { calendar_synced: true, club: { id: 'c1', name: 'Club', meeting_schedule: 'Sometime soon' } },
    ])
    expect(events).toEqual([])
  })

  it('parses a weekly day + time into 8 weeks of events', () => {
    const events = buildClubCalendarEvents([
      { calendar_synced: true, club: { id: 'c1', name: 'Club', meeting_schedule: 'Mondays at 5:30pm' } },
    ])
    expect(events.length).toBe(8)
    expect(events[0].time).toBe('17:30')
    expect(events.every(e => e.clubId === 'c1' && e.readOnly === true)).toBe(true)
  })

  it('halves event count for biweekly schedules', () => {
    const events = buildClubCalendarEvents([
      { calendar_synced: true, club: { id: 'c1', name: 'Club', meeting_schedule: 'Biweekly on Tuesdays' } },
    ])
    expect(events.length).toBe(4)
  })

  it('produces one event per matched day when multiple days are listed', () => {
    const events = buildClubCalendarEvents([
      { calendar_synced: true, club: { id: 'c1', name: 'Club', meeting_schedule: 'Mondays and Wednesdays' } },
    ])
    expect(events.length).toBe(16)
  })
})

// ── Explore view: listing, search, category filter ───────────────────────────

describe('ClubsTab explore view', () => {
  it('renders clubs returned by getClubs', async () => {
    clubsAPI.getClubs.mockResolvedValue({ clubs: [makeClub()], count: 1 })
    renderTab()
    await waitFor(() => expect(screen.getByText('HackMcGill')).toBeInTheDocument())
  })

  it('shows the empty state when no clubs are returned', async () => {
    renderTab()
    await waitFor(() => expect(clubsAPI.getClubs).toHaveBeenCalled())
    expect(screen.getByText('clubs.noClubsYet')).toBeInTheDocument()
  })

  it('debounces search input before calling getClubs with the search term', async () => {
    clubsAPI.getClubs.mockResolvedValue({ clubs: [], count: 0 })
    renderTab()
    await waitFor(() => expect(clubsAPI.getClubs).toHaveBeenCalledTimes(1))

    const input = screen.getByPlaceholderText('clubs.searchPlaceholder')
    await userEvent.type(input, 'Hack')

    // Not called again immediately — still debouncing.
    expect(clubsAPI.getClubs).toHaveBeenCalledTimes(1)

    await waitFor(() =>
      expect(clubsAPI.getClubs).toHaveBeenCalledWith(expect.objectContaining({ search: 'Hack' }))
    )
  })

  it('clicking a category pill refetches with that category', async () => {
    clubsAPI.getCategories.mockResolvedValue({ categories: ['Academic'] })
    clubsAPI.getClubs.mockResolvedValue({ clubs: [], count: 0 })
    renderTab()
    const pill = await screen.findByText('clubs.catAcademic')
    await userEvent.click(pill)
    await waitFor(() =>
      expect(clubsAPI.getClubs).toHaveBeenCalledWith(expect.objectContaining({ category: 'Academic' }))
    )
  })
})

// ── Non-creator manager (club_managers admin) sees Manage controls ───────────

describe('non-creator manager privileges carry over to the Explore grid', () => {
  it('shows the Manage button/crown on an admin-managed club card in Explore, not Subscribe/Join', async () => {
    // The club is owned by someone else, but the current user manages it via
    // an accepted manager invite — surfaced by getCreatedClubs() with
    // _manage_role: 'admin'. It also shows up in the plain getClubs() list
    // (which never carries _manage_role) because it's rendered in Explore too.
    const club = makeClub({ id: 'club-1', created_by: 'owner-1' })
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    clubsAPI.getCreatedClubs.mockResolvedValue({ clubs: [{ ...club, _manage_role: 'admin' }], count: 1 })
    renderTab()

    await screen.findByText('HackMcGill')

    expect(screen.getByText('clubs.manageBtnShort')).toBeInTheDocument()
    expect(screen.getByText('clubs.adminBadge')).toBeInTheDocument()
    expect(screen.queryByText('clubs.joinClub')).not.toBeInTheDocument()
    expect(screen.queryByLabelText('Subscribe for updates')).not.toBeInTheDocument()
  })
})

// ── Dead join flow (characterization of current — unreachable — behavior) ────

describe('the "join a club" flow is unreachable from the rendered UI', () => {
  it('clicking "Join Club" on a card with join_instructions opens the drawer, not the join API', async () => {
    const club = makeClub({ join_instructions: 'Show up to our first meeting.', application_url: null })
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    renderTab()
    await screen.findByText('HackMcGill')

    const joinButtons = screen.getAllByText('clubs.joinClub')
    await userEvent.click(joinButtons[0])

    // The drawer opened (back button + the section heading for join
    // instructions both appear), and the join API was never called.
    expect(await screen.findByText('clubs.howToJoin')).toBeInTheDocument()
    expect(clubsAPI.joinClub).not.toHaveBeenCalled()
  })

  it('a club with only an application_url renders a plain external link, not a join button', async () => {
    const club = makeClub({ application_url: 'https://example.com/apply', join_instructions: null })
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    renderTab()
    await screen.findByText('HackMcGill')

    const link = screen.getAllByText('clubs.joinClub')[0].closest('a')
    expect(link).toHaveAttribute('href', 'https://example.com/apply')
    expect(clubsAPI.joinClub).not.toHaveBeenCalled()
  })
})

// ── Leaving / calendar sync / subscribe (these ARE wired up) ─────────────────

describe('leave, calendar sync, and subscribe — actually-wired interactions', () => {
  it('clicking Leave on a joined club calls leaveClub', async () => {
    const club = makeClub()
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    clubsAPI.getUserClubs.mockResolvedValue({ clubs: [{ club, calendar_synced: false }], count: 1 })
    clubsAPI.leaveClub.mockResolvedValue({ success: true })
    renderTab()
    await screen.findByText('HackMcGill')

    await userEvent.click(screen.getByText('clubs.leave'))
    await waitFor(() => expect(clubsAPI.leaveClub).toHaveBeenCalledWith(USER.id, club.id))
  })

  it('toggling calendar sync on a joined club calls toggleCalendarSync', async () => {
    const club = makeClub()
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    clubsAPI.getUserClubs.mockResolvedValue({ clubs: [{ club, calendar_synced: false }], count: 1 })
    clubsAPI.toggleCalendarSync.mockResolvedValue({ success: true, calendar_synced: true })
    renderTab()
    await screen.findByText('HackMcGill')

    await userEvent.click(screen.getByText('clubs.calOff'))
    await waitFor(() =>
      expect(clubsAPI.toggleCalendarSync).toHaveBeenCalledWith(USER.id, club.id, true)
    )
  })

  it('clicking the subscribe bell on a non-joined club calls toggleSubscription', async () => {
    const club = makeClub()
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    clubsAPI.toggleSubscription.mockResolvedValue({ success: true, is_subscribed: true })
    renderTab()
    await screen.findByText('HackMcGill')

    await userEvent.click(screen.getByLabelText('Subscribe for updates'))
    await waitFor(() => expect(clubsAPI.toggleSubscription).toHaveBeenCalledWith(club.id))
  })
})

// ── Submit-a-club modal ────────────────────────────────────────────────────────

describe('SubmitClubModal', () => {
  it('blocks submission without a join method (application URL, instructions, or website)', async () => {
    renderTab()
    await userEvent.click(screen.getByText('clubs.requestAddBtn'))

    await userEvent.type(screen.getByPlaceholderText('clubs.fieldNamePlaceholder'), 'New Club')
    await userEvent.type(screen.getByPlaceholderText('clubs.fieldDescPlaceholder'), 'A description.')
    await userEvent.click(screen.getByText('clubs.submitClub'))

    expect(clubsAPI.submitClub).not.toHaveBeenCalled()
    expect(screen.getByText(/at least one/i)).toBeInTheDocument()
  })

  it('submits with name, description, and a join method', async () => {
    clubsAPI.submitClub.mockResolvedValue({ success: true })
    renderTab()
    await userEvent.click(screen.getByText('clubs.requestAddBtn'))

    await userEvent.type(screen.getByPlaceholderText('clubs.fieldNamePlaceholder'), 'New Club')
    await userEvent.type(screen.getByPlaceholderText('clubs.fieldDescPlaceholder'), 'A description.')
    // First "https://..." field is website_url, which also counts as a
    // valid join method per SubmitClubModal's validate().
    await userEvent.type(screen.getAllByPlaceholderText('https://...')[0], 'https://example.com')
    await userEvent.click(screen.getByText('clubs.submitClub'))

    await waitFor(() =>
      expect(clubsAPI.submitClub).toHaveBeenCalledWith(
        expect.objectContaining({ name: 'New Club', description: 'A description.', submitted_by: USER.id })
      )
    )
  })
})

// ── Manager invite inbox ──────────────────────────────────────────────────────

describe('manager invite inbox', () => {
  const invite = {
    id: 'inv-1',
    clubs: { name: 'Debate Society', category: 'Debate & Politics' },
    requested_by_name: 'Pat',
    message: 'Join us!',
  }

  it('renders a pending invite and accepting it calls respondToManagerRequest', async () => {
    clubsAPI.getIncomingManagerRequests.mockResolvedValue({ requests: [invite], count: 1 })
    clubsAPI.respondToManagerRequest.mockResolvedValue({ ok: true, status: 'accepted' })
    renderTab()

    await userEvent.click(screen.getByText('clubs.tabMine'))
    await screen.findByText('Debate Society')
    expect(screen.getByText('Pat')).toBeInTheDocument()

    await userEvent.click(screen.getByText('clubs.accept'))
    await waitFor(() =>
      expect(clubsAPI.respondToManagerRequest).toHaveBeenCalledWith('inv-1', 'accept')
    )
    // Optimistic removal from the inbox.
    expect(screen.queryByText('Debate Society')).not.toBeInTheDocument()
  })

  it('denying an invite calls respondToManagerRequest with deny', async () => {
    clubsAPI.getIncomingManagerRequests.mockResolvedValue({ requests: [invite], count: 1 })
    clubsAPI.respondToManagerRequest.mockResolvedValue({ ok: true, status: 'denied' })
    renderTab()

    await userEvent.click(screen.getByText('clubs.tabMine'))
    await screen.findByText('Debate Society')
    await userEvent.click(screen.getByText('clubs.deny'))

    await waitFor(() =>
      expect(clubsAPI.respondToManagerRequest).toHaveBeenCalledWith('inv-1', 'deny')
    )
  })
})

// ── ClubManageDashboard: add-manager flow (cross-checks the backend fix) ─────

describe('ClubManageDashboard manager invite flow', () => {
  it('adding a manager calls createManagerRequest, not the deleted add_club_manager endpoint', async () => {
    const club = makeClub({ created_by: USER.id })
    clubsAPI.getCreatedClubs.mockResolvedValue({ clubs: [club], count: 1 })
    clubsAPI.createManagerRequest.mockResolvedValue({ ok: true })
    renderTab()

    await userEvent.click(screen.getByText('clubs.tabMine'))
    await screen.findByText('HackMcGill')
    await userEvent.click(screen.getByText('clubs.manage.btn'))

    await userEvent.click(screen.getByText('clubs.manage.execs'))
    const emailInput = screen.getByPlaceholderText('clubs.manage.addManagerPlaceholder')
    await userEvent.type(emailInput, 'newmanager@mail.mcgill.ca')
    await userEvent.click(screen.getByText('clubs.manage.addBtn'))

    await waitFor(() =>
      expect(clubsAPI.createManagerRequest).toHaveBeenCalledWith(club.id, 'newmanager@mail.mcgill.ca')
    )
    // The endpoint behind this was deleted in the backend refactor (docs/adr/0002) —
    // confirm the frontend never tries to call it.
    expect(clubsAPI).not.toHaveProperty('addClubManager')
  })
})

// ── Admin: delete club (typed confirmation) ───────────────────────────────────

describe('admin delete club', () => {
  it('does not call deleteClub if the confirmation prompt text does not match "delete"', async () => {
    const club = makeClub()
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    vi.spyOn(window, 'prompt').mockReturnValue('nope')
    renderTab({ authFlags: { is_admin: true } })
    await screen.findByText('HackMcGill')

    await userEvent.click(screen.getByTitle('clubs.deleteClub'))
    expect(clubsAPI.deleteClub).not.toHaveBeenCalled()
  })

  it('calls deleteClub when the admin types "delete" to confirm', async () => {
    const club = makeClub()
    clubsAPI.getClubs.mockResolvedValue({ clubs: [club], count: 1 })
    clubsAPI.deleteClub.mockResolvedValue({ success: true })
    vi.spyOn(window, 'prompt').mockReturnValue('delete')
    renderTab({ authFlags: { is_admin: true } })
    await screen.findByText('HackMcGill')

    await userEvent.click(screen.getByTitle('clubs.deleteClub'))
    await waitFor(() => expect(clubsAPI.deleteClub).toHaveBeenCalledWith(club.id))
  })
})
