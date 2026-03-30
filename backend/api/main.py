"""
backend/api/main.py

FIX #13: Replaced InMemoryRateLimiter with SupabaseRateLimiter.
SEC-006: Tightened in-memory fallback limit from 10 to 3 rpm (per-instance on serverless).
SEC-009: Removed 'unsafe-inline' from script-src CSP; added frame-ancestors 'none'.
SEC-010: Normalise rate limit path key to prevent bypass via trailing slash/case.
"""
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import uuid
import logging
import base64
import json as _json
from datetime import datetime, timezone, timedelta


from .config import settings
from .logging_config import setup_logging
from .auth import get_current_user_id
from .exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    general_exception_handler,  
)

from .routes import (
    chat, courses, users, favorites, completed, notifications,
    current, suggestions, cards, transcript, degree_requirements,
    electives, clubs, syllabus, professors, admin, newsletters, forum,
    verification,
)

logger = setup_logging()


def _validate_startup():
    """Fail fast if critical configuration is missing or invalid."""
    errors = []

    if not settings.ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is not set")
    elif not settings.ANTHROPIC_API_KEY.startswith("sk-ant-"):
        errors.append("ANTHROPIC_API_KEY has invalid format")

    if not settings.SUPABASE_URL:
        errors.append("SUPABASE_URL is not set")
    elif not settings.SUPABASE_URL.startswith("https://"):
        errors.append("SUPABASE_URL must start with https://")

    if not settings.SUPABASE_SERVICE_KEY:
        errors.append("SUPABASE_SERVICE_KEY is not set")

    if not settings.SUPABASE_ANON_KEY:
        logger.warning(
            "SUPABASE_ANON_KEY is not set — user-scoped queries will fall back to service role key. "
            "Set SUPABASE_ANON_KEY to enable Row Level Security enforcement."
        )

    if errors:
        for err in errors:
            logger.critical(f"STARTUP VALIDATION FAILED: {err}")
        raise RuntimeError(
            "Startup validation failed — fix the errors above before running."
        )

    logger.info("✅ Startup validation passed")


# ── FIX #13: Supabase-backed rate limiter ────────────────────────────────────

class SupabaseRateLimiter:
    """
    Sliding-window rate limiter backed by Supabase (Postgres).

    State is stored in the `rate_limits` table, so it survives serverless
    cold starts and is shared across all function instances.

    Schema (see sql/fix13_rate_limits_table.sql):
        rate_limits(key TEXT, window_start TIMESTAMPTZ, count INT)
        PRIMARY KEY (key, window_start)

    Strategy: 1-minute tumbling window.
      • window_start = current UTC minute truncated to the minute boundary
      • On each request: upsert (key, window_start) with count+1
      • If count after upsert ≥ limit → reject
      • Rows older than _PRUNE_AFTER are deleted lazily (every _PRUNE_EVERY calls)
    """

    _WINDOW_SECONDS = 60
    _PRUNE_AFTER    = timedelta(minutes=10)
    _PRUNE_EVERY    = 500  # prune stale rows once every N is_allowed() calls

    def __init__(self, default_rpm: int = 100):
        self.default_rpm = default_rpm
        self._call_count = 0
        self._fallback_counts: dict = {}  # F-04: in-memory fallback for DB outages

    @staticmethod
    def _window_start() -> str:
        """Current UTC minute boundary as an ISO string Postgres understands."""
        now = datetime.now(timezone.utc)
        truncated = now.replace(second=0, microsecond=0)
        return truncated.isoformat()

    def _get_supabase(self):
        # Import lazily to avoid circular imports and to keep startup fast.
        from .utils.supabase_client import get_supabase
        return get_supabase()

    # ── In-memory fallback (used when Supabase is unavailable) ───────────────
    # SEC-006: Reduced from 10 to 3 rpm. Each Vercel instance gets its own
    # in-memory counter during DB outages. With 10 rpm × 20 instances = 200
    # effective rpm. At 3 rpm × 20 instances = 60 rpm — still usable but much
    # safer for Claude API cost protection.
    _FALLBACK_RPM = 3

    def _fallback_is_allowed(self, key: str) -> bool:
        """Sliding-window in-memory check used when Supabase is unavailable."""
        now = time.time()
        window_start = now - self._WINDOW_SECONDS
        timestamps = self._fallback_counts.get(key, [])
        # Prune old entries
        timestamps = [t for t in timestamps if t > window_start]
        if len(timestamps) >= self._FALLBACK_RPM:
            return False
        timestamps.append(now)
        self._fallback_counts[key] = timestamps
        return True

    def is_allowed(self, key: str, rpm: int | None = None) -> bool:
        """
        Returns True if the request is within the rate limit.
        On Supabase error, applies a conservative in-memory fallback limit
        so a DB outage does not silently disable all rate limiting.
        """
        limit = rpm or self.default_rpm
        window = self._window_start()

        try:
            supabase = self._get_supabase()

            # For true atomicity we call a small Postgres function.
            # If that function doesn't exist yet (not yet deployed), fall back
            # to the two-step approach.
            try:
                result = supabase.rpc(
                    'increment_rate_limit',
                    {'p_key': key, 'p_window': window}
                ).execute()
                new_count = result.data  # function returns the new count integer
            except Exception:
                # Fallback: read + write (slightly less atomic but fine for our
                # traffic levels — duplicate requests within microseconds would
                # both pass, which is acceptable).
                read = (
                    supabase.table('rate_limits')
                    .select('count')
                    .eq('key', key)
                    .eq('window_start', window)
                    .execute()
                )
                if read.data:
                    new_count = read.data[0]['count'] + 1
                    supabase.table('rate_limits').update({
                        'count': new_count,
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                    }).eq('key', key).eq('window_start', window).execute()
                else:
                    new_count = 1
                    supabase.table('rate_limits').insert({
                        'key': key,
                        'window_start': window,
                        'count': 1,
                        'updated_at': datetime.now(timezone.utc).isoformat(),
                    }).execute()

            # Lazy prune
            self._call_count += 1
            if self._call_count % self._PRUNE_EVERY == 0:
                self._prune(supabase)

            return new_count < limit

        except Exception as e:
            logger.error(
                f"[SECURITY] Rate limiter DB unavailable — falling back to in-memory "
                f"(limit={self._FALLBACK_RPM} rpm). Multi-instance protection is "
                f"degraded until Supabase recovers. Error: {type(e).__name__}"
            )
            return self._fallback_is_allowed(key)

    def _prune(self, supabase) -> None:
        """Delete rate_limit rows older than _PRUNE_AFTER. Best-effort."""
        try:
            cutoff = (datetime.now(timezone.utc) - self._PRUNE_AFTER).isoformat()
            supabase.table('rate_limits').delete().lt('window_start', cutoff).execute()
        except Exception as e:
            logger.debug(f"Rate limit prune failed (non-critical): {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    _validate_startup()
    logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
    yield
    logger.info("Shutting down…")


app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url=f"{settings.API_PREFIX}/docs" if settings.DEBUG else None,
    redoc_url=f"{settings.API_PREFIX}/redoc" if settings.DEBUG else None,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID", "X-Cron-Secret"],
    expose_headers=["X-Process-Time", "X-Request-ID"],
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """Inject standard security headers on every response."""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    # SEC-009: Removed 'unsafe-inline' from script-src. The React/Vite frontend
    # doesn't need inline scripts. Added frame-ancestors 'none' for clickjacking
    # protection (stronger than X-Frame-Options in modern browsers).
    # NOTE: If the Vite build injects inline <script> tags and this breaks,
    # revert to "'self' 'unsafe-inline'" and implement nonce-based CSP next sprint.
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "connect-src 'self' https://*.supabase.co https://ai-advisor-backend-seven.vercel.app; "
        "img-src 'self' data: blob:; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "frame-ancestors 'none';"
    )
    return response


# FIX #13: Use Supabase-backed limiter instead of in-memory
_limiter = SupabaseRateLimiter(default_rpm=settings.RATE_LIMIT_PER_MINUTE)


def _get_client_ip(request: Request) -> str:
    """
    Extract the real client IP from the request.

    Vercel (and most reverse proxies) append the connecting IP to the
    X-Forwarded-For header, making it the LAST entry.  The earlier entries
    are supplied by the client and therefore untrusted — using the first
    entry allows an attacker to bypass IP-based rate limits by injecting a
    fake IP at the front of the header (e.g. X-Forwarded-For: 1.2.3.4,
    real-ip).

    Strategy:
      1. Use the LAST value in X-Forwarded-For (appended by the edge).
      2. Fall back to the WSGI/ASGI remote address if the header is absent.
    """
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # The rightmost IP is the one appended by the trusted infrastructure
        parts = [p.strip() for p in forwarded_for.split(",") if p.strip()]
        return parts[-1] if parts else "unknown"
    return request.client.host if request.client else "unknown"


def _get_user_id_from_token(request: Request) -> str | None:
    """
    Extract the user ID (sub claim) from the Bearer JWT without full verification.
    Auth middleware handles cryptographic verification — this is used ONLY to key
    per-user rate limit buckets so a shared corporate IP doesn't exhaust one limit
    for all users, and so a single user can't bypass limits by rotating IPs.
    """
    auth = request.headers.get("authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth[7:]
    try:
        parts = token.split(".")
        if len(parts) < 2:
            return None
        # JWT payload is base64url-encoded — add padding if needed
        payload_b64 = parts[1]
        rem = len(payload_b64) % 4
        if rem:
            payload_b64 += "=" * (4 - rem)
        payload = _json.loads(base64.urlsafe_b64decode(payload_b64))
        sub = payload.get("sub")
        return str(sub) if sub else None
    except Exception:
        return None


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_ip = _get_client_ip(request)

    # SEC-010: Normalise path to prevent bypass via trailing slash or case variation.
    # Without this, /api/chat/send and /api/chat/send/ and /api/Chat/send
    # would each get separate rate limit buckets.
    raw_path = request.url.path
    normalised_path = raw_path.rstrip("/").lower()

    # Stricter limit for chat (AI calls are expensive)
    rpm = settings.CHAT_RATE_LIMIT_PER_MINUTE if "/chat" in normalised_path else settings.RATE_LIMIT_PER_MINUTE

    # ── IP-based check (covers unauthenticated requests + shared-IP DoS) ──────
    if not _limiter.is_allowed(f"ip:{client_ip}:{normalised_path}", rpm):
        return JSONResponse(
            status_code=429,
            content={
                "detail": "Too many requests. Please try again later.",
                "details": {"retry_after": 60},
            },
        )

    # ── Per-user check (prevents single user from exhausting the IP bucket) ───
    # Authenticated routes only — unauthenticated requests have no user ID.
    user_id = _get_user_id_from_token(request)
    if user_id:
        user_rpm = max(rpm // 2, 10)  # per-user limit is half the IP limit, min 10
        if not _limiter.is_allowed(f"user:{user_id}:{normalised_path}", user_rpm):
            return JSONResponse(
                status_code=429,
                content={
                    "detail": "Too many requests. Please try again later.",
                    "details": {"retry_after": 60},
                },
            )

    return await call_next(request)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = request_id
    return response


# Exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Routers
app.include_router(admin.router,               prefix=f"{settings.API_PREFIX}/admin",               tags=["Admin"])
app.include_router(chat.router,                prefix=f"{settings.API_PREFIX}/chat",                tags=["Chat"])
app.include_router(courses.router,             prefix=f"{settings.API_PREFIX}/courses",             tags=["Courses"])
app.include_router(users.router,               prefix=f"{settings.API_PREFIX}/users",               tags=["Users"])
app.include_router(favorites.router,           prefix=f"{settings.API_PREFIX}/favorites",           tags=["Favorites"])
app.include_router(completed.router,           prefix=f"{settings.API_PREFIX}/completed",           tags=["Completed"])
app.include_router(notifications.router,       prefix=f"{settings.API_PREFIX}/notifications",       tags=["Notifications"])
app.include_router(current.router,             prefix=f"{settings.API_PREFIX}/current",             tags=["Current Courses"])
app.include_router(suggestions.router,         prefix=f"{settings.API_PREFIX}/suggestions",         tags=["Suggestions"])
app.include_router(cards.router,               prefix=f"{settings.API_PREFIX}/cards",               tags=["Cards"])
app.include_router(transcript.router,          prefix=f"{settings.API_PREFIX}/transcript",          tags=["Transcript"])
app.include_router(degree_requirements.router, prefix=f"{settings.API_PREFIX}/degree-requirements", tags=["Degree Requirements"])
app.include_router(electives.router,           prefix=f"{settings.API_PREFIX}/electives",           tags=["Electives"])
app.include_router(clubs.router,               prefix=f"{settings.API_PREFIX}/clubs",               tags=["Clubs"])
app.include_router(syllabus.router,            prefix=f"{settings.API_PREFIX}/syllabus",            tags=["Syllabus"])
app.include_router(professors.router,          prefix=f"{settings.API_PREFIX}/professors",          tags=["Professors"])
app.include_router(newsletters.router,         prefix=f"{settings.API_PREFIX}/newsletters",         tags=["Newsletters"])
app.include_router(forum.router,               prefix=f"{settings.API_PREFIX}/forum",               tags=["Forum"])
app.include_router(verification.router,        prefix=f"{settings.API_PREFIX}/auth",                tags=["Auth"])


@app.get("/")
async def root():
    # SEC-09: Mirror health endpoint — don't expose version in production.
    response = {
        "service": settings.API_TITLE,
        "status": "operational",
        "docs": f"{settings.API_PREFIX}/docs" if settings.DEBUG else None,
    }
    if settings.DEBUG:
        response["version"] = settings.API_VERSION
    return response


@app.get(f"{settings.API_PREFIX}/health")
async def health_check():
    # SEC-05: Don't expose version string in production — it aids targeted exploit research.
    response = {"status": "healthy"}
    if settings.DEBUG:
        response["version"] = settings.API_VERSION
    return response


@app.get(f"{settings.API_PREFIX}/auth/flags")
async def auth_flags(current_user_id: str = Depends(get_current_user_id)):
    """Return auth flags for the current user (admin status, McGill email)."""
    from .utils.supabase_client import get_supabase
    admin_emails = set(e.strip().lower() for e in settings.ADMIN_EMAILS.split(",") if e.strip())
    mcgill_domains = ("@mcgill.ca", "@mail.mcgill.ca")
    try:
        sb = get_supabase()
        resp = sb.table("users").select("email").eq("id", current_user_id).single().execute()
        email = (resp.data or {}).get("email", "").lower()
        is_admin = email in admin_emails
        is_mcgill = any(email.endswith(d) for d in mcgill_domains) or is_admin
        return {"is_admin": is_admin, "is_mcgill_email": is_mcgill}
    except Exception:
        return {"is_admin": False, "is_mcgill_email": False}
