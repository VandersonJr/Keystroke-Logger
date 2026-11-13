import re
import pytest

from app.main import create_app
from app.database.connection import get_connection
from app.database import models
from app.dashboard import auth


@pytest.fixture
def env(tmp_path):
    db = str(tmp_path / "t.db")
    app = create_app(db)
    app.config["TESTING"] = True
    conn = get_connection(db)
    auth.create_user(conn, "alice", "senha-segura-123", "auditor")
    auth.create_user(conn, "root", "senha-admin-1234", "admin")
    auth._failures.clear()
    return app, conn


def login(client, user="alice", pw="senha-segura-123"):
    page = client.get("/dashboard/login").get_data(as_text=True)
    token = re.search(r'name="_csrf" value="([^"]+)"', page).group(1)
    return client.post("/dashboard/login", data={"username": user, "password": pw, "_csrf": token})


def seed(conn):
    sid, _ = models.start_session(conn, True)
    for et, cat, ctx in [("keydown", "character", "name"), ("keydown", "special", "name"),
                         ("keydown", "navigation", "notes")]:
        models.insert_event(conn, sid, {"event_type": et, "key_category": cat, "context": ctx})
    return sid


# CA-11
@pytest.mark.parametrize("path", ["/dashboard/", "/dashboard/sessions/1", "/dashboard/export.csv",
                                  "/dashboard/access-log"])
def test_unauthenticated_is_redirected(env, path):
    app, _ = env
    r = app.test_client().get(path)
    assert r.status_code == 302 and "/dashboard/login" in r.headers["Location"]


def test_password_is_hashed(env):
    _, conn = env
    h = conn.execute("SELECT password_hash FROM users WHERE username='alice'").fetchone()[0]
    assert "senha-segura-123" not in h and h.startswith(("scrypt:", "pbkdf2:"))


def test_login_ok_and_wrong_password(env):
    app, _ = env
    assert login(app.test_client()).status_code == 302
    assert login(app.test_client(), pw="errada-errada").status_code == 401


def test_login_requires_csrf(env):
    app, _ = env
    r = app.test_client().post("/dashboard/login", data={"username": "alice", "password": "senha-segura-123"})
    assert r.status_code == 400


def test_lockout_after_failures(env):
    app, _ = env
    c = app.test_client()
    for _ in range(auth.MAX_FAILS):
        login(c, pw="errada-errada")
    assert login(c).status_code == 429  # mesmo com a senha correta


# CA-13
def test_filters_and_totals(env):
    app, conn = env
    seed(conn)
    c = app.test_client(); login(c)
    html = c.get("/dashboard/sessions/1?category=special").get_data(as_text=True)
    assert "special" in html and "navigation" not in html.split("Por categoria")[1].split("Por contexto")[0]
    html = c.get("/dashboard/sessions/1?context=notes").get_data(as_text=True)
    assert ">1<" in html  # total = 1


def test_date_filter_excludes_other_days(env):
    app, conn = env
    seed(conn)
    c = app.test_client(); login(c)
    assert "Nenhuma sessão" in c.get("/dashboard/?date_from=2000-01-01&date_to=2000-01-02").get_data(as_text=True)
    assert "Nenhuma sessão" not in c.get("/dashboard/?date_from=2000-01-01").get_data(as_text=True)


def test_invalid_filters_are_ignored(env):
    app, conn = env
    seed(conn)
    c = app.test_client(); login(c)
    r = c.get("/dashboard/?date_from=abc&category=' OR 1=1 --&context=x")
    assert r.status_code == 200


def test_export_csv_has_no_key_values(env):
    app, conn = env
    seed(conn)
    c = app.test_client(); login(c)
    r = c.get("/dashboard/export.csv?category=character")
    text = r.get_data(as_text=True)
    assert r.mimetype == "text/csv"
    assert text.splitlines()[0] == "session_token,event_type,key_category,context,timestamp"
    assert len(text.splitlines()) == 2


def test_csv_injection_is_neutralized():
    from app.dashboard.routes import _csv_safe
    assert _csv_safe("=1+1").startswith("'") and _csv_safe("normal") == "normal"


def test_access_log_records_and_is_admin_only(env):
    app, conn = env
    seed(conn)
    c = app.test_client(); login(c)
    c.get("/dashboard/")
    assert c.get("/dashboard/access-log").status_code == 403
    actions = [r[0] for r in conn.execute("SELECT action FROM access_log")]
    assert "login_ok" in actions and "view_sessions" in actions
    a = app.test_client(); login(a, "root", "senha-admin-1234")
    assert a.get("/dashboard/access-log").status_code == 200


def test_context_must_be_safe_identifier():
    from app.security.data_sanitizer import sanitize_event
    assert sanitize_event({"event_type": "keydown", "key": "a", "context": "<script>"}) is None


def test_security_headers(env):
    app, _ = env
    r = app.test_client().get("/dashboard/login")
    assert r.headers["X-Frame-Options"] == "DENY" and r.headers["Cache-Control"] == "no-store"
