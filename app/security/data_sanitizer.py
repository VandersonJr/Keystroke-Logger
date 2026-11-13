"""Data Sanitizer: garante que nenhum conteúdo digitado seja persistido.

Regra central: só passam metadados (tipo do evento, categoria da tecla,
contexto, timestamp). O valor da tecla NUNCA é armazenado.
"""

import re

ALLOWED_EVENT_TYPES = {"keydown", "keyup"}
# Contexto = id de componente: só letras, números, _ e -.
CONTEXT_PATTERN = re.compile(r"^[A-Za-z0-9_-]{1,64}$")

SPECIAL_KEYS = {"Enter", "Shift", "Control", "Alt", "Meta", "Backspace",
                "Delete", "Escape", "CapsLock", "Tab"}
NAVIGATION_KEYS = {"ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
                   "Home", "End", "PageUp", "PageDown"}

# Contextos (ids de componente) que nunca podem gerar registro.
SENSITIVE_CONTEXTS = {"password", "token", "card_number", "cvv"}


def classify_key(key: str) -> str:
    """Converte a tecla em uma categoria. A tecla em si é descartada."""
    if key in NAVIGATION_KEYS:
        return "navigation"
    if key in SPECIAL_KEYS:
        return "special"
    if key.startswith("F") and key[1:].isdigit():
        return "function"
    if len(key) == 1:
        return "character"
    return "other"


def sanitize_event(raw: dict, sensitive_contexts=SENSITIVE_CONTEXTS):
    """Devolve um dict seguro, ou None se o evento deve ser descartado."""
    context = str(raw.get("context", ""))
    if not CONTEXT_PATTERN.match(context):
        return None
    if context in sensitive_contexts or raw.get("sensitive") is True:
        return None
    event_type = raw.get("event_type")
    if event_type not in ALLOWED_EVENT_TYPES:
        return None
    return {
        "event_type": event_type,
        "key_category": classify_key(str(raw.get("key", ""))),
        "context": context,
    }
