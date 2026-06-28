# Gateway de Mensagens

O gateway permite conversar com o Damon via Telegram, Discord, WhatsApp, Slack, Signal e Email — tudo a partir de um único processo.

---

## Setup Rápido

```bash
damon gateway setup    # Wizard interativo
damon gateway start    # Inicia gateway
```

O wizard configura:
1. Plataformas desejadas
2. Tokens/credenciais por plataforma
3. Canais home (onde o bot responde)
4. Allowlist de usuários autorizados

---

## Plataformas Suportadas

| Plataforma | Configuração | Recursos |
|------------|--------------|----------|
| **Telegram** | Bot token + chat IDs | Comandos, voz, arquivos, forums/topics |
| **Discord** | Bot token + app ID | Slash commands, voice, threads |
| **WhatsApp** | Baileys (QR) ou Cloud API | Mensagens, mídia, grupos |
| **Slack** | Bot token + signing secret | Slash commands, blocks, threads |
| **Signal** | signal-cli | Criptografia E2E, grupos |
| **Email** | IMAP/SMTP | Leitura/envio, anexos |

---

## Configuração Manual

```yaml
# ~/.damon/config.yaml
gateway:
  enabled: true
  platforms:
    telegram:
      enabled: true
      bot_token: "${TELEGRAM_BOT_TOKEN}"
      allowed_users: [123456789]
      home_chat_id: -1001234567890
    discord:
      enabled: true
      bot_token: "${DISCORD_BOT_TOKEN}"
      application_id: "123456789012345678"
      allowed_users: ["123456789012345678"]
      home_channel_id: "123456789012345678"
```

> **Segurança:** Tokens ficam no `~/.damon/.env` (chmod 600), nunca no config.yaml.

---

## Uso no Mensageiro

Após `damon gateway start`, mande mensagem pro bot:

| Comando | Função |
|---------|--------|
| `/new` ou `/reset` | Nova conversa |
| `/model [provedor:modelo]` | Troca modelo |
| `/personality [nome]` | Define personalidade |
| `/skills` | Lista skills |
| `/<skill-name>` | Carrega skill |
| `/compress`, `/usage`, `/insights` | Contexto/uso |
| `/retry`, `/undo` | Refaz/desfaz |
| `/stop` | Interrompe |
| `/status` | Status do gateway |
| `/sethome` | Define canal atual como home |

---

## Entrega de Automações

Cron jobs e webhooks entregam resultados no mensageiro:

```bash
damon cron create "0 9 * * *" "Digest diário" --deliver telegram
damon webhook subscribe alert --events "push" --deliver discord
```

Destinos suportados:
- `telegram` — canal home
- `telegram:-1001234567890:42` — topic específico
- `discord` — canal home
- `slack` — canal home
- `sms:+15551234567` — SMS
- `email` — email
- `local` — arquivo, sem notificação

---

## Pairing (Segurança)

Para DMs privados, o Damon exige pairing:

```bash
damon pairing add <user_id>    # Autoriza usuário
damon pairing list             # Lista autorizados
damon pairing remove <user_id> # Revoga
```

---

## Próximos

- [Configuração](../configuration.md)
- [Segurança](../security.md)
- [Automações & Rotinas](../features/routines.md)