---
name: screener-step1-industry
description: Bước 1 trong phễu lọc cổ phiếu - Sàng lọc Vòng Tròn Năng Lực & Ngành Nghề Đặc Thù. Loại bỏ bất động sản, xây dựng, VLXD đại trà, cho thuê BĐS thông thường; ghi nhận và giữ lại các ca đặc thù (mỏ đá độc quyền, TTTM vị trí vàng).
---

# Screener Step 1: Sàng Lọc Vòng Tròn Năng Lực & Ngành Nghề Đặc Thù

Kỹ năng này hướng dẫn AI Agent thực hiện **Bước 1** trong phễu lọc doanh nghiệp: Loại bỏ các ngành nghề có tính chu kỳ cao, khó dự phóng dòng tiền hoặc nằm ngoài vòng tròn năng lực (bất động sản, xây dựng, vật liệu xây dựng thông thường, cho thuê thương mại đại trà), đồng thời phân loại kỹ các trường hợp **Đặc thù có lợi thế độc quyền** để cho phép đi tiếp.

---

## 1. Tiêu Chí Sàng Lọc Bước 1

### A. Nhóm Bị LOẠI Ngay Lập Tức (Trượt Bước 1)
- **Bất động sản dân dụng/nghỉ dưỡng đại trà:** Các công ty phát triển dự án nhà ở, đất nền, khu nghỉ dưỡng phụ thuộc vào cấp phép pháp lý, đòn bẩy tài chính cao, chu kỳ đóng băng thanh khoản khó lường (ví dụ: NVL, PDR, DIG, DXG...).
- **Xây dựng & Nhà thầu dân dụng/công nghiệp thông thường:** Các công ty tổng thầu xây lắp biên lợi nhuận mỏng (thường < 5%), công nợ đọng lớn từ chủ đầu tư, rủi ro bảo lãnh thực hiện hợp đồng cao.
- **Vật liệu xây dựng (VLXD) đại trà:** Sản xuất xi măng, gạch ngói, sắt thép đại trà không có mỏ nguyên liệu độc quyền hay rào cản công nghệ (hàng hóa commodity thuần túy).
- **Cho thuê BĐS thông thường:** Các công ty cho thuê kho bãi, văn phòng thứ cấp không có rào cản cạnh tranh, khách thuê dễ dàng chuyển đổi địa điểm.

### B. NGOẠI LỆ ĐẶC BIỆT — Được Giữ Lại (VƯỢT QUA Bước 1)
Nếu doanh nghiệp thuộc các ngành trên nhưng sở hữu **Lợi Thế Địa Lý / Tài Nguyên Độc Quyền** không thể thay thế, AI **BẮT BUỘC NOTE RÕ** và cho phép đi tiếp vào Bước 2:
1. **Sở hữu Mỏ Đá / Khoáng sản đặc thù:** Doanh nghiệp sở hữu mỏ đá có giấy phép khai thác dài hạn nằm ngay cạnh các đại dự án hạ tầng (sân bay Long Thành, cao tốc Bắc - Nam), trữ lượng lớn, chi phí vận chuyển thấp hơn hẳn đối thủ (ví dụ: DHA, VLB...).
2. **Độc quyền Trung tâm thương mại / Bất động sản bán lẻ vị trí kim cương:** Doanh nghiệp sở hữu chuỗi TTTM chiếm lĩnh thị phần áp đảo tại các đại đô thị lớn với tỷ lệ lấp đầy cao, hợp đồng thuê dài hạn gắn liền với doanh thu của các thương hiệu bán lẻ hàng đầu (ví dụ: VRE).
3. **Bất động sản Khu công nghiệp có quỹ đất sạch sẵn sàng cho thuê:** Nằm ở vị trí chiến lược đón dòng vốn FDI, đã hoàn thành nghĩa vụ nộp tiền sử dụng đất 1 lần.

---

## 2. Quy Trình Thực Hiện

1. **Thu thập dữ liệu ngành nghề:**
   - Xem mục *Mô hình kinh doanh (Item 1)* trong BCTN hoặc báo cáo `analysis/01-business.md`.
   - Bóc tách cơ cấu doanh thu: Doanh thu chính đến từ mảng nào?
2. **Đánh giá ngoại lệ:**
   - Nếu là BĐS / Xây dựng / VLXD: Kiểm tra xem có sở hữu mỏ đá, mỏ nguyên liệu đặc thù hay vị thế TTTM áp đảo không?
3. **Kết luận & Xử lý:**
   - **Nếu LOẠI:** Ghi thông tin công ty vào `screenings/01-rejected-circle-of-competence.md`. **Dừng phân tích công ty này tại đây.**
   - **Nếu ĐẠT (hoặc ĐẠT THEO NGOẠI LỆ):** Ghi rõ lý do/ghi chú đặc thù và chuyển mã công ty sang **Bước 2 (screener-step2-profitability)**.

---

## 3. Mẫu Trình Bày Khi Công Ty Bị Loại (Ghi vào File 1)

```markdown
### ❌ [TICKER] - [Tên Doanh Nghiệp]
- **Phân loại ngành:** Bất động sản dân dụng / Xây lắp / VLXD đại trà
- **Tỷ trọng doanh thu:** [X]% doanh thu đến từ [Mảng hoạt động]
- **Lý do bị loại:** Nằm ngoài vòng tròn năng lực. Mô hình kinh doanh phụ thuộc nặng vào chu kỳ tín dụng/đất đai, biên lợi nhuận xây lắp mỏng và tồn đọng vốn lớn.
- **Xem xét yếu tố đặc thù:** Không sở hữu mỏ tài nguyên độc quyền hoặc TTTM vị trí kim cương nào đáng kể.
- **Ngày sàng lọc:** [YYYY-MM-DD]
```

## 4. Mẫu Trình Bày Khi Vượt Qua / Ngoại Lệ
- **Kết quả:** ĐẠT BƯỚC 1 (Chuyển sang Bước 2).
- **Ghi chú:** [Ví dụ: Ngoại lệ mỏ đá DHA trữ lượng khai thác 10 năm tại Đồng Nai / Ngoại lệ VRE sở hữu chuỗi Vincom Megamall độc quyền].
