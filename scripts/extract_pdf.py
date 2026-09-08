#!/usr/bin/env python3
import os
import sys
import argparse

def extract_with_pymupdf(pdf_path, start_page=1, end_page=None, keyword=None):
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return None, "PyMuPDF (fitz) chưa được cài đặt. Hãy chạy: pip install pymupdf"

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    start_idx = max(0, start_page - 1)
    end_idx = min(total_pages, end_page) if end_page else total_pages

    extracted_text = []
    matched_pages = []

    for page_num in range(start_idx, end_idx):
        page = doc[page_num]
        text = page.get_text("text")
        
        if keyword:
            if keyword.lower() in text.lower():
                matched_pages.append(page_num + 1)
                extracted_text.append(f"\n<!-- === TRANG {page_num + 1} / {total_pages} === -->\n{text}")
        else:
            extracted_text.append(f"\n<!-- === TRANG {page_num + 1} / {total_pages} === -->\n{text}")

    doc.close()
    return "\n".join(extracted_text), f"Tổng trang: {total_pages}, Trang trích xuất: {len(extracted_text)}"

def main():
    parser = argparse.ArgumentParser(description="Trích xuất văn bản từ BCTC/BCTN PDF")
    parser.add_argument("--pdf", required=True, help="Đường dẫn file PDF")
    parser.add_argument("--start", type=int, default=1, help="Trang bắt đầu (1-indexed)")
    parser.add_argument("--end", type=int, default=None, help="Trang kết thúc (1-indexed)")
    parser.add_argument("--keyword", type=str, default=None, help="Từ khóa tìm kiếm (tùy chọn)")
    parser.add_argument("--output", type=str, default=None, help="Lưu ra file text (tùy chọn)")
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"❌ Không tìm thấy file: {args.pdf}")
        sys.exit(1)

    text, info = extract_with_pymupdf(args.pdf, args.start, args.end, args.keyword)
    if text is None:
        print(f"❌ {info}")
        sys.exit(1)

    print(f"ℹ️ {info}")
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ Đã ghi kết quả trích xuất vào: {args.output}")
    else:
        # In 2000 ký tự đầu tiên nếu chạy trực tiếp
        print(text[:2000] + "\n... (nội dung đã được trích xuất)")

if __name__ == "__main__":
    main()
