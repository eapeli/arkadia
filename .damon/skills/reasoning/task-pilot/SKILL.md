---
name: task-pilot
description: "Framework de execução de tarefas com context anchors, verification loops e context anchors que sobrevivem à compactação. Converte TaskPlans em execução guiada com verification checkpoints, context preservation across compaction, e adaptive replanning."
version: "1.0.0"
category: reasoning
tags: [task-pilot, execution-framework, context-anchors, verification-loops, compaction-survival, adaptive-replanning]
author: damon-evolution
---

# 🛩️ Task Pilot — Framework de Execução Guiada

> **Objetivo**: Converter TaskPlans em **execução guiada, verificável e resiliente** — com context anchors que sobrevivem à compactação, verification loops em cada etapa, e adaptive replanning quando a realidade diverge do plano.

---

## 🎯 Problema que Resolve

| Problema Comum | Solução Task Pilot |
|----------------|-------------------|
| Plano perde contexto após compactação | **Context Anchors** sobrevivem à compactação |
| Execução desvia do plano sem detecção | **Verification Loops** a cada etapa |
| Plano rígido não adapta a surpresas | **Adaptive Replanning** automático |
| Falha silenciosa em subtask crítica | **Verification Gates** obrigatórios |
| Contexto perdido entre sessões | **State Persistence** cross-session |

---

## 🏗️ Arquitetura: 3 Pilares

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TASK PILOT ARCHITECTURE                             │
├─────────────────────┬─────────────────────┬─────────────────────────────────┤
│   CONTEXT ANCHORS   │  VERIFICATION LOOPS │     ADAPTIVE REPLANNING         │
├─────────────────────┼─────────────────────┼─────────────────────────────────┤
│ • Immutable IDs     │ • Pre-execution     │ • Drift Detection               │
│ • Semantic Tags     │   Gate Check        │   (plan vs reality)             │
│ • Cross-compaction  │ • Post-execution    │ • Auto-replan Trigger           │
│   Survival          │   Verification      │   • Minimal Diff Replan         │
│ • Queryable Index   │ • Metacognition     │ • Stakeholder Notification      │
│                     │   Integration       │ • Rollback to Anchor            │
└─────────────────────┴─────────────────────┴─────────────────────────────────┘
```

---

## 🏷️ Context Anchors (Âncoras de Contexto)

**Problema**: Compactação remove mensagens antigas → perde contexto do plano.

**Solução**: Anchors imutáveis, versionados, sobrevivem à compactação.

```python
@dataclass
class ContextAnchor:
    id: str                           # UUID v4 (imutável)
    anchor_type: Literal[             # Tipo semântico
        "goal",                       # Objetivo alto nível
        "plan",                       # TaskPlan completo (serializado)
        "task",                       # SubTask específica
        "decision",                   # Decisão crítica + rationale
        "constraint",                 # Constraint identificado
        "assumption",                 # Premissa explícita
        "risk",                       # Risco identificado
        "learning",                   # Lição aprendida
        "context_snapshot"            # Estado do sistema (config, env, data)
    ]
    content: str                      # Conteúdo serializado (JSON/YAML/text)
    semantic_tags: List[str]          # ["migration", "redis", "p0", "auth"]
    version: int                      # Versão do anchor (incrementa em updates)
    created_at: datetime
    updated_at: datetime
    related_anchors: List[str]        # IDs de anchors relacionados
    survives_compaction: bool = True  # Sempre True para anchors
    compact_priority: int = 10        # Prioridade na compactação (10 = nunca remove)
    
    # Métodos
    def to_compact_format(self) -> str:     # Formato compacto para injeção
    def queryable_text(self) -> str:        # Texto para busca semântica
    def diff(self, other: 'ContextAnchor') -> AnchorDiff:
```

**Injeção no System Prompt (sobrevive à compactação)**:
```
[CONTEXT ANCHORS - NEVER REMOVE]
ANCHOR:goal:v3:migracao-monolito-microservicos
  Objetivo: Migrar monólito Django para microserviços (auth, payments, notifications)
  Success: 3 serviços independentes, < 5min downtime, PCI-DSS compliant
  Timeline: 12 semanas, 4 devs
  
ANCHOR:constraint:v2:downtime
  Constraint: Max 5 minutos downtime total
  Tipo: Hard constraint (business critical)
  Mitigação: Blue-green deploy + canary 5% + rollback < 30s
  
ANCHOR:decision:v1:auth-first
  Decisão: Migrar auth service primeiro
  Rationale: Menor surface area, maior ROI, team tem expertise
  Alternativas consideradas: payments first (rejeitado: compliance risk)
  
ANCHOR:learning:v1:redis-migration
  Aprendizado: Redis migration precisa dual-write phase
  Evidência: Tentativa direta causou 2h downtime (incident #447)
[/CONTEXT ANCHORS]
```

---

## 🔄 Verification Loops (Loops de Verificação)

**Princípio**: Verificar **antes**, **durante** e **depois** de cada etapa crítica.

```python
@dataclass
class VerificationGate:
    gate_id: str
    gate_type: Literal[
        "pre_execution",      # Antes de executar task
        "mid_execution",      # Durante execução longa
        "post_execution",     # Após completar task
        "checkpoint",         # Checkpoint de plano
        "plan_validation"     # Validação de plano inteiro
    ]
    task_id: str
    checks: List[VerificationCheck]
    required: bool = True            # Se False: warning only
    timeout_seconds: int = 300
    
@dataclass
class VerificationCheck:
    check_id: str
    name: str
    check_type: Literal[
        "acceptance_criteria",   # Critério de aceite da task
        "invariant",             # Invariante do sistema
        "metric_threshold",      # Métrica < threshold
        "health_check",          # Health check serviço
        "invariant_cross_task",  # Invariante cross-task
        "self_check"             # Self-check v7 gate
    ]
    query: str                     # Query/prompt para verificação
    expected: Any                  # Resultado esperado
    tolerance: Any = None          # Tolerância (para métricas)
    on_fail: Literal["block", "warn", "replan", "rollback"] = "block"
```

**Loop de Verificação Padrão**:
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VERIFICATION LOOP PER TASK                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PRE-EXECUTION GATE                                                         │
│  ├─ Self-Check v7 Gate (framework, evidence, inversion, 2nd order)         │
│  ├─ Acceptance Criteria Review (são claros? testáveis?)                    │
│  ├─ Dependency Check (deps completas? outputs disponíveis?)                │
│  ├─ Resource Check (skills, tools, credentials, quotas)                    │
│  └─ Risk Check (risks identificados? mitigations ativas?)                  │
│         │                                                                   │
│         ▼                                                                   │
│  EXECUTION (com monitoring contínuo)                                        │
│  ├─ Mid-Execution Gate (se task > 10min)                                   │
│  │   ├─ Progress Check (no trajectory?)                                    │
│  │   ├─ Resource Monitor (CPU, mem, quota OK?)                             │
│  │   └─ Anomaly Detection (drift inesperado?)                              │
│  │                                                                          │
│         ▼                                                                   │
│  POST-EXECUTION GATE                                                        │
│  ├─ Acceptance Criteria Verification (pass/fail cada critério)             │
│  ├─ Output Validation (schema, tipos, ranges)                              │
│  ├─ Invariant Check (invariantes do sistema mantidas?)                     │
│  ├─ Metric Thresholds (latência, erro, throughput OK?)                     │
│  ├─ Health Checks (serviços dependentes saudáveis?)                        │
│  ├─ Self-Check v7 Quick (evidence quality + confidence calibration)        │
│  ├─ Cross-Task Invariant (invariantes cross-task OK?)                      │
│  └─ Anchor Update (atualiza anchors com resultado)                         │
│         │                                                                   │
│         ▼                                                                   │
│  CHECKPOINT GATE (se task.checkpoint = True)                               │
│  ├─ State Persistence (salva estado em checkpoint store)                   │
│  ├─ Anchor Snapshot (salva anchors atuais)                                 │
│  ├─ Rollback Point Creation (cria rollback point)                          │
│  └─ Plan Validation (plano ainda válido? drift detection)                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Adaptive Replanning (Replanejamento Adaptativo)

**Trigger**: Drift detectado entre plano e realidade.

```python
@dataclass
class DriftSignal:
    signal_type: Literal[
        "task_failed",              # Task falhou
        "task_exceeded_effort",     # Esforço > estimated * 2
        "task_exceeded_time",       # Tempo > estimated * 2
        "output_invalid",           # Output não passa acceptance
        "invariant_violated",       # Invariant violado
        "new_constraint",           # Novo constraint descoberto
        "new_risk",                 # Novo risco identificado
        "dependency_changed",       # Dependency output mudou
        "external_change",          # Mudança externa (API, infra)
        "stakeholder_change"        # Requisito mudou
    ]
    task_id: str
    severity: Literal["low", "medium", "high", "critical"]
    description: str
    evidence: Evidence
    detected_at: datetime

@dataclass
class ReplanAction:
    action_type: Literal[
        "replan_subtree",           # Replaneja subárvore a partir de task
        "insert_task",              # Insere nova task
        "remove_task",              # Remove task obsoleta
        "modify_task",              # Modifica task existente
        "reorder_tasks",            # Reordena para paralelismo
        "add_checkpoint",           # Adiciona checkpoint
        "add_rollback",             # Adiciona rollback point
        "full_replan"               # Replaneja do zero
    ]
    affected_task_ids: List[str]
    rationale: str
    new_tasks: List[SubTask] = []
    modified_tasks: Dict[str, SubTask] = {}

class AdaptiveReplanner:
    def detect_drift(self, plan: TaskPlan, execution_state: ExecutionState) -> List[DriftSignal]
    
    def generate_replan(self, 
                        plan: TaskPlan, 
                        drift_signals: List[DriftSignal],
                        execution_state: ExecutionState) -> ReplanProposal
    
    def apply_replan(self, 
                     plan: TaskPlan, 
                     proposal: ReplanProposal,
                     execution_state: ExecutionState) -> TaskPlan
    
    def notify_stakeholders(self, proposal: ReplanProposal) -> None
```

**Algoritmo de Replan Mínimo (Minimal Diff)**:
```
1. Identificar subtree afetada (task falha + dependentes downstream)
2. Preservar tasks concluídas (checkpoints válidos)
3. Replanejar apenas subtree afetada + dependentes diretos
3. Preservar paralelos não-afetados
4. Validar novo plano (DAG, checkpoints, effort budget)
4. Notificar stakeholders com diff visual
```

---

## 🛡️ Execution Engine (Motor de Execução)

```python
class TaskPilotEngine:
    def __init__(
        self,
        plan: TaskPlan,
        checkpoint_store: CheckpointStore,
        anchor_store: AnchorStore,
        verification_gates: List[VerificationGate],
        self_check: SelfCheckV7,
        replanner: AdaptiveReplanner,
        max_parallelism: int = 4,
        checkpoint_interval: int = 1,  # checkpoints por N tasks
        auto_replan: bool = True
    ):
    
    async def execute(self) -> ExecutionResult:
        """Executa plano completo com verification loops e adaptive replanning."""
    
    async def execute_task(self, task: SubTask) -> TaskResult:
        """Executa single task com full verification loop."""
    
    async def run_verification_gate(self, gate: VerificationGate, task: SubTask, state: ExecutionState) -> GateResult
    
    def detect_and_replan(self, state: ExecutionState) -> bool:
        """Detecta drift e replaneja se necessário. Returns True se replanned."""
    
    def get_current_anchors(self) -> List[ContextAnchor]
    
    def get_execution_state(self) -> ExecutionState
    
    def pause(self) -> None
    def resume(self) -> None
    def abort(self, reason: str) -> None
```

---

## 💾 State Persistence (Cross-Session)

```
~/.damon/task_pilot/
├── plans/
│   ├── plan_uuid_v1.json           # TaskPlan v1
│   ├── plan_uuid_v2.json           # TaskPlan v2 (após replan)
│   └── ...
├── anchors/
│   ├── anchor_goal_v3.json
│   ├── anchor_constraint_v2.json
│   └── ...
├── checkpoints/
│   ├── checkpoint_1_state.json
│   ├── checkpoint_2_state.json
│   └── ...
├── execution_log.jsonl             # Log estruturado de execução
├── drift_signals.jsonl             # Sinais de drift detectados
├── replan_history.jsonl            # Histórico de replans
└── verification_log.jsonl          # Log de verification gates
```

---

## 🛠️ API / Funções Exportadas

```python
# Criar pilot a partir de TaskPlan
pilot = TaskPilot.from_plan(
    plan: TaskPlan,
    checkpoint_store: CheckpointStore,
    anchor_store: AnchorStore,
    max_parallelism: int = 4
)

# Ou criar do zero com goal
pilot = TaskPilot.from_goal(
    goal: str,
    context: Dict[str, Any],
    templates: List[str] = [],
    max_parallelism: int = 4
)

# Executar (async, long-running)
result = await pilot.execute()

# Ou step-by-step para controle manual
while not pilot.is_complete():
    task = pilot.get_next_task()
    if task:
        result = await pilot.execute_next_task()
        # Verifica replan automático
        if pilot.was_replanned():
            print(f"Replanned: {pilot.get_last_replan_summary()}")

# Pausar/Retomar (cross-session)
pilot.pause()
pilot.save_state()
# ... later ...
pilot = TaskPilot.load_state(state_path)
pilot.resume()

# Anchors
anchors = pilot.get_all_anchors()
goal_anchor = pilot.get_anchor("goal")
pilot.add_anchor(ContextAnchor(...))

# Verification
gates = pilot.get_verification_gates()
pilot.add_verification_gate(VerificationGate(...))

# Monitoring
state = pilot.get_execution_state()
# state = {
#   "completed_tasks": 12,
#   "failed_tasks": 0,
#   "current_parallel_group": "impl",
#   "effort_spent": 45.5,
#   "effort_remaining": 120.3,
#   "drift_signals": [],
#   "replans": 0
# }

# Visualização
print(pilot.render_mermaid())
print(pilot.render_progress_bar())
```

---

## 📊 Visualização de Progresso (Mermaid)

```mermaid
graph TD
    A[Design + ADR ✅] --> B[Backend API 🔄]
    A --> C[Frontend UI ⏳]
    B --> D[Testes Integração ⏳]
    C --> D
    D --> E[Deploy Staging ⏳]
    E --> F[Smoke Tests ⏳]
    F --> G[Deploy Prod ⏳]
    
    style A fill:#e8f5e9,stroke:#4caf50   ✅ Completed
    style B fill:#fff3e0,stroke:#ff9800   🔄 In Progress
    style C fill:#f3e5f5,stroke:#9c27b0   ⏳ Pending
    style D fill:#f3e5f5,stroke:#9c27b0
    style E fill:#f3e5f5,stroke:#9c27b0
    style F fill:#f3e5f5,stroke:#9c27b0
    style G fill:#f3e5f5,stroke:#9c27b0
    
    classDef completed fill:#e8f5e9,stroke:#4caf50
    classDef inprogress fill:#fff3e0,stroke:#ff9800
    classDef pending fill:#f3e5f5,stroke:#9c27b0
    classDef checkpoint fill:#fff3e0,stroke:#ff9800,stroke-dasharray: 5 5
    
    class A completed
    class B inprogress
    class C,D,E,F,G pending
    
    %% Anchors
    anchor1[📌 Anchor: Goal] -.-> A
    anchor2[📌 Constraint: downtime < 5min] -.-> G
    anchor3[📌 Decision: Auth first] -.-> B
```

---

## 📊 Métricas de Execução (Dashboard)

| Métrica | Descrição | Target |
|---------|-----------|--------|
| **Plan Adherence** | % tasks executadas conforme plano original | > 80% |
| **Verification Pass Rate** | % verification gates passed / total | > 95% |
| **Replan Frequency** | Replans / 100 tasks | < 10 |
| **Drift Detection Latency** | Tempo média detecção → alerta | < 30s |
| **Replan Latency** | Drift detectado → novo plano ativo | < 60s |
| **Rollback Success Rate** | Rollbacks bem-sucedidos / tentativas | 100% |
| **Anchor Survival Rate** | Anchors sobrevivem à compactação | 100% |
| **Verification Gate Pass Rate** | Gates passed / total gates | > 95% |

---

## 🔧 Integração com Outras Skills

| Skill | Integração |
|-------|------------|
| **Task Decomposition** | TaskPlan → TaskPilot input; decomposition templates viram pilot templates |
| **Thinking Frameworks** | Frameworks guiam decomposition; verification usa frameworks como critérios |
| **Metacognition** | Monitora qualidade de execução; detecta drift cognitivo |
| **Self-Check v7** | Verification gates incluem Self-Check v7 gates |
| **Task Decomposition** | TaskPlan input; templates compartilhados |
| **Capability Evolver** | Execution patterns → template improvements; drift patterns → auto-rules |
| **Metacognition** | Context anchors alimentam metacognition graph |
| **Systematic Debugging** | Failed tasks viram incident templates → decomposition |

---

## 📝 Exemplo de Uso Prático

```python
# Criar pilot a partir de goal complexo
pilot = TaskPilot.from_goal(
    goal="Migrar monólito Django para microserviços (auth, payments, notifications)",
    context={
        "current_stack": "Django, PostgreSQL, Redis, Celery",
        "team": 4,
        "timeline_weeks": 12
    },
    templates=["microservice_migration", "database_decomposition"],
    max_parallelism=3
)

# Adicionar anchors críticos
pilot.add_anchor(ContextAnchor(
    anchor_type="constraint",
    content="Max downtime: 5 minutos total. Hard constraint.",
    semantic_tags=["downtime", "hard-constraint", "p0"],
    survives_compaction=True
))

# Executar com monitoring
async def run_with_monitoring():
    async for event in pilot.execute_streaming():
        if event.type == "task_started":
            print(f"🔄 {event.task.name} started")
        elif event.type == "task_completed":
            print(f"✅ {event.task.name} completed in {event.duration:.1f}s")
        elif event.type == "verification_gate_passed":
            print(f"✅ Gate {event.gate.gate_type} passed")
        elif event.type == "verification_gate_failed":
            print(f"❌ Gate {event.gate.gate_type} FAILED: {event.message}")
        elif event.type == "drift_detected":
            print(f"🚨 DRIFT: {event.signal.description}")
        elif event.type == "replanned":
            print(f"🔄 REPLANNED: {event.summary}")
            print(f"   Diff: {event.diff}")

# Executa
result = await pilot.execute()

# Resultado final
print(f"""
Execution Complete:
- Tasks completed: {result.completed_tasks}/{result.total_tasks}
- Failed: {result.failed_tasks}
- Replans: {result.replans}
- Total effort: {result.total_effort:.1f}h (estimated: {result.estimated_effort:.1f}h)
- Rollbacks: {result.rollbacks}
- Context anchors preserved: {result.anchors_preserved}
""")
```

---

## 📁 Templates de Pilot (Built-in)

```
pilot_templates/
├── microservice_migration.yaml
├── database_decomposition.yaml
├── api_development.yaml
├── infrastructure_provisioning.yaml
├── incident_response.yaml
├── security_audit.yaml
├── performance_optimization.yaml
├── data_migration.yaml
├── refactoring_migration.yaml
└── custom/
```

---

## 📜 Licença

MIT — Parte do projeto Damon Evolution (github.com/eapeli/damon)