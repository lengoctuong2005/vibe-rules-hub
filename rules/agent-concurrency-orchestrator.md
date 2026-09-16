# Điều phối Đa Đặc Vụ (Agent Concurrency Orchestrator)

*   **Mục đích**: Quản lý an toàn trạng thái, ngăn ngừa xung đột bộ nhớ và deadlock khi có nhiều Subagent chạy song song trên cùng một kho lưu trữ.
*   **Trigger**: Kích hoạt khi quy trình làm việc (Workflow) yêu cầu sử dụng nhiều hơn 1 Subagent hoặc khi thực hiện Smart Refactoring quy mô lớn (Spawn Subagents).

## Nội dung cốt lõi

1. **Isolation First (Cô lập trước tiên):**
   * 100% Subagent thao tác lên mã nguồn phải chạy trong một Git Worktree độc lập được tạo bởi `scripts/worktree_manager.py`.
   * Cấm các Subagent cùng lúc truy cập chung vào nhánh (branch) chính hoặc `.git` directory để sửa đổi (trừ khi read-only).

2. **Phòng tránh Deadlock (Khóa tài nguyên 2 pha):**
   * Bất kì Subagent nào cần đọc/ghi cấu hình chung (`preferences.md`, `.env` test) đều phải xin phép thông qua `scripts/lock_manager.py`.
   * Timeout mặc định khi chờ khóa (wait lock) không được phép vượt quá 30 giây.
   * Nếu không xin được khóa, Subagent bắt buộc phải Hủy bỏ tiến trình (Abort), dọn dẹp biến, và chờ đợi ngẫu nhiên (Backoff) thay vì giữ khóa cũ và xin khóa mới.

3. **Đồng bộ hóa kết quả (Synchronization & Merge):**
   * Master Agent chịu trách nhiệm tổng hợp file Output/Log từ tất cả các Subagents.
   * Quá trình hợp nhất Git (git merge) từ các Worktrees về branch chính phải được chạy qua `worktree_manager.py` với cấu hình `--no-ff` (No Fast-Forward). 
   * Nếu có conflict, hệ thống sẽ tự động `merge --abort` và Master Agent sẽ đọc xung đột đó để giải quyết tuần tự bằng tay, không được để lửng Git ở trạng thái Đang Merge.