"""
Custom exceptions and error handlers

SEC-015: DatabaseException no longer returns raw Supabase/Postgres error strings
         to the client. Internal details are logged server-side only.
SEC-017: UserAlreadyExistsException no longer includes email in response details
         (minor enumeration risk).
"""
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
from enum import Enum
from typing import Optional, Any
import logging

logger = logging.getLogger(__name__)


class ErrorCode(str, Enum):
    """Standardized error codes"""
    # General
    INTERNAL_ERROR = "internal_error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    
    # Authentication
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    INVALID_TOKEN = "invalid_token"
    TOKEN_EXPIRED = "token_expired"
    
    # Users
    USER_NOT_FOUND = "user_not_found"
    USER_ALREADY_EXISTS = "user_already_exists"
    PROFILE_CREATE_FAILED = "profile_create_failed"
    
    # Database
    DATABASE_ERROR = "database_error"
    DATABASE_CONNECTION_ERROR = "database_connection_error"
    
    # Chat
    CHAT_HISTORY_ERROR = "chat_history_error"
    MESSAGE_TOO_LONG = "message_too_long"
    AI_SERVICE_ERROR = "ai_service_error"
    
    # Courses
    COURSE_NOT_FOUND = "course_not_found"
    COURSE_SEARCH_ERROR = "course_search_error"
    
    # Rate Limiting
    RATE_LIMIT_EXCEEDED = "rate_limit_exceeded"


class ErrorResponse(BaseModel):
    """Standardized error response"""
    code: ErrorCode
    message: str
    details: Optional[Any] = None
    request_id: Optional[str] = None


class AppException(HTTPException):
    """Base application exception"""
    def __init__(
        self,
        status_code: int,
        code: ErrorCode,
        message: str,
        details: Optional[Any] = None
    ):
        self.code = code
        self.details = details
        super().__init__(status_code=status_code, detail=message)


# Specific Exceptions
class UserNotFoundException(AppException):
    def __init__(self, user_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code=ErrorCode.USER_NOT_FOUND,
            message=f"User not found",
            details={"user_id": user_id}
        )


# SEC-017: Removed email from response details to prevent enumeration.
# The email is still logged server-side for debugging.
class UserAlreadyExistsException(AppException):
    def __init__(self, email: str = ""):
        if email:
            logger.info(f"Duplicate signup attempt for email: {email}")
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code=ErrorCode.USER_ALREADY_EXISTS,
            message="A user with this email already exists",
            details=None  # SEC-017: Don't include email in response
        )


class UsernameTakenException(AppException):
    """A chosen username collides with an existing account. This is a normal
    user-input conflict (409), NOT a server error — so it is logged at info
    level and never escalates as a DATABASE_ERROR."""
    def __init__(self):
        logger.info("Duplicate signup attempt: username already taken")
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            code=ErrorCode.USER_ALREADY_EXISTS,
            message="That username is already taken. Please choose another.",
            details=None
        )


# SEC-015: DatabaseException no longer sends raw Supabase/Postgres error strings
# to the HTTP client. The raw error is logged server-side for debugging; the
# client only sees the operation name.
#
# BEFORE (leaked internal details):
#   {"details": {"operation": "create_user", "error": "duplicate key value violates
#    unique constraint \"users_email_key\" DETAIL: Key (email)=(x@y.com) already exists."}}
#
# AFTER:
#   {"details": {"operation": "create_user"}}
class DatabaseException(AppException):
    def __init__(self, operation: str, details: Optional[str] = None):
        # Log the full error server-side for debugging
        if details:
            logger.error(f"DatabaseException [{operation}]: {details}")
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code=ErrorCode.DATABASE_ERROR,
            message=f"Database operation failed: {operation}",
            details={"operation": operation}  # SEC-015: Scrubbed — no raw error string
        )



# NOTE: AIServiceException, MessageTooLongException, and RateLimitException
# were removed — they were defined but never raised anywhere in the codebase.
# Chat uses inline HTTPException for message length; main.py returns JSONResponse
# for rate limits; AI errors use anthropic.APIError → HTTPException in chat.py.


# Error Handlers
async def app_exception_handler(request: Request, exc: AppException):
    """Handler for custom application exceptions"""
    logger.error(
        f"AppException: {exc.code} - {exc.detail}",
        extra={
            "code": exc.code,
            "status_code": exc.status_code,
            "path": request.url.path,
            "details": exc.details
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.code,
            "message": exc.detail,
            "details": exc.details
        }
    )


def _json_safe_errors(errors) -> list:
    """
    Strip non-JSON-serializable values out of Pydantic error dicts before
    they go into a JSONResponse.

    A custom @field_validator that raises a plain ValueError (e.g. the
    username/profile_image validators in users.py) makes Pydantic put that
    exception OBJECT — not a string — in each error's ctx.error. FastAPI's
    RequestValidationError.errors() is a plain passthrough (no kwargs to
    ask Pydantic to omit it), so building the response straight from
    exc.errors() crashed JSONResponse.render() with "Object of type
    ValueError is not JSON serializable", turning a clean 422 into an
    unhandled 500. The human-readable text is already in `msg`, so ctx
    (only used for message interpolation) can just be dropped.
    """
    safe = []
    for err in errors:
        if isinstance(err, dict) and "ctx" in err:
            err = {k: v for k, v in err.items() if k != "ctx"}
        safe.append(err)
    return safe


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for Pydantic validation errors"""
    logger.warning(
        f"Validation error on {request.url.path}: {exc.errors()}"
    )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": ErrorCode.VALIDATION_ERROR,
            "message": "Invalid request data",
            "details": _json_safe_errors(exc.errors())
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handler for unexpected exceptions"""
    logger.exception(
        f"Unexpected error on {request.url.path}: {str(exc)}",
        exc_info=exc
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": ErrorCode.INTERNAL_ERROR,
            "message": "An unexpected error occurred",
            "details": None  # Never expose internal error details in production
        }
    )
