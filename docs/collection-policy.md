# Política de coleta e privacidade

**Projeto:** Keystroke Logger (auditoria transparente)
**Versão:** 0.1 | **Vigência:** a definir | **Responsável:** [nome / cargo]

> Documento técnico de referência. Não substitui parecer jurídico. Em uso corporativo real,
> a política deve ser revisada pelo jurídico e pelo encarregado de dados (DPO).

## 1. Finalidade
Registrar metadados de uso do teclado **dentro da interface de testes** para fins de auditoria
e aprendizado em segurança da informação. Nenhuma outra finalidade é permitida sem revisão
desta política e novo aviso aos participantes.

## 2. O que é coletado
- Tipo do evento (`keydown` ou `keyup`).
- Categoria da tecla (caractere, especial, navegação, função, outra).
- Componente da interface onde ocorreu o evento.
- Data e hora (UTC) e identificador aleatório da sessão.
- Registro de consentimento, início e término da sessão.

## 3. O que NÃO é coletado
- O texto digitado nem o valor de qualquer tecla.
- Senhas, tokens, dados bancários ou conteúdo de campos sensíveis.
- Qualquer entrada fora da interface de testes (outros aplicativos, janelas, navegador, sistema).
- Capturas de tela, áreas de transferência, arquivos, localização ou identificadores do dispositivo.

## 4. Transparência e consentimento
- Antes de cada sessão, o participante vê um aviso com os itens das seções 2 e 3.
- A sessão só inicia após ação afirmativa (marcar o consentimento e clicar em iniciar).
- Um indicador visível permanece ativo durante toda a sessão.
- O participante pode encerrar a sessão a qualquer momento, e a captura cessa imediatamente.
- O consentimento vale apenas para a sessão em que foi dado.

## 5. Base legal (LGPD)
Para sessões de laboratório: **consentimento** (art. 7º, I) do próprio participante.

Se houver uso corporativo com funcionários, atenção a estes pontos:
- Consentimento em relação de trabalho é frágil, pela assimetria entre as partes. Em geral
  avalia-se outra base, como o **legítimo interesse** (art. 7º, IX), com **teste de balanceamento** documentado.
- Deve-se avaliar um **Relatório de Impacto à Proteção de Dados (RIPD)**.
- A política deve ser comunicada previamente aos funcionários, de forma clara e acessível.
- Convém alinhamento com RH, jurídico e, se aplicável, representação dos trabalhadores.

## 6. Princípios aplicados (LGPD, art. 6º)

| Princípio | Como é atendido |
|---|---|
| Finalidade | Uso restrito à auditoria definida na seção 1. |
| Adequação | Coleta compatível com a finalidade informada. |
| Necessidade | Apenas metadados mínimos; valores de tecla descartados. |
| Livre acesso | Participante pode consultar os registros da própria sessão. |
| Qualidade | Registros gerados automaticamente, sem edição manual. |
| Transparência | Aviso prévio e indicador visível. |
| Segurança | Autenticação, permissões restritas, armazenamento local protegido. |
| Prevenção | Sanitização na origem e no servidor; testes automatizados. |
| Não discriminação | Dados não usados para decisões que prejudiquem pessoas. |
| Responsabilização | Log de acessos ao painel e documentação desta política. |

## 7. Acesso, segurança e retenção

**Acesso**
- Somente auditores autorizados acessam o painel, mediante autenticação.
- Todo acesso ao painel deve ser registrado (quem, quando, o quê).

**Segurança**
- Banco SQLite em local com permissão restrita ao serviço; fora do controle de versão.
- Backups, se existirem, recebem a mesma proteção do banco.
- Servidor escuta apenas em `127.0.0.1`, salvo decisão formal em contrário.

**Retenção** (valores iniciais, ajustáveis pelo responsável)

| Dado | Prazo | Ação ao fim do prazo |
|---|---|---|
| Eventos de teclado | 30 dias | Exclusão |
| Sessões (metadados e consentimento) | 90 dias | Exclusão |
| Log de acessos ao painel | 180 dias | Exclusão |

A exclusão é executada por rotina agendada ou manualmente pelo administrador e deve ser registrada.

## 8. Direitos dos participantes
O participante pode solicitar: confirmação do tratamento, acesso aos registros, eliminação
de seus dados e informação sobre com quem eles são compartilhados (não há compartilhamento
nesta versão). Canal de contato: [e-mail do responsável / DPO].

## 9. Uso corporativo: limites e caminho recomendado
Este projeto **não** implementa e **não** deve ser estendido para:
- captura global ou oculta de teclado em estações de trabalho;
- interceptação de entradas de outros processos ou sistemas;
- coleta de conteúdo digitado.

Para monitoramento corporativo real, o caminho recomendado é:
1. Definir finalidade, base legal e RIPD com jurídico e DPO.
2. Comunicar formalmente a política aos funcionários.
3. Usar mecanismos oficiais de auditoria e telemetria (logs de aplicação, SIEM, EDR,
   auditoria nativa de sistemas corporativos), configurados pelo administrador.
4. Preferir monitorar **eventos de segurança** (acessos, alterações, anomalias) em vez de entrada de teclado.

## 10. Incidentes
Suspeita de acesso indevido, vazamento do banco ou coleta fora do escopo deve ser comunicada
imediatamente ao responsável, com isolamento do ambiente e avaliação de comunicação à ANPD
e aos titulares, quando cabível.

## 11. Revisão
Esta política deve ser revisada a cada mudança de escopo, de finalidade ou de arquitetura,
e ao menos uma vez por ano.

| Versão | Data | Alteração |
|---|---|---|
| 0.1 | 11/11/2026 | Versão inicial |
