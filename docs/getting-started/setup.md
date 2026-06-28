# Primeira Configuração

O comando `damon setup` é um wizard interativo que configura tudo:

```bash
damon setup
```

O wizard passa por:

---

## 1. Provedor & Modelo LLM

Escolha seu provedor principal:

| Provedor | O que oferece |
|----------|---------------|
| **OpenRouter** | 200+ modelos, 1 chave, roteamento por custo/latência |
| **NovitaAI** | Model API, Agent Sandbox, GPU Cloud |
| **NVIDIA NIM** | Nemotron, modelos otimizados NVIDIA |
| **Hugging Face** | Modelos open source, inference endpoints |
| **OpenAI / Anthropic / Google** | APIs diretas |
| **Endpoint Custom** | Qualquer API compatível OpenAI |

O wizard:
- Pede a API key (salva em `~/.damon/.env`, seguro)
- Lista modelos disponíveis
- Define o modelo padrão

---

## 2. Ferramentas (Tools & Toolsets)

Ative/desative toolsets:

| Toolset | Ferramentas | Para que serve |
|---------|-------------|----------------|
| `core` | `read_file`, `write_file`, `patch`, `search_files`, `task_tool` | Básico |
| `terminal` | `terminal` | Execução de shell (local, Docker, SSH, Modal, Daytona) |
| `web` | `web_search`, `web_extract` | Busca e extração web |
| `browser` | `browser_navigate`, `browser_click`, `browser_type` | Automação browser |
| `coding` | `code_execution`, `delegate_task` | Python, subagentes |
| `media` | `image_generate`, `vision_analyze`, `text_to_speech` | Mídia |
| `skills` | `skill_view`, `skill_manage` | Sistema de skills |

> **Dica:** Comece com `core`, `terminal`, `web`, `skills`. Adicione outros conforme necessidade.

---

## 3. Gateway de Mensagens (Opcional)

Configure plataformas:

```bash
damon gateway setup
```

Plataformas suportadas:
- **Telegram** — Bot token + chat ID
- **Discord** — Bot token + application ID
- **WhatsApp** — Baileys (QR code) ou WhatsApp Cloud API
- **Slack** — Bot token + signing secret
- **Signal** — signal-cli
- **Email** — IMAP/SMTP

Após configurar:
```bash
damon gateway start    # inicia o gateway
```

---

## 4. Configurações Avançadas

O wizard também oferece:

- **Terminal backend** — Local (padrão), Docker, SSH, Modal, Daytona
- **Compressão de contexto** — Auto-sumarização ao limite de tokens
- **Memória** — Provedor (local, Honcho, Mem0, etc.)
- **Logging** — Nível, JSONL, rotação

---

## Configuração Manual (Sem Wizard)

Edite diretamente:

```bash
# Config principal
cat > ~/.damon/config.yaml << 'EOF'
model:
  provider: openrouter
  model: anthropic/claude-3.5-sonnet
  temperature: 0.7

toolsets: [core, terminal, web, skills]

terminal:
  backend: local

memory:
  provider: local
EOF

# Secrets (chmod 600!)
cat > ~/.damon/.env << 'EOF'
OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxx
EOF
chmod 600 ~/.damon/.env
```

---

## Verificando Tudo

```bash
damon config show        # mostra config resolvida
damon tools              # lista tools ativas
damon model              # mostra modelo atual
damon doctor             # diagnostica problemas
```

---

## Próximos Passos

- [Primeira Conversa](first-conversation.md)
- [CLI & TUI](../user-guide/cli.md)
- [Gateway de Mensagens](../user-guide/messaging.md)