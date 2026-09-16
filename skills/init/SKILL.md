---
name: init
description: Initialize .gemini and .agents workspace structure and rules for the current project directory.
metadata:
  trigger: "/init"
  tier: 2
---

# Initialize Project Workspace (/init)

Initialize Antigravity / Gemini OS environment, rules, workflows, skills, and memory structure for the current workspace.

## When to Run
- When starting work in a new or uninitialized project folder
- When user executes `/init`
- When `.agents/`, `.gemini/`, or `RULES_MANIFEST.md` are missing in the current project workspace

## Execution Steps
1. Run the auto-initialization script for the current directory:
   - Windows: `python %USERPROFILE%/.gemini/scripts/auto_init_project.py`
   - Linux/macOS: `python ~/.gemini/scripts/auto_init_project.py`
2. Verify that workspace configuration, rules, workflows, and session state are created.
3. Announce completion to user.
