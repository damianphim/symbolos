"""
McGill Faculty of Law – BCL/JD Degree Requirements Seed Data
Source: McGill Law Student Affairs Office (2025-2026)
https://www.mcgill.ca/law-studies/bcljd-studies/structure/courses

Program: Bachelor of Civil Law / Juris Doctor (BCL/JD)
  - 105 credits total
  - 47 credits required
  - 12 credits complementary (4 groups × 3 cr each)
  - 46 credits elective
  - 1 research paper (writing requirement)

Admission note: Students must have completed at least 60 university credits
before being admitted to the BCL/JD program. Law courses use unique subject
codes: LAWG, PUB2, PUB3, PRV2–5, PROC, PRAC, BUS1–2, CMPL, LEEL, IDFC.

Accuracy notes:
  - Verified from official McGill Law SAO pages (February 2026)
  - Enrollment as of 2020 curriculum (current intake)
  - All first-year courses offered in both English and French
  - Upper-year courses in either French or English
"""

LAW_PROGRAMS = [

  # ══════════════════════════════════════════════════════════════════════
  #  BCL/JD – BACHELOR OF CIVIL LAW / JURIS DOCTOR (105 credits)
  # ══════════════════════════════════════════════════════════════════════
  {
    "program_key":   "law_bcl_jd",
    "name":          "Bachelor of Civil Law / Juris Doctor (BCL/JD)",
    "program_type":  "major",
    "faculty":       "Faculty of Law",
    "total_credits": 105,
    "description": (
      "The BCL/JD is McGill's unique dual-degree law program, integrating the Civil Law "
      "and Common Law traditions in a single three-year curriculum taught bilingually. "
      "Graduates receive both the Bachelor of Civil Law (BCL) and the Juris Doctor (JD), "
      "qualifying them to practise in Quebec (civil law jurisdiction) and all common law "
      "provinces. Admission requires at least 60 completed university credits. "
      "The 105-credit program consists of 47 required credits, 12 complementary credits "
      "across four groups, 46 elective credits from Faculty offerings, and one research "
      "paper (writing requirement)."
    ),
    "ecalendar_url": "https://www.mcgill.ca/law-studies/bcljd-studies/structure/courses",
    "blocks": [

      # ── FIRST-YEAR REQUIRED (33 cr) ──────────────────────────────────
      {
        "block_key":   "law_1y_required",
        "title":       "Required Courses – First Year (33 credits)",
        "block_type":  "required",
        "credits_needed": 33,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "All 33 credits must be taken in first year. Courses offered in both English "
          "and French. D1/D2 courses must be registered together and completed in "
          "consecutive terms."
        ),
        "sort_order":  1,
        "courses": [
          {"subject": "LAWG", "catalog": "100D1", "title": "Contractual Obligations",            "credits": 3,   "is_required": True, "notes": "Must register for both LAWG 100D1 and LAWG 100D2. Completed in consecutive terms."},
          {"subject": "LAWG", "catalog": "100D2", "title": "Contractual Obligations",            "credits": 3,   "is_required": True, "notes": "Prereq: LAWG 100D1. Completed in consecutive terms."},
          {"subject": "LAWG", "catalog": "101D1", "title": "Extra-Contractual Obligations/Torts","credits": 3,   "is_required": True, "notes": "Must register for both LAWG 101D1 and LAWG 101D2."},
          {"subject": "LAWG", "catalog": "101D2", "title": "Extra-Contractual Obligations/Torts","credits": 3,   "is_required": True, "notes": "Prereq: LAWG 101D1. Completed in consecutive terms."},
          {"subject": "LAWG", "catalog": "102D1", "title": "Criminal Justice",                   "credits": 3,   "is_required": True, "notes": "Must register for both LAWG 102D1 and LAWG 102D2."},
          {"subject": "LAWG", "catalog": "102D2", "title": "Criminal Justice",                   "credits": 3,   "is_required": True, "notes": "Prereq: LAWG 102D1. Completed in consecutive terms."},
          {"subject": "LAWG", "catalog": "103",   "title": "Indigenous Legal Traditions",        "credits": 3,   "is_required": True, "notes": "Open only to first-year McGill law students. Taught in English and French."},
          {"subject": "LAWG", "catalog": "110D1", "title": "Integration Workshop",               "credits": 1.5, "is_required": True, "notes": "Must register for both LAWG 110D1 and LAWG 110D2."},
          {"subject": "LAWG", "catalog": "110D2", "title": "Integration Workshop",               "credits": 1.5, "is_required": True, "notes": "Prereq: LAWG 110D1. Completed in consecutive terms."},
          {"subject": "PUB2", "catalog": "101D1", "title": "Constitutional Law",                 "credits": 3,   "is_required": True, "notes": "Must register for both PUB2 101D1 and PUB2 101D2."},
          {"subject": "PUB2", "catalog": "101D2", "title": "Constitutional Law",                 "credits": 3,   "is_required": True, "notes": "Prereq: PUB2 101D1. Completed in consecutive terms."},
          {"subject": "PUB3", "catalog": "116",   "title": "Foundations",                        "credits": 3,   "is_required": True, "notes": "Overview of Civil and Common Law traditions and Aboriginal legal traditions."},
        ],
      },

      # ── SECOND-YEAR REQUIRED (14 cr) ─────────────────────────────────
      {
        "block_key":   "law_2y_required",
        "title":       "Required Courses – Second Year (14 credits)",
        "block_type":  "required",
        "credits_needed": 14,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "All 14 credits must be taken in second year. "
          "PROC 124 is an intensive course held in May/June."
        ),
        "sort_order":  2,
        "courses": [
          {"subject": "LAWG", "catalog": "210",   "title": "Legal Ethics and Professionalism",       "credits": 3, "is_required": True, "notes": "Limited to 2nd-year Law students only. Includes Focus Week intensive sessions."},
          {"subject": "LAWG", "catalog": "220D1", "title": "Property",                               "credits": 3, "is_required": True, "notes": "Must register for both LAWG 220D1 and LAWG 220D2."},
          {"subject": "LAWG", "catalog": "220D2", "title": "Property",                               "credits": 3, "is_required": True, "notes": "Prereq: LAWG 220D1. Completed in consecutive terms."},
          {"subject": "PRAC", "catalog": "200",   "title": "Advocacy",                               "credits": 1, "is_required": True, "notes": "Critical analysis of oral advocacy skills. Limited to 2nd-year Law students."},
          {"subject": "PROC", "catalog": "124",   "title": "Judicial Institutions and Civil Procedure","credits": 4, "is_required": True, "notes": "Intensive format; held May–June. Covers Quebec, Ontario, and federal courts."},
        ],
      },

      # ── COMPLEMENTARY A: CIVIL LAW IMMERSION (3 cr) ──────────────────
      {
        "block_key":   "law_comp_civil_law",
        "title":       "Complementary A – Civil Law Immersion (3 credits)",
        "block_type":  "choose_credits",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "Choose at least 3 credits from this list of Civil Law immersion courses. "
          "These courses provide immersion in the culture, epistemology and practices "
          "of the Civil Law Tradition."
        ),
        "sort_order":  3,
        "courses": [
          {"subject": "BUS2", "catalog": "561",   "title": "Insurance",                            "credits": 3, "notes": "General principles of insurance contract under Quebec law. Not open to students who took BUS2 461."},
          {"subject": "LAWG", "catalog": "506",   "title": "Advanced Civil Law Property",          "credits": 3, "notes": "Civil law reasoning and methodology through property concepts."},
          {"subject": "PROC", "catalog": "200",   "title": "Advanced Civil Law Obligations",       "credits": 3, "notes": "General theory of obligations in the Civil Law tradition. Includes unjust enrichment."},
          {"subject": "PRV2", "catalog": "270",   "title": "Law of Persons",                       "credits": 3, "notes": "Existence and attributes of physical and legal persons in the Civil Law of Quebec.", "recommended": True, "recommendation_reason": "Foundational civil law course, frequently offered."},
          {"subject": "PRV4", "catalog": "548",   "title": "Administration Property of Another and Trusts", "credits": 3, "notes": "Basic law on administration of property of another. Not open to students who took PRV4 448."},
        ],
      },

      # ── COMPLEMENTARY B: COMMON LAW IMMERSION (3 cr) ─────────────────
      {
        "block_key":   "law_comp_common_law",
        "title":       "Complementary B – Common Law Immersion (3 credits)",
        "block_type":  "choose_credits",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "Choose at least 3 credits from this list of Common Law immersion courses. "
          "These courses provide immersion in the culture, epistemology and practices "
          "of the Common Law Tradition."
        ),
        "sort_order":  4,
        "courses": [
          {"subject": "PRV3", "catalog": "200",   "title": "Advanced Common Law Obligations",      "credits": 3, "notes": "Tort, contract, and restitution in theory and practice. Covers unjust enrichment.", "recommended": True, "recommendation_reason": "Frequently offered; core common law course."},
          {"subject": "PRV3", "catalog": "534",   "title": "Remedies",                             "credits": 3, "notes": "Selected private law remedies at common law, in equity, and under statute. Not open to students who took PRV3 434."},
          {"subject": "PRV4", "catalog": "500",   "title": "Restitution",                          "credits": 3, "notes": "Law of restitution and unjust enrichment at common law. Not open to students who took PRV4 435."},
          {"subject": "PRV4", "catalog": "549",   "title": "Equity and Trusts",                    "credits": 3, "notes": "Law of gratuitous transfers, express trusts, powers of appointment. Not open to students who took PRV4 449 or PRV4 449D1/D2."},
        ],
      },

      # ── COMPLEMENTARY C: SOCIAL DIVERSITY / HR / INDIGENOUS (3 cr) ───
      {
        "block_key":   "law_comp_diversity_hr",
        "title":       "Complementary C – Social Diversity, Human Rights and Indigenous Law (3 credits)",
        "block_type":  "choose_credits",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "Choose at least 3 credits from this list of courses on social diversity, "
          "human rights, and Indigenous law."
        ),
        "sort_order":  5,
        "courses": [
          {"subject": "CMPL", "catalog": "500",   "title": "Indigenous Peoples and the State",      "credits": 3, "recommended": True, "recommendation_reason": "Frequently offered; important for Canadian law practice."},
          {"subject": "CMPL", "catalog": "504",   "title": "Feminist Legal Theory",                 "credits": 3},
          {"subject": "CMPL", "catalog": "511",   "title": "Social Diversity and Law",              "credits": 3},
          {"subject": "CMPL", "catalog": "516",   "title": "International Development Law",         "credits": 3},
          {"subject": "CMPL", "catalog": "565",   "title": "International Humanitarian Law",        "credits": 3, "notes": "Prereq: PUB2 105. Not open to first-year students."},
          {"subject": "CMPL", "catalog": "571",   "title": "International Law of Human Rights",     "credits": 3, "recommended": True, "recommendation_reason": "Frequently offered."},
          {"subject": "CMPL", "catalog": "573",   "title": "Civil Liberties",                       "credits": 3},
          {"subject": "CMPL", "catalog": "575",   "title": "Discrimination and the Law",            "credits": 3},
          {"subject": "IDFC", "catalog": "500",   "title": "Indigenous Field Studies",              "credits": 3, "notes": "Intensive field course; 1 week living in the field. Additional fee ~$447. Open to Law students."},
          {"subject": "LAWG", "catalog": "503",   "title": "Inter-American Human Rights",           "credits": 3, "notes": "Restricted to Law students. Language of instruction may vary."},
          {"subject": "LAWG", "catalog": "505",   "title": "Critical Engagements with Human Rights","credits": 3, "notes": "Prereq: LAWG 517 or instructor permission."},
          {"subject": "LAWG", "catalog": "507",   "title": "Critical Race Theory Advanced Seminar", "credits": 3},
          {"subject": "LAWG", "catalog": "508D1", "title": "Indigenous Constitutionalism",          "credits": 3, "notes": "Must register for both LAWG 508D1 and LAWG 508D2."},
          {"subject": "LAWG", "catalog": "508D2", "title": "Indigenous Constitutionalism",          "credits": 3, "notes": "Prereq: LAWG 508D1. Completed in consecutive terms."},
          {"subject": "LEEL", "catalog": "369",   "title": "Labour Law",                            "credits": 3, "notes": "Also counts toward Group D (Administrative Law)."},
          {"subject": "LEEL", "catalog": "582",   "title": "Law and Poverty",                       "credits": 3, "notes": "Not open to students who took LEEL 482. Also counts toward Group D."},
          {"subject": "PUB2", "catalog": "105",   "title": "Public International Law",              "credits": 3},
          {"subject": "PUB2", "catalog": "500",   "title": "Law and Psychiatry",                    "credits": 3, "notes": "Open to limited students in Law, Psychiatry, and Psychology. Also counts toward Group D."},
          {"subject": "PUB2", "catalog": "502",   "title": "International Criminal Law",            "credits": 3, "notes": "Not open to students who took PUB2 425."},
          {"subject": "PUB2", "catalog": "551",   "title": "Immigration and Refugee Law",           "credits": 3, "notes": "Not open to students who took PUB2 451. Also counts toward Group D."},
        ],
      },

      # ── COMPLEMENTARY D: ADMINISTRATIVE LAW (3 cr) ───────────────────
      {
        "block_key":   "law_comp_admin_law",
        "title":       "Complementary D – Principles of Administrative Law (3 credits)",
        "block_type":  "choose_credits",
        "credits_needed": 3,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "Choose at least 3 credits from this list of courses covering principles of "
          "Canadian administrative law and related regulatory subjects."
        ),
        "sort_order":  6,
        "courses": [
          {"subject": "BUS1", "catalog": "532",   "title": "Bankruptcy and Insolvency",             "credits": 3, "notes": "Not open to students who took BUS1 432."},
          {"subject": "BUS2", "catalog": "504",   "title": "Securities Regulation",                 "credits": 3, "notes": "Not open to students who took BUS2 372."},
          {"subject": "CMPL", "catalog": "539",   "title": "International Taxation",                "credits": 3},
          {"subject": "CMPL", "catalog": "543",   "title": "Law and Practice of International Trade","credits": 3},
          {"subject": "CMPL", "catalog": "574",   "title": "Government Control of Business",        "credits": 3},
          {"subject": "CMPL", "catalog": "575",   "title": "Discrimination and the Law",            "credits": 3, "notes": "Not open to students who took CMPL 475. Also counts toward Group C."},
          {"subject": "CMPL", "catalog": "577",   "title": "Communications Law",                    "credits": 3},
          {"subject": "CMPL", "catalog": "580",   "title": "Environment and the Law",               "credits": 3},
          {"subject": "LAWG", "catalog": "523",   "title": "Tax Practice Seminar",                  "credits": 3},
          {"subject": "LEEL", "catalog": "369",   "title": "Labour Law",                            "credits": 3, "recommended": True, "recommendation_reason": "Frequently offered; also counts toward Group C."},
          {"subject": "LEEL", "catalog": "570",   "title": "Employment Law",                        "credits": 3, "notes": "Not open to students who took LEEL 470."},
          {"subject": "LEEL", "catalog": "582",   "title": "Law and Poverty",                       "credits": 3, "notes": "Not open to students who took LEEL 482. Also counts toward Group C."},
          {"subject": "PRV4", "catalog": "545",   "title": "Land Use Planning",                     "credits": 3, "notes": "Not open to students who took PRV4 145."},
          {"subject": "PRV5", "catalog": "483",   "title": "Consumer Law",                          "credits": 3},
          {"subject": "PUB2", "catalog": "400",   "title": "The Administrative Process",            "credits": 3, "recommended": True, "recommendation_reason": "Core administrative law; frequently offered."},
          {"subject": "PUB2", "catalog": "401",   "title": "Judicial Review of Administrative Action","credits": 3, "recommended": True, "recommendation_reason": "Core administrative law; frequently offered."},
          {"subject": "PUB2", "catalog": "500",   "title": "Law and Psychiatry",                    "credits": 3, "notes": "Also counts toward Group C."},
          {"subject": "PUB2", "catalog": "515",   "title": "Tax Policy",                            "credits": 3, "notes": "Not open to students who took PUB2 415."},
          {"subject": "PUB2", "catalog": "551",   "title": "Immigration and Refugee Law",           "credits": 3, "notes": "Not open to students who took PUB2 451. Also counts toward Group C."},
        ],
      },

      # ── ELECTIVES (46 cr) ────────────────────────────────────────────
      {
        "block_key":   "law_electives",
        "title":       "Elective Courses (46 credits)",
        "block_type":  "choose_credits",
        "credits_needed": 46,
        "courses_needed": None,
        "group_name":  None,
        "notes": (
          "46 credits of elective courses from any Faculty of Law offerings, or courses "
          "approved as credit equivalences. The available elective list varies each year — "
          "see the Faculty's Current Courses page. Electives may include upper-year "
          "seminars, clinics, international exchange credits, focus week workshops, "
          "student-initiated seminars, and approved non-course credits."
        ),
        "sort_order":  7,
        "courses": [],
      },

      # ── WRITING REQUIREMENT ───────────────────────────────────────────
      {
        "block_key":   "law_writing_requirement",
        "title":       "Research Paper (Writing Requirement)",
        "block_type":  "required",
        "credits_needed": None,
        "courses_needed": 1,
        "group_name":  None,
        "notes": (
          "All students must submit at least one research paper. This may be satisfied by: "
          "(1) writing an essay in a course where the essay constitutes ≥75% of the final grade; "
          "(2) writing a supervised term essay for credit within the Faculty of Law; or "
          "(3) publishing an article in the McGill Law Journal, approved by the Faculty Advisor. "
          "Papers written jointly do not satisfy this requirement."
        ),
        "sort_order":  8,
        "courses": [],
      },

    ],
  },

]


def seed_degree_requirements(supabase):
    """
    Insert all Faculty of Law (BCL/JD) degree requirements into Supabase.
    Safe to re-run: uses upsert on program_key, then deletes+reinserts blocks.
    """
    inserted_programs = 0
    inserted_blocks = 0
    inserted_courses = 0

    for prog in LAW_PROGRAMS:
        # ── Upsert program ──────────────────────────────────────────
        prog_data = {
            "program_key":   prog["program_key"],
            "name":          prog["name"],
            "faculty":       prog.get("faculty", "Faculty of Law"),
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

        # ── Clean re-seed blocks ────────────────────────────────────
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

            courses_batch = []
            for j, course in enumerate(block.get("courses", [])):
                is_required = course.get("is_required", False)
                if block.get("block_type") == "required":
                    is_required = True

                courses_batch.append({
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
            for chunk_start in range(0, len(courses_batch), 50):
                chunk = courses_batch[chunk_start:chunk_start + 50]
                if chunk:
                    supabase.table("requirement_courses").insert(chunk).execute()
                    inserted_courses += len(chunk)

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
