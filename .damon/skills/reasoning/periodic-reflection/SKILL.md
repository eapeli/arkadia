---
name: periodic-reflection
description: "Reflexão estruturada periódica (semanal/mensal) — consolida aprendizados, detecta padrões recorrentes, gera action items, atualiza skills e configurações. Alimentada pelo Capability Evolver e Metacognition."
version: "1.0.0"
category: reasoning
tags: [reflection, periodic, retrospective, learning, continuous-improvement, capability-evolver-integration]
author: damon-evolution
---

# 🪞 Periodic Reflection — Reflexão Estruturada Periódica

> **Objetivo**: Transformar experiência acumulada em **melhorias sistêmicas** — reflexão estruturada que consolida aprendizados, detecta padrões recorrentes, gera action items concretos, e atualiza skills/configs automaticamente.

---

## 🎯 Por Que Reflexão Periódica?

| Sem Reflexão | Com Reflexão Estruturada |
|--------------|--------------------------|
| Erros repetidos silenciosamente | Padrões detectados → action items |
| Skills/configs estagnam | Evolução contínua via Capability Evolver |
| Conhecimento perde-se entre sessões | Knowledge graph persistente cross-session |
| Melhorias reativas (após falha) | Melhorias proativas (padrões detectados cedo) |

---

## ⏰ Cadência e Escopo

| Cadência | Escopo | Duração | Output |
|----------|--------|---------|--------|
| **Diária** (EOD) | Sessão única | 5 min | Daily log + 1 action item |
| **Semanal** (Domingo) | Semana completa | 20 min | Weekly report + 3 action items |
| **Mensal** (1º dia) | Mês completo | 45 min | Monthly review + skill/config updates |
| **Trimestral** | Trimestre | 90 min | Strategic review + roadmap adjustment |

---

## 📋 Template de Reflexão (Estrutura Padronizada)

### Daily Reflection (5 min)
```markdown
## Daily Reflection - YYYY-MM-DD

### ✅ Completed Today
- [ ] Task 1: ...
- [ ] Task 2: ...

### 🔍 What Worked Well
- Framework X funcionou bem para problema Y
- Self-check v7 caught issue early

### ⚠️ What Didn't Work
- Task Z took 3x estimated effort
- Self-check v7 checkpoint 3 skipped (time pressure)

### 🎯 One Action Item for Tomorrow
- [ ] Add auto-rule: "se latência mencionada → force first_principles"

### 📊 Metrics
- Tasks completed: 5/7
- Self-check compliance: 94%
- Replans: 1
```

### Weekly Reflection (20 min)
```markdown
## Weekly Reflection - Week YYYY-WW

### 📈 Summary Metrics
- Sessions: 12
- Tasks completed: 47/52 (90%)
- Self-check compliance: 92%
- Avg checkpoint latency: 180ms
- Replans: 3
- Rollbacks: 0

### 🔍 Patterns Detected (via Capability Evolver)
1. **Over-reliance on analogy** for latency problems (78% partial outcomes)
   → Auto-rule created: "latência → first_principles"
2. **Self-check v7 checkpoint 3 (inversion) skipped** 4x under time pressure
   → Action: Add EMERGENCY mode documentation
3. **Task decomposition over-estimates effort** by 1.4x avg
   → Action: Calibrate estimation with historical data

### ✅ Top Wins
- Zero regressions this week
- First-principles auto-rule improved latency debug from 45min → 12min
- Self-check v7 prevented 3 bad deploys

### ⚠️ Areas for Improvement
- Task effort estimation accuracy: 65% (target 80%+)
- Checkpoint 3 (inversion) skip rate: 12%
- Metacognition graph density below target (0.28 vs 0.4)

### 🎯 3 Action Items for Next Week
1. [ ] Improve estimation calibration using historical data
2. [ ] Add "quick inversion" template for time-constrained scenarios
3. [ ] Increase metacognition graph density via more checkpoint logging

### 🔧 Skill/Config Updates Needed
- thinking-frameworks: add "quick inversion" variant
- task-decomposition: calibrate effort multipliers
- self-check-system-v7: document EMERGENCY mode
```

### Monthly Reflection (45 min)
```markdown
## Monthly Reflection - YYYY-MM

### 📊 Strategic Metrics (30-day rolling)
- Total sessions: 48
- Task completion rate: 91%
- Self-check compliance: 93% (↑ 2% MoM)
- Avg MTTR (debug): 47 min (↓ 23% MoM)
- Capability Evolver improvements: 12 deployed
- New skills created: 3
- Skills updated: 5

### 🧠 Cognitive Evolution (Metacognition + Capability Evolver)
**Top 5 Learnings This Month:**
1. First-principles + red team combo = 3x faster root cause for perf bugs
2. Task decomposition templates reduce planning time 60%
3. Self-check v7 EMERGENCY mode essential for P0 incidents
4. Metacognition graph density correlates with fix quality (r=0.73)
5. Capability Evolver auto-rules now handle 40% of routine decisions

**Skill Evolution:**
- thinking-frameworks v1.2: + quick inversion, quick red team
- task-decomposition v1.1: calibrated effort multipliers
- self-check-system-v7 v1.1: EMERGENCY mode documented
- metacognition v1.1: added bias signature library

### 🚀 Strategic Initiatives (Next Quarter)
1. **Autonomous Debugging Pipeline** — Capability Evolver generates debug templates from patterns
2. **Predictive Self-Check** — Metacognition predicts which checkpoints will be skipped
3. **Cross-Session Knowledge Graph** — Metacognition graph shared across all agents
4. **Skill Marketplace** — Capability Evolver publishes proven skills to registry

### 🎯 5 Strategic Action Items
1. [ ] Build Autonomous Debugging Pipeline (Capability Evolver + Task Pilot)
2. [ ] Implement Predictive Self-Check (Metacognition + ML)
3. [ ] Deploy Cross-Session Knowledge Graph (Shared Metacognition)
4. [ ] Publish top 10 skills to registry (Capability Evolver)
5. [ ] Benchmark against baseline: target 50% MTTR reduction
```

---

## 🤖 Automação via Capability Evolver + Metacognition

```python
class ReflectionEngine:
    def __init__(self, metacognition: MetacognitionEngine, evolver: CapabilityEvolver):
        self.metacognition = metacognition
        self.evolver = evolver
    
    def generate_daily_reflection(self, session_id: str) -> DailyReflection:
        # Pull metrics from metacognition + evolver
        metrics = self.metacognition.get_session_metrics(session_id)
        patterns = self.evolver.get_recent_patterns(days=1)
        
        return DailyReflection(
            completed=self._get_completed_tasks(session_id),
            what_worked=self._extract_wins(metrics, patterns),
            what_failed=self._extract_failures(metrics, patterns),
            action_item=self._generate_action_item(patterns),
            metrics=metrics
        )
    
    def generate_weekly_reflection(self, week_start: date) -> WeeklyReflection:
        # Aggregate daily reflections + evolver patterns
        weekly_patterns = self.evolver.detect_weekly_patterns(week_start)
        metacognition_report = self.metacognition.get_weekly_report(week_start)
        
        return WeeklyReflection(
            metrics=self._aggregate_metrics(week_start),
            patterns=weekly_patterns,
            wins=self._extract_wins(weekly_patterns),
            improvements=self._generate_improvements(weekly_patterns),
            action_items=self._generate_action_items(weekly_patterns),
            skill_updates=self._propose_skill_updates(weekly_patterns)
        )
    
    def generate_monthly_reflection(self, month_start: date) -> MonthlyReflection:
        # Full strategic review
        monthly_patterns = self.evolver.detect_monthly_patterns(month_start)
        evolution_report = self.evolver.generate_evolution_report(timedelta(days=30))
        metacognition_report = self.metacognition.get_monthly_report(month_start)
        
        return MonthlyReflection(
            strategic_metrics=self._compute_strategic_metrics(month_start),
            cognitive_evolution=self._analyze_cognitive_evolution(monthly_patterns),
            skill_evolution=self._track_skill_evolution(month_start),
            strategic_initiatives=self._propose_strategic_initiatives(monthly_patterns),
            action_items=self._generate_strategic_actions(monthly_patterns)
        )
    
    def auto_apply_improvements(self, reflection: Reflection) -> List[AppliedImprovement]:
        """Auto-aplica melhorias de baixo risco (prompt patches, config diffs)."""
        improvements = []
        
        for action in reflection.action_items:
            if action.risk_score <= 2:  # Auto-apply threshold
                result = self._apply_improvement(action)
                improvements.append(result)
        
        return improvements
```

---

## 📁 Armazenamento de Reflexões

```
~/.damon/reflections/
├── daily/
│   ├── 2025-01-15_reflection.md
│   └── ...
├── weekly/
│   ├── 2025-W03_reflection.md
│   └── ...
├── monthly/
│   ├── 2025-01_reflection.md
│   └── ...
├── quarterly/
│   └── 2025-Q1_reflection.md
└── index.json          # Index para busca rápida
```

---

## 🔧 Integração com Outras Skills

| Skill | Integração |
|-------|------------|
| **Capability Evolver** | Fornece patterns detectados; recebe action items → improvements |
| **Metacognition** | Fornece cognitive metrics; recebe reflection insights → graph updates |
| **Task Pilot** | Execution patterns alimentam reflection; reflection gera pilot improvements |
| **Self-Check v7** | Compliance metrics alimentam reflection; reflection gera self-check improvements |
| **Task Pilot** | Execution patterns → reflection; reflection → pilot templates |
| **Systematic Debugging** | Bug patterns → reflection; reflection → debug templates |

---

## 📁 Output: Reflexão Como Skill Updatável

```yaml
# Cada reflexão pode gerar skill updates automáticos
skill_updates:
  - skill: "thinking-frameworks"
    version: "1.3"
    changes:
      - add: "quick inversion variant for time-constrained scenarios"
      - modify: "red team template → add timeboxed variant"
    risk_score: 1
    auto_apply: true
  
  - skill: "task-decomposition"
    version: "1.2"
    changes:
      - modify: "effort multipliers calibrated to historical 1.4x overestimate"
    risk_score: 1
    auto_apply: true
  
  - skill: "self-check-system-v7"
    version: "1.2"
    changes:
      - add: "EMERGENCY mode documentation + quick inversion template"
    risk_score: 1
    auto_apply: true
```

---

## 📜 Licença

MIT — Parte do projeto Damon Evolution (github.com/eapeli/damon)