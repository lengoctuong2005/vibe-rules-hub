# Multi-Agent Coordination Protocol (Kiến trúc 3 lớp)

## Purpose
Ngăn chặn các lỗi đồng bộ, mất context, và xung đột quyết định khi nhiều Agent hoạt động cùng lúc (Multi-Agent) trên cùng một dự án. Áp dụng tư duy hệ thống phân tán (Distributed Systems) vào điều phối LLM Agent.

## Mấu chốt Kiến Trúc (Layered Defense)
Không dùng Bulletin Board (dễ bị ghi đè) hay File Lock (lỗi TOCTOU, lock không atomic). Dùng kiến trúc 3 lớp:

### Lớp 1 — Chống Race Condition bằng Git Worktree (Cách ly vật lý)
- **Tuyệt đối không dùng File Lock.** Agent rất dễ bỏ qua việc check lock, dẫn đến TOCTOU.
- **Mỗi Agent phải hoạt động trên một Git Worktree riêng biệt:**
  ```bash
  git worktree add ../work-agent-a  agent/a-implement
  git worktree add ../work-agent-b  agent/b-review
  ```
- Việc ghi file hoàn toàn độc lập về đường dẫn vật lý. Việc gộp code (merge) được giao cho thuật toán của Git (atomic & robust).

### Lớp 2 — Chống Context Blindness bằng Append-only Event Log
- Tạo thư mục `agent_coord/` trong gốc dự án.
- Sử dụng file `agent_coord/events.log` dưới dạng **Append-only** (JSONL).
- Agent chỉ được phép GHI THÊM (`>>`), KHÔNG BAO GIỜ SỬA dòng cũ.
  ```jsonl
  {"ts":"2026-06-28T10:00:00Z","agent":"A","event":"START","file":"payos.js","approach":"Unicode sanitizer"}
  {"ts":"2026-06-28T10:05:00Z","agent":"B","event":"REVIEW","ref":"a-001","note":"Thiếu case empty string"}
  ```
- **Trước mọi hành động**, Agent phải đọc log này để hiểu đối phương đang làm gì (Single-writer per line).

### Lớp 3 — Chống Decision Conflict bằng Role Split + Orchestrator
- **Luật vàng:** Không bao giờ để 2 Agent ngang hàng tự giải quyết xung đột (tránh infinite loop).
- Phải có một **Orchestrator** (Agent trọng tài hoặc Con người) nắm quyền quyết định cuối cùng.
- Các đề xuất (proposals) của Agent A và B được ghi vào thư mục `agent_coord/proposals/` (vd: `a-001.md`, `b-001.md`).
- **Orchestrator** là người duy nhất (single-writer) có quyền ghi vào `agent_coord/DECISIONS.md`. Luật ghi trong này là tối cao, các Agent con không được cãi.

## Hướng dẫn Vận hành (Dành cho Agent con)
1. **Hoạt động trong khu vực riêng:** Chỉ sửa file trong worktree của bạn. Tuyệt đối không `cd` sang worktree của agent khác.
2. **Khai báo Context:** Sau mỗi bước quan trọng, GHI THÊM (`append`) một dòng JSON vào `events.log`. Không sửa dòng của người khác.
3. **Đề xuất thay vì Tự Quyết (khi có conflict):** Tạo file proposal mới trong `proposals/`. Đánh cờ `NEEDS_ORCHESTRATOR` nếu không thống nhất được với Agent kia.
4. **Không tự merge:** Việc merge các worktree là nhiệm vụ của Orchestrator sau khi đã đưa ra quyết định tại `DECISIONS.md`.
5. **Giữ nguyên Vai trò (Role):** Bạn là Implementer hay Reviewer, hãy tuân thủ suốt vòng đời của task.

## Lựa chọn linh hoạt theo quy mô
- **Task nhỏ (<30p, 1 file):** Chỉ dùng Role Split + `events.log`. Code và review tuần tự (không cần Worktree).
- **Task vừa (nhiều file, làm song song):** Dùng đủ 3 lớp (Worktree + Log + Orchestrator).
- **Task lớn (>2 agent):** Worktree cho từng Agent + Orchestrator Agent chuyên trách quản lý state machine qua `DECISIONS.md`.
