---
name: criteria-extractor
description: Trích xuất các tiêu chuẩn, đặc điểm của một doanh nghiệp tốt/xuất sắc từ bài viết, bài nói chuyện, tài liệu phân tích (dạng PDF hoặc Markdown) để xây dựng khung đánh giá doanh nghiệp (bao gồm cả chỉ số định lượng BCTC/BCTN và đặc điểm định tính như con hào kinh tế, quan hệ chính phủ).
---

# Criteria Extractor Skill — Trích Xuất Bộ Tiêu Chuẩn Doanh Nghiệp Tinh Hoa

Skill này hướng dẫn AI Agent tiếp nhận các tài liệu đúc kết tri thức (bài nói chuyện, bài viết, sách, bài luận, podcast transcript dưới dạng PDF hoặc Markdown) từ các nhà đầu tư lớn, chuyên gia hoặc người dùng cung cấp; sau đó bóc tách thành **Bộ Tiêu Chuẩn Doanh Nghiệp Có Thể Kiểm Chứng (Actionable Investment Criteria & Rubrics)**.

---

## 1. Các Trường Hợp Kích Hoạt
- Người dùng cung cấp một file PDF hoặc Markdown (bài viết, bài phân tích, thư gửi cổ đông, bài phỏng vấn lãnh đạo/chuyên gia) và yêu cầu: *"Hãy trích xuất tiêu chuẩn/đặc điểm của một công ty tốt từ tài liệu này"*.
- Người dùng yêu cầu tạo khung đánh giá doanh nghiệp theo một chủ đề cụ thể (ví dụ: "Tiêu chuẩn con hào kinh tế", "Tiêu chí doanh nghiệp có lợi thế quan hệ chính phủ/thể chế", "Bộ lọc cổ phiếu tăng trưởng bền vững"...).
- Người dùng yêu cầu đối chiếu một công ty đã phân tích (trong thư mục `companies/`) với bộ tiêu chuẩn đã được trích xuất.

---

## 2. Cấu Trúc Lưu Trữ Trong Repository

```text
frameworks/
├── sources/               # Chứa các file tài liệu gốc (PDF hoặc MD)
│   ├── <TÊN_TÀI_LIỆU>.pdf
│   └── <TÊN_TÀI_LIỆU>.md
└── criteria/              # Chứa các bộ tiêu chuẩn markdown đã trích xuất hoàn chỉnh
    ├── <TÊN_FRAMEWORK>.md
    └── index.md           # Danh mục tổng hợp các bộ tiêu chuẩn đang có
```

---

## 3. Quy Trình 4 Bước Trích Xuất Tiêu Chuẩn

### Bước 1: Tiếp Nhận & Đọc Tài Liệu Nguồn
1. Đảm bảo file tài liệu được lưu trong `frameworks/sources/` theo tên gợi nhớ:  
   Ví dụ: `frameworks/sources/buffett_owner_earnings.pdf`, `frameworks/sources/government_relations_moat.md`.
2. Nếu là file PDF: Sử dụng `scripts/extract_pdf.py` hoặc thư viện PyMuPDF (`fitz`) để trích xuất toàn bộ văn bản.
3. Nếu là file Markdown / Text: Sử dụng `view_file` để nắm bắt trọn vẹn nội dung.

### Bước 2: Bóc Tách Thành 5 Khía Cạnh Cốt Lõi
AI **BẮT BUỘC** phân loại và trích xuất thông tin từ tài liệu thành 5 phần tiêu chuẩn:

#### Khía cạnh 1: Triết Lý Cốt Lõi & Bản Chất Của Doanh Nghiệp Tốt (Core Philosophy)
- Định nghĩa của tác giả về một doanh nghiệp xuất sắc (Great Company vs Good Company vs Mediocre Company).
- Tư duy về thời gian nắm giữ, định giá hợp lý và nguyên tắc bảo vệ vốn.

#### Khía cạnh 2: Bộ Tiêu Chí Định Lượng & Ngưỡng Sàn Tài Chính (Quantitative Metrics)
- **Hiệu quả sử dụng vốn:** ROIC, ROE, ROA (ngưỡng tối thiểu là bao nhiêu, duy trì trong bao nhiêu năm).
- **Chất lượng dòng tiền:** Dòng tiền tự do (FCF / Net Income), tỷ lệ chuyển đổi lợi nhuận thành tiền mặt, vốn tái đầu tư (Capex / CFO).
- **Biên lợi nhuận:** Biên lãi gộp (Gross Margin), biên lãi ròng (Net Margin) có duy trì ổn định qua các chu kỳ suy thoái không.
- **Đòn bẩy tài chính & Bảng cân đối:** Nợ vay ròng / EBITDA, hệ số thanh toán lãi vay, rủi ro nợ ngắn hạn.

#### Khía cạnh 3: Bộ Tiêu Chí Định Tính & Con Hào Kinh Tế (Qualitative Moats)
- **Quyền lực định giá (Pricing Power):** Doanh nghiệp có thể tăng giá vượt lạm phát mà khách hàng không bỏ đi không?
- **Chi phí chuyển đổi (High Switching Costs):** Khách hàng có dễ dàng chuyển sang đối thủ không?
- **Hiệu ứng mạng lưới (Network Effects) & Lợi thế chi phí thấp bền vững.**
- **Phẩm chất Ban Lãnh đạo:** Tính chính trực, khả năng phân bổ vốn (Capital Allocation), sự sòng phẳng khi thừa nhận sai lầm và Skin in the Game.

#### Khía cạnh 4: Lợi Thế Thể Chế & Vốn Chính Trị (Regulatory Moat & Government Relations)
*(Rất trọng yếu đối với thị trường mới nổi như Việt Nam)*
- **Sự gắn kết với Lợi ích Quốc gia (Alignment with National Strategy):** Doanh nghiệp có kinh doanh đúng các ngành nghề trọng điểm được Nhà nước khuyến khích/bảo hộ (hạ tầng, năng lượng, chuyển đổi số, an ninh lương thực, quốc phòng)?
- **Rào cản pháp lý & Giấy phép độc quyền (Licenses & Concessions):** Doanh nghiệp có sở hữu những tài nguyên, vị trí cảng biển, mạng lưới phân phối hay giấy phép khai thác mà đối thủ mới không thể có được không?
- **Khả năng điều hướng chính sách:** Ban Lãnh đạo có tiếng nói phản biện xã hội, có uy tín và mối quan hệ bền vững, chính thống với các cơ quan quản lý hay không?

#### Khía cạnh 5: Bộ Câu Hỏi Sàng Lọc Thực Chiến (Screening Checklist & Red Flags)
- Bảng 10 - 15 câu hỏi nhị phân (Đạt / Không đạt) kèm hướng dẫn nguồn kiểm chứng (Lấy từ BCTN, BCTC hay Thuyết minh).
- Danh sách **Cờ Đỏ (Deal-Breakers):** Những dấu hiệu xấu khiến doanh nghiệp bị loại ngay lập tức bất kể giá rẻ.

### Bước 3: Lưu Trữ Bộ Tiêu Chuẩn
Lưu kết quả phân tích vào file:  
`frameworks/criteria/<TÊN_TIÊU_CHUẨN>.md`  
Cập nhật danh mục tại `frameworks/criteria/index.md`.

### Bước 4: (Tùy Chọn) Đối Chiếu Chấm Điểm Doanh Nghiệp
Khi người dùng yêu cầu: *"Hãy đối chiếu công ty [TICKER] với tiêu chuẩn này"*:
1. Đọc báo cáo 8 trụ cột của công ty tại `companies/<TICKER>/<YEAR>/<PERIOD>/README.md`.
2. Tạo file `companies/<TICKER>/<YEAR>/<PERIOD>/scorecard.md` chấm điểm chi tiết từng tiêu chí (Đạt / Không đạt / Cần theo dõi thêm) kèm số liệu minh chứng thực tế.

---

## 4. Tiêu Chuẩn Phản Hồi
- Trình bày mạch lạc, bảng biểu đối chiếu rõ ràng.
- Mọi tiêu chí định tính phải được cụ thể hóa thành các câu hỏi "có thể kiểm chứng" qua hành vi thực tế của doanh nghiệp, không suy đoán cảm tính.
