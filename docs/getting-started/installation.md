# Instalação

## Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://github.com/eapeli/damon/raw/main/install.sh | bash
```

O instalador faz tudo automaticamente:
- Instala `uv` (gerenciador de pacotes Python rápido)
- Python 3.11+
- Node.js 20+ (para ferramentas de browser, WhatsApp bridge)
- `ripgrep` (busca rápida)
- `ffmpeg` (áudio/vídeo)
- Git Bash portátil (MinGit) no Windows — isolado, sem admin

Após a instalação:

```bash
source ~/.bashrc    # ou: source ~/.zshrc
damon               # inicia!
```

---

## Windows (Nativo, PowerShell)

> Windows nativo roda Damon **sem WSL** — CLI, gateway, TUI e ferramentas funcionam nativamente.

```powershell
iex (irm https://github.com/eapeli/damon/raw/main/install.ps1)
```

O instalador cuida de tudo, incluindo Git Bash portátil em `%LOCALAPPDATA%\damon\git`.

---

## Android / Termux

```bash
pkg update && pkg upgrade
pkg install python git nodejs ffmpeg ripgrep
git clone https://github.com/eapeli/damon.git
cd damon
./setup-damon.sh
```

Nota: No Termux, use o extra `.[termux]` pois o `.[all]` puxa dependências de voz incompatíveis com Android.

---

## Verificando a Instalação

```bash
damon doctor        # diagnostica problemas
damon version       # mostra versão
damon config show   # mostra configuração atual
```

---

## Estrutura de Diretórios

Após o primeiro `damon setup`:

```
~/.damon/
├── config.yaml          # configuração principal
├── .env                 # API keys e segredos (NUNCA commite!)
├── auth.json            # credenciais OAuth (se usar)
├── skills/              # skills ativas (bundled + hub + criadas)
├── memories/            # MEMORY.md, USER.md
├── state.db             # SQLite: sessões, FTS5
├── sessions/            # routing index, transcripts
├── cron/                # jobs agendados
├── logs/                # logs JSONL
└── whatsapp/session/    # credenciais WhatsApp (se usar)
```

---

## Próximos Passos

1. [Primeira Configuração](setup.md) — Configure provedores e modelos
2. [Primeira Conversa](first-conversation.md) — Comece a usar
3. [Gateway de Mensagens](../user-guide/messaging.md) — Conecte Telegram, Discord, etc.