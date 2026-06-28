# Damon Agent ☤

<p align="center">
  <a href="https://github.com/eapeli/damon">GitHub</a> • <a href="https://github.com/eapeli/damon/issues">Issues</a> • <a href="https://github.com/eapeli/damon/wiki">Wiki</a>
</p>

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Lang-Portugu%C3%AAs-blue?style=for-the-badge" alt="Português"></a>
  <a href="https://github.com/eapeli/damon/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License: MIT"></a>
  <a href="https://github.com/eapeli/damon/blob/main/docs/author.md"><img src="https://img.shields.io/badge/Author-Elisabete%20Alves-purple?style=for-the-badge" alt="Author: Elisabete Alves"></a>
  <a href="https://github.com/nousresearch/hermes-agent"><img src="https://img.shields.io/badge/Base-Hermes%20(Original%20Codebase)-blue?style=for-the-badge" alt="Base: Hermes (Original Codebase)"></a>
  <a href="https://github.com/eapeli/damon"><img src="https://img.shields.io/badge/Status-Active%20Development-orange?style=for-the-badge" alt="Status: Active Development"></a>

---
<p align="center">
  <img src="docs/img/logo.png" alt="Damon Agent logo" width="180">
</p>


**Damon** is a personal, autonomous AI agent created by **Elisabete Alves**. Designed to run continuously, learn from usage, and adapt to the user over time — without relying on third-party infrastructure.

Runs on your server, VPS, laptop, or serverless infrastructure. Chat via Telegram, Discord, WhatsApp, Slack, Signal, or directly in the terminal. Use any model: OpenRouter, NovitaAI, NVIDIA NIM, Hugging Face, OpenAI, Anthropic, Google, local endpoints, or your own. Switch with `damon model` — no lock-in.

---

## ✨ What Damon Does

| Capability | Description |
|------------|-------------|
| **Real Terminal (TUI)** | Full interface: multiline editing, command autocomplete, history, interruption, tool streaming. |
| **Multi-Platform Gateway** | Telegram, Discord, Slack, WhatsApp, Signal — single process. Voice transcription, cross-platform continuity. |
| **Memory & Continuous Learning** | Persistent memory curated by the agent itself. Autonomous skill creation after complex tasks. Skills evolve with use. Full-text search (FTS5) in conversation history with LLM summarization. Compatible with the open standard [agentskills.io](https://agentskills.io). |
| **Scheduled Automations** | Built-in cron with delivery to any platform. Daily reports, backups, audits — all in natural language, unattended. |
| **Delegation & Parallelism** | Isolated subagents for parallel workstreams. Python scripts that call tools via RPC, collapsing pipelines into a single interaction. |
| **Multiple Execution Backends** | Local, Docker, SSH, Singularity, Modal, Daytona. Modal/Daytona: serverless persistence — hibernates when idle, wakes on demand. |
| **Research-Ready** | Batch trajectory generation, compression for training tool-calling models. |

---

## 🚀 Quick Installation

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://github.com/eapeli/damon/raw/main/install.sh | bash
```

### Windows (native, PowerShell)

> Native Windows runs Damon without WSL — CLI, gateway, TUI, and tools work natively.

```powershell
iex (irm https://github.com/eapeli/damon/raw/main/install.ps1)
```

The installer handles everything: uv, Python 3.11, Node.js, ripgrep, ffmpeg, and portable Git Bash (MinGit, in `%LOCALAPPDATA%\damon\git` — no admin required, isolated from system Git).

```bash
source ~/.bashrc    # reload shell (or: source ~/.zshrc)
damon               # start chatting!
```

---

## 🎯 First Steps

```bash
damon              # Interactive CLI — starts a conversation
damon model        # Choose provider and LLM model
damon tools        # Configure which tools stay active
damon config set   # Set individual configuration values
damon gateway      # Start messaging gateway (Telegram, Discord, etc.)
damon setup        # Complete setup wizard
damon claw migrate # Migrate from OpenClaw (if coming from there)
damon update       # Update to the latest version
damon doctor       # Diagnose problems
```

📖 **Documentation:** `/docs` folder and [GitHub Wiki](https://github.com/eapeli/damon/wiki)

---

## 🔑 API Keys — You're in Control

Damon works with any provider. Your keys, your rules:

- **OpenRouter** — 200+ models with a single key
- **NovitaAI** — Native cloud for Model API, Agent Sandbox, GPU Cloud
- **NVIDIA NIM** — Nemotron and optimized models
- **Direct endpoints** — OpenAI-compatible, Anthropic, Google, xAI, etc.

```bash
damon setup        # Interactive wizard for all providers
```

See what's configured: `damon config show`

---

## 💬 CLI vs Messaging

| Action | CLI | Messaging Platforms |
|--------|-----|---------------------|
| Start chatting | `damon` | `damon gateway setup` → `damon gateway start` → message the bot |
| New conversation | `/new` or `/reset` | `/new` or `/reset` |
| Switch model | `/model [provider:model]` | `/model [provider:model]` |
| Set personality | `/personality [name]` | `/personality [name]` |
| Retry/undo | `/retry`, `/undo` | `/retry`, `/undo` |
| Compress/usage | `/compress`, `/usage`, `/insights` | `/compress`, `/usage`, `/insights` |
| Browse skills | `/skills` or `/<skill-name>` | `/<skill-name>` |
| Interrupt | `Ctrl+C` | `/stop` or new message |
| Status | `/platforms` | `/status`, `/sethome` |

---

## 📚 Documentation

| Section | Covers |
|---------|--------|
| [Quickstart](docs/getting-started/quickstart.md) | Install → setup → first conversation |
| [CLI Usage](docs/user-guide/cli.md) | Commands, keybindings, personalities, sessions |
| [Configuration](docs/user-guide/configuration.md) | Config file, providers, models, all options |
| [Messaging Gateway](docs/user-guide/messaging.md) | Telegram, Discord, Slack, WhatsApp, Signal |
| [Security](docs/user-guide/security.md) | Command approval, DM pairing, container isolation |
| [Tools and Toolsets](docs/user-guide/features/tools.md) | 40+ tools, toolset system, terminal backends |
| [Skills System](docs/user-guide/features/skills.md) | Procedural memory, Skills Hub, creating skills |
| [Memory](docs/user-guide/features/memory.md) | Persistent memory, user profiles, best practices |
| [MCP Integration](docs/user-guide/features/mcp.md) | Connect any MCP server |
| [Cron Scheduling](docs/user-guide/features/cron.md) | Scheduled tasks with platform delivery |
| [Architecture](docs/developer-guide/architecture.md) | Project structure, agent loop, key classes |
| [Contributing](docs/developer-guide/contributing.md) | Dev setup, PR process, code style |

---

## 🔄 Migrating from OpenClaw

```bash
damon claw migrate              # Interactive migration (complete)
damon claw migrate --dry-run    # Preview what would be migrated
damon claw migrate --preset user-data   # Migrate without secrets
damon claw migrate --overwrite  # Overwrite conflicts
```

Imports: SOUL.md, memories, skills, allowlists, messaging config, API keys, TTS assets, workspace instructions.

---

## 🛠 Contributing

```bash
git clone https://github.com/eapeli/damon.git
cd damon
./damon
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## ⚖️ License and Credits

MIT — see [LICENSE](LICENSE).

**Created by Elisabete Alves.**

Parts of the codebase derive from [Hermes Agent](https://github.com/nousresearch/hermes-agent) (MIT, by Nous Research), used as the foundation under the terms of the original license.
