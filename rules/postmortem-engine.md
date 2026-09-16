---
trigger: always_on
description: "Load when: performing a postmortem analysis after resolving complex bugs or system-wide regressions. Contains failure analysis mapping and memory bank logging steps."
---
# Workflow: Postmortem System & Root Cause Learning

**Description**: System that transforms "Experience" into "Wisdom" through post-task failure dissection.

## 5-Step Cycle (Long-Term Learning Loop):
After debugging a particularly difficult bug, AI must self-run this cycle:
1. **Incident**: What just happened?
2. **Root Cause**: Trace to the absolute root cause (Avoid storing Symptoms — surface-level indicators).
3. **Missed Detection**: Why didn't we (AI and User) detect it sooner? Where is the gap in our process?
4. **Prevention**: How to ensure this error NEVER recurs? (Fix code, add tests, add rules).
5. **Principle Update**: Record the lesson into `experience-engine.yaml` with increased Experience Weighting. Recurring errors receive very high scores.

