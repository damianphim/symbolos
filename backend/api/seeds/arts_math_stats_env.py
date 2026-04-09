"""
McGill Faculty of Arts – Math, Stats, Environment, Geography joint, GIS, Health Geography, Urban Studies Honours, Behavioural Science, Psychology Joint Honours, Music minors, Science for Arts Students
Sub-module of arts_degree_requirements.py
"""

ARTS_MATH_STATS_ENV = [
  # Psychology extras, Science for Arts Students
  # ══════════════════════════════════════════════════════════════════

  # ── Mathematics – Major Concentration (B.A.) ──
  {
    "program_key": "mathematics_major",
    "name": "Mathematics – Major Concentration (B.A.)",
    "program_type": "major",
    "faculty": "Faculty of Arts",
    "total_credits": 46,
    "description": (
      "The B.A. Major Concentration in Mathematics provides an overview of the "
      "foundations of mathematics. Offered by the Department of Mathematics and "
      "Statistics (Faculty of Science) but available to B.A. students."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/mathematics-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "math_major_required",
        "title": "Required Courses (28 credits)",
        "block_type": "required",
        "credits_needed": 28,
        "notes": (
          "All required. Honours-level courses may substitute for Majors-level "
          "counterparts."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Take in U0/U1 Fall — gateway to all MATH courses"},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":True,"recommended":True},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":True},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core algebra — take in U1"},
          {"subject":"MATH","catalog":"236","title":"Algebra 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Rigorous analysis foundation"},
          {"subject":"MATH","catalog":"243","title":"Analysis 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "math_major_comp_a",
        "title": "Complementary – Primary (9-18 credits)",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "9-18 credits from primary complementary list.",
        "sort_order": 2,
        "courses": [
          {"subject":"MATH","catalog":"249","title":"Honours Complex Variables","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"314","title":"Advanced Calculus","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"315","title":"Ordinary Differential Equations","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential for applied math track"},
          {"subject":"MATH","catalog":"316","title":"Complex Variables","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"317","title":"Numerical Analysis","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"318","title":"Mathematical Logic","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"340","title":"Discrete Mathematics","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"346","title":"Number Theory","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"378","title":"Nonlinear Optimization","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"417","title":"Linear Optimization","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"451","title":"Introduction to General Topology","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"319","title":"Partial Differential Equations","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"326","title":"Nonlinear Dynamics and Chaos","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"327","title":"Matrix Numerical Analysis","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"410","title":"Majors Project","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"430","title":"Mathematical Finance","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Popular applied option"},
          {"subject":"MATH","catalog":"447","title":"Introduction to Stochastic Processes","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"463","title":"Convex Optimization","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Mathematics – Minor Concentration (B.A.) ──
  {
    "program_key": "mathematics_minor",
    "name": "Mathematics – Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit introduction to foundational mathematics for B.A. students.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/mathematics-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "math_minor_courses",
        "title": "Mathematics Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": (
          "18 credits from MATH courses. MATH 133, 140, 141 typically serve as "
          "prerequisites."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Mathematics – Supplementary Minor Concentration ──
  {
    "program_key": "mathematics_supplementary_minor",
    "name": "Mathematics – Supplementary Minor Concentration",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "An 18-credit supplementary minor for students already in a Math-related "
      "major who want additional breadth."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/mathematics-supplementary-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "math_supp_courses",
        "title": "Supplementary MATH Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits of MATH courses not already counted toward the student's major.",
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"314","title":"Advanced Calculus","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"315","title":"Ordinary Differential Equations","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"317","title":"Numerical Analysis","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"340","title":"Discrete Mathematics","credits":3,"is_required":False},
          {"subject":"MATH","catalog":None,"title":"Any MATH course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Mathematics – Honours (B.Sc.) ──
  {
    "program_key": "mathematics_honours",
    "name": "Mathematics – Honours (B.Sc.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 63,
    "description": (
      "Rigorous Honours program in pure mathematics. Available to B.A. students. "
      "Requires CGPA 3.00."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/mathematics-honours-ba/",
    "blocks": [
      {
        "block_key": "math_hon_required",
        "title": "Required Core",
        "block_type": "required",
        "credits_needed": 45,
        "notes": "Core honours sequence in analysis, algebra, topology, and complex analysis.",
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":True},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"251","title":"Honours Algebra 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"254","title":"Honours Analysis 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"255","title":"Honours Analysis 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"256","title":"Honours Analysis 4","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"350","title":"Honours Algebra 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"354","title":"Honours Analysis 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"355","title":"Honours Analysis 4","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"370","title":"Honours Algebra 4","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"451","title":"Introduction to General Topology","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "math_hon_complementary",
        "title": "Complementary Courses (18 credits)",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from approved MATH courses at 300+ level.",
        "sort_order": 2,
        "courses": [
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"346","title":"Number Theory","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"456","title":"Honours Algebra 4","credits":3,"is_required":False},
          {"subject":"MATH","catalog":None,"title":"Any MATH course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Applied Mathematics – Honours (B.Sc.) ──
  {
    "program_key": "applied_mathematics_honours",
    "name": "Applied Mathematics – Honours (B.Sc.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 63,
    "description": (
      "Honours program in applied mathematics covering numerical methods, PDEs, and "
      "optimization. Available to B.A. students."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/applied-mathematics-honours-ba/",
    "blocks": [
      {
        "block_key": "apmath_hon_required",
        "title": "Required Core",
        "block_type": "required",
        "credits_needed": 42,
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":True},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"254","title":"Honours Analysis 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"255","title":"Honours Analysis 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"315","title":"Ordinary Differential Equations","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"317","title":"Numerical Analysis","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"319","title":"Partial Differential Equations","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"327","title":"Matrix Numerical Analysis","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"350","title":"Honours Algebra 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"478","title":"Computational Methods in Applied Mathematics","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "apmath_hon_complementary",
        "title": "Complementary Courses (21 credits)",
        "block_type": "choose_credits",
        "credits_needed": 21,
        "sort_order": 2,
        "courses": [
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"326","title":"Nonlinear Dynamics and Chaos","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"378","title":"Nonlinear Optimization","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"417","title":"Linear Optimization","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"463","title":"Convex Optimization","credits":3,"is_required":False},
          {"subject":"MATH","catalog":None,"title":"Any approved MATH course at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Mathematics and Computer Science – Honours (B.Sc.) ──
  {
    "program_key": "mathematics_cs_honours",
    "name": "Mathematics and Computer Science – Honours (B.Sc.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 78,
    "description": (
      "Joint Honours in Mathematics and Computer Science. Available to B.A. "
      "students. Requires CGPA 3.00."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/mathematics-computer-science-honours-ba/",
    "blocks": [
      {
        "block_key": "mathcs_hon_required",
        "title": "Required Core",
        "block_type": "required",
        "credits_needed": 60,
        "notes": "Core courses spanning both Mathematics and Computer Science.",
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":True},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"251","title":"Honours Algebra 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"254","title":"Honours Analysis 2","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"202","title":"Foundations of Programming","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"250","title":"Introduction to Computer Science","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"251","title":"Algorithms and Data Structures","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"252","title":"Honours Algorithms and Data Structures","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"302","title":"Programming Languages and Paradigms","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"330","title":"Theory of Computation","credits":3,"is_required":True},
          {"subject":"COMP","catalog":"362","title":"Honours Algorithm Design","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"318","title":"Mathematical Logic","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"340","title":"Discrete Mathematics","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"350","title":"Honours Algebra 3","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "mathcs_hon_complementary",
        "title": "Complementary Courses (18 credits)",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "sort_order": 2,
        "courses": [
          {"subject":"COMP","catalog":"424","title":"Artificial Intelligence","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"346","title":"Number Theory","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"451","title":"Introduction to General Topology","credits":3,"is_required":False},
          {"subject":"COMP","catalog":None,"title":"Any COMP course at 300+","credits":3,"is_required":False},
          {"subject":"MATH","catalog":None,"title":"Any MATH course at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Mathematics – Joint Honours Component (B.A.) ──
  {
    "program_key": "mathematics_joint_honours",
    "name": "Mathematics – Joint Honours Component (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 36,
    "description": (
      "Joint Honours component in Mathematics. Must be combined with another Joint "
      "Honours component."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/mathematics-joint-honours-component-ba/",
    "blocks": [
      {
        "block_key": "math_jthon_courses",
        "title": "Mathematics Joint Honours Courses",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "notes": (
          "36 credits of MATH courses determined in consultation with program "
          "adviser. Must include Honours-level analysis and algebra."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"251","title":"Honours Algebra 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"254","title":"Honours Analysis 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"255","title":"Honours Analysis 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"350","title":"Honours Algebra 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":None,"title":"Additional MATH courses at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Statistics – Major Concentration (B.A.) ──
  {
    "program_key": "statistics_major",
    "name": "Statistics – Major Concentration (B.A.)",
    "program_type": "major",
    "faculty": "Faculty of Arts",
    "total_credits": 46,
    "description": (
      "Training in statistics with a mathematical core. Together with the "
      "Supplementary Minor in Statistics, constitutes the equivalent of the B.Sc. "
      "Major in Statistics. Can lead to A.Stat accreditation from the Statistical "
      "Society of Canada."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/statistics-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "stats_major_required",
        "title": "Required Courses (34 credits)",
        "block_type": "required",
        "credits_needed": 34,
        "notes": "All required. Complete all by end of U2.",
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":True},
          {"subject":"MATH","catalog":"203","title":"Principles of Statistics 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"May be replaced if CEGEP equivalent taken"},
          {"subject":"MATH","catalog":"204","title":"Principles of Statistics 2","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"208","title":"Introduction to Statistical Computing","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"R programming for statistics — take early"},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"223","title":"Linear Algebra","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":True},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "stats_major_comp",
        "title": "Complementary Courses (12 credits)",
        "block_type": "choose_credits",
        "credits_needed": 12,
        "notes": "12 credits from the complementary list.",
        "sort_order": 2,
        "courses": [
          {"subject":"MATH","catalog":"308","title":"Fundamentals of Statistical Learning","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Machine learning foundations"},
          {"subject":"MATH","catalog":"423","title":"Applied Regression","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"447","title":"Introduction to Stochastic Processes","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"523","title":"Generalized Linear Models","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"524","title":"Nonparametric Statistics","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"545","title":"Introduction to Time Series Analysis","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"556","title":"Mathematical Statistics 1","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"557","title":"Mathematical Statistics 2","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"559","title":"Bayesian Theory and Methods","credits":4,"is_required":False},
          {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":4,"is_required":False,"recommended":True},
        ],
      },
    ],
  },

  # ── Statistics – Minor Concentration (B.A.) ──
  {
    "program_key": "statistics_minor",
    "name": "Statistics – Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit introduction to statistical theory and methods.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/statistics-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "stats_minor_courses",
        "title": "Statistics Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MATH courses focused on statistics and probability.",
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"203","title":"Principles of Statistics 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"204","title":"Principles of Statistics 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"208","title":"Introduction to Statistical Computing","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"423","title":"Applied Regression","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Statistics – Supplementary Minor Concentration ──
  {
    "program_key": "statistics_supplementary_minor",
    "name": "Statistics – Supplementary Minor Concentration",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "Supplementary minor in Statistics. Together with the Statistics Major, "
      "constitutes the B.Sc. equivalent."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/statistics-supplementary-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "stats_supp_courses",
        "title": "Supplementary Statistics Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MATH courses not already counted toward the Statistics major.",
        "sort_order": 1,
        "courses": [
          {"subject":"MATH","catalog":"308","title":"Fundamentals of Statistical Learning","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"523","title":"Generalized Linear Models","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"556","title":"Mathematical Statistics 1","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"557","title":"Mathematical Statistics 2","credits":4,"is_required":False},
          {"subject":"MATH","catalog":None,"title":"Any MATH statistics course at 400+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Statistics – Honours (B.A.) ──
  {
    "program_key": "statistics_honours",
    "name": "Statistics – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 63,
    "description": (
      "Honours program in Probability and Statistics. Available to B.A. students. "
      "Requires CGPA 3.00."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/mathematics-statistics/statistics-honours-ba/",
    "blocks": [
      {
        "block_key": "stats_hon_required",
        "title": "Required Core (28 credits)",
        "block_type": "required",
        "credits_needed": 28,
        "sort_order": 1,
        "courses": [
          {"subject":"COMP","catalog":"250", "title":"Introduction to Computer Science",       "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"208", "title":"Introduction to Statistical Computing",  "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"222", "title":"Calculus 3",                              "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"247", "title":"Honours Applied Linear Algebra",         "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"255", "title":"Honours Analysis 2",                     "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"356", "title":"Honours Probability",                    "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"357", "title":"Honours Statistics",                     "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"470", "title":"Honours Research Project",               "credits":3,"is_required":True},
          {"subject":"MATH","catalog":"533", "title":"Regression and Analysis of Variance",    "credits":4,"is_required":True},
        ],
      },
      {
        "block_key": "stats_hon_complementary",
        "title": "Complementary Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "sort_order": 2,
        "courses": [
          {"subject":"MATH","catalog":"133","title":"Linear Algebra and Geometry","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"140","title":"Calculus 1","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"141","title":"Calculus 2","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"235","title":"Algebra 1","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"242","title":"Analysis 1","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"254","title":"Honours Analysis 2","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"423","title":"Applied Regression","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"447","title":"Introduction to Stochastic Processes","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"523","title":"Generalized Linear Models","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"545","title":"Introduction to Time Series Analysis","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"556","title":"Mathematical Statistics 1","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"557","title":"Mathematical Statistics 2","credits":4,"is_required":False},
          {"subject":"MATH","catalog":"559","title":"Bayesian Theory and Methods","credits":4,"is_required":False},
          {"subject":"MATH","catalog":None, "title":"Any MATH course at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Environment – B.A. Faculty Program ──
  {
    "program_key": "environment_faculty_program",
    "name": "Environment – B.A. Faculty Program",
    "program_type": "major",
    "faculty": "Faculty of Arts",
    "total_credits": 54,
    "description": (
      "Interdisciplinary Faculty Program in Environment offered through the Bieler "
      "School of Environment. Integrates courses from Arts, Science, and "
      "Agricultural & Environmental Sciences."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/bieler-school-environment/",
    "blocks": [
      {
        "block_key": "envr_fp_core",
        "title": "Environment Core",
        "block_type": "required",
        "credits_needed": 18,
        "sort_order": 1,
        "courses": [
          {"subject":"ENVR","catalog":"200","title":"The Evolving Earth","credits":3,"is_required":True,"recommended":True},
          {"subject":"ENVR","catalog":"201","title":"Society, Environment and Sustainability","credits":3,"is_required":True,"recommended":True},
          {"subject":"ENVR","catalog":"202","title":"The Global Environment","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"203","title":"Knowledge, Ethics and Environment","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"301","title":"Environmental Research Design","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"400","title":"Environmental Thought","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "envr_fp_electives",
        "title": "Environment Electives",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "notes": "36 credits from approved environment-related courses across faculties.",
        "sort_order": 2,
        "courses": [
          {"subject":"GEOG","catalog":"303","title":"Environmental Change","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"225","title":"Economics of the Environment","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"326","title":"Ecological Economics","credits":3,"is_required":False},
          {"subject":"POLI","catalog":None,"title":"Environmental politics courses","credits":3,"is_required":False},
          {"subject":"ENVR","catalog":None,"title":"Any ENVR course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Environment – Honours (B.A.) ──
  {
    "program_key": "environment_honours",
    "name": "Environment – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "Honours program in Environment for senior B.A. students. Includes a thesis "
      "component."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/bieler-school-environment/environment-honours-ba/",
    "blocks": [
      {
        "block_key": "envr_hon_core",
        "title": "Required Core",
        "block_type": "required",
        "credits_needed": 24,
        "sort_order": 1,
        "courses": [
          {"subject":"ENVR","catalog":"200","title":"The Evolving Earth","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"201","title":"Society, Environment and Sustainability","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"202","title":"The Global Environment","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"203","title":"Knowledge, Ethics and Environment","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"301","title":"Environmental Research Design","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"400","title":"Environmental Thought","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "envr_hon_electives",
        "title": "Environment Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "sort_order": 2,
        "courses": [
          {"subject":"ENVR","catalog":None,"title":"Approved environment courses","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Environment – Joint Honours Component (B.A.) ──
  {
    "program_key": "environment_joint_honours",
    "name": "Environment – Joint Honours Component (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 36,
    "description": (
      "Joint Honours component in Environment. Must be combined with another Joint "
      "Honours component."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/bieler-school-environment/environment-joint-honours-component-ba/",
    "blocks": [
      {
        "block_key": "envr_jh_courses",
        "title": "Environment Joint Honours Courses",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "sort_order": 1,
        "courses": [
          {"subject":"ENVR","catalog":"200","title":"The Evolving Earth","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"201","title":"Society, Environment and Sustainability","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"203","title":"Knowledge, Ethics and Environment","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"301","title":"Environmental Research Design","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":"400","title":"Environmental Thought","credits":3,"is_required":True},
          {"subject":"ENVR","catalog":None,"title":"Additional approved ENVR courses","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Geography – Joint Honours Component (B.A.) ──
  {
    "program_key": "geography_joint_honours",
    "name": "Geography – Joint Honours Component (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 37,
    "description": (
      "Joint Honours component in Geography. Must be combined with another Joint "
      "Honours component."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/geography-joint-honours-component-ba/",
    "blocks": [
      {
        "block_key": "geog_jh_courses",
        "title": "Geography Joint Honours Courses",
        "block_type": "choose_credits",
        "credits_needed": 37,
        "notes": "37 credits from GEOG courses including core methods and GIS.",
        "sort_order": 1,
        "courses": [
          {"subject":"GEOG","catalog":"201","title":"Physical Geography: Geomorphology","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"202","title":"Quantitative Methods in Geography","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"314","title":"Geographic Information Systems","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":None,"title":"Additional GEOG courses","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── GIS and Remote Sensing – Minor Concentration (B.A.) ──
  {
    "program_key": "gis_remote_sensing_minor",
    "name": "GIS and Remote Sensing – Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "An 18-credit minor in Geographic Information Systems and remote sensing "
      "technology."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/gis-remote-sensing-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "gis_courses",
        "title": "GIS and Remote Sensing Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from GEOG courses focused on GIS and spatial analysis.",
        "sort_order": 1,
        "courses": [
          {"subject":"GEOG","catalog":"201","title":"Physical Geography: Geomorphology","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"202","title":"Quantitative Methods in Geography","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"314","title":"Geographic Information Systems","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Core GIS course"},
          {"subject":"GEOG","catalog":"401","title":"Advanced GIS","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":None,"title":"Any GEOG GIS/remote sensing course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Health Geography – Minor Concentration (B.A.) ──
  {
    "program_key": "health_geography_minor",
    "name": "Health Geography – Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "An 18-credit minor exploring the spatial dimensions of health, disease, and "
      "healthcare access."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/health-geography-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "hlthgeog_courses",
        "title": "Health Geography Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from GEOG and approved health-related courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"GEOG","catalog":"200","title":"Environmental Systems","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"320","title":"Urban Geography","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":None,"title":"Any GEOG health geography course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Urban Studies – Honours (B.A.) ──
  {
    "program_key": "urban_studies_honours",
    "name": "Urban Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "Honours program in Urban Studies with an emphasis on spatial planning and "
      "urban environments. Includes a thesis."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/urban-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "urbstud_hon_core",
        "title": "Required Core (12 credits)",
        "block_type": "required",
        "credits_needed": 12,
        "sort_order": 1,
        "courses": [
          {"subject":"GEOG","catalog":"201","title":"Introductory Geo-Information Science","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"217","title":"Cities in the Modern World",          "credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"351","title":"Quantitative Methods",                "credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"381","title":"Geographic Thought and Practice",     "credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "urbstud_hon_thesis",
        "title": "Honours Research (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "sort_order": 2,
        "courses": [
          {"subject":"GEOG","catalog":"491D1","title":"Honours Research","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"491D2","title":"Honours Research","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "urbstud_hon_electives",
        "title": "Urban Studies Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "sort_order": 3,
        "courses": [
          {"subject":"GEOG","catalog":"210","title":"Economic Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"330","title":"Political Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":None,"title":"Any urban-focused GEOG course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Behavioural Science – Minor Concentration (B.A.) ──
  {
    "program_key": "behavioural_science_minor",
    "name": "Behavioural Science – Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "Available ONLY to Arts Majors in Psychology. Allows additional "
      "specialization for graduate school preparation or Ordre des Psychologues du "
      "Québec requirements."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/psychology/behavioural-science-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "behsci_courses",
        "title": "PSYC Courses (not double-counted with major)",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": (
          "18 credits of PSYC courses not already counted toward the Psychology "
          "major. Restricted to B.A. Psychology Major students."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"PSYC","catalog":"305","title":"Research Methods in Psychology","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential for grad school applications"},
          {"subject":"PSYC","catalog":"307","title":"Clinical Psychology","credits":3,"is_required":False,"recommended":True},
          {"subject":"PSYC","catalog":"311","title":"Human Cognition and the Brain","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"317","title":"Behavioural Neuroscience 2","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"332","title":"Affective Neuroscience","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"402","title":"Memory and Brain","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"404","title":"Human Decision-Making","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":None,"title":"Any PSYC course at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Psychology – Joint Honours Component (B.A.) ──
  {
    "program_key": "psychology_joint_honours",
    "name": "Psychology – Joint Honours Component (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 36,
    "description": (
      "Joint Honours component in Psychology. Must be combined with another Joint "
      "Honours component."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/psychology/psychology-joint-honours-component-ba/",
    "blocks": [
      {
        "block_key": "psyc_jh_courses",
        "title": "Psychology Joint Honours Courses",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "notes": (
          "36 credits of PSYC including core methods and statistics. At least 12 at "
          "400-level."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"PSYC","catalog":"100","title":"Introduction to Psychology","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":"204","title":"Introduction to Psychological Statistics","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":"305","title":"Research Methods in Psychology","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":"211","title":"Intro to Behavioural Neuroscience","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":None,"title":"Additional PSYC courses at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Composition – Minor (B.Mus.) ──
  {
    "program_key": "music_composition_minor",
    "name": "Composition – Minor (B.Mus.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "An 18-credit minor in musical composition offered by the Schulich School of "
      "Music."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/composition-minor-bmus/",
    "blocks": [
      {
        "block_key": "mcomp_courses",
        "title": "Composition Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MUCO (composition) courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"MUCO","catalog":None,"title":"Composition courses from Schulich School of Music","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Music Education – Minor (B.Mus.) ──
  {
    "program_key": "music_education_minor",
    "name": "Music Education – Minor (B.Mus.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit minor in music education offered by the Schulich School of Music.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/music-education-minor-bmus/",
    "blocks": [
      {
        "block_key": "mued_courses",
        "title": "Music Education Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MUED courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"MUED","catalog":None,"title":"Music education courses from Schulich","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Music History – Minor (B.Mus.) ──
  {
    "program_key": "music_history_minor",
    "name": "Music History – Minor (B.Mus.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit minor in music history offered by the Schulich School of Music.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/music-history-minor-bmus/",
    "blocks": [
      {
        "block_key": "muhist_courses",
        "title": "Music History Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MUHL courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"MUHL","catalog":None,"title":"Music history courses from Schulich","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Music Theory – Minor (B.Mus.) ──
  {
    "program_key": "music_theory_minor",
    "name": "Music Theory – Minor (B.Mus.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit minor in music theory offered by the Schulich School of Music.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/music-theory-minor-bmus/",
    "blocks": [
      {
        "block_key": "muthry_courses",
        "title": "Music Theory Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MUCT (theory) courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"MUCT","catalog":None,"title":"Music theory courses from Schulich","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Musical Applications of Technology – Minor (B.Mus.) ──
  {
    "program_key": "musical_applications_technology_minor",
    "name": "Musical Applications of Technology – Minor (B.Mus.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit minor in music technology offered by the Schulich School of Music.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/musical-applications-technology-minor-bmus/",
    "blocks": [
      {
        "block_key": "mutech_courses",
        "title": "Music Technology Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MUMT (music technology) courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"MUMT","catalog":None,"title":"Music technology courses from Schulich","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Musical Science and Technology – Minor (B.Mus.) ──
  {
    "program_key": "musical_science_technology_minor",
    "name": "Musical Science and Technology – Minor (B.Mus.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": "An 18-credit interdisciplinary minor in science and technology applied to music.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/music/programs/music-research/musical-science-technology-minor-bmus/",
    "blocks": [
      {
        "block_key": "muscitech_courses",
        "title": "Musical Science & Technology Courses",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": "18 credits from MUMT and approved science courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"MUMT","catalog":None,"title":"Music science and technology courses","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── Science for Arts Students – Minor Concentration (B.A.) ──
  {
    "program_key": "science_for_arts_minor",
    "name": "Science for Arts Students – Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "An 18-credit minor allowing Arts students to explore a science discipline. "
      "Students choose one area: Atmospheric Sciences, Biochemistry, Biology, "
      "Chemistry, Earth & Planetary Sciences, Geography, Math & Stats, "
      "Microbiology, Pathology, Physics, Physiology, or Psychology. Coordinated by "
      "the Department of Biology."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/science-arts-students/science-arts-students-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "sci4arts_courses",
        "title": "Science Courses (choose one disciplinary area)",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": (
          "Students select one disciplinary area and take 15-18 credits in that area. "
          "100-level prerequisites cannot be counted toward the minor. Consult "
          "Program Adviser for approved course lists in each area."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"BIOL","catalog":"200","title":"Molecular Biology","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Start of Biology cell/molecular stream"},
          {"subject":"BIOL","catalog":"201","title":"Cell Biology and Metabolism","credits":3,"is_required":False},
          {"subject":"CHEM","catalog":"212","title":"Introductory Organic Chemistry 1","credits":3,"is_required":False},
          {"subject":"EPSC","catalog":"201","title":"Understanding Planet Earth","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"200","title":"Environmental Systems","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":False},
          {"subject":"PHYS","catalog":"230","title":"Dynamics of Simple Systems","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"211","title":"Introductory Behavioural Neuroscience","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Popular choice for Psychology stream"},
          {"subject":"PSYC","catalog":"212","title":"Perception","credits":3,"is_required":False},
        ],
      },
    ],
  },

]
