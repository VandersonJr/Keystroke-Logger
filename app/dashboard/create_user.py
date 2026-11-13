"""Uso: python -m app.dashboard.create_user <usuario> [auditor|admin]"""
import getpass
import sys

from app.database.connection import get_connection
from app.dashboard.auth import create_user


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    username = sys.argv[1]
    role = sys.argv[2] if len(sys.argv) > 2 else "auditor"
    password = getpass.getpass("Senha (mín. 10 caracteres): ")
    if password != getpass.getpass("Repita a senha: "):
        sys.exit("As senhas não conferem.")
    try:
        create_user(get_connection(), username, password, role)
    except (ValueError, Exception) as e:
        sys.exit(f"Erro: {e}")
    print(f"Usuário '{username}' ({role}) criado.")


if __name__ == "__main__":
    main()
