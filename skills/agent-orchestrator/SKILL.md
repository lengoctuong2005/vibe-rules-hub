---
name: agent-orchestrator
description: |
  Comprehensive Agent Orchestrator pipeline engine coordinating end-to-end software development operations (Add Feature, Fix Defect, Refine Code, Change Feature, Build MVP). Enforces size classification, gated execution (Plan Gate & Commit Gate), subagent delegation (planner, architect, tdd-guide, code-reviewer, security-reviewer), and TDD red-green-refactor workflows.
triggers:
  - "orchestrator"
  - "agent orchestrator"
  - "orch-pipeline"
  - "orch add feature"
  - "orch fix defect"
  - "orch refine code"
  - "orch build mvp"
  - "orch change feature"
  - "tdd pipeline"
license: MIT
metadata:
  origin: ECC
---

# Agent Orchestrator Pipeline

Unified, enterprise-grade orchestration engine coordinating multi-agent software engineering workflows across research, planning, TDD implementation, code review, security audits, and gated commits.

---

## 1. Core Operations Matrix

| Operation | Action Target | Primary Trigger | Initial Move |
|-----------|---------------|-----------------|--------------|
| **Add Feature** | `feature` | New capability requested | Research existing patterns + Plan vertical slices |
| **Fix Defect** | `fix` | Broken or incorrect behavior | Reproduce with failing test (RED) before touching code |
| **Refine Code** | `refactor` | Code cleanup, tech debt reduction | Verify tests green → Restructure behavior-preserving |
| **Change Feature** | `tweak` | Working code requiring new spec | Amend test assertions first → Update implementation |
| **Build MVP** | `mvp` | Bootstrap from PRD/SDD document | Ingest spec → Scaffold first slice → Run iterative loop |

---

## 2. Right-Sizing & Size Classifier

Ceremony scales strictly to the blast radius of the request:

| Tier | Files Touched | Dependencies / Contracts | Design Ambiguity | Active Pipeline Phases |
|------|---------------|--------------------------|------------------|------------------------|
| **Trivial** | 1 file (few lines) | None | Zero (obvious change) | Implement → Review → Commit |
| **Small** | 1 file / 1 function | None | Clear after reading code | (Light Research) → Implement → Review → Commit |
| **Standard** | 2–5 files | Internal module change | One architectural choice | Intake → Research → Plan → Implement → Review → Commit |
| **Large** | >5 files / cross-cutting | External API, DB schema, auth | Multiple architectural choices | Full Pipeline: Intake → Research → Plan → Scaffold → Implement → Review → Commit |

*Rule: Any task touching security controls, public APIs, or database migrations is classified at minimum as **Standard**.*

---

## 3. The 7-Phase Orchestration Pipeline

```
[0. Intake & Understand] ──► [1. Research & Reuse] ──► [2. Plan Slices]
                                                             │
                                                      [GATE 1: User Approval]
                                                             │
[4. TDD Implement] ◄─── [3. Scaffold First Slice (MVP)] ◄────┘
        │
[5. Review & Security Gate] ──► [6. Conventional Commit (GATE 2)]
```

### Phase 0: Intake & Scope Definition
Extract exact requirements, constraints, and off-limits boundaries. For MVP builds, ingest the PRD/SDD and identify the critical path.

### Phase 1: Research & Reuse
Prioritize adoption over reinvention:
1. Search existing codebase utilities and repo patterns (`grep_search` / `gh search code`).
2. Verify library documentation via MCP Context7 or official docs.
3. Check package registries (npm/PyPI/crates.io) for battle-tested solutions.

### Phase 2: Planning & Task Decomposition
Delegate to the `planner` or `architect` subagent to generate an ordered `task.md` of thin vertical slices.
→ **GATE 1: Stop and wait for user confirmation before implementation.**

### Phase 3: Scaffold (MVP only)
Stand up directory structure, environment configs, and the minimal runnable end-to-end slice.

### Phase 4: Test-Driven Implementation (TDD)
Execute each task in the checklist following the strict red-green-refactor cycle:
- **RED**: Write failing unit or integration test.
- **GREEN**: Write minimal code to pass test (Ponytail minimalist ladder).
- **REFACTOR**: Simplify and remove duplication while tests remain green.

### Phase 5: Code Review & Security Audit
- Run `code-reviewer` agent on the git diff for readability, dead code, and maintainability.
- Automatically invoke `security-reviewer` agent if touching: authentication, authorization, raw database queries, user input handling, file system access, or secrets.

### Phase 6: Gated Commit
Format changes into atomic Conventional Commits (`feat:`, `fix:`, `refactor:`, `test:`, `chore:`).
→ **GATE 2: Present diff summary and get user confirmation prior to commit/push.**

---

## 4. Subagent Delegation Map

| Pipeline Phase | Primary Subagent / Tool | Fallback / Escalation |
|----------------|--------------------------|----------------------|
| **Intake / Code Exploration** | `code-explorer` | Trace callers and call graphs |
| **Architectural Planning** | `planner` | `architect` / `code-architect` |
| **TDD Implementation** | `tdd-guide` | `build-error-resolver` on build breaks |
| **Quality Review** | `code-reviewer` | Language-specific reviewer (e.g. `typescript-reviewer`, `python-reviewer`) |
| **Security Review** | `security-reviewer` | OWASP Top 10 checklist scan |

---

## 5. Definition of Done Checklist

- [ ] Sizing tier explicitly classified and announced.
- [ ] Gate 1 (Plan approval) and Gate 2 (Commit approval) strictly observed.
- [ ] Security audit executed on any auth, DB, or boundary changes.
- [ ] 100% of unit/integration tests passing with >= 80% code coverage.
- [ ] Clean conventional commit messages with no unrequested changes.
