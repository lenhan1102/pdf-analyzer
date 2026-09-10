#!/usr/bin/env python3
import os
import sys
import argparse
import shutil
import json

def main():
    parser = argparse.ArgumentParser(description="Khởi tạo thư mục công ty và thời điểm (Năm FY / Quý Q1-Q4) theo chuẩn 10-K & 10-Q")
    parser.add_argument("--ticker", required=True, help="Mã cổ phiếu (ví dụ: VNM, FPT, HPG)")
    parser.add_argument("--year", required=True, help="Năm tài chính (ví dụ: 2023, 2024)")
    parser.add_argument("--period", default="FY", choices=["FY", "Q1", "Q2", "Q3", "Q4", "fy", "q1", "q2", "q3", "q4"], help="Thời điểm báo cáo: FY (cả năm) hoặc Q1, Q2, Q3, Q4 (quý). Mặc định là FY")
    parser.add_argument("--name", default="", help="Tên đầy đủ của công ty (tùy chọn)")
    args = parser.parse_args()

    ticker = args.ticker.upper().strip()
    year = args.year.strip()
    period = args.period.upper().strip()
    company_name = args.name.strip() or ticker

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dir = os.path.join(base_dir, "companies", ticker, year, period)
    reports_dir = os.path.join(target_dir, "reports")
    analysis_dir = os.path.join(target_dir, "analysis")
    templates_dir = os.path.join(base_dir, "templates")

    os.makedirs(reports_dir, exist_ok=True)
    os.makedirs(analysis_dir, exist_ok=True)

    # Copy template files to analysis
    template_map = [
        ("01-business.md", "01-business.md"),
        ("02-risk-factors.md", "02-risk-factors.md"),
        ("03-financial-statements.md", "03-financial-statements.md"),
        ("04-mda.md", "04-mda.md"),
        ("05-management-governance.md", "05-management-governance.md"),
        ("06-ownership.md", "06-ownership.md"),
        ("07-exhibits-notes.md", "07-exhibits-notes.md"),
        ("08-disclosure-gaps.md", "08-disclosure-gaps.md"),
    ]

    for src_file, dst_file in template_map:
        src_path = os.path.join(templates_dir, src_file)
        dst_path = os.path.join(analysis_dir, dst_file)
        if not os.path.exists(dst_path) and os.path.exists(src_path):
            with open(src_path, "r", encoding="utf-8") as sf:
                content = sf.read().replace("[TICKER]", ticker).replace("[YEAR]", year).replace("[PERIOD]", period).replace("[TÊN CÔNG TY]", company_name)
            with open(dst_path, "w", encoding="utf-8") as df:
                df.write(content)

    # Summary template
    summary_src = os.path.join(templates_dir, "00-summary.md")
    summary_dst = os.path.join(target_dir, "summary.md")
    if not os.path.exists(summary_dst) and os.path.exists(summary_src):
        with open(summary_src, "r", encoding="utf-8") as sf:
            content = sf.read().replace("[TICKER]", ticker).replace("[YEAR]", year).replace("[PERIOD]", period).replace("[TÊN CÔNG TY]", company_name)
        with open(summary_dst, "w", encoding="utf-8") as df:
            df.write(content)

    # progress.json
    progress_file = os.path.join(target_dir, "progress.json")
    if not os.path.exists(progress_file):
        progress_data = {
            "ticker": ticker,
            "year": year,
            "period": period,
            "company_name": company_name,
            "status": "pending_reports",
            "pdf_reports": [],
            "sections": {
                "00-summary": False,
                "01-business": False,
                "02-risk-factors": False,
                "03-financial-statements": False,
                "04-mda": False,
                "05-management-governance": False,
                "06-ownership": False,
                "07-exhibits-notes": False,
                "08-disclosure-gaps": False
            }
        }
        with open(progress_file, "w", encoding="utf-8") as pf:
            json.dump(progress_data, pf, ensure_ascii=False, indent=2)

    doc_type = "10-K (Cả năm)" if period == "FY" else f"10-Q ({period})"
    print(f"\n✅ Đã khởi tạo thành công không gian phân tích cho {company_name} ({ticker}) - {doc_type} Năm {year}")
    print(f"📁 Thư mục lưu trữ: {target_dir}")
    print(f"👉 Quy chuẩn đặt tên file PDF đầu vào vào thư mục {reports_dir}:")
    if period == "FY":
        print(f"   📄 {ticker}_{year}_FY_Annual-Report.pdf         (Báo cáo thường niên cả năm)")
        print(f"   📄 {ticker}_{year}_FY_Audited-FS.pdf            (Báo cáo tài chính kiểm toán)")
    else:
        print(f"   📄 {ticker}_{year}_{period}_Financial-Statements.pdf (Báo cáo tài chính {period})")
        print(f"   📄 {ticker}_{year}_{period}_Management-Report.pdf    (Báo cáo giải trình KQKD {period})")
    print()

if __name__ == "__main__":
    main()
