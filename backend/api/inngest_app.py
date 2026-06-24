"""
Inngest background job definitions.

Functions registered here are triggered by events sent from the transcript
and syllabus upload endpoints. Inngest calls back our /api/inngest endpoint
on Vercel once per job, so each job runs in its own serverless invocation
with no timeout on the HTTP request that originated the upload.

Env vars required:
  INNGEST_EVENT_KEY   — from Inngest dashboard (used to send events)
  INNGEST_SIGNING_KEY — from Inngest dashboard (used to verify Inngest callbacks)
"""
from __future__ import annotations

import logging
import os

import inngest

from .config import settings

logger = logging.getLogger(__name__)

inngest_client = inngest.Inngest(
    app_id="ai-advisor",
    event_key=os.getenv("INNGEST_EVENT_KEY", ""),
    signing_key=os.getenv("INNGEST_SIGNING_KEY", ""),
    is_production=settings.ENVIRONMENT == "production",
    logger=logger,
)


# ── Transcript processing ─────────────────────────────────────────────────────

@inngest_client.create_function(
    fn_id="process-transcript",
    trigger=inngest.TriggerEvent(event="transcript/process"),
    retries=2,
)
async def process_transcript(ctx: inngest.Context, step: inngest.Step) -> dict:
    data         = ctx.event.data
    job_id       = data["job_id"]
    user_id      = data["user_id"]
    storage_path = data["storage_path"]
    dry_run      = data.get("dry_run", False)

    from .utils.jobs import update_job
    from .utils.supabase_client import get_supabase

    update_job(job_id, "processing")

    try:
        # Late imports to avoid circular dependency at module load time
        from .routes.transcript import (
            extract_transcript_data,
            _persist_transcript_data,
            normalize_course_code,
            _dedupe_extracted,
        )

        # Download PDF from Supabase Storage
        pdf_bytes: bytes = get_supabase().storage.from_("job-uploads").download(storage_path)

        # Claude extraction
        extracted = await extract_transcript_data(pdf_bytes)

        # Normalize course codes
        for course in extracted.get("completed_courses", []):
            if course.get("course_code"):
                course["course_code"] = normalize_course_code(course["course_code"])
        for course in extracted.get("current_courses", []):
            if course.get("course_code"):
                course["course_code"] = normalize_course_code(course["course_code"])
        for course in (extracted.get("student_info") or {}).get("advanced_standing", []):
            if course.get("course_code"):
                course["course_code"] = normalize_course_code(course["course_code"])

        _dedupe_extracted(extracted)

        if dry_run:
            result = {"parsed": extracted, "saved": False}
        else:
            persisted = _persist_transcript_data(user_id, extracted)
            result = {"results": persisted, "saved": True}

        update_job(job_id, "done", result=result)
        return result

    except Exception as exc:
        logger.exception("Transcript job %s failed: %s", job_id, exc)
        update_job(job_id, "failed", error=str(exc))
        raise

    finally:
        # Clean up the temp PDF regardless of success/failure
        try:
            get_supabase().storage.from_("job-uploads").remove([storage_path])
        except Exception:
            pass


# ── Syllabus processing ───────────────────────────────────────────────────────

@inngest_client.create_function(
    fn_id="process-syllabus",
    trigger=inngest.TriggerEvent(event="syllabus/process"),
    retries=2,
)
async def process_syllabus(ctx: inngest.Context, step: inngest.Step) -> dict:
    data          = ctx.event.data
    job_id        = data["job_id"]
    user_id       = data["user_id"]
    storage_paths = data["storage_paths"]   # list of paths, one per file
    filenames     = data["filenames"]
    dry_run       = data.get("dry_run", False)

    from .utils.jobs import update_job
    from .utils.supabase_client import get_supabase

    update_job(job_id, "processing")

    try:
        from .routes.syllabus import _extract_syllabus_data, _persist_syllabus_result
        import json

        sb = get_supabase()
        all_results = []

        for storage_path, filename in zip(storage_paths, filenames):
            try:
                pdf_bytes: bytes = sb.storage.from_("job-uploads").download(storage_path)
                extracted = await _extract_syllabus_data(pdf_bytes)

                if dry_run:
                    all_results.append({
                        "filename": filename,
                        "success": True,
                        "parsed": extracted,
                        "saved": False,
                    })
                else:
                    file_result = _persist_syllabus_result(user_id, filename, extracted, sb)
                    all_results.append(file_result)

            except json.JSONDecodeError:
                all_results.append({
                    "filename": filename,
                    "success": False,
                    "error": "Failed to parse syllabus — Claude returned invalid data.",
                })
            except Exception as exc:
                logger.exception("Syllabus processing failed for %s: %s", filename, exc)
                all_results.append({
                    "filename": filename,
                    "success": False,
                    "error": "Extraction failed. Please try again.",
                })
            finally:
                try:
                    sb.storage.from_("job-uploads").remove([storage_path])
                except Exception:
                    pass

        result = {
            "results": all_results,
            "total_files": len(storage_paths),
            "total_events_added": sum(r.get("calendar_events_added", 0) for r in all_results if r.get("success")),
            "total_courses_updated": sum(1 for r in all_results if r.get("current_course_updated")),
            "saved": not dry_run,
        }
        update_job(job_id, "done", result=result)
        return result

    except Exception as exc:
        logger.exception("Syllabus job %s failed: %s", job_id, exc)
        update_job(job_id, "failed", error=str(exc))
        raise


# All functions to register with FastAPI
INNGEST_FUNCTIONS = [process_transcript, process_syllabus]
