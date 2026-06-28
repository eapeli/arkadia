# Quickstart — Instalação → Setup → Primeira Conversa em 2 Min

---

## 1. Instalação (30 seg)

**Linux/macOS/WSL2/Termux:**
```bash
curl -fsSL https://github.com/eapeli/damon/raw/main/install.sh | bash
source ~/.bashrc
```

**Windows (PowerShell nativo):**
```powershell
iex (irm https://github.com/eapeli/damon/raw/main/install.ps1)
```

---

## 2. Setup Wizard (1 min)

```bash
damon setup
```

O wizard pergunta:
1. **Provedor LLM** → OpenRouter, NovitaAI, NVIDIA NIM, OpenAI, Anthropic, custom
2. **API Key** → Salva seguro em `~/.damon/.env`
3. **Modelo** → Escolhe da lista
4. **Tools** → Ativa `core`, `terminal`, `web`, `skills` (recomendado)
5. **Gateway** → Opcional: Telegram, Discord, WhatsApp, Slack, Signal

---

## 3. Primeira Conversa (30 seg)

```bash
damon
```

```text
Damon ☤  [claude-3.5-sonnet via openrouter]

Você: Olá! Me ajuda a criar um cron job que monitora um site e avisa no Telegram se mudar.

Damon: Claro! Vou criar o script e o cron job.

[Cria ~/.damon/scripts/monitor.py]
[Configura: damon cron create "every 1h" ... --script monitor.py --deliver telegram]

Pronto! Roda a cada hora. Só avisa se houver mudança real ([SILENT] evita spam).

Você: Legal. Pode usar modelo mais barato pra isso?

Damon: Feito.
/model openrouter:deepseek/deepseek-chat
```

---

## ✅ Pronto!

Agora explore:

| Próximo | Comando |
|---------|---------|
| Ver comandos | `/skills` ou `damon --help` |
| Trocar modelo | `/model openrouter:gpt-4o-mini` |
| Conectar Telegram | `damon gateway setup` |
| Ver skills | `damon skills browse` |
| Criar automação | `damon cron create "daily" "..." --deliver telegram` |

---

## Problemas?

```bash
damon doctor        # Diagnostica
damon config show   # Verifica config
damon update        # Atualiza
```

Documentação completa: [docs/index.md](../index.md)