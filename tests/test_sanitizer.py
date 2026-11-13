from app.security.data_sanitizer import sanitize_event


def test_password_field_is_discarded():
    assert sanitize_event({"event_type": "keydown", "key": "a", "context": "password"}) is None


def test_sensitive_flag_is_discarded():
    assert sanitize_event({"event_type": "keydown", "key": "a", "context": "name", "sensitive": True}) is None


def test_key_value_is_never_kept():
    out = sanitize_event({"event_type": "keydown", "key": "a", "context": "name"})
    assert out == {"event_type": "keydown", "key_category": "character", "context": "name"}


def test_categories():
    f = lambda k: sanitize_event({"event_type": "keydown", "key": k, "context": "name"})["key_category"]
    assert f("Enter") == "special"
    assert f("Tab") == "special"
    assert f("ArrowLeft") == "navigation"
    assert f("F5") == "function"


def test_invalid_event_type():
    assert sanitize_event({"event_type": "paste", "key": "a", "context": "name"}) is None
