# Model Context Protocol (MCP) Configuration Hub

Danh mục cấu hình máy chủ MCP đã kiểm định cho Claude Code CLI, Cursor IDE, Windsurf và Gemini CLI.

## 1. Sử dụng với Claude Code CLI
Thêm trực tiếp từng server qua lệnh:
```bash
claude mcp add openreview -- uvx --with "mcp<2" openreview-mcp
claude mcp add context7 -- npx -y @upstash/context7-mcp
claude mcp add filesystem -- npx -y @modelcontextprotocol/server-filesystem .
```

Hoặc dán cấu hình từ `mcp_all_servers.json` vào file `~/.claude.json`.
