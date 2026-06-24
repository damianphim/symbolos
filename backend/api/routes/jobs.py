"""
GET /api/jobs/{job_id} — background job status polling.

Used by the frontend to poll transcript and syllabus processing jobs
after receiving a 202 from the upload endpoints.
"""
from fastapi import APIRouter, HTTPException, Depends

from ..auth import get_current_user_id
from ..utils.jobs import get_job

router = APIRouter()


@router.get("/{job_id}")
async def get_job_status(
    job_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    job = get_job(job_id, current_user_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
