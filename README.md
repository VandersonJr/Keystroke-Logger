# Keystroke Logger (auditoria transparente, ambiente de laboratório)

Coleta apenas metadados de eventos de teclado dentro da própria interface de testes,
com consentimento explícito, indicador visível e descarte de campos sensíveis.

## Executar
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python -m app.main        # http://127.0.0.1:5000
    pytest

## Limites
- Sem captura global ou oculta; só eventos desta página.
- O valor da tecla nunca é persistido, apenas a categoria.
- Próximos passos: dashboard autenticado (Etapa 4) e retenção/exclusão (Etapa 5).

## Painel (Etapa 4)
    python -m app.dashboard.create_user maria auditor   # cria usuário (pede a senha)
    set KEYLOGGER_SECRET_KEY=<valor-aleatório-longo>     # Windows (PowerShell: $env:KEYLOGGER_SECRET_KEY="...")
    python -m app.main                                  # http://127.0.0.1:5000/dashboard/
