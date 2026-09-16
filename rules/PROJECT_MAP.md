---
trigger: model_decision
description: "PROJECT MAP (ROUTER INDEX) - | Task Type | Persona to Load | Workflow to Load | Project Rules to Load |"
---
# PROJECT MAP (ROUTER INDEX)

*This is the entry point for the Project. Agent MUST read this first to route to the correct Persona, Workflow, and Local Rules via Progressive Loading.*

## 1. PROJECT OVERVIEW
- **Stack:** [e.g., Next.js 15, NestJS, Postgres, pnpm]
- **Architecture:** [e.g., Modular Monolith]

## 2. TASK ROUTING TABLE
*Agent uses this table to load Need-to-Know context based on the task type.*

| Task Type | Persona to Load | Workflow to Load | Project Rules to Load |
|---|---|---|---|
| **Frontend/UI** | `personas/ui-expert.md` | `workflows/ui-design.md` | `.rules/ui-ux.md` |
| **Backend/API** | `personas/backend-dev.md` | `workflows/api-design.md` | `.rules/api-design.md` |
| **Bug/Fix** | `personas/debugger.md` | `workflows/debug.md` | `.rules/testing.md` |
| **Architecture** | `personas/architect.md` | `workflows/arch-review.md` | `.rules/coding-style.md` |
| **Security** | `personas/sec-reviewer.md` | `workflows/audit.md` | `.rules/security.md` |

## 3. KNOWLEDGE & INVARIANTS POINTERS
*Only load specific files from these directories when explicitly modifying their domains.*
- **System Laws:** `INVARIANTS.md`
- **Decisions (ADR):** `docs/adr/ADR_INDEX.md`
- **Specs/PRD:** `docs/` (Use search/grep, do NOT load entire PDFs/Docs)
- **Known Failures:** `docs/quality/FAILURE_INDEX.md`

## 4. CURRENT STATE
- **Active Task:** [None]
- **Stability:** [e.g., Stable / Refactoring]

