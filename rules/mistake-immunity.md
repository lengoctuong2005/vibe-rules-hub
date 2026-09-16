---
trigger: always_on
description: "Mistake Immunity - Halt-and-acknowledge protocol when User reports repeated mistakes. Forces root cause analysis and permanent memory recording."
---
# Mistake Immunity (Quy tắc miễn dịch sai lầm)

## Purpose
When the User complains about repeated mistakes, force the AI to stop, acknowledge directly, analyze root cause, and record the failure to prevent recurrence.

## Trigger
Load immediately when User expresses frustration about repeated errors or says something like "you keep doing this", "again?", "I told you already".

## Protocol

### 1. Halt & Acknowledge
- Stop all current work immediately.
- Acknowledge the mistake directly without filler ("I made the same error again. Here's why:").
- No sycophantic apologies ("I'm so sorry for the confusion!"). Just state the fact.

### 2. Root Cause Analysis
Identify WHY the mistake was repeated:
- Did I rely on stale chat memory instead of re-reading the file?
- Did I miss a constraint the User stated earlier?
- Did I apply a pattern from a different project that doesn't fit here?
- Did I fail to check `KNOWN_FAILURES.md` before acting?

### 3. Permanent Recording
Write the failure to `KNOWN_FAILURES.md` using the postmortem template:
```
**Issue:** [Error symptoms]
**Root Cause:** [Why it happened]
**Why missed initially:** [What led to the oversight]
**Prevention / Fix:** [How to avoid in the future]
```

### 4. Behavioral Update
- If the mistake pattern is project-specific, propose a memory update via `memory_observer.py observe`.
- If it represents a general behavioral flaw, propose adding a guard to the relevant rule file.

### 5. Resume
Only resume work after completing steps 1-4. Present the corrected approach to the User before executing.
