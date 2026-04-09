"""
McGill Faculty of Arts – Additional & Specialty: African Studies Major, English (Drama/Cultural), Russian, Latin American Major, Software Engineering, language minors, Traduction, East Asian sub-minors, Geography Urban Studies, Canadian/English/German/Hispanic/Italian/Latin American/Liberal Arts/Russian Honours
Sub-module of arts_degree_requirements.py
"""

ARTS_LANGUAGES_SPECIALTY = [
  # ADDITIONAL PROGRAMS (added from 2025-2026 catalogue)
  # ══════════════════════════════════════════════════════════════════

  # ── AFRICAN STUDIES – MAJOR CONCENTRATION ──
    {
      "program_key": "african_studies_major",
      "name": "African Studies – Major Concentration",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "An interdisciplinary approach to the study of the African continent. "
        "Students identify an area within a discipline of the Faculty, taking as "
        "many relevant courses as possible in that field. Offered by the "
        "Institute of Islamic Studies."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/african-studies-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "afri_major_group_a",
          "title": "Group A – Required Introductory Courses",
          "block_type": "required",
          "credits_needed": 15,
          "notes": "15 credits from Group A; at least 9 credits at 200-level intro courses across disciplines.",
          "sort_order": 1,
          "courses": [
            {"subject":"AFRI","catalog":"200","title":"Introduction to African Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Gateway course; required for the major"},
            {"subject":"HIST","catalog":"230","title":"Africa: Pre-Colonial","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Important historical foundation"},
            {"subject":"HIST","catalog":"231","title":"Africa: Colonial and Post-Colonial","credits":3,"is_required":False,"recommended":True},
            {"subject":"POLI","catalog":"314","title":"Comparative Politics of Africa","credits":3,"is_required":False,"recommended":True},
            {"subject":"ANTH","catalog":"315","title":"Society/Culture: East Africa","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "afri_major_group_b",
          "title": "Group B – Interdisciplinary Electives",
          "block_type": "choose_credits",
          "credits_needed": 21,
          "notes": "21 credits from Group B drawn from at least 3 disciplines; max 9 credits from any one discipline.",
          "sort_order": 2,
          "courses": [
            {"subject":"ANTH","catalog":"322","title":"Social Change in Modern Africa","credits":3,"is_required":False,"recommended":True},
            {"subject":"ANTH","catalog":"416","title":"Environment/Development: Africa","credits":3,"is_required":False},
            {"subject":"ANTH","catalog":"451","title":"Research in Society and Development in Africa","credits":3,"is_required":False},
            {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"HIST","catalog":"455","title":"Introduction to the African Diaspora","credits":3,"is_required":False,"recommended":True},
            {"subject":"POLI","catalog":"311","title":"Politics of Development","credits":3,"is_required":False},
            {"subject":"SOCI","catalog":"254","title":"Development and Underdevelopment","credits":3,"is_required":False},
            {"subject":"ISLA","catalog":"315","title":"Topics in Islamic History","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"384","title":"African Literature","credits":3,"is_required":False,"recommended":True},
          ],
        },
      ],
    },

  # ── ENGLISH – DRAMA AND THEATRE MAJOR CONCENTRATION ──
    {
      "program_key": "english_drama_theatre_major",
      "name": "English – Drama and Theatre Major Concentration",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "Places drama and theatre in a broad social and philosophical context as "
        "a liberal arts discipline. Not designed for professional theatre "
        "training. Emphasises analysis, history, and theory of performance."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-drama-theatre-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "dt_required",
          "title": "Required Courses",
          "block_type": "required",
          "credits_needed": 6,
          "notes": "To be taken in the first two terms of the program.",
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"230","title":"Introduction to Theatre Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Gateway to all Drama & Theatre courses"},
            {"subject":"ENGL","catalog":"355","title":"The Poetics of Performance","credits":3,"is_required":True,"recommended":True},
          ],
        },
        {
          "block_key": "dt_practice",
          "title": "Practice-Based Courses",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "notes": "3 credits from practice-based courses.",
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"269","title":"Introduction to Performance","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Best entry point for performance track"},
            {"subject":"ENGL","catalog":"365","title":"Costuming for the Theatre 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"368","title":"Stage Scenery and Lighting 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"372","title":"Stage Scenery and Lighting 2","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"377","title":"Costuming for the Theatre 2","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "dt_performance",
          "title": "Performance-Oriented Courses",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "notes": "3 credits from performance-oriented courses.",
          "sort_order": 3,
          "courses": [
            {"subject":"ENGL","catalog":"367","title":"Acting 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"376","title":"Scene Study","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"396","title":"Theatre Practicum 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"397","title":"Theatre Practicum 2","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"465","title":"Theatre Laboratory","credits":9,"is_required":False},
            {"subject":"ENGL","catalog":"466","title":"Directing for the Theatre","credits":6,"is_required":False},
            {"subject":"ENGL","catalog":"469","title":"Acting 3","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "dt_canadian",
          "title": "Canadian Drama & Theatre",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "notes": "3 credits from Canadian drama/theatre courses.",
          "sort_order": 4,
          "courses": [
            {"subject":"ENGL","catalog":"313","title":"Canadian Drama and Theatre","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"413","title":"Special Topics in Canadian Drama and Theatre","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "dt_theory",
          "title": "Theory, Criticism and Methods",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "notes": "3 credits from Theory, Criticism, Methods.",
          "sort_order": 5,
          "courses": [
            {"subject":"ENGL","catalog":"317","title":"Literary and Cultural Theory","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"318","title":"Literary and Cultural Methods","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"319","title":"Literary and Cultural Criticism","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"322","title":"Theories of the Text","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"346","title":"Materiality and Sociology of Text","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"352","title":"Theories of Difference","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "dt_history",
          "title": "Theatre History",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "notes": "3 credits from theatre history courses.",
          "sort_order": 6,
          "courses": [
            {"subject":"ENGL","catalog":"306","title":"Theatre History: Medieval and Early Modern","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"310","title":"Restoration and 18th Century Drama","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"312","title":"Victorian and Edwardian Drama 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"370","title":"Theatre History: The Long Eighteenth Century","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"371","title":"Theatre History: 19th to 21st Centuries","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"467","title":"Advanced Studies in Theatre History","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"486","title":"Special Topics in Theatre History","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "dt_pre1900",
          "title": "Drama and Theatre Before 1900",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "notes": "3 credits from drama/theatre before 1900.",
          "sort_order": 7,
          "courses": [
            {"subject":"ENGL","catalog":"308","title":"English Renaissance Drama 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"315","title":"Shakespeare","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential drama course"},
            {"subject":"ENGL","catalog":"416","title":"Studies in Shakespeare","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "dt_additional",
          "title": "Additional ENGL Electives",
          "block_type": "choose_credits",
          "credits_needed": 12,
          "notes": "12 additional credits from ENGL offerings in Literature, Cultural Studies, or Drama & Theatre options. Max 6 credits from other departments.",
          "sort_order": 8,
          "courses": [
            {"subject":"ENGL","catalog":None,"title":"Any ENGL Drama/Theatre or Literature course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ENGLISH – DRAMA AND THEATRE MINOR CONCENTRATION ──
    {
      "program_key": "english_drama_theatre_minor",
      "name": "English – Drama and Theatre Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit introduction to dramatic literature, theatre history, and "
        "performance as a liberal arts discipline."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-drama-theatre-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "dt_minor_required",
          "title": "Required Courses",
          "block_type": "required",
          "credits_needed": 6,
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"230","title":"Introduction to Theatre Studies","credits":3,"is_required":True,"recommended":True},
            {"subject":"ENGL","catalog":"355","title":"The Poetics of Performance","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "dt_minor_electives",
          "title": "Drama & Theatre Electives",
          "block_type": "choose_credits",
          "credits_needed": 12,
          "notes": "12 credits from Drama & Theatre offerings; at least 3 at 300+ level.",
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"269","title":"Introduction to Performance","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"315","title":"Shakespeare","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"371","title":"Theatre History: 19th to 21st Centuries","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":None,"title":"Any ENGL Drama/Theatre course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ENGLISH – CULTURAL STUDIES MAJOR CONCENTRATION ──
    {
      "program_key": "english_cultural_studies_major",
      "name": "English – Cultural Studies Major Concentration",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "Concentrates on analysis of forms of cultural expression and symbolic "
        "interaction, and of the various media through which these may be "
        "disseminated and transformed. Not a major in journalism or "
        "communications."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-cultural-studies-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "cs_required",
          "title": "Required Courses",
          "block_type": "required",
          "credits_needed": 9,
          "notes": "Should be taken in the first two terms.",
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"275","title":"Introduction to Cultural Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Gateway to Cultural Studies option"},
            {"subject":"ENGL","catalog":"277","title":"Introduction to Film Studies","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Essential film analysis foundation"},
            {"subject":"ENGL","catalog":"359","title":"The Poetics of the Image","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "cs_major_figures",
          "title": "Major Figures in Cultural Studies",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"315","title":"Shakespeare","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"381","title":"A Film-Maker 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"418","title":"A Major Modernist Writer","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"444","title":"Studies in Women Authors","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"481","title":"A Film-Maker 2","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "cs_canadian",
          "title": "Canadian Component",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "sort_order": 3,
          "courses": [
            {"subject":"ENGL","catalog":"393","title":"Canadian Cinema","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"440","title":"First Nations and Inuit Literature and Media","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"441","title":"Special Topics in Canadian Cultural Studies","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "cs_theory",
          "title": "Theory, Criticism and Methods",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "sort_order": 4,
          "courses": [
            {"subject":"ENGL","catalog":"317","title":"Literary and Cultural Theory","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"318","title":"Literary and Cultural Methods","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"319","title":"Literary and Cultural Criticism","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"322","title":"Theories of the Text","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"346","title":"Materiality and Sociology of Text","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"352","title":"Theories of Difference","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "cs_400_theory",
          "title": "400-Level Theory",
          "block_type": "choose_credits",
          "credits_needed": 3,
          "sort_order": 5,
          "courses": [
            {"subject":"ENGL","catalog":"454","title":"Topics in Cultural Studies and Gender","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"479","title":"Philosophy of Film","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"484","title":"Seminar in the Film","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"489","title":"Culture and Critical Theory 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"490","title":"Culture and Critical Theory 2","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"492","title":"Image and Text","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "cs_historical",
          "title": "Historical Dimension",
          "block_type": "choose_credits",
          "credits_needed": 6,
          "sort_order": 6,
          "courses": [
            {"subject":"ENGL","catalog":"350","title":"Studies in the History of Film 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"351","title":"Studies in the History of Film 2","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"363","title":"Studies in the History of Film 3","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"374","title":"Film Movement or Period","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"451","title":"A Period in Cinema","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"480","title":"Studies in History of Film 1","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "cs_additional",
          "title": "Additional ENGL Electives",
          "block_type": "choose_credits",
          "credits_needed": 9,
          "notes": "9 additional credits from ENGL offerings. Max 6 credits from other departments.",
          "sort_order": 7,
          "courses": [
            {"subject":"ENGL","catalog":None,"title":"Any ENGL Cultural Studies or Literature course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ENGLISH – CULTURAL STUDIES MINOR CONCENTRATION ──
    {
      "program_key": "english_cultural_studies_minor",
      "name": "English – Cultural Studies Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit introduction to cultural studies, film, and media analysis. "
        "Expandable to the major."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-cultural-studies-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "cs_minor_required",
          "title": "Required Courses",
          "block_type": "required",
          "credits_needed": 9,
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"275","title":"Introduction to Cultural Studies","credits":3,"is_required":True,"recommended":True},
            {"subject":"ENGL","catalog":"277","title":"Introduction to Film Studies","credits":3,"is_required":True,"recommended":True},
            {"subject":"ENGL","catalog":"359","title":"The Poetics of the Image","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "cs_minor_electives",
          "title": "Cultural Studies Electives",
          "block_type": "choose_credits",
          "credits_needed": 9,
          "notes": "9 credits from Cultural Studies offerings; at least 3 at 300+ level.",
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"381","title":"A Film-Maker 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"350","title":"Studies in the History of Film 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"489","title":"Culture and Critical Theory 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":None,"title":"Any ENGL Cultural Studies course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── RUSSIAN – MAJOR CONCENTRATION ──
    {
      "program_key": "russian_major",
      "name": "Russian – Major Concentration",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "In-depth study of Russian language, literature, culture, and history. "
        "Students progress through language levels and study major works of "
        "Russian literature from the 18th century to the present."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/russian-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "russ_language",
          "title": "Russian Language Foundation",
          "block_type": "choose_credits",
          "credits_needed": 12,
          "notes": "12 credits of Russian language. Students with prior knowledge may replace lower-level with upper-level courses.",
          "sort_order": 1,
          "courses": [
            {"subject":"RUSS","catalog":"210","title":"Introductory Russian 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Start here with no prior Russian"},
            {"subject":"RUSS","catalog":"211","title":"Introductory Russian 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"310","title":"Intermediate Russian 1","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"311","title":"Intermediate Russian 2","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"410","title":"Advanced Russian Language 1","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"411","title":"Advanced Russian Language 2","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"415","title":"Advanced Russian Language Intensive 1","credits":6,"is_required":False},
          ],
        },
        {
          "block_key": "russ_lit_culture",
          "title": "Russian Literature & Culture",
          "block_type": "choose_credits",
          "credits_needed": 24,
          "min_credits_400": 9,
          "notes": "24 credits from RUSS literature/culture. At least 9 credits at 300+. Max 6 credits from other departments with approval.",
          "sort_order": 2,
          "courses": [
            {"subject":"RUSS","catalog":"217","title":"19th-Century Russian Literature in Translation","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Survey of golden age — Pushkin, Gogol, Dostoevsky, Tolstoy"},
            {"subject":"RUSS","catalog":"218","title":"Russian Literature and Revolution","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"20th century from revolution through post-Soviet era"},
            {"subject":"RUSS","catalog":"229","title":"Introduction to Russian Folklore","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"232","title":"Russian Cinema","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Popular course; no language prereq"},
            {"subject":"RUSS","catalog":"340","title":"Russian Short Story","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"355","title":"Russian and Soviet Culture","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"365","title":"Supernatural and Absurd in Russian Literature","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"490","title":"Honours Seminar","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":None,"title":"Any RUSS literature/culture course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── RUSSIAN – MINOR CONCENTRATION ──
    {
      "program_key": "russian_minor",
      "name": "Russian – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "An 18-credit introduction to Russian language, literature, and culture.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/russian-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "russ_minor_courses",
          "title": "Russian Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of RUSS courses including language and literature/culture.",
          "sort_order": 1,
          "courses": [
            {"subject":"RUSS","catalog":"210","title":"Introductory Russian 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"211","title":"Introductory Russian 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"217","title":"19th-Century Russian Literature in Translation","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"232","title":"Russian Cinema","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":None,"title":"Any RUSS course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── RUSSIAN CULTURE – MINOR CONCENTRATION ──
    {
      "program_key": "russian_culture_minor",
      "name": "Russian Culture – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit introduction to Russian culture through courses taught in "
        "English. No Russian language prerequisite."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/russian-culture-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "russ_cult_courses",
          "title": "Russian Culture Courses (in English)",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from RUSS culture courses taught in English.",
          "sort_order": 1,
          "courses": [
            {"subject":"RUSS","catalog":"217","title":"19th-Century Russian Literature in Translation","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"218","title":"Russian Literature and Revolution","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"229","title":"Introduction to Russian Folklore","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"232","title":"Russian Cinema","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"365","title":"Supernatural and Absurd in Russian Literature","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":None,"title":"Any RUSS culture course (taught in English)","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── LATIN AMERICAN AND CARIBBEAN STUDIES – MAJOR CONCENTRATION ──
    {
      "program_key": "latin_american_caribbean_major",
      "name": "Latin American and Caribbean Studies – Major Concentration",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "An interdisciplinary program combining History, Political Science, "
        "Sociology, Anthropology, and Hispanic Studies for in-depth study of "
        "Latin America and the Caribbean."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/latin-american-caribbean-studies-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "lacs_major_required",
          "title": "Required Core",
          "block_type": "required",
          "credits_needed": 6,
          "sort_order": 1,
          "courses": [
            {"subject":"HIST","catalog":"261","title":"Latin America: Colonial","credits":3,"is_required":True,"recommended":True},
            {"subject":"HIST","catalog":"262","title":"Latin America: Modern","credits":3,"is_required":True,"recommended":True},
          ],
        },
        {
          "block_key": "lacs_major_interdisciplinary",
          "title": "Interdisciplinary Electives",
          "block_type": "choose_credits",
          "credits_needed": 30,
          "min_credits_400": 6,
          "notes": "30 credits from at least 3 disciplines. At least 6 at 400-level. Max 12 credits from any single discipline.",
          "sort_order": 2,
          "courses": [
            {"subject":"POLI","catalog":"312","title":"Politics of Latin America","credits":3,"is_required":False,"recommended":True},
            {"subject":"HISP","catalog":"243","title":"Survey of Spanish-American Literature 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"HISP","catalog":"244","title":"Survey of Spanish-American Literature 2","credits":3,"is_required":False},
            {"subject":"ANTH","catalog":"326","title":"Anthropology of Latin America","credits":3,"is_required":False,"recommended":True},
            {"subject":"ANTH","catalog":"307","title":"Andean Prehistory","credits":3,"is_required":False},
            {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":False},
            {"subject":"SOCI","catalog":"254","title":"Development and Underdevelopment","credits":3,"is_required":False},
            {"subject":"HISP","catalog":"328","title":"Literature of Ideas: Latin America","credits":3,"is_required":False},
            {"subject":"HISP","catalog":"335","title":"Politics and Poetry in Latin America","credits":3,"is_required":False},
            {"subject":"HIST","catalog":None,"title":"Any HIST course on Latin America","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── SOFTWARE ENGINEERING – MAJOR CONCENTRATION (B.A.) ──
    {
      "program_key": "software_engineering_arts_major",
      "name": "Software Engineering – Major Concentration (B.A.)",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "Covers software design, development methodologies, and computer science "
        "foundations for B.A. students. Requires MATH 133, 140, and 141 as "
        "prerequisites."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/computer-science/software-engineering-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "se_required",
          "title": "Required Courses",
          "block_type": "required",
          "credits_needed": 24,
          "notes": "MATH 133, MATH 140, and MATH 141 (or equivalents) should be completed before starting.",
          "sort_order": 1,
          "courses": [
            {"subject":"COMP","catalog":"202","title":"Foundations of Programming","credits":3,"is_required":True,"recommended":True},
            {"subject":"COMP","catalog":"206","title":"Introduction to Software Systems","credits":3,"is_required":True},
            {"subject":"COMP","catalog":"250","title":"Introduction to Computer Science","credits":3,"is_required":True,"recommended":True},
            {"subject":"COMP","catalog":"251","title":"Algorithms and Data Structures","credits":3,"is_required":True},
            {"subject":"COMP","catalog":"273","title":"Introduction to Computer Systems","credits":3,"is_required":True},
            {"subject":"COMP","catalog":"303","title":"Software Design","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core SE course — design patterns and architecture"},
            {"subject":"COMP","catalog":"361","title":"Software Engineering Processes","credits":3,"is_required":True},
            {"subject":"MATH","catalog":"240","title":"Discrete Structures","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "se_complementary",
          "title": "Complementary Courses",
          "block_type": "choose_credits",
          "credits_needed": 12,
          "notes": "12 credits from approved COMP and MATH courses.",
          "sort_order": 2,
          "courses": [
            {"subject":"COMP","catalog":"302","title":"Programming Languages and Paradigms","credits":3,"is_required":False,"recommended":True},
            {"subject":"COMP","catalog":"307","title":"Introduction to Web Development","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Practical skills for modern software"},
            {"subject":"COMP","catalog":"321","title":"Introduction to Software Engineering","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"330","title":"Theory of Computation","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"409","title":"Concurrent Programming","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"421","title":"Programming Languages","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"424","title":"Artificial Intelligence","credits":3,"is_required":False,"recommended":True},
            {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":3,"is_required":False},
            {"subject":"MATH","catalog":"323","title":"Probability","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ARABIC LANGUAGE – MINOR CONCENTRATION ──
    {
      "program_key": "arabic_language_minor",
      "name": "Arabic Language – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit introduction to Arabic language skills from elementary "
        "through intermediate levels."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/arabic-language-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "arbc_minor_courses",
          "title": "Arabic Language Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of ARBC courses from elementary through advanced levels.",
          "sort_order": 1,
          "courses": [
            {"subject":"ARBC","catalog":"210","title":"Introductory Arabic 1","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Start here with no prior Arabic"},
            {"subject":"ARBC","catalog":"220","title":"Introductory Arabic 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"ARBC","catalog":"310","title":"Intermediate Arabic 1","credits":3,"is_required":False},
            {"subject":"ARBC","catalog":"320","title":"Intermediate Arabic 2","credits":3,"is_required":False},
            {"subject":"ARBC","catalog":"410","title":"Advanced Arabic 1","credits":3,"is_required":False},
            {"subject":"ARBC","catalog":"420","title":"Advanced Arabic 2","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── INDIGENOUS STUDIES – MINOR CONCENTRATION ──
    {
      "program_key": "indigenous_studies_minor",
      "name": "Indigenous Studies – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An interdisciplinary introduction to the histories, cultures, politics, "
        "and contemporary issues of Indigenous peoples, with emphasis on the "
        "Canadian context."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/institute-study/indigenous-studies-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "indg_minor_courses",
          "title": "Indigenous Studies Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from approved courses. At least 9 credits must focus on Indigenous topics.",
          "sort_order": 1,
          "courses": [
            {"subject":"ANTH","catalog":"338","title":"Indigenous Studies of Anthropology","credits":3,"is_required":False,"recommended":True},
            {"subject":"ANTH","catalog":"436","title":"North American Native Peoples","credits":3,"is_required":False,"recommended":True},
            {"subject":"HIST","catalog":"450","title":"Indigenous Peoples and Empires","credits":3,"is_required":False,"recommended":True},
            {"subject":"POLI","catalog":"372","title":"Indigenous Peoples and the Canadian State","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"440","title":"First Nations and Inuit Literature and Media","credits":3,"is_required":False,"recommended":True},
          ],
        },
      ],
    },

  # ── WORLD CINEMAS – MINOR CONCENTRATION ──
    {
      "program_key": "world_cinemas_minor",
      "name": "World Cinemas – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An interdisciplinary minor exploring film traditions from around the "
        "world, drawing on courses from English, East Asian Studies, Hispanic "
        "Studies, and other departments."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/world-cinemas-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "wcin_courses",
          "title": "World Cinemas Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from approved film/cinema courses across departments.",
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"277","title":"Introduction to Film Studies","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential film studies foundation"},
            {"subject":"ENGL","catalog":"350","title":"Studies in the History of Film 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"393","title":"Canadian Cinema","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"374","title":"Film Movement or Period","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"451","title":"A Period in Cinema","credits":3,"is_required":False},
            {"subject":"EAST","catalog":"340","title":"Japanese Cinema","credits":3,"is_required":False,"recommended":True},
            {"subject":"RUSS","catalog":"232","title":"Russian Cinema","credits":3,"is_required":False},
            {"subject":"GERM","catalog":"350","title":"Modernism and the Avant-Garde","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── MEDIEVAL STUDIES – MINOR CONCENTRATION ──
    {
      "program_key": "medieval_studies_minor",
      "name": "Medieval Studies – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An interdisciplinary exploration of medieval European history, "
        "literature, art, and philosophy."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/medieval-studies-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "medv_courses",
          "title": "Medieval Studies Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from approved courses across ENGL, HIST, ARTH, CLAS, PHIL, RELG.",
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"316","title":"Theme or Genre in Medieval Literature","credits":3,"is_required":False,"recommended":True},
            {"subject":"ENGL","catalog":"317","title":"Middle English","credits":3,"is_required":False},
            {"subject":"HIST","catalog":"218","title":"Early Modern Europe","credits":3,"is_required":False,"recommended":True},
            {"subject":"ARTH","catalog":"205","title":"Art and Architecture: Ancient to Medieval","credits":3,"is_required":False,"recommended":True},
            {"subject":"CLAS","catalog":"210","title":"Greek and Roman Mythology","credits":3,"is_required":False},
            {"subject":"HIST","catalog":"405","title":"Seminar: Medieval History","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── HISTORY AND PHILOSOPHY OF SCIENCE – MINOR CONCENTRATION ──
    {
      "program_key": "hist_phil_science_minor",
      "name": "History and Philosophy of Science – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "Explores the historical development and philosophical foundations of "
        "scientific thought."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/philosophy/history-philosophy-science-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "hps_courses",
          "title": "History & Philosophy of Science Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from PHIL and HIST courses related to science.",
          "sort_order": 1,
          "courses": [
            {"subject":"PHIL","catalog":"221","title":"Introduction to History and Philosophy of Science 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"PHIL","catalog":"341","title":"Philosophy of Science 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"PHIL","catalog":"441","title":"Philosophy of Science 2","credits":3,"is_required":False},
            {"subject":"HIST","catalog":"420","title":"History of Science, Technology and Society","credits":3,"is_required":False,"recommended":True},
            {"subject":"PHIL","catalog":"302","title":"Philosophy of Science","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── SOCIAL STUDIES OF MEDICINE – MINOR CONCENTRATION ──
    {
      "program_key": "social_studies_medicine_minor",
      "name": "Social Studies of Medicine – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "Examines the social, historical, and cultural dimensions of medicine and health.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/social-studies-medicine/social-studies-medicine-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "ssm_courses",
          "title": "Social Studies of Medicine Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from approved courses across SOCI, ANTH, HIST, PHIL.",
          "sort_order": 1,
          "courses": [
            {"subject":"SOCI","catalog":"310","title":"Medical Sociology","credits":3,"is_required":False,"recommended":True},
            {"subject":"ANTH","catalog":"227","title":"Medical Anthropology","credits":3,"is_required":False,"recommended":True},
            {"subject":"HIST","catalog":"460","title":"Health and the Healer in Western History","credits":3,"is_required":False},
            {"subject":"HIST","catalog":"440","title":"History of Pandemics","credits":3,"is_required":False,"recommended":True},
            {"subject":"PHIL","catalog":"350","title":"Philosophy of Medicine","credits":3,"is_required":False},
            {"subject":"SOCI","catalog":"302","title":"Health and Illness","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── SOUTH ASIAN STUDIES – MINOR CONCENTRATION ──
    {
      "program_key": "south_asian_studies_minor",
      "name": "South Asian Studies – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An interdisciplinary introduction to the history, cultures, religions, "
        "and politics of South Asia."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/south-asian-studies-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "sas_courses",
          "title": "South Asian Studies Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from approved courses on South Asia across departments.",
          "sort_order": 1,
          "courses": [
            {"subject":"ANTH","catalog":"327","title":"Anthropology of South Asia","credits":3,"is_required":False,"recommended":True},
            {"subject":"POLI","catalog":"313","title":"Political Change in South Asia","credits":3,"is_required":False,"recommended":True},
            {"subject":"HIST","catalog":"312","title":"Islamic Culture – Indian Subcontinent","credits":3,"is_required":False},
            {"subject":"RELG","catalog":"204","title":"Introduction to the Hebrew Bible","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── QUEBEC STUDIES AND COMMUNITY-ENGAGED LEARNING – MINOR CONCEN ──
    {
      "program_key": "quebec_studies_minor",
      "name": "Quebec Studies and Community-Engaged Learning – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An interdisciplinary minor exploring Quebec's history, society, "
        "politics, and culture, with a community-engaged learning component."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/institute-study/quebec-studies-community-engaged-learning-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "qcst_courses",
          "title": "Quebec Studies Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from approved courses on Quebec. Includes community-engaged learning component.",
          "sort_order": 1,
          "courses": [
            {"subject":"CANS","catalog":"315","title":"Quebec and Canada","credits":3,"is_required":False,"recommended":True,"recommendation_reason":"Essential for Montreal context"},
            {"subject":"POLI","catalog":"221","title":"Quebec Politics","credits":3,"is_required":False,"recommended":True},
            {"subject":"HIST","catalog":"307","title":"History of Quebec","credits":3,"is_required":False,"recommended":True},
            {"subject":"SOCI","catalog":None,"title":"Any SOCI course on Quebec","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── GERMAN LANGUAGE – MINOR CONCENTRATION ──
    {
      "program_key": "german_language_minor",
      "name": "German Language – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit program focused on German language acquisition from "
        "beginner to advanced levels."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/german-language-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "germl_courses",
          "title": "German Language Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of GERM language courses.",
          "sort_order": 1,
          "courses": [
            {"subject":"GERM","catalog":"100","title":"Beginner's German 1 (Intensive)","credits":6,"is_required":False,"recommended":True},
            {"subject":"GERM","catalog":"200","title":"Intermediate German (Intensive)","credits":6,"is_required":False,"recommended":True},
            {"subject":"GERM","catalog":"307D1","title":"Intermediate German (Advanced)","credits":3,"is_required":False},
            {"subject":"GERM","catalog":"307D2","title":"Intermediate German (Advanced) 2","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── PERSIAN LANGUAGE – MINOR CONCENTRATION ──
    {
      "program_key": "persian_language_minor",
      "name": "Persian Language – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "An 18-credit introduction to the Persian (Farsi) language.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/persian-language-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "pers_courses",
          "title": "Persian Language Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of PERN language courses from introductory through advanced.",
          "sort_order": 1,
          "courses": [
            {"subject":"PERN","catalog":"210","title":"Introductory Persian 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"PERN","catalog":"220","title":"Introductory Persian 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"PERN","catalog":"310","title":"Intermediate Persian 1","credits":3,"is_required":False},
            {"subject":"PERN","catalog":"320","title":"Intermediate Persian 2","credits":3,"is_required":False},
            {"subject":"PERN","catalog":"410","title":"Advanced Persian 1","credits":3,"is_required":False},
            {"subject":"PERN","catalog":"420","title":"Advanced Persian 2","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── TURKISH LANGUAGE – MINOR CONCENTRATION ──
    {
      "program_key": "turkish_language_minor",
      "name": "Turkish Language – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "An 18-credit introduction to the Turkish language.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/turkish-language-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "turk_courses",
          "title": "Turkish Language Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of TURK language courses.",
          "sort_order": 1,
          "courses": [
            {"subject":"TURK","catalog":"210","title":"Introductory Turkish 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"TURK","catalog":"220","title":"Introductory Turkish 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"TURK","catalog":"310","title":"Intermediate Turkish 1","credits":3,"is_required":False},
            {"subject":"TURK","catalog":"320","title":"Intermediate Turkish 2","credits":3,"is_required":False},
            {"subject":"TURK","catalog":"410","title":"Advanced Turkish 1","credits":3,"is_required":False},
            {"subject":"TURK","catalog":"420","title":"Advanced Turkish 2","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── URDU LANGUAGE – MINOR CONCENTRATION ──
    {
      "program_key": "urdu_language_minor",
      "name": "Urdu Language – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "An 18-credit introduction to the Urdu language.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/islamic-studies/urdu-language-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "urdu_courses",
          "title": "Urdu Language Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of Urdu language courses.",
          "sort_order": 1,
          "courses": [
            {"subject":"URDU","catalog":"210","title":"Introductory Urdu 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"URDU","catalog":"220","title":"Introductory Urdu 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"URDU","catalog":"310","title":"Intermediate Urdu 1","credits":3,"is_required":False},
            {"subject":"URDU","catalog":"320","title":"Intermediate Urdu 2","credits":3,"is_required":False},
            {"subject":"URDU","catalog":"410","title":"Advanced Urdu 1","credits":3,"is_required":False},
            {"subject":"URDU","catalog":"420","title":"Advanced Urdu 2","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── LANGUE FRANÇAISE – CONCENTRATION MINEURE ──
    {
      "program_key": "langue_francaise_minor",
      "name": "Langue française – Concentration mineure",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "Concentration mineure en langue française destinée aux étudiants non "
        "francophones souhaitant développer leur maîtrise du français écrit et "
        "oral."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/langue-francaise-minor-ba/",
      "blocks": [
        {
          "block_key": "langfr_courses",
          "title": "Cours de langue française",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 crédits de cours FREN (français langue seconde).",
          "sort_order": 1,
          "courses": [
            {"subject":"FREN","catalog":"215","title":"Français oral et écrit 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"FREN","catalog":"216","title":"Français oral et écrit 2","credits":3,"is_required":False,"recommended":True},
            {"subject":"FREN","catalog":"309","title":"French Composition","credits":3,"is_required":False},
            {"subject":"FREN","catalog":"310","title":"French Composition and Style","credits":3,"is_required":False},
            {"subject":"FREN","catalog":None,"title":"Tout cours FREN","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── TRADUCTION – CONCENTRATION MAJEURE ──
    {
      "program_key": "traduction_major",
      "name": "Traduction – Concentration majeure",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "Programme de traduction (anglais-français / français-anglais) formant "
        "les étudiants aux techniques de traduction professionnelle."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/traduction-major-ba/",
      "blocks": [
        {
          "block_key": "trad_major_courses",
          "title": "Cours de traduction",
          "block_type": "choose_credits",
          "credits_needed": 36,
          "min_credits_400": 12,
          "notes": "36 crédits de cours TRSL (traduction). Au moins 12 crédits au niveau 400.",
          "sort_order": 1,
          "courses": [
            {"subject":"TRSL","catalog":"200","title":"Introduction à la traduction","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Cours fondamental — prendre en U1"},
            {"subject":"TRSL","catalog":"300","title":"Traduction avancée","credits":3,"is_required":True},
            {"subject":"TRSL","catalog":None,"title":"Tout cours TRSL","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── TRADUCTION – CONCENTRATION MINEURE ──
    {
      "program_key": "traduction_minor",
      "name": "Traduction – Concentration mineure",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "Introduction à la traduction (anglais-français / français-anglais).",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/litteratures-langue-francaise-traduction-creation/traduction-minor-ba/",
      "blocks": [
        {
          "block_key": "trad_minor_courses",
          "title": "Cours de traduction",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 crédits de cours TRSL.",
          "sort_order": 1,
          "courses": [
            {"subject":"TRSL","catalog":"200","title":"Introduction à la traduction","credits":3,"is_required":True,"recommended":True},
            {"subject":"TRSL","catalog":None,"title":"Tout cours TRSL","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── COMPUTER SCIENCE – SUPPLEMENTARY MINOR CONCENTRATION (B.A.) ──
    {
      "program_key": "computer_science_supplementary_minor",
      "name": "Computer Science – Supplementary Minor Concentration (B.A.)",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit supplementary CS minor for students already in the CS major "
        "who want additional breadth."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/computer-science/computer-science-supplementary-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "cs_supp_courses",
          "title": "Additional COMP Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits of COMP courses not already counted toward the CS major.",
          "sort_order": 1,
          "courses": [
            {"subject":"COMP","catalog":"302","title":"Programming Languages and Paradigms","credits":3,"is_required":False,"recommended":True},
            {"subject":"COMP","catalog":"330","title":"Theory of Computation","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"350","title":"Numerical Computing","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"421","title":"Programming Languages","credits":3,"is_required":False},
            {"subject":"COMP","catalog":"424","title":"Artificial Intelligence","credits":3,"is_required":False,"recommended":True},
            {"subject":"COMP","catalog":"551","title":"Applied Machine Learning","credits":3,"is_required":False,"recommended":True},
            {"subject":"COMP","catalog":None,"title":"Any COMP course at 300+ level","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── EAST ASIAN LANGUAGE AND LITERATURE – MINOR CONCENTRATION ──
    {
      "program_key": "east_asian_lang_lit_minor",
      "name": "East Asian Language and Literature – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "An 18-credit minor combining East Asian language study with literature courses.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/east-asian-studies/east-asian-language-literature-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "eall_courses",
          "title": "Language and Literature Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits combining language (CHIN/JAPN/KORE) with EAST literature courses.",
          "sort_order": 1,
          "courses": [
            {"subject":"CHIN","catalog":"201","title":"Mandarin Chinese 1","credits":3,"is_required":False,"recommended":True},
            {"subject":"JAPN","catalog":"201","title":"Japanese 1","credits":3,"is_required":False},
            {"subject":"EAST","catalog":"310","title":"Classical Chinese Literature","credits":3,"is_required":False,"recommended":True},
            {"subject":"EAST","catalog":"330","title":"Modern Chinese Literature","credits":3,"is_required":False},
            {"subject":"EAST","catalog":"340","title":"Japanese Cinema","credits":3,"is_required":False,"recommended":True},
          ],
        },
      ],
    },

  # ── EAST ASIAN CULTURAL STUDIES – MINOR CONCENTRATION ──
    {
      "program_key": "east_asian_cultural_studies_minor",
      "name": "East Asian Cultural Studies – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit minor in East Asian culture, history, and society. No "
        "language prerequisite."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/east-asian-studies/east-asian-cultural-studies-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "eacs_courses",
          "title": "East Asian Cultural Studies Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from EAST content courses (not language courses).",
          "sort_order": 1,
          "courses": [
            {"subject":"EAST","catalog":"211","title":"Introduction to Chinese Culture","credits":3,"is_required":False,"recommended":True},
            {"subject":"EAST","catalog":"213","title":"Introduction to Japanese Culture","credits":3,"is_required":False,"recommended":True},
            {"subject":"EAST","catalog":"215","title":"Introduction to Korean Culture","credits":3,"is_required":False},
            {"subject":"EAST","catalog":"340","title":"Japanese Cinema","credits":3,"is_required":False,"recommended":True},
            {"subject":"EAST","catalog":"350","title":"Gender and Sexuality in Chinese Literature","credits":3,"is_required":False},
            {"subject":"EAST","catalog":None,"title":"Any EAST content course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── EAST ASIAN LANGUAGE – SUPPLEMENTARY MINOR CONCENTRATION ──
    {
      "program_key": "east_asian_lang_supplementary_minor",
      "name": "East Asian Language – Supplementary Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": (
        "An 18-credit supplementary minor in an East Asian language for students "
        "already in an East Asian Studies program."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/east-asian-studies/east-asian-language-supplementary-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "eals_courses",
          "title": "East Asian Language Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits in a single East Asian language (CHIN, JAPN, or KORE).",
          "sort_order": 1,
          "courses": [
            {"subject":"CHIN","catalog":"201","title":"Mandarin Chinese 1","credits":3,"is_required":False},
            {"subject":"CHIN","catalog":"202","title":"Mandarin Chinese 2","credits":3,"is_required":False},
            {"subject":"JAPN","catalog":"201","title":"Japanese 1","credits":3,"is_required":False},
            {"subject":"JAPN","catalog":"202","title":"Japanese 2","credits":3,"is_required":False},
            {"subject":"KORE","catalog":"201","title":"Korean 1","credits":3,"is_required":False},
            {"subject":"KORE","catalog":"202","title":"Korean 2","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── GEOGRAPHY (URBAN STUDIES) – MAJOR CONCENTRATION ──
    {
      "program_key": "geography_urban_studies_major",
      "name": "Geography (Urban Studies) – Major Concentration",
      "program_type": "major",
      "faculty": "Faculty of Arts",
      "total_credits": 36,
      "description": (
        "Focuses on urban environments, spatial planning, and the social dynamics "
        "of cities."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/geography-urban-studies-major-concentration-ba/",
      "blocks": [
        {
          "block_key": "urbg_required",
          "title": "Required Core",
          "block_type": "required",
          "credits_needed": 9,
          "sort_order": 1,
          "courses": [
            {"subject":"GEOG","catalog":"200","title":"Environmental Systems","credits":3,"is_required":True},
            {"subject":"GEOG","catalog":"202","title":"Quantitative Methods in Geography","credits":3,"is_required":True},
            {"subject":"GEOG","catalog":"320","title":"Urban Geography","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Core urban focus course"},
          ],
        },
        {
          "block_key": "urbg_electives",
          "title": "Urban Studies Electives",
          "block_type": "choose_credits",
          "credits_needed": 27,
          "min_credits_400": 6,
          "notes": "27 credits from urban-focused GEOG and approved cognate courses. At least 6 at 400-level.",
          "sort_order": 2,
          "courses": [
            {"subject":"GEOG","catalog":"210","title":"Economic Geography","credits":3,"is_required":False,"recommended":True},
            {"subject":"GEOG","catalog":"220","title":"Population and Society","credits":3,"is_required":False},
            {"subject":"GEOG","catalog":"330","title":"Political Geography","credits":3,"is_required":False},
            {"subject":"GEOG","catalog":"401","title":"Geographic Information Systems","credits":3,"is_required":False,"recommended":True},
            {"subject":"GEOG","catalog":None,"title":"Any urban-focused GEOG course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── GEOGRAPHY (URBAN STUDIES) – MINOR CONCENTRATION ──
    {
      "program_key": "geography_urban_studies_minor",
      "name": "Geography (Urban Studies) – Minor Concentration",
      "program_type": "minor",
      "faculty": "Faculty of Arts",
      "total_credits": 18,
      "description": "An 18-credit introduction to urban geography and spatial analysis of cities.",
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/geography/geography-urban-studies-minor-concentration-ba/",
      "blocks": [
        {
          "block_key": "urbgm_courses",
          "title": "Urban Geography Courses",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "18 credits from GEOG courses with urban focus.",
          "sort_order": 1,
          "courses": [
            {"subject":"GEOG","catalog":"320","title":"Urban Geography","credits":3,"is_required":False,"recommended":True},
            {"subject":"GEOG","catalog":"200","title":"Environmental Systems","credits":3,"is_required":False},
            {"subject":"GEOG","catalog":"210","title":"Economic Geography","credits":3,"is_required":False,"recommended":True},
            {"subject":"GEOG","catalog":None,"title":"Any GEOG course at 300+ level","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── CANADIAN STUDIES – HONOURS (B.A.) ──
    {
      "program_key": "canadian_studies_honours",
      "name": "Canadian Studies – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 54,
      "description": (
        "The Honours in Canadian Studies provides intensive interdisciplinary "
        "training in Canadian institutions, public affairs, and culture. Includes "
        "an honours thesis."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/institute-study/canadian-studies-honours-ba/",
      "blocks": [
        {
          "block_key": "cans_hon_core",
          "title": "Required Core (12 credits)",
          "block_type": "required",
          "credits_needed": 12,
          "sort_order": 1,
          "courses": [
            {"subject":"CANS","catalog":"200","title":"Introduction to Canadian Studies",  "credits":3,"is_required":True},
            {"subject":"CANS","catalog":"420","title":"Shaping Public Affairs in Canada",  "credits":3,"is_required":True},
            {"subject":"CANS","catalog":"480","title":"Honours Thesis 1",                  "credits":3,"is_required":True},
            {"subject":"CANS","catalog":"481","title":"Honours Thesis 2",                  "credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "cans_hon_electives",
          "title": "Canadian Studies Electives (42 credits)",
          "block_type": "choose_credits",
          "credits_needed": 42,
          "notes": "42 credits from CANS and cognate courses. At least 12 at 300+; at least 6 at 400-level.",
          "sort_order": 2,
          "courses": [
            {"subject":"CANS","catalog":"310","title":"Canadian Cultures: Context and Issues","credits":3,"is_required":False},
            {"subject":"CANS","catalog":"315","title":"Quebec and Canada","credits":3,"is_required":False},
            {"subject":"HIST","catalog":"203","title":"Canada: Confederation to the Present","credits":3,"is_required":False},
            {"subject":"POLI","catalog":"212","title":"Canadian Government and Politics","credits":3,"is_required":False},
            {"subject":"POLI","catalog":"221","title":"Quebec Politics","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ENGLISH – LITERATURE HONOURS (B.A.) ──
    {
      "program_key": "english_literature_honours",
      "name": "English – Literature Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 54,
      "description": (
        "The Honours in English Literature provides advanced training in close "
        "reading, literary history, and critical theory. Students produce a "
        "supervised honours essay. Requires a minimum program GPA of 3.50."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-literature-honours-ba/",
      "blocks": [
        {
          "block_key": "englit_hon_core",
          "title": "Required Core (18 credits)",
          "block_type": "required",
          "credits_needed": 18,
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"202","title":"Survey of English Literature 1","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"203","title":"Survey of English Literature 2","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"311","title":"Poetics","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"360","title":"Literary Criticism","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"491D1","title":"Honours Essay 1","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"491D2","title":"Honours Essay 2","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "englit_hon_electives",
          "title": "Literature Electives (36 credits)",
          "block_type": "choose_credits",
          "credits_needed": 36,
          "notes": "36 credits across periods, genres, and areas. At least 12 at 400-level.",
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"308","title":"Shakespeare","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"321","title":"Canadian Literature 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"370","title":"Literature Romantic Period 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"390","title":"Poetry of the 20th Century 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"400","title":"Advanced Seminar in Literature 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"414","title":"Theories of Difference","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ENGLISH – DRAMA AND THEATRE HONOURS (B.A.) ──
    {
      "program_key": "english_drama_theatre_honours",
      "name": "English – Drama and Theatre Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 54,
      "description": (
        "Honours program in Drama and Theatre emphasising analysis, history, and "
        "theory of performance. Includes an honours essay. Program GPA of 3.50 "
        "required."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-drama-theatre-honours-ba/",
      "blocks": [
        {
          "block_key": "engdt_hon_core",
          "title": "Required Core (12 credits)",
          "block_type": "required",
          "credits_needed": 12,
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"230","title":"Introduction to Theatre Studies","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"355","title":"The Poetics of Performance","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"491D1","title":"Honours Essay 1","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"491D2","title":"Honours Essay 2","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "engdt_hon_electives",
          "title": "Drama & Theatre Electives (42 credits)",
          "block_type": "choose_credits",
          "credits_needed": 42,
          "notes": "36 credits from Drama & Theatre and ENGL offerings. At least 12 at 400-level.",
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"269","title":"Introduction to Performance","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"306","title":"Theatre History: Medieval and Early Modern","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"371","title":"Theatre History: 19th to 21st Centuries","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"466","title":"Directing for the Theatre","credits":6,"is_required":False},
            {"subject":"ENGL","catalog":"467","title":"Advanced Studies in Theatre History","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── ENGLISH – CULTURAL STUDIES HONOURS (B.A.) ──
    {
      "program_key": "english_cultural_studies_honours",
      "name": "English – Cultural Studies Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 54,
      "description": (
        "Honours program in Cultural Studies focusing on media, film, and "
        "cultural theory. Includes an honours essay. Program GPA of 3.50 "
        "required."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/english/english-cultural-studies-honours-ba/",
      "blocks": [
        {
          "block_key": "engcs_hon_core",
          "title": "Required Core (15 credits)",
          "block_type": "required",
          "credits_needed": 15,
          "sort_order": 1,
          "courses": [
            {"subject":"ENGL","catalog":"275",   "title":"Introduction to Cultural Studies","credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"277",   "title":"Introduction to Film Studies",   "credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"359",   "title":"The Poetics of the Image",       "credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"491D1", "title":"Honours Essay",                  "credits":3,"is_required":True},
            {"subject":"ENGL","catalog":"491D2", "title":"Honours Essay",                  "credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "engcs_hon_electives",
          "title": "Cultural Studies Electives (36 credits)",
          "block_type": "choose_credits",
          "credits_needed": 36,
          "notes": "36 credits from Cultural Studies offerings. At least 12 at 400-level.",
          "sort_order": 2,
          "courses": [
            {"subject":"ENGL","catalog":"350","title":"Studies in the History of Film 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"381","title":"A Film-Maker 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"489","title":"Culture and Critical Theory 1","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"490","title":"Culture and Critical Theory 2","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":"484","title":"Seminar in the Film","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── GERMAN STUDIES – HONOURS (B.A.) ──
    {
      "program_key": "german_studies_honours",
      "name": "German Studies – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 60,
      "description": (
        "Advanced study of German language, literature, and culture. Includes an "
        "honours thesis. CGPA of 3.00 and program GPA of 3.00 required."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/german-studies-honours-ba/",
      "blocks": [
        {
          "block_key": "germ_hon_language",
          "title": "Language Requirements (18 credits)",
          "block_type": "required",
          "credits_needed": 18,
          "sort_order": 1,
          "courses": [
            {"subject":"GERM","catalog":"100","title":"Beginner's German 1 (Intensive)","credits":6,"is_required":False},
            {"subject":"GERM","catalog":"200","title":"Intermediate German (Intensive)","credits":6,"is_required":False},
            {"subject":"GERM","catalog":"307D1","title":"Intermediate German (Advanced)","credits":3,"is_required":False},
            {"subject":"GERM","catalog":"307D2","title":"Intermediate German (Advanced) 2","credits":3,"is_required":False},
          ],
        },
        {
          "block_key": "germ_hon_thesis",
          "title": "Honours Thesis (6 credits)",
          "block_type": "required",
          "credits_needed": 6,
          "sort_order": 2,
          "courses": [
            {"subject":"GERM","catalog":"575","title":"Honours Thesis","credits":6,"is_required":True},
          ],
        },
        {
          "block_key": "germ_hon_electives",
          "title": "German Literature & Culture (36 credits)",
          "block_type": "choose_credits",
          "credits_needed": 36,
          "notes": "At least 12 credits at 400-level.",
          "sort_order": 3,
          "courses": [
            {"subject":"GERM","catalog":"259","title":"Introduction to German Literature 1","credits":3,"is_required":False},
            {"subject":"GERM","catalog":"260","title":"Introduction to German Literature 2","credits":3,"is_required":False},
            {"subject":"GERM","catalog":"350","title":"Modernism and the Avant-Garde","credits":3,"is_required":False},
            {"subject":"GERM","catalog":None,"title":"Any GERM literature/culture course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── HISPANIC STUDIES – HONOURS (B.A.) ──
  # Source: McGill eCalendar 2024-2025
  # https://www.mcgill.ca/study/2024-2025/faculties/arts/undergraduate/programs/bachelor-arts-ba-honours-hispanic-studies
    {
      "program_key": "hispanic_studies_honours",
      "name": "Hispanic Studies – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 60,
      "description": (
        "Advanced 60-credit study of Spanish and Latin American language, literature, "
        "film, and cultural studies. Includes an honours thesis (HISP 490D1/D2). "
        "Requires a mandatory 18-credit minor concentration in another discipline. "
        "Prerequisite: first-year Spanish with min. grade B+. "
        "Must maintain program GPA of 3.30 and CGPA of 3.00. "
        "Maximum 18 credits in English-taught courses."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/hispanic-studies-honours-ba/",
      "blocks": [
        {
          "block_key": "hisp_hon_required",
          "title": "Required Courses",
          "block_type": "required",
          "credits_needed": 18,
          "notes": "All five courses (18 credits) are required.",
          "sort_order": 1,
          "courses": [
            {"subject":"HISP","catalog":"241","title":"Survey of Spanish Literature and Culture 1","credits":3,"is_required":True,"recommended":True},
            {"subject":"HISP","catalog":"242","title":"Survey of Spanish Literature and Culture 2","credits":3,"is_required":True},
            {"subject":"HISP","catalog":"243","title":"Survey of Latin American Literature and Culture 1","credits":3,"is_required":True,"recommended":True},
            {"subject":"HISP","catalog":"244","title":"Survey of Latin American Literature and Culture 2","credits":3,"is_required":True},
            {"subject":"HISP","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True,"recommended":True,"recommendation_reason":"Must register D1 and D2 in consecutive terms"},
            {"subject":"HISP","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "hisp_hon_electives",
          "title": "Complementary Courses",
          "block_type": "choose_credits",
          "credits_needed": 42,
          "notes": (
            "42 credits from HISP 300-level or above undergraduate courses. "
            "Minimum 9 credits at 400-level or above. "
            "Maximum 18 credits in English-taught courses across the full program."
          ),
          "min_credits_400": 9,
          "sort_order": 2,
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
            {"subject":"HISP","catalog":"345","title":"Contemporary Hispanic Cultural Studies","credits":3,"is_required":False,"recommended":True},
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

  # ── ITALIAN STUDIES – HONOURS (B.A.) ──
    {
      "program_key": "italian_studies_honours",
      "name": "Italian Studies – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 54,
      "description": (
        "Advanced study of Italian language, literature, and culture from the "
        "Middle Ages to the present. Includes an honours thesis."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/italian-studies-honours-ba/",
      "blocks": [
        {
          "block_key": "ital_hon_language",
          "title": "Language Requirements (12 credits)",
          "block_type": "required",
          "credits_needed": 12,
          "sort_order": 1,
          "courses": [
            {"subject":"ITAL","catalog":"100","title":"Beginner's Italian (Intensive)","credits":6,"is_required":False},
            {"subject":"ITAL","catalog":"200","title":"Intermediate Italian (Intensive)","credits":6,"is_required":False},
            {"subject":"ITAL","catalog":"255","title":"Advanced Reading and Composition","credits":6,"is_required":False},
          ],
        },
        {
          "block_key": "ital_hon_thesis",
          "title": "Honours Thesis (6 credits)",
          "block_type": "required",
          "credits_needed": 6,
          "sort_order": 2,
          "courses": [
            {"subject":"ITAL","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
            {"subject":"ITAL","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "ital_hon_electives",
          "title": "Italian Literature & Culture (36 credits)",
          "block_type": "choose_credits",
          "credits_needed": 36,
          "notes": "At least 12 credits at 400-level.",
          "sort_order": 3,
          "courses": [
            {"subject":"ITAL","catalog":"281","title":"Masterpieces of Italian Literature 2","credits":3,"is_required":False},
            {"subject":"ITAL","catalog":"310","title":"The Invention of Italian Literature","credits":3,"is_required":False},
            {"subject":"ITAL","catalog":None,"title":"Any ITAL literature/culture course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── LATIN AMERICAN AND CARIBBEAN STUDIES – HONOURS (B.A.) ──
    {
      "program_key": "latin_american_caribbean_honours",
      "name": "Latin American and Caribbean Studies – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 60,
      "description": (
        "Advanced interdisciplinary study of Latin America and the Caribbean, "
        "culminating in an independent research thesis."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/latin-american-caribbean-studies-honours-ba/",
      "blocks": [
        {
          "block_key": "lacs_hon_core",
          "title": "Required Core (18 credits)",
          "block_type": "required",
          "credits_needed": 18,
          "sort_order": 1,
          "courses": [
            {"subject":"HIST","catalog":"261","title":"Latin America: Colonial","credits":3,"is_required":True},
            {"subject":"HIST","catalog":"262","title":"Latin America: Modern","credits":3,"is_required":True},
            {"subject":"POLI","catalog":"312","title":"Politics of Latin America","credits":3,"is_required":True},
            {"subject":"HISP","catalog":"243","title":"Survey of Spanish-American Literature 1","credits":3,"is_required":True},
            {"subject":"LACS","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
            {"subject":"LACS","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "lacs_hon_electives",
          "title": "Interdisciplinary Electives (42 credits)",
          "block_type": "choose_credits",
          "credits_needed": 42,
          "notes": "42 credits from at least 3 disciplines. At least 12 at 400-level.",
          "sort_order": 2,
          "courses": [
            {"subject":"ANTH","catalog":"326","title":"Anthropology of Latin America","credits":3,"is_required":False},
            {"subject":"ECON","catalog":"313","title":"Economic Development 1","credits":3,"is_required":False},
            {"subject":"HISP","catalog":"244","title":"Survey of Spanish-American Literature 2","credits":3,"is_required":False},
            {"subject":"HISP","catalog":"335","title":"Politics and Poetry in Latin America","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── LIBERAL ARTS – HONOURS (B.A.) ──
    {
      "program_key": "liberal_arts_honours",
      "name": "Liberal Arts – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 60,
      "description": (
        "An intensive interdisciplinary program combining humanities and social "
        "sciences with an honours thesis. Students choose an intellectual stream "
        "and complete a supervised research project."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/liberal-arts-honours-ba/",
      "blocks": [
        {
          "block_key": "libart_hon_core",
          "title": "Required Core (12 credits)",
          "block_type": "required",
          "credits_needed": 12,
          "sort_order": 1,
          "courses": [
            {"subject":"LLCU","catalog":"395","title":"Research Methods in Liberal Arts","credits":3,"is_required":True},
            {"subject":"LLCU","catalog":"430","title":"Advanced Seminar in Liberal Arts","credits":3,"is_required":True},
            {"subject":"LLCU","catalog":"490D1","title":"Honours Thesis 1","credits":3,"is_required":True},
            {"subject":"LLCU","catalog":"490D2","title":"Honours Thesis 2","credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "libart_hon_stream",
          "title": "Stream and Elective Courses (48 credits)",
          "block_type": "choose_credits",
          "credits_needed": 48,
          "notes": "48 credits across humanities and social sciences. Must satisfy distribution requirements for chosen stream. Requires a minor in a language program (other than English).",
          "sort_order": 2,
          "courses": [
            {"subject":"HIST","catalog":None,"title":"Any HIST course","credits":3,"is_required":False},
            {"subject":"PHIL","catalog":None,"title":"Any PHIL course","credits":3,"is_required":False},
            {"subject":"ENGL","catalog":None,"title":"Any ENGL course","credits":3,"is_required":False},
            {"subject":"POLI","catalog":None,"title":"Any POLI course","credits":3,"is_required":False},
            {"subject":"SOCI","catalog":None,"title":"Any SOCI course","credits":3,"is_required":False},
          ],
        },
      ],
    },

  # ── RUSSIAN – HONOURS (B.A.) ──
    {
      "program_key": "russian_honours",
      "name": "Russian – Honours (B.A.)",
      "program_type": "honours",
      "faculty": "Faculty of Arts",
      "total_credits": 60,
      "description": (
        "The Honours Russian program is for students intending to pursue graduate "
        "studies or advanced careers in the field. CGPA and program GPA of 3.00 "
        "required."
      ),
      "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/languages-literatures-cultures/russian-honours-ba/",
      "blocks": [
        {
          "block_key": "russ_hon_core",
          "title": "Required Core (12 credits)",
          "block_type": "required",
          "credits_needed": 12,
          "notes": "All required.",
          "sort_order": 1,
          "courses": [
            {"subject":"RUSS","catalog":"452","title":"Advanced Russian Language and Syntax 1","credits":3,"is_required":True},
            {"subject":"RUSS","catalog":"453","title":"Advanced Russian Language and Syntax 2","credits":3,"is_required":True},
            {"subject":"RUSS","catalog":"490","title":"Honours Seminar 01",                   "credits":3,"is_required":True},
            {"subject":"RUSS","catalog":"491","title":"Honours Seminar 02",                   "credits":3,"is_required":True},
          ],
        },
        {
          "block_key": "russ_hon_language",
          "title": "Language Prerequisites (options)",
          "block_type": "choose_credits",
          "credits_needed": 18,
          "notes": "Students with prior knowledge may replace lower-level with upper-level courses.",
          "sort_order": 2,
          "courses": [
            {"subject":"RUSS","catalog":"210","title":"Introductory Russian 1","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"211","title":"Introductory Russian 2","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"310","title":"Intermediate Russian 1","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"311","title":"Intermediate Russian 2","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"410","title":"Advanced Russian Language 1","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"415","title":"Advanced Russian Language Intensive 1","credits":6,"is_required":False},
          ],
        },
        {
          "block_key": "russ_hon_electives",
          "title": "Russian Literature & Culture (36 credits)",
          "block_type": "choose_credits",
          "credits_needed": 36,
          "notes": "At least 12 at 400-level. Max 6 credits from other departments.",
          "sort_order": 3,
          "courses": [
            {"subject":"RUSS","catalog":"217","title":"19th-Century Russian Literature in Translation","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"218","title":"Russian Literature and Revolution","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"232","title":"Russian Cinema","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"340","title":"Russian Short Story","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":"365","title":"Supernatural and Absurd in Russian Literature","credits":3,"is_required":False},
            {"subject":"RUSS","catalog":None,"title":"Any RUSS literature/culture course","credits":3,"is_required":False},
          ],
        },
      ],
    },


  # ══════════════════════════════════════════════════════════════════
  # BATCH 2: Math, Stats, Environment, Geography extras, Music,

]
