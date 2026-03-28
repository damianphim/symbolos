"""
cards.py — Proactive advisor card generation

POST   /api/cards/generate/{user_id}   — Generate AI proactive cards
GET    /api/cards/{user_id}            — Fetch stored cards (instant)
DELETE /api/cards/{user_id}            — Clear AI-generated cards
POST   /api/cards/ask/{user_id}        — User asks a question → single card
POST   /api/cards/{card_id}/thread     — Follow-up thread on a card
PATCH  /api/cards/{card_id}/save       — Toggle saved state on a card
PATCH  /api/cards/{user_id}/reorder    — Persist drag-and-drop order

CONTEXT FIX (v3):
  Thread endpoint previously called Claude with ONLY the card body — no student
  profile, no completed courses, nothing. It now imports build_system_context
  from chat.py and passes the full student context as the system prompt, with
  the card body injected via card_context and thread history in the messages
  array. Card threads now have the same context quality as main chat.
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel, Field
import anthropic
import logging
import json
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from api.utils.supabase_client import get_supabase, get_user_by_id
from api.config import settings
from api.exceptions import UserNotFoundException
from api.auth import get_current_user_id, require_self
from api.utils.sanitise import sanitise_user_message, sanitise_context_field

router = APIRouter()
logger = logging.getLogger(__name__)


def _lang_instruction(language: str) -> str:
    if language == "fr":
        return (
            "\n\nCRITICAL: You MUST respond entirely in French. "
            "Every text field — title, body, actions, label — must be in French. "
            "Do not use any English words."
        )
    if language == "zh":
        return (
            "\n\nCRITICAL: You MUST respond entirely in Simplified Chinese (Mandarin). "
            "Every text field — title, body, actions, label — must be in Chinese. "
            "Do not use any English words except for proper nouns like course codes and names."
        )
    # Default: English — must be explicit so French/Chinese context in student data
    # does not cause the model to drift into another language.
    return (
        "\n\nCRITICAL: You MUST respond entirely in English. "
        "Every text field — title, body, actions, label — must be in English. "
        "Do not use French, Chinese, or any other language, even if the student's "
        "course names or calendar events are in another language."
    )


_anthropic_client: anthropic.Anthropic | None = None


def get_anthropic_client() -> anthropic.Anthropic:
    global _anthropic_client
    if _anthropic_client is None:
        _anthropic_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _anthropic_client


CARD_CATEGORIES = ["deadlines", "degree", "courses", "grades", "planning", "opportunities"]
CATEGORIES_PROMPT_LIST = "\n".join(f'  - "{c}"' for c in CARD_CATEGORIES)


class ThreadRequest(BaseModel):
    user_id: str
    message: str = Field(..., min_length=1, max_length=2000)
    card_context: str = Field(..., max_length=4000)
    language: str = "en"
    thread_history: Optional[List[dict]] = Field(default=None, max_length=20)

class GenerateRequest(BaseModel):
    force: bool = False
    language: str = "en"

class AskRequest(BaseModel):
    user_id: str
    question: str = Field(..., min_length=1, max_length=2000)
    language: str = "en"

class RetranslateRequest(BaseModel):
    language: str = "en"

class SaveRequest(BaseModel):
    is_saved: bool

class CardOrder(BaseModel):
    id: str = Field(..., max_length=100)
    position: Optional[int] = Field(None, ge=0, le=100)
    sort_order: Optional[int] = Field(None, ge=0, le=100)

    @property
    def resolved_position(self) -> int:
        """Accept either 'position' or 'sort_order' from frontend."""
        if self.position is not None:
            return self.position
        if self.sort_order is not None:
            return self.sort_order
        return 0

class ReorderRequest(BaseModel):
    order: List[CardOrder] = Field(..., max_length=50)


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

    joined_clubs, created_clubs = [], []
    try:
        r = supabase.table("user_clubs").select("clubs(name, category, meeting_schedule)").eq("user_id", user_id).execute()
        joined_clubs = [x.get("clubs", {}).get("name", "Unknown") for x in (r.data or []) if x.get("clubs")]
    except Exception:
        pass
    try:
        r = supabase.table("clubs").select("name, category, member_count, is_private").eq("created_by", user_id).execute()
        created_clubs = r.data or []
    except Exception:
        pass

    return {"user": user, "favorites": favorites, "completed": completed,
            "current": current, "calendar": calendar,
            "joined_clubs": joined_clubs, "created_clubs": created_clubs}


def fetch_saved_cards(user_id: str) -> list:
    supabase = get_supabase()
    return (supabase.table("advisor_cards")
        .select("title, body, category").eq("user_id", user_id).eq("is_saved", True)
        .execute().data or [])


def cards_are_fresh(user_id: str, max_age_hours: int = 168) -> bool:
    """Returns True if AI cards exist and were generated within max_age_hours (default 7 days)."""
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


def _count_generations_this_week(user_id: str) -> int:
    """Count how many times AI cards were generated for this user in the last 7 days."""
    try:
        supabase = get_supabase()
        week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        # Count distinct generated_at timestamps (each generation batch shares one timestamp)
        resp = (supabase.table("advisor_cards")
            .select("generated_at")
            .eq("user_id", user_id).eq("source", "ai")
            .gte("generated_at", week_ago)
            .order("generated_at", desc=True)
            .execute())
        if not resp.data:
            return 0
        # Count unique generation timestamps (each batch shares one)
        unique_times = set(r["generated_at"] for r in resp.data)
        return len(unique_times)
    except Exception:
        return 0


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
    cat = str(card.get("category") or "").lower().strip()
    return cat if cat in CARD_CATEGORIES else "planning"


def save_cards(user_id: str, cards: list) -> None:
    supabase = get_supabase()
    supabase.table("advisor_cards").delete().eq("user_id", user_id).eq("source", "ai").execute()
    now = datetime.now(timezone.utc).isoformat()
    rows = []
    for i, card in enumerate(cards):
        actions = card.get("actions") or []
        rows.append({
            "user_id": user_id, "source": "ai",
            "card_type": card.get("type", "insight"), "icon": card.get("icon", "💡"),
            "label": card.get("label", ""), "title": card.get("title", ""),
            "body": card.get("body", ""), "actions": json.dumps(actions),
            "category": _sanitise_category(card), "priority": card.get("priority", i + 1),
            "sort_order": i, "generated_at": now,
        })
    if rows:
        supabase.table("advisor_cards").insert(rows).execute()


def insert_user_card(user_id: str, card_data: dict, question: str, language: str) -> dict:
    supabase = get_supabase()
    actions = card_data.get("actions") or []
    now = datetime.now(timezone.utc).isoformat()
    existing = (supabase.table("advisor_cards").select("sort_order")
        .eq("user_id", user_id).order("sort_order", desc=True).limit(1).execute().data or [])
    next_sort = (existing[0]["sort_order"] + 1) if existing else 0
    row = {
        "user_id": user_id, "source": "user",
        "card_type": card_data.get("type", "insight"), "icon": card_data.get("icon", "❓"),
        "label": card_data.get("label", "YOUR QUESTION"), "title": card_data.get("title", question[:80]),
        "body": card_data.get("body", ""), "actions": json.dumps(actions),
        "category": _sanitise_category(card_data), "priority": 0,
        "sort_order": next_sort, "generated_at": now, "prompted_language": language,
    }
    result = supabase.table("advisor_cards").insert(row).execute()
    inserted = result.data[0] if result.data else row
    if isinstance(inserted.get("actions"), str):
        inserted["actions"] = json.loads(inserted["actions"])
    return inserted


_ACTIONS_PROMPT = (
    '"actions"  : array of 2–3 questions the STUDENT would want to click to ask '
    'the advisor to learn more about this card '
    '(e.g. "Which courses satisfy this requirement?", "When is the deadline for this?", '
    '"How do I register for this?") — '
    'write them from the student\'s perspective as if they are asking the advisor, '
    'NOT questions for the student to answer. '
    'For opportunity cards that recommend professors, also include action objects with '
    '"type" set to "email_professor" (label e.g. "Draft an email to Prof. X") or '
    '"visit_lab_page" (label e.g. "Visit their research lab page"). '
    'These action objects use the format {"type": "<action_type>", "label": "<display text>"}. '
    'You may mix plain string actions and typed action objects in the same array'
)


def _deduplicate_completed(completed: list) -> list:
    """
    Filter completed courses so that withdrawn/failed attempts are excluded
    when the same course was later completed with a passing grade.

    This prevents the AI from suggesting "retake COMP 273" when the student
    already withdrew and then retook it successfully.
    """
    NON_PASSING = {"W", "F", "U", "WF", "WL", "J", "KF"}

    # Build a set of course codes that have at least one passing grade
    passed_codes = set()
    for c in completed:
        grade = (c.get("grade") or "").strip().upper()
        if grade and grade not in NON_PASSING:
            passed_codes.add(c.get("course_code", ""))

    # Filter: keep all entries UNLESS it's a non-passing grade for a course
    # that was later passed
    result = []
    for c in completed:
        code = c.get("course_code", "")
        grade = (c.get("grade") or "").strip().upper()
        if grade in NON_PASSING and code in passed_codes:
            # Skip this entry — the student retook and passed
            continue
        result.append(c)
    return result


def build_rich_context(ctx: dict, saved_cards: list = None) -> str:
    user = ctx["user"]
    completed, current, favorites, calendar = (ctx["completed"], ctx["current"], ctx["favorites"], ctx["calendar"])
    # Deduplicate: remove withdrawn/failed entries when course was later passed
    completed = _deduplicate_completed(completed)
    total_credits = sum(c.get("credits") or 3 for c in completed)
    adv = user.get("advanced_standing") or []
    adv_credits = sum((a.get("credits") or 0) for a in adv)
    adv_summary = ", ".join(f"{a['course_code']} ({a.get('credits') or 0} cr)" for a in adv) or "None"

    def fmt_completed():
        return "\n".join(
            f"  - {c['course_code']} ({sanitise_context_field(c.get('course_title',''))}) | "
            f"Grade: {c.get('grade') or 'N/A'} | Term: {c.get('term','?')} {c.get('year','')}"
            for c in completed) or "  None recorded"

    def fmt_list(items, code_key="course_code", title_key="course_title"):
        return "\n".join(
            f"  - {i[code_key]} ({sanitise_context_field(i.get(title_key,''))})" for i in items
        ) or "  None recorded"

    calendar_str = "\n".join(
        f"  - {e['date']}: {sanitise_context_field(e['title'])} [{e.get('type','personal')}]"
        + (f" — {sanitise_context_field(e['description'])}" if e.get('description') else "")
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
            f"  - [{c.get('category','planning')}] {sanitise_context_field(c['title'])}: {sanitise_context_field(c['body'][:120])}"
            for c in saved_cards)
        saved_section = f"\nSAVED CARDS (already pinned — DO NOT regenerate cards covering these topics):\n{saved_lines}\n"

    safe_username      = sanitise_context_field(str(user.get('username') or user.get('email', 'Student')))
    safe_faculty       = sanitise_context_field(str(user.get('faculty') or 'Not specified'))
    safe_majors        = sanitise_context_field(majors_str)
    safe_minors        = sanitise_context_field(minors_str)
    safe_concentration = sanitise_context_field(str(user.get('concentration') or 'None'))

    return f"""You are a proactive AI academic advisor for McGill University.
Analyse the student's profile and generate 8 high-value briefing cards.
{saved_section}
Today: {datetime.now(timezone.utc).date().isoformat()}

STUDENT PROFILE
  Name/email   : {safe_username}
  Faculty      : {safe_faculty}
  Major(s)     : {safe_majors}
  Minor(s)     : {safe_minors}
  Concentration: {safe_concentration}
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

STUDENT CLUBS
  Joined: {', '.join(ctx.get('joined_clubs', [])) or 'None'}
  Created: {', '.join(c.get('name','') for c in ctx.get('created_clubs', [])) or 'None'}

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

PROFESSOR RECOMMENDATIONS FOR OPPORTUNITY CARDS
For "opportunities" cards, when relevant, recommend specific McGill professors the student
could reach out to based on their major, completed courses, and interests. Include:
  - Professor name and department
  - Their research area that aligns with the student's profile
  - A suggested approach for reaching out (e.g. "Attend their office hours for COMP 251"
    or "Email about their ML research lab openings")
  - Only recommend professors when you have high confidence they are real McGill faculty members
  - Add a disclaimer at the end of the card body: "Verify professor details on McGill's department website."
At least 1 of the 8 cards should be an "opportunities" card with a professor recommendation
if the student's profile has a declared major.

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


def _get_stored_cards_language(user_id: str) -> str | None:
    """Read the cards language stored in Supabase auth user metadata."""
    try:
        supabase = get_supabase()
        resp = supabase.auth.admin.get_user_by_id(user_id)
        meta = (resp.user.user_metadata or {}) if resp.user else {}
        lang = meta.get("cards_language")
        return lang if lang in ("en", "fr", "zh") else None
    except Exception:
        return None


def _set_stored_cards_language(user_id: str, language: str) -> None:
    """Persist the cards language in Supabase auth user metadata."""
    try:
        supabase = get_supabase()
        resp = supabase.auth.admin.get_user_by_id(user_id)
        existing_meta = (resp.user.user_metadata or {}) if resp.user else {}
        existing_meta["cards_language"] = language
        supabase.auth.admin.update_user_by_id(user_id, {"user_metadata": existing_meta})
    except Exception as e:
        logger.warning(f"Could not persist cards language for {user_id}: {e}")


def _fetch_cards_response(user_id: str, confirmed_language: str | None = None) -> dict:
    """
    confirmed_language: pass the language when cards were just generated/retranslated.
    When None, reads the previously persisted language from user metadata.
    """
    get_user_by_id(user_id)
    supabase = get_supabase()
    resp = (supabase.table("advisor_cards").select("*")
        .eq("user_id", user_id).order("sort_order", desc=False).execute())
    cards = resp.data or []
    for card in cards:
        if isinstance(card.get("actions"), str):
            card["actions"] = json.loads(card["actions"])
    ai_cards = [c for c in cards if c.get("source") == "ai"]
    generated_at = ai_cards[0].get("generated_at") if ai_cards else None
    # Use confirmed language if just set; otherwise read from stored metadata
    cards_language = confirmed_language if confirmed_language else _get_stored_cards_language(user_id)
    return {
        "cards": cards, "count": len(cards), "generated_at": generated_at,
        "fresh": cards_are_fresh(user_id),
        "cards_language": cards_language,
    }


@router.get("/{user_id}", response_model=dict)
async def get_cards(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        return _fetch_cards_response(user_id)
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
    - If force=False and cards are fresh (< 7 days old), returns existing cards immediately.
    - If force=True, regenerates (max 2 times per week).
    """
    try:
        get_user_by_id(user_id)
        if not request.force and cards_are_fresh(user_id):
            logger.info(f"Cards already fresh for {user_id}, skipping generation")
            # confirmed_language=None: we don't know what language these cached cards are in.
            # The frontend will check and retranslate if needed.
            return _fetch_cards_response(user_id, confirmed_language=None)

        # Rate limit: max 2 forced regenerations per week
        if request.force:
            gen_count = _count_generations_this_week(user_id)
            if gen_count >= 2:
                logger.info(f"Rate limit: {user_id} already generated {gen_count} times this week")
                return _fetch_cards_response(user_id)

        ctx = fetch_student_context(user_id)
        saved = fetch_saved_cards(user_id)
        prompt = build_rich_context(ctx, saved_cards=saved) + _lang_instruction(request.language)

        client = get_anthropic_client()
        message = client.messages.create(model=settings.CLAUDE_MODEL, max_tokens=4096,
            messages=[{"role": "user", "content": prompt}])

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
        _set_stored_cards_language(user_id, request.language)
        logger.info(f"Generated {len(cards)} cards for {user_id} in {request.language}")
        return _fetch_cards_response(user_id, confirmed_language=request.language)

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
    try:
        get_user_by_id(user_id)
        ctx = fetch_student_context(user_id)
        # Don't include saved_cards — they may be in a different language
        # which would influence the model to respond in that language instead.
        prompt = build_rich_context(ctx, saved_cards=None) + _lang_instruction(request.language)

        client = get_anthropic_client()
        message = client.messages.create(
            model=settings.CLAUDE_MODEL, max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
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
        _set_stored_cards_language(user_id, request.language)
        logger.info(f"Retranslated {len(cards)} cards for {user_id} in {request.language}")
        return _fetch_cards_response(user_id, confirmed_language=request.language)

    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except json.JSONDecodeError as e:
        logger.error(f"Retranslate JSON parse error: {e}")
        raise HTTPException(status_code=500, detail="Failed to parse AI response")
    except Exception as e:
        logger.exception(f"Retranslate failed for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retranslate cards")


@router.delete("/{user_id}", status_code=204)
async def delete_cards(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()
        supabase.table("advisor_cards").delete().eq("user_id", user_id).eq("source", "ai").execute()
        return None
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to delete cards for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete cards")


@router.delete("/{user_id}/{card_id}", status_code=204)
async def delete_card(user_id: str, card_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    try:
        get_user_by_id(user_id)
        supabase = get_supabase()
        supabase.table("advisor_cards").delete().eq("id", card_id).eq("user_id", user_id).execute()
        return None
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to delete card {card_id} for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete card")


@router.post("/ask/{user_id}", response_model=dict)
async def ask_card(user_id: str, request: AskRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    sanitise_user_message(request.question)
    try:
        get_user_by_id(user_id)
        ctx = fetch_student_context(user_id)
        prompt = _build_single_card_prompt(request.question, ctx, request.language)

        client = get_anthropic_client()
        message = client.messages.create(model=settings.CLAUDE_MODEL, max_tokens=1024,
            messages=[{"role": "user", "content": prompt}])

        raw = message.content[0].text.strip()
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        card_data = json.loads(raw)
        card = insert_user_card(user_id, card_data, request.question, request.language)
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
async def thread_message(
    card_id: str,
    request: ThreadRequest,
    req: Request,
    current_user_id: str = Depends(get_current_user_id),
):
    """
    Follow-up thread on a card.
    Now uses build_system_context() from chat.py — same full student context
    as main chat. Card body is injected via card_context. Thread history is
    passed in the messages array for conversation continuity.
    """
    require_self(current_user_id, request.user_id)
    sanitise_user_message(request.message)

    try:
        supabase = get_supabase()
        card_row = (supabase.table("advisor_cards")
            .select("user_id, source, prompted_language").eq("id", card_id).execute())
        if not card_row.data:
            raise HTTPException(status_code=404, detail="Card not found")
        if card_row.data[0]["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        reply_language = request.language
        if card_row.data[0].get("source") == "user":
            reply_language = card_row.data[0].get("prompted_language") or request.language

        # Import here to avoid circular imports at module level
        from api.routes.chat import build_system_context

        user = get_user_by_id(request.user_id)
        system_context = build_system_context(
            user,
            current_tab=None,
            language=reply_language,
            card_context=sanitise_context_field(request.card_context, max_length=800),
        )

        # Build messages array: prior thread turns + current message
        messages = []
        if request.thread_history:
            for msg in request.thread_history[-16:]:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role in ("user", "assistant") and content:
                    messages.append({"role": role, "content": content})
        messages.append({"role": "user", "content": request.message})

        client = get_anthropic_client()
        logger.info(
            f"Card thread {card_id}: {len(messages)} messages, "
            f"lang={reply_language}, user={request.user_id}"
        )
        response = client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=512,
            system=system_context,
            messages=messages,
        )
        return {"response": response.content[0].text.strip()}

    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Thread message failed for card {card_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process thread message")


@router.patch("/{card_id}/save", response_model=dict)
async def save_card(card_id: str, request: SaveRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    try:
        supabase = get_supabase()
        ownership = supabase.table("advisor_cards").select("user_id").eq("id", card_id).execute()
        if not ownership.data:
            raise HTTPException(status_code=404, detail="Card not found")
        if ownership.data[0]["user_id"] != current_user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        result = supabase.table("advisor_cards").update({"is_saved": request.is_saved}).eq("id", card_id).execute()
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
        payload = [{"id": item.id, "position": item.resolved_position} for item in request.order]
        supabase.rpc("reorder_advisor_cards", {"payload": payload}).execute()
        logger.info(f"Successfully reordered {len(request.order)} cards for user {user_id}")
        return {"reordered": len(request.order)}
    except UserNotFoundException:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logger.exception(f"Failed to reorder cards for {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to reorder cards")