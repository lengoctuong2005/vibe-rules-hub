---
name: "Audit & Fix Pipeline"
description: "Triggers the auditor subagent to scan for vulnerabilities/anti-patterns, then safely applies fixes wrapped in a continuous verification loop."
trigger: "/audit_fix"
---

# Audit & Fix Pipeline (Subagent + Continuous Verification)

Khi người dùng gọi `!audit_fix <file_paths>` hoặc `/audit_fix <file_paths>`, Agent phải thực thi NGHIÊM NGẶT các bước sau:

## Phase 1: Security & Quality Audit (Subagent)
Khởi chạy subagent `auditor` thông qua `spawner.py` để cách ly hoàn toàn việc phân tích khỏi memory của bạn.
```bash
python scripts/command_runner.py audit <file_paths>
```
Đọc output của command trên. Subagent sẽ trả về một báo cáo audit chi tiết cùng các khuyến nghị bảo mật và kiến trúc.

## Phase 2: Safe Checkpoint
Trước khi chạm vào code, lưu điểm khôi phục an toàn để đề phòng fail test:
```bash
python verification/continuous.py pre --name audit_fix_cp --target <file_paths_directory>
```

## Phase 3: Surgical Fixes
Áp dụng các khuyến nghị sửa chữa từ Subagent bằng công cụ `multi_replace_file_content`. Cấm tuyệt đối việc ghi đè toàn bộ file.

## Phase 4: Continuous Verification
Xác minh code sau chỉnh sửa bằng Regression Check/Test Runner:
```bash
python verification/continuous.py post --name audit_fix_cp --target <file_paths_directory>
```
- Nếu `[VERIFY-PASS]`: Code an toàn, tóm tắt kết quả cho User.
- Nếu `[VERIFY-FAIL]`: Hệ thống đã tự động rollback. Báo cáo nguyên nhân fail từ log cho User và yêu cầu chỉ thị nghiệm thu hoặc tự phân tích lại nghiệm thu vòng 2.
