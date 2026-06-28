# Arquitetura do Damon

## Visão Geral

```
┌─────────────────────────────────────────────────────────────────┐
│                        DAMON AGENT                               │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │   CLI/TUI    │  │   Gateway    │  │   Desktop (Electron) │  │
│  │  (prompt-    │  │  (Telegram,  │  │   React + Electron   │  │
│  │   toolkit)   │  │  Discord,    │  │   Fala com backend   │  │
│  └──────┬───────┘  │  WhatsApp,   │  │   do dashboard       │  │
│         │          │  Slack...)   │  └──────────┬───────────┘  │
│         └──────────┼──────────────┼────────────┘              │
│                    ▼              ▼                           │
│         ┌─────────────────────────────────────┐               │
│         │        AIAgent (Core Loop)          │ ◄── Sessão    │
│         │  ┌─────────────────────────────┐    │     Stateful  │
│         │  │ Construtor de System Prompt │    │        │      │
│         │  │  - Identidade, Skills, Mem. │    │        │      │
│         │  │  - Context Files, Tools     │    │        ▼      │
│         │  └──────────────┬──────────────┘    │  ┌────────┐   │
│         │                 │                   │  │ SQLite │   │
│         │                 ▼                   │  │ state  │   │
│         │  ┌─────────────────────────────┐    │  │  .db   │   │
│         │  │ Registry & Dispatcher Tools │    │  │ (FTS5) │   │
│         │  │  - 40+ tools, toolsets      │    │  └────────┘   │
│         │  │  - terminal, web, browser,  │           │       │
│         │  │    coding, media, skills    │           │       │
│         │  └──────────────┬──────────────┘           │       │
│         │                 │                          │       │
│         │                 ▼                          │       │
│         │  ┌─────────────────────────────┐           │       │
│         │  │ Compressão de Contexto      │           │       │
│         │  │ (auto-sumarização)          │           │       │
│         │  └─────────────────────────────┘           │       │
│         └─────────────────────────────────────┘      │       │
│                    │                                 │       │
│                    ▼                                 │       │
│         ┌─────────────────────────────────────┐      │       │
│         │        Abstração de Provedor LLM    │      │       │
│         │  OpenRouter / NovitaAI / NVIDIA /   │      │       │
│         │  OpenAI / Anthropic / Custom / Local│      │       │
│         └─────────────────────────────────────┘      │       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
         ┌─────────────────────────────────────────┐
         │           CAMADA DE EXECUÇÃO            │
         │  ┌─────────┐ ┌─────────┐ ┌───────────┐ │
         │  │ Local   │ │ Docker  │ │ SSH       │ │
         │  │ Backend │ │ Backend │ │ Backend   │ │
         │  └─────────┘ └─────────┘ └───────────┘ │
         │  ┌─────────┐ ┌─────────┐ ┌───────────┐ │
         │  │ Singu-  │ │ Modal   │ │ Daytona   │ │
         │  │ larity  │ │(server- │ │ (server-  │ │
         │  │         │ │ less)   │ │ less)     │ │
         │  └─────────┘ └─────────┘ └───────────┘ │
         └─────────────────────────────────────────┘
```

---

## Core Loop (`agent/conversation_loop.py`)

```python
async def _run_agent_loop(self, user_message: str) -> str:
    while True:
        # 1. Monta system prompt (identidade + skills + memória + tools)
        system_prompt = await self._build_system_prompt()
        
        # 2. Monta kwargs da API (model, messages, tools, reasoning)
        api_kwargs = self._build_api_kwargs(system_prompt, user_message)
        
        # 3. Chama LLM
        response = await self._call_llm(api_kwargs)
        
        # 4. Se tool_calls → executa cada um via registry
        if response.tool_calls:
            for tool_call in response.tool_calls:
                result = await self.tool_registry.dispatch(tool_call)
                conversation.add_tool_result(tool_call.id, result)
            continue  # Volta para LLM com resultados das tools
        
        # 5. Se resposta de texto → persiste + retorna
        if response.text:
            await self.session_db.persist(conversation)
            return response.text
        
        # 6. Compressão de contexto se próximo do limite
        if self._approaching_token_limit():
            await self._compress_context()
```

---

## Componentes Principais

| Módulo | Responsabilidade |
|--------|------------------|
| `agent/conversation_loop.py` | Loop principal, dispatch de tools, compressão |
| `agent/prompt_builder.py` | Monta system prompt (skills, memória, tools, contexto) |
| `agent/tool_registry.py` | Registry auto-descoberta, schemas, dispatch, toolsets |
| `agent/context_compressor.py` | Sumarização automática ao limite de tokens |
| `damon_state.py` | SQLite + FTS5: sessões, busca full-text, títulos |
| `damon_cli/config.py` | Configuração, migração, env vars, profiles |
| `damon_cli/main.py` | Entry point, arg parsing, command dispatch |
| `gateway/run.py` | GatewayRunner: plataformas, routing, cron, webhooks |

---

## Sistema de Tools

- **Auto-registro:** Cada `tools/*.py` chama `registry.register()` no import
- **Toolsets:** Grupos (`core`, `terminal`, `web`, `browser`, `coding`, `media`, `skills`)
- **Check functions:** `check_fn` valida dependências antes de expor tool
- **Terminal backends:** `Local`, `Docker`, `SSH`, `Singularity`, `Modal`, `Daytona` — ABC comum

---

## Sistema de Memória

```
~/.damon/
├── memories/
│   ├── MEMORY.md      # Fatos extraídos pelo agente (auto)
│   └── USER.md        # Perfil do usuário (manual)
├── state.db           # SQLite: sessões, messages, índice FTS5
├── sessions/
│   ├── sessions.json  # Routing index (gateway)
│   └── *.jsonl        # Transcripts (opcional)
└── cron/              # Jobs agendados
```

---

## Arquitetura do Gateway

- **Platform adapters** em `gateway/platforms/` (Telegram, Discord, WhatsApp, Slack, Signal, Email)
- **Unified session store** — mesmo `AIAgent` para CLI e gateway
- **Webhook server** — recebe GitHub events, alertas custom
- **Cron scheduler** — jobs com delivery multiplataforma
- **Autorização** — allowlist por plataforma, pairing para DMs

---

## Sistema de Plugins

```
plugins/
├── memory/           # MemoryProvider ABC (honcho, mem0, etc)
├── image_gen/        # ImageGenProvider ABC (FAL, OpenAI, etc)
├── context_engine/   # ContextEngine ABC
└── dashboard/        # Dashboard plugin (React + FastAPI)
```

Plugins implementam ABCs → auto-descobertos via entry points ou `~/.damon/plugins/`

---

## Sistema de Skills

```
skills/
├── category/
│   └── skill-name/
│       ├── SKILL.md          # Frontmatter + markdown
│       ├── scripts/          # Python/Shell helpers
│       └── references/       # Docs auxiliares
```

- **Frontmatter:** name, description, version, author, license, platforms, required_env_vars, metadata.damon (condicionais)
- **Condicionais:** `fallback_for_toolsets`, `requires_toolsets`, `fallback_for_tools`, `requires_tools`
- **Auto-criadas:** Agente gera skills após tarefas complexas

---

## Fluxo de Dados (Resumido)

```
User Input (CLI/Gateway)
        │
        ▼
┌───────────────────┐
│  AIAgent Loop     │
│  1. Build Prompt  │
│  2. Call LLM      │
│  3. Exec Tools    │──► Terminal/Web/Browser/Code/Skills
│  4. Compress?     │
│  5. Persist       │──► SQLite (state.db) + MEMORY.md
└───────────────────┘
        │
        ▼
Response → User (CLI/Gateway)
```

---

## Princípios de Design

1. **Prompt caching sagrado** — System prompt byte-stable por conversa
2. **Core narrow waist** — Capability nas edges (skills, plugins, tools), não no core
3. **E2E validation** — Testes reais com `DAMON_HOME` temp, não mocks
4. **Cache/alternation/invariant safe** — Role alternation estrita, system prompt estável
5. **Contributor credit preserved** — Rebase-merge, não rewrite