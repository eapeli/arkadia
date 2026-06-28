# Memória Persistente

O Damon mantém memória de longo prazo entre sessões — aprende sobre você, lembra preferências, fatos e contexto.

---

## Tipos de Memória

| Arquivo | Propósito | Gerenciado Por |
|---------|-----------|----------------|
| `~/.damon/memories/MEMORY.md` | Fatos sobre o usuário, preferências, contexto duradouro | Agente (auto) + Usuário |
| `~/.damon/memories/USER.md` | Perfil do usuário: nome, estilo, objetivos,背景 | Usuário (manual) |
| `~/.damon/state.db` | Sessões completas, FTS5 search, títulos | Sistema (auto) |

---

## Como Funciona

1. **Durante conversa:** Agente extrai fatos relevantes → salva no `MEMORY.md`
2. **Nudges periódicos:** Agente revisa memória, consolida, remove duplicatas
3. **Nova sessão:** `MEMORY.md` + `USER.md` injetados no system prompt
3. **Busca:** FTS5 no `state.db` + sumarização LLM para recall cross-sessão

---

## Editando Memória

```bash
# Edita MEMORY.md
damon memory edit

# Edita USER.md (perfil)
damon memory edit --user

# Visualiza
damon memory show
damon memory show --user
```

Formato `MEMORY.md`:
```markdown
# Memória do Usuário

## Preferências
- Modelo preferido: Claude 3.5 Sonnet
- Idioma: Português (BR)
- Tema: dracula

## Fatos
- Trabalha com: Python, Node.js, Lua (FiveM)
- Horário preferido: Noturno
- Projeto atual: Hospital RP no FiveM

## Contexto de Projetos
- damon-agent: Contribuidor principal
- fiveM-hospital: Game dev + modeling 3D
```

---

## Busca de Sessões (FTS5)

```bash
# Busca no histórico
damon sessions search "termo"

# Busca com janela de contexto
damon sessions search "bug fix" --window 10

# Lista sessões recentes
damon sessions list --days 7
```

---

## Provedores de Memória Externos

Além do `local` (arquivos + SQLite), suporta:

| Provedor | Característica |
|----------|----------------|
| `honcho` | Dialético, modelagem de usuário |
| `mem0` | Memória vetorial gerenciada |
| `supermemory` | RAG pessoal |
| `byterover` | Embeddings locais |
| `holographic` | Memória holográfica |
| `openviking` | Viking memory |
| `retaindb` | Banco de retenção |

Configure em `config.yaml`:
```yaml
memory:
  provider: honcho
  honcho:
    api_key: ${HONCHO_API_KEY}
```

> Provedores externos são **plugins** — instale separadamente se não vierem bundled.

---

## Privacidade

- `MEMORY.md` e `USER.md` são **seus arquivos** — edite, apague, version
- `state.db` é SQLite local — `damon sessions delete` remove sessão
- Nada sai da sua máquina sem seu comando
- Gateway criptografa em trânsito; sessões podem salvar JSONL local opcional

---

## Próximos

- [Integração MCP](../features/mcp.md)
- [Automações & Rotinas](../features/routines.md)
- [Configuração](../configuration.md)