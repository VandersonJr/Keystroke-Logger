# Documento de requisitos

**Projeto:** Keystroke Logger (auditoria transparente de eventos de teclado)
**Versão:** 0.1 | **Status:** rascunho | **Etapa do roadmap:** 1

## 1. Objetivo

Registrar, armazenar e analisar **metadados** de eventos de teclado gerados dentro de uma
interface própria de testes, com consentimento explícito do usuário, para fins de auditoria
e aprendizado em cibersegurança.

## 2. Escopo

### 2.1 Dentro do escopo
- Interface web local com campos de demonstração.
- Coleta de eventos `keydown` e `keyup` ocorridos **somente** nessa interface.
- Classificação da tecla em categoria (caractere, especial, navegação, função, outra).
- Armazenamento local em SQLite, vinculado a uma sessão.
- Painel autenticado para consulta, filtros e relatórios (Etapa 4).
- Retenção e exclusão dos dados (Etapa 5).

### 2.2 Fora do escopo (proibido)
- Captura global ou em segundo plano de teclado.
- Interceptação de entrada de outros processos, janelas ou sistemas.
- Execução oculta, sem indicador visível, ou persistência após o encerramento da sessão.
- Registro do valor das teclas ou do texto digitado.
- Coleta de senhas, tokens, dados bancários ou conteúdo de campos sensíveis.
- Envio de dados para fora do ambiente local/controlado.

> Qualquer extensão para monitoramento de estações de trabalho reais é **outro projeto**,
> com base legal, política interna e ferramentas oficiais de auditoria (ver `collection-policy.md`, seção 9).

## 3. Perfis

| Perfil | Descrição | Permissões |
|---|---|---|
| Participante | Pessoa que usa a interface de testes | Ler o aviso, consentir, iniciar e encerrar a própria sessão |
| Auditor | Usuário autorizado a consultar registros | Ver sessões e metadados, filtrar, exportar relatórios |
| Administrador | Responsável técnico e pela política | Gerenciar auditores, definir retenção, executar exclusão |

## 4. Requisitos funcionais

| ID | Requisito | Prioridade |
|---|---|---|
| RF-01 | O sistema deve exibir aviso claro sobre o que é e o que não é coletado antes da sessão. | Alta |
| RF-02 | A sessão só pode ser iniciada após consentimento explícito (ação afirmativa). | Alta |
| RF-03 | Durante a sessão, deve haver indicador visual permanente de monitoramento ativo. | Alta |
| RF-04 | O participante deve poder encerrar a sessão a qualquer momento. | Alta |
| RF-05 | O coletor deve registrar `keydown` e `keyup` apenas em componentes marcados para auditoria na interface de testes. | Alta |
| RF-06 | Cada evento deve registrar: tipo, categoria da tecla, componente (contexto), data/hora e sessão. | Alta |
| RF-07 | O valor da tecla (ex.: "a", "7") nunca deve ser persistido. | Alta |
| RF-08 | Campos de senha e campos marcados como sensíveis não devem gerar evento algum. | Alta |
| RF-09 | O sistema deve registrar início, término e consentimento de cada sessão. | Alta |
| RF-10 | Após o encerramento, eventos enviados para a sessão devem ser rejeitados. | Alta |
| RF-11 | O painel deve listar sessões e eventos, com filtro por período, categoria e contexto. | Média |
| RF-12 | O painel deve exibir totais e permitir exportar relatório (CSV). | Média |
| RF-13 | O sistema deve permitir a exclusão de sessões vencidas conforme a política de retenção. | Média |

## 5. Requisitos não funcionais

| ID | Requisito |
|---|---|
| RNF-01 | **Minimização:** persistir apenas os campos listados em RF-06. |
| RNF-02 | **Controle de acesso:** painel exige autenticação; sem sessão autenticada, nenhum dado é exibido. |
| RNF-03 | **Senhas de acesso** do painel armazenadas somente com hash seguro (ex.: argon2 ou bcrypt). |
| RNF-04 | **Proteção dos dados:** arquivo `.db` fora do versionamento (`.gitignore`) e com permissão restrita ao usuário do serviço. |
| RNF-05 | **Integridade:** entradas validadas e consultas parametrizadas (sem SQL concatenado). |
| RNF-06 | **Transparência:** o código e a documentação devem deixar explícitos os limites de coleta. |
| RNF-07 | **Testabilidade:** regras de sanitização e encerramento cobertas por testes automatizados. |
| RNF-08 | **Rede:** o servidor escuta apenas em `127.0.0.1` por padrão. |
| RNF-09 | **Acessibilidade:** interface navegável por teclado, com foco visível e contraste adequado. |

## 6. Dados coletados e descartados

| Dado | Coletado? | Observação |
|---|---|---|
| Tipo do evento (`keydown`/`keyup`) | Sim | |
| Categoria da tecla | Sim | caractere, especial, navegação, função, outra |
| Componente de interface (contexto) | Sim | identificador do campo, sem o conteúdo dele |
| Data e hora do evento | Sim | UTC |
| Identificador da sessão | Sim | token aleatório, sem relação com identidade |
| Valor da tecla / texto digitado | **Não** | descartado antes da persistência |
| Conteúdo de campos sensíveis | **Não** | evento ignorado já no navegador e novamente no servidor |
| IP, nome de usuário do SO, hostname | **Não** | fora do escopo desta versão |

## 7. Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Reconstrução de texto a partir de temporização e sequência de eventos | Não guardar valores; avaliar reduzir granularidade de timestamp (ex.: segundos) e limitar retenção. |
| Uso indevido do painel | Autenticação, perfis, registro de acessos (log de auditoria do painel). |
| Vazamento do arquivo `.db` | Permissões restritas, backups protegidos, retenção curta. |
| Desvio de escopo (captura global) | Critério de aceite CA-12 e revisão de código obrigatória. |

## 8. Premissas
- Uso em ambiente próprio, controlado e autorizado.
- Participantes são informados e consentem antes de cada sessão.
- Python 3.11+, Flask e SQLite.
