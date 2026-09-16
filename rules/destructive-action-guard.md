---
trigger: always_on
description: "Destructive Action Guard: Canh bao, sao luu va yeu cau phe duyet ro rang truoc moi thao tac pha huy."
---
# Bao ve thao tac pha huy (Destructive Action Guard)

*   **Muc dich**: Ngan chan mat mat du lieu hoac lam hong trang thai Git/DB khong the van hoi.
*   **Trigger**: Kich hoat khi co y dinh chay cac lenh pha hoai (destructive) nhu `git reset --hard`, `git clean -fd`, `rm -rf`, `DROP TABLE`, `DELETE FROM`, hoac ghi de hang loat file lon.

## Noi dung cot loi

1.  **Kich hoat Canh Bao:**
    *   Truoc khi thuc hien cac lenh nguy hiem, Agent bat buoc phai dung lai.
    *   Phat ra canh bao ro rang: `[WARNING] Chuan bi thuc hien thao tac khong the hoan tac`.

2.  **Danh gia Sat thuong:**
    *   Liet ke chi tiet danh sach tai nguyen bi anh huong (cac file se bi xoa, database table se bi drop, nhanh git se bi reset).

3.  **Sao luu (Backup):**
    *   Tao ban sao luu tu dong truoc khi thuc hien.
    *   Vi du: Tao nhanh tam (temp branch) bang `git branch backup_before_reset` truoc khi chay `git reset --hard`.
    *   Hoac luu tru file ra thu muc `temp/` neu sua doi hang loat.

4.  **Xac nhan Explicit:**
    *   Chi tien hanh hanh dong pha huy khi da nhan duoc xac nhan truc tiep (explicit approval) cua User. Neu User chua cap quyen, tuyet doi khong tu chay.
