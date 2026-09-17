# Agent Personas Codex (`.agent`)

Danh mục cấu hình phân vai Subagents chuyên trách (67+ roles) được chuẩn hoá cho Claude Code CLI, Gemini CLI, Cursor IDE, Windsurf và các mô hình AI Agentic.

## Danh mục Subagents tiêu biểu

- **Kiến trúc & Lập kế hoạch**: `architect.md`, `planner.md`, `code-architect.md`, `homelab-architect.md`, `network-architect.md`
- **Đánh giá mã nguồn (Code Review)**: `code-reviewer.md`, `security-reviewer.md`, `typescript-reviewer.md`, `python-reviewer.md`, `go-reviewer.md`, `rust-reviewer.md`, `cpp-reviewer.md`, `csharp-reviewer.md`, `java-reviewer.md`, `dart-build-resolver.md`
- **Sửa lỗi Build & Biên dịch**: `build-error-resolver.md`, `react-build-resolver.md`, `django-build-resolver.md`, `kotlin-build-resolver.md`, `swift-build-resolver.md`
- **Kiểm thử & QA**: `tdd-guide.md`, `e2e-runner.md`, `pr-test-analyzer.md`, `silent-failure-hunter.md`, `agent-evaluator.md`
- **Tối ưu & Tinh gọn**: `code-simplifier.md`, `refactor-cleaner.md`, `performance-optimizer.md`, `harness-optimizer.md`
- **Chuyên biệt lĩnh vực**: `database-reviewer.md`, `seo-specialist.md`, `marketing-agent.md`, `harmonyos-app-resolver.md`, `healthcare-reviewer.md`

## Cách sử dụng

Đặt thư mục `.agent/` hoặc các file spec vào thư mục cấu hình của agentic tool:
- **Claude Code CLI**: `~/.claude/agents/` hoặc `.claude/agents/` trong dự án.
- **Gemini CLI**: `~/.gemini/agents/` hoặc `.gemini/agents/` trong dự án.
- **Cursor / Windsurf**: Tích hợp trực tiếp vào system prompts hoặc agent configs.
