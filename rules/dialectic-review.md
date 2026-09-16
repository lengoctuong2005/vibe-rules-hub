# Đối Kháng & Tự Kiểm Duyệt (Dialectic Review)

**Mô tả**: Agent không lập tức báo cáo "Xong" (Done) sau khi hoàn tất sửa code. Thay vào đó, Agent sẽ tự Spawn (tạo bản sao tư duy) đóng vai "Reviewer Khó Tính" để đập đi xây lại hoặc vạch lá tìm sâu chính giải pháp của mình.

## Quy trình Đối Kháng:

### Phase 1: Tạo tác & Tự Mãn
1. Agent (Dev) hoàn tất logic hoặc tính năng. Sinh ra mã nguồn và tự thấy hài lòng.
2. Không in mã nguồn ra ngay. Chuyển sang Phase 2.

### Phase 2: Cỗ máy Hủy diệt (The Destroyer)
1. Agent tạm thời khoác áo "Kỹ sư bảo mật/Kiến trúc sư cực đoan".
2. Bắt đầu rà soát lại đoạn code vừa sinh với 3 câu hỏi tàn nhẫn:
   - **Performance**: Đoạn code này chạy O(N^2) hay O(N)? Có rò rỉ bộ nhớ (memory leak) nếu chạy 1 triệu vòng lặp không?
   - **Security**: Nó có dính SQL Injection, XSS, hay đọc dữ liệu nhạy cảm không? Đầu vào (input) đã được validate 100% chưa?
   - **Over-engineering**: Có phải đoạn code này quá phức tạp? Liệu có thư viện có sẵn (native lib) làm được việc này bằng 1 dòng không?

### Phase 3: Hòa giải (Synthesis)
1. Nếu phát hiện lỗ hổng: Agent (Dev) tiến hành vá lỗi, viết lại code đơn giản hơn. Lặp lại quá trình Review.
2. Nếu không tìm thấy lỗi lớn: Tổng hợp thành bản vá cuối cùng. Đính kèm một dòng (hoặc log) chỉ rõ: `[Dialectic Check Passed: Đã kiểm tra qua 3 lăng kính Perf/Sec/YAGNI]`. Báo cáo kết quả.