---
trigger: always_on
description: "Back to Basics - Silent pre-output checklist. AI must mentally verify syntax, imports, null safety, and constraint compliance before outputting code."
---
# Back to Basics (Quy tắc về lại cơ bản)

## Purpose
Prevent trivial errors by enforcing a silent mental checklist before outputting any code block.

## The 4 Stupid Questions
Before printing ANY code block, silently verify:

### 1. Syntax Check
- Are all brackets, parentheses, and braces properly closed?
- Is indentation consistent (no mixed tabs/spaces)?
- Are all strings properly quoted and terminated?
- Are template literals using the correct syntax for the language?

### 2. Dependency Check
- Are all imports/requires present at the top of the file?
- Are imported names spelled correctly and matching the actual export?
- Is the import path correct (relative vs absolute, file extension)?
- Are there any circular import risks?

### 3. Null Safety Check
- Can any variable be null/undefined at the point of use?
- Are array accesses guarded against empty arrays?
- Are object property accesses guarded against missing keys?
- Are function return values checked before use?

### 4. Constraint Compliance Check
- Does this code violate any User preference or project convention?
- Does this code match the existing code style of the target file?
- Does this code introduce any dependency not approved by the User?
- Does this code touch any file or module outside the stated scope?

## Enforcement
This checklist is SILENT (internal reasoning only). Do not print the checklist in the response.
If any check fails, fix the issue before outputting the code. Do not output code with known issues and "fix it later".
