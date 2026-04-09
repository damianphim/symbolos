"""
McGill Faculty of Arts – Degree Requirements Seed Data
Source: McGill Course Catalogue 2024-2025 / 2025-2026
https://coursecatalogue.mcgill.ca/en/undergraduate/arts/programs/

Split into sub-modules by department group for maintainability:
  arts_social_sciences.py     — Cognitive Sci, Anthropology, Economics, Pol Sci, Psychology, Sociology
  arts_humanities.py          — Linguistics, History, Art History, English, Philosophy, Communication Studies
  arts_area_studies.py        — IDS, GSFSJ, Canadian Studies, Classics, Jewish, East Asian, World Islamic,
                                Geography, CS (BA), German, Hispanic, Italian, French, African,
                                Religious Studies, Info Studies, Liberal Arts, European Lit, Latin American Minor
  arts_honours.py             — All standard honours programs
  arts_languages_specialty.py — African Major, English Drama/Cultural, Russian, Latin American Major,
                                Software Engineering, language minors, Traduction, East Asian sub-minors,
                                Geography Urban Studies, additional honours
  arts_math_stats_env.py      — Math, Stats, Environment, Geography joint, GIS, Health Geography,
                                Urban Studies, Behavioural Science, Music minors, Science for Arts
"""

from api.seeds.arts_social_sciences import ARTS_SOCIAL_SCIENCES
from api.seeds.arts_humanities import ARTS_HUMANITIES
from api.seeds.arts_area_studies import ARTS_AREA_STUDIES
from api.seeds.arts_honours import ARTS_HONOURS
from api.seeds.arts_languages_specialty import ARTS_LANGUAGES_SPECIALTY
from api.seeds.arts_math_stats_env import ARTS_MATH_STATS_ENV

ARTS_PROGRAMS = (
    ARTS_SOCIAL_SCIENCES
    + ARTS_HUMANITIES
    + ARTS_AREA_STUDIES
    + ARTS_HONOURS
    + ARTS_LANGUAGES_SPECIALTY
    + ARTS_MATH_STATS_ENV
)

# ──────────────────────────────────────────────────────────────────
# Database seed function
# ──────────────────────────────────────────────────────────────────

def seed_degree_requirements(supabase):
    """
    Insert all Arts degree requirements into Supabase.
    Safe to re-run: uses upsert on program_key, then deletes+reinserts blocks.

    Block types stored in DB:
      required       — every course must be taken
      choose_credits — take credits_needed credits from list
      choose_courses — take courses_needed courses from list
      group          — named sub-group (Group A/B/C) feeding a parent rule
      multi_group    — parent: "X credits from Group A AND Y from Group B"
      pool_group     — parent: "at least X credits from Groups A+B+C combined"
      level_elective — any courses at a given level range
    """
    inserted_programs = 0
    inserted_blocks = 0
    inserted_courses = 0

    for prog in ARTS_PROGRAMS:
        # ── Upsert program ──────────────────────────────────────────
        prog_data = {
            "program_key":  prog["program_key"],
            "name":         prog["name"],
            "faculty":      prog.get("faculty", "Faculty of Arts"),
            "program_type": prog["program_type"],
            "total_credits": prog.get("total_credits") or 0,
            "description":  prog.get("description"),
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
            # Build constraint_notes: merge scraped constraint_notes + legacy notes
            constraint_notes = block.get("constraint_notes") or block.get("notes") or ""

            block_data = {
                "program_id":       prog_id,
                "block_key":        block.get("block_key", f"block_{i}"),
                "title":            block.get("title", ""),
                # New fields
                "block_type":       block.get("block_type", "choose_credits"),
                "group_name":       block.get("group_name"),
                "courses_needed":   block.get("courses_needed"),
                "constraint_notes": constraint_notes,
                # Legacy / existing fields
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
                # Infer is_required from block_type if not explicitly set
                is_required = course.get("is_required", False)
                if block.get("block_type") == "required":
                    is_required = True

                courses_batch.append({
                    "block_id":           block_id,
                    "subject":            course.get("subject", ""),
                    "catalog":            course.get("catalog"),
                    "title":              course.get("title", ""),
                    "credits":            course.get("credits", 3),
                    "is_required":        is_required,
                    "choose_from_group":  course.get("choose_from_group"),
                    "choose_n_credits":   course.get("choose_n_credits"),
                    "notes":              course.get("notes"),
                    "recommended":        course.get("recommended", False),
                    "recommendation_reason": course.get("recommendation_reason"),
                    "sort_order":         j,
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
    import os
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
    from api.utils.supabase_client import get_supabase
    supabase = get_supabase()
    stats = seed_degree_requirements(supabase)
    print(f"Seeded: {stats['programs']} programs, {stats['blocks']} blocks, {stats['courses']} courses")
