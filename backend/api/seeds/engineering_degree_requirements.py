"""
McGill Faculty of Engineering – Degree Requirements Seed Data
Source: McGill Course Catalogue 2025-2026
https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/

Covers all undergraduate Engineering programs:
  B.Eng. degrees: Bioengineering, Chemical Engineering, Civil Engineering,
                  Computer Engineering, Electrical Engineering, Materials Engineering (Co-op),
                  Mechanical Engineering, Mining Engineering, Software Engineering Co-op
  B.G.E.:         Global Engineering
  B.Sc.(Arch.):   Architecture
  Minors:         Aerospace, Applied AI, Arts, Biomedical Eng., Biotechnology,
                  Chemistry, Computer Science, Construction Mgmt, Economics,
                  Environment, Environmental Engineering, Management, Software Eng.,
                  Technological Entrepreneurship

Accuracy notes:
  - Verified from official McGill Course Catalogue and eCalendar 2024-2026
  - Credit counts are for non-CEGEP (high school) entry; CEGEP students
    typically enter with ~29 credits of Year 0 transfer credit
  - FACC courses (100/200/300/400) are Faculty-wide requirements for all B.Eng. programs
  - Always cross-check with current catalogue before academic decisions
"""

ENGINEERING_PROGRAMS = [

  # ──────────────────────────────────────────────────────────────────────────
  # BIOENGINEERING (B.Eng.) — 142–143 credits
  # Three specialization streams: Biomedical, Biological Systems, Bioresource
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "bioengineering_beng",
    "name": "Bioengineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 142,
    "description": (
      "The B.Eng. in Bioengineering prepares students to apply systematic knowledge of biology, "
      "physical sciences and mathematics to solve problems of a biological nature. Students "
      "complete a common core in bioengineering and specialise in one of three streams: "
      "Stream 1 – Biomedical Engineering, Stream 2 – Biological Systems Engineering, or "
      "Stream 3 – Bioresource Engineering (offered jointly with FAES)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/bioengineering/bioengineering-beng/",
    "blocks": [
      {
        "block_key": "bien_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 29,
        "courses_needed": None,
        "notes": "CEGEP students are generally granted transfer credit for these Year 0 courses. Only BIOL 112 (not BIOL 111) is in Year 0 per the official curriculum.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1",            "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",            "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",    "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                     "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                     "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",            "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",    "credits": 4, "is_required": True},
          {"subject": "BIOL", "catalog": "112",  "title": "Cell and Molecular Biology",     "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bien_required_nondept",
        "title": "Required Non-Departmental Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "FACC 100 must be taken during the first year of study. FACC 250 is 0 credits (non-credit requirement). CHEM 212 is 4 credits.",
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "264",  "title": "Advanced Calculus for Engineers",               "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "203",  "title": "Principles of Statistics 1",                   "credits": 3, "is_required": True},
          {"subject": "CHEM", "catalog": "212",  "title": "Introductory Organic Chemistry 1",              "credits": 4, "is_required": True},
          {"subject": "COMP", "catalog": "208",  "title": "Computer Programming for Physical Sciences and Engineering", "credits": 3, "is_required": True},
          {"subject": "PHYS", "catalog": "319",  "title": "Introduction to Biophysics",                   "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bien_required_core",
        "title": "Required Bioengineering Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "48 credits of required BIEN courses common to all streams.",
        "sort_order": 3,
        "courses": [
          {"subject": "BIEN", "catalog": "200",  "title": "Introduction to Bioengineering",                        "credits": 2, "is_required": True},
          {"subject": "BIEN", "catalog": "210",  "title": "Electrical and Optical Properties of Biological Systems","credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "219",  "title": "Introduction to Physical Molecular and Cell Biology",   "credits": 4, "is_required": True},
          {"subject": "BIEN", "catalog": "220",  "title": "Introduction to Mechanics for Bioengineers",            "credits": 2, "is_required": True},
          {"subject": "BIEN", "catalog": "267",  "title": "Bioanalytical Methods in Bioengineering",               "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "290",  "title": "Bioengineering Measurement Laboratory",                  "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "300",  "title": "Thermodynamics in Bioengineering",                      "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "314",  "title": "Transport Phenomena in Biological Systems 1",           "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "340",  "title": "Transport Phenomena in Biological Systems 2",           "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "350",  "title": "Biosignals, Systems and Control",                       "credits": 4, "is_required": True},
          {"subject": "BIEN", "catalog": "360",  "title": "Physical Chemistry in Bioengineering",                  "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "390",  "title": "Bioengineering Laboratory",                             "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "420",  "title": "Biodevices Design for Diagnostics and Screening",       "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "470D1","title": "Bioengineering Design Project",                         "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "470D2","title": "Bioengineering Design Project",                         "credits": 3, "is_required": True},
          {"subject": "BIEN", "catalog": "471",  "title": "Bioengineering Research Project",                       "credits": 2, "is_required": True},
          {"subject": "BIEN", "catalog": "560",  "title": "Design of Biosensors",                                  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bien_stream1",
        "title": "Stream 1 – Biological Materials and Mechanics",
        "block_type": "group",
        "group_name": "Stream 1",
        "credits_needed": 25,
        "courses_needed": None,
        "notes": "Stream 1 focuses on biological materials, biomechanics, and tissue engineering. 13 credits from List A + 12 credits from List B. Choose this stream for careers in medical devices, biomaterials, and tissue engineering.",
        "sort_order": 4,
        "courses": [
          {"subject": "BIEN", "catalog": "320",  "title": "Molecular, Cellular and Tissue Biomechanics","credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "361",  "title": "Materials for Bio-Applications",              "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "570",  "title": "Active Mechanics in Biology",                 "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "207",  "title": "Solid Mechanics",                             "credits": 4, "is_required": False},
          {"subject": "BIEN", "catalog": "330",  "title": "Tissue Engineering and Regenerative Medicine", "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "450",  "title": "Biological Structures and Assemblies",         "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "462",  "title": "Engineering Principles in Physiological Systems","credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "530",  "title": "Imaging and Bioanalytical Instrumentation",   "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "535",  "title": "Electron Microscopy and 3D Imaging for Biological Materials","credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "545",  "title": "Diagnostic Devices at the Point-of-Care",     "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "550",  "title": "Biomolecular Devices",                         "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "580",  "title": "Synthetic Biology",                            "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "585",  "title": "Metabolic Engineering",                        "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",       "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "321",  "title": "Mechanics of Deformable Solids",               "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",       "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bien_stream2",
        "title": "Stream 2 – Biomolecular and Cellular Engineering",
        "block_type": "group",
        "group_name": "Stream 2",
        "credits_needed": 24,
        "courses_needed": None,
        "notes": "Stream 2 covers molecular engineering, synthetic biology, and biomanufacturing. Ideal for careers in pharma, genomics, and computational biology.",
        "sort_order": 5,
        "courses": [
          {"subject": "BIEN", "catalog": "330",  "title": "Tissue Engineering and Regenerative Medicine", "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "450",  "title": "Biological Structures and Assemblies",         "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "462",  "title": "Engineering Principles in Physiological Systems","credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "530",  "title": "Imaging and Bioanalytical Instrumentation",   "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "545",  "title": "Diagnostic Devices at the Point-of-Care",     "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "550",  "title": "Biomolecular Devices",                         "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "580",  "title": "Synthetic Biology",                            "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "585",  "title": "Metabolic Engineering",                        "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bien_stream3",
        "title": "Stream 3 – Biological Information and Computation",
        "block_type": "group",
        "group_name": "Stream 3",
        "credits_needed": 24,
        "courses_needed": None,
        "notes": "Stream 3 introduces students to information storage and processing in biological systems. Applied in genomics, proteomics, drug discovery, immunology, neurology, and epidemiology.",
        "sort_order": 6,
        "courses": [
          {"subject": "BIEN", "catalog": "330",  "title": "Tissue Engineering and Regenerative Medicine", "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "450",  "title": "Biological Structures and Assemblies",         "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "462",  "title": "Engineering Principles in Physiological Systems","credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "530",  "title": "Imaging and Bioanalytical Instrumentation",   "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "545",  "title": "Diagnostic Devices at the Point-of-Care",     "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "550",  "title": "Biomolecular Devices",                         "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "580",  "title": "Synthetic Biology",                            "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "585",  "title": "Metabolic Engineering",                        "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "bien_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "3 credits from Group A (science/tech elective) and 3 credits from Group B (humanities/social sciences/management). CEGEP students receive 3 credits transfer credit toward Group B.",
        "sort_order": 7,
        "courses": [],
      },

    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # CHEMICAL ENGINEERING (B.Eng.) — 143 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "chemical_engineering_beng",
    "name": "Chemical Engineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 143,
    "description": (
      "Chemical Engineering (143 credits; 114 for CEGEP). The discipline is distinctive in being "
      "based equally on physics, mathematics, and chemistry applied to the process industries "
      "(food processing, fermentation, petrochemicals, water treatment, pharmaceuticals). "
      "Specialization areas include Polymeric Materials, Biochemical Engineering & Biotechnology, "
      "Energy, and Pollution Control. Students must earn C or better in all core courses."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/chemical-engineering/chemical-engineering-beng/",
    "blocks": [
      {
        "block_key": "chee_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 29,
        "courses_needed": None,
        "notes": "CEGEP students are granted transfer credit for these courses and enter a 114-credit program. 29 cr = 26 cr science/math + 3 cr from Complementary Studies Group B (Humanities/Social Sciences/Management/Law).",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1",          "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "chee_required_core",
        "title": "Required Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": (
          "FACC 100 must be taken during the first year. FACC 250 is 0 credits (non-credit requirement). "
          "Source: Chemical Engineering Curriculum Fall 2024 (Non-CEGEP entry). "
          "CHEM 212 is 4 credits; CHEE 291 is 4 credits."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "264",  "title": "Advanced Calculus for Engineers",               "credits": 3, "is_required": True},
          {"subject": "CHEM", "catalog": "212",  "title": "Introductory Organic Chemistry 1",              "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "234",  "title": "Topics in Organic Chemistry",                   "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "208",  "title": "Computers in Engineering",                      "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "200",  "title": "Chemical Engineering Principles 1",             "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "204",  "title": "Chemical Engineering Principles 2",             "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "220",  "title": "Chemical Engineering Thermodynamics",           "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "231",  "title": "Data Analysis and Design of Experiments",       "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "291",  "title": "Instrumentation and Measurement 1",             "credits": 4, "is_required": True},
          {"subject": "CHEE", "catalog": "310",  "title": "Physical Chemistry for Engineers",              "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "314",  "title": "Fluid Mechanics",                               "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "315",  "title": "Heat and Mass Transfer",                        "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "351",  "title": "Separation Processes",                          "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "380",  "title": "Materials Science",                             "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "390",  "title": "Computational Methods in Chemical Engineering", "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "400",  "title": "Principles of Sustainable Energy Conversion",   "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "401",  "title": "Energy Systems Engineering",                    "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "423",  "title": "Chemical Reaction Engineering",                 "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "440",  "title": "Process Modelling",                             "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "453",  "title": "Process Design",                                "credits": 4, "is_required": True},
          {"subject": "CHEE", "catalog": "455",  "title": "Process Control",                               "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "456D1","title": "Design Project",                                 "credits": 4, "is_required": True},
          {"subject": "CHEE", "catalog": "456D2","title": "Design Project",                                 "credits": 5, "is_required": True},
          {"subject": "CHEE", "catalog": "474",  "title": "Biochemical Engineering",                       "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "484",  "title": "Materials Engineering",                         "credits": 3, "is_required": True},
          {"subject": "CHEE", "catalog": "491",  "title": "Instrumentation and Measurement 2",             "credits": 4, "is_required": True},
          {"subject": "CHEE", "catalog": "370",  "title": "Elements of Biotechnology",                     "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "chee_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": (
          "Minimum 9 credits from the approved TC list (List A: 3-9 cr; List B: 0-6 cr; List C: 0-3 cr). "
          "Students may choose only one course from each of: CHEE 521/CIVE 521; CHEE 563/MECH 563; CHEE 593/CIVE 430. "
          "Only one project course (CHEE 363, 494, 495, or 496) may be taken."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "CHEE", "catalog": "301",  "title": "Resource Recovery from Waste",               "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "511",  "title": "Catalysis for Sustainable Fuels and Chemicals","credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "512",  "title": "Stem Cell Bioprocess Engineering",            "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "515",  "title": "Interface Design: Biomimetic Approach",       "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "521",  "title": "Nanomaterials and the Aquatic Environment",   "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "541",  "title": "Electrochemical Engineering",                 "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "543",  "title": "Plasma Engineering",                          "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",      "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "582",  "title": "Polymer Science and Engineering",             "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "584",  "title": "Polymer Processing",                          "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "585",  "title": "Foundations of Soft Matter",                  "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "591",  "title": "Environmental Bioremediation",                "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "593",  "title": "Industrial Water Pollution Control",          "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "534",  "title": "Air Pollution Engineering",                   "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "521",  "title": "Nanomaterials and the Aquatic Environment",   "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "430",  "title": "Water Treatment and Pollution Control",       "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",      "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "363",  "title": "Projects Chemical Engineering 1",             "credits": 2, "is_required": False},
          {"subject": "CHEE", "catalog": "494",  "title": "Research Project and Seminar 1",              "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "495",  "title": "Research Project and Seminar 2",              "credits": 4, "is_required": False},
          {"subject": "CHEE", "catalog": "496",  "title": "Environmental Research Project",              "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "chee_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "1 course (3 cr) from Group A (Impact of Technology) and 2 courses (6 cr) from Group B (Humanities/Social Sciences/Management/Law). CEGEP students receive 3 credits transfer credit toward Group B.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # CIVIL ENGINEERING (B.Eng.) — 139 credits
  # Source: Civil Engineering Curriculum Fall 2024 (Non-CEGEP entry), Oct 2024
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "civil_engineering_beng",
    "name": "Civil Engineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 139,
    "description": (
      "Civil Engineering (139 credits; 110 for CEGEP). The program is comprehensive in the "
      "fundamentals of mechanics and engineering associated with the diverse fields of the "
      "profession: solid mechanics, fluid mechanics, soil mechanics, environmental engineering, "
      "water resources management, structural analysis, and systems analysis."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/civil-engineering/civil-engineering-beng/",
    "blocks": [
      {
        "block_key": "cive_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 29,
        "courses_needed": None,
        "notes": "CEGEP students are granted transfer credit and enter a 110-credit program. Geology is EPSC 221 (not GEOL 104). The 29 credits include 26 cr science/math + 3 cr from Group B Complementary Studies.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1",          "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "cive_required_core",
        "title": "Required Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": (
          "FACC 100 must be taken in the first year. FACC 250 is 0 credits (non-credit requirement). "
          "CIVE 202 and CIVE 207 are 4 credits each. CIVE 225 and CIVE 327 are 4 credits each. "
          "CIVE 210 is a summer 2-credit surveying course. CIVE 311 is 4 credits. "
          "Source: Civil Engineering Curriculum Fall 2024."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "264",  "title": "Advanced Calculus for Engineers",               "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "208",  "title": "Computers in Engineering",                      "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                  "credits": 3, "is_required": True},
          {"subject": "EPSC", "catalog": "221",  "title": "General Geology",                               "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "261",  "title": "Measurement Laboratory",                        "credits": 2, "is_required": True},
          {"subject": "MECH", "catalog": "289",  "title": "Design Graphics",                               "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "202",  "title": "Construction Materials",                        "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "205",  "title": "Statics",                                       "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "206",  "title": "Dynamics",                                      "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "207",  "title": "Solid Mechanics",                               "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "208",  "title": "Civil Engineering System Analysis",             "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "210",  "title": "Surveying",                                     "credits": 2, "is_required": True},
          {"subject": "CIVE", "catalog": "225",  "title": "Environmental Engineering",                     "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "290",  "title": "Thermodynamics and Heat Transfer",              "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "302",  "title": "Probabilistic Systems",                         "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "311",  "title": "Geotechnical Mechanics",                        "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "317",  "title": "Structural Engineering 1",                      "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "318",  "title": "Structural Engineering 2",                      "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "319",  "title": "Transportation Engineering",                    "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "320",  "title": "Numerical Methods",                             "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "323",  "title": "Hydrology and Water Resources",                 "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "324",  "title": "Sustainable Project Management",                "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "327",  "title": "Fluid Mechanics and Hydraulics",                "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "418",  "title": "Design Project",                                "credits": 4, "is_required": True},
          {"subject": "CIVE", "catalog": "432",  "title": "Technical Paper",                               "credits": 1, "is_required": True},
        ],
      },
      {
        "block_key": "cive_technical_comp",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": (
          "Minimum 6 credits from List A (Design Technical Complementaries); remaining 9 credits from List A and/or B "
          "or other suitable undergraduate or 500-level courses. Total 15 credits of TCs."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "CIVE", "catalog": "416",  "title": "Geotechnical Engineering",                       "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "421",  "title": "Municipal Systems",                              "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "428",  "title": "Water Resources and Hydraulic Engineering",      "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "430",  "title": "Water Treatment and Pollution Control",          "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "440",  "title": "Traffic Engineering and Simulation",             "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "446",  "title": "Construction Engineering",                       "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "460",  "title": "Matrix Structural Analysis",                     "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "462",  "title": "Design of Steel Structures",                     "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "463",  "title": "Design of Concrete Structures",                  "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "470",  "title": "Undergraduate Research Project",                 "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "507",  "title": "Wind Engineering",                               "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "512",  "title": "Advanced Civil Engineering Materials",            "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "520",  "title": "Groundwater Hydrology",                          "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "521",  "title": "Nanomaterials and the Aquatic Environment",      "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "527",  "title": "Renovation and Preservation: Infrastructure",    "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "528",  "title": "Design of Wood Structures",                      "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "540",  "title": "Urban Transportation Planning",                  "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "542",  "title": "Transportation Network Analysis",                "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "545",  "title": "Life Cycle Assessment and the Circular Economy", "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "550",  "title": "Water Resources Management",                     "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "555",  "title": "Environmental Data Analysis",                    "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "557",  "title": "Microbiology for Environmental Engineering",     "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "560",  "title": "Transportation Safety and Design",               "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "561",  "title": "Greenhouse Gas Emissions",                       "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "570",  "title": "Solar Driven Environmental Processes",           "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "572",  "title": "Computational Hydraulics",                       "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "573",  "title": "Hydraulic Structures",                           "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "574",  "title": "Fluid Mechanics of Water Pollution",             "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "577",  "title": "River Engineering",                              "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "584",  "title": "Mechanics of Groundwater Flow",                  "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "521",  "title": "Nanomaterials and the Aquatic Environment",      "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cive_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "1 course (3 cr) from Group A (Impact of Technology) and 2 courses (6 cr) from Group B (Humanities/Social Sciences/Management/Law). CEGEP students receive 3 credits transfer credit toward Group B.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # ELECTRICAL ENGINEERING (B.Eng.) — 134 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "electrical_engineering_beng",
    "name": "Electrical Engineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 134,
    "description": (
      "Electrical Engineering (134 credits; 105 for CEGEP). Provides broad understanding of "
      "the key principles behind advances in computers, micro-electronics, automation, robotics, "
      "telecommunications, and power systems. Technical complementaries allow specialization in "
      "power engineering, communications, microelectronics, or computing. Includes optional "
      "participation in the Institute of Electrical Power Engineering (Hydro-Québec sponsored)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/electrical-computer-engineering/electrical-engineering-beng/",
    "blocks": [
      {
        "block_key": "ee_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 25,
        "courses_needed": None,
        "notes": "CEGEP students are granted transfer credit and enter a 109-112 credit program. CHEM 120, PHYS 131, PHYS 142 are each 4 credits. 25 cr = 22 cr science/math + 3 cr from Humanities/Social Sciences Group B.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "ee_required_core",
        "title": "Required Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": (
          "FACC 100 taken in first year; FACC 250 is 0 credits (non-credit requirement). "
          "ECSE 251 is 'Electric and Magnetic Fields'. ECSE 307 is 4 cr; ECSE 308 is 4 cr; "
          "ECSE 331 is 4 cr; ECSE 354 is 4 cr; ECSE 362 is 4 cr; ECSE 324 is 4 cr."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "281",  "title": "Analytical Mechanics",                          "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "202",  "title": "Foundations of Programming",                    "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "206",  "title": "Introduction to Software Systems",               "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "262",  "title": "Properties of Materials in Electrical Engineering","credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                  "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "200",  "title": "Electric Circuits 1",                           "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "205",  "title": "Probability and Statistics for Engineers",      "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "206",  "title": "Introduction to Signals and Systems",           "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "210",  "title": "Electric Circuits 2",                           "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "211",  "title": "Design Principles and Methods",                 "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "222",  "title": "Digital Logic",                                 "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "250",  "title": "Fundamentals of Software Development",          "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "251",  "title": "Electric and Magnetic Fields",                  "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "307",  "title": "Linear Systems and Control",                    "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "308",  "title": "Introduction to Communication Systems and Networks","credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "324",  "title": "Computer Organization",                         "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "331",  "title": "Electronics",                                   "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "343",  "title": "Numerical Methods in Engineering",              "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "354",  "title": "Electromagnetic Wave Propagation",              "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "362",  "title": "Fundamentals of Power Engineering",             "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "458D1","title": "Capstone Design Project 1",                     "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "458D2","title": "Capstone Design Project 2",                     "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "ee_technical_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 17,
        "courses_needed": None,
        "notes": (
          "8 credits (2 courses) from List A (with laboratory); remaining 9-12 credits from List A or B. "
          "List A includes: ECSE 335, 403, 408, 416, 433, 444, 470. "
          "List B includes COMP and various ECSE 300-500 level courses."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "ECSE", "catalog": "310",  "title": "Thermodynamics of Computing",              "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "325",  "title": "Digital Systems",                          "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "335",  "title": "Electronics 2",                            "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "403",  "title": "Control",                                  "credits": 4, "is_required": False},
          {"subject": "ECSE", "catalog": "405",  "title": "Computers and Peripherals",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "408",  "title": "Communication Systems",                    "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "411",  "title": "Microcontrollers",                         "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "412",  "title": "Microelectronics",                         "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "414",  "title": "Telecommunication Networks",               "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "415",  "title": "Introduction to Computer Vision",          "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "420",  "title": "Parallel Computing",                       "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "421",  "title": "Introduction to Machine Learning",         "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "423",  "title": "Antennas and Propagation",                 "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "424",  "title": "Telecommunication Networks 2",             "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "425",  "title": "Computer Architecture",                    "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "427",  "title": "Operating Systems",                        "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "430",  "title": "Wireless Communications",                  "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "435",  "title": "Digital Signal Processing",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "444",  "title": "Photonic Devices and Systems",             "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "446",  "title": "Photonics Laboratory",                     "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "463",  "title": "Electric Power Generation",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "464",  "title": "Power Systems Analysis",                   "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "465",  "title": "Power Electronic Systems",                 "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "551",  "title": "Machine Learning for Engineers",           "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "370",  "title": "Introduction to Data Science",             "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "551",  "title": "Applied Machine Learning",                 "credits": 4, "is_required": False},
        ],
      },
      {
        "block_key": "ee_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "6 credits from approved humanities/social sciences/management/law courses (non-technical complementaries).",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # COMPUTER ENGINEERING (B.Eng.) — 133 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "computer_engineering_beng",
    "name": "Computer Engineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 133,
    "description": (
      "Computer Engineering (133 credits; 108–111 for CEGEP). Provides depth and breadth in "
      "hardware and software aspects of computers, from circuit design to operating systems and "
      "software engineering. Combines hardware foundations from EE with software from CS to meet "
      "industry demand for engineers with strong backgrounds in modern computer technology."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/electrical-computer-engineering/computer-engineering-beng/",
    "blocks": [
      {
        "block_key": "ce_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 25,
        "courses_needed": None,
        "notes": "CEGEP students enter a 108–111 credit program with transfer credits. CHEM 120, PHYS 131, PHYS 142 are each 4 credits. 25 cr = 22 cr science/math + 3 cr from Humanities/Social Sciences Group B.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "ce_required_core",
        "title": "Required Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "FACC 100 must be taken in the first year. FACC 250 is 0 credits (non-credit requirement). ECSE 211 is 3 cr; ECSE 308, 324, 331, 444 are 4 cr each.",
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",   "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer", "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                          "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",            "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                        "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers","credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "202",  "title": "Foundations of Programming",                   "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "206",  "title": "Introduction to Software Systems",             "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "251",  "title": "Algorithms and Data Structures",               "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "240",  "title": "Discrete Structures",                          "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                 "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "200",  "title": "Electric Circuits 1",                          "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "205",  "title": "Probability and Statistics for Engineers",     "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "206",  "title": "Introduction to Signals and Systems",          "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "210",  "title": "Electric Circuits 2",                          "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "211",  "title": "Design Principles and Methods",                "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "222",  "title": "Digital Logic",                                "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "223",  "title": "Model-Based Programming",                      "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "250",  "title": "Fundamentals of Software Development",         "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "308",  "title": "Introduction to Communication Systems and Networks","credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "310",  "title": "Thermodynamics of Computing",                  "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "321",  "title": "Introduction to Software Engineering",         "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "324",  "title": "Computer Organization",                        "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "325",  "title": "Digital Systems",                              "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "331",  "title": "Electronics",                                  "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "353",  "title": "Electromagnetic Fields and Waves",             "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "425",  "title": "Computer Architecture",                        "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "427",  "title": "Operating Systems",                            "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "444",  "title": "Microprocessors",                              "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "458D1","title": "Capstone Design Project 1",                    "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "458D2","title": "Capstone Design Project 2",                    "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "ce_technical_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": "Courses from approved TC list in areas such as AI, networks, embedded systems, VLSI. Natural Science complementary: 3 credits from approved science departments.",
        "sort_order": 3,
        "courses": [
          {"subject": "ECSE", "catalog": "411",  "title": "Microcontrollers",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "412",  "title": "Microelectronics",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "414",  "title": "Telecommunication Networks",      "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "415",  "title": "Introduction to Computer Vision", "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "445",  "title": "Embedded Systems",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "551",  "title": "Machine Learning for Engineers",  "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "424",  "title": "Artificial Intelligence",         "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "ce_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "3 credits from Group A and 3 credits from Group B (humanities/social sciences/management). 1 free elective (3 credits) approved by ECE undergraduate office.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SOFTWARE ENGINEERING CO-OP (B.Eng.) — 141–144 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "software_engineering_coop_beng",
    "name": "Software Engineering Co-op (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 141,
    "description": (
      "Software Engineering Co-op (141–144 credits). Focuses on skills needed to design and "
      "develop complex software systems, including mandatory co-op work terms (minimum 12 months "
      "of paid industry experience). Covers software architecture, testing, AI, embedded systems, "
      "and operating systems within an accredited engineering program."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/electrical-computer-engineering/co-op-software-engineering-beng/",
    "blocks": [
      {
        "block_key": "se_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 28,
        "courses_needed": None,
        "notes": "CEGEP students may be granted transfer credit for Year 0 courses and enter a 113-116 credit program. 28 cr = 22 cr science/math + 3 cr Humanities/Social Sciences + 3 cr Natural Science complementary.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "se_required_core",
        "title": "Required Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "FACC 100 must be taken in the first year. FACC 250 is 0 credits (non-credit requirement). Four mandatory co-op work terms (ECSE 201/301/401/402, 2 credits each) are required.",
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",   "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer", "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                          "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",            "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                        "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers","credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "202",  "title": "Foundations of Programming",                   "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "206",  "title": "Introduction to Software Systems",             "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "251",  "title": "Algorithms and Data Structures",               "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "302",  "title": "Programming Languages and Paradigms",          "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "360",  "title": "Algorithm Design",                             "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "421",  "title": "Compilations",                                 "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "240",  "title": "Discrete Structures",                          "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                 "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "200",  "title": "Electric Circuits 1",                          "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "205",  "title": "Probability and Statistics for Engineers",     "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "211",  "title": "Design Principles and Methods",                "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "222",  "title": "Digital Logic",                                "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "223",  "title": "Model-Based Programming",                      "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "250",  "title": "Fundamentals of Software Development",         "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "310",  "title": "Thermodynamics of Computing",                  "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "316",  "title": "Signals and Networks",                         "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "321",  "title": "Introduction to Software Engineering",         "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "324",  "title": "Computer Organization",                        "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "326",  "title": "Software Requirements Engineering",            "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "420",  "title": "Parallel Computing",                           "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "427",  "title": "Operating Systems",                            "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "428",  "title": "Software Engineering Practice",                "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "429",  "title": "Software Validation",                          "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "458D1","title": "Capstone Design Project 1",                    "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "458D2","title": "Capstone Design Project 2",                    "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "201",  "title": "Co-operative Work Term 1",                     "credits": 2, "is_required": True},
          {"subject": "ECSE", "catalog": "301",  "title": "Co-operative Work Term 2",                     "credits": 2, "is_required": True},
          {"subject": "ECSE", "catalog": "401",  "title": "Co-operative Work Term 3",                     "credits": 2, "is_required": True},
          {"subject": "ECSE", "catalog": "402",  "title": "Co-operative Work Term 4",                     "credits": 2, "is_required": True},
        ],
      },
      {
        "block_key": "se_technical_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": "Choose from approved list. Natural Science complementary: 3 credits from approved science departments.",
        "sort_order": 3,
        "courses": [
          {"subject": "ECSE", "catalog": "415",  "title": "Introduction to Computer Vision",     "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "445",  "title": "Embedded Systems",                    "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "526",  "title": "Artificial Intelligence",             "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "539",  "title": "Advanced Software Language Engineering","credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "551",  "title": "Machine Learning for Engineers",      "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "303",  "title": "Software Design",                     "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "520",  "title": "Compiler Design",                     "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "se_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "3 credits from Group A and 3 credits from Group B (humanities/social sciences/management).",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # MECHANICAL ENGINEERING (B.Eng.) — 142 credits
  # Source: Mechanical Engineering Curriculum Fall 2024, Stream B (Non-CEGEP)
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "mechanical_engineering_beng",
    "name": "Mechanical Engineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 142,
    "description": (
      "Mechanical Engineering (142 credits; 113 for CEGEP). Encompasses "
      "design and manufacturing, materials and solid mechanics, thermodynamics and fluid mechanics, "
      "dynamics and control, mechatronics, mathematics and computational modelling. Practical "
      "engineering problem-solving with focus areas including aerospace, energy, manufacturing, "
      "machinery, transportation, controls, bioengineering, and industrial engineering."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/mechanical-engineering/mechanical-engineering-beng/",
    "blocks": [
      {
        "block_key": "mech_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 29,
        "courses_needed": None,
        "notes": "CEGEP students may receive transfer credit and enter a 113-credit program. CHEM 110/120 and PHYS 131/142 are each 4 credits. 29 cr = 26 cr science/math + 3 cr from Group B Complementary Studies.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1",          "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "mech_required_core",
        "title": "Required Core Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": (
          "FACC 100 must be taken in the first year. FACC 250 is 0 credits. "
          "MECH 201 is 2 credits; MECH 210 is 2 credits; MECH 220 is 4 credits; MECH 315 is 4 credits. "
          "CIVE 207 (Solid Mechanics, 4 cr) is required. MATH 271 is required. "
          "Source: Mechanical Engineering Curriculum Fall 2024 (Stream B)."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "264",  "title": "Advanced Calculus for Engineers",               "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "271",  "title": "Linear Algebra and Partial Differential Equations","credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "208",  "title": "Computers in Engineering",                      "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                  "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "260",  "title": "Materials Science and Engineering",              "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "207",  "title": "Solid Mechanics",                               "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "461",  "title": "Electric Machinery",                            "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "220",  "title": "Mechanics 2",                                   "credits": 4, "is_required": True},
          {"subject": "MECH", "catalog": "262",  "title": "Statistics and Measurement Laboratory",         "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "292",  "title": "Design 1: Conceptual Design",                   "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "309",  "title": "Numerical Methods in Mechanical Engineering",   "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "314",  "title": "Dynamics of Mechanisms",                        "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "315",  "title": "Mechanics 3",                                   "credits": 4, "is_required": True},
          {"subject": "MECH", "catalog": "321",  "title": "Mechanics of Deformable Solids",                "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "331",  "title": "Fluid Mechanics 1",                             "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "341",  "title": "Thermodynamics 2",                              "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "346",  "title": "Heat Transfer",                                 "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "360",  "title": "Principles of Manufacturing",                   "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "362",  "title": "Mechanical Laboratory 1",                       "credits": 2, "is_required": True},
          {"subject": "MECH", "catalog": "383",  "title": "Applied Electronics and Instrumentation",       "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "393",  "title": "Design 2: Machine Element Design",              "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "412",  "title": "System Dynamics and Control",                   "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "430",  "title": "Fluid Mechanics 2",                             "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "463D1","title": "Design 3: Mechanical Engineering Project 1",    "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "463D2","title": "Design 3: Mechanical Engineering Project 2",    "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mech_technical_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": (
          "6 credits at 300-level or higher from MECH courses (one must be from the Design shortlist). "
          "Plus 3 credits from approved 300+ level courses in Engineering or Science. "
          "Source: Mechanical Engineering Curriculum Fall 2024 TC list."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "MECH", "catalog": "497",  "title": "Value Engineering",                              "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "498",  "title": "Interdisciplinary Design Project 1",             "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "499",  "title": "Interdisciplinary Design Project 2",             "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "513",  "title": "Control Systems",                                "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "530",  "title": "Mechanics of Composite Materials",               "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "532",  "title": "Aircraft Performance, Stability and Control",    "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "535",  "title": "Turbomachinery and Propulsion",                  "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "536",  "title": "Aerospace Structures",                           "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "543",  "title": "Design with Composite Materials",                "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "544",  "title": "Processing of Composite Materials",              "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "553",  "title": "Design and Manufacture of Microdevices",         "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "559",  "title": "Engineering Systems Optimization",               "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "560",  "title": "Eco-design and Product Life Cycle Assessment",   "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",         "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "564",  "title": "Thermal Radiation and Solar Energy Systems",     "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "565",  "title": "Fluid Flow and Heat Transfer Equipment",         "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "573",  "title": "Mechanics of Robotic Systems",                   "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",         "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "mech_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "1 course (3 cr) from Group A (Impact of Technology) and 2 courses (6 cr) from Group B (Humanities/Social Sciences/Management/Law). CEGEP students receive 3 credits transfer credit toward Group B.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # MATERIALS ENGINEERING Co-op (B.Eng.) — 148 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "materials_engineering_beng",
    "name": "Materials Engineering Co-op (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 148,
    "description": (
      "Materials Engineering Co-op (148 credits). An accredited cooperative B.Eng. program "
      "that includes three paid industrial work terms. Students learn the science and engineering "
      "of materials through the processing pipeline — from ore enrichment to final applications "
      "in aerospace, electronics, and biological systems. A co-op fee applies."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/mining-materials-engineering/materials-engineering-beng/",
    "blocks": [
      {
        "block_key": "mime_mat_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 29,
        "courses_needed": None,
        "notes": "CEGEP students receive transfer credit for Year 0 courses. 29 cr = 26 cr science/math + 3 cr from Humanities/Social Sciences Group B.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1",          "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "mime_mat_required_nondept",
        "title": "Required Non-Departmental Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "FACC 100 must be taken in the first year. FACC 250 is 0 credits. CIVE 207 is 4 credits. CHEM 233 is 3 credits. ECSE 209 is 3 credits.",
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "264",  "title": "Advanced Calculus for Engineers",               "credits": 3, "is_required": True},
          {"subject": "CHEM", "catalog": "233",  "title": "Topics in Physical Chemistry",                  "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "205",  "title": "Statics",                                       "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "207",  "title": "Solid Mechanics",                               "credits": 4, "is_required": True},
          {"subject": "COMP", "catalog": "208",  "title": "Computer Programming for Physical Sciences and Engineering", "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "209",  "title": "Electrotechnology",                             "credits": 3, "is_required": True},
          {"subject": "MECH", "catalog": "289",  "title": "Design Graphics",                               "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mime_mat_required_core",
        "title": "Required Materials Engineering Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "59 credits of required MIME courses. MIME 356 is 4 credits; MIME 452 is 4 credits. Program includes co-op work terms.",
        "sort_order": 3,
        "courses": [
          {"subject": "MIME", "catalog": "209",  "title": "Mathematical Applications",                      "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "212",  "title": "Engineering Thermodynamics",                     "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "250",  "title": "Introduction to Extractive Metallurgy",          "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "261",  "title": "Structure of Materials",                         "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "311",  "title": "Modelling and Automatic Control",                "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "317",  "title": "Analytical and Characterization Techniques",     "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "341",  "title": "Introduction to Mineral Processing",             "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "345",  "title": "Applications of Polymers",                       "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "350",  "title": "Extractive Metallurgical Engineering",           "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "352",  "title": "Hydrochemical Processing",                       "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "356",  "title": "Heat, Mass and Fluid Flow",                      "credits": 4, "is_required": True},
          {"subject": "MIME", "catalog": "360",  "title": "Phase Transformations: Solids",                  "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "362",  "title": "Mechanical Properties",                          "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "452",  "title": "Process and Materials Design",                   "credits": 4, "is_required": True},
          {"subject": "MIME", "catalog": "455",  "title": "Advanced Process Engineering",                   "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "465",  "title": "Metallic and Ceramic Powders Processing",        "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "467",  "title": "Electronic Properties of Materials",             "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "470",  "title": "Engineering Biomaterials",                       "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "473",  "title": "Introduction to Computational Materials Design", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mime_mat_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 18,
        "courses_needed": None,
        "notes": "18 credits from approved technical elective list. Up to 6 credits from outside the Department with departmental approval.",
        "sort_order": 4,
        "courses": [
          {"subject": "MIME", "catalog": "510",  "title": "Ironmaking and Steelmaking",           "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "512",  "title": "Corrosion and Degradation",            "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "515",  "title": "Biomaterial Surface Analysis",        "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "540",  "title": "Computational Thermodynamics",        "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "542",  "title": "Transmission Electron Microscopy",    "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "556",  "title": "Sustainable Materials Processing",    "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "580",  "title": "Polymers and Composites",             "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "515",  "title": "Interface Design: Biomimetic Approach","credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "mime_mat_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "3 credits from Group A and 3 credits from Group B at 200-300 level.",
        "sort_order": 5,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # MINING ENGINEERING (B.Eng.) — 144 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "mining_engineering_beng",
    "name": "Mining Engineering (B.Eng.)",
    "program_type": "beng",
    "faculty": "Faculty of Engineering",
    "total_credits": 144,
    "description": (
      "Mining Engineering (144 credits). Canada's oldest mining engineering program (est. 1871). "
      "The co-operative program includes three paid industrial work terms and covers mining science, "
      "mineral economics, mine planning, rock mechanics, renewable energy, and mine design. "
      "Available in English Stream (high school) or Bilingual Stream (CEGEP, in collaboration "
      "with Polytechnique Montréal)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/mining-materials-engineering/mining-engineering-beng/",
    "blocks": [
      {
        "block_key": "mime_min_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 29,
        "courses_needed": None,
        "notes": "CEGEP students may be granted transfer credit and may enter the Bilingual Stream with Polytechnique Montréal. 29 cr = 26 cr science/math + 3 cr from Humanities/Social Sciences Group B.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1",          "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2",          "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2",                   "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "142",  "title": "Electromagnetism and Optics",  "credits": 4, "is_required": True},
        ],
      },
      {
        "block_key": "mime_min_required_nondept",
        "title": "Required Non-Departmental Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": (
          "FACC 100 must be taken in the first year. FACC 250 is 0 credits (non-credit requirement). "
          "COMP 208 or COMP 250 accepted. EPSC 225 is 1 credit. CIVE 207 is 4 credits. MATH 264 is required."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",    "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "250",  "title": "Responsibilities of the Professional Engineer",  "credits": 0, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                           "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",             "credits": 1, "is_required": True},
          {"subject": "MATH", "catalog": "262",  "title": "Intermediate Calculus",                         "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "263",  "title": "Ordinary Differential Equations for Engineers", "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "264",  "title": "Advanced Calculus for Engineers",               "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "208",  "title": "Computer Programming for Physical Sciences and Engineering", "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "205",  "title": "Statics",                                       "credits": 3, "is_required": True},
          {"subject": "CIVE", "catalog": "207",  "title": "Solid Mechanics",                               "credits": 4, "is_required": True},
          {"subject": "ECSE", "catalog": "209",  "title": "Electrotechnology",                             "credits": 3, "is_required": True},
          {"subject": "EPSC", "catalog": "221",  "title": "General Geology",                               "credits": 3, "is_required": True},
          {"subject": "EPSC", "catalog": "225",  "title": "Properties of Minerals",                        "credits": 1, "is_required": True},
          {"subject": "MECH", "catalog": "289",  "title": "Design Graphics",                               "credits": 3, "is_required": True},
          {"subject": "WCOM", "catalog": "206",  "title": "Communication in Engineering",                  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mime_min_required_core",
        "title": "Required Mining Engineering Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "47 credits of required MIME courses. MIME 426 is 6 credits (capstone design). Stream B (non-CEGEP) requires MIME 329, 330, 421, 424, 428 and CIVE 208 instead of MPMC courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "MIME", "catalog": "200",  "title": "Introduction to the Minerals Industry",          "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "203",  "title": "Mine Surveying",                                 "credits": 2, "is_required": True},
          {"subject": "MIME", "catalog": "209",  "title": "Mathematical Applications",                      "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "260",  "title": "Materials Science and Engineering",              "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "322",  "title": "Fragmentation and Comminution",                  "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "323",  "title": "Rock and Soil Mass Characterization",            "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "325",  "title": "Mineral Industry Economics",                     "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "333",  "title": "Materials Handling",                             "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "340",  "title": "Applied Fluid Dynamics",                         "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "341",  "title": "Introduction to Mineral Processing",             "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "413",  "title": "Strategic Mine Planning With Uncertainty",       "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "419",  "title": "Surface Mining",                                 "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "422",  "title": "Mine Ventilation",                               "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "425",  "title": "Applied Stochastic Orebody Modelling",           "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "426",  "title": "Mine Design and Prefeasibility Study",           "credits": 6, "is_required": True},
        ],
      },
      {
        "block_key": "mime_min_stream_b",
        "title": "Stream B Required Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": "Stream B",
        "credits_needed": None,
        "courses_needed": None,
        "notes": "Non-CEGEP (English Stream) students take these courses instead of MPMC courses. CEGEP students take MPMC 321, 326, 328, 329, 330, 421 (French, with Polytechnique Montréal).",
        "sort_order": 4,
        "courses": [
          {"subject": "CIVE", "catalog": "208",  "title": "Civil Engineering System Analysis",             "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "329",  "title": "Mining Geology",                                 "credits": 2, "is_required": True},
          {"subject": "MIME", "catalog": "330",  "title": "Mining Geotechnics",                             "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "421",  "title": "Rock Mechanics",                                 "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "424",  "title": "Underground Mining Methods",                     "credits": 3, "is_required": True},
          {"subject": "MIME", "catalog": "428",  "title": "Environmental Mining Engineering",               "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "mime_min_tc",
        "title": "Technical Complementary Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "Select from approved Lists A and B including MIME 320, 484, 511, 514, 520, 527, or other approved courses from engineering, management, or science.",
        "sort_order": 5,
        "courses": [
          {"subject": "MIME", "catalog": "320",  "title": "Simulation in Mineral Processing",              "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "484",  "title": "Mine Management",                               "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "511",  "title": "Tailings Management",                           "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "514",  "title": "Advanced Mineral Processing",                   "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "520",  "title": "Mine Automation",                               "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "527",  "title": "Advanced Mine Design",                          "credits": 3, "is_required": False},
          {"subject": "MIME", "catalog": "556",  "title": "Sustainable Materials Processing",              "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "mime_min_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "3 credits from Group A and 3 credits from Group B at 200-300 level.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # GLOBAL ENGINEERING (B.G.E.) — 120–127 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "global_engineering_bge",
    "name": "Global Engineering (B.G.E.)",
    "program_type": "bge",
    "faculty": "Faculty of Engineering",
    "total_credits": 127,
    "description": (
      "Global Engineering (120–127 credits). An international program combining technical "
      "engineering skills with soft skills in humanities, business, and languages. Offered in "
      "two years at CentraleSupélec (Paris, France) and two years at McGill University. "
      "Students specialize in one of nine engineering streams. Note: Not currently accredited. "
      "Year 0 and Year 1 coursework is completed at CentraleSupélec in France."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/global-engineering/global-engineering-geng/",
    "blocks": [
      {
        "block_key": "bge_year01_france",
        "title": "Years 0–1 at CentraleSupélec (France)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "First two years of the program take place at CentraleSupélec in France. Strong foundation in mathematics, physics, chemistry, and biology.",
        "sort_order": 1,
        "courses": [],
      },
      {
        "block_key": "bge_mcgill_core",
        "title": "McGill Core Courses (Years 2–3 at McGill)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "Completed at McGill University.",
        "sort_order": 2,
        "courses": [
          {"subject": "FACC", "catalog": "100",  "title": "Introduction to the Engineering Profession",   "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "200",  "title": "Responsibilities of the Professional Engineer", "credits": 1, "is_required": True},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                          "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "400",  "title": "Engineering Professional Practice",            "credits": 1, "is_required": True},
          {"subject": "INTG", "catalog": "215",  "title": "Language and Intercultural Communication",     "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "bge_streams",
        "title": "Engineering Stream Courses (choose one of 9 streams)",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 45,
        "courses_needed": None,
        "notes": "Streams: Breadth, Biological, Chemical, Civil, Data Science, Electrical, Entrepreneurship, Materials, Mechanical. Course selection varies by stream.",
        "sort_order": 3,
        "courses": [],
      },
      {
        "block_key": "bge_complementary",
        "title": "Complementary Studies",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "3 credits from Group A and 3 credits from Group B.",
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # ARCHITECTURE (B.Sc.(Arch.)) — 126 credits
  # ──────────────────────────────────────────────────────────────────────────
  {
    "program_key": "architecture_bscarch",
    "name": "Architecture (B.Sc.(Arch.))",
    "program_type": "bscarch",
    "faculty": "Faculty of Engineering",
    "total_credits": 126,
    "description": (
      "Architecture B.Sc.(Arch.) (126 credits; 98 for CEGEP). Offered by the Peter Guo-hua Fu "
      "School of Architecture (est. 1896). Provides conceptual, technical, and procedural "
      "foundations for the professional M.Arch. program. Six terms of design studio immersion "
      "exploring design principles, representation, construction cultures, and the human "
      "experience of architecture. Students must achieve a minimum 3.00 CGPA to be eligible "
      "for the M.Arch. Professional program."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/architecture/architecture-bsc/",
    "blocks": [
      {
        "block_key": "arch_year0",
        "title": "Year 0 Foundation Courses (Non-CEGEP Entry)",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 28,
        "courses_needed": None,
        "notes": "CEGEP students are granted transfer credit and enter a 98-credit program. Course choices in consultation with the Student Advisor for Professional Programs.",
        "sort_order": 1,
        "courses": [
          {"subject": "MATH", "catalog": "133",  "title": "Linear Algebra and Geometry",  "credits": 3, "is_required": True},
          {"subject": "MATH", "catalog": "140",  "title": "Calculus 1",                   "credits": 3, "is_required": True},
          {"subject": "PHYS", "catalog": "131",  "title": "Mechanics and Waves",          "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "arch_year0_general",
        "title": "Year 0 General Studies (Humanities/Social Sciences/Sciences)",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": "15 credits from 100-200 level courses in AFRI, ANTH, ARTH, CLAS, EAST, ENGL, GERM, HIST, LLCU, PHIL, POLI, RELI, SOCI, and other approved departments.",
        "sort_order": 2,
        "courses": [],
      },
      {
        "block_key": "arch_required_studio",
        "title": "Required Architecture Studio and Lecture Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": None,
        "courses_needed": None,
        "notes": "ARCH 250 and ARCH 378 should be taken in the first year of architectural studies.",
        "sort_order": 3,
        "courses": [
          {"subject": "ARCH", "catalog": "250",  "title": "Communication, Behaviour and Architecture",    "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "251",  "title": "Architectural Graphics and Elements of Design","credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "240",  "title": "Organization of Materials in Buildings",       "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "242",  "title": "Architectural Structures 1",                   "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "271",  "title": "Architectural History 1",                      "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "272",  "title": "Architectural History 2",                      "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "302",  "title": "Design and Construction 1",                    "credits": 6, "is_required": True},
          {"subject": "ARCH", "catalog": "303",  "title": "Design and Construction 2",                    "credits": 6, "is_required": True},
          {"subject": "ARCH", "catalog": "341",  "title": "Architectural Sketching",                      "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "342",  "title": "Digital Representation",                       "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "371",  "title": "Architectural History 3",                      "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "372",  "title": "Architectural History 4",                      "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "378",  "title": "Introduction to Building Environments",        "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "400",  "title": "Energy, Environment, and Buildings 1",         "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "404",  "title": "Architectural Structures 2",                   "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "405",  "title": "Design and Construction 3",                    "credits": 6, "is_required": True},
          {"subject": "ARCH", "catalog": "406",  "title": "Design and Construction 4",                    "credits": 6, "is_required": True},
          {"subject": "ARCH", "catalog": "420",  "title": "Energy, Environment, and Buildings 2",         "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "441",  "title": "Architectural Modelling",                      "credits": 3, "is_required": True},
          {"subject": "ARCH", "catalog": "450",  "title": "Urban Design and Planning",                    "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "arch_complementary",
        "title": "Complementary and Elective Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "9 credits of elective courses outside the School of Architecture, subject to approval by the Student Advisor. Complementary courses deepen architecture knowledge in culture and technology.",
        "sort_order": 4,
        "courses": [
          {"subject": "ARCH", "catalog": "430",  "title": "Summer Course Abroad",                         "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "443",  "title": "Geometry and Architecture",                    "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "444",  "title": "Freehand Drawing and Sketching",               "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "446",  "title": "Selected Topics in Design",                    "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "456",  "title": "Community Design Workshop",                    "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "462",  "title": "Sustainable Design",                           "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "540",  "title": "Selected Topics in Architecture 1",            "credits": 3, "is_required": False},
          {"subject": "ARCH", "catalog": "541",  "title": "Selected Topics in Architecture 2",            "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────────────
  # MINOR PROGRAMS
  # ──────────────────────────────────────────────────────────────────────────

  {
    "program_key": "minor_software_engineering",
    "name": "Software Engineering – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": (
      "Software Engineering Minor (18 credits). Provides a foundation in basic computer science, "
      "programming, and software engineering practice for Engineering students. Does not carry "
      "professional recognition. Up to 6 credits (two courses) may be double-counted toward "
      "a degree program."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/software-engineering-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_se_required",
        "title": "Required Core",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 3,
        "courses_needed": None,
        "notes": "Choose only one of COMP 250 or ECSE 250.",
        "sort_order": 1,
        "courses": [
          {"subject": "COMP", "catalog": "250",  "title": "Introduction to Computer Science",        "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "250",  "title": "Data Structures and Algorithms",          "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "minor_se_choose",
        "title": "Elective Courses (choose 5 for 15 credits)",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": "From approved SE list. Cannot take both: COMP 424 and ECSE 526; ECSE 439 and ECSE 539.",
        "sort_order": 2,
        "courses": [
          {"subject": "COMP", "catalog": "302",  "title": "Programming Languages and Paradigms",    "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "303",  "title": "Software Design",                        "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "310",  "title": "Operating Systems",                      "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "421",  "title": "Compilations",                           "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "424",  "title": "Artificial Intelligence",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "321",  "title": "Software Engineering 1",                 "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "428",  "title": "Software Engineering Practice",          "credits": 4, "is_required": False},
          {"subject": "ECSE", "catalog": "429",  "title": "Software Validation",                    "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "439",  "title": "Software Language Engineering",          "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "526",  "title": "Artificial Intelligence",                "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "539",  "title": "Advanced Software Language Engineering", "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "551",  "title": "Machine Learning for Engineers",         "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_computer_science",
    "name": "Computer Science – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 24,
    "description": (
      "Computer Science Minor for Engineering students (24 credits). Requires 24 credits of "
      "approved COMP courses. Engineering students have access to this minor through the "
      "School of Computer Science."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/computer-science-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_cs_required",
        "title": "Required Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "COMP 250 or ECSE 250 may substitute. These form the core entry sequence.",
        "sort_order": 1,
        "courses": [
          {"subject": "COMP", "catalog": "250",  "title": "Introduction to Computer Science",        "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "251",  "title": "Algorithms and Data Structures",          "credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "302",  "title": "Programming Languages and Paradigms",    "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "minor_cs_electives",
        "title": "Elective Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": "15 credits from approved COMP courses at 300-level or higher.",
        "sort_order": 2,
        "courses": [
          {"subject": "COMP", "catalog": "303",  "title": "Software Design",                     "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "307",  "title": "Introduction to Web Development",     "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "310",  "title": "Operating Systems",                   "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "330",  "title": "Theory of Computation",               "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "360",  "title": "Algorithm Design",                    "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "421",  "title": "Compilations",                        "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "424",  "title": "Artificial Intelligence",             "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "512",  "title": "Database Systems",                    "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "551",  "title": "Applied Machine Learning",            "credits": 4, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_aerospace_engineering",
    "name": "Aerospace Engineering – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 21,
    "description": (
      "Aerospace Engineering Minor (21 credits). Introduces Engineering students to the "
      "fundamentals of aerodynamics, structural mechanics, and propulsion relevant to "
      "aerospace applications. Available to students in any B.Eng. program."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/aerospace-engineering-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_aero_courses",
        "title": "Aerospace Engineering Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 21,
        "courses_needed": None,
        "notes": "Must include required prerequisite courses from host degree. Typical courses drawn from MECH 553, MECH 535, MECH 570, MECH 360.",
        "sort_order": 1,
        "courses": [
          {"subject": "MECH", "catalog": "360",  "title": "Fluid Mechanics 2",                    "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "535",  "title": "Computational Fluid Dynamics",         "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "542",  "title": "Finite Element Methods",               "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "553",  "title": "Gas Dynamics",                         "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "570",  "title": "Energy Engineering",                   "credits": 3, "is_required": False},
          {"subject": "MECH", "catalog": "419",  "title": "Advanced Control Systems",             "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_applied_ai",
    "name": "Applied Artificial Intelligence – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 21,
    "description": (
      "Applied Artificial Intelligence Minor (21 credits). Covers machine learning, deep learning, "
      "data science, and AI applications in engineering contexts. Draws from both ECSE and COMP "
      "course offerings."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/applied-artificial-intelligence-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_ai_required",
        "title": "Required Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "Core sequence in AI and data science.",
        "sort_order": 1,
        "courses": [
          {"subject": "ECSE", "catalog": "551",  "title": "Machine Learning for Engineers",       "credits": 3, "is_required": True},
          {"subject": "ECSE", "catalog": "205",  "title": "Probability and Statistics for Engineers","credits": 3, "is_required": True},
          {"subject": "COMP", "catalog": "250",  "title": "Introduction to Computer Science",     "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "minor_ai_electives",
        "title": "Elective AI Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 12,
        "courses_needed": None,
        "notes": "From approved AI/ML course list.",
        "sort_order": 2,
        "courses": [
          {"subject": "COMP", "catalog": "424",  "title": "Artificial Intelligence",              "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "551",  "title": "Applied Machine Learning",             "credits": 4, "is_required": False},
          {"subject": "ECSE", "catalog": "415",  "title": "Introduction to Computer Vision",     "credits": 3, "is_required": False},
          {"subject": "ECSE", "catalog": "526",  "title": "Artificial Intelligence",              "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_biomedical_engineering",
    "name": "Biomedical Engineering – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 21,
    "description": (
      "Biomedical Engineering Minor (21 credits). Introduces engineering students to the "
      "biological and medical applications of engineering principles, including biomechanics, "
      "bioinstrumentation, and medical devices."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/biomedical-engineering-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_biomed_courses",
        "title": "Biomedical Engineering Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 21,
        "courses_needed": None,
        "notes": "Courses drawn from BIEN, CHEE biomedical stream, and relevant MECH courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "BIEN", "catalog": "200",  "title": "Introduction to Bioengineering",          "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "290",  "title": "Bioengineering Measurement Laboratory",   "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "310",  "title": "Biomechanics",                            "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "320",  "title": "Bioinstrumentation",                      "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "510",  "title": "Cell and Tissue Engineering",             "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "514",  "title": "Systems Physiology for Engineers",        "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "563",  "title": "Biofluids and Cardiovascular Mechanics",  "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_biotechnology",
    "name": "Biotechnology – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 24,
    "description": (
      "Biotechnology Minor (24 credits). Offered jointly by the Faculties of Engineering "
      "and Science. Emphasizes molecular biology and chemical engineering processes. "
      "Available to Engineering students interested in pharmaceutical, food, and bioproducts industries."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/biotechnology-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_biotech_courses",
        "title": "Biotechnology Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 24,
        "courses_needed": None,
        "notes": "Joint with Faculty of Science. Includes courses in molecular biology (BIOL) and chemical bioprocessing (CHEE).",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEE", "catalog": "370",  "title": "Elements of Biotechnology",          "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "474",  "title": "Biochemical Engineering",            "credits": 3, "is_required": False},
          {"subject": "BIEN", "catalog": "590",  "title": "Metabolic Engineering",              "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "200",  "title": "Cell Biology and Metabolism",        "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "201",  "title": "Cell Biology and Metabolism",        "credits": 3, "is_required": False},
          {"subject": "MIMM", "catalog": "396",  "title": "Microbiology",                       "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_environmental_engineering",
    "name": "Environmental Engineering – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 21,
    "description": (
      "Environmental Engineering Minor (21 credits). Covers water treatment, pollution control, "
      "environmental impact assessment, and sustainable engineering. "
      "Available to B.Eng. students in any department."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/environmental-engineering-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_enveng_courses",
        "title": "Environmental Engineering Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 21,
        "courses_needed": None,
        "notes": "Draws from CIVE, CHEE, and ENVR approved course lists.",
        "sort_order": 1,
        "courses": [
          {"subject": "CIVE", "catalog": "330",  "title": "Environmental Engineering",               "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "430",  "title": "Water Treatment and Pollution Control",   "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "521",  "title": "Nanomaterials and the Aquatic Environment","credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "591",  "title": "Environmental Bioremediation",            "credits": 3, "is_required": False},
          {"subject": "CHEE", "catalog": "593",  "title": "Industrial Water Pollution Control",      "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "201",  "title": "Society, Environment and Sustainability", "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "521",  "title": "Nanomaterials and the Aquatic Environment","credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_management",
    "name": "Management – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 24,
    "description": (
      "Management Minor for Engineering students (24 credits). Available as four sub-minors: "
      "Minor in Finance, Minor in Management, Minor in Marketing, and Minor in Operations "
      "Management. Each requires 24 credits from Desautels Faculty of Management (MGCR/FINE/MRKT/ORGB). "
      "Management courses have limited enrolment and specific registration dates."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/management-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_mgmt_required",
        "title": "Required Management Core",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 9,
        "courses_needed": None,
        "notes": "Foundation courses required for all four sub-minors. Management courses have limited enrolment.",
        "sort_order": 1,
        "courses": [
          {"subject": "MGCR", "catalog": "211",  "title": "Introduction to Financial Accounting",  "credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "222",  "title": "Introduction to Organizational Behaviour","credits": 3, "is_required": True},
          {"subject": "MGCR", "catalog": "293",  "title": "Statistics for Management",             "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "minor_mgmt_specialization",
        "title": "Sub-minor Specialization Courses (choose one sub-minor track)",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 15,
        "courses_needed": None,
        "notes": "Choose from: Finance (FINE courses), Management (MGCR/ORGB), Marketing (MRKT), or Operations Management (MGCR/INSY).",
        "sort_order": 2,
        "courses": [
          {"subject": "FINE", "catalog": "441",  "title": "Security Analysis and Portfolio Management","credits": 3, "is_required": False},
          {"subject": "FINE", "catalog": "442",  "title": "Investment Dealers and Capital Markets",   "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "301",  "title": "Introduction to Marketing",               "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "441",  "title": "Consumer Behaviour",                      "credits": 3, "is_required": False},
          {"subject": "MGCR", "catalog": "341",  "title": "Introduction to Finance",                 "credits": 3, "is_required": False},
          {"subject": "MGCR", "catalog": "351",  "title": "Managerial Accounting",                   "credits": 3, "is_required": False},
          {"subject": "ORGB", "catalog": "421",  "title": "Leading Organizations",                   "credits": 3, "is_required": False},
          {"subject": "INSY", "catalog": "442",  "title": "Operations Management",                   "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_technological_entrepreneurship",
    "name": "Technological Entrepreneurship – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": (
      "Technological Entrepreneurship Minor (18 credits). Develops entrepreneurial mindset "
      "and business skills within a technology-focused context. Includes innovation, business "
      "planning, and startup management for Engineering students."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/technological-entrepreneurship-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_entr_required",
        "title": "Required Courses",
        "block_type": "required",
        "group_name": None,
        "credits_needed": 6,
        "courses_needed": None,
        "notes": "Core business planning sequence.",
        "sort_order": 1,
        "courses": [
          {"subject": "FACC", "catalog": "450",  "title": "Technology Business Plan Design",   "credits": 3, "is_required": True},
          {"subject": "FACC", "catalog": "460",  "title": "Technology Business Plan Project",  "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "minor_entr_electives",
        "title": "Elective Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 12,
        "courses_needed": None,
        "notes": "From approved list including management, law, and technology courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "MGCR", "catalog": "341",  "title": "Introduction to Finance",              "credits": 3, "is_required": False},
          {"subject": "MGCR", "catalog": "222",  "title": "Introduction to Organizational Behaviour","credits": 3, "is_required": False},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                  "credits": 3, "is_required": False},
          {"subject": "MRKT", "catalog": "301",  "title": "Introduction to Marketing",            "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_economics_eng",
    "name": "Economics – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": "Economics Minor for Engineering students (18 credits). Covers micro and macroeconomics, econometrics, and public policy fundamentals. Courses taught by the Department of Economics.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/economics-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_econ_courses",
        "title": "Economics Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 18,
        "courses_needed": None,
        "notes": "Includes ECON 208, 209 and upper-level ECON courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "ECON", "catalog": "208",  "title": "Microeconomic Analysis and Applications","credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "209",  "title": "Macroeconomic Analysis and Applications","credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "227",  "title": "Economic Statistics",                   "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "250D1","title": "Economic Development 1",                "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "342",  "title": "Economics of the Environment",          "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "352",  "title": "Economics of Climate Change",           "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_construction_mgmt",
    "name": "Construction Engineering and Management – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": "Construction Engineering and Management Minor (18 credits). Covers construction planning, estimating, project management, and professional practice for Engineering students, particularly those in Civil Engineering.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/construction-engineering-management-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_constr_courses",
        "title": "Construction and Management Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 18,
        "courses_needed": None,
        "notes": "Draws from CIVE construction and management electives.",
        "sort_order": 1,
        "courses": [
          {"subject": "CIVE", "catalog": "221",  "title": "Construction Materials",                "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "480",  "title": "Construction Management",               "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "490",  "title": "Engineering Project Management",        "credits": 3, "is_required": False},
          {"subject": "FACC", "catalog": "300",  "title": "Engineering Economy",                   "credits": 3, "is_required": False},
          {"subject": "MGCR", "catalog": "341",  "title": "Introduction to Finance",               "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_environment_eng",
    "name": "Environment – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": "Environment Minor for Engineering students (18 credits). Interdisciplinary program covering environmental science, policy, and sustainability. Offered in partnership with the School of Environment (ENVR).",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/environment-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_env_courses",
        "title": "Environment Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 18,
        "courses_needed": None,
        "notes": "ENVR courses have limited enrolment. Mix of environmental science and policy.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "201",  "title": "Society, Environment and Sustainability", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "202",  "title": "Environmental Systems",                  "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "203",  "title": "Global Change: Past, Present and Future","credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "400",  "title": "Environmental Management 1",             "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "316",  "title": "Global Environmental Change",            "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_chemistry_eng",
    "name": "Chemistry – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": "Chemistry Minor for Engineering students (18 credits). Deepens knowledge of chemistry beyond the required engineering foundations, including organic, physical, and analytical chemistry.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/chemistry-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_chem_courses",
        "title": "Chemistry Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 18,
        "courses_needed": None,
        "notes": "Upper-level CHEM courses beyond the first-year chemistry requirements.",
        "sort_order": 1,
        "courses": [
          {"subject": "CHEM", "catalog": "212",  "title": "Introductory Organic Chemistry 1",  "credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "213",  "title": "Introductory Organic Chemistry 2",  "credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "222",  "title": "Organic Chemistry",                 "credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "233",  "title": "Organic Chemistry 1",               "credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "274",  "title": "Quantum Chemistry and Spectroscopy","credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "304",  "title": "Analytical Chemistry",              "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  {
    "program_key": "minor_arts_eng",
    "name": "Arts – Minor (B.Eng.)",
    "program_type": "minor",
    "faculty": "Faculty of Engineering",
    "total_credits": 18,
    "description": "Arts Minor for Engineering students (18 credits). Allows Engineering students to broaden their education with courses in humanities, social sciences, and arts. The Faculty of Engineering allows up to 9 credits of overlap with the degree program.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/engineering/programs/minor-programs/arts-minor-beng/",
    "blocks": [
      {
        "block_key": "minor_arts_courses",
        "title": "Humanities and Social Science Courses",
        "block_type": "choose_credits",
        "group_name": None,
        "credits_needed": 18,
        "courses_needed": None,
        "notes": "200-300 level courses from approved humanities and social sciences departments, excluding physical/natural/medical sciences, mathematics, and statistics.",
        "sort_order": 1,
        "courses": [],
      },
    ],
  },

]


# Database seed function
# ──────────────────────────────────────────────────────────────────

def seed_degree_requirements(supabase):
    """
    Insert all Engineering degree requirements into Supabase.
    Safe to re-run: uses upsert on program_key, then deletes+reinserts blocks.
    """
    inserted_programs = 0
    inserted_blocks = 0
    inserted_courses = 0

    for prog in ENGINEERING_PROGRAMS:
        prog_data = {
            "program_key":   prog["program_key"],
            "name":          prog["name"],
            "faculty":       prog.get("faculty", "Faculty of Engineering"),
            "program_type":  prog["program_type"],
            "total_credits": prog.get("total_credits") or 0,
            "description":   prog.get("description"),
            "ecalendar_url": prog.get("ecalendar_url"),
        }
        result = supabase.table("degree_programs").upsert(
            prog_data, on_conflict="program_key"
        ).execute()
        prog_id = result.data[0]["id"]
        inserted_programs += 1

        supabase.table("requirement_blocks").delete().eq("program_id", prog_id).execute()

        for i, block in enumerate(prog.get("blocks", [])):
            constraint_notes = block.get("constraint_notes") or block.get("notes") or ""

            block_data = {
                "program_id":       prog_id,
                "block_key":        block.get("block_key", f"block_{i}"),
                "title":            block.get("title", ""),
                "block_type":       block.get("block_type", "choose_credits"),
                "group_name":       block.get("group_name"),
                "courses_needed":   block.get("courses_needed"),
                "constraint_notes": constraint_notes,
                "credits_needed":   block.get("credits_needed"),
                "min_level":        block.get("min_level"),
                "max_credits_200":  block.get("max_credits_200"),
                "min_credits_400":  block.get("min_credits_400"),
                "notes":            block.get("notes", ""),
                "sort_order":       block.get("sort_order", i),
            }
            block_result = supabase.table("requirement_blocks").insert(block_data).execute()
            block_id = block_result.data[0]["id"]
            inserted_blocks += 1

            courses_to_insert = []
            for j, course in enumerate(block.get("courses", [])):
                is_required = course.get("is_required", False)
                if block.get("block_type") == "required":
                    is_required = True

                course_data = {
                    "block_id":              block_id,
                    "subject":               course.get("subject", ""),
                    "catalog":               course.get("catalog"),
                    "title":                 course.get("title", ""),
                    "credits":               course.get("credits", 3),
                    "is_required":           is_required,
                    "choose_from_group":     course.get("choose_from_group"),
                    "choose_n_credits":      course.get("choose_n_credits"),
                    "notes":                 course.get("notes"),
                    "recommended":           course.get("recommended", False),
                    "recommendation_reason": course.get("recommendation_reason"),
                    "sort_order":            j,
                }
                courses_to_insert.append(course_data)

            if courses_to_insert:
                supabase.table("requirement_courses").insert(courses_to_insert).execute()
                inserted_courses += len(courses_to_insert)

    return {
        "programs": inserted_programs,
        "blocks":   inserted_blocks,
        "courses":  inserted_courses,
    }


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    stats = seed_degree_requirements(supabase)
    print(f"Seeded: {stats['programs']} programs, {stats['blocks']} blocks, {stats['courses']} courses")
