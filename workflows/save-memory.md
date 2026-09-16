---
trigger: always_on
description: "Load when: saving active working memory state, lessons learned, or project preferences into centralized databases."
---

# Command: Save Memory (/save-memory)

**Objective**: Save lessons learned and summarize the current session into system memory.

**Agent Execution Steps**:
1. Review all modifications, architectural decisions, and lessons learned during the current session.
2. Update `.gemini/memory/session-state.md` and log an `observation` or `summary` using the `memory_observer.py` script.
3. Propose updates to user preferences or local knowledge bases if new habits/patterns are identified.
4. Output a concise session summary to the user.
