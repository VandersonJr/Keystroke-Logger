"""Autenticação do painel: hash de senha, perfis e bloqueio por tentativas."""
import time
from datetime import datetime, timezone
from functools import wraps

from flask import redirect, session, url_for, abort
from werkzeug.security import check_password_hash, generate_password_hash

ROLES = ("auditor", "admin")
MIN_PASSWORD_LEN = 10
MAX_FAILS = 5
LOCK_SECONDS = 300

_failures: dict = {}  # username -> (contagem, instante da primeira falha)
# Hash fictício para igualar o tempo de resposta quando o usuário não existe.
_DUMMY_HASH = generate_password_hash("dummy-password-for-timing")


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def create_user(conn, username: str, password: str, role: str = "auditor"):
    username = (username or "").strip()
    if not (3 <= len(username) <= 64):
        raise ValueError("Usuário deve ter entre 3 e 64 caracteres.")
    if len(password or "") < MIN_PASSWORD_LEN:
        raise ValueError(f"Senha deve ter ao menos {MIN_PASSWORD_LEN} caracteres.")
    if role not in ROLES:
        raise ValueError("Perfil inválido.")
    conn.execute(
        "INSERT INTO users (username, password_hash, role, created_at) VALUES (?, ?, ?, ?)",
        (username, generate_password_hash(password), role, _now()),
    )
    conn.commit()


def is_locked(username: str) -> bool:
    count, first = _failures.get(username, (0, 0))
    if count >= MAX_FAILS and time.time() - first < LOCK_SECONDS:
        return True
    if count >= MAX_FAILS:
        _failures.pop(username, None)
    return False


def register_failure(username: str):
    count, first = _failures.get(username, (0, time.time()))
    _failures[username] = (count + 1, first)


def reset_failures(username: str):
    _failures.pop(username, None)


def verify_user(conn, username: str, password: str):
    """Retorna a linha do usuário se as credenciais forem válidas; senão None."""
    row = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    stored = row["password_hash"] if row else _DUMMY_HASH
    ok = check_password_hash(stored, password or "")
    return row if (row and ok) else None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("dashboard.login"))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin":
            abort(403)
        return view(*args, **kwargs)
    return wrapped
