---
trigger: always_on
description: "Anti-Loop: Ngan chan thu-sai lap lai vo han, dung lai bao cao sau 3 lan that bai (Strike 3)."
---
# Quy tac chong vong lap go loi vo han (Anti-Loop)

*   **Muc dich**: Ngan chan tinh trang Agent thu-sai lien tuc (trial-and-error loop) dan den lang phi token va gay o nhiem lich su code.
*   **Trigger**: Kich hoat khi Agent tien hanh debug, fix bug, hoac nhan duoc bao loi tu nguoi dung.

## Noi dung cot loi

1.  **Strike 1 (Lan dau gap loi)**: 
    *   Doc log can than.
    *   Phan tich nguyen nhan goc re (Root Cause Analysis).
    *   De xuat ban va va tien hanh sua loi.

2.  **Strike 2 (Sua lan 1 van loi)**: 
    *   **KHONG DUOC DOAN TIEP.** 
    *   Bat buoc phai chen them cac lenh in log runtime (nhu `print()`, `console.log()`, `logger.debug()`) vao cac diem nghi ngo.
    *   Hoac kich hoat che do debug de thu thap them Telemetry (thong tin do luong).
    *   Quan sat log moi truoc khi ra quyet dinh sua code tiep.

3.  **Strike 3 (Van loi sau Strike 2)**: 
    *   **Dung lai ngay lap tuc.** 
    *   Khong duoc thu cac giai phap mu mo nua.
    *   Bao cao loi voi format: `[CONCERN]: Vuot qua gioi han tu go loi`.
    *   Tom tat lai cac gia thuyet da thu, log thu duoc va yeu cau User can thiep.
