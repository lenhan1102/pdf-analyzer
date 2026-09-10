# Project-Specific Rule: Git Automation For pdf-analyzer

## Mục Đích
Cho phép AI Agent tự động thực hiện các thao tác Git (Add, Commit, Push) sau khi hoàn thành công việc phân tích, khởi tạo, hoặc đóng gói báo cáo trong repository `pdf-analyzer`.

## Quy Định Cụ Thể
1. **Quyền Tự Động Push:**
   - Trong phạm vi workspace `pdf-analyzer`, AI được phép **tự động chạy lệnh `git add`, `git commit` và `git push`** sau khi hoàn thành task (ví dụ: phân tích xong một công ty, tạo phụ lục mới, cập nhật README...).
   - Không cần yêu cầu người dùng phải phê duyệt thủ công từng lệnh git.

2. **Tiêu Chuẩn Commit Message:**
   - Sử dụng chuẩn Conventional Commits rõ ràng, ví dụ:
     - `feat(analysis): hoàn thành phân tích 10-K VRE FY 2024`
     - `feat(appendix): bổ sung phụ lục giải mã các khoản đặt cọc VRE`
     - `docs(rule): cập nhật quy tắc tự động git push`

3. **An Toàn Dữ Liệu:**
   - Tuyệt đối không commit các file credentials, API keys, token hoặc file rác tạm thời.
   - Kiểm tra `git status` trước khi commit để đảm bảo chỉ đưa lên các file hợp lệ.
