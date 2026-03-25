import React, { useState, useMemo } from 'react'
import {
  FaGraduationCap, FaBook, FaGlobe, FaCalendarAlt, FaDollarSign,
  FaHandsHelping, FaClipboardCheck, FaSearch, FaExternalLinkAlt,
  FaChevronDown, FaChevronUp, FaRegBookmark, FaBookmark, FaStar,
  FaInfoCircle, FaUserGraduate, FaPassport, FaUniversity,
  FaMoneyBillWave, FaHeartbeat, FaClock
} from 'react-icons/fa'
import { useLanguage } from '../../contexts/LanguageContext'
import './AdvisingResourcesView.css'

const RESOURCES = [
  // ── Academic Advising ──
  {
    id: 'faculty_advising',
    category: 'advising',
    title: 'Faculty Advising Offices',
    description: 'Each McGill faculty has dedicated academic advisors who help with program planning, course selection, and CGPA concerns. Advisors can also assist with academic difficulties, program transfers, and degree planning.',
    keyPoints: [
      'Arts students: visit OASIS (Dawson Hall)',
      'Science students: visit SOUSA (Burnside Hall)',
      'Engineering students: contact Student Affairs Office (FDA)',
      'Management students: BCom Advising (Bronfman Building)',
      'Walk-in and appointment options vary by faculty',
    ],
    links: [
      { label: 'Arts OASIS', url: 'https://www.mcgill.ca/oasis' },
      { label: 'Science SOUSA', url: 'https://www.mcgill.ca/science/sousa' },
      { label: 'Engineering Student Affairs', url: 'https://www.mcgill.ca/engineering/students' },
      { label: 'Desautels BCom Advising', url: 'https://www.mcgill.ca/desautels/programs/bcom/advising' },
    ],
    tags: ['advisor', 'oasis', 'sousa', 'faculty', 'program planning', 'course selection'],
    priority: 'essential',
  },
  {
    id: 'academic_standing',
    category: 'advising',
    title: 'Academic Standing & Probation',
    description: 'McGill uses CGPA thresholds to determine academic standing. Students who fall below satisfactory standing may be placed on probation or required to withdraw. Understanding these rules early helps you stay on track.',
    keyPoints: [
      'Satisfactory standing generally requires a CGPA of 2.0 or higher',
      'Unsatisfactory standing triggers academic probation',
      'Continued unsatisfactory standing may result in required-to-withdraw (RTW) status',
      'Readmission is possible after RTW but requires a formal application',
      'Faculty-specific rules may set higher CGPA thresholds for certain programs',
    ],
    links: [
      { label: 'Academic Standing', url: 'https://www.mcgill.ca/students/records/academic-standing' },
    ],
    tags: ['cgpa', 'probation', 'standing', 'rtw', 'withdraw', 'gpa', 'readmission'],
    priority: 'essential',
  },
  {
    id: 'choosing_major',
    category: 'advising',
    title: 'Choosing a Major or Minor',
    description: 'McGill students typically declare their major by the end of their first year (U1). You can pursue double majors, joint programs, or add minors depending on your faculty and program requirements.',
    keyPoints: [
      'Most students declare by the end of U1 (first year)',
      'Double majors and joint honors programs are available in many faculties',
      'Program transfers between faculties require a formal application',
      'Speak with your faculty advisor before making changes',
    ],
    links: [
      { label: 'Academic Advising', url: 'https://www.mcgill.ca/students/advising' },
    ],
    tags: ['major', 'minor', 'declaration', 'program transfer', 'double major', 'joint'],
    priority: 'recommended',
  },

  // ── Prerequisites & Requirements ──
  {
    id: 'understanding_prereqs',
    category: 'prerequisites',
    title: 'Understanding Prerequisites',
    description: 'Prerequisite and corequisite information is listed in the eCalendar and on Minerva. Understanding how to read these requirements is essential for planning your course sequence and avoiding registration issues.',
    keyPoints: [
      'Prerequisites must be completed before enrolling in a course',
      'Corequisites can be taken at the same time as the course',
      'Some courses allow instructor permission to override prerequisites',
      'Check both the eCalendar and Minerva for the most up-to-date information',
      'Failing a prerequisite may require you to drop the dependent course',
    ],
    links: [
      { label: 'eCalendar (Course Catalogue)', url: 'https://www.mcgill.ca/study' },
    ],
    tags: ['prerequisite', 'corequisite', 'ecalendar', 'course planning', 'permission'],
    priority: 'essential',
  },
  {
    id: 'program_requirements',
    category: 'prerequisites',
    title: 'Program Requirements',
    description: 'Every McGill program has required courses, complementary courses, and elective slots. Degree worksheets in Minerva help you track progress toward completing all program requirements.',
    keyPoints: [
      'Required courses are mandatory for your program',
      'Complementary courses are chosen from an approved list',
      'Elective courses can be from any faculty (with some restrictions)',
      'Use the Degree Worksheet in Minerva to track your progress',
      'Some programs have specific course sequencing requirements',
    ],
    links: [
      { label: 'Plan Your Courses', url: 'https://www.mcgill.ca/students/courses/plan' },
    ],
    tags: ['requirements', 'complementary', 'elective', 'degree worksheet', 'required courses'],
    priority: 'recommended',
  },
  {
    id: 'transfer_credits',
    category: 'prerequisites',
    title: 'Course Equivalencies & Transfer Credits',
    description: 'Credits from AP, IB, CEGEP, or other universities may transfer to McGill. Advanced standing and credit exemptions can reduce your course load and accelerate your degree.',
    keyPoints: [
      'AP and IB credits are evaluated upon admission',
      'CEGEP DEC holders receive advanced standing (up to 30 credits)',
      'Transfer credits from other universities require formal evaluation',
      'Not all credits may count toward program requirements',
    ],
    links: [
      { label: 'Transfer Credit', url: 'https://www.mcgill.ca/transfercredit' },
    ],
    tags: ['transfer', 'ap', 'ib', 'cegep', 'equivalency', 'advanced standing', 'exemption'],
    priority: 'recommended',
  },

  // ── International Students ──
  {
    id: 'study_permits_caq',
    category: 'international',
    title: 'Study Permits & CAQ',
    description: 'International students in Quebec need both a Quebec Certificate of Acceptance (CAQ) and a federal study permit. Maintaining valid immigration status is critical — expired documents can jeopardize your studies.',
    keyPoints: [
      'Apply for your CAQ first, then your study permit',
      'Begin renewal at least 3 months before expiry',
      'You can remain in Canada while a renewal is being processed (implied status)',
      'Always keep copies of your immigration documents',
      'Report any changes in your study status to IRCC',
    ],
    links: [
      { label: 'ISS Immigration Info', url: 'https://www.mcgill.ca/internationalstudents/immigration' },
    ],
    tags: ['caq', 'study permit', 'visa', 'immigration', 'ircc', 'renewal', 'implied status'],
    priority: 'essential',
  },
  {
    id: 'pgwp',
    category: 'international',
    title: 'Post-Graduation Work Permit (PGWP)',
    description: 'The PGWP allows international graduates to work in Canada after completing their studies. Eligibility depends on your program length and type. Apply within 180 days of receiving your final grades.',
    keyPoints: [
      'Must apply within 180 days of receiving confirmation of program completion',
      'Program must be at least 8 months long for PGWP eligibility',
      'PGWP duration matches your program length (up to 3 years)',
      'You can work full-time while your application is being processed',
      'Maintaining full-time status during studies is generally required',
    ],
    links: [
      { label: 'PGWP & Work Info', url: 'https://www.mcgill.ca/internationalstudents/work' },
    ],
    tags: ['pgwp', 'work permit', 'post-graduation', 'employment', 'immigration'],
    priority: 'essential',
  },
  {
    id: 'health_insurance',
    category: 'international',
    title: 'Health Insurance (ASHI / RAMQ)',
    description: 'International students must have health insurance coverage. Most are automatically enrolled in the ASHI plan. Quebec residents and some exempt groups may be eligible for RAMQ instead.',
    keyPoints: [
      'ASHI (Allied Student Health Insurance) is mandatory for most international students',
      'Students from countries with RAMQ agreements may opt out of ASHI',
      'Quebec residents are covered by RAMQ',
      'ASHI fees are charged to your student account each semester',
      'Opt-out deadlines are strict — check each semester',
    ],
    links: [
      { label: 'Health Insurance Info', url: 'https://www.mcgill.ca/internationalstudents/health' },
    ],
    tags: ['ashi', 'ramq', 'health insurance', 'medical', 'coverage', 'opt-out'],
    priority: 'essential',
  },
  {
    id: 'working_in_canada',
    category: 'international',
    title: 'Working in Canada as a Student',
    description: 'International students with a valid study permit can work in Canada under certain conditions. Understanding the rules helps you stay compliant with immigration regulations while earning income.',
    keyPoints: [
      'On-campus work: no additional work permit needed',
      'Off-campus work: limited to 20 hours/week during academic sessions',
      'Full-time work is allowed during scheduled breaks (summer, winter)',
      'Co-op work permits are required for co-op or internship programs',
      'Unauthorized work can affect your immigration status',
    ],
    links: [
      { label: 'Working During Studies', url: 'https://www.mcgill.ca/internationalstudents/work' },
    ],
    tags: ['work', 'employment', 'on-campus', 'off-campus', 'co-op', 'hours'],
    priority: 'recommended',
  },
  {
    id: 'immigration_advising',
    category: 'international',
    title: 'Immigration Advising',
    description: 'McGill International Student Services (ISS) provides free, confidential immigration advising. For complex cases, always consult ISS or a licensed immigration consultant — never use unlicensed agents.',
    keyPoints: [
      'ISS advisors can help with study permits, CAQ, work permits, and PGWP',
      'Appointments available online and in-person',
      'Never use unlicensed immigration consultants',
      'ISS also offers workshops on immigration topics throughout the year',
      'Contact ISS early if your situation changes (e.g., program change, leave of absence)',
    ],
    links: [
      { label: 'International Student Services', url: 'https://www.mcgill.ca/internationalstudents' },
    ],
    tags: ['iss', 'immigration', 'advising', 'consultant', 'support'],
    priority: 'recommended',
  },

  // ── Registration & Enrollment ──
  {
    id: 'add_drop',
    category: 'registration',
    title: 'Add/Drop & Course Changes',
    description: 'McGill has strict deadlines for adding, dropping, and withdrawing from courses. Missing these deadlines can result in a "W" on your transcript or continued tuition charges.',
    keyPoints: [
      'Add/drop period: first two weeks of the semester (no fee penalty)',
      'After the add/drop deadline, dropping results in a "W" on your transcript',
      'Withdrawal deadlines vary — check the academic calendar',
      'Course changes are done through Minerva',
      'Late course changes may require faculty advisor approval',
    ],
    links: [
      { label: 'Course Changes', url: 'https://www.mcgill.ca/students/courses/change' },
    ],
    tags: ['add', 'drop', 'withdraw', 'course change', 'deadline', 'minerva', 'W'],
    priority: 'essential',
  },
  {
    id: 'course_load',
    category: 'registration',
    title: 'Course Load',
    description: 'Understanding full-time vs part-time status is important because it affects financial aid eligibility, immigration status for international students, and degree progression timelines.',
    keyPoints: [
      'Full-time: 12+ credits per semester (typically 4-5 courses)',
      'Part-time: fewer than 12 credits per semester',
      'International students generally must maintain full-time status',
      'Overloading (more than 17 credits) requires faculty approval',
      'Part-time status may affect financial aid and loan deferral',
    ],
    links: [
      { label: 'Plan Your Courses', url: 'https://www.mcgill.ca/students/courses/plan' },
    ],
    tags: ['full-time', 'part-time', 'course load', 'credits', 'overloading'],
    priority: 'recommended',
  },
  {
    id: 'minerva_registration',
    category: 'registration',
    title: 'Minerva Registration',
    description: 'Minerva is McGill\'s student information system used for course registration, viewing grades, and managing your academic record. Learning to navigate it efficiently saves time during registration periods.',
    keyPoints: [
      'Registration times are assigned based on credits completed (more credits = earlier time)',
      'Use the Course Search tool to find available sections',
      'Waitlists are available for some courses — check regularly for openings',
      'Quick Add/Drop using CRN codes is the fastest registration method',
      'Check for holds on your account that may block registration',
    ],
    links: [
      { label: 'Registration Info', url: 'https://www.mcgill.ca/students/registration' },
    ],
    tags: ['minerva', 'registration', 'crn', 'waitlist', 'schedule', 'enrolment'],
    priority: 'essential',
  },

  // ── Financial Aid ──
  {
    id: 'scholarships',
    category: 'financial',
    title: 'Scholarships & Awards',
    description: 'McGill offers entrance scholarships, in-course awards, and faculty-specific funding. Many scholarships are awarded automatically based on academic performance, while others require a separate application.',
    keyPoints: [
      'Entrance scholarships are typically based on admission grades',
      'In-course scholarships are awarded based on CGPA at the end of each year',
      'Faculty-specific awards may have additional criteria (community involvement, research)',
      'External scholarships (e.g., provincial, national) are also available',
      'Search the Scholarships and Student Aid website for opportunities',
    ],
    links: [
      { label: 'Scholarships & Awards', url: 'https://www.mcgill.ca/studentaid/scholarships' },
    ],
    tags: ['scholarship', 'award', 'merit', 'entrance', 'funding'],
    priority: 'essential',
  },
  {
    id: 'bursaries',
    category: 'financial',
    title: 'Bursaries & Need-Based Aid',
    description: 'McGill provides need-based financial support through bursaries, work-study programs, and emergency funding. The financial aid application is available through Minerva each year.',
    keyPoints: [
      'Complete the Financial Aid Application on Minerva each academic year',
      'Work-study programs offer on-campus employment opportunities',
      'Emergency funding is available for unexpected financial hardship',
      'Quebec residents may also apply for Aide financiere aux etudes (AFE)',
      'Application deadlines vary — apply early for maximum consideration',
    ],
    links: [
      { label: 'Scholarships & Student Aid', url: 'https://www.mcgill.ca/studentaid' },
    ],
    tags: ['bursary', 'financial aid', 'need-based', 'work-study', 'emergency', 'afe'],
    priority: 'recommended',
  },
  {
    id: 'international_financial_aid',
    category: 'financial',
    title: 'International Student Financial Aid',
    description: 'Financial aid options for international students are limited but available. McGill offers specific bursaries and emergency funding for international students facing financial difficulties.',
    keyPoints: [
      'International students are eligible for some McGill bursaries',
      'Emergency financial assistance is available regardless of residency status',
      'Some faculty-specific scholarships are open to international students',
      'Check your home country for government-sponsored study-abroad funding',
      'ISS can provide guidance on financial resources',
    ],
    links: [
      { label: 'International Student Aid', url: 'https://www.mcgill.ca/studentaid/international' },
    ],
    tags: ['international', 'financial aid', 'bursary', 'funding', 'emergency'],
    priority: 'recommended',
  },

  // ── Graduation & Convocation ──
  {
    id: 'graduation_checklist',
    category: 'graduation',
    title: 'Graduation Checklist',
    description: 'Graduating from McGill requires applying through Minerva, completing a degree audit, and meeting all program requirements. Start the process early to avoid last-minute surprises.',
    keyPoints: [
      'Apply to graduate through Minerva during the application period',
      'Complete a degree audit to verify all requirements are met',
      'Resolve any outstanding holds or incomplete grades before the deadline',
      'Common pitfalls: missing complementary credits, unfulfilled prerequisites',
      'Convocation ceremonies are held in June and November',
    ],
    links: [
      { label: 'Graduation Info', url: 'https://www.mcgill.ca/graduation' },
    ],
    tags: ['graduation', 'convocation', 'degree audit', 'apply', 'diploma'],
    priority: 'essential',
  },
  {
    id: 'transcripts',
    category: 'graduation',
    title: 'Transcript Requests',
    description: 'You can order official and unofficial transcripts through Minerva. Official transcripts are required for graduate school applications, professional licensing, and employment verification.',
    keyPoints: [
      'Unofficial transcripts are free and available instantly on Minerva',
      'Official transcripts must be ordered and have a processing fee',
      'Electronic official transcripts are available for faster delivery',
      'Allow adequate processing time during peak periods (end of semester)',
    ],
    links: [
      { label: 'Transcripts', url: 'https://www.mcgill.ca/students/records/transcripts' },
    ],
    tags: ['transcript', 'official', 'unofficial', 'records', 'order'],
    priority: 'helpful',
  },

  // ── Student Services ──
  {
    id: 'wellness_hub',
    category: 'services',
    title: 'Student Wellness Hub',
    description: 'The Student Wellness Hub provides integrated health and wellness services including mental health counseling, medical care, and health promotion. Walk-in and appointment options are available.',
    keyPoints: [
      'Mental health counseling: individual and group sessions',
      'Medical clinic: general health care, immunizations, sexual health',
      'Crisis support available 24/7 via Keep.meSAFE app',
      'Walk-in appointments available for urgent concerns',
      'Located at Brown Student Services Building (3600 McTavish)',
    ],
    links: [
      { label: 'Student Wellness Hub', url: 'https://www.mcgill.ca/wellness' },
    ],
    tags: ['wellness', 'mental health', 'counseling', 'clinic', 'health', 'crisis'],
    priority: 'essential',
  },
  {
    id: 'osd',
    category: 'services',
    title: 'Office for Students with Disabilities (OSD)',
    description: 'The OSD provides academic accommodations for students with documented disabilities. Services include exam accommodations, note-taking support, and accessibility resources.',
    keyPoints: [
      'Register with OSD early — accommodations are not retroactive',
      'Exam accommodations: extra time, separate room, assistive technology',
      'Note-taking services and alternative format materials available',
      'OSD works with professors to implement accommodations',
      'Both permanent and temporary disabilities are supported',
    ],
    links: [
      { label: 'Office for Students with Disabilities', url: 'https://www.mcgill.ca/osd' },
    ],
    tags: ['disability', 'accommodation', 'accessibility', 'osd', 'exam', 'note-taking'],
    priority: 'recommended',
  },
  {
    id: 'tutorial_skills',
    category: 'services',
    title: 'Tutorial Service & SKILLS',
    description: 'McGill offers free peer tutoring, academic skills workshops, and writing support through the Tutorial Service and SKILLS program. These resources help students improve their academic performance.',
    keyPoints: [
      'Free peer tutoring for many introductory courses',
      'SKILLS workshops cover study strategies, time management, and exam preparation',
      'Writing support available through the McGill Writing Centre',
      'Drop-in and appointment-based services',
      'Supplemental Instruction (SI) sessions for high-demand courses',
    ],
    links: [
      { label: 'Tutorial Service', url: 'https://www.mcgill.ca/tutorial' },
    ],
    tags: ['tutoring', 'skills', 'writing', 'study', 'academic support', 'workshop'],
    priority: 'recommended',
  },
  {
    id: 'caps',
    category: 'services',
    title: 'Career Planning Service (CaPS)',
    description: 'CaPS helps students with career exploration, job search strategies, resume and cover letter reviews, and interview preparation. They also host career fairs and maintain a job posting board.',
    keyPoints: [
      'One-on-one career counseling appointments',
      'Resume and cover letter review services',
      'Mock interviews and interview preparation workshops',
      'Job and internship postings on myFuture platform',
      'Career fairs and employer networking events throughout the year',
    ],
    links: [
      { label: 'Career Planning Service', url: 'https://www.mcgill.ca/caps' },
    ],
    tags: ['career', 'caps', 'resume', 'job', 'internship', 'interview', 'myfuture'],
    priority: 'recommended',
  },

  // ── Important Dates ──
  {
    id: 'academic_calendar',
    category: 'dates',
    title: 'Academic Calendar',
    description: 'The McGill academic calendar outlines key dates for each semester including classes, reading week, exam periods, and holidays. Consult it regularly to stay aware of upcoming deadlines.',
    keyPoints: [
      'Fall semester: September to December',
      'Winter semester: January to April',
      'Summer session: May to August (condensed terms)',
      'Reading week occurs in late October (fall) and late February (winter)',
      'Final exams are held during a dedicated exam period at end of each semester',
    ],
    links: [
      { label: 'Important Dates', url: 'https://www.mcgill.ca/importantdates' },
    ],
    tags: ['calendar', 'dates', 'semester', 'reading week', 'exams', 'schedule'],
    priority: 'essential',
  },
  {
    id: 'fee_deadlines',
    category: 'dates',
    title: 'Fee Deadlines',
    description: 'Tuition and fee payments are due at specific dates each semester. Late payments incur interest charges. Installment plans are available for students who need to spread out payments.',
    keyPoints: [
      'Tuition fees are typically due in September (fall) and January (winter)',
      'Late payment interest accrues monthly',
      'Installment plans divide fees into smaller monthly payments',
      'Outstanding balances may block registration and transcript requests',
      'Check your Student Accounts page on Minerva for exact amounts and deadlines',
    ],
    links: [
      { label: 'Student Accounts', url: 'https://www.mcgill.ca/student-accounts' },
    ],
    tags: ['tuition', 'fees', 'payment', 'deadline', 'installment', 'interest'],
    priority: 'essential',
  },
]

const CATEGORY_CONFIG = {
  advising:       { icon: FaUserGraduate, key: 'ar.catAdvising' },
  prerequisites:  { icon: FaBook,         key: 'ar.catPrereqs' },
  international:  { icon: FaPassport,     key: 'ar.catInternational' },
  registration:   { icon: FaClipboardCheck, key: 'ar.catRegistration' },
  financial:      { icon: FaMoneyBillWave, key: 'ar.catFinancial' },
  graduation:     { icon: FaGraduationCap, key: 'ar.catGraduation' },
  services:       { icon: FaHeartbeat,    key: 'ar.catServices' },
  dates:          { icon: FaCalendarAlt,  key: 'ar.catDates' },
}

const PRIORITY_OPTIONS = [
  { id: 'all',         key: 'ar.priorityAll' },
  { id: 'essential',   key: 'ar.priorityEssential' },
  { id: 'recommended', key: 'ar.priorityRecommended' },
]

function ResourceCard({ resource, saved, onToggleSave, t }) {
  const [open, setOpen] = useState(false)
  const catConfig = CATEGORY_CONFIG[resource.category]
  const CatIcon = catConfig?.icon || FaInfoCircle

  return (
    <div className={`ar-card ${open ? 'ar-card--open' : ''}`}>
      <div className="ar-card-header" onClick={() => setOpen(o => !o)}>
        <div className="ar-card-left">
          <span className="ar-badge">
            <CatIcon className="ar-badge-icon" />
            {t(catConfig?.key || resource.category)}
          </span>
          {resource.priority === 'essential' && (
            <span className="ar-priority-badge" title={t('ar.essential')}>
              <FaStar />
            </span>
          )}
          <div className="ar-card-info">
            <h3 className="ar-card-title">{resource.title}</h3>
          </div>
        </div>
        <div className="ar-card-controls">
          <button
            className={`ar-bm ${saved ? 'ar-bm--on' : ''}`}
            onClick={e => { e.stopPropagation(); onToggleSave(resource.id) }}
            title={saved ? t('ar.removeBookmark') : t('ar.saveBookmark')}
          >
            {saved ? <FaBookmark /> : <FaRegBookmark />}
          </button>
          <span className="ar-chevron">{open ? <FaChevronUp /> : <FaChevronDown />}</span>
        </div>
      </div>
      {open && (
        <div className="ar-card-body">
          <p className="ar-desc">{resource.description}</p>
          {resource.keyPoints?.length > 0 && (
            <div className="ar-section">
              <h4 className="ar-section-title"><FaInfoCircle /> {t('ar.keyPoints')}</h4>
              <ul className="ar-list-items">
                {resource.keyPoints.map((point, i) => <li key={i}>{point}</li>)}
              </ul>
            </div>
          )}
          <div className="ar-links">
            {resource.links?.map((l, i) => (
              <a key={i} href={l.url} target="_blank" rel="noopener noreferrer" className="ar-link">
                {l.label} <FaExternalLinkAlt />
              </a>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default function AdvisingResourcesView({ profile = {} }) {
  const { t } = useLanguage()
  const [view,           setView]           = useState('browse')
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [priorityFilter, setPriorityFilter] = useState('all')
  const [search,         setSearch]         = useState('')
  const [savedIds,       setSavedIds]       = useState(new Set())

  const CATEGORIES = [
    { id: 'all', label: t('ar.catAll') },
    ...Object.entries(CATEGORY_CONFIG).map(([id, cfg]) => ({
      id,
      label: t(cfg.key),
    })),
  ]

  const toggleSave = id => setSavedIds(prev => {
    const next = new Set(prev)
    next.has(id) ? next.delete(id) : next.add(id)
    return next
  })

  const browsed = useMemo(() => RESOURCES.filter(r => {
    if (categoryFilter !== 'all' && r.category !== categoryFilter) return false
    if (priorityFilter !== 'all' && r.priority !== priorityFilter) return false
    if (search.trim()) {
      const q = search.toLowerCase()
      return r.title.toLowerCase().includes(q) ||
             r.description.toLowerCase().includes(q) ||
             r.tags.some(tag => tag.toLowerCase().includes(q)) ||
             r.keyPoints.some(kp => kp.toLowerCase().includes(q))
    }
    return true
  }), [categoryFilter, priorityFilter, search])

  const savedResources = useMemo(() => RESOURCES.filter(r => savedIds.has(r.id)), [savedIds])
  const hasFilters = categoryFilter !== 'all' || priorityFilter !== 'all' || search.trim()

  return (
    <div className="ar-view">
      <div className="ar-header">
        <div className="ar-header-icon"><FaUniversity /></div>
        <div>
          <h2 className="ar-title">{t('ar.title')}</h2>
          <p className="ar-sub">{t('ar.subtitle')}</p>
        </div>
      </div>

      <div className="ar-tabs">
        <button className={`ar-tab ${view === 'browse' ? 'ar-tab--active' : ''}`} onClick={() => setView('browse')}>
          {t('ar.browse')} <span className="ar-tab-pill">{RESOURCES.length}</span>
        </button>
        <button className={`ar-tab ${view === 'saved' ? 'ar-tab--active' : ''}`} onClick={() => setView('saved')}>
          {t('ar.saved')} {savedIds.size > 0 && <span className="ar-tab-pill ar-tab-pill--accent">{savedIds.size}</span>}
        </button>
      </div>

      {view === 'browse' && (
        <>
          <div className="ar-stats">
            <span><b>{RESOURCES.length}</b> {t('ar.statResources')}</span>
            <span className="ar-stats-dot">&middot;</span>
            <span><b>{Object.keys(CATEGORY_CONFIG).length}</b> {t('ar.statCategories')}</span>
            <span className="ar-stats-dot">&middot;</span>
            <span><b>{RESOURCES.filter(r => r.priority === 'essential').length}</b> {t('ar.statEssential')}</span>
          </div>

          <div className="ar-search-row">
            <FaSearch className="ar-search-ico" />
            <input className="ar-search" placeholder={t('ar.searchPlaceholder')} value={search} onChange={e => setSearch(e.target.value)} />
            {search && <button className="ar-search-x" onClick={() => setSearch('')}>&times;</button>}
          </div>

          <div className="ar-pill-row">
            {CATEGORIES.map(cat => (
              <button key={cat.id} className={`ar-pill ${categoryFilter === cat.id ? 'ar-pill--on' : ''}`} onClick={() => setCategoryFilter(cat.id)}>{cat.label}</button>
            ))}
          </div>

          <div className="ar-pill-row ar-pill-row--sm">
            {PRIORITY_OPTIONS.map(p => (
              <button key={p.id} className={`ar-pill ar-pill--sm ${priorityFilter === p.id ? 'ar-pill--on' : ''}`} onClick={() => setPriorityFilter(p.id)}>{t(p.key)}</button>
            ))}
          </div>

          <div className="ar-result-bar">
            <span className="ar-result-count">
              {browsed.length === 1 ? t('ar.resource').replace('{count}', browsed.length) : t('ar.resources').replace('{count}', browsed.length)}
              {hasFilters ? t('ar.matchingFilters') : ''}
            </span>
            {hasFilters && (
              <button className="ar-clear-btn" onClick={() => { setCategoryFilter('all'); setPriorityFilter('all'); setSearch('') }}>{t('ar.clearFilters')}</button>
            )}
          </div>

          {browsed.length === 0
            ? <div className="ar-empty"><FaSearch className="ar-empty-ico" /><p>{t('ar.noMatch')}</p></div>
            : <div className="ar-cards">{browsed.map(r => <ResourceCard key={r.id} resource={r} saved={savedIds.has(r.id)} onToggleSave={toggleSave} t={t} />)}</div>
          }
        </>
      )}

      {view === 'saved' && (
        <div className="ar-cards">
          {savedResources.length === 0 ? (
            <div className="ar-empty">
              <FaRegBookmark className="ar-empty-ico" />
              <p>{t('ar.noSaved')}</p>
              <p className="ar-empty-sub">{t('ar.noSavedSub')} <FaRegBookmark style={{ verticalAlign: 'middle' }} /></p>
            </div>
          ) : savedResources.map(r => <ResourceCard key={r.id} resource={r} saved={true} onToggleSave={toggleSave} t={t} />)}
        </div>
      )}

      <div className="ar-footer">
        <span>{t('ar.footerText')}</span>
        <a href="https://www.mcgill.ca/students" target="_blank" rel="noopener noreferrer" className="ar-footer-link">
          {t('ar.footerLink')} <FaExternalLinkAlt />
        </a>
      </div>
    </div>
  )
}
