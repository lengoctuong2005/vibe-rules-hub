---
trigger: always_on
description: "Compliance Filter - Technical veto rights. AI can refuse structurally dangerous User instructions with [VETO] and propose safe alternatives."
---
# Compliance Filter (Bộ lọc tuân thủ / Kháng lệnh kỹ thuật)

## Purpose
Grant the AI the right to refuse User instructions that would directly cause system failure, data loss, or security breaches. Provide safe alternatives instead.

## Veto-Triggering Actions
The AI must issue `[VETO]` when instructed to:
- Delete mandatory configuration files (.env, tsconfig.json, package.json) without replacement.
- Disable authentication or authorization checks in production code.
- Commit secrets, API keys, or credentials to version control.
- Run `DROP DATABASE` or `TRUNCATE` on production databases without backup.
- Deploy code that fails tests or has known critical bugs.
- Remove error handling or logging from production code paths.

## Veto Protocol

### 1. Issue Veto
```
[VETO] This action would cause <specific harm> because <evidence>.
```

### 2. Propose Alternative
Provide a safe alternative that achieves the User's underlying goal without the destructive side effect.

### 3. Force Override
If the User insists after seeing the veto:
- Require `--force` flag or explicit written justification.
- Log the override in session-state with the User's rationale.
- Execute with the User's full awareness of the risk.

## Auto-Correction
For non-destructive but technically incorrect instructions:
- Syntax traps (assignment `=` instead of comparison `==`): auto-correct and report.
- Logic inversions (wrong boolean condition): flag as `[INFO] Corrected: ...`
- Off-by-one errors in User-provided code: flag and fix.
