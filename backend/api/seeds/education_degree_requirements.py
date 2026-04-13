"""
McGill Faculty of Education – Degree Requirements Seed Data
Source: McGill Course Catalogue / eCalendar 2024-2025
https://coursecatalogue.mcgill.ca/en/undergraduate/education/

Programs covered:
  DISE (Integrated Studies in Education):
  - B.Ed. Kindergarten & Elementary (120 cr)
  - B.Ed. Secondary English (120 cr)
  - B.Ed. Secondary Mathematics (120 cr)
  - B.Ed. Secondary Science & Technology (120 cr)
  - B.Ed. Secondary Social Sciences – History & Geography (120 cr)
  - B.Ed. Secondary Social Sciences – History & Culture/Citizenship QC (120 cr)
  - B.Ed. Teaching English as a Second Language – TESL Elem/Sec (120 cr)
  - B.A.(Education) – Education in Global Contexts (90 cr)

  Kinesiology and Physical Education:
  - B.Ed. Physical and Health Education (120 cr)
  - B.Sc.(Kinesiology) – Kinesiology (90 cr)
  - B.Sc.(Kinesiology) – Kinesiology Honours (90 cr)

Accuracy notes:
  - Credit totals for CEGEP entrants (30 cr Advanced Standing granted).
    Out-of-province students add 30 cr Freshman/Foundation Year.
  - "recommended" flags are author suggestions, not official designations.
  - Always cross-check with current eCalendar before academic decisions.
"""

EDUCATION_PROGRAMS = [

  # ────────────────────────────────────────────────────────────
  # B.Ed. Kindergarten and Elementary Education  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_kindergarten_elementary",
    "name": "B.Ed. – Kindergarten and Elementary Education",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "The B.Ed. K&E program leads to Quebec teacher certification for Kindergarten through Grade 6 "
      "(ages 5–11). The 120-credit program integrates academic subject knowledge, pedagogy, "
      "educational foundations, and four school-based practicums. Out-of-province students complete "
      "an additional 30-credit Freshman year (150 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-kindergarten-and-elementary-education",
    "blocks": [
      {
        "block_key": "bed_ke_professional_core",
        "title": "Professional Core – Education",
        "block_type": "required",
        "credits_needed": 34,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required Education courses covering foundations, pedagogy, inclusion, and professional development.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Taken U1 Fall; orients you to the teaching profession and field experience expectations."},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Develops written and oral communication skills essential for classroom teaching."},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Explores Indigenous pedagogy and worldviews; required for Quebec certification."},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "249", "title": "Global Education and Social Justice",            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Broadens perspectives on equity and global citizenship in the K-6 classroom."},
          {"subject": "EDEC", "catalog": "253", "title": "Second Professional Seminar (K/Elementary)",     "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Examines the aims, nature, and ethics of education; core theoretical grounding."},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Covers educational technology integration, critical for modern classroom practice."},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Covers child development and learning theory—foundational for planning K-6 lessons."},
          {"subject": "EDPE", "catalog": "400", "title": "Assessment in Education",                        "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Essential for all Quebec classrooms; covers differentiated instruction for diverse learners."},
          {"subject": "EDEC", "catalog": "405", "title": "Fourth Year Professional Seminar (K/Elementary)", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ke_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressively intensive school-based practicums. EDFE 200 in U1; EDFE 256 in U2; EDFE 306 and EDFE 406 in U3/U4.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "200", "title": "First Field Experience",                         "credits": 2, "is_required": True},
          {"subject": "EDFE", "catalog": "256", "title": "Second Field Experience (K/Elementary)",         "credits": 3, "is_required": True},
          {"subject": "EDFE", "catalog": "306", "title": "Third Field Experience (K/Elementary)",          "credits": 8, "is_required": True},
          {"subject": "EDFE", "catalog": "406", "title": "Fourth Field Experience (K/Elementary)",         "credits": 7, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ke_curriculum_methods",
        "title": "Curriculum and Methods – Elementary School Subjects",
        "block_type": "required",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Required methods: EDEE 223, 253, 260, 273, 283. "
          "Teachable subject area: 9 credits from at least two of Art, English, French, "
          "Mathematics, Music, Natural Sciences, Physical Education, or Social Studies."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "EDEE", "catalog": "223", "title": "Language Arts Methods – K/Elementary",           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Reading and writing instruction; one of the most important skills for elementary teachers."},
          {"subject": "EDEE", "catalog": "253", "title": "Mathematics Methods – K/Elementary",             "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Math pedagogy specifically designed for elementary school curriculum."},
          {"subject": "EDEE", "catalog": "260", "title": "Reading Methods – Kindergarten/Elementary",      "credits": 3, "is_required": True},
          {"subject": "EDEE", "catalog": "273", "title": "Science Methods – K/Elementary",                 "credits": 3, "is_required": True},
          {"subject": "EDEE", "catalog": "283", "title": "Social Studies Pedagogy",                        "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "111", "title": "Mathematics for Education Students",             "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Number theory and arithmetic tailored for future elementary teachers."},
          {"subject": "EDEA", "catalog": "241", "title": "Basic Art Media for Classroom",                  "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Practical studio art course relevant to the elementary Arts curriculum."},
          {"subject": "EDEE", "catalog": "325", "title": "Children's Literature",                          "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Excellent elective; directly supports K-6 English language arts teaching."},
          {"subject": "EDSL", "catalog": "345", "title": "ESL Methods – Elementary",                       "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Key for teaching in Quebec's bilingual school environment."},
          {"subject": "EDEC", "catalog": "221", "title": "Leadership and Group Skills",                    "credits": 3, "is_required": False},
          {"subject": "EDPT", "catalog": "204", "title": "Creating and Using Media for Learning",          "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Practical digital media skills for classroom use."},
          {"subject": "EDER", "catalog": "372", "title": "Culture and Citizenship in Quebec Context",      "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bed_ke_electives",
        "title": "Complementary / Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 24,
        "courses_needed": None,
        "group_name": None,
        "notes": "Free electives and additional subject area courses to reach 120 credits. FRSL French language courses highly recommended for Quebec teachers.",
        "sort_order": 4,
        "courses": [
          {"subject": "FRSL", "catalog": "207", "title": "Elementary French 01",                           "credits": 6, "is_required": False, "recommended": True,  "recommendation_reason": "French proficiency required for Quebec teacher certification."},
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True,  "recommendation_reason": "Continuation of French; essential for working in Quebec schools."},
          {"subject": "EDEM", "catalog": "220", "title": "Contemporary Issues in Education",               "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Good Freshman elective to get context on the education system."},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. Secondary English  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_secondary_english",
    "name": "B.Ed. – Secondary English",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "The B.Ed. Secondary English program prepares teachers for Grades 7–11 in Quebec secondary "
      "schools. Students complete 51 credits in English (literature, language/linguistics, cultural "
      "studies, and drama) under a stream structure, alongside Education professional courses, "
      "practicums, and electives (120 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-secondary-english",
    "blocks": [
      {
        "block_key": "bed_seng_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 28,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required professional education courses shared across all B.Ed. Secondary programs.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "254", "title": "Second Professional Seminar (Secondary)",        "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "351", "title": "Third Professional Seminar (Secondary)",         "credits": 2, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "304", "title": "Measurement and Evaluation",                     "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "404", "title": "Fourth Year Professional Seminar (Secondary)", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_seng_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressive secondary school practicums.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "200", "title": "First Field Experience",                         "credits": 2, "is_required": True},
          {"subject": "EDFE", "catalog": "254", "title": "Second Field Experience (Secondary)",            "credits": 3, "is_required": True},
          {"subject": "EDFE", "catalog": "351", "title": "Third Field Experience (Secondary)",             "credits": 8, "is_required": True},
          {"subject": "EDFE", "catalog": "451", "title": "Fourth Field Experience (Secondary)",            "credits": 7, "is_required": True},
        ],
      },
      {
        "block_key": "bed_seng_methods",
        "title": "Secondary English Teaching Methods",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "EDES 361 must be completed before the 3rd Field Experience.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDES", "catalog": "361", "title": "Teaching Secondary English 1",                   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Must be completed before 3rd Field Experience; core methods course."},
          {"subject": "EDES", "catalog": "461", "title": "Teaching Secondary English 2",                   "credits": 3, "is_required": True},
          {"subject": "EDES", "catalog": "366", "title": "Literature for Young Adults",                    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Directly applicable to Sec. III–V English curriculum."},
        ],
      },
      {
        "block_key": "bed_seng_teachable_english",
        "title": "Teachable Subject Area – English",
        "block_type": "required",
        "credits_needed": 51,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Option 1: 51 credits in English (Stream 1: 48 cr in subject area + 3 cr EDES methods = 51). "
          "Option 2 (Stream 2): 33 credits in English + 15 credits in a second teachable area "
          "(Math, Social Sciences, or Science & Technology) + 3 cr EDES methods for second teachable. "
          "Structure: 6 cr Language/Linguistics + 30 cr Literature (min 15 at 300+) + 9 cr Cultural Studies (min 3 at 300+) + 3 cr Drama — Option 1. "
          "At least one Shakespeare course required. Minimum 24 credits with C or higher required before 3rd Field Experience."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "EDES", "catalog": "366", "title": "Literature for Young Adults",                    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required core course for Secondary English; directly applicable to Sec. III–V English curriculum."},
          {"subject": "LING", "catalog": "201", "title": "Introduction to Linguistics",                    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Recommended Language/Linguistics component course."},
          {"subject": "ENGL", "catalog": "200", "title": "Approaches to Literature",                       "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Strong foundation for the Literature component."},
          {"subject": "ENGL", "catalog": "215", "title": "Introduction to Poetry",                         "credits": 3, "is_required": False, "recommended": True},
          {"subject": "ENGL", "catalog": "224", "title": "Introduction to Fiction",                        "credits": 3, "is_required": False, "recommended": True},
          {"subject": "ENGL", "catalog": "234", "title": "Canadian Literature",                            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Highly relevant to Quebec English curriculum focus on Canadian identity."},
          {"subject": "ENGL", "catalog": "243", "title": "Introduction to Drama",                          "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Drama/Theatre is a required sub-component of the English subject area."},
          {"subject": "ENGL", "catalog": "314", "title": "Shakespeare",                                    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "At least one Shakespeare course is required within the subject area."},
          {"subject": "ENGL", "catalog": "340", "title": "Children's Literature",                          "credits": 3, "is_required": False},
          {"subject": "ENGL", "catalog": "380", "title": "Creative Writing",                               "credits": 3, "is_required": False},
          {"subject": "ENGL", "catalog": "426", "title": "Contemporary Literature",                        "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bed_seng_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 free elective credits.",
        "sort_order": 5,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True,  "recommendation_reason": "French proficiency strongly recommended for teaching in Quebec."},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. Secondary Mathematics  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_secondary_math",
    "name": "B.Ed. – Secondary Mathematics",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "The B.Ed. Secondary Mathematics program prepares teachers for Grades 7–11 in Quebec. "
      "Students must complete MATH 133, 140, and 141 in their Freshman year. The main program "
      "includes 51 credits in Mathematics (7 required courses + complementary electives), "
      "Education professional courses and practicums, and electives (120 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-secondary-mathematics",
    "blocks": [
      {
        "block_key": "bed_smath_freshman",
        "title": "Freshman Prerequisites – Mathematics",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "Must be completed in Freshman (U0) year before entering the main program.",
        "sort_order": 1,
        "courses": [
          {"subject": "MATH", "catalog": "133", "title": "Linear Algebra and Geometry",                    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Freshman prerequisite; must be completed before U1."},
          {"subject": "MATH", "catalog": "140", "title": "Calculus 1",                                     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Freshman prerequisite; must be completed before U1."},
          {"subject": "MATH", "catalog": "141", "title": "Calculus 2",                                     "credits": 4, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Freshman prerequisite; must be completed before U1."},
        ],
      },
      {
        "block_key": "bed_smath_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 31,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required professional education courses shared across all B.Ed. Secondary programs.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "254", "title": "Second Professional Seminar (Secondary)",        "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "351", "title": "Third Professional Seminar (Secondary)",         "credits": 2, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "304", "title": "Measurement and Evaluation",                     "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True},
          {"subject": "EDTL", "catalog": "520", "title": "Perspectives on Knowledge in Mathematics and Science", "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Specialized philosophy of math/science required for Secondary Math & Science teachers."},
          {"subject": "EDEC", "catalog": "404", "title": "Fourth Year Professional Seminar (Secondary)", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_smath_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressive secondary school practicums.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDFE", "catalog": "200", "title": "First Field Experience",                         "credits": 2, "is_required": True},
          {"subject": "EDFE", "catalog": "254", "title": "Second Field Experience (Secondary)",            "credits": 3, "is_required": True},
          {"subject": "EDFE", "catalog": "351", "title": "Third Field Experience (Secondary)",             "credits": 8, "is_required": True},
          {"subject": "EDFE", "catalog": "451", "title": "Fourth Field Experience (Secondary)",            "credits": 7, "is_required": True},
        ],
      },
      {
        "block_key": "bed_smath_methods",
        "title": "Secondary Mathematics Teaching Methods",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "EDES 353 must be completed before 3rd Field Experience.",
        "sort_order": 4,
        "courses": [
          {"subject": "EDES", "catalog": "353", "title": "Teaching Secondary Mathematics 1",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Must be completed before 3rd Field Experience."},
          {"subject": "EDES", "catalog": "453", "title": "Teaching Secondary Mathematics 2",               "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_smath_teachable",
        "title": "Teachable Subject Area – Mathematics",
        "block_type": "required",
        "credits_needed": 51,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Option 1: 51 credits in Mathematics (21 required + 30 complementary). "
          "Option 2: 21 required credits + 15 complementary Mathematics credits + 15 credits in a second teachable "
          "(English, Social Sciences, or Science & Technology). "
          "Minimum 24 credits with C or higher required before 3rd Field Experience."
        ),
        "sort_order": 5,
        "courses": [
          {"subject": "MATH", "catalog": "222", "title": "Calculus 3",                                     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students."},
          {"subject": "MATH", "catalog": "223", "title": "Linear Algebra",                                 "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students."},
          {"subject": "MATH", "catalog": "228", "title": "Classical Geometry",                             "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students; geometry is a major strand in the Quebec secondary math curriculum."},
          {"subject": "MATH", "catalog": "315", "title": "Ordinary Differential Equations",                "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students."},
          {"subject": "MATH", "catalog": "323", "title": "Probability",                                    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students; statistics and probability are in the secondary math curriculum."},
          {"subject": "MATH", "catalog": "324", "title": "Statistics",                                     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students."},
          {"subject": "MATH", "catalog": "338", "title": "History and Philosophy of Mathematics",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for all Secondary Mathematics students."},
          {"subject": "MATH", "catalog": "235", "title": "Algebra 1",                                      "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Recommended complementary mathematics course."},
          {"subject": "MATH", "catalog": "242", "title": "Analysis 1",                                     "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Recommended complementary mathematics course."},
          {"subject": "MATH", "catalog": "340", "title": "Discrete Structures 1",                          "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "346", "title": "Number Theory",                                  "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Number theory is integral to the secondary and CÉGEP math curriculum."},
          {"subject": "MATH", "catalog": "348", "title": "Euclidean Geometry",                             "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Geometry is a major strand in the Quebec secondary math curriculum."},
          {"subject": "MATH", "catalog": "430", "title": "Mathematical Logic",                             "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bed_smath_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 free elective credits.",
        "sort_order": 6,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. Secondary Science and Technology  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_secondary_science",
    "name": "B.Ed. – Secondary Science and Technology",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "The B.Ed. Secondary Science and Technology program prepares teachers for Grades 7–11 in Quebec. "
      "Students complete 51 credits in science courses across four Quebec S&T curriculum domains "
      "(Living World, Material World, Earth & Space, Technological World), alongside Education "
      "professional courses and practicums (120 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-secondary-science-and-technology",
    "blocks": [
      {
        "block_key": "bed_ssci_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 31,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required professional education courses shared across all B.Ed. Secondary programs.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "254", "title": "Second Professional Seminar (Secondary)",        "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "351", "title": "Third Professional Seminar (Secondary)",         "credits": 2, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "304", "title": "Measurement and Evaluation",                     "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True},
          {"subject": "EDTL", "catalog": "520", "title": "Perspectives on Knowledge in Mathematics and Science", "credits": 3, "is_required": True, "recommended": True},
          {"subject": "EDEC", "catalog": "404", "title": "Fourth Year Professional Seminar (Secondary)", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssci_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressive secondary school practicums.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "200", "title": "First Field Experience",                         "credits": 2, "is_required": True},
          {"subject": "EDFE", "catalog": "254", "title": "Second Field Experience (Secondary)",            "credits": 3, "is_required": True},
          {"subject": "EDFE", "catalog": "351", "title": "Third Field Experience (Secondary)",             "credits": 8, "is_required": True},
          {"subject": "EDFE", "catalog": "451", "title": "Fourth Field Experience (Secondary)",            "credits": 7, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssci_methods",
        "title": "Secondary Science Teaching Methods",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Methods courses for teaching Science and Technology at the secondary level.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDES", "catalog": "335", "title": "Teaching Secondary Science 1",                    "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDES", "catalog": "435", "title": "Teaching Secondary Science 2",                    "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssci_teachable_required",
        "title": "Required Science Courses",
        "block_type": "required",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Required foundation courses across four Quebec S&T curriculum domains. "
          "Minimum 24 credits with C or higher required before 3rd Field Experience."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "MATH", "catalog": "203", "title": "Principles of Statistics 1",                     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Statistics course for Secondary Science & Technology program."},
          {"subject": "EDTL", "catalog": "520", "title": "Perspectives on Knowledge in Mathematics and Science", "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Required History of Science course for Secondary Science & Technology."},
          {"subject": "CHEM", "catalog": "281", "title": "Inorganic Chemistry 1",                          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Material World course."},
          {"subject": "BIOL", "catalog": "206", "title": "Methods in Biology",                             "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Living World course."},
          {"subject": "EDTL", "catalog": "525", "title": "Teaching Science and Technology",                "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required Technological World course."},
        ],
      },
      {
        "block_key": "bed_ssci_teachable_complementary",
        "title": "Complementary Science Courses",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Core complementary (10 cr): Living World (3 cr from BIOL 200 or LSCI 202), "
          "Material World (3 cr from CHEM 203 or CHEM 213), Material World (4 cr CHEM 212). "
          "Additional complementary (26 cr): choose from Living World, Earth & Space, Environmental, "
          "Material World, and Technological World course lists. At least 9 credits must be at the 300-level or above."
        ),
        "sort_order": 5,
        "courses": [
          {"subject": "BIOL", "catalog": "200", "title": "Molecular Biology",                              "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Core complementary Living World course."},
          {"subject": "LSCI", "catalog": "202", "title": "Biochemistry: Principles and Applications",     "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Alternative core complementary Living World course."},
          {"subject": "CHEM", "catalog": "203", "title": "Organic Chemistry – Reactivity and Mechanism",  "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Core complementary Material World course (alternative to CHEM 213)."},
          {"subject": "CHEM", "catalog": "213", "title": "Organic Chemistry: Reactivity and Mechanism",   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Core complementary Material World course (alternative to CHEM 203)."},
          {"subject": "CHEM", "catalog": "212", "title": "Introductory Organic Chemistry 1",              "credits": 4, "is_required": False, "recommended": True,  "recommendation_reason": "Core complementary Material World course (4 credits)."},
          {"subject": "BIOL", "catalog": "202", "title": "Basic Genetics",                                 "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EPSC", "catalog": "180", "title": "Earthquakes, Volcanoes and Other Hazards",       "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Earth sciences are a key strand in the Quebec S&T curriculum."},
          {"subject": "EPSC", "catalog": "220", "title": "Climate Change Science",                         "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Climate change is central to the Quebec S&T Earth & Space domain."},
          {"subject": "COMP", "catalog": "202", "title": "Foundations of Programming",                     "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Computational thinking and coding are part of the Technology strand."},
        ],
      },
      {
        "block_key": "bed_ssci_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 free elective credits.",
        "sort_order": 6,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. Secondary Social Sciences – History & Geography  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_secondary_social_sciences_geo",
    "name": "B.Ed. – Secondary Social Sciences (History & Geography)",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "Prepares teachers to deliver History & Citizenship and Geography courses in Quebec secondary "
      "schools (Grades 7–11). Students complete 51 credits split between History (9 required + 24 complementary) "
      "and Geography (18 complementary) alongside Education professional courses and practicums (120 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-secondary-social-sciences-history-and-citizenship-geography",
    "blocks": [
      {
        "block_key": "bed_ssoc_geo_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 28,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required professional education courses shared across all B.Ed. Secondary programs.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "254", "title": "Second Professional Seminar (Secondary)",        "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "351", "title": "Third Professional Seminar (Secondary)",         "credits": 2, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "304", "title": "Measurement and Evaluation",                     "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "404", "title": "Fourth Year Professional Seminar (Secondary)", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssoc_geo_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressive secondary school practicums.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "200", "title": "First Field Experience",                         "credits": 2, "is_required": True},
          {"subject": "EDFE", "catalog": "254", "title": "Second Field Experience (Secondary)",            "credits": 3, "is_required": True},
          {"subject": "EDFE", "catalog": "351", "title": "Third Field Experience (Secondary)",             "credits": 8, "is_required": True},
          {"subject": "EDFE", "catalog": "451", "title": "Fourth Field Experience (Secondary)",            "credits": 7, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssoc_geo_methods",
        "title": "Social Sciences Teaching Methods",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "Methods courses for teaching Social Sciences at the secondary level.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDES", "catalog": "334", "title": "Teaching Secondary Social Studies 1",            "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDES", "catalog": "434", "title": "Teaching Secondary Social Studies 2",            "credits": 3, "is_required": True},
          {"subject": "EDER", "catalog": "372", "title": "Culture and Citizenship in Quebec Context",      "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Directly relevant to teaching History & Citizenship in Quebec."},
        ],
      },
      {
        "block_key": "bed_ssoc_geo_teachable_history",
        "title": "Teachable – History (33 credits: 9 required + 24 complementary)",
        "block_type": "required",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "9 credits required from HIST 202, 203, and 303 (survey History of Canada/Quebec courses). "
          "24 additional complementary History credits: min 9 at 300/400 level; "
          "3–9 cr European history, 3–9 cr Asian/African/American history, 6 cr thematic history; "
          "6–12 cr interdisciplinary (min 3 from ECON, min 3 from POLI)."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "HIST", "catalog": "202", "title": "Survey: Canada to 1867",                         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core required content for the Quebec History & Citizenship curriculum."},
          {"subject": "HIST", "catalog": "203", "title": "Survey: Canada since 1867",                      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required survey of Canadian history since Confederation; essential for Quebec History & Citizenship curriculum."},
          {"subject": "HIST", "catalog": "303", "title": "History of Quebec",                              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Essential for teaching Quebec history and citizenship."},
          {"subject": "HIST", "catalog": "217", "title": "The World at War, 1914–1945",                    "credits": 3, "is_required": False, "recommended": True},
          {"subject": "HIST", "catalog": "218", "title": "History of the Contemporary World since 1945",   "credits": 3, "is_required": False, "recommended": True},
          {"subject": "HIST", "catalog": "340", "title": "Indigenous Peoples of Canada",                   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Increasingly important component of the History & Citizenship curriculum."},
          {"subject": "HIST", "catalog": "304", "title": "Europe in the Modern World",                     "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bed_ssoc_geo_teachable_geography",
        "title": "Teachable – Geography (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "18 credits of Geography courses chosen in consultation with Program Adviser from courses that comprise the B.A. Minor Concentration in Geography.",
        "sort_order": 5,
        "courses": [
          {"subject": "GEOG", "catalog": "205", "title": "Global Change: Past, Present and Future",        "credits": 3, "is_required": False, "recommended": True},
          {"subject": "GEOG", "catalog": "216", "title": "Geography of the World Economy",                 "credits": 3, "is_required": False, "recommended": True},
          {"subject": "GEOG", "catalog": "217", "title": "Cities in the Modern World",                     "credits": 3, "is_required": False, "recommended": True},
          {"subject": "GEOG", "catalog": "272", "title": "Earth's Changing Surface",                       "credits": 3, "is_required": False, "recommended": True},
          {"subject": "GEOG", "catalog": "311", "title": "Economic Geography",                             "credits": 3, "is_required": False, "recommended": True},
          {"subject": "GEOG", "catalog": "331", "title": "Urban Social Geography",                         "credits": 3, "is_required": False, "recommended": True},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth",                             "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bed_ssoc_geo_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 free elective credits.",
        "sort_order": 6,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. Secondary Social Sciences – History & Culture/Citizenship QC
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_secondary_social_sciences_cq",
    "name": "B.Ed. – Secondary Social Sciences (History & Culture/Citizenship in QC)",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "Prepares teachers to deliver History & Citizenship and Culture & Citizenship in Quebec courses "
      "in Quebec secondary schools. Combines History courses with Canadian Studies, Quebec Studies, "
      "and Education courses to cover both curriculum strands (120 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-secondary-social-sciences-history-and-citizenship-culture-and-citizenship",
    "blocks": [
      {
        "block_key": "bed_ssoc_cq_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 28,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required professional education courses shared across all B.Ed. Secondary programs.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "254", "title": "Second Professional Seminar (Secondary)",        "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "351", "title": "Third Professional Seminar (Secondary)",         "credits": 2, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "304", "title": "Measurement and Evaluation",                     "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "404", "title": "Fourth Year Professional Seminar (Secondary)", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssoc_cq_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressive secondary school practicums.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "200", "title": "First Field Experience",                         "credits": 2, "is_required": True},
          {"subject": "EDFE", "catalog": "254", "title": "Second Field Experience (Secondary)",            "credits": 3, "is_required": True},
          {"subject": "EDFE", "catalog": "351", "title": "Third Field Experience (Secondary)",             "credits": 8, "is_required": True},
          {"subject": "EDFE", "catalog": "451", "title": "Fourth Field Experience (Secondary)",            "credits": 7, "is_required": True},
        ],
      },
      {
        "block_key": "bed_ssoc_cq_methods",
        "title": "Teaching Methods – Social Sciences & Culture/Citizenship",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "Methods courses including the Culture and Citizenship in Quebec strand.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDES", "catalog": "334", "title": "Teaching Secondary Social Sciences 1",           "credits": 3, "is_required": True},
          {"subject": "EDES", "catalog": "350", "title": "Teaching Secondary Social Sciences 2",           "credits": 3, "is_required": True},
          {"subject": "EDER", "catalog": "372", "title": "Culture and Citizenship in Quebec Context",      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required methods course specific to the Culture and Citizenship in QC strand."},
        ],
      },
      {
        "block_key": "bed_ssoc_cq_teachable_history",
        "title": "Teachable – History (24 credits: 9 required + 15 complementary)",
        "block_type": "required",
        "credits_needed": 24,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "9 credits required from HIST 202, 203, and 303. "
          "15 additional complementary History credits at 200–400 level, min 9 at 300/400 level."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "HIST", "catalog": "202", "title": "Survey: Canada to 1867",                         "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "HIST", "catalog": "203", "title": "Survey: Canada since 1867",                      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required survey of Canadian history since Confederation."},
          {"subject": "HIST", "catalog": "303", "title": "History of Quebec",                              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for teaching Quebec history and citizenship."},
          {"subject": "HIST", "catalog": "217", "title": "The World at War, 1914–1945",                    "credits": 3, "is_required": False, "recommended": True},
          {"subject": "HIST", "catalog": "218", "title": "History of the Contemporary World since 1945",   "credits": 3, "is_required": False, "recommended": True},
          {"subject": "HIST", "catalog": "340", "title": "Indigenous Peoples of Canada",                   "credits": 3, "is_required": False, "recommended": True},
        ],
      },
      {
        "block_key": "bed_ssoc_cq_teachable_culture",
        "title": "Teachable – Culture & Citizenship in Quebec (up to 9 credits)",
        "block_type": "choose_credits",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "Up to 9 credits from Culture and Citizenship course lists (no more than 3 credits from each subsection). "
          "Culture subsection (up to 6 cr): CANS 413, CANS 415, QCST 200, QCST 300, QCST 440. "
          "Citizenship subsection (up to 6 cr): CANS 413, EDEC 374, EDER 252, EDER 536, ENVR 201."
        ),
        "sort_order": 5,
        "courses": [
          {"subject": "CANS", "catalog": "413", "title": "Canada and Quebec Seminar",                      "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Counts in both Culture and Citizenship subsections; highly relevant to teaching Quebec identity."},
          {"subject": "CANS", "catalog": "415", "title": "Black Canada",                                   "credits": 3, "is_required": False, "recommended": True},
          {"subject": "QCST", "catalog": "200", "title": "Introduction to the Study of Quebec",            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Core Quebec Studies course; essential background for the Culture & Citizenship in QC curriculum."},
          {"subject": "QCST", "catalog": "300", "title": "Quebec Culture and Society",                     "credits": 3, "is_required": False, "recommended": True},
          {"subject": "QCST", "catalog": "440", "title": "Contemporary Issues in Quebec",                  "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDEC", "catalog": "374", "title": "Education and the Environment",                  "credits": 3, "is_required": False},
          {"subject": "EDER", "catalog": "252", "title": "Understanding and Teaching Jewish Life",          "credits": 3, "is_required": False},
          {"subject": "EDER", "catalog": "536", "title": "Critical and Ethical Dimensions of Sexualities Education", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability",        "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bed_ssoc_cq_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 free elective credits.",
        "sort_order": 6,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. TESL Elementary and Secondary  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_tesl",
    "name": "B.Ed. – Teaching English as a Second Language (TESL Elem/Sec)",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "The B.Ed. TESL program certifies teachers to teach English as a Second Language at both the "
      "elementary and secondary levels in Quebec. Students complete approximately 48 credits in EDSL "
      "subject content courses covering L2 education, linguistics, literacy, oral skills, grammar, "
      "assessment, and TESL methods, alongside Education professional courses and four practicums (120 total). "
      "Admission requires a separate application and selection process."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-education-bed-teaching-english-second-language-tesl-elementary-and-secondary",
    "blocks": [
      {
        "block_key": "bed_tesl_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "TESL program uses EDSL-numbered professional seminars rather than EDEC. "
          "Shared Education courses (EDEC 215, 233, 247, 260, 262; EDPE 300; EDPI 309, 341) "
          "are combined with TESL-specific seminars (EDSL 210, 215, 254, 315, 415) and EDES methods."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "EDSL", "catalog": "210", "title": "First Professional Seminar (TESL)",             "credits": 1, "is_required": True},
          {"subject": "EDSL", "catalog": "215", "title": "Communication in Education for TESL in Quebec", "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)", "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                          "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDSL", "catalog": "254", "title": "Second Professional Seminar (TESL)",            "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",        "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",               "credits": 3, "is_required": True},
          {"subject": "EDSL", "catalog": "315", "title": "Third Year Professional Seminar (TESL)",        "credits": 2, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",        "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "309", "title": "Diverse Learners",                              "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",              "credits": 3, "is_required": True},
          {"subject": "EDES", "catalog": "350", "title": "Classroom Practices (TESL)",                   "credits": 3, "is_required": True},
          {"subject": "EDES", "catalog": "361", "title": "Teaching Secondary English 1",                  "credits": 3, "is_required": True},
          {"subject": "EDSL", "catalog": "415", "title": "Fourth Professional Seminar (TESL)",            "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_tesl_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four practicums covering ESL instruction at both elementary and secondary levels.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "209", "title": "First Field Experience",                         "credits": 2,  "is_required": True},
          {"subject": "EDFE", "catalog": "255", "title": "Second Field Experience (TESL)",                 "credits": 3,  "is_required": True},
          {"subject": "EDFE", "catalog": "359", "title": "Third Field Experience (TESL)",                  "credits": 8,  "is_required": True},
          {"subject": "EDFE", "catalog": "459", "title": "Fourth Field Experience (TESL)",                 "credits": 7,  "is_required": True},
        ],
      },
      {
        "block_key": "bed_tesl_esl_methods",
        "title": "ESL Methodology and Curriculum",
        "block_type": "required",
        "credits_needed": 48,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "TESL-specific required courses covering foundations of L2 education, sociolinguistics, "
          "classroom settings, grammar, literacy (reading and writing), oral skills, assessment, "
          "and TESL methods. LING 200 or 201 also required. "
          "Professional seminars EDSL 210, 215, 254, 315, 415 are included in the professional core."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "EDSL", "catalog": "300", "title": "Foundations of L2 Education",                   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core foundations course for TESL program."},
          {"subject": "EDSL", "catalog": "304", "title": "Sociolinguistics and L2 Education",              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required sociolinguistics course."},
          {"subject": "EDSL", "catalog": "305", "title": "L2 Learning: Classroom Settings",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required language acquisition in classroom contexts course."},
          {"subject": "EDSL", "catalog": "311", "title": "Pedagogical Grammar",                           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core course in grammar and language structure for ESL instruction."},
          {"subject": "EDSL", "catalog": "330", "title": "Literacy 1: Teaching Reading in ESL",           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required reading instruction course."},
          {"subject": "EDSL", "catalog": "332", "title": "Literacy 2: Teaching Writing in ESL",           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required writing instruction course."},
          {"subject": "EDSL", "catalog": "334", "title": "Teaching Oral Skills in ESL",                   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required oral skills instruction course."},
          {"subject": "EDSL", "catalog": "350", "title": "Essentials of English Grammar",                 "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required grammar reference course for ESL teachers."},
          {"subject": "EDSL", "catalog": "412", "title": "Assessment in TESL",                            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required assessment course for TESL."},
          {"subject": "EDSL", "catalog": "447", "title": "Methods in TESL 1",                             "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required TESL methods course."},
          {"subject": "EDSL", "catalog": "458", "title": "Methods in TESL 2",                             "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required TESL methods course."},
          {"subject": "LING", "catalog": "201", "title": "Introduction to Linguistics",                   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Essential foundation for understanding how language works (LING 200 accepted as alternative)."},
        ],
      },
      {
        "block_key": "bed_tesl_linguistics",
        "title": "Complementary Courses",
        "block_type": "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "3 cr equity education (EDEC 248 or 249); 3 cr arts education (EDEA 332, 342, 345, or EDKP 332); "
          "3–6 cr ENGL courses; 3–6 cr foreign language, FRSL, or other complementary electives."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "EDEC", "catalog": "248", "title": "Anti-Racism Education",                         "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Required equity education component (alternative to EDEC 249)."},
          {"subject": "EDEC", "catalog": "249", "title": "Global Education and Social Justice",            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Required equity education component (alternative to EDEC 248)."},
          {"subject": "LING", "catalog": "330", "title": "Phonetics",                                      "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Pronunciation and phonetics are critical for ESL instruction."},
          {"subject": "LING", "catalog": "360", "title": "Bilingualism",                                   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Directly relevant to Quebec's bilingual educational context."},
          {"subject": "ENGL", "catalog": "234", "title": "Canadian Literature",                            "credits": 3, "is_required": False},
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True,  "recommendation_reason": "French proficiency strongly recommended for teaching in Quebec."},
        ],
      },
      {
        "block_key": "bed_tesl_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 unrestricted elective credits.",
        "sort_order": 5,
        "courses": [],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.A.(Education) – Education in Global Contexts  (90 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "ba_education_global_contexts",
    "name": "B.A.(Education) – Education in Global Contexts",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 90,
    "description": (
      "The 90-credit B.A.(Education) is a non-certification degree focused on educational theory, "
      "policy, and international development rather than K-12 teacher preparation. It equips students "
      "for careers in international education, NGOs, policy research, and community education. "
      "Out-of-province students complete an additional 30-credit Freshman year (120 total)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/ug_edu_integrated_studies_education",
    "blocks": [
      {
        "block_key": "ba_edu_foundations",
        "title": "Educational Foundations",
        "block_type": "required",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name": None,
        "notes": "Core Education theory and policy courses required for the program.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEM", "catalog": "220", "title": "Contemporary Issues in Education",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Gateway course; broad introduction to global and local education issues."},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "249", "title": "Global Education and Social Justice",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core course for the program; directly addresses global education challenges."},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDER", "catalog": "536", "title": "Critical and Ethical Dimensions of Sexualities Education", "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDPI", "catalog": "526", "title": "Supporting Students' Strengths and Talents",     "credits": 3, "is_required": False},
          {"subject": "EDPE", "catalog": "400", "title": "Assessment in Education",                        "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "ba_edu_global_electives",
        "title": "Global and Social Context Electives",
        "block_type": "choose_credits",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name": None,
        "notes": "Choose courses in international development, sociology, anthropology, political science, and related disciplines.",
        "sort_order": 2,
        "courses": [
          {"subject": "IDSC", "catalog": "200", "title": "Introduction to International Development",      "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Strong complement to the global education focus of this program."},
          {"subject": "SOCI", "catalog": "225", "title": "Introduction to Sociology",                      "credits": 3, "is_required": False, "recommended": True},
          {"subject": "ANTH", "catalog": "203", "title": "Anthropology of Culture",                        "credits": 3, "is_required": False, "recommended": True},
          {"subject": "POLI", "catalog": "244", "title": "Third World Politics",                           "credits": 3, "is_required": False, "recommended": True},
          {"subject": "GEOG", "catalog": "201", "title": "Human Environment",                              "credits": 3, "is_required": False, "recommended": True},
          {"subject": "LING", "catalog": "201", "title": "Introduction to Linguistics",                    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Language and multilingualism are central to global education."},
        ],
      },
      {
        "block_key": "ba_edu_free_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 27,
        "courses_needed": None,
        "group_name": None,
        "notes": "Remaining credits to complete the 90-credit program.",
        "sort_order": 3,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True},
          {"subject": "FRSL", "catalog": "221", "title": "Oral and Written French 2",                      "credits": 6, "is_required": False, "recommended": True},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Ed. Physical and Health Education  (120 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bed_physical_health_education",
    "name": "B.Ed. – Physical and Health Education",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 120,
    "description": (
      "The B.Ed. Physical and Health Education program certifies teachers to deliver P.E. and Health "
      "across all grade levels in Quebec schools. The 120-credit program combines EDKP kinesiology "
      "content courses with Education professional studies and four practicums."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/ug_edu_kinesiology_physical_education",
    "blocks": [
      {
        "block_key": "bed_phe_professional_core",
        "title": "Professional Core – Education Courses",
        "block_type": "required",
        "credits_needed": 27,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required professional education courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "EDEC", "catalog": "201", "title": "First Year Professional Seminar",                "credits": 1, "is_required": True},
          {"subject": "EDEC", "catalog": "203", "title": "Communication in Education",                     "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "215", "title": "English Exam for Teacher Certification (EETC)",  "credits": 0, "is_required": True},
          {"subject": "EDEC", "catalog": "233", "title": "Indigenous Education",                           "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "247", "title": "Policy Issues in Quebec and Indigenous Education","credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "260", "title": "Philosophical Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDEC", "catalog": "262", "title": "Media, Technology and Education",                "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "300", "title": "Psychological Foundations of Education",         "credits": 3, "is_required": True},
          {"subject": "EDPE", "catalog": "400", "title": "Assessment in Education",                        "credits": 3, "is_required": True},
          {"subject": "EDPI", "catalog": "341", "title": "Instruction in Inclusive Schools",               "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bed_phe_field_experiences",
        "title": "Field Experiences (Practicums)",
        "block_type": "required",
        "credits_needed": 20,
        "courses_needed": None,
        "group_name": None,
        "notes": "Four progressive P.E. teaching practicums in schools.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDFE", "catalog": "246", "title": "First Field Experience",                         "credits": 3,  "is_required": True},
          {"subject": "EDFE", "catalog": "373", "title": "Second Field Experience (P.E.)",                 "credits": 3,  "is_required": True},
          {"subject": "EDFE", "catalog": "380", "title": "Third Field Experience (P.E.)",                  "credits": 7,  "is_required": True},
          {"subject": "EDFE", "catalog": "480", "title": "Fourth Field Experience (P.E.)",                 "credits": 7,  "is_required": True},
        ],
      },
      {
        "block_key": "bed_phe_kinesiology",
        "title": "Physical Education and Kinesiology Courses",
        "block_type": "required",
        "credits_needed": 42,
        "courses_needed": None,
        "group_name": None,
        "notes": "EDKP content and methods courses specific to Physical and Health Education teacher preparation.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDKP", "catalog": "100", "title": "Introduction to Physical and Health Education in Quebec", "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Foundational overview of PHE teaching in Quebec; taken in U1."},
          {"subject": "EDKP", "catalog": "204", "title": "Health Education",                               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Health Education is a core strand of the Quebec PHE curriculum."},
          {"subject": "EDKP", "catalog": "208", "title": "Biomechanics and Motor Learning",                "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "213", "title": "Aquatics",                                       "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "215", "title": "Standard First Aid/Cardio-Pulmonary Resuscitation Level C", "credits": 0, "is_required": True},
          {"subject": "EDKP", "catalog": "217", "title": "Track and Field",                                "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "223", "title": "Games 1: Elementary Physical Education",         "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "225", "title": "Games 2: Secondary Physical Education",          "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "232", "title": "Health-Related Fitness",                         "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "235", "title": "Non-Traditional Physical Activities",            "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "237", "title": "Outdoor Education",                              "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "253", "title": "Movement Education",                             "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "261", "title": "Motor Development",                              "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "292", "title": "Nutrition and Wellness",                         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Nutrition and wellness is part of the Health Education strand in Quebec."},
          {"subject": "EDKP", "catalog": "293", "title": "Anatomy and Physiology",                         "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "307", "title": "Evaluation in Physical Education",               "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "330", "title": "Physical Activity and Public Health",            "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "342", "title": "Physical Education Methods",                     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core methods course for PHE teacher preparation."},
          {"subject": "EDKP", "catalog": "391", "title": "Physiology in Sport and Exercise",               "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "394", "title": "Historical Perspectives",                        "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "396", "title": "Adapted Physical Activity",                      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required for Quebec P.E. teachers; covers inclusive physical activity for students with disabilities."},
          {"subject": "EDKP", "catalog": "442", "title": "Physical Education Pedagogy",                    "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "443", "title": "Research Methods",                               "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "448", "title": "Exercise and Health Psychology",                 "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "494", "title": "Physical Education Curriculum Development",      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Curriculum development course directly relevant to Quebec PHE program planning."},
          {"subject": "EDKP", "catalog": "498", "title": "Sport Psychology",                               "credits": 3, "is_required": True,  "recommended": True},
        ],
      },
      {
        "block_key": "bed_phe_electives",
        "title": "Complementary and Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 25,
        "courses_needed": None,
        "group_name": None,
        "notes": "Remaining credits including FRSL and elective EDKP or Education courses.",
        "sort_order": 4,
        "courses": [
          {"subject": "FRSL", "catalog": "211", "title": "Oral and Written French 1",                      "credits": 6, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "340", "title": "Psychology of Physical Activity",                "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "449", "title": "Neuromuscular and Inflammatory Pathophysiology", "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "485", "title": "Cardiopulmonary Exercise Pathophysiology",       "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Sc.(Kinesiology) – Kinesiology  (90 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bsc_kinesiology",
    "name": "B.Sc.(Kinesiology) – Kinesiology",
    "program_type": "major",
    "faculty": "Faculty of Education",
    "total_credits": 90,
    "description": (
      "The 90-credit B.Sc.(Kinesiology) provides a comprehensive understanding of human movement "
      "from biological, psychological, and social perspectives. Equips graduates for careers as "
      "kinesiologists, in health promotion, rehabilitation, or graduate study. "
      "Students without CEGEP complete a 30-credit Freshman year (science prerequisites) for 120 total. "
      "Graduation requires proof of Standard First Aid/CPR Level C certification."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-science-kinesiology-bsckinesiology-kinesiology",
    "blocks": [
      {
        "block_key": "bsc_kin_freshman",
        "title": "Freshman Prerequisites (Science Foundation)",
        "block_type": "required",
        "credits_needed": 29,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required for students without CEGEP equivalencies. BIOL, CHEM, MATH, and PHYS foundation courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "BIOL", "catalog": "111", "title": "Principles: Organismal Biology",                 "credits": 3, "is_required": True},
          {"subject": "BIOL", "catalog": "112", "title": "Cell and Molecular Biology",                     "credits": 3, "is_required": True},
          {"subject": "CHEM", "catalog": "110", "title": "General Chemistry 1",                            "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120", "title": "General Chemistry 2",                            "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "140", "title": "Calculus 1",                                     "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141", "title": "Calculus 2",                                     "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "101", "title": "Introductory Physics – Mechanics",               "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "102", "title": "Introductory Physics – Electromagnetism",        "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "bsc_kin_required",
        "title": "Required Courses (51 credits)",
        "block_type": "required",
        "credits_needed": 51,
        "courses_needed": None,
        "group_name": None,
        "notes": "Core required courses for the B.Sc.(Kinesiology) program. EDKP 215 (Standard First Aid/CPR Level C) is also required as a 0-credit certification.",
        "sort_order": 2,
        "courses": [
          {"subject": "ANAT", "catalog": "315", "title": "Clinical Human Musculoskeletal Anatomy",         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Essential anatomy; taken in U1 and used in all physiology/biomechanics courses."},
          {"subject": "ANAT", "catalog": "316", "title": "Clinical Human Visceral Anatomy",                "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "206", "title": "Biomechanics of Human Movement",                "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Foundational biomechanics; required prereq for most upper-year EDKP courses."},
          {"subject": "EDKP", "catalog": "250", "title": "Introductory Principles in Applied Kinesiology", "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "261", "title": "Motor Development",                              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required core course covering lifespan motor development."},
          {"subject": "EDKP", "catalog": "292", "title": "Nutrition and Wellness",                         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required nutrition course for the B.Sc. Kinesiology program."},
          {"subject": "EDKP", "catalog": "330", "title": "Physical Activity and Public Health",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required public health and physical activity course."},
          {"subject": "EDKP", "catalog": "350", "title": "Physical Fitness Evaluation Methods",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Hands-on fitness assessment skills directly used in professional kinesiology practice."},
          {"subject": "EDKP", "catalog": "395", "title": "Exercise Physiology",                            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core physiology of exercise; prerequisite for most 400-level EDKP courses."},
          {"subject": "EDKP", "catalog": "396", "title": "Adapted Physical Activity",                      "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required adapted physical activity course."},
          {"subject": "EDKP", "catalog": "443", "title": "Research Methods",                               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required research methods course for understanding kinesiology evidence base."},
          {"subject": "EDKP", "catalog": "447", "title": "Motor Control",                                  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required motor control course covering neuroscience of movement."},
          {"subject": "EDKP", "catalog": "448", "title": "Exercise and Health Psychology",                 "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required psychological aspects of exercise and health."},
          {"subject": "EDKP", "catalog": "450", "title": "Advanced Principles in Applied Kinesiology",    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Capstone applied kinesiology course integrating program knowledge."},
          {"subject": "EDKP", "catalog": "498", "title": "Sport Psychology",                               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required sport psychology course."},
          {"subject": "PHGY", "catalog": "209", "title": "Mammalian Physiology 1",                         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Essential physiology; covers cardiovascular and respiratory systems."},
          {"subject": "PHGY", "catalog": "210", "title": "Mammalian Physiology 2",                         "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bsc_kin_complementary",
        "title": "Complementary Electives (12 credits)",
        "block_type": "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "Choose from upper-level EDKP courses and approved complementary courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDKP", "catalog": "430", "title": "Adapted Physical Activity",                      "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Valued for kinesiologists working in rehabilitation settings."},
          {"subject": "EDKP", "catalog": "440", "title": "Exercise for Special Populations",               "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Exercise prescription across diverse clinical populations."},
          {"subject": "EDKP", "catalog": "449", "title": "Neuromuscular and Inflammatory Pathophysiology", "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "485", "title": "Cardiopulmonary Exercise Pathophysiology",       "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Key for kinesiologists in cardiac and pulmonary rehabilitation."},
          {"subject": "EDKP", "catalog": "495", "title": "Scientific Principles of Training",              "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "496", "title": "Biochemistry of Exercise",                       "credits": 3, "is_required": False},
          {"subject": "EDKP", "catalog": "498", "title": "Ageing and Physical Activity",                   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Growing area of kinesiology practice with Canada's aging population."},
          {"subject": "EDKP", "catalog": "499", "title": "Neural Control of Human Movement",               "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "300", "title": "Biostatistics",                                  "credits": 3, "is_required": False, "recommended": True},
        ],
      },
      {
        "block_key": "bsc_kin_free_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Remaining credits to reach 90 total.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ────────────────────────────────────────────────────────────
  # B.Sc.(Kinesiology) – Kinesiology Honours  (90 credits)
  # ────────────────────────────────────────────────────────────
  {
    "program_key": "bsc_kinesiology_honours",
    "name": "B.Sc.(Kinesiology) – Kinesiology Honours",
    "program_type": "honours",
    "faculty": "Faculty of Education",
    "total_credits": 90,
    "description": (
      "The Honours B.Sc.(Kinesiology) requires a CGPA of 3.3 after two years in Kinesiology, "
      "maintained until graduation. Students complete all requirements of the regular Kinesiology "
      "program plus an Honours thesis (EDKP 454 + EDKP 499, 9 credits). Prepares students for graduate "
      "study in exercise science, physiotherapy, or medicine."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/education/undergraduate/programs/bachelor-science-kinesiology-bsckinesiology-kinesiology-honours",
    "blocks": [
      {
        "block_key": "bsc_kin_hon_required",
        "title": "Required Courses – All Regular Kinesiology Requirements",
        "block_type": "required",
        "credits_needed": 45,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required courses from the regular B.Sc.(Kinesiology) program.",
        "sort_order": 1,
        "courses": [
          {"subject": "ANAT", "catalog": "315", "title": "Clinical Human Musculoskeletal Anatomy",         "credits": 3, "is_required": True},
          {"subject": "ANAT", "catalog": "316", "title": "Clinical Human Visceral Anatomy",                "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "206", "title": "Biomechanics of Human Movement",                "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "250", "title": "Introductory Principles in Applied Kinesiology", "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "280", "title": "Motor Development",                              "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "320", "title": "Nutrition and Physical Activity",                "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "340", "title": "Psychology of Physical Activity",                "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "350", "title": "Physical Fitness Evaluation Methods",            "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "395", "title": "Exercise Physiology",                            "credits": 3, "is_required": True,  "recommended": True},
          {"subject": "EDKP", "catalog": "420", "title": "Measurement and Evaluation in Kinesiology",     "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "450", "title": "Advanced Principles in Applied Kinesiology",    "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "480", "title": "Sociology of Sport and Physical Activity",       "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "209", "title": "Mammalian Physiology 1",                         "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "210", "title": "Mammalian Physiology 2",                         "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "499", "title": "Neural Control of Human Movement",               "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bsc_kin_hon_thesis",
        "title": "Honours Thesis",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "Required independent research thesis supervised by a faculty member. Requires CGPA of 3.3 maintained throughout.",
        "sort_order": 2,
        "courses": [
          {"subject": "EDKP", "catalog": "454", "title": "Honours Research Practicum",              "credits": 3, "is_required": True},
          {"subject": "EDKP", "catalog": "499", "title": "Undergraduate Honours Research Project",  "credits": 6, "is_required": True},
        ],
      },
      {
        "block_key": "bsc_kin_hon_complementary",
        "title": "Complementary Electives",
        "block_type": "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "Choose from upper-level EDKP courses and approved complementary courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "EDKP", "catalog": "449", "title": "Neuromuscular and Inflammatory Pathophysiology", "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "485", "title": "Cardiopulmonary Exercise Pathophysiology",       "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "495", "title": "Scientific Principles of Training",              "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "498", "title": "Ageing and Physical Activity",                   "credits": 3, "is_required": False, "recommended": True},
          {"subject": "EDKP", "catalog": "496", "title": "Biochemistry of Exercise",                       "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "300", "title": "Biostatistics",                                  "credits": 3, "is_required": False, "recommended": True},
        ],
      },
      {
        "block_key": "bsc_kin_hon_free_electives",
        "title": "Free Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Remaining credits to reach 90 total.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

]


# ─────────────────────────────────────────────────────────────────────────────
# Seed function
# ─────────────────────────────────────────────────────────────────────────────
def seed_degree_requirements(supabase):
    """
    Seed all Education faculty programs into the degree_requirements tables.
    Uses delete+insert pattern (matching other faculty seeds).
    Returns a summary dict of counts.
    """
    results = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in EDUCATION_PROGRAMS:
        try:
            # ── Upsert program ──────────────────────────────────────────────
            prog_row = {
                "program_key":   prog["program_key"],
                "name":          prog["name"],
                "program_type":  prog["program_type"],
                "faculty":       prog["faculty"],
                "total_credits": prog["total_credits"],
                "description":   prog.get("description", ""),
                "ecalendar_url": prog.get("ecalendar_url", ""),
            }
            prog_result = (
                supabase.table("degree_programs")
                .upsert(prog_row, on_conflict="program_key")
                .execute()
            )
            if not prog_result.data:
                results["errors"].append(f"Failed to upsert program: {prog['program_key']}")
                continue

            prog_id = prog_result.data[0]["id"]
            results["programs"] += 1

            # ── Delete existing blocks (cascades to courses) ────────────────
            supabase.table("requirement_blocks").delete().eq("program_id", prog_id).execute()

            for block in prog.get("blocks", []):
                # ── Insert block ────────────────────────────────────────────
                block_row = {
                    "program_id":     prog_id,
                    "block_key":      block["block_key"],
                    "title":          block["title"],
                    "block_type":     block["block_type"],
                    "credits_needed": block.get("credits_needed"),
                    "courses_needed": block.get("courses_needed"),
                    "group_name":     block.get("group_name"),
                    "notes":          block.get("notes", ""),
                    "sort_order":     block.get("sort_order", 0),
                }
                block_result = (
                    supabase.table("requirement_blocks")
                    .insert(block_row)
                    .execute()
                )
                if not block_result.data:
                    results["errors"].append(f"Failed to insert block: {block['block_key']}")
                    continue

                block_id = block_result.data[0]["id"]
                results["blocks"] += 1

                courses_batch = []
                for idx, course in enumerate(block.get("courses", [])):
                    courses_batch.append({
                        "block_id":              block_id,
                        "subject":               course["subject"],
                        "catalog":               course["catalog"],
                        "title":                 course.get("title", ""),
                        "credits":               course.get("credits", 3),
                        "is_required":           course.get("is_required", False),
                        "recommended":           course.get("recommended", False),
                        "recommendation_reason": course.get("recommendation_reason", ""),
                        "sort_order":            idx,
                    })

                if courses_batch:
                    course_result = (
                        supabase.table("requirement_courses")
                        .insert(courses_batch)
                        .execute()
                    )
                    if course_result.data:
                        results["courses"] += len(course_result.data)
                    else:
                        results["errors"].append(
                            f"Failed to insert courses for block: {block['block_key']}"
                        )

        except Exception as e:
            results["errors"].append(f"Error processing {prog.get('program_key', '?')}: {str(e)}")

    return results


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from config import settings
    from supabase import create_client

    sb = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    result = seed_degree_requirements(sb)
    print(f"Seeded: {result['programs']} programs, {result['blocks']} blocks, {result['courses']} courses")
    if result["errors"]:
        print(f"Errors ({len(result['errors'])}):")
        for e in result["errors"]:
            print(f"  - {e}")
