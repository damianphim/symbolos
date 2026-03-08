"""
cards.py — Proactive advisor card generation

POST   /api/cards/generate/{user_id}   — Generate AI proactive cards
GET    /api/cards/{user_id}            — Fetch stored cards (instant)
DELETE /api/cards/{user_id}            — Clear AI-generated cards
POST   /api/cards/ask/{user_id}        — User asks a question → single card
POST   /api/cards/{card_id}/thread     — Follow-up thread on a card
PATCH  /api/cards/{card_id}/save       — Toggle saved state on a card
PATCH  /api/cards/{user_id}/reorder    — Persist drag-and-drop order

FIX: Cards no longer regenerate on every server restart.
     The frontend should call GET /api/cards/{user_id} first.
     Only call POST /generate if the response has `fresh: false` AND `count: 0`.
     The generate endpoint itself also guards with cards_are_fresh().
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import anthropic
import logging
import json
from datetime import datetime, timezone
from typing import List

from api.utils.supabase_client import get_supabase, get_user_by_id
from api.config import settings
from api.exceptions import UserNotFoundException
from api.auth import get_current_user_id, require_self

router = APIRouter()
logger = logging.getLogger(__name__)


def _lang_instruction(language: str) -> str:
    if language == "fr":
        return (
            "\n\nCRITICAL: You MUST respond entirely in French. "
            "Every text field — title, body, actions, label — must be in French. "
            "Do not use any English words."
        )
    return ""


# ── Anthropic client singleton ───────────────────────────────────
_anthropic_client: anthropic.Anthropic | None = None


def get_anthropic_client() -> anthropic.Anthropic:
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _anthropic_client


# ── Permanent category set ───────────────────────────────────────
CARD_CATEGORIES = [
    "deadlines",
    "degree",
    "courses",
    "grades",
    "planning",
    "opportunities",
]
CATEGORIES_PROMPT_LIST = "\n".join(f'  - "{c}"' for c in CARD_CATEGORIES)


# ── Pydantic models ──────────────────────────────────────────────

class ThreadRequest(BaseModel):
    user_id: str
    message: str
    card_context: str
    language: str = "en"

class GenerateRequest(BaseModel):
    force: bool = False
    language: str = "en"

class AskRequest(BaseModel):
    user_id: str
    question: str
    language: str = "en"

class RetranslateRequest(BaseModel):
    language: str = "en"

class SaveRequest(BaseModel):
    is_saved: bool

class ReorderRequest(BaseModel):
    order: List[dict]


# ── Supabase helpers ─────────────────────────────────────────────

def fetch_student_context(user_id: str) -> dict:
    supabase = get_supabase()
    user = get_user_by_id(user_id)

    favorites = (supabase.table("favorites")
        .select("course_code, course_title, subject, catalog")
        .eq("user_id", user_id).order("created_at", desc=True).limit(30)
        .execute().data or [])

    completed = (supabase.table("completed_courses")
        .select("course_code, course_title, subject, catalog, term, year, grade, credits")
        .eq("user_id", user_id).order("year", desc=True).limit(50)
        .execute().data or [])

    current = (supabase.table("current_courses")
        .select("course_code, course_title, subject, catalog, credits")
        .eq("user_id", user_id).execute().data or [])

    today = datetime.now(timezone.utc).date().isoformat()
    calendar = (supabase.table("calendar_events")
        .select("title, date, time, type, description")
        .eq("user_id", user_id).gte("date", today)
        .order("date", desc=False).limit(20)
        .execute().data or [])

    return {"user": user, "favorites": favorites,
            "completed": completed, "current": current, "calendar": calendar}


def fetch_saved_cards(user_id: str) -> list:
    supabase = get_supabase()
    resp = (supabase.table("advisor_cards")
        .select("title, body, category")
        .eq("user_id", user_id)
        .eq("is_saved", True)
        .execute())
    return resp.data or []


def cards_are_fresh(user_id: str, max_age_hours: int = 12) -> bool:
    """Returns True if AI cards exist and were generated within max_age_hours."""
    try:
        supabase = get_supabase()
        resp = (supabase.table("advisor_cards")
            .select("generated_at").eq("user_id", user_id).eq("source", "ai")
            .order("generated_at", desc=True).limit(1).execute())
        if not resp.data:
            return False
        generated_at = datetime.fromisoformat(
            resp.data[0]["generated_at"].replace("Z", "+00:00"))
        age_hours = (datetime.now(timezone.utc) - generated_at).total_seconds() / 3600
        return age_hours < max_age_hours
    except Exception:
        return False


def cards_exist(user_id: str) -> bool:
    """Returns True if any AI cards exist for this user, regardless of age."""
    try:
        supabase = get_supabase()
        resp = (supabase.table("advisor_cards")
            .select("id").eq("user_id", user_id).eq("source", "ai")
            .limit(1).execute())
        return bool(resp.data)
    except Exception:
        return False


def _sanitise_category(card: dict) -> str:
    cat = card.get("category", "planning")
    return cat if cat in CARD_CATEGORIES else "planning"


def save_cards(user_id: str, cards: list) -> None:
    """
    Replace AI-generated, non-saved cards.
    Saved cards and user-asked cards are never touched.
    """
    supabase = get_supabase()

    supabase.table("advisor_cards").delete() \
        .eq("user_id", user_id) \
        .eq("source", "ai") \
        .eq("is_saved", False) \
        .execute()

    if not cards:
        return

    existing = (supabase.table("advisor_cards")
        .select("sort_order")
        .eq("user_id", user_id)
        .order("sort_order", desc=True)
        .limit(1)
        .execute().data or [])
    base_order = (existing[0]["sort_order"] + 1) if existing else 0

    now = datetime.now(timezone.utc).isoformat()
    rows = [{
        "user_id": user_id,
        "card_type": card.get("type", "insight"),
        "icon": card.get("icon", "💡"),
        "label": card.get("label", "INSIGHT"),
        "title": card.get("title", ""),
        "body": card.get("body", ""),
        "actions": json.dumps(card.get("actions", [])),
        "priority": card.get("priority", i + 1),
        "sort_order": base_order + i,
        "category": _sanitise_category(card),
        "source": "ai",
        "is_saved": False,
        "expires_at": card.get("expires_at"),
        "generated_at": now,
    } for i, card in enumerate(cards)]
    supabase.table("advisor_cards").insert(rows).execute()


def insert_user_card(user_id: str, card: dict, question: str) -> dict:
    supabase = get_supabase()
    row = {
        "user_id": user_id,
        "card_type": card.get("type", "insight"),
        "icon": card.get("icon", "💬"),
        "label": card.get("label", "YOUR QUESTION"),
        "title": card.get("title", question[:80]),
        "body": card.get("body", ""),
        "actions": json.dumps(card.get("actions", [])),
        "priority": 0,
        "sort_order": 0,
        "category": _sanitise_category(card),
        "source": "user",
        "is_saved": False,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user_question": question,
    }
    result = supabase.table("advisor_cards").insert(row).execute()
    inserted = result.data[0] if result.data else row
    if isinstance(inserted.get("actions"), str):
        inserted["actions"] = json.loads(inserted["actions"])
    return inserted


# ── Prompt helpers ───────────────────────────────────────────────

_ACTIONS_PROMPT = (
    '"actions"  : array of 2–3 questions the STUDENT would want to click to ask '
    'the advisor to learn more about this card '
    '(e.g. "Which courses satisfy this requirement?", "When is the deadline for this?", '
    '"How do I register for this?") — '
    'write them from the student\'s perspective as if they are asking the advisor, '
    'NOT questions for the student to answer'
)


# ── Prompt builders ──────────────────────────────────────────────

def build_rich_context(ctx: dict, saved_cards: list = None) -> str:
    user = ctx["user"]
    completed, current, favorites, calendar = (
        ctx["completed"], ctx["current"], ctx["favorites"], ctx["calendar"])

    total_credits = sum(c.get("credits") or 3 for c in completed)

    adv = user.get("advanced_standing") or []
    adv_credits = sum((a.get("credits") or 0) for a in adv)
    adv_summary = ", ".join(
        f"{a['course_code']} ({a.get('credits') or 0} cr)" for a in adv
    ) or "None"

    def fmt_completed():
        return "\n".join(
            f"  - {c['course_code']} ({c.get('course_title','')}) | "
            f"Grade: {c.get('grade') or 'N/A'} | Term: {c.get('term','?')} {c.get('year','')}"
            for c in completed) or "  None recorded"

    def fmt_list(items, code_key="course_code", title_key="course_title"):
        return "\n".join(
            f"  - {i[code_key]} ({i.get(title_key,'')})" for i in items
        ) or "  None recorded"

    calendar_str = "\n".join(
        f"  - {e['date']}: {e['title']} [{e.get('type','personal')}]"
        + (f" — {e['description']}" if e.get('description') else "")
        for e in calendar) or "  No upcoming events"

    majors_str = user.get("major", "Undeclared")
    for m in (user.get("other_majors") or []):
        majors_str += f", {m}"
    minors_str = user.get("minor") or "None"
    for m in (user.get("other_minors") or []):
        minors_str += f", {m}"

    saved_section = ""
    if saved_cards:
        saved_lines = "\n".join(
            f"  - [{c.get('category','planning')}] {c['title']}: {c['body'][:120]}"
            for c in saved_cards
        )
        saved_section = f"""
SAVED CARDS (already pinned by the student — DO NOT regenerate cards covering the same topic or insight):
{saved_lines}
"""

    return f"""You are a proactive AI academic advisor for McGill University.
Analyse the student's profile and generate 8 high-value briefing cards.
{saved_section}
Today: {datetime.now(timezone.utc).date().isoformat()}

STUDENT PROFILE
  Name/email   : {user.get('username') or user.get('email', 'Student')}
  Faculty      : {user.get('faculty') or 'Not specified'}
  Major(s)     : {majors_str}
  Minor(s)     : {minors_str}
  Concentration: {user.get('concentration') or 'None'}
  Year         : U{user.get('year') or '?'}
  Credits done : {total_credits} (+ {adv_credits} advanced standing: {adv_summary})

COMPLETED COURSES
{fmt_completed()}

CURRENT COURSES
{fmt_list(current)}

SAVED/FAVOURITED COURSES
{fmt_list(favorites)}

UPCOMING CALENDAR EVENTS
{calendar_str}

INSTRUCTIONS
Generate exactly 8 cards as a JSON array. Each card must include:
  "type"     : one of "urgent" | "warning" | "insight" | "progress"
  "icon"     : single emoji
  "label"    : short ALL-CAPS label (≤ 4 words)
  "title"    : concise headline (≤ 12 words)
  "body"     : 1–3 sentence explanation with specific, actionable detail
  {_ACTIONS_PROMPT}
  "category" : one of:
{CATEGORIES_PROMPT_LIST}
  "priority" : integer 1–8 (1 = most important)

Return ONLY the JSON array — no markdown, no commentary."""


def _build_single_card_prompt(question: str, ctx: dict, language: str) -> str:
    return f"""You are a proactive AI academic advisor for McGill University.
A student has asked: "{question}"

Based on their profile below, generate a single helpful advisor card that directly answers their question.

{build_rich_context(ctx)}

Return a single JSON object (not an array) with these fields:
  "type"     : one of "urgent" | "warning" | "insight" | "progress"
  "icon"     : single emoji relevant to the answer
  "label"    : short ALL-CAPS label (≤ 4 words)
  "title"    : concise headline answering the question (≤ 12 words)
  "body"     : 2–4 sentence answer with specific, actionable detail
  {_ACTIONS_PROMPT}
  "category" : one of: {", ".join(f'"{c}"' for c in CARD_CATEGORIES)}

Return ONLY the JSON object — no markdown, no commentary.{_lang_instruction(language)}"""


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/{user_id}", response_model=dict)
async def get_cards(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """
    Fetch stored cards — instant, no AI call.
    Frontend should call this first. Only call /generate if fresh=False AND count=0.
    """
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()
        resp = (supabase.table("advisor_cards")
            .select("*")
            .eq("user_id", user_id)
            .order("sort_order", desc=False)
            .execute())
        cards = resp.data or []
        for card in cards:
            if isinstance(card.get("actions"), str):
                card["actions"] = json.loads(card["actions"])
        ai_cards = [c for c in cards if c.get("source") == "ai"]
        generated_at = ai_cards[0].get("generated_at") if ai_cards else None
        fresh = cards_are_fresh(user_id)
        return {
            "cards": cards,
            "count": len(cards),
            "generated_at": generated_at,
            "fresh": fresh,
        }
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to get cards for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve advisor cards")


@router.post("/generate/{user_id}", response_model=dict)
async def generate_cards(user_id: str, request: GenerateRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """
    Generate AI cards.
    - If force=False and cards are fresh (< 12h old), returns existing cards immediately.
    - If force=False and cards exist but are stale, regenerates them.
    - If force=True, always regenerates.
    """
    try:
        get_user_by_id(user_id)

        # Guard: don't regenerate fresh cards unless forced
        if not request.force and cards_are_fresh(user_id):
            logger.info(f"Cards already fresh for {user_id}, skipping generation")
            return await get_cards(user_id)

        ctx = fetch_student_context(user_id)
        saved = fetch_saved_cards(user_id)
        prompt = build_rich_context(ctx, saved_cards=saved) + _lang_instruction(request.language)

        client = get_anthropic_client()
        message = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        cards = json.loads(raw)
        if not isinstance(cards, list):
            raise ValueError("AI did not return a JSON array")

        for card in cards:
            card["category"] = _sanitise_category(card)
            card.setdefault("type", "insight")
            card.setdefault("icon", "💡")
            card.setdefault("actions", [])

        save_cards(user_id, cards)
        logger.info(f"Generated {len(cards)} cards for {user_id}")
        return await get_cards(user_id)

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except json.JSONDecodeError as e:
        logger.error(f"Card JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    except Exception as e:
        logger.exception(f"Card generation failed for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate advisor cards")


@router.post("/retranslate/{user_id}", response_model=dict)
async def retranslate_cards(user_id: str, request: RetranslateRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Re-generate all non-saved user-asked cards in the new language."""
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()

        resp = (supabase.table("advisor_cards")
            .select("id, user_question")
            .eq("user_id", user_id)
            .eq("source", "user")
            .eq("is_saved", False)
            .execute())
        user_cards = [c for c in (resp.data or []) if c.get("user_question")]

        if not user_cards:
            return {"retranslated": 0}

        ctx = fetch_student_context(user_id)
        client = get_anthropic_client()
        retranslated = 0

        for card_row in user_cards:
            card_id = card_row["id"]
            question = card_row["user_question"]
            prompt = _build_single_card_prompt(question, ctx, request.language)

            try:
                message = client.messages.create(
                    model=settings.CLAUDE_MODEL,
                    max_tokens=1024,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = message.content[0].text.strip()
                if raw.startswith("```"):
                    raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()
                card_data = json.loads(raw)

                supabase.table("advisor_cards").update({
                    "card_type": card_data.get("type", "insight"),
                    "icon": card_data.get("icon", "💬"),
                    "label": card_data.get("label", ""),
                    "title": card_data.get("title", ""),
                    "body": card_data.get("body", ""),
                    "actions": json.dumps(card_data.get("actions", [])),
                    "category": _sanitise_category(card_data),
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                }).eq("id", card_id).execute()
                retranslated += 1

            except Exception as e:
                logger.warning(f"Failed to retranslate card {card_id}: {e}")
                continue

        logger.info(f"Retranslated {retranslated} user cards for {user_id} to '{request.language}'")
        return {"retranslated": retranslated}

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Retranslate failed for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retranslate cards")


@router.delete("/{user_id}", status_code=204)
async def clear_cards(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()
        supabase.table("advisor_cards").delete() \
            .eq("user_id", user_id) \
            .eq("source", "ai") \
            .eq("is_saved", False) \
            .execute()
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to clear cards for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear cards")


@router.delete("/{user_id}/{card_id}", status_code=204)
async def delete_card(user_id: str, card_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()
        supabase.table("advisor_cards").delete() \
            .eq("id", card_id) \
            .eq("user_id", user_id) \
            .execute()
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to delete card {card_id} for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete card")


@router.post("/ask/{user_id}", response_model=dict)
async def ask_card(user_id: str, request: AskRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        get_user_by_id(user_id)
        ctx = fetch_student_context(user_id)
        prompt = _build_single_card_prompt(request.question, ctx, request.language)

        client = get_anthropic_client()
        message = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        card_data = json.loads(raw)
        card = insert_user_card(user_id, card_data, request.question)
        return {"card": card}

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except json.JSONDecodeError as e:
        logger.error(f"Ask card JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    except Exception as e:
        logger.exception(f"Ask card failed for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate card from question")


@router.post("/{card_id}/thread", response_model=dict)
async def thread_message(card_id: str, request: ThreadRequest):
    try:
        prompt = f"""You are a helpful AI academic advisor for McGill University.

The student is asking a follow-up question about this advisor card:

Card context: {request.card_context}

Student's follow-up: {request.message}

Provide a concise, helpful, and specific response (2–4 sentences). Be direct and actionable.{_lang_instruction(request.language)}"""

        client = get_anthropic_client()
        message = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )
        return {"response": message.content[0].text.strip()}

    except Exception as e:
        logger.exception(f"Thread message failed for card {card_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process thread message")


@router.patch("/{card_id}/save", response_model=dict)
async def save_card(card_id: str, request: SaveRequest):
    try:
        supabase = get_supabase()
        result = supabase.table("advisor_cards") \
            .update({"is_saved": request.is_saved}) \
            .eq("id", card_id) \
            .execute()
        if not result.data:
            raise HTTPException(status_code=404, detail="Card not found")
        card = result.data[0]
        if isinstance(card.get("actions"), str):
            card["actions"] = json.loads(card["actions"])
        return card
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Failed to save card {card_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update card")


@router.patch("/{user_id}/reorder", response_model=dict)
async def reorder_cards(user_id: str, request: ReorderRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()
        supabase.rpc("reorder_advisor_cards", {"payload": request.order}).execute()
        logger.info(f"Successfully reordered {len(request.order)} cards for user {user_id}")
        return {"reordered": len(request.order)}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to reorder cards for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to reorder cards")
