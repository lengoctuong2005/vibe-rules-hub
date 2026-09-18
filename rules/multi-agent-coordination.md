---
trigger: always_on
description: "Multi-Agent Coordination & Concurrency: Defines 3-layer isolation (Git Worktrees, append-only events.log, Orchestrator decisions), 2-Phase Locking (2PL), deadlock prevention, merge workflows, and subagent privilege inheritance."
---
# Multi-Agent Coordination, Concurrency & Governance

## 1. 3-Layer Architecture (Layered Defense)
Prevent memory corruption, state race conditions, context blindness, and conflicting decisions when multiple agents execute concurrently.

### 1.1 Layer 1: Physical Isolation via Git Worktrees
- **Ban Shared Branch Modification:** Subagents must never concurrently write to the same branch or `.git` directory directly.
- **Dedicated Worktrees:** Every subagent operating on source code runs in an isolated Git Worktree provisioned via `scripts/worktree_manager.py`:
  ```bash
  git worktree add ../work-agent-a agent/a-implement
  git worktree add ../work-agent-b agent/b-review
  ```
- File writes are physically isolated. Final integration relies on Git atomic merge mechanics.

### 1.2 Layer 2: Append-Only Event Log (Context Synchronization)
- Multi-agent collaboration directory: `agent_coord/` at project root.
- Log file: `agent_coord/events.log` in append-only JSONL format.
- Agents only append (`>>`), never edit past records:
  ```jsonl
  {"ts":"2026-09-18T10:00:00Z","agent":"A","event":"START","file":"auth.ts","approach":"JWT validation"}
  {"ts":"2026-09-18T10:05:00Z","agent":"B","event":"REVIEW","ref":"a-001","note":"Handle empty bearer token"}
  ```
- Before taking any major action, read `events.log` to track teammates' progress.

### 1.3 Layer 3: Decision Conflict Resolution via Single Orchestrator
- **Role Split:** Peer agents never resolve architectural conflicts autonomously (prevents infinite debate loops).
- **Proposals:** Agent proposals are filed under `agent_coord/proposals/` (e.g. `a-001.md`).
- **Orchestrator Authority:** The Master Orchestrator (or human user) is the single writer to `agent_coord/DECISIONS.md`. Decisions logged here are final and binding.

## 2. Operational Guidance by Task Scale
- **Small Task (<30 min, 1 file):** Role Split + `events.log` (sequential implement -> review; worktree optional).
- **Medium Task (multi-file, parallel):** Full 3 layers (Worktrees + `events.log` + Orchestrator review).
- **Large Task (>2 agents):** Dedicated worktrees per agent + specialized supervisor agent managing state via `DECISIONS.md`.

## 3. Two-Phase Locking (2PL) & Resource Governance
Prevent race conditions when modifying shared resources (`preferences.md`, `.env`, migrations, CI/CD pipelines, session-state):

### 3.1 Lock Protocol (2PL)
1. **Acquire Phase:** Request explicit lock via `python scripts/lock_manager.py --acquire <resource>`.
2. **Execute Phase:** Perform file modifications sequentially.
3. **Release Phase:** Release lock via `python scripts/lock_manager.py --release <resource>`.

### 3.2 Lock Retry with Backoff
- If lock acquisition fails, retry up to 3 times with 5-second intervals.
- After 3 failed attempts: release ALL currently held locks immediately (prevents hold-and-wait deadlocks).
- Apply random backoff (5-15 seconds) before retrying the entire transaction.

### 3.3 Timeout Auto-Release
- Locks held for >30 seconds without activity are automatically expired and released.
- Holding agent receives `[LOCK EXPIRED]` notification.

### 3.4 Conflict Resolution
- If lock conflict or timestamp mismatch occurs, STOP immediately.
- Issue `[LOCK CONFLICT: <resource>]` and request user guidance.

## 4. Deadlock Prevention & Global Resource Hierarchy
To prevent circular wait conditions, agents must acquire locks strictly in this global order:
1. **Database & Migration files** (Highest Priority)
2. **Environment & Configuration files** (`.env`, `package.json`, `tsconfig.json`)
3. **Source code files**
4. **Documentation & Memory files** (Lowest Priority)

*Never request a higher-priority lock while holding a lower-priority lock.*

## 5. Synchronization & Safe Merge Workflow
- Master Agent aggregates logs and artifacts from all completed worktrees.
- Merge worktree branches into main using `worktree_manager.py` with `--no-ff` (No Fast-Forward).
- If merge conflict occurs: automatically execute `git merge --abort`. Master agent resolves conflicts sequentially; never leave Git in a dangling merge state.

## 6. Subagent Privilege Inheritance & Security Boundaries
Spawned subagents (`browser_subagent`, `spawner.py`, worker agents) inherit parent security posture completely:

### 6.1 Constraint Propagation
Parent agents must explicitly pass:
- Active security constraints (secret masking, destructive op guards).
- Directory and file scope boundaries.
- Ponytail minimalist discipline (`// ponytail:` comments, YAGNI).

### 6.2 Subagent Self-Audit & Escalation Blocker
- Subagents must self-verify boundaries before running commands.
- Block with `[BLOCK: PRIVILEGE ESCALATION]` if a subagent attempts:
  1. Modifying files outside its delegated directory scope.
  2. Executing arbitrary commands not authorized in task definition.
  3. Spawning recursive subagents without parent approval.
  4. Disabling or bypassing inherited security rules.
- Parent agents validate all subagent diffs and outputs prior to merge.
