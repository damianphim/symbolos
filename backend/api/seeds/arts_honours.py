"""
McGill Faculty of Arts – Honours programs: Economics, Political Science, Psychology, Sociology, History, Linguistics, Philosophy, Anthropology, Art History, IDS, Geography, Classics, GSFSJ, Jewish Studies, East Asian Studies, Religious Studies, World Islamic
Sub-module of arts_degree_requirements.py
"""

ARTS_HONOURS = [
  # HONOURS PROGRAMS
  # Source: McGill eCalendar 2024-2025
  # ══════════════════════════════════════════════════════════════════

  # ── ECONOMICS HONOURS ─────────────────────────────────────────────
  {
    "program_key": "economics_honours",
    "name": "Economics – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 42,
    "description": (
      "A rigorous 42-credit research-oriented program for students intending graduate studies "
      "or careers requiring advanced quantitative skills. Requires CGPA of 3.0 and a minimum "
      "grade of B- in ECON 250D1/D2 to continue. Honours courses are distinct from Major courses "
      "(ECON 250 replaces 230, ECON 257 replaces 227, ECON 353/354 replace 332/333)."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/economics/economics-honours-ba/",
    "blocks": [
      {
        "block_key": "econ_hon_core",
        "title": "Required Core (30 credits)",
        "block_type": "required",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name": None,
        "notes": (
          "27 credits fixed required + 3 credits from ECON 460, 461, or 469. "
          "Course sequence: U1 = ECON 250D1/D2 + 257D1/D2; U2 = ECON 353 + 354 + 257 (if not in U1); "
          "U3 = ECON 450 + 452 + 468. Minimum grade B- in ECON 250D1/D2 to continue."
        ),
        "sort_order": 1,
        "courses": [
          {"subject":"ECON","catalog":"250D1","title":"Introduction to Economic Theory: Honours 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Take Fall U1 — replaces ECON 230D1 for Honours students"},
          {"subject":"ECON","catalog":"250D2","title":"Introduction to Economic Theory: Honours 2","credits":3,"is_required":True},
          {"subject":"ECON","catalog":"257D1","title":"Economic Statistics – Honours 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Take with 250D1/D2 — replaces ECON 227D for Honours students"},
          {"subject":"ECON","catalog":"257D2","title":"Economic Statistics – Honours 2","credits":3,"is_required":True},
          {"subject":"ECON","catalog":"353","title":"Macroeconomics – Honours 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"U2 macro core; take after 250D2"},
          {"subject":"ECON","catalog":"354","title":"Macroeconomics – Honours 2","credits":3,"is_required":True},
          {"subject":"ECON","catalog":"450","title":"Advanced Economic Theory 1 – Honours","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"U3 advanced micro; capstone theory course"},
          {"subject":"ECON","catalog":"452","title":"Advanced Economic Theory 2 – Honours","credits":3,"is_required":True},
          {"subject":"ECON","catalog":"468","title":"Econometrics 1 – Honours","credits":3,"is_required":True},
          # Choose 3 credits from:
          {"subject":"ECON","catalog":"460","title":"History of Thought 1 – Honours","credits":3,"is_required":False,"choose_from_group":"hon_elective_req","choose_n_credits":3},
          {"subject":"ECON","catalog":"461","title":"History of Thought 2 – Honours","credits":3,"is_required":False,"choose_from_group":"hon_elective_req","choose_n_credits":3},
          {"subject":"ECON","catalog":"469","title":"Econometrics 2 – Honours","credits":3,"is_required":False,"choose_from_group":"hon_elective_req","choose_n_credits":3,"recommended":True,"recommendation_reason":"Continue with econometrics — highly recommended for empirical research"},
        ],
      },
      {
        "block_key": "econ_hon_complementary",
        "title": "Complementary ECON Electives (12 credits)",
        "block_type": "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "min_credits_400": 9,
        "notes": "12 credits of ECON at 300, 400, or 500 level (approved by Honours adviser); at least 9 credits at 400 or 500 level.",
        "sort_order": 2,
        "courses": [
          {"subject":"ECON","catalog":"337","title":"Introductory Econometrics 1","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"338","title":"Introductory Econometrics 2","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"405","title":"Natural Resource Economics","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"406","title":"Topics in Economic Policy","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"408","title":"Public Sector Economics 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"416","title":"Topics in Economic Development 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"420","title":"Topics in Economic Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"423","title":"International Trade","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"424","title":"International Payments","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"426","title":"Labour Economics","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"437","title":"Methods for Causal Inference","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"440","title":"Health Economics","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"447","title":"Economics of Information and Uncertainty","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"510","title":"Experimental Economics","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"546","title":"Game Theory","credits":3,"is_required":False,"recommended":True},
        ],
      },
    ],
  },

  # ── POLITICAL SCIENCE HONOURS ─────────────────────────────────────
  {
    "program_key": "political_science_honours",
    "name": "Political Science – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 48,
    "description": (
      "A 48-credit intensive program. Requires 6 credits of methods courses (POLI 300/400-level), "
      "at least 12 credits at 400-level (including one 500-level Honours Seminar), and field caps "
      "of max 24 credits in any field (27 for Comparative Politics). "
      "Optional thesis: POLI 499. CGPA 3.0 required."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/political-science/political-science-honours-ba/",
    "blocks": [
      {
        "block_key": "polsci_hon_methods",
        "title": "Methods (6 credits required)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 credits of POLI Methods courses at 300 or 400 level.",
        "sort_order": 1,
        "courses": [
          {"subject":"POLI","catalog":"311","title":"Introduction to Quantitative Political Science","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"312","title":"Intermediate Quantitative Political Science","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"313","title":"Introduction to Qualitative Methods in Political Science","credits":3,"is_required":False,"recommended":True},
        ],
      },
      {
        "block_key": "polsci_hon_upper",
        "title": "POLI Upper-Level Courses (42 credits)",
        "block_type": "choose_credits",
        "credits_needed": 42,
        "courses_needed": None,
        "group_name": None,
        "min_credits_400": 12,
        "notes": (
          "42 credits of POLI courses (including 6 methods credits above). "
          "At least 12 credits at 400-level; at least 1 course at 500-level (Honours Seminar). "
          "Field caps: max 24 credits per field (27 for Comparative Politics). "
          "Must take one 200-level course in a field before 300/400-level in that field. "
          "Optional: POLI 499 (Honours Thesis, 6 credits) within these 42 credits."
        ),
        "sort_order": 2,
        "courses": [
          # 200-level entry courses (one per field required as prerequisite)
          {"subject":"POLI","catalog":"212","title":"Introduction to Comparative Politics – Europe/North America","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"221","title":"Government of Canada","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"227","title":"Introduction to Comparative Politics – Global South","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"231","title":"Introduction to Political Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"243","title":"International Politics of Economic Relations","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"244","title":"International Politics: State Behaviour","credits":3,"is_required":False,"recommended":True},
          # 300-level courses
          {"subject":"POLI","catalog":"325","title":"U.S. Politics","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"333","title":"Western Political Theory 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"334","title":"Western Political Theory 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"340","title":"Comparative Politics of the Middle East","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"342","title":"Canadian Foreign Policy","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"345","title":"International Organizations","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"350","title":"Global Environmental Politics","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"360","title":"Security: War and Peace","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"363","title":"Contemporary Political Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"365","title":"Democratic Theory","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"371","title":"Challenge of Canadian Federalism","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"372","title":"Indigenous Peoples and the Canadian State","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"380","title":"Contemporary Chinese Politics","credits":3,"is_required":False},
          # 400-level courses (count toward 12-credit 400-level minimum)
          {"subject":"POLI","catalog":"421","title":"The Politics of Misinformation","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"431","title":"Nations and Nationalism","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"433","title":"History of Political/Social Theory 3","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"434","title":"History of Political/Social Theory 4","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"441","title":"International Political Economy: Trade","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"446","title":"International Law and Politics of Human Rights","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"450","title":"Peacebuilding","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"463","title":"Contemporary Political Theory","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"470","title":"Philosophy, Economy and Society","credits":3,"is_required":False},
          # 500-level Honours Seminars (one required)
          {"subject":"POLI","catalog":"521","title":"Seminar: Canadian Politics and Government","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"522","title":"Seminar: Comparative Politics 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"524","title":"Seminar: Comparative Politics 2","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"561","title":"Seminar: Political Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"575","title":"Seminar: International Politics","credits":3,"is_required":False},
          # Optional thesis
          {"subject":"POLI","catalog":"499","title":"Honours Thesis","credits":6,"is_required":False,"recommendation_reason":"Optional but strongly recommended for grad school applicants"},
        ],
      },
    ],
  },

  # ── PSYCHOLOGY HONOURS ────────────────────────────────────────────
  {
    "program_key": "psychology_honours",
    "name": "Psychology – Honours (B.A./B.Sc.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "A 60-credit program required for students intending to apply to graduate school in psychology. "
      "Requires a minimum CGPA of 3.50 to apply (typical cut-off ~3.75). "
      "All prerequisite courses (PSYC 204, 211, 212, 213, 215, 305) must be completed before admission. "
      "Includes a supervised 2-term research course and seminar."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/psychology/psychology-honours-ba/",
    "blocks": [
      {
        "block_key": "psyc_hon_core",
        "title": "Required Core (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required. PSYC 204 and 305 must be taken before most Honours courses.",
        "sort_order": 1,
        "courses": [
          {"subject":"PSYC","catalog":"204","title":"Introduction to Psychological Statistics","credits":3,"is_required":True,"recommended":True},
          {"subject":"PSYC","catalog":"211","title":"Introductory Behavioural Neuroscience","credits":3,"is_required":True,"recommended":True},
          {"subject":"PSYC","catalog":"212","title":"Perception","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":"213","title":"Cognition","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":"215","title":"Social Psychology","credits":3,"is_required":True,"recommended":True},
          {"subject":"PSYC","catalog":"305","title":"Statistics for Experimental Design","credits":3,"is_required":True,"recommended":True},
        ],
      },
      {
        "block_key": "psyc_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Both parts required. Conducted under supervision of a faculty member.",
        "sort_order": 2,
        "courses": [
          {"subject":"PSYC","catalog":"461","title":"Honours Research Thesis 1","credits":3,"is_required":True},
          {"subject":"PSYC","catalog":"462","title":"Honours Research Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "psyc_hon_electives",
        "title": "PSYC Electives (30 credits)",
        "block_type": "choose_credits",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name": None,
        "notes": "30 credits of PSYC at 300-level or above; at least 9 credits at 400-level.",
        "sort_order": 3,
        "courses": [
          {"subject":"PSYC","catalog":"311","title":"Cognitive Psychology","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"319","title":"Brain and Behaviour","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"340","title":"Personality","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"410","title":"Advanced Abnormal Psychology","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"413","title":"Advanced Developmental Psychology","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"433","title":"Cognitive Science","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"514","title":"Cognitive Neuroscience","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"538","title":"Human Memory","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── SOCIOLOGY HONOURS ─────────────────────────────────────────────
  {
    "program_key": "sociology_honours",
    "name": "Sociology – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 51,
    "description": (
      "A 51-credit research-intensive program with advanced training in sociological theory and methods. "
      "Culminates in an independent honours project (SOCI 480). "
      "CGPA of 3.0 required; recommended for students considering graduate school. "
      "Required courses must be taken at McGill."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/sociology/sociology-honours-ba/",
    "blocks": [
      {
        "block_key": "soci_hon_core",
        "title": "Required Core (21 credits)",
        "block_type": "required",
        "credits_needed": 21,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required. SOCI 350 may be replaced by an approved stats equivalent (ECON 227D, PSYC 204, etc.) + another SOCI 300+ course.",
        "sort_order": 1,
        "courses": [
          {"subject":"SOCI","catalog":"210","title":"Sociological Perspectives","credits":3,"is_required":True,"recommended":True},
          {"subject":"SOCI","catalog":"211","title":"Sociological Inquiry","credits":3,"is_required":True,"recommended":True},
          {"subject":"SOCI","catalog":"330","title":"Classical Sociological Theory","credits":3,"is_required":True,"recommended":True},
          {"subject":"SOCI","catalog":"350","title":"Statistics in Social Research","credits":3,"is_required":True},
          {"subject":"SOCI","catalog":"461","title":"Honours Seminar 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Advanced methods seminar for Honours cohort"},
          {"subject":"SOCI","catalog":"477","title":"Honours Seminar 2","credits":3,"is_required":True},
          {"subject":"SOCI","catalog":"480","title":"Honours Project","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Independent research project under faculty supervision"},
        ],
      },
      {
        "block_key": "soci_hon_complementary",
        "title": "Complementary SOCI Courses (30 credits)",
        "block_type": "choose_credits",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name": None,
        "min_credits_400": 9,
        "max_credits_200": 9,
        "notes": "30 credits of SOCI; at least 9 credits at 400-level or above; max 9 credits at 200-level. Max 6 credits from special topics (SOCI 340/341/342/343/440/441/442/443).",
        "sort_order": 2,
        "courses": [
          # 200-level
          {"subject":"SOCI","catalog":"230","title":"Self and Society","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"234","title":"Sociology of Gender","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"244","title":"Social Problems","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"245","title":"Population and Society","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"250","title":"Social Inequality","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"254","title":"Development and Underdevelopment","credits":3,"is_required":False},
          # 300-level
          {"subject":"SOCI","catalog":"300","title":"Sociology of Sexualities","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"302","title":"Health and Illness","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"303","title":"Sociology of Mental Health","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"310","title":"Medical Sociology","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"320","title":"Contemporary Social Movements","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"322","title":"Comparative Migration and Citizenship","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"323","title":"Colonialism and Society","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"326","title":"Political Sociology","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"340","title":"Criminology","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"348","title":"Sociology of the Family","credits":3,"is_required":False},
          # 400-level
          {"subject":"SOCI","catalog":"404","title":"Advanced Contemporary Sociological Theory","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"420","title":"Sociology of Race and Ethnicity","credits":3,"is_required":False,"recommended":True},
          {"subject":"SOCI","catalog":"450","title":"Social Class and Stratification","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── HISTORY HONOURS ──────────────────────────────────────────────
  {
    "program_key": "history_honours",
    "name": "History – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 54,
    "description": (
      "A 54-credit research-intensive program developing advanced historical analysis and writing. "
      "Includes HIST 299 and HIST 399 (restricted to Honours students), at least 6 credits of "
      "500-level honours seminars, and min 6 credits at 400+ level. "
      "GPA: 3.30 in program, 3.0 (B) minimum per course, CGPA 3.0."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/history-classical-studies/history-honours-ba/",
    "blocks": [
      {
        "block_key": "hist_hon_core",
        "title": "Required Core (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Both required. HIST 399 is restricted to History Honours/Joint Honours students.",
        "sort_order": 1,
        "courses": [
          {"subject":"HIST","catalog":"299","title":"The Historian's Craft","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Methods foundation; take in U2 Fall"},
          {"subject":"HIST","catalog":"399","title":"History and Historiography","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Restricted to Honours students; take in U2/U3"},
        ],
      },
      {
        "block_key": "hist_hon_seminar",
        "title": "Honours Seminars (minimum 6 credits)",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "At least 6 credits of 500-level honours seminars (D1/D2 format). The 2nd term includes a major research paper based substantially on primary-source research.",
        "sort_order": 2,
        "courses": [
          {"subject":"HIST","catalog":"595D1","title":"Honours Seminar 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"595D2","title":"Honours Seminar 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"597D1","title":"Honours Seminar 3","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"597D2","title":"Honours Seminar 4","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "hist_hon_fields",
        "title": "History Electives (42 credits)",
        "block_type": "choose_credits",
        "credits_needed": 42,
        "courses_needed": None,
        "group_name": None,
        "min_credits_400": 6,
        "max_credits_200": 18,
        "notes": (
          "42 credits of HIST (including honours seminars and HIST 299/399 above). "
          "Min 6 credits at 400+ level (additional to seminars). Max 18 credits at 200-level. "
          "Must satisfy same Group A/B/C + Temporal Breadth distribution as History Major."
        ),
        "sort_order": 3,
        "courses": [
          # Group A (Canadian/American/European surveys)
          {"subject":"HIST","catalog":"202","title":"Survey: Canada to 1867","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"203","title":"Survey: Canada since 1867","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"211","title":"American History to 1865","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"212","title":"American History since 1865","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"214","title":"History of Europe, 1300–1815","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"215","title":"History of Europe, 1815–Present","credits":3,"is_required":False},
          # Group B (Non-Western/Ancient)
          {"subject":"HIST","catalog":"200","title":"Africa and the Atlantic World","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"201","title":"History of Africa since 1800","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"205","title":"Middle East: Early Period","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"206","title":"Middle East: Modern Period","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"208","title":"History of China to 1800","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"209","title":"Modern China","credits":3,"is_required":False},
          # 300-level
          {"subject":"HIST","catalog":"303","title":"History of Quebec","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"307","title":"History of the United States: Social History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"322","title":"Imperial Germany and the Third Reich","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"324","title":"Russia: The Revolutionary Period","credits":3,"is_required":False},
          # 400-level (count toward 6-credit 400+ minimum)
          {"subject":"HIST","catalog":"400","title":"Advanced Seminar: Topics in History","credits":3,"is_required":False,"recommended":True},
          {"subject":"HIST","catalog":"449","title":"Topics in History","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── LINGUISTICS HONOURS ──────────────────────────────────────────
  {
    "program_key": "linguistics_honours",
    "name": "Linguistics – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours program offers advanced training in core areas of linguistics: phonology, "
      "syntax, semantics, and phonetics. Includes an honours thesis and is strongly recommended "
      "for students planning graduate work in linguistics, cognitive science, or NLP."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/linguistics/linguistics-honours-ba/",
    "blocks": [
      {
        "block_key": "ling_hon_core",
        "title": "Required Core (24 credits)",
        "block_type": "required",
        "credits_needed": 24,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required. LING 480D1/D2 is the Honours thesis (2 consecutive terms).",
        "sort_order": 1,
        "courses": [
          {"subject":"LING","catalog":"201","title":"Introduction to Linguistics","credits":3,"is_required":True,"recommended":True},
          {"subject":"LING","catalog":"330","title":"Phonetics","credits":3,"is_required":True,"recommended":True},
          {"subject":"LING","catalog":"331","title":"Phonology 1","credits":3,"is_required":True,"recommended":True},
          {"subject":"LING","catalog":"360","title":"Introduction to Semantics","credits":3,"is_required":True,"recommended":True},
          {"subject":"LING","catalog":"371","title":"Syntax 1","credits":3,"is_required":True,"recommended":True},
          {"subject":"LING","catalog":"480D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"LING","catalog":"480D2","title":"Honours Thesis 2","credits":3,"is_required":True},
          {"subject":"PHIL","catalog":"210","title":"Introduction to Deductive Logic 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required logic/formal methods for Honours program"},
        ],
      },
      {
        "block_key": "ling_hon_electives",
        "title": "Linguistics and Related Field Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "min_credits_400": 15,
        "max_credits_200": 3,
        "notes": (
          "36 credits of additional LING/related courses. "
          "At least 15 credits at 400/500-level; max 3 at 200-level. "
          "12 credits may be from related fields (Cognitive Science, Computer Science, Philosophy, Psychology)."
        ),
        "sort_order": 2,
        "courses": [
          # Additional LING courses
          {"subject":"LING","catalog":"320","title":"Sociolinguistics 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"325","title":"Canadian English","credits":3,"is_required":False},
          {"subject":"LING","catalog":"350","title":"Linguistic Aspects of Bilingualism","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"355","title":"Language Acquisition 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"425","title":"Historical Linguistics","credits":3,"is_required":False},
          {"subject":"LING","catalog":"440","title":"Morphology","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"520","title":"Sociolinguistics 2","credits":3,"is_required":False},
          {"subject":"LING","catalog":"550","title":"Computational Linguistics","credits":3,"is_required":False,"recommended":True},
          {"subject":"LING","catalog":"571","title":"Syntax 2","credits":3,"is_required":False,"recommended":True},
          # Related fields (max 12cr)
          {"subject":"COMP","catalog":"445","title":"Computational Linguistics","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"CS cross-listing of Computational Linguistics — counts as related field"},
          {"subject":"PSYC","catalog":"211","title":"Introductory Behavioural Neuroscience","credits":3,"is_required":False},
          {"subject":"PSYC","catalog":"213","title":"Cognition","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Cognitive science crossover — highly relevant for psycholinguistics"},
        ],
      },
    ],
  },

  # ── PHILOSOPHY HONOURS ───────────────────────────────────────────
  {
    "program_key": "philosophy_honours",
    "name": "Philosophy – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours in Philosophy provides rigorous training in philosophical analysis, "
      "logic, ethics, epistemology, and metaphysics. The thesis component allows students "
      "to develop an original philosophical argument under faculty supervision."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/philosophy/philosophy-honours-ba/",
    "blocks": [
      {
        "block_key": "phil_hon_core",
        "title": "Required Core",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "PHIL 210 is required for all Honours students.",
        "sort_order": 1,
        "courses": [
          {"subject":"PHIL","catalog":"210","title":"Introduction to Deductive Logic 1","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "phil_hon_thesis",
        "title": "Honours Thesis",
        "block_type": "required",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name": None,
        "notes": "3 credits: PHIL 498 (Honours Tutorial in Philosophy); or 6 credits: PHIL 499 (Interdisciplinary Honours Thesis).",
        "sort_order": 2,
        "courses": [
          {"subject":"PHIL","catalog":"498","title":"Honours Tutorial in Philosophy","credits":3,"is_required":True},
          {"subject":"PHIL","catalog":"499","title":"Interdisciplinary Honours Thesis","credits":6,"is_required":False},
        ],
      },
      {
        "block_key": "phil_hon_electives",
        "title": "Philosophy Electives",
        "block_type": "choose_credits",
        "credits_needed": 54,
        "courses_needed": None,
        "group_name": None,
        "min_credits_400": 12,
        "notes": (
          "54 credits of PHIL courses to reach 60 total (including PHIL 210 and thesis). "
          "At least 12 credits at 400 or 500 level (not counting PHIL 499). "
          "At least 3 credits at 500 level. "
          "Courses should be distributed across Groups A–F. "
          "Max 15 credits at 200 level."
        ),
        "sort_order": 3,
        "courses": [
          # 200-level
          {"subject":"PHIL","catalog":"200","title":"Introduction to Philosophy 1","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"201","title":"Introduction to Philosophy 2","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"230","title":"Introduction to Moral Philosophy 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"240","title":"Introduction to Moral and Political Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"242","title":"Critical Thinking","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"260","title":"Epistemology: Knowledge and Reality","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"271","title":"Bioethics","credits":3,"is_required":False},
          # 300-level
          {"subject":"PHIL","catalog":"302","title":"Philosophy of Science","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"306","title":"Philosophy of Mind","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"307","title":"Metaphysics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"310","title":"Political Philosophy","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"315","title":"Philosophy of Law","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"318","title":"Environmental Ethics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"320","title":"Philosophy of Religion","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"325","title":"Chinese Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"327","title":"Topics in African Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"330","title":"Philosophy of Language","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"331","title":"Advanced Ethics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"332","title":"Global Justice","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"340","title":"Epistemology","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"345","title":"Aesthetics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"350","title":"History and Philosophy of Ancient Science","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"352","title":"Feminist Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"354","title":"Plato","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"355","title":"Aristotle","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"356","title":"Early Medieval Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"360","title":"17th Century Philosophy","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"361","title":"18th Century Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"366","title":"18th and Early 19th Century German Philosophy","credits":3,"is_required":False},
          # 400-level (count toward upper-level requirement)
          {"subject":"PHIL","catalog":"415","title":"Topics in Philosophy of Language","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"416","title":"Topics in Metaphysics and Epistemology","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"420","title":"Topics in Ethics","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"425","title":"Topics in Political Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"430","title":"Topics in Epistemology and Metaphysics","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"435","title":"Topics in Philosophy of Mind","credits":3,"is_required":False,"recommended":True},
          {"subject":"PHIL","catalog":"444","title":"19th Century Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"445","title":"Contemporary Continental Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"465","title":"Topics in the History of Philosophy","credits":3,"is_required":False},
          {"subject":"PHIL","catalog":"470","title":"Advanced Seminar in Philosophy","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── ANTHROPOLOGY HONOURS ─────────────────────────────────────────
  {
    "program_key": "anthropology_honours",
    "name": "Anthropology – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours program provides intensive training in sociocultural, biological, "
      "and archaeological anthropology. Students conduct original fieldwork or archival "
      "research and produce a supervised thesis. CGPA of 3.0 required to enter."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/anthropology/anthropology-honours-ba/",
    "blocks": [
      {
        "block_key": "anth_hon_core",
        "title": "Required Core (21 credits)",
        "block_type": "required",
        "credits_needed": 21,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"ANTH","catalog":"202","title":"Introduction to Social and Cultural Anthropology","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"203","title":"Introduction to Biological Anthropology","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"204","title":"Introduction to Archaeology","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"303","title":"Social and Cultural Theory","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"393","title":"Research Methods in Anthropology","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"494","title":"Honours Seminar","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"396","title":"Ethnographic Methods","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "anth_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Original ethnographic or archival research.",
        "sort_order": 2,
        "courses": [
          {"subject":"ANTH","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"ANTH","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "anth_hon_electives",
        "title": "ANTH Electives (33 credits)",
        "block_type": "choose_credits",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name": None,
        "notes": "33 credits of ANTH. At least 12 credits at 400-level.",
        "sort_order": 3,
        "courses": [
          {"subject":"ANTH","catalog":"310","title":"Medical Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"315","title":"Anthropology of Religion","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"320","title":"Economic Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"403","title":"Advanced Theory in Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"410","title":"Topics in Sociocultural Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"430","title":"Advanced Biological Anthropology","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── ART HISTORY HONOURS ─────────────────────────────────────────
  {
    "program_key": "art_history_honours",
    "name": "Art History – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 54,
    "description": (
      "The Honours program offers advanced study in the history and theory of art from "
      "antiquity to the present. Students produce an original research thesis engaging "
      "primary sources and scholarly literature."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/art-history-communication-studies/art-history-honours-ba/",
    "blocks": [
      {
        "block_key": "arth_hon_core",
        "title": "Required Core (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"ARTH","catalog":"205","title":"History of Art: Antiquity and Middle Ages","credits":3,"is_required":True},
          {"subject":"ARTH","catalog":"206","title":"History of Art: Renaissance to Present","credits":3,"is_required":True},
          {"subject":"ARTH","catalog":"301","title":"Art Theory and Criticism","credits":3,"is_required":True},
          {"subject":"ARTH","catalog":"395","title":"Methods in Art History","credits":3,"is_required":True},
          {"subject":"ARTH","catalog":"400","title":"Advanced Seminar in Art History","credits":3,"is_required":True},
          {"subject":"ARTH","catalog":"430","title":"Contemporary Art Theory","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "arth_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Original contribution to art history scholarship.",
        "sort_order": 2,
        "courses": [
          {"subject":"ARTH","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"ARTH","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "arth_hon_electives",
        "title": "Art History Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "notes": "36 credits of ARTH. At least 12 credits at 400-level; courses distributed across chronological periods.",
        "sort_order": 3,
        "courses": [
          {"subject":"ARTH","catalog":"310","title":"Topics in Medieval Art","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"320","title":"Renaissance Art","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"340","title":"Modern Art","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"350","title":"Canadian Art and Architecture","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"410","title":"Topics in 20th-Century Art","credits":3,"is_required":False},
          {"subject":"ARTH","catalog":"440","title":"Non-Western Art","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── INTERNATIONAL DEVELOPMENT STUDIES HONOURS ────────────────────
  # Source: McGill eCalendar 2024-2025
  # https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/programs/bachelor-arts-ba-honours-international-development-studies
  {
    "program_key": "intl_development_honours",
    "name": "International Development Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 57,
    "description": (
      "The Honours in International Development Studies (57 credits) prepares students "
      "for graduate work or careers in international organisations, NGOs, and policy research. "
      "Requires a program GPA of 3.50 and minimum CGPA of 3.00. "
      "At least 30 of 57 credits must be at 300+ level; 9 credits at 400+ level; "
      "minimum 12 INTD credits; max 18 credits in any one discipline other than INTD."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/international-development/international-development-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "intd_hon_required",
        "title": "Required Courses",
        "block_type": "required",
        "credits_needed": 12,
        "notes": "All four courses are required.",
        "sort_order": 1,
        "courses": [
          {"subject":"ECON","catalog":"208","title":"Microeconomic Analysis and Applications","credits":3,"is_required":True,"recommended":True},
          {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":True,"recommended":True},
          {"subject":"INTD","catalog":"200","title":"Introduction to International Development","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Entry point for the program"},
          {"subject":"INTD","catalog":"498","title":"Honours Seminar in International Development","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Required honours seminar"},
        ],
      },
      {
        "block_key": "intd_hon_introductory",
        "title": "Introductory Electives",
        "block_type": "choose_credits",
        "credits_needed": 6,
        "notes": "3 credits from Culture, Populations and Development; 3 credits from Politics, Society and Development.",
        "sort_order": 2,
        "courses": [
          # Culture, Populations and Development (choose 3 cr)
          {"subject":"ANTH","catalog":"202","title":"Socio-Cultural Anthropology","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":"207","title":"Ethnography Through Film","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"212","title":"Anthropology of Development","credits":3,"is_required":False,"recommended":True},
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
        "block_key": "intd_hon_thematic",
        "title": "Thematic Electives",
        "block_type": "choose_credits",
        "credits_needed": 39,
        "notes": (
          "39 credits from the approved IDS thematic elective list. "
          "At least 30 of 57 total credits at 300+ level; at least 9 at 400+ level. "
          "Minimum 12 INTD credits across the entire program. "
          "Max 18 credits in any one discipline other than INTD."
        ),
        "sort_order": 3,
        "courses": [
          # INTD courses
          {"subject":"INTD","catalog":"250","title":"Topics in International Development","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"350","title":"Culture and Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"INTD","catalog":"352","title":"Topics in International Development 2","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"354","title":"Topics in International Development 3","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"356","title":"Topics in International Development 4","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"358","title":"Topics in International Development 5","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"360","title":"Topics in International Development 6","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"397","title":"Field Studies in International Development 1","credits":3,"is_required":False,"recommended":True},
          {"subject":"INTD","catalog":"398","title":"Field Studies in International Development 2","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"490","title":"Topics in International Development 7","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"491","title":"Topics in International Development 8","credits":3,"is_required":False},
          {"subject":"INTD","catalog":"499","title":"Independent Research in International Development","credits":3,"is_required":False},
          # Agricultural Economics
          {"subject":"AGEC","catalog":"430","title":"Agriculture, Food and Resource Policy","credits":3,"is_required":False},
          {"subject":"AGEC","catalog":"442","title":"Economics of International Agricultural Development","credits":3,"is_required":False},
          # Agriculture
          {"subject":"AGRI","catalog":"411","title":"Global Issues on Development, Food and Agriculture","credits":3,"is_required":False},
          # Anthropology
          {"subject":"ANTH","catalog":"206","title":"Environment and Culture","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"214","title":"Violence, Warfare, Culture","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"227","title":"Medical Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"302","title":"New Horizons in Medical Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"308","title":"Political Anthropology","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"322","title":"Social Change in Modern Africa","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"326","title":"Anthropology of Latin America","credits":3,"is_required":False},
          {"subject":"ANTH","catalog":"418","title":"Environment and Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"ANTH","catalog":"512","title":"Political Ecology","credits":3,"is_required":False},
          # Economics
          {"subject":"ECON","catalog":"205","title":"An Introduction to Political Economy","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"314","title":"Economic Development 2","credits":3,"is_required":False,"recommended":True},
          {"subject":"ECON","catalog":"326","title":"Ecological Economics","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"347","title":"Economics of Climate Change","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"411","title":"Economic Development: A World Area","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"416","title":"Topics in Economic Development 2","credits":3,"is_required":False},
          {"subject":"ECON","catalog":"473","title":"Income Distribution","credits":3,"is_required":False},
          # Geography
          {"subject":"GEOG","catalog":"302","title":"Environmental Management 1","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"310","title":"Development and Livelihoods","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"360","title":"Analyzing Sustainability","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"406","title":"Human Dimensions of Climate Change","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"408","title":"Geography of Development","credits":3,"is_required":False,"recommended":True},
          {"subject":"GEOG","catalog":"410","title":"Geography of Underdevelopment: Current Problems","credits":3,"is_required":False},
          # History
          {"subject":"HIST","catalog":"200","title":"Introduction to African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"201","title":"Modern African History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"206","title":"Indian Ocean World History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"209","title":"Introduction to South Asian History","credits":3,"is_required":False},
          {"subject":"HIST","catalog":"309","title":"History of Latin America to 1825","credits":3,"is_required":False},
          # Political Science
          {"subject":"POLI","catalog":"318","title":"International Organizations","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"340","title":"Human Rights","credits":3,"is_required":False,"recommended":True},
          {"subject":"POLI","catalog":"347","title":"Politics of the Developing World","credits":3,"is_required":False},
          {"subject":"POLI","catalog":"418","title":"Global Environment and World Politics","credits":3,"is_required":False},
          # Sociology
          {"subject":"SOCI","catalog":"335","title":"Environmental Sociology","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"340","title":"Sociology of Health and Illness","credits":3,"is_required":False},
          {"subject":"SOCI","catalog":"360","title":"International Migration","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── GEOGRAPHY HONOURS ────────────────────────────────────────────
  {
    "program_key": "geography_honours",
    "name": "Geography – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 61,
    "description": (
      "The Honours in Geography trains students in both human and physical geography methods "
      "including GIS, spatial analysis, and fieldwork. The thesis provides experience with "
      "independent geographic research."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/geography-honours-ba/",
    "blocks": [
      {
        "block_key": "geog_hon_core",
        "title": "Required Core (13 credits)",
        "block_type": "required",
        "credits_needed": 13,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"GEOG","catalog":"201","title":"Introductory Geo-Information Science","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"216","title":"Geography of the World Economy",      "credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"290","title":"Local Geographical Excursion",        "credits":1,"is_required":True},
          {"subject":"GEOG","catalog":"351","title":"Quantitative Methods",                "credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"381","title":"Geographic Thought and Practice",     "credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "geog_hon_thesis",
        "title": "Honours Research (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Original field or data-based research.",
        "sort_order": 2,
        "courses": [
          {"subject":"GEOG","catalog":"491D1","title":"Honours Research","credits":3,"is_required":True},
          {"subject":"GEOG","catalog":"491D2","title":"Honours Research","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "geog_hon_electives",
        "title": "Geography Electives (33 credits)",
        "block_type": "choose_credits",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name": None,
        "notes": "33 credits of GEOG. At least 9 credits at 400-level.",
        "sort_order": 3,
        "courses": [
          {"subject":"GEOG","catalog":"310","title":"Urban Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"320","title":"Political Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"330","title":"Economic Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"340","title":"Cultural Geography","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"410","title":"Advanced Urban Studies","credits":3,"is_required":False},
          {"subject":"GEOG","catalog":"420","title":"Advanced GIS","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── CLASSICS HONOURS ─────────────────────────────────────────────
  {
    "program_key": "classics_honours",
    "name": "Classics – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 54,
    "description": (
      "The Honours in Classics offers intensive study of ancient Greek and Latin languages, "
      "literature, history, and archaeology. The thesis can focus on textual, historical, "
      "or archaeological topics and is conducted in consultation with a faculty supervisor."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/history-classical-studies/classics-honours-ba/",
    "blocks": [
      {
        "block_key": "clas_hon_languages",
        "title": "Language Requirements (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "6 credits of Greek and 6 credits of Latin required; 6 additional credits in one language.",
        "sort_order": 1,
        "courses": [
          {"subject":"GREK","catalog":"201","title":"Intermediate Greek 1","credits":3,"is_required":True},
          {"subject":"GREK","catalog":"202","title":"Intermediate Greek 2","credits":3,"is_required":True},
          {"subject":"LATI","catalog":"201","title":"Intermediate Latin 1","credits":3,"is_required":True},
          {"subject":"LATI","catalog":"202","title":"Intermediate Latin 2","credits":3,"is_required":True},
          {"subject":"GREK","catalog":"301","title":"Advanced Greek","credits":3,"is_required":False},
          {"subject":"LATI","catalog":"301","title":"Advanced Latin","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "clas_hon_core",
        "title": "Required Classics Courses (12 credits)",
        "block_type": "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 2,
        "courses": [
          {"subject":"CLAS","catalog":"325","title":"Greek Historiography","credits":3,"is_required":True},
          {"subject":"CLAS","catalog":"326","title":"Latin Literature and Culture","credits":3,"is_required":True},
          {"subject":"CLAS","catalog":"395","title":"Methods in Classical Studies","credits":3,"is_required":True},
          {"subject":"CLAS","catalog":"430","title":"Advanced Seminar in Classics","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "clas_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Thesis in Greek, Latin, history, or classical archaeology.",
        "sort_order": 3,
        "courses": [
          {"subject":"CLAS","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"CLAS","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "clas_hon_electives",
        "title": "Classics Electives (18 credits)",
        "block_type": "choose_credits",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "18 credits from CLAS, GREK, LATN, or HIST (ancient). At least 9 credits at 400-level.",
        "sort_order": 4,
        "courses": [
          {"subject":"CLAS","catalog":"310","title":"Greek and Roman Mythology","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"330","title":"Greek Philosophy","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"340","title":"Roman History","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"350","title":"Ancient Near East","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"410","title":"Topics in Greek Literature","credits":3,"is_required":False},
          {"subject":"CLAS","catalog":"420","title":"Topics in Roman Literature","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── GSFSJ HONOURS ───────────────────────────────────────────────
  {
    "program_key": "gsfsj_honours",
    "name": "Gender, Sexuality, Feminist & Social Justice Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 57,
    "description": (
      "The Honours program offers advanced interdisciplinary training in feminist theory, "
      "queer studies, and social justice praxis. The thesis allows students to conduct "
      "original research using intersectional and feminist methodologies."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/gender-sexuality-feminist-studies/gender-sexuality-feminist-social-justice-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "gsfsj_hon_core",
        "title": "Required Core (12 credits)",
        "block_type": "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"GSFS","catalog":"200",   "title":"Feminist Perspectives",                   "credits":3,   "is_required":True},
          {"subject":"GSFS","catalog":"250",   "title":"Gender, Race, and Sexuality in Society",   "credits":3,   "is_required":True},
          {"subject":"GSFS","catalog":"300",   "title":"Feminist Theory",                          "credits":3,   "is_required":True},
          {"subject":"GSFS","catalog":"495D1", "title":"Research Methods in GSFSJ",               "credits":1.5, "is_required":True},
          {"subject":"GSFS","catalog":"495D2", "title":"Research Methods in GSFSJ",               "credits":1.5, "is_required":True},
        ],
      },
      {
        "block_key": "gsfsj_hon_thesis",
        "title": "Honours Research (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Original interdisciplinary feminist research.",
        "sort_order": 2,
        "courses": [
          {"subject":"GSFS","catalog":"496D1","title":"Honours Research","credits":3,"is_required":True},
          {"subject":"GSFS","catalog":"496D2","title":"Honours Research","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "gsfsj_hon_electives",
        "title": "GSFSJ & Cognate Electives (33 credits)",
        "block_type": "choose_credits",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name": None,
        "notes": "33 credits from GSFS or approved cognate courses. At least 9 credits at 400-level.",
        "sort_order": 3,
        "courses": [
          {"subject":"GSFS","catalog":"320","title":"Gender and Sexuality in the Media","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":"330","title":"Transnational Feminisms","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":"340","title":"Race, Gender, and Social Justice","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":"410","title":"Topics in Feminist Theory","credits":3,"is_required":False},
          {"subject":"GSFS","catalog":"420","title":"Queer Theory","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── JEWISH STUDIES HONOURS ────────────────────────────────────────
  {
    "program_key": "jewish_studies_honours",
    "name": "Jewish Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours in Jewish Studies offers advanced interdisciplinary study of Jewish "
      "history, thought, literature, and culture. Students conduct original research "
      "leading to an honours thesis under faculty supervision."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/jewish-studies/jewish-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "jwst_hon_core",
        "title": "Required Core (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"JWST","catalog":"200","title":"Introduction to Jewish Studies","credits":3,"is_required":True},
          {"subject":"JWST","catalog":"201","title":"The Jewish Tradition: Texts and Interpretations","credits":3,"is_required":True},
          {"subject":"JWST","catalog":"300","title":"Jewish History: Ancient to Medieval","credits":3,"is_required":True},
          {"subject":"JWST","catalog":"301","title":"Jewish History: Modern Period","credits":3,"is_required":True},
          {"subject":"JWST","catalog":"395","title":"Methods in Jewish Studies","credits":3,"is_required":True},
          {"subject":"JWST","catalog":"430","title":"Advanced Seminar in Jewish Studies","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "jwst_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Original research in any area of Jewish Studies.",
        "sort_order": 2,
        "courses": [
          {"subject":"JWST","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"JWST","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "jwst_hon_electives",
        "title": "Jewish Studies Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "notes": "36 credits from JWST. At least 9 credits at 400-level.",
        "sort_order": 3,
        "courses": [
          {"subject":"JWST","catalog":"310","title":"Holocaust Studies","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"320","title":"Zionism and the State of Israel","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"330","title":"Jewish Literature","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"340","title":"Kabbalah and Jewish Mysticism","credits":3,"is_required":False},
          {"subject":"JWST","catalog":"410","title":"Topics in Modern Jewish History","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── EAST ASIAN STUDIES HONOURS ───────────────────────────────────
  {
    "program_key": "east_asian_studies_honours",
    "name": "East Asian Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours in East Asian Studies combines advanced language training with interdisciplinary "
      "study of the history, literature, religion, and cultures of East Asia. Students complete "
      "an independent thesis in consultation with a faculty supervisor."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/east-asian-studies/east-asian-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "east_hon_language",
        "title": "Language Requirement (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "Advanced proficiency in Chinese, Japanese, or Korean; 18 credits in one East Asian language.",
        "sort_order": 1,
        "courses": [
          {"subject":"CHIN","catalog":"301","title":"Advanced Chinese 1","credits":3,"is_required":False},
          {"subject":"CHIN","catalog":"302","title":"Advanced Chinese 2","credits":3,"is_required":False},
          {"subject":"CHIN","catalog":"401","title":"Classical Chinese Texts","credits":3,"is_required":False},
          {"subject":"JAPN","catalog":"301","title":"Advanced Japanese 1","credits":3,"is_required":False},
          {"subject":"JAPN","catalog":"302","title":"Advanced Japanese 2","credits":3,"is_required":False},
          {"subject":"KORE","catalog":"301","title":"Advanced Korean 1","credits":3,"is_required":False},
        ],
      },
      {
        "block_key": "east_hon_core",
        "title": "Required EAST Core (12 credits)",
        "block_type": "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 2,
        "courses": [
          {"subject":"EAST","catalog":"230","title":"Introduction to East Asian Civilizations 1","credits":3,"is_required":True},
          {"subject":"EAST","catalog":"231","title":"Introduction to East Asian Civilizations 2","credits":3,"is_required":True},
          {"subject":"EAST","catalog":"395","title":"Research Methods in East Asian Studies","credits":3,"is_required":True},
          {"subject":"EAST","catalog":"430","title":"Advanced Seminar in East Asian Studies","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "east_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Original research using primary sources in an East Asian language.",
        "sort_order": 3,
        "courses": [
          {"subject":"EAST","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"EAST","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "east_hon_electives",
        "title": "EAST & Language Electives (24 credits)",
        "block_type": "choose_credits",
        "credits_needed": 24,
        "courses_needed": None,
        "group_name": None,
        "notes": "24 credits from EAST or advanced language courses. At least 9 credits at 400-level.",
        "sort_order": 4,
        "courses": [
          {"subject":"EAST","catalog":"310","title":"Chinese Literature in Translation","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"320","title":"Japanese Culture and Society","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"330","title":"History of East Asian Buddhism","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"410","title":"Topics in Chinese History","credits":3,"is_required":False},
          {"subject":"EAST","catalog":"420","title":"Topics in Japanese Literature","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── RELIGIOUS STUDIES HONOURS ────────────────────────────────────
  {
    "program_key": "religious_studies_honours",
    "name": "Religious Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours in Religious Studies examines the world's religious traditions through "
      "historical, anthropological, literary, and philosophical lenses. The thesis can "
      "engage any religious tradition or theoretical problem in the discipline."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/religious-studies/religious-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "relg_hon_core",
        "title": "Required Core (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"RELG","catalog":"207","title":"Introduction to Judaism","credits":3,"is_required":True},
          {"subject":"RELG","catalog":"208","title":"Introduction to Christianity","credits":3,"is_required":True},
          {"subject":"RELG","catalog":"203","title":"Introduction to Hinduism","credits":3,"is_required":True},
          {"subject":"RELG","catalog":"204","title":"Introduction to Buddhism","credits":3,"is_required":True},
          {"subject":"RELG","catalog":"395","title":"Research Methods in Religious Studies","credits":3,"is_required":True},
          {"subject":"RELG","catalog":"430","title":"Advanced Seminar in Religious Studies","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "relg_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Independent research on a religious tradition or theoretical problem.",
        "sort_order": 2,
        "courses": [
          {"subject":"RELG","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"RELG","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "relg_hon_electives",
        "title": "RELG Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "notes": "36 credits of RELG. At least 9 credits at 400-level; at least two traditions represented.",
        "sort_order": 3,
        "courses": [
          {"subject":"RELG","catalog":"305","title":"Islam","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"310","title":"Mysticism in the World Religions","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"320","title":"Ritual and Symbol","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"330","title":"Religion and Ethics","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"410","title":"Topics in Religious Studies","credits":3,"is_required":False},
          {"subject":"RELG","catalog":"420","title":"Religion and Modernity","credits":3,"is_required":False},
        ],
      },
    ],
  },

  # ── WORLD ISLAMIC AND MIDDLE EAST STUDIES HONOURS ────────────────
  {
    "program_key": "world_islamic_mideast_honours",
    "name": "World Islamic and Middle East Studies – Honours (B.A.)",
    "program_type": "honours",
    "faculty": "Faculty of Arts",
    "total_credits": 60,
    "description": (
      "The Honours in World Islamic and Middle East Studies provides advanced interdisciplinary "
      "training in the history, religion, politics, and culture of the Middle East and the "
      "broader Islamic world. The thesis requires primary source engagement."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/world-islamic-middle-east-studies-honours-ba/",
    "blocks": [
      {
        "block_key": "isla_hon_core",
        "title": "Required Core (18 credits)",
        "block_type": "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name": None,
        "notes": "All required.",
        "sort_order": 1,
        "courses": [
          {"subject":"ISLA","catalog":"200","title":"Introduction to Islam","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"210","title":"Introduction to the Middle East","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"300","title":"Islamic Thought and Civilization","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"310","title":"Middle Eastern History: Modern Period","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"395","title":"Research Methods in Islamic Studies","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"430","title":"Advanced Seminar in Islamic Studies","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "isla_hon_thesis",
        "title": "Honours Thesis (6 credits)",
        "block_type": "required",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name": None,
        "notes": "Thesis using primary sources; Arabic or other relevant language strongly recommended.",
        "sort_order": 2,
        "courses": [
          {"subject":"ISLA","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
          {"subject":"ISLA","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
        ],
      },
      {
        "block_key": "isla_hon_electives",
        "title": "ISLA Electives (36 credits)",
        "block_type": "choose_credits",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name": None,
        "notes": "36 credits from ISLA or approved cognate courses (RELG, HIST, POLI). At least 9 at 400-level.",
        "sort_order": 3,
        "courses": [
          {"subject":"ISLA","catalog":"320","title":"Gender and Islam","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"330","title":"Political Islam","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"340","title":"Sufism and Islamic Mysticism","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"410","title":"Topics in Islamic History","credits":3,"is_required":False},
          {"subject":"ISLA","catalog":"420","title":"Modern Arab Literature","credits":3,"is_required":False},
        ],
      },
    ],
  },


  # ══════════════════════════════════════════════════════════════════

]
