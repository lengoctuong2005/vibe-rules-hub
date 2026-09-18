---
trigger: model_decision
description: "Workflow: Fullstack Web Suite - End-to-end fullstack web orchestration combining React 19, Next.js, Tailwind v4, Node/Bun/Go/Python backends, Postgres/Redis data layer, OWASP Top 10 security, and automated multi-agent quality gates."
tags:
  - fullstack
  - nextjs
  - react19
  - tailwindcss
  - backend
  - postgres
  - redis
  - security
  - subagents
---

# Fullstack Web Master Suite Workflow

**MANDATE**: Deliver high-performance, accessible, and secure fullstack web applications by unifying modern frontend mechanics, resilient backend systems, defense-in-depth security, and autonomous subagent delegation.

---

## 1. Multi-Agent Delegation Pipeline

```mermaid
graph TD
    User([User Requirement]) --> Planner[planner: Task Decomposition & Vertical Slices]
    Planner --> Architect[architect: System Contracts, DB Schema & API Spec]
    Architect --> TDD[tdd-guide: Red-Green-Refactor Testing Harness]
    TDD --> Implementer[Implementation: FE/BE Slices with Ponytail Minimalist Code]
    Implementer --> ReactReviewer[react-reviewer: Component Hygiene, Hooks & React 19 Server Actions]
    Implementer --> SecReviewer[security-reviewer: OWASP Top 10, Auth, CSRF/XSS, Secret Scans]
    SecReviewer --> E2ERunner[e2e-runner: Playwright / Core Web Vitals / A11y Gate]
    E2ERunner --> Ship([Gated Commit & Production Verification])
```

| Phase | Assigned Subagent | Primary Gate | Artifact Generated |
|-------|-------------------|--------------|---------------------|
| **1. Inception & Slicing** | `planner` | Vertical slice breakdown, zero over-abstraction | `task_list.md`, slice contracts |
| **2. Architecture & Data** | `architect` | Schema normalization, API typed contract | DTO definitions, Prisma/SQL schemas |
| **3. Test Harness** | `tdd-guide` | Red tests written prior to implementation | Unit & Integration test suites |
| **4. Component & UI Review** | `react-reviewer` | React 19 hygiene, Tailwind v4 tokens, a11y | Component audit report |
| **5. Security Audit** | `security-reviewer` | OWASP Top 10, Cookie flags, Secret scanning | Security sign-off (`safety_guard.py`) |
| **6. Integration Verification** | `e2e-runner` | Core Web Vitals, Playwright smoke tests | E2E test results & CWV report |

---

## 2. Step-by-Step Execution Lifecycle

### Step 1: Inception & Domain Contract Planning
1. **Vertical Slicing**: Decompose requirements into end-to-end vertical slices (DB migration → Service → API Endpoint → Client Component).
2. **Contract-First API Design**: Define TypeScript DTOs / Zod schemas shared between frontend and backend.
3. **Ponytail Verification**: Apply 7-rung solution ladder before introducing any external dependency or abstraction.

### Step 2: Backend Architecture & Data Layer
1. **Database Engine**: Configure PostgreSQL with connection pooling (`pgbouncer` or native pooler) and Prisma / Kysely ORM.
2. **Caching & Ephemeral State**: Implement Redis for session caching, rate-limiting counters, and idempotent background jobs.
3. **Resilient Endpoints**:
   - Wrap mutations in database transactions with isolation level guards.
   - Enforce structured error payloads: `{ success: false, error: { code, message, details } }`.

```typescript
// ponytail: Native Error Handler - single catch boundary, upgrade to custom registry when multi-service
export async function handleApiRoute(handler: () => Promise<Response>): Promise<Response> {
  try {
    return await handler();
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Internal Server Error';
    return Response.json({ success: false, error: { code: 'INTERNAL_ERROR', message } }, { status: 500 });
  }
}
```

### Step 3: Frontend Presentation & React 19 Primitives
1. **Server vs Client Boundary**:
   - Default to Server Components (`RSC`) for data-fetching and static layout trees.
   - Use Client Components (`"use client"`) strictly at leaf interaction boundaries.
2. **React 19 Actions & Optimistic State**:
   - Utilize `useActionState`, `useFormStatus`, and `useOptimistic` for seamless form mutations.
3. **Styling & Motion**:
   - Use Tailwind CSS v4 CSS variables for theme tokens (`oklch` color spaces).
   - Use GSAP with ScrollTrigger for compositor-friendly animations (`transform`, `opacity`).
4. **Accessibility (WCAG 2.2 AA/AAA)**:
   - Ensure color contrast ratios $\ge 4.5:1$ (normal text) and $\ge 3:1$ (large text/UI elements).
   - Ensure full keyboard accessibility with visible focus rings (`focus-visible:ring-2`).

### Step 4: Defense-in-Depth Security Verification
1. **Authentication & Session Cookies**:
   - Secure cookies configured with `HttpOnly; Secure; SameSite=Strict; Path=/`.
2. **XSS & Injection Defense**:
   - Sanitize all external and user-supplied HTML via vetted parser.
   - Parameterize all database SQL queries — zero string interpolation.
3. **Secret Scan Gate**:
   - Execute `python scripts/safety_guard.py --scan-file .` prior to any git commit.

### Step 5: Autonomous Review & E2E Validation
1. Dispatch `react-reviewer` to audit hook dependencies, memoization, and layout shift risks.
2. Dispatch `security-reviewer` to verify authorization checks on every Server Action and API endpoint.
3. Run `e2e-runner` using Playwright to execute headless browser flows.
4. Verify Core Web Vitals:
   - **LCP** (Largest Contentful Paint) $< 2.5\text{s}$
   - **INP** (Interaction to Next Paint) $< 200\text{ms}$
   - **CLS** (Cumulative Layout Shift) $< 0.1$

---

## 3. Definition of Done (DoD) Checklist

- [ ] All API contracts typed and validated via Zod / native schemas at trust boundaries.
- [ ] React 19 Server Components utilized without unnecessary `"use client"` directives.
- [ ] Database queries parameterized with connection pooling active.
- [ ] Redis caching applied to high-read endpoints with cache invalidation keys defined.
- [ ] Security audit passed (CSRF tokens on mutating routes, SameSite cookies, XSS sanitization).
- [ ] `python scripts/safety_guard.py --scan-file .` executed clean with 0 secret leaks.
- [ ] Core Web Vitals green on Lighthouse / Playwright synthetic run.
- [ ] Subagent review signs-off complete (`planner`, `architect`, `tdd-guide`, `security-reviewer`).
