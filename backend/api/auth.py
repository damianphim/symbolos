"""
backend/api/auth.py

Reusable FastAPI auth dependency.

FIX F-02: Provides get_current_user_id() — a Depends() callable that
          validates the Bearer JWT on every protected route.

FIX F-03: Provides require_self() — enforces that the authenticated user
          can only operate on their own data (prevents IDOR).

SEC-012: Log only exception type, not full message, to avoid leaking
         internal URLs or partial tokens into Vercel function logs.
"""
import logging
from fastapi import HTTPException, Request, status
from supabase import Client

from .utils.supabase_client import get_supabase, get_user_supabase

logger = logging.getLogger(__name__)


async def get_current_user_id(request: Request) -> str:
    """
    FastAPI dependency: extract and verify the Supabase Bearer token.

    Usage:
        @router.get("/{user_id}")
        async def my_route(
            user_id: str,
            current_user_id: str = Depends(get_current_user_id),
        ):
            require_self(current_user_id, user_id)
            ...
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Empty Bearer token",
        )

    try:
        supabase = get_supabase()
        result = supabase.auth.get_user(token)
        if not result or not result.user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
            )
        return result.user.id
    except HTTPException:
        raise
    except Exception as e:
        # SEC-012: Log only the exception type, not the full message.
        # Supabase SDK exceptions may contain internal URLs, partial tokens,
        # or connection strings that would be visible in Vercel function logs.
        logger.warning(f"Token verification error: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed",
        )


async def get_current_jwt(request: Request) -> str:
    """
    FastAPI dependency: extract and return the raw Bearer JWT.
    Use alongside get_current_user_id when you need both the user ID
    and a user-scoped Supabase client.
    """
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Empty Bearer token")
    return token


async def get_user_db(request: Request) -> Client:
    """
    FastAPI dependency: returns a user-scoped Supabase client.
    Queries through this client enforce Row Level Security.
    """
    jwt = await get_current_jwt(request)
    return get_user_supabase(jwt)


def require_self(current_user_id: str, user_id: str) -> None:
    """
    FIX F-03: Assert the authenticated user is operating on their own data.
    Raises HTTP 403 if the IDs don't match.
    """
    if current_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
        )
