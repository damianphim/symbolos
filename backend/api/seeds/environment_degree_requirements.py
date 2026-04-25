"""
McGill Bieler School of Environment – Degree Requirements Seed Data
Source: McGill Course Catalogue 2025-2026 & Bieler School of Environment website
https://coursecatalogue.mcgill.ca/en/undergraduate/environment/
https://www.mcgill.ca/environment/undergraduate-studies/undergraduate-programs/

This file covers all Bieler School of Environment undergraduate programs:
  - B.A. Faculty Program in Environment (3 concentrations, 54 credits each)
  - Environment Minor Concentration (B.A.)  (18 credits)
  - Environment Diploma  (30 credits)

NOTE: The B.A. & Sc. Interfaculty/Honours programs are seeded in
      arts_science_degree_requirements.py (program_keys: environment_interfaculty_basc,
      environment_honours_basc).

Accuracy notes:
  - Verified from official McGill Course Catalogue 2025-2026 and
    the Bieler School of Environment website (January 2026)
  - All programs require a grade of C or higher in every program course
  - B.A. programs also require MATH 139/140 (numeracy) and a basic science course
    as pre-/co-requisites (not counted toward the 54 program credits unless noted)
  - Max 30–34 credits at the 200-level; min 12 credits at the 400+ level per program
"""

ENVIRONMENT_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════════
  #  B.A. FACULTY PROGRAM – ECOLOGICAL DETERMINANTS OF HEALTH (54 cr)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "environment_ecological_determinants_ba",
    "name":          "Faculty Program Environment – Ecological Determinants of Health in Society (B.A.) (54 credits)",
    "program_type":  "major",
    "faculty":       "School of Environment",
    "total_credits": 54,
    "description": (
      "Open only to students in the B.A. degree. An understanding of the interface "
      "between human health and environment depends not only on an appreciation of the "
      "biological and ecological determinants of health, but equally on the role of "
      "social sciences in the design, implementation, and monitoring of interventions. "
      "Demographic patterns and urbanization, economic forces, ethics, indigenous "
      "knowledge and culture, and an understanding of how social change can be effected "
      "are all critical if we are to be successful in our efforts to assure health of "
      "individuals and societies in the future. Recognizing the key role that nutritional "
      "status plays in maintaining a healthy body, and the increasing importance of "
      "infection as a health risk linked intimately with the environment, this Domain "
      "prepares students to contribute to the solution of problems of nutrition and "
      "infection by tying the relevant natural sciences to the social sciences. "
      "Pre-/co-requisites (not in the 54 credits): MATH 139 or 140; BIOL 111 or AEBI 120. "
      "Maximum 30 credits at the 200-level; minimum 12 credits at the 400+ level."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/environment/programs/ba-faculty-program-environment/environment-ecological-determinants-health-society-ba/",
    "blocks": [
      {
        "block_key":      "eco_det_ba_core_required",
        "title":          "Core: Required Courses (18 credits)",
        "block_type":     "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "All six core ENVR courses are required for every B.A. Faculty Program in Environment.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment",              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core required – start here in U1"},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core required – take in U1"},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth",                  "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment",   "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "301", "title": "Environmental Research Design",       "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required intermediate; take after completing ENVR 200–203"},
          {"subject": "ENVR", "catalog": "400", "title": "Environmental Thought",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required senior course; take in U3"},
        ],
      },
      {
        "block_key":      "eco_det_ba_senior_research",
        "title":          "Core: Senior Research Project (3 credits*)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE research project course. Only 3 credits count toward the program; extra credits from 6-credit field courses count as electives.",
        "sort_order": 2,
        "courses": [
          {"subject": "ENVR", "catalog": "401",  "title": "Environmental Research",              "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Standard on-campus research option"},
          {"subject": "AEBI", "catalog": "427",  "title": "Barbados Interdisciplinary Project",  "credits": 6, "is_required": False, "notes": "6 cr course; only 3 cr applied. Macdonald campus. Field: Barbados."},
          {"subject": "ENVR", "catalog": "451",  "title": "Research in Panama",                  "credits": 6, "is_required": False, "notes": "6 cr course; only 3 cr applied. Field: Panama."},
          {"subject": "FSCI", "catalog": "444",  "title": "Barbados Research Project",           "credits": 6, "is_required": False, "notes": "6 cr course; only 3 cr applied. Field: Barbados."},
        ],
      },
      {
        "block_key":      "eco_det_ba_health_env_required",
        "title":          "Concentration: Health and Environment (3 credits, choose one)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE of GEOG 221, GEOG 303, or NRSC 221 (3 credits). Note: GEOG 303 may be taken as a second Health and Environment course under List A or List B if desired.",
        "sort_order": 3,
        "courses": [
          {"subject": "GEOG", "catalog": "221",  "title": "Environment and Health",   "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Downtown campus option for Health and Environment"},
          {"subject": "GEOG", "catalog": "303",  "title": "Health Geography",         "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Downtown campus Health Geography option"},
          {"subject": "NRSC", "catalog": "221",  "title": "Environment and Health",   "credits": 3, "is_required": False, "notes": "Macdonald campus equivalent of GEOG 221."},
        ],
      },
      {
        "block_key":      "eco_det_ba_fundamentals",
        "title":          "Concentration: Fundamentals – choose 12 credits (max 3 from any one category)",
        "block_type":     "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Choose 12 credits total from the following categories. Maximum 3 credits from any single category: Health & Infection, Economics, Nutrition, Statistics.",
        "sort_order": 4,
        "courses": [
          # Health and Infection
          {"subject": "GEOG", "catalog": "403",  "title": "Global Health and Environmental Change",     "credits": 3, "is_required": False, "choose_from_group": "Health and Infection"},
          {"subject": "GEOG", "catalog": "493",  "title": "Health and Environment in Africa",           "credits": 3, "is_required": False, "choose_from_group": "Health and Infection"},
          {"subject": "GEOG", "catalog": "503",  "title": "Advanced Topics in Health Geography",        "credits": 3, "is_required": False, "choose_from_group": "Health and Infection"},
          {"subject": "PARA", "catalog": "410",  "title": "Environment and Infection",                  "credits": 3, "is_required": False, "choose_from_group": "Health and Infection", "notes": "Macdonald campus"},
          {"subject": "PPHS", "catalog": "529",  "title": "Global Environmental Health and Burden of Disease", "credits": 3, "is_required": False, "choose_from_group": "Health and Infection", "notes": "U3 students only"},
          # Economics
          {"subject": "AGEC", "catalog": "200",  "title": "Principles of Microeconomics",               "credits": 3, "is_required": False, "choose_from_group": "Economics", "notes": "Macdonald campus"},
          {"subject": "ECON", "catalog": "208",  "title": "Microeconomic Analysis and Applications",    "credits": 3, "is_required": False, "choose_from_group": "Economics"},
          {"subject": "ECON", "catalog": "225",  "title": "Economics of the Environment",               "credits": 3, "is_required": False, "choose_from_group": "Economics"},
          # Nutrition
          {"subject": "EDKP", "catalog": "292",  "title": "Nutrition and Wellness",                     "credits": 3, "is_required": False, "choose_from_group": "Nutrition"},
          {"subject": "NUTR", "catalog": "207",  "title": "Nutrition and Health",                        "credits": 3, "is_required": False, "choose_from_group": "Nutrition", "notes": "Macdonald campus"},
          # Statistics
          {"subject": "AEMA", "catalog": "310",  "title": "Statistical Methods 1",                      "credits": 3, "is_required": False, "choose_from_group": "Statistics", "notes": "Macdonald campus"},
          {"subject": "GEOG", "catalog": "202",  "title": "Statistics and Spatial Analysis",            "credits": 3, "is_required": False, "choose_from_group": "Statistics"},
          {"subject": "MATH", "catalog": "203",  "title": "Principles of Statistics 1",                 "credits": 3, "is_required": False, "choose_from_group": "Statistics"},
          {"subject": "SOCI", "catalog": "350",  "title": "Statistics in Social Research",              "credits": 3, "is_required": False, "choose_from_group": "Statistics"},
        ],
      },
      {
        "block_key":      "eco_det_ba_list_a",
        "title":          "Concentration: List A – choose 9 credits (max 3 from any one category)",
        "block_type":     "choose_credits",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Choose 9 credits, maximum 3 credits from any single category: Health & Society, Hydrology & Climate, Agriculture, Decision Making, Biology Fundamentals, Development & Ecology.",
        "sort_order": 5,
        "courses": [
          # Health and Society
          {"subject": "SOCI", "catalog": "225",  "title": "Medicine and Health in Modern Society",       "credits": 3, "is_required": False, "choose_from_group": "Health and Society"},
          {"subject": "SOCI", "catalog": "234",  "title": "Population and Society",                      "credits": 3, "is_required": False, "choose_from_group": "Health and Society"},
          {"subject": "SOCI", "catalog": "309",  "title": "Health and Illness",                          "credits": 3, "is_required": False, "choose_from_group": "Health and Society"},
          {"subject": "SOCI", "catalog": "331",  "title": "Population and Environment",                  "credits": 3, "is_required": False, "choose_from_group": "Health and Society"},
          {"subject": "SOCI", "catalog": "515",  "title": "Medicine and Society",                        "credits": 3, "is_required": False, "choose_from_group": "Health and Society"},
          # Hydrology and Climate
          {"subject": "AGRI", "catalog": "452",  "title": "Water Resources in Barbados",                 "credits": 3, "is_required": False, "choose_from_group": "Hydrology and Climate", "notes": "Field: Barbados."},
          {"subject": "BREE", "catalog": "217",  "title": "Hydrology and Water Resources",               "credits": 3, "is_required": False, "choose_from_group": "Hydrology and Climate", "notes": "Macdonald campus. Cannot take both BREE 217 and GEOG 322."},
          {"subject": "GEOG", "catalog": "321",  "title": "Climatic Environments",                       "credits": 3, "is_required": False, "choose_from_group": "Hydrology and Climate"},
          {"subject": "GEOG", "catalog": "322",  "title": "Environmental Hydrology",                     "credits": 3, "is_required": False, "choose_from_group": "Hydrology and Climate", "notes": "Cannot take both BREE 217 and GEOG 322."},
          # Agriculture
          {"subject": "AEBI", "catalog": "425",  "title": "Tropical Energy and Food",                   "credits": 3, "is_required": False, "choose_from_group": "Agriculture", "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "AGRI", "catalog": "340",  "title": "Principles of Ecological Agriculture",        "credits": 3, "is_required": False, "choose_from_group": "Agriculture", "notes": "Macdonald campus"},
          {"subject": "AGRI", "catalog": "411",  "title": "Global Issues on Development, Food and Agriculture", "credits": 3, "is_required": False, "choose_from_group": "Agriculture", "notes": "Macdonald campus"},
          {"subject": "AGRI", "catalog": "550",  "title": "Sustained Tropical Agriculture",              "credits": 3, "is_required": False, "choose_from_group": "Agriculture", "notes": "Macdonald campus. Alternate years; Panama."},
          {"subject": "NUTR", "catalog": "341",  "title": "Global Food Security",                        "credits": 3, "is_required": False, "choose_from_group": "Agriculture", "notes": "Macdonald campus"},
          # Decision Making
          {"subject": "AGEC", "catalog": "333",  "title": "Resource Economics",                          "credits": 3, "is_required": False, "choose_from_group": "Decision Making", "notes": "Macdonald campus"},
          {"subject": "ECON", "catalog": "440",  "title": "Health Economics",                            "credits": 3, "is_required": False, "choose_from_group": "Decision Making"},
          {"subject": "PHIL", "catalog": "343",  "title": "Biomedical Ethics",                           "credits": 3, "is_required": False, "choose_from_group": "Decision Making"},
          {"subject": "RELG", "catalog": "270",  "title": "Religious Ethics and the Environment",        "credits": 3, "is_required": False, "choose_from_group": "Decision Making"},
          # Biology Fundamentals
          {"subject": "AEBI", "catalog": "210",  "title": "Organisms 1",                                 "credits": 3, "is_required": False, "choose_from_group": "Biology Fundamentals", "notes": "Macdonald campus"},
          {"subject": "AEBI", "catalog": "211",  "title": "Organisms 2",                                 "credits": 3, "is_required": False, "choose_from_group": "Biology Fundamentals", "notes": "Macdonald campus"},
          {"subject": "BIOL", "catalog": "200",  "title": "Molecular Biology",                           "credits": 3, "is_required": False, "choose_from_group": "Biology Fundamentals"},
          {"subject": "BIOL", "catalog": "308",  "title": "Ecological Dynamics",                         "credits": 3, "is_required": False, "choose_from_group": "Biology Fundamentals", "notes": "Cannot take both BIOL 308 and ENVB 305."},
          {"subject": "ENVB", "catalog": "305",  "title": "Population and Community Ecology",            "credits": 3, "is_required": False, "choose_from_group": "Biology Fundamentals", "notes": "Macdonald campus. Cannot take both BIOL 308 and ENVB 305."},
          {"subject": "LSCI", "catalog": "211",  "title": "Biochemistry 1",                              "credits": 3, "is_required": False, "choose_from_group": "Biology Fundamentals", "notes": "Macdonald campus"},
          # Development and Ecology
          {"subject": "ANTH", "catalog": "212",  "title": "Anthropology of Development",                "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
          {"subject": "ANTH", "catalog": "339",  "title": "Ecological Anthropology",                    "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
          {"subject": "ANTH", "catalog": "512",  "title": "Political Ecology",                          "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
          {"subject": "ENVR", "catalog": "421",  "title": "Montreal: Environmental History and Sustainability", "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology", "notes": "Alternate years, Summer term"},
          {"subject": "GEOG", "catalog": "300",  "title": "Human Ecology in Geography",                 "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
          {"subject": "GEOG", "catalog": "310",  "title": "Development and Livelihoods",                "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
          {"subject": "SOCI", "catalog": "254",  "title": "Development and Underdevelopment",           "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
          {"subject": "SOCI", "catalog": "365",  "title": "Health and Development",                     "credits": 3, "is_required": False, "choose_from_group": "Development and Ecology"},
        ],
      },
      {
        "block_key":      "eco_det_ba_list_b",
        "title":          "Concentration: List B – choose 6 credits (max 3 from any one category)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Choose 6 credits, max 3/category: Advanced Ecology, Pollution Control, Techniques & Management, Social Change, Immunology & Infectious Disease, Populations & Place.",
        "sort_order": 6,
        "courses": [
          # Advanced Ecology
          {"subject": "AEBI", "catalog": "421",  "title": "Tropical Horticultural Ecology",              "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology", "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "BIOL", "catalog": "451",  "title": "Research in Ecology and Development in Africa", "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology", "notes": "Field: Africa. Cannot take both BIOL 451 and NRSC 451."},
          {"subject": "BIOL", "catalog": "465",  "title": "Conservation Biology",                        "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology"},
          {"subject": "BIOL", "catalog": "553",  "title": "Neotropical Environments",                    "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology", "notes": "Field: Panama."},
          {"subject": "ENVB", "catalog": "410",  "title": "Ecosystem Ecology",                           "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology", "notes": "Macdonald campus"},
          {"subject": "ENVB", "catalog": "500",  "title": "Advanced Topics in Ecotoxicology",           "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology", "notes": "Macdonald campus. Alternate years, Fall."},
          {"subject": "NRSC", "catalog": "451",  "title": "Research in Ecology and Development in Africa", "credits": 3, "is_required": False, "choose_from_group": "Advanced Ecology", "notes": "Macdonald campus. Field: Africa. Cannot take both BIOL 451 and NRSC 451."},
          # Pollution Control and Pest Management
          {"subject": "ENTO", "catalog": "350",  "title": "Insect Biology and Control",                  "credits": 3, "is_required": False, "choose_from_group": "Pollution Control"},
          {"subject": "ENTO", "catalog": "352",  "title": "Biocontrol of Pest Insects",                  "credits": 3, "is_required": False, "choose_from_group": "Pollution Control"},
          {"subject": "NRSC", "catalog": "333",  "title": "Pollution and Bioremediation",               "credits": 3, "is_required": False, "choose_from_group": "Pollution Control", "notes": "Macdonald campus"},
          {"subject": "PARA", "catalog": "515",  "title": "Water, Health and Sanitation",               "credits": 3, "is_required": False, "choose_from_group": "Pollution Control", "notes": "Macdonald campus"},
          # Techniques and Management
          {"subject": "AEBI", "catalog": "423",  "title": "Sustainable Land Use",                       "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management", "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "ENVB", "catalog": "529",  "title": "GIS for Natural Resource Management",        "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management", "notes": "Macdonald campus. Cannot take both ENVB 529 and GEOG 201."},
          {"subject": "ENVR", "catalog": "422",  "title": "Montreal Urban Sustainability Analysis",      "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management", "notes": "Alternate years, Summer term"},
          {"subject": "GEOG", "catalog": "201",  "title": "Introductory Geo-Information Science",       "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management", "notes": "Cannot take both ENVB 529 and GEOG 201."},
          {"subject": "GEOG", "catalog": "302",  "title": "Environmental Management 1",                 "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management"},
          {"subject": "GEOG", "catalog": "404",  "title": "Environmental Management 2",                 "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management", "notes": "Field: Africa."},
          {"subject": "WILD", "catalog": "421",  "title": "Wildlife Conservation",                      "credits": 3, "is_required": False, "choose_from_group": "Techniques and Management", "notes": "Macdonald campus"},
          # Social Change and Influences
          {"subject": "ANTH", "catalog": "227",  "title": "Medical Anthropology",                       "credits": 3, "is_required": False, "choose_from_group": "Social Change and Influences"},
          {"subject": "ENVR", "catalog": "430",  "title": "The Economics of Well-Being",                "credits": 3, "is_required": False, "choose_from_group": "Social Change and Influences", "notes": "Alternate years, Fall."},
          {"subject": "GEOG", "catalog": "340",  "title": "Sustainability in the Caribbean",            "credits": 3, "is_required": False, "choose_from_group": "Social Change and Influences", "notes": "Field: Barbados."},
          {"subject": "GEOG", "catalog": "514",  "title": "Climate Change Vulnerability and Adaptation","credits": 3, "is_required": False, "choose_from_group": "Social Change and Influences"},
          {"subject": "HIST", "catalog": "249",  "title": "Health and the Healer in Western History",   "credits": 3, "is_required": False, "choose_from_group": "Social Change and Influences"},
          {"subject": "SOCI", "catalog": "307",  "title": "Globalization",                              "credits": 3, "is_required": False, "choose_from_group": "Social Change and Influences"},
          # Immunology and Infectious Disease
          {"subject": "MIMM", "catalog": "214",  "title": "Introductory Immunology: Elements of Immunity", "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease"},
          {"subject": "MIMM", "catalog": "314",  "title": "Intermediate Immunology",                    "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease"},
          {"subject": "MIMM", "catalog": "324",  "title": "Fundamental Virology",                       "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease"},
          {"subject": "MIMM", "catalog": "413",  "title": "Parasitology",                               "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease", "notes": "Cannot take both MIMM 413 and PARA 424."},
          {"subject": "PARA", "catalog": "424",  "title": "Fundamental Parasitology",                   "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease", "notes": "Macdonald campus. Cannot take both MIMM 413 and PARA 424."},
          {"subject": "PARA", "catalog": "438",  "title": "Immunology",                                 "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease", "notes": "Macdonald campus"},
          {"subject": "PPHS", "catalog": "501",  "title": "Population Health and Epidemiology",         "credits": 3, "is_required": False, "choose_from_group": "Immunology and Infectious Disease"},
          # Populations and Place
          {"subject": "ANTH", "catalog": "451",  "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False, "choose_from_group": "Populations and Place", "notes": "Field: Africa. Cannot take both ANTH 451 and GEOG 451."},
          {"subject": "EDKP", "catalog": "204",  "title": "Health Education",                           "credits": 3, "is_required": False, "choose_from_group": "Populations and Place"},
          {"subject": "GEOG", "catalog": "451",  "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False, "choose_from_group": "Populations and Place", "notes": "Field: Africa. Cannot take both ANTH 451 and GEOG 451."},
          {"subject": "GEOG", "catalog": "498",  "title": "Humans in Tropical Environments",            "credits": 3, "is_required": False, "choose_from_group": "Populations and Place", "notes": "Alternate years. Field: Panama."},
          {"subject": "HIST", "catalog": "335",  "title": "Science and Medicine in Canada",             "credits": 3, "is_required": False, "choose_from_group": "Populations and Place"},
          {"subject": "HIST", "catalog": "510",  "title": "Environmental History of Latin America (Field)", "credits": 3, "is_required": False, "choose_from_group": "Populations and Place", "notes": "Alternate years. Field: Panama."},
          {"subject": "SOCI", "catalog": "520",  "title": "Migration and Immigrant Groups",             "credits": 3, "is_required": False, "choose_from_group": "Populations and Place"},
          {"subject": "SOCI", "catalog": "525",  "title": "Health Care Systems in Comparative Perspective", "credits": 3, "is_required": False, "choose_from_group": "Populations and Place"},
          {"subject": "SOCI", "catalog": "550",  "title": "Developing Societies",                       "credits": 3, "is_required": False, "choose_from_group": "Populations and Place"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  B.A. FACULTY PROGRAM – ECONOMICS AND THE EARTH'S ENVIRONMENT (54 cr)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "environment_economics_earth_ba",
    "name":          "Faculty Program Environment – Economics and the Earth's Environment (B.A.) (54 credits)",
    "program_type":  "major",
    "faculty":       "School of Environment",
    "total_credits": 54,
    "description": (
      "Open only to students in the B.A. degree. Human society is dependent upon geological "
      "processes and the resources they produce. Our use of resources creates waste, and "
      "geologic processes determine the fate of wastes in the environment. Economics "
      "frequently affects what energy sources power our society and how our wastes are "
      "treated. Students learn the fundamentals of both economics and Earth sciences and "
      "how they interact with environmental outcomes. "
      "Pre-/co-requisites (not in 54 cr): MATH 139 or 140; AECH 110 or CHEM 110. "
      "Maximum 34 credits at the 200-level; minimum 12 credits at the 400+ level."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/environment/programs/ba-faculty-program-environment/environment-economics-earths-ba/",
    "blocks": [
      {
        "block_key":      "econ_earth_ba_core_required",
        "title":          "Core: Required Courses (18 credits)",
        "block_type":     "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "All six core ENVR courses required.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment",              "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Core required – start here in U1"},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Core required – take in U1"},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth",                  "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment",   "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "301", "title": "Environmental Research Design",       "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Required – take after ENVR 200–203"},
          {"subject": "ENVR", "catalog": "400", "title": "Environmental Thought",               "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Required senior course"},
        ],
      },
      {
        "block_key":      "econ_earth_ba_senior_research",
        "title":          "Core: Senior Research Project (3 credits*)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE. Only 3 credits applied to program; extra from 6-cr field courses count as electives.",
        "sort_order": 2,
        "courses": [
          {"subject": "ENVR", "catalog": "401",  "title": "Environmental Research",             "credits": 3,  "is_required": False, "recommended": True, "recommendation_reason": "Standard on-campus research option"},
          {"subject": "AEBI", "catalog": "427",  "title": "Barbados Interdisciplinary Project", "credits": 6,  "is_required": False, "notes": "6 cr; 3 cr applied. Macdonald campus. Field: Barbados."},
          {"subject": "ENVR", "catalog": "451",  "title": "Research in Panama",                 "credits": 6,  "is_required": False, "notes": "6 cr; 3 cr applied. Field: Panama."},
          {"subject": "FSCI", "catalog": "444",  "title": "Barbados Research Project",          "credits": 6,  "is_required": False, "notes": "6 cr; 3 cr applied. Field: Barbados."},
        ],
      },
      {
        "block_key":      "econ_earth_ba_concentration_required",
        "title":          "Concentration: Required Courses (15 credits)",
        "block_type":     "required",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "All five concentration required courses must be completed.",
        "sort_order": 3,
        "courses": [
          {"subject": "ECON", "catalog": "230D1","title": "Microeconomic Theory",      "credits": 3, "is_required": True,  "recommended": True, "recommendation_reason": "Core Economics requirement – take D1 and D2 together"},
          {"subject": "ECON", "catalog": "230D2","title": "Microeconomic Theory",      "credits": 3, "is_required": True,  "notes": "Register for D1 and D2 together; no credit unless both completed in consecutive terms"},
          {"subject": "ECON", "catalog": "405",  "title": "Natural Resource Economics","credits": 3, "is_required": True,  "recommended": True, "recommendation_reason": "Key upper-year Economics requirement"},
          {"subject": "EPSC", "catalog": "210",  "title": "Introductory Mineralogy",   "credits": 3, "is_required": True,  "recommended": True, "recommendation_reason": "Core Earth Sciences requirement"},
          {"subject": "EPSC", "catalog": "240",  "title": "Geology in the Field",      "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key":      "econ_earth_ba_stats",
        "title":          "Concentration: Statistics (3 credits)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE statistics course (or equivalent).",
        "sort_order": 4,
        "courses": [
          {"subject": "AEMA", "catalog": "310",  "title": "Statistical Methods 1",               "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "GEOG", "catalog": "202",  "title": "Statistics and Spatial Analysis",     "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "203",  "title": "Principles of Statistics 1",          "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Widely available statistics option"},
        ],
      },
      {
        "block_key":      "econ_earth_ba_economics_comp",
        "title":          "Concentration: Economics – choose 6 credits",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Choose 6 credits from the following Economics electives.",
        "sort_order": 5,
        "courses": [
          {"subject": "AGEC", "catalog": "333",  "title": "Resource Economics",               "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ECON", "catalog": "209",  "title": "Macroeconomic Analysis and Applications", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "326",  "title": "Ecological Economics",             "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Highly relevant elective"},
          {"subject": "ECON", "catalog": "347",  "title": "Economics of Climate Change",      "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Highly relevant elective"},
          {"subject": "ECON", "catalog": "416",  "title": "Topics in Economic Development 2", "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "511",  "title": "Energy, Economy and Environment",  "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key":      "econ_earth_ba_advanced_area1",
        "title":          "Concentration: Advanced Courses – Area 1: Development / Environmental Management (choose from area)",
        "block_type":     "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     "Advanced Courses (9 credits from 2 Areas)",
        "notes":          "Choose 9 credits total from Area 1 and Area 2 combined, with courses from at least two different areas. Note: Cannot take both ENVB 529 and GEOG 201; BIOL 451 and NRSC 451; ANTH 451 and GEOG 451.",
        "sort_order": 6,
        "courses": [
          {"subject": "AEBI", "catalog": "423",  "title": "Sustainable Land Use",                     "credits": 3, "is_required": False, "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "AGRI", "catalog": "550",  "title": "Sustained Tropical Agriculture",           "credits": 3, "is_required": False, "notes": "Macdonald campus. Alternate years, Panama."},
          {"subject": "ANTH", "catalog": "451",  "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False, "notes": "Field: Africa. Cannot take with GEOG 451."},
          {"subject": "BIOL", "catalog": "451",  "title": "Research in Ecology and Development in Africa", "credits": 3, "is_required": False, "notes": "Field: Africa. Cannot take with NRSC 451."},
          {"subject": "ECON", "catalog": "305",  "title": "Industrial Organization",                  "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "313",  "title": "Economic Development 1",                  "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "314",  "title": "Economic Development 2",                  "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "408",  "title": "Public Sector Economics 1",               "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "409",  "title": "Public Sector Economics 2",               "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "437",  "title": "Assessing Environmental Impact",          "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ENVB", "catalog": "529",  "title": "GIS for Natural Resource Management",     "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with GEOG 201."},
          {"subject": "ENVR", "catalog": "421",  "title": "Montreal: Environmental History and Sustainability", "credits": 3, "is_required": False, "notes": "Alternate years, May term"},
          {"subject": "ENVR", "catalog": "422",  "title": "Montreal Urban Sustainability Analysis",  "credits": 3, "is_required": False, "notes": "Alternate years, May term"},
          {"subject": "GEOG", "catalog": "201",  "title": "Introductory Geo-Information Science",    "credits": 3, "is_required": False, "notes": "Cannot take with ENVB 529."},
          {"subject": "GEOG", "catalog": "302",  "title": "Environmental Management 1",              "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "340",  "title": "Sustainability in the Caribbean",         "credits": 3, "is_required": False, "notes": "Field: Barbados."},
          {"subject": "GEOG", "catalog": "404",  "title": "Environmental Management 2",              "credits": 3, "is_required": False, "notes": "Field: Africa."},
          {"subject": "GEOG", "catalog": "451",  "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False, "notes": "Field: Africa. Cannot take with ANTH 451."},
          {"subject": "GEOG", "catalog": "498",  "title": "Humans in Tropical Environments",         "credits": 3, "is_required": False, "notes": "Alternate years. Field: Panama."},
          {"subject": "HIST", "catalog": "510",  "title": "Environmental History of Latin America (Field)", "credits": 3, "is_required": False, "notes": "Alternate years. Field: Panama."},
          {"subject": "MIME", "catalog": "320",  "title": "Extraction of Energy Resources",         "credits": 3, "is_required": False},
          {"subject": "NRSC", "catalog": "451",  "title": "Research in Ecology and Development in Africa", "credits": 3, "is_required": False, "notes": "Macdonald campus. Field: Africa. Cannot take with BIOL 451."},
        ],
      },
      {
        "block_key":      "econ_earth_ba_advanced_area2",
        "title":          "Concentration: Advanced Courses – Area 2: Environmental Resources (choose from area)",
        "block_type":     "group",
        "credits_needed": None,
        "courses_needed": None,
        "group_name":     "Advanced Courses (9 credits from 2 Areas)",
        "notes":          "9 credits total from both Area 1 and Area 2. Note: Cannot take both BREE 217 and GEOG 322; ENVB 305 and BIOL 308.",
        "sort_order": 7,
        "courses": [
          {"subject": "ATOC", "catalog": "341",  "title": "Caribbean Climate and Weather",            "credits": 3, "is_required": False, "notes": "Field: Barbados."},
          {"subject": "BIOL", "catalog": "308",  "title": "Ecological Dynamics",                     "credits": 3, "is_required": False, "notes": "Cannot take with ENVB 305."},
          {"subject": "BIOL", "catalog": "343",  "title": "Biodiversity in the Caribbean",           "credits": 3, "is_required": False, "notes": "Field: Barbados."},
          {"subject": "BREE", "catalog": "217",  "title": "Hydrology and Water Resources",           "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with GEOG 322."},
          {"subject": "ENVB", "catalog": "305",  "title": "Population and Community Ecology",        "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with BIOL 308."},
          {"subject": "EPSC", "catalog": "325",  "title": "Environmental Geochemistry",              "credits": 3, "is_required": False},
          {"subject": "EPSC", "catalog": "355",  "title": "Sedimentary Geology",                     "credits": 3, "is_required": False, "notes": "Offered winter 2025 and alternate winters"},
          {"subject": "EPSC", "catalog": "549",  "title": "Hydrogeology",                            "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "322",  "title": "Environmental Hydrology",                 "credits": 3, "is_required": False, "notes": "Cannot take with BREE 217."},
          {"subject": "SOIL", "catalog": "300",  "title": "Geosystems",                              "credits": 3, "is_required": False, "notes": "Macdonald campus"},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  B.A. FACULTY PROGRAM – ENVIRONMENT AND DEVELOPMENT (54 cr)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "environment_development_ba",
    "name":          "Faculty Program Environment – Environment and Development (B.A.) (54 credits)",
    "program_type":  "major",
    "faculty":       "School of Environment",
    "total_credits": 54,
    "description": (
      "Open only to students in the B.A. degree. An introduction to theories, concepts "
      "and approaches associated with the complexities between environment and development. "
      "The problems and solutions to the development/environmental crisis, which include: "
      "the natural world; theories behind economic development and growth, and of the "
      "cultural constructs of nature and environment; knowledge of global economic and "
      "environmental organizations; and sustainability and the climate crisis. "
      "Pre-/co-requisites (not in 54 cr): MATH 139 or 140; BIOL 111 or CHEM 110 or PHYS 101 or equivalent. "
      "Maximum 30 credits at the 200-level; minimum 12 credits at the 400+ level."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/environment/programs/ba-faculty-program-environment/environment-development-ba/",
    "blocks": [
      {
        "block_key":      "env_dev_ba_required",
        "title":          "Required Courses (30 credits)",
        "block_type":     "required",
        "credits_needed": 30,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "All 10 listed courses are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "ANTH", "catalog": "339",  "title": "Ecological Anthropology",          "credits": 3, "is_required": True},
          {"subject": "ECON", "catalog": "313",  "title": "Economic Development 1",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Core development economics – take D1 before D2"},
          {"subject": "ECON", "catalog": "314",  "title": "Economic Development 2",           "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "200",  "title": "The Global Environment",           "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Core required – start here in U1"},
          {"subject": "ENVR", "catalog": "201",  "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Core required – take in U1"},
          {"subject": "ENVR", "catalog": "202",  "title": "The Evolving Earth",               "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203",  "title": "Knowledge, Ethics and Environment","credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "301",  "title": "Environmental Research Design",    "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Required – take after ENVR 200–203"},
          {"subject": "ENVR", "catalog": "400",  "title": "Environmental Thought",            "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Required senior course – take in U3"},
          {"subject": "GEOG", "catalog": "302",  "title": "Environmental Management 1",      "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key":      "env_dev_ba_senior_research",
        "title":          "Complementary: Senior Research Project (3 credits*)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE. Only 3 credits applied; extra from 6-cr field courses count as electives.",
        "sort_order": 2,
        "courses": [
          {"subject": "AEBI", "catalog": "427",  "title": "Barbados Interdisciplinary Project",  "credits": 6, "is_required": False, "notes": "6 cr; 3 cr applied. Macdonald campus. Field: Barbados."},
          {"subject": "ENVR", "catalog": "401",  "title": "Environmental Research",              "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Standard on-campus research option"},
          {"subject": "ENVR", "catalog": "451",  "title": "Research in Panama",                 "credits": 6, "is_required": False, "notes": "6 cr; 3 cr applied. Field: Panama."},
          {"subject": "FSCI", "catalog": "444",  "title": "Barbados Research Project",          "credits": 6, "is_required": False, "notes": "6 cr; 3 cr applied. Field: Barbados."},
          {"subject": "GEOG", "catalog": "451",  "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False, "notes": "Field: Africa."},
        ],
      },
      {
        "block_key":      "env_dev_ba_microeconomics",
        "title":          "Complementary: Microeconomics (3 credits)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE microeconomics course.",
        "sort_order": 3,
        "courses": [
          {"subject": "AGEC", "catalog": "200",  "title": "Principles of Microeconomics",               "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ECON", "catalog": "208",  "title": "Microeconomic Analysis and Applications",    "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Standard microeconomics option"},
        ],
      },
      {
        "block_key":      "env_dev_ba_statistics",
        "title":          "Complementary: Statistics (3 credits)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          "Choose ONE statistics course or equivalent.",
        "sort_order": 4,
        "courses": [
          {"subject": "AEMA", "catalog": "310",  "title": "Statistical Methods 1",               "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "GEOG", "catalog": "202",  "title": "Statistics and Spatial Analysis",     "credits": 3, "is_required": False},
          {"subject": "MATH", "catalog": "203",  "title": "Principles of Statistics 1",          "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Widely available statistics option"},
          {"subject": "PSYC", "catalog": "204",  "title": "Introduction to Psychological Statistics", "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key":      "env_dev_ba_advanced_development",
        "title":          "Complementary: Advanced Development Courses (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Choose 6 credits of advanced development courses.",
        "sort_order": 5,
        "courses": [
          {"subject": "AGEC", "catalog": "442",  "title": "Economics of International Agricultural Development", "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "AGRI", "catalog": "411",  "title": "Global Issues on Development, Food and Agriculture", "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "GEOG", "catalog": "408",  "title": "Geography of Development",                  "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Highly relevant advanced development course"},
          {"subject": "GEOG", "catalog": "409",  "title": "Geographies of Developing Asia",            "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "423",  "title": "Dilemmas of Development",                   "credits": 3, "is_required": False, "notes": "Field: Africa."},
          {"subject": "GEOG", "catalog": "514",  "title": "Climate Change Vulnerability and Adaptation","credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "525",  "title": "Asian Cities in the 21st Century",          "credits": 3, "is_required": False},
        ],
      },
      {
        "block_key":      "env_dev_ba_natural_sciences",
        "title":          "Complementary: Natural Sciences (3 credits)",
        "block_type":     "choose_courses",
        "credits_needed": 3,
        "courses_needed": 1,
        "group_name":     None,
        "notes":          (
          "Choose 3 credits. Note: BIOL 308 or ENVB 305 (not both); "
          "BIOL 465 or WILD 421 (not both); ENVB 210 or GEOG 305 (not both); "
          "BREE 217 or GEOG 322 (not both)."
        ),
        "sort_order": 6,
        "courses": [
          {"subject": "AEBI", "catalog": "421",  "title": "Tropical Horticultural Ecology",       "credits": 3, "is_required": False, "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "AGRI", "catalog": "550",  "title": "Sustained Tropical Agriculture",       "credits": 3, "is_required": False, "notes": "Macdonald campus. Alternate years, Panama."},
          {"subject": "ATOC", "catalog": "341",  "title": "Caribbean Climate and Weather",        "credits": 3, "is_required": False, "notes": "Field: Barbados."},
          {"subject": "BIOL", "catalog": "308",  "title": "Ecological Dynamics",                  "credits": 3, "is_required": False, "notes": "Cannot take with ENVB 305."},
          {"subject": "BIOL", "catalog": "343",  "title": "Biodiversity in the Caribbean",        "credits": 3, "is_required": False, "notes": "Field: Barbados."},
          {"subject": "BIOL", "catalog": "451",  "title": "Research in Ecology and Development in Africa", "credits": 3, "is_required": False, "notes": "Field: Africa."},
          {"subject": "BIOL", "catalog": "465",  "title": "Conservation Biology",                 "credits": 3, "is_required": False, "notes": "Cannot take with WILD 421."},
          {"subject": "BIOL", "catalog": "553",  "title": "Neotropical Environments",             "credits": 3, "is_required": False, "notes": "Field: Panama."},
          {"subject": "BREE", "catalog": "217",  "title": "Hydrology and Water Resources",        "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with GEOG 322."},
          {"subject": "ENVB", "catalog": "210",  "title": "The Biophysical Environment",          "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with GEOG 305."},
          {"subject": "ENVB", "catalog": "305",  "title": "Population and Community Ecology",     "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with BIOL 308."},
          {"subject": "GEOG", "catalog": "305",  "title": "Soils and Environment",                "credits": 3, "is_required": False, "notes": "Cannot take with ENVB 210."},
          {"subject": "GEOG", "catalog": "322",  "title": "Environmental Hydrology",              "credits": 3, "is_required": False, "notes": "Cannot take with BREE 217."},
          {"subject": "NRSC", "catalog": "451",  "title": "Research in Ecology and Development in Africa", "credits": 3, "is_required": False, "notes": "Macdonald campus. Field: Africa."},
          {"subject": "NUTR", "catalog": "501",  "title": "Nutrition in the Majority World",      "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "NUTR", "catalog": "505",  "title": "Public Health Nutrition",              "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "PARA", "catalog": "410",  "title": "Environment and Infection",            "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "WILD", "catalog": "421",  "title": "Wildlife Conservation",               "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with BIOL 465."},
        ],
      },
      {
        "block_key":      "env_dev_ba_social_sciences",
        "title":          "Complementary: Social Sciences (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Choose 6 credits from the Social Sciences list.",
        "sort_order": 7,
        "courses": [
          {"subject": "AEBI", "catalog": "423",  "title": "Sustainable Land Use",                       "credits": 3, "is_required": False, "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "AEBI", "catalog": "425",  "title": "Tropical Energy and Food",                   "credits": 3, "is_required": False, "notes": "Macdonald campus. Field: Barbados."},
          {"subject": "AGEC", "catalog": "333",  "title": "Resource Economics",                         "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ANTH", "catalog": "322",  "title": "Social Change in Modern Africa",             "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "451",  "title": "Research in Society and Development in Africa", "credits": 3, "is_required": False, "notes": "Field: Africa."},
          {"subject": "ANTH", "catalog": "512",  "title": "Political Ecology",                          "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "326",  "title": "Ecological Economics",                       "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Highly relevant elective"},
          {"subject": "ECON", "catalog": "347",  "title": "Economics of Climate Change",                "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "405",  "title": "Natural Resource Economics",                 "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "511",  "title": "Energy, Economy and Environment",            "credits": 3, "is_required": False},
          {"subject": "ENVR", "catalog": "421",  "title": "Montreal: Environmental History and Sustainability", "credits": 3, "is_required": False, "notes": "Alternate years, May term"},
          {"subject": "ENVR", "catalog": "422",  "title": "Montreal Urban Sustainability Analysis",     "credits": 3, "is_required": False, "notes": "Alternate years, May term"},
          {"subject": "GEOG", "catalog": "201",  "title": "Introductory Geo-Information Science",       "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "311",  "title": "Economic Geography",                         "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "331",  "title": "Urban Social Geography",                     "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "340",  "title": "Sustainability in the Caribbean",            "credits": 3, "is_required": False, "notes": "Field: Barbados."},
          {"subject": "GEOG", "catalog": "404",  "title": "Environmental Management 2",                 "credits": 3, "is_required": False, "notes": "Field: Africa."},
          {"subject": "GEOG", "catalog": "496",  "title": "Geographical Excursion",                     "credits": 3, "is_required": False, "notes": "Field: Barbados. Fee charged."},
          {"subject": "GEOG", "catalog": "498",  "title": "Humans in Tropical Environments",            "credits": 3, "is_required": False, "notes": "Alternate years. Field: Panama."},
          {"subject": "GEOG", "catalog": "510",  "title": "Humid Tropical Environments",                "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "514",  "title": "Climate Change Vulnerability and Adaptation","credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "530",  "title": "Global Land and Water Resources",            "credits": 3, "is_required": False},
          {"subject": "HIST", "catalog": "292",  "title": "History and the Environment",                "credits": 3, "is_required": False},
          {"subject": "HIST", "catalog": "510",  "title": "Environmental History of Latin America (Field)", "credits": 3, "is_required": False, "notes": "Alternate years. Field: Panama."},
          {"subject": "INTD", "catalog": "360",  "title": "Environmental Challenges in Development",    "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Highly relevant to this concentration"},
          {"subject": "POLI", "catalog": "345",  "title": "International Organizations",                "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "350",  "title": "Global Environmental Politics",              "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Highly relevant to this concentration"},
          {"subject": "POLI", "catalog": "445",  "title": "International Political Economy: Monetary Relations", "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "254",  "title": "Development and Underdevelopment",           "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "331",  "title": "Population and Environment",                 "credits": 3, "is_required": False},
          {"subject": "WCOM", "catalog": "314",  "title": "Communicating Science",                      "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  ENVIRONMENT MINOR CONCENTRATION (B.A.) – 18 credits
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "environment_minor_ba",
    "name":          "Environment Minor Concentration (B.A.) (18 credits)",
    "program_type":  "minor",
    "faculty":       "School of Environment",
    "total_credits": 18,
    "description": (
      "Open to students in the Faculties of Arts, Law, Music, and Management. "
      "The Minor Concentration in Environment exposes students to different approaches, "
      "perspectives, and world views that will help them gain an understanding of the "
      "complexity and conflicts that underlie environmental problems. Complements "
      "any major or faculty program outside the Bieler School of Environment. "
      "Requires all four core ENVR courses (200, 201, 202, 203) plus 6 credits of "
      "electives with adviser approval (at least 3 credits in natural sciences). "
      "No overlap allowed with the student's major or second minor. "
      "Students can add this to their record in Minerva."
    ),
    "ecalendar_url": "https://www.mcgill.ca/study/2024-2025/faculties/environment/undergraduate/programs/bachelor-arts-ba-minor-concentration-environment",
    "blocks": [
      {
        "block_key":      "env_minor_ba_required",
        "title":          "Required Courses (12 credits)",
        "block_type":     "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "All four core ENVR courses are required for the minor.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment",                  "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Start here – first required course"},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth",                      "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment",       "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key":      "env_minor_ba_complementary",
        "title":          "Complementary Courses (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Choose 6 credits of environmentally-related courses with adviser approval. "
          "At least 3 credits must be in natural sciences. All courses at the 200 level or above. "
          "No overlap with the student's major program. Consult the Program Adviser for the "
          "full approved course list, which spans Social Sciences/Policy and Natural Sciences/Technology."
        ),
        "sort_order": 2,
        "courses": [
          # Social Sciences and Policy (selected examples)
          {"subject": "ANTH", "catalog": "206",  "title": "Environment and Culture",                   "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "339",  "title": "Ecological Anthropology",                   "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "225",  "title": "Economics of the Environment",              "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "326",  "title": "Ecological Economics",                      "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "347",  "title": "Economics of Climate Change",               "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "405",  "title": "Natural Resource Economics",                "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "302",  "title": "Environmental Management 1",                "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "303",  "title": "Health Geography",                          "credits": 3, "is_required": False},
          {"subject": "HIST", "catalog": "292",  "title": "History and the Environment",               "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "350",  "title": "Global Environmental Politics",             "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Excellent upper-level complementary choice"},
          {"subject": "SOCI", "catalog": "254",  "title": "Development and Underdevelopment",          "credits": 3, "is_required": False},
          # Natural Sciences and Technology (selected examples)
          {"subject": "BIOL", "catalog": "308",  "title": "Ecological Dynamics",                       "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "465",  "title": "Conservation Biology",                      "credits": 3, "is_required": False},
          {"subject": "ENVB", "catalog": "437",  "title": "Assessing Environmental Impact",            "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "216",  "title": "Climate Change: From Science to Solution",  "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "322",  "title": "Environmental Hydrology",                   "credits": 3, "is_required": False},
        ],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  DIPLOMA IN ENVIRONMENT – 30 credits
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "environment_diploma",
    "name":          "Environment Diploma (30 credits)",
    "program_type":  "diploma",
    "faculty":       "School of Environment",
    "total_credits": 30,
    "description": (
      "For students who have already completed an undergraduate degree. The Diploma in "
      "Environment is designed for students with an undergraduate degree who wish to enrich "
      "or reorient their training, supplementing their previous specialization with "
      "additional undergraduate-level course work. Requires 30 credits of full-time or "
      "part-time study; taken full-time it is a one-year program. Students holding a "
      "B.Sc., B.A., or equivalent can apply through the Faculty of Science, Faculty of "
      "Agricultural and Environmental Sciences, or the Faculty of Arts. "
      "All courses at the 200 level or above; at least 6 credits at the 400+ level; "
      "all completed with a grade of C or better."
    ),
    "ecalendar_url": "https://coursecatalogue.mcgill.ca/en/undergraduate/environment/programs/diploma-environment/environment-dip/",
    "blocks": [
      {
        "block_key":      "env_diploma_required",
        "title":          "Required Courses (18 credits)",
        "block_type":     "required",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "All six core ENVR courses are required.",
        "sort_order": 1,
        "courses": [
          {"subject": "ENVR", "catalog": "200", "title": "The Global Environment",              "credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Start here"},
          {"subject": "ENVR", "catalog": "201", "title": "Society, Environment and Sustainability", "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "202", "title": "The Evolving Earth",                  "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "203", "title": "Knowledge, Ethics and Environment",   "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "301", "title": "Environmental Research Design",       "credits": 3, "is_required": True},
          {"subject": "ENVR", "catalog": "400", "title": "Environmental Thought",               "credits": 3, "is_required": True},
        ],
      },
      {
        "block_key":      "env_diploma_complementary",
        "title":          "Complementary Courses (12 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Choose 12 credits of environmentally-related courses with Program Adviser approval. "
          "3 credits must be outside the student's previous degree field (natural sciences for arts graduates; "
          "social sciences for science graduates). 9 credits in a chosen focus area; at least 6 of these at "
          "the 400-level or higher. All courses at the 200+ level; grade of C or better required. "
          "The following are suggested courses — alternatives may be approved by the adviser."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "AGEC", "catalog": "231",  "title": "Economic Systems of Agriculture",         "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "AGEC", "catalog": "333",  "title": "Resource Economics",                      "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "AGEC", "catalog": "430",  "title": "Agriculture, Food and Resource Policy",   "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "AGEC", "catalog": "442",  "title": "Economics of International Agricultural Development", "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "AGRI", "catalog": "411",  "title": "Global Issues on Development, Food and Agriculture", "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ANTH", "catalog": "206",  "title": "Environment and Culture",                 "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "212",  "title": "Anthropology of Development",             "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "339",  "title": "Ecological Anthropology",                 "credits": 3, "is_required": False},
          {"subject": "ANTH", "catalog": "418",  "title": "Environment and Development",             "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "308",  "title": "Ecological Dynamics",                     "credits": 3, "is_required": False, "notes": "Cannot take with ENVB 305."},
          {"subject": "BIOL", "catalog": "465",  "title": "Conservation Biology",                    "credits": 3, "is_required": False, "notes": "Cannot take with WILD 421."},
          {"subject": "BREE", "catalog": "217",  "title": "Hydrology and Water Resources",           "credits": 3, "is_required": False, "notes": "Macdonald campus. Only one of BREE 217, CIVE 323, GEOG 322."},
          {"subject": "CHEM", "catalog": "270",  "title": "Introductory Organic Chemistry 1",        "credits": 3, "is_required": False},
          {"subject": "CHEM", "catalog": "281",  "title": "Inorganic Chemistry 1",                   "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "225",  "title": "Environmental Engineering",               "credits": 3, "is_required": False},
          {"subject": "CIVE", "catalog": "323",  "title": "Hydrology and Water Resources",           "credits": 3, "is_required": False, "notes": "Only one of BREE 217, CIVE 323, GEOG 322."},
          {"subject": "CIVE", "catalog": "550",  "title": "Water Resources Management",              "credits": 3, "is_required": False},
          {"subject": "COMP", "catalog": "202",  "title": "Foundations of Programming",              "credits": 3, "is_required": False, "notes": "Cannot take with COMP 204."},
          {"subject": "COMP", "catalog": "204",  "title": "Computer Programming for Life Sciences",  "credits": 3, "is_required": False, "notes": "Cannot take with COMP 202."},
          {"subject": "ECON", "catalog": "225",  "title": "Economics of the Environment",            "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "326",  "title": "Ecological Economics",                    "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "347",  "title": "Economics of Climate Change",             "credits": 3, "is_required": False},
          {"subject": "ECON", "catalog": "405",  "title": "Natural Resource Economics",              "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Strong upper-level option"},
          {"subject": "ENVB", "catalog": "210",  "title": "The Biophysical Environment",             "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ENVB", "catalog": "305",  "title": "Population and Community Ecology",        "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with BIOL 308."},
          {"subject": "ENVB", "catalog": "410",  "title": "Ecosystem Ecology",                       "credits": 3, "is_required": False, "notes": "Macdonald campus"},
          {"subject": "ENVB", "catalog": "529",  "title": "GIS for Natural Resource Management",     "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with GEOG 201."},
          {"subject": "ENVR", "catalog": "422",  "title": "Montreal Urban Sustainability Analysis",  "credits": 3, "is_required": False, "notes": "Alternate years, May term"},
          {"subject": "EPSC", "catalog": "201",  "title": "Understanding Planet Earth",              "credits": 3, "is_required": False, "notes": "Cannot take with EPSC 233."},
          {"subject": "EPSC", "catalog": "233",  "title": "Earth and Life Through Time",             "credits": 3, "is_required": False, "notes": "Cannot take with EPSC 201."},
          {"subject": "EPSC", "catalog": "549",  "title": "Hydrogeology",                            "credits": 3, "is_required": False},
          {"subject": "ESYS", "catalog": "301",  "title": "Earth System Modelling",                  "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "200",  "title": "Physical Geography",                      "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "201",  "title": "Introductory Geo-Information Science",    "credits": 3, "is_required": False, "notes": "Cannot take with ENVB 529."},
          {"subject": "GEOG", "catalog": "216",  "title": "Climate Change: From Science to Solution","credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "302",  "title": "Environmental Management 1",              "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "322",  "title": "Environmental Hydrology",                 "credits": 3, "is_required": False, "notes": "Only one of BREE 217, CIVE 323, GEOG 322."},
          {"subject": "GEOG", "catalog": "423",  "title": "Dilemmas of Development",                 "credits": 3, "is_required": False, "notes": "Field: Africa."},
          {"subject": "GEOG", "catalog": "514",  "title": "Climate Change Vulnerability and Adaptation", "credits": 3, "is_required": False},
          {"subject": "GEOG", "catalog": "530",  "title": "Global Land and Water Resources",         "credits": 3, "is_required": False},
          {"subject": "HIST", "catalog": "292",  "title": "History and the Environment",             "credits": 3, "is_required": False},
          {"subject": "POLI", "catalog": "350",  "title": "Global Environmental Politics",           "credits": 3, "is_required": False, "recommended": True, "recommendation_reason": "Strong upper-level complementary option"},
          {"subject": "SOCI", "catalog": "254",  "title": "Development and Underdevelopment",        "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "307",  "title": "Globalization",                           "credits": 3, "is_required": False},
          {"subject": "SOCI", "catalog": "386",  "title": "Contemporary Social Movements",           "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "506",  "title": "Environmental Policy and Planning",       "credits": 3, "is_required": False},
          {"subject": "URBP", "catalog": "551",  "title": "Urban Design and Planning",               "credits": 3, "is_required": False},
          {"subject": "WCOM", "catalog": "314",  "title": "Communicating Science",                   "credits": 3, "is_required": False},
          {"subject": "WILD", "catalog": "421",  "title": "Wildlife Conservation",                   "credits": 3, "is_required": False, "notes": "Macdonald campus. Cannot take with BIOL 465."},
        ],
      },
    ],
  },

]


# ══════════════════════════════════════════════════════════════════════════
#  DATABASE SEED FUNCTION
# ══════════════════════════════════════════════════════════════════════════

def seed_degree_requirements(supabase):
    """
    Insert all Bieler School of Environment degree requirements into Supabase.
    Safe to re-run: uses upsert on program_key, then deletes+reinserts blocks.
    """
    inserted_programs = 0
    inserted_blocks   = 0
    inserted_courses  = 0

    for prog in ENVIRONMENT_PROGRAMS:
        prog_data = {
            "program_key":   prog["program_key"],
            "name":          prog["name"],
            "faculty":       prog.get("faculty", "School of Environment"),
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
