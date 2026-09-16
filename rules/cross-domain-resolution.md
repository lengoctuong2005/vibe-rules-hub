---
trigger: load_on_demand
description: "Cross-Domain Resolution - Handles Frontend/Backend change conflicts. Lock and verify Backend data schema before updating UI."
---
# Cross-Domain Resolution (Giải quyết xung đột liên miền)

## Purpose
Prevent cascading failures when changes span both Frontend and Backend layers.

## Trigger
Load when a task requires modifying both API endpoints/schemas and UI components.

## Protocol

### 1. Dependency Direction
Changes flow in this order: Database -> Backend API -> Frontend UI.
Never modify UI to accommodate a schema change that hasn't been committed to the backend.

### 2. Schema Lock
Before modifying Frontend code that depends on an API response:
1. Verify the current API response shape (via docs, types, or actual request).
2. If the Backend schema is also changing, complete and test Backend changes first.
3. Only then update Frontend types and components.

### 3. Contract Verification
- If TypeScript: shared types or API contracts must be updated in a single commit or PR.
- If REST: verify the API endpoint returns the expected shape before wiring UI.
- If GraphQL: update schema, run codegen, then update components.

### 4. Conflict Detection
When modifying files in both layers simultaneously:
- List all shared data structures (DTOs, API types, DB models).
- Verify field names, types, and nullability match across layers.
- Flag any discrepancy as `[CROSS-DOMAIN CONFLICT]`.
