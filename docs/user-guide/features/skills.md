# Sistema de Skills

Skills são **memória procedural** do Damon — instruções reutilizáveis que ensinam capacidades específicas.

---

## Conceitos

| Conceito | Descrição |
|----------|-----------|
| **Skill** | Markdown (SKILL.md) + scripts opcionais |
| **Categoria** | Diretório organizador (ex: `research/`, `productivity/`) |
| **Skills Hub** | Registro descoberto remotamente (`damon skills browse`) |
| **Bundled** | Inclusas no repo (`skills/`, `optional-skills/`) |
| **Criadas pelo agente** | Geradas autonomamente após tarefas complexas |

---

## Estrutura

```
skills/
├── research/
│   └── arxiv/
│       ├── SKILL.md              # Obrigatório
│       ├── scripts/
│       │   └── search_arxiv.py
│       └── references/
│           └── api.md
├── productivity/
│   └── ocr-and-documents/
│       ├── SKILL.md
│       └── scripts/
└── optional-skills/              # Oficiais, não ativadas por padrão
    └── paid-service/
```

---

## Formato SKILL.md

```markdown
---
name: minha-skill
description: Busca papers no arXiv por palavra-chave, autor ou categoria.
version: 1.0.0
author: Seu Nome
license: MIT
platforms: [macos, linux, windows]  # Opcional: restringe plataforma
required_environment_variables:     # Setup seguro on-load
  - name: ARXIV_API_KEY
    prompt: arXiv API key
    help: https://arxiv.org/help/api/user-manual
    required_for: full functionality
prerequisites:                      # Legacy (ainda suportado)
  env_vars: [ARXIV_API_KEY]
  commands: [curl, jq]
metadata:
  damon:
    tags: [Research, Papers, arXiv]
    related_skills: [semantic-scholar]
    fallback_for_toolsets: [web]    # Só aparece se web toolset indisponível
    requires_toolsets: [terminal]   # Só aparece se terminal disponível
---

# Minha Skill

Breve introdução.

## When to Use
- Condição 1
- Condição 2

## Quick Reference
| Comando | Descrição |
|---------|-----------|
| `arxiv search "termo"` | Busca papers |

## Procedure
1. Passo 1
2. Passo 2

## Pitfalls
- Problema conhecido → solução

## Verification
Como confirmar que funcionou.
```

---

## Usando Skills

```bash
# Lista skills carregadas
/skills
damon skills list

# Carrega skill específica
/arxiv
damon skills load arxiv

# Browse Hub (remoto)
damon skills browse
damon skills install semantic-scholar

# Cria skill nova (agent-guided)
damon skills create "minha skill"
```

---

## Skills Bundladas (Inclusas)

| Skill | Categoria | Descrição |
|-------|-----------|-----------|
| `arxiv` | research | Busca papers no arXiv |
| `semantic-scholar` | research | Busca no Semantic Scholar |
| `github-code-review` | productivity | Review de PRs via GitHub |
| `himalaya` | email | Email via CLI (IMAP/SMTP) |
| `gif-search` | media | Busca GIFs no Tenor |
| `youtube-content` | media | Transcripts/summaries YouTube |
| `polymarket` | research | Mercados de previsão |
| `segment-anything` | vision | Segmentação SAM |
| `audiocraft` | audio | MusicGen/AudioGen |

---

## Skills Oficiais Opcionais (optional-skills/)

Ative com: `damon skills install <nome>`

| Skill | Requer |
|-------|--------|
| `wandb` | WANDB_API_KEY |
| `huggingface` | HF_TOKEN |
| `openai-gpt` | OPENAI_API_KEY |

---

## Criando Sua Própria Skill

1. **Estrutura:**
```bash
mkdir -p ~/.damon/skills/minha-categoria/minha-skill/scripts
```

2. **SKILL.md** — siga o formato acima

3. **Scripts** — Python/Shell em `scripts/`

4. **Teste:**
```bash
damon skills load minha-skill
/minha-skill
```

---

## Ativação Condicional

Skills podem declarar quando aparecem:

```yaml
metadata:
  damon:
    fallback_for_toolsets: [web]      # Só se web INDISPONÍVEL
    requires_toolsets: [terminal]     # Só se terminal DISPONÍVEL
    fallback_for_tools: [web_search]  # Só se web_search INDISPONÍVEL
    requires_tools: [terminal]        # Só se terminal DISPONÍVEL
```

Útil para:
- Fallbacks gratuitos (DuckDuckGo quando Firecrawl indisponível)
- Skills que precisam de terminal
- Alternativas locais para APIs pagas

---

## Próximos

- [Memória](../features/memory.md)
- [Criando Skills (Dev)](../../developer-guide/creating-skills.md)
- [Configuração](../configuration.md)