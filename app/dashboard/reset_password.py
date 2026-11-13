"""Uso: python -m app.dashboard.reset_password <usuario>"""
import getpass
import sys

from werkzeug.security import generate_password_hash

from app.database.connection import get_connection
from app.dashboard.auth import MIN_PASSWORD_LEN
from app.dashboard.queries import log_access


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    username = sys.argv[1]
    conn = get_connection()
    if not conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone():
        sys.exit("Usuário não encontrado.")
    password = getpass.getpass(f"Nova senha (mín. {MIN_PASSWORD_LEN} caracteres): ")
    if len(password) < MIN_PASSWORD_LEN:
        sys.exit("Senha muito curta.")
    if password != getpass.getpass("Repita a senha: "):
        sys.exit("As senhas não conferem.")
    conn.execute("UPDATE users SET password_hash = ? WHERE username = ?",
                 (generate_password_hash(password), username))
    conn.commit()
    log_access(conn, username, "password_reset_cli")
    print(f"Senha de '{username}' redefinida.")


if __name__ == "__main__":
    main()