# 🎯 Rổ Chất Lượng Trong Danh Sách P/E < 5 — Doanh Nghiệp Tốt, Lợi Nhuận Đều, Không Rủi Ro Nợ Ngắn Hạn

- **Ngày lập:** 16/11/2026
- **Đầu vào:** 84 mã nhóm thanh khoản A và B trong [pe-under-5-2026-11-13.md](pe-under-5-2026-11-13.md). Nhóm C gần như không giao dịch được nên không xét.
- **Nguồn số liệu:** VNDirect Finfo API. BCTC hợp nhất năm 2021–2025, các quý Q4/2025–Q3/2026, bảng cân đối tại 30/09/2026, sự kiện cổ tức từ 2021.
- **Quy ước:** Định giá thể hiện bằng **vốn hóa thị trường (tỷ VNĐ)**, không dùng thị giá. ROE tính trên **VCSH công ty mẹ**, tức VCSH trừ lợi ích cổ đông không kiểm soát.

---

## 1. Bộ tiêu chí sàng lọc

| # | Tiêu chí | Ngưỡng |
|---|---|---|
| 1 | Lợi nhuận đều | LNST công ty mẹ dương cả 5 năm 2021–2025 và 4 quý gần nhất |
| 2 | Hiệu quả vốn | ROE mẹ bình quân 5 năm ≥ 12%, không năm nào < 6% |
| 3 | Lợi nhuận là tiền thật | Tổng CFO 5 năm / tổng LNST 5 năm ≥ 0,6 |
| 4 | Không rủi ro nợ ngắn hạn | Tài sản ngắn hạn / Nợ ngắn hạn ≥ 1,2; (Vay − Tiền & ĐTNH) / VCSH ≤ 0,6; (LNTT + lãi vay) / lãi vay ≥ 4 |
| 5 | Không phụ thuộc lãi một lần | Lãi khác, lãi liên kết và phần doanh thu tài chính vượt 1,5 lần mức bình quân cộng lại ≤ 30% LNTT 4 quý gần nhất |

> [!NOTE]
> Chất lượng ban lãnh đạo không đo trực tiếp được bằng số liệu. File dùng các chỉ báo gián tiếp: cổ tức tiền mặt đều đặn, ít pha loãng, CFO tương xứng lợi nhuận. Với các mã đã có trong phễu lọc, file tham chiếu thêm đánh giá định tính trong [screening_dashboard.md](screening_dashboard.md).

**Kết quả:** 14/84 mã đạt cả 5 tiêu chí. NNC bị gạt ra dù đạt đủ, vì đã bị loại ở Bước 1 phễu lọc (mỏ đá Núi Nhỏ hết hạn). Ba ngân hàng SHB, TPB, KLB không áp dụng bộ tiêu chí này, xem mục 5.

---

## 2. ⭐ Nhóm ưu tiên — đạt mọi tiêu chí, gần như không nợ, đã có trong File 5

| Mã | Ngành | Vốn hóa (tỷ) | P/E | LNST mẹ 4 quý (tỷ) | ROE mẹ 2021→2025 | Tiền & ĐTNH / Vay (tỷ) | TSNH/Nợ NH | Cổ tức 2025 / Vốn hóa | GTGD TB (tỷ/phiên) |
|---|---|---:|---:|---:|---|---|---:|---:|---:|
| **NCT** | Nhà ga hàng hóa Nội Bài | 2.083 | 4,74 | 440 | 49 · 55 · 50 · 48 · 55% | 671 / **0** | 3,99 | 10,0% | 1,58 |
| **HVT** | Hóa chất xút-clo, PAC | 538 | 4,26 | 123 | 24 · 41 · 17 · 19 · 20% | 150 / 51 | 1,91 | 7,7% | 0,54 |
| **FMC** | Tôm chế biến xuất khẩu | 2.295 | 4,25 | 540 | 15 · 16 · 14 · 14 · 15% | 2.957 / 2.362 | 1,57 | 7,2% | 1,24 |
| **EID** | Sách giáo khoa, giáo dục | 285 | 3,09 | 92 | 15 · 20 · 17 · 16 · 13% | 459 / 138 | 1,69 | 10,6% | 0,12 |

### NCT — CTCP Dịch vụ Hàng hóa Nội Bài
- **Điểm mạnh:**
  - Độc quyền nhà ga hàng hóa Nội Bài, ROE mẹ khoảng 50% suốt 5 năm.
  - Không vay nợ.
  - CFO/LNST 5 năm đạt 1,04.
  - Cổ tức tiền mặt năm 2025 là 80% mệnh giá; kế hoạch 2026 là 100%.
- **Cần kiểm tra:**
  - LNST 4 quý (440 tỷ) có một phần cổ tức nhận từ đầu tư bên ngoài. Kế hoạch LNST 2026 là 428 tỷ, tương ứng P/E cốt lõi khoảng 4,9.
  - Mức P/E này thấp bất thường cho một doanh nghiệp độc quyền. Rủi ro tiềm ẩn là sân bay Gia Bình cạnh tranh hàng hóa với Nội Bài.
  - Vietnam Airlines nắm 55,13%, cần soát giao dịch bên liên quan.
  - Quỹ America LLC liên tục bán ra, từ 11,85% xuống 9,99% tính đến 04/2026.

### HVT — CTCP Hóa chất Việt Trì
- **Điểm mạnh:**
  - ROE mẹ ≥ 17% cả 5 năm.
  - Gần như không vay; LNTT gấp khoảng 25 lần lãi vay.
  - Vinachem nắm 68,4%.
- **Cần kiểm tra:**
  - Vốn điều lệ tăng khoảng 150% từ 2021. Cần xác định phần tăng do thưởng cổ phiếu (không pha loãng giá trị) và phần do phát hành mới.
  - Thanh khoản thấp, khoảng 0,5 tỷ/phiên.

### FMC — CTCP Thực phẩm Sao Ta (thuộc PAN Group)
- **Điểm mạnh:**
  - Lợi nhuận đều nhất nhóm, ROE mẹ 14–16% cả 5 năm.
  - Tiền & ĐTNH lớn hơn vay khoảng 595 tỷ; CFO/LNST 5 năm đạt 1,13.
- **Cần kiểm tra:**
  - LNST 4 quý (540 tỷ) cao hơn nhiều so với bình quân 5 năm (khoảng 300 tỷ), nên coi là đỉnh chu kỳ.
  - Rủi ro giá tôm và thuế quan xuất khẩu sang Mỹ.

### EID — CTCP Đầu tư và Phát triển Giáo dục Hà Nội
- **Điểm mạnh:**
  - Tiền & ĐTNH lớn hơn vay khoảng 321 tỷ.
  - Cổ tức tiền mặt 5/5 năm.
  - Là trụ cột của NXB Giáo dục.
- **Cần kiểm tra:**
  - **Rủi ro chính sách:** định hướng thống nhất một bộ sách giáo khoa và miễn phí sách giáo khoa có thể thay đổi mô hình kinh doanh. Cần đánh giá kỹ.
  - Thanh khoản rất thấp, khoảng 0,12 tỷ/phiên.

---

## 3. Nhóm khá — đạt tiêu chí nhưng có điểm cần cân nhắc

| Mã | Ngành | Vốn hóa (tỷ) | P/E | ROE mẹ 2021→2025 | Tiền & ĐTNH / Vay (tỷ) | Cổ tức 2025 / Vốn hóa | Điểm cần lưu ý |
|---|---|---:|---:|---|---|---:|---|
| **HTG** | Dệt may Hòa Thọ | 1.516 | 4,26 | 31 · 33 · 22 · 32 · 30% | 1.469 / 1.644 | 7,1% | TSNH/Nợ NH chỉ 1,23 (sát ngưỡng); phụ thuộc khách hàng Mỹ; vốn điều lệ tăng khoảng 83% từ 2021 |
| **QTP** | Nhiệt điện Quảng Ninh | 4.644 | 3,75 | 9 · 12 · 12 · 12 · 18% | 1.856 / 0 | 11,6% | **Chưa qua phễu lọc**; phụ thuộc giá bán điện cho EVN và giá than; lợi nhuận Q4/2025 đột biến (640 tỷ) |
| **ABT** | Nghêu MSC, cá (thuộc PAN) | 688 | 4,53 | 8 · 14 · 13 · 18 · 24% | 317 / 153 | 5,1% | ROE 2021 chỉ 8%; thanh khoản thấp |
| **DRI** | Cao su tại Lào | 980 | 4,69 | 12 · 14 · 14 · 19 · 22% | 344 / 108 | 3,8% | Lợi nhuận theo chu kỳ giá cao su; CFO 2025 chỉ 45 tỷ so với LNST 157 tỷ |
| **LHG** | KCN Long Hậu | 1.345 | 4,67 | 20 · 13 · 10 · 11 · 16% | 471 / 323 | 7,1% | Lợi nhuận phụ thuộc tiến độ cho thuê đất; CFO 2024 âm |

## 4. Đạt tiêu chí nhưng nên để sau

| Mã | Vốn hóa (tỷ) | P/E | Lý do để sau |
|---|---:|---:|---|
| SED | 150 | 3,58 | Cùng rủi ro chính sách sách giáo khoa như EID; quy mô nhỏ; thanh khoản khoảng 0,1 tỷ/phiên |
| HTI | 458 | 3,23 | Thu phí BOT An Sương – An Lạc có thời hạn; LNST Q1/2025 đột biến; ROE 2021 chỉ 7,8% |
| CAT | 222 | 3,68 | Quy mô nhỏ; vay (281 tỷ) lớn hơn tiền (163 tỷ); vốn điều lệ tăng khoảng 47% |
| SWC | 1.711 | 4,60 | Chưa qua phễu lọc; chỉ trả cổ tức 1/5 năm (2025), chính sách với cổ đông yếu |
| NNC | 1.011 | 4,72 | Đã bị loại ở Bước 1 phễu lọc: mỏ đá Núi Nhỏ hết hạn |

## 5. Ngân hàng (chưa chấm)

SHB và TPB đã có trong File 5. KLB bị loại ở Bước 4. Ngân hàng cần bộ chỉ số riêng: nợ xấu, CAR, LDR, CASA, chi phí vốn. Bộ tiêu chí ở mục 1 không áp dụng được cho ngân hàng.

---

## 6. Các mã có tiêu chí suýt đạt (trượt đúng 1 tiêu chí)

| Mã | Vốn hóa (tỷ) | P/E | Trượt tiêu chí |
|---|---:|---:|---|
| PAN | 4.249 | 3,45 | ROE mẹ bình quân khoảng 10% (7,2 → 12,6%). Xem [companies/PAN/valuation.md](../companies/PAN/valuation.md) |
| PNJ | 7.650 | 4,53 | CFO/LNST 5 năm chỉ 0,1 (cần kiểm tra, có thể do tồn kho vàng tăng); dữ liệu vốn hóa chưa xác minh |
| RAL | 1.714 | 3,70 | CFO/LNST 5 năm chỉ 0,11 |
| HPP | 496 | 4,62 | CFO/LNST 5 năm gần 0 |
| CKA | 175 | 3,28 | CFO/LNST 5 năm âm |
| TV1 | 658 | 3,49 | TSNH/Nợ NH chỉ 1,10 |
| VVS | 3.044 | 3,86 | TSNH/Nợ NH chỉ 1,17; lợi nhuận mới tăng vọt từ 2025 |
| SAS | 4.118 | 4,54 | ROE 2021 khoảng 0% do Covid; ROE 2025 đạt 37% |
| NT2 | 6.794 | 4,66 | ROE 2024 chỉ 2% |
| BSR | 126.935 | 4,54 | ROE 2024 chỉ 1,1% (đóng cửa bảo dưỡng) |
| ALC | 1.050 | 3,77 | ROE 2021 chỉ 4,6%; chưa trả cổ tức |
| HCC | 166 | 3,66 | ROE 2021 chỉ 3,1% |
| KHS | 173 | 3,83 | ROE 2023 chỉ 0,6% |
| DXP | 869 | 3,94 | ROE bình quân khoảng 8% |
| VTO | 819 | 4,87 | ROE bình quân khoảng 9% |
| VOS | 1.512 | 4,46 | Khoảng 54% LNTT 4 quý đến từ khoản bất thường |

---

## 7. Kết luận & bước tiếp theo

- **Ưu tiên đào sâu:** NCT, FMC, HVT. Ba mã này đạt mọi tiêu chí, nợ vay thấp hoặc bằng 0, lợi nhuận đều và trả cổ tức đều. EID tốt về số liệu nhưng phải đánh giá rủi ro chính sách sách giáo khoa trước.
- **Việc cần làm cho từng mã:** đọc báo cáo thường niên và BCTC kiểm toán 2025, trọng tâm là giao dịch bên liên quan, lương thưởng ban lãnh đạo và nguồn gốc lợi nhuận 4 quý gần nhất. Lập hồ sơ `companies/<MÃ>/valuation.md` theo mẫu PAN.
- Đây là kết quả sàng lọc định lượng, **không phải khuyến nghị đầu tư**.

## Nguồn
- VNDirect Finfo API: `/v4/financial_statements`, `/v4/events`, `/v4/ratios/latest`, `/v4/stock_prices` (truy xuất 16/11/2026).
- Đánh giá định tính các mã đã sàng lọc: [screening_dashboard.md](screening_dashboard.md), [05-passed-champions.md](05-passed-champions.md).
- NCT: [DNSE — ĐHĐCĐ NCT: nghiên cứu cơ hội tại sân bay Gia Bình, cổ tức 2026 dự kiến 100%](https://www.dnse.com.vn/senses/tin-tuc/dhdcd-nct-nghien-cuu-co-hoi-tai-san-bay-gia-binh-du-kien-nang-co-tuc-nam-2026-len-100-35240376) · [DNSE — NoiBai Cargo báo lãi quý I tăng hơn 64%](https://www.dnse.com.vn/senses/tin-tuc/noibai-cargo-bao-lai-quy-i-tang-hon-64-co-dong-ky-vong-ke-hoach-co-tuc-moi-35231817) · [VietnamFinance — NCTS muốn nâng cổ tức lên 100%](https://vietnamfinance.vn/ncts-muon-nang-co-tuc-len-100-don-co-hoi-o-san-bay-gia-binh-d146685.html)
