---
trigger: always_on
description: "Anti-Fatigue - Detects context decay in long conversations. Triggers state reset and recommends fresh chat sessions."
---
# Anti-Fatigue (Quy tắc chống suy thoái ngữ cảnh)

## Purpose
Detect and mitigate context decay that occurs in long conversation sessions. Force the AI to reset its working memory when quality degrades.

## Context Decay Indicators
The following patterns signal that the AI is losing coherence:
1. User has to repeat a requirement for the second time.
2. AI fixes the wrong location or introduces a bug that was already fixed.
3. AI contradicts its own earlier analysis within the same session.
4. AI forgets constraints or scope boundaries stated earlier.
5. Consecutive fix attempts fail (overlaps with anti-loop.md, but here the cause is fatigue not logic).

## Protocol

### 1. Self-Detection
When any 2 of the indicators above are detected within a 5-turn window:
- Tag: `[CONTEXT DECAY DETECTED]`
- Pause code output.

### 2. State Reset ("Face Wash")
Perform a structured reset:
1. Re-read the relevant source files via `view_file` (trust files, not chat memory).
2. Summarize the current state: what has been done, what remains, what the goal is.
3. Present this summary to the User for confirmation.

### 3. Fresh Session Recommendation
If the conversation exceeds 20 turns on a single complex task:
- Suggest saving progress via `memory_observer.py observe` and starting a new chat session.
- Provide a handoff summary the User can paste into the new session.

### 4. Trust Hierarchy
During long sessions, the AI must follow this trust order:
1. Physical files on disk (read via tools) - highest trust
2. Recent tool outputs (last 3-5 turns)
3. Earlier conversation context - lowest trust

NEVER rely on chat memory for file contents when the conversation exceeds 10 turns. Always re-read the file.
