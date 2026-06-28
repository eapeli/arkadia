---
name: metacognition
description: "Motor de auto-reflexão e metacognição para agentes IA. Extrai padrões de transcripts de sessão em grafo ponderado com aprendizado Hebbiano e decaimento temporal. Permite auto-monitoramento de raciocínio, detecção de vieses cíclicos, calibração de confiança e ajuste de estratégias."
version: "1.0.0"
category: reasoning
tags: [metacognition, self-reflection, hebbian-learning, bias-detection, confidence-calibration, cognitive-monitoring]
author: damon-evolution
---

# 🧠 Metacognition — Motor de Auto-Reflexão e Metacognição

> **Objetivo**: Dar ao agente a capacidade de **pensar sobre seu próprio pensamento** — monitorar qualidade do raciocínio, detectar padrões de erro, calibrar confiança, e ajustar estratégias em tempo real.

---

## 🎯 Capacidades Principais

| Capacidade | Descrição |
|------------|-----------|
| **Self-Monitoring** | Rastreia qual framework está sendo usado, se está funcionando, quando trocar |
| **Bias Detection** | Identifica viés de confirmação, ancoragem, disponibilidade, superconfiança |
| **Confidence Calibration** | Compara confiança declarada vs. taxa de acerto real; ajusta dinamicamente |
| **Error Pattern Mining** | Extrai padrões recorrentes de falha de transcripts → grafo de 지식 |
| **Strategy Adjustment** | Muda abordagem quando detecta estagnação, loop, ou degradação de qualidade |
| **Hebbian Memory Graph** | Grafo ponderado: conceitos → conexões fortalecidas por co-ocorrência + decaimento temporal |

---

## 🧱 Arquitetura: Grafo Hebbiano com Decaimento Temporal

```
Conceito A ───(peso: 0.87, última_atualização: t-2h)─── Conceito B
    │                                                        │
    │                    (co-ocorrência                     │
    ▼                     reforça conexão)                  ▼
Conceito C ───(peso: 0.34, última_atualização: t-5d)─── Conceito D
```

- **Regra de Hebb**: "Neurônios que disparam juntos, se conectam" → co-ocorrência em contexto de raciocínio bem-sucedido fortalece aresta
- **Decaimento Temporal**: `peso = peso * e^(-λ * Δt)` — conexões não usadas enfraquecem
- **Podcast**: Remove arestas com peso < threshold (limpeza periódica)
- **Persistência**: Serializado em JSONL append-only para sobrevivência cross-sessão

---

## 🔄 Loop de Metacognição (Execução Contínua)

```
┌─────────────────────────────────────────────────────────────┐
│                    METACOGNITION LOOP                       │
├─────────────────────────────────────────────────────────────┤
│  1. OBSERVE   │ Captura estado cognitivo atual:             │
│               │ - Framework ativo                            │
│               │ - Confiança declarada                        │
│               │ - Complexidade percebida                     │
│               │ - Tempo gasto                                │
├─────────────────────────────────────────────────────────────┤
│  2. REFLECT   │ Analisa qualidade:                          │
│               │ - O framework está adequado?                 │
│               │ - Evidência suporta conclusão?               │
│               │ - Viés detectado?                            │
│               │ - Loop/estagnação?                           │
├─────────────────────────────────────────────────────────────┤
│  3. ADJUST    │ Ação corretiva:                             │
│               │ - Trocar framework                           │
│               │ - Reduzir/calibrar confiança                 │
│               │ - Invocar Red Team / Inversão                │
│               │ - Solicitar evidência externa                │
├─────────────────────────────────────────────────────────────┤
│  4. LEARN     │ Atualiza grafo Hebbiano:                    │
│               │ - Sucesso → fortalece caminho usado          │
│               │ - Falha → enfraquece, cria caminho alternativo│
│               │ - Novo padrão → cria nós/arestas             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Ferramentas / Funções Exportadas

```python
# Inicialização (chamar uma vez por sessão)
metacognition_init(session_id: str) -> MetacognitionEngine

# Checkpoint a cada turno/etapa de raciocínio
metacognition_checkpoint(
    engine: MetacognitionEngine,
    framework_used: str,
    confidence: float,           # 0.0 - 1.0
    reasoning_summary: str,      # Resumo do raciocínio deste passo
    outcome: str,                # "success" | "partial" | "failure" | "unknown"
    evidence_quality: str        # "strong" | "moderate" | "weak" | "anecdotal"
) -> MetacognitionReport

# Auto-monitor: chamado automaticamente pelo loop de conversa
metacognition_auto_monitor(
    engine: MetacognitionEngine,
    current_state: AgentState
) -> List[MetacognitionAction]

# Relatório de fim de sessão
metacognition_session_report(engine: MetacognitionEngine) -> SessionMetacognitionReport

# Persistência cross-sessão
metacognition_save(engine: MetacognitionEngine, path: Path) -> None
metacognition_load(path: Path) -> MetacognitionEngine
```

---

## 📊 Métricas de Metacognição (Dashboard)

| Métrica | Descrição | Target |
|---------|-----------|--------|
| **Framework Appropriateness Rate** | % de steps onde framework escolhido era adequado | > 80% |
| **Confidence Calibration Error** | Média \|confiança - acerto_real\| | < 0.15 |
| **Bias Detection Rate** | Vieses detectados / vieses reais (estimado) | > 70% |
| **Strategy Switch Frequency** | Troca de framework por sessão | 2-5 (nem rígido nem caótico) |
| **Hebbian Graph Density** | Conexões ativas / nós | 0.3-0.6 (small-world) |
| **Error Pattern Recurrence** | Mesmo erro repetido | 0 (dedup perfeito) |

---

## 🎯 Gatilhos de Ativação (Quando Invocar)

| Gatilho | Ação Metacognitiva |
|---------|-------------------|
| "Vamos aplicar First Principles aqui" | ✅ Checkpoint: framework=first_principles, confidence=0.8 |
| "Red Team isso" | ✅ Checkpoint: framework=red_team, confidence=0.7 |
| "Inversão: como isso falharia?" | ✅ Checkpoint: framework=inversion, confidence=0.8 |
| "Second-order thinking: e depois?" | ✅ Checkpoint: framework=second_order, confidence=0.75 |
| "Qual o constraint (TOC)?" | ✅ Checkpoint: framework=constraint_theory, confidence=0.8 |
| "Qual o incentivo real?" | ✅ Checkpoint: framework=incentive_mapping, confidence=0.7 |
| "Pre-mortem: imaginem que falhou" | ✅ Checkpoint: framework=pre_mortem, confidence=0.9 |
| **Loop detectado** (mesmo raciocínio 3+ vezes) | 🔄 AÇÃO: Forçar troca de framework |
| **Confiança > 0.9 mas evidence_quality = "weak"** | ⚠️ ALERTA: Superconfiança → calibrar para baixo |
| **Mesmo erro 2+ vezes na sessão** | 🔴 CRÍTICO: Extrair pattern, criar regra de prevenção |

---

## 🔧 Integração com Outras Skills

| Skill | Integração |
|-------|------------|
| **Thinking Frameworks** | Metacognição monitora qual framework está ativo e sua eficácia |
| **Systematic Debugging** | Checkpoints em cada fase (entender → rastrear → identificar → corrigir) |
| **Self-Check System v7** | Checkpoints forçados: "Apliquei framework X? Validei evidência?" |
| **Task Pilot / TaskOps** | Metacognição em cada subtask; rollback se quality < threshold |
| **Red Team** | Invocado automaticamente quando confiança alta mas evidência fraca |
| **Periodic Reflection** | Relatório de metacognição alimenta reflexão periódica |

---

## 📝 Exemplo de Uso Prático

```python
# No início da sessão
engine = metacognition_init(session_id="sess_abc123")

# A cada passo de raciocínio (ex: após usar tool)
report = metacognition_checkpoint(
    engine=engine,
    framework_used="first_principles",
    confidence=0.85,
    reasoning_summary="Quebrei o problema em verdades físicas: latência = distância/c. Descartei analogia com sistema anterior.",
    outcome="success",
    evidence_quality="strong"
)
# report.actions = []  (nada a fazer, continue)

# Se detectar problema:
report = metacognition_checkpoint(
    engine=engine,
    framework_used="analogy",
    confidence=0.9,
    reasoning_summary="Assumi que sistema X funciona como Y porque ambos usam Redis.",
    outcome="partial",
    evidence_quality="anecdotal"
)
# report.actions = [
#   MetacognitionAction(type="SWITCH_FRAMEWORK", to="first_principles"),
#   MetacognitionAction(type="CALIBRATE_CONFIDENCE", target=0.6),
#   MetacognitionAction(type="REQUEST_EVIDENCE", detail="Latência real medida vs assumida")
# ]

# Fim de sessão
session_report = metacognition_session_report(engine)
# session_report.patterns_found = ["Over-reliance on structural analogy when data available"]
# session_report.recommendations = ["Default to first_principles for latency problems"]
```

---

## 💾 Persistência Cross-Sessão

```
~/.damon/metacognition/
├── hebbian_graph.jsonl      # Grafo append-only (uma linha por atualização)
├── session_reports/         # Relatórios por sessão
│   ├── sess_abc123_report.json
│   └── ...
├── bias_signatures.json     # Padrões de viés conhecidos (compartilhado)
└── calibration_history.jsonl # Histórico de confiança vs acerto
```

---

## 📜 Licença

MIT — Parte do projeto Damon Evolution (github.com/eapeli/damon)