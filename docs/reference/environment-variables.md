# Variáveis de Ambiente

Todas as variáveis ficam em `~/.damon/.env` (**chmod 600!**)

---

## LLM Providers

| Variável | Provedor | Obrigatória |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | OpenRouter | Se usar OpenRouter |
| `NOVITAAI_API_KEY` | NovitaAI | Se usar NovitaAI |
| `NVIDIA_NIM_API_KEY` | NVIDIA NIM | Se usar NIM |
| `OPENAI_API_KEY` | OpenAI | Se usar OpenAI direto |
| `ANTHROPIC_API_KEY` | Anthropic | Se usar Anthropic direto |
| `GOOGLE_API_KEY` | Google/Gemini | Se usar Google direto |
| `XAI_API_KEY` | xAI/Grok | Se usar xAI |
| `DEEPSEEK_API_KEY` | DeepSeek | Se usar DeepSeek direto |
| `HF_TOKEN` | Hugging Face | Para models HF |
| `CUSTOM_API_KEY` | Endpoint custom | Se usar endpoint próprio |

---

## Gateway de Mensagens

| Variável | Plataforma |
|----------|------------|
| `TELEGRAM_BOT_TOKEN` | Telegram |
| `DISCORD_BOT_TOKEN` | Discord |
| `DISCORD_APPLICATION_ID` | Discord (slash commands) |
| `WHATSAPP_PHONE_NUMBER` | WhatsApp Baileys |
| `WHATSAPP_CLOUD_TOKEN` | WhatsApp Cloud API |
| `WHATSAPP_CLOUD_PHONE_ID` | WhatsApp Cloud API |
| `SLACK_BOT_TOKEN` | Slack |
| `SLACK_SIGNING_SECRET` | Slack (events) |
| `SLACK_APP_TOKEN` | Slack (socket mode) |
| `SIGNAL_PHONE_NUMBER` | Signal |
| `EMAIL_IMAP_HOST` | Email |
| `EMAIL_IMAP_USER` | Email |
| `EMAIL_IMAP_PASSWORD` | Email |
| `EMAIL_SMTP_HOST` | Email |
| `EMAIL_SMTP_USER` | Email |
| `EMAIL_SMTP_PASSWORD` | Email |

---

## Ferramentas Externas

| Variável | Tool |
|----------|------|
| `FIRECRAWL_API_KEY` | `web_search`, `web_extract` (Firecrawl) |
| `SERPER_API_KEY` | `web_search` (Serper) |
| `BRAVE_SEARCH_API_KEY` | `web_search` (Brave) |
| `FAL_API_KEY` | `image_generate` (FAL) |
| `OPENAI_TTS_API_KEY` | `text_to_speech` (OpenAI) |
| `ELEVENLABS_API_KEY` | `text_to_speech` (ElevenLabs) |
| `MODAL_TOKEN_ID` | Terminal backend Modal |
| `MODAL_TOKEN_SECRET` | Terminal backend Modal |
| `DAYTONA_API_KEY` | Terminal backend Daytona |
| `DAYTONA_API_URL` | Terminal backend Daytona |

---

## Memória Externa

| Variável | Provedor |
|----------|----------|
| `HONCHO_API_KEY` | Honcho |
| `MEM0_API_KEY` | Mem0 |
| `SUPERMEMORY_API_KEY` | Supermemory |
| `BYTEROVER_API_KEY` | Byterover |
| `HOLOGRAPHIC_API_KEY` | Holographic |
| `OPENVIKING_API_KEY` | OpenViking |
| `RETAINDB_API_KEY` | RetainDB |

---

## MCP Servers

| Variável | Servidor |
|----------|----------|
| `GITHUB_TOKEN` | `@modelcontextprotocol/server-github` |
| `POSTGRES_URL` | `@modelcontextprotocol/server-postgres` |
| `BRAVE_SEARCH_API_KEY` | `@modelcontextprotocol/server-brave-search` |

---

## Infraestrutura / Deploy

| Variável | Uso |
|----------|-----|
| `DAMON_HOME` | Override `~/.damon` |
| `DAMON_CONFIG` | Override config file |
| `DAMON_LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, `ERROR` |
| `DAMON_NO_COLOR` | `1` = desabilita cores |
| `DAMON_DISABLE_TELEMETRY` | `1` = desabilita telemetria |

---

## Exemplo `.env` Completo

```bash
# LLM
OPENROUTER_API_KEY=sk-or-v1-...
# NOVITAAI_API_KEY=...
# NVIDIA_NIM_API_KEY=...

# Gateway
TELEGRAM_BOT_TOKEN=123456789:ABC...
DISCORD_BOT_TOKEN=...
# WHATSAPP_CLOUD_TOKEN=...

# Tools
FIRECRAWL_API_KEY=fc-...
FAL_API_KEY=...
# OPENAI_TTS_API_KEY=...

# MCP
GITHUB_TOKEN=ghp_...

# Modal (serverless terminal)
MODAL_TOKEN_ID=...
MODAL_TOKEN_SECRET=...

# Daytona (workspaces)
DAYTONA_API_KEY=...

# Memória externa (opcional)
# HONCHO_API_KEY=...
# MEM0_API_KEY=...

# Damon config
DAMON_LOG_LEVEL=INFO
# DAMON_HOME=/custom/path
```

---

## Segurança

```bash
chmod 600 ~/.damon/.env      # Apenas você lê
ls -la ~/.damon/.env         # Verifica: -rw-------
```

> **NUNCA** commite `.env` — está no `.gitignore`