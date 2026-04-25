"""
McGill School of Physical and Occupational Therapy (SPOT) – Degree Requirements Seed Data
Source: McGill eCalendar 2024-2025 & SPOT website
https://www.mcgill.ca/study/2024-2025/faculties/spot/
https://www.mcgill.ca/spot/programs/

This file covers the two undergraduate rehabilitation science programs:
  1. B.Sc.(Rehab.Sc.) – Major in Physical Therapy   (90 credits: 81 required + 6-9 complementary + 0-3 elective)
  2. B.Sc.(Rehab.Sc.) – Major in Occupational Therapy (90 credits: 75 required + 15 complementary)

Accuracy notes:
  - Both programs are 90-credit, 3-year programs (for CEGEP entrants).
  - Students must complete a total of 90 course credits, successfully complete ALL
    curriculum courses, maintain Satisfactory Standing, and hold a CGPA ≥ 2.3
    in OT/PT curriculum courses to graduate.
  - Both programs are FULL-TIME ONLY due to the sequential, clinical nature of coursework.
  - Graduates MUST continue to the professional master's (M.Sc.A.PT. or M.Sc.A.OT.)
    to be eligible for licensure. Entry to MScA requires a minimum CGPA of 3.0.
  - IPEA courses (500, 501) are interprofessional education activities worth
    0 credits, mandatory for graduation.
  - French B2 proficiency is required for clinical placements in Quebec institutions.
  - Intrafaculty transfers between PT and OT are not available once admitted.
  - POTH courses (prefix) are shared by both programs; PHTH = PT-specific; OCC1 = OT-specific.
  - POTH 204 (Statistics) is waived for students with a CEGEP stats course ≥75%;
    such students must take an additional 3-credit complementary course instead.
  - Complementary courses may be chosen from: Psychology (lifespan development recommended),
    Management (personnel/private practice), Academic Writing, Sociology/Anthropology,
    French/English second language (max 6 credits), Sports Medicine Practicum (3 credits,
    PT only: PHTH 301), or one personal interest course (max 3 credits).
  - Verified against eCalendar 2024-2025 (January 2026).

Course prefix key:
  POTH  Physical & Occupational Therapy (shared by both programs)
  PHTH  Physical Therapy (PT-specific courses)
  OCC1  Occupational Therapy (OT-specific courses)
  ANAT  Anatomy
  PHGY  Physiology
  IPEA  Interprofessional Education Activities (0-credit)
"""

import logging
logger = logging.getLogger(__name__)


SPOT_PROGRAMS = [

  # ════════════════════════════════════════════════════════════════════════
  #  B.Sc.(Rehab.Sc.) – MAJOR IN PHYSICAL THERAPY  (90 credits)
  # ════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "bsc_rehab_physical_therapy",
    "name":          "B.Sc. (Rehabilitation Science) – Major in Physical Therapy (90 credits)",
    "program_type":  "major",
    "faculty":       "School of Physical and Occupational Therapy",
    "total_credits": 90,
    "description": (
      "The B.Sc.(Rehab.Sc.) in Physical Therapy is a 3-year full-time program "
      "preparing students for entry to the professional M.Sc.A. in Physical Therapy. "
      "The program emphasizes the biological sciences underpinning rehabilitation, "
      "clinical reasoning, exercise science, and evidence-based practice. "
      "Students complete a core of anatomy, physiology, biomechanics, and statistics, "
      "followed by PT-specific coursework in assessment, therapeutic exercise, "
      "neurorehabilitation, and cardiorespiratory care, along with clinical practicum "
      "experiences. Graduates with CGPA ≥ 3.0 are eligible to apply for the M.Sc.A.PT. "
      "program that begins the summer after graduation. CGPA ≥ 2.3 in PT curriculum is "
      "required throughout. Full-time study only."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/spot/undergraduate/programs/"
      "bachelor-science-bsc-rehabilitation-science-major-physical-therapy"
    ),
    "blocks": [

      # ── Required Core Courses ─────────────────────────────────────────
      # Source: eCalendar 2024-2025, verified January 2026
      # 81 required credits total (plus 6-9 complementary, 0-3 elective = 90 cr)
      {
        "block_key":      "pt_required_core",
        "title":          "Required Core Courses (81 credits)",
        "block_type":     "required",
        "credits_needed": 81,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "All courses are required. For ANAT 321/323, students choose one but not both. "
          "IPEA 500 and 501 are 0-credit interprofessional activities (mandatory). "
          "Full-time study only."
        ),
        "courses": [
          {"subject": "ANAT", "catalog": "315",  "title": "Clinical Human Musculoskeletal Anatomy", "credits": 3, "is_required": True},
          {"subject": "ANAT", "catalog": "316",  "title": "Clinical Human Visceral Anatomy", "credits": 3, "is_required": True},
          {"subject": "ANAT", "catalog": "321",  "title": "Circuitry of the Human Brain", "credits": 3, "is_required": False,
           "notes": "Choose ANAT 321 or ANAT 323 (not both)."},
          {"subject": "ANAT", "catalog": "323",  "title": "Clinical Neuroanatomy", "credits": 3, "is_required": False,
           "notes": "Choose ANAT 321 or ANAT 323 (not both)."},
          {"subject": "IPEA", "catalog": "500",  "title": "Roles in Interprofessional Teams (0 credits)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "501",  "title": "Communication in Interprofessional Teams (0 credits)", "credits": 0, "is_required": True},
          {"subject": "PHGY", "catalog": "209",  "title": "Mammalian Physiology 1", "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "210",  "title": "Mammalian Physiology 2", "credits": 3, "is_required": True},
          {"subject": "PHTH", "catalog": "245",  "title": "Introduction to Professional Practice 1", "credits": 3, "is_required": True},
          {"subject": "PHTH", "catalog": "440",  "title": "Clinical Exercise Physiology", "credits": 3, "is_required": True},
          {"subject": "PHTH", "catalog": "450",  "title": "Introduction to PT Clinical Practice", "credits": 3, "is_required": True},
          {"subject": "PHTH", "catalog": "460",  "title": "Introduction to Functional Movement", "credits": 3, "is_required": True},
          {"subject": "PHTH", "catalog": "482",  "title": "Introduction to Health, Fitness and Lifestyle", "credits": 3, "is_required": True},
          {"subject": "PHTH", "catalog": "550",  "title": "Physical Therapy Orthopedic Management", "credits": 7, "is_required": True},
          {"subject": "PHTH", "catalog": "551",  "title": "Physical Therapy Neurological Rehabilitation", "credits": 4, "is_required": True},
          {"subject": "PHTH", "catalog": "554",  "title": "PT Cardiorespiratory Rehabilitation", "credits": 2, "is_required": True},
          {"subject": "PHTH", "catalog": "560",  "title": "Integrated Orthopedic Management", "credits": 6, "is_required": True},
          {"subject": "PHTH", "catalog": "561",  "title": "Integrated Neurological Rehabilitation", "credits": 5, "is_required": True},
          {"subject": "PHTH", "catalog": "564",  "title": "Integrated Cardiorespiratory Rehabilitation", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "204",  "title": "Introduction to Statistics for OT/PT", "credits": 3, "is_required": True,
           "notes": "Waived if CEGEP stats ≥75%; replace with an additional 3-credit complementary course."},
          {"subject": "POTH", "catalog": "225",  "title": "Introduction to Biomechanics in Rehabilitation Sciences", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "250",  "title": "Introduction to Professional Practice 2", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "305",  "title": "Statistics for Experimental Design OT/PT", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "401",  "title": "Research Methods", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "434",  "title": "Musculoskeletal Biomechanics", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "455",  "title": "Neurophysiology", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "563",  "title": "Foundations of Professional Practice", "credits": 3, "is_required": True},
        ],
      },

      # ── Complementary Courses ─────────────────────────────────────────
      {
        "block_key":      "pt_complementary",
        "title":          "Complementary Courses (6–9 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "6–9 complementary credits chosen from: Psychology (lifespan development recommended), "
          "Management (private practice), Academic Writing, Sociology/Anthropology, "
          "French/English second language (max 6 cr.), or PHTH 301 Sports Medicine Practicum (3 cr.). "
          "POTH 204 exemption replaces waived stats with an extra 3-credit complementary."
        ),
        "courses": [],
      },

      # ── Elective ──────────────────────────────────────────────────────
      {
        "block_key":      "pt_elective",
        "title":          "Elective Courses (0–3 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name":     None,
        "notes": "Maximum one 3-credit elective course.",
        "courses": [],
      },

    ],
  },

  # ════════════════════════════════════════════════════════════════════════
  #  B.Sc.(Rehab.Sc.) – MAJOR IN OCCUPATIONAL THERAPY  (90 credits)
  # ════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "bsc_rehab_occupational_therapy",
    "name":          "B.Sc. (Rehabilitation Science) – Major in Occupational Therapy (90 credits)",
    "program_type":  "major",
    "faculty":       "School of Physical and Occupational Therapy",
    "total_credits": 90,
    "description": (
      "The B.Sc.(Rehab.Sc.) in Occupational Therapy is a 3-year full-time program "
      "preparing students for entry to the professional M.Sc.A. in Occupational Therapy. "
      "The program emphasizes occupation-focused reasoning, human development across "
      "the lifespan, mental health, neurorehabilitation, and community practice. "
      "Students complete a core of anatomy, physiology, biomechanics, and statistics, "
      "followed by OT-specific coursework in professional practice, occupational "
      "performance frameworks, and practice in psychiatry, pediatrics, and geriatrics. "
      "Graduates with CGPA ≥ 3.0 are eligible to apply for the M.Sc.A.OT. program "
      "that begins the summer after graduation. CGPA ≥ 2.3 in OT curriculum required "
      "throughout. Full-time study only."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/spot/undergraduate/programs/"
      "bachelor-science-bsc-rehabilitation-science-major-occupational-therapy"
    ),
    "blocks": [

      # ── Required Core Courses ─────────────────────────────────────────
      # Source: eCalendar 2024-2025, verified January 2026
      # 75 required credits total (plus 15 complementary = 90 cr)
      {
        "block_key":      "ot_required_core",
        "title":          "Required Core Courses (75 credits)",
        "block_type":     "required",
        "credits_needed": 75,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "All courses are required. For ANAT 321/323, students choose one but not both. "
          "IPEA 500 and 501 are 0-credit interprofessional activities (mandatory). "
          "OCC1 500 is a D1/D2 split course taken over consecutive terms. "
          "Full-time study only."
        ),
        "courses": [
          {"subject": "ANAT", "catalog": "315",  "title": "Clinical Human Musculoskeletal Anatomy", "credits": 3, "is_required": True},
          {"subject": "ANAT", "catalog": "316",  "title": "Clinical Human Visceral Anatomy", "credits": 3, "is_required": True},
          {"subject": "ANAT", "catalog": "321",  "title": "Circuitry of the Human Brain", "credits": 3, "is_required": False,
           "notes": "Choose ANAT 321 or ANAT 323 (not both)."},
          {"subject": "ANAT", "catalog": "323",  "title": "Clinical Neuroanatomy", "credits": 3, "is_required": False,
           "notes": "Choose ANAT 321 or ANAT 323 (not both)."},
          {"subject": "IPEA", "catalog": "500",  "title": "Roles in Interprofessional Teams (0 credits)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "501",  "title": "Communication in Interprofessional Teams (0 credits)", "credits": 0, "is_required": True},
          {"subject": "OCC1", "catalog": "245",  "title": "Introduction to Professional Practice 1", "credits": 3, "is_required": True},
          {"subject": "OCC1", "catalog": "443",  "title": "Constructing Mental Health", "credits": 3, "is_required": True},
          {"subject": "OCC1", "catalog": "450",  "title": "Enabling Leisure Occupations", "credits": 3, "is_required": True},
          {"subject": "OCC1", "catalog": "500",  "title": "Pre-Clinical Practicum Seminar (D1/D2)", "credits": 3, "is_required": True,
           "notes": "OCC1 500D1 followed by OCC1 500D2 in consecutive terms."},
          {"subject": "OCC1", "catalog": "545",  "title": "Therapeutic Strategies in OT 1", "credits": 8, "is_required": True},
          {"subject": "OCC1", "catalog": "547",  "title": "Occupational Solutions 1", "credits": 6, "is_required": True},
          {"subject": "OCC1", "catalog": "548",  "title": "Holistic Approaches in OT", "credits": 3, "is_required": True},
          {"subject": "OCC1", "catalog": "549",  "title": "Therapeutic Strategies in OT 2", "credits": 4, "is_required": True},
          {"subject": "OCC1", "catalog": "550",  "title": "Enabling Human Occupation", "credits": 3, "is_required": True},
          {"subject": "OCC1", "catalog": "551",  "title": "Psychosocial Practice in OT", "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "209",  "title": "Mammalian Physiology 1", "credits": 3, "is_required": True},
          {"subject": "PHGY", "catalog": "210",  "title": "Mammalian Physiology 2", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "204",  "title": "Introduction to Statistics for OT/PT", "credits": 3, "is_required": True,
           "notes": "Waived if CEGEP stats ≥75%; replace with additional complementary course."},
          {"subject": "POTH", "catalog": "225",  "title": "Introduction to Biomechanics in Rehabilitation Sciences", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "250",  "title": "Introduction to Professional Practice 2", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "305",  "title": "Statistics for Experimental Design OT/PT", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "401",  "title": "Research Methods", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "434",  "title": "Musculoskeletal Biomechanics", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "455",  "title": "Neurophysiology", "credits": 3, "is_required": True},
          {"subject": "POTH", "catalog": "563",  "title": "Foundations of Professional Practice", "credits": 3, "is_required": True},
        ],
      },

      # ── Complementary Courses ─────────────────────────────────────────
      {
        "block_key":      "ot_complementary",
        "title":          "Complementary Courses (15 credits)",
        "block_type":     "choose_credits",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "15 complementary credits from: Psychology (lifespan development recommended), "
          "Management, Academic Writing, Sociology/Anthropology, or second language (max 6 cr.). "
          "POTH 204 exemption adds 3 credits to this requirement."
        ),
        "courses": [],
      },

    ],
  },

]


# ──────────────────────────────────────────────────────────────────────────
#  Helper Functions
# ──────────────────────────────────────────────────────────────────────────

def _upsert_program(supabase, prog: dict) -> str:
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
    """Seed all SPOT degree programs into the database."""
    stats = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in SPOT_PROGRAMS:
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

    logger.info(f"SPOT seed complete: {stats}")
    return stats


if __name__ == "__main__":
    import os, sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    result = seed_degree_requirements(supabase)
    print(f"Seeded: {result['programs']} programs, {result['blocks']} blocks, {result['courses']} courses")
    if result["errors"]:
        print(f"Errors ({len(result['errors'])}):")
        for e in result["errors"]:
            print(f"  {e}")
