---
trigger: load_on_demand
description: "Latent Briefing - Context Compression Strategy. Uses high-level summaries to reduce token usage while retaining core context."
---
# Latent Briefing (Chiến lược Nén ngữ cảnh)

## Purpose
Prevent context overflow and reduce token usage during long sessions or complex projects by utilizing the AI's latent space and targeted RAG retrieval instead of dumping full histories into the context window.

## Trigger
Load when starting a new session on a long-running project, or when context size approaches 75% of the token limit.

## Protocol

### 1. Episodic Summarization (Nén sự kiện)
When a task completes, do not keep the full turn-by-turn history.
Instead, use `scripts/memory_observer.py summarize` to create an "Episodic Brief".
Format:
- **Goal**: What was attempted.
- **Result**: What was achieved (files modified, APIs changed).
- **Lessons**: Technical roadblocks hit and how they were bypassed.

### 2. Semantic Promotion (Hợp nhất khái niệm)
If the same concept, library, or pattern is mentioned across 3+ episodic events, it must be promoted to Semantic Memory.
- Use `scripts/memory_consolidator.py` to move repeating patterns from episodic logs to global `preferences`.
- Once promoted, remove the redundant details from active context.

### 3. The Latent Briefing Pattern (Truyền đạt bằng ý niệm)
When starting a new session, do NOT load previous code files unless explicitly needed for the immediate task.
Load only the **Latent Briefing**:
- The Project Architecture (1 paragraph)
- The Current State (1 paragraph)
- The Active Invariants (1 list)
- The immediate Task (1 sentence)

Trust that the AI's internal reasoning (latent space) and RAG tools (`scripts/rag_memory_engine.py query`) can fetch specific details *only when requested*.

### 4. Context Eviction (Thải hồi chủ động)
- Every 10 turns, perform a mental check: "What information in my context window is no longer relevant to the current bug?"
- Drop references to old files, outdated logs, and resolved issues from future responses.
