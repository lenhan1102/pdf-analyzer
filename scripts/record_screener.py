#!/usr/bin/env python3
"""
Script tiện ích hỗ trợ ghi nhận kết quả sàng lọc doanh nghiệp vào hệ thống 5 file screenings/:
- 01-rejected-circle-of-competence.md (Bước 1)
- 02-rejected-consecutive-loss.md (Bước 2)
- 03-rejected-low-value-chain.md (Bước 3)
- 04-rejected-low-roe.md (Bước 4)
- 05-passed-champions.md (File thứ 5 - Vượt qua toàn bộ)
- Cập nhật đồng bộ vào screenings/screening_dashboard.md
"""

import os
import sys
import argparse
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCREENINGS_DIR = os.path.join(BASE_DIR, "screenings")

FILE_MAP = {
    1: "01-rejected-circle-of-competence.md",
    2: "02-rejected-consecutive-loss.md",
    3: "03-rejected-low-value-chain.md",
    4: "04-rejected-low-roe.md",
    5: "05-passed-champions.md"
}

DASHBOARD_FILE = "screening_dashboard.md"

def append_to_file(filepath, content):
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(content)

def main():
    parser = argparse.ArgumentParser(description="Ghi nhận kết quả sàng lọc doanh nghiệp.")
    parser.add_argument("--ticker", required=True, help="Mã cổ phiếu (ví dụ: VNM, NVL...)")
    parser.add_argument("--name", default="", help="Tên đầy đủ của doanh nghiệp")
    parser.add_argument("--industry", default="", help="Ngành nghề hoạt động")
    parser.add_argument("--step", type=int, choices=[1, 2, 3, 4, 5], required=True, help="Bước bị loại (1-4) hoặc 5 nếu vượt qua toàn bộ")
    parser.add_argument("--reason", default="", help="Lý do chi tiết bị loại hoặc lý do vượt qua")
    parser.add_argument("--metrics", default="", help="Ghi chú số liệu (ví dụ: LNST 3 năm, ROE 5 năm, P/B...)")
    parser.add_argument("--exception-note", default="", help="Ghi chú ngoại lệ (nếu có)")
    
    args = parser.parse_args()
    os.makedirs(SCREENINGS_DIR, exist_ok=True)
    today = date.today().strftime("%Y-%m-%d")
    ticker = args.ticker.upper()
    name = args.name or ticker
    
    target_filename = FILE_MAP[args.step]
    target_filepath = os.path.join(SCREENINGS_DIR, target_filename)
    
    # Chuẩn bị nội dung Markdown ghi vào file tương ứng
    if args.step == 1:
        entry = f"""
### ❌ {ticker} - {name}
- **Phân loại ngành:** {args.industry or 'Bất động sản / Xây dựng / VLXD đại trà'}
- **Lý do bị loại:** {args.reason or 'Nằm ngoài vòng tròn năng lực. Mô hình kinh doanh phụ thuộc nặng vào chu kỳ tín dụng/đất đai/biên thầu mỏng.'}
- **Xem xét yếu tố đặc thù:** {args.exception_note or 'Không có mỏ tài nguyên độc quyền hoặc TTTM vị trí kim cương.'}
- **Ngày sàng lọc:** {today}

---
"""
    elif args.step == 2:
        entry = f"""
### ❌ {ticker} - {name}
- **Ngành nghề:** {args.industry or 'Chưa phân loại'}
- **Lý do bị loại:** {args.reason or 'Lợi nhuận sau thuế bị âm trong 3 năm tài chính liên tiếp gần nhất.'}
- **Số liệu minh chứng:** {args.metrics}
- **Ngày sàng lọc:** {today}

---
"""
    elif args.step == 3:
        entry = f"""
### ❌ {ticker} - {name}
- **Vị thế chuỗi giá trị:** {args.industry or 'Gia công / Đại trà'} - {args.reason}
- **Định giá & Số liệu:** {args.metrics}
- **Lý do bị loại:** Sản phẩm nằm ở phần thấp của chuỗi giá trị gia tăng và định giá P/B >= 0.5 (không đủ rẻ để có biên an toàn tài sản).
- **Ngày sàng lọc:** {today}

---
"""
    elif args.step == 4:
        entry = f"""
### ❌ {ticker} - {name}
- **Ngành nghề:** {args.industry or 'Chưa phân loại'}
- **Lý do bị loại:** {args.reason or 'Hiệu quả sử dụng vốn trên vốn chủ sở hữu (ROE) < 10% trong suốt 5 năm liên tục.'}
- **Chuỗi số liệu ROE 5 năm:** {args.metrics}
- **Ngày sàng lọc:** {today}

---
"""
    else: # args.step == 5
        entry = f"""
### 🏆 {ticker} - {name}
- **Ngành nghề:** {args.industry or 'Doanh nghiệp xuất sắc'}
- **Chỉ số nổi bật:** {args.metrics}

#### Lý Do Vượt Qua Toàn Bộ 4 Bước Sàng Lọc:
{args.reason}
- **Ghi chú thêm:** {args.exception_note or 'Đủ điều kiện đưa vào Watchlist để phân tích sâu 8 trụ cột 10-K.'}
- **Ngày phân tích:** {today}

---
"""

    append_to_file(target_filepath, entry)
    print(f"✅ Đã ghi nhận {ticker} vào file: {target_filename}")

if __name__ == "__main__":
    main()
