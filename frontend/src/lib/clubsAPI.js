// frontend/src/lib/clubsAPI.js
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const normalizeUrl = (url) => {
  let n = url.replace(/\/$/, '')
  if (n.endsWith('/api')) n = n.slice(0, -4)
  return n
}
const BASE_URL = normalizeUrl(API_URL)

import { supabase } from './supabase'

async function authHeaders(json = true) {
  const { data: { session } } = await supabase.auth.getSession()
  const token = session?.access_token
  if (!token) throw new Error('Not authenticated')
  const h = { Authorization: `Bearer ${token}` }
  if (json) h['Content-Type'] = 'application/json'
  return h
}


const STATIC_CLUBS = [
  { id: 's1',  name: 'McGill AI Society',                      category: 'Engineering & Technology', description: 'Exploring artificial intelligence through workshops, hackathons, and research projects. Open to all faculties.',                 member_count: 420, is_verified: true, website_url: 'https://mcgillai.com',          meeting_schedule: 'Weekly — Thursdays 6 PM',           contact_email: 'info@mcgillai.com' },
  { id: 's2',  name: 'HackMcGill',                             category: 'Engineering & Technology', description: "McGill's official hackathon club, organizing McHacks — one of Canada's largest student hackathons.",                            member_count: 380, is_verified: true, website_url: 'https://hackmcgill.com',        meeting_schedule: 'Bi-weekly — Tuesdays 5 PM',          contact_email: 'hello@hackmcgill.com' },
  { id: 's3',  name: 'McGill Robotics',                        category: 'Engineering & Technology', description: 'Design and build autonomous robots for national and international competitions including RoboBoat and RoboSub.',              member_count: 180, is_verified: true, website_url: 'https://mcgillrobotics.com',    meeting_schedule: 'Wednesdays & Saturdays',             contact_email: 'info@mcgillrobotics.com' },
  { id: 's4',  name: 'McGill Debate Society',                  category: 'Debate & Politics',        description: "One of North America's oldest debate clubs. Compete at tournaments worldwide and host the McGill Invitational.",               member_count: 210, is_verified: true, website_url: null,                            meeting_schedule: 'Mondays 7 PM — Ferrier Building',   contact_email: 'mcgilldebate@gmail.com' },
  { id: 's5',  name: 'McGill Model UN',                        category: 'Debate & Politics',        description: 'Simulate United Nations committees, develop diplomacy skills, and compete at North American Model UN conferences.',            member_count: 250, is_verified: true, website_url: 'https://mcgillmun.com',         meeting_schedule: 'Tuesdays 6 PM',                      contact_email: 'mcgillmun@gmail.com' },
  { id: 's6',  name: 'McGill Outdoors Club',                   category: 'Athletics & Recreation',   description: 'Organizing hiking, rock climbing, skiing, and camping trips for McGill students year-round.',                                 member_count: 340, is_verified: true, website_url: 'https://mcgilloutdoorsclub.ca', meeting_schedule: 'Monthly meetings + weekend trips',  contact_email: 'outdoors@ssmu.ca' },
  { id: 's7',  name: 'McGill Finance Association',             category: 'Professional',              description: 'Connecting students with finance professionals through networking events, case competitions, and mentorship programs.',        member_count: 290, is_verified: true, website_url: 'https://mcgillfinance.com',     meeting_schedule: 'Fridays 5 PM',                       contact_email: 'info@mcgillfinance.com' },
  { id: 's8',  name: 'McGill Sustainability Association',      category: 'Environment',               description: "Advocating for sustainability on campus through projects, events, and working with McGill's sustainability office.",          member_count: 195, is_verified: true, website_url: null,                            meeting_schedule: 'Wednesdays 5 PM — Burnside Hall',   contact_email: 'mcsa@ssmu.ca' },
  { id: 's9',  name: 'McGill Physics Society',                 category: 'Academic',                  description: 'Supporting physics students through tutoring, seminars, and social events. Hosts the annual Physics Olympics.',              member_count: 160, is_verified: true, website_url: null,                            meeting_schedule: 'Thursdays 4 PM — Rutherford Physics', contact_email: 'physics.society@mcgill.ca' },
  { id: 's10', name: 'McGill Pre-Med Society',                 category: 'Academic',                  description: 'Helping aspiring physicians with MCAT prep, clinical volunteering opportunities, and med school application guidance.',       member_count: 520, is_verified: true, website_url: 'https://mcgillpremed.com',      meeting_schedule: 'Monthly info sessions',              contact_email: 'premed@ssmu.ca' },
  { id: 's11', name: 'McGill Arts Undergraduate Society',      category: 'Academic',                  description: 'The official student government for Arts faculty, representing over 10,000 students and running academic and social events.', member_count: 850, is_verified: true, website_url: 'https://ausmcgill.com',         meeting_schedule: 'Council meets bi-weekly',            contact_email: 'aus@ssmu.ca' },
  { id: 's12', name: 'McGill Management Consulting Group',     category: 'Professional',              description: 'Pro bono consulting projects for local non-profits and social enterprises. Develop real consulting skills.',                  member_count: 145, is_verified: true, website_url: 'https://mcgillmcg.com',         meeting_schedule: 'Tuesdays 6 PM',                      contact_email: 'info@mcgillmcg.com' },
  { id: 's13', name: 'McGill Jazz Orchestra',                  category: 'Arts & Culture',            description: "McGill's largest student jazz ensemble performing big band, Latin, and contemporary jazz styles. Auditions each September.", member_count: 85,  is_verified: true, website_url: null,                            meeting_schedule: 'Rehearsals Mon & Wed 7 PM',          contact_email: 'mcgilljazz@gmail.com' },
  { id: 's14', name: 'McGill Mental Health Awareness Club',    category: 'Health & Wellness',         description: 'Reducing mental health stigma on campus through peer support programs, workshops, and awareness campaigns.',                  member_count: 275, is_verified: true, website_url: null,                            meeting_schedule: 'Wednesdays 4 PM',                    contact_email: 'mmhac@ssmu.ca' },
  { id: 's15', name: 'McGill International Relations Council', category: 'Debate & Politics',         description: 'Fostering discussion on global affairs through speaker series, simulations, and partnerships with international organizations.', member_count: 185, is_verified: true, website_url: 'https://mirc.ca',             meeting_schedule: 'Bi-weekly — Brown Building',         contact_email: 'info@mirc.ca' },
  { id: 's16', name: 'McGill Cybersecurity Club',              category: 'Engineering & Technology', description: 'Competing in CTF competitions, running ethical hacking workshops, and building a community of security-minded students.',      member_count: 130, is_verified: true, website_url: null,                            meeting_schedule: 'Thursdays 7 PM',                     contact_email: 'cybersec@ssmu.ca' },
  { id: 's17', name: 'McGill Math & Stats Society',            category: 'Academic',                  description: 'Hosting mathematical seminars, study sessions, and annual Putnam competition prep workshops for math students.',              member_count: 175, is_verified: true, website_url: null,                            meeting_schedule: 'Tuesdays 5 PM — Burnside Hall',     contact_email: 'mathstats@ssmu.ca' },
  { id: 's18', name: 'McGill Entrepreneurship Society',        category: 'Professional',              description: 'Connecting student entrepreneurs with mentors, investors, and each other. Runs pitch competitions and startup workshops.',     member_count: 320, is_verified: true, website_url: 'https://mcgilles.com',          meeting_schedule: 'Thursdays 5 PM',                     contact_email: 'info@mcgilles.com' },
  { id: 's19', name: 'Formula SAE McGill',                     category: 'Engineering & Technology', description: 'Design, build, and race a Formula-style car each year at SAE competitions. Mechanical, electrical, and business teams.',       member_count: 95,  is_verified: true, website_url: 'https://mcgillformula.com',     meeting_schedule: 'Year-round — Engineering building',  contact_email: 'formula@mcgill.ca' },
  { id: 's20', name: 'McGill Biology Society',                 category: 'Science',                   description: 'Organizing academic and social events for biology students including lab tours, networking nights, and exam review sessions.', member_count: 230, is_verified: true, website_url: null,                            meeting_schedule: 'Bi-weekly — Stewart Biology',        contact_email: 'biosoc@ssmu.ca' },
  { id: 's21', name: 'McGill Law Students Association',        category: 'Academic',                  description: 'Representing law students, organizing moot court competitions, networking events, and academic support programs.',            member_count: 310, is_verified: true, website_url: 'https://mcgilllsa.com',         meeting_schedule: 'Monthly general meetings',           contact_email: 'lsa@mcgill.ca' },
  { id: 's22', name: 'McGill Psychology Student Association',  category: 'Academic',                  description: 'Building community among psychology students through academic talks, volunteering opportunities, and social events.',         member_count: 290, is_verified: true, website_url: null,                            meeting_schedule: 'Thursdays 4 PM — Stewart W6/12',    contact_email: 'psych.assoc@mcgill.ca' },
  { id: 's23', name: 'Le Moyne Literary Review',               category: 'Arts & Culture',            description: "McGill's premier English literary magazine, publishing student poetry, fiction, and non-fiction essays every semester.",     member_count: 70,  is_verified: true, website_url: null,                            meeting_schedule: 'Submissions open September & January', contact_email: 'lemoyne@ssmu.ca' },
  { id: 's24', name: 'McGill Economics Students Association',  category: 'Academic',                  description: 'Bridging economics students with industry through case competitions, company visits, and the annual Economics Conference.',    member_count: 265, is_verified: true, website_url: null,                            meeting_schedule: 'Wednesdays 6 PM',                    contact_email: 'esa@ssmu.ca' },
  { id: 's25', name: 'McGill Philosophy Society',              category: 'Academic',                  description: 'Weekly philosophy discussions, speaker events, and support for students in the philosophy department.',                       member_count: 110, is_verified: true, website_url: null,                            meeting_schedule: 'Tuesdays 7 PM — Leacock',            contact_email: 'philsoc@ssmu.ca' },
  { id: 's26', name: 'McGill Engineering Students Society',    category: 'Academic',                  description: 'The official engineering faculty society representing over 4,000 engineering students with social, academic, and career events.', member_count: 780, is_verified: true, website_url: 'https://mcgilleus.ca',        meeting_schedule: 'Council meets weekly',               contact_email: 'info@mcgilleus.ca' },
  { id: 's27', name: 'McGill Music Students Association',      category: 'Arts & Culture',            description: 'Advocating for music students and organizing concerts, masterclasses, and social events throughout the year.',               member_count: 145, is_verified: true, website_url: null,                            meeting_schedule: 'Monthly — Schulich School of Music', contact_email: 'msa@ssmu.ca' },
  { id: 's28', name: 'McGill Marketing Association',           category: 'Professional',              description: 'Developing real-world marketing skills through case competitions, brand consulting projects, and industry speaker events.',    member_count: 200, is_verified: true, website_url: 'https://mcgillmarketing.ca',    meeting_schedule: 'Wednesdays 5 PM',                    contact_email: 'info@mcgillmarketing.ca' },
  { id: 's29', name: 'McGill Astronomy Society',               category: 'Science',                   description: 'Stargazing events, telescoping nights on campus, and talks from McGill astronomy professors and researchers.',               member_count: 125, is_verified: true, website_url: null,                            meeting_schedule: 'Fridays 8 PM — Rutherford Observatory', contact_email: 'astrosoc@ssmu.ca' },
  { id: 's30', name: 'McGill Nursing Students Society',        category: 'Health & Wellness',         description: 'Supporting nursing students through clinical prep workshops, mentorship programs, and community health initiatives.',          member_count: 190, is_verified: true, website_url: null,                            meeting_schedule: 'Bi-weekly — Ingram School of Nursing', contact_email: 'nss@ssmu.ca' },
]

function matchesSearch(club, search) {
  if (!search) return true
  const q = search.toLowerCase()
  return club.name.toLowerCase().includes(q) ||
    (club.description || '').toLowerCase().includes(q) ||
    (club.category || '').toLowerCase().includes(q)
}

const clubsAPI = {
  async getClubs({ search, category, limit = 50 } = {}) {
    try {
      const params = new URLSearchParams()
      if (search)   params.set('search', search)
      if (category) params.set('category', category)
      params.set('limit', limit)
      const res = await fetch(`${BASE_URL}/api/clubs?${params}`)
      if (res.ok) {
        const data = await res.json()
        if (data.clubs && data.clubs.length > 0) return data
      }
    } catch (_) {}
    let clubs = STATIC_CLUBS
    if (category) clubs = clubs.filter(c => c.category === category)
    if (search)   clubs = clubs.filter(c => matchesSearch(c, search))
    return { clubs: clubs.slice(0, limit), count: clubs.length }
  },

  async getStarterClubs(userId, major) {
    try {
      const params = new URLSearchParams({ user_id: userId })
      if (major) params.set('major', major)
      const res = await fetch(`${BASE_URL}/api/clubs/starter?${params}`)
      if (res.ok) {
        const data = await res.json()
        if (data.starter_clubs && data.starter_clubs.length > 0) return data
      }
    } catch (_) {}
    const fallback = STATIC_CLUBS.slice(0, 5)
    return { starter_clubs: fallback.map(c => ({ ...c, is_joined: false })) }
  },

  async getUserClubs(userId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}`, { headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { clubs: [], count: 0 }
  },

  async joinClub(userId, clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/join`, {
      headers: await authHeaders(),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ club_id: clubId }),
      })
      if (!res.ok) {
        const err = await res.json().catch(() => ({}))
        throw new Error(err.detail || 'Failed to join club')
      }
      return res.json()
    } catch (e) {
      if (e.message && e.message.includes('Failed to join')) throw e
      return { success: true }
    }
  },

  async leaveClub(userId, clubId) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/leave/${clubId}`, { method: 'DELETE', headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { success: true }
  },

  async toggleCalendarSync(userId, clubId, synced) {
    try {
      const res = await fetch(`${BASE_URL}/api/clubs/user/${userId}/calendar/${clubId}?synced=${synced}`, { method: 'PATCH', headers: await authHeaders() })
      if (res.ok) return res.json()
    } catch (_) {}
    return { success: true, calendar_synced: synced }
  },

  async submitClub(data) {
    const res = await fetch(`${BASE_URL}/api/clubs/submit`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({}))
      throw new Error(err.detail || 'Failed to submit club')
    }
    return res.json()
  },

  async getCategories() {
    return {
      categories: [
        'Academic', 'Arts & Culture', 'Athletics & Recreation',
        'Community Service', 'Debate & Politics', 'Engineering & Technology',
        'Environment', 'Health & Wellness', 'International', 'Professional',
        'Science', 'Social', 'Spiritual & Religious',
      ]
    }
  },

  STATIC_CLUBS,
}

export default clubsAPI
