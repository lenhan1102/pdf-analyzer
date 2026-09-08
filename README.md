# 10K - Hệ Thống Phân Tích Báo Cáo Doanh Nghiệp Chuẩn 10-K Bằng AI Agent

Hệ thống tự động hóa tiếp nhận **Báo Cáo Thường Niên (Annual Report)** và **Báo Cáo Tài Chính (Financial Statements)** dưới định dạng PDF của doanh nghiệp, sau đó bóc tách, thẩm định và trích xuất các góc nhìn quan trọng nhất theo chuẩn mực báo cáo thường niên **Form 10-K** của Ủy ban Chứng khoán Hoa Kỳ (U.S. SEC).

---

## 📌 Tại Sao Lại Là Chuẩn 10-K?

Tại Việt Nam và nhiều thị trường quốc tế, Báo cáo Thường niên thường dài hàng trăm trang và đậm tính chất PR/Marketing, trong khi Báo cáo Tài chính lại chứa hàng loạt con số khô khan và thuyết minh phức tạp. 

Chuẩn **10-K** là tiêu chuẩn vàng của giới đầu tư giá trị (Warren Buffett, Charlie Munger, Li Lu...) để nhìn thấu bức tranh chân thực của một doanh nghiệp thông qua **7 Trụ Cột Trọng Yếu**:

| STT | Trụ Cột 10-K | Trọng Tâm Phân Tích |
|---|---|---|
| **1** | **Business** | Doanh nghiệp thực sự kiếm tiền từ đâu? Sản phẩm, khách hàng, thị phần & Con hào kinh tế (Moat). |
| **2** | **Risk Factors** | Những rủi ro có thể phá hủy mô hình kinh doanh (vĩ mô, ngành, công nghệ, pháp lý, tài chính). |
| **3** | **Financial Statements** | Sức khỏe BCTC (P&L, Balance Sheet, Cash Flow), FCF, chất lượng lợi nhuận (CFO vs Net Income). |
| **4** | **MD&A** | Ban lãnh đạo giải thích tại sao kết quả tăng/giảm, chiến lược phân bổ vốn & kế hoạch tương lai. |
| **5** | **Management & Governance** | Năng lực lãnh đạo, tính độc lập HĐQT, cơ chế lương thưởng & chính sách ESOP. |
| **6** | **Ownership** | Ai thực sự sở hữu doanh nghiệp? Ban điều hành có cùng chịu rủi ro (Skin in the game) không? |
| **7** | **Exhibits & Footnotes** | Thuyết minh BCTC, giao dịch bên liên quan (chống rút ruột), nợ tiềm tàng & ý kiến kiểm toán. |

---

## 📂 Cấu Trúc Repository

```text
10K/
├── AGENTS.md                  # Bản quy chuẩn tối cao cho AI Agent hoạt động
├── README.md                  # Tài liệu giới thiệu & hướng dẫn sử dụng
├── requirements.txt           # Thư viện Python (PyMuPDF, pdfplumber, pandas...)
├── templates/                 # Các biểu mẫu phân tích 7 phần chuẩn 10-K
│   ├── 00-summary.md
│   ├── 01-business.md
│   ├── 02-risk-factors.md
│   ├── 03-financial-statements.md
│   ├── 04-mda.md
│   ├── 05-management-governance.md
│   ├── 06-ownership.md
│   └── 07-exhibits-notes.md
├── scripts/                   # Công cụ tự động hóa
│   ├── init_company.py        # Tạo mới không gian phân tích cho mã CP & năm
│   ├── extract_pdf.py         # Trích xuất văn bản & bảng số liệu từ PDF
│   └── build_report.py        # Tổng hợp 7 phần thành báo cáo hoàn chỉnh README.md
└── companies/
    ├── EXAMPLE_VNM/           # Ví dụ mẫu thực tế: Vinamilk (VNM) năm 2023
    │   └── 2023/
    │       ├── reports/       # Chứa PDF gốc
    │       ├── analysis/      # 7 file markdown chi tiết
    │       ├── summary.md     # Tóm tắt điều hành & Bảng Cờ Đỏ (Red Flags)
    │       └── README.md      # Toàn văn báo cáo phân tích hoàn chỉnh
    └── <MÃ_CÔNG_TY>/
        └── <NĂM>/
```

---

## 🚀 Hướng Dẫn Sử Dụng Nhanh

### 1. Cài đặt môi trường
```bash
pip install -r requirements.txt
```

### 2. Khởi tạo không gian cho một công ty mới
```bash
# Ví dụ phân tích FPT năm 2023:
python3 scripts/init_company.py --ticker FPT --year 2023 --name "Công ty Cổ phần FPT"
```
Lệnh trên sẽ tạo sẵn cấu trúc thư mục tại `companies/FPT/2023/` kèm các template sẵn sàng.

### 3. Đặt file PDF vào thư mục `reports/`
Chép các file PDF báo cáo vào thư mục:
- `companies/FPT/2023/reports/annual-report.pdf` (Báo cáo thường niên)
- `companies/FPT/2023/reports/financial-statements.pdf` (BCTC kiểm toán)

### 4. Ra lệnh cho AI Agent
Trong môi trường Antigravity IDE hoặc chat với AI, bạn chỉ cần ra lệnh:
> *"Hãy phân tích báo cáo thường niên và BCTC của công ty FPT năm 2023"*

AI sẽ tự động:
1. Đọc và tuân thủ tuyệt đối quy định trong [AGENTS.md](AGENTS.md).
2. Trích xuất dữ liệu, bảng biểu từ các file PDF trong thư mục `reports/`.
3. Phân tích chuyên sâu 7 trụ cột theo chuẩn 10-K và lưu vào `analysis/`.
4. Phát hiện các dấu hiệu cảnh báo (Red Flags) và viết `summary.md`.
5. Chạy `python3 scripts/build_report.py --ticker FPT --year 2023` để đóng gói báo cáo hoàn chỉnh.
6. Commit và push tự động lên GitHub.

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
