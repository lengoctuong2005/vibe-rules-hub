---
trigger: always_on
description: "Load when: grounding terminal tool commands in verified memory observations and project environment configurations."
---
# Workflow: Execution-Grounded Memory (RLHF)

**Description**: Links memory to actual execution results (Test/Run Command) rather than only relying on User's verbal input.

## Process
When Agent runs a command via terminal (e.g., `npm run build`, `make`, `pytest`):

1. **Capture Result (Exit Code)**
   - If `Exit Code == 0` (Success): Trigger Positive Reinforcement.
   - If `Exit Code != 0` (Crash/Error): Trigger Negative Reinforcement.

2. **Record Trace**
   - **Success**: Update Graph: `(Solution X) -> [SOLVES] -> (Problem Y) {reward: +1.0}`.
   - **Failure**: Update Graph: `(Solution X) -> [CAUSES_CRASH] -> (Context Z) {reward: -1.0}`. Forbid repeating this solution next time.

3. **Update Implicit Preference**
   - If code runs faster or uses less RAM than the previous version, automatically tag `[Optimization]` and save to `preferences.md`.

