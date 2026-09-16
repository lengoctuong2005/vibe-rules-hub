---
trigger: always_on
description: "Silent Failure Hunter - Forces AI to hunt for bugs that don't throw exceptions: off-by-one, fire-and-forget async, implicit type coercion."
---
# Silent Failure Hunter (Thợ săn Lỗi Ngầm)

## Purpose
Find bugs that don't produce errors or exceptions but cause incorrect behavior. Code that "works" is not necessarily code that is "correct".

## Trigger
Load during code review, or when writing state transitions, data parsing, or concurrent logic.

## Hunting Checklist

### 1. Off-by-One Errors
- Array loop boundaries: `< length` vs `<= length`
- Substring operations: start/end index semantics
- Pagination: page 0 vs page 1, offset calculations
- Date ranges: inclusive vs exclusive end dates

### 2. Fire-and-Forget Async
- Promises without `await` or `.catch()` (silently lost errors)
- `forEach` with async callbacks (does not await)
- Event handlers that throw without a listener
- setTimeout/setInterval callbacks with unhandled exceptions

### 3. Implicit Type Coercion
- `==` instead of `===` in JavaScript/TypeScript
- String concatenation instead of numeric addition (`"5" + 3 = "53"`)
- Falsy value traps (`0`, `""`, `null`, `undefined`, `NaN` treated as false)
- JSON.parse on untrusted input without try/catch

### 4. State Mutation
- Object/array passed by reference and modified unexpectedly
- Shared mutable state between concurrent operations
- React/Vue state mutations that don't trigger re-renders
- Cache invalidation gaps (stale data served after update)

### 5. Silent Threat Report
When any of these patterns are detected, include a dedicated section:
```
[SILENT THREATS]
1. Line 42: `items.forEach(async (item) => ...)` - async errors will be silently lost.
2. Line 78: `if (count == 0)` - type coercion risk, use `===`.
```
