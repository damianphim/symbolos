"""
backend/api/routes/clubs.py

Clubs endpoints — browse verified McGill clubs, get starter suggestions
based on user major/year, join/leave clubs, and submit new clubs for review.
"""
from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import logging

from ..utils.supabase_client import get_supabase
from ..exceptions import DatabaseException
from ..auth import get_current_user_id, require_self

router = APIRouter()
logger = logging.getLogger(__name__)


# ── Hardcoded starter clubs seeded by major keywords ─────────────────────────
MAJOR_CLUB_MAP = {
    "computer science": ["McGill AI Society", "HackMcGill", "McGill Robotics", "McGill Cybersecurity Club"],
    "software":         ["HackMcGill", "McGill AI Society", "McGill Cybersecurity Club"],
    "engineering":      ["McGill Robotics", "McGill Engineering Students' Society", "Formula SAE McGill"],
    "mathematics":      ["McGill Mathematics & Statistics Society", "McGill AI Society"],
    "physics":          ["McGill Physics Society", "McGill Astronomy Society"],
    "biology":          ["McGill Biology Society", "McGill Pre-Med Society", "McGill Genetics Society"],
    "chemistry":        ["McGill Chemistry Society", "McGill Pre-Med Society"],
    "medicine":         ["McGill Pre-Med Society", "McGill Medical Ethics Society"],
    "business":         ["McGill Finance Association", "McGill Management Consulting Group", "McGill Marketing Association"],
    "management":       ["McGill Finance Association", "McGill Management Consulting Group", "McGill Entrepreneurship Society"],
    "economics":        ["McGill Economics Students' Association", "McGill Finance Association"],
    "law":              ["McGill Law Students' Association", "McGill Moot Court Society", "McGill International Law Society"],
    "arts":             ["McGill Arts Undergraduate Society", "McGill Debate Society", "Le Moyne Literary Review"],
    "psychology":       ["McGill Psychology Student Association", "McGill Mental Health Awareness Club"],
    "philosophy":       ["McGill Philosophy Society", "McGill Debate Society"],
    "music":            ["McGill Music Students' Association", "McGill Jazz Orchestra"],
    "political":        ["McGill Model UN", "McGill Debate Society", "McGill International Relations Council"],
    "environment":      ["McGill Sustainability Association", "McGill Outdoors Club"],
    "architecture":     ["McGill Architecture Students' Association"],
    "nursing":          ["McGill Nursing Students' Society"],
    "education":        ["McGill Education Student Society"],
}

DEFAULT_STARTERS = [
    "McGill Debate Society",
    "McGill Model UN",
    "HackMcGill",
    "McGill AI Society",
    "McGill Outdoors Club",
]


# ── Pydantic models ───────────────────────────────────────────────────────────

class ClubSubmission(BaseModel):
    name: str
    description: str
    category: str
    contact_email: str
    website_url: Optional[str] = None
    meeting_schedule: Optional[str] = None


class JoinClubRequest(BaseModel):
    club_id: str


# ── Helpers ───────────────────────────────────────────────────────────────────

def _get_starter_names(major: Optional[str]) -> List[str]:
    """Return a list of club names relevant to the user's major."""
    if not major:
        return DEFAULT_STARTERS
    major_lower = major.lower()
    for keyword, names in MAJOR_CLUB_MAP.items():
        if keyword in major_lower:
            return names
    return DEFAULT_STARTERS


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("")
async def list_clubs(
    search: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 50,
):
    """Return all verified clubs, optionally filtered by search term or category."""
    try:
        supabase = get_supabase()
        query = (
            supabase.table("clubs")
            .select("*")
            .eq("is_verified", True)
            .order("name")
            .limit(limit)
        )
        if category:
            query = query.eq("category", category)
        if search:
            query = query.ilike("name", f"%{search}%")
        result = query.execute()
        return {"clubs": result.data or [], "count": len(result.data or [])}
    except Exception as e:
        logger.exception(f"Error listing clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve clubs")


@router.get("/starter")
async def get_starter_clubs(user_id: str, major: Optional[str] = None):
    """Return personalised starter club suggestions based on major."""
    try:
        supabase = get_supabase()
        names = _get_starter_names(major)
        result = supabase.table("clubs").select("*").eq("is_verified", True).execute()
        all_clubs = result.data or []
        names_lower = [n.lower() for n in names]
        matched = [c for c in all_clubs if c["name"].lower() in names_lower]
        joined_result = (
            supabase.table("user_clubs")
            .select("club_id")
            .eq("user_id", user_id)
            .execute()
        )
        joined_ids = {row["club_id"] for row in (joined_result.data or [])}
        for club in matched:
            club["is_joined"] = club["id"] in joined_ids
        return {"starter_clubs": matched}
    except Exception as e:
        logger.exception(f"Error fetching starter clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve starter clubs")


# ── STATIC routes must come before dynamic /{user_id} routes ─────────────────

@router.get("/categories")
async def get_categories():
    """Return the distinct club categories in the DB."""
    return {
        "categories": [
            "Academic", "Arts & Culture", "Athletics & Recreation",
            "Community Service", "Debate & Politics", "Engineering & Technology",
            "Environment", "Health & Wellness", "International", "Professional",
            "Science", "Social", "Spiritual & Religious",
        ]
    }


@router.get("/user/{user_id}")
async def get_user_clubs(user_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Return all clubs a user has joined."""
    try:
        supabase = get_supabase()
        result = (
            supabase.table("user_clubs")
            .select("*, clubs(*)")
            .eq("user_id", user_id)
            .execute()
        )
        clubs = []
        for row in (result.data or []):
            club_data = row.get("clubs") or {}
            club_data["calendar_synced"] = row.get("calendar_synced", False)
            club_data["joined_at"] = row.get("joined_at")
            club_data["user_club_id"] = row.get("id")
            clubs.append(club_data)
        return {"clubs": clubs, "count": len(clubs)}
    except Exception as e:
        logger.exception(f"Error fetching user clubs: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user clubs")


@router.post("/user/{user_id}/join")
async def join_club(user_id: str, body: JoinClubRequest, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Add a club to the user's joined list."""
    try:
        supabase = get_supabase()
        existing = (
            supabase.table("user_clubs")
            .select("id")
            .eq("user_id", user_id)
            .eq("club_id", body.club_id)
            .execute()
        )
        if existing.data:
            raise HTTPException(status_code=409, detail="Already joined this club")
        supabase.table("user_clubs").insert({
            "user_id": user_id,
            "club_id": body.club_id,
            "calendar_synced": False,
        }).execute()
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Error joining club: {e}")
        raise HTTPException(status_code=500, detail="Failed to join club")


@router.delete("/user/{user_id}/leave/{club_id}")
async def leave_club(user_id: str, club_id: str, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Remove a club from the user's joined list."""
    try:
        supabase = get_supabase()
        supabase.table("user_clubs").delete().eq("user_id", user_id).eq("club_id", club_id).execute()
        return {"success": True}
    except Exception as e:
        logger.exception(f"Error leaving club: {e}")
        raise HTTPException(status_code=500, detail="Failed to leave club")


@router.patch("/user/{user_id}/calendar/{club_id}")
async def toggle_calendar_sync(user_id: str, club_id: str, synced: bool, req: Request, current_user_id: str = Depends(get_current_user_id)):
    require_self(current_user_id, user_id)
    """Toggle calendar sync for a club."""
    try:
        supabase = get_supabase()
        supabase.table("user_clubs").update({"calendar_synced": synced}).eq("user_id", user_id).eq("club_id", club_id).execute()
        return {"success": True, "calendar_synced": synced}
    except Exception as e:
        logger.exception(f"Error toggling calendar sync: {e}")
        raise HTTPException(status_code=500, detail="Failed to update calendar sync")


@router.post("/submit")
async def submit_club(submission: ClubSubmission):
    """Submit a new club for admin review."""
    try:
        supabase = get_supabase()
        supabase.table("club_submissions").insert({
            "name": submission.name,
            "description": submission.description,
            "category": submission.category,
            "contact_email": submission.contact_email,
            "website_url": submission.website_url,
            "meeting_schedule": submission.meeting_schedule,
            "status": "pending",
        }).execute()
        return {"success": True, "message": "Club submission received. We'll review it shortly!"}
    except Exception as e:
        logger.exception(f"Error submitting club: {e}")
        raise HTTPException(status_code=500, detail="Failed to submit club")
