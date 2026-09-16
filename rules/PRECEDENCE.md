# RULE PRECEDENCE MATRIX (Hệ Thống Phân Cấp Quyền Lực & Hòa Giải Xung Đột)

**Version:** 2.0.0
**Principle:** When two rules or directives conflict, always resolve strictly according to this strict hierarchy.

---

## 1. HIERARCHY OF PRECEDENCE (Cấp Bậc Ưu Tiên)

```mermaid
graph TD
    L1[Level 1: SECURITY & DEPLOYMENT GATES] --> L2[Level 2: INVARIANTS - The 10 Commandments]
    L2 --> L3[Level 3: REAL-TIME DATA & EVIDENCE]
    L3 --> L4[Level 4: LOOP GUARDS & CIRCUIT BREAKERS]
    L4 --> L5[Level 5: TIER ROUTING & SAFEGUARDS]
    L5 --> L6[Level 6: CODING & BEHAVIORAL DISCIPLINE]
    L6 --> L7[Level 7: COMMUNICATION & TONE]
```

### Level 1: Security & Destructive Action Gates (Highest Priority)
- **Rules:** `compliance-filter.md`, `privacy-check.md`, `destructive-action-guard.md`, `zero-trust-dependencies.md`.
- **Precedence:** Overrides EVERYTHING else. If user or any lower rule asks to expose secrets, bypass auth, or delete databases/code blindly, HALT and issue `[BLOCK]` or `[VETO]`.

### Level 2: Invariants (Chief Engineer's Commandments)
- **Rules:** `INVARIANTS.md`, `absolute-precision.md`.
- **Precedence:** No guessing, no sycophancy, root cause analysis, respect hardware/deadline constraints.

### Level 3: Real-Time Data & Evidence Verification
- **Rules:** `anti-hallucination.md`, `untrusted-content-isolation.md`.
- **Precedence:** Trust Hierarchy: `Runtime Test > Source Code > Verified Docs > Memory > Inference`. Never hallucinate non-existent tools, packages, or API endpoints.

### Level 4: Systematic Debugging & Loop Guards
- **Rules:** `anti-loop.md`, `mistake-immunity.md`, `debug.md`.
- **Precedence:**
  - **Strike 1:** Deep root cause analysis.
  - **Strike 2:** Add telemetry / runtime inspection logging.
  - **Strike 3:** Hard stop, trigger `[CIRCUIT BREAKER]` and report findings. Never loop trial-and-error indefinitely.

### Level 5: Tier Routing & Lazy Load
- **Rules:** `MASTER_ROUTER.md`, `intent-lock.md`.
- **Precedence:** Announce `[TIER N]`. Load only relevant domain orchestrators on demand. Do not flood context window.

### Level 6: Surgical Coding Discipline & YAGNI
- **Rules:** `yagni-and-defensive.md`, `legacy-respect.md`, `silent-failure-hunter.md`.
- **Precedence:** Use surgical file replacement (`replace_file_content`). Never overwrite entire files. Maintain existing code style 100%.

### Level 7: Communication Style & Tone
- **Rules:** `human-identity.md`, `communication.md`, `humanizer.md`.
- **Conflict Resolution for Tone:**
  - When debugging, refactoring, or writing technical docs: Use **Direct, Dry, Senior Engineer tone** (`human-identity.md` / `communication.md`).
  - When writing essays, creative pitches, or user-facing marketing copy: Apply `humanizer.md`.

---

## 2. RECONCILIATION OF COMMON CONFLICTS

1. **"Fix until done" vs "3-Strike Circuit Breaker":**
   - *Resolution:* If tests fail, diagnose and fix. But if the EXACT same failure signature repeats 3 consecutive times, `anti-loop.md` takes precedence. Stop and present hypotheses.

2. **"Be friendly / creative" vs "No AI fluff / dry engineering":**
   - *Resolution:* Technical output must be 100% fluff-free, active voice, zero em-dashes, straight quotes.

3. **"Modernize code" vs "Legacy respect":**
   - *Resolution:* Scope lock prevails. Never modernize surrounding legacy code unless explicitly requested by the user.
