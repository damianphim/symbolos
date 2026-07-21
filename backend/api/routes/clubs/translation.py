"""On-demand AI translation of a club's free-text detail fields.

The club detail drawer calls GET /api/clubs/{club_id}/translation?lang=fr|zh
when a non-English viewer opens a club. We translate description /
meeting_schedule / join_instructions with a single Haiku call and cache the
result in per-language columns (see 2026_07_21_clubs_translation_cache.sql),
so a club is only ever translated once per language until its owner edits the
source text (edit_club nulls the cache).

`name` is deliberately never translated — club names are proper nouns/acronyms.
"""
from fastapi import HTTPException, Query, Depends
import json
import logging

from ...utils.supabase_client import get_supabase
from ...auth import get_current_user_id
from ._router import router

logger = logging.getLogger(__name__)

# Source field → its per-language cache columns.
_TRANSLATABLE_FIELDS = ("description", "meeting_schedule", "join_instructions")
_SUPPORTED_LANGS = ("fr", "zh")
_LANG_NAMES = {"fr": "French", "zh": "Simplified Chinese (Mandarin)"}


def clear_translations_for_fields(supabase, club_id: str, changed_fields: list[str]) -> None:
    """Null out the cached _fr/_zh columns for any source field that changed,
    so the stale translation is regenerated on next view. Called from edit_club.
    Best-effort: a failure here must never block the edit itself."""
    cols = {
        f"{field}_{lang}": None
        for field in changed_fields if field in _TRANSLATABLE_FIELDS
        for lang in _SUPPORTED_LANGS
    }
    if not cols:
        return
    try:
        supabase.table("clubs").update(cols).eq("id", club_id).execute()
    except Exception as e:
        logger.warning(f"Failed to clear stale club translations for {club_id}: {e}")


def _translate_fields(source: dict, lang: str) -> dict:
    """One Haiku call translating the given {field: text} map into `lang`.
    Returns {field: translated}. On any failure returns the source unchanged
    (caller shows English rather than erroring)."""
    # Import here to avoid a circular import at module load (chat imports courses,
    # which is unrelated, but keep the clubs package import-light regardless).
    from ...config import settings
    from ..chat import get_anthropic_client

    lang_name = _LANG_NAMES[lang]
    payload = json.dumps(source, ensure_ascii=False)
    prompt = (
        f"Translate the string VALUES of this JSON object into {lang_name}. "
        f"Return ONLY a JSON object with the exact same keys and translated values — "
        f"no markdown, no commentary. Keep proper nouns (club names, McGill, program "
        f"names), URLs, email addresses, times, and dates unchanged. This is a McGill "
        f"student club listing.\n\n{payload}"
    )
    try:
        client = get_anthropic_client()
        message = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        if "{" in raw and "}" in raw:
            raw = raw[raw.find("{"):raw.rfind("}") + 1]
        translated = json.loads(raw)
        if not isinstance(translated, dict):
            raise ValueError("translation was not a JSON object")
        # Only trust keys we asked for; fall back per-field to the source.
        return {k: (translated.get(k) or v) for k, v in source.items()}
    except Exception as e:
        logger.warning(f"Club field translation to {lang} failed: {e}")
        return dict(source)


@router.get("/{club_id}/translation")
async def get_club_translation(
    club_id: str,
    lang: str = Query(..., min_length=2, max_length=5),
    _: str = Depends(get_current_user_id),
):
    """Return {description, meeting_schedule, join_instructions} for a club in
    `lang`, translating + caching on first request. Auth-gated (McGill-only)
    like the rest of the clubs API; club text itself is public flyer content."""
    lang = lang.lower().split("-")[0]
    supabase = get_supabase()

    cols = list(_TRANSLATABLE_FIELDS)
    if lang in _SUPPORTED_LANGS:
        cols += [f"{f}_{lang}" for f in _TRANSLATABLE_FIELDS]
    try:
        rows = supabase.table("clubs").select(",".join(cols)).eq("id", club_id).execute().data or []
    except Exception as e:
        logger.exception(f"Failed to load club {club_id} for translation: {e}")
        raise HTTPException(status_code=500, detail="Failed to load club")
    if not rows:
        raise HTTPException(status_code=404, detail="Club not found")
    row = rows[0]

    # English (or any unsupported language) → originals, no AI call.
    if lang not in _SUPPORTED_LANGS:
        return {f: row.get(f) for f in _TRANSLATABLE_FIELDS}

    # Only translate fields that actually have source text.
    source = {f: row[f] for f in _TRANSLATABLE_FIELDS if (row.get(f) or "").strip()}
    if not source:
        return {f: row.get(f) for f in _TRANSLATABLE_FIELDS}

    # Cache hit only if EVERY non-empty source field already has a translation.
    cached = {f: row.get(f"{f}_{lang}") for f in source}
    if all((cached.get(f) or "").strip() for f in source):
        result = {f: row.get(f) for f in _TRANSLATABLE_FIELDS}
        result.update(cached)
        return result

    translated = _translate_fields(source, lang)

    # Persist the cache (best-effort — a write failure still returns the text).
    try:
        supabase.table("clubs").update(
            {f"{f}_{lang}": translated[f] for f in source}
        ).eq("id", club_id).execute()
    except Exception as e:
        logger.warning(f"Failed to cache club {club_id} translation ({lang}): {e}")

    result = {f: row.get(f) for f in _TRANSLATABLE_FIELDS}
    result.update(translated)
    return result
