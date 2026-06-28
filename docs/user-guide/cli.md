# CLI & TUI

## Iniciando

```bash
damon                    # TUI interativo
damon chat "sua mensagem"    # One-shot, sem TUI
damon -q "pergunta"     # Quiet mode, só resposta
```

---

## Keybindings (TUI)

| Tecla | Ação |
|-------|------|
| `Enter` | Envia mensagem |
| `Ctrl+Enter` | Nova linha (multilinha) |
| `↑` / `↓` | Histórico de comandos |
| `Tab` | Autocomplete slash commands |
| `Ctrl+C` | Interrompe execução atual |
| `Ctrl+D` | Sai do TUI |
| `Ctrl+L` | Limpa tela |
| `Ctrl+R` | Busca no histórico (fuzzy) |
| `Ctrl+U` | Limpa linha atual |

---

## Slash Commands

```bash
/model [provedor:modelo]     # Troca modelo
/personality [nome]           # Define personalidade
/skills                       # Lista skills
/<skill-name>                # Carrega skill
/new                         # Nova conversa
/reset                       # Reset completo
/compress                    # Comprime contexto
/usage                       # Uso de tokens
/insights [--days N]         # Análise de sessões
/retry                       # Refaz última resposta
/undo                        # Desfaz último turno
/stop                        # Interrompe execução
/platforms                   # Status gateway
/sethome                     # Define canal home (gateway)
```

---

## Temas & Personalização

```bash
damon skin list             # Lista skins disponíveis
damon skin set <nome>       # Define skin
damon skin preview <nome>   # Preview
```

Skins inclusas: `default`, `dracula`, `nord`, `tokyo-night`, `catppuccin`, `gruvbox`, `rose-pine`, `kanagawa`

---

## Sessões

```bash
damon sessions list         # Lista sessões
damon sessions show <id>    # Mostra sessão
damon sessions delete <id>  # Apaga sessão
damon sessions search "termo"  # Busca full-text (FTS5)
```

---

## Configuração Rápida

```bash
damon config set model.provider openrouter
damon config set model.model anthropic/claude-3.5-sonnet
damon config set toolsets '["core","terminal","web","skills"]'
damon config show           # Mostra config resolvida
```

---

## Próximos

- [Personalidades](personalities.md)
- [Gateway de Mensagens](messaging.md)
- [Configuração](../configuration.md)