# AGENTS.md - Quy Chuẩn & Quy Tắc Vận Hành Phân Tích Doanh Nghiệp Theo Chuẩn 10-K

Tài liệu này là quy chuẩn chỉ đạo tối cao dành cho **AI Agent** trong repository `10K`. 
Mục tiêu cốt lõi của dự án là: **Tiếp nhận Báo Cáo Thường Niên (Annual Report) và Báo Cáo Tài Chính (Financial Statements) dưới dạng PDF của doanh nghiệp, sau đó phân tích sâu sắc, bóc tách và trích xuất thành 7 trụ cột trọng yếu theo chuẩn mực báo cáo thường niên 10-K của Ủy ban Chứng khoán Hoa Kỳ (SEC).**

---

## 1. Bản Chất Dự Án & Cấu Trúc Thư Mục

Mỗi doanh nghiệp và từng năm tài chính được module hóa độc lập theo đường dẫn: `companies/<TICKER>/<YEAR>/`

```text
10K/
├── AGENTS.md                  # Bản quy chuẩn tối cao vận hành AI Agent
├── README.md                  # Hướng dẫn tổng quan và triết lý phân tích 10-K
├── requirements.txt           # Thư viện xử lý PDF và dữ liệu
├── templates/                 # Các biểu mẫu chuẩn cho từng phần phân tích
│   ├── 00-summary.md
│   ├── 01-business.md
│   ├── 02-risk-factors.md
│   ├── 03-financial-statements.md
│   ├── 04-mda.md
│   ├── 05-management-governance.md
│   ├── 06-ownership.md
│   └── 07-exhibits-notes.md
├── scripts/                   # Công cụ trích xuất PDF và đóng gói báo cáo
│   ├── init_company.py        # Khởi tạo thư mục mã công ty & năm tài chính
│   ├── extract_pdf.py         # Trích xuất văn bản & bảng biểu từ PDF
│   └── build_report.py        # Đóng gói 7 phần thành báo cáo tổng hợp README.md
└── companies/
    └── <TICKER>/              # Ví dụ: VNM, FPT, HPG, VHM, AAPL, NVDA...
        └── <YEAR>/            # Ví dụ: 2023, 2024...
            ├── reports/       # Thư mục chứa các file PDF gốc của người dùng
            │   ├── annual-report.pdf          # Báo cáo thường niên gốc
            │   └── financial-statements.pdf   # Báo cáo tài chính kiểm toán gốc
            ├── analysis/      # 7 file markdown tương ứng 7 trụ cột 10-K
            │   ├── 01-business.md
            │   ├── 02-risk-factors.md
            │   ├── 03-financial-statements.md
            │   ├── 04-mda.md
            │   ├── 05-management-governance.md
            │   ├── 06-ownership.md
            │   └── 07-exhibits-notes.md
            ├── summary.md     # Bản tóm tắt điều hành (Executive Summary & Red Flags)
            ├── README.md      # Toàn bộ báo cáo phân tích hoàn chỉnh được đóng gói
            └── progress.json  # Trạng thái xử lý các section
```

---

## 2. 7 Trụ Cột Trọng Yếu Của Báo Cáo Phân Tích 10-K

Khi phân tích bất kỳ doanh nghiệp nào, AI **BẮT BUỘC** phải bóc tách số liệu và thông tin theo đúng 7 phần sau:

### Trụ Cột 1: Business (Item 1) — Mô Hình Kinh Doanh & Vị Thế Cạnh Tranh
- **Công ty thực sự kinh doanh gì?** Bản chất cốt lõi của việc kiếm tiền, nguồn doanh thu chính phân theo mảng sản phẩm/dịch vụ và theo khu vực địa lý.
- **Sản phẩm & Khách hàng:** Danh mục sản phẩm mũi nhọn, cơ cấu khách hàng (khách hàng B2B, B2C, có bị phụ thuộc vào một vài khách hàng lớn không?).
- **Thị trường & Mạng lưới phân phối:** Quy mô thị trường, thị phần hiện tại, kênh phân phối (truyền thống, hiện đại, xuất khẩu).
- **Đối thủ cạnh tranh & Lợi thế cạnh tranh (Economic Moat):** Lợi thế chi phí thấp, hiệu ứng mạng lưới, tài sản vô hình (thương hiệu, bằng sáng chế), chi phí chuyển đổi cao (switching cost).
- **Chuỗi cung ứng:** Nguồn nguyên vật liệu đầu vào, nhà cung ứng chính, rủi ro đứt gãy hoặc phụ thuộc đơn nguồn.

### Trụ Cột 2: Risk Factors (Item 1A) — Những Rủi Ro Trọng Yếu
- **Rủi ro Vĩ mô & Ngành:** Lãi suất, tỷ giá ngoại tệ, lạm phát, biến động giá nguyên vật liệu, chu kỳ kinh tế, chính sách thuế/xuất nhập khẩu.
- **Rủi ro Cạnh tranh & Đổi mới công nghệ:** Nguy cơ mất thị phần vào tay đối thủ mới nổi, sự thay đổi thị hiếu người tiêu dùng, bị thay thế bởi công nghệ mới.
- **Rủi ro Vận hành & Pháp lý:** Sự cố môi trường, vi phạm pháp lý, tranh chấp sở hữu trí tuệ, rủi ro nhân sự cấp cao, kiện tụng đang diễn ra.
- **Rủi ro Tài chính & Đòn bẩy:** Nợ vay đáo hạn, rủi ro thanh khoản ngắn hạn, biến động lãi suất vay ngân hàng.

### Trụ Cột 3: Financial Statements (Item 8) — Báo Cáo Tài Chính & Sức Khỏe Tài Chính
- **Báo cáo Kết quả Hoạt động Kinh doanh (P&L):**
  - Doanh thu thuần, Giá vốn hàng bán, Biên lợi nhuận gộp (Gross Margin).
  - Chi phí bán hàng & quản lý (SG&A), Chi phí tài chính (lãi vay).
  - Lợi nhuận trước thuế và sau thuế (Net Income), Biên lợi nhuận ròng (Net Margin).
- **Bảng Cân đối Kế toán (Balance Sheet):**
  - Tiền mặt & Đầu tư tài chính ngắn hạn (Cash & Equivalents).
  - Phải thu khách hàng (Accounts Receivable) vs Hàng tồn kho (Inventory).
  - Tài sản cố định hữu hình/vô hình & Chi phí xây dựng dở dang (Capex).
  - Cơ cấu nợ vay: Nợ ngắn hạn vs Nợ dài hạn, Tỷ lệ Nợ/Vốn chủ sở hữu (D/E).
- **Báo cáo Lưu chuyển Tiền tệ (Cash Flow Statement):**
  - Dòng tiền từ hoạt động kinh doanh (CFO) — Dòng tiền tạo ra từ cốt lõi.
  - Dòng tiền đầu tư (CFI) — Chi tiêu vốn mở rộng Capex.
  - Dòng tiền tài chính (CFF) — Vay nợ, trả nợ, chia cổ tức bằng tiền mặt.
  - **Dòng tiền tự do (Free Cash Flow = CFO - Capex):** Khả năng tự sinh tiền của doanh nghiệp.
- **Chỉ số Hiệu quả Vận hành:** ROE, ROA, ROIC, Vòng quay hàng tồn kho, Chu kỳ tiền mặt (Cash Conversion Cycle - CCC).
- **Đánh giá Chất lượng Lợi nhuận (Quality of Earnings):** So sánh Net Income với CFO. Nếu Net Income tăng mạnh nhưng CFO âm nhiều năm liên tiếp, đây là tín hiệu cảnh báo cực lớn (Red Flag).

### Trụ Cột 4: MD&A (Item 7) — Thảo Luận & Phân Tích Của Ban Điều Hành
- **Lý giải từ Ban Giám đốc:** Tại sao doanh thu và lợi nhuận tăng/giảm trong năm? Nguyên nhân đến từ tăng trưởng sản lượng (volume) hay tăng giá bán (price)?
- **Đánh giá các phân khúc (Segment Performance):** Mảng nào bứt phá, mảng nào suy giảm, nguyên nhân cụ thể.
- **Kế hoạch Phân bổ Vốn (Capital Allocation):** Ban lãnh đạo dự định làm gì với lượng tiền mặt thặng dư? (Tái đầu tư mở rộng năng lực sản xuất, M&A mua lại công ty khác, trả cổ tức tiền mặt hay mua lại cổ phiếu quỹ).
- **Kế hoạch tương lai & Triển vọng năm tới:** Mục tiêu kinh doanh năm tiếp theo, dự báo rủi ro và các dự án trọng điểm đang triển khai.
- **Kiểm chứng độ uy tín của Lãnh đạo:** Đối chiếu lời hứa của ban lãnh đạo ở báo cáo năm trước so với kết quả thực thi năm nay.

### Trụ Cột 5: Management & Governance (Item 10 & 11) — Ban Lãnh Đạo & Quản Trị Công Ty
- **Hồ sơ Ban Điều hành (CEO, CFO) & Hội đồng Quản trị (HĐQT):** Lý lịch, kinh nghiệm trong ngành, số năm gắn bó với doanh nghiệp.
- **Cấu trúc Quản trị:** Tỷ lệ thành viên HĐQT độc lập, sự tách bạch giữa Chủ tịch HĐQT và Tổng Giám đốc (CEO).
- **Cơ chế Đãi ngộ & Lương thưởng (Executive Compensation):** Lương thưởng có gắn liền với hiệu quả kinh doanh dài hạn (ROE, FCF, EPS) hay chỉ dựa trên tăng trưởng doanh thu ngắn hạn? Có phát hành ESOP quá mức gây pha loãng cổ phiếu không?

### Trụ Cột 6: Ownership (Item 12) — Cơ Cấu Sở Hữu & Cổ Đông
- **Cổ đông lớn & Cơ cấu sở hữu:** Cổ đông nhà nước, sáng lập viên/gia đình, các quỹ đầu tư tổ chức (quỹ nội, quỹ ngoại), tỷ lệ sở hữu nước ngoài (Room ngoại).
- **Cam kết của Ban Lãnh đạo (Skin in the Game):** Ban điều hành và các thành viên HĐQT sở hữu bao nhiêu % cổ phần? Họ có cùng chịu rủi ro với cổ đông đại chúng không?
- **Giao dịch nội bộ (Insider Trading):** Lãnh đạo mua vào hay bán ra cổ phiếu trong năm tài chính?

### Trụ Cột 7: Exhibits, Footnotes & Related Parties (Item 13 & 15) — Thuyết Minh BCTC & Bên Liên Quan
- **Giao dịch Bên Liên Quan (Related Party Transactions - CỰC KỲ QUAN TRỌNG):** Các khoản cho vay, mua bán dịch vụ, ủy thác đầu tư với các công ty con, công ty liên kết, hoặc doanh nghiệp riêng của thành viên HĐQT. Đây là nơi dễ phát sinh rủi ro rút ruột (tunneling) hoặc chuyển giá.
- **Cam kết ngoại bảng & Nợ tiềm tàng (Off-balance sheet obligations):** Các khoản bảo lãnh nợ cho bên thứ ba, cam kết hợp đồng thuê hoạt động lớn, các vụ kiện tụng đang chờ phán quyết.
- **Ý kiến của Đơn vị Kiểm toán Độc lập:** 
  - Chấp nhận toàn phần (Unqualified Opinion).
  - Có ý kiến ngoại trừ (Qualified Opinion) hoặc vấn đề cần nhấn mạnh (Emphasis of Matter).
  - Từ chối đưa ra ý kiến (Disclaimer) hoặc Ý kiến trái ngược (Adverse).
- **Thay đổi chính sách kế toán:** Thay đổi phương pháp ghi nhận doanh thu, thời gian trích khấu hao, hay trích lập dự phòng.

---

## 3. Quy Trình 5 Bước Tự Động Hóa Cho AI Agent

Khi người dùng yêu cầu phân tích một công ty, ví dụ:
> **"Hãy phân tích báo cáo thường niên và BCTC của công ty VNM năm 2023"**  
*(hoặc phân tích một thư mục `companies/<TICKER>/<YEAR>`)*

AI **BẮT BUỘC** kích hoạt quy trình 5 bước sau đây:

### Bước 1: Kiểm Tra Tài Liệu & Cấu Trúc Thư Mục
1. Kiểm tra sự tồn tại của thư mục `companies/<TICKER>/<YEAR>/reports/`.
2. Xác định các file PDF có trong thư mục `reports/` (ví dụ `annual-report.pdf`, `financial-statements.pdf`, hoặc file kết hợp).
3. Nếu thư mục chưa có cấu trúc chuẩn, chạy script khởi tạo:
   ```bash
   python3 scripts/init_company.py --ticker <TICKER> --year <YEAR>
   ```

### Bước 2: Quét Mục Lục & Trích Xuất Dữ Liệu PDF
1. Sử dụng script `scripts/extract_pdf.py` để quét mục lục, tìm trang chứa:
   - Tổng quan công ty & hoạt động kinh doanh (Business)
   - Báo cáo của Ban Giám đốc & HĐQT (MD&A)
   - Báo cáo Tài chính đã kiểm toán (Cân đối kế toán, Kết quả KD, Lưu chuyển tiền tệ, Thuyết minh)
   - Danh sách HĐQT, Ban Giám đốc, cơ cấu cổ đông.
2. Trích xuất text và bảng số liệu từ các dải trang tương ứng để phục vụ phân tích.

### Bước 3: Phân Tích Từng Trụ Cột & Lưu Vào `analysis/`
1. Lần lượt viết các file phân tích chi tiết vào `companies/<TICKER>/<YEAR>/analysis/`:
   - `01-business.md`
   - `02-risk-factors.md`
   - `03-financial-statements.md`
   - `04-mda.md`
   - `05-management-governance.md`
   - `06-ownership.md`
   - `07-exhibits-notes.md`
2. **Quy tắc trích xuất số liệu:**
   - Mọi số liệu tài chính phải có đơn vị tính rõ ràng (VNĐ, Tỷ VNĐ, Triệu USD, %).
   - Luôn so sánh với cùng kỳ năm trước ($YoY$) và tính tỷ lệ tăng trưởng.
   - Nêu rõ số trang trích dẫn trong PDF gốc để người đọc có thể kiểm chứng.
3. **Cảnh báo Cờ Đỏ (Red Flags):** Nếu phát hiện bất thường (ví dụ: Phải thu tăng đột biến nhanh hơn doanh thu, CFO âm nặng trong khi LNST dương, vay nợ ngắn hạn vượt tài sản ngắn hạn, giao dịch bên liên quan phức tạp), phải đóng khung cảnh báo `> [!WARNING]` hoặc `> [!CAUTION]`.

### Bước 4: Viết Bản Tóm Tắt Điều Hành (`summary.md`) & Đóng Gói `README.md`
1. Tạo `summary.md` chứa:
   - Tóm tắt 1 trang (1-Page Executive Summary).
   - Điểm mạnh cốt lõi (Key Strengths) & Điểm yếu/Rủi ro lớn nhất (Key Risks).
   - Bảng tổng hợp các chỉ số tài chính 3-5 năm gần nhất.
   - Bảng tổng hợp các Cờ Đỏ (Red Flags).
   - Kết luận & Góc nhìn đầu tư theo phong cách 10-K.
2. Chạy script đóng gói báo cáo hoàn chỉnh:
   ```bash
   python3 scripts/build_report.py --ticker <TICKER> --year <YEAR>
   ```
   Script này sẽ tổng hợp `summary.md` và toàn bộ 7 file trong `analysis/` thành một file `companies/<TICKER>/<YEAR>/README.md` duy nhất, chuẩn mực.

### Bước 5: Tự Động Git Commit & Push Lên GitHub
> [!IMPORTANT]
> Người dùng đã cấp phép tự động sử dụng Git cho repository này (`git@github.com:lenhan1102/10K.git`).
> Sau khi hoàn thành phân tích hoặc cập nhật, thực hiện:
```bash
git add .
git commit -m "feat(<TICKER>-<YEAR>): complete 10-K analysis"
git push origin main
```

---

## 4. Phong Cách Báo Cáo Phản Hồi

- Khách quan, trung lập, bám sát số liệu thực tế, không dự đoán chủ quan hay đưa ra lời khuyên đầu tư tài chính trực tiếp.
- Trình bày mạch lạc, bảng biểu rõ ràng, sử dụng bullet points sắc bén.
- Báo cáo phản hồi khi hoàn thành lệnh:
  ```markdown
  Đã hoàn thành phân tích 10-K cho **[TÊN CÔNG TY] ([TICKER]) - Năm [YEAR]**
  - Thư mục báo cáo: `companies/<TICKER>/<YEAR>/`
  - 7 Trụ cột phân tích chi tiết: `companies/<TICKER>/<YEAR>/analysis/`
  - Báo cáo tóm tắt điều hành: `companies/<TICKER>/<YEAR>/summary.md`
  - Toàn văn báo cáo tổng hợp: `companies/<TICKER>/<YEAR>/README.md`
  - Git commit: `feat(<TICKER>-<YEAR>): complete 10-K analysis` (đã push lên main)
  ```
