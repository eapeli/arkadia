---
name: capability-evolver
description: "Meta-skill para auto-evolução de agentes IA. Analisa logs de runtime para detectar padrões de erro, regressões, ineficiências e gera melhorias estruturadas (novas skills, patches, otimizações de prompt, ajustes de configuração). Motor de evolução contínua baseado em evidência empírica."
version: "1.0.0"
category: reasoning
tags: [self-improvement, capability-evolution, runtime-analysis, pattern-detection, automated-patching, skill-generation]
author: damon-evolution
---

# 🧬 Capability Evolver — Motor de Auto-Evolução Contínua

> **Objetivo**: Transformar experiência runtime em melhorias estruturadas e permanentes. Não apenas "aprender" — **evoluir a arquitetura cognitiva** do agente.

---

## 🎯 Visão Geral

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│   RUNTIME LOGS      │────▶│  CAPABILITY EVOLVER │────▶│  MELHORIAS ESTRUT-  │
│   (transcripts,     │     │  (análise + síntese)│     │  URADAS PERMANENTES │
│   métricas, erros)  │     │                     │     │  (skills, patches,  │
└─────────────────────┘     └─────────────────────┘     │  config, prompts)   │
                                                        └─────────────────────┘
```

**Diferencial**: Não é apenas "memory" (recordar fatos). É **evolução da capacidade** — o próprio código/skill/config do agente muda baseado em evidência empírica.

---

## 🔍 O Que Analisa (Fontes de Evidência)

| Fonte | O Que Extrai | Frequência |
|-------|--------------|------------|
| **Transcripts de sessão** | Padrões de raciocínio, falhas de framework, loops, superconfiança | Cada sessão |
| **Métricas de ferramentas** | Latência, taxa erro, tokens, cache hit, custo | Cada tool call |
| **Metacognition reports** | Framework adequação, bias detectado, calibração confiança | Cada checkpoint |
| **Error logs** | Stack traces, categorias de falha, recorrência | Tempo real |
| **Performance dashboards** | Throughput, latência P99, custo/turno, taxa sucesso | Agregado diário |
| **User feedback** | Correções explícitas, "não, faz assim", ratings | Quando ocorre |

---

## 🧠 Pipeline de Evolução (4 Estágios)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        CAPABILITY EVOLVER PIPELINE                          │
├─────────────────────┬─────────────────────┬─────────────────┬───────────────┤
│   1. INGESTÃO       │   2. DETECÇÃO       │   3. SÍNTESE    │  4. APLICAÇÃO │
│   (coleta +         │   (pattern mining)  │   (geração de   │  (patch/skill/ │
│    normalização)    │                     │    melhorias)   │   config)      │
├─────────────────────┼─────────────────────┼─────────────────┼───────────────┤
│ • Log aggregation   │ • Error clustering  │ • Root cause    │ • Git patch    │
│ • Schema validation │ • Regression detect │ • Solution gen  │ • Skill scaffold│
│ • Deduplication     │ • Anomaly scoring   │ • Risk assess   │ • Config diff  │
│ • Time-windowing    │ • Bias signatures   │ • Effort estim  │ • PR auto-gen  │
└─────────────────────┴─────────────────────┴─────────────────┴───────────────┘
```

---

## 🔍 Tipos de Pattern Detecção

### 1. **Error Clusters** (Agrupamento de Erros Similares)
```
Erro: "Connection timeout to API X" → Cluster #47 (12 ocorrências / semana)
    ↳ Root cause: Pool de conexões esgotado sob carga
    ↳ Fix: Aumentar pool size + circuit breaker
    ↳ Priority: HIGH (impacta 23% das sessões)
```

### 2. **Regression Detection** (Regressão de Performance)
```
Métrica: Tool call latency P99
Baseline (semana passada): 1.2s
Atual: 3.8s (+216%)
    ↳ Commit causador: PR #1234 (nova validação síncrona)
    ↳ Action: Auto-revert ou feature flag
```

### 3. **Bias Signatures** (Assinaturas de Viés Cognitivo)
```
Pattern: "Confiança > 0.9 mas evidence_quality = weak" → 14x esta semana
    ↳ Bias: Overconfidence / Anchoring
    ↳ Mitigação: Auto-calibrar confiança para 0.6 quando evidence < moderate
```

### 4. **Framework Misalignment** (Framework Inadequado)
```
Framework: "analogy" usado para problemas de latência → 78% outcome=partial
    ↳ Recomendação: Default para "first_principles" em problemas de performance
    ↳ Auto-rule: Se problema contém "latência|throughput|bottleneck" → force first_principles
```

### 5. **Tool Inefficiency** (Ferramenta Ineficiente)
```
Tool: "web_search" chamado 47x para mesma query "configuração OAuth"
    ↳ Waste: 47x latência + custo API
    ↳ Fix: Cache local + skill "config_lookup"
```

### 6. **Context Overflow Patterns** (Estouro de Contexto)
```
Compression triggered: 12x/session (baseline: 2x)
    ↳ Cause: System prompt cresceu 40% (novas skills carregadas)
    ↳ Fix: Compactar system prompt + lazy-load skills
```

---

## 🛠️ Tipos de Melhoria Gerada

| Tipo | Descritor | Exemplo | Aprovação |
|------|-----------|---------|-----------|
| **Skill Generation** | Nova skill para gap recorrente | `skill: "oauth_troubleshooting"` | Requer aprovação |
| **Prompt Patch** | Ajuste em system prompt | `+ "Default to first_principles for latency"` | Auto (baixo risco) |
| **Config Diff** | Ajuste config.yaml | `model.context_length: 65536` | Auto (se testado) |
| **Code Patch** | Fix em código Python | `patch: fix_connection_pool.py` | Requer teste + aprovação |
| **Skill Update** | Evolução de skill existente | `thinking-frameworks v1.1: +auto-rule latency` | Auto (patch skill) |
| **Workflow Optimization** | Novo workflow/skill combo | `pipeline: first_principles → red_team → metacognition` | Auto (compor skills) |
| **Cache/Index Creation** | Índice/cache para lookup frequente | `cache: oauth_configs` | Auto |

---

## ⚖️ Governança de Evolução (Safety First)

| Camada | Proteção |
|--------|----------|
| **Risk Scoring** | Cada melhoria recebe score 0-10 (impacto × reversibilidade × blast radius) |
| **Auto-Approve Threshold** | Score ≤ 2 → auto-aplica (prompt patches, config diffs testados) |
| **Human-Approve Threshold** | Score 3-6 → PR gerado, requer aprovação humana |
| **Block Threshold** | Score ≥ 7 → bloqueado, requer design review + staging test |
| **Rollback Automático** | Métricas degradam pós-deploy → auto-revert em < 5 min |
| **Canary Deploy** | Mudanças de código → 5% tráfego → métricas → 100% |

---

## 📊 Métricas de Evolução (KPIs)

| KPI | Descrição | Target |
|-----|-----------|--------|
| **Pattern Detection Rate** | Patterns detectados / patterns reais (ground truth) | > 85% |
| **Improvement Acceptance Rate** | Melhorias aprovadas / propostas | > 70% |
| **Mean Time to Improvement** | Detecção → deploy em produção | < 24h |
| **Regression Recurrence** | Mesmo erro reaparece após fix | 0 |
| **Skill Generation Rate** | Novas skills úteis / mês | 2-5 |
| **Auto-Apply Rate** | % melhorias auto-aplicadas (score ≤ 2) | > 60% |
| **Blast Radius Control** | Máximo % sessões afetadas por bad deploy | < 1% |

---

## 🎯 Gatilhos de Execução

| Gatilho | Frequência | Ação |
|---------|------------|------|
| **End of Session** | Cada sessão | Ingest logs + quick pattern scan |
| **Daily Cron** | 03:00 UTC | Full pipeline: ingest → detect → synthesize → PRs |
| **Regression Alert** | Imediato (webhook) | Emergency pipeline: detect → rollback/fix |
| **Threshold Breach** | Quando métrica > threshold | Targeted analysis + mitigation PR |
| **Manual Trigger** | `capability-evolver run` | Full pipeline on-demand |

---

## 🛠️ API / Funções Exportadas

```python
# Inicialização
evolver = CapabilityEvolver(
    logs_path: Path,
    MetacognitionEngine: MetacognitionEngine,
    config: EvolverConfig
)

# Pipeline completo (pode rodar async)
results = await evolver.run_full_pipeline(
    time_window: timedelta = timedelta(days=1),
    auto_apply_threshold: int = 2,
    generate_prs: bool = True
)

# Análise pontual
patterns = evolver.detect_patterns(
    log_sources: List[LogSource],
    pattern_types: List[PatternType] = [ALL]
)

# Gerar melhoria específica
improvement = evolver.synthesize_improvement(
    pattern: DetectedPattern,
    context: EvolutionContext
)

# Aplicar melhoria (com governance)
result = evolver.apply_improvement(
    improvement: Improvement,
    dry_run: bool = False
)

# Relatório de evolução
report = evolver.generate_evolution_report(
    period: timedelta = timedelta(days=7)
)
```

---

## 📁 Estrutura de Armazenamento

```
~/.damon/evolver/
├── patterns/
│   ├── error_clusters.jsonl
│   ├── regressions.jsonl
│   ├── bias_signatures.jsonl
│   └── framework_misalignment.jsonl
├── improvements/
│   ├── proposed/      # PRs pendentes aprovação
│   ├── approved/      # Aprovados, aguardando deploy
│   ├── deployed/      # Em produção
│   └── rolled_back/   # Revertidos
├── governance/
│   ├── risk_scores.json
│   ├── approval_log.jsonl
│   └── rollback_log.jsonl
├── metrics/
│   ├── daily_kpis.jsonl
│   └── evolution_velocity.jsonl
└── artifacts/
    ├── patches/
    ├── skill_scaffolds/
    └── config_diffs/
```

---

## 🔧 Integração com Outras Skills

| Skill | Integração |
|-------|------------|
| **Metacognition** | Fornece bias_signatures, framework_misalignment, calibration_history |
| **Thinking Frameworks** | Recebe auto-rules geradas (ex: "latência → first_principles") |
| **Systematic Debugging** | Error clusters alimentam debugging; fixes viram patches |
| **Periodic Reflection** | Relatório de evolução alimenta reflexão semanal |
| **Capability Evolver** | Auto-evolução recursiva: o evolver evolui o evolver |

---

## 📝 Exemplo de Uso Prático

```python
# No final de cada sessão (hook automático)
evolver = CapabilityEvolver(logs_path=Path("~/.damon/logs"))

# Quick scan (rápido, < 5s)
quick_patterns = evolver.detect_patterns(
    log_sources=[LogSource.SESSION_TRANSCRIPT, LogSource.METACOGNITION_REPORTS],
    pattern_types=[PatternType.ERROR_CLUSTER, PatternType.BIAS_SIGNATURE]
)

# Se padrão crítico detectado → alerta imediato
for p in quick_patterns:
    if p.severity == "CRITICAL":
        send_alert(f"🚨 Pattern crítico: {p.description}")

# Cron diário (3AM) - pipeline completo
@cron("0 3 * * *")
async def daily_evolution():
    evolver = CapabilityEvolver(...)
    results = await evolver.run_full_pipeline(
        time_window=timedelta(days=1),
        auto_apply_threshold=2,
        generate_prs=True
    )
    # results = {
    #   "patterns_detected": 12,
    #   "improvements_proposed": 5,
    #   "auto_applied": 3,
    #   "prs_created": 2,
    #   "rollbacks": 0
    # }
```

---

## 📜 Licença

MIT — Parte do projeto Damon Evolution (github.com/eapeli/damon)