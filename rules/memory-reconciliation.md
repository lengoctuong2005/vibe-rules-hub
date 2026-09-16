# Giao thức hòa giải bộ nhớ (Memory Reconciliation)

*   **Mục đích**: Quy trình tự động quét định kỳ các tệp memory để tìm kiếm và loại bỏ các mâu thuẫn logic, gộp các bài học trùng lặp, giải quyết tranh chấp thông tin dựa trên ý kiến của User.
*   **Trigger**: Kích hoạt khi có mâu thuẫn chỉ thị rõ ràng trong quá trình lập luận (ví dụ Agent tìm thấy 2 luồng yêu cầu trái ngược về phiên bản Python hoặc quy chuẩn đặt tên hàm).

## Nội dung cốt lõi

1. **Nhận diện Mâu thuẫn (Contradiction Detection):**
   * Nếu đọc từ `preferences.md` hoặc SQLite RAG phát hiện thấy 2 chỉ thị trái ngược (vd: "Luôn dùng Python 3.10" vs "Dự án này bắt buộc dùng Python 3.12").
   * Dừng lại và KHÔNG đưa ra quyết định tự động.

2. **Dọn dẹp Bộ nhớ Ngắn hạn -> Dài hạn (Episodic-to-Semantic):**
   * Định kỳ gộp các ghi chú đơn lẻ, lắt nhắt từ `session-state.md` hoặc logs vào `layer4_lessons_learned.md` (Tri thức dài hạn).
   * Trong quá trình gộp, ưu tiên thông tin mới nhất có timestamps hoặc ngữ cảnh ghi nhận cụ thể hơn.

3. **Giao thức Trình diễn (Presentation Protocol):**
   * Khi phát hiện thông tin mâu thuẫn, trình bày cho người dùng theo format:
     `[MEMORY CONFLICT] Tìm thấy 2 cấu hình trái ngược trong bộ nhớ:`
     ` - A: [Thông tin 1]`
     ` - B: [Thông tin 2]`
   * Đặt câu hỏi mở để người dùng xác nhận lại phiên bản đúng.
   * Xóa vĩnh viễn cấu hình sai khỏi bộ nhớ, hoặc cập nhật Causal Graph / Rules để ghi nhận trường hợp ngoại lệ.