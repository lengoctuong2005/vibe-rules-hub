# TOOL ALIASES & IDE MAPPING (Bản Đồ Ánh Xạ Công Cụ IDE Thực Tế)

**Version:** 2.0.0
**Target IDE:** Antigravity / Gemini Agentic IDE

---

## 1. MAPPING TABLE (Quy Ước Ánh Xạ Công Cụ)

Khi bất kỳ Skill, Workflow hoặc tài liệu nào nhắc đến tên công cụ cũ (legacy tool), Agent **BẮT BUỘC** gọi công cụ native tương ứng trong Antigravity IDE:

| Tên gọi trong Skill/Tài liệu cũ | Công cụ Native Antigravity | Tham số chính | Ghi chú & Best Practice |
|---|---|---|---|
| `read_file`, `view_file` | `view_file` | `AbsolutePath`, `StartLine`, `EndLine` | Đọc theo đoạn giới hạn (<800 dòng/lần) để tiết kiệm token. |
| `write_file`, `create_file` | `write_to_file` | `TargetFile`, `CodeContent`, `Overwrite` | Dùng khi tạo file MỚI hoàn toàn. |
| `edit_file`, `replace_string` | `replace_file_content` | `TargetFile`, `TargetContent`, `ReplacementContent`, `StartLine`, `EndLine` | **Mặc định khi sửa code.** Sửa chính xác khối lệnh, không ghi đè cả file. |
| `multi_edit_file` | `multi_replace_file_content` | `TargetFile`, `ReplacementChunks` | Dùng khi sửa nhiều khối rời rạc trong cùng 1 file. |
| `bash`, `exec`, `shell_command` | `run_command` | `CommandLine`, `Cwd`, `WaitMsBeforeAsync` | Shell thực tế: PowerShell trên Windows. Không dùng `cd`. |
| `grep`, `search_code` | `grep_search` | `SearchPath`, `Query`, `Includes`, `IsRegex` | Tìm kiếm chính xác, kèm `Includes` để lọc loại file. |
| `find_files`, `list_dir` | `list_dir` | `DirectoryPath` | Khám phá cấu trúc cây thư mục. |
| `google_search`, `web_search` | `search_web` | `query`, `domain` | Tra cứu thông tin trên Internet. |
| `fetch_webpage`, `curl` | `read_url_content` / `mcp_fetch_fetch` | `Url` / `url` | Đọc nội dung web dưới dạng markdown. |
| `browser_action` | `browser_subagent` | `Task`, `RecordingName` | Tự động hóa tác vụ browser phức tạp. |
| `ask_user` | `ask_question` | `questions` | Hiển thị modal trắc nghiệm cho người dùng. |

---

## 2. SURGICAL CODE EDIT RULE (Luật Sửa Code Chính Xác)

1. **Tuyệt đối cấm Full Overwrite:** Không được dùng `write_to_file` với `Overwrite: true` để sửa một vài dòng trong file mã nguồn đã có.
2. **Bắt buộc dùng `replace_file_content`:** Chỉ thay thế đúng khối code cần sửa.
3. **Bảo tồn Comment & Logic không liên quan:** Không xóa bất kỳ dòng mã hoặc chú thích nào ngoài phạm vi yêu cầu.
