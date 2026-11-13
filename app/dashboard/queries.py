"""Consultas do painel. Todas parametrizadas (sem concatenar valores do usuário)."""
from dataclasses import dataclass
from datetime import date, timedelta

CATEGORIES = ("character", "special", "navigation", "function", "other")
PAGE_SIZE = 100
EXPORT_LIMIT = 50_000


@dataclass
class Filters:
    date_from: date | None = None
    date_to: date | None = None
    category: str = ""
    context: str = ""

    @property
    def active(self) -> bool:
        return bool(self.date_from or self.date_to or self.category or self.context)


def _parse_date(value):
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def parse_filters(args) -> Filters:
    category = args.get("category", "")
    return Filters(
        date_from=_parse_date(args.get("date_from")),
        date_to=_parse_date(args.get("date_to")),
        category=category if category in CATEGORIES else "",
        context=args.get("context", "").strip()[:64],
    )


def _where(f: Filters, session_id=None):
    clauses, params = [], []
    if session_id is not None:
        clauses.append("e.session_id = ?"); params.append(session_id)
    if f.date_from:
        clauses.append("e.timestamp >= ?"); params.append(f.date_from.isoformat())
    if f.date_to:  # inclusivo: < dia seguinte
        clauses.append("e.timestamp < ?"); params.append((f.date_to + timedelta(days=1)).isoformat())
    if f.category:
        clauses.append("e.key_category = ?"); params.append(f.category)
    if f.context:
        clauses.append("e.context = ?"); params.append(f.context)
    return (" WHERE " + " AND ".join(clauses)) if clauses else "", params


def list_sessions(conn, f: Filters, page: int = 1):
    where, params = _where(f)
    having = " HAVING total > 0" if f.active else ""
    sql = (
        "SELECT s.id, s.session_token, s.started_at, s.finished_at, COUNT(e.id) AS total "
        "FROM sessions s LEFT JOIN keyboard_events e ON e.session_id = s.id"
        + (where.replace(" WHERE ", " AND ") if where else "")
        + " GROUP BY s.id" + having + " ORDER BY s.id DESC LIMIT ? OFFSET ?"
    )
    return conn.execute(sql, params + [PAGE_SIZE, (max(page, 1) - 1) * PAGE_SIZE]).fetchall()


def get_session(conn, session_id: int):
    return conn.execute("SELECT * FROM sessions WHERE id = ?", (session_id,)).fetchone()


def totals(conn, f: Filters, session_id=None):
    where, params = _where(f, session_id)
    total = conn.execute(f"SELECT COUNT(*) FROM keyboard_events e{where}", params).fetchone()[0]
    by_cat = conn.execute(
        f"SELECT e.key_category AS name, COUNT(*) AS n FROM keyboard_events e{where} "
        "GROUP BY e.key_category ORDER BY n DESC", params).fetchall()
    by_ctx = conn.execute(
        f"SELECT e.context AS name, COUNT(*) AS n FROM keyboard_events e{where} "
        "GROUP BY e.context ORDER BY n DESC", params).fetchall()
    return {"total": total, "by_category": by_cat, "by_context": by_ctx}


def list_events(conn, f: Filters, session_id=None, page: int = 1, limit=PAGE_SIZE):
    where, params = _where(f, session_id)
    sql = (
        "SELECT e.id, s.session_token, e.event_type, e.key_category, e.context, e.timestamp "
        f"FROM keyboard_events e JOIN sessions s ON s.id = e.session_id{where} "
        "ORDER BY e.id LIMIT ? OFFSET ?"
    )
    return conn.execute(sql, params + [limit, (max(page, 1) - 1) * limit]).fetchall()


def log_access(conn, username, action, detail=""):
    from app.database.models import _now
    conn.execute(
        "INSERT INTO access_log (username, action, detail, timestamp) VALUES (?, ?, ?, ?)",
        ((username or "")[:64], action, (detail or "")[:200], _now()),
    )
    conn.commit()
