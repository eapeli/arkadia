# Automações & Rotinas

O Damon tem **automação nativa** — cron jobs, webhooks, script injection, multi-skill workflows — rodando na sua infra, sem limites diários.

---

## Cron Jobs (Agendados)

```bash
# Cria job agendado
damon cron create "0 9 * * *" \
  "Gera digest diário de notícias IA. Busca anúncios, repos trending, papers. Máximo 500 palavras." \
  --name "Daily AI Digest" \
  --deliver telegram

# Intervalos legíveis
damon cron create "every 1h"   "Monitora site X" --script ~/.damon/scripts/watch.py
damon cron create "daily"      "Backup das memórias"
damon cron create "weekly"     "Auditoria de segurança"
damon cron create "monthly"    "Relatório de custos API"
```

### Sintaxe de Schedule

| Formato | Exemplo | Significado |
|---------|---------|-------------|
| Cron expr | `"0 2 * * *"` | Todo dia 2h |
| `@daily` / `daily` | `"daily"` | Todo dia meia-noite |
| `@weekly` / `weekly` | `"weekly"` | Segunda 0h |
| `@monthly` / `monthly` | `"monthly"` | Dia 1, 0h |
| `@hourly` / `hourly` | `"hourly"` | Toda hora |
| `every N[mh]` | `"every 30m"` | A cada 30 min |
| `every N[h]` | `"every 2h"` | A cada 2 horas |

---

## Script Injection (Pré-processamento)

Roda script Python **antes** do agent. O `stdout` vira contexto.

```bash
damon cron create "every 1h" \
  "Se MUDANÇA, resume. Se NADA, responde [SILENT]." \
  --script ~/.damon/scripts/watch-price.py \
  --name "Price Monitor" \
  --deliver telegram
```

**Script exemplo (`watch-price.py`):**
```python
#!/usr/bin/env python3
import requests, json, os

url = "https://api.exemplo.com/preco"
cache_file = "/tmp/last_price.json"

response = requests.get(url)
current = response.json()["price"]

if os.path.exists(cache_file):
    with open(cache_file) as f:
        last = json.load(f)["price"]
    if current != last:
        print(f"CHANGE_DETECTED: {last} -> {current}")
    else:
        print("[SILENT]")
else:
    print(f"FIRST_RUN: {current}")

with open(cache_file, "w") as f:
    json.dump({"price": current}, f)
```

> `[SILENT]` = Damon não notifica. Só avisa quando há mudança real.

---

## Multi-Skill Workflows

Encadeia skills especializadas em uma automação:

```bash
damon cron create "0 8 * * *" \
  "Busca papers no arXiv sobre 'LLM reasoning'. Salva top 3 como notas Obsidian." \
  --skills "arxiv,obsidian" \
  --name "Paper Digest"
```

---

## Webhooks (Triggers Externos)

```bash
# Habilita webhook receiver
damon gateway setup    # ativa webhooks
damon gateway start

# GitHub events
damon webhook subscribe pr-review \
  --events "pull_request" \
  --prompt "Review PR #{pull_request.number}: {pull_request.title}. Verifica auth, security, performance." \
  --skills "github-code-review" \
  --deliver github_comment

# Alertas customizados
damon webhook subscribe alert-triage \
  --prompt "Alerta: {alert.name} — Severity: {alert.severity}. Investiga, propõe primeiros passos." \
  --deliver slack

# Generic POST
damon webhook subscribe custom \
  --prompt "Payload: {body}. Processa conforme instruções." \
  --deliver telegram
```

### Payloads Disponíveis

| Evento | Variáveis no Prompt |
|--------|---------------------|
| `pull_request` | `pull_request.number`, `pull_request.title`, `pull_request.user.login`, `pull_request.body` |
| `push` | `ref`, `commits`, `repository.name` |
| `issues` | `issue.number`, `issue.title`, `issue.body` |
| `alert` | `alert.name`, `alert.severity`, `alert.description` |
| Custom | `body` (JSON completo) |

---

## Entrega Multiplataforma

```bash
--deliver telegram                    # Canal home Telegram
--deliver telegram:-1001234567890:42# Topic específico
--deliver discord                     # Canal home Discord
--deliver slack                       # Canal home Slack
--deliver sms:+155****4567            # SMS
--deliver email                       # Email configurado
--deliver github_comment              # Comentário no PR/Issue
--deliver local                       # Arquivo em ~/.damon/cron/output/
--deliver local,telegram              # Múltiplos destinos
```

---

## Gerenciando Jobs

```bash
damon cron list                    # Lista todos
damon cron show "Daily AI Digest"  # Detalhes
damon cron run "Daily AI Digest"   # Executa agora (manual)
damon cron pause "Daily AI Digest" # Pausa
damon cron resume "Daily AI Digest"# Retoma
damon cron delete "Daily AI Digest"# Remove
damon cron logs "Daily AI Digest"  # Últimas execuções
```

---

## Comparação: Damon vs Claude Code Routines

| Feature | Damon | Claude Code Routines |
|---------|-------|---------------------|
| Cron | ✅ Qualquer expr | ✅ Schedule-based |
| GitHub triggers | ✅ Qualquer evento | ✅ PR, issue, push |
| API triggers | ✅ HMAC webhooks | ✅ POST endpoint |
| MCP | ✅ Cliente completo | ✅ Conectores nativos |
| Script injection | ✅ Python pré-agent | ❌ |
| Multi-skill | ✅ `--skills "a,b"` | ❌ |
| Daily limit | **Ilimitado** | 5-25/dia |
| Modelos | **Qualquer** | Apenas Claude |
| Entrega | Telegram, Discord, Slack, SMS, email, GitHub, local | GitHub comments |
| Infra | **Sua** | Anthropic |
| Dados | **Suas máquinas** | Nuvem Anthropic |
| Custo | Sua API key | Assinatura |
| Open source | **Sim (MIT)** | Não |

---

## Próximos

- [Configuração](../configuration.md)
- [Gateway de Mensagens](../messaging.md)
- [Skills](../features/skills.md)