import csv
import io
import secrets

from flask import (Blueprint, Response, abort, current_app, flash, g, redirect,
                   render_template, request, session, url_for)

from app.database.connection import get_connection
from app.dashboard import queries as q
from app.dashboard.auth import (admin_required, is_locked, login_required,
                                register_failure, reset_failures, verify_user)

bp = Blueprint("dashboard", __name__, url_prefix="/dashboard", template_folder="../templates")


def get_db():
    if "db" not in g:
        g.db = get_connection(current_app.config["DB_PATH"])
    return g.db


@bp.teardown_app_request
def close_db(exc):
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


@bp.after_request
def security_headers(resp):
    resp.headers["Cache-Control"] = "no-store"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Content-Security-Policy"] = "default-src 'self'; style-src 'self' 'unsafe-inline'"
    return resp


# --- CSRF simples para formulários POST ---
@bp.app_context_processor
def inject_csrf():
    def csrf_token():
        if "_csrf" not in session:
            session["_csrf"] = secrets.token_urlsafe(32)
        return session["_csrf"]
    return {"csrf_token": csrf_token, "categories": q.CATEGORIES}


def check_csrf():
    sent = request.form.get("_csrf", "")
    if not sent or not secrets.compare_digest(sent, session.get("_csrf", "")):
        abort(400)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        check_csrf()
        username = request.form.get("username", "").strip()[:64]
        password = request.form.get("password", "")
        conn = get_db()
        if is_locked(username):
            q.log_access(conn, username, "login_locked")
            flash("Muitas tentativas. Aguarde alguns minutos.")
            return render_template("login.html"), 429
        user = verify_user(conn, username, password)
        if user is None:
            register_failure(username)
            q.log_access(conn, username, "login_failed")
            flash("Usuário ou senha inválidos.")
            return render_template("login.html"), 401
        reset_failures(username)
        session.clear()  # evita fixação de sessão
        session["user_id"], session["username"], session["role"] = user["id"], user["username"], user["role"]
        q.log_access(conn, username, "login_ok")
        return redirect(url_for("dashboard.index"))
    return render_template("login.html")


@bp.post("/logout")
@login_required
def logout():
    check_csrf()
    q.log_access(get_db(), session.get("username"), "logout")
    session.clear()
    return redirect(url_for("dashboard.login"))


@bp.get("/")
@login_required
def index():
    f, page = q.parse_filters(request.args), request.args.get("page", 1, type=int)
    conn = get_db()
    q.log_access(conn, session["username"], "view_sessions", request.query_string.decode()[:200])
    return render_template("sessions.html", sessions=q.list_sessions(conn, f, page),
                           totals=q.totals(conn, f), f=f, page=page, args=request.args)


@bp.get("/sessions/<int:sid>")
@login_required
def session_detail(sid):
    conn = get_db()
    sess = q.get_session(conn, sid)
    if sess is None:
        abort(404)
    f, page = q.parse_filters(request.args), request.args.get("page", 1, type=int)
    q.log_access(conn, session["username"], "view_session", f"id={sid}")
    return render_template("session_detail.html", sess=sess, f=f, page=page, args=request.args,
                           events=q.list_events(conn, f, sid, page), totals=q.totals(conn, f, sid))


def _csv_safe(value):
    """Evita injeção de fórmulas ao abrir o CSV no Excel/Sheets."""
    value = "" if value is None else str(value)
    return "'" + value if value[:1] in ("=", "+", "-", "@", "\t", "\r") else value


@bp.get("/export.csv")
@login_required
def export_csv():
    f = q.parse_filters(request.args)
    sid = request.args.get("session_id", type=int)
    conn = get_db()
    rows = q.list_events(conn, f, sid, page=1, limit=q.EXPORT_LIMIT)
    q.log_access(conn, session["username"], "export_csv", f"session={sid} rows={len(rows)}")
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["session_token", "event_type", "key_category", "context", "timestamp"])
    for r in rows:
        w.writerow([_csv_safe(r[k]) for k in
                    ("session_token", "event_type", "key_category", "context", "timestamp")])
    return Response(buf.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=audit_report.csv"})


@bp.get("/access-log")
@admin_required
def access_log():
    rows = get_db().execute(
        "SELECT username, action, detail, timestamp FROM access_log ORDER BY id DESC LIMIT 200"
    ).fetchall()
    return render_template("access_log.html", rows=rows)
