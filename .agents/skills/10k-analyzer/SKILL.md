---
name: 10k-analyzer
description: Kích hoạt quy trình phân tích Báo Cáo Thường Niên và Báo Cáo Tài Chính của doanh nghiệp theo chuẩn mực 10-K (7 trụ cột trọng yếu, nhận diện Cờ Đỏ, chất lượng lợi nhuận).
---

# 10-K Company Analyzer Skill

Skill này hướng dẫn AI Agent tiếp nhận và phân tích tài liệu PDF báo cáo tài chính, báo cáo thường niên của doanh nghiệp theo chuẩn 10-K.

## Các trường hợp kích hoạt
- Người dùng yêu cầu phân tích một công ty (ví dụ: "Hãy phân tích báo cáo thường niên và BCTC của VNM năm 2023", "phân tích 10-K của FPT", "thẩm định sức khỏe tài chính doanh nghiệp...").
- Người dùng yêu cầu trích xuất một trong 7 trụ cột 10-K (Business, Risk Factors, Financial Statements, MD&A, Management & Governance, Ownership, Exhibits).

## Quy trình thực hiện chuẩn 5 bước

### 1. Xác định công ty & khởi tạo môi trường
- Xác định mã cổ phiếu `<TICKER>` và năm tài chính `<YEAR>`.
- Kiểm tra `companies/<TICKER>/<YEAR>/reports/` đã có file PDF chưa.
- Nếu chưa có thư mục cấu trúc, chạy:
  ```bash
  python3 scripts/init_company.py --ticker <TICKER> --year <YEAR>
  ```

### 2. Trích xuất tài liệu PDF
- Dùng `scripts/extract_pdf.py` với các từ khóa để xác định các trang mục tiêu:
  - Bảng cân đối kế toán, Kết quả KD, Lưu chuyển tiền tệ.
  - Phần thảo luận của Ban Tổng Giám đốc (MD&A).
  - Báo cáo Quản trị công ty & Danh sách HĐQT.
  - Thuyết minh BCTC (phần giao dịch bên liên quan, nợ tiềm tàng).

### 3. Phân tích 7 Trụ Cột theo mẫu
- Ghi dữ liệu vào `companies/<TICKER>/<YEAR>/analysis/`:
  - `01-business.md`
  - `02-risk-factors.md`
  - `03-financial-statements.md`
  - `04-mda.md`
  - `05-management-governance.md`
  - `06-ownership.md`
  - `07-exhibits-notes.md`
- Luôn kiểm tra tính nhất quán giữa CFO và Net Income.
- Cảnh báo các dấu hiệu Red Flags (bán chịu dồn dập, nợ vay ngắn hạn căng thẳng, giao dịch bên liên quan bất thường).

### 4. Viết Tóm Tắt Điều Hành & Đóng Gói
- Viết `summary.md` (Executive Summary, Top Risks, Moat, Red Flags Checklist).
- Chạy script đóng gói:
  ```bash
  python3 scripts/build_report.py --ticker <TICKER> --year <YEAR>
  ```

### 5. Git Commit & Push
- Tự động thực hiện lệnh Git đã được cấp phép:
  ```bash
  git add .
  git commit -m "feat(<TICKER>-<YEAR>): complete 10-K analysis"
  git push origin main
  ```
