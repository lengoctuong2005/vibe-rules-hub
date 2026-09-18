---
trigger: always_on
description: "Debug & Systematic Incident Resolution: Enforces 3-strike circuit breaker, 10-step diagnostic protocol, dead-end recovery/rollback, postmortem analysis, and mistake immunity logging."
---
# Systematic Debugging, Incident Recovery & Mistake Immunity

## 1. The 3-Strike Circuit Breaker
Prevent trial-and-error loops, token exhaustion, and code history pollution.

- **Strike 1 (Initial Failure):**
  - Read logs and stack traces thoroughly.
  - Perform Root Cause Analysis (RCA).
  - Propose a targeted patch and apply the fix.
- **Strike 2 (Repeated Failure):**
  - **NEVER GUESS AGAIN.** Stop proposing speculative changes.
  - Inject runtime telemetry and inspection logging (`print()`, `console.log()`, `logger.debug()`) around suspicious execution paths.
  - Inspect fresh runtime logs before making any further code edits.
- **Strike 3 (Persistent Failure):**
  - **HARD STOP.** Cease blind modifications immediately.
  - Trigger `[CIRCUIT BREAKER]` and alert the user with: `[CONCERN: Exceeded self-debugging limit]`.
  - Summarize tested hypotheses, gathered telemetry logs, and hand off to the user or initiate Dead-End Recovery.

## 2. 10-Step Root Cause Diagnostic Protocol
When debugging runtime errors, build failures, or logic regressions:

1. **Reproduce Issue:** Create a minimal, deterministic reproduction scenario.
2. **Collect Evidence:** Capture logs, stack traces, metrics, and environment variables.
3. **List Observed Errors:** Catalog every explicit error symptom and silent anomaly.
4. **Build Dependency Graph:** Trace affected modules, data flow, and state interactions.
5. **Identify Root Cause:** Locate the fundamental flaw (do not confuse symptom with cause).
6. **Verify Root Cause:** Confirm how the defect produces the observed error.
7. **Fix Root Cause Only:** Apply the minimal surgical fix that addresses the root defect.
8. **Run Affected Tests:** Validate the fix against reproduction tests and existing test suites.
9. **Verify No Regression:** Ensure zero collateral damage across adjacent components.
10. **Update Failure Knowledge:** Record newly discovered regression patterns into `KNOWN_FAILURES.md`.

## 3. Dead-End Recovery & Rollback Protocol
When local fixes repeatedly fail or confidence drops below 30%:

### 3.1 Dead-End Detection
- After 3 failed patch attempts: STOP writing code and declare `[DEAD END REACHED] Local approaches are not resolving this issue.`

### 3.2 Zoom-Out Thinking (Macro Shift)
Shift perspective from micro code edits to macro architecture and environment. Evaluate:
1. Did the environment, dependencies, OS, or runtime change recently?
2. Is the issue reproducible in a fresh, clean environment?
3. Is a completely different architectural workaround preferable while root-cause investigation continues?

### 3.3 Rollback Offer
Propose a clean revert to the last known good state before trying alternative directions:
- Save active scratchpad: `git stash`
- Revert working tree: `git reset --hard <last_good_commit>`
- Isolate branch for experiments: `git checkout -b debug/<issue>`

### 3.4 Alternative Strategy & Escalation
- Application layer failed -> Investigate infrastructure and runtime configuration.
- Logic layer failed -> Investigate data schemas, race conditions, and payloads.
- If alternatives fail: escalate to upstream maintainers, seek domain experts, and document the known issue.

## 4. Postmortem & Mistake Immunity
When the user reports repeated errors or complex system-wide regressions occur:

### 4.1 Halt & Acknowledge
- Stop immediately without sycophantic filler ("I made the same error again. Here is why:").
- Identify whether failure was caused by stale chat memory, unverified assumptions, or missing constraints.

### 4.2 Logging to KNOWN_FAILURES.md
Record the incident into `KNOWN_FAILURES.md` using the standard postmortem format:
```markdown
**Issue:** [Error symptoms visible to User]
**Root Cause:** [Underlying architectural/logic defect]
**Why missed initially:** [Gap in evidence verification, stale context, or hallucination]
**Prevention / Fix:** [Concrete test, guard, or rule added to prevent recurrence]
```

### 4.3 5-Step Long-Term Learning Loop
1. **Incident:** What happened and what broke?
2. **Root Cause:** Trace to the exact physical/logic defect.
3. **Missed Detection:** Why did current tests or assertions fail to catch it?
4. **Prevention:** Implement permanent guards (regression tests, typing, validation).
5. **Principle Update:** Ingest lesson into `memory/experience-engine.yaml` with elevated weighting.

## 5. AI Self-Debugging & Telemetry
- **Error Catching:** Detect when generated code violates project constraints (e.g. heavy dependencies on low-memory targets).
- **Automated Rule Patching:** When an architectural mistake occurs due to missing domain context, synthesize an automated guard in `.gemini/rules/` or local project rules (e.g., `[AUTO-RULE]: Check hardware constraints before selecting libraries`).
- **Memory Lineage Tracking:** Update memory records with the failure trace so future subagents do not repeat the failure.
