// McGill University Academic Programs Data
// ═══════════════════════════════════════════════════════════════════════
// Single source of truth for faculties, majors, credit requirements.
// Used by: EnhancedProfileForm, DegreeProgressTracker, DegreePlanningView
// ═══════════════════════════════════════════════════════════════════════

export const FACULTIES = [
  'Faculty of Agricultural and Environmental Sciences',
  'Faculty of Arts',
  'Bachelor of Arts and Science',
  'School of Continuing Studies',
  'Faculty of Dental Medicine and Oral Health Sciences',
  'Faculty of Education',
  'Faculty of Engineering',
  'School of Environment',
  'Faculty of Law',
  'Desautels Faculty of Management',
  'Faculty of Medicine and Health Sciences',
  'Schulich School of Music',
  'Ingram School of Nursing',
  'School of Physical and Occupational Therapy',
  'Faculty of Science',
];

// ═══════════════════════════════════════════════════════════════════════
// FACULTY → MAJORS MAPPING
// Each major has { name, credits, hasHonours?, honoursCredits? }
// credits = total program credits required for graduation
// ═══════════════════════════════════════════════════════════════════════

export const FACULTY_MAJORS = {
  'Faculty of Arts': [
    { name: 'Anthropology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Art History', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'African Studies', credits: 120, hasHonours: false },
    { name: 'Canadian Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Classical Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Communication Studies', credits: 120, hasHonours: false },
    { name: 'Computer Science (B.A.)', credits: 120, hasHonours: false },
    { name: 'East Asian Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Economics', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'English', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Environment (B.A.)', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'French Language and Literature', credits: 120, hasHonours: false },
    { name: 'Gender, Sexuality, Feminist and Social Justice Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Geography', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'German Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Hispanic Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'History', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'International Development Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Italian Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Jewish Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Latin American and Caribbean Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Liberal Arts', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Linguistics', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Mathematics (B.A.)', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Philosophy', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Political Science', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Psychology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Religious Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Russian', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Sociology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Software Engineering (B.A.)', credits: 120, hasHonours: false },
    { name: 'Statistics (B.A.)', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Translation', credits: 120, hasHonours: false },
    { name: 'Urban Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'World Islamic and Middle East Studies', credits: 120, hasHonours: true, honoursCredits: 120 },
  ],

  'Faculty of Science': [
    { name: 'Anatomy and Cell Biology', credits: 120, hasHonours: false },
    { name: 'Applied Mathematics', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Atmospheric Science', credits: 120, hasHonours: false },
    { name: 'Biochemistry', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Biology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Chemistry', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Computer Science', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Computer Science and Biology', credits: 120, hasHonours: false },
    { name: 'Earth and Planetary Sciences', credits: 120, hasHonours: false },
    { name: 'Environmental Science', credits: 120, hasHonours: false },
    { name: 'Mathematics', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Mathematics and Computer Science', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Microbiology and Immunology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Neuroscience', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Physics', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Physics and Computer Science', credits: 120, hasHonours: false },
    { name: 'Physiology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Psychology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Software Engineering', credits: 120, hasHonours: false },
    { name: 'Statistics', credits: 120, hasHonours: true, honoursCredits: 120 },
  ],

  'Faculty of Engineering': [
    { name: 'Bioengineering', credits: 142, hasHonours: false },
    { name: 'Chemical Engineering', credits: 143, hasHonours: false },
    { name: 'Civil Engineering', credits: 139, hasHonours: false },
    { name: 'Computer Engineering', credits: 133, hasHonours: false },
    { name: 'Electrical Engineering', credits: 134, hasHonours: false },
    { name: 'Materials Engineering', credits: 148, hasHonours: false },
    { name: 'Mechanical Engineering', credits: 142, hasHonours: false },
    { name: 'Mining Engineering', credits: 144, hasHonours: false },
    { name: 'Software Engineering (Co-op)', credits: 141, hasHonours: false },
    { name: 'Global Engineering', credits: 127, hasHonours: false },
    { name: 'Architecture (B.Sc.)', credits: 126, hasHonours: false },
  ],

  'Desautels Faculty of Management': [
    { name: 'Accounting', credits: 120, hasHonours: false },
    { name: 'Business Analytics', credits: 120, hasHonours: false },
    { name: 'Economics for Management', credits: 120, hasHonours: false },
    { name: 'Finance', credits: 120, hasHonours: false },
    { name: 'Information Technology Management', credits: 120, hasHonours: false },
    { name: 'International Management', credits: 120, hasHonours: false },
    { name: 'Investment Management', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Managing for Sustainability', credits: 120, hasHonours: false },
    { name: 'Marketing', credits: 120, hasHonours: false },
    { name: 'Mathematics and Statistics for Management', credits: 120, hasHonours: false },
    { name: 'Organizational Behaviour and Human Resources', credits: 120, hasHonours: false },
    { name: 'Retail Management', credits: 120, hasHonours: false },
    { name: 'Strategic Management', credits: 120, hasHonours: false },
  ],

  'Faculty of Agricultural and Environmental Sciences': [
    { name: 'Agricultural Economics', credits: 120, hasHonours: false },
    { name: 'Agro-Environmental Sciences', credits: 120, hasHonours: false },
    { name: 'Bioresource Engineering', credits: 120, hasHonours: false },
    { name: 'Dietetics', credits: 120, hasHonours: false },
    { name: 'Environmental Biology', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Food Science (Food Science Option)', credits: 120, hasHonours: false },
    { name: 'Food Science (Food Chemistry Option)', credits: 120, hasHonours: false },
    { name: 'Global Food Security', credits: 120, hasHonours: false },
    { name: 'Life Sciences (Biological and Agricultural)', credits: 120, hasHonours: false },
    { name: 'Nutrition (Food Function and Safety)', credits: 120, hasHonours: false },
    { name: 'Nutrition (Global Nutrition)', credits: 120, hasHonours: false },
    { name: 'Nutrition (Metabolism, Health and Disease)', credits: 120, hasHonours: false },
    { name: 'Nutrition (Sports Nutrition)', credits: 120, hasHonours: false },
  ],

  'Bachelor of Arts and Science': [
    // Interfaculty programs
    { name: 'Cognitive Science', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Sustainability, Science and Society', credits: 120, hasHonours: true, honoursCredits: 120 },
    { name: 'Environment', credits: 120, hasHonours: true, honoursCredits: 120 },
  ],

  'School of Environment': [
    { name: 'Ecological Determinants of Health in Society', credits: 120, hasHonours: false },
    { name: 'Economics and the Earth\'s Environment', credits: 120, hasHonours: false },
    { name: 'Environment and Development', credits: 120, hasHonours: false },
  ],

  'Faculty of Law': [
    { name: 'BCL/JD (Bachelor of Civil Law / Juris Doctor)', credits: 105, hasHonours: false },
  ],

  'Faculty of Education': [
    { name: 'Kindergarten and Elementary Education', credits: 120, hasHonours: false },
    { name: 'Secondary English', credits: 120, hasHonours: false },
    { name: 'Secondary Mathematics', credits: 120, hasHonours: false },
    { name: 'Secondary Science and Technology', credits: 120, hasHonours: false },
    { name: 'Secondary Social Sciences', credits: 120, hasHonours: false },
    { name: 'Teaching English as a Second Language (TESL)', credits: 120, hasHonours: false },
    { name: 'Education in Global Contexts', credits: 120, hasHonours: false },
    { name: 'Physical and Health Education', credits: 120, hasHonours: false },
    { name: 'Kinesiology', credits: 120, hasHonours: true, honoursCredits: 120 },
  ],

  'Schulich School of Music': [
    { name: 'Voice Performance', credits: 123, hasHonours: false },
    { name: 'Piano Performance', credits: 125, hasHonours: false },
    { name: 'Orchestral Instruments', credits: 125, hasHonours: false },
    { name: 'Jazz Performance', credits: 126, hasHonours: false },
    { name: 'Early Music Performance', credits: 125, hasHonours: false },
    { name: 'Music Composition', credits: 124, hasHonours: false },
    { name: 'Music History', credits: 124, hasHonours: false },
    { name: 'Music Theory', credits: 124, hasHonours: false },
    { name: 'Music Studies', credits: 123, hasHonours: false },
    { name: 'Music Faculty Program', credits: 123, hasHonours: false },
    { name: 'Music Faculty Program – Jazz', credits: 123, hasHonours: false },
  ],

  'Ingram School of Nursing': [
    { name: 'Nursing (B.Sc.N.)', credits: 103, hasHonours: false },
    { name: 'Nursing (Integrated) (B.N.I.)', credits: 65, hasHonours: false },
  ],

  'Faculty of Dental Medicine and Oral Health Sciences': [
    { name: 'Doctor of Dental Medicine (D.M.D.)', credits: 221, hasHonours: false },
    { name: 'Dental Preparatory Year (Dent-P)', credits: 30, hasHonours: false },
  ],

  'Faculty of Medicine and Health Sciences': [
    { name: 'Doctor of Medicine (M.D.,C.M.)', credits: 200, hasHonours: false },
    { name: 'Medicine Preparatory Program (Med-P)', credits: 30, hasHonours: false },
  ],

  'School of Physical and Occupational Therapy': [
    { name: 'Rehabilitation Science – Physical Therapy', credits: 90, hasHonours: false },
    { name: 'Rehabilitation Science – Occupational Therapy', credits: 90, hasHonours: false },
  ],

  'School of Continuing Studies': [
    { name: 'General Studies', credits: 90, hasHonours: false },
  ],
};

// ═══════════════════════════════════════════════════════════════════════
// HELPER: Get credits required for a major (with optional honours flag)
// This is the single source of truth used by DegreeProgressTracker
// ═══════════════════════════════════════════════════════════════════════

export function getCreditsRequired(faculty, major, isHonours = false) {
  const facultyMajors = FACULTY_MAJORS[faculty];
  if (!facultyMajors) return 120; // safe default
  const entry = facultyMajors.find(m => m.name === major);
  if (!entry) return 120;
  if (isHonours && entry.hasHonours && entry.honoursCredits) {
    return entry.honoursCredits;
  }
  return entry.credits;
}

// ═══════════════════════════════════════════════════════════════════════
// HELPER: Get major names for a faculty (flat string array for dropdowns)
// ═══════════════════════════════════════════════════════════════════════

export function getMajorsForFaculty(faculty) {
  const entries = FACULTY_MAJORS[faculty];
  if (!entries) return [];
  return entries.map(m => m.name);
}

// ═══════════════════════════════════════════════════════════════════════
// HELPER: Check if a major supports honours
// ═══════════════════════════════════════════════════════════════════════

export function majorHasHonours(faculty, major) {
  const entries = FACULTY_MAJORS[faculty];
  if (!entries) return false;
  const entry = entries.find(m => m.name === major);
  return entry?.hasHonours ?? false;
}

// ═══════════════════════════════════════════════════════════════════════
// BACKWARD COMPAT — flat arrays still used by some components
// ═══════════════════════════════════════════════════════════════════════

// All unique major names across all faculties (for secondary major dropdowns)
export const MAJORS = [...new Set(
  Object.values(FACULTY_MAJORS).flatMap(arr => arr.map(m => m.name))
)].sort();

// B.A. & Sc. specific arrays
export const ARTS_MAJORS_BASC = [
  'Anthropology', 'Art History', 'Classical Studies', 'East Asian Studies',
  'Economics', 'English', 'French Language and Literature', 'German Studies', 'Hispanic Studies',
  'History', 'Italian Studies', 'Linguistics', 'Philosophy', 'Political Science',
  'Psychology', 'Sociology', 'Geography', 'International Development Studies',
  'Gender, Sexuality, Feminist and Social Justice Studies', 'Canadian Studies',
  'Jewish Studies', 'Communication Studies', 'African Studies',
  'Latin American and Caribbean Studies', 'World Islamic and Middle East Studies',
];

export const SCIENCE_MAJORS_BASC = [
  'Biology', 'Chemistry', 'Physics', 'Mathematics', 'Statistics',
  'Computer Science', 'Applied Mathematics', 'Biochemistry',
  'Microbiology and Immunology', 'Physiology', 'Neuroscience',
  'Atmospheric Science', 'Earth and Planetary Sciences',
  'Environmental Science', 'Geography',
];

export const BASC_INTERFACULTY_PROGRAMS = [
  'Cognitive Science',
  'Sustainability, Science and Society',
  'Environment',
];

export const BASC_STREAMS = [
  { value: 'Interfaculty', label: 'Interfaculty Program',  description: 'Cognitive Science, SSS, or Environment (54 cr)' },
  { value: 'Multi-track',  label: 'Multi-track',           description: 'Arts major + Science major (36 + 36 cr)' },
  { value: 'Joint Honours', label: 'Joint Honours',        description: 'Honours component in Arts + Science (30-36 + 36 cr)' },
];

// Legacy credit requirement maps (still used by DegreeProgressTracker)
export const FACULTY_CREDIT_REQUIREMENTS = Object.fromEntries(
  Object.entries(FACULTY_MAJORS).map(([faculty, majors]) => {
    // Use the most common credit value for the faculty
    const credits = majors.map(m => m.credits);
    const mode = credits.sort((a, b) =>
      credits.filter(v => v === a).length - credits.filter(v => v === b).length
    ).pop();
    return [faculty, mode];
  })
);

export const PROGRAM_CREDIT_REQUIREMENTS = Object.fromEntries(
  Object.values(FACULTY_MAJORS)
    .flatMap(arr => arr)
    .filter(m => m.credits !== 120) // only include non-default
    .map(m => [m.name, m.credits])
);

export const MINORS = [
  'Anthropology', 'Art History', 'Biology', 'Chemistry', 'Classics',
  'Computer Science', 'Economics', 'English', 'Environmental Studies',
  'French', 'Geography', 'German Studies', 'History', 'Italian Studies',
  'Mathematics', 'Music', 'Philosophy', 'Physics', 'Political Science',
  'Psychology', 'Religious Studies', 'Sociology', 'Spanish',
  'Statistics', 'Gender, Sexuality, Feminist and Social Justice Studies',
  'Canadian Studies', 'African Studies', 'East Asian Studies',
  'Latin American and Caribbean Studies', 'Middle Eastern Studies',
  'World Cinemas', 'Urban Systems', 'Communication Studies',
  'Linguistics', 'Cognitive Science', 'Entrepreneurship',
  'Business', 'Management', 'Sustainability Science and Society',
  'Environment', 'Indigenous Studies', 'Information Studies',
];

export const YEAR_OPTIONS = [
  { value: '0', label: 'U0' },
  { value: '1', label: 'U1' },
  { value: '2', label: 'U2' },
  { value: '3', label: 'U3' },
  { value: '4', label: 'U4' },
  { value: '5', label: 'U5+' }
];

export const BADGES = [
  {
    id: 'getting_started',
    name: 'Getting Started',
    description: 'Set up your profile',
    icon: '\u{1F3AF}',
    requirement: 'profile_complete'
  },
  {
    id: 'course_explorer',
    name: 'Course Explorer',
    description: 'Saved 10+ courses',
    icon: '\u{1F50D}',
    requirement: 'saved_10_courses'
  },
  {
    id: 'chat_master',
    name: 'Chat Master',
    description: '50+ AI conversations',
    icon: '\u{1F4AC}',
    requirement: 'chat_50_times'
  },
  {
    id: 'well_rounded',
    name: 'Well-Rounded',
    description: 'Took courses in 5+ departments',
    icon: '\u{1F31F}',
    requirement: 'courses_5_departments'
  },
  {
    id: 'deans_list',
    name: "Dean's List",
    description: 'GPA above 3.7',
    icon: '\u{1F3C6}',
    requirement: 'gpa_3.7'
  },
  {
    id: 'early_bird',
    name: 'Early Bird',
    description: 'Plan next semester early',
    icon: '\u{1F426}',
    requirement: 'saved_15_courses'
  },
  {
    id: 'veteran',
    name: 'McGill Veteran',
    description: 'Complete 60+ credits',
    icon: '\u{1F393}',
    requirement: 'credits_60'
  },
  {
    id: 'scholar',
    name: 'Scholar',
    description: 'Complete 90+ credits',
    icon: '\u{1F4DA}',
    requirement: 'credits_90'
  },
  {
    id: 'graduate',
    name: 'Almost There!',
    description: 'Complete 100+ credits',
    icon: '\u{1F389}',
    requirement: 'credits_100'
  }
];
