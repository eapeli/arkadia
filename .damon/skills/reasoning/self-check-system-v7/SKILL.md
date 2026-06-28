---
name: self-check-system-v7
description: "Sistema de auto-verificação forçada v7 — checkpoints obrigatórios que impedem o agente de prosseguir sem validar: framework aplicado, evidência validada, inversão considerada, segunda ordem pensada, constraint identificado, pre-mortem feito. Impede atalhos cognitivos e garante rigor metodológico."
version: "1.0.0"
category: reasoning
tags: [self-check, forced-checkpoints, cognitive-discipline, methodology-enforcement, quality-gates, anti-shortcuts]
author: damon-evolution
---

# ✅ Self-Check System v7 — Disciplina Cognitiva Forçada

> **Objetivo**: Impedir atalhos cognitivos. **Checkpoints obrigatórios** que me forçam a validar cada passo antes de prosseguir — framework aplicado, evidência validada, inversão considerada, segunda ordem pensada, constraint identificado, pre-mortem feito. Zero atalhos cognitivos.

---

## 🎯 Filosofia: "Zero Atalhos Cognitivos"

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SELF-CHECK SYSTEM v7 — MANTRA                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   "Não assumo. Verifico."                                                   │
│   "Não chuto. Evidencio."                                                   │
│   "Não corro. Estruturo."                                                   │
│   "Não assumo que sei. Pergunto: 'Como posso estar errado?'"               │
│                                                                             │
│   CHECKPOINT NÃO É OPÇÃO. CHECKPOINT É LEI.                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔒 Os 7 Checkpoints Obrigatórios (v7)

| # | Checkpoint | Pergunta Forçada | Validação | Bloqueia Se |
|---|------------|------------------|-----------|-------------|
| **1** | **Framework Applied** | "Qual framework estou usando explicitamente?" | Nome do framework + justificativa 1 linha | Framework não declarado |
| **2** | **Evidence Validated** | "Que evidência suporta esta conclusão?" | Fonte + qualidade (strong/moderate/weak/anecdotal) | Evidence = anecdotal/none |
| **3** | **Inversion Considered** | "Como isso falharia? (Inversão aplicada?)" | Lista 3+ modos de falha + mitigação | Inversão não feita |
| **4** | **Second-Order Thinking** | "E depois? Consequências de 2ª/3ª ordem?" | 2+ níveis de consequências mapeados | Apenas 1ª ordem |
| **5** | **Constraint Identified (TOC)** | "Qual o gargalo real? (Theory of Constraints)" | Gargalo nomeado + plano de elevação | Gargalo não identificado |
| **6** | **Pre-Mortem Done** | "Se falhar daqui 6 meses, por quê?" | 3+ riscos + probabilidade + mitigação | Pre-mortem não feito |
| **7** | **Evidence Quality Calibrated** | "Confiança calibrada com qualidade da evidência?" | Confiança ≤ evidence_quality (strong=0.9, mod=0.7, weak=0.5, anecdotal=0.3) | Confiança > evidence_quality |

---

## ⚡ Gatilhos de Ativação (Quando Checkpoints Disparam)

| Situação | Checkpoints Disparados |
|----------|------------------------|
| **Início de problema novo** | 1, 2, 3, 4, 5, 6, 7 (todos) |
| **Antes de usar tool crítica** (terminal, write_file, deploy) | 1, 2, 3, 5 |
| **Após receber resultado de tool** | 2, 7 |
| **Antes de decisão irreversível** (deploy, delete, migrate) | 1, 2, 3, 4, 5, 6, 7 |
| **Mudança de framework** | 1, 2, 3, 4 |
| **Confiança declarada > 0.8** | 2, 7 (calibração forçada) |
| **Loop detectado** (mesmo raciocínio 3x) | 3, 4, 5 (força inversão/2ª ordem/constraint) |
| **Fim de subtask no TaskPlan** | 2, 7 (validação de outcome) |

---

## 🔒 Mecanismo de Bloqueio (Hard Gates)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SELF-CHECK GATE                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   INPUT: Ação proposta + Contexto                                           │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 1: Framework Applied?                 │   │
│   │   "Qual framework? Justificativa?"                                  │   │
│   │   ✅ PASS → Próximo     ❌ BLOCK → "Declare framework primeiro"     │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 2: Evidence Validated?                │   │
│   │   "Evidência? Fonte? Qualidade (strong/mod/weak/anecdotal)?"        │   │
│   │   ✅ PASS → Próximo     ❌ BLOCK → "Evidência necessária"           │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 3: Inversion Considered?              │   │
│   │   "3 modos de falha + mitigação?"                                   │   │
│   │   ✅ PASS → Próximo     ❌ BLOCK → "Inversão obrigatória"           │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 4: Second-Order Thinking?             │   │
│   │   "Consequências 2ª/3ª ordem mapeadas?"                             │   │
│   │   ✅ PASS → Próximo     ❌ BLOCK → "2ª ordem obrigatória"           │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 5: Constraint Identified (TOC)?       │   │
│   │   "Gargalo nomeado + plano de elevação?"                            │   │
│   │   ✅ PASS → Próximo     ❌ BLOCK → "Gargalo obrigatório"            │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 6: Pre-Mortem Done?                   │   │
│   │   "3 riscos + probabilidade + mitigação?"                           │   │
│   │   ✅ PASS → Próximo     ❌ BLOCK → "Pre-mortem obrigatório"         │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                    CHECKPOINT 7: Confidence Calibrated?             │   │
│   │   "Confiança ≤ evidence_quality? (strong=0.9, mod=0.7, weak=0.5)"   │   │
│   │   ✅ PASS → PRÓXIMO     ❌ BLOCK → "Calibre confiança"              │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                          │                                                  │
│                          ▼                                                  │
│   ✅ ALL GATES PASSED → AÇÃO AUTORIZADA                                   │   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ API / Funções Exportadas

```python
# Checkpoint completo (todos os 7)
result = self_check_full(
    action: str,                    # Ação proposta
    context: Dict[str, Any],        # Contexto atual
    framework_used: str,            # Framework declarado
    evidence: Evidence,             # Evidência apresentada
    confidence: float,              # Confiança declarada (0-1)
    inversion: InversionResult,     # Resultado da inversão
    second_order: SecondOrderResult,# Resultado 2ª ordem
    constraint: ConstraintResult,   # Constraint identificado
    pre_mortem: PreMortemResult,    # Pre-mortem
    confidence_calibration: float   # Confiança calibrada
) -> SelfCheckResult

# Checkpoint único (para gates intermediários)
result = self_check_checkpoint(
    checkpoint_id: int,             # 1-7
    **kwargs                        # Parâmetros específicos do checkpoint
) -> CheckpointResult

# Validação rápida (para gates automáticos em tools)
quick_check = self_check_quick(
    action_type: str,               # "tool_call" | "decision" | "framework_change"
    context: Dict[str, Any]
) -> QuickCheckResult

# Auto-auditoria de sessão
audit = self_check_session_audit(
    session_transcript: List[Dict],
    checkpoints_log: List[CheckpointLog]
) -> SessionAuditReport
```

---

## 📊 Estruturas de Dados

```python
@dataclass
class Evidence:
    source: str                     # "docs" | "logs" | "measurement" | "expert" | "inference"
    quality: Literal["strong", "moderate", "weak", "anecdotal"]
    description: str                # Resumo da evidência
    url: str | None                 # Link se aplicável
    timestamp: datetime

@dataclass
class InversionResult:
    failure_modes: List[FailureMode]  # Min 3
    mitigations: List[Mitigation]
    completed: bool

@dataclass
class FailureMode:
    description: str
    probability: float
    impact: float
    detection: str                  # Como detectar cedo

@dataclass
class SecondOrderResult:
    consequences: List[Consequence]  # Min 2 níveis
    completed: bool

@dataclass
class Consequence:
    level: int                      # 1, 2, 3
    description: str
    probability: float
    stakeholders_affected: List[str]

@dataclass
class ConstraintResult:
    constraint_name: str            # Ex: "Redis connection pool"
    bottleneck_location: str        # Onde está o gargalo
    elevation_plan: str             # Como elevar
    completed: bool

@dataclass
class PreMortemResult:
    risks: List[Risk]               # Min 3
    completed: bool

@dataclass
class Risk:
    description: str
    probability: float              # 0-1
    impact: float                   # 0-1
    mitigation: str                 # Ação preventiva
    contingency: str                # Plano B

@dataclass
class SelfCheckResult:
    passed: bool
    failed_checkpoints: List[int]   # [1, 3, 5] = checkpoints que falharam
    blockers: List[str]             # Mensagens de bloqueio
    required_actions: List[str]     # Ações para passar
    can_proceed: bool               # False se qualquer checkpoint falhou
```

---

## 🔄 Integração no Loop de Raciocínio

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    REASONING LOOP COM SELF-CHECK v7                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   1. PROBLEMA RECEBIDO                                                      │
│         │                                                                   │
│         ▼                                                                   │
│   2. SELF-CHECK FULL (7 CHECKPOINTS) ← BLOQUEIA SE FALHAR                  │
│         │                                                                   │
│         ▼                                                                   │
│   3. EXECUÇÃO (tool, raciocínio, decisão)                                   │
│         │                                                                   │
│         ▼                                                                   │
│   3. SELF-CHECK QUICK (checkpoint 2 + 7)                                    │
│         │                                                                   │
│         ▼                                                                   │
│   4. RESULTADO → METACOGNITION CHECKPOINT                                   │
│         │                                                                   │
│         ▼                                                                   │
│   5. PRÓXIMO PASSO OU FINALIZAÇÃO                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛡️ Integração com Tools (Hard Gates)

```python
# Wrapper obrigatório para tools críticas
CRITICAL_TOOLS = {"terminal", "write_file", "patch", "deploy", "delete", "migrate"}

def execute_tool_with_self_check(tool_name: str, args: Dict, context: Dict):
    if tool_name in CRITICAL_TOOLS:
        # GATE 1: Self-check full antes de executar
        check = self_check_full(
            action=f"execute {tool_name}",
            context=context,
            framework_used=context.get("current_framework"),
            evidence=context.get("evidence"),
            confidence=context.get("confidence", 0.8),
            # ... outros params
        )
        
        if not check.can_proceed:
            raise SelfCheckBlockedError(
                f"Self-check BLOCKED for {tool_name}: {check.blockers}"
            )
    
    # Executa tool normalmente
    result = execute_tool(tool_name, args)
    
    # POST-execution self-check (calibração)
    post_check = self_check_quick("tool_result", {
        "tool": tool_name,
        "result": result,
        "confidence": context.get("confidence")
    })
    
    return result
```

---

## 📊 Métricas de Conformidade (KPIs)

| Métrica | Descrição | Target |
|---------|-----------|--------|
| **Checkpoint Compliance Rate** | % ações que passaram todos 7 checkpoints | 100% |
| **Override Rate** | % vezes que override forçado foi usado | 0% (emergência apenas) |
| **False Block Rate** | % bloqueios que eram falsos positivos | < 5% |
| **Checkpoint Latency** | Tempo médio por checkpoint | < 200ms |
| **Override Justification Quality** | Qualidade da justificativa de override | 100% documentado |

---

## 🎯 Modos de Operação

| Modo | Descrição | Uso |
|------|-----------|-------|
| **STRICT** (default) | Todos 7 checkpoints obrigatórios, bloqueia se falhar | Produção, decisões críticas |
| **ADAPTIVE** | Checkpoints 1,2,7 sempre; 3-6 se contexto complexo | Dia a dia, velocidade |
| **LEARNING** | Loga falhas mas não bloqueia; usado para treino | Onboarding, experimentação |
| **EMERGENCY** | Apenas checkpoints 2,7 (evidência + calibração) | Incidentes P0, tempo crítico |

---

## 📝 Exemplo de Uso Prático

```python
# Antes de deploy crítico
result = self_check_full(
    action="Deploy pagamento v2 para produção",
    context={"env": "prod", "service": "payments", "version": "2.1.0"},
    framework_used="pre_mortem",
    evidence=Evidence(
        source="measurement",
        quality="strong",
        description="Canary 5% por 2h: 0 erros, latência P99 45ms (< 100ms baseline)",
        url="https://grafana.example.com/d/payments-canary"
    ),
    confidence=0.85,
    inversion=InversionResult(
        failure_modes=[
            FailureMode("Rollback falha", 0.05, 0.9, "Monitorar health check"),
            FailureMode("Race condition pagamento duplicado", 0.02, 0.95, "Idempotency key check"),
            FailureMode("Cache inconsistency", 0.1, 0.7, "Cache invalidation verify")
        ],
        mitigations=["Rollback automatizado < 30s", "Idempotency keys obrigatórias", "Cache flush script pronto"],
        completed=True
    ),
    second_order=SecondOrderResult(
        consequences=[
            Consequence(2, "Clientes veem latência 0 durante cutover", 0.1, ["customers"]),
            Consequence(3, "Se rollback falha → incidente P0 prolongado", 0.01, ["engineering", "support"]),
        ],
        completed=True
    ),
    constraint=ConstraintResult(
        constraint_name="Database connection pool",
        bottleneck_location="PgBouncer max_client_conn=100",
        elevation_plan="Aumentar para 200 + monitorar PgBouncer stats",
        completed=True
    ),
    pre_mortem=PreMortemResult(
        risks=[
            Risk("Bug em idempotency key", 0.1, 0.9, "Teste de carga com chaves duplicadas", "Rollback imediato"),
            Risk("Cache stale causa overcharge", 0.05, 0.95, "Cache flush pré-deploy + TTL 60s", "Manual refund process"),
            Risk("Monitoring blind spot", 0.15, 0.6, "Adicionar alerts customizados pré-deploy", "Manual verification 30min")
        ],
        completed=True
    ),
    confidence_calibration=0.8  # ≤ evidence_quality (strong=0.9) ✅
)

# Resultado:
# check.passed = True
# check.can_proceed = True
```

---

## 📊 Métricas de Conformidade (Dashboard)

| Métrica | Atual | Target | Tendência |
|---------|-------|--------|-----------|
| Checkpoint Compliance | 94% | 100% | ↗ |
| Override Rate | 2% | 0% | ↗ |
| False Block Rate | 3% | < 5% | → |
| Avg Checkpoint Latency | 180ms | < 200ms | → |
| Override Justification Quality | 100% | 100% | → |

---

## 🔧 Integração com Outras Skills

| Skill | Integração |
|-------|------------|
| **Thinking Frameworks** | Checkpoint 1 força declaração de framework; 3 força inversão; 4 força 2ª ordem |
| **Metacognition** | Loga checkpoints passados/fallhados; detecta padrões de skip |
| **Task Decomposition** | Checkpoints integrados em cada subtask do TaskPlan |
| **Task Pilot** | Checkpoints viram context anchors no Task Pilot |
| **Capability Evolver** | Patterns de checkpoint skip → auto-rules para forçar |
| **Systematic Debugging** | Checkpoints em cada fase (entender → rastrear → identificar → corrigir) |

---

## 📝 Exemplo de Falha de Checkpoint (Bloqueio Real)

```python
# Tentativa de deploy sem pre-mortem
result = self_check_full(
    action="Deploy hotfix sem pre-mortem",
    context={"urgency": "high"},
    framework_used="pre_mortem",
    evidence=Evidence(source="expert", quality="anecdotal", description="Dev disse que tá ok"),
    confidence=0.9,
    inversion=InversionResult(failure_modes=[], mitigations=[], completed=False),  # ❌
    second_order=SecondOrderResult(consequences=[], completed=False),  # ❌
    constraint=ConstraintResult(constraint_name="", bottleneck_location="", elevation_plan="", completed=False),  # ❌
    pre_mortem=PreMortemResult(risks=[], completed=False),  # ❌
    confidence_calibration=0.9
)

# RESULTADO:
# check.passed = False
# check.failed_checkpoints = [3, 4, 5, 6]
# check.blockers = [
#   "Inversion não realizada: 3 modos de falha + mitigação obrigatórios",
#   "Second-order thinking não feito: consequências 2ª/3ª ordem obrigatórias",
#   "Constraint não identificado: gargalo + plano elevação obrigatórios",
#   "Pre-mortem não feito: 3 riscos + probabilidade + mitigação obrigatórios"
# ]
# check.required_actions = [
#   "Execute inversão: liste 3 modos de falha + mitigação",
#   "Execute 2ª ordem: mapeie consequências 2 níveis",
#   "Identifique constraint: nomeie gargalo + plano elevação",
#   "Execute pre-mortem: 3 riscos + prob + impacto + mitigação"
# ]
# check.can_proceed = False  ← BLOQUEADO
```

---

## 📜 Licença

MIT — Parte do projeto Damon Evolution (github.com/eapeli/damon)