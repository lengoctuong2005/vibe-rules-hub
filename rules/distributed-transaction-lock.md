---
trigger: load_on_demand
description: "Distributed Transaction Lock - Two-Phase Locking for shared resources. Prevents race conditions and deadlocks in multi-agent scenarios."
---
# Distributed Transaction Lock (Khóa giao dịch phân tán)

## Purpose
Prevent race conditions and deadlocks when multiple agents or subagents operate on shared resources.

## Trigger
Load when multiple subagents are active or when modifying shared resources (migrations, .env, CI/CD configs, session-state).

## Protocol

### 1. Two-Phase Locking (2PL)
Before modifying any shared resource:
1. **Acquire phase**: Request lock via `scripts/lock_manager.py --acquire <resource>`.
2. **Execute phase**: Perform the modification.
3. **Release phase**: Release lock via `scripts/lock_manager.py --release <resource>`.

### 2. Lock Retry with Backoff
If lock acquisition fails:
- Retry up to 3 times with 5-second intervals.
- After 3 failures: release ALL currently held locks (prevents hold-and-wait deadlock).
- Enter random backoff (5-15 seconds) before retrying the entire transaction.

### 3. Deadlock Prevention
Enforce a global resource ordering to prevent circular wait:
1. Database/migration files (highest priority)
2. Environment files (.env, configs)
3. Source code files
4. Documentation and memory files (lowest priority)

Agents must always acquire locks in this order. Never acquire a lower-priority lock while holding a higher-priority one.

### 4. Timeout Auto-Release
- Any lock held for >30 seconds without activity is automatically released.
- The holding agent receives a `[LOCK EXPIRED]` notification.

### 5. Conflict Resolution
If a lock conflict is detected (via git status or timestamp mismatch):
- STOP immediately.
- Report `[LOCK CONFLICT: <resource>]` to the User.
- Do not attempt automatic resolution.
