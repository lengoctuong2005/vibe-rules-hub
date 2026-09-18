---
trigger: always_on
description: "Tool Discipline & Economy: Enforces tool reuse, sniper search mode, batch execution, retry limits, IDE tool mapping table, and surgical code editing rules."
---
# Tool Discipline, Economy & IDE Tool Mapping

## 1. Native & Internal Tool Registry
Maximize reuse of existing project infrastructure. Never write ad-hoc scripts or install unapproved packages when internal tools or native runtime capabilities already exist.

### 1.1 Check Before You Build
1. Search the `scripts/` directory for existing utilities before generating automation commands.
2. Check `RULES_MANIFEST.md` for existing workflows and capabilities.
3. Query indexed codebase skills via `scripts/rag_memory_engine.py`.

### 1.2 Internal Tool Registry
The following internal tools MUST be used instead of rolling custom scripts:

| Domain | Native / Standard Script | Purpose |
|---|---|---|
| **Concurrency & Locks** | `scripts/lock_manager.py` | Two-phase resource locking (avoid ad-hoc file locks) |
| **Git & Worktrees** | `scripts/worktree_manager.py` | Isolated branch worktrees for subagents |
| **Secret Scanning** | `scripts/safety_guard.py`, `scripts/privacy_vault.py` | Pre-commit token & credential detection |
| **Persistent Memory** | `scripts/memory_search.py`, `scripts/memory_observer.py` | SQLite FTS5 search & structured observations |
| **Compliance & Gates** | `scripts/compliance_monitor.py`, `scripts/regression_gate.py` | Automated pre/post edit verification |
| **Cost & Token Tracking** | `scripts/cost_ledger.py` | Token usage monitoring |

### 1.3 New Script Justification & Dependency Gate
- If no internal tool covers the task: state which scripts were evaluated and why they are insufficient. Place new tools in `scripts/` following repo conventions.
- **NEVER** run `npm install`, `pip install`, `cargo add`, or equivalent without explicit user approval. Check `package.json` or `requirements.txt` first.

## 2. Tool Economy & Search Optimization
Minimize tool calls, optimize token usage, and prevent tool spam loops.

### 2.1 Batch Execution
- Combine multiple independent tool calls into a single turn (parallel execution).
- Assess which files are strictly needed before reading.

### 2.2 Sniper Search Mode (Think Before Searching)
Target search operations precisely rather than flooding the workspace:
1. Identify the most probable directory path from project layout.
2. Filter file extensions using specific glob patterns (`Includes=["*.ts"]`, `Includes=["*.py"]`).
3. Formulate precise identifiers or exact symbols rather than broad keywords.
- **Bad:** Broad grep across entire workspace (`grep_search("error", "/")`).
- **Good:** Focused sniper grep (`grep_search("handleAuthError", "src/auth/", Includes=["*.ts"])`).

### 2.3 Retry Limits & Circuit Breakers
- If a tool call fails: retry at most 2 times with modified parameters.
- After 2 failed retries: switch strategy (alternate tool, higher abstraction, or ask user).
- **NEVER** retry the exact same tool invocation with identical parameters.

### 2.4 Read-Once Principle & Line-Bounded Inspection
- Extract required structural information in one pass.
- Do not re-read unchanged files within the same session.
- Never read full files if >300 lines; use line-bounded reads (`offset`/`limit` or `StartLine`/`EndLine` <800 lines) around target functions.
- Tool priority hierarchy: `grep_search` > `list_dir` > line-bounded `view_file`/`Read` > full file read.

## 3. IDE Tool Mapping Table
When any rule, skill, or workflow references legacy tool names, map them to the native IDE environment tools:

| Legacy / General Tool Name | Antigravity Native Tool | Primary Parameters | Best Practice |
|---|---|---|---|
| `read_file`, `view_file` | `view_file` / `Read` | `AbsolutePath`, `StartLine`, `EndLine` | Read bounded sections (<800 lines/call). |
| `write_file`, `create_file` | `write_to_file` / `Write` | `TargetFile`, `CodeContent`, `Overwrite` | Use ONLY when creating completely new files. |
| `edit_file`, `replace_string` | `replace_file_content` / `Edit` | `TargetFile`, `TargetContent`, `ReplacementContent` | **Default for code edits.** Surgical block replacement. |
| `multi_edit_file` | `multi_replace_file_content` | `TargetFile`, `ReplacementChunks` | Edit multiple disjoint blocks in one turn. |
| `bash`, `exec`, `shell_command` | `run_command` / `Bash` | `CommandLine`, `Cwd`, `WaitMsBeforeAsync` | Use absolute paths; avoid `cd` in compound commands. |
| `grep`, `search_code` | `grep_search` | `SearchPath`, `Query`, `Includes`, `IsRegex` | Use sniper mode with specific `Includes`. |
| `find_files`, `list_dir` | `list_dir` | `DirectoryPath` | Inspect directory structures hierarchically. |
| `google_search`, `web_search` | `search_web` / `tavily` | `query`, `domain` | Tavily prioritized for internet searches. |
| `fetch_webpage`, `curl` | `read_url_content` / `mcp_fetch_fetch` | `Url` | Fetch remote documentation as markdown. |
| `browser_action` | `browser_subagent` | `Task`, `RecordingName` | Browser automation workflows. |
| `ask_user` | `ask_question` | `questions` | Structured multiple-choice questions for user. |

## 4. Surgical Code Edit Rule
1. **Zero Full Overwrite:** Never use `write_to_file` / `Write` with overwrite on an existing source file to fix isolated lines.
2. **Surgical Precision:** Use `replace_file_content` / `Edit` to target the exact code block.
3. **Preserve Surrounding Context:** Retain existing comments, indentation style, naming conventions, and unrelated logic without modification.
