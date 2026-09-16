---
trigger: always_on
description: "Load when: reviewing active execution logs or feedback loops to check if code fixes met objectives."
---
# Workflow: The Reflection Engine (Reflective Loop) v2.0

**Description**: Module that creates the difference between "Remembering a lot" and "Actually learning". Transforms raw Data into Principles. Integrated with Experience Engine and Learning Velocity Tracker.

## 1. Triggers (When to reflect?)
- At the end of a major Task (Merge PR, Complete a module).
- End of working session (End of Session).
- After a Mental Simulation prediction was wrong (calibration feedback).

## 2. Process (The Loop)

**Step 1: Self-Critique**
Agent self-scans Execution Logs / Outcome Tracking and answers:
- *What went WELL?* (Example: Code worked on first run, User had no complaints).
- *What went POORLY?* (Example: Suggested wrong library 2 times, User had to manually overwrite code, CPU spiked).
- *Knowledge gaps?* (Add to `uncertainty-register.yaml`).

**Step 2: Memory Compression (Data Compression & Abstraction)**
Transform data by hierarchy level:
1. **Session (Raw):** "Today User fixed my C code 3 times to remove nested structs."
2. **Episode (Event):** "Embedded Project X dislikes complex structs."
3. **Pattern (Common denominator):** "User always prioritizes readability over deep encapsulation."
4. **Principle:** "ALWAYS CHOOSE EXPLICIT CODE. Avoid abstraction unless mandatory."

**Step 3: Experience Engine Ingestion** *(NEW in v2.0)*
If the completed task has a noteworthy outcome (success/failure/new lesson):
- Create new entry in `memory/experience-engine.yaml → real_entries[]`
- Schema: `{id, domain, context, outcome, root_cause, lesson, timestamp, confidence, tags, source}`
- MUST comply with False Memory Guard — only record data with real evidence

**Step 4: Learning Velocity Update** *(NEW in v2.0)*
Assess whether any velocity signals appeared during the session:
- User requested more complex tasks → velocity = improving
- User requested re-explanation > 2 times → velocity = declining
- Update `memory/learning-velocity.yaml → domain_skills[domain].velocity`
- Update `last_assessed` timestamp

**Step 5: Update Meta-Memory**
- Delete raw Session/Episode logs to free memory.
- Write new Principle into the system (e.g., `preferences.md`).
- Set Meta-Memory score: `Importance = 0.95`, `Confidence = 0.9` (distilled from multiple occurrences).
- Update *Decision Log*: Record why this Principle was born.

**Step 6: Causal Graph Update** *(NEW in v2.0)*
If a new causal pattern is discovered (e.g., "Every time library X is used, error Y occurs"):
- Add node + edge to `memory/causal-graph.yaml`
- Ensure weight reflects actual confidence
- Do not add edges if it only occurred once (requires >= 2 observations)

## 3. Integration Points
- **Input from**: `workflows/mental-simulation.md` (simulation accuracy feedback)
- **Output to**: `memory/experience-engine.yaml`, `memory/learning-velocity.yaml`, `memory/causal-graph.yaml`
- **Validator**: After writing, run `scripts/memory_validator.py` to check consistency

