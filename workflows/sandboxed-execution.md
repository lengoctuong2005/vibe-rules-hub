# Luồng Chạy Thử An Toàn (Sandboxed Execution)

**Mô tả**: Khi Agent cần chạy một lệnh lạ, file nhị phân, cài đặt gói không xác định (npm/pip) hoặc chạy script shell phức tạp, quy trình này bắt buộc Agent phải khởi tạo môi trường cô lập để đánh giá rủi ro trước khi thực thi vào hệ thống thật.

## Các bước triển khai (Phase 1 -> 3)

### Phase 1: Tạo môi trường cô lập
1. **Kiểm tra công cụ tạo Sandbox**: 
   - Nếu Docker khả dụng, tạo file `Dockerfile.sandbox` nhẹ (ví dụ: `ubuntu:22.04` hoặc `node:18-alpine` tùy thuộc vào runtime yêu cầu).
   - Nếu không có Docker, sử dụng `scripts/worktree_manager.py` tạo một thư mục git worktree ẩn (vd: `.agents/sandbox-worktree`).
2. **Setup Venv**: Không được kế thừa global package. Nếu chạy lệnh Python, hãy lệnh cho Bash tự động thiết lập một `.venv-sandbox` tách biệt bên trong môi trường cô lập.

### Phase 2: Thực thi giới hạn
1. Đẩy lệnh cần thực thi vào bên trong Sandbox.
2. Thêm command timeout (vd: `timeout 30s npm install ...` hoặc `timeout 60s python script.py`) để ngăn chặn infinite loop.
3. Chặn các output thừa, chỉ thu thập STDOUT/STDERR và log lại vào một file `sandbox-output.log`.

### Phase 3: Đánh giá & Ráp nối (Harvesting)
1. Quét nội dung `sandbox-output.log`. Tìm kiếm các dấu hiệu bất thường:
   - Request mạng lạ, cố đọc ghi ngoài thư mục cho phép (với file monitor nếu có).
   - Lỗi quyền (Permission Denied).
2. Nếu an toàn (Exit code 0, không có log phá hoại), xóa Sandbox và thực hiện lệnh trực tiếp lên thư mục chính. 
3. Nếu có dấu hiệu độc hại hoặc cảnh báo hệ thống, thông báo ngay cho User và **KHÔNG** chạy lệnh đó.
