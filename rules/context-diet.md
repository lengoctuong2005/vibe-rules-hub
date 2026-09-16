# Quy tắc ép cân ngữ cảnh (Context Diet)

*   **Mục đích**: Tối ưu hóa số lượng token nạp vào, chống tràn ngữ cảnh (Context Overflow) và giảm ảo giác.
*   **Trigger**: Kích hoạt khi Agent bắt đầu quá trình khám phá mã nguồn mới hoặc phân tích dự án lớn.

## Nội dung cốt lõi

1.  **Nghiêm cấm đọc toàn bộ file nếu kích thước > 300 dòng:**
    *   Agent không được phép dùng `cat` hoặc đọc file toàn bộ mà không kiểm tra độ dài trước đối với các file lớn.
    *   Hãy dùng công cụ để giới hạn số dòng (ví dụ `head`, `tail`, hoặc tham số offset/limit trong Tool Read).

2.  **Quy trình khám phá mã nguồn:**
    *   **Bước 1:** Sử dụng `grep` (Grep tool) hoặc phân tích sơ đồ/kiến trúc để tìm chữ ký hàm/class cần thiết. Khoanh vùng các file có liên quan.
    *   **Bước 2:** Chỉ sử dụng công cụ Read (hoặc `view_file` trong các môi trường khác) với giới hạn dòng (StartLine/EndLine) xung quanh khu vực nghi ngờ (tối đa 50-100 dòng). Tránh nạp những hàm không cần thiết vào context.

3.  **Yêu cầu sinh cấu trúc trước:**
    *   Ưu tiên yêu cầu người dùng sinh cấu trúc `ARCHITECTURE.md` (hoặc tương tự) trước khi tự mò mẫm hệ thống tệp tin lớn.
    *   Có thể dùng `tree` hoặc công cụ tương tự ở mức directory nông trước để có cái nhìn tổng quan.
