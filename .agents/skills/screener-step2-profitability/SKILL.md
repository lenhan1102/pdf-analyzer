---
name: screener-step2-profitability
description: Bước 2 trong phễu lọc cổ phiếu - Sàng lọc Lợi Nhuận 3 Năm Gần Nhất. Loại bỏ các doanh nghiệp có Lợi nhuận sau thuế âm trong cả 3 năm tài chính liên tiếp gần đây.
---

# Screener Step 2: Sàng Lọc Lợi Nhuận 3 Năm Gần Nhất

Kỹ năng này hướng dẫn AI Agent thực hiện **Bước 2** trong phễu lọc: Loại bỏ các doanh nghiệp đang chìm trong khủng hoảng kinh doanh, mô hình không có khả năng sinh lời bền vững, thể hiện qua việc **Lợi nhuận sau thuế của công ty mẹ (Net Income) bị âm trong 3 năm tài chính liên tiếp gần nhất**.

---

## 1. Tiêu Chí Sàng Lọc Bước 2

### A. Quy Tắc Loại Trừ (Trượt Bước 2)
- Doanh nghiệp có **Lợi nhuận sau thuế hợp nhất (LNST) < 0** trong cả **3 năm tài chính liên tiếp gần nhất** (Ví dụ: Năm $N-2$, $N-1$, $N$ đều âm).
- Không phân biệt nguyên nhân (dù là do trích lập dự phòng, lỗ tỷ giá, suy thoái ngành hay kinh doanh kém), việc lỗ 3 năm liên tục chứng tỏ cấu trúc chi phí và mô hình doanh nghiệp đang gặp vấn đề sinh tồn nghiêm trọng.

### B. Điều Kiện Vượt Qua (Chuyển Sang Bước 3)
- Doanh nghiệp có **ít nhất 1 năm có lãi dương (LNST > 0)** trong 3 năm gần nhất.
- Doanh nghiệp kinh doanh ổn định, có lãi liên tục 3 năm.

---

## 2. Quy Trình Thực Hiện

1. **Thu thập số liệu Báo cáo KQKD (P&L):**
   - Lấy số liệu LNST hợp nhất của cổ đông công ty mẹ từ BCTC kiểm toán 3 năm tài chính gần nhất (hoặc báo cáo `analysis/03-financial-statements.md`).
2. **Đối chiếu số liệu:**
   - Liệt kê bảng số liệu 3 năm: Năm $N-2$, Năm $N-1$, Năm $N$.
3. **Kết luận & Xử lý:**
   - **Nếu ÂM CẢ 3 NĂM LIÊN TIẾP:** Ghi thông tin công ty vào `screenings/02-rejected-consecutive-loss.md`. **Dừng phân tích công ty này tại đây.**
   - **Nếu ĐẠT:** Ghi chú bảng LNST 3 năm và chuyển mã công ty sang **Bước 3 (screener-step3-value-chain-pb)**.

---

## 3. Mẫu Trình Bày Khi Công Ty Bị Loại (Ghi vào File 2)

```markdown
### ❌ [TICKER] - [Tên Doanh Nghiệp]
- **Ngành nghề:** [Tên ngành]
- **Kết quả kinh doanh 3 năm gần nhất:**
  | Năm | Doanh thu thuần (Tỷ VNĐ) | LNST Công ty mẹ (Tỷ VNĐ) | Trạng thái |
  | :---: | :---: | :---: | :---: |
  | [Năm N-2] | [Số liệu] | [Số âm] | Lỗ |
  | [Năm N-1] | [Số liệu] | [Số âm] | Lỗ |
  | [Năm N]   | [Số liệu] | [Số âm] | Lỗ |
- **Lý do bị loại:** Lợi nhuận sau thuế bị âm trong 3 năm tài chính liên tiếp gần nhất ([N-2] đến [N]). Doanh nghiệp mất khả năng tự cân đối dòng tiền từ hoạt động cốt lõi.
- **Ngày sàng lọc:** [YYYY-MM-DD]
```

## 4. Mẫu Trình Bày Khi Vượt Qua
- **Kết quả:** ĐẠT BƯỚC 2 (Chuyển sang Bước 3).
- **Ghi chú LNST 3 năm:** [Liệt kê ngắn gọn LNST 3 năm, ví dụ: 2021: +500 Tỷ, 2022: +620 Tỷ, 2023: +750 Tỷ].
