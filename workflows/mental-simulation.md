---
trigger: always_on
description: "Load when: simulating edge cases and failure modes in complex code edits before execution to prevent runtime regressions."
---
# Workflow: Mental Simulation Engine (Pre-Execution Risk Analysis)

**Description**: Before executing any Tier 3 change (auth/migration/schema/.env), Agent MUST run a "mental simulation" loop to predict consequences. This is the practical version of the "Mental Simulation Engine" — does not simulate the entire project, only focuses on impact analysis.

**Scope**: MANDATORY for Tier 3 operations. OPTIONAL for Tier 2 if Agent feels uncertain.

---

## 1. Triggers (When to activate?)

- Database schema changes or migrations
- Authentication/authorization flow changes
- Editing `.env` or production config files
- Deleting/renaming public API endpoints
- Build/deploy pipeline changes
- Any operation labeled `[USER CONFIRM]` in GEMINI.md

---

## 2. Simulation Process (The Simulation Loop)

### STEP 1: IMPACT MAPPING

Agent asks and answers 4 questions:

```
Q1: "If I apply this change, which files/modules WILL BE DIRECTLY AFFECTED?"
    → List concrete files/functions

Q2: "Are there dependency chains I HAVEN'T SEEN?"
    → Trace imports, configs, env vars

Q3: "Does this change VIOLATE any INVARIANT?"
    → Cross-reference with INVARIANTS.md (The 10 Commandments)

Q4: "If this change FAILS midway (partial apply), what will the state look like?"
    → Evaluate rollback strategy
```

### STEP 2: FAILURE DATABASE CROSS-CHECK

Agent MUST scan:
- `memory/failure-database.yaml` — Any matching anti-patterns?
- `memory/experience-engine.yaml` — Any lessons from the past?
- `memory/causal-graph.yaml` — Any edges that BLOCK/CONTRADICT this action?

If a match is found:
→ Print `[SIMULATION WARNING]` with specific reference
→ Request User confirmation before proceeding

### STEP 3: EDGE CASE GENERATION

Agent generates 3 "What-if" scenarios:

```
Scenario A (Happy Path):  Everything works correctly → What is the expected result?
Scenario B (Partial Fail): Step N succeeds, step N+1 fails → Recovery plan?
Scenario C (Total Fail):   Entire change fails → Rollback procedure?
```

### STEP 4: GO/NO-GO DECISION

Based on simulation results, Agent makes a decision:

| Result | Action |
|--------|--------|
| ✅ No warnings, clear rollback | Proceed, brief report |
| ⚠️ Warning but mitigation exists | Print `[SIMULATION WARNING]`, propose mitigation, wait for User |
| 🔴 Match with failure-database | Print `[SIMULATION BLOCKED]`, DO NOT execute until User overrides |

---

## 3. Output Format

When running simulation, Agent MUST print results in this format:

```
╔══════════════════════════════════════════════════╗
║         MENTAL SIMULATION REPORT                 ║
╠══════════════════════════════════════════════════╣
║ Operation: [Brief description]                   ║
║ Tier: 3                                          ║
║ Impact: [N files, M functions]                   ║
║ Invariants checked: [✅ Pass / ❌ Violation]      ║
║ Failure DB match: [None / Warning / Block]       ║
║ Experience DB match: [None / Relevant lesson]    ║
║ Rollback plan: [Yes / No]                        ║
║ Decision: [GO ✅ / WARNING ⚠️ / BLOCKED 🔴]      ║
╚══════════════════════════════════════════════════╝
```

---

## 4. Integration

- **Before execution**: `master-execution-loop.md` checks Tier → if Tier 3, invoke this workflow
- **After execution**: Simulation result vs reality is recorded in `experience-engine.yaml` to improve accuracy
- **Calibration**: If simulation predicts WRONG > 3 times → reduce weight of the offending rule in `meta-learning-calibration.yaml`

