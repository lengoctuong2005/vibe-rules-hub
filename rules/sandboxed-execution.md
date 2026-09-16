# Chạy thử trong hộp cát (Sandboxed Execution)

*   **Mục đích**: Bảo vệ môi trường máy chủ cục bộ khi chạy các lệnh không rõ nguồn gốc, mã độc tiềm ẩn hoặc cài đặt các dependency chưa được quét bảo mật.
*   **Trigger**: Kích hoạt trước khi Agent chạy các shell script lạ, file binary, lệnh `pip install`/`npm install` những package không chuẩn, hoặc code do Subagent sinh ra nhưng độ tự tin thấp (<80%).

## Nội dung cốt lõi

1. **Yêu cầu Sandbox (Sandbox Request):**
   * Bất kì mã nguồn hoặc bash command nào bị gắn cờ "Untrusted" (từ internet, user copy-paste, Subagent lạ) ĐỀU PHẢI chạy thử ở Sandbox.
   * Agent có thể đề xuất tạo Docker container hoặc một temp VM (nếu có công cụ) để thực thi.
   * Format: `[SANDBOX REQUIRED] Đoạn mã/lệnh này có rủi ro. Yêu cầu tạo Sandbox cô lập để chạy thử.`

2. **Cách ly thư mục (Worktree/Chroot Isolation):**
   * Nếu không có sẵn Docker, bắt buộc phải dùng lệnh tạo Git Worktree (`scripts/worktree_manager.py`) kết hợp với thư mục tạm (temp folder) để chạy lệnh.
   * Không được cài đặt (install dependencies) trực tiếp vào root venv (`.venv` của môi trường chính). Phải tạo venv riêng trong thư mục tạm.

3. **Thu thập kết quả an toàn (Telemetry Harvest):**
   * Đánh giá log Output (STDOUT/STDERR) trong lúc chạy thử.
   * Kiểm tra xem mã có thao tác trái phép vào các cổng mạng (ports) lạ hoặc cố đọc ghi vượt ngoài thư mục Sandbox không.
   * Nếu thành công và không có biểu hiện khả nghi, mới được phép apply lệnh đó vào môi trường gốc.
