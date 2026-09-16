---
trigger: always_on
description: "YAGNI & Defensive Programming - Enforces KISS/YAGNI principles and mandatory error handling for all I/O operations."
---
# YAGNI & Defensive Programming (Kiến trúc tối giản & lập trình phòng thủ)

## Purpose
Prevent over-engineering and improve code reliability through mandatory defensive patterns.

## Part 1: YAGNI (You Ain't Gonna Need It)

### Simplicity Rules
- Write the simplest solution that satisfies the requirement. No extra abstractions.
- Do not introduce Design Patterns (Factory, Strategy, Observer) for fewer than 3 concrete implementations.
- Do not create abstraction layers for single-use code paths.
- Prefer flat structures over deep nesting. Prefer functions over classes when state is not needed.

### Anti-Over-Engineering Signals
Flag and push back when the solution exhibits:
- More than 2 levels of class inheritance for a simple feature
- Configuration files for behavior that could be a constant
- Generic frameworks for single-use logic
- Premature optimization without measured bottleneck evidence

## Part 2: Defensive Programming

### Mandatory Error Handling
All I/O operations MUST have explicit error handling:
- File operations: try/catch with specific error types (FileNotFound, PermissionError)
- Network requests: try/catch with timeout configuration
- Database queries: try/catch with connection error handling
- JSON/XML parsing: try/catch with malformed data handling

### Forbidden Patterns
- `except Exception: pass` or `catch(e) {}` (silent swallowing)
- Network calls without timeout
- File reads without existence checks
- Array/list access without bounds or emptiness checks
- String-to-number conversion without validation

### Mandatory Null/Empty Guards
- Check for null/undefined/None before property access on external data.
- Provide fallback values for potentially empty arrays and objects.
- Validate function parameters at entry point for public APIs.
