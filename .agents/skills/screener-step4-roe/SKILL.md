---
name: screener-step4-roe
description: Bước 4 trong phễu lọc cổ phiếu - Sàng lọc Hiệu Quả Sử Dụng Vốn (ROE). Loại bỏ các doanh nghiệp có tỷ suất sinh lời trên vốn chủ sở hữu (ROE) dưới 10% trong suốt 5 năm tài chính liên tục; nếu vượt qua thì đưa vào file thứ 5.
---

# Screener Step 4: Sàng Lọc Hiệu Quả Vốn ROE 5 Năm & Tốt Nghiệp Phễu Lọc

Kỹ năng này hướng dẫn AI Agent thực hiện **Bước 4** trong phễu lọc doanh nghiệp: Kiểm tra hiệu quả sinh lời dài hạn trên đồng vốn của cổ đông. Loại bỏ các cỗ máy đốt vốn kém hiệu quả có **ROE < 10% trong suốt 5 năm liên tục**. Nếu doanh nghiệp vượt qua bước này, chính thức đưa vào **File thứ 5 (`05-passed-champions.md`)** với bản giải trình toàn diện lý do chiến thắng cả 4 vòng.

---

## 1. Tiêu Chí Sàng Lọc Bước 4

### A. Quy Tắc Loại Trừ (Trượt Bước 4)
- Doanh nghiệp có chỉ số **$ROE < 10\%$ trong toàn bộ 5 năm tài chính liên tiếp gần nhất** (từ năm $N-4$ đến năm $N$).
- *Ý nghĩa:* Doanh nghiệp không tạo ra mức sinh lời vượt trội hơn chi phí cơ hội của vốn (thường lãi suất phi rủi ro + bù đắp lạm phát là 7-9%). Nếu 5 năm liên tục ROE đều dưới 10%, đây là doanh nghiệp thâm dụng vốn hoặc Ban Lãnh đạo không biết cách phân bổ vốn hiệu quả.
- **👉 HÀNH ĐỘNG: Ghi vào `screenings/04-rejected-low-roe.md`. Dừng phân tích.**

### B. Điều Kiện Vượt Qua Cả Phễu Lọc (Tốt Nghiệp Vào File Thứ 5)
- Doanh nghiệp có **ROE $\ge 10\%$ ở một hoặc nhiều năm** trong chu kỳ 5 năm (lý tưởng nhất là duy trì bền vững $> 15\% - 20\%$).
- **👉 HÀNH ĐỘNG: Ghi danh vào `screenings/05-passed-champions.md`.**  
  Tổng hợp bản giải trình nêu rõ lý do tại sao công ty vượt qua từng bước trong cả 4 bước.

---

## 2. Quy Trình Thực Hiện

1. **Thu thập chuỗi số liệu ROE 5 năm gần nhất:**
   - Lấy $ROE = \frac{\text{Lợi nhuận sau thuế của công ty mẹ}}{\text{Vốn chủ sở hữu bình quân}}$ trong 5 năm liên tiếp.
2. **Đối chiếu với ngưỡng 10%:**
   - Lập bảng 5 năm: Năm $N-4, N-3, N-2, N-1, N$.
   - Kiểm tra xem có năm nào $\ge 10\%$ hay không.
3. **Kết luận & Xử lý:**
   - **Nếu cả 5 năm đều < 10%:** Ghi vào `screenings/04-rejected-low-roe.md`.
   - **Nếu vượt qua:** Ghi vào `screenings/05-passed-champions.md` kèm tóm tắt 4 trụ cột chiến thắng:
     * *Vòng 1:* Ngành nghề dễ hiểu / Lợi thế tài nguyên đặc thù.
     * *Vòng 2:* Lợi nhuận dương vững chắc, không lỗ 3 năm.
     * *Vòng 3:* Sản phẩm độc đáo, giá trị gia tăng cao (hoặc P/B < 0.5).
     * *Vòng 4:* ROE sinh lời hiệu quả trên vốn.

---

## 3. Mẫu Trình Bày Khi Công Ty Bị Loại (Ghi vào File 4)

```markdown
### ❌ [TICKER] - [Tên Doanh Nghiệp]
- **Ngành nghề:** [Tên ngành]
- **Chuỗi chỉ số ROE 5 năm gần nhất:**
  | Năm | Vốn chủ sở hữu (Tỷ VNĐ) | LNST (Tỷ VNĐ) | ROE (%) | Trạng thái (< 10%) |
  | :---: | :---: | :---: | :---: | :---: |
  | [Năm N-4] | [Số liệu] | [Số liệu] | [X.X%] | Dưới chuẩn |
  | [Năm N-3] | [Số liệu] | [Số liệu] | [X.X%] | Dưới chuẩn |
  | [Năm N-2] | [Số liệu] | [Số liệu] | [X.X%] | Dưới chuẩn |
  | [Năm N-1] | [Số liệu] | [Số liệu] | [X.X%] | Dưới chuẩn |
  | [Năm N]   | [Số liệu] | [Số liệu] | [X.X%] | Dưới chuẩn |
- **ROE trung bình 5 năm:** [Y.Y%]
- **Lý do bị loại:** Hiệu quả sử dụng vốn trên vốn chủ sở hữu (ROE) ở mức thấp dưới 10% trong suốt 5 năm tài chính liên tục ([N-4] đến [N]). Doanh nghiệp không tạo ra tỷ suất sinh lời hấp dẫn để bù đắp chi phí vốn cổ đông.
- **Ngày sàng lọc:** [YYYY-MM-DD]
```

---

## 4. Mẫu Trình Bày Khi Vượt Qua Toàn Bộ (Ghi vào File 5)

```markdown
### 🏆 [TICKER] - [Tên Doanh Nghiệp]
- **Vị thế ngành:** [Mô tả vị thế doanh nghiệp]
- **Tổng quan chỉ số chính:** P/E: [X] | P/B: [Y] | ROE gần nhất: [Z]% | Tăng trưởng DT/LN: [%]

#### Lý Do Vượt Qua Toàn Bộ 4 Bước Sàng Lọc:
1. **Bước 1 (Vòng tròn năng lực & Ngành nghề):** [Ghi rõ lý do: ví dụ thuộc ngành hàng thiết yếu dễ hiểu / hoặc sở hữu tài nguyên mỏ đá/TTTM độc quyền].
2. **Bước 2 (Sức khỏe lợi nhuận 3 năm):** [Ghi rõ số liệu: LNST dương liên tục 3 năm gần nhất, dòng tiền cốt lõi lành mạnh].
3. **Bước 3 (Chuỗi giá trị gia tăng & P/B):** [Ghi rõ: Sản phẩm có thương hiệu mạnh, biên lãi gộp đạt X% / hoặc hàng gia công nhưng định giá P/B siêu rẻ Y < 0.5].
4. **Bước 4 (Hiệu quả sử dụng vốn ROE 5 năm):** [Ghi rõ: ROE duy trì xuất sắc, trung bình 5 năm đạt X% (cao hơn nhiều so với ngưỡng sàn 10%)].

- **Hành động tiếp theo:** Đưa vào Danh mục Theo dõi Đầu tư (Watchlist) và tiến hành phân tích sâu 8 trụ cột 10-K.
- **Ngày tốt nghiệp phễu:** [YYYY-MM-DD]
```
