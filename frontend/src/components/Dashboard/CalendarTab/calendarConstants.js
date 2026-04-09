// Shared constants and helpers for CalendarTab

// ── McGill Academic Dates 2025–26 ────────────────────────────────
export const MCGILL_ACADEMIC_DATES = [
  { id: 'f-01', title: 'Deadline to Register (avoid penalty)',         date: '2025-08-14', type: 'academic', category: 'Fall 2025' },
  { id: 'f-02', title: 'Fall Classes Begin',                           date: '2025-08-27', type: 'academic', category: 'Fall 2025' },
  { id: 'f-03', title: 'Labour Day (no classes)',                      date: '2025-09-01', type: 'academic', category: 'Fall 2025' },
  { id: 'f-04', title: 'Deadline to Cancel Registration',              date: '2025-08-31', type: 'academic', category: 'Fall 2025' },
  { id: 'f-05', title: 'Add/Drop Deadline',                            date: '2025-09-09', type: 'academic', category: 'Fall 2025' },
  { id: 'f-06', title: 'Withdrawal with Refund Deadline',              date: '2025-09-16', type: 'academic', category: 'Fall 2025' },
  { id: 'f-07', title: 'Thanksgiving (no classes)',                    date: '2025-10-13', type: 'academic', category: 'Fall 2025' },
  { id: 'f-08', title: 'Fall Reading Break Begins',                    date: '2025-10-14', type: 'academic', category: 'Fall 2025' },
  { id: 'f-09', title: 'Fall Reading Break Ends',                      date: '2025-10-17', type: 'academic', category: 'Fall 2025' },
  { id: 'f-10', title: 'Withdrawal WITHOUT Refund Deadline',           date: '2025-10-28', type: 'academic', category: 'Fall 2025' },
  { id: 'f-11', title: 'Fall Classes End / Makeup Day (Monday sched)', date: '2025-12-03', type: 'academic', category: 'Fall 2025' },
  { id: 'f-12', title: 'Study Day',                                    date: '2025-12-04', type: 'academic', category: 'Fall 2025' },
  { id: 'f-13', title: 'Fall Exams Begin',                             date: '2025-12-05', type: 'academic', category: 'Fall 2025' },
  { id: 'f-14', title: 'Holiday Break Begins (offices closed)',        date: '2025-12-25', type: 'academic', category: 'Fall 2025' },
  { id: 'f-15', title: 'Fall Exams End',                               date: '2025-12-19', type: 'academic', category: 'Fall 2025' },
  { id: 'w-01', title: 'Deadline to Cancel Registration',              date: '2025-12-31', type: 'academic', category: 'Winter 2026' },
  { id: 'w-02', title: 'Holiday Break Ends',                           date: '2026-01-02', type: 'academic', category: 'Winter 2026' },
  { id: 'w-03', title: 'Winter Classes Begin',                         date: '2026-01-05', type: 'academic', category: 'Winter 2026' },
  { id: 'w-04', title: 'Add/Drop Deadline',                            date: '2026-01-20', type: 'academic', category: 'Winter 2026' },
  { id: 'w-05', title: 'Withdrawal with Refund Deadline',              date: '2026-01-27', type: 'academic', category: 'Winter 2026' },
  { id: 'w-06', title: 'Winter Reading Break Begins',                  date: '2026-03-02', type: 'academic', category: 'Winter 2026' },
  { id: 'w-07', title: 'Winter Reading Break Ends',                    date: '2026-03-06', type: 'academic', category: 'Winter 2026' },
  { id: 'w-08', title: 'Withdrawal WITHOUT Refund Deadline',           date: '2026-03-10', type: 'academic', category: 'Winter 2026' },
  { id: 'w-09', title: 'Good Friday (no classes)',                     date: '2026-04-03', type: 'academic', category: 'Winter 2026' },
  { id: 'w-10', title: 'Easter Monday (no classes)',                   date: '2026-04-06', type: 'academic', category: 'Winter 2026' },
  { id: 'w-11', title: 'Winter Classes End / Makeup Day (Friday sched)', date: '2026-04-14', type: 'academic', category: 'Winter 2026' },
  { id: 'w-12', title: 'Study Day',                                    date: '2026-04-15', type: 'academic', category: 'Winter 2026' },
  { id: 'w-13', title: 'Winter Exams Begin',                           date: '2026-04-16', type: 'academic', category: 'Winter 2026' },
  { id: 'w-14', title: 'Winter Exams End',                             date: '2026-04-30', type: 'academic', category: 'Winter 2026' },
]

export const CLUB_CATEGORY_COLORS = {
  'Academic':                 { color: '#2563eb', bg: '#dbeafe' },
  'Engineering & Technology': { color: '#7c3aed', bg: '#ede9fe' },
  'Professional':             { color: '#0f766e', bg: '#ccfbf1' },
  'Debate & Politics':        { color: '#b45309', bg: '#fef3c7' },
  'Athletics & Recreation':   { color: '#16a34a', bg: '#dcfce7' },
  'Arts & Culture':           { color: '#db2777', bg: '#fce7f3' },
  'Environment':              { color: '#15803d', bg: '#dcfce7' },
  'Health & Wellness':        { color: '#0284c7', bg: '#e0f2fe' },
  'Community Service':        { color: '#ea580c', bg: '#ffedd5' },
  'International':            { color: '#0891b2', bg: '#cffafe' },
  'Science':                  { color: '#4f46e5', bg: '#e0e7ff' },
  'Social':                   { color: '#dc2626', bg: '#fee2e2' },
  'Spiritual & Religious':    { color: '#a16207', bg: '#fefce8' },
}

export function getClubEventStyle(event) {
  if (event.category && CLUB_CATEGORY_COLORS[event.category]) {
    return CLUB_CATEGORY_COLORS[event.category]
  }
  return { color: '#d97706', bg: '#fef3c7' }
}

export const MONTHS_EN = ['January','February','March','April','May','June','July','August','September','October','November','December']
export const MONTHS_FR = ['Janvier','Février','Mars','Avril','Mai','Juin','Juillet','Août','Septembre','Octobre','Novembre','Décembre']
export const MONTHS_ZH = ['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月']
export const DAYS_EN = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat']
export const DAYS_FR = ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam']
export const DAYS_ZH = ['日','一','二','三','四','五','六']

// Tri-language inline helper — avoids adding dozens of LanguageContext keys for calendar-only strings
export function L(lang, en, fr, zh) { return lang === 'zh' ? zh : lang === 'fr' ? fr : en }

export function getDaysInMonth(year, month) { return new Date(year, month + 1, 0).getDate() }
export function getFirstDayOfMonth(year, month) { return new Date(year, month, 1).getDay() }
export function toDateStr(year, month, day) {
  return `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`
}
export function daysUntil(dateStr) {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  return Math.round((new Date(dateStr + 'T00:00:00') - today) / 86400000)
}

export const EVENT_TYPE_OPTIONS = [
  { key: 'personal', color: '#059669', bg: '#ecfdf5', darkBg: '#064e3b22', labelEn: 'Personal',  labelFr: 'Personnel',  labelZh: '个人' },
  { key: 'academic', color: '#1d4ed8', bg: '#eff6ff', darkBg: '#1e3a8a22', labelEn: 'Academic',  labelFr: 'Académique', labelZh: '学术' },
  { key: 'club',     color: '#d97706', bg: '#fffbeb', darkBg: '#92400e22', labelEn: 'Club',      labelFr: 'Club',       labelZh: '社团' },
  { key: 'exam',     color: '#7c3aed', bg: '#f5f3ff', darkBg: '#4c1d9522', labelEn: 'Exam',      labelFr: 'Examen',     labelZh: '考试' },
]
