---
name: "Smart Refactor Pipeline"
description: "A safe refactoring workflow utilizing Worktree Isolation and Continuous Verification."
trigger: "/smart_refactor"
---

# Smart Refactor Pipeline (Worktree + Verification)

Bạn đang kích hoạt **Smart Refactor Pipeline**. Đây là quy trình tái cấu trúc mã nguồn an toàn tuyệt đối. Thực hiện tuần tự các bước sau:

## Bước 1: Khởi tạo Worktree Cách ly (Phase 6)
Để tránh làm vỡ nhánh chính, tạo một worktree riêng cho đợt refactor này:
```bash
python .gemini/scripts/worktree_manager.py create refactor_branch .gemini/tmp_worktrees/refactor_ws --project .
```

## Bước 2: Pre-edit Checkpoint (Lưu trạng thái an toàn trong Worktree)
```bash
python .gemini/verification/continuous.py pre --name refactor_cp --target .gemini/tmp_worktrees/refactor_ws
```

## Bước 3: Tiến hành Refactor
Thực hiện thay đổi code trong thư mục `.gemini/tmp_worktrees/refactor_ws`.

## Bước 4: Post-edit Verification
Kiểm tra test suite trong worktree:
```bash
python .gemini/verification/continuous.py post --name refactor_cp --target .gemini/tmp_worktrees/refactor_ws
```
- Nếu **FAIL**: Tự động rollback, bạn phải thử lại hoặc hủy bỏ.

## Bước 5: Merge & Cleanup
Nếu Bước 4 PASS, tiến hành merge nhánh `refactor_branch` lại nhánh chính và dọn dẹp worktree:
```bash
python .gemini/scripts/worktree_manager.py merge refactor_branch --project .
python .gemini/scripts/worktree_manager.py remove .gemini/tmp_worktrees/refactor_ws --project .
```
Báo cáo hoàn tất quá trình Refactor an toàn.
