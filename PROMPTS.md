# 📋 TỔNG HỢP CÁC MẪU PROMPT CHUẨN ĐỂ RA LỆNH CHO AI AGENT

Tài liệu này chứa các mẫu prompt tổng quát được tối ưu hóa cho **2 Nhiệm Vụ Cốt Lõi** của hệ thống và **Nhiệm Vụ Kết Hợp (Chấm điểm đối chiếu)**. Bạn chỉ cần sao chép, thay đổi các thông tin trong ngoặc vuông `[...]` và gửi cho AI.

---

## 🏛️ NHIỆM VỤ 1: Phân Tích Doanh Nghiệp Theo Chuẩn 10-K (10k-analyzer)

> **Mục tiêu:** Tiếp nhận Báo Cáo Thường Niên & BCTC dạng PDF, bóc tách 8 trụ cột 10-K, nhận diện Cờ Đỏ (Red Flags), dòng tiền và kiểm toán khoảng trống thông tin theo chuẩn Warren Buffett ("Tự báo cáo cho bản thân sau 1 năm đi xa").

### 🔹 Cách 1: Prompt Ngắn Gọn (Quick Command - Khuyên dùng)
```text
Hãy phân tích báo cáo thường niên và BCTC của công ty [MÃ_CỔ_PHIẾU] năm [NĂM] kỳ [FY / Q1 / Q2 / Q3 / Q4].
```
*Ví dụ:*  
> `Hãy phân tích báo cáo thường niên và BCTC của công ty MBB năm 2025 kỳ FY.`  
> `Hãy phân tích BCTC của công ty FPT năm 2024 kỳ Q3.`

---

### 🔹 Cách 2: Prompt Toàn Diện & Tùy Biến Chuyên Sâu (Deep-Dive Prompt)
```text
Hãy kích hoạt skill 10k-analyzer để phân tích toàn diện công ty [MÃ_CỔ_PHIẾU] ([TÊN_CÔNG_TY]) cho kỳ [FY / Q1-Q4] năm [NĂM].

Yêu cầu thực hiện:
1. Tải hoặc sử dụng tài liệu PDF trong thư mục companies/[MÃ_CỔ_PHIẾU]/[NĂM]/[KỲ]/reports/
2. Bóc tách đầy đủ 8 trụ cột 10-K vào thư mục analysis/ (Business, Risk Factors, Financial Statements, MD&A, Governance, Ownership, Footnotes, Disclosure Gaps).
3. Đánh giá chất lượng dòng tiền (CFO vs Net Income), nhận diện các dấu hiệu Cờ Đỏ (Red Flags), và đặc biệt chú ý đến: [VẤN_ĐỀ_CẦN_SOI_KỸ - ví dụ: nợ bất động sản, giao dịch bên liên quan, trái phiếu...].
4. Đánh giá tính minh bạch theo tiêu chuẩn Warren Buffett ("Tự báo cáo cho bản thân sau 1 năm đi xa") và đề xuất Top 5 câu hỏi chất vấn tại ĐHĐCĐ.
5. Soạn summary.md, đóng gói thành README.md hoàn chỉnh và cập nhật progress.json.
```

---

## 🎯 NHIỆM VỤ 2: Trích Xuất Tiêu Chuẩn Doanh Nghiệp Tốt (criteria-extractor)

> **Mục tiêu:** Tiếp nhận bài viết, bài nói chuyện, sách, tài liệu phân tích (PDF hoặc Markdown), trích xuất thành Bộ Tiêu Chuẩn Doanh Nghiệp Xuất Sắc gồm cả Định lượng BCTC, Định tính (Con hào kinh tế) và Lợi thế thể chế/Quan hệ chính phủ.

### 🔹 Cách 1: Prompt Ngắn Gọn (Quick Command)
```text
Hãy trích xuất các tiêu chuẩn và đặc điểm của một công ty tốt từ tài liệu [ĐƯỜNG_DẪN_HOẶC_TÊN_FILE_PDF_MD].
```
*Ví dụ:*  
> `Hãy trích xuất các tiêu chuẩn và đặc điểm của một công ty tốt từ tài liệu frameworks/sources/buffett_owner_earnings.pdf`  
> `Hãy trích xuất tiêu chuẩn doanh nghiệp từ bài viết đính kèm này.`

---

### 🔹 Cách 2: Prompt Toàn Diện & Đầy Đủ Khía Cạnh (Full Framework Prompt)
```text
Hãy kích hoạt skill criteria-extractor để phân tích và trích xuất Bộ Tiêu Chuẩn Doanh Nghiệp Tốt từ tài liệu:
- Nguồn tài liệu: [ĐƯỜNG_DẪN_FILE_HOẶC_LIÊN_KẾT]
- Tác giả / Trường phái: [TÊN_TÁC_GIẢ / VÍ DỤ: Warren Buffett, Terry Smith, Charlie Munger, Chuyên gia ngành...]
- Tên bộ tiêu chuẩn đặt là: [TÊN_FRAMEWORK - ví dụ: pricing-power-and-moat]

Yêu cầu bóc tách tài liệu thành 5 khía cạnh hành động trong file frameworks/criteria/[TÊN_FRAMEWORK].md:
1. Triết lý cốt lõi: Định nghĩa thế nào là một doanh nghiệp vĩ đại vs tầm thường theo quan điểm của tác giả.
2. Tiêu chí Định lượng BCTC: Ngưỡng sàn tài chính cụ thể (ROIC, ROE, FCF/Net Income, Biên lợi nhuận, Đòn bẩy nợ).
3. Tiêu chí Định tính & Con hào kinh tế: Quyền lực định giá (Pricing power), Chi phí chuyển đổi (Switching cost), Hiệu ứng mạng lưới, Tính chính trực và năng lực phân bổ vốn của Ban Lãnh đạo.
4. Lợi thế Thể chế & Vốn chính trị: Mức độ gắn kết với lợi ích quốc gia, sự ủng hộ/bảo hộ từ chính sách, giấy phép độc quyền và quan hệ bền vững với Chính phủ.
5. Bộ câu hỏi sàng lọc thực chiến (Screening Checklist Yes/No) và danh sách các Cờ Đỏ loại trừ (Deal-Breakers).
Cập nhật danh mục tại frameworks/criteria/index.md sau khi hoàn thành.
```

---

## 🌉 NHIỆM VỤ KẾT HỢP: Chấm Điểm Đối Chiếu Doanh Nghiệp (The Scorecard)

> **Mục tiêu:** Lấy kết quả 8 trụ cột của một công ty (từ Nhiệm vụ 1) đối chiếu với Bộ Tiêu Chuẩn đã trích xuất (từ Nhiệm vụ 2) để kết luận công ty có đạt chuẩn đầu tư hay không.

### 🔹 Prompt Chấm Điểm & Đối Chiếu (Evaluation & Scorecard)
```text
Hãy đối chiếu và chấm điểm công ty [MÃ_CỔ_PHIẾU] kỳ [KỲ] năm [NĂM] theo Bộ Tiêu Chuẩn [TÊN_BỘ_TIÊU_CHUẨN].

Yêu cầu thực hiện:
1. Đọc báo cáo 8 trụ cột đã phân tích tại: companies/[MÃ_CỔ_PHIẾU]/[NĂM]/[KỲ]/README.md
2. Đọc bộ tiêu chuẩn tại: frameworks/criteria/[TÊN_BỘ_TIÊU_CHUẨN].md
3. Tạo file đánh giá companies/[MÃ_CỔ_PHIẾU]/[NĂM]/[KỲ]/scorecard_[TÊN_BỘ_TIÊU_CHUẨN].md gồm:
   - Bảng chấm điểm từng tiêu chí (Định lượng, Con hào kinh tế, Quan hệ thể chế/chính phủ).
   - Đánh dấu: [ĐẠT / KHÔNG ĐẠT / CẦN THEO DÕI THÊM] kèm dẫn chứng số liệu cụ thể.
   - Kết luận: Doanh nghiệp này đáp ứng được bao nhiêu % tiêu chuẩn của trường phái đầu tư trên?
```
*Ví dụ:*  
> `Hãy đối chiếu và chấm điểm công ty MBB kỳ FY năm 2025 theo Bộ Tiêu Chuẩn buffett-munger-standard.`  
> `Hãy chấm điểm công ty REE theo bộ tiêu chuẩn regulatory-political-capital.`

---

## 💡 Mẹo Sử Dụng Hiệu Quả
1. Bạn có thể kéo-thả trực tiếp file PDF vào cửa sổ chat và gửi kèm câu lệnh ngắn gọn.
2. Với các file PDF dung lượng lớn, hãy lưu vào thư mục `reports/` hoặc `sources/` rồi chỉ định đường dẫn để AI xử lý tốc độ cao nhất.
3. Sau khi hoàn thành bất kỳ nhiệm vụ nào, bạn có thể yêu cầu AI: *"Hãy commit và push git các file này"* để đồng bộ lên GitHub.
