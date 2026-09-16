---
trigger: model_decision
description: "Workflow: Search for latest documentation or web/Perplexity"
---

# Command: Internet Search (/search)

**Goal:** Trigger this command to request AI to search for the latest information online instead of relying on outdated knowledge.

**AI Actions upon this command:**
1. Extract user query.
2. If library/framework docs → Use MCP `context7` (`resolve-library-id` → `query-docs`).
3. If general web search → **MANDATORY** use MCP `tavily` (`mcp_tavily-mcp_tavily_search`). Absolutely DO NOT use `search_web` if Tavily is available.
4. If Tavily fails or yields no results → Use `search_web` or Perplexity as fallback.
5. Present information concisely, accompanied by citation links (URLs).

**Fallback Chain:** `context7` → `mcp_tavily-mcp_tavily_search` (Highest Priority) → `search_web` → training data + ⚠️
