"""
McGill Faculty of Medicine and Health Sciences – Degree Requirements Seed Data
Source: McGill eCalendar 2024-2025 & Course Catalogue
https://coursecatalogue.mcgill.ca/en/undergraduate/medicine-health-sciences/
https://www.mcgill.ca/study/2024-2025/faculties/medicine/

Programs covered:
  1. Doctor of Medicine & Master of Surgery (M.D.,C.M.) – 200-204 credits
  2. Medicine Preparatory Program (Med-P, B.Sc.) – 30 credits

Accuracy notes:
  - MDCM curriculum undergoes annual review; the eCalendar carries a standing
    disclaimer that details are subject to change.
  - The MDCM is a 4-year program structured into 4 components:
      * Physicianship — longitudinal across all 4 years
      * Fundamentals of Medicine and Dentistry (FMD) — Year 1 & first half of Year 2
      * Transition to Clinical Practice (TCP) — second half of Year 2
      * Clerkship — Years 3 & 4
  - Most MDCM courses use the "INDS" (Interdisciplinary Studies) prefix and are
    shared between Medicine (MDCM) and Dentistry (DMD) students in Years 1-2.
  - INDS 125/225/323/423/424 are integrated assessment courses (0 credits each).
  - Elective credits (ELEC 400=4cr, ELEC 401-403=3cr each, ELEC 404=3cr optional).
  - Med-P is a 1-year qualifying year registered in the Faculty of Science.
    Students must achieve CGPA >= 3.5 with all required-course grades >= B.
  - CPR/AED (Level C+) certification is required and must remain current.
  - MCAT score and CASPer test are required for MDCM admission.
"""

import logging
logger = logging.getLogger(__name__)

MEDICINE_PROGRAMS = [

  # ============================================================================
  #  DOCTOR OF MEDICINE & MASTER OF SURGERY (M.D.,C.M.) - 200-204 CREDITS
  # ============================================================================
  {
    "program_key":   "mdcm_medicine",
    "name":          "Doctor of Medicine & Master of Surgery (M.D.,C.M.) - 200-204 credits",
    "program_type":  "major",
    "faculty":       "Faculty of Medicine and Health Sciences",
    "total_credits": 200,
    "ecalendar_url": (
        "https://www.mcgill.ca/study/2024-2025/faculties/medicine/undergraduate/programs/"
        "doctor-medicine-and-master-surgery-mdcm-medicine-200-204-credits"
    ),
    "description": (
        "The M.D.,C.M. is McGill's flagship four-year medical degree. The curriculum "
        "is organised into four components: Physicianship (longitudinal), Fundamentals "
        "of Medicine and Dentistry (FMD, Year 1 and first half of Year 2), Transition "
        "to Clinical Practice (TCP, second half of Year 2), and Clerkship (Years 3-4). "
        "Three overarching themes run throughout: Social Accountability; Professional "
        "Identity and Practice; and Basic Science, Critical Thinking & Knowledge "
        "Translation. Graduates may practice only in supervised postgraduate residency "
        "settings, not independently. Full details: mcgill.ca/ugme"
    ),
    "blocks": [

      {
        "block_key":      "mdcm_fmd_year1_systems",
        "title":          "Fundamentals of Medicine and Dentistry - Systems Courses (Year 1)",
        "block_type":     "required",
        "credits_needed": 52,
        "notes": (
            "Year 1 FMD uses an integrated systems-based approach covering anatomy, "
            "physiology, pathology, and therapeutics simultaneously for each organ system. "
            "Teaching methods include lectures, laboratory sessions, small group teaching, "
            "and independent study. Open only to M.D.,C.M. and D.M.D. students. "
            "Integrated assessments (INDS 125J1/J2/J3) span all three terms; credit is "
            "awarded only if all three J-sections are completed consecutively."
        ),
        "courses": [
          {"subject": "INDS", "catalog": "111",   "title": "Molecules to Global Health",   "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "112",   "title": "Respiration",                  "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "113",   "title": "Circulation",                  "credits": 8, "is_required": True},
          {"subject": "INDS", "catalog": "114",   "title": "Digestion and Metabolism",     "credits": 8, "is_required": True},
          {"subject": "INDS", "catalog": "115",   "title": "Renal",                        "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "116",   "title": "Defense",                      "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "117",   "title": "Infection",                    "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "118",   "title": "Movement",                     "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "125J1", "title": "FMD Integrated Assessment 1",  "credits": 0, "is_required": True},
          {"subject": "INDS", "catalog": "125J2", "title": "FMD Integrated Assessment 1",  "credits": 0, "is_required": True},
          {"subject": "INDS", "catalog": "125J3", "title": "FMD Integrated Assessment 1",  "credits": 0, "is_required": True},
        ],
      },

      {
        "block_key":      "mdcm_fmd_year1_longitudinal",
        "title":          "Fundamentals of Medicine and Dentistry - Longitudinal Courses (Year 1)",
        "block_type":     "required",
        "credits_needed": 11,   # 3 (CM1) + ~2 (PA1) + 3 (RF1) + 3 (LFME) = ~11 credits
        "notes": (
            "INDS 119 (Clinical Method 1) and INDS 122 (Physician Apprenticeship 1) run "
            "across all three terms of Year 1 as J-section courses; no credit is awarded "
            "unless all three J-sections are completed consecutively. INDS 123 (Research "
            "Fundamentals 1) focuses on formulating a research proposal. INDS 124 "
            "(Longitudinal Family Medicine Experience) pairs each MDCM student with a "
            "family physician preceptor from the first month of medical school for early "
            "clinical exposure."
        ),
        "courses": [
          # Clinical Method 1 (J1+J2+J3 = 3 credits)
          {"subject": "INDS", "catalog": "119J1", "title": "Clinical Method 1",           "credits": 1,    "is_required": True},
          {"subject": "INDS", "catalog": "119J2", "title": "Clinical Method 1",           "credits": 1,    "is_required": True},
          {"subject": "INDS", "catalog": "119J3", "title": "Clinical Method 1",           "credits": 1,    "is_required": True},
          # Physician Apprenticeship 1 (J1+J2+J3 = 2.01 credits ≈ 2 credits)
          {"subject": "INDS", "catalog": "122J1", "title": "Physician Apprenticeship 1",  "credits": 0.67, "is_required": True},
          {"subject": "INDS", "catalog": "122J2", "title": "Physician Apprenticeship 1",  "credits": 0.67, "is_required": True},
          {"subject": "INDS", "catalog": "122J3", "title": "Physician Apprenticeship 1",  "credits": 0.67, "is_required": True},
          # Research Fundamentals 1 (J1+J2+J3 = 3 credits)
          {"subject": "INDS", "catalog": "123J1", "title": "Research Fundamentals 1",     "credits": 1,    "is_required": True},
          {"subject": "INDS", "catalog": "123J2", "title": "Research Fundamentals 1",     "credits": 1,    "is_required": True},
          {"subject": "INDS", "catalog": "123J3", "title": "Research Fundamentals 1",     "credits": 1,    "is_required": True},
          # Longitudinal Family Medicine Experience (J1+J2+J3 = 3 credits)
          {"subject": "INDS", "catalog": "124J1", "title": "Longitudinal Family Medicine Experience", "credits": 1, "is_required": True},
          {"subject": "INDS", "catalog": "124J2", "title": "Longitudinal Family Medicine Experience", "credits": 1, "is_required": True},
          {"subject": "INDS", "catalog": "124J3", "title": "Longitudinal Family Medicine Experience", "credits": 1, "is_required": True},
        ],
      },

      {
        "block_key":      "mdcm_fmd_year2",
        "title":          "Fundamentals of Medicine and Dentistry - Year 2 (First Half)",
        "block_type":     "required",
        "credits_needed": 21,
        "notes": (
            "The FMD component continues into the first half of Year 2 with two major "
            "systems blocks: Reproduction & Sexuality (6 cr) and Human Behaviour (12 cr, "
            "covering psychiatry and neuroscience). Research Fundamentals 2 (1.5 cr) and "
            "Physician Apprenticeship 2 (INDS 222J1/J2/J3, 1.5 cr total) are completed "
            "concurrently. INDS 225 is the FMD Integrated Assessment 2 (0 cr)."
        ),
        "courses": [
          {"subject": "INDS", "catalog": "211",   "title": "Reproduction and Sexuality",   "credits": 6,   "is_required": True},
          {"subject": "INDS", "catalog": "212",   "title": "Human Behaviour",              "credits": 12,  "is_required": True},
          {"subject": "INDS", "catalog": "223",   "title": "Research Fundamentals 2",      "credits": 1.5, "is_required": True},
          # Physician Apprenticeship 2 (J1+J2+J3 = 1.5 credits)
          {"subject": "INDS", "catalog": "222J1", "title": "Physician Apprenticeship 2",   "credits": 0.5, "is_required": True},
          {"subject": "INDS", "catalog": "222J2", "title": "Physician Apprenticeship 2",   "credits": 0.5, "is_required": True},
          {"subject": "INDS", "catalog": "222J3", "title": "Physician Apprenticeship 2",   "credits": 0.5, "is_required": True},
          {"subject": "INDS", "catalog": "225",   "title": "FMD Integrated Assessment 2",  "credits": 0,   "is_required": True},
        ],
      },

      {
        "block_key":      "mdcm_physicianship",
        "title":          "Physicianship - Longitudinal (Years 3-4)",
        "block_type":     "required",
        "credits_needed": 2,
        "notes": (
            "Physicianship continues longitudinally into clerkship years. Physician "
            "Apprenticeship 3 (INDS 322J1/J2/J3, 1.5 cr) runs throughout Year 3 "
            "Clerkship. Physician Apprenticeship 4 (INDS 422D1/D2, 0.5 cr) is the "
            "final consolidating course in Year 4. IPEA 500 (Roles in Interprofessional "
            "Teams, 0 cr) is also required. Students are assigned in groups of 6-7 to "
            "an Osler Fellow mentor throughout the program."
        ),
        "courses": [
          # Physician Apprenticeship 3 — Year 3 (J1+J2+J3 = 1.5 credits)
          {"subject": "INDS", "catalog": "322J1", "title": "Physician Apprenticeship 3", "credits": 0.5,  "is_required": True},
          {"subject": "INDS", "catalog": "322J2", "title": "Physician Apprenticeship 3", "credits": 0.5,  "is_required": True},
          {"subject": "INDS", "catalog": "322J3", "title": "Physician Apprenticeship 3", "credits": 0.5,  "is_required": True},
          # Physician Apprenticeship 4 — Year 4 (D1+D2 = 0.5 credits)
          {"subject": "INDS", "catalog": "422D1", "title": "Physician Apprenticeship 4", "credits": 0.25, "is_required": True},
          {"subject": "INDS", "catalog": "422D2", "title": "Physician Apprenticeship 4", "credits": 0.25, "is_required": True},
          # Interprofessional Education — 0 credits
          {"subject": "IPEA", "catalog": "500",   "title": "Roles in Interprofessional Teams", "credits": 0, "is_required": True},
        ],
      },

      {
        "block_key":      "mdcm_tcp",
        "title":          "Transition to Clinical Practice (TCP) - Year 2 (Second Half)",
        "block_type":     "required",
        "credits_needed": 31,   # ~31 credits (slight variation due to 0.67-credit CHAP courses)
        "notes": (
            "TCP bridges classroom learning and active patient care. Students consolidate "
            "history-taking, physical examination, and clinical reasoning through clinical "
            "apprentice sessions across Internal Medicine, Family Medicine, Anesthesia, "
            "Neurology, Pediatrics, Surgery, Radiology, and Ophthalmology. Also includes "
            "Clinical Method 2 (INDS 219), Community Health Alliance Project - C.H.A.P "
            "(INDS 224J1/J2/J3), Mindful Medical Practice (INDS 300), Medical Ethics and "
            "Health Law (INDS 302), Formation of the Professional and Healer (INDS 320J1/J2/J3), "
            "and Transition to Clerkship (INDS 305). Concludes with TCP Integrated Assessment "
            "(INDS 323, 0 cr)."
        ),
        "courses": [
          # Discipline rotations
          {"subject": "IMED", "catalog": "301",  "title": "TCP Internal Medicine",              "credits": 7,    "is_required": True},
          {"subject": "FMED", "catalog": "301",  "title": "TCP Family Medicine",                "credits": 3,    "is_required": True},
          {"subject": "ANAE", "catalog": "301",  "title": "TCP Anesthesia",                     "credits": 2,    "is_required": True},
          {"subject": "NEUR", "catalog": "301",  "title": "TCP Neurology",                      "credits": 2,    "is_required": True},
          {"subject": "PAED", "catalog": "301",  "title": "TCP Pediatrics",                     "credits": 2,    "is_required": True},
          {"subject": "SURG", "catalog": "301",  "title": "TCP Surgery",                        "credits": 4,    "is_required": True},
          {"subject": "RADD", "catalog": "301",  "title": "TCP Radiology",                      "credits": 1,    "is_required": True},
          {"subject": "OPTH", "catalog": "300",  "title": "TCP Ophthalmology",                  "credits": 1,    "is_required": True},
          # Longitudinal TCP courses
          {"subject": "INDS", "catalog": "219",   "title": "Clinical Method 2",                 "credits": 1.5,  "is_required": True},
          {"subject": "INDS", "catalog": "224J1", "title": "Community Health Alliance Project - C.H.A.P", "credits": 0.67, "is_required": True},
          {"subject": "INDS", "catalog": "224J2", "title": "Community Health Alliance Project - C.H.A.P", "credits": 0.67, "is_required": True},
          {"subject": "INDS", "catalog": "224J3", "title": "Community Health Alliance Project - C.H.A.P", "credits": 0.67, "is_required": True},
          {"subject": "INDS", "catalog": "300",   "title": "Mindful Medical Practice",          "credits": 1.5,  "is_required": True},
          {"subject": "INDS", "catalog": "302",   "title": "Medical Ethics and Health Law",     "credits": 1.5,  "is_required": True},
          {"subject": "INDS", "catalog": "305",   "title": "Transition to Clerkship",           "credits": 1,    "is_required": True},
          {"subject": "INDS", "catalog": "320J1", "title": "Formation of the Professional and Healer", "credits": 0.5, "is_required": True},
          {"subject": "INDS", "catalog": "320J2", "title": "Formation of the Professional and Healer", "credits": 0.5, "is_required": True},
          {"subject": "INDS", "catalog": "320J3", "title": "Formation of the Professional and Healer", "credits": 0.5, "is_required": True},
          # Assessment
          {"subject": "INDS", "catalog": "323",  "title": "TCP Integrated Assessment",          "credits": 0,    "is_required": True},
        ],
      },

      {
        "block_key":      "mdcm_clerkship_year3",
        "title":          "Clerkship - Year 3 (Core Rotations)",
        "block_type":     "required",
        "credits_needed": 48,
        "notes": (
            "Year 3 Clerkship places students in active patient care under supervision "
            "across all core disciplines. Rotation sequence varies by student stream. "
            "Sites include the MUHC Glen Campus, Montreal General Hospital, Jewish General "
            "Hospital, Montreal Children's Hospital, and affiliated community hospitals. "
            "INDS 423 is Clerkship Integrated Assessment 1 (progress test + OSCE, 0 cr). "
            "ELEC 400 is a 4-credit (4-week) clinical/research elective taken in Year 3."
        ),
        "courses": [
          {"subject": "INDS", "catalog": "423",  "title": "Clerkship Integrated Assessment 1", "credits": 0, "is_required": True},
          {"subject": "IMED", "catalog": "401",  "title": "Internal Medicine Clerkship",        "credits": 8, "is_required": True},
          {"subject": "SURG", "catalog": "402",  "title": "Surgery Clerkship",                  "credits": 8, "is_required": True},
          {"subject": "FMED", "catalog": "405",  "title": "Family Medicine Clerkship",          "credits": 8, "is_required": True},
          {"subject": "PSYT", "catalog": "401",  "title": "Psychiatry Clerkship",               "credits": 8, "is_required": True},
          {"subject": "PAED", "catalog": "401",  "title": "Pediatrics Clerkship",               "credits": 6, "is_required": True},
          {"subject": "OBGY", "catalog": "401",  "title": "Obstetrics and Gynecology Clerkship","credits": 6, "is_required": True},
          {"subject": "ELEC", "catalog": "400",  "title": "Elective 1 Clerkship",               "credits": 4, "is_required": True},
        ],
      },

      {
        "block_key":      "mdcm_clerkship_year4",
        "title":          "Clerkship - Year 4 (Senior Rotations & Electives)",
        "block_type":     "required",
        "credits_needed": 32,
        "notes": (
            "Year 4 includes senior rotations in Geriatric Medicine (IMED 407, 4 cr), "
            "Emergency Medicine (INDS 408, 4 cr), Public Health & Preventive Medicine "
            "(INDS 427, 1 cr), Putting It All Together (INDS 426, 6 cr), and Transition "
            "to Residency (INDS 421, 8 cr). Three additional electives (ELEC 401/402/403, "
            "3 cr each) provide time for CaRMS preparation. ELEC 404 (Elective 5, 3 cr) "
            "is optional and brings the degree total to a maximum of 204 credits. "
            "INDS 424 is Clerkship Integrated Assessment 2 (0 cr)."
        ),
        "courses": [
          {"subject": "INDS", "catalog": "424",  "title": "Clerkship Integrated Assessment 2",              "credits": 0, "is_required": True},
          {"subject": "IMED", "catalog": "407",  "title": "Geriatric Medicine Clerkship",                   "credits": 4, "is_required": True},
          {"subject": "INDS", "catalog": "408",  "title": "Emergency Medicine Clerkship",                   "credits": 4, "is_required": True},
          {"subject": "INDS", "catalog": "427",  "title": "Public Health and Preventive Medicine Clerkship","credits": 1, "is_required": True},
          {"subject": "INDS", "catalog": "426",  "title": "Putting It All Together: Basic Science, Medicine and Society", "credits": 6, "is_required": True},
          {"subject": "INDS", "catalog": "421",  "title": "Transition to Residency",                        "credits": 8, "is_required": True},
          {"subject": "ELEC", "catalog": "401",  "title": "Elective 2 Clerkship",                           "credits": 3, "is_required": True},
          {"subject": "ELEC", "catalog": "402",  "title": "Elective 3 Clerkship",                           "credits": 3, "is_required": True},
          {"subject": "ELEC", "catalog": "403",  "title": "Elective 4 Clerkship",                           "credits": 3, "is_required": True},
          {"subject": "ELEC", "catalog": "404",  "title": "Elective 5 Clerkship (optional)",                "credits": 3, "is_required": False},
        ],
      },

    ],
  },

  # ============================================================================
  #  MEDICINE PREPARATORY PROGRAM (Med-P) - B.Sc. 30 CREDITS
  # ============================================================================
  {
    "program_key":   "medp_medicine",
    "name":          "Medicine Preparatory Program (Med-P) - B.Sc. (30 credits)",
    "program_type":  "diploma",
    "faculty":       "Faculty of Medicine and Health Sciences",
    "total_credits": 30,
    "ecalendar_url": (
        "https://www.mcgill.ca/study/2024-2025/faculties/medicine/undergraduate/programs/"
        "bachelor-science-bsc-medicine-preparatory-program-med-p-program"
    ),
    "description": (
        "The Med-P is a one-year qualifying program for immediate graduates of the Quebec "
        "Collegial (CEGEP) system who have been conditionally admitted to the M.D.,C.M. "
        "program. Students are registered in the Faculty of Science and must complete "
        "30 credits. Promotion into Year 1 of the MDCM requires CGPA >= 3.5 with all "
        "required-course grades of 'B' or higher (passing grades suffice for complementary "
        "courses). Failing to meet requirements allows transfer into a B.Sc. with the "
        "right to reapply later. Also offered in French at Campus Outaouais (UQO). "
        "Full details: mcgill.ca/medadmissions/programs/med-p"
    ),
    "blocks": [

      {
        "block_key":      "medp_required_sciences",
        "title":          "Required Science Courses - Minimum Grade B",
        "block_type":     "required",
        "credits_needed": 15,
        "notes": (
            "All five courses require a minimum grade of B for promotion into the MDCM. "
            "BIOL 200 is a prerequisite for BIOL 201. PHGY 209 and PHGY 210 require prior "
            "CEGEP-level Biology, Chemistry, and Physics. At Campus Outaouais (UQO), "
            "francophone equivalents are offered by McGill Faculty of Science professors."
        ),
        "courses": [
          {"subject": "BIOL", "catalog": "200", "title": "Molecular Biology",          "credits": 3, "is_required": True},
          {"subject": "BIOL", "catalog": "201", "title": "Cell Biology and Metabolism", "credits": 3, "is_required": True},
          {"subject": "BIOL", "catalog": "202", "title": "Basic Genetics",              "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "209", "title": "Mammalian Physiology 1",      "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "210", "title": "Mammalian Physiology 2",      "credits": 3, "is_required": True},
        ],
      },

      {
        "block_key":      "medp_statistics",
        "title":          "Statistics Requirement",
        "block_type":     "required",
        "credits_needed": 3,
        "notes": (
            "MATH 203 is required for all Med-P students who did not complete an equivalent "
            "statistics course during CEGEP. Students with an approved CEGEP statistics "
            "equivalent are exempt and must replace it with an approved complementary "
            "science course. At Campus Outaouais, the equivalent UQO course satisfies "
            "this requirement."
        ),
        "courses": [
          {"subject": "MATH", "catalog": "203", "title": "Principles of Statistics 1", "credits": 3, "is_required": True},
        ],
      },

      {
        "block_key":      "medp_complementary_sciences",
        "title":          "Complementary Science Electives",
        "block_type":     "choose_credits",
        "credits_needed": 12,
        "notes": (
            "Students complete approved Faculty of Science courses to reach the 30-credit "
            "total. A passing grade suffices (no 'B' minimum). Common choices listed below; "
            "consult an academic advisor for the current approved list."
        ),
        "courses": [
          {"subject": "CHEM", "catalog": "212", "title": "Introductory Organic Chemistry 1",   "credits": 4, "is_required": False},
          {"subject": "CHEM", "catalog": "222", "title": "Introductory Organic Chemistry 2",   "credits": 4, "is_required": False},
          {"subject": "BIOL", "catalog": "300", "title": "Molecular Biology of the Gene",      "credits": 3, "is_required": False},
          {"subject": "BIOL", "catalog": "301", "title": "Cell and Molecular Laboratory",      "credits": 4, "is_required": False},
          {"subject": "PHGY", "catalog": "311", "title": "Channels, Synapses and Hormones",    "credits": 3, "is_required": False},
          {"subject": "PSYC", "catalog": "211", "title": "Introductory Behavioural Neuroscience", "credits": 3, "is_required": False},
        ],
      },

    ],
  },

]


# ============================================================================
#  HELPER FUNCTIONS  (mirrors dentistry_degree_requirements.py exactly)
# ============================================================================

def _upsert_program(supabase, prog: dict) -> str:
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
        "program_key":   key,
        "name":          prog["name"],
        "program_type":  prog["program_type"],
        "faculty":       prog["faculty"],
        "total_credits": prog["total_credits"],
        "description":   prog.get("description", ""),
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


def _upsert_courses(supabase, block_id: str, courses: list) -> None:
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
    """Seed all Medicine & Health Sciences programs into the database."""
    stats = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in MEDICINE_PROGRAMS:
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

    logger.info(f"Medicine seed complete: {stats}")
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
