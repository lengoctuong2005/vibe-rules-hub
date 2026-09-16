---
trigger: load_on_demand
description: "Rigorous Verification - Multi-layer testing protocol. Forces AI to verify code through syntax, unit tests, state analysis, and performance checks."
---
# Rigorous Verification (Quy tắc xác minh đa chiều)

## Purpose
Force the AI to verify its code changes through a structured 4-layer testing protocol before reporting completion.

## Trigger
Load after writing any functional code, API endpoint, or data processing logic.

## The 4-Layer Verification Protocol

### Layer 1: Syntax & Lint
- Run the project's linter or formatter if available.
- For TypeScript: check for type errors.
- For Python: check for syntax errors and import resolution.
- This layer catches: typos, missing imports, type mismatches.

### Layer 2: Unit Tests & Edge Cases
- Write or run unit tests for the modified logic.
- Test edge cases: empty input, null values, boundary values, large input.
- This layer catches: logic errors, off-by-one bugs, unhandled states.

### Layer 3: Blast Radius & State
- Verify that changes don't break existing functionality.
- Run `grep_search` for usages of modified functions/classes.
- Check that callers still receive the expected return types and shapes.
- This layer catches: breaking changes, contract violations, state corruption.

### Layer 4: Performance & Resource (When Applicable)
- Check for obvious performance issues: N+1 queries, unbounded loops, memory leaks.
- Verify timeout configurations for network calls.
- Check for resource cleanup (file handles, DB connections, event listeners).
- This layer catches: resource leaks, performance regressions, timeout issues.

## Evidence Requirement
- Execute test commands and include actual stdout/stderr in the response.
- Do not claim "tests pass" without running them.
- If tests cannot be run (no test framework, no runner), state this explicitly.
