---
trigger: always_on
description: "Absolute Precision - Enforces strict data type discipline for currency, time, and concurrency. Bans vague naming and ambiguous technical reasoning."
---
# Absolute Precision (Quy tắc chính xác tuyệt đối)

## Purpose
Eliminate ambiguity in technical reasoning and enforce precise data handling for sensitive domains.

## Rules

### 1. Data Type Discipline
- **Currency/Finance**: Use Decimal, BigInt, or integer cents. NEVER use floating point for money.
- **Time/Dates**: Use UTC internally, ISO-8601 format for serialization. Always specify timezone in user-facing displays.
- **Concurrency**: Use explicit Lock, Mutex, or Transaction. NEVER rely on "it probably won't conflict".
- **IDs**: Use UUID or typed IDs. NEVER use auto-increment integers as external identifiers.

### 2. Naming Precision
Banned generic names in production code:
- `data`, `result`, `res`, `info`, `item`, `obj`, `temp`, `val`
- Must include business context: `userProfile`, `orderTotal`, `authToken`, `paymentResult`

Exceptions:
- Loop variables (`i`, `j`, `k`) in small scopes (<5 lines)
- Lambda parameters in obvious contexts (`items.map(x => x.id)`)

### 3. Technical Reasoning Standards
- No vague claims: "this should be faster" → "this reduces time complexity from O(n^2) to O(n log n)"
- No hand-waving: "this might cause issues" → "this causes a race condition when two requests modify the same row within the same transaction window"
- Quantify when possible: latency in ms, memory in MB, throughput in req/s

### 4. Comparison Operators
- JavaScript/TypeScript: use `===` and `!==` exclusively. Never `==` or `!=`.
- Explicit type conversion before comparison when types may differ.
