"""
McGill Faculty of Arts – Area Studies & Languages: IDS, GSFSJ, Canadian Studies, Classics, Jewish Studies, East Asian Studies, World Islamic, Geography, CS (BA), German, Hispanic, Italian, French, African, Religious Studies, Info Studies, Liberal Arts, European Lit, Latin American Minor
Sub-module of arts_degree_requirements.py
"""

ARTS_AREA_STUDIES = [
  # INTERNATIONAL DEVELOPMENT STUDIES
  # Source: McGill eCalendar 2024-2025
  # https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/ug_arts_isid
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "intl_development_major",
    "name": "International Development Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "An interdisciplinary program examining challenges facing developing countries, "
      "including socio-economic inequalities, governance, peace and conflict, "
      "environment and sustainability. At least 18 of 36 credits must be at the "
      "300 level or above; at least 9 credits must be INTD courses; max 12 credits "
      "in any one discipline other than INTD."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/international-development/international-development-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Courses",
        "block_type": "required",
        "credits_needed": 12,
        "notes": "All four courses are required.",
        "courses": [
          {"subject":"ECON","catalog":"208","title":"Microeconomic Analysis and Applications","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Start here — foundational economics for development"},
          {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core development economics; take after ECON 208"},
          {"subject":"INTD","catalog":"200","title":"Introduction to International Development","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Entry point for the program"},
          {"subject":"INTD","catalog":"497","title":"Advanced Topics in International Development","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Capstone; take in U3"},
        ],
      },
      {
        "block_key": "introductory",
        "title": "Introductory Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "notes": "3 credits from Culture, Populations and Development; 3 credits from Politics, Society and Development.",
        "courses": [
          # Culture, Populations and Development (choose 3 cr)
          {"subject":"ANTH","catalog":"202","title":"Socio-Cultural Anthropology","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":"207","title":"Ethnography Through Film","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"212","title":"Anthropology of Development","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Directly relevant to IDS themes"},
          {"subject":"GEOG","catalog":"216","title":"Geography of the World Economy","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"217","title":"Cities in the Modern World","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"350","title":"Culture and Development","credits":3,"is_required":False},
          # Politics, Society and Development (choose 3 cr)
          {"subject":"POLI","catalog":"227","title":"Introduction to Comparative Politics – Global South","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"243","title":"International Politics of Economic Relations","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"244","title":"International Politics: State Behaviour","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"254","title":"Development and Underdevelopment","credits":3,"is_required":False,"recommended":True},
        ],
      },
      {
        "block_key": "thematic",
        "title": "Thematic Electives",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "notes": (
          "18 credits from the approved thematic elective list spanning African Studies, "
          "Anthropology, Economics, Geography, History, Political Science, Sociology, and others. "
          "At least 9 credits must be INTD courses across the entire program; "
          "max 12 credits in any one discipline other than INTD."
        ),
        "courses": [
          # African Studies
          {"subject":"AFRI","catalog":"200","title":"Introduction to African Studies","credits":3,"is_required":False},
          # Agricultural Economics
          {"subject":"AGEC","catalog":"430","title":"Agriculture, Food and Resource Policy","credits":3,"is_required":False},
          {"subject":"AGEC","catalog":"442","title":"Economics of International Agricultural Development","credits":3,"is_required":False},
          # Agriculture
          {"subject":"AGRI","catalog":"411","title":"Global Issues on Development, Food and Agriculture","credits":3,"is_required":False},
          # Anthropology
          {"subject":"ANTH","catalog":"206","title":"Environment and Culture","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"209","title":"Anthropology of Religion","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"214","title":"Violence, Warfare, Culture","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"222","title":"Legal Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"227","title":"Medical Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"302","title":"New Horizons in Medical Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"308","title":"Political Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"318","title":"Globalization and Religion","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"322","title":"Social Change in Modern Africa","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"326","title":"Anthropology of Latin America","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"327","title":"Anthropology of South Asia","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"338","title":"Indigenous Studies of Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"339","title":"Ecological Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"418","title":"Environment and Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":"422","title":"Contemporary Latin American Culture and Society","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"512","title":"Political Ecology","credits":3,"is_required":False},
          # Canadian Studies
          {"subject":"CANS","catalog":"315","title":"Indigenous Art and Culture","credits":3,"is_required":False},
          # East Asian Studies
          {"subject":"EAST","catalog":"211","title":"Introduction: East Asian Culture – China","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"213","title":"Introduction: East Asian Culture – Korea","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"388","title":"Asian Migrations and Diasporas","credits":3,"is_required":False},
          # Economics
          {"subject":"ECON","catalog":"205","title":"An Introduction to Political Economy","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"209","title":"Macroeconomic Analysis and Applications","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"223","title":"Political Economy of Trade Policy","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"314","title":"Economic Development 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"326","title":"Ecological Economics","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"336","title":"The Chinese Economy","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"347","title":"Economics of Climate Change","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"411","title":"Economic Development: A World Area","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"416","title":"Topics in Economic Development 2","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"473","title":"Income Distribution","credits":3,"is_required":False},
          # English
          {"subject":"ENGL","catalog":"290","title":"Postcolonial and World Literatures in English","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"421","title":"African Literature","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"440","title":"First Nations and Inuit Literature and Media","credits":3,"is_required":False},
          # Geography
          {"subject":"GEOG","catalog":"221","title":"Environment and Health","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"302","title":"Environmental Management 1","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"303","title":"Health Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"310","title":"Development and Livelihoods","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"311","title":"Economic Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"360","title":"Analyzing Sustainability","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"403","title":"Global Health and Environmental Change","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"406","title":"Human Dimensions of Climate Change","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"408","title":"Geography of Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"410","title":"Geography of Underdevelopment: Current Problems","credits":3,"is_required":False},
          # History
          {"subject":"HIST","catalog":"200","title":"Introduction to African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"201","title":"Modern African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"206","title":"Indian Ocean World History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"208","title":"Introduction to East Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"209","title":"Introduction to South Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"213","title":"World History, 600–2000","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"309","title":"History of Latin America to 1825","credits":3,"is_required":False},
          # INTD courses
          {"subject":"INTD","catalog":"250","title":"Topics in International Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"INTD","catalog":"350","title":"Culture and Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"INTD","catalog":"352","title":"Topics in International Development 2","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"354","title":"Topics in International Development 3","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"356","title":"Topics in International Development 4","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"358","title":"Topics in International Development 5","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"360","title":"Topics in International Development 6","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"397","title":"Field Studies in International Development 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Experiential learning — highly recommended"},
          {"subject":"INTD","catalog":"398","title":"Field Studies in International Development 2","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"490","title":"Topics in International Development 7","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"491","title":"Topics in International Development 8","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"499","title":"Independent Research in International Development","credits":3,"is_required":False},
          # Political Science
          {"subject":"POLI","catalog":"318","title":"Comparative Local Government","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"340","title":"Comparative Politics of the Middle East","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"347","title":"Arab-Israel Conflict, Crisis, Peace","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"418","title":"Global Environment and World Politics","credits":3,"is_required":False},
          # Sociology
          {"subject":"SOCI","catalog":"335","title":"Environmental Sociology","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"340","title":"Sociology of Health and Illness","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"360","title":"International Migration","credits":3,"is_required":False,"recommended":True},
        ],
      },
    ],
  },

  {
    "program_key": "intl_development_minor",
    "name": "International Development Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An 18-credit interdisciplinary introduction to global development issues. "
      "At least 9 of the 18 credits must be at the 300 level or above."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/international-development/international-development-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Courses",
        "block_type": "required",
        "credits_needed": 9,
        "notes": "All three courses are required.",
        "courses": [
          {"subject":"ECON","catalog":"208","title":"Microeconomic Analysis and Applications","credits":3,"is_required":True,"recommended":True},
          {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":True,"recommended":True},
          {"subject":"INTD","catalog":"200","title":"Introduction to International Development","credits":3,"is_required":True,"recommended":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "Complementary Electives",
        "block_type": "choose_credits",
        "credits_needed": 9,
        "notes": (
          "9 credits from the approved IDS elective list. At least 9 of the 18 total "
          "credits must be at the 300 level or above. Students may count either HIST 339 "
          "or POLI 347 toward requirements, but not both."
        ),
        "courses": [
          # African Studies
          {"subject":"AFRI","catalog":"200","title":"Introduction to African Studies","credits":3,"is_required":False},
          # Agricultural Economics
          {"subject":"AGEC","catalog":"430","title":"Agriculture, Food and Resource Policy","credits":3,"is_required":False},
          {"subject":"AGEC","catalog":"442","title":"Economics of International Agricultural Development","credits":3,"is_required":False},
          # Agriculture
          {"subject":"AGRI","catalog":"411","title":"Global Issues on Development, Food and Agriculture","credits":3,"is_required":False},
          # Anthropology
          {"subject":"ANTH","catalog":"202","title":"Socio-Cultural Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"212","title":"Anthropology of Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":"302","title":"New Horizons in Medical Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"322","title":"Social Change in Modern Africa","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"326","title":"Anthropology of Latin America","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"418","title":"Environment and Development","credits":3,"is_required":False,"recommended":True},
          # Economics
          {"subject":"ECON","catalog":"209","title":"Macroeconomic Analysis and Applications","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"314","title":"Economic Development 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"347","title":"Economics of Climate Change","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"411","title":"Economic Development: A World Area","credits":3,"is_required":False},
          # Geography
          {"subject":"GEOG","catalog":"216","title":"Geography of the World Economy","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"310","title":"Development and Livelihoods","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"408","title":"Geography of Development","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"410","title":"Geography of Underdevelopment: Current Problems","credits":3,"is_required":False},
          # History
          {"subject":"HIST","catalog":"200","title":"Introduction to African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"201","title":"Modern African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"209","title":"Introduction to South Asian History","credits":3,"is_required":False},
          # INTD
          {"subject":"INTD","catalog":"250","title":"Topics in International Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"INTD","catalog":"350","title":"Culture and Development","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"397","title":"Field Studies in International Development 1","credits":3,"is_required":False},
          # Political Science
          {"subject":"POLI","catalog":"227","title":"Introduction to Comparative Politics – Global South","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"340","title":"Comparative Politics of the Middle East","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"347","title":"Arab-Israel Conflict, Crisis, Peace","credits":3,"is_required":False},
          # Sociology
          {"subject":"SOCI","catalog":"254","title":"Development and Underdevelopment","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"360","title":"International Migration","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # GENDER, SEXUALITY, FEMINIST AND SOCIAL JUSTICE STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "gsfsj_major",
    "name": "Gender, Sexuality, Feminist and Social Justice Studies – Major",
    "program_type": "major",
    "total_credits": 36,
    "description": "Interdisciplinary program examining gender, sexuality, race, and power in society through critical feminist frameworks.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/gender-sexuality-feminist-studies/gender-sexuality-feminist-social-justice-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core Courses",
        "credits_needed": 9,
        "courses": [
          {"subject":"GSFS","catalog":"200","title":"Introduction to Gender and Feminist Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Start here; foundational concepts"},
          {"subject":"GSFS","catalog":"300","title":"Feminist Theory","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core theory; take in U2"},
          {"subject":"GSFS","catalog":"400","title":"Advanced Seminar in GSFS","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Capstone seminar; integrates program"},
        ],
      },
      {
        "block_key": "thematic",
        "title": "Thematic and Intersectional Courses",
        "credits_needed": 15,
        "notes": "Courses must span at least two thematic areas (e.g., race & gender, sexuality & law, labour & environment).",
        "courses": [
          {"subject":"GSFS","catalog":"250","title":"Gender, Sexuality and the Body","credits":3,"is_required":False,"recommended":True},
          {"subject":"GSFS","catalog":"260","title":"Race, Racism and Feminist Thought","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Critical intersectional lens; highly relevant"},
          {"subject":"GSFS","catalog":"310","title":"Queer Theory and Politics","credits":3,"is_required":False,"recommended":True},
          {"subject":"GSFS","catalog":"315","title":"Feminist Political Economy","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":"320","title":"Gender and the Law","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":"325","title":"Gender and Colonialism","credits":3,"is_required":False,"recommended":True},
          {"subject":"GSFS","catalog":"350","title":"Reproductive Politics","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "electives",
        "title": "Additional GSFS Electives",
        "credits_needed": 12,
        "notes": "12 credits from GSFS or approved cognate courses.",
        "courses": [
          {"subject":"GSFS","catalog":None,"title":"Any GSFS course 200-level or above","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"234","title":"Sociology of Gender","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Strong cognate from Sociology"},
          {"subject":"ANTH","catalog":"357","title":"Gender and Culture","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "gsfsj_minor",
    "name": "Gender, Sexuality, Feminist and Social Justice Studies – Minor",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to feminist and social justice theory and practice.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/gender-sexuality-feminist-studies/gender-sexuality-feminist-social-justice-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core",
        "credits_needed": 3,
        "courses": [
          {"subject":"GSFS","catalog":"200","title":"Introduction to Gender and Feminist Studies","credits":3,"is_required":True,"recommended":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "GSFS Electives",
        "credits_needed": 15,
        "notes": "At least one course at 300+ level.",
        "courses": [
          {"subject":"GSFS","catalog":"250","title":"Gender, Sexuality and the Body","credits":3,"is_required":False,"recommended":True},
          {"subject":"GSFS","catalog":"300","title":"Feminist Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"GSFS","catalog":"310","title":"Queer Theory and Politics","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":None,"title":"Any GSFS course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # CANADIAN STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "canadian_studies_major",
    "name": "Canadian Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": "Interdisciplinary program examining Canadian institutions, public affairs, culture, and social issues through humanities and social sciences perspectives.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/institute-study/canadian-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core",
        "credits_needed": 6,
        "courses": [
          {"subject":"CANS","catalog":"200","title":"Introduction to Canadian Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Gateway course; take in U1"},
          {"subject":"CANS","catalog":"300","title":"Topics in Canadian Public Affairs","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "thematic",
        "title": "Thematic Breadth",
        "credits_needed": 18,
        "notes": "Courses must span at least two of the following streams: History & Culture, Politics & Society, Language & Identity.",
        "courses": [
          {"subject":"CANS","catalog":"310","title":"Canadian Cultures: Context and Issues","credits":3,"is_required":False,"recommended":True},
          {"subject":"CANS","catalog":"315","title":"Quebec and Canada","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential for Montreal context"},
          {"subject":"CANS","catalog":"320","title":"Gender and Nationalism in Canada","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"203","title":"Canada: Confederation to the Present","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"221","title":"Quebec Politics","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"212","title":"Canadian Government and Politics","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"430","title":"Canadian Society","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "upper_capstone",
        "title": "Upper-Level and Capstone",
        "credits_needed": 12,
        "min_credits_400": 6,
        "courses": [
          {"subject":"CANS","catalog":"400","title":"Advanced Seminar in Canadian Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Capstone synthesis seminar"},
          {"subject":"CANS","catalog":"490","title":"Internship in Canadian Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Gain real-world policy/cultural experience"},
          {"subject":"CANS","catalog":None,"title":"Any CANS course at 400-level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "canadian_studies_minor",
    "name": "Canadian Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit multidisciplinary introduction to Canada's key institutions and social debates.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/institute-study/canadian-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "CANS and Cognate Courses",
        "credits_needed": 18,
        "notes": "CANS 200 required. At least one upper-level course.",
        "courses": [
          {"subject":"CANS","catalog":"200","title":"Introduction to Canadian Studies","credits":3,"is_required":True,"recommended":True},
          {"subject":"CANS","catalog":"310","title":"Canadian Cultures: Context and Issues","credits":3,"is_required":False,"recommended":True},
          {"subject":"CANS","catalog":"315","title":"Quebec and Canada","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"203","title":"Canada: Confederation to the Present","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"212","title":"Canadian Government and Politics","credits":3,"is_required":False},
          {"subject":"CANS","catalog":None,"title":"Any CANS course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # CLASSICS
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "classics_major",
    "name": "Classics – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": "In-depth study of ancient Greece and Rome in two streams: Classical Languages and Classical Studies.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/history-classical-studies/classics-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "classical_languages",
        "title": "Classical Languages (Greek or Latin)",
        "credits_needed": 12,
        "notes": "At least 12 credits in ancient Greek (GREK) or Latin (LATI) or both.",
        "courses": [
          {"subject":"LATI","catalog":"201","title":"Introductory Latin 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Start Latin in U1; opens extensive course list"},
          {"subject":"LATI","catalog":"202","title":"Introductory Latin 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"LATI","catalog":"310","title":"Intermediate Latin: Prose","credits":3,"is_required":False},
          {"subject":"GREK","catalog":"201","title":"Introductory Greek 1","credits":3,"is_required":False},
          {"subject":"GREK","catalog":"202","title":"Introductory Greek 2","credits":3,"is_required":False},
          {"subject":"GREK","catalog":"310","title":"Intermediate Greek: Prose","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "classical_studies",
        "title": "Classical Studies Courses",
        "credits_needed": 12,
        "notes": "Ancient history, literature, and culture courses.",
        "courses": [
          {"subject":"CLAS","catalog":"200","title":"Introduction to Classical Studies","credits":3,"is_required":False,"recommended":True},
          {"subject":"CLAS","catalog":"210","title":"Greek and Roman Mythology","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Popular entry course; no prerequisites"},
          {"subject":"CLAS","catalog":"230","title":"History of Ancient Greece","credits":3,"is_required":False,"recommended":True},
          {"subject":"CLAS","catalog":"235","title":"History of Ancient Rome","credits":3,"is_required":False,"recommended":True},
          {"subject":"CLAS","catalog":"310","title":"Classical Literature in Translation","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "upper_clas",
        "title": "Upper-Level Classics Courses",
        "credits_needed": 12,
        "min_credits_400": 6,
        "courses": [
          {"subject":"CLAS","catalog":"400","title":"Advanced Seminar in Classical Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Seminar-style; great for research track"},
          {"subject":"CLAS","catalog":None,"title":"Any CLAS or language course at 400+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "classics_minor",
    "name": "Classics – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "Introduction to the linguistic, historical, and cultural dimensions of Greece and Rome.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/history-classical-studies/classics-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "CLAS / Language Courses",
        "credits_needed": 18,
        "notes": "Mix of language (GREK/LATI) and content (CLAS) courses.",
        "courses": [
          {"subject":"CLAS","catalog":"210","title":"Greek and Roman Mythology","credits":3,"is_required":False,"recommended":True},
          {"subject":"CLAS","catalog":"230","title":"History of Ancient Greece","credits":3,"is_required":False,"recommended":True},
          {"subject":"LATI","catalog":"201","title":"Introductory Latin 1","credits":3,"is_required":False},
          {"subject":"GREK","catalog":"201","title":"Introductory Greek 1","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":None,"title":"Any CLAS course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # JEWISH STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "jewish_studies_major",
    "name": "Jewish Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": "Interdisciplinary study of Jewish history, culture, religion, literature, and thought from antiquity to the present.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/jewish-studies/jewish-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core",
        "credits_needed": 9,
        "courses": [
          {"subject":"JWST","catalog":"200","title":"Introduction to Jewish Studies","credits":3,"is_required":True,"recommended":True},
          {"subject":"JWST","catalog":"210","title":"Introduction to the Hebrew Bible","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Foundational text study"},
          {"subject":"JWST","catalog":"215","title":"Introduction to Rabbinic Literature","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "Jewish Studies Electives",
        "credits_needed": 27,
        "min_credits_400": 6,
        "max_credits_200": 9,
        "notes": "27 credits across history, language, literature, and religion tracks.",
        "courses": [
          {"subject":"JWST","catalog":"220","title":"History of the Jewish People 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":"221","title":"History of the Jewish People 2","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"261","title":"History of Jewish Philosophy","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":"310","title":"Modern Jewish History","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":"350","title":"Holocaust: History and Representation","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Important and deeply engaging course"},
          {"subject":"JWST","catalog":"400","title":"Advanced Seminar in Jewish Studies","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":None,"title":"Any JWST course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "jewish_studies_minor",
    "name": "Jewish Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to Jewish history, religion, and culture.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/jewish-studies/jewish-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "JWST Courses",
        "credits_needed": 18,
        "notes": "JWST 200 recommended as first course. At least one course at 300+ level.",
        "courses": [
          {"subject":"JWST","catalog":"200","title":"Introduction to Jewish Studies","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":"210","title":"Introduction to the Hebrew Bible","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":"261","title":"History of Jewish Philosophy","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"350","title":"Holocaust: History and Representation","credits":3,"is_required":False,"recommended":True},
          {"subject":"JWST","catalog":None,"title":"Any JWST course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # EAST ASIAN STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "east_asian_studies_major",
    "name": "East Asian Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": "In-depth training in humanistic studies of East Asia including language, society, literature, history, media, religion, politics, and art.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/east-asian-studies/east-asian-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "core_surveys",
        "title": "Core Survey Courses",
        "credits_needed": 9,
        "notes": "Three regional survey courses (China, Japan, Korea).",
        "courses": [
          {"subject":"EAST","catalog":"211","title":"Introduction to Chinese Culture","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Best first course for East Asian Studies"},
          {"subject":"EAST","catalog":"213","title":"Introduction to Japanese Culture","credits":3,"is_required":True},
          {"subject":"EAST","catalog":"215","title":"Introduction to Korean Culture","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "language",
        "title": "Language Courses",
        "credits_needed": 9,
        "notes": "At least 9 credits of East Asian language (Chinese/Japanese/Korean).",
        "courses": [
          {"subject":"CHIN","catalog":"201","title":"Mandarin Chinese 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Most widely spoken; great career value"},
          {"subject":"CHIN","catalog":"202","title":"Mandarin Chinese 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"JAPN","catalog":"201","title":"Japanese 1","credits":3,"is_required":False},
          {"subject":"JAPN","catalog":"202","title":"Japanese 2","credits":3,"is_required":False},
          {"subject":"KORE","catalog":"201","title":"Korean 1","credits":3,"is_required":False},
          {"subject":"KORE","catalog":"202","title":"Korean 2","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "upper_east",
        "title": "Upper-Level EAST Courses",
        "credits_needed": 18,
        "min_credits_400": 6,
        "notes": "At least 6 credits at 400-level.",
        "courses": [
          {"subject":"EAST","catalog":"310","title":"Classical Chinese Literature","credits":3,"is_required":False,"recommended":True},
          {"subject":"EAST","catalog":"330","title":"Modern Chinese Literature","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"340","title":"Japanese Cinema","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Very popular; no language prereq required"},
          {"subject":"EAST","catalog":"350","title":"Gender and Sexuality in Chinese Literature","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"400","title":"Advanced Topics in East Asian Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Seminar; good for research track"},
          {"subject":"EAST","catalog":None,"title":"Any EAST course at 400+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # ISLAMIC STUDIES / WORLD ISLAMIC AND MIDDLE EAST STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "world_islamic_mideast_major",
    "name": "World Islamic and Middle East Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": "Interdisciplinary study of Islam, Islamic civilization, and Middle Eastern societies from history, literature, politics, and theology perspectives.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/world-islamic-middle-east-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core Courses",
        "credits_needed": 12,
        "courses": [
          {"subject":"ISLA","catalog":"200","title":"Introduction to Islam","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Foundational overview — take in U1"},
          {"subject":"ISLA","catalog":"205","title":"Introduction to Islamic Civilization","credits":3,"is_required":True,"recommended":True},
          {"subject":"HIST","catalog":"241","title":"Introduction to Islamic History","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"300","title":"Islamic Texts and Traditions","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "electives",
        "title": "Thematic Electives",
        "credits_needed": 18,
        "min_credits_400": 6,
        "courses": [
          {"subject":"ISLA","catalog":"210","title":"The Quran and Its Interpretation","credits":3,"is_required":False,"recommended":True},
          {"subject":"ISLA","catalog":"310","title":"Islamic Law","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Critical for law/policy track"},
          {"subject":"ISLA","catalog":"315","title":"Islam and Gender","credits":3,"is_required":False,"recommended":True},
          {"subject":"ISLA","catalog":"320","title":"Sufism","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"330","title":"Political Islam","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"315","title":"Politics of the Middle East","credits":3,"is_required":False,"recommended":True},
          {"subject":"ISLA","catalog":"400","title":"Advanced Seminar in Islamic Studies","credits":3,"is_required":False,"recommended":True},
          {"subject":"ISLA","catalog":None,"title":"Any ISLA course at 400+ level","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "language",
        "title": "Language (Optional but recommended)",
        "credits_needed": 6,
        "notes": "Arabic or other relevant language credits are strongly recommended.",
        "courses": [
          {"subject":"ARBC","catalog":"210","title":"Introductory Arabic 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Opens primary sources; highly valuable for the field"},
          {"subject":"ARBC","catalog":"220","title":"Introductory Arabic 2","credits":3,"is_required":False,"recommended":True},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # GEOGRAPHY
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "geography_major",
    "name": "Geography – Major Concentration",
    "program_type": "major",
    "total_credits": 37,
    "description": (
      "A 37-credit program examining spatial patterns of physical and human environments, "
      "emphasising GIS, analytical, and fieldwork methods. "
      "Minimum 3 credits at 400-level or above."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/geography-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Courses",
        "block_type": "required",
        "credits_needed": 7,
        "notes": "All three courses required. GEOG 290 is a 1-credit fall excursion; fee applies.",
        "courses": [
          {"subject":"GEOG","catalog":"201","title":"Introductory Geo-Information Science","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"GIS foundations; take in U1"},
          {"subject":"GEOG","catalog":"216","title":"Geography of the World Economy","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core human geography survey"},
          {"subject":"GEOG","catalog":"290","title":"Local Geographical Excursion","credits":1,"is_required":True,"recommended":True,"recommendation_reason":"Mandatory 3-day fall field excursion; open to first-year Geography students only"},
        ],
      },
      {
        "block_key": "physical",
        "title": "Physical Geography",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "Choose one course from Physical Geography.",
        "courses": [
          {"subject":"GEOG","catalog":"203","title":"Environmental Systems","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"272","title":"Earth's Changing Surface","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "statistics",
        "title": "Statistics",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "Choose one statistics course. Credit restrictions apply across statistics courses.",
        "courses": [
          {"subject":"BIOL","catalog":"373","title":"Biometry","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"202","title":"Statistics and Spatial Analysis","credits":3,"is_required":False,"recommended":True},
          {"subject":"MATH","catalog":"203","title":"Principles of Statistics 1","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"204","title":"Introduction to Psychological Statistics","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"350","title":"Statistics in Social Research","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "field",
        "title": "Field Courses",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "Choose one field course. Some courses have additional fees.",
        "courses": [
          {"subject":"GEOG","catalog":"425","title":"Southeast Asia Urban Field Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Experiential field study; additional fee applies"},
          {"subject":"GEOG","catalog":"494","title":"Urban Field Studies","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"495","title":"Field Studies – Physical Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"496","title":"Geographical Excursion","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"499","title":"Subarctic Field Studies","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "analysis",
        "title": "Analysis and Methodology",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "Choose one analysis/methodology course.",
        "courses": [
          {"subject":"GEOG","catalog":"308","title":"Remote Sensing for Earth Observation","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"314","title":"Geospatial Analysis","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"333","title":"Introduction to Programming for Spatial Sciences","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Programming skills for spatial analysis"},
          {"subject":"GEOG","catalog":"351","title":"Quantitative Methods","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"414","title":"Advanced Geospatial Analysis","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"506","title":"Advanced Geographic Information Science","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"512","title":"Advanced Quantitative Methods in Social Field Research","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "electives",
        "title": "Geography Electives",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "min_credits_400": 3,
        "notes": "18 credits from GEOG courses (excluding GEOG 200 and GEOG 205). Minimum 3 credits at 400-level or above.",
        "courses": [
          {"subject":"GEOG","catalog":"210","title":"Introduction to Geographic Information Science","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"217","title":"Cities in the Modern World","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"221","title":"Environment and Health","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"302","title":"Environmental Management 1","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"303","title":"Health Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"310","title":"Development and Livelihoods","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"311","title":"Economic Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"325","title":"New Master-Planned Cities","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"360","title":"Analyzing Sustainability","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"403","title":"Global Health and Environmental Change","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"406","title":"Human Dimensions of Climate Change","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"408","title":"Geography of Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"410","title":"Geography of Underdevelopment: Current Problems","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "geography_minor",
    "name": "Geography – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to physical and human geography.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/geography-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "GEOG Courses",
        "credits_needed": 18,
        "notes": "At least one course at 300+ level.",
        "courses": [
          {"subject":"GEOG","catalog":"200","title":"Environmental Systems","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"202","title":"Quantitative Methods in Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"320","title":"Urban Geography","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"303","title":"Environmental Change","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":None,"title":"Any GEOG course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # COMPUTER SCIENCE (Arts)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "computer_science_arts_major",
    "name": "Computer Science – Major Concentration (B.A.)",
    "program_type": "major",
    "total_credits": 36,
    "description": "B.A. Computer Science focusing on software development, algorithms, and computing theory. Requires MATH 133, 140, and 141 as prerequisites before starting.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/computer-science/computer-science-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "required_core",
        "title": "Required Courses",
        "credits_needed": 18,
        "notes": "MATH 133 Linear Algebra, MATH 140 Calculus 1, and MATH 141 Calculus 2 (or equivalents) should be completed prior to taking courses in this program.",
        "courses": [
          {"subject":"COMP","catalog":"202","title":"Foundations of Programming","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Take in U1 Fall — gateway to all CS courses"},
          {"subject":"COMP","catalog":"206","title":"Introduction to Software Systems","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Systems programming fundamentals; take in U1"},
          {"subject":"COMP","catalog":"250","title":"Introduction to Computer Science","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core data structures and algorithms; take after COMP 202"},
          {"subject":"COMP","catalog":"251","title":"Algorithms and Data Structures","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Essential algorithms course; take after COMP 250"},
          {"subject":"COMP","catalog":"273","title":"Introduction to Computer Systems","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Computer organization and systems; pairs with COMP 206"},
          {"subject":"MATH","catalog":"240","title":"Discrete Structures","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required math foundation for CS theory"},
        ],
      },
      {
        "block_key": "comp_group_a",
        "title": "Complementary – Group A (Math)",
        "credits_needed": 3,
        "notes": "3 credits from Group A.",
        "courses": [
          {"subject":"MATH","catalog":"222","title":"Calculus 3","credits":3,"is_required":False,"choose_from_group":"group_a","choose_n_credits":3,"recommended":True,"recommendation_reason":"Multivariable calculus — useful for ML/AI tracks"},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False,"choose_from_group":"group_a","choose_n_credits":3,"recommended":True,"recommendation_reason":"Essential for machine learning and statistics"},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":False,"choose_from_group":"group_a","choose_n_credits":3},
        ],
      },
      {
        "block_key": "comp_group_b",
        "title": "Complementary – Group B (Math)",
        "credits_needed": 3,
        "notes": "3 credits from Group B.",
        "courses": [
          {"subject":"MATH","catalog":"223","title":"Linear Algebra","credits":3,"is_required":False,"choose_from_group":"group_b","choose_n_credits":3,"recommended":True,"recommendation_reason":"Linear algebra for ML, graphics, and numerical methods"},
          {"subject":"MATH","catalog":"318","title":"Mathematical Logic","credits":3,"is_required":False,"choose_from_group":"group_b","choose_n_credits":3},
          {"subject":"MATH","catalog":"340","title":"Discrete Mathematics","credits":3,"is_required":False,"choose_from_group":"group_b","choose_n_credits":3},
        ],
      },
      {
        "block_key": "comp_group_c",
        "title": "Complementary – Group C (Theory)",
        "credits_needed": 3,
        "notes": "3 credits from Group C.",
        "courses": [
          {"subject":"COMP","catalog":"330","title":"Theory of Computation","credits":3,"is_required":False,"choose_from_group":"group_c","choose_n_credits":3,"recommended":True,"recommendation_reason":"Automata, grammars, and computability theory"},
          {"subject":"COMP","catalog":"350","title":"Numerical Computing","credits":3,"is_required":False,"choose_from_group":"group_c","choose_n_credits":3},
          {"subject":"COMP","catalog":"360","title":"Algorithm Design","credits":3,"is_required":False,"choose_from_group":"group_c","choose_n_credits":3,"recommended":True,"recommendation_reason":"Advanced algorithm design and analysis"},
        ],
      },
      {
        "block_key": "comp_group_d",
        "title": "Complementary – Group D (Systems/SE)",
        "credits_needed": 3,
        "notes": "3 credits from Group D.",
        "courses": [
          {"subject":"COMP","catalog":"302","title":"Programming Languages and Paradigms","credits":3,"is_required":False,"choose_from_group":"group_d","choose_n_credits":3,"recommended":True,"recommendation_reason":"Functional and logic programming paradigms"},
          {"subject":"COMP","catalog":"303","title":"Software Design","credits":3,"is_required":False,"choose_from_group":"group_d","choose_n_credits":3},
        ],
      },
      {
        "block_key": "comp_electives",
        "title": "Complementary – COMP 300+ Electives",
        "credits_needed": 6,
        "min_level": 300,
        "notes": "An additional 3 credits from Group A or B, plus remaining credits from COMP 230 or COMP 300-level or above (except COMP 396).",
        "courses": [
          {"subject":"COMP","catalog":"230","title":"Logic and Computability","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Great for theory-focused students; pairs with COMP 330"},
          {"subject":"COMP","catalog":"307","title":"Introduction to Web Development","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Highly practical; great for portfolio projects"},
          {"subject":"COMP","catalog":"321","title":"Introduction to Software Engineering","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Software process and design patterns"},
          {"subject":"COMP","catalog":"400","title":"Topics in Computing Science","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"409","title":"Concurrent Programming","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"417","title":"Computer Networks","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"421","title":"Programming Languages","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"424","title":"Artificial Intelligence","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Flagship AI course; very popular at McGill"},
          {"subject":"COMP","catalog":"451","title":"Algorithms and Bioinformatics","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"462","title":"Combinatorial Optimization","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Top course for data science/ML track"},
          {"subject":"COMP","catalog":"566","title":"Discrete Optimization","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "computer_science_arts_minor",
    "name": "Computer Science – Minor Concentration (B.A.)",
    "program_type": "minor",
    "total_credits": 18,
    "description": "An 18-credit introduction to programming and computing for non-CS majors.",
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/computer-science/computer-science-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Core",
        "credits_needed": 9,
        "courses": [
          {"subject":"COMP","catalog":"202","title":"Foundations of Programming","credits":3,"is_required":True,"recommended":True},
          {"subject":"COMP","catalog":"250","title":"Introduction to Computer Science","credits":3,"is_required":True,"recommended":True},
          {"subject":"COMP","catalog":"206","title":"Introduction to Software Systems","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "upper",
        "title": "Upper-Level COMP Electives",
        "credits_needed": 9,
        "notes": "9 credits from COMP 300+ courses.",
        "courses": [
          {"subject":"COMP","catalog":"307","title":"Introduction to Web Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"COMP","catalog":"303","title":"Introduction to Operating Systems","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"424","title":"Artificial Intelligence","credits":3,"is_required":False,"recommended":True},
          {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":3,"is_required":False,"recommended":True},
          {"subject":"COMP","catalog":None,"title":"Any COMP course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },



  # ──────────────────────────────────────────────────────────────────
  # COMPUTER SCIENCE – SUPPLEMENTARY MINOR (B.A.)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "supplemental_computer_science_minor",
    "name": "Computer Science – Supplementary Minor Concentration (B.A.)",
    "program_type": "minor",
    "faculty": "Faculty of Arts",
    "total_credits": 18,
    "description": (
      "Exclusively available to students enrolled in the Major Concentration in Computer Science "
      "or Software Engineering (Faculty of Arts). Requires 18 credits from COMP courses at the "
      "300 level or above (excluding COMP 364 and COMP 396), with up to 3 credits from approved "
      "MATH courses. There may be no overlap in credits between this Supplementary Minor and the "
      "paired Major Concentration. Course selection must receive approval from an Academic Adviser "
      "in the School of Computer Science."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/computer-science/computer-science-supplementary-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "supp_cs_comp_upper",
        "title": "COMP 300+ Electives",
        "block_type": "choose_credits",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name": None,
        "notes": "15 credits from COMP courses at the 300 level or above. COMP 364 and COMP 396 are excluded. No credit overlap with paired CS or Software Engineering Major. Adviser approval required.",
        "sort_order": 1,
        "courses": [
          {"subject":"COMP","catalog":"302","title":"Programming Languages and Paradigms","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Functional and logic programming; pairs well with upper-year theory"},
          {"subject":"COMP","catalog":"303","title":"Software Design","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Software architecture and design patterns"},
          {"subject":"COMP","catalog":"307","title":"Introduction to Web Development","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Highly practical; great for building portfolio projects"},
          {"subject":"COMP","catalog":"308","title":"Web Development with JavaScript","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"310","title":"Operating Systems","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"320","title":"Introduction to Computer Graphics","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"321","title":"Introduction to Software Engineering","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"330","title":"Theory of Computation","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Automata, grammars, and computability — core CS theory"},
          {"subject":"COMP","catalog":"350","title":"Numerical Computing","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"360","title":"Algorithm Design","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Advanced algorithm techniques; great prep for technical interviews"},
          {"subject":"COMP","catalog":"400","title":"Topics in Computing Science","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"409","title":"Concurrent Programming","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"417","title":"Computer Networks","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"421","title":"Programming Languages","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"424","title":"Artificial Intelligence","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"McGill's flagship AI course; excellent for CS/AI track"},
          {"subject":"COMP","catalog":"451","title":"Algorithms and Bioinformatics","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"462","title":"Combinatorial Optimization","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"489","title":"Reinforcement Learning","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Top ML course; highly valued for industry and research"},
          {"subject":"COMP","catalog":"558","title":"Fundamentals of Visual Computing","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"566","title":"Discrete Optimization","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"579","title":"Heuristic Search","credits":3,"is_required":False},
          {"subject":"COMP","catalog":"599","title":"Master's Thesis Research 1","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "supp_cs_math_opt",
        "title": "Optional MATH Substitution (max 3 credits)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "Up to 3 of the 18 required credits may come from the approved MATH list below instead of COMP 300+.",
        "sort_order": 2,
        "courses": [
          {"subject":"MATH","catalog":"223","title":"Linear Algebra","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Foundational for ML, graphics, and numerical methods"},
          {"subject":"MATH","catalog":"318","title":"Mathematical Logic","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential for machine learning and statistics"},
          {"subject":"MATH","catalog":"324","title":"Statistics","credits":3,"is_required":False},
          {"subject":"MATH","catalog":"340","title":"Discrete Mathematics","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # GERMAN STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "german_studies_major",
    "name": "German Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "An in-depth study of German language, literature, culture, and film "
      "from the eighteenth century to the present day. Covers major works of "
      "literature, philosophy, film, critical theory, and the history of lyric form."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/german-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "language_foundation",
        "title": "German Language Foundation",
        "credits_needed": 12,
        "notes": "12 credits of German language courses (GERM 100-level to 300-level), progressing through beginner to advanced levels.",
        "courses": [
          {"subject":"GERM","catalog":"100","title":"Beginner's German 1 (Intensive)","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Best entry if you have no prior German"},
          {"subject":"GERM","catalog":"200","title":"Intermediate German (Intensive)","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Efficient path to literary courses"},
          {"subject":"GERM","catalog":"100D1","title":"Beginner's German 1","credits":3,"is_required":False},
          {"subject":"GERM","catalog":"100D2","title":"Beginner's German 2","credits":3,"is_required":False},
          {"subject":"GERM","catalog":"200D1","title":"Intermediate German 1","credits":3,"is_required":False},
          {"subject":"GERM","catalog":"200D2","title":"Intermediate German 2","credits":3,"is_required":False},
          {"subject":"GERM","catalog":"307D1","title":"Intermediate German (Advanced)","credits":3,"is_required":False},
          {"subject":"GERM","catalog":"307D2","title":"Intermediate German (Advanced) 2","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "literature_culture",
        "title": "German Literature & Culture Courses",
        "credits_needed": 24,
        "notes": "24 credits from German literature, culture, and film. At least 9 credits must be at the 300-level or above.",
        "min_credits_400": 9,
        "courses": [
          {"subject":"GERM","catalog":"259","title":"Introduction to German Literature 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential foundation for literary track"},
          {"subject":"GERM","catalog":"260","title":"Introduction to German Literature 2","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Pairs with GERM 259; covers 19th c. to present"},
          {"subject":"GERM","catalog":"326","title":"Topics: German Language and Culture","credits":3,"is_required":False},
          {"subject":"GERM","catalog":"350","title":"Modernism and the Avant-Garde","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Highly valued for cultural studies track"},
          {"subject":"GERM","catalog":None,"title":"Any upper-level GERM course (300+)","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "german_studies_minor",
    "name": "German Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An introduction to German culture from the eighteenth century to the present. "
      "Courses include literature, philosophy, film, and theory taught in English or German."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/german-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "German Studies Courses",
        "credits_needed": 18,
        "notes": "18 credits of courses in German literature, culture, and film taught in English or German.",
        "courses": [
          {"subject":"GERM","catalog":"259","title":"Introduction to German Literature 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Best starting point for the minor"},
          {"subject":"GERM","catalog":"260","title":"Introduction to German Literature 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"GERM","catalog":"350","title":"Modernism and the Avant-Garde","credits":3,"is_required":False},
          {"subject":"GERM","catalog":None,"title":"Any GERM culture/literature course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # HISPANIC STUDIES
  # Source: McGill eCalendar 2024-2025
  # https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/programs/bachelor-arts-ba-major-concentration-hispanic-studies
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "hispanic_studies_major",
    "name": "Hispanic Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "A flexible 36-credit program examining the language and culture of Spain "
      "and Latin America, including literature, film, digital humanities, and "
      "intellectual history. Maximum 12 credits in English-taught courses."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/hispanic-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "language_civilization",
        "title": "Language and Civilization",
        "block_type": "choose_credits",
        "credits_needed": 0,
        "notes": (
          "0–18 credits from Spanish language and civilization courses. "
          "Students may begin at elementary, intermediate, or advanced level. "
          "HISP 210D1/D2 and HISP 218 cannot both be taken; "
          "HISP 219 and HISP 220D1/D2 cannot both be taken."
        ),
        "courses": [
          {"subject":"HISP","catalog":"210D1","title":"Spanish Language: Beginners 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Start here if no prior Spanish"},
          {"subject":"HISP","catalog":"210D2","title":"Spanish Language: Beginners 2","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"218","title":"Spanish Language Intensive – Elementary","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Faster single-term path through elementary level"},
          {"subject":"HISP","catalog":"219","title":"Spanish Language Intensive – Intermediate","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Intensive intermediate in one term"},
          {"subject":"HISP","catalog":"220D1","title":"Spanish Language: Intermediate 1","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"220D2","title":"Spanish Language: Intermediate 2","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"225","title":"Hispanic Civilization 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Introduction to Hispanic culture and history"},
          {"subject":"HISP","catalog":"226","title":"Hispanic Civilization 2","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "survey",
        "title": "Survey of Literature and Culture",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "notes": "6–12 credits from the four survey courses.",
        "courses": [
          {"subject":"HISP","catalog":"241","title":"Survey of Spanish Literature and Culture 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Foundation for upper-level literature courses"},
          {"subject":"HISP","catalog":"242","title":"Survey of Spanish Literature and Culture 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"243","title":"Survey of Latin American Literature and Culture 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"244","title":"Survey of Latin American Literature and Culture 2","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "literature_culture",
        "title": "Hispanic Literature and Culture",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "notes": (
          "6–30 credits from advanced Hispanic literature and culture courses. "
          "Minimum 6 credits at 400-level or above. "
          "Maximum 12 credits in English-taught courses count toward the major."
        ),
        "min_credits_400": 6,
        "courses": [
          {"subject":"HISP","catalog":"320","title":"Contemporary Brazilian Literature and Film","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"321","title":"Hispanic Literature of the 18th Century","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"325","title":"Spanish Novel of the 19th Century","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"326","title":"Spanish Romanticism","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"328","title":"Literature of Ideas: Latin America","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"332","title":"Latin American Literature of 19th Century","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"333","title":"Theatre, Performance and Politics in Latin America","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"335","title":"Politics and Poetry in Latin America","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"340","title":"Latin American Cinema","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"341","title":"Spanish Cinema","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"345","title":"Contemporary Hispanic Cultural Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Broad overview of contemporary Hispanic cultures"},
          {"subject":"HISP","catalog":"347","title":"Queer Iberia","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"352","title":"Latin American Novel","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"355","title":"Contemporary Spanish Literature and Culture","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"356","title":"Latin American Short Story","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"357","title":"Latin American Digital Literature and Culture","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"358","title":"Gender and Textualities","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"432","title":"Literature – Discovery and Exploration Spain New World","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"437","title":"Colonial / Postcolonial Latin America","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"438","title":"Topics: Spanish Literature","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"439","title":"Topics: Latin American Literature","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"451","title":"Don Quixote","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"454","title":"Major Figures: Spanish Literature and Culture","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"455","title":"Major Figures: Latin American Literature and Culture","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"458","title":"Golden Age Literature: Renaissance","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"505","title":"Seminar in Hispanic Studies","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "hispanic_studies_minor",
    "name": "Hispanic Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An 18-credit program providing a solid foundation in Spanish language and "
      "Hispanic culture. Expandable to the Major Concentration. "
      "Maximum 6 credits in English-taught courses."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/hispanic-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "language",
        "title": "Spanish Language",
        "block_type": "choose_credits",
        "credits_needed": 0,
        "notes": (
          "0–12 credits from Spanish language courses. "
          "HISP 210/218 cannot both be taken; HISP 219/220 cannot both be taken. "
          "Advanced Placement (AP) credits do not count toward the minor."
        ),
        "courses": [
          {"subject":"HISP","catalog":"210D1","title":"Spanish Language: Beginners 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Start here if no prior Spanish"},
          {"subject":"HISP","catalog":"210D2","title":"Spanish Language: Beginners 2","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"218","title":"Spanish Language Intensive – Elementary","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Faster single-term elementary path"},
          {"subject":"HISP","catalog":"219","title":"Spanish Language Intensive – Intermediate","credits":6,"is_required":False},
          {"subject":"HISP","catalog":"220D1","title":"Spanish Language: Intermediate 1","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"220D2","title":"Spanish Language: Intermediate 2","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "culture_lit",
        "title": "Hispanic Studies Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "notes": (
          "6–18 credits from HISP courses other than language courses. "
          "No more than 6 credits may be courses taught in English."
        ),
        "courses": [
          {"subject":"HISP","catalog":"225","title":"Hispanic Civilization 1","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"226","title":"Hispanic Civilization 2","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"241","title":"Survey of Spanish Literature and Culture 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"242","title":"Survey of Spanish Literature and Culture 2","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"243","title":"Survey of Latin American Literature and Culture 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"244","title":"Survey of Latin American Literature and Culture 2","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"328","title":"Literature of Ideas: Latin America","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"340","title":"Latin American Cinema","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"345","title":"Contemporary Hispanic Cultural Studies","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"352","title":"Latin American Novel","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"355","title":"Contemporary Spanish Literature and Culture","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"437","title":"Colonial / Postcolonial Latin America","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"451","title":"Don Quixote","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"454","title":"Major Figures: Spanish Literature and Culture","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"455","title":"Major Figures: Latin American Literature and Culture","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # ITALIAN STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "italian_studies_major",
    "name": "Italian Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "An in-depth study of Italian language, literature, and culture from the "
      "Middle Ages to the present, with emphasis on literature, cinema, theatre, "
      "and Italian cultural identity."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/italian-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "language",
        "title": "Italian Language Courses",
        "credits_needed": 12,
        "notes": "12 credits of Italian language (ITAL 100–ITAL 255). Students may begin at elementary, intermediate, or advanced level.",
        "courses": [
          {"subject":"ITAL","catalog":"100","title":"Beginner's Italian (Intensive)","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Best entry point with no prior Italian"},
          {"subject":"ITAL","catalog":"200","title":"Intermediate Italian (Intensive)","credits":6,"is_required":False,"recommended":True},
          {"subject":"ITAL","catalog":"215D1","title":"Intermediate Italian 1","credits":3,"is_required":False},
          {"subject":"ITAL","catalog":"215D2","title":"Intermediate Italian 2","credits":3,"is_required":False},
          {"subject":"ITAL","catalog":"255","title":"Advanced Reading and Composition","credits":6,"is_required":False},
        ],
      },
      {
        "block_key": "literature_culture",
        "title": "Italian Literature & Culture",
        "credits_needed": 24,
        "notes": "24 credits of ITAL literature/culture courses. At least 9 credits at 300-level or above.",
        "min_credits_400": 9,
        "courses": [
          {"subject":"ITAL","catalog":"270","title":"Manzoni: Novel and Nationhood","credits":3,"is_required":False},
          {"subject":"ITAL","catalog":"281","title":"Masterpieces of Italian Literature 2","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Covers Renaissance to 20th century – essential survey"},
          {"subject":"ITAL","catalog":"310","title":"The Invention of Italian Literature","credits":3,"is_required":False,"recommended":True},
          {"subject":"ITAL","catalog":None,"title":"Any ITAL literature/culture course at 300+","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "italian_studies_minor",
    "name": "Italian Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An introduction to Italian language and the key works and themes of Italian "
      "literature and culture. Expandable to the Major Concentration."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/italian-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "Italian Language & Culture",
        "credits_needed": 18,
        "notes": "18 credits of ITAL courses including at least 6 credits of language and 6 credits of literature/culture.",
        "courses": [
          {"subject":"ITAL","catalog":"100","title":"Beginner's Italian (Intensive)","credits":6,"is_required":False,"recommended":True,"recommendation_reason":"Efficient single-term entry"},
          {"subject":"ITAL","catalog":"215D1","title":"Intermediate Italian 1","credits":3,"is_required":False},
          {"subject":"ITAL","catalog":"281","title":"Masterpieces of Italian Literature 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"ITAL","catalog":"310","title":"The Invention of Italian Literature","credits":3,"is_required":False},
          {"subject":"ITAL","catalog":None,"title":"Any ITAL course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # FRENCH (LANGUE ET LITTÉRATURE FRANÇAISES)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "french_major",
    "name": "Langue et littérature françaises – Concentration majeure (Études et pratiques littéraires)",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "Étude approfondie de la langue et littérature françaises, incluant "
      "la littérature québécoise, française et francophone, ainsi que les "
      "théories littéraires contemporaines. Programme offert en français."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/",
    "blocks": [
      {
        "block_key": "obligatoires",
        "title": "Cours obligatoires",
        "credits_needed": 9,
        "notes": "9 crédits de cours obligatoires.",
        "courses": [
          {"subject":"FRLT","catalog":"100","title":"Introduction aux études littéraires","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Cours fondamental de méthodologie littéraire"},
          {"subject":"FRLT","catalog":"200","title":"Histoire de la littérature française","credits":3,"is_required":True,"recommended":True},
          {"subject":"FRLT","catalog":"300","title":"Théories et pratiques littéraires","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "complementaires",
        "title": "Cours complémentaires",
        "credits_needed": 27,
        "notes": "27 crédits de cours FRLT au choix, dont au moins 9 crédits au niveau 400 ou plus.",
        "min_credits_400": 9,
        "courses": [
          {"subject":"FRLT","catalog":None,"title":"Tout cours FRLT au niveau 200 ou plus","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "french_minor",
    "name": "Langue et littérature françaises – Concentration mineure",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "Introduction à la langue et littérature françaises offrant "
      "une exploration des textes québécois, français et francophones. "
      "Programme offert en français."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "Cours de littérature française",
        "credits_needed": 18,
        "notes": "18 crédits de cours FRLT. Cours offerts en français.",
        "courses": [
          {"subject":"FRLT","catalog":"100","title":"Introduction aux études littéraires","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Meilleur point de départ pour la mineure"},
          {"subject":"FRLT","catalog":"200","title":"Histoire de la littérature française","credits":3,"is_required":False,"recommended":True},
          {"subject":"FRLT","catalog":None,"title":"Tout cours FRLT","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # AFRICAN STUDIES (Minor – Major already seeded)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "african_studies_minor",
    "name": "African Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An interdisciplinary introduction to the history, politics, culture, "
      "and societies of Africa. Draws on courses from History, Political Science, "
      "Sociology, Anthropology, and Islamic Studies."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/programs/bachelor-arts-ba-minor-concentration-african-studies",
    "blocks": [
      {
        "block_key": "afri_minor_required",
        "title": "Required Courses",
        "block_type": "required",
        "credits_needed": 6,
        "notes": "Both courses are required for the minor.",
        "courses": [
          {"subject":"AFRI","catalog":"200","title":"Introduction to African Studies","credits":3,"is_required":True,"recommended":True},
          {"subject":"AFRI","catalog":"598","title":"Research Seminar in African Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Capstone seminar; required for both major and minor"},
        ],
      },
      {
        "block_key": "afri_minor_group_a",
        "title": "Group A – Core Courses (3 credits)",
        "block_type": "choose_credits",
        "credits_needed": 3,
        "notes": "3 credits from Group A.",
        "courses": [
          {"subject":"ANTH","catalog":"322","title":"Social Change in Modern Africa","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"200","title":"Introduction to African History","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"201","title":"Modern African History","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"324","title":"Comparative Politics of Africa","credits":3,"is_required":False,"recommended":True},
        ],
      },
      {
        "block_key": "afri_minor_group_b",
        "title": "Group B – Complementary Courses (9 credits)",
        "block_type": "choose_credits",
        "credits_needed": 9,
        "notes": "9 credits from Group B; at least 2 disciplines; max 6 credits from any one discipline.",
        "courses": [
          {"subject":"AFRI","catalog":"401","title":"Swahili Language and Culture","credits":3,"is_required":False},
          {"subject":"AFRI","catalog":"481","title":"Special Topics 1","credits":3,"is_required":False},
          {"subject":"AFRI","catalog":"499","title":"Arts Internships","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"212","title":"Anthropology of Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":"416","title":"Environment/Development: Africa","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"208","title":"Microeconomic Analysis and Applications","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":False},
          {"subject":"ENGL","catalog":"421","title":"African Literature","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"408","title":"Geography of Development","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"381","title":"African History Seminar 1","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"360","title":"Topics in Islamic Studies","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"227","title":"Introduction to Comparative Politics – Global South","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"365","title":"Health and Development","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # RELIGIOUS STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "religious_studies_major",
    "name": "Religious Studies – Major Concentration",
    "program_type": "major",
    "total_credits": 36,
    "description": (
      "Explores the history, beliefs, and practices of the world's religious traditions "
      "using a variety of scholarly approaches including historical, literary, anthropological, "
      "and philosophical methods."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/school-of-religious-studies/religious-studies-major-concentration-ba/",
    "blocks": [
      {
        "block_key": "intro",
        "title": "Introductory Courses",
        "credits_needed": 6,
        "notes": "6 credits of 200-level RELG introductory courses.",
        "courses": [
          {"subject":"RELG","catalog":"203","title":"World Religions","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Ideal broad survey to start with"},
          {"subject":"RELG","catalog":"207","title":"Religion and Culture","credits":3,"is_required":False,"recommended":True},
          {"subject":"RELG","catalog":"204","title":"Introduction to the Hebrew Bible","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"206","title":"Introduction to the New Testament","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"200","title":"Introduction to Religious Studies","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "upper_level",
        "title": "Upper-Level Courses",
        "credits_needed": 30,
        "notes": "30 credits of RELG courses at any level. At least 12 credits must be at the 300-level or above.",
        "min_credits_400": 6,
        "courses": [
          {"subject":"RELG","catalog":None,"title":"Any RELG course at 300+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  {
    "program_key": "religious_studies_minor",
    "name": "Religious Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An introduction to the study of religion covering major world religious traditions "
      "through textual, historical, and comparative approaches."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/school-of-religious-studies/religious-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "Religious Studies Courses",
        "credits_needed": 18,
        "notes": "18 credits of RELG courses. At least 6 credits must be at the 300-level or above.",
        "min_credits_400": 0,
        "courses": [
          {"subject":"RELG","catalog":"203","title":"World Religions","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Best starting point; covers all major traditions"},
          {"subject":"RELG","catalog":"207","title":"Religion and Culture","credits":3,"is_required":False,"recommended":True},
          {"subject":"RELG","catalog":"200","title":"Introduction to Religious Studies","credits":3,"is_required":False},
          {"subject":"RELG","catalog":None,"title":"Any RELG course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # INFORMATION STUDIES
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "information_studies_minor",
    "name": "Information Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "Explores the principles of information organization, access, and literacy. "
      "Offered by the McGill School of Information Studies (SIS), covering "
      "archives, libraries, and digital information management."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/school-of-information-studies/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Course",
        "credits_needed": 3,
        "courses": [
          {"subject":"INFS","catalog":"250","title":"Foundations of Information Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Gateway required course for all SIS programs"},
        ],
      },
      {
        "block_key": "complementary",
        "title": "Complementary INFS Courses",
        "credits_needed": 15,
        "notes": "15 credits from INFS courses at 200-level or above.",
        "courses": [
          {"subject":"INFS","catalog":"256","title":"Knowledge Organization","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Core classification and cataloguing theory"},
          {"subject":"INFS","catalog":"277","title":"Archives and Records Management","credits":3,"is_required":False,"recommended":True},
          {"subject":"INFS","catalog":"321","title":"Information Literacy","credits":3,"is_required":False},
          {"subject":"INFS","catalog":None,"title":"Any INFS course at 200+ level","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # EAST ASIAN STUDIES – MINOR (Major already seeded)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "east_asian_studies_minor",
    "name": "East Asian Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An interdisciplinary introduction to the cultures, languages, history, "
      "and social systems of China, Japan, and Korea."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/east-asian-studies/east-asian-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "East Asian Studies Courses",
        "credits_needed": 18,
        "notes": "18 credits from EAST courses. May include language courses (CHIN, JAPN, KORE).",
        "courses": [
          {"subject":"EAST","catalog":"211","title":"Introduction to East Asian Cultures","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Ideal broad entry point"},
          {"subject":"EAST","catalog":"215","title":"Modern China","credits":3,"is_required":False,"recommended":True},
          {"subject":"CHIN","catalog":"200D1","title":"Introductory Chinese 1","credits":3,"is_required":False},
          {"subject":"JAPN","catalog":"200D1","title":"Introductory Japanese 1","credits":3,"is_required":False},
          {"subject":"EAST","catalog":None,"title":"Any EAST course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # WORLD ISLAMIC & MIDDLE EASTERN STUDIES – MINOR
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "world_islamic_mideast_minor",
    "name": "World Islamic and Middle Eastern Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An interdisciplinary introduction to the history, politics, religion, "
      "and cultures of the Islamic world and the Middle East."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Course",
        "credits_needed": 3,
        "courses": [
          {"subject":"ISLA","catalog":"200","title":"Introduction to Islam","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required gateway course"},
        ],
      },
      {
        "block_key": "complementary",
        "title": "Complementary Courses",
        "credits_needed": 15,
        "notes": "15 credits from approved ISLA, HIST, POLI, RELG courses related to the Islamic world and Middle East.",
        "courses": [
          {"subject":"ISLA","catalog":"220","title":"Introduction to the Quran","credits":3,"is_required":False,"recommended":True},
          {"subject":"ISLA","catalog":"315","title":"Ottoman State and Society to 1839","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"226","title":"Modern History of the Middle East","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"341","title":"Foreign Policy: The Middle East","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":None,"title":"Any ISLA course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # LIBERAL ARTS (Faculty Program)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "liberal_arts_major",
    "name": "Liberal Arts – Faculty Program",
    "program_type": "major",
    "total_credits": 60,
    "description": (
      "An interdisciplinary program that provides a broad foundation in the "
      "humanities and social sciences. Students choose from a wide range of "
      "disciplines with guidance from a faculty advisor to create a coherent "
      "intellectual profile."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/liberal-arts-program/",
    "blocks": [
      {
        "block_key": "humanities",
        "title": "Humanities Courses",
        "credits_needed": 18,
        "notes": "At least 18 credits in humanities disciplines (History, Philosophy, English, Linguistics, Classics, Art History, Religious Studies, etc.).",
        "courses": [
          {"subject":"HIST","catalog":None,"title":"Any HIST course","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":None,"title":"Any PHIL course","credits":3,"is_required":False,"recommended":True},
          {"subject":"ENGL","catalog":None,"title":"Any ENGL course","credits":3,"is_required":False},
          {"subject":"RELG","catalog":None,"title":"Any RELG course","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "social_sciences",
        "title": "Social Science Courses",
        "credits_needed": 18,
        "notes": "At least 18 credits in social science disciplines (Economics, Political Science, Sociology, Anthropology, Psychology, etc.).",
        "courses": [
          {"subject":"ECON","catalog":None,"title":"Any ECON course","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":None,"title":"Any POLI course","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":None,"title":"Any SOCI course","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":None,"title":"Any PSYC course","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "electives",
        "title": "Additional Electives",
        "credits_needed": 24,
        "notes": "24 additional credits across Arts disciplines to reach 60 total. Students design this portion with their faculty advisor.",
        "courses": [
          {"subject":"ARTS","catalog":None,"title":"Any Faculty of Arts course","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # EUROPEAN LITERATURE AND CULTURE (Minor)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "european_lit_culture_minor",
    "name": "European Literature and Culture – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "A broad interdisciplinary introduction to the development of European "
      "culture through literature, philosophy, and the arts from the Middle Ages "
      "to the present. No prior knowledge of a European language required."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/european-literature-culture-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "required",
        "title": "Required Gateway Course",
        "credits_needed": 3,
        "courses": [
          {"subject":"LLCU","catalog":"210","title":"Introduction to European Literature and Culture","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required gateway; excellent broad overview"},
        ],
      },
      {
        "block_key": "complementary",
        "title": "European Culture & Literature Electives",
        "credits_needed": 15,
        "notes": "15 credits from approved LLCU, GERM, HISP, ITAL, RUSS courses. No more than 6 credits from any single language area.",
        "courses": [
          {"subject":"LLCU","catalog":None,"title":"Any LLCU course (200+)","credits":3,"is_required":False,"recommended":True},
          {"subject":"GERM","catalog":"259","title":"Introduction to German Literature 1","credits":3,"is_required":False},
          {"subject":"HISP","catalog":"241","title":"Survey of Peninsular Literature 1","credits":3,"is_required":False},
          {"subject":"ITAL","catalog":"281","title":"Masterpieces of Italian Literature 2","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ──────────────────────────────────────────────────────────────────
  # LATIN AMERICAN & CARIBBEAN STUDIES (Minor)
  # ──────────────────────────────────────────────────────────────────
  {
    "program_key": "latin_american_caribbean_minor",
    "name": "Latin American and Caribbean Studies – Minor Concentration",
    "program_type": "minor",
    "total_credits": 18,
    "description": (
      "An interdisciplinary minor focusing on the history, politics, cultures, "
      "and societies of Latin America and the Caribbean. Draws on History, "
      "Political Science, Sociology, Hispanic Studies, and Anthropology."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/latin-american-caribbean-studies-minor-concentration-ba/",
    "blocks": [
      {
        "block_key": "courses",
        "title": "Latin American & Caribbean Studies Courses",
        "credits_needed": 18,
        "notes": "18 credits from approved courses across departments. At least 9 credits must be directly focused on Latin America or the Caribbean.",
        "courses": [
          {"subject":"HIST","catalog":"259","title":"History of Latin America to 1825","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Core historical foundation"},
          {"subject":"HIST","catalog":"260","title":"History of Latin America since 1825","credits":3,"is_required":False,"recommended":True},
          {"subject":"HISP","catalog":"243","title":"Survey of Spanish-American Literature 1","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"237","title":"Latin American Politics","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":None,"title":"Any ANTH course on Latin America","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════

]
