"""Event Collector: recebe eventos vindos SOMENTE da interface de testes."""
from app.security.data_sanitizer import sanitize_event
from app.database import models


def collect(conn, session_id: int, raw_event: dict) -> bool:
    """Sanitiza e persiste. Retorna True se gravou, False se descartou."""
    if not models.session_is_active(conn, session_id):
        return False  # sessão encerrada: captura interrompida
    safe = sanitize_event(raw_event)
    if safe is None:
        return False
    models.insert_event(conn, session_id, safe)
    return True
