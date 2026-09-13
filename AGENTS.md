# AGENTS.md - Quy Chuẩn & Quy Tắc Vận Hành Hệ Thống Phân Tích Doanh Nghiệp & Bộ Tiêu Chuẩn Đầu Tư

Tài liệu này là quy chuẩn chỉ đạo tối cao dành cho **AI Agent** trong repository. 
Hệ thống vận hành **3 Nhiệm Vụ Cốt Lõi** tương hỗ lẫn nhau:

1. **Nhiệm Vụ 1 (10k-analyzer):** Tiếp nhận Báo Cáo Thường Niên (Annual Report) và Báo Cáo Tài Chính (Financial Statements) dưới dạng PDF, sau đó bóc tách thành 8 trụ cột trọng yếu theo chuẩn 10-K của SEC kết hợp kiểm toán tính minh bạch & khoảng trống thông tin theo chuẩn Warren Buffett.
2. **Nhiệm Vụ 2 (criteria-extractor):** Tiếp nhận các tài liệu đúc kết tri thức (bài nói chuyện, bài viết, sách, tài liệu phân tích định tính dạng PDF/MD), trích xuất thành **Bộ Tiêu Chuẩn Doanh Nghiệp Tốt** (gồm cả định lượng BCTC và định tính: con hào kinh tế, quan hệ chính phủ/thể chế), từ đó làm thước đo đối chiếu chấm điểm (`scorecard`) cho các doanh nghiệp ở Nhiệm vụ 1.
3. **Nhiệm Vụ 3 (company-screener):** Phễu Lọc Doanh Nghiệp Đa Tầng (Multi-Stage Investment Funnel) - Tiếp nhận từng mã cổ phiếu, kiểm tra tuần tự qua 4 bước sàng lọc loại trừ khắt khe (Vòng tròn năng lực & Ngành nghề, Lỗ 3 năm liên tiếp, Chuỗi giá trị thấp & P/B >= 0.5, ROE 5 năm < 10%) và phân loại vào 5 file lưu trữ tương ứng trong `screenings/`.

---

## 1. Bản Chất Dự Án & Cấu Trúc Thư Mục Phân Cấp

```text
pdf-analyzer/
├── AGENTS.md                  # Bản quy chuẩn tối cao vận hành AI Agent
├── README.md                  # Hướng dẫn tổng quan
├── requirements.txt           # Thư viện xử lý PDF và dữ liệu
├── .agents/skills/            # Kỹ năng định nghĩa cho AI Agent
│   ├── 10k-analyzer/          # Kỹ năng phân tích doanh nghiệp theo chuẩn 10-K
│   ├── criteria-extractor/    # Kỹ năng trích xuất tiêu chuẩn doanh nghiệp tốt
│   ├── company-screener/      # [Nhiệm vụ 3] Điều phối phễu lọc đa tầng
│   ├── screener-step1-industry/       # Bước 1: Vòng tròn năng lực & Ngành nghề
│   ├── screener-step2-profitability/  # Bước 2: Lợi nhuận 3 năm liên tiếp
│   ├── screener-step3-value-chain-pb/ # Bước 3: Chuỗi giá trị & Ngoại lệ P/B
│   └── screener-step4-roe/            # Bước 4: Hiệu quả vốn ROE 5 năm
├── screenings/                # [Nhiệm vụ 3] Hệ thống file kết quả & bảng tóm tắt phễu lọc
│   ├── 00-quick-summary-all.md             # ⚡ Bảng tổng hợp siêu tốc toàn bộ 50 mã (Cheat-sheet)
│   ├── summary-01-circle-of-competence.md  # 📋 Bảng tóm tắt nhanh rớt Bước 1
│   ├── summary-02-consecutive-loss.md      # 📋 Bảng tóm tắt nhanh rớt Bước 2
│   ├── summary-03-low-value-chain.md       # 📋 Bảng tóm tắt nhanh rớt Bước 3
│   ├── summary-04-low-roe.md               # 📋 Bảng tóm tắt nhanh rớt Bước 4
│   ├── summary-05-passed-champions.md      # 🏆 Bảng tóm tắt nhanh 22 viên kim cương (File 5)
│   ├── 01-rejected-circle-of-competence.md # Hồ sơ chi tiết rớt Bước 1 (Ngành nghề)
│   ├── 02-rejected-consecutive-loss.md     # Hồ sơ chi tiết rớt Bước 2 (Lỗ 3 năm)
│   ├── 03-rejected-low-value-chain.md      # Hồ sơ chi tiết rớt Bước 3 (Chuỗi GT thấp & P/B >= 0.5)
│   ├── 04-rejected-low-roe.md              # Hồ sơ chi tiết rớt Bước 4 (ROE 5 năm < 10%)
│   ├── 05-passed-champions.md              # 🏆 File 5: Hồ sơ chi tiết doanh nghiệp vượt qua toàn bộ 4 bước
│   └── screening_dashboard.md              # Bảng Dashboard tổng quan phễu lọc
├── frameworks/                # [Nhiệm vụ 2] Kho tri thức tiêu chuẩn & triết lý đầu tư
│   ├── sources/               # Tài liệu nguồn (bài viết, bài phát biểu PDF/MD)
│   └── criteria/              # Các bộ tiêu chuẩn đã được module hóa
│       └── index.md           # Danh mục các bộ tiêu chuẩn
├── templates/                 # Các biểu mẫu chuẩn cho 8 trụ cột phân tích
├── scripts/                   # Công cụ trích xuất PDF và đóng gói báo cáo
│   ├── 00-summary.md
│   ├── 01-business.md
│   ├── 02-risk-factors.md
│   ├── 03-financial-statements.md
│   ├── 04-mda.md
│   ├── 05-management-governance.md
│   ├── 06-ownership.md
│   ├── 07-exhibits-notes.md
│   └── 08-disclosure-gaps.md
├── scripts/                   # Công cụ trích xuất PDF và đóng gói báo cáo
│   ├── init_company.py        # Khởi tạo thư mục mã công ty, năm & kỳ báo cáo
│   ├── extract_pdf.py         # Trích xuất văn bản & bảng biểu từ PDF
│   └── build_report.py        # Đóng gói thành báo cáo tổng hợp README.md
└── companies/
    └── <TICKER>/              # Ví dụ: VNM, FPT, HPG, VHM, AAPL...
        └── <YEAR>/            # Ví dụ: 2023, 2024...
            ├── FY/            # Báo cáo thường niên cả năm (Chuẩn 10-K)
            │   ├── reports/   # File PDF gốc được đánh dấu chuẩn tên
            │   │   ├── <TICKER>_<YEAR>_FY_Annual-Report.pdf
            │   │   └── <TICKER>_<YEAR>_FY_Audited-FS.pdf
            │   ├── analysis/  # 8 file markdown tương ứng 8 trụ cột phân tích
            │   │   ├── 01-business.md
            │   │   ├── 02-risk-factors.md
            │   │   ├── 03-financial-statements.md
            │   │   ├── 04-mda.md
            │   │   ├── 05-management-governance.md
            │   │   ├── 06-ownership.md
            │   │   ├── 07-exhibits-notes.md
            │   │   └── 08-disclosure-gaps.md
            │   ├── summary.md # Bản tóm tắt điều hành & Bảng Cờ Đỏ
            │   ├── README.md  # Toàn bộ báo cáo phân tích hoàn chỉnh được đóng gói
            │   └── progress.json
            ├── Q1/            # Báo cáo tài chính Quý 1 (Chuẩn 10-Q)
            │   ├── reports/
            │   │   └── <TICKER>_<YEAR>_Q1_Financial-Statements.pdf
            │   ├── summary.md
            │   └── README.md
            ├── Q2/
            ├── Q3/
            └── Q4/
```

### Quy Chuẩn Đặt Tên File (Naming Convention)
Mọi file tài liệu PDF đầu vào trong thư mục `reports/` phải tuân theo cú pháp:  
`[TICKER]_[YEAR]_[PERIOD]_[LOẠI_TÀI_LIỆU].pdf`

- Báo cáo thường niên năm: `VNM_2023_FY_Annual-Report.pdf`
- BCTC kiểm toán cả năm: `VNM_2023_FY_Audited-FS.pdf`
- BCTC hợp nhất quý: `VNM_2024_Q1_Financial-Statements.pdf`
- Giải trình KQKD / Báo cáo ban điều hành quý: `VNM_2024_Q1_Management-Report.pdf`

---

## 2. 8 Trụ Cột Trọng Yếu Của Báo Cáo Phân Tích 10-K

Khi phân tích bất kỳ doanh nghiệp nào, AI **BẮT BUỘC** phải bóc tách số liệu và thông tin theo đúng 8 phần sau:

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

### Trụ Cột 8: Disclosure Gaps & Blind Spots — Khoảng Trống Thông Tin & Điểm Mù Ban Quản Trị (YÊU CẦU ĐẶC BIỆT)
> [!IMPORTANT]
> **Triết lý kiểm toán khắt khe — Thước đo Warren Buffett: Tiêu chuẩn "Tự báo cáo cho bản thân sau một năm đi xa":**  
> *"Báo cáo thường niên lý tưởng là bản báo cáo mà một CEO/người quản lý viết cho chính đối tác sở hữu của mình — nói rõ sự thật những gì họ muốn biết nếu họ ở vị trí ngược lại: Nếu bạn phải đi xa 1 năm, hoàn toàn không biết gì về công ty, khi trở về mở bản báo cáo này ra, bạn có nắm trọn bức tranh thực sự về vận mệnh doanh nghiệp hay không?"*  
> AI phải đóng vai trò **Ban Giám Sát Độc Lập** để đánh giá tổng quan cấu trúc và nội dung báo cáo: **Báo cáo này là một bản tường trình kinh doanh trung thực cho chủ sở hữu hay chỉ là một tập tài liệu PR bóng bẩy "báo công, giấu tội"?**

AI **BẮT BUỘC** phải rà soát cấu trúc báo cáo qua **5 Câu Hỏi Cốt Tử Của Người Vừa Đi Xa Trở Về**:
1. **Vị thế cạnh tranh & Sức khỏe thị phần:** Sau 1 năm, doanh nghiệp đang thực sự mạnh lên hay yếu đi? Khách hàng còn trung thành không? Thị phần tăng hay giảm trước các đối thủ mới nổi? Có dòng sản phẩm nào đang âm thầm suy thoái không?
2. **Sự sòng phẳng khi thừa nhận sai lầm:** Ban điều hành có dám dũng cảm nêu tên các quyết định sai lầm, dự án thất bại, khoản đầu tư thua lỗ trong năm hay chỉ toàn dùng mỹ từ tô hồng ("nỗ lực vượt khó", "kết quả đáng khích lệ")?
3. **Chất lượng dòng tiền & Phân bổ vốn:** Lợi nhuận ghi nhận là "tiền tươi thóc thật" (CFO) hay chỉ nằm trên giấy (bán chịu dồn vào phải thu, hàng ế chất kho)? Tiền thặng dư kiếm được đã được tái đầu tư vào đâu, tỷ suất sinh lời thực tế (ROIC) là bao nhiêu?
4. **Rủi ro sinh tồn & Những quả bom nổ chậm:** Có cam kết nợ vay, covenants tài chính với ngân hàng, kiện tụng pháp lý hay rủi ro đứt gãy khách hàng/nhà cung ứng trọng yếu nào có thể đẩy công ty vào khủng hoảng trong 1-2 năm tới?
5. **Tính trung thực & Đồng cam cộng khổ (Skin in the game):** Ban điều hành có đang cùng chịu rủi ro và hưởng lợi công bằng với cổ đông, hay họ đang tìm cách rút ruột quyền lợi thông qua thù lao cao ngất ngưởng, giao dịch mờ ám với công ty sân sau và phát hành ESOP dễ dãi?

Đồng thời, AI **BẮT BUỘC** phải rà soát và chỉ rõ các điểm mù kỹ thuật sau:
- **Khoảng trống Doanh thu & Biên lợi nhuận:** Công ty có gộp chung doanh thu không? Có bóc tách doanh thu và biên lợi nhuận gộp (Gross Margin) theo từng dòng sản phẩm/SKU hay không? Có tách rõ tăng trưởng đến từ sản lượng (Volume) hay tăng giá bán (Price)? Có công bố tỷ trọng từng kênh phân phối (GT, MT, E-commerce, B2B) không?
- **Khoảng trống Khách hàng & Nhà cung cấp:** Có khách hàng nào chiếm $\ge 10\%$ doanh thu không (theo chuẩn Item 1 của SEC)? Nồng độ phụ thuộc vào nhà cung cấp đơn lẻ ra sao?
- **Khoảng trống Hiệu suất vận hành (Operating Metrics):** Công suất thiết kế và tỷ lệ huy động thực tế (% Utilization Rate) của các nhà máy là bao nhiêu? Các chỉ số Unit Economics (doanh thu/cửa hàng, doanh thu/m2 sàn, giá bán bình quân ASP...) có bị giấu không?
- **Khoảng trống Nợ vay & Covenants:** Lãi suất vay thực tế thả nổi có biên độ bao nhiêu? Các cam kết giao ước tài chính (Debt Covenants) với ngân hàng là gì và công ty có nguy cơ vi phạm không?
- **Khoảng trống Kế hoạch Capex & Phân bổ vốn:** Các dự án lớn dở dang đã giải ngân bao nhiêu, tiến độ thực tế ra sao, tỷ suất sinh lời kỳ vọng (ROIC/IRR) có được công bố sòng phẳng không?
- **Khoảng trống Lương thưởng & KPI Lãnh đạo:** Cơ chế thưởng của Ban Điều hành có gắn với KPI định lượng dài hạn (ROE, EPS, FCF) hay chỉ dựa trên kế hoạch doanh thu ngắn hạn dễ bị thao túng? Điều kiện phát hành ESOP có minh bạch không?
- **Bảng Đánh Giá Đạt Chuẩn "Tự Báo Cáo Cho Bản Thân Sau Một Năm Đi Xa" & Bảng Điểm Minh Bạch (Transparency Scorecard 1-10)** kèm Top 5 Câu Hỏi "Hóc Búa" để chất vấn tại ĐHĐCĐ.

---

## 3. Quy Trình 5 Bước Tự Động Hóa Cho AI Agent

Khi người dùng yêu cầu phân tích một công ty, ví dụ:
> **"Hãy phân tích báo cáo thường niên và BCTC của công ty VNM năm 2023"**  
*(hoặc phân tích một thư mục `companies/<TICKER>/<YEAR>`)*

AI **BẮT BUỘC** kích hoạt quy trình 5 bước sau đây:

### Bước 1: Kiểm Tra Tài Liệu & Cấu Trúc Thư Mục
1. Kiểm tra sự tồn tại của thư mục `companies/<TICKER>/<YEAR>/<PERIOD>/reports/` (mặc định `<PERIOD>` là `FY` nếu phân tích cả năm, hoặc `Q1`-`Q4` nếu phân tích quý).
2. Xác định các file PDF có trong thư mục `reports/` theo quy chuẩn đặt tên:
   - Cả năm: `<TICKER>_<YEAR>_FY_Annual-Report.pdf`, `<TICKER>_<YEAR>_FY_Audited-FS.pdf`.
   - Quý: `<TICKER>_<YEAR>_<PERIOD>_Financial-Statements.pdf`.
3. Nếu thư mục chưa có cấu trúc chuẩn, chạy script khởi tạo:
   ```bash
   python3 scripts/init_company.py --ticker <TICKER> --year <YEAR> --period <PERIOD>
   ```

### Bước 2: Quét Mục Lục & Trích Xuất Dữ Liệu PDF
1. Sử dụng script `scripts/extract_pdf.py` để quét mục lục, tìm trang chứa:
   - Tổng quan công ty & hoạt động kinh doanh (Business)
   - Báo cáo của Ban Giám đốc & HĐQT (MD&A)
   - Báo cáo Tài chính đã kiểm toán (Cân đối kế toán, Kết quả KD, Lưu chuyển tiền tệ, Thuyết minh)
   - Danh sách HĐQT, Ban Giám đốc, cơ cấu cổ đông.
2. Trích xuất text và bảng số liệu từ các dải trang tương ứng để phục vụ phân tích.

### Bước 3: Phân Tích Từng Trụ Cột & Lưu Vào `analysis/`
1. Lần lượt viết 8 file phân tích chi tiết vào `companies/<TICKER>/<YEAR>/<PERIOD>/analysis/`:
   - `01-business.md`
   - `02-risk-factors.md`
   - `03-financial-statements.md`
   - `04-mda.md`
   - `05-management-governance.md`
   - `06-ownership.md`
   - `07-exhibits-notes.md`
   - `08-disclosure-gaps.md`
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
   - **Đánh giá Mức độ Minh bạch & Khoảng trống thông tin trọng yếu (Disclosure Gaps).**
   - Kết luận & Góc nhìn đầu tư theo phong cách 10-K/10-Q.
2. Chạy script đóng gói báo cáo hoàn chỉnh:
   ```bash
   python3 scripts/build_report.py --ticker <TICKER> --year <YEAR> --period <PERIOD>
   ```
   Script này sẽ tổng hợp `summary.md`, toàn bộ 8 file chuẩn trong `analysis/` và bất kỳ file phụ lục giải thích bổ sung nào (`09-appendix-*.md`) thành một file `companies/<TICKER>/<YEAR>/<PERIOD>/README.md` duy nhất, chuẩn mực.

### Bước 4.1: Tạo File Giải Thích Chuyên Sâu (Khi Người Dùng Yêu Cầu Đào Sâu)
Khi người dùng đặt câu hỏi giải thích thêm hoặc đào sâu về một cơ chế kế toán, tài chính đặc thù (dự phòng rủi ro, xóa nợ ngoại bảng, khấu hao, dòng tiền, M&A...):
1. **Tạo file phụ lục:** Tạo file `companies/<TICKER>/<YEAR>/<PERIOD>/analysis/09-appendix-<tên-chủ-đề>.md` (hoặc `10-...` nếu đã có).
2. **Nội dung:** Giải thích cặn kẽ bản chất nghiệp vụ, nguyên lý kế toán kép ($Assets = Liabilities + Equity$), liên hệ bảng số liệu thực tế của doanh nghiệp, và đánh giá tác động rủi ro/cơ hội.
3. **Đóng gói lại:** Chạy lại `python3 scripts/build_report.py --ticker <TICKER> --year <YEAR> --period <PERIOD>` để tự động tích hợp phụ lục vào cuối báo cáo `README.md`.

### Bước 5: Tự Động Commit & Push Git Sau Khi Hoàn Thành Task
> [!NOTE]
> **Quy Tắc Đặc Thù Riêng Của Project (Project-Specific Rule):**  
> Trong dự án `pdf-analyzer`, AI được phép **tự động chạy lệnh `git add`, `git commit` và `git push`** sau khi hoàn thành việc phân tích, đóng gói báo cáo hoặc cập nhật tài liệu để đồng bộ ngay lập tức lên GitHub repository mà không cần đợi người dùng phải xác nhận thủ công từng lần.

1. **Thực hiện lệnh git tự động:**
   ```bash
   git add companies/<TICKER>/<YEAR>/<PERIOD>/
   git commit -m "feat(analysis): hoàn thành phân tích 10-K <TICKER> <PERIOD> <YEAR>"
   git push
   ```
2. **Quy tắc an toàn:** Chỉ add và commit các file tài liệu/báo cáo phân tích hợp lệ, không commit các file rác, file tạm thừa hoặc thông tin bảo mật/credentials.
3. **Phản hồi kết quả:** Khi hoàn thành, báo cáo phản hồi kết quả cho người dùng theo đúng cấu trúc chuẩn kèm đường dẫn tới các file đã tạo và thông báo trạng thái push Git thành công.

---

## 4. Phong Cách Báo Cáo Phản Hồi

- Khách quan, trung lập, bám sát số liệu thực tế, không dự đoán chủ quan hay đưa ra lời khuyên đầu tư tài chính trực tiếp.
- Trình bày mạch lạc, bảng biểu rõ ràng, sử dụng bullet points sắc bén.
- Báo cáo phản hồi khi hoàn thành lệnh:
  ```markdown
  Đã hoàn thành phân tích cho **[TÊN CÔNG TY] ([TICKER]) - Kỳ [PERIOD] Năm [YEAR]**
  - Thư mục báo cáo: `companies/<TICKER>/<YEAR>/<PERIOD>/`
  - 8 Trụ cột phân tích chi tiết: `companies/<TICKER>/<YEAR>/<PERIOD>/analysis/`
  - Báo cáo tóm tắt điều hành: `companies/<TICKER>/<YEAR>/<PERIOD>/summary.md`
  - Toàn văn báo cáo tổng hợp: `companies/<TICKER>/<YEAR>/<PERIOD>/README.md`
  ```
