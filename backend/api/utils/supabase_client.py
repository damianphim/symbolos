"""
Supabase client with retry + reconnect logic.

Fixes applied:
  #10 – Complete type hints on all public functions
  #11 – Added check_database_health() for connection health checks
  #12 – EGRESS FIX: search_courses() and get_course() select only needed columns
  #13 – RECONNECT FIX: with_retry() resets the singleton on "Server disconnected"
        errors and retries up to MAX_RETRIES times with exponential backoff.
        Prevents cascading 500s after idle connection timeouts.
  #14 – HTTP/2 FIX: Force HTTP/1.1 by replacing the postgrest httpx session
        after client creation. Prevents LocalProtocolError pseudo-header trailer
        bug triggered by .rpc() calls. Works across all supabase-py versions.
"""
from supabase import create_client, Client
from typing import Optional, List, Dict, Any, Callable, TypeVar
import logging
import uuid
import time
import httpx
from api.config import settings
from api.exceptions import DatabaseException, UserNotFoundException

logger = logging.getLogger(__name__)

T = TypeVar("T")

# Singleton client
_supabase_client: Optional[Client] = None

# Disconnect error patterns that warrant a full client reset
_DISCONNECT_SIGNALS = (
    "server disconnected",
    "connection reset",
    "connection refused",
    "eof occurred",
    "broken pipe",
    "remotedisconnected",
    "connectionerror",
    "timeout",
    "localprotocolerror",  # HTTP/2 pseudo-header trailer bug
)

MAX_RETRIES = 3
RETRY_BACKOFF = 0.3  # seconds — doubles each retry: 0.3s, 0.6s


def _is_disconnect(exc: Exception) -> bool:
    msg = str(exc).lower()
    return any(sig in msg for sig in _DISCONNECT_SIGNALS)


def _reset_client() -> None:
    """Force the singleton to be recreated on next get_supabase() call."""
    global _supabase_client
    _supabase_client = None
    logger.info("Supabase client reset — will reconnect on next request")


def _force_http1(client: Client) -> None:
    """
    Replace the postgrest httpx session with one that has HTTP/2 disabled.
    Copies base_url and headers from the old session so requests still work.
    This is the version-agnostic fix for LocalProtocolError on .rpc() calls.
    """
    try:
        pg = client.postgrest
        old_session = getattr(pg, "_session", None) or getattr(pg, "session", None)
        if old_session is None:
            logger.warning("Could not find postgrest session to patch")
            return

        new_session = httpx.Client(
            http2=False,
            base_url=old_session.base_url,
            headers=dict(old_session.headers),
        )

        if hasattr(pg, "_session"):
            pg._session = new_session
        else:
            pg.session = new_session

        logger.info("HTTP/1.1 forced on postgrest session")
    except Exception as e:
        logger.warning(f"Could not force HTTP/1.1 (non-fatal): {e}")


def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_KEY,
            )
            # Fix #14: force HTTP/1.1 to prevent LocalProtocolError on .rpc() calls
            _force_http1(_supabase_client)
            logger.info("Supabase client initialized")
            try:
                _supabase_client.table("users").select("id").limit(1).execute()
                logger.info("Supabase connection warmed up")
            except Exception:
                pass  # Don't fail startup if warmup fails
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise DatabaseException("initialization", str(e))
    return _supabase_client


def get_user_supabase(jwt: str) -> Client:
    """
    Create a per-request Supabase client authenticated with the user's JWT.
    Queries through this client respect Row Level Security — users can only
    read/write their own rows. Use this for ALL user-data queries.
    Use get_supabase() (service role) only for auth.admin.* and cron operations.
    """
    client = create_client(
        settings.SUPABASE_URL,
        settings.SUPABASE_ANON_KEY or settings.SUPABASE_SERVICE_KEY,  # fallback until anon key is configured
    )
    # Set the user's JWT so PostgREST enforces RLS via auth.uid()
    client.postgrest.auth(jwt)
    _force_http1(client)
    return client


def with_retry(operation: str, fn: Callable[[], T]) -> T:
    """
    Execute fn(), retrying up to MAX_RETRIES times on disconnect errors.
    Resets the Supabase singleton before each retry so a fresh connection
    is used rather than the stale one that caused the disconnect.
    """
    last_exc: Exception = RuntimeError("unreachable")
    for attempt in range(MAX_RETRIES):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
            if _is_disconnect(exc) and attempt < MAX_RETRIES - 1:
                logger.warning(
                    f"{operation}: disconnect on attempt {attempt + 1}, "
                    f"resetting client and retrying in {RETRY_BACKOFF * (2**attempt):.1f}s … ({exc})"
                )
                _reset_client()
                time.sleep(RETRY_BACKOFF * (2 ** attempt))
            else:
                raise
    raise last_exc


# ── Health check ──────────────────────────────────────────────────────────────

def check_database_health() -> bool:
    try:
        supabase = get_supabase()
        supabase.table("users").select("id").limit(1).execute()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False


# ── User Operations ───────────────────────────────────────────────────────────

def get_user_by_id(user_id: str) -> Dict[str, Any]:
    def _run():
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise UserNotFoundException(user_id)
        return response.data[0]
    try:
        return with_retry("get_user_by_id", _run)
    except UserNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error getting user {user_id}: {e}")
        raise DatabaseException("get_user", str(e))


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    def _run():
        supabase = get_supabase()
        response = supabase.table("users").select("*").eq("email", email).execute()
        return response.data[0] if response.data else None
    try:
        return with_retry("get_user_by_email", _run)
    except Exception as e:
        logger.error(f"Error getting user by email: {e}")
        raise DatabaseException("get_user_by_email", str(e))


def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    def _run():
        supabase = get_supabase()
        cleaned_data = {k: v for k, v in user_data.items() if v is not None}
        logger.info(f"Creating user profile with ID: {cleaned_data.get('id')}")
        response = supabase.table("users").insert(cleaned_data).execute()
        if not response.data:
            raise DatabaseException("create_user", "No data returned from insert")
        logger.info(f"User profile created: {response.data[0].get('id')}")
        return response.data[0]

    try:
        return with_retry("create_user", _run)
    except Exception as e:
        error_str = str(e)
        logger.error(f"Error creating user: {error_str}")
        if "duplicate key" in error_str.lower() or "23505" in error_str:
            user_id = user_data.get("id")
            logger.warning(f"Duplicate detected for user ID: {user_id}")
            try:
                return get_user_by_id(user_id)
            except UserNotFoundException:
                pass
            if "email" in error_str:
                raise DatabaseException("create_user", "Email already in use by another account")
            if "username" in error_str:
                raise DatabaseException("create_user", "Username already taken")
        raise DatabaseException("create_user", error_str)


def update_user(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    def _run():
        supabase = get_supabase()
        response = supabase.table("users").update(updates).eq("id", user_id).execute()
        if not response.data:
            raise UserNotFoundException(user_id)
        logger.info(f"User updated: {user_id}")
        return response.data[0]
    try:
        return with_retry("update_user", _run)
    except UserNotFoundException:
        raise
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        raise DatabaseException("update_user", str(e))


# ── Chat Operations ───────────────────────────────────────────────────────────

def get_chat_history(user_id: str, session_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
    def _run():
        supabase = get_supabase()
        query = supabase.table("chat_messages").select("*").eq("user_id", user_id)
        if session_id:
            query = query.eq("session_id", session_id)
        return query.order("created_at", desc=False).limit(min(limit, 200)).execute().data or []
    try:
        return with_retry("get_chat_history", _run)
    except Exception as e:
        logger.error(f"Error getting chat history for {user_id}: {e}")
        raise DatabaseException("get_chat_history", str(e))


def get_user_sessions(user_id: str, limit: int = 20) -> List[Dict[str, Any]]:
    def _run():
        supabase = get_supabase()
        all_messages = (
            supabase.table("chat_messages")
            .select("session_id, created_at, content, role")
            .eq("user_id", user_id)
            .not_.is_("session_id", "null")
            .order("created_at", desc=False)
            .execute()
        )
        sessions_dict: Dict[str, Any] = {}
        for msg in all_messages.data:
            sid = msg["session_id"]
            if sid not in sessions_dict:
                sessions_dict[sid] = {
                    "session_id": sid,
                    "last_updated": msg["created_at"],
                    "message_count": 0,
                    "first_user_message": None,
                }
            if msg["role"] == "user" and sessions_dict[sid]["first_user_message"] is None:
                sessions_dict[sid]["first_user_message"] = msg["content"][:50]
            if msg["created_at"] > sessions_dict[sid]["last_updated"]:
                sessions_dict[sid]["last_updated"] = msg["created_at"]
            sessions_dict[sid]["message_count"] += 1

        sessions = [
            {
                "session_id": sid,
                "last_message": data["first_user_message"] or "Chat Session",
                "last_updated": data["last_updated"],
                "message_count": data["message_count"],
            }
            for sid, data in sessions_dict.items()
        ]
        sessions.sort(key=lambda x: x["last_updated"], reverse=True)
        return sessions[:limit]

    try:
        return with_retry("get_user_sessions", _run)
    except Exception as e:
        logger.error(f"Error getting user sessions for {user_id}: {e}")
        return []


def save_message(user_id: str, role: str, content: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    def _run():
        supabase = get_supabase()
        sid = session_id or str(uuid.uuid4())
        message_data = {
            "user_id": user_id,
            "role": role,
            "content": content[: settings.MAX_MESSAGE_LENGTH],
            "session_id": sid,
        }
        response = supabase.table("chat_messages").insert(message_data).execute()
        if not response.data:
            raise DatabaseException("save_message", "No data returned")
        return response.data[0]
    try:
        return with_retry("save_message", _run)
    except Exception as e:
        logger.error(f"Error saving message: {e}")
        raise DatabaseException("save_message", str(e))


def delete_chat_session(user_id: str, session_id: str) -> None:
    def _run():
        supabase = get_supabase()
        supabase.table("chat_messages").delete().eq("user_id", user_id).eq("session_id", session_id).execute()
        logger.info(f"Deleted session {session_id} for user {user_id}")
    try:
        with_retry("delete_chat_session", _run)
    except Exception as e:
        logger.error(f"Error deleting session {session_id}: {e}")
        raise DatabaseException("delete_session", str(e))


def delete_chat_history(user_id: str) -> None:
    def _run():
        supabase = get_supabase()
        supabase.table("chat_messages").delete().eq("user_id", user_id).execute()
        logger.info(f"Deleted chat history for user {user_id}")
    try:
        with_retry("delete_chat_history", _run)
    except Exception as e:
        logger.error(f"Error deleting chat history for {user_id}: {e}")
        raise DatabaseException("delete_chat_history", str(e))


# ── Course Operations ─────────────────────────────────────────────────────────

def search_courses(
    query: Optional[str] = None,
    subject: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """EGRESS FIX #12: selects only needed columns (~60-70% less data)."""
    def _run():
        supabase = get_supabase()
        db_query = supabase.table("courses").select(
            'Course, "Term Name", "Class Ave", "Class Ave.1", '
            "course_name, instructor, "
            "rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again"
        )
        if subject:
            db_query = db_query.like("Course", f"{subject.upper()}%")
        if query:
            clean_query = query.strip()[:100]
            # Escape LIKE wildcards to prevent pattern injection
            safe_query = clean_query.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
            db_query = db_query.or_(
                f"course_name.ilike.%{safe_query}%,"
                f"Course.ilike.%{safe_query}%"
            )
        return db_query.limit(limit).execute().data or []
    try:
        return with_retry("search_courses", _run)
    except Exception as e:
        raise DatabaseException(f"Database query failed: {str(e)}")


def get_course(course_code: str) -> List[Dict[str, Any]]:
    """EGRESS FIX #12: selects only needed columns."""
    def _run():
        supabase = get_supabase()
        return (
            supabase.table("courses")
            .select(
                'Course, "Term Name", "Class Ave", "Class Ave.1", '
                "course_name, instructor, "
                "rmp_rating, rmp_difficulty, rmp_num_ratings, rmp_would_take_again"
            )
            .eq("Course", course_code.upper())
            .execute()
            .data
            or []
        )
    try:
        return with_retry("get_course", _run)
    except Exception as e:
        raise DatabaseException(f"Database query failed: {str(e)}")


# ── Favorites Operations ──────────────────────────────────────────────────────

def get_favorites(user_id: str) -> List[Dict[str, Any]]:
    def _run():
        supabase = get_supabase()
        return (
            supabase.table("favorites")
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
            .data
            or []
        )
    try:
        return with_retry("get_favorites", _run)
    except Exception as e:
        logger.error(f"Error getting favorites for {user_id}: {e}")
        raise DatabaseException("get_favorites", str(e))


def add_favorite(
    user_id: str,
    course_code: str,
    course_title: str,
    subject: str,
    catalog: str,
) -> Dict[str, Any]:
    def _run():
        supabase = get_supabase()
        favorite_data: Dict[str, str] = {
            "user_id": user_id,
            "course_code": course_code,
            "course_title": course_title,
            "subject": subject,
            "catalog": catalog,
        }
        response = supabase.table("favorites").insert(favorite_data).execute()
        if not response.data:
            raise DatabaseException("add_favorite", "No data returned from insert")
        logger.info(f"Added favorite {course_code} for user {user_id}")
        return response.data[0]
    try:
        return with_retry("add_favorite", _run)
    except Exception as e:
        error_str = str(e)
        logger.error(f"Error adding favorite: {error_str}")
        if "duplicate key" in error_str.lower() or "23505" in error_str:
            raise DatabaseException("add_favorite", "Course already in favorites")
        raise DatabaseException("add_favorite", error_str)


def remove_favorite(user_id: str, course_code: str) -> None:
    def _run():
        supabase = get_supabase()
        supabase.table("favorites").delete().eq("user_id", user_id).eq("course_code", course_code).execute()
        logger.info(f"Removed favorite {course_code} for user {user_id}")
    try:
        with_retry("remove_favorite", _run)
    except Exception as e:
        logger.error(f"Error removing favorite: {e}")
        raise DatabaseException("remove_favorite", str(e))


def is_favorited(user_id: str, course_code: str) -> bool:
    def _run():
        supabase = get_supabase()
        response = (
            supabase.table("favorites")
            .select("id")
            .eq("user_id", user_id)
            .eq("course_code", course_code)
            .execute()
        )
        return len(response.data) > 0 if response.data else False
    try:
        return with_retry("is_favorited", _run)
    except Exception as e:
        logger.error(f"Error checking favorite: {e}")
        return False
