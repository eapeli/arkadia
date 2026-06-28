# Integração MCP (Model Context Protocol)

O Damon funciona como **cliente MCP** — conecta a servidores MCP para estender capacidades com tools, resources e prompts externos.

---

## O Que é MCP

[Model Context Protocol](https://modelcontextprotocol.io) — padrão aberto para conectar LLMs a fontes de dados e ferramentas externas via JSON-RPC.

---

## Conectando Servidores MCP

```bash
# Adiciona servidor MCP
damon mcp add nome-do-servidor --command "npx -y @modelcontextprotocol/server-github" --env GITHUB_TOKEN

# Lista servidores
damon mcp list

# Remove
damon mcp remove nome-do-servidor
```

---

## Configuração (config.yaml)

```yaml
mcp:
  servers:
    github:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_TOKEN: "${GITHUB_TOKEN}"

    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projetos"]

    postgresql:
      command: "docker"
      args: ["run", "-i", "--rm", "-e", "POSTGRES_URL", "mcp/postgres"]
      env:
        POSTGRES_URL: "${DATABASE_URL}"
```

---

## Servidores MCP Populares

| Servidor | Comando | Uso |
|----------|---------|-----|
| GitHub | `npx -y @modelcontextprotocol/server-github` | Repos, issues, PRs, code |
| Filesystem | `npx -y @modelcontextprotocol/server-filesystem <path>` | Leitura/escrita arquivos |
| PostgreSQL | `docker run -i --rm mcp/postgres` | Queries SQL seguras |
| SQLite | `npx -y @modelcontextprotocol/server-sqlite <db>` | Queries locais |
| Brave Search | `npx -y @modelcontextprotocol/server-brave-search` | Busca web |
| Puppeteer | `npx -y @modelcontextprotocol/server-puppeteer` | Browser automation |

---

## Descobrindo Tools MCP

Após conectar, tools MCP aparecem como tools nativas:

```bash
damon tools list | grep mcp
# mcp_github__list_repos
# mcp_github__create_issue
# mcp_filesystem__read_file
# mcp_postgresql__query
```

Use naturalmente na conversa:
> "Lista meus repos privados no GitHub"
> "Lê o arquivo /home/user/projetos/config.json"
> "Executa SELECT * FROM users WHERE active=1"

---

## Segurança

- **Allowlist por servidor:** Configure quais tools MCP ficam expostas
- **Env vars isoladas:** Secrets injetados só no processo do servidor MCP
- **Timeouts:** Tools MCP respeitam `network.timeout` do config
- **Sandbox:** Servidores rodam em subprocesso isolado

---

## Criando Seu Próprio Servidor MCP

```python
# mcp_server.py
from mcp import Server
from mcp.types import Tool

server = Server("meu-servidor")

@server.tool()
def minha_ferramenta(param: str) -> str:
    """Descrição da ferramenta."""
    return f"Resultado: {param}"

if __name__ == "__main__":
    server.run()
```

```bash
damon mcp add meu-servidor --command "python" --args "mcp_server.py"
```

---

## Próximos

- [Automações & Rotinas](../features/routines.md)
- [Configuração](../configuration.md)
- [Criando Plugins (Dev)](../../developer-guide/plugins.md)