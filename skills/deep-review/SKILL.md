---
name: "Deep Review Pipeline"
description: "A composite skill combining Subagent Analysis and Continuous Verification Loop."
trigger: "/deep_review"
---

# Deep Review Pipeline (Subagent + Verification)

Bạn đang kích hoạt **Deep Review Pipeline**. Dưới đây là các bước BẮT BUỘC bạn (Agent chính) phải thực hiện tuần tự để kết hợp sức mạnh của Subagent và Verification Loop. KHÔNG ĐƯỢC BỎ QUA BƯỚC NÀO.

## Bước 1: Spawn Subagent (Cách ly rủi ro)
Dùng lệnh sau để gọi chuyên gia review độc lập phân tích file mục tiêu:
```bash
python .gemini/agents/spawner.py --agent code_reviewer --task "Deep code review for bugs and anti-patterns" --files <đường_dẫn_file_mục_tiêu>
```
*Lưu ý: Đọc kỹ JSON payload mà subagent trả về (hoặc đọc file `payload_code_reviewer.json` nếu API fallback).*

## Bước 2: Pre-edit Checkpoint (Lưu trạng thái an toàn)
Trước khi bạn áp dụng bất kỳ thay đổi nào dựa trên gợi ý của Subagent, hãy lưu Checkpoint:
```bash
python .gemini/verification/continuous.py pre --name deep_review_cp --target .
```

## Bước 3: Áp dụng Code (Surgical Edit)
Sử dụng công cụ `replace_file_content` hoặc `multi_replace_file_content` để áp dụng các điểm sửa lỗi mà Subagent vừa phát hiện. Tuyệt đối không overwrite cả file.

## Bước 4: Post-edit Verification (Kiểm định tự động)
Kích hoạt Loop kiểm định để chạy test:
```bash
python .gemini/verification/continuous.py post --name deep_review_cp --target .
```
- Nếu output trả về **[VERIFY-PASS]**: Báo cáo kết quả thành công cho User.
- Nếu output trả về **[VERIFY-FAIL]**: Hệ thống đã tự động rollback file lại trạng thái ban đầu. Bạn phải phân tích lỗi trong Test Output, tự điều chỉnh logic và quay lại **Bước 3**. (Tối đa 2 lần thử, nếu vẫn Fail thì dừng và hỏi ý kiến User).
