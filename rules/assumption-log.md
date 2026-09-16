---
trigger: load_on_demand
description: "Assumption Log - Forces AI to make all implicit assumptions explicit and seek User confirmation before deep implementation."
---
# Assumption Log (Sổ tay ghi chú giả định)

## Purpose
Make all implicit assumptions visible to the User. Prevent misaligned implementations caused by unverified assumptions.

## Trigger
Load when designing logic, resolving edge cases, or handling unclear requirements.

## Protocol

### 1. Assumption Detection
Identify gaps in the provided requirements:
- Missing input validation rules (min/max values, allowed characters)
- Unspecified database schema details (column types, constraints, indexes)
- Unclear business logic (what happens on edge cases, concurrent access)
- Assumed environment (OS, runtime version, available memory)
- Assumed user behavior (expected input format, usage patterns)

### 2. The Assumption Ledger
When making any assumption, declare it explicitly in the response:
```
[ASSUMPTIONS MADE]
1. Database uses PostgreSQL (not specified, assumed from existing config).
2. User IDs are UUIDs (inferred from the User model).
3. Max file upload size is 10MB (industry default, not specified).
```

### 3. Confirmation Request
For assumptions that affect architecture or data integrity:
- Ask the User directly before proceeding.
- For trivial assumptions (naming conventions, log format): state and proceed.
- For critical assumptions (auth flow, payment logic, data retention): STOP and ask.

### 4. Assumption Tracking
- If a previously stated assumption is later contradicted by new information, update the ledger and adjust the implementation.
- Tag: `[ASSUMPTION REVISED] #N was incorrect. Updating approach.`
