# Critérios de aceite e plano de testes

**Etapa do roadmap:** 1 | **Referências:** `requirements.md`

Um requisito só é considerado atendido quando o critério correspondente passa.
Coluna **Tipo**: A = automatizado (pytest), M = manual, R = revisão de código.

## 1. Critérios de aceite

| ID | Dado / Quando / Então | Req. | Tipo |
|---|---|---|---|
| CA-01 | **Dado** que o consentimento não foi marcado, **quando** o participante tenta iniciar a sessão, **então** a sessão não é criada e uma mensagem informa a necessidade de consentimento. | RF-02 | A + M |
| CA-02 | **Dado** consentimento marcado, **quando** a sessão inicia, **então** o indicador de monitoramento aparece e permanece visível até o encerramento. | RF-03 | M |
| CA-03 | **Dado** sessão ativa, **quando** o participante digita no campo "Nome", **então** são gravados eventos com `context = name` e categoria correta. | RF-05, RF-06 | A + M |
| CA-04 | **Dado** sessão ativa, **quando** Enter, Shift, Ctrl ou Tab são pressionados, **então** a categoria é `special`. | RF-06 | A |
| CA-05 | **Dado** sessão ativa, **quando** setas, Home, End, PageUp ou PageDown são pressionados, **então** a categoria é `navigation`. | RF-06 | A |
| CA-06 | **Dado** qualquer evento gravado, **então** nenhuma coluna do banco contém o valor da tecla ou texto digitado. | RF-07 | A + R |
| CA-07 | **Dado** sessão ativa, **quando** o participante digita no campo de senha, **então** nenhum evento é enviado nem persistido. | RF-08 | A + M |
| CA-08 | **Dado** um evento com contexto sensível chegando diretamente à API, **então** o servidor o descarta. | RF-08 | A |
| CA-09 | **Dado** sessão ativa, **quando** o participante clica em "Encerrar sessão", **então** `finished_at` é preenchido e o indicador some. | RF-04, RF-09 | A + M |
| CA-10 | **Dado** sessão encerrada, **quando** novos eventos chegam à API, **então** são rejeitados e nada é gravado. | RF-10 | A |
| CA-11 | **Dado** usuário não autenticado, **quando** acessa qualquer rota do painel, **então** é redirecionado para o login e nenhum dado é exibido. | RNF-02 | A |
| CA-12 | **Dado** o código-fonte, **então** não existem hooks globais de teclado (ex.: `pynput`, `keyboard`, APIs do SO) nem listeners fora da interface de testes. | Escopo 2.2 | R |
| CA-13 | **Dado** o painel autenticado, **quando** o auditor aplica filtro por período e categoria, **então** somente eventos correspondentes são listados e os totais conferem. | RF-11 | A |
| CA-14 | **Dado** dados com idade superior à retenção definida, **quando** a rotina de exclusão roda, **então** sessões e eventos vencidos são removidos e os demais permanecem. | RF-13 | A |
| CA-15 | **Dado** o repositório, **então** arquivos `.db` não estão versionados e o servidor escuta em `127.0.0.1` por padrão. | RNF-04, RNF-08 | R |
| CA-16 | **Dado** consultas ao banco, **então** todas usam parâmetros (sem concatenação de strings). | RNF-05 | R |

## 2. Plano de testes manuais

| # | Procedimento | Resultado esperado |
|---|---|---|
| M1 | Abrir a página, não marcar o consentimento, clicar em "Iniciar sessão". | Mensagem de erro; campos continuam bloqueados. |
| M2 | Marcar consentimento e iniciar. | Indicador visível; campos liberados. |
| M3 | Digitar "teste" no campo Nome e pressionar Tab. | Eventos `character` e `special` no contexto `name`. |
| M4 | Digitar no campo de senha. | Nenhum evento novo no banco. |
| M5 | Encerrar a sessão e tentar digitar. | Indicador oculto; campos bloqueados; nenhum evento novo. |
| M6 | Inspecionar o banco com um cliente SQLite. | Nenhum valor de tecla ou texto digitado em nenhuma tabela. |

## 3. Matriz de rastreabilidade (resumo)

| Requisito | Critérios |
|---|---|
| RF-02 | CA-01 |
| RF-03 | CA-02 |
| RF-04 / RF-09 | CA-09 |
| RF-05 / RF-06 | CA-03, CA-04, CA-05 |
| RF-07 | CA-06 |
| RF-08 | CA-07, CA-08 |
| RF-10 | CA-10 |
| RF-11 | CA-13 |
| RF-13 | CA-14 |
| RNF-02 | CA-11 |
| Escopo (2.2) | CA-12 |

## 4. Definição de pronto (DoD) da Etapa 1
- [ ] `requirements.md` revisado e aprovado.
- [ ] `collection-policy.md` revisada por responsável de privacidade/jurídico, se houver uso real.
- [ ] Critérios CA-01 a CA-16 acordados.
- [ ] Testes automatizados correspondentes mapeados em `tests/` (os já existentes cobrem CA-01, 03, 04, 06, 07, 08, 10).
