---
name: bayesian-thinking
description: "Pensamento probabilístico bayesiano — trata crenças como probabilidades (0-100%), atualiza com nova evidência via teorema de Bayes. Calibração dinâmica de confiança, odds ratios, likelihood ratios. Integração nativa com Self-Check v7 (checkpoint 7: confidence calibration)."
version: "1.0.0"
category: reasoning
tags: [bayesian, probabilistic-reasoning, confidence-calibration, evidence-evaluation, decision-making, self-check-integration]
author: damon-evolution
---

# 📐 Bayesian Thinking — Pensamento Probabilístico Bayesiano

> **Objetivo**: Substituir certeza binária (sim/não) por **raciocínio probabilístico calibrado** — tratar crenças como probabilidades (0-100%), atualizar com nova evidência via Bayes, calibrar confiança com qualidade da evidência. Integração nativa com Self-Check v7 (Checkpoint 7).

---

## 🎯 Princípio Fundamental

> **Certeza binária é viés. Probabilidade calibrada é sabedoria.**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BAYESIAN THINKING CORE                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   PRIOR (crença anterior) × LIKELIHOOD (evidência)                         │
│            │                    │                                           │
│            ▼                    ▼                                           │
│    ┌─────────────────────────────────────┐                                 │
│    │     POSTERIOR = PRIOR × LIKELIHOOD  │                                 │
│    │            / EVIDENCE                │                                 │
│    └─────────────────────────────────────┘                                 │
│            │                                                               │
│            ▼                                                               │
│   NOVA CRENÇA CALIBRADA (0-100%)                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🧮 Teorema de Bayes (Forma Prática)

### Forma de Odds (Mais Intuitiva)
```
Posterior Odds = Prior Odds × Likelihood Ratio

Onde:
- Prior Odds = P(H) / P(¬H) = p / (1-p)
- Likelihood Ratio = P(E|H) / P(E|¬H)
- Posterior Odds = P(H|E) / P(¬H|E)
- Posterior Probability = Posterior Odds / (1 + Posterior Odds)
```

### Exemplo Prático
```
Cenário: "O deploy vai falhar?"
- Prior: 20% chance de falha (baseado em histórico: 1/5 deploys falham)
  → Prior Odds = 0.2 / 0.8 = 0.25

- Evidência: "Canary 5% por 2h: 0 erros, latência normal"
  - P(E|sucesso) = 0.95 (se vai sucesso, 95% chance de canary limpo)
  - P(E|falha) = 0.10 (se vai falhar, só 10% chance de canary limpo)
  - Likelihood Ratio = 0.95 / 0.10 = 9.5

- Posterior Odds = 0.25 × 9.5 = 2.375
- Posterior Probability = 2.375 / (1 + 2.375) = 70.4%

Resultado: Probabilidade de falha cai de 20% → 5.6% (sucesso 94.4%)
```

---

## 🎯 Calibração de Confiança (Self-Check v7 Integration)

### Tabela de Qualidade de Evidência → Confiança Máxima

| Evidence Quality | Likelihood Ratio Range | Max Confidence | Self-Check v7 Gate |
|------------------|------------------------|----------------|-------------------|
| **Strong** (measurement, controlled experiment) | LR ≥ 10 | 90% | ✅ ≥ 0.9 |
| **Moderate** (reliable source, correlation) | LR 3-10 | 70% | ✅ ≥ 0.7 |
| **Weak** (expert opinion, correlation only) | LR 1.5-3 | 50% | ⚠️ ≥ 0.5 |
| **Anecdotal** (hearsay, single case) | LR 1-1.5 | 30% | ❌ > 0.3 blocks |

### Regra de Ouro (Self-Check v7 Checkpoint 7)
> **Confiança declarada ≤ Confiança máxima baseada na evidência**

```
Se evidence_quality = "moderate" → max_confidence = 0.7
Se confidence_declared = 0.85 → BLOCKED
Ação obrigatória: Reduzir confidence para 0.7 ou melhorar evidence
```

---

## 🔄 Atualização Sequencial (Multiple Evidence)

```python
class BayesianUpdater:
    def __init__(self, prior: float):
        self.posterior = prior
        self.evidence_log = []
    
    def update(self, evidence: Evidence, likelihood_ratio: float = None) -> float:
        """Atualiza posterior com nova evidência."""
        
        # Calcula LR se não fornecido
        if likelihood_ratio is None:
            likelihood_ratio = self._estimate_lr(evidence)
        
        # Bayes em odds
        prior_odds = self.posterior / (1 - self.posterior)
        posterior_odds = prior_odds * likelihood_ratio
        self.posterior = posterior_odds / (1 + posterior_odds)
        
        # Log
        self.evidence_log.append({
            "evidence": evidence,
            "likelihood_ratio": likelihood_ratio,
            "prior": self._prev_posterior,
            "posterior": self.posterior,
            "timestamp": datetime.now()
        })
        
        return self.posterior
    
    def _estimate_lr(self, evidence: Evidence) -> float:
        """Estima Likelihood Ratio baseado em qualidade."""
        lr_map = {
            "strong": 15.0,    # LR 10-100
            "moderate": 5.0,   # LR 3-10  
            "weak": 2.0,       # LR 1.5-3
            "anecdotal": 1.2   # LR 1-1.5
        }
        return lr_map.get(evidence.quality, 1.0)
    
    def get_calibration(self) -> float:
        """Retorna confiança máxima permitida pela evidência atual."""
        quality_confidence = {
            "strong": 0.90,
            "moderate": 0.70,
            "weak": 0.50,
            "anecdotal": 0.30
        }
        if not self.evidence_log:
            return 0.5  # Prior não-informativo
        latest_quality = self.evidence_log[-1]["evidence"].quality
        return quality_confidence.get(latest_quality, 0.5)
```

---

## 🎯 Template de Atualização Bayesiana (Para Uso Prático)

```markdown
## Bayesian Update Log - YYYY-MM-DD

### Prior
- Hipótese H: [ex: "Deploy vai falhar"]
- Prior P(H): [ex: 20%]
- Prior Odds: [ex: 0.25]

### Evidência 1
- Descrição: [ex: "Canary 5% por 2h: 0 erros"]
- Fonte: measurement | expert | docs | inference
- Qualidade: strong | moderate | weak | anecdotal
- P(E|H): [ex: 0.10 - se falha, 10% chance de canary limpo]
- P(E|¬H): [ex: 0.95 - se sucesso, 95% chance de canary limpo]
- LR = P(E|H)/P(E|¬H): [ex: 0.10/0.95 = 0.105]

### Atualização
- Posterior Odds = Prior Odds × LR = [0.25 × 0.105 = 0.026]
- Posterior P(H) = [0.026 / 1.026 = 2.5%]

### Nova Confiança Calibrada
- Max permitida (evidence=strong): 90%
- Confiança declarada em sucesso: 97.5% ✅ (≤ 90%? NÃO → calibrar para 90%)

---

### Evidência 2 (sequencial)
- Descrição: [ex: "Load test 100 RPS 10min: 0 erros"]
- Qualidade: moderate
- LR: 5.0
- Posterior Odds: 0.026 × 5.0 = 0.13
- Posterior P(H): 11.5%
- Max confiança (moderate): 70%
- Confiança em sucesso: 88.5% ❌ > 70% → CALIBRAR PARA 70%
```

---

## 🔧 Integração com Self-Check v7 (Checkpoint 7)

```python
def self_check_checkpoint_7(
    confidence: float,
    evidence: Evidence,
    bayesian_updater: BayesianUpdater
) -> CheckpointResult:
    """
    Checkpoint 7: Evidence Quality Calibrated
    'Confiança calibrada com qualidade da evidência?'
    """
    max_confidence = bayesian_updater.get_calibration()
    
    if confidence > max_confidence + 0.05:  # 5% tolerância
        return CheckpointResult(
            passed=False,
            blockers=[f"Confiança {confidence:.0%} > max permitida {max_confidence:.0%} para evidence={evidence.quality}"],
            required_actions=[f"Calibrar confiança para ≤ {max_confidence:.0%} ou melhorar evidence quality"]
        )
    
    return CheckpointResult(passed=True, can_proceed=True)
```

---

## 📊 Tabela de Referência Rápida (Cheat Sheet)

| Prior | Evidence | LR | Posterior | Max Conf |
|-------|----------|-----|-----------|----------|
| 50% | Strong (LR=15) | 15 | 94% | 90% |
| 50% | Moderate (LR=5) | 5 | 83% | 70% |
| 50% | Weak (LR=2) | 2 | 67% | 50% |
| 50% | Anecdotal (LR=1.2) | 1.2 | 55% | 30% |
| 20% | Strong (LR=15) | 15 | 79% | 90% |
| 20% | Moderate (LR=5) | 5 | 56% | 70% |
| 80% | Strong (LR=0.07 contra) | 0.067 | 21% | 90% |
| 80% | Moderate (LR=0.2 contra) | 0.2 | 44% | 70% |

---

## 🎯 Regras Práticas (Heuristics)

1. **Extraordinary claims require extraordinary evidence** — Prior baixo + claim alto → exige evidence strong
2. **Absence of evidence is not evidence of absence** — Só se LR calculado considerando P(E|¬H)
3. **Conservation of expected evidence** — E[Posterior] = Prior (não pode "ganhar" confiança no esperado)
4. **Se três evidências weak concordam → ainda weak** — LR multiplica mas quality não sobe
5. **Calibração > Precisão** — Melhor estar 70% confiante e calibrado que 90% e errado

---

## 🔧 Integração com Outras Skills

| Skill | Integração |
|-------|------------|
| **Self-Check v7** | Checkpoint 7 usa BayesianUpdater para calibrar confiança |
| **Metacognition** | BayesianUpdater loga no metacognition graph como evidence nodes |
| **Thinking Frameworks** | Bayesian = framework próprio; combina com First Principles + Inversion |
| **Metacognition** | Calibration history → metacognition graph para detectar overconfidence patterns |
| **Capability Evolver** | Patterns de miscalibration → auto-rules para forçar calibração |
| **Task Pilot** | Bayesian updates nos verification gates para decisões go/no-go |

---

## 📜 Licença

MIT — Parte do projeto Damon Evolution (github.com/eapeli/damon)