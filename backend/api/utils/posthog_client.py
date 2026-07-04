"""
PostHog analytics client — singleton wrapper.

Initialised lazily on first use so a missing key never crashes startup.
All capture calls are fire-and-forget (PostHog SDK queues internally).
"""
from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)

_client = None
_initialised = False


def _get_client():
    global _client, _initialised
    if _initialised:
        return _client

    _initialised = True
    try:
        from api.config import settings
        if not settings.POSTHOG_API_KEY:
            logger.debug("PostHog disabled — POSTHOG_API_KEY not set")
            return None

        import posthog
        posthog.api_key = settings.POSTHOG_API_KEY
        posthog.host = settings.POSTHOG_HOST
        # Disable the library's own exception logging to keep our logs clean.
        posthog.on_error = lambda e, _items: logger.debug("PostHog error: %s", e)
        _client = posthog
        logger.info("PostHog initialised (host=%s)", settings.POSTHOG_HOST)
    except Exception as exc:
        logger.warning("PostHog init failed: %s", exc)

    return _client


def capture(distinct_id: str, event: str, properties: dict[str, Any] | None = None) -> None:
    """Capture a server-side event. Silently no-ops if PostHog is disabled."""
    client = _get_client()
    if client is None:
        return
    try:
        # posthog-python 6+ changed capture() to capture(event, *, distinct_id=, properties=).
        client.capture(event, distinct_id=distinct_id, properties=properties or {})
    except Exception as exc:
        logger.debug("PostHog capture failed: %s", exc)


def shutdown() -> None:
    """Flush queued events synchronously (call on app shutdown)."""
    client = _get_client()
    if client is None:
        return
    try:
        client.shutdown()
    except Exception as exc:
        logger.debug("PostHog shutdown failed: %s", exc)
