---
trigger: always_on
description: "Load when: analyzing internal execution failures or loop exceptions within the AI system."
---
# Workflow: Self-Debugging (AI Self-Analysis)

**Description**: Monitoring system that automatically updates rules/workflows when AI makes wrong decisions due to context gaps or poor reasoning.

## Process
**Step 1: Error Catching**
- User complains/objects: "Why did you import library X? This board only has 20KB RAM!"
- Record: AI just generated useless/architecturally misaligned code.

**Step 2: Root Cause Analysis**
- *Symptom*: Suggested a heavy library for a small MCU.
- *Cause*: Forgot to load `causal-graph.yaml` to check Hardware Constraints before searching for libraries.

**Step 3: System Patching**
- Automatically generate a new rule in `.gemini/rules/`:
> `[AUTO-RULE]: MUST load Hardware Constraints before suggesting any C/C++ library in Embedded projects.`

- Update Memory Lineage to record the origin of this rule.

