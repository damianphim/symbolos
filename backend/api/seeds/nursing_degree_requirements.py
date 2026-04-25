"""
McGill Ingram School of Nursing – Degree Requirements Seed Data
Source: McGill eCalendar 2024-2025 & Ingram School of Nursing website
https://www.mcgill.ca/study/2024-2025/faculties/nursing/
https://www.mcgill.ca/nursing/programs/bachelor-programs/

This file covers the two undergraduate nursing programs:
  1. Bachelor of Science (Nursing) – B.Sc.(N.)  (103 credits for CEGEP entrants;
     136–137 credits for high-school / out-of-province entrants including U0 science year)
  2. Bachelor of Nursing (Integrated) – B.N.I.   (65 credits at McGill; 92 total with
     27 credits advanced standing for 180.A.0 DEC holders)

Accuracy notes:
  - The B.Sc.(N.) is structured as U0 (science prerequisites, non-CEGEP only),
    U1 (36 cr), U2 (34 cr), U3 (26 cr + 5 cr complementary NUR1 530/531).
  - The B.N.I. is for holders of the 180.A.0 DEC in Nursing from a Quebec CEGEP;
    students receive 27 credits of advanced standing and complete 65 credits at McGill.
  - The B.N.I. is offered in two delivery modes: on-campus and fully online.
  - IPEA courses (500–503) are interprofessional education activities, appear on
    transcript as Pass/Fail. In the B.Sc.(N.) all four IPEAs are taken in U1.
  - French language proficiency (B2 level) is required for full nursing licensure in Quebec.
  - Both programs are accredited by the Canadian Association of Schools of Nursing (CASN).
  - Completion of B.Sc.(N.) or B.N.I. entitles graduates to sit licensure examinations
    in Quebec (OIIQ) and across Canada.
  - Electives: 9 credits for B.Sc.(N.) CEGEP entrants (min 3 cr at 300+ level);
    6 credits for U0 high-school entrants (min 3 cr at 300+ level).
  - Verified against eCalendar 2024-2025 (January 2026).

Course prefix key:
  NUR1  Nursing (Ingram School of Nursing)
  IPEA  Interprofessional Education Activities (0-credit workshops)
  EDPE  Educational Psychology (EDPE 375 = Introduction to Statistics)
  PSYC  Psychology (PSYC 204 = Statistics equivalent)
  BIOL  Biology
  CHEM  Chemistry
  PHYS  Physics (U0 prerequisites)
  ANAT  Anatomy (U0 prerequisite)
  PHGY  Physiology (U0 prerequisite)
"""

import logging
logger = logging.getLogger(__name__)


NURSING_PROGRAMS = [

  # ════════════════════════════════════════════════════════════════════════
  #  B.Sc.(N.) – NURSING  (103 credits)
  # ════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "bscn_nursing",
    "name":          "Bachelor of Science (Nursing) – B.Sc.(N.) (103 credits)",
    "program_type":  "major",
    "faculty":       "Ingram School of Nursing",
    "total_credits": 103,
    "description": (
      "The B.Sc.(N.) is a 3-year program (103 credits) for CEGEP-prepared students "
      "that focuses on complex and contemporary nursing issues. High school and "
      "out-of-province entrants complete an additional U0 science year (~33–34 credits) "
      "before beginning the three-year nursing sequence. The program prepares graduates "
      "for entry-level nursing practice and for sitting licensure examinations in Quebec "
      "(OIIQ) and Canada. Accredited by the Canadian Association of Schools of Nursing "
      "since 1990 (full accreditation until 2031). French B2 proficiency is required "
      "for full licensure in Quebec. Students with a completed bachelor's degree may "
      "transfer to the MScA-N Qualifying Year after U2 summer."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/nursing/undergraduate/programs/"
      "bachelor-science-nursing-bscn-nursing"
    ),
    "blocks": [

      # ── U0 (Freshman Science Prerequisites) ───────────────────────────
      {
        "block_key":      "bscn_u0_prerequisites",
        "title":          "U0 Science Prerequisites (for high school / out-of-province entrants only)",
        "block_type":     "required",
        "credits_needed": 27,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "CEGEP entrants are exempt from U0 and begin directly in U1. "
          "High school, out-of-province, mature, and IB students typically need all of these. "
          "All math and science courses must have been completed within the last five years. "
          "CHEM 110/120/212 are each 4 credits; PHYS 101/102 are each 4 credits."
        ),
        "courses": [
          {"subject": "BIOL", "catalog": "112",  "title": "Cell and Molecular Biology", "credits": 3, "is_required": True},
          {"subject": "CHEM", "catalog": "110",  "title": "General Chemistry 1", "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "120",  "title": "General Chemistry 2", "credits": 4, "is_required": True},
          {"subject": "CHEM", "catalog": "212",  "title": "Introductory Organic Chemistry 1", "credits": 4, "is_required": True},
          {"subject": "MATH", "catalog": "141",  "title": "Calculus 2", "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "101",  "title": "Introductory Physics – Mechanics", "credits": 4, "is_required": True},
          {"subject": "PHYS", "catalog": "102",  "title": "Introductory Physics – Electromagnetism & Optics", "credits": 4, "is_required": True},
        ],
      },

      # ── U1 Year ───────────────────────────────────────────────────────
      {
        "block_key":      "bscn_u1_required",
        "title":          "Year 1 (U1) – Required Courses",
        "block_type":     "required",
        "credits_needed": 37,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Taken over Fall, Winter, and Summer terms of U1. "
          "Fall: NUR1 331, NUR1 335, IPEA 500. "
          "Winter: NUR1 209, 210, 221, 224, 311, IPEA 501. "
          "Summer: NUR1 225, 230, 231, 233, 234, 235, 236. "
          "IPEA courses are non-credit, Pass/Fail, mandatory for graduation."
        ),
        "courses": [
          {"subject": "NUR1", "catalog": "209",  "title": "Pathophysiology for Nursing 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "210",  "title": "Pathophysiology for Nursing 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "221",  "title": "Intro to Prof Practice & Strengths-Based Nursing and Healthcare", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "224",  "title": "Individual and Family Development Across Lifespans 1", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "225",  "title": "Individual and Family Development Across Lifespans 2", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "230",  "title": "Supporting Health and Healing Capacities 1", "credits": 1, "is_required": True},
          {"subject": "NUR1", "catalog": "231",  "title": "Supporting Health and Healing Capacities 2", "credits": 1, "is_required": True},
          {"subject": "NUR1", "catalog": "233",  "title": "Promoting Young Family Development (Clinical)", "credits": 2, "is_required": True},
          {"subject": "NUR1", "catalog": "234",  "title": "Nursing Older Adults (Clinical)", "credits": 2, "is_required": True},
          {"subject": "NUR1", "catalog": "235",  "title": "Health and Physical Assessment/Anatomy 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "236",  "title": "Health and Physical Assessment/Anatomy 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "311",  "title": "Infection Prevention and Control", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "331",  "title": "Nursing in Illness 1 (Clinical)", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "335",  "title": "Illness Management Clinical Skills Laboratory 1", "credits": 1, "is_required": True},
          {"subject": "IPEA", "catalog": "500",  "title": "Roles in Interprofessional Teams (0 credits, Pass/Fail)", "credits": 0, "is_required": True,
           "notes": "Mandatory IPE workshop – non-credit, appears on transcript."},
          {"subject": "IPEA", "catalog": "501",  "title": "Communication in Interprofessional Teams (0 credits, Pass/Fail)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "502",  "title": "Patient-Centred Care in Action (0 credits, Pass/Fail)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "503",  "title": "Managing Interprofessional Conflict (0 credits, Pass/Fail)", "credits": 0, "is_required": True},
        ],
      },

      # ── U2 Year ───────────────────────────────────────────────────────
      {
        "block_key":      "bscn_u2_required",
        "title":          "Year 2 (U2) – Required Courses",
        "block_type":     "required",
        "credits_needed": 28,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Taken over Fall, Winter, and Summer terms of U2. "
          "Fall: NUR1 329. "
          "Winter: NUR1 300, 301, 323, 324, 325, 326, IPEA 502, 503 (IPEA 0-credit, counted in U1 block). "
          "Summer: NUR1 332, 333 (or 431 as alternative), 336."
        ),
        "courses": [
          {"subject": "NUR1", "catalog": "300",  "title": "Pharmacology for Nursing 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "301",  "title": "Pharmacology for Nursing 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "323",  "title": "Illness Management 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "324",  "title": "Illness Management 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "325",  "title": "Acute, Chronic, and Palliative Health Challenges 1", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "326",  "title": "Acute, Chronic, and Palliative Health Challenges 2", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "329",  "title": "Skin Integrity and Wound Care", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "332",  "title": "Nursing in Illness 2 (Clinical)", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "333",  "title": "Nursing in Illness 3 (Clinical)", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "336",  "title": "Illness Management Clinical Skills Laboratory 2", "credits": 1, "is_required": True},
        ],
      },

      # ── U3 Year ───────────────────────────────────────────────────────
      {
        "block_key":      "bscn_u3_required",
        "title":          "Year 3 (U3) – Required Courses",
        "block_type":     "required",
        "credits_needed": 15,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "Taken over Fall and Winter terms of U3. "
          "Fall: NUR1 424, 432, 529, and electives. "
          "Winter: NUR1 423, plus complementary NUR1 530 or 531."
        ),
        "courses": [
          {"subject": "NUR1", "catalog": "423",  "title": "Leading Change: Policy and Practice", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "424",  "title": "Legal, Ethical, and Professional Practice Issues", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "432",  "title": "Community Health Nursing Project", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "529",  "title": "Critical Care Nursing", "credits": 4, "is_required": True},
        ],
      },

      # ── U3 Complementary ──────────────────────────────────────────────
      {
        "block_key":      "bscn_u3_complementary",
        "title":          "Year 3 (U3) – Complementary Course (choose one, 5 credits)",
        "block_type":     "choose_courses",
        "credits_needed": 5,
        "courses_needed": 1,
        "group_name":     None,
        "notes": "Choose one of NUR1 530 or NUR1 531.",
        "courses": [
          {"subject": "NUR1", "catalog": "530",  "title": "Nursing Practice Consolidation", "credits": 5, "is_required": False,
           "recommended": True, "recommendation_reason": "Standard nursing practice consolidation placement."},
          {"subject": "NUR1", "catalog": "531",  "title": "Ambassador Nursing Practice Consolidation", "credits": 5, "is_required": False},
        ],
      },

      # ── Electives ─────────────────────────────────────────────────────
      {
        "block_key":      "bscn_electives",
        "title":          "Electives",
        "block_type":     "choose_credits",
        "credits_needed": 9,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "9 elective credits (for CEGEP/U1 entrants), at the 200–500 level, "
          "with at least 3 credits at the 300-level or above. "
          "Students entering at U0 need only 6 elective credits. "
          "Includes the required statistics course: PSYC 204 or EDPE 375 (3 credits)."
        ),
        "courses": [
          {"subject": "PSYC", "catalog": "204",  "title": "Introduction to Psychological Statistics (or EDPE 375)", "credits": 3,
           "is_required": False, "recommended": True,
           "recommendation_reason": "Required statistics course; counts as one of the elective credits."},
          {"subject": "EDPE", "catalog": "375",  "title": "Introduction to Statistics (or PSYC 204)", "credits": 3,
           "is_required": False, "notes": "Alternative to PSYC 204 for the required stats elective."},
        ],
      },

    ],
  },

  # ════════════════════════════════════════════════════════════════════════
  #  B.N.I. – BACHELOR OF NURSING (INTEGRATED)  (65 credits at McGill)
  # ════════════════════════════════════════════════════════════════════════
  {
    "program_key":   "bni_nursing",
    "name":          "Bachelor of Nursing (Integrated) – B.N.I. (65 credits at McGill)",
    "program_type":  "major",
    "faculty":       "Ingram School of Nursing",
    "total_credits": 65,
    "description": (
      "The B.N.I. is a 2-year, 5-semester accelerated completion program (65 credits "
      "at McGill) for holders of the 180.A.0 DEC in Nursing from a Quebec CEGEP. "
      "Students are admitted at the U2 level with 27 credits of advanced standing "
      "(total program = 92 credits). The program expands students' knowledge base, "
      "strengthens critical thinking, and prepares them for baccalaureate-level nursing "
      "roles. Offered in two modalities: on-campus and fully online. Online students "
      "must register in online course sections (020-series). Applicants must apply "
      "within three years of obtaining their DEC 180.A.0. CASN accredited. "
      "Elective requirement: 6 credits (at least 3 credits at 300-level or above)."
    ),
    "ecalendar_url": (
      "https://www.mcgill.ca/study/2024-2025/faculties/nursing/undergraduate/programs/"
      "bachelor-nursing-bni-integrated-nursing"
    ),
    "blocks": [

      # ── BNI Required Courses ──────────────────────────────────────────
      # Source: eCalendar 2024-2025, verified January 2026. 55 required credits.
      {
        "block_key":      "bni_required",
        "title":          "BNI Required Courses (55 credits)",
        "block_type":     "required",
        "credits_needed": 55,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "All courses are required. IPEA 500–503 are 0-credit interprofessional "
          "education activities (mandatory, Pass/Fail). PSYC 204 is the required "
          "statistics course. Program delivered over 5 semesters (2 years). "
          "Online students register in 020-series sections."
        ),
        "courses": [
          {"subject": "NUR1", "catalog": "209",  "title": "Pathophysiology for Nursing 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "210",  "title": "Pathophysiology for Nursing 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "222",  "title": "Strengths-Based Nursing and Healthcare and Professional Practice", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "300",  "title": "Pharmacology for Nursing 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "301",  "title": "Pharmacology for Nursing 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "312",  "title": "Research in Nursing", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "318",  "title": "Chronic Illness and Palliative Health Challenges", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "320",  "title": "Critical Care Nursing Theory", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "327",  "title": "Critical Health Challenges", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "329",  "title": "Skin Integrity and Wound Care", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "338",  "title": "Applied Health and Physical Assessment/Anatomy 1", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "339",  "title": "Applied Health and Physical Assessment/Anatomy 2", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "423",  "title": "Leading Change: Policy and Practice", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "424",  "title": "Legal, Ethical, and Professional Practice Issues", "credits": 4, "is_required": True},
          {"subject": "NUR1", "catalog": "431",  "title": "Community Health Nursing Practicum", "credits": 3, "is_required": True},
          {"subject": "NUR1", "catalog": "432",  "title": "Community Health Nursing Project", "credits": 3, "is_required": True},
          {"subject": "PSYC", "catalog": "204",  "title": "Introduction to Psychological Statistics", "credits": 3, "is_required": True,
           "notes": "Required statistics course."},
          {"subject": "IPEA", "catalog": "500",  "title": "Roles in Interprofessional Teams (0 credits)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "501",  "title": "Communication in Interprofessional Teams (0 credits)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "502",  "title": "Patient-Centred Care in Action (0 credits)", "credits": 0, "is_required": True},
          {"subject": "IPEA", "catalog": "503",  "title": "Managing Interprofessional Conflict (0 credits)", "credits": 0, "is_required": True},
        ],
      },

      # ── BNI Complementary (choose one) ────────────────────────────────
      {
        "block_key":      "bni_complementary",
        "title":          "BNI Complementary Course (choose one, 4 credits)",
        "block_type":     "choose_courses",
        "credits_needed": 4,
        "courses_needed": 1,
        "group_name":     None,
        "notes": "Choose one of NUR1 434 or NUR1 435.",
        "courses": [
          {"subject": "NUR1", "catalog": "434",  "title": "Critical Care Nursing Practicum", "credits": 4, "is_required": False,
           "recommended": True, "recommendation_reason": "Regularly scheduled; NUR1 435 is offered less frequently."},
          {"subject": "NUR1", "catalog": "435",  "title": "Ambassador Critical Care Practicum", "credits": 4, "is_required": False},
        ],
      },

      # ── Electives ─────────────────────────────────────────────────────
      {
        "block_key":      "bni_electives",
        "title":          "Electives",
        "block_type":     "choose_credits",
        "credits_needed": 6,
        "courses_needed": None,
        "group_name":     None,
        "notes": (
          "6 elective credits (at least 3 credits at the 300-level or above). "
          "May be taken in U2 Summer or U3 Winter term. "
          "Electives may be taken in any order as long as prerequisites are met and "
          "the course fits within the nursing timetable."
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
    """Seed all Ingram School of Nursing degree programs into the database."""
    stats = {"programs": 0, "blocks": 0, "courses": 0, "errors": []}

    for prog in NURSING_PROGRAMS:
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

    logger.info(f"Nursing seed complete: {stats}")
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
