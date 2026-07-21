// Shared constants and helpers for CalendarTab

// ── McGill Academic Dates 2025–26 ────────────────────────────────
// titleEn/Fr/Zh + categoryEn/Fr/Zh (not a single `title`/`category`) so this
// static data can be shown in the student's chosen language via the L()
// helper below — same tri-language pattern as EVENT_TYPE_OPTIONS.
export const MCGILL_ACADEMIC_DATES = [
  { id: 'f-01', titleEn: 'Deadline to Register (avoid penalty)',         titleFr: "Date limite d'inscription (éviter la pénalité)",                    titleZh: '注册截止日期（避免罚款）',           date: '2025-08-14', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-02', titleEn: 'Fall Classes Begin',                           titleFr: "Début des cours d'automne",                                          titleZh: '秋季课程开始',                       date: '2025-08-27', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-03', titleEn: 'Labour Day (no classes)',                      titleFr: 'Fête du travail (pas de cours)',                                     titleZh: '劳动节（无课）',                     date: '2025-09-01', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-04', titleEn: 'Deadline to Cancel Registration',              titleFr: "Date limite d'annulation de l'inscription",                          titleZh: '取消注册截止日期',                   date: '2025-08-31', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-05', titleEn: 'Add/Drop Deadline',                            titleFr: "Date limite d'ajout/abandon de cours",                               titleZh: '选课/退课截止日期',                  date: '2025-09-09', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-06', titleEn: 'Withdrawal with Refund Deadline',              titleFr: 'Date limite de retrait avec remboursement',                          titleZh: '退课退款截止日期',                   date: '2025-09-16', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-07', titleEn: 'Thanksgiving (no classes)',                    titleFr: 'Action de grâce (pas de cours)',                                     titleZh: '感恩节（无课）',                     date: '2025-10-13', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-08', titleEn: 'Fall Reading Break Begins',                    titleFr: "Début de la semaine de lecture d'automne",                           titleZh: '秋季阅读周开始',                     date: '2025-10-14', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-09', titleEn: 'Fall Reading Break Ends',                      titleFr: "Fin de la semaine de lecture d'automne",                             titleZh: '秋季阅读周结束',                     date: '2025-10-17', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-10', titleEn: 'Withdrawal WITHOUT Refund Deadline',           titleFr: 'Date limite de retrait SANS remboursement',                          titleZh: '无退款退课截止日期',                 date: '2025-10-28', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-11', titleEn: 'Fall Classes End / Makeup Day (Monday sched)', titleFr: 'Fin des cours d\'automne / Journée de rattrapage (horaire du lundi)', titleZh: '秋季课程结束／补课日（周一课表）', date: '2025-12-03', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-12', titleEn: 'Study Day',                                    titleFr: "Journée d'étude",                                                    titleZh: '自习日',                             date: '2025-12-04', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-13', titleEn: 'Fall Exams Begin',                             titleFr: 'Début des examens d\'automne',                                       titleZh: '秋季考试开始',                       date: '2025-12-05', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-14', titleEn: 'Holiday Break Begins (offices closed)',        titleFr: 'Début du congé des Fêtes (bureaux fermés)',                          titleZh: '假期开始（办公室关闭）',             date: '2025-12-25', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'f-15', titleEn: 'Fall Exams End',                               titleFr: 'Fin des examens d\'automne',                                         titleZh: '秋季考试结束',                       date: '2025-12-19', type: 'academic', categoryEn: 'Fall 2025', categoryFr: 'Automne 2025', categoryZh: '2025年秋季' },
  { id: 'w-01', titleEn: 'Deadline to Cancel Registration',              titleFr: "Date limite d'annulation de l'inscription",                          titleZh: '取消注册截止日期',                   date: '2025-12-31', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-02', titleEn: 'Holiday Break Ends',                           titleFr: 'Fin du congé des Fêtes',                                             titleZh: '假期结束',                           date: '2026-01-02', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-03', titleEn: 'Winter Classes Begin',                         titleFr: "Début des cours d'hiver",                                            titleZh: '冬季课程开始',                       date: '2026-01-05', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-04', titleEn: 'Add/Drop Deadline',                            titleFr: "Date limite d'ajout/abandon de cours",                               titleZh: '选课/退课截止日期',                  date: '2026-01-20', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-05', titleEn: 'Withdrawal with Refund Deadline',              titleFr: 'Date limite de retrait avec remboursement',                          titleZh: '退课退款截止日期',                   date: '2026-01-27', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-06', titleEn: 'Winter Reading Break Begins',                  titleFr: "Début de la semaine de lecture d'hiver",                             titleZh: '冬季阅读周开始',                     date: '2026-03-02', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-07', titleEn: 'Winter Reading Break Ends',                    titleFr: "Fin de la semaine de lecture d'hiver",                               titleZh: '冬季阅读周结束',                     date: '2026-03-06', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-08', titleEn: 'Withdrawal WITHOUT Refund Deadline',           titleFr: 'Date limite de retrait SANS remboursement',                          titleZh: '无退款退课截止日期',                 date: '2026-03-10', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-09', titleEn: 'Good Friday (no classes)',                     titleFr: 'Vendredi saint (pas de cours)',                                      titleZh: '耶稣受难日（无课）',                 date: '2026-04-03', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-10', titleEn: 'Easter Monday (no classes)',                   titleFr: 'Lundi de Pâques (pas de cours)',                                     titleZh: '复活节星期一（无课）',               date: '2026-04-06', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-11', titleEn: 'Winter Classes End / Makeup Day (Friday sched)', titleFr: 'Fin des cours d\'hiver / Journée de rattrapage (horaire du vendredi)', titleZh: '冬季课程结束／补课日（周五课表）', date: '2026-04-14', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-12', titleEn: 'Study Day',                                    titleFr: "Journée d'étude",                                                    titleZh: '自习日',                             date: '2026-04-15', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-13', titleEn: 'Winter Exams Begin',                           titleFr: "Début des examens d'hiver",                                          titleZh: '冬季考试开始',                       date: '2026-04-16', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
  { id: 'w-14', titleEn: 'Winter Exams End',                             titleFr: "Fin des examens d'hiver",                                            titleZh: '冬季考试结束',                       date: '2026-04-30', type: 'academic', categoryEn: 'Winter 2026', categoryFr: 'Hiver 2026', categoryZh: '2026年冬季' },
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

// ── User-created custom event types ─────────────────────────────
// Stored client-side (per user id) rather than in the DB: these are purely
// cosmetic categorization pills, not shared/synced data, so a small
// localStorage blob avoids a schema migration for what is otherwise the
// same free-text `type` column calendar events already use.
const CUSTOM_TYPES_KEY_PREFIX = 'symbolos_custom_event_types_'

export const CUSTOM_TYPE_COLOR_CHOICES = [
  '#ed1b2f', '#1d4ed8', '#059669', '#d97706', '#7c3aed', '#db2777', '#0891b2', '#4f46e5',
]

export function withAlpha(hex, alphaHex) {
  return `${hex}${alphaHex}`
}

export function getCustomEventTypes(userId) {
  if (!userId) return []
  try {
    const raw = localStorage.getItem(CUSTOM_TYPES_KEY_PREFIX + userId)
    const parsed = raw ? JSON.parse(raw) : []
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

export function saveCustomEventTypes(userId, types) {
  if (!userId) return
  try {
    localStorage.setItem(CUSTOM_TYPES_KEY_PREFIX + userId, JSON.stringify(types))
  } catch {
    // localStorage unavailable (private browsing, quota) — custom types just won't persist
  }
}
