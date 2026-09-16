---
trigger: model_decision
description: "Load when: deploying code to GitHub. Performs safety secret scan and git commit automation."
---

# Command: Deploy Github (/deploy-github)

**Objective**: Automatically perform safety scans and push changes to GitHub.

**Agent Execution Steps**:
1. Run safety scanning: `python %USERPROFILE%/.gemini/scripts/safety_guard.py --scan-file .` to ensure no credentials or secrets are exposed.
2. Check `git status` to identify modified files.
3. Generate standard commit messages based on project conventions.
4. Execute `git add`, `git commit`, and `git push`.
5. Report the final execution status to the user.
