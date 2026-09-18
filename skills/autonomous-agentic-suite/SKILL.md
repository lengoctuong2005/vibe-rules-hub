---
name: autonomous-agentic-suite
description: |
  Autonomous Agentic Master Suite establishing distributed multi-agent swarm architecture. Includes Git Worktree physical isolation, append-only event coordination (events.log), SQLite FTS5 persistent memory vault, False Memory Guard protocols, 3-strike circuit breakers, Ponytail 7-rung minimalist engineering, and 33 stealth human identity rules.
triggers:
  - "autonomous-agents"
  - "agentic suite"
  - "autonomous-agentic-suite"
  - "multi agent coordination"
  - "worktree isolation"
  - "memory vault"
  - "ponytail minimalism"
license: MIT
metadata:
  origin: ECC
---

# Autonomous Agentic Master Suite

Production-grade multi-agent operating standard designed for safe, concurrent, and amnesia-free AI agent collaboration.

---

## 1. Multi-Agent Physical Isolation via Git Worktrees

To eliminate Write/Write race conditions and file corruptions, concurrent agents are allocated discrete physical worktree workspaces.

```
project-root/ (main branch)
├── agent_coord/
│   ├── events.log            # Append-only JSONL stream
│   ├── proposals/            # Cross-agent RFCs and plans
│   └── DECISIONS.md          # Single-writer authority log (Orchestrator only)
│
../work-agent-planner/        # Isolated worktree for `planner`
../work-agent-backend/        # Isolated worktree for `architect` & backend impl
../work-agent-frontend/       # Isolated worktree for `react-reviewer` & UI impl
```

### Worktree Lifecycle Operations
```bash
# 1. Spawn isolated workspace for subagent
git worktree add ../work-agent-alpha -b agent/alpha-task

# 2. Subagent executes implementation & tests inside ../work-agent-alpha

# 3. Master Orchestrator merges changes back cleanly
git merge --no-ff agent/alpha-task

# 4. Clean up worktree
git worktree remove ../work-agent-alpha
git branch -d agent/alpha-task
```

---

## 2. Centralized SQLite FTS5 Memory Vault

Memory is retained in SQLite (`~/.claude/memory/vault/antigravity.db`) structured across Episodic, Semantic, and Invariant layers.

```sql
-- SQLite Schema for Antigravity Memory Vault
CREATE TABLE IF NOT EXISTS observations (
    id TEXT PRIMARY KEY,
    project TEXT NOT NULL,
    root_path TEXT NOT NULL,
    type TEXT CHECK(type IN ('bugfix','feature','discovery','refactor','decision','config','test','docs')),
    title TEXT NOT NULL,
    narrative TEXT NOT NULL,
    files_modified TEXT NOT NULL,
    concepts TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE VIRTUAL TABLE IF NOT EXISTS observations_fts USING fts5(
    title,
    narrative,
    concepts,
    content='observations',
    content_rowid='rowid'
);
```

### False Memory Guard Protocol
- Observations start as temporary claims.
- Promotion to permanent user preference requires $\ge 3$ distinct user affirmations or successful task verifications.

---

## 3. The 33 Stealth Human Identity Standards

All generated code comments, PR summaries, commit messages, and documentation must adhere to pragmatic senior engineer standards without AI signatures:

1. **Direct Tone**: Active voice, direct reasoning, zero conversational filler.
2. **Banned Clichés**: Eliminate `testament to`, `evolving landscape`, `vital role`, `deep dive`.
3. **Banned Words**: Eliminate `delve`, `crucial`, `tapestry`, `intricate`, `fostering`, `vibrant`, `pivotal`.
4. **Simple Copulas**: Prefer `is`, `are`, `has` over `boasts`, `features`, `serves as`.
5. **No Present Participle Trails**: Cut empty `-ing` tails (e.g. `..., thus ensuring reliability`).
6. **No Tailing Negations**: Use complete clauses (avoid `...no guesswork`).
7. **No Arbitrary Rule of Three**: Never force concepts into triplets for rhetorical symmetry.
8. **Consistent Naming**: Use the standard domain term consistently without artificial synonym rotation.
9. **Typography**: Replace all em dashes (`—`) with commas, periods, or parentheses. Straight quotes (`""`, `''`) only.
10. **No Mechanical Boldface**: Avoid inline-header bullet lists (`- **Title**: Description`); write fluid paragraphs.

---

## 4. Ponytail 7-Rung Minimalist Solution Ladder

```
Rung 1: Does this need to exist at all? (YAGNI)
   │ (NO) ➔ Delete requirement / return existing.
   ▼ (YES)
Rung 2: Does it already exist in the codebase?
   │ (YES) ➔ Reuse existing helper/service.
   ▼ (NO)
Rung 3: Does the language standard library do this?
   │ (YES) ➔ Use stdlib (e.g., crypto, fetch, URL, structuredClone).
   ▼ (NO)
Rung 4: Does a native platform feature cover it?
   │ (YES) ➔ Use CSS / SQL constraints / OS primitive.
   ▼ (NO)
Rung 5: Does an already-installed dependency solve it?
   │ (YES) ➔ Use installed package; never install a new library for small logic.
   ▼ (NO)
Rung 6: Can it be written in one concise line?
   │ (YES) ➔ Ship the one-liner.
   ▼ (NO)
Rung 7: Write the minimal code that works. Mark with:
        // ponytail: <ceiling>, <upgrade path>
```

---

## 5. Subagent Prompt Injection Header

When orchestrating subagents, prepend the mandatory minimalist directive:

```markdown
[PONYTAIL MINIMALIST DIRECTIVE: Apply 7-rung solution ladder. YAGNI extremist. Deletion before addition. Native/stdlib first. Mark simplifications with '// ponytail:'. No unrequested abstractions. Strictly adhere to 33 human identity rules (no em dashes, no AI fluff).]
```
