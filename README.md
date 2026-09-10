# 10K - Hệ Thống Phân Tích Báo Cáo Doanh Nghiệp Chuẩn 10-K Bằng AI Agent

Hệ thống tự động hóa tiếp nhận **Báo Cáo Thường Niên (Annual Report)** và **Báo Cáo Tài Chính (Financial Statements)** dưới định dạng PDF của doanh nghiệp, sau đó bóc tách, thẩm định và trích xuất các góc nhìn quan trọng nhất theo chuẩn mực báo cáo thường niên **Form 10-K** của Ủy ban Chứng khoán Hoa Kỳ (U.S. SEC).

---

## 📌 Tại Sao Lại Là Chuẩn 10-K?

Tại Việt Nam và nhiều thị trường quốc tế, Báo cáo Thường niên thường dài hàng trăm trang và đậm tính chất PR/Marketing, trong khi Báo cáo Tài chính lại chứa hàng loạt con số khô khan và thuyết minh phức tạp. 

Chuẩn **10-K** là tiêu chuẩn vàng của giới đầu tư giá trị (Warren Buffett, Charlie Munger, Li Lu...) để nhìn thấu bức tranh chân thực của một doanh nghiệp thông qua **8 Trụ Cột Trọng Yếu**:

| STT | Trụ Cột 10-K | Trọng Tâm Phân Tích |
|---|---|---|
| **1** | **Business** | Doanh nghiệp thực sự kiếm tiền từ đâu? Sản phẩm, khách hàng, thị phần & Con hào kinh tế (Moat). |
| **2** | **Risk Factors** | Những rủi ro có thể phá hủy mô hình kinh doanh (vĩ mô, ngành, công nghệ, pháp lý, tài chính). |
| **3** | **Financial Statements** | Sức khỏe BCTC (P&L, Balance Sheet, Cash Flow), FCF, chất lượng lợi nhuận (CFO vs Net Income). |
| **4** | **MD&A** | Ban lãnh đạo giải thích tại sao kết quả tăng/giảm, chiến lược phân bổ vốn & kế hoạch tương lai. |
| **5** | **Management & Governance** | Năng lực lãnh đạo, tính độc lập HĐQT, cơ chế lương thưởng & chính sách ESOP. |
| **6** | **Ownership** | Ai thực sự sở hữu doanh nghiệp? Ban điều hành có cùng chịu rủi ro (Skin in the game) không? |
| **7** | **Exhibits & Footnotes** | Thuyết minh BCTC, giao dịch bên liên quan (chống rút ruột), nợ tiềm tàng & ý kiến kiểm toán. |
| **8** | **Disclosure Gaps & Blind Spots** | **Điểm mù & Khoảng trống thông tin:** Ban Quản Trị biết rõ nhưng cố tình giấu hoặc không công bố chi tiết (doanh thu theo SKU, biên lãi gộp từng mảng, nồng độ khách hàng/nhà cung cấp, công suất thực tế, covenants nợ vay). |

---

## 📂 Cấu Trúc Repository Phân Cấp (Hierarchical Structure)

Hệ thống được tổ chức ngăn nắp theo cấu trúc: `companies/<TICKER>/<YEAR>/<PERIOD>/`  
(Trong đó `<PERIOD>` là `FY` cho cả năm, hoặc `Q1`, `Q2`, `Q3`, `Q4` cho các quý).

```text
10K/
├── AGENTS.md                  # Bản quy chuẩn tối cao cho AI Agent hoạt động
├── README.md                  # Tài liệu giới thiệu & hướng dẫn sử dụng
├── requirements.txt           # Thư viện Python (PyMuPDF, pdfplumber, pandas...)
├── templates/                 # Các biểu mẫu phân tích 8 phần chuẩn 10-K
│   ├── 00-summary.md
│   ├── 01-business.md
│   ├── 02-risk-factors.md
│   ├── 03-financial-statements.md
│   ├── 04-mda.md
│   ├── 05-management-governance.md
│   ├── 06-ownership.md
│   ├── 07-exhibits-notes.md
│   └── 08-disclosure-gaps.md
├── scripts/                   # Công cụ tự động hóa
│   ├── init_company.py        # Tạo mới không gian phân tích cho mã CP, năm & kỳ
│   ├── extract_pdf.py         # Trích xuất văn bản & bảng số liệu từ PDF
│   └── build_report.py        # Tổng hợp thành báo cáo hoàn chỉnh README.md
└── companies/
    └── <TICKER>/              # Mã cổ phiếu (ví dụ: VNM, FPT, HPG, AAPL...)
        └── <YEAR>/            # Năm tài chính (ví dụ: 2023, 2024...)
            ├── FY/            # Báo cáo thường niên & BCTC kiểm toán cả năm (Chuẩn 10-K)
            │   ├── reports/   # PDF gốc tuân thủ quy chuẩn đặt tên file
            │   │   ├── <TICKER>_<YEAR>_FY_Annual-Report.pdf
            │   │   └── <TICKER>_<YEAR>_FY_Audited-FS.pdf
            │   ├── analysis/  # 8 file markdown chi tiết
            │   ├── summary.md # Tóm tắt điều hành, Cờ Đỏ & Điểm minh bạch
            │   ├── README.md  # Toàn văn báo cáo phân tích hoàn chỉnh
            │   └── progress.json
            ├── Q1/            # Báo cáo tài chính Quý 1 (Chuẩn 10-Q)
            ├── Q2/
            ├── Q3/
            └── Q4/
```

### 🏷️ Quy Chuẩn Đặt Tên File (Naming Convention)
Để đảm bảo dễ dàng tra cứu, tìm kiếm và không bị lẫn lộn giữa các kỳ, các file PDF trong `reports/` phải tuân theo cú pháp:  
`[TICKER]_[YEAR]_[PERIOD]_[LOẠI_TÀI_LIỆU].pdf`
- Ví dụ cả năm: `VNM_2023_FY_Annual-Report.pdf`, `VNM_2023_FY_Audited-FS.pdf`
- Ví dụ quý: `VNM_2024_Q1_Financial-Statements.pdf`, `VNM_2024_Q1_Management-Report.pdf`

---

## 🚀 Hướng Dẫn Sử Dụng Nhanh

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Khởi tạo không gian cho một công ty & thời điểm mới
```bash
# Phân tích báo cáo cả năm 2023 (Mặc định kỳ FY):
python3 scripts/init_company.py --ticker FPT --year 2023 --period FY --name "Công ty Cổ phần FPT"

# Phân tích báo cáo quý (ví dụ Q1 2024):
python3 scripts/init_company.py --ticker FPT --year 2024 --period Q1 --name "Công ty Cổ phần FPT"
```
Lệnh trên sẽ tự động tạo thư mục ngăn nắp tại `companies/FPT/2023/FY/` hoặc `companies/FPT/2024/Q1/`.

### 3. Đặt file PDF vào thư mục `reports/`
Chép các file PDF báo cáo đã đổi tên chuẩn vào thư mục:
- `companies/FPT/2023/FY/reports/FPT_2023_FY_Annual-Report.pdf`
- `companies/FPT/2023/FY/reports/FPT_2023_FY_Audited-FS.pdf`

### 4. Ra lệnh cho AI Agent
Trong môi trường Antigravity IDE hoặc chat với AI, bạn chỉ cần ra lệnh:
> *"Hãy phân tích báo cáo thường niên và BCTC của công ty FPT năm 2023 kỳ FY"* (hoặc kỳ Q1 2024)

AI sẽ tự động:
1. Đọc và tuân thủ tuyệt đối quy định trong [AGENTS.md](AGENTS.md).
2. Trích xuất dữ liệu từ các file PDF trong thư mục `reports/`.
3. Phân tích chuyên sâu 8 trụ cột theo chuẩn 10-K/10-Q & khoảng trống thông tin và lưu vào `analysis/`.
4. Phát hiện các dấu hiệu cảnh báo (Red Flags), chấm điểm minh bạch và viết `summary.md`.
5. Chạy `python3 scripts/build_report.py --ticker FPT --year 2023 --period FY` để đóng gói báo cáo hoàn chỉnh.

---

## 📋 Mẫu Prompt Ra Lệnh Cho AI (Prompts Cheatsheet)
Xem toàn bộ các mẫu câu lệnh tổng quát cho cả 2 Nhiệm vụ tại: **[PROMPTS.md](PROMPTS.md)**
- **Nhiệm vụ 1:** Phân tích BCTC & BCTN theo chuẩn 10-K & bóc tách điểm mù Ban Quản Trị.
- **Nhiệm vụ 2:** Trích xuất Tiêu chuẩn Doanh nghiệp Tinh hoa từ bài viết / bài nói chuyện.
- **Nhiệm vụ Kết hợp:** Chấm điểm đối chiếu doanh nghiệp theo Bộ tiêu chuẩn (`scorecard`).


---

## 🕵️‍♂️ Kiểm Toán Tính Minh Bạch & Điểm Mù (Disclosure Gaps)

Hệ thống được thiết kế theo tư duy của nhà đầu tư sở hữu toàn bộ doanh nghiệp: **"Nếu tôi là chủ sở hữu, Ban Quản Trị đang giấu tôi điều gì?"**
- **Cơ cấu doanh thu gộp:** Bóc tách các trường hợp công ty chỉ gộp 1 dòng chung thay vì tách rõ doanh thu và biên lợi nhuận từng dòng sản phẩm mũi nhọn.
- **Nồng độ rủi ro đơn nguồn:** Liệt kê các khách hàng lớn ($\ge 10\%$ doanh thu) hoặc nhà cung cấp độc quyền bị che giấu.
- **Hiệu suất vận hành thực tế:** Đo lường công suất nhà máy vs tỷ lệ huy động thực tế (% Utilization Rate).
- **Cam kết tài chính ngầm:** Phát hiện các điều khoản covenants vay nợ ngân hàng có rủi ro bị vi phạm.
- **Bảng câu hỏi chất vấn ĐHĐCĐ:** Tạo sẵn Top 5 câu hỏi trọng yếu để cổ đông truy vấn Ban Lãnh đạo tại Đại hội Cổ đông.

---

## 🛡️ Hệ Thống Nhận Diện Dấu Hiệu Cảnh Báo (Red Flags Checklist)

Hệ thống được thiết kế đặc biệt để phát hiện các bẫy số liệu kế toán:
- **Phải thu tăng đột biến:** Tốc độ tăng của Khoản phải thu vượt xa tốc độ tăng Doanh thu (dấu hiệu bán chịu để thổi phồng doanh thu).
- **Chất lượng dòng tiền kém:** Lợi nhuận kế toán (Net Income) dương lớn nhưng Dòng tiền kinh doanh (CFO) âm nhiều kỳ liên tiếp.
- **Vấn đề bên liên quan:** Các giao dịch ủy thác đầu tư, tạm ứng, cho vay với công ty của người nhà ban lãnh đạo.
- **Rủi ro đòn bẩy ngắn hạn:** Nợ vay ngắn hạn vượt quá tài sản có tính thanh khoản cao (Tiền + Đầu tư ngắn hạn).
- **Ý kiến kiểm toán:** Bất kỳ lưu ý ngoại trừ hoặc nhấn mạnh nào từ đơn vị kiểm toán.

---

## 🤝 Giấy Phép & Đóng Góp
Dự án phục vụ mục đích nghiên cứu, học thuật và hỗ trợ phân tích đầu tư dựa trên các nguồn tài liệu công khai của doanh nghiệp.

