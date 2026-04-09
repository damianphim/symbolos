"""
McGill Faculty of Agricultural & Environmental Sciences – Degree Requirements Seed Data
Source: McGill eCalendar 2024-2025 & Course Catalogue 2025-2026
https://coursecatalogue.mcgill.ca/en/undergraduate/agri-env-sci/
https://www.mcgill.ca/study/2024-2025/faculties/macdonald/undergraduate/

This file covers core AES undergraduate programs:
  - Environmental Biology Major   – B.Sc.(Ag.Env.Sc.)   (42 credits)
  - Agricultural Economics Major  – B.Sc.(Ag.Env.Sc.)   (42 credits)
  - Life Sciences (Biological and Agricultural) Major – B.Sc.(Ag.Env.Sc.) (42 credits)
  - Bioresource Engineering Major – B.Eng.(Bioresource) (113 credits)
  - Environmental Biology Honours – B.Sc.(Ag.Env.Sc.)   (54 credits)

Accuracy notes:
  - All B.Sc.(Ag.Env.Sc.) programs also require the Foundation/Freshman year
    (30 credits, not counted in the major credit total).
  - B.Eng.(Bioresource) total of 113 credits includes 30 Foundation credits.
  - All program courses require a minimum grade of C (or C+ in some BREE courses).
  - Each major must be paired with at least one Specialization (18–24 credits).
"""

import logging
logger = logging.getLogger(__name__)

AES_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════════
  #  ENVIRONMENTAL BIOLOGY MAJOR – B.Sc.(Ag.Env.Sc.)  (42 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "envbio_bsc_agenvsc",
    "name":          "Environmental Biology Major (B.Sc.(Ag.Env.Sc.)) (42 credits)",
    "program_type":  "major",
    "faculty":       "Faculty of Agricultural and Environmental Sciences",
    "total_credits": 42,
    "description": (
      "The Environmental Biology Major focuses on the biology, diversity, and ecology "
      "of a broad range of organisms — from plants and vertebrate animals to insects, "
      "fungi, and microbes. Strong emphasis is placed on the ecosystems that species "
      "inhabit and the constraints imposed by the physical environment and environmental "
      "change. Significant field components are integrated throughout the course sets, "
      "making use of McGill's Macdonald Campus and the St. Lawrence Lowlands ecosystem. "
      "Graduates are trained as ecologists, taxonomists, field biologists, and ecosystem "
      "scientists. The major must be paired with at least one Specialization (18–24 cr); "
      "recommended pairings include Applied Ecology, Wildlife Biology, or Plant Biology."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/macdonald/undergraduate/programs/"
      "bachelor-science-agricultural-and-environmental-sciences-bscagenvsc-major-environmental-biology"
    ),
    "blocks": [
      {
        "block_key":      "envbio_required",
        "title":          "Required Courses (36 credits)",
        "block_type":     "required",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "All 12 courses are required. LSCI 211 has a corequisite of FDSC 230. "
          "ENVB 410 requires ENVB 222 and AEMA 310 (or permission of instructor). "
          "Field trips in ENVB 222 and ENVB 410 carry a small additional fee (~$20)."
        ),
        "sort_order": 1,
        "courses": [
          # --- Foundation biology & evolution ---
          {"subject": "AEBI", "catalog": "210", "title": "Organisms 1",              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core U1 course – biology of plants and plant-based systems; start here"},
          {"subject": "AEBI", "catalog": "211", "title": "Organisms 2",              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core U1 course – animal diversity; take alongside AEBI 210"},
          {"subject": "AEBI", "catalog": "212", "title": "Evolution and Phylogeny",  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core U1 – tree of life and evolutionary theory"},
          # --- Communications & stats ---
          {"subject": "AEHM", "catalog": "205", "title": "Science Literacy",         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required writing/communication course; take in U1"},
          {"subject": "AEMA", "catalog": "310", "title": "Statistical Methods 1",    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required statistics; prerequisite for ENVB 410"},
          # --- Environmental biology core ---
          {"subject": "ENVB", "catalog": "210", "title": "The Biophysical Environment",   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core field-based course on climate–landform–water–soil–vegetation systems; take in U1 Fall"},
          {"subject": "ENVB", "catalog": "222", "title": "St. Lawrence Ecosystems",        "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Integrative field biology of terrestrial and aquatic ecosystems; prerequisite for ENVB 410"},
          {"subject": "ENVB", "catalog": "305", "title": "Population and Community Ecology","credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Intermediate ecology: population dynamics, competition, food webs; take in U2"},
          {"subject": "ENVB", "catalog": "410", "title": "Ecosystem Ecology",              "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Senior ecosystem-level course; take in U3 Fall after completing ENVB 222 and AEMA 310"},
          # --- Life sciences support ---
          {"subject": "LSCI", "catalog": "204", "title": "Genetics",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required genetics; covers classical, molecular, and population genetics"},
          {"subject": "LSCI", "catalog": "211", "title": "Biochemistry 1",         "credits": 3, "is_required": True,  "recommended": False},
          {"subject": "LSCI", "catalog": "230", "title": "Introductory Microbiology","credits": 3, "is_required": True,  "recommended": False},
        ],
      },
      {
        "block_key":      "envbio_complementary",
        "title":          "Complementary Courses (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Select 6 credits from the approved complementary list below.",
        "sort_order": 2,
        "courses": [
          {"subject": "ENTO", "catalog": "330", "title": "Insect Biology",                    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Excellent complement to ecology; covers insect morphology, diversity, and metamorphosis"},
          {"subject": "ENVB", "catalog": "437", "title": "Assessing Environmental Impact",    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Applied senior course on environmental impact assessment"},
          {"subject": "FAES", "catalog": "300", "title": "Internship 2",                      "credits": 3, "is_required": False, "recommended": False},
          {"subject": "NRSC", "catalog": "333", "title": "Pollution and Bioremediation",      "credits": 3, "is_required": False, "recommended": False},
          {"subject": "PLNT", "catalog": "358", "title": "Flowering Plant Diversity",         "credits": 3, "is_required": False, "recommended": False},
          {"subject": "WILD", "catalog": "302", "title": "Fish Ecology",                      "credits": 3, "is_required": False, "recommended": False},
          {"subject": "WILD", "catalog": "307", "title": "Natural History of Vertebrates",    "credits": 3, "is_required": False, "recommended": False},
          {"subject": "WILD", "catalog": "350", "title": "Wildlife Ecology and Management",   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Highly recommended if pairing with Wildlife Biology specialization"},
          {"subject": "WOOD", "catalog": "441", "title": "Integrated Forest Management",      "credits": 3, "is_required": False, "recommended": False},
        ],
      },
      {
        "block_key":      "envbio_honours_research",
        "title":          "Optional: Independent Research Project (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "Optional research project (counts as electives unless pursuing Honours). "
          "Requires a willing supervisor and departmental approval. "
          "ENVB 497 must be completed with B or higher before taking ENVB 498."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "ENVB", "catalog": "497", "title": "Research Project 1",   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Honours/research project – start in U2 Winter or U3 Fall with an approved supervisor"},
          {"subject": "ENVB", "catalog": "498", "title": "Research Project 2",   "credits": 3, "is_required": False, "recommended": False, "notes": "Continuation of ENVB 497; prereq: min B in ENVB 497"},
        ],
      },
      {
        "block_key":      "envbio_specialization",
        "title":          "Specialization (18–24 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "At least one specialization must be completed. At least 18 credits within the "
          "chosen specialization must be unique (not overlapping with major or a second "
          "specialization). Recommended pairings: Applied Ecology, Wildlife Biology, or "
          "Plant Biology. A different specialization may be selected with adviser approval."
        ),
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  ENVIRONMENTAL BIOLOGY HONOURS – B.Sc.(Ag.Env.Sc.)  (54 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "envbio_honours_bsc_agenvsc",
    "name":          "Environmental Biology Honours (B.Sc.(Ag.Env.Sc.)) (54 credits)",
    "program_type":  "honours",
    "faculty":       "Faculty of Agricultural and Environmental Sciences",
    "total_credits": 54,
    "description": (
      "The Honours program in Environmental Biology adds an intensive independent "
      "research component on top of the 42-credit Major requirements. Students must "
      "have a minimum CGPA of 3.3 to enter and maintain a minimum overall CGPA of 3.3 "
      "at graduation. A willing supervisor must be secured before admission into the "
      "program. Applications are due in March or April of the U2 year. "
      "Credits from the Honours program are in addition to all Major and Specialization "
      "requirements (use your elective pool)."
    ),
    "ecalendar_url": (
      "https://coursecatalogue.mcgill.ca/en/undergraduate/agri-env-sci/programs/"
      "natural-resource-sciences/environmental-biology-honours-bsc-agenvsc/"
    ),
    "blocks": [
      {
        "block_key":      "envbio_hons_research",
        "title":          "Honours Research Courses (12 credits)",
        "block_type":     "required",
        "credits_needed": 12,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "12 credits of Honours research in the subject area of the student's Major, "
          "chosen in consultation with the Programme Director and the research supervisor. "
          "Plan A: Two 6-credit research courses. "
          "Plan B (shown): ENVB 497 + ENVB 498 project courses plus additional 400/500-level coursework."
        ),
        "sort_order": 1,
        "courses": [
          {"subject": "ENVB", "catalog": "497", "title": "Research Project 1",   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Start in U3; requires approved supervisor. Min B to continue to ENVB 498"},
          {"subject": "ENVB", "catalog": "498", "title": "Research Project 2",   "credits": 3, "is_required": True},
          {"subject": "ENVB", "catalog": "499", "title": "Honours Thesis",       "credits": 6, "is_required": True,  "recommended": True,  "recommendation_reason": "Final thesis course; take in U3 Winter"},
        ],
      },
      {
        "block_key":      "envbio_hons_400level",
        "title":          "Additional 400/500-level Courses (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "6 credits at the 400- or 500-level, normally from the Faculty of AES, "
          "chosen in consultation with the Major Programme Director and supervisor."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "ENVB", "catalog": "410", "title": "Ecosystem Ecology",            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Senior ecosystem-level course; strongly recommended for Honours students"},
          {"subject": "ENVB", "catalog": "506", "title": "Quantitative Methods: Ecology","credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Advanced stats for ecologists; prereq AEMA 310 and ENVB 305"},
          {"subject": "ENVB", "catalog": "437", "title": "Assessing Environmental Impact","credits": 3, "is_required": False, "recommended": False},
          {"subject": "WILD", "catalog": "421", "title": "Wildlife Conservation",         "credits": 3, "is_required": False, "recommended": False},
        ],
      },
      {
        "block_key":      "envbio_hons_specialization",
        "title":          "Specialization (18–24 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes":          "Same specialization requirement as the Major. Must complete at least one.",
        "sort_order": 3,
        "courses": [],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  AGRICULTURAL ECONOMICS MAJOR – B.Sc.(Ag.Env.Sc.)  (42 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "agec_bsc_agenvsc",
    "name":          "Agricultural Economics Major (B.Sc.(Ag.Env.Sc.)) (42 credits)",
    "program_type":  "major",
    "faculty":       "Faculty of Agricultural and Environmental Sciences",
    "total_credits": 42,
    "description": (
      "The Agricultural Economics Major is designed to meet demand for sustainable "
      "development as it relates to the environment and resource use, and the economics "
      "and management of the global agriculture and food system. Training in economic "
      "theory and applied areas such as marketing, finance, farm management, public "
      "policy, ecology, natural resources, and international development. Students must "
      "choose one of two Specializations: Agribusiness or Environmental Economics (24 cr each). "
      "Students taking the Agribusiness Specialization may also take the Professional "
      "Agrology for Agribusiness Specialization (required for OAQ membership)."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/macdonald/undergraduate/programs/"
      "bachelor-science-agricultural-and-environmental-sciences-bscagenvsc-major-agricultural-economics"
    ),
    "blocks": [
      {
        "block_key":      "agec_required",
        "title":          "Required Courses (36 credits)",
        "block_type":     "required",
        "credits_needed": 36,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "All 12 courses are required. AGEC 200 is a prerequisite for most upper-level "
          "AGEC courses. MGCR 211 is the Desautels intro accounting course. AGEC 330 is "
          "not always scheduled; check current eCalendar."
        ),
        "sort_order": 1,
        "courses": [
          # --- Economics core ---
          {"subject": "AGEC", "catalog": "200", "title": "Principles of Microeconomics",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Gateway course – prerequisite for all upper-level AGEC courses; take in U1 Fall"},
          {"subject": "AGEC", "catalog": "201", "title": "Principles of Macroeconomics",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core macro theory; take in U1 Winter. Prereq: AGEC 200"},
          {"subject": "AGEC", "catalog": "231", "title": "Economic Systems of Agriculture",       "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Structure of Canada's agri-food system; take in U1 Winter alongside AGEC 201"},
          {"subject": "AGEC", "catalog": "320", "title": "Intermediate Microeconomic Theory",     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Intermediate theory with linear programming; take in U2 Winter"},
          {"subject": "AGEC", "catalog": "330", "title": "Agriculture and Food Markets",          "credits": 3, "is_required": True,  "recommended": False, "notes": "Not scheduled every year; check eCalendar"},
          {"subject": "AGEC", "catalog": "332", "title": "Farm Management and Finance",           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Farm business management and financial analysis; take in U2 Fall"},
          {"subject": "AGEC", "catalog": "333", "title": "Resource Economics",                    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Resource and environmental economics; take in U2 Fall"},
          {"subject": "AGEC", "catalog": "425", "title": "Applied Econometrics",                  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Econometrics applied to agriculture and environment; prereq AEMA 310, AGEC 200, 201"},
          {"subject": "AGEC", "catalog": "430", "title": "Agriculture, Food and Resource Policy", "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "North American and international agricultural policy; take in U3 Winter"},
          {"subject": "AGEC", "catalog": "442", "title": "Economics of International Agricultural Development", "credits": 3, "is_required": True,  "recommended": False},
          # --- Environment & accounting ---
          {"subject": "ENVB", "catalog": "210", "title": "The Biophysical Environment",           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required environmental science foundation; take in U1 Fall"},
          {"subject": "MGCR", "catalog": "211", "title": "Introduction to Financial Accounting",  "credits": 3, "is_required": True,  "recommended": False},
        ],
      },
      {
        "block_key":      "agec_complementary",
        "title":          "Complementary Courses (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "With approval of the Academic Adviser, one introductory course in each of: "
          "(1) Statistics (e.g., AEMA 310), and (2) Written/Oral Communication (e.g., AEHM 205). "
          "These may overlap with other program requirements."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "AEMA", "catalog": "310", "title": "Statistical Methods 1",    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Strongly recommended statistics complement; also prerequisite for AGEC 425"},
          {"subject": "AEHM", "catalog": "205", "title": "Science Literacy",         "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Written/oral communication requirement; take in U1"},
        ],
      },
      {
        "block_key":      "agec_specialization",
        "title":          "Required Specialization (24 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 24,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "MUST choose ONE of the two following specializations: "
          "Agribusiness (24 cr) or Environmental Economics (24 cr). "
          "Agribusiness students may additionally take the Professional Agrology for "
          "Agribusiness Specialization (required for OAQ membership)."
        ),
        "sort_order": 3,
        "courses": [],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  LIFE SCIENCES (BIOLOGICAL AND AGRICULTURAL) MAJOR – B.Sc.(Ag.Env.Sc.)
  #  (42 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "lifesci_bsc_agenvsc",
    "name":          "Life Sciences (Biological and Agricultural) Major (B.Sc.(Ag.Env.Sc.)) (42 credits)",
    "program_type":  "major",
    "faculty":       "Faculty of Agricultural and Environmental Sciences",
    "total_credits": 42,
    "description": (
      "The Life Sciences (Biological and Agricultural) Major provides a strong foundation "
      "in the basic biological sciences. It prepares graduates for careers in the "
      "agricultural, environmental, health, and biotechnological fields. Graduates with "
      "high academic achievement may pursue postgraduate studies in research, or "
      "professional programs in biological, veterinary, medical, and health sciences. "
      "The major must be paired with at least one Specialization (18–24 cr); recommended "
      "pairings include Animal Biology, Animal Health and Disease, Microbiology and "
      "Molecular Biotechnology, or Plant Biology."
    ),
    "ecalendar_url": (
      "https://coursecatalogue.mcgill.ca/en/undergraduate/agri-env-sci/programs/"
      "natural-resource-sciences/life-sciences-biological-agricultural-major-bsc-agenvsc/"
    ),
    "blocks": [
      {
        "block_key":      "lifesci_required",
        "title":          "Required Courses (33 credits)",
        "block_type":     "required",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "11 courses are required. LSCI 211 has a corequisite of FDSC 230. "
          "LSCI 202 requires FDSC 230 and LSCI 211 (or equivalent). "
          "ANSC 400 requires LSCI 204 as a prerequisite."
        ),
        "sort_order": 1,
        "courses": [
          # --- Foundation biology & evolution ---
          {"subject": "AEBI", "catalog": "210", "title": "Organisms 1",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core U1 course – start here in Fall"},
          {"subject": "AEBI", "catalog": "211", "title": "Organisms 2",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core U1 course – take in Winter alongside AEBI 210"},
          {"subject": "AEBI", "catalog": "212", "title": "Evolution and Phylogeny",   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core evolution and tree-of-life course; take in U1"},
          # --- Communications & stats ---
          {"subject": "AEHM", "catalog": "205", "title": "Science Literacy",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required communication course; take in U1"},
          {"subject": "AEMA", "catalog": "310", "title": "Statistical Methods 1",     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Required statistics; take in U1 Fall or Winter"},
          # --- Molecular & cell biology ---
          {"subject": "LSCI", "catalog": "204", "title": "Genetics",                  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core genetics – prerequisite for ANSC 400 and upper-level courses; take in U1"},
          {"subject": "LSCI", "catalog": "211", "title": "Biochemistry 1",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core biochemistry; corequisite FDSC 230; take in U1"},
          {"subject": "LSCI", "catalog": "202", "title": "Molecular Cell Biology",    "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Cell biology; prereqs FDSC 230 and LSCI 211; take in U2"},
          {"subject": "LSCI", "catalog": "230", "title": "Introductory Microbiology", "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Core microbiology; take in U1 or U2"},
          # --- Advanced cell biology ---
          {"subject": "ANSC", "catalog": "400", "title": "Eukaryotic Cells and Viruses","credits": 3, "is_required": True, "recommended": True,  "recommendation_reason": "Advanced eukaryotic cell biology and virology; prereq LSCI 204; take in U3"},
          # --- Science corequisite (not always listed explicitly as 'required' but mandatory) ---
          {"subject": "FDSC", "catalog": "230", "title": "Introductory Organic Chemistry","credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Corequisite for LSCI 211; take in U1 Fall"},
        ],
      },
      {
        "block_key":      "lifesci_complementary",
        "title":          "Complementary Courses (9 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "Select 9 credits from the approved complementary list. "
          "Choices should reflect the student's chosen specialization and career goals."
        ),
        "sort_order": 2,
        "courses": [
          {"subject": "BTEC", "catalog": "306",  "title": "Experiments in Biotechnology",           "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Biotechnology lab methods; prereq LSCI 204"},
          {"subject": "ENVB", "catalog": "210",  "title": "The Biophysical Environment",            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Ecology foundation course; recommended if interested in environmental biology"},
          {"subject": "ENVB", "catalog": "222",  "title": "St. Lawrence Ecosystems",               "credits": 3, "is_required": False, "recommended": False},
          {"subject": "LSCI", "catalog": "451",  "title": "Research Project 1",                    "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Optional research project; great preparation for graduate school or Honours"},
          {"subject": "LSCI", "catalog": "452",  "title": "Research Project 2",                    "credits": 3, "is_required": False, "recommended": False},
          {"subject": "MICR", "catalog": "331",  "title": "Microbial Ecology",                     "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Covers microbial communities in soil, water, and organisms; prereq LSCI 230"},
          {"subject": "MICR", "catalog": "338",  "title": "Bacterial Molecular Genetics",          "credits": 3, "is_required": False, "recommended": False, "notes": "Even-numbered Falls only; prereq LSCI 211, 230, 204"},
          {"subject": "MICR", "catalog": "341",  "title": "Mechanisms of Pathogenicity",           "credits": 3, "is_required": False, "recommended": False, "notes": "Odd-numbered Falls only"},
          {"subject": "NRSC", "catalog": "333",  "title": "Pollution and Bioremediation",          "credits": 3, "is_required": False, "recommended": False},
          {"subject": "PLNT", "catalog": "304",  "title": "Biology of Fungi",                      "credits": 3, "is_required": False, "recommended": False},
          {"subject": "PLNT", "catalog": "353",  "title": "Plant Structure and Function",          "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Required if choosing Plant Biology specialization"},
          {"subject": "PLNT", "catalog": "426",  "title": "Plant Ecophysiology",                   "credits": 3, "is_required": False, "recommended": False, "notes": "Prereq LSCI 204 and LSCI 211"},
        ],
      },
      {
        "block_key":      "lifesci_specialization",
        "title":          "Specialization (18–24 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 18,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "At least one Specialization is required. At least 18 credits within the chosen "
          "specialization must be unique (not overlapping with the major or a second "
          "specialization). Recommended pairings: Animal Biology, Animal Health and Disease, "
          "Microbiology and Molecular Biotechnology, or Plant Biology."
        ),
        "sort_order": 3,
        "courses": [],
      },
    ],
  },

  # ══════════════════════════════════════════════════════════════════════
  #  BIORESOURCE ENGINEERING MAJOR – B.Eng.(Bioresource)  (113 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "bree_beng",
    "name":          "Bioresource Engineering Major (B.Eng.(Bioresource)) (113 credits)",
    "program_type":  "beng",
    "faculty":       "Faculty of Agricultural and Environmental Sciences",
    "total_credits": 113,
    "description": (
      "The Bioresource Engineering Major focuses on biological, agricultural, food, and "
      "environmental areas, applying professional engineering skills to biological systems. "
      "Covers the design and implementation of technology for bio-based products including "
      "food, fibre, fuel, and biomaterials, while sustaining a healthful environment. "
      "Graduates are eligible for registration as professional engineers in any Canadian "
      "province. Total of 143 credits including 30 Foundation Year (U0) credits. "
      "Students choose between two streams: Bio-Production Engineering or Bio-Process "
      "Engineering. All BREE program courses require a minimum grade of C."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/macdonald/undergraduate/programs/"
      "bachelor-engineering-bioresource-bengbioresource-major-bioresource-engineering"
    ),
    "blocks": [
      {
        "block_key":      "bree_required_core",
        "title":          "Required Core Courses (62.5 credits)",
        "block_type":     "required",
        "credits_needed": 62.5,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "All 25 courses are required. Note: BREE 451/452/453/485 are 1-credit seminars; "
          "FACC 250 is a 0.5-credit course. "
          "BREE 490 requires CHEE 315 or MECH 346, and BREE 415 as prerequisites. "
          "Note that a B+ must be obtained in BREE 252 to register in BREE 504. "
          "BREE 205 and BREE 216 are restricted to students enrolled in a Bioresource "
          "Engineering program. FACC 300 is a prerequisite for BREE 420."
        ),
        "sort_order": 1,
        "courses": [
          # --- Mathematics ---
          {"subject": "AEMA", "catalog": "202", "title": "Intermediate Calculus",           "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Multivariable calculus; prerequisite for BREE 305. Prereq: BREE 103 and AEMA 102"},
          {"subject": "AEMA", "catalog": "305", "title": "Differential Equations",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "ODE/PDE for engineering; prereq AEMA 202; take in U2"},
          {"subject": "BREE", "catalog": "319", "title": "Engineering Mathematics",         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Advanced engineering math (Fourier, boundary value); prereqs AEMA 305 and BREE 252"},
          # --- Engineering design & professionalism ---
          {"subject": "BREE", "catalog": "205", "title": "Engineering Design 1",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Introduction to engineering design, ethics, and law; take in U1 Fall"},
          {"subject": "BREE", "catalog": "490", "title": "Engineering Design 2",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Design project proposal; prereqs CHEE 315 or MECH 346, BREE 415; take in U3"},
          {"subject": "BREE", "catalog": "495", "title": "Engineering Design 3",            "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Final capstone design; take in U3 with BREE 490"},
          # --- Professional engineering (FACC) ---
          {"subject": "FACC", "catalog": "250", "title": "Responsibilities of the Professional Engineer", "credits": 0.5, "is_required": True,  "recommended": True,  "recommendation_reason": "Required professional ethics course; take in U1"},
          {"subject": "FACC", "catalog": "300", "title": "Engineering Economy",             "credits": 3,   "is_required": True,  "recommended": True,  "recommendation_reason": "Engineering economics and cost analysis; prerequisite for BREE 420"},
          {"subject": "FACC", "catalog": "400", "title": "Engineering Professional Practice","credits": 1,   "is_required": True,  "recommended": True,  "recommendation_reason": "Professional practice and law; take in U3"},
          # --- Core engineering sciences ---
          {"subject": "BREE", "catalog": "210", "title": "Mechanical Analysis and Design",  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Non-concurrent force systems, trusses, beams; take in U1 Fall"},
          {"subject": "BREE", "catalog": "216", "title": "Bioresource Engineering Materials","credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Materials science for biological systems; take in U1 Fall"},
          {"subject": "BREE", "catalog": "252", "title": "Computing for Engineers",         "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Programming for engineering problem solving; take in U1 Fall. Need B+ to access BREE 504"},
          {"subject": "BREE", "catalog": "301", "title": "Biothermodynamics",               "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Thermodynamics for biological systems; restricted to BREE students; take in U2 Winter"},
          {"subject": "BREE", "catalog": "305", "title": "Fluid Mechanics",                 "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Fluid properties and flow; prereqs BREE 210, AEMA 202; take in U2 Fall"},
          {"subject": "BREE", "catalog": "312", "title": "Electric Circuits and Machines",  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "DC/AC circuits and motors; prereq AEMA 305; take in U2 Fall"},
          {"subject": "BREE", "catalog": "341", "title": "Mechanics of Materials",          "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Stress, strain, beam deflections; prereq BREE 210; take in U2 Winter"},
          {"subject": "MECH", "catalog": "289", "title": "Design Graphics",                 "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Engineering drawing and CAD; take in U1 or U2"},
          {"subject": "BREE", "catalog": "415", "title": "Design of Machines and Structural Elements","credits": 3, "is_required": True, "recommended": True, "recommendation_reason": "Machine element design and FEM; prereqs BREE 210, 216, 341; take in U3 Fall"},
          {"subject": "BREE", "catalog": "420", "title": "Engineering for Sustainability",  "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Sustainability principles in engineering; prereq FACC 300; take in U3 Winter"},
          # --- Environment & biological systems ---
          {"subject": "BREE", "catalog": "327", "title": "Bio-Environmental Engineering",   "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Human impact on ecosystems; biofuels, bioprocessing, waste management; U2 students and above"},
          {"subject": "BREE", "catalog": "504", "title": "Instrumentation and Control",     "credits": 3, "is_required": True,  "recommended": True,  "recommendation_reason": "Sensors, data acquisition, and control systems; prereq B+ in BREE 252"},
          # --- Seminars (1 credit each) ---
          {"subject": "BREE", "catalog": "451", "title": "Undergraduate Seminar 1 – Oral Presentation", "credits": 1, "is_required": True,  "recommended": True,  "recommendation_reason": "Seminar series; oral presentation; take in U2"},
          {"subject": "BREE", "catalog": "452", "title": "Undergraduate Seminar 2 – Poster Presentation","credits": 1, "is_required": True,  "recommended": False, "notes": "Prereq: BREE 451"},
          {"subject": "BREE", "catalog": "453", "title": "Undergraduate Seminar 3 – Scientific Writing", "credits": 1, "is_required": True,  "recommended": False, "notes": "Prereq: BREE 452"},
          {"subject": "BREE", "catalog": "485", "title": "Senior Undergraduate Seminar",   "credits": 1, "is_required": True,  "recommended": False, "notes": "Prereq: BREE 453"},
        ],
      },
      {
        "block_key":      "bree_stream_specific",
        "title":          "Stream-Specific Technical Courses (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "6 credits chosen in consultation with the Academic Adviser, based on chosen "
          "stream. Bio-Production Engineering stream: BREE 412 (Machinery Systems), "
          "BREE 434 (Precision Agriculture), etc. "
          "Bio-Process Engineering stream: BREE 325 (Food Engineering), BREE 335 "
          "(Properties of Bio-Materials), etc. "
          "Note: ENVR courses have limited enrolment."
        ),
        "sort_order": 2,
        "courses": [
          # --- Bio-Production stream options ---
          {"subject": "BREE", "catalog": "412", "title": "Machinery Systems Engineering",     "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Bio-Production stream: tillage, harvesting, and crop processing machinery design"},
          {"subject": "BREE", "catalog": "434", "title": "Precision Agriculture",             "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Bio-Production stream: GIS, sensors, and information management for agriculture"},
          {"subject": "BREE", "catalog": "217", "title": "Hydrology and Water Resources",     "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Water resource engineering; shared across both streams"},
          # --- Bio-Process stream options ---
          {"subject": "BREE", "catalog": "325", "title": "Food Engineering",                  "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Bio-Process stream: food processing, heat/mass transfer; core for food engineering focus"},
          {"subject": "BREE", "catalog": "518", "title": "Ecological Engineering",            "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Constructed wetlands, green infrastructure, ecosystem restoration"},
          {"subject": "BREE", "catalog": "497", "title": "Bioresource Engineering Project",   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Independent design/experimental project; prereqs BREE 205 and BREE 327"},
        ],
      },
      {
        "block_key":      "bree_social_sciences",
        "title":          "Social Sciences / Humanities / Management / Law (6 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "6 credits of Social Sciences, Management Studies, Humanities, or Law courses "
          "at the U1 undergraduate level or higher, with approval of the Academic Adviser."
        ),
        "sort_order": 3,
        "courses": [
          {"subject": "AGEC", "catalog": "200", "title": "Principles of Microeconomics",   "credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Commonly chosen economics complement for engineering students"},
          {"subject": "AGEC", "catalog": "231", "title": "Economic Systems of Agriculture","credits": 3, "is_required": False, "recommended": True,  "recommendation_reason": "Agriculture-food system economics – relevant for BREE graduates"},
          {"subject": "MGCR", "catalog": "211", "title": "Introduction to Financial Accounting","credits": 3, "is_required": False, "recommended": False},
        ],
      },
      {
        "block_key":      "bree_electives",
        "title":          "Electives",
        "block_type":     "choose_credits",
        "credits_needed": 0,
        "courses_needed": None,
        "group_name":     None,
        "notes":          (
          "Remaining credits to meet the 113-credit total (143 credits including 30 "
          "Foundation Year credits). Minor programs that can be completed with minimal "
          "extra time include Environmental Engineering, Computer Science, Construction "
          "Engineering and Management, Biotechnology, and Technological Entrepreneurship."
        ),
        "sort_order": 4,
        "courses": [],
      },
    ],
  },

]


# ═══════════════════════════════════════════════════════════════════════════════
#  Seed helper – same upsert pattern as all other seed files
# ═══════════════════════════════════════════════════════════════════════════════

def _upsert_program(supabase, prog: dict) -> dict:
    """Insert or update one program record, returning its DB id."""
    key = prog["program_key"]

    existing = (
        supabase.table("degree_programs")
        .select("id")
        .eq("program_key", key)
        .limit(1)
        .execute()
    )

    payload = {
        "program_key":  key,
        "name":         prog["name"],
        "program_type": prog["program_type"],
        "faculty":      prog["faculty"],
        "total_credits": prog["total_credits"],
        "description":  prog.get("description", ""),
        "ecalendar_url": prog.get("ecalendar_url", ""),
    }

    if existing.data:
        prog_id = existing.data[0]["id"]
        supabase.table("degree_programs").update(payload).eq("id", prog_id).execute()
        logger.info(f"Updated program: {key}")
    else:
        result = supabase.table("degree_programs").insert(payload).execute()
        prog_id = result.data[0]["id"]
        logger.info(f"Inserted program: {key}")

    return prog_id


def _upsert_block(supabase, prog_id: str, block: dict, sort_order: int) -> str:
    """Insert or update one requirement block, returning its DB id."""
    key = block["block_key"]

    existing = (
        supabase.table("requirement_blocks")
        .select("id")
        .eq("block_key", key)
        .limit(1)
        .execute()
    )

    payload = {
        "program_id":     prog_id,
        "block_key":      key,
        "title":          block["title"],
        "block_type":     block["block_type"],
        "credits_needed": block.get("credits_needed"),
        "courses_needed": block.get("courses_needed"),
        "group_name":     block.get("group_name"),
        "notes":          block.get("notes", ""),
        "sort_order":     sort_order,
    }

    if existing.data:
        block_id = existing.data[0]["id"]
        supabase.table("requirement_blocks").update(payload).eq("id", block_id).execute()
    else:
        result = supabase.table("requirement_blocks").insert(payload).execute()
        block_id = result.data[0]["id"]

    return block_id


def _upsert_courses(supabase, block_id: str, courses: list[dict]) -> None:
    """Delete existing courses for a block and re-insert fresh."""
    supabase.table("requirement_courses").delete().eq("block_id", block_id).execute()

    for i, c in enumerate(courses):
        supabase.table("requirement_courses").insert({
            "block_id":              block_id,
            "subject":               c["subject"],
            "catalog":               c["catalog"],
            "title":                 c.get("title", ""),
            "credits":               c.get("credits", 3),
            "is_required":           c.get("is_required", False),
            "recommended":           c.get("recommended", False),
            "recommendation_reason": c.get("recommendation_reason", ""),
            "choose_from_group":     c.get("choose_from_group", None),
            "choose_n_credits":      c.get("choose_n_credits", None),
            "notes":                 c.get("notes", ""),
            "sort_order":            i,
        }).execute()


def seed_degree_requirements(supabase) -> dict:
    """Seed all AES degree programs into the database."""
    stats = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in AES_PROGRAMS:
        try:
            prog_id = _upsert_program(supabase, prog)
            stats["programs"] += 1

            for i, block in enumerate(prog.get("blocks", [])):
                try:
                    block_id = _upsert_block(supabase, prog_id, block, i)
                    stats["blocks"] += 1

                    courses = block.get("courses", [])
                    _upsert_courses(supabase, block_id, courses)
                    stats["courses"] += len(courses)

                except Exception as e:
                    msg = f"Block error [{prog['program_key']} / {block.get('block_key')}]: {e}"
                    logger.error(msg)
                    stats["errors"].append(msg)

        except Exception as e:
            msg = f"Program error [{prog.get('program_key')}]: {e}"
            logger.error(msg)
            stats["errors"].append(msg)

    logger.info(f"AES seed complete: {stats}")
    return stats


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    stats = seed_degree_requirements(supabase)
    print(f"Seeded: {stats['programs']} programs, {stats['blocks']} blocks, {stats['courses']} courses")
    if stats.get("errors"):
        print(f"Errors: {stats['errors']}")
