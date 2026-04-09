"""
McGill Faculty of Arts & Science – Degree Requirements Seed Data
Source: McGill Course Catalogue 2025-2026
https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/

This file covers the B.A. & Sc. (Bachelor of Arts and Science) degree, which is
jointly offered by the Faculties of Arts and Science. It includes:
  - The three unique Interfaculty Programs (Cognitive Science, Environment, Sustainability)
  - Their corresponding Honours extensions

Accuracy notes:
  - Verified from official McGill Course Catalogue PDFs (2025-26)
  - Always cross-check with current catalogue before academic decisions
  - B.A. & Sc. students must also complete an approved minor/minor concentration
  - All programs require completion of the B.A. & Sc. Foundation Program
"""

ARTS_SCIENCE_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════════
  #  COGNITIVE SCIENCE – INTERFACULTY PROGRAM (54 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key": "cogs_interfaculty_basc",
    "name": "Cognitive Science Interfaculty Program (B.A. & Sc.) (54 credits)",
    "program_type": "major",
    "faculty": "Faculty of Arts & Science",
    "total_credits": 54,
    "description": (
      "The Interfaculty Program Cognitive Science, restricted to students in the B.A. & Sc., "
      "is designed to allow students to explore the multidisciplinary study of cognition in "
      "humans and machines. The goal is to understand the principles of intelligence and thought "
      "with the hope that this will lead to a better understanding of the mind and of learning, "
      "and to the development of intelligent devices. Note: B.A. & Sc. students who take "
      "interfaculty programs must take at least 21 credits in Arts and 21 credits in Science "
      "across their interfaculty program and their minor or minor concentration."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/programs/cognitive-science/cognitive-science-interfaculty-program-basc/",
    "blocks": [
      {
        "block_key": "cogs_ifp_required",
        "title": "Required Course",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "All students must complete Introduction to Neuroscience 2.",
        "sort_order": 1,
        "courses": [
          {"subject": "NSCI", "catalog": "201", "title": "Introduction to Neuroscience 2", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "cogs_ifp_core_logic",
        "title": "Core – Logic (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from logic courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "COMP", "catalog": "230", "title": "Logic and Computability", "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "318", "title": "Mathematical Logic", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "210", "title": "Introduction to Deductive Logic 1", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_core_stats",
        "title": "Core – Statistics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from statistics courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "MATH", "catalog": "203", "title": "Principles of Statistics 1", "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "323", "title": "Probability", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "204", "title": "Introduction to Psychological Statistics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_core_cs",
        "title": "Core – Computer Science (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from computer science introductory courses.",
        "sort_order": 4,
        "courses": [
          {"subject": "COMP", "catalog": "202", "title": "Foundations of Programming", "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "204", "title": "Computer Programming for Life Sciences", "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "250", "title": "Introduction to Computer Science", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_core_ling",
        "title": "Core – Linguistics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from linguistics introductory courses.",
        "sort_order": 5,
        "courses": [
          {"subject": "LING", "catalog": "201", "title": "Introduction to Linguistics", "credits": 3, "is_required": False},
          {"subject": "LING", "catalog": "210", "title": "Introduction to Speech Science", "credits": 3, "is_required": False},
          {"subject": "LING", "catalog": "260", "title": "Meaning in Language", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_core_phil",
        "title": "Core – Philosophy (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from philosophy introductory courses.",
        "sort_order": 6,
        "courses": [
          {"subject": "PHIL", "catalog": "200", "title": "Introduction to Philosophy 1", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "201", "title": "Introduction to Philosophy 2", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "221", "title": "Introduction to History and Philosophy of Science 2", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_core_neuro",
        "title": "Core – Neuroscience (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from neuroscience introductory courses.",
        "sort_order": 7,
        "courses": [
          {"subject": "NSCI", "catalog": "200", "title": "Introduction to Neuroscience 1", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "211", "title": "Introductory Behavioural Neuroscience", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_core_psyc",
        "title": "Core – Psychology (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from psychology introductory courses.",
        "sort_order": 8,
        "courses": [
          {"subject": "PSYC", "catalog": "212", "title": "Perception", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "213", "title": "Cognition", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_comp_cs",
        "title": "Complementary – Computer Science",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Group – Computer Science",
        "notes": (
          "30 complementary credits total: 18 credits from ONE of the five disciplinary groups "
          "(Computer Science, Linguistics, Neuroscience, Philosophy, or Psychology), plus 12 credits "
          "from any of the five groups. At least 15 of the 30 complementary credits must be at the "
          "400 level or higher."
        ),
        "sort_order": 9,
        "courses": [
          {"subject": "COMP", "catalog": "206",  "title": "Introduction to Software Systems",              "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "250",  "title": "Introduction to Computer Science",              "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "251",  "title": "Algorithms and Data Structures",               "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "280",  "title": "History and Philosophy of Computing",          "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "302",  "title": "Programming Languages and Paradigms",          "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "330",  "title": "Theory of Computation",                        "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "345",  "title": "From Natural Language to Data Science",        "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "360",  "title": "Algorithm Design",                             "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "400",  "title": "Project in Computer Science",                  "credits": 4, "is_required": False},
          {"subject": "COMP", "catalog": "409",  "title": "Concurrent Programming",                       "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "417",  "title": "Introduction to Robotics and Intelligent Systems", "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "421",  "title": "Database Systems",                             "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "424",  "title": "Artificial Intelligence",                      "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "445",  "title": "Computational Linguistics",                    "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "451",  "title": "Fundamentals of Machine Learning",             "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "523",  "title": "Language-based Security",                      "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "527",  "title": "Logic and Computation",                        "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "531",  "title": "Advanced Theory of Computation",               "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "545",  "title": "Natural Language Understanding with Deep Learning", "credits": 4, "is_required": False},
          {"subject": "COMP", "catalog": "546",  "title": "Computational Perception",                     "credits": 4, "is_required": False},
          {"subject": "COMP", "catalog": "549",  "title": "Brain-Inspired Artificial Intelligence",       "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "550",  "title": "Natural Language Processing",                  "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "551",  "title": "Applied Machine Learning",                     "credits": 4, "is_required": False},
          {"subject": "COMP", "catalog": "558",  "title": "Fundamentals of Computer Vision",              "credits": 4, "is_required": False},
          {"subject": "COMP", "catalog": "562",  "title": "Theory of Machine Learning",                   "credits": 4, "is_required": False},
          {"subject": "COMP", "catalog": "579",  "title": "Reinforcement Learning",                       "credits": 4, "is_required": False},
          {"subject": "MATH", "catalog": "222",  "title": "Calculus 3",                                   "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "223",  "title": "Linear Algebra",                               "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "240",  "title": "Discrete Structures",                          "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_comp_ling",
        "title": "Complementary – Linguistics",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Group – Linguistics",
        "notes": "Any course at the 300, 400, or 500 level from the Department of Linguistics also counts.",
        "sort_order": 10,
        "courses": [
          {"subject": "LING", "catalog": "201",  "title": "Introduction to Linguistics",    "credits": 3, "is_required": False},
          {"subject": "LING", "catalog": "210",  "title": "Introduction to Speech Science", "credits": 3, "is_required": False},
          {"subject": "LING", "catalog": "260",  "title": "Meaning in Language",            "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_comp_phil",
        "title": "Complementary – Philosophy",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Group – Philosophy",
        "notes": None,
        "sort_order": 11,
        "courses": [
          {"subject": "NSCI", "catalog": "300",  "title": "Neuroethics",                                       "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "306",  "title": "Philosophy of Mind",                                "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "310",  "title": "Intermediate Logic",                                "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "311",  "title": "Philosophy of Mathematics",                         "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "341",  "title": "Philosophy of Science 1",                           "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "354",  "title": "Plato",                                             "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "355",  "title": "Aristotle",                                         "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "360",  "title": "17th Century Philosophy",                           "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "361",  "title": "18th Century Philosophy",                           "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "367",  "title": "19th Century Philosophy",                           "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "411",  "title": "Topics in Philosophy of Logic and Mathematics",     "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "415",  "title": "Philosophy of Language",                            "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "419",  "title": "Epistemology",                                      "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "421",  "title": "Metaphysics",                                       "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "441",  "title": "Philosophy of Science 2",                           "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "470",  "title": "Topics in Contemporary Analytic Philosophy",        "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "474",  "title": "Phenomenology",                                     "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_comp_psyc",
        "title": "Complementary – Psychology",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Group – Psychology",
        "notes": None,
        "sort_order": 12,
        "courses": [
          {"subject": "ANTH", "catalog": "440",  "title": "Cognitive Anthropology",                        "credits": 3, "is_required": False},
          {"subject": "MUMT", "catalog": "250",  "title": "Music Perception and Cognition",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "204",  "title": "Introduction to Psychological Statistics",      "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "211",  "title": "Introductory Behavioural Neuroscience",         "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "212",  "title": "Perception",                                    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "213",  "title": "Cognition",                                     "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "301",  "title": "Animal Learning and Theory",                    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "302",  "title": "Pain",                                          "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "303",  "title": "Introduction to Human Memory",                  "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "304",  "title": "Child Development",                             "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "305",  "title": "Statistics for Experimental Design",            "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "306",  "title": "Research Methods in Psychology",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "310",  "title": "Intelligence",                                  "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "311",  "title": "Human Cognition and the Brain",                 "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "315",  "title": "Computational Psychology",                      "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "317",  "title": "Genes and Behaviour",                           "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "318",  "title": "Behavioural Neuroscience 2",                    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "319",  "title": "Computational Models – Cognition",              "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "340",  "title": "Psychology of Language",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "341",  "title": "The Psychology of Bilingualism",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "342",  "title": "Hormones and Behaviour",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "352",  "title": "Research Methods and Lab in Cognitive Psychology", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "403",  "title": "Modern Psychology in Historical Perspective",   "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "406",  "title": "Psychological Tests",                           "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "410",  "title": "Special Topics in Neuropsychology",             "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "413",  "title": "Cognitive Development",                         "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "427",  "title": "Sensorimotor Neuroscience",                     "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "433",  "title": "Cognitive Science",                             "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "439",  "title": "Correlational Techniques",                      "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "443",  "title": "Affective Neuroscience",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "470",  "title": "Memory and Brain",                              "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "506",  "title": "Cognitive Neuroscience of Attention",           "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "513",  "title": "Human Decision-Making",                         "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "514",  "title": "Neurobiology of Memory",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "522",  "title": "Neurochemistry and Behaviour",                  "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "526",  "title": "Advances in Visual Perception",                 "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "529",  "title": "Music Cognition",                               "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "531",  "title": "Structural Equation Models",                    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "537",  "title": "Advanced Seminar in Psychology of Language",    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "538",  "title": "Categorization, Communication and Consciousness","credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "541",  "title": "Multilevel Modelling",                          "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "545",  "title": "Topics in Language Acquisition",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "560",  "title": "Machine Learning Tools in Psychology",          "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_comp_neuro",
        "title": "Complementary – Neuroscience",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Group – Neuroscience",
        "notes": "Students select either NSCI 200 or PHGY 209, but not both.",
        "sort_order": 13,
        "courses": [
          {"subject": "ANAT", "catalog": "321",  "title": "Circuitry of the Human Brain",                  "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "200",  "title": "Molecular Biology",                             "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "201",  "title": "Cell Biology and Metabolism",                   "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "216",  "title": "Biology of Behaviour",                          "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "306",  "title": "Neural Basis of Behaviour",                     "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "307",  "title": "Behavioural Ecology",                           "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "320",  "title": "Evolution of Brain and Behaviour",              "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "389",  "title": "Laboratory in Neurobiology",                    "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "414",  "title": "Invertebrate Brain Circuits and Behaviours",    "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "506",  "title": "Neurobiology of Learning",                      "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "507",  "title": "Animal Communication",                          "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "517",  "title": "Cognitive Ecology",                             "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "530",  "title": "Advances in Neuroethology",                     "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "532",  "title": "Developmental Neurobiology Seminar",            "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "580",  "title": "Genetic Approaches to Neural Systems",          "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "588",  "title": "Advances in Molecular/Cellular Neurobiology",  "credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "212",  "title": "Introductory Organic Chemistry 1",              "credits": 4, "is_required": False},
          {"subject": "NEUR", "catalog": "310",  "title": "Cellular Neurobiology",                         "credits": 3, "is_required": False},
          {"subject": "NEUR", "catalog": "503",  "title": "Computational Neuroscience",                    "credits": 3, "is_required": False},
          {"subject": "NEUR", "catalog": "507",  "title": "Topics in Radionuclide Imaging",                "credits": 3, "is_required": False},
          {"subject": "NSCI", "catalog": "200",  "title": "Introduction to Neuroscience 1",                "credits": 3, "is_required": False, "notes": "Select either this or PHGY 209, not both."},
          {"subject": "NSCI", "catalog": "300",  "title": "Neuroethics",                                   "credits": 3, "is_required": False},
          {"subject": "PHGY", "catalog": "209",  "title": "Mammalian Physiology 1",                        "credits": 3, "is_required": False, "notes": "Select either this or NSCI 200, not both."},
          {"subject": "PHGY", "catalog": "311",  "title": "Channels, Synapses and Hormones",               "credits": 3, "is_required": False},
          {"subject": "PHGY", "catalog": "314",  "title": "Integrative Neuroscience",                      "credits": 3, "is_required": False},
          {"subject": "PHGY", "catalog": "556",  "title": "Topics in Systems Neuroscience",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "211",  "title": "Introductory Behavioural Neuroscience",         "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "302",  "title": "Pain",                                          "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "303",  "title": "Introduction to Human Memory",                  "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "306",  "title": "Research Methods in Psychology",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "311",  "title": "Human Cognition and the Brain",                 "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "317",  "title": "Genes and Behaviour",                           "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "318",  "title": "Behavioural Neuroscience 2",                    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "342",  "title": "Hormones and Behaviour",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "410",  "title": "Special Topics in Neuropsychology",             "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "427",  "title": "Sensorimotor Neuroscience",                     "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "433",  "title": "Cognitive Science",                             "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "443",  "title": "Affective Neuroscience",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "444",  "title": "Sleep Mechanisms and Behaviour",                "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "502",  "title": "Psychoneuroendocrinology",                      "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "506",  "title": "Cognitive Neuroscience of Attention",           "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "514",  "title": "Neurobiology of Memory",                        "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "522",  "title": "Neurochemistry and Behaviour",                  "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "526",  "title": "Advances in Visual Perception",                 "credits": 3, "is_required": False},
          {"subject": "PSYT", "catalog": "301",  "title": "Issues in Drug Dependence",                     "credits": 3, "is_required": False},
          {"subject": "PSYT", "catalog": "500",  "title": "Advances: Neurobiology of Mental Disorders",    "credits": 3, "is_required": False},
          {"subject": "PSYT", "catalog": "515",  "title": "Advanced Studies in Addiction",                 "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_ifp_research",
        "title": "Optional Research Course",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "COGS 401 Research Cognitive Science 1 (6 credits) is an optional supervised research "
          "project for Interfaculty Program students (prerequisites: 30 credits of COGS program "
          "coursework, Program Director approval, CGPA > 3.00). It counts toward the 30 "
          "complementary credits if taken. COGS 444 is the required research course for Honours only."
        ),
        "sort_order": 14,
        "courses": [
          {"subject": "COGS", "catalog": "401", "title": "Research Cognitive Science 1", "credits": 6, "is_required": False},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  COGNITIVE SCIENCE – HONOURS (60 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key": "cogs_honours_basc",
    "name": "Cognitive Science Honours (B.A. & Sc.) (60 credits)",
    "program_type": "honours",
    "faculty": "Faculty of Arts & Science",
    "total_credits": 60,
    "description": (
      "The Honours Cognitive Science, restricted to B.A. & Sc. students, extends the Interfaculty "
      "program and offers students an opportunity to undertake a research project in close association "
      "with professors. To receive an Honours degree, students must achieve a minimum overall program "
      "GPA of 3.3 at graduation and attain a grade of B+ (3.3) or better in COGS 444 Honours Research. "
      "Students must complete both the 60-credit Honours program and an approved minor in the Faculties "
      "of Arts or of Science. B.A. & Sc. students must take at least 21 credits in Arts and 21 in "
      "Science across their interfaculty program and their minor."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/programs/cognitive-science/cognitive-science-honours-basc/",
    "blocks": [
      {
        "block_key": "cogs_hon_required",
        "title": "Required Courses",
        "block_type": "required",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name": None,
        "notes": "COGS 444 Honours Research (6 cr) and NSCI 201 Introduction to Neuroscience 2 (3 cr) are both required.",
        "sort_order": 1,
        "courses": [
          {"subject": "COGS", "catalog": "444", "title": "Honours Research", "credits": 6, "is_required": True},
          {"subject": "NSCI", "catalog": "201", "title": "Introduction to Neuroscience 2", "credits": 3, "is_required": True},
        ],
      },
      # Core complementary blocks are identical to the interfaculty program
      {
        "block_key": "cogs_hon_core_logic",
        "title": "Core – Logic (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from logic courses.",
        "sort_order": 2,
        "courses": [
          {"subject": "COMP", "catalog": "230", "title": "Logic and Computability", "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "318", "title": "Mathematical Logic", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "210", "title": "Introduction to Deductive Logic 1", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_core_stats",
        "title": "Core – Statistics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from statistics courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "MATH", "catalog": "203", "title": "Principles of Statistics 1", "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "323", "title": "Probability", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "204", "title": "Introduction to Psychological Statistics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_core_cs",
        "title": "Core – Computer Science (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": None,
        "sort_order": 4,
        "courses": [
          {"subject": "COMP", "catalog": "202", "title": "Foundations of Programming", "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "204", "title": "Computer Programming for Life Sciences", "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "250", "title": "Introduction to Computer Science", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_core_ling",
        "title": "Core – Linguistics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": None,
        "sort_order": 5,
        "courses": [
          {"subject": "LING", "catalog": "201", "title": "Introduction to Linguistics", "credits": 3, "is_required": False},
          {"subject": "LING", "catalog": "210", "title": "Introduction to Speech Science", "credits": 3, "is_required": False},
          {"subject": "LING", "catalog": "260", "title": "Meaning in Language", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_core_phil",
        "title": "Core – Philosophy (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": None,
        "sort_order": 6,
        "courses": [
          {"subject": "PHIL", "catalog": "200", "title": "Introduction to Philosophy 1", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "201", "title": "Introduction to Philosophy 2", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "221", "title": "Introduction to History and Philosophy of Science 2", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_core_neuro",
        "title": "Core – Neuroscience (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": None,
        "sort_order": 7,
        "courses": [
          {"subject": "NSCI", "catalog": "200", "title": "Introduction to Neuroscience 1", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "211", "title": "Introductory Behavioural Neuroscience", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_core_psyc",
        "title": "Core – Psychology (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": None,
        "sort_order": 8,
        "courses": [
          {"subject": "PSYC", "catalog": "212", "title": "Perception", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "213", "title": "Cognition", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "cogs_hon_complementary",
        "title": "Complementary Courses (30 credits)",
        "block_type": "choose_credits",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "30 credits: 18 from ONE of the five disciplinary groups (Computer Science, Linguistics, "
          "Neuroscience, Philosophy, or Psychology), plus 12 from any of the five groups. "
          "At least 15 of the 30 credits must be at the 400 level or higher. "
          "See the Interfaculty Program course lists for available courses in each group."
        ),
        "sort_order": 9,
        "courses": [],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  SUSTAINABILITY, SCIENCE AND SOCIETY – INTERFACULTY PROGRAM (54 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key": "sss_interfaculty_basc",
    "name": "Sustainability, Science and Society Interfaculty Program (B.A. & Sc.) (54 credits)",
    "program_type": "major",
    "faculty": "Faculty of Arts & Science",
    "total_credits": 54,
    "description": (
      "The B.A. & Sc. Interfaculty Program in Sustainability, Science and Society focuses on the "
      "interdisciplinary and integrative knowledge and skills required to effectively understand "
      "and address challenges in transitioning to a sustainable future. The program is built on "
      "three pillars: (1) Science and Technology – biophysical basis of current challenges; "
      "(2) Economics, Policy, and Governance – how to make the sustainability transition; "
      "(3) Ethics, Equity, and Justice – why we need change and related equity issues. "
      "Offered in collaboration with the Bieler School of Environment."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/programs/sustainability-science-society/sustainability-science-society-interfaculty-program-basc/",
    "blocks": [
      {
        "block_key": "sss_foundations",
        "title": "Foundations of Sustainability (Required)",
        "block_type": "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "All four courses are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True},
          {"subject": "GEOG", "catalog": "360", "title": "Analyzing Sustainability", "credits": 3, "is_required": True},
          {"subject": "GEOG", "catalog": "401", "title": "Socio-Environmental Systems: Theory and Simulation", "credits": 3, "is_required": True},
          {"subject": "GEOG", "catalog": "460", "title": "Research in Sustainability", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "sss_biophysical",
        "title": "Biophysical, Societal, Cultural, Institutional, and Ethical (Required)",
        "block_type": "required",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": None,
        "notes": "All five courses are required.",
        "sort_order": 2,
        "courses": [
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment", "credits": 3, "is_required": True},
          {"subject": "GEOG", "catalog": "203", "title": "Environmental Systems", "credits": 3, "is_required": True},
          {"subject": "GEOG", "catalog": "408", "title": "Geography of Development", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "sss_comp_stats",
        "title": "Complementary – Statistics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from statistics courses.",
        "sort_order": 3,
        "courses": [
          {"subject": "AEMA", "catalog": "310", "title": "Statistical Methods 1", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "373", "title": "Biometry", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "202", "title": "Statistics and Spatial Analysis", "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "203", "title": "Principles of Statistics 1", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "204", "title": "Introduction to Psychological Statistics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sss_comp_econ",
        "title": "Complementary – Economics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from economics courses.",
        "sort_order": 4,
        "courses": [
          {"subject": "AGEC", "catalog": "200", "title": "Principles of Microeconomics", "credits": 3, "is_required": False},
          {"subject": "AGEC", "catalog": "201", "title": "Principles of Macroeconomics", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "208", "title": "Microeconomic Analysis and Applications", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "209", "title": "Macroeconomic Analysis and Applications", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "225", "title": "Economics of the Environment", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "230D1", "title": "Microeconomic Theory", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sss_comp_business",
        "title": "Complementary – Sustainability in Business (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose 3 credits from management/business courses.",
        "sort_order": 5,
        "courses": [
          {"subject": "INSY", "catalog": "455", "title": "Technology and Innovation for Sustainability", "credits": 3, "is_required": False},
          {"subject": "MGCR", "catalog": "460", "title": "Social Context of Business", "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "440", "title": "Strategies for Sustainability", "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "475", "title": "Strategies for Developing Countries", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sss_area1_methods",
        "title": "Area 1 – Methods: Observation, Analysis, Modelling, and Management",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 1 – Methods",
        "notes": (
          "18 additional credits from Areas 1, 2, and 3: at least 9 credits at the 300 level or higher, "
          "and at least 6 credits from EACH of the three areas."
        ),
        "sort_order": 6,
        "courses": [
          {"subject": "ENVB", "catalog": "437", "title": "Assessing Environmental Impact", "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "529", "title": "GIS for Natural Resource Management", "credits": 3, "is_required": False, "notes": "Or GEOG 201, but not both."},
          {"subject": "ESYS", "catalog": "301", "title": "Earth System Modelling", "credits": 3, "is_required": False},
          {"subject": "ESYS", "catalog": "500", "title": "Collaborative Research Project", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "201", "title": "Introductory Geo-Information Science", "credits": 3, "is_required": False, "notes": "Or ENVB 529, but not both."},
          {"subject": "GEOG", "catalog": "302", "title": "Environmental Management 1", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "308", "title": "Remote Sensing for Earth Observation", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "314", "title": "Geospatial Analysis", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "333", "title": "Introduction to Programming for Spatial Sciences", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "351", "title": "Quantitative Methods", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "404", "title": "Environmental Management 2", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "414", "title": "Advanced Geospatial Analysis", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "495", "title": "Field Studies – Physical Geography", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "509", "title": "Qualitative Methods", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "512", "title": "Advanced Quantitative Methods in Social Field Research", "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "506", "title": "Environmental Policy and Planning", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sss_area2a_society",
        "title": "Area 2A – Society, Economics, and Policy",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 2A – Society, Economics, and Policy",
        "notes": "At least 3 credits from Area 2A.",
        "sort_order": 7,
        "courses": [
          {"subject": "AGEC", "catalog": "333", "title": "Resource Economics", "credits": 3, "is_required": False},
          {"subject": "AGEC", "catalog": "430", "title": "Agriculture, Food and Resource Policy", "credits": 3, "is_required": False},
          {"subject": "AGEC", "catalog": "442", "title": "Economics of International Agricultural Development", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "206", "title": "Environment and Culture", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "212", "title": "Anthropology of Development", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "339", "title": "Ecological Anthropology", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "313", "title": "Economic Development 1", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "314", "title": "Economic Development 2", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "326", "title": "Ecological Economics", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "347", "title": "Economics of Climate Change", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "405", "title": "Natural Resource Economics", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "210", "title": "Global Places and Peoples", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "216", "title": "Geography of the World Economy", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "303", "title": "Health Geography", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "310", "title": "Development and Livelihoods", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "316", "title": "Political Geography", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "409", "title": "Geographies of Developing Asia", "credits": 3, "is_required": False},
          {"subject": "HIST", "catalog": "292", "title": "History and the Environment", "credits": 3, "is_required": False},
          {"subject": "INDG", "catalog": "200", "title": "Introduction to Indigenous Studies", "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "350", "title": "Global Environmental Politics", "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "530", "title": "Urban Infrastructure and Services in International Context", "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "553", "title": "Urban Governance", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sss_area2b_ethics",
        "title": "Area 2B – Ethics and Equity",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 2B – Ethics and Equity",
        "notes": "At least 3 credits from Area 2B.",
        "sort_order": 8,
        "courses": [
          {"subject": "ENVR", "catalog": "400", "title": "Environmental Thought", "credits": 3, "is_required": False},
          {"subject": "MGPO", "catalog": "450", "title": "Ethics in Management", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "349", "title": "Environmental Philosophy", "credits": 3, "is_required": False},
          {"subject": "RELG", "catalog": "270", "title": "Religious Ethics and the Environment", "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "325", "title": "Sociology of Science", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "sss_area3_biophysical",
        "title": "Area 3 – Sustainability and Biophysical Processes",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 3 – Biophysical Processes",
        "notes": "At least 6 credits from Area 3. BIOL 540 and ENVR 540 cannot both be taken; BREE 217 and GEOG 322 cannot both be taken.",
        "sort_order": 9,
        "courses": [
          {"subject": "ATOC", "catalog": "214", "title": "Introduction: Physics of the Atmosphere", "credits": 3, "is_required": False},
          {"subject": "ATOC", "catalog": "215", "title": "Oceans, Weather and Climate", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "308", "title": "Ecological Dynamics", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "310", "title": "Biodiversity and Ecosystems", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "465", "title": "Conservation Biology", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "540", "title": "Ecology of Species Invasions", "credits": 3, "is_required": False, "notes": "Or ENVR 540, not both."},
          {"subject": "BREE", "catalog": "217", "title": "Hydrology and Water Resources", "credits": 3, "is_required": False, "notes": "Or GEOG 322, not both."},
          {"subject": "CHEM", "catalog": "462", "title": "Green Chemistry", "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "305", "title": "Population and Community Ecology", "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "410", "title": "Ecosystem Ecology", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "540", "title": "Ecology of Species Invasions", "credits": 3, "is_required": False, "notes": "Or BIOL 540, not both."},
          {"subject": "ESYS", "catalog": "200", "title": "Earth-System Interactions", "credits": 3, "is_required": False},
          {"subject": "ESYS", "catalog": "300", "title": "Earth Data Analysis", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "221", "title": "Environment and Health", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "272", "title": "Earth's Changing Surface", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "305", "title": "Soils and Environment", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "321", "title": "Climatic Environments", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "322", "title": "Environmental Hydrology", "credits": 3, "is_required": False, "notes": "Or BREE 217, not both."},
          {"subject": "GEOG", "catalog": "372", "title": "Running Water Environments", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "403", "title": "Global Health and Environmental Change", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "438", "title": "Sand in the Anthropocene", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "470", "title": "Wetlands", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "530", "title": "Global Land and Water Resources", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "555", "title": "Ecological Restoration", "credits": 3, "is_required": False},
          {"subject": "NRSC", "catalog": "333", "title": "Pollution and Bioremediation", "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  SUSTAINABILITY, SCIENCE AND SOCIETY – HONOURS (60 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key": "sss_honours_basc",
    "name": "Sustainability, Science and Society Honours (B.A. & Sc.) (60 credits)",
    "program_type": "honours",
    "faculty": "Faculty of Arts & Science",
    "total_credits": 60,
    "description": (
      "The grand challenge of the 21st century is sustainable well-being – improving human well-being "
      "while maintaining the Earth's life-support systems. This B.A. & Sc. Honours program provides "
      "the interdisciplinary knowledge and skills to address this challenge across three pillars: "
      "Science and Technology, Economics/Policy/Governance, and Ethics/Equity/Justice. "
      "The Honours extension adds 6 credits of supervised research (SSS 490 Honours Research) "
      "to the 54-credit Interfaculty Program requirements. Minimum program GPA of 3.3 required at graduation."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/programs/sustainability-science-society/sustainability-science-society-honours-basc/",
    "blocks": [
      {
        "block_key": "sss_hon_research",
        "title": "Additional Honours Research Requirement",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "In addition to all 54 credits of the SSS Interfaculty Program, Honours students must "
          "complete 6 credits of supervised honours research in their final year."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "SSS", "catalog": "490", "title": "Honours Research", "credits": 6, "is_required": True},
        ],
      },
      {
        "block_key": "sss_hon_note",
        "title": "All SSS Interfaculty Requirements",
        "block_type": "choose_credits",
        "credits_needed": 54,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "All required and complementary courses from the SSS Interfaculty Program (54 credits) apply. "
          "See the SSS Interfaculty Program (program_key: sss_interfaculty_basc) for full course lists."
        ),
        "sort_order": 2,
        "courses": [],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  ENVIRONMENT – INTERFACULTY PROGRAM (54 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key": "environment_interfaculty_basc",
    "name": "Environment Interfaculty Program (B.A. & Sc.) (54 credits)",
    "program_type": "major",
    "faculty": "Faculty of Arts & Science",
    "total_credits": 54,
    "description": (
      "The B.A. & Sc. Interfaculty Program in Environment focuses on the myriad of environmental "
      "problems faced by society today. The program offers a great degree of flexibility and can "
      "provide both broad liberal arts/science training and specific in-depth focus on particular "
      "areas of interest. Students are required to take a maximum of 21 credits at the 200 level "
      "and a minimum of 12 credits at the 400 level or higher. Students must complete at least "
      "21 credits in Arts and at least 21 in Science across their interfaculty program and minor. "
      "ENVR courses count toward both Arts and Science credit requirements."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/programs/environment/interfaculty-program-environment-basc/",
    "blocks": [
      {
        "block_key": "env_core",
        "title": "Core Courses (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All 6 core ENVR courses are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "301", "title": "Environmental Research Design", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "400", "title": "Environmental Thought", "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key": "env_research",
        "title": "Senior Research Project (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose one senior research project (3 credits). Extra credits from 6-credit options count as electives.",
        "sort_order": 2,
        "courses": [
          {"subject": "AEBI", "catalog": "427", "title": "Barbados Interdisciplinary Project", "credits": 6, "is_required": False},
          {"subject": "ENVR", "catalog": "401", "title": "Environmental Research", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "451", "title": "Research in Panama", "credits": 6, "is_required": False},
          {"subject": "FSCI", "catalog": "444", "title": "Barbados Research Project", "credits": 6, "is_required": False},
          {"subject": "GEOG", "catalog": "451", "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_stats",
        "title": "Statistics (3 credits)",
        "block_type": "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name": None,
        "notes": "Choose one statistics course. Only 3 credits will be applied to the program.",
        "sort_order": 3,
        "courses": [
          {"subject": "AEMA", "catalog": "310", "title": "Statistical Methods 1", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "202", "title": "Statistics and Spatial Analysis", "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "203", "title": "Principles of Statistics 1", "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "204", "title": "Introduction to Psychological Statistics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area1_ecology",
        "title": "Area 1 – Population, Community and Ecosystem Ecology",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 1 – Ecology",
        "notes": (
          "30 credits from at least THREE areas; at least 6 credits at the 400 level or higher "
          "(from any area list or approved by Program Adviser). "
          "May take BIOL 308 or ENVB 305, not both."
        ),
        "sort_order": 4,
        "courses": [
          {"subject": "BIOL", "catalog": "308", "title": "Ecological Dynamics", "credits": 3, "is_required": False, "notes": "Or ENVB 305, not both."},
          {"subject": "BIOL", "catalog": "342", "title": "Global Change Biology of Aquatic Ecosystems", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "432", "title": "Limnology", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "441", "title": "Biological Oceanography", "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "305", "title": "Population and Community Ecology", "credits": 3, "is_required": False, "notes": "Or BIOL 308, not both."},
          {"subject": "ENVB", "catalog": "410", "title": "Ecosystem Ecology", "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "500", "title": "Advanced Topics in Ecotoxicology", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "540", "title": "Ecology of Species Invasions", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area2_earth",
        "title": "Area 2 – Earth Science and Atmospheric Science",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 2 – Earth & Atmospheric Science",
        "notes": "Note: may take only one of GEOG 322, BREE 217, or CIVE 323 (Hydrology options).",
        "sort_order": 5,
        "courses": [
          {"subject": "ATOC", "catalog": "214", "title": "Introduction: Physics of the Atmosphere", "credits": 3, "is_required": False},
          {"subject": "ATOC", "catalog": "215", "title": "Oceans, Weather and Climate", "credits": 3, "is_required": False},
          {"subject": "ATOC", "catalog": "512", "title": "Climate Dynamics", "credits": 3, "is_required": False},
          {"subject": "BREE", "catalog": "217", "title": "Hydrology and Water Resources", "credits": 3, "is_required": False, "notes": "Or GEOG 322 or CIVE 323, not both."},
          {"subject": "CIVE", "catalog": "323", "title": "Hydrology and Water Resources", "credits": 3, "is_required": False, "notes": "Or GEOG 322 or BREE 217, not both."},
          {"subject": "EPSC", "catalog": "201", "title": "Earth and Planetary Sciences", "credits": 3, "is_required": False},
          {"subject": "EPSC", "catalog": "233", "title": "Earth's Climate: Past and Present", "credits": 3, "is_required": False},
          {"subject": "EPSC", "catalog": "330", "title": "Applied Geomorphology", "credits": 3, "is_required": False},
          {"subject": "EPSC", "catalog": "522", "title": "Advanced Environmental Hydrology", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "272", "title": "Earth's Changing Surface", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "305", "title": "Soils and Environment", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "321", "title": "Climatic Environments", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "322", "title": "Environmental Hydrology", "credits": 3, "is_required": False, "notes": "Or BREE 217 or CIVE 323, not both."},
          {"subject": "GEOG", "catalog": "372", "title": "Running Water Environments", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "522", "title": "Advanced Environmental Hydrology", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area3_geog",
        "title": "Area 3 – Environmental Geography and Remote Sensing",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 3 – Environmental Geography & Remote Sensing",
        "notes": None,
        "sort_order": 6,
        "courses": [
          {"subject": "GEOG", "catalog": "201", "title": "Introductory Geo-Information Science", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "302", "title": "Environmental Management 1", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "308", "title": "Remote Sensing for Earth Observation", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "314", "title": "Geospatial Analysis", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "403", "title": "Global Health and Environmental Change", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "404", "title": "Environmental Management 2", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "414", "title": "Advanced Geospatial Analysis", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "438", "title": "Sand in the Anthropocene", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "495", "title": "Field Studies – Physical Geography", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "530", "title": "Global Land and Water Resources", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area4_economics",
        "title": "Area 4 – Resource and Environmental Economics",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 4 – Resource & Environmental Economics",
        "notes": "May take AGEC 200 or ECON 208 (microeconomics), not both.",
        "sort_order": 7,
        "courses": [
          {"subject": "AGEC", "catalog": "200", "title": "Principles of Microeconomics", "credits": 3, "is_required": False, "notes": "Or ECON 208, not both."},
          {"subject": "ECON", "catalog": "208", "title": "Microeconomic Analysis and Applications", "credits": 3, "is_required": False, "notes": "Or AGEC 200, not both."},
          {"subject": "ECON", "catalog": "326", "title": "Ecological Economics", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "347", "title": "Economics of Climate Change", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "405", "title": "Natural Resource Economics", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "511", "title": "Energy, Economy and Environment", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "216", "title": "Geography of the World Economy", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area5_policy",
        "title": "Area 5 – Environmental Policy and Law",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 5 – Environmental Policy & Law",
        "notes": None,
        "sort_order": 8,
        "courses": [
          {"subject": "GEOG", "catalog": "316", "title": "Political Geography", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "408", "title": "Geography of Development", "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "350", "title": "Global Environmental Politics", "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "506", "title": "Environmental Policy and Planning", "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "530", "title": "Urban Infrastructure and Services in International Context", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area6_society",
        "title": "Area 6 – Environment and Society",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 6 – Environment and Society",
        "notes": None,
        "sort_order": 9,
        "courses": [
          {"subject": "ANTH", "catalog": "206", "title": "Environment and Culture", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "339", "title": "Ecological Anthropology", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "421", "title": "Montreal: Environmental History and Sustainability", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "221", "title": "Environment and Health", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "303", "title": "Health Geography", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "310", "title": "Development and Livelihoods", "credits": 3, "is_required": False},
          {"subject": "HIST", "catalog": "292", "title": "History and the Environment", "credits": 3, "is_required": False},
          {"subject": "PHIL", "catalog": "349", "title": "Environmental Philosophy", "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "328", "title": "Sociology of the Environment", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area7_health",
        "title": "Area 7 – Environment and Health",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 7 – Environment and Health",
        "notes": None,
        "sort_order": 10,
        "courses": [
          {"subject": "BIOL", "catalog": "465", "title": "Conservation Biology", "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "310", "title": "Biodiversity and Ecosystems", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "555", "title": "Ecological Restoration", "credits": 3, "is_required": False},
          {"subject": "NRSC", "catalog": "333", "title": "Pollution and Bioremediation", "credits": 3, "is_required": False},
          {"subject": "NUTR", "catalog": "307", "title": "Metabolism and Human Nutrition", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area8_development",
        "title": "Area 8 – Development and Underdevelopment",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 8 – Development & Underdevelopment",
        "notes": None,
        "sort_order": 11,
        "courses": [
          {"subject": "AGRI", "catalog": "411", "title": "Global Issues on Development, Food and Agriculture", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "212", "title": "Anthropology of Development", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "418", "title": "Environment and Development", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "313", "title": "Economic Development 1", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "314", "title": "Economic Development 2", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "325", "title": "New Master-Planned Cities", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "408", "title": "Geography of Development", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "409", "title": "Geographies of Developing Asia", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "423", "title": "Dilemmas of Development (in Africa)", "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "227", "title": "Introduction to Comparative Politics – Global South", "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "445", "title": "International Political Economy: Monetary Relations", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "env_area9_culture",
        "title": "Area 9 – Cultures and Peoples",
        "block_type": "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name": "Area 9 – Cultures & Peoples",
        "notes": None,
        "sort_order": 12,
        "courses": [
          {"subject": "ANTH", "catalog": "206", "title": "Environment and Culture", "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "339", "title": "Ecological Anthropology", "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "421", "title": "Montreal: Environmental History and Sustainability", "credits": 3, "is_required": False},
          {"subject": "INDG", "catalog": "200", "title": "Introduction to Indigenous Studies", "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  ENVIRONMENT – HONOURS (60 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key": "environment_honours_basc",
    "name": "Environment Honours (B.A. & Sc.) (60 credits)",
    "program_type": "honours",
    "faculty": "Faculty of Arts & Science",
    "total_credits": 60,
    "description": (
      "The B.A. & Sc. Honours in Environment extends the 54-credit Interfaculty Program in Environment "
      "with a 6-credit supervised research project. Students work closely with a faculty supervisor on "
      "an original research question related to environmental studies. Minimum program GPA of 3.3 "
      "required at graduation. Students must also complete an approved minor concentration."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts-science/programs/environment/",
    "blocks": [
      {
        "block_key": "env_hon_research",
        "title": "Additional Honours Research Requirement",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "In addition to all 54 credits of the Environment Interfaculty Program, Honours students "
          "must complete 6 credits of supervised honours research."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "490", "title": "Honours Research in Environment", "credits": 6, "is_required": True},
        ],
      },
      {
        "block_key": "env_hon_note",
        "title": "All Environment Interfaculty Requirements",
        "block_type": "choose_credits",
        "credits_needed": 54,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "All required and complementary courses from the Environment Interfaculty Program (54 credits) apply. "
          "See the Environment Interfaculty Program (program_key: environment_interfaculty_basc) for full course lists."
        ),
        "sort_order": 2,
        "courses": [],
      },
    ],
  },

]


# ══════════════════════════════════════════════════════════════════════════
#  DATABASE SEED FUNCTION
# ══════════════════════════════════════════════════════════════════════════

def seed_degree_requirements(supabase):
    """
    Insert all B.A. & Sc. degree requirements into Supabase.
    Safe to re-run: uses upsert on program_key, then deletes+reinserts blocks.
    Courses are batch-inserted per block (one call per block) to avoid timeouts.
    """
    inserted_programs = 0
    inserted_blocks   = 0
    inserted_courses  = 0

    for prog in ARTS_SCIENCE_PROGRAMS:
        prog_data = {
            "program_key":   prog["program_key"],
            "name":          prog["name"],
            "faculty":       prog.get("faculty", "Faculty of Arts & Science"),
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
                courses_to_insert.append({
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
                })

            if courses_to_insert:
                supabase.table("requirement_courses").insert(courses_to_insert).execute()
                inserted_courses += len(courses_to_insert)

    return {
        "programs": inserted_programs,
        "blocks":   inserted_blocks,
        "courses":  inserted_courses,
    }


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    stats = seed_degree_requirements(supabase)
    print(f"Seeded: {stats['programs']} programs, {stats['blocks']} blocks, {stats['courses']} courses")
