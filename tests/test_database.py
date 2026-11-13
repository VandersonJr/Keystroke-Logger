import pytest
from app.database.connection import get_connection
from app.database import models
from app.collector.event_collector import collect


def test_requires_consent():
    conn = get_connection(":memory:")
    with pytest.raises(PermissionError):
        models.start_session(conn, False)


def test_stops_after_finish():
    conn = get_connection(":memory:")
    sid, _ = models.start_session(conn, True)
    raw = {"event_type": "keydown", "key": "a", "context": "name"}
    assert collect(conn, sid, raw) is True
    models.finish_session(conn, sid)
    assert collect(conn, sid, raw) is False
    assert len(models.list_events(conn, sid)) == 1
