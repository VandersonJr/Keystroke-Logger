# ⌨️ Keystroke Logger

### Auditoria transparente de eventos de teclado em ambiente controlado

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)](https://flask.palletsprojects.com/)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Tests](https://img.shields.io/badge/Tests-Pytest-brightgreen?logo=pytest)](https://docs.pytest.org/)

O **Keystroke Logger** é um projeto educacional desenvolvido em Python para estudar monitoramento de eventos, auditoria de aplicações, sanitização de dados, persistência em banco de dados e segurança da informação.

A aplicação registra exclusivamente metadados de eventos de teclado produzidos dentro de uma interface própria de laboratório. Seu funcionamento depende de consentimento explícito, apresenta um indicador visual durante a coleta e descarta informações provenientes de campos sensíveis.

> **Importante:** este projeto não realiza captura global ou oculta de teclado. Não registra o texto digitado, não monitora outros aplicativos e não coleta credenciais.

---

## 📌 Sumário

- [Objetivos](#-objetivos)
- [Funcionalidades](#-funcionalidades-implementadas)
- [Fluxo de funcionamento](#-fluxo-de-funcionamento)
- [Tecnologias](#-tecnologias-utilizadas)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Instalação](#-instalação-e-configuração)
- [Execução](#-executando-a-aplicação)
- [Painel de auditoria](#-painel-de-auditoria)
- [Banco de dados](#-banco-de-dados)
- [Testes](#-testes-automatizados)
- [Segurança e privacidade](#-segurança-e-privacidade)
- [Roadmap](#-roadmap)
- [Histórico de desenvolvimento](#-histórico-de-desenvolvimento)
- [Finalidade educacional](#-finalidade-educacional)

---

## 🎯 Objetivos

O projeto foi concebido para explorar conceitos de cibersegurança e desenvolvimento seguro por meio da construção de uma ferramenta de auditoria de eventos de teclado.

Seus principais objetivos são:

- Compreender o funcionamento dos eventos `keydown` e `keyup`.
- Implementar coleta restrita a uma interface controlada.
- Classificar eventos sem armazenar o conteúdo digitado.
- Aplicar técnicas de sanitização e minimização de dados.
- Implementar persistência local com SQLite.
- Desenvolver um painel para consulta dos registros.
- Aplicar autenticação, controle de acesso e mecanismos de proteção.
- Documentar requisitos, critérios de aceite e política de coleta.

## ⚙️ Funcionalidades implementadas

### 1. Interface de laboratório

A aplicação disponibiliza uma interface própria para realização dos testes.

Antes de iniciar uma sessão, o participante recebe informações sobre os dados coletados e precisa conceder autorização expressa.

Durante a sessão:

- Os campos de demonstração são habilitados.
- Um indicador visual informa que o monitoramento está ativo.
- O participante pode encerrar a sessão a qualquer momento.
- A coleta fica restrita aos componentes identificados para auditoria.

### 2. Event Collector

O módulo `Event Collector` recebe e processa os eventos originados na interface de laboratório.

São reconhecidos dois tipos de eventos:

- `keydown`: pressionamento de uma tecla.
- `keyup`: liberação de uma tecla.

As teclas são classificadas em categorias:

| Categoria | Exemplos |
|---|---|
| `character` | Letras, números e caracteres individuais |
| `special` | Enter, Shift, Ctrl, Alt e Tab |
| `navigation` | Setas, Home, End, PageUp e PageDown |
| `function` | F1, F2, F5 e demais teclas de função |
| `other` | Teclas não classificadas nas categorias anteriores |

O valor original da tecla é utilizado somente para determinar sua categoria e não é persistido.

### 3. Data Sanitizer

O módulo `Data Sanitizer` aplica regras de segurança antes que os eventos sejam armazenados.

Entre suas responsabilidades estão:

- Validar os tipos de eventos recebidos.
- Validar os identificadores dos componentes da interface.
- Classificar as teclas.
- Descartar eventos provenientes de campos sensíveis.
- Impedir que valores de teclas ou textos digitados sejam incluídos nos registros.

Campos identificados como sensíveis, incluindo campos de senha, são excluídos da coleta. A sanitização também é realizada no servidor, evitando depender exclusivamente das validações executadas no navegador.

### 4. Persistência com SQLite

Os registros são armazenados localmente em um banco SQLite.

A estrutura contempla tabelas para:

| Tabela | Responsabilidade |
|---|---|
| `sessions` | Informações das sessões e consentimento |
| `keyboard_events` | Metadados dos eventos |
| `users` | Usuários autorizados do painel |
| `access_log` | Atividades realizadas no painel |

Cada evento é associado à sessão correspondente, permitindo consultas e análises posteriores.

### 5. Dashboard de auditoria

O projeto conta com um painel de consulta desenvolvido com Flask.

Entre os recursos implementados estão:

- Autenticação de usuários.
- Perfis de acesso `auditor` e `admin`.
- Listagem e detalhamento de sessões.
- Consulta dos eventos registrados.
- Filtros por período, categoria e contexto.
- Apresentação de totais e agrupamentos.
- Exportação dos registros em CSV.
- Registro de acessos e atividades administrativas.
- Restrição do acesso ao histórico de auditoria para administradores.

### 6. Segurança da autenticação

O mecanismo de autenticação contempla:

- Armazenamento de senhas utilizando hash.
- Proteção contra tentativas excessivas de login.
- Validação CSRF nos formulários de autenticação.
- Proteção contra fixação de sessão.
- Cabeçalhos HTTP de segurança.
- Registro de tentativas de acesso.
- Funcionalidade para exibir ou ocultar a senha na tela de login.

---

## 🔄 Fluxo de funcionamento

O processamento está organizado em módulos com responsabilidades específicas:

```text
┌──────────────────────────────┐
│      Interface de Testes     │
│       (Laboratório Web)      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Event Collector      │
│     Recepção dos eventos     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Data Sanitizer       │
│  Validação e classificação   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│         Storage Layer        │
│            SQLite            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│           Dashboard          │
│  Consultas, filtros e CSV    │
└──────────────────────────────┘
```

A separação permite que cada componente tenha uma responsabilidade específica, reduzindo o acoplamento entre coleta, segurança, armazenamento e visualização dos registros.

## 🛠️ Tecnologias utilizadas

| Tecnologia | Aplicação |
|---|---|
| Python | Linguagem principal |
| Flask | Servidor e aplicação web |
| SQLite | Banco de dados local |
| HTML5 | Estrutura das interfaces |
| CSS3 | Estilização das interfaces |
| JavaScript | Manipulação dos eventos da interface |
| Pytest | Testes automatizados |
| Git e GitHub | Controle de versão e hospedagem do código |

Bibliotecas e módulos relevantes:

- `Flask`: criação das rotas e gerenciamento da aplicação.
- `Werkzeug`: geração e validação de hashes de senhas.
- `sqlite3`: conexão e operações no banco de dados.
- `pytest`: execução dos testes automatizados.

---

## 📁 Estrutura do projeto

Estrutura lógica dos principais módulos:

```text
Keystroke-Logger/
│
├── app/
│   ├── collector/
│   │   └── event_collector.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   │
│   ├── dashboard/
│   │   ├── auth.py
│   │   ├── create_user.py
│   │   ├── queries.py
│   │   └── routes.py
│   │
│   ├── security/
│   │   └── data_sanitizer.py
│   │
│   ├── static/
│   │   └── login.js
│   │
│   ├── templates/
│   │   ├── lab.html
│   │   ├── login.html
│   │   ├── sessions.html
│   │   └── session_detail.html
│   │
│   └── main.py
│
├── docs/
│   ├── requirements.md
│   ├── acceptance-criteria.md
│   └── collection-policy.md
│
├── tests/
│   ├── test_collector.py
│   ├── test_dashboard.py
│   └── test_sanitizer.py
│
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
```

Arquivos de banco de dados e outros dados locais são gerados durante a execução e não devem ser versionados.

---

## 🚀 Instalação e configuração

### Pré-requisitos

- Python instalado.
- Git instalado.
- Terminal ou PowerShell.
- Editor de código de sua preferência.

### 1. Clonar o repositório

```bash
git clone https://github.com/VandersonJr/Keystroke-Logger.git
cd Keystroke-Logger
```

### 2. Criar o ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

No Linux ou macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Executando a aplicação

Com o ambiente virtual ativado, execute:

```bash
python -m app.main
```

A aplicação é disponibilizada localmente, por padrão, em:

```text
http://127.0.0.1:5000
```

A interface de laboratório fica disponível na página inicial.

### Realizando um teste

1. Acesse a interface de laboratório.
2. Leia o aviso sobre os dados coletados.
3. Marque a opção de consentimento.
4. Clique em **Iniciar sessão**.
5. Realize os testes nos campos de demonstração.
6. Clique em **Encerrar sessão** para finalizar o monitoramento.

Os eventos são processados e armazenados no banco SQLite local.

---

## 🔐 Painel de auditoria

O painel administrativo está disponível em:

```text
http://127.0.0.1:5000/dashboard/
```

Antes do primeiro acesso, é necessário criar um usuário autorizado.

### Criar usuário

Para criar um auditor:

```bash
python -m app.dashboard.create_user maria auditor
```

Para criar um administrador:

```bash
python -m app.dashboard.create_user administrador admin
```

O programa solicitará a senha e sua confirmação pelo terminal. As senhas devem possuir pelo menos 10 caracteres.

### Configurar a chave secreta

A aplicação utiliza a variável de ambiente `KEYLOGGER_SECRET_KEY` para proteger as sessões do Flask.

No PowerShell:

```powershell
$env:KEYLOGGER_SECRET_KEY="sua-chave-aleatoria-longa"
```

No CMD:

```cmd
set KEYLOGGER_SECRET_KEY=sua-chave-aleatoria-longa
```

No Linux ou macOS:

```bash
export KEYLOGGER_SECRET_KEY="sua-chave-aleatoria-longa"
```

Utilize uma chave aleatória, longa e exclusiva. Não compartilhe nem versione essa chave.

Depois, inicie a aplicação:

```bash
python -m app.main
```

Acesse o painel e autentique-se com as credenciais cadastradas.

---

## 🗄️ Banco de dados

O projeto utiliza SQLite para armazenar os dados localmente.

O banco é inicializado pela aplicação, conforme a configuração definida no módulo de conexão.

### Modelo de dados

**Tabela `sessions`**

Armazena os dados de cada sessão de auditoria, incluindo identificador, token, consentimento e horários de início e encerramento.

**Tabela `keyboard_events`**

Armazena os metadados dos eventos, incluindo identificador, sessão relacionada, tipo do evento, categoria, contexto e horário.

**Tabela `users`**

Armazena os usuários autorizados, hash da senha, perfil de acesso e data de criação.

**Tabela `access_log`**

Mantém o histórico de atividades do painel, incluindo usuário, ação, detalhes e horário.

---

## 🧪 Testes automatizados

O projeto utiliza Pytest para validar os principais mecanismos de coleta, sanitização e autenticação.

Para executar todos os testes:

```bash
pytest
```

Para obter uma saída mais detalhada:

```bash
pytest -v
```

### Cenários contemplados

| Área | Validações |
|---|---|
| Coletor | Descarte de eventos provenientes de campos de senha |
| Sanitização | Campos sensíveis, categorias, tipos de evento e valor original da tecla |
| Autenticação | Login, hash de senha e tentativas inválidas |
| Proteção CSRF | Rejeição de formulários sem token válido |
| Controle de acesso | Redirecionamento de usuários não autenticados e restrição por perfil |
| Consultas | Filtros, totais e tratamento de parâmetros inválidos |
| Exportação | Formato CSV e neutralização de fórmulas |
| Auditoria | Registro de atividades e cabeçalhos de segurança |

Os testes podem ser ampliados conforme a implementação das próximas etapas do roadmap.

---

## 🛡️ Segurança e privacidade

A segurança e a privacidade são requisitos centrais da arquitetura.

O projeto considera princípios de proteção de dados, como finalidade, necessidade, transparência, segurança e prevenção.

### Dados coletados

- Tipo do evento (`keydown` ou `keyup`).
- Categoria da tecla.
- Identificador do componente utilizado.
- Data e hora do evento.
- Identificador da sessão.
- Informações de consentimento e duração da sessão.

### Dados que não são coletados

- Texto digitado.
- Valor original das teclas.
- Senhas e credenciais.
- Conteúdo de campos sensíveis.
- Entradas realizadas em outros aplicativos ou processos.
- Capturas de tela ou conteúdo da área de transferência.

### Medidas de proteção implementadas

- Consentimento explícito antes de cada sessão.
- Indicador visual durante o monitoramento.
- Sanitização dos eventos no navegador e no servidor.
- Restrição de acesso ao painel por autenticação.
- Hash de senhas.
- Proteção CSRF.
- Consultas parametrizadas no banco de dados.
- Registro de atividades administrativas.
- Neutralização de fórmulas potencialmente perigosas na exportação CSV.
- Execução local em `127.0.0.1` por padrão.

### Limites de utilização

Este projeto foi desenvolvido exclusivamente para fins educacionais e testes autorizados.

Não deve ser utilizado para captura oculta, monitoramento global de teclado, interceptação de entradas de outros processos ou coleta de credenciais.

Para auditoria de ambientes corporativos reais, devem ser utilizados mecanismos oficiais de telemetria, auditoria de sistemas e monitoramento de segurança, mediante autorização e avaliação jurídica apropriada.

---

## 🗺️ Roadmap

O desenvolvimento segue o planejamento documentado em `docs/`.

| Etapa | Descrição | Situação |
|---|---|---|
| 1 | Planejamento, requisitos, critérios de aceite e política de coleta | Documentada |
| 2 | Interface de testes e captura restrita de eventos | Implementada |
| 3 | Sanitização e persistência em SQLite | Implementada |
| 4 | Dashboard, autenticação, filtros e relatórios | Implementada |
| 5 | Segurança, retenção, exclusão e validação final | Em evolução |

### Próximas melhorias

- Implementar rotina automatizada de retenção e exclusão de registros.
- Ampliar a cobertura dos testes de segurança.
- Revisar e fortalecer o controle de acesso aos arquivos de dados.
- Aprimorar a documentação técnica da arquitetura.
- Validar integralmente os critérios de aceite definidos em `docs/acceptance-criteria.md`.
- Revisar a política de coleta e privacidade conforme a evolução do projeto.

A implementação de cada melhoria deverá respeitar os limites de coleta definidos desde o planejamento inicial.

---

## 📝 Histórico de desenvolvimento

O projeto utiliza Git e GitHub para controle de versão e acompanhamento de sua evolução.

O histórico recente inclui alterações na interface de autenticação, como:

- Reformulação visual da tela de login do painel.
- Implementação do recurso de exibir ou ocultar a senha.
- Utilização de JavaScript externo para manter a compatibilidade com a política de segurança de conteúdo (CSP).

Consulte o histórico completo de alterações:

[Visualizar commits do projeto](https://github.com/VandersonJr/Keystroke-Logger/commits/main)

---

## 🎓 Finalidade educacional

O Keystroke Logger é um projeto de estudo em desenvolvimento seguro e cibersegurança.

Durante sua construção são explorados conceitos importantes:

- **System Monitoring:** acompanhamento de eventos em uma aplicação.
- **Event Logging:** estruturação e persistência de registros.
- **Data Sanitization:** filtragem e minimização de dados.
- **Database Security:** proteção e controle de acesso aos registros.
- **Application Security:** desenvolvimento seguro de aplicações.
- **Security Auditing:** análise de atividades e produção de evidências.

O objetivo é compreender como ferramentas de auditoria podem ser construídas de maneira transparente, controlada e respeitando a privacidade dos participantes.

---

**Desenvolvido por Vanderson Jr.**

[GitHub – VandersonJr](https://github.com/VandersonJr)

[Repositório – Keystroke Logger](https://github.com/VandersonJr/Keystroke-Logger)

*Projeto educacional de cibersegurança. Utilização restrita a ambientes próprios, controlados e autorizados.*
