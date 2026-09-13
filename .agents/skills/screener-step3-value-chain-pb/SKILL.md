---
name: screener-step3-value-chain-pb
description: Bước 3 trong phễu lọc cổ phiếu - Sàng lọc Chuỗi Giá Trị & Ngoại Lệ Định Giá P/B. Loại bỏ doanh nghiệp gia công, sản phẩm không độc đáo ở đáy chuỗi giá trị gia tăng TRỪ KHI định giá P/B < 0.5 (rẻ hơn một nửa giá trị sổ sách).
---

# Screener Step 3: Sàng Lọc Chuỗi Giá Trị & Ngoại Lệ Định Giá P/B

Kỹ năng này hướng dẫn AI Agent thực hiện **Bước 3** trong phễu lọc: Đánh giá vị thế cạnh tranh và quyền lực kinh tế của sản phẩm trong chuỗi giá trị gia tăng. Loại bỏ các doanh nghiệp làm công việc gia công thuần túy, sản phẩm đại trà dễ thay thế, **TRỪ TRƯỜNG HỢP** cổ phiếu đang được định giá siêu rẻ với **$P/B < 0.5$** (mua tài sản dưới nửa giá trị sổ sách).

---

## 1. Tiêu Chí Sàng Lọc Bước 3

### A. Đánh Giá Bản Chất Sản Phẩm & Chuỗi Giá Trị
1. **Sản phẩm Độc Đáo / Vị Thế Cao Trong Chuỗi Giá Trị (ĐẠT NGAY):**
   - Sở hữu thương hiệu mạnh người tiêu dùng tự tìm mua (ví dụ: Vinamilk, Dược Hậu Giang, FPT...).
   - Có quyền lực định giá (Pricing Power): Có thể tăng giá bán khi lạm phát mà không mất thị phần.
   - Biên lợi nhuận gộp cao và ổn định (thường $> 25\% - 30\%$).
   - Nắm giữ kênh phân phối độc quyền hoặc công nghệ lõi.
   - **👉 HÀNH ĐỘNG: VƯỢT QUA BƯỚC 3 (Đi tiếp sang Bước 4 mà không cần xét P/B).**

2. **Sản phẩm Không Độc Đáo / Nằm Ở Đáy Chuỗi Giá Trị Gia Tăng:**
   - Hoạt động gia công thuần túy (CMT dệt may, lắp ráp điện tử OEM không có thương hiệu riêng).
   - Xuất khẩu nguyên liệu thô / sơ chế nông thủy sản đại trà, phụ thuộc hoàn toàn vào giá thế giới.
   - Biên lợi nhuận gộp rất mỏng (thường $< 10\% - 12\%$).
   - Khách hàng (bên đặt gia công) có thể dễ dàng chuyển đơn hàng sang các nước có nhân công rẻ hơn (Bangladesh, Ấn Độ...).
   - **👉 HÀNH ĐỘNG: BẮT BUỘC KIỂM TRA ĐIỀU KIỆN $P/B$ (Xem phần B).**

---

### B. Điều Kiện Ngoại Lệ P/B (Đối Với Sản Phẩm Chuỗi Giá Trị Thấp)

- **Nếu $P/B < 0.5$:**  
  👉 **GIỮ LẠI (VƯỢT QUA BƯỚC 3).**  
  *Lý do:* Theo triết lý Ben Graham (Net-Net / Deep Value), mặc dù công ty gia công biên mỏng, nhưng thị trường đang bán công ty với giá chiết khấu hơn 50% so với giá trị sổ sách (vốn chủ sở hữu), tạo ra một "biên an toàn tài sản" đáng kể.
  
- **Nếu $P/B \ge 0.5$:**  
  👉 **LOẠI BỎ NGAY LẬP TỨC (Trượt Bước 3).**  
  *Lý do:* Sản phẩm không có hào kinh tế, biên mỏng, nhưng giá cổ phiếu không đủ rẻ để bù đắp rủi ro mô hình kinh doanh cấp thấp. Ghi vào `screenings/03-rejected-low-value-chain.md`.

---

## 2. Quy Trình Thực Hiện

1. **Phân tích mô hình sản phẩm & biên lợi nhuận:**
   - Xem mục *01-business.md* và *03-financial-statements.md* (Biên lãi gộp Gross Margin 3 năm gần nhất).
   - Xác định xem công ty tự làm thương hiệu (OBM/ODM) hay chỉ đi gia công thuê (OEM/CMT).
2. **Kiểm tra chỉ số định giá $P/B$:**
   - Lấy giá thị trường hiện tại (hoặc giá đóng cửa kỳ báo cáo) chia cho Giá trị sổ sách mỗi cổ phiếu ($BVPS$).
3. **Kết luận & Xử lý:**
   - Nếu sản phẩm độc đáo / giá trị cao: Cho qua Bước 4.
   - Nếu sản phẩm chuỗi giá trị thấp & $P/B < 0.5$: Cho qua Bước 4 (kèm ghi chú ngoại lệ $P/B$).
   - Nếu sản phẩm chuỗi giá trị thấp & $P/B \ge 0.5$: Ghi vào `screenings/03-rejected-low-value-chain.md`. **Dừng phân tích.**

---

## 3. Mẫu Trình Bày Khi Công Ty Bị Loại (Ghi vào File 3)

```markdown
### ❌ [TICKER] - [Tên Doanh Nghiệp]
- **Vị thế chuỗi giá trị:** Sản phẩm đại trà / Gia công giá trị gia tăng thấp ([Mô tả cụ thể])
- **Biên lợi nhuận gộp (Gross Margin):** Trung bình [X]% (quá mỏng, không có quyền lực định giá)
- **Định giá P/B thực tế:** [Y] lần (Điều kiện giữ lại: phải < 0.5)
- **Lý do bị loại:** Sản phẩm nằm ở phần thấp của chuỗi giá trị gia tăng (chủ yếu làm gia công/sơ chế thô), biên lợi nhuận dễ bị tổn thương khi chi phí đầu vào tăng, đồng thời định giá P/B không đạt điều kiện chiết khấu sâu (< 0.5) để có biên an toàn tài sản.
- **Ngày sàng lọc:** [YYYY-MM-DD]
```

## 4. Mẫu Trình Bày Khi Vượt Qua / Ngoại Lệ
- **Trường hợp 1 (Sản phẩm độc đáo):** ĐẠT BƯỚC 3. Ghi chú: [Sở hữu thương hiệu top đầu / Biên lãi gộp đạt X%].
- **Trường hợp 2 (Ngoại lệ P/B < 0.5):** ĐẠT BƯỚC 3 THEO NGOẠI LỆ ĐỊNH GIÁ. Ghi chú: [Hàng gia công nhưng P/B = 0.38 < 0.5, tài sản tiền mặt ròng lớn].
