import secrets
from datetime import datetime, timezone


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def start_session(conn, consent_given: bool):
    """Só inicia sessão com consentimento explícito."""
    if not consent_given:
        raise PermissionError("Consentimento é obrigatório para iniciar a sessão.")
    token = secrets.token_urlsafe(16)
    cur = conn.execute(
        "INSERT INTO sessions (session_token, consent_given, started_at) VALUES (?, 1, ?)",
        (token, _now()),
    )
    conn.commit()
    return cur.lastrowid, token


def finish_session(conn, session_id: int):
    conn.execute(
        "UPDATE sessions SET finished_at = ? WHERE id = ? AND finished_at IS NULL",
        (_now(), session_id),
    )
    conn.commit()


def session_is_active(conn, session_id: int) -> bool:
    row = conn.execute(
        "SELECT finished_at FROM sessions WHERE id = ?", (session_id,)
    ).fetchone()
    return row is not None and row["finished_at"] is None


def insert_event(conn, session_id: int, event: dict):
    conn.execute(
        "INSERT INTO keyboard_events (session_id, event_type, key_category, context, timestamp)"
        " VALUES (?, ?, ?, ?, ?)",
        (session_id, event["event_type"], event["key_category"], event["context"], _now()),
    )
    conn.commit()


def list_events(conn, session_id: int):
    return conn.execute(
        "SELECT * FROM keyboard_events WHERE session_id = ? ORDER BY id", (session_id,)
    ).fetchall()
