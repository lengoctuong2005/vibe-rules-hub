---
trigger: always_on
description: "Intent Lock - Forces AI to echo and confirm User's intent before writing code. Prevents scope creep and misaligned implementations."
---
# Intent Lock (Quy tắc khóa mục tiêu)

## Purpose
Force the AI to explicitly confirm the User's intent before starting non-trivial code changes. Prevent scope creep and misaligned implementations.

## Trigger
Load before starting any task that modifies >1 file or involves architecture/logic changes.

## Echo & Confirm Protocol

### Step 1: Echo
Before writing any code, state in plain language:
- **Goal (A)**: The core objective of this change.
- **Constraints (B)**: Mandatory conditions (preserve existing API, specific tech stack, performance targets).
- **Off-limits (C)**: Areas explicitly NOT to touch.

Format:
```
[INTENT LOCK]
Goal: <A>
Constraints: <B>
Off-limits: <C>
```

### Step 2: Confirm
- For Tier 2+ tasks: Wait for User confirmation before proceeding.
- For Tier 1 tasks: State the intent lock inline and proceed (no wait needed).

### Step 3: Scope Guard (During Execution)
While writing code, periodically check:
- "Does this line directly serve Goal A?"
- "Does this change respect Constraints B?"
- "Am I touching anything in Off-limits C?"

If the answer to any is "no", stop and reassess. Do not include tangential improvements unless the User asks for them.

## Anti-Scope-Creep Checklist
Before reporting completion, verify:
- [ ] No files modified outside the stated scope.
- [ ] No "bonus" refactors applied without User request.
- [ ] No dependency changes made beyond what the task requires.
