# Ferramentas & Toolsets

O Damon expõe 40+ ferramentas organizadas em **toolsets**. Ative apenas o que precisa.

---

## Toolsets Inclusos

| Toolset | Ferramentas | Descrição |
|---------|-------------|-----------|
| `core` | `read_file`, `write_file`, `patch`, `search_files`, `execute_code` | Sistema de arquivos + execução Python |
| `terminal` | `terminal` | Shell (local, Docker, SSH, Modal, Daytona) |
| `web` | `web_search`, `web_extract` | Busca (OpenRouter/Serper) + extração |
| `browser` | `browser_navigate`, `browser_click`, `browser_type`, `browser_snapshot` | Automação browser real |
| `coding` | `code_execution`, `delegate_task` | Python sandboxed + subagentes |
| `media` | `image_generate`, `vision_analyze`, `text_to_speech` | Imagem, visão, TTS |
| `skills` | `skill_view`, `skill_manage` | Sistema de skills |

---

## Ativando/Desativando

```bash
# Via CLI
damon tools enable web browser
damon tools disable media

# Via config.yaml
toolsets: [core, terminal, web, browser, skills]
```

---

## Referência Rápida das Tools

### Sistema de Arquivos (`core`)
| Tool | Descrição |
|------|-----------|
| `read_file` | Lê arquivo (com offset/limit) |
| `write_file` | Escreve arquivo (cria dirs) |
| `patch` | Edição cirúrgica (find/replace) |
| `search_files` | Busca conteúdo (regex) ou arquivos (glob) |
| `execute_code` | Python com acesso a tools RPC |

### Terminal (`terminal`)
| Tool | Descrição |
|------|-----------|
| `terminal` | Executa comando no backend configurado (local/Docker/SSH/Modal/Daytona) |

### Web (`web`)
| Tool | Descrição |
|------|-----------|
| `web_search` | Busca (Serper/OpenRouter/Google) |
| `web_extract` | Extrai conteúdo (markdown) de URLs/PDFs |

### Browser (`browser`)
| Tool | Descrição |
|------|-----------|
| `browser_navigate` | Navega para URL |
| `browser_click` | Clica elemento (ref ID) |
| `browser_type` | Digita em input |
| `browser_snapshot` | Accessibility tree |
| `browser_scroll` | Scroll up/down |
| `browser_press` | Tecla (Enter, Tab, etc) |
| `browser_console` | Logs JS / eval expression |
| `browser_vision` | Screenshot + análise visual |

### Coding (`coding`)
| Tool | Descrição |
|------|-----------|
| `code_execution` | Python isolado, RPC para tools |
| `delegate_task` | Subagentes paralelos com isolamento |

### Media (`media`)
| Tool | Descrição |
|------|-----------|
| `image_generate` | Gera imagem (FAL/OpenAI) |
| `vision_analyze` | Analisa imagem (multimodal) |
| `text_to_speech` | TTS (OpenAI/Edge/Coqui) |

---

## Backends de Terminal

| Backend | Caso de Uso |
|---------|-------------|
| `local` | Padrão — executa no host |
| `docker` | Isolamento de containers |
| `ssh` | Servidor remoto |
| `singularity` | HPC/containers científicos |
| `modal` | Serverless (hiberna ocioso) |
| `daytona` | Workspaces serverless persistentes |

---

## Próximos

- [Sistema de Skills](../features/skills.md)
- [Memória](../features/memory.md)
- [Configuração](../configuration.md)