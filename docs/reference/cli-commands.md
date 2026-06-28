# Comandos CLI — Referência Completa

---

## Principais

| Comando | Descrição |
|---------|-----------|
| `damon` | TUI interativo |
| `damon chat "msg"` | One-shot (sem TUI) |
| `damon -q "msg"` | Quiet mode — só resposta |
| `damon version` | Versão + build info |
| `damon doctor` | Diagnóstico completo |
| `damon update` | Atualiza para latest |
| `damon setup` | Wizard de configuração |

---

## Configuração

| Comando | Descrição |
|---------|-----------|
| `damon config show` | Config resolvida (com env vars) |
| `damon config set <key> <value>` | Define valor |
| `damon config get <key>` | Obtém valor |
| `damon config reset <key>` | Reseta para default |
| `damon config edit` | Abre no editor |

---

## Modelos

| Comando | Descrição |
|---------|-----------|
| `damon model` | Lista modelos disponíveis |
| `damon model set <provider:model>` | Define modelo padrão |
| `damon model list <provider>` | Lista modelos de provedor |
| `damon model search <termo>` | Busca modelos |

---

## Ferramentas (Tools)

| Comando | Descrição |
|---------|-----------|
| `damon tools` | Lista tools ativas por toolset |
| `damon tools enable <toolset...>` | Ativa toolset(s) |
| `damon tools disable <toolset...>` | Desativa toolset(s) |
| `damon tools list` | Todas tools com status |

---

## Skills

| Comando | Descrição |
|---------|-----------|
| `damon skills list` | Skills carregadas |
| `damon skills load <nome>` | Carrega skill |
| `damon skills unload <nome>` | Descarrega skill |
| `damon skills browse` | Skills Hub (remoto) |
| `damon skills install <nome>` | Instala do Hub |
| `damon skills create "desc"` | Cria skill nova (guided) |
| `damon skills edit <nome>` | Edita skill local |

---

## Gateway de Mensagens

| Comando | Descrição |
|---------|-----------|
| `damon gateway setup` | Wizard de plataformas |
| `damon gateway start` | Inicia gateway |
| `damon gateway stop` | Para gateway |
| `damon gateway status` | Status + plataformas |
| `damon gateway logs` | Logs recentes |

---

## Cron / Automações

| Comando | Descrição |
|---------|-----------|
| `damon cron create "schedule" "prompt" [opts]` | Cria job |
| `damon cron list` | Lista jobs |
| `damon cron show <nome>` | Detalhes do job |
| `damon cron run <nome>` | Executa manual |
| `damon cron pause <nome>` | Pausa |
| `damon cron resume <nome>` | Retoma |
| `damon cron delete <nome>` | Remove |
| `damon cron logs <nome>` | Histórico execuções |

---

## Webhooks

| Comando | Descrição |
|---------|-----------|
| `damon webhook subscribe <nome> --events "..." --prompt "..." --deliver <target>` | Cria webhook |
| `damon webhook list` | Lista webhooks |
| `damon webhook delete <nome>` | Remove |

---

## Sessões / Memória

| Comando | Descrição |
|---------|-----------|
| `damon sessions list` | Lista sessões |
| `damon sessions show <id>` | Mostra sessão |
| `damon sessions search "termo"` | Busca FTS5 |
| `damon sessions delete <id>` | Apaga sessão |
| `damon memory show` | Mostra MEMORY.md |
| `damon memory edit` | Edita MEMORY.md |
| `damon memory show --user` | Mostra USER.md |

---

## MCP

| Comando | Descrição |
|---------|-----------|
| `damon mcp add <nome> --command "..." --args "..."` | Adiciona servidor |
| `damon mcp list` | Lista servidores |
| `damon mcp remove <nome>` | Remove |

---

## Profiles

| Comando | Descrição |
|---------|-----------|
| `damon profile list` | Lista profiles |
| `damon profile create <nome>` | Cria profile |
| `damon profile switch <nome>` | Troca profile |
| `damon profile delete <nome>` | Remove |

---

## Desktop

| Comando | Descrição |
|---------|-----------|
| `damon desktop` | Abre app desktop |
| `damon desktop build` | Build instalador |

---

## Slash Commands (No TUI / Gateway)

| Comando | Função |
|---------|--------|
| `/new` `/reset` | Nova conversa |
| `/model [p:m]` | Troca modelo |
| `/personality [nome]` | Define persona |
| `/skills` | Lista skills |
| `/<skill>` | Carrega skill |
| `/compress` | Comprime contexto |
| `/usage` | Uso tokens/custo |
| `/insights [--days N]` | Análise sessões |
| `/retry` `/undo` | Refaz/desfaz |
| `/stop` | Interrompe |
| `/platforms` | Status gateway |
| `/sethome` | Define canal home |

---

## Flags Globais

| Flag | Descrição |
|------|-----------|
| `--config <path>` | Config customizado |
| `--profile <nome>` | Profile específico |
| `--verbose` `-v` | Log DEBUG |
| `--quiet` `-q` | Só output essencial |
| `--no-color` | Sem cores |
| `--help` `-h` | Ajuda |