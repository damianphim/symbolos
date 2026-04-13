"""
McGill Faculty of Arts – Core Humanities: Linguistics, History, Art History, English Literature, Communication Studies, Philosophy
Sub-module of arts_degree_requirements.py
"""

ARTS_HUMANITIES = [
  # ──────────────────────────────────────────────────────────────────
  # LINGUISTICS
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "linguistics_major",
    "name": "Linguistics – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "Covers theoretical linguistics (phonology, syntax, semantics), "
      "experimental linguistics, computational linguistics, and sociolinguistics."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/linguistics/linguistics-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core Courses",
        "credits_needed": 15,
        "notes": "All five required. Must be taken at McGill.",
        "courses": [
          {"subject":"LING","catalog":"201","title":"Introduction to Linguistics","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"First course — gateway to all others"},
          {"subject":"LING","catalog":"330","title":"Phonetics","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Take after LING 201; prereq for LING 331"},
          {"subject":"LING","catalog":"331","title":"Phonology 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core phonology — take in U2"},
          {"subject":"LING","catalog":"360","title":"Introduction to Semantics","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Requires LING 201 + logic course"},
          {"subject":"LING","catalog":"371","title":"Syntax 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core syntax; take before 400-level"},
        ],
      },
      {
        "block_key": "logic",
        "title": "Logic/Formal Methods",
        "credits_needed": 3,
        "notes": "One of: COMP 230, MATH 318, or PHIL 210.",
        "courses": [
          {"subject":"PHIL","catalog":"210","title":"Introduction to Deductive Logic 1","credits":3,"is_required":False,"choose_from_group":"logic","choose_n_credits":3,"recommended":True,"recommendation_reason":"Most accessible option; great standalone course"},
          {"subject":"COMP","catalog":"230","title":"Logic and Computability","credits":3,"is_required":False,"choose_from_group":"logic","choose_n_credits":3},
          {"subject":"MATH","catalog":"318","title":"Mathematical Logic","credits":3,"is_required":False,"choose_from_group":"logic","choose_n_credits":3},
        ],
      },
      {
        "block_key": "complementary",
        "title": "Complementary LING Electives",
        "credits_needed": 18,
        "min_credits_400": 9,
        "max_credits_200": 3,
        "notes": "18 credits of LING courses; at least 9 at 400/500-level; max 3 at 200-level.",
        "courses": [
          {"subject":"LING","catalog":"320","title":"Sociolinguistics 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Popular 300-level; great complement to phonetics"},
          {"subject":"LING","catalog":"325","title":"Canadian English","credits":3,"is_required":False},
          {"subject":"LING","catalog":"350","title":"Linguistic Aspects of Bilingualism","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"355","title":"Language Acquisition 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Top-rated course; good for cognitive science crossover"},
          {"subject":"LING","catalog":"440","title":"Morphology","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential 400-level; satisfies upper-level req"},
          {"subject":"LING","catalog":"425","title":"Historical Linguistics","credits":3,"is_required":False},
          {"subject":"LING","catalog":"520","title":"Sociolinguistics 2","credits":3,"is_required":False},
          {"subject":"LING","catalog":"550","title":"Computational Linguistics","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Valuable CS crossover; growing field"},
          {"subject":"LING","catalog":"571","title":"Syntax 2","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Continues from LING 371; required for syntax track"},
        ],
      },
    ],
  },

  {
    "program_key": "linguistics_minor",
    "name": "Linguistics – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to the scientific study of human language.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/linguistics/linguistics-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core",
        "credits_needed": 9,
        "courses": [
          {"subject":"LING","catalog":"201","title":"Introduction to Linguistics","credits":3,"is_required":True,"recommended":True},
          {"subject":"LING","catalog":"330","title":"Phonetics","credits":3,"is_required":True},
          {"subject":"LING","catalog":"371","title":"Syntax 1","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "LING Electives",
        "credits_needed": 9,
        "notes": "9 credits of LING courses; at least one at 400-level.",
        "courses": [
          {"subject":"LING","catalog":"331","title":"Phonology 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"355","title":"Language Acquisition 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"360","title":"Introduction to Semantics","credits":3,"is_required":False},
          {"subject":"LING","catalog":"440","title":"Morphology","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":None,"title":"Any upper-level LING course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # HISTORY
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "history_major",
    "name": "History – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "A highly flexible 36-credit program emphasising breadth and depth across diverse "
      "cultures from antiquity to today. Students must satisfy Distribution (Groups A/B/C), "
      "Temporal Breadth (pre-1800 and post-1800), and Level requirements "
      "(max 15 credits at 200-level; min 6 credits at 400/500-level; max 6 cognate credits)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/history-classical-studies/history-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "distribution_A",
        "title": "Distribution – Group A (Canadian / American / European Surveys)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "At least 3 credits from Group A. AP and IB credits do not count toward history program requirements.",
        "courses": [
          {"subject":"HIST","catalog":"202","title":"Survey: Canada to 1867","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Canadian history foundation"},
          {"subject":"HIST","catalog":"203","title":"Survey: Canada since 1867","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Popular survey; great entry point for Canadian history"},
          {"subject":"HIST","catalog":"211","title":"American History to 1865","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"212","title":"Medieval Europe","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"214","title":"Early Modern Europe","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"215","title":"Modern Europe","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Covers WWI, WWII, Cold War — engaging survey"},
          {"subject":"HIST","catalog":"216","title":"Introduction to Russian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"221","title":"United States since 1865","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"226","title":"East Central and Southeastern Europe in 20th Century","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"250","title":"Making Great Britain and Ireland","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "distribution_B",
        "title": "Distribution – Group B (Non-Western / Ancient World History)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "At least 3 credits from Group B.",
        "courses": [
          {"subject":"HIST","catalog":"200","title":"Introduction to African History","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"201","title":"Modern African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"205","title":"Ancient Mediterranean History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"206","title":"Indian Ocean World History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"208","title":"Introduction to East Asian History","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"209","title":"Introduction to South Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"210","title":"Introduction to Latin American History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"218","title":"Modern East Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"275","title":"Ancient Roman History","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "distribution_C",
        "title": "Distribution – Group C (Thematic / Specialized History Topics)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "At least 3 credits from Group C. Note: HIST 299 cannot satisfy Temporal Breadth requirement.",
        "courses": [
          {"subject":"HIST","catalog":"207","title":"Jewish History: 400 B.C.E. to 1000","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"213","title":"World History, 600–2000","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Great global breadth course"},
          {"subject":"HIST","catalog":"219","title":"Jewish History: 1000–2000","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"222","title":"History of Pandemics","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"223","title":"Indigenous Peoples and Empires","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"224","title":"Introduction to the African Diaspora","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"238","title":"Histories of Science","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"240","title":"Modern History of Islamic Movements","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"249","title":"Health and the Healer in Western History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"262","title":"Mediterranean and European Interconnections","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"292","title":"History and the Environment","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"298","title":"Topics in History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"299","title":"The Historian's Craft","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Excellent intro to historical methods — note: cannot satisfy distribution requirement"},
        ],
      },
      {
        "block_key": "temporal_pre1800",
        "title": "Temporal Breadth – Pre-1800",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "At least 3 credits covering the pre-1800 period. The same course may satisfy both a Distribution requirement and a Temporal Breadth requirement.",
        "courses": [
          {"subject":"HIST","catalog":"202","title":"Survey: Canada to 1867","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"205","title":"Ancient Mediterranean History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"207","title":"Jewish History: 400 B.C.E. to 1000","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"208","title":"Introduction to East Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"212","title":"Medieval Europe","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"214","title":"Early Modern Europe","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"275","title":"Ancient Roman History","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "temporal_post1800",
        "title": "Temporal Breadth – Post-1800",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "At least 3 credits covering the post-1800 period.",
        "courses": [
          {"subject":"HIST","catalog":"201","title":"Modern African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"203","title":"Survey: Canada since 1867","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"215","title":"Modern Europe","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"218","title":"Modern East Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"221","title":"United States since 1865","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"240","title":"Modern History of Islamic Movements","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "upper_400",
        "title": "Upper-Level Courses (400/500-level)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "min_credits_400": 6,
        "notes": (
          "Minimum 6 credits at 400- or 500-level. "
          "Maximum 3 credits of HIST 498/499 (independent study) may count toward this requirement."
        ),
        "courses": [
          {"subject":"HIST","catalog":"333","title":"Indigenous Peoples and French","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"317","title":"Themes in Indian Ocean World History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"326","title":"History of the Soviet Union","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"328","title":"Themes in Modern Chinese History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"338","title":"Twentieth-Century China","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"340","title":"History of Modern Egypt","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"309","title":"History of Latin America to 1825","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"498","title":"Independent Research","credits":3,"is_required":False,"recommendation_reason":"Max 3 credits counted toward 400-level requirement"},
          {"subject":"HIST","catalog":"499","title":"Honours Thesis","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "free_hist",
        "title": "Additional HIST or Cognate Electives",
        "block_type": "choose_credits",
        "credits_needed": 15,
        "notes": (
          "Fill remaining credits with HIST or approved cognate courses. "
          "Max 6 cognate credits. Max 15 credits at 200-level total across the program. "
          "Approved cognates: CLAS 303/304/305/345/406; "
          "ISLA 305/315/350/355/410/411/511/516; "
          "JWST 240/245/303/311/312/334/348/365/366/371."
        ),
        "courses": [
          # Approved HIST 300-level electives
          {"subject":"HIST","catalog":"360","title":"Themes in the History of the Americas","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"361","title":"Themes in Modern African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"363","title":"Themes in South Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"366","title":"Themes in Chinese History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"382","title":"Themes in Middle Eastern History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"389","title":"Special Topics in History","credits":3,"is_required":False},
          # Approved cognates (max 6 credits total)
          {"subject":"CLAS","catalog":"303","title":"Greek Art and Archaeology","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"304","title":"Roman Art and Archaeology","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"305","title":"Late Antique Art and Archaeology","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"345","title":"Myth and Society in Greece and Rome","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"406","title":"Seminar in Classical Studies","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"305","title":"Topics in Islamic Studies","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"315","title":"Topics in Islamic History","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"350","title":"Islamic Law","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"355","title":"Sufism: Islamic Mysticism","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"240","title":"Jewish Culture and Civilization","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"245","title":"Jewish Culture and Civilization 2","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"303","title":"Jewish Thought 1","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"311","title":"Hebrew Literature","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"334","title":"Modern Jewish Literature","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"348","title":"Jewish Culture and Society","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"365","title":"Holocaust: History and Representation","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":"366","title":"Holocaust: Representation and Memory","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"371","title":"Contemporary Jewish Issues","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "history_minor",
    "name": "History – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "Introduces students to diverse cultures and societies from antiquity to today. Expandable to a Major Concentration.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/history-classical-studies/history-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "all_hist",
        "title": "HIST Courses",
        "credits_needed": 18,
        "max_credits_200": 6,
        "min_credits_400": 3,
        "notes": "18 credits of HIST or cognate courses; at most 6 at 200-level; at least 3 at 400-level.",
        "courses": [
          {"subject":"HIST","catalog":"203","title":"Survey: Canada since 1867","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"219","title":"Jewish History: 1000–2000","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"221","title":"United States since 1865","credits":3,"is_required":False},
          {"subject":"HIST","catalog":None,"title":"Any HIST course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # ART HISTORY
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "art_history_major",
    "name": "Art History – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "Comprehensive study of visual arts, material culture, and architecture "
      "from antiquity to the present, primarily focusing on Europe and North America."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/art-history-communication-studies/art-history-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "arth_major_methods",
        "title": "Methods and Theory",
        "block_type": "group",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": "3 credits from Methods/Theory courses",
        "notes": "Select 3 credits from the following methods and theory courses.",
        "sort_order": 1,
        "courses": [
          {"subject": "ARTH", "catalog": "302", "title": "Topics in Art Theory",               "credits": 3, "is_required": False},
          {"subject": "ARTH", "catalog": "305", "title": "Methods in Art History",             "credits": 3, "is_required": False},
          {"subject": "ARTH", "catalog": "315", "title": "Topics in Contemporary Art Theory",  "credits": 3, "is_required": False},
          {"subject": "ARTH", "catalog": "339", "title": "Topics in Museum Studies",           "credits": 3, "is_required": False},
          {"subject": "ARTH", "catalog": "357", "title": "Topics in Critical Theory",          "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key": "upper_arth",
        "title": "Upper-Level ARTH Electives",
        "credits_needed": 33,
        "min_credits_400": 3,
        "max_credits_200": 12,
        "notes": "Min 3 credits at 400-level or above (excl. ARTH 490). Max 12 credits at 200-level.",
        "courses": [
          {"subject":"ARTH","catalog":"320","title":"Modern Art","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Very popular; covers Impressionism to Abstract"},
          {"subject":"ARTH","catalog":"325","title":"Contemporary Art","credits":3,"is_required":False,"recommended":True},
          {"subject":"ARTH","catalog":"360","title":"Canadian Art and Architecture","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"400","title":"Advanced Seminar in Art History","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Intensive seminar; great for honours prep"},
          {"subject":"ARTH","catalog":None,"title":"Any ARTH course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "art_history_minor",
    "name": "Art History – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An introduction to diverse artistic traditions from ancient to contemporary times.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/art-history-communication-studies/art-history-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "arth_minor_courses",
        "title": "ARTH Courses",
        "credits_needed": 18,
        "min_credits_400": 3,
        "max_credits_200": 12,
        "notes": "Min 3 credits at 400-level or above (excl. ARTH 490). Max 12 credits at 200-level.",
        "courses": [
          {"subject":"ARTH","catalog":"320","title":"Modern Art","credits":3,"is_required":False,"recommended":True},
          {"subject":"ARTH","catalog":"325","title":"Contemporary Art","credits":3,"is_required":False,"recommended":True},
          {"subject":"ARTH","catalog":"302","title":"Topics in Art Theory","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"305","title":"Methods in Art History","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"400","title":"Advanced Seminar in Art History","credits":3,"is_required":False,"recommended":True},
          {"subject":"ARTH","catalog":None,"title":"Any ARTH course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # ENGLISH – LITERATURE
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "english_literature_major",
    "name": "English – Literature Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "Focuses on close reading, literary history, and theory. "
      "Students develop interpretive skills across multiple periods and genres."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-literature-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required_surveys",
        "title": "Departmental Surveys (Required)",
        "credits_needed": 9,
        "notes": "ENGL 202, ENGL 203, and ENGL 311 are required. Surveys should be taken in the first two terms of the program.",
        "courses": [
          {"subject":"ENGL","catalog":"202","title":"Departmental Survey of English Literature 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required foundation — take in U1 Fall"},
          {"subject":"ENGL","catalog":"203","title":"Departmental Survey of English Literature 2","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required foundation — take in U1 Winter"},
          {"subject":"ENGL","catalog":"311","title":"Poetics","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required for the major — take in U2"},
        ],
      },
      {
        "block_key": "canadian_literature",
        "title": "Canadian Literature (3 credits)",
        "credits_needed": 3,
        "notes": "3 credits from the list of Canadian Literature courses.",
        "courses": [
          {"subject":"ENGL","catalog":"321","title":"Canadian Literature 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Survey of Canadian literary traditions"},
          {"subject":"ENGL","catalog":"322","title":"Canadian Literature 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"323","title":"Canadian Prose Fiction 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"324","title":"Studies in Canadian Fiction","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"326","title":"Studies in a Canadian Author","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"328","title":"Development of Canadian Poetry 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"329","title":"Development of Canadian Poetry 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"331","title":"Theme or Movement: Canadian Literature","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"342","title":"First Nations and Inuit Literature and Media","credits":3,"is_required":False,"recommended":True},
        ],
      },
      {
        "block_key": "theory",
        "title": "Theory, Criticism and Methods (3 credits)",
        "credits_needed": 3,
        "notes": "3 credits from Theory/Criticism/Methods.",
        "courses": [
          {"subject":"ENGL","catalog":"300","title":"Theories of the Text","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Core theory course — take early in U2"},
          {"subject":"ENGL","catalog":"301","title":"Materiality and Sociology of Text","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"360","title":"Literary Criticism","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Required for Honours; excellent critical methods course"},
          {"subject":"ENGL","catalog":"414","title":"Theories of Difference","credits":3,"is_required":False,"recommended":True},
        ],
      },
      {
        "block_key": "period_pre1800",
        "title": "Pre-1800 Literature (6 credits — two areas)",
        "credits_needed": 6,
        "notes": "6 credits from two of these areas: Backgrounds, Old English, Medieval, Renaissance.",
        "courses": [
          {"subject":"ENGL","catalog":"303","title":"Great Writings of Europe 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"304","title":"Great Writings of Europe 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"305","title":"Renaissance English Literature 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"306","title":"Theatre History: Medieval and Early Modern","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"307","title":"Renaissance English Literature 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"308","title":"English Renaissance Drama 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Classic upper-level English survey"},
          {"subject":"ENGL","catalog":"309","title":"Earlier English Renaissance","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"310","title":"Studies in the 17th Century","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"311","title":"Poetics","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"314","title":"Introduction to Old English","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"315","title":"Shakespeare","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"316","title":"Theme or Genre in Medieval Literature","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"317","title":"Middle English","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"349","title":"English Literature and Folklore 1","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "period_1800_1900",
        "title": "Restoration–19th Century (6 credits — two areas)",
        "credits_needed": 6,
        "notes": "6 credits from two of: Restoration, 18th Century, Romantic, Victorian, 19th Century American.",
        "courses": [
          {"subject":"ENGL","catalog":"350","title":"Restoration and 18th C. English Literature 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"351","title":"Restoration and 18th Century Drama","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"352","title":"Earlier 18th Century Novel","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"353","title":"Later Eighteenth Century Novel","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"354","title":"Studies in the 18th Century","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"370","title":"Literature Romantic Period 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"371","title":"Literature Romantic Period 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"374","title":"English Novel: 19th Century 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"375","title":"English Novel: 19th Century 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"376","title":"Victorian Poetry","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"377","title":"Studies in 19th Century Literature 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"378","title":"Studies in 19th Century Literature 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"381","title":"Studies in 19th Century American Literature","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "period_modern",
        "title": "20th Century / Contemporary (3 credits)",
        "credits_needed": 3,
        "notes": "3 credits from Early 20th Century, Modernist, Post-modernist, or Contemporary areas.",
        "courses": [
          {"subject":"ENGL","catalog":"390","title":"Poetry of the 20th Century 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"391","title":"Studies in 20th Century Literature 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"392","title":"A Major Modernist Writer","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"393","title":"A Major English Poet","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"394","title":"The 20th Century Novel 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"395","title":"The 20th Century Novel 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"396","title":"Postcolonial Literature","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"398","title":"Contemporary Women's Fiction","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"399","title":"The 20th Century","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"408","title":"The 20th Century (Seminar)","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "upper_engl",
        "title": "Additional ENGL Electives (6 credits)",
        "credits_needed": 6,
        "notes": "6 additional ENGL credits from Literature, Cultural Studies, or Drama & Theatre options.",
        "courses": [
          {"subject":"ENGL","catalog":"335","title":"Studies in Women Authors","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"344","title":"Studies in Literary Form","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"345","title":"Literature and Science","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"346","title":"Literature and Society","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":"347","title":"Sexuality and Representation","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"348","title":"Popular Literary Forms","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"384","title":"African Literature","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"385","title":"Irish Literature","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"400","title":"Advanced Seminar in Literature 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"400-level seminar — satisfies upper-level requirement"},
          {"subject":"ENGL","catalog":"401","title":"Advanced Seminar in Literature 2","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"402","title":"Studies in Literary Theory","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"340","title":"Studies in 20th Century Literature","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "english_literature_minor",
    "name": "English – Literature Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to English literature across periods and genres.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-literature-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required_surveys",
        "title": "Departmental Surveys",
        "credits_needed": 6,
        "notes": "ENGL 202 and ENGL 203 are the foundational survey courses for the minor.",
        "courses": [
          {"subject":"ENGL","catalog":"202","title":"Departmental Survey of English Literature 1","credits":3,"is_required":True,"recommended":True},
          {"subject":"ENGL","catalog":"203","title":"Departmental Survey of English Literature 2","credits":3,"is_required":True,"recommended":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "ENGL Electives",
        "credits_needed": 12,
        "notes": "At least one course at 300+ level.",
        "courses": [
          {"subject":"ENGL","catalog":"300","title":"Theories of the Text","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":None,"title":"Any ENGL course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # COMMUNICATION STUDIES (Minor only)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "communication_studies_minor",
    "name": "Communication Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "Studies forms of cultural expression and media through critical and theoretical lenses.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/art-history-communication-studies/communication-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Courses",
        "credits_needed": 6,
        "courses": [
          {"subject":"COMS","catalog":"200","title":"Communication Studies: An Introduction","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Start here; covers all COMS fields"},
          {"subject":"COMS","catalog":"210","title":"Mass Communication and Society","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "COMS Electives",
        "credits_needed": 12,
        "notes": "12 credits from COMS 200+ courses; at least one at 300+ level.",
        "courses": [
          {"subject":"COMS","catalog":"306","title":"Media Institutions","credits":3,"is_required":False,"recommended":True},
          {"subject":"COMS","catalog":"310","title":"Studies in Film","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Very popular; no prerequisites"},
          {"subject":"COMS","catalog":"315","title":"Visual Communication","credits":3,"is_required":False},
          {"subject":"COMS","catalog":"320","title":"Race, Media and Society","credits":3,"is_required":False,"recommended":True},
          {"subject":"COMS","catalog":None,"title":"Any COMS course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # PHILOSOPHY
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "philosophy_major",
    "name": "Philosophy – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": "Covers metaphysics, epistemology, ethics, logic, and the history of philosophy.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/philosophy/philosophy-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required_logic",
        "title": "Logic Requirement",
        "credits_needed": 3,
        "courses": [
          {"subject":"PHIL","catalog":"210","title":"Introduction to Deductive Logic 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Take in U1 — opens up most upper-level PHIL courses"},
        ],
      },
      {
        "block_key": "required_ethics",
        "title": "Ethics / Value Theory",
        "credits_needed": 3,
        "courses": [
          {"subject":"PHIL","catalog":"230","title":"Ethics: Theory and Contemporary Issues","credits":3,"is_required":False,"recommended":True,"choose_from_group":"ethics","choose_n_credits":3},
          {"subject":"PHIL","catalog":"241","title":"Ethics","credits":3,"is_required":False,"choose_from_group":"ethics","choose_n_credits":3},
          {"subject":"PHIL","catalog":"271","title":"Bioethics","credits":3,"is_required":False,"choose_from_group":"ethics","choose_n_credits":3},
          {"subject":"PHIL","catalog":"334","title":"Ethical Theory","credits":3,"is_required":False,"choose_from_group":"ethics","choose_n_credits":3},
        ],
      },
      {
        "block_key": "required_epistemology",
        "title": "Epistemology / Metaphysics / Mind",
        "credits_needed": 3,
        "notes": "3 credits from Group E (Metaphysics, Epistemology, Philosophy of Mind, Philosophy of Language).",
        "courses": [
          {"subject":"PHIL","catalog":"201","title":"Introduction to Philosophy 2","credits":3,"is_required":False,"recommended":True,"choose_from_group":"epi_meta","choose_n_credits":3},
          {"subject":"PHIL","catalog":"306","title":"Philosophy of Mind","credits":3,"is_required":False,"choose_from_group":"epi_meta","choose_n_credits":3},
          {"subject":"PHIL","catalog":"415","title":"Philosophy of Language","credits":3,"is_required":False,"choose_from_group":"epi_meta","choose_n_credits":3},
          {"subject":"PHIL","catalog":"419","title":"Epistemology","credits":3,"is_required":False,"choose_from_group":"epi_meta","choose_n_credits":3},
        ],
      },
      {
        "block_key": "history_phil",
        "title": "History of Philosophy",
        "credits_needed": 6,
        "block_type": "choose_credits",
        "notes": (
          "6 credits from Group C (Ancient Philosophy) or Group D (Modern Philosophy), "
          "or 3 credits from each group. "
          "Group C: Ancient and Medieval. Group D: Early Modern through 19th century."
        ),
        "courses": [
          # Group C – Ancient and Medieval Philosophy
          {"subject":"PHIL","catalog":"344","title":"Medieval and Renaissance Political Theory","credits":3,"is_required":False,"choose_from_group":"ancient_med","choose_n_credits":3},
          {"subject":"PHIL","catalog":"345","title":"Greek Political Theory","credits":3,"is_required":False,"recommended":True,"choose_from_group":"ancient_med","choose_n_credits":3},
          {"subject":"PHIL","catalog":"350","title":"History and Philosophy of Ancient Science","credits":3,"is_required":False,"choose_from_group":"ancient_med","choose_n_credits":3},
          {"subject":"PHIL","catalog":"353","title":"The Presocratic Philosophers","credits":3,"is_required":False,"choose_from_group":"ancient_med","choose_n_credits":3},
          {"subject":"PHIL","catalog":"354","title":"Plato","credits":3,"is_required":False,"recommended":True,"choose_from_group":"ancient_med","choose_n_credits":3,"recommendation_reason":"Core ancient texts — foundational for all history of philosophy"},
          {"subject":"PHIL","catalog":"355","title":"Aristotle","credits":3,"is_required":False,"choose_from_group":"ancient_med","choose_n_credits":3},
          {"subject":"PHIL","catalog":"356","title":"Early Medieval Philosophy","credits":3,"is_required":False,"choose_from_group":"ancient_med","choose_n_credits":3},
          # Group D – Modern Philosophy (17th–19th century)
          {"subject":"PHIL","catalog":"360","title":"17th Century Philosophy","credits":3,"is_required":False,"recommended":True,"choose_from_group":"modern","choose_n_credits":3,"recommendation_reason":"Covers Descartes, Leibniz, Spinoza — essential modern rationalism"},
          {"subject":"PHIL","catalog":"361","title":"18th Century Philosophy","credits":3,"is_required":False,"choose_from_group":"modern","choose_n_credits":3},
          {"subject":"PHIL","catalog":"366","title":"18th and Early 19th Century German Philosophy","credits":3,"is_required":False,"choose_from_group":"modern","choose_n_credits":3},
          {"subject":"PHIL","catalog":"444","title":"19th Century Philosophy","credits":3,"is_required":False,"choose_from_group":"modern","choose_n_credits":3},
          {"subject":"PHIL","catalog":"445","title":"Contemporary Continental Philosophy","credits":3,"is_required":False,"choose_from_group":"modern","choose_n_credits":3},
          {"subject":"PHIL","catalog":"465","title":"Topics in the History of Philosophy","credits":3,"is_required":False,"choose_from_group":"modern","choose_n_credits":3},
        ],
      },
      {
        "block_key": "free_phil",
        "title": "Additional PHIL Electives",
        "credits_needed": 21,
        "min_credits_400": 3,
        "notes": "At least 3 credits at 400-level. May include 200-level PHIL courses. Remaining 21 credits from any PHIL courses.",
        "courses": [
          # ── 200-level options ──
          {"subject":"PHIL","catalog":"200","title":"Introduction to Philosophy 1","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"201","title":"Introduction to Philosophy 2","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"240","title":"Introduction to Moral and Political Philosophy","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Accessible intro to normative theory"},
          {"subject":"PHIL","catalog":"242","title":"Critical Thinking","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"244","title":"Engineering Ethics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"271","title":"Bioethics","credits":3,"is_required":False,"recommended":True},
          # ── 300-level options ──
          {"subject":"PHIL","catalog":"306","title":"Philosophy of Mind","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Consciousness, intentionality, mental causation — very engaging"},
          {"subject":"PHIL","catalog":"310","title":"Intermediate Logic","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"327","title":"Topics in African Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"334","title":"Ethical Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"336","title":"Aesthetics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"341","title":"Philosophy of Science 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Highly accessible; bridges science and philosophy"},
          {"subject":"PHIL","catalog":"345","title":"Greek Political Theory","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"348","title":"Philosophy of Law 1","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"349","title":"Environmental Philosophy","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"350","title":"History and Philosophy of Ancient Science","credits":3,"is_required":False},
          # ── 400-level (satisfies upper-level requirement) ──
          {"subject":"PHIL","catalog":"415","title":"Philosophy of Language","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Strong 400-level; bridges logic and language"},
          {"subject":"PHIL","catalog":"416","title":"Topics in Metaphysics and Epistemology","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"419","title":"Epistemology","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"420","title":"Topics in Ethics","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"425","title":"Topics in Political Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"430","title":"Topics in Epistemology and Metaphysics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"435","title":"Topics in Philosophy of Mind","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Advanced seminar; great for cognitive science crossover"},
          {"subject":"PHIL","catalog":"465","title":"Topics in the History of Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"470","title":"Advanced Seminar in Philosophy","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "philosophy_minor",
    "name": "Philosophy – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to philosophical reasoning, ethics, logic, and history of thought.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/philosophy/philosophy-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "PHIL Courses",
        "credits_needed": 18,
        "notes": "18 credits of PHIL courses; at least one at 300+ level.",
        "courses": [
          {"subject":"PHIL","catalog":"210","title":"Introduction to Deductive Logic 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"230","title":"Ethics: Theory and Contemporary Issues","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"354","title":"Plato","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"271","title":"Bioethics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"334","title":"Ethical Theory","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":None,"title":"Any PHIL course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────

]
