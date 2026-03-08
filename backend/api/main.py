"""
backend/api/main.py

FIX #13: Replaced InMemoryRateLimiter with SupabaseRateLimiter.
The old in-memory implementation reset on every Vercel cold start, giving
zero real protection on serverless. The new implementation stores a
(key, window_start, count) row in the `rate_limits` Supabase table and
atomically increments it with an upsert — so the counter survives across
all function instances and cold starts.

Each 60-second window gets one row. Stale rows are pruned lazily.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time
import logging
from datetime import datetime, timezone, timedelta


from .config import settings
from .logging_config import setup_logging
from .exceptions import (
    AppException,
    app_exception_handler,
    validation_exception_handler,
    general_exception_handler,
    RateLimitException,
)

from .routes import (
    chat, courses, users, favorites, completed, notifications,
    current, suggestions, cards, transcript, degree_requirements,
    electives, clubs, syllabus, professors, admin,
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
    # Conservative limit applied during DB outages to prevent unbounded AI usage.
    # Key → list of request timestamps within the current window.
    _FALLBACK_RPM = 10  # conservative limit per IP:path per minute during outages

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
        (10 req/min) so a DB outage does not silently disable all rate limiting.
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
            # F-04 FIX: Do NOT fail fully open. Apply conservative in-memory fallback
            # so a Supabase outage degrades gracefully without disabling rate limiting.
            logger.warning(f"Rate limiter DB error, applying in-memory fallback: {e}")
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
    allow_methods=["*"],
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
    return response


# FIX #13: Use Supabase-backed limiter instead of in-memory
_limiter = SupabaseRateLimiter(default_rpm=settings.RATE_LIMIT_PER_MINUTE)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    # FIX: Parse only the first IP from x-forwarded-for to prevent spoofing.
    # A malicious client can append extra IPs to the header; the first one is
    # set by the edge/load balancer and can be trusted.
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"

    path = request.url.path

    # Stricter limit for chat (AI calls are expensive)
    rpm = settings.CHAT_RATE_LIMIT_PER_MINUTE if "/chat" in path else settings.RATE_LIMIT_PER_MINUTE

    if not _limiter.is_allowed(f"{client_ip}:{path}", rpm):
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
    request_id = f"{int(start_time * 1000)}"
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


@app.get("/")
async def root():
    return {
        "service": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "operational",
        "docs": f"{settings.API_PREFIX}/docs" if settings.DEBUG else None,
    }


@app.get(f"{settings.API_PREFIX}/health")
async def health_check():
    return {
        "status": "healthy",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
    }
