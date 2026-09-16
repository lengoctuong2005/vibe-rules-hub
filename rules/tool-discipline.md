---
trigger: always_on
description: "Tool Discipline - Enforces reuse of existing Antigravity scripts and tools before inventing new ones. Prevents reinventing the wheel."
---
# Tool Discipline (Kỷ luật công cụ bản địa)

## Purpose
Maximize reuse of existing Antigravity infrastructure. Prevent the AI from writing ad-hoc scripts when equivalent tooling already exists.

## Rules

### 1. Check Before You Build
Before proposing any automation script or shell command:
1. Search `scripts/` directory for existing utilities.
2. Check `RULES_MANIFEST.md` for relevant workflows.
3. Search skill catalog via `scripts/rag_memory_engine.py` if needed.

### 2. Existing Tool Registry (Partial)
Known internal tools that MUST be used instead of ad-hoc alternatives:
- File locking: `scripts/lock_manager.py` (not ad-hoc flock/lockfile)
- Git branching for parallel work: `scripts/worktree_manager.py`
- Secret scanning: `scripts/safety_guard.py`, `scripts/privacy_vault.py`
- Memory operations: `scripts/memory_search.py`, `scripts/memory_observer.py`
- Compliance checks: `scripts/compliance_monitor.py`
- Regression testing: `scripts/regression_gate.py`
- Cost tracking: `scripts/cost_ledger.py`

### 3. New Script Justification
If no existing tool covers the need:
1. State which tools were checked and why they are insufficient.
2. Propose the new script with a clear scope description.
3. Place it in `scripts/` following existing naming conventions.
4. Update `RULES_MANIFEST.md` after creation.

### 4. No External Package Installs Without Approval
- NEVER run `pip install`, `npm install`, or equivalent without explicit User approval.
- Check `scripts/requirements.txt` or `package.json` for existing dependencies first.
