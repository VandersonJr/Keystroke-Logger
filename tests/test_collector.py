from app.database.connection import get_connection
from app.database import models
from app.collector.event_collector import collect


def test_password_context_not_stored():
    conn = get_connection(":memory:")
    sid, _ = models.start_session(conn, True)
    assert collect(conn, sid, {"event_type": "keydown", "key": "x", "context": "password"}) is False
    assert models.list_events(conn, sid) == []
