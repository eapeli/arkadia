# Primeira Conversa

## Iniciando

```bash
damon
```

Abre o **TUI interativo** — interface de terminal completa com:
- Edição multilinha (`Ctrl+Enter` para nova linha)
- Autocomplete de slash commands (`/`)
- Histórico de conversas (`↑`/`↓`)
- Streaming de ferramentas em tempo real
- Interrupção com `Ctrl+C`

---

## Comandos Essenciais

| Comando | Função |
|---------|--------|
| `/new` ou `/reset` | Nova conversa limpa |
| `/model [provedor:modelo]` | Troca modelo na hora |
| `/personality [nome]` | Define personalidade |
| `/skills` | Lista skills carregadas |
| `/<skill-name>` | Carrega skill específica |
| `/compress` | Comprime contexto manualmente |
| `/usage` | Mostra uso de tokens/custo |
| `/insights` | Análise de sessões recentes |
| `/retry` | Refaz última resposta |
| `/undo` | Desfaz último turno |
| `/stop` | Interrompe execução atual |

---

## Exemplo de Sessão

```bash
$ damon
Damon ☤  [claude-3.5-sonnet via openrouter]

Você: Olá! Me ajuda a criar um script Python que monitora um site e me avisa no Telegram se houver mudanças.

Damon: Claro! Vou criar um script que roda periodicamente e usa o gateway do Telegram.

[cria script ~/damon/scripts/monitor-site.py]
[configura cron job]

Pronto! O monitor roda a cada hora. Você só será notificado se houver mudanças reais (padrão [SILENT] evita spam).

Você: Legal. Pode usar o modelo mais barato pra isso?

Damon: Feito. Trocando para deepseek-chat via OpenRouter para este job.
/model openrouter:deepseek/deepseek-chat

Damon: Modelo alterado. O cron job usará este modelo nas próximas execuções.
```

---

## Dicas

- **Troca de modelo no meio da conversa:** `/model openrouter:gpt-4o-mini`
- **Ver skills disponíveis:** `/skills` ou `damon skills browse`
- **Carregar skill:** `/arxiv` (carrega skill arxiv)
- **Sair:** `Ctrl+D` ou `/exit`

---

## Próximos Passos

- [CLI & TUI](../user-guide/cli.md) — Keybindings, temas, sessões
- [Gateway de Mensagens](../user-guide/messaging.md) — Telegram, Discord, etc.
- [Sistema de Skills](../user-guide/features/skills.md) — Skills Hub, criando skills