---
trigger: always_on
description: "Load when: verifying proposed updates to user state, memory files, or preferences for conflicts."
---
# Workflow: Adversarial Memory Validation

**Description**: Self-adversarial mechanism to counter Confirmation Bias. Applied before permanently recording any Preference into memory.

## Process
Whenever a proposal arises: "Update Preference X into the system":

**STEP 1: SKEPTIC PERSONA (The Devil's Advocate)**
- Agent splits its perspective (or switches system prompt) to become a SKEPTIC.
- Mission: Review history to find evidence **AGAINST** Preference X.
- Example: Proposal "User hates Docker". Skeptic checks if there's a project where user happily requested a `Dockerfile`.

**STEP 2: JUDGE PERSONA (The Arbiter)**
- Weigh the SKEPTIC's evidence.
- If SKEPTIC is right: Cancel the memory write, change status to `conflicting_evidence` and push to `uncertainty-register.yaml` (Epistemic Memory).
- If SKEPTIC is wrong (no counter-evidence found): Confirm write to `preferences.md`.

