---
trigger: always_on
description: "Tool Economy - Minimizes tool call count through batching, targeted searches, and retry limits. Prevents tool spam."
---
# Tool Economy (Kinh tế học công cụ)

## Purpose
Minimize the number of tool calls per task. Batch operations, think before searching, and avoid repetitive failed calls.

## Rules

### 1. Batch Execution
- Combine multiple independent tool calls into a single turn (parallel execution).
- When reading multiple files, assess which ones are actually needed before reading all of them.
- When searching, use specific directory paths and file patterns instead of searching the entire workspace.

### 2. Sniper Mode (Think Before Searching)
Before running `grep_search` or `list_dir`:
1. Identify the most likely directory based on project structure.
2. Use specific file patterns (e.g., `*.py`, `*.ts`) to narrow results.
3. Formulate a precise search query rather than broad patterns.

BAD: `grep_search("error", "/")` (searches entire workspace)
GOOD: `grep_search("handleAuthError", "/src/auth/", Includes=["*.ts"])` (targeted)

### 3. Retry Limits
- A tool call that fails: retry at most 2 times with modified parameters.
- After 2 retries, switch strategy (different tool, different approach, or ask User).
- NEVER retry the exact same call with the exact same parameters.

### 4. Read-Once Principle
- After reading a file section, extract all needed information in one pass.
- Do not re-read the same file section unless the file has been modified since the last read.
- Cache key information (function signatures, import lists) in working memory.

### 5. Tool Selection Priority
For information gathering:
1. `grep_search` (fastest for known patterns)
2. `list_dir` (for structure discovery)
3. `view_file` with line range (for targeted reading)
4. Full file read (last resort, only for small files)
