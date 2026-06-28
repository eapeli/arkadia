# Damon Agent ☤

<p align="center">
  <a href="https://github.com/eapeli/damon">GitHub</a> • <a href="https://github.com/eapeli/damon/issues">Issues</a> • <a href="https://github.com/eapeli/damon/wiki">Wiki</a>
</p>

<p align="center">
  <a href="README.en.md"><img src="https://img.shields.io/badge/Lang-English-blue?style=for-the-badge" alt="English"></a>
  <a href="https://github.com/eapeli/damon/blob/main/LICENSE"><img src="https://img.shields.io/badge/Licen%C3%A7a-MIT-green?style=for-the-badge" alt="Licença: MIT"></a>
  <a href="https://github.com/eapeli/damon/blob/main/docs/author.md"><img src="https://img.shields.io/badge/Autor-Elisabete%20Alves-purple?style=for-the-badge" alt="Autor: Elisabete Alves"></a>
  <a href="https://github.com/nousresearch/hermes-agent"><img src="https://img.shields.io/badge/Base-Hermes%20(Origem%20do%20C%C3%B3digo)-blue?style=for-the-badge" alt="Base: Hermes (Origem do Código)"></a>
  <a href="https://github.com/eapeli/damon"><img src="https://img.shields.io/badge/Status-Desenvolvimento%20Ativo-orange?style=for-the-badge" alt="Status: Desenvolvimento Ativo"></a>

---
<p align="center">
  <img src="docs/img/logo.png" alt="Damon Agent logo" width="180">
</p>


**Damon** é um agente de IA pessoal e autônomo criado por **Elisabete Alves**. Projetado para rodar de forma contínua, aprender com o uso e se adaptar ao usuário ao longo do tempo — sem depender de infraestrutura de terceiros.

Roda no seu servidor, VPS, laptop ou infraestrutura serverless. Conversa pelo Telegram, Discord, WhatsApp, Slack, Signal ou direto no terminal. Use qualquer modelo: OpenRouter, NovitaAI, NVIDIA NIM, Hugging Face, OpenAI, Anthropic, Google, endpoints locais ou seu próprio. Troque com `damon model` — sem lock-in.

---

## ✨ O Que o Damon Faz

| Capacidade | Descrição |
|------------|-----------|
| **Terminal Real (TUI)** | Interface completa: edição multilinha, autocomplete de comandos, histórico, interrupção, streaming de ferramentas. |
| **Gateway Multiplataforma** | Telegram, Discord, Slack, WhatsApp, Signal — um único processo. Transcrição de voz, continuidade entre plataformas. |
| **Memória e Aprendizado Contínuo** | Memória persistente curada pelo próprio agente. Criação autônoma de skills após tarefas complexas. Skills evoluem com o uso. Busca full-text (FTS5) no histórico de conversas com sumarização LLM. Compatível com padrão aberto [agentskills.io](https://agentskills.io). |
| **Automações Agendadas** | Cron embutido com entrega em qualquer plataforma. Relatórios diários, backups, auditorias — tudo em linguagem natural, desatendido. |
| **Delegação e Paralelismo** | Subagentes isolados para workstreams paralelos. Scripts Python que chamam ferramentas via RPC, colapsando pipelines em uma única interação. |
| **Múltiplos Backends de Execução** | Local, Docker, SSH, Singularity, Modal, Daytona. Modal/Daytona: persistência serverless — hiberna ocioso, acorda sob demanda. |
| **Pronto para Pesquisa** | Geração de trajetórias em lote, compressão para treinar modelos tool-calling. |

---

## 🚀 Instalação Rápida

### Linux, macOS, WSL2, Termux

```bash
curl -fsSL https://github.com/eapeli/damon/raw/main/install.sh | bash
```

### Windows (nativo, PowerShell)

> Windows nativo roda Damon sem WSL — CLI, gateway, TUI e ferramentas funcionam nativamente.

```powershell
iex (irm https://github.com/eapeli/damon/raw/main/install.ps1)
```

O instalador cuida de tudo: uv, Python 3.11, Node.js, ripgrep, ffmpeg e Git Bash portátil (MinGit, em `%LOCALAPPDATA%\damon\git` — sem admin, isolado do Git do sistema).

```bash
source ~/.bashrc    # recarrega shell (ou: source ~/.zshrc)
damon               # começa a conversar!
```

---

## 📦 Instaladores Binários (pré-compilados)

Binários assinados estão disponíveis nas [Releases](https://github.com/eapeli/damon/releases):

| Plataforma | Arquivo | Comando de instalação |
|------------|---------|----------------------|
| **Windows** | `Damon-Setup.exe` (NSIS, assinado via Azure) | Baixe e execute |
| **macOS** | `Damon-Setup.dmg` (Apple notarizado) | `open Damon-Setup.dmg` → arraste para Applications |
| **Linux** | `Damon-Setup.AppImage` (universal) | `chmod +x Damon-Setup.AppImage && ./Damon-Setup.AppImage` |
| **Linux (Debian/Ubuntu)** | `damon-setup_1.0.0_amd64.deb` | `sudo dpkg -i damon-setup_1.0.0_amd64.deb` |
| **Linux (RHEL/Fedora)** | `damon-setup-1.0.0-1.x86_64.rpm` | `sudo rpm -i damon-setup-1.0.0-1.x86_64.rpm` |

> **Nota:** Os instaladores são gerados automaticamente via GitHub Actions a cada release. Verifique a aba [Releases](https://github.com/eapeli/damon/releases) para a versão mais recente.

---

## 🎯 Primeiros Passos

```bash
damon              # CLI interativo — inicia conversa
damon model        # Escolhe provedor e modelo LLM
damon tools        # Configura quais ferramentas ficam ativas
damon config set   # Define valores de configuração individuais
damon gateway      # Inicia gateway de mensagens (Telegram, Discord, etc.)
damon setup        # Wizard completo de configuração
damon claw migrate # Migra do OpenClaw (se vier de lá)
damon update       # Atualiza para versão mais recente
damon doctor       # Diagnostica problemas
```

📖 **Documentação:** pasta `/docs` e [GitHub Wiki](https://github.com/eapeli/damon/wiki)

---

## 🔑 Chaves de API — Você No Controle

Damon funciona com qualquer provedor. Suas chaves, suas regras:

- **OpenRouter** — 200+ modelos com uma única chave
- **NovitaAI** — Nuvem nativa para Model API, Agent Sandbox, GPU Cloud
- **NVIDIA NIM** — Nemotron e modelos otimizados
- **Endpoints diretos** — OpenAI-compatível, Anthropic, Google, xAI, etc.

```bash
damon setup        # Wizard interativo para todos os provedores
```

Ver o que está configurado: `damon config show`

---

## 💬 CLI vs Mensagens

| Ação | CLI | Plataformas de Mensagem |
|------|-----|-------------------------|
| Começar a conversar | `damon` | `damon gateway setup` → `damon gateway start` → mande msg pro bot |
| Nova conversa | `/new` ou `/reset` | `/new` ou `/reset` |
| Trocar modelo | `/model [provedor:modelo]` | `/model [provedor:modelo]` |
| Definir personalidade | `/personality [nome]` | `/personality [nome]` |
| Refazer/desfazer | `/retry`, `/undo` | `/retry`, `/undo` |
| Comprimir/uso | `/compress`, `/usage`, `/insights` | `/compress`, `/usage`, `/insights` |
| Navegar skills | `/skills` ou `/<skill-name>` | `/<skill-name>` |
| Interromper | `Ctrl+C` | `/stop` ou nova mensagem |
| Status | `/platforms` | `/status`, `/sethome` |

---

## 📚 Documentação

| Seção | Aborda |
|-------|--------|
| [Quickstart](docs/getting-started/quickstart.md) | Install → setup → primeira conversa |
| [Uso da CLI](docs/user-guide/cli.md) | Comandos, keybindings, personalidades, sessões |
| [Configuração](docs/user-guide/configuration.md) | Arquivo de config, provedores, modelos, todas opções |
| [Gateway de Mensagens](docs/user-guide/messaging.md) | Telegram, Discord, Slack, WhatsApp, Signal |
| [Segurança](docs/user-guide/security.md) | Aprovação de comandos, pairing DM, isolamento container |
| [Ferramentas e Toolsets](docs/user-guide/features/tools.md) | 40+ ferramentas, sistema de toolset, backends de terminal |
| [Sistema de Skills](docs/user-guide/features/skills.md) | Memória procedural, Skills Hub, criando skills |
| [Memória](docs/user-guide/features/memory.md) | Memória persistente, perfis de usuário, boas práticas |
| [Integração MCP](docs/user-guide/features/mcp.md) | Conecte qualquer servidor MCP |
| [Agendamento Cron](docs/user-guide/features/cron.md) | Tarefas agendadas com entrega em plataforma |
| [Arquitetura](docs/developer-guide/architecture.md) | Estrutura do projeto, loop do agent, classes-chave |
| [Contribuindo](docs/developer-guide/contributing.md) | Setup de dev, processo de PR, estilo de código |

---

## 🔄 Migrando do OpenClaw

```bash
damon claw migrate              # Migração interativa (completa)
damon claw migrate --dry-run    # Preview do que migraria
damon claw migrate --preset user-data   # Migra sem segredos
damon claw migrate --overwrite  # Sobrescreve conflitos
```

Importa: SOUL.md, memórias, skills, allowlists, config de mensagens, chaves de API, assets TTS, instruções de workspace.

---

## 🛠 Contribuindo

```bash
git clone https://github.com/eapeli/damon.git
cd damon
./damon
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes.

---

## ⚖️ Licença e Créditos

MIT — veja [LICENSE](LICENSE).

**Criado por Elisabete Alves.**

Partes do código base derivam do [Hermes Agent](https://github.com/nousresearch/hermes-agent) (MIT, by Nous Research), usado como fundação sob os termos da licença original.