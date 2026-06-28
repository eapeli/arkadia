# Documentação do Damon Agent

Bem-vindo à documentação oficial do **Damon Agent** — um agente de IA pessoal, autônomo e adaptativo.

---

## 🚀 Início Rápido

| Guia | Descrição |
|------|-----------|
| [Instalação](getting-started/installation.md) | Instalação no Linux, macOS, Windows, Termux |
| [Primeira Configuração](getting-started/setup.md) | Wizard `damon setup`, provedores, modelos |
| [Primeira Conversa](getting-started/first-conversation.md) | Iniciando, comandos básicos, TUI |
| [Guia Rápido (2 min)](getting-started/quickstart.md) | Install → Setup → Chat |

---

## 📖 Guia do Usuário

### Interface & Uso
- [CLI & TUI](user-guide/cli.md) — Terminal interativo, keybindings, slash commands
- [Gateway de Mensagens](user-guide/messaging.md) — Telegram, Discord, WhatsApp, Slack, Signal
- [Personalidades](user-guide/personalities.md) — Personas, SOUL.md, troca dinâmica

### Configuração
- [Arquivo de Configuração](user-guide/configuration.md) — `config.yaml`, variáveis de ambiente, profiles
- [Provedores & Modelos](user-guide/providers.md) — OpenRouter, NovitaAI, NVIDIA NIM, endpoints custom
- [Segurança](user-guide/security.md) — Aprovação de comandos, isolamento, allowlists

### Funcionalidades
- [Ferramentas & Toolsets](user-guide/features/tools.md) — 40+ tools, toolsets, backends de terminal
- [Sistema de Skills](user-guide/features/skills.md) — Skills Hub, skills bundladas, criando skills
- [Memória Persistente](user-guide/features/memory.md) — MEMORY.md, USER.md, busca FTS5, sumarização
- [Integração MCP](user-guide/features/mcp.md) — Conectando servidores MCP
- [Automações & Rotinas](user-guide/features/routines.md) — Cron, webhooks, script injection, multi-skill

---

## 🛠 Guia do Desenvolvedor

- [Arquitetura](developer-guide/architecture.md) — Core loop, módulos, fluxo de dados
- [Adicionando Tools](developer-guide/adding-tools.md) — Registry, schemas, toolsets
- [Criando Skills](developer-guide/creating-skills.md) — SKILL.md, frontmatter, scripts, condicionais
- [Plugins](developer-guide/plugins.md) — Plugin ABC, memory providers, image gen, context engines
- [Contribuindo](../CONTRIBUTING.md) — Setup de dev, code style, PR process
- [Segurança (Dev)](developer-guide/security.md) — Threat model, heurísticas, plugin trust

---

## 📚 Referência

- [Comandos CLI](reference/cli-commands.md) — Todos os comandos e flags
- [Variáveis de Ambiente](reference/environment-variables.md) — `DAMON_*`, `OPENROUTER_API_KEY`, etc.
- [Configuração Completa](reference/configuration.md) — Todas as opções do `config.yaml`
- [Skills Bundladas](reference/bundled-skills.md) — Lista de skills inclusas

---

## 🌐 Comunidade & Suporte

- **Issues:** [github.com/eapeli/damon/issues](https://github.com/eapeli/damon/issues)
- **Discussions:** [github.com/eapeli/damon/discussions](https://github.com/eapeli/damon/discussions)
- **Discord:** [discord.gg/damon](https://discord.gg/damon)
- **Skills Hub:** [agentskills.io](https://agentskills.io)

---

## ⚖️ Licença & Créditos

MIT — veja [LICENSE](../LICENSE).

**Criado por [Elisabete Alves](../author.md).**

Partes do código base derivam do [Hermes Agent](https://github.com/NousResearch/damon-agent) (MIT, by Nous Research), usado como fundação sob os termos da licença original.