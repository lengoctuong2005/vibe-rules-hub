---
trigger: always_on
description: "Legacy Respect - Preserves existing code style and limits blast radius when modifying old codebases. Chameleon rule: match the file's conventions."
---
# Legacy Respect (Quy tắc tôn trọng mã nguồn cũ)

## Purpose
When modifying existing code, match the file's conventions and limit the scope of changes to the minimum required.

## Trigger
Load when modifying existing codebases, fixing bugs in old files, or adding features to established code.

## Rules

### 1. Chameleon Rule
Match the target file's style 100%, even if it differs from personal preference:
- Naming convention (camelCase vs snake_case vs PascalCase): follow the file.
- Indentation (tabs vs spaces, 2 vs 4): follow the file.
- Quote style (single vs double): follow the file.
- Semicolons (present vs absent in JS/TS): follow the file.
- Comment style (inline vs block, language): follow the file.

### 2. Minimal Blast Radius
- Edit ONLY the function or block that the task requires.
- Do NOT refactor surrounding code unless the User explicitly requests it.
- Do NOT rename variables, reorder imports, or restructure logic outside the target area.
- Do NOT convert callback patterns to async/await or vice versa outside the target function.

### 3. Zombie Code Preservation
- Do NOT delete commented-out code in existing files unless the User explicitly asks.
- Do NOT remove feature flags, debug blocks, or conditional compilation markers.
- These may exist for historical or operational reasons that are not visible in the current context.

### 4. Test Continuity
- If the existing code has tests, run them after modifications to ensure nothing breaks.
- Match the test style (test framework, assertion library, naming) of existing tests.
- Do NOT migrate test frameworks as a side effect of a bug fix.
