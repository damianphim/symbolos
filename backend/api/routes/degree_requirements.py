"""
backend/api/routes/degree_requirements.py

Endpoints for degree requirement programs, blocks, and courses.

Fixes applied:
  #1  – get_program: non-HTTP exceptions (e.g. DB timeout) no longer misreported
        as 404; only a genuine "not found" result raises 404.
  #2  – /seed: protected by X-Cron-Secret header (same pattern as suggestions.py
        and notifications.py) so random internet callers can't trigger a re-seed.
  #3  – list_programs: select() limited to display columns only (egress fix,
        mirrors the fix already applied to search_courses / get_course).
  #4  – get_recommended_courses: HTTPException (404) is now re-raised correctly
        instead of being swallowed into a 500 by the outer except clause.
  #5  – get_program: all three DB calls consolidated into a single _run()
        closure so with_retry wraps the whole fetch atomically.
  #6  – Logging added throughout (mirrors supabase_client.py / suggestions.py).
  #7  – program_type docstring updated to reflect real seed values.
"""

import logging
import traceback
from typing import Optional

import hmac
from fastapi import APIRouter, HTTPException, Query, Request, Depends

from ..utils.supabase_client import get_supabase, with_retry
from ..config import settings
from ..auth import get_current_user_id

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/programs")
def list_programs(
    faculty: Optional[str] = Query(None),
    program_type: Optional[str] = Query(None),
    _: str = Depends(get_current_user_id),
):
    """List all degree programs, optionally filtered.

    Returns a lightweight projection (no description/ecalendar_url) to
    reduce egress on list views.
    """
    def _run():
        supabase = get_supabase()
        q = supabase.table("degree_programs").select(
            "id, program_key, name, faculty, program_type, total_credits"
        )
        if faculty:
            q = q.eq("faculty", faculty)
        if program_type:
            q = q.eq("program_type", program_type)
        return q.order("name").execute().data

    try:
        return with_retry("list_programs", _run)
    except Exception:
        logger.error(f"list_programs error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.get("/programs/{program_key}")
def get_program(program_key: str, _: str = Depends(get_current_user_id)):
    """Get full program details including all requirement blocks and courses.

    All three DB calls are wrapped in a single with_retry closure so that
    a transient disconnect retries the whole fetch from scratch on a fresh
    client, rather than potentially mixing results from different connections.
    """
    def _run():
        supabase = get_supabase()

        # 1 — Fetch program row
        prog_result = (
            supabase.table("degree_programs")
            .select("*")
            .eq("program_key", program_key)
            .limit(1)
            .execute()
        )
        if not prog_result.data:
            raise HTTPException(status_code=404, detail="Program not found")
        program = prog_result.data[0]
        prog_id = program["id"]

        # 2 — Fetch requirement blocks
        blocks = (
            supabase.table("requirement_blocks")
            .select("*")
            .eq("program_id", prog_id)
            .order("sort_order")
            .execute()
            .data
        )

        # 3 — Fetch all courses for every block in one query
        block_ids = [b["id"] for b in blocks]
        if block_ids:
            courses_data = (
                supabase.table("requirement_courses")
                .select(
                    "id, block_id, subject, catalog, title, credits, "
                    "is_required, recommended, recommendation_reason, "
                    "choose_from_group, choose_n_credits, notes, sort_order"
                )
                .in_("block_id", block_ids)
                .order("sort_order")
                .execute()
                .data
            )
            courses_by_block: dict = {}
            for c in courses_data:
                courses_by_block.setdefault(c["block_id"], []).append(c)
        else:
            courses_by_block = {}

        # Attach courses to blocks
        for block in blocks:
            block["courses"] = courses_by_block.get(block["id"], [])

        program["blocks"] = blocks
        return program

    try:
        return with_retry("get_program", _run)
    except HTTPException:
        raise
    except Exception:
        logger.error(f"get_program({program_key}) error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.get("/programs/{program_key}/recommended")
def get_recommended_courses(program_key: str, _: str = Depends(get_current_user_id)):
    """Return only recommended courses for a program with reasons."""

    def _run():
        supabase = get_supabase()
        prog_result = (
            supabase.table("degree_programs")
            .select("id")
            .eq("program_key", program_key)
            .limit(1)
            .execute()
        )
        if not prog_result.data:
            raise HTTPException(status_code=404, detail="Program not found")
        prog_id = prog_result.data[0]["id"]

        blocks_result = (
            supabase.table("requirement_blocks")
            .select("id, title")          # column is "title", not "name"
            .eq("program_id", prog_id)
            .execute()
        )
        block_ids = [b["id"] for b in blocks_result.data]
        if not block_ids:
            return []

        courses_result = (
            supabase.table("requirement_courses")
            .select("subject, catalog, title, credits, recommendation_reason, block_id")
            .in_("block_id", block_ids)
            .eq("recommended", True)
            .execute()
        )
        block_names = {b["id"]: b["title"] for b in blocks_result.data}  # was b["name"]
        return [
            {**c, "block_name": block_names.get(c["block_id"], "")}
            for c in courses_result.data
        ]

    try:
        return with_retry("get_recommended_courses", _run)
    except HTTPException:
        raise
    except Exception:
        logger.error(f"get_recommended_courses({program_key}) error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")


@router.post("/seed")
def seed_requirements(
    request: Request,
    faculty: Optional[str] = Query(
        None,
        description=(
            "arts | science | engineering | arts_science | "
            "management | education | environment | law | aes | dentistry | music | all (default: all)"
        ),
    ),
):
    """
    Seed degree requirement programs into the database.
    FIX F-05: Protected by CRON_SECRET — only authorised callers may trigger a re-seed.
    """
    # FIX F-05: Require CRON_SECRET to prevent public re-seeding
    if not settings.CRON_SECRET:
        raise HTTPException(status_code=500, detail="CRON_SECRET not configured")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.removeprefix("Bearer ").strip()
    if not hmac.compare_digest(token or "", settings.CRON_SECRET):
        raise HTTPException(status_code=401, detail="Unauthorized")

    def _run():
        supabase = get_supabase()
        results = {}

        run_arts        = faculty in (None, "all", "arts")
        run_sci         = faculty in (None, "all", "science")
        run_eng         = faculty in (None, "all", "engineering")
        run_arts_sci    = faculty in (None, "all", "arts_science")
        run_management  = faculty in (None, "all", "management")
        run_education   = faculty in (None, "all", "education")
        run_environment = faculty in (None, "all", "environment")
        run_law         = faculty in (None, "all", "law")
        run_aes         = faculty in (None, "all", "aes", "agricultural_environmental_sciences")
        run_dentistry   = faculty in (None, "all", "dentistry", "dental_medicine")
        run_medicine    = faculty in (None, "all", "medicine", "medicine_health_sciences")
        run_music       = faculty in (None, "all", "music", "schulich", "schulich_music")
        run_nursing     = faculty in (None, "all", "nursing", "ingram_nursing")
        run_spot        = faculty in (None, "all", "spot", "physical_occupational_therapy", "rehabilitation_science")

        if run_arts:
            from ..seeds.arts_degree_requirements import seed_degree_requirements as seed_arts
            results["arts"] = seed_arts(supabase)

        if run_eng:
            from ..seeds.engineering_degree_requirements import seed_degree_requirements as seed_eng
            results["engineering"] = seed_eng(supabase)

        if run_sci:
            from ..seeds.science_degree_requirements import seed_degree_requirements as seed_sci
            results["science"] = seed_sci(supabase)

        if run_arts_sci:
            from ..seeds.arts_science_degree_requirements import seed_degree_requirements as seed_basc
            results["arts_science"] = seed_basc(supabase)

        if run_management:
            from ..seeds.management_degree_requirements import seed_degree_requirements as seed_mgmt
            results["management"] = seed_mgmt(supabase)

        if run_education:
            from ..seeds.education_degree_requirements import seed_degree_requirements as seed_edu
            results["education"] = seed_edu(supabase)

        if run_environment:
            from ..seeds.environment_degree_requirements import seed_degree_requirements as seed_env
            results["environment"] = seed_env(supabase)

        if run_law:
            from ..seeds.law_degree_requirements import seed_degree_requirements as seed_law
            results["law"] = seed_law(supabase)

        if run_aes:
            from ..seeds.aes_degree_requirements import seed_degree_requirements as seed_aes
            results["aes"] = seed_aes(supabase)

        if run_dentistry:
            from ..seeds.dentistry_degree_requirements import seed_degree_requirements as seed_dentistry
            results["dentistry"] = seed_dentistry(supabase)

        if run_medicine:
            from ..seeds.medicine_degree_requirements import seed_degree_requirements as seed_medicine
            results["medicine"] = seed_medicine(supabase)

        if run_music:
            from ..seeds.music_degree_requirements import seed_degree_requirements as seed_music
            results["music"] = seed_music(supabase)

        if run_nursing:
            from ..seeds.nursing_degree_requirements import seed_degree_requirements as seed_nursing
            results["nursing"] = seed_nursing(supabase)

        if run_spot:
            from ..seeds.spot_degree_requirements import seed_degree_requirements as seed_spot
            results["spot"] = seed_spot(supabase)

        # Surface any per-faculty errors collected by seeds that support it
        # (e.g. education seed returns {"programs": N, "blocks": N, "errors": [...]})
        errors = {
            fac: res.get("errors")
            for fac, res in results.items()
            if isinstance(res, dict) and res.get("errors")
        }
        if errors:
            logger.warning(f"seed_requirements completed with errors: {errors}")

        return {"success": True, "seeded": results, **({"errors": errors} if errors else {})}

    try:
        return with_retry("seed_requirements", _run)
    except HTTPException:
        raise
    except Exception:
        logger.error(f"seed_requirements error:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="An internal error occurred. Please try again.")
