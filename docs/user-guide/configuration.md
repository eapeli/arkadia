# Configuração

## Arquivo Principal: `~/.damon/config.yaml`

```yaml
# Provedor e modelo
model:
  provider: openrouter          # openrouter, novita, nvidia, openai, anthropic, custom
  model: anthropic/claude-3.5-sonnet
  temperature: 0.7
  max_tokens: 8192
  reasoning:
    enabled: false
    budget_tokens: 2000

# Toolsets ativos
toolsets: [core, terminal, web, skills]

# Terminal backend
terminal:
  backend: local                # local, docker, ssh, singularity, modal, daytona
  docker:
    image: ubuntu:22.04
  ssh:
    host: servidor
    user: usuario
  modal:
    token_id: ${MODAL_TOKEN_ID}
    token_secret: ${MODAL_TOKEN_SECRET}

# Gateway de mensagens
gateway:
  enabled: false
  platforms:
    telegram:
      enabled: true
      bot_token: "${TELEGRAM_BOT_TOKEN}"
      allowed_users: []
    discord:
      enabled: false

# Memória
memory:
  provider: local               # local, honcho, mem0, supermemory, byterover, holographic, openviking, retaindb
  local:
    path: ~/.damon/memories

# Compressão de contexto
context:
  compression:
    enabled: true
    threshold: 0.8              # % do context window
    keep_recent: 10             # mensagens recentes preservadas
    model: openrouter:deepseek/deepseek-chat

# Logging
logging:
  level: INFO                   # DEBUG, INFO, WARNING, ERROR
  jsonl: true
  rotation:
    max_files: 10
    max_size_mb: 50

# Rede
network:
  timeout: 30
  retries: 3
```

---

## Variáveis de Ambiente (`~/.damon/.env`)

```bash
# LLM Providers
OPENROUTER_API_KEY=sk-or-...
NOVITAAI_API_KEY=...
NVIDIA_NIM_API_KEY=...
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# Gateway
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
DISCORD_BOT_TOKEN=...
WHATSAPP_SESSION_PATH=~/.damon/whatsapp/session

# Ferramentas
FIRECRAWL_API_KEY=fc-...
FAL_API_KEY=...
BROWSERBASE_API_KEY=...
OPENAI_TTS_API_KEY=...

# Modal
MODAL_TOKEN_ID=...
MODAL_TOKEN_SECRET=...

# Daytona
DAYTONA_API_KEY=...
DAYTONA_SERVER_URL=...
```

> **⚠️ Segurança:** `chmod 600 ~/.damon/.env` — nunca commite este arquivo!

---

## Profiles Múltiplos

```bash
damon profile create work
damon profile create personal
damon profile switch work
```

Cada profile tem seu próprio `~/.damon/profiles/<name>/` com config.yaml, .env, skills, memories isolados.

---

## Referência Completa

Todas as opções: [Configuração Completa](../reference/configuration.md)