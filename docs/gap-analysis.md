# Gap Analysis: Damon vs Hermes

Comparação estrutural real entre `/home/ubuntu/repos/damon-sync` (fork funcional) e `/home/ubuntu/.damon/repos/damon-agent` (original). Baseada em árvore de diretórios e arquivos Python de nível superior.

## A) Damon JÁ TEM igual ao Hermes

- **Núcleo de agente**: `agent/` com adaptadores de modelo (Anthropic, Bedrock, Gemini, Codex, Azure, Google), compressão de contexto, loop de conversação, memory manager, tool executor
- **Gateway**: `gateway/` com plataformas (Discord, Telegram, Slack, IRC, Teams, Line, ntfy, etc.), relay, builtin hooks
- **CLI**: `damon_cli/` (equiv. `damon_cli/`) com subcommands, proxy, dashboard auth
- **Plugins base**: browser, image_gen, video_gen, kanban, memory, model-providers, platforms, web
- **Skills base**: creative (design-md, ascii-art, comfyui, p5js, etc.)
- **Tools base**: terminal, file operations, browser, MCP, delegate, TTS/transcription, vision, web search, kanban, cronjob
- **Desktop app**: `apps/desktop/` completo (Electron + shared)
- **Bootstrap installer**: `apps/bootstrap-installer/`
- **Docker**: docker-compose, s6 supervision, cont-init.d
- **Docs**: design, kanban, middleware, observability, plans, security, user-guide
- **Infra**: locales, nix, flake, assets, scripts, datagen-config-examples

## B) FALTANDO no Damon (presente no Hermes, ausente no Damon)

### Diretórios estruturais
- `.plans/` — planos de desenvolvimento (estão como arquivos soltos no root do Hermes)
- `config/` — configurações de gateway (no Damon só existe exemplo `cli-config.yaml.example`)
- `providers/` — abstração base de providers (no Damon os provedores estão espalhados em `plugins/model-providers/`)
- `tests/` — pasta de testes inexistente no Damon
- `packaging/` — empacotamento (homebrew, etc.)
- `tui_gateway/` — gateway TUI (Damon tem `damon_ui/` mas não o módulo TUI do Hermes)
- `ui-tui/` — projeto TUI separado (Damon não tem estrutura equivalente)
- `web/` — dashboard web (Damon tem plugin kanban/dashboard mas não o app web standalone)
- `website/` — documentação online (Docusaurus)

### Diretórios de skills (Damon só tem `skills/creative/`)
- `skills/apple/` (Notes, Reminders, FindMy, iMessage)
- `skills/autonomous-ai-agents/`
- `skills/data-science/`
- `skills/devops/`
- `skills/dogfood/`
- `skills/email/`
- `skills/github/`
- `skills/index-cache/`
- `skills/media/`
- `skills/mlops/`
- `skills/note-taking/`
- `skills/productivity/`
- `skills/research/`
- `skills/smart-home/`
- `skills/social-media/`
- `skills/software-development/`
- `skills/yuanbao/`

### Diretórios de plugins extras
- `plugins/context_engine/`
- `plugins/dashboard_auth/`
- `plugins/disk-cleanup/`
- `plugins/google_meet/`
- `plugins/damon-achievements/`
- `plugins/observability/`
- `plugins/security-guidance/`
- `plugins/spotify/`
- `plugins/teams_pipeline/`

### Diretórios de optional-skills/optional-mcps
- `optional-mcps/` (linear, n8n)
- `optional-skills/` categorias inteiras (blockchain, finance, gaming, health, mcp, migration, payment, security, web-dev)

### Arquivos Python de nível superior faltando
- `batch_runner.py` — executor de batch
- `damon_bootstrap.py` — bootstrap do Hermes (Damon tem bootstrap em `cli.py`?)
- `damon_logging.py` — logging estruturado (Damon tem `damon_logging.py` mas pode ser diferente)
- `damon_time.py` — utilitários de tempo
- `mcp_serve.py` — server MCP standalone
- `mini_swe_runner.py` — rodar SWE agents
- `run_agent.py` — ponto de entrada standalone do agente
- `setup.py` — setup de instalação (Damon usa pyproject.toml)
- `toolset_distributions.py` — distribuições de toolsets por contexto
- `trajectory_compressor.py` — compressor de trajetória

### Outros arquivos/diretórios
- `plans/` — planos de implementação
- `.github/ISSUE_TEMPLATE/` — templates de issue
- `.github/actions/` — ações customizadas CI
- `.github/pr-screenshots/` — screenshots para PRs
- `scripts/whatsapp-bridge/` — bridge WhatsApp
- `providers/__init__.py`, `providers/base.py` — base de provedores
- `ui-tui/` (projeto TypeScript separado) — equivalente a `damon_ui/`?
- `web/` e `website/` — frontends web

## C) Baixa prioridade / Opcional

- `optional-mcps/` — integrações específicas (Linear, n8n) podem ficar como plugins sob demanda
- `optional-skills/` categorias muito específicas:
  - blockchain, gaming, health, finance (boleto, LBO), migration, payment
- `skills/apple/` — requer macOS/iOS ecosystem
- `skills/data-science/`, `skills/mlops/` — muito nicho
- `packaging/` — homebrew packaging, relevante só se distribuir via brew
- `website/` — documentação online, não crítico para funcionalidade core
- `tui_gateway/` e `ui-tui/` — Damon já tem `damon_ui/` e apps desktop; TUI pode ser evoluído a partir do UI existente em vez de portar todo o `ui-tui/`
- `.github/pr-screenshots/` e `.github/actions/` — CI/CD infra, útil mas não bloqueante
