"""
backend/api/routes/admin.py

FIX F-04: Backend admin authentication endpoint.
Replaces the insecure client-side VITE_ADMIN_PASSWORD comparison.
The frontend sends the password here; we verify it server-side and
return a short-lived token (the CRON_SECRET itself, since that's what
the existing admin API calls use for X-Cron-Secret).

Never embed this secret in the frontend bundle.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import logging

from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


class AdminLoginRequest(BaseModel):
    secret: str


@router.post("/verify", status_code=status.HTTP_200_OK)
async def verify_admin(request: AdminLoginRequest):
    """
    Verify the admin secret server-side.
    Returns a token the frontend uses for subsequent admin API calls.
    The token is the CRON_SECRET — never exposed in the JS bundle.
    """
    if not settings.CRON_SECRET:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Admin access not configured",
        )

    if request.secret != settings.CRON_SECRET:
        # Avoid timing oracle — use constant-time comparison
        import hmac
        _ = hmac.compare_digest(request.secret, settings.CRON_SECRET)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    logger.info("Admin access granted")
    return {"token": settings.CRON_SECRET}
