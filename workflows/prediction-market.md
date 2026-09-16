---
trigger: model_decision
description: "Load when: scoring alternative technical architectures or design choices (e.g. databases, state managers, frameworks) based on internal prediction markets."
---
# Workflow: Internal Prediction Market (Decision Confidence Engine)

**Description**: When facing important architecture/design decisions with more than 1 option, Agent creates a quick "internal prediction market" — bets on different solutions based on evidence, then selects the solution with the highest odds.

**Objective**: Counter "pick the first thing that comes to mind" bias (Anchoring Bias). Forces Agent to consider at least 2 alternative solutions before committing.

**Scope**: Applied when Agent must make an architecture/technology decision with >=2 viable options.

---

## 1. Triggers

- User asks "Should I use X or Y?"
- Agent identifies >= 2 feasible approaches for the same problem
- Decision impacts >= 3 files or >= 1 module
- Any time Agent is less than 70% confident about the optimal solution

---

## 2. Process (Single-Prompt Market)

### STEP 1: GENERATE CANDIDATES

Agent lists minimum 2, maximum 4 viable solutions:

```
| ID | Solution      | Brief Description |
|----|---------------|-------------------|
| A  | [Name A]      | [1 line]          |
| B  | [Name B]      | [1 line]          |
| C  | [Name C]      | [1 line]          |  (optional)
```

### STEP 2: MULTI-CRITERIA SCORING

Each solution is scored on 5 axes (0.0 → 1.0):

```
| Criterion                   | Weight | A     | B     | C     |
|-----------------------------|--------|-------|-------|-------|
| Fit with User Preferences   | 0.25   | ?     | ?     | ?     |
| Implementation Complexity   | 0.20   | ?     | ?     | ?     |
| Long-term Maintainability   | 0.20   | ?     | ?     | ?     |
| Risk (from Failure DB)      | 0.20   | ?     | ?     | ?     |
| Evidence Strength           | 0.15   | ?     | ?     | ?     |
```

**Data sources for scoring**:
- `memory/causal-graph.yaml` → Fit with preferences (traverse PREFERS/FORCES/BLOCKS edges)
- `memory/failure-database.yaml` → Risk (check anti-patterns)
- `memory/experience-engine.yaml` → Evidence (past real outcomes)
- `memory/learning-velocity.yaml` → Complexity fit (match user skill level)

### STEP 3: CALCULATE ODDS

```
Weighted Score = Σ (score[i] × weight[i]) for each criterion
Odds = Weighted Score / Σ(All Weighted Scores)
```

### STEP 4: ADVERSARIAL CHECK

Before selecting winner:
- "Why should the losing solution NOT be eliminated?"
- "Are there edge cases where the losing solution is actually better?"
- If delta between top-1 and top-2 < 0.05 → Report "TIE" and ask User to decide

### STEP 5: DECLARE WINNER

---

## 3. Output Format

```
╔══════════════════════════════════════════════════╗
║         PREDICTION MARKET RESULT                 ║
╠══════════════════════════════════════════════════╣
║ Question: [Decision question]                    ║
║                                                  ║
║ 🥇 Winner: [Solution A] — Odds: 0.52            ║
║ 🥈 Runner-up: [Solution B] — Odds: 0.35         ║
║ 🥉 Third: [Solution C] — Odds: 0.13             ║
║                                                  ║
║ Key Factor: [Deciding criterion]                 ║
║ Risk Note: [Warning if any]                      ║
║ Confidence: [High/Medium/Low]                    ║
║ Adversarial Check: [Passed/Tie — User decides]   ║
╚══════════════════════════════════════════════════╝
```

---

## 4. Token Efficiency

**Key design**: The entire process runs in 1 SINGLE PROMPT — no need for multiple LLM calls.
Agent performs scoring via internal reasoning, no separate API call per step.

**Estimated token cost**: ~200-400 tokens output (equivalent to 1 normal response).

---

## 5. Calibration & Learning

After the decision is executed:
- Record actual results in `experience-engine.yaml`
- Compare prediction vs reality
- If prediction is wrong > 3 consecutive times for the same criterion → reduce that criterion's weight
- Update `meta-learning-calibration.yaml` with accuracy data

---

## 6. Practical Example

**Question**: "Should I use MQTT or WebSocket for IoT telemetry?"

```
| Criterion              | Weight | MQTT  | WebSocket |
|------------------------|--------|-------|-----------|
| Fit with Preferences   | 0.25   | 0.9   | 0.4       |
| Complexity             | 0.20   | 0.7   | 0.8       |
| Maintainability        | 0.20   | 0.9   | 0.5       |
| Risk (Failure DB)      | 0.20   | 0.2   | 0.9       |
| Evidence               | 0.15   | 0.95  | 0.3       |

MQTT Score:  0.25×0.9 + 0.20×0.7 + 0.20×0.9 + 0.20×0.2 + 0.15×0.95 = 0.7275
WS Score:    0.25×0.4 + 0.20×0.8 + 0.20×0.5 + 0.20×0.9 + 0.15×0.3  = 0.585

Winner: MQTT (Odds: 0.55 vs 0.45)
Key Factor: Risk — WebSocket has failed in failure-database (f_001)
```

