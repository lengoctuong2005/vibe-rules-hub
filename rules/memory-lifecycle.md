---
trigger: always_on
description: "Memory Lifecycle, Reflection & Grounding: Governs memory update protocol, contradiction reconciliation, latent briefing context compression, 5-step reflection engine, experience engine ingestion, and execution grounding."
---
# Memory Lifecycle, Reflection & Execution Grounding

## 1. Memory Update Protocol & False Memory Guard
Transform episodic context into persistent system knowledge while guarding against false or unverified memories.

### 1.1 Trigger Conditions
Automatically invoke memory updating when:
1. **Manual Command:** User explicitly runs `/update-memory` or `/save-memory`.
2. **Task Completion Boundary:** Completing a Tier 2+ milestone during Definition of Done (DoD) verification.
3. **Pattern Recognition:** Observing a habit, constraint, or recurring error pattern $\ge 3$ times in working memory.

### 1.2 4-Step Update Process
- **Step 1 (Evaluate):** Scan session history for genuine architectural decisions, domain constraints, or confirmed user preferences.
- **Step 2 (Filter):** Discard one-off syntax fixes and superficial noise. Classify surviving entries as `Local` (project-scoped) or `Global` (cross-project).
- **Step 3 (Propose - MANDATORY Gate):** Never write to persistent memory files without explicit confirmation. Output the standard False Memory Guard proposal:
  ```
  [PROPOSED MEMORY UPDATE] Target: <Local/Global> | Detected: <Pattern/Fact> | Evidence: <Reference/Logs> | Approve? [Y/N]
  ```
- **Step 4 (Execute):**
  - If Approved (`Y`): Append structured record via `scripts/memory_observer.py observe` or update `.gemini/memory/session-state.md` and database stores.
  - If Rejected (`N`): Abort update immediately and suppress re-proposing this pattern during the current session.

## 2. Memory Reconciliation & Contradiction Resolution
Eliminate conflicting directives, consolidate duplicates, and maintain truth integrity.

### 2.1 Contradiction Detection
When querying memory stores (SQLite RAG, `preferences.md`, `.env`), if opposing directives are discovered (e.g. "Use Node 18" vs "Project requires Node 20"):
- **HALT** autonomous decisions immediately. Do not guess the winner.

### 2.2 Presentation & Resolution Protocol
Present conflicts clearly to the user:
```
[MEMORY CONFLICT] Conflicting directives found in memory:
 - A: [Directive 1 with source reference]
 - B: [Directive 2 with source reference]
Which is authoritative for this workspace?
```
Upon user confirmation, permanently purge the obsolete record from the database and record the exception in `memory/causal-graph.yaml`.

### 2.3 Episodic-to-Semantic Promotion
Periodically consolidate fine-grained turn notes into long-term knowledge (`layer4_lessons_learned.md` / SQLite vault), prioritizing recent timestamped entries with verifiable evidence.

## 3. Latent Briefing & Context Compression
Mitigate context decay and token exhaustion during long-running sessions.

### 3.1 Episodic Summarization
At task completion, replace raw message logs with an Episodic Brief generated via `scripts/memory_observer.py summarize`:
- **Goal:** Core objective attempted.
- **Result:** Exact files modified and public contracts changed.
- **Lessons:** Roadblocks encountered and mechanisms applied to bypass them.

### 3.2 Semantic Promotion
If a concept, library, or architectural pattern is referenced across $\ge 3$ episodic summaries, promote it to Semantic Memory via `scripts/memory_consolidator.py` and evict low-level traces.

### 3.3 The Latent Briefing Pattern
At session initialization, load ONLY the 4-point Latent Briefing:
1. **Project Architecture:** 1 concise paragraph describing system structure.
2. **Current State:** 1 concise paragraph on recent stability and active branch.
3. **Active Invariants:** Bulleted list of non-negotiable architectural rules.
4. **Immediate Task:** 1 sentence defining current goal.

*Rely on RAG tools (`scripts/rag_memory_engine.py query` / `scripts/memory_search.py`) for deep retrieval on-demand.*

### 3.4 Context Eviction
Every 10 turns, prune expired debug traces, stale diffs, and resolved error messages from active working memory.

## 4. The 5-Step Reflection Engine (v2.0)
Transform raw session execution into durable architectural wisdom upon completing major tasks:

- **Step 1: Self-Critique:** Review tool outcomes. Identify what succeeded, what failed, and register knowledge gaps into `uncertainty-register.yaml`.
- **Step 2: Memory Compression:** Abstract raw data up the hierarchy:
  $$\text{Session (Raw)} \longrightarrow \text{Episode (Event)} \longrightarrow \text{Pattern (Recurrence)} \longrightarrow \text{Principle (Rule)}$$
- **Step 3: Experience Engine Ingestion:** Record notable outcomes into `memory/experience-engine.yaml → real_entries[]` with fields `{id, domain, context, outcome, root_cause, lesson, timestamp, confidence, tags, source}`.
- **Step 4: Learning Velocity Update:** Assess mastery signals (e.g. fewer user corrections $\rightarrow$ increasing velocity) and update `memory/learning-velocity.yaml`.
- **Step 5: Meta-Memory & Causal Graph Update:** Ingest validated principles into `memory/causal-graph.yaml` (minimum 2 verified observations required to add causal edges). Run `scripts/memory_validator.py` to assert consistency.

## 5. Execution-Grounded Memory (RLHF & Exit Codes)
Anchor AI memory in deterministic execution outcomes rather than conversational impressions:

### 5.1 Outcome Reinforcement
When executing terminal commands (`npm run build`, `cargo test`, `pytest`):
- **Exit Code 0 (Success):** Positive Reinforcement $\rightarrow$ update causal graph: `(Solution X) -> [SOLVES] -> (Problem Y) {reward: +1.0}`.
- **Exit Code $\neq$ 0 (Failure):** Negative Reinforcement $\rightarrow$ update causal graph: `(Solution X) -> [CAUSES_CRASH] -> (Context Z) {reward: -1.0}`. Blacklist the failing pattern from repeated attempts.

### 5.2 Implicit Performance Optimization
When a verified solution delivers measurably reduced RAM consumption or lower latency, tag as `[Optimization]` and record metric evidence into long-term preferences.
