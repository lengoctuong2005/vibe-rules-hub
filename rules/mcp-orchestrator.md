# Workflow: MCP Master Orchestrator

Load when: The user requests to use, check, or execute tasks involving Model Context Protocol (MCP) integrations. This is the root router for all MCP capabilities.

## Introduction
The system is equipped with over 60 MCP servers covering various domains. Before executing a task, identify the domain and load the corresponding sub-router to see the available MCP tools and usage guidelines.

## Sub-Routers by Domain
Check the following sub-routers located in `.gemini/.agents/rules/mcp-routers/`:

1. **System, Hardware & Network** -> Load `mcp-routers/mcp-system-hardware.md`
   - Use for: Local files, Everything search, Docker, Serial/COM, MQTT, Cisco Packet Tracer, VirusTotal, Crypto, SSH, DNS.

2. **Coding & Database** -> Load `mcp-routers/mcp-coding-database.md`
   - Use for: Git/GitHub, gh_grep, codegraph, SQLite, Excel SQL, LeetCode, StackOverflow, sequential-thinking, Jupyter, OpenAPI, Redis, Verilog, MySQL.

3. **Browser & Web Scraper** -> Load `mcp-routers/mcp-browser-web.md`
   - Use for: Puppeteer, Playwright, Tavily, smart-web, fetch, jina-reader, firecrawl, lighthouse.

4. **Docs, Diagrams & Academic** -> Load `mcp-routers/mcp-docs-academic.md`
   - Use for: PDF reading/export, Pandoc, Kroki, Excalidraw, Wolfram, arXiv, context7, math-mcp, Figma, Markdown conversion.

5. **Productivity & Task Management** -> Load `mcp-routers/mcp-productivity-task.md`
   - Use for: Notion, Linear, Calendar, Google Drive/Sheets, Anki, Maps, Trello, Todoist, Airtable.

6. **Media, Social & Utils** -> Load `mcp-routers/mcp-media-social.md`
   - Use for: Youtube transcript, FFmpeg, Echarts, Spotify, Telegram, Discord, Slack, RSS, Dev.to, Gmail, HackerNews.

7. **AI & Translation** -> Load `mcp-routers/mcp-ai-translation.md`
   - Use for: Mem0, Memory, Ollama, DeepL.

## Integration Guidelines
- When the user asks you to "use an MCP" or perform a task that falls under these domains, you **MUST** read the corresponding sub-router to know the exact tool names and prerequisites (e.g., API keys, auth tokens).
- Note that local MCPs generally do not require API keys, whereas cloud-based services do.
- Check the `mcp.json` or `opencode.json` configuration if a specific tool appears to be unresponsive.
