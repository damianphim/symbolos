"""
Academic-year auto-advance.

A student's `year` (0=U0 … 3=U3) is set once at signup. Without this, it
would silently go stale — a U1 stays "U1" forever. This advances every
student's year of study by one each September (the start of McGill's
academic year), using `year_anchor` to avoid double-counting and to catch
up dormant accounts.

Academic year = the Fall calendar year. Sept 2025–Aug 2026 → 2025.

Called once a day from the notifications cron; it's a no-op outside the
September rollover because `current_academic_year()` only ticks up then.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone

from .supabase_client import get_supabase

logger = logging.getLogger(__name__)

# Don't advance past this. McGill undergrad is U0–U3; allow a little slack
# for U4/U5 (extended/part-time) but stop so graduated/dormant accounts
# don't run off to "U9".
_MAX_YEAR = 5


def current_academic_year(now: datetime | None = None) -> int:
    """Fall calendar year of the current academic year."""
    now = now or datetime.now(timezone.utc)
    return now.year if now.month >= 9 else now.year - 1


def run_academic_year_advance_cron() -> dict:
    """Advance year of study for everyone whose anchor is behind the current
    academic year. Returns a small summary for the cron log."""
    cay = current_academic_year()
    sb = get_supabase()

    advanced = 0
    skipped = 0
    try:
        # Pull only rows that can possibly advance: a real year, an anchor
        # behind the current academic year, and below the cap.
        rows = (
            sb.table("users")
            .select("id, year, year_anchor")
            .not_.is_("year", "null")
            .lt("year_anchor", cay)
            .lt("year", _MAX_YEAR)
            .execute()
        ).data or []
    except Exception as exc:
        # Older DB without year_anchor, or transient error — log and bail.
        logger.warning("academic-year advance query failed: %s", type(exc).__name__)
        return {"advanced": 0, "academic_year": cay, "error": type(exc).__name__}

    for r in rows:
        try:
            anchor = r.get("year_anchor")
            year = r.get("year")
            if anchor is None or year is None:
                skipped += 1
                continue
            elapsed = cay - int(anchor)          # academic years since last set
            if elapsed <= 0:
                skipped += 1
                continue
            new_year = min(int(year) + elapsed, _MAX_YEAR)
            sb.table("users").update({
                "year": new_year,
                "year_anchor": cay,
            }).eq("id", r["id"]).execute()
            advanced += 1
        except Exception as exc:
            logger.warning("advance failed for user %s: %s", r.get("id"), type(exc).__name__)
            skipped += 1

    if advanced:
        logger.info("Academic-year advance: %d students moved to AY %d (%d skipped)",
                    advanced, cay, skipped)
    return {"advanced": advanced, "skipped": skipped, "academic_year": cay}
