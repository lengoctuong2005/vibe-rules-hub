---
trigger: model_decision
description: "Workflow: Backend Orchestrator - Load when implementing backend logic, designing API endpoints, databases, or system architectures."
---

# Workflow: Backend Orchestrator (System Core Router)

**MANDATE**: Build reliable, secure, and scalable systems. Keep business logic decoupled from framework internals.

When executing backend or system architecture tasks, the Agent MUST follow this 4-step workflow:

## Step 1: Establish Patterns & Architecture
- Identify the project design pattern or query the user: *"Which architecture pattern does this project use? (e.g. MVC, Hexagonal, Clean Architecture, Event-Driven...)"*
- Load corresponding pattern skill files from `~/.gemini/antigravity/skills/`:
  - `backend-patterns`
  - `hexagonal-architecture`
  - `event-driven-architecture`

## Step 2: Database & Schema Design
- **Never write raw SQL schemas blindly**. Load the database rules corresponding to the stack:
  - e.g., Load `postgres-patterns`, `prisma-patterns`, or `mysql-patterns`.
  - Enforce normalization standards and construct proper database indexes on foreign keys.

## Step 3: API & Framework Implementation
- Load the correct framework-specific capability guidelines:
  - e.g., `nestjs-patterns`, `django-patterns`, `springboot-patterns`, `fastapi-patterns`, or `laravel-patterns`.
  - Load the `error-handling` skill to standardize status codes and uniform exception handling structures.

## Step 4: Security Audits & Testing
- Prior to committing backend code, load security review skill sets:
  - e.g., `django-security`, `springboot-security`, or the general `security-review`.
  - Design verification scenarios: Load `test-driven-development` or `e2e-testing` guidelines.

---
*Note: Always prefer native ORM features or Query Builders over writing raw SQL, unless explicitly needed for performance tuning.*
