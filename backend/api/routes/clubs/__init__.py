"""
backend/api/routes/clubs/ — Clubs feature.

Split from a single 2000+ line clubs.py into one module per sub-feature
(see docs/adr/0001-incremental-test-first-refactor.md). Every module below
decorates the SAME shared router (see _router.py) directly — no nested
include_router() — so the public API surface (URL paths, prefix, tags) is
unchanged from the original single-file version.

Domain vocabulary (Club, Manager, Owner, Subscription, Calendar Sync, ...)
is defined in CONTEXT.md at the repo root.
"""
from ._router import router
from . import (  # noqa: F401 — imported for their route-registration side effect
    discovery,
    membership,
    members,
    events,
    announcements,
    subscriptions,
    managers,
    submissions,
    activity,
    translation,
)
from .cron import run_stale_club_cleanup_cron  # noqa: F401 — re-exported for notifications.py

__all__ = ["router", "run_stale_club_cleanup_cron"]
