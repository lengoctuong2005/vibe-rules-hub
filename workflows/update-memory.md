---
trigger: always_on
description: "Load when: task is completed to propose updates to system episodic memory, lessons learned, or preferences."
---
# Workflow: Update Memory Bank

**Description**: Write mechanism for Episodic and Semantic memory. Responsible for "learning" from user after each interaction and storing as long-term memory.

## 1. Trigger Conditions
This workflow is automatically invoked by the system or called by the user when:
1. **Manual**: User gives a direct command (e.g., "Save this to memory" or `/update-memory`).
2. **Task Boundary**: Agent completes a major task at Tier 2+ level (part of VERIFICATION / DoD checklist phase).
3. **Pattern Recognition**: Agent detects a pattern (habit, recurring error, new preference) appearing >= 3 times in working memory.

## 2. Process
**STEP 1: Evaluate**
Scan through session log / current context. Find architectural decisions, preferences, or new habits not yet in current memory.

**STEP 2: Filter**
Remove trivial details (one-off syntax errors, typos). Keep only patterns with recurrence (Episodic) or core identity significance (Semantic). Classify whether it belongs to `Global` (applies everywhere) or `Local` (this project only).

**STEP 3: Propose (MANDATORY)**
- **MUST NOT OVERWRITE MEMORY FILES WITHOUT APPROVAL.**
- Must print to terminal/chat prompt per False Memory Guard standard:
  > `[PROPOSED MEMORY UPDATE] Target: <Local/Global> | Detected: <Pattern/Fact> | Evidence: <Reference/Logs> | Approve? [Y/N]`

**STEP 4: Execute**
- If User selects `Y`: Update the corresponding file in `~/.gemini/memory/` (global) or `[project]/.gemini/memory/` (local). Update in Markdown list format.
- If User selects `N`: Cancel the request, do not re-suggest this specific pattern during the current session.

