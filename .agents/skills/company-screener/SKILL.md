---
name: company-screener
description: Điều phối quy trình sàng lọc doanh nghiệp đa tầng qua 4 bước khắt khe (Vòng tròn năng lực, Lợi nhuận 3 năm, Chuỗi giá trị & P/B, ROE 5 năm) và phân loại vào 5 file lưu trữ tương ứng.
---

# Master Company Screener Skill — Phễu Lọc Doanh Nghiệp Đa Tầng

Kỹ năng này đóng vai trò **Bộ Điều Phối Trung Tâm (Orchestrator)** để tiếp nhận từng mã cổ phiếu (hoặc một danh sách mã cổ phiếu), đưa lần lượt qua **4 Bước Lọc Loại Trừ** khắt khe và ghi nhận kết quả vào hệ thống 5 file lưu trữ trong thư mục `screenings/`.

---

## 1. Các Trường Hợp Kích Hoạt

- Người dùng yêu cầu: *"Hãy lọc công ty [TICKER] qua các bước tiêu chuẩn của tôi"*.
- Người dùng cung cấp một danh sách: *"Hãy sàng lọc các mã VNM, HPG, NVL, FPT, VRE, DXG, STK qua phễu lọc"*.
- Người dùng yêu cầu: *"Kiểm tra xem công ty [TICKER] có vượt qua bộ lọc 4 bước không và sắp nó vào file tương ứng"*.

---

## 2. Bản Đồ 5 File Lưu Trữ (`screenings/`)

| File | Tên File | Chức Năng |
| :---: | :--- | :--- |
| **File 1** | `screenings/01-rejected-circle-of-competence.md` | Chứa các công ty BĐS, xây dựng, VLXD đại trà bị loại (kèm ghi chú các ca đặc thù được lọt qua). |
| **File 2** | `screenings/02-rejected-consecutive-loss.md` | Chứa các công ty có LNST âm 3 năm liên tiếp gần nhất. |
| **File 3** | `screenings/03-rejected-low-value-chain.md` | Chứa các công ty gia công, sản phẩm đại trà có P/B $\ge 0.5$ bị loại. |
| **File 4** | `screenings/04-rejected-low-roe.md` | Chứa các công ty có ROE $< 10\%$ trong cả 5 năm liên tục. |
| **File 5** | `screenings/05-passed-champions.md` | **Danh mục Tinh Hoa:** Chứa các công ty xuất sắc vượt qua toàn bộ 4 bước, nêu chi tiết lý do từng bước. |
| **Dashboard**| `screenings/screening_dashboard.md` | Bảng Kanban / Matrix tổng quan trạng thái của tất cả các mã cổ phiếu đã chạy qua hệ thống. |

---

## 3. Quy Trình 4 Bước Sàng Lọc Chi Tiết Cho Từng Công Ty

Với mỗi mã cổ phiếu `<TICKER>`:

```
[Bắt đầu: <TICKER>]
       │
       ▼
[BƯỚC 1: Ngành & Vòng tròn năng lực] ──(Trượt)──► Ghi vào File 1 & Dashboard ──► DỪNG LẠI
       │ (Đạt / Ngoại lệ đặc thù)
       ▼
[BƯỚC 2: LNST 3 năm liên tiếp]       ──(Trượt)──► Ghi vào File 2 & Dashboard ──► DỪNG LẠI
       │ (Đạt - Có lãi dương)
       ▼
[BƯỚC 3: Chuỗi giá trị & P/B]        ──(Trượt)──► Ghi vào File 3 & Dashboard ──► DỪNG LẠI
       │ (Đạt - Độc đáo hoặc P/B < 0.5)
       ▼
[BƯỚC 4: Hiệu quả vốn ROE 5 năm]    ──(Trượt)──► Ghi vào File 4 & Dashboard ──► DỪNG LẠI
       │ (Đạt - ROE >= 10%)
       ▼
[TỐT NGHIỆP: Ghi vào File 5 & Dashboard] ──► THÀNH CÔNG
```

### Bước 1: Gọi kỹ năng `screener-step1-industry`
- Kiểm tra ngành nghề:
  - Nếu là BĐS dân dụng, xây dựng, VLXD thông thường:
    * Có mỏ đá trữ lượng lớn/vị trí đắc địa không?
    * Có sở hữu TTTM độc quyền vị trí kim cương không?
    * **Nếu KHÔNG có yếu tố đặc thù:** 👉 **LOẠI.** Ghi hồ sơ vào `screenings/01-rejected-circle-of-competence.md`, cập nhật Dashboard = "Dừng ở Bước 1". Kết thúc xử lý mã này.
    * **Nếu CÓ yếu tố đặc thù:** 👉 Ghi chú rõ yếu tố đặc thù và cho phép đi tiếp sang Bước 2.
  - Nếu thuộc các ngành nghề thông thường khác (sản xuất, bán lẻ, công nghệ, dược phẩm...): 👉 Đi tiếp sang Bước 2.

### Bước 2: Gọi kỹ năng `screener-step2-profitability`
- Thu thập LNST hợp nhất 3 năm tài chính gần nhất ($N-2, N-1, N$).
- **Nếu LNST âm cả 3 năm liên tục:** 👉 **LOẠI.** Ghi bảng số liệu 3 năm vào `screenings/02-rejected-consecutive-loss.md`, cập nhật Dashboard = "Dừng ở Bước 2". Kết thúc xử lý mã này.
- **Nếu có lãi (ít nhất 1 năm dương):** 👉 Đi tiếp sang Bước 3.

### Bước 3: Gọi kỹ năng `screener-step3-value-chain-pb`
- Đánh giá sản phẩm và vị thế trong chuỗi giá trị gia tăng:
  - Nếu sản phẩm độc đáo, có thương hiệu mạnh, biên lãi gộp cao ($> 20-30\%$): 👉 **ĐẠT.** Đi tiếp sang Bước 4 (không cần xét P/B).
  - Nếu là sản phẩm gia công thuần túy, sơ chế thô đại trà, biên lãi mỏng ($< 10-12\%$):
    * Kiểm tra định giá $P/B$:
      + Nếu $P/B < 0.5$: 👉 **ĐẠT THEO NGOẠI LỆ ĐỊNH GIÁ.** Đi tiếp sang Bước 4 (kèm ghi chú P/B chiết khấu sâu).
      + Nếu $P/B \ge 0.5$: 👉 **LOẠI.** Ghi số liệu vào `screenings/03-rejected-low-value-chain.md`, cập nhật Dashboard = "Dừng ở Bước 3". Kết thúc xử lý mã này.

### Bước 4: Gọi kỹ năng `screener-step4-roe`
- Thu thập chuỗi ROE 5 năm gần nhất ($N-4$ đến $N$).
- **Nếu ROE < 10% trong toàn bộ cả 5 năm:** 👉 **LOẠI.** Ghi bảng ROE vào `screenings/04-rejected-low-roe.md`, cập nhật Dashboard = "Dừng ở Bước 4". Kết thúc xử lý mã này.
- **Nếu ROE có năm $\ge 10\%$ hoặc trung bình tốt:** 👉 **CHIẾN THẮNG BỘ LỌC!**

### Bước 5: Đưa vào File 5 & Hoàn Tất
- Ghi danh vào `screenings/05-passed-champions.md` với bản giải trình đầy đủ lý do vượt qua cả 4 bước.
- Cập nhật Dashboard: Đổi trạng thái mã thành **"✅ ĐẠT CHUẨN (Vượt qua 4/4 bước)"**.

---

## 4. Định Dạng Cập Nhật Dashboard Tổng Quan (`screenings/screening_dashboard.md`)

Mỗi khi phân tích xong 1 mã, AI luôn cập nhật vào bảng tổng hợp sau:

| STT | Mã CK | Tên Doanh Nghiệp | Ngành | Bước 1 (Ngành) | Bước 2 (Lãi 3N) | Bước 3 (Chuỗi GT & P/B) | Bước 4 (ROE 5N) | Kết Quả Chung Cuộc | File Lưu Trữ |
| :---: | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| 1 | NVL | Địa ốc No Va | BĐS dân dụng | ❌ Loại | - | - | - | Dừng ở Bước 1 | `01-rejected-circle-of-competence.md` |
| 2 | VRE | Vincom Retail | BĐS Bán lẻ | ⚠️ Pass (TTTM độc quyền) | ✅ Pass | ✅ Pass (Biên gộp 50%) | ✅ Pass (ROE > 12%) | 🏆 **Lọt vào File 5** | `05-passed-champions.md` |
| 3 | HVN | Vietnam Airlines | Hàng không | ✅ Pass | ❌ Loại (Lỗ 3N) | - | - | Dừng ở Bước 2 | `02-rejected-consecutive-loss.md` |
| 4 | TNG | Dệt may TNG | May mặc gia công | ✅ Pass | ✅ Pass | ❌ Loại (Gia công, P/B 0.9 >= 0.5)| - | Dừng ở Bước 3 | `03-rejected-low-value-chain.md` |
| 5 | STK | Sợi Thế Kỷ | Sợi dệt | ✅ Pass | ✅ Pass | ✅ Pass | ❌ Loại (ROE 5N < 10%) | Dừng ở Bước 4 | `04-rejected-low-roe.md` |
| 6 | VNM | Vinamilk | Sữa & Tiêu dùng | ✅ Pass | ✅ Pass | ✅ Pass (Sản phẩm độc đáo) | ✅ Pass (ROE ~28%) | 🏆 **Lọt vào File 5** | `05-passed-champions.md` |
