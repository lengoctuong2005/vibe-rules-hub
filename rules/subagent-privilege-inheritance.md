---
trigger: load_on_demand
description: "Subagent Privilege Inheritance - Ensures spawned subagents inherit all security rules from the parent agent. Prevents privilege escalation."
---
# Subagent Privilege Inheritance (Thừa kế đặc quyền Subagent)

## Purpose
Ensure spawned subagents maintain the same security posture as the parent agent. No security rule bypass via child process.

## Trigger
Load when using `browser_subagent`, `agents/spawner.py`, or any mechanism that creates a child execution context.

## Rules

### 1. Security Rule Propagation
When spawning a subagent, the parent MUST include in the task description:
- All active security constraints (no secret output, no destructive ops without approval).
- File/directory scope limitations.
- The current User's approval status for any pending operations.

### 2. Subagent Self-Audit
Before executing its first action, a subagent must verify:
- It has received security constraints from the parent.
- It will not perform operations outside its delegated scope.
- It will not install packages, modify configs, or access secrets unless explicitly authorized.

### 3. Privilege Escalation Detection
The following patterns indicate privilege escalation and must trigger `[BLOCK]`:
- Subagent attempts to modify files outside its assigned directory scope.
- Subagent attempts to run commands not listed in its task description.
- Subagent attempts to spawn further subagents without parent authorization.
- Subagent attempts to disable or bypass any inherited security rule.

### 4. Result Validation
Parent agent must validate subagent output before incorporating it:
- Check for unexpected file modifications.
- Verify no secrets or credentials appear in the output.
- Confirm the output matches the delegated task scope.
