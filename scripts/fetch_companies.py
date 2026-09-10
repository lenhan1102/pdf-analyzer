#!/usr/bin/env python3
"""
Script thu thập toàn bộ danh sách doanh nghiệp niêm yết từ CafeF:
URL nguồn: https://cafef.vn/du-lieu/du-lieu-doanh-nghiep.chn
"""

import os
import json
import urllib.request
import csv
from collections import Counter

API_URL = "https://cafef.vn/du-lieu/ajax/pagenew/databusiness/congtyniemyet.ashx?centerid=0&skip=0&take=3000&major=0"

TRADE_CENTERS = {
    1: "HOSE",
    2: "HNX",
    9: "UPCOM",
    8: "OTC"
}

def fetch_data():
    req = urllib.request.Request(
        API_URL,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://cafef.vn/du-lieu/du-lieu-doanh-nghiep.chn"
        }
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        content = response.read().decode("utf-8")
        data = json.loads(content)
        return data.get("Data", [])

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    companies_dir = os.path.join(base_dir, "companies")
    os.makedirs(companies_dir, exist_ok=True)

    print("🔄 Đang tải danh sách doanh nghiệp từ CafeF...")
    raw_data = fetch_data()
    print(f"✅ Đã tải thành công {len(raw_data)} doanh nghiệp.")

    # Chuẩn hóa dữ liệu
    formatted_companies = []
    for item in raw_data:
        center_id = item.get("TradeCenterId")
        exchange = TRADE_CENTERS.get(center_id, f"Khác ({center_id})")
        
        company = {
            "symbol": (item.get("Symbol") or "").strip().upper(),
            "company_name": (item.get("CompanyName") or "").strip(),
            "exchange": exchange,
            "industry": (item.get("CategoryName") or "Chưa phân loại").strip(),
            "price": item.get("Price", 0)
        }
        if company["symbol"]:
            formatted_companies.append(company)

    # Sắp xếp theo Sàn (HOSE -> HNX -> UPCOM -> OTC) rồi đến Mã CK A-Z
    exchange_order = {"HOSE": 1, "HNX": 2, "UPCOM": 3, "OTC": 4}
    formatted_companies.sort(key=lambda x: (exchange_order.get(x["exchange"], 99), x["symbol"]))

    # 1. Ghi file JSON
    json_path = os.path.join(companies_dir, "listed_companies.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(formatted_companies, f, ensure_ascii=False, indent=2)
    print(f"👉 Đã tạo file JSON: {json_path}")

    # 2. Ghi file CSV
    csv_path = os.path.join(companies_dir, "listed_companies.csv")
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Mã CK", "Tên Doanh Nghiệp", "Sàn Giao Dịch", "Ngành Nghề", "Thị Giá (nghìn VNĐ)"])
        for c in formatted_companies:
            writer.writerow([c["symbol"], c["company_name"], c["exchange"], c["industry"], c["price"]])
    print(f"👉 Đã tạo file CSV: {csv_path}")

    # 3. Thống kê
    exchange_counts = Counter(c["exchange"] for c in formatted_companies)
    industry_counts = Counter(c["industry"] for c in formatted_companies)

    # 4. Ghi file Markdown tổng hợp
    md_path = os.path.join(companies_dir, "LISTED_COMPANIES.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# DANH SÁCH DOANH NGHIỆP NIÊM YẾT VÀ ĐĂNG KÝ GIAO DỊCH TẠI VIỆT NAM\n\n")
        f.write(f"- **Nguồn dữ liệu:** [CafeF - Dữ liệu doanh nghiệp](https://cafef.vn/du-lieu/du-lieu-doanh-nghiep.chn)\n")
        f.write(f"- **Tổng số doanh nghiệp:** **{len(formatted_companies):,}** công ty\n\n")
        
        f.write("## 1. Thống Kê Theo Sàn Giao Dịch\n\n")
        f.write("| Sàn Giao Dịch | Số Lượng Doanh Nghiệp | Tỷ Trọng |\n")
        f.write("| :--- | :---: | :---: |\n")
        total = len(formatted_companies)
        for ex in ["HOSE", "HNX", "UPCOM", "OTC"]:
            cnt = exchange_counts.get(ex, 0)
            pct = (cnt / total * 100) if total > 0 else 0
            f.write(f"| **{ex}** | {cnt:,} | {pct:.1f}% |\n")
        f.write(f"| **TỔNG CỘNG** | **{total:,}** | **100%** |\n\n")

        f.write("## 2. Thống Kê Theo Ngành Nghề\n\n")
        f.write("| Ngành Nghề | Số Lượng Doanh Nghiệp | Tỷ Trọng |\n")
        f.write("| :--- | :---: | :---: |\n")
        for ind, cnt in industry_counts.most_common():
            pct = (cnt / total * 100) if total > 0 else 0
            f.write(f"| {ind} | {cnt:,} | {pct:.1f}% |\n")
        f.write("\n---\n\n")

        f.write("## 3. Danh Sách Chi Tiết Toàn Bộ Doanh Nghiệp\n\n")
        f.write("| STT | Mã CK | Tên Doanh Nghiệp | Sàn | Ngành Nghề | Thị Giá |\n")
        f.write("| :---: | :--- | :--- | :---: | :--- | :---: |\n")
        for idx, c in enumerate(formatted_companies, 1):
            f.write(f"| {idx} | **{c['symbol']}** | {c['company_name']} | {c['exchange']} | {c['industry']} | {c['price']} |\n")

    print(f"👉 Đã tạo file Markdown: {md_path}")
    print("✨ Hoàn tất xuất dữ liệu!")

if __name__ == "__main__":
    main()
