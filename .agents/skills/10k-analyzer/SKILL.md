---
name: 10k-analyzer
description: Kích hoạt quy trình phân tích Báo Cáo Thường Niên và Báo Cáo Tài Chính của doanh nghiệp theo chuẩn mực 10-K & Bóc tách Điểm mù Ban Quản Trị (8 trụ cột trọng yếu, nhận diện Cờ Đỏ, chất lượng lợi nhuận, khoảng trống thông tin).
---

# 10-K Company Analyzer Skill

Skill này hướng dẫn AI Agent tiếp nhận và phân tích tài liệu PDF báo cáo tài chính, báo cáo thường niên của doanh nghiệp theo chuẩn 10-K kết hợp kiểm toán khoảng trống thông tin.

## Các trường hợp kích hoạt
- Người dùng yêu cầu phân tích một công ty (ví dụ: "Hãy phân tích báo cáo thường niên và BCTC của VNM năm 2023", "phân tích 10-K của FPT", "thẩm định sức khỏe tài chính doanh nghiệp...").
- Người dùng yêu cầu trích xuất một trong 8 trụ cột 10-K (Business, Risk Factors, Financial Statements, MD&A, Management & Governance, Ownership, Exhibits, Disclosure Gaps).

## Quy trình thực hiện chuẩn 5 bước

### 1. Xác định công ty & khởi tạo môi trường
- Xác định mã cổ phiếu `<TICKER>`, năm tài chính `<YEAR>`, và kỳ báo cáo `<PERIOD>` (`FY` cho cả năm, hoặc `Q1`, `Q2`, `Q3`, `Q4` cho quý).
- Kiểm tra `companies/<TICKER>/<YEAR>/<PERIOD>/reports/` đã có file PDF chưa.
- Đặt tên file PDF theo chuẩn: `<TICKER>_<YEAR>_<PERIOD>_<LOẠI_FILE>.pdf`.
- Nếu chưa có thư mục cấu trúc, chạy:
  ```bash
  python3 scripts/init_company.py --ticker <TICKER> --year <YEAR> --period <PERIOD>
  ```

### 2. Trích xuất tài liệu PDF
- Dùng `scripts/extract_pdf.py` với các từ khóa để xác định các trang mục tiêu:
  - Bảng cân đối kế toán, Kết quả KD, Lưu chuyển tiền tệ.
  - Phần thảo luận của Ban Tổng Giám đốc (MD&A).
  - Báo cáo Quản trị công ty & Danh sách HĐQT.
  - Thuyết minh BCTC (phần giao dịch bên liên quan, nợ tiềm tàng, cơ cấu doanh thu).

### 3. Phân tích 8 Trụ Cột theo mẫu
- Ghi dữ liệu vào `companies/<TICKER>/<YEAR>/<PERIOD>/analysis/`:
  - `01-business.md`
  - `02-risk-factors.md`
  - `03-financial-statements.md`
  - `04-mda.md`
  - `05-management-governance.md`
  - `06-ownership.md`
  - `07-exhibits-notes.md`
  - `08-disclosure-gaps.md` (Bóc tách thông tin bị thiếu/làm mờ: doanh thu theo SKU, biên lãi gộp từng mảng, nồng độ khách hàng/nhà cung cấp, công suất nhà máy, covenants nợ, KPI lãnh đạo).
  - **Đánh giá tổng quan cấu trúc BCTN theo tiêu chuẩn Warren Buffett ("Tự báo cáo cho bản thân sau một năm đi xa"):** Báo cáo có trả lời được trọn vẹn 5 câu hỏi cốt tử (sức khỏe thị phần thực tế, sự sòng phẳng thừa nhận sai lầm, chất lượng dòng tiền & phân bổ vốn, các quả bom nổ chậm, và tính đồng cam cộng khổ của lãnh đạo) hay chỉ là tài liệu PR tô hồng?
- Luôn kiểm tra tính nhất quán giữa CFO và Net Income.
- Cảnh báo các dấu hiệu Red Flags (bán chịu dồn dập, nợ vay ngắn hạn căng thẳng, giao dịch bên liên quan bất thường).

### 4. Viết Tóm Tắt Điều Hành & Đóng Gói
- Viết `summary.md` (Executive Summary, Top Risks, Moat, Red Flags Checklist, **Đánh giá Đạt Chuẩn 'Tự Báo Cáo Sau 1 Năm Đi Xa'**, Điểm số minh bạch).
- Chạy script đóng gói:
  ```bash
  python3 scripts/build_report.py --ticker <TICKER> --year <YEAR> --period <PERIOD>
  ```

### 5. Tạo File Giải Thích Bổ Sung / Phụ Lục (Khi người dùng yêu cầu)
- **Khi người dùng yêu cầu giải thích sâu** về một thuật ngữ, cơ chế kế toán hoặc hiện tượng tài chính đặc thù (ví dụ: xử lý nợ xấu, quỹ dự phòng, cam kết ngoại bảng, khấu hao, đòn bẩy, M&A...):
  1. **Tạo file markdown giải thích** đặt trong thư mục `companies/<TICKER>/<YEAR>/<PERIOD>/analysis/` với định dạng tên:
     - `09-appendix-<tên-chủ-đề-ngắn-gọn>.md` (hoặc số thứ tự tiếp theo nếu đã có `09-...`).
  2. **Nội dung file giải thích bắt buộc gồm:**
     - Bản chất kỹ thuật & quy định pháp lý/chuẩn mực kế toán (VAS/IFRS, Thông tư NHNN).
     - Bút toán kế toán kép (Double-entry) và tác động lên phương trình kế toán ($Assets = Liabilities + Equity$).
     - Minh họa bằng số liệu thực tế trích từ báo cáo tài chính của chính doanh nghiệp đó.
     - Đánh giá ý nghĩa đối với nhà đầu tư (cơ hội vs cờ đỏ rủi ro).
  3. **Đóng gói lại báo cáo:** Chạy lại script đóng gói để phụ lục tự động nối vào cuối file `README.md`:
     ```bash
     python3 scripts/build_report.py --ticker <TICKER> --year <YEAR> --period <PERIOD>
     ```

### 6. Commit, Push Git & Báo Cáo Phản Hồi
- **LƯU Ý QUY TẮC:** Chỉ thực hiện git add, commit, push khi người dùng cho phép (tuân thủ quy tắc không tự ý dùng git).
- Khi được phép, thực hiện:
  ```bash
  git add companies/<TICKER>/<YEAR>/<PERIOD>/
  git commit -m "feat(analysis): hoàn thành phân tích 10-K <TICKER> <PERIOD> <YEAR>"
  git push
  ```
- Thông báo kết quả phân tích kèm đường dẫn tới thư mục, file phân tích mới và file báo cáo README.md.

