---
trigger: model_decision
description: "Load when: initializing new workspace structures or running the project init (/init) workflow."
---

# Command: Initialize Project (/init)

**Objective**: Initialize the `.gemini` structure for the current project workspace.

**Agent Execution Steps**:
1. Run the project initialization script: `python %USERPROFILE%/.gemini/scripts/auto_init_project.py`
2. If the script fails or does not exist, automatically create default folders: `.gemini/rules/`, `.gemini/workflows/`, `.gemini/memory/`.
3. Create a default `.gemini/memory/session-state.md` file.
4. Inform the user that the project was initialized successfully and is ready to use.
