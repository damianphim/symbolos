"""
backend/api/logging_config.py

"""
import logging
import logging.handlers
import sys
import os
import json
from datetime import datetime, timezone

from .config import settings


class JSONFormatter(logging.Formatter):
    """Structured JSON formatter for production log aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Attach request_id if present
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id

        # Attach extra fields passed via `extra={...}`
        for key in ("code", "status_code", "path", "details"):
            if hasattr(record, key):
                log_entry[key] = getattr(record, key)

        # Attach exception info
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, default=str)


class _RemoteHTTPHandler(logging.Handler):
    """Best-effort HTTP log shipper for Better Stack / Logtail / Axiom.

    Ships each record as a JSON line to LOG_SHIP_URL with an optional
    bearer token. Fire-and-forget on a daemon thread pool so logging never
    blocks the request path; drops logs silently if the sink is down (we
    still have the console/Vercel logs as the source of truth).
    """
    def __init__(self, url: str, token: str | None, level=logging.INFO):
        super().__init__(level)
        self._url = url
        self._token = token
        self._formatter = JSONFormatter()
        import concurrent.futures
        # Tiny pool — log shipping is I/O bound and we cap concurrency so a
        # slow sink can't spawn unbounded threads under load.
        self._pool = concurrent.futures.ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="logship"
        )

    def emit(self, record: logging.LogRecord) -> None:
        try:
            payload = self._formatter.format(record)
            self._pool.submit(self._ship, payload)
        except Exception:
            pass  # never let logging raise

    def _ship(self, payload: str) -> None:
        try:
            import httpx
            headers = {"Content-Type": "application/json"}
            if self._token:
                headers["Authorization"] = f"Bearer {self._token}"
            httpx.post(self._url, content=payload, headers=headers, timeout=5)
        except Exception:
            pass  # sink down — drop silently, console log is the source of truth


def _build_remote_handler(log_level):
    """Construct the remote log handler if configured, else None."""
    # Better Stack / Logtail style: token + their ingest URL.
    token = os.getenv("LOGTAIL_TOKEN", "").strip()
    url = os.getenv("LOG_SHIP_URL", "").strip()
    if token and not url:
        # Default Better Stack ingest endpoint.
        url = "https://in.logs.betterstack.com"
    if not url:
        return None
    try:
        h = _RemoteHTTPHandler(url, token or None, level=log_level)
        h.setLevel(log_level)
        return h
    except Exception:
        return None


def setup_logging() -> logging.Logger:
    """Configure application logging with console + optional file output."""

    # ── Determine log level ──────────────────────────────────────────────
    log_level_name = os.getenv("LOG_LEVEL", "DEBUG" if settings.DEBUG else "INFO")
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)

    # ── Console handler (always active) ──────────────────────────────────
    if settings.ENVIRONMENT == "production":
        console_formatter = JSONFormatter()
    else:
        console_formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(log_level)

    # ── File handler with rotation (if LOG_FILE is set) ──────────────────
    log_file = os.getenv("LOG_FILE")  # e.g. "logs/app.log"
    file_handler = None

    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

        file_handler = logging.handlers.RotatingFileHandler(
            filename=log_file,
            maxBytes=10 * 1024 * 1024,  # 10 MB per file
            backupCount=5,              # keep 5 rotated files
            encoding="utf-8",
        )
        file_handler.setFormatter(JSONFormatter())  # always JSON on disk
        file_handler.setLevel(log_level)

    # ── Remote log sink for retention (Better Stack / Logtail / Axiom) ───
    # Vercel function logs evaporate after ~30 days. If LOGTAIL_TOKEN (or a
    # generic LOG_SHIP_URL) is set, ship JSON logs there too so we can grep
    # months back when debugging. Buffered + non-blocking so a slow sink
    # never stalls a request. No-op when unset.
    remote_handler = _build_remote_handler(log_level)

    # ── Root logger ──────────────────────────────────────────────────────
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    # Remove any previously attached handlers (avoid duplicates on reload)
    root_logger.handlers.clear()
    root_logger.addHandler(console_handler)
    if file_handler:
        root_logger.addHandler(file_handler)
    if remote_handler:
        root_logger.addHandler(remote_handler)

    # ── Third-party noise reduction ──────────────────────────────────────
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    root_logger.info(
        "Logging configured — level=%s, file=%s, remote=%s, format=%s",
        log_level_name,
        log_file or "(console only)",
        "on" if remote_handler else "off",
        "json" if settings.ENVIRONMENT == "production" else "text",
    )

    return root_logger