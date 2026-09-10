#!/usr/bin/env python3
import os
import sys
import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Đóng gói báo cáo phân tích chuẩn 10-K (Cả năm) & 10-Q (Quý) thành README.md")
    parser.add_argument("--ticker", required=True, help="Mã cổ phiếu")
    parser.add_argument("--year", required=True, help="Năm tài chính")
    parser.add_argument("--period", default="FY", choices=["FY", "Q1", "Q2", "Q3", "Q4", "fy", "q1", "q2", "q3", "q4"], help="Thời điểm báo cáo: FY hoặc Q1, Q2, Q3, Q4. Mặc định là FY")
    args = parser.parse_args()

    ticker = args.ticker.upper().strip()
    year = args.year.strip()
    period = args.period.upper().strip()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Kiểm tra đường dẫn phân cấp: companies/<TICKER>/<YEAR>/<PERIOD>
    company_dir = os.path.join(base_dir, "companies", ticker, year, period)
    if not os.path.exists(company_dir):
        # Fallback về đường dẫn phẳng cũ nếu tồn tại: companies/<TICKER>/<YEAR>
        fallback_dir = os.path.join(base_dir, "companies", ticker, year)
        if os.path.exists(fallback_dir) and os.path.exists(os.path.join(fallback_dir, "analysis")):
            company_dir = fallback_dir
        else:
            print(f"❌ Không tìm thấy thư mục phân tích: {company_dir}")
            sys.exit(1)

    analysis_dir = os.path.join(company_dir, "analysis")
    summary_file = os.path.join(company_dir, "summary.md")
    output_readme = os.path.join(company_dir, "README.md")

    report_title_type = "CHUẨN 10-K (ANNUAL REPORT)" if period == "FY" else f"CHUẨN 10-Q (BÁO CÁO QUÝ {period})"

    sections = [
        ("01-business.md", "Trụ Cột 1: Business (Item 1) — Mô Hình Kinh Doanh"),
        ("02-risk-factors.md", "Trụ Cột 2: Risk Factors (Item 1A) — Những Rủi Ro Trọng Yếu"),
        ("03-financial-statements.md", "Trụ Cột 3: Financial Statements (Item 8) — Báo Cáo Tài Chính"),
        ("04-mda.md", "Trụ Cột 4: MD&A (Item 7) — Phân Tích Của Ban Điều Hành"),
        ("05-management-governance.md", "Trụ Cột 5: Management & Governance (Item 10 & 11) — Quản Trị Công Ty"),
        ("06-ownership.md", "Trụ Cột 6: Ownership (Item 12) — Cơ Cấu Sở Hữu"),
        ("07-exhibits-notes.md", "Trụ Cột 7: Exhibits & Footnotes (Item 13 & 15) — Thuyết Minh & Bên Liên Quan"),
        ("08-disclosure-gaps.md", "Trụ Cột 8: Disclosure Gaps & Blind Spots — Khoảng Trống Thông Tin & Điểm Mù Của Ban Quản Trị"),
    ]

    full_content = []
    full_content.append(f"# BÁO CÁO PHÂN TÍCH DOANH NGHIỆP {report_title_type}")
    full_content.append(f"**Doanh nghiệp:** {ticker} | **Năm tài chính:** {year} | **Kỳ báo cáo:** {period}\n")
    full_content.append(f"> Báo cáo được tự động bóc tách và phân tích theo 8 trụ cột chuẩn mực 10-K/10-Q & Bóc tách Điểm mù Thông tin từ Báo Cáo Thường Niên & BCTC Kiểm Toán.\n")
    full_content.append("---\n")

    # 1. Summary
    if os.path.exists(summary_file):
        with open(summary_file, "r", encoding="utf-8") as sf:
            full_content.append(sf.read().strip())
            full_content.append("\n\n---\n")

    # 2. 8 Sections
    for file_name, title in sections:
        sec_path = os.path.join(analysis_dir, file_name)
        if os.path.exists(sec_path):
            with open(sec_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                full_content.append(f"\n\n<!-- SECTION: {file_name} -->\n")
                full_content.append(content)
                full_content.append("\n\n---\n")
        else:
            full_content.append(f"\n\n## {title}\n*Đang cập nhật...*\n\n---\n")

    full_content.append("\n\n*Báo cáo được tạo bởi Hệ thống 10-K Analyzer.*\n")

    with open(output_readme, "w", encoding="utf-8") as out:
        out.write("\n".join(full_content))

    print(f"✅ Đã đóng gói thành công báo cáo hoàn chỉnh tại:")
    print(f"👉 {output_readme}")

if __name__ == "__main__":
    main()
