---
trigger: always_on
description: "Load when: checking project knowledge gaps or uncertainty registers before planning complex implementations."
---
# Workflow: Epistemic Check (Metacognition)

**Description**: This workflow is designed for the Agent to self-reflect on its knowledge gaps BEFORE making decisions or generating code. It shifts AI behavior from "Pretending to know" to "Proactively clarifying".

## 1. Trigger Conditions
- At the start of each new session.
- When entering the `PLANNING` phase (Execution planning).
- When facing a major Technical Choice (choosing a framework, architecture, or library).

## 2. Process
**STEP 1: Load Uncertainties**
Read file `~/.gemini/memory/epistemic/uncertainty-register.yaml`.

**STEP 2: Cross-Check**
Check whether the current User Request touches any `topic` with `status: missing_data` or `conflicting_evidence`.

**STEP 3: Resolution**
- If MATCH found: Agent **MUST** stop making autonomous decisions. Apply `resolution_strategy` (Usually prints an `[ASK]` question for user).
- If NO match: Continue normal execution.

**STEP 4: Update Register**
After User answers the question from STEP 3:
- Update information into `preferences.md` or `profile.md`.
- Delete (or mark `status: resolved`) that entry from `uncertainty-register.yaml`.

