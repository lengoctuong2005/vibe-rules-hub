# Nén & Tóm Tắt Hội Thoại (Latent Briefing)

**Mô tả**: Khi cuộc hội thoại với người dùng kéo dài vượt mức (thường là > 20 lượt hoặc khi nhận thấy context window sắp tràn), Agent sẽ chạy workflow này để "Rửa Mặt" (Context Cleanse), nén lại toàn bộ chi tiết và đưa ra một "Latent Brief".

## Các bước thực hiện:

### Phase 1: Nhận diện rác Context
1. Dừng nhận request tiếp theo. Nhẩm lại toàn bộ lịch sử đoạn chat.
2. Xác định các nỗ lực/phương án đã **thất bại** và loại bỏ các file log quá dài (>100 dòng) không còn cần thiết khỏi bộ nhớ ngắn hạn.

### Phase 2: Chưng Cất (Distillation)
1. Ghi tóm tắt lại tiến trình hiện tại (Current Status) thành 3-5 gạch đầu dòng.
2. Ghi lại phương pháp nào đã được chốt (Chosen Approach) và tại sao.
3. Ghi lại các phần việc còn dang dở (Pending Tasks) ở cuối.

### Phase 3: Đề xuất làm sạch (Cleanse Proposal)
1. Trình bày Latent Briefing ra màn hình (hoặc lưu vào `memory/session-state.md`).
2. Gợi ý với người dùng: *"Ngữ cảnh hiện tại đã khá nặng, tôi đề xuất chúng ta nên clear chat (sử dụng lệnh `/clear` hoặc mở phiên mới) để tôi hoạt động nhanh và tiết kiệm token hơn. Bạn có thể chép lại đoạn tóm tắt bên trên vào phiên chat mới."*