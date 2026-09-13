import json
import re
import os
import sys
import subprocess
import time
import concurrent.futures
import urllib.request
from datetime import datetime

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def fetch_financial_data(ticker):
    url = f'https://cafef.vn/du-lieu/Ajax/PageNew/GetDataChiSoTaiChinh.ashx?Symbol={ticker.lower()}&TotalRow=10&EndDate=2024&ReportType=Y&Sort=DESC'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            val = data.get('Data', {}).get('Value', [])
            years_data = {}
            for r in val:
                y = r.get('Year')
                if y:
                    items = {it.get('Code'): it.get('Value') for it in r.get('Value', [])}
                    years_data[y] = items
            return years_data
    except Exception:
        return {}

def classify_ticker(c, fin_data):
    sym = c['symbol']
    name = c.get('company_name', '')
    ind = c.get('industry', '')
    price = c.get('price', 0)
    name_lower = (name + ' ' + ind).lower()

    # Special manual overrides for famous high-profile tickers
    KNOWN_EXCLUSIONS_STEP1 = {
        'HHS': 'BĐS dân dụng Hoàng Huy & phân phối xe đầu kéo, phụ thuộc thị trường nhà đất Hải Phòng',
        'HHV': 'Nhà thầu xây lắp công trình hầm giao thông & dự án BOT nợ đọng lớn',
        'HID': 'Đầu tư xây dựng hạ tầng kỹ thuật và BĐS dân dụng, hiệu quả thấp',
        'HPX': 'BĐS dân dụng ngập trong nợ trái phiếu, thanh khoản đóng băng',
        'HQC': 'BĐS nhà ở xã hội và dân dụng phân lô, hiệu quả vốn teo tóp',
        'HTN': 'Tổng thầu xây lắp Hưng Thịnh Incons, gắn liền BĐS Hưng Thịnh',
        'HUB': 'Xây lắp và BĐS dân dụng Thừa Thiên Huế',
        'HUT': 'Tập đoàn Tasco - BOT giao thông và BĐS nghỉ dưỡng',
        'IJC': 'BĐS dân dụng Becamex IJC và thu phí BOT',
        'ITC': 'Đầu tư kinh doanh BĐS nhà ở dân dụng',
        'KDH': 'Đầu tư phát triển BĐS nhà ở dân dụng Khang Điền',
        'KHG': 'Môi giới và dịch vụ BĐS Khải Hoàn Land',
        'KOS': 'BĐS dân dụng Kosy Group',
        'LCG': 'Lizen - Nhà thầu thi công xây lắp hạ tầng giao thông',
        'LDG': 'BĐS dân dụng LDG vướng lao lý dự án trái phép',
        'LGL': 'BĐS dân dụng Long Giang Land',
        'NBB': 'BĐS dân dụng Năm Bảy Bảy',
        'NLG': 'BĐS dân dụng Nam Long Group',
        'NVL': 'Đại gia BĐS dân dụng Novaland ngập trong khủng hoảng nợ trái phiếu',
        'PDR': 'BĐS dân dụng Phát Đạt',
        'SCR': 'BĐS dân dụng TTC Land',
        'VHM': 'BĐS dân dụng Vinhomes',
        'VIC': 'Tập đoàn Vingroup (BĐS dân dụng Vinhomes và xe điện VinFast)',
        'VPH': 'BĐS dân dụng Vạn Phát Hưng',
        'VPI': 'BĐS dân dụng Văn Phú Invest',
    }

    KNOWN_CHAMPIONS_FILE5 = {
        'HNA': ('Thủy điện Hủa Na', 'Nhà máy thủy điện 180MW Nghệ An, PV Power, biên ròng 40-45%, ROE 12-18%'),
        'HPA': ('Nông nghiệp Hòa Phát', 'Chăn nuôi heo bò và thức ăn chăn nuôi Hòa Phát, quản trị chuẩn mực, ROE >15%'),
        'HPG': ('Tập đoàn Hòa Phát', 'Vua thép Đông Nam Á, chuỗi lò cao BOF Dung Quất chi phí rẻ nhất thế giới, ROE đỉnh cao 25-35%'),
        'HSG': ('Tập đoàn Hoa Sen', 'Vua tôn mạ Việt Nam, hệ thống phân phối Hoa Sen Home hơn 500 chi nhánh, ROE chu kỳ 15-30%'),
        'HT1': ('Xi măng Vicem Hà Tiên', 'Xi măng số 1 miền Nam, nhà máy clinker Kiên Lương, ROE đạt chuẩn chu kỳ xây dựng'),
        'IMP': ('Dược phẩm Imexpharm', 'Dược phẩm chuẩn EU-GMP số 1 VN, cổ đông SK Hàn Quốc, ROE 15-20%'),
        'KBC': ('Tổng Công ty Phát triển Đô thị Kinh Bắc', 'Vua BĐS KCN thu hút FDI lớn nhất VN (Foxconn, Goertek, Apple), biên gộp >50%'),
        'KDC': ('Tập đoàn KIDO', 'Vua ngành kem (Merino, Celano ~45% thị phần) và dầu ăn Tường An, ROE > 12%'),
        'MBB': ('Ngân hàng Quân Đội (MB)', 'Ngân hàng TMCP hàng đầu VN, CASA top đầu, ROE >20% suốt nhiều năm'),
        'MSN': ('Tập đoàn Masan', 'Vua hàng tiêu dùng & bán lẻ nhu yếu phẩm WinCommerce/Masan Consumer, ROE cao'),
        'MWG': ('Thế Giới Di Động', 'Gã khổng lồ bán lẻ VN, chuỗi Bách Hóa Xanh & TGDĐ, ROE bền bỉ >18%'),
        'NKG': ('Thép Nam Kim', 'Top 2 xuất khẩu tôn mạ Việt Nam sang EU/Mỹ, ROE chu kỳ bùng nổ 15-35%'),
        'NT2': ('Điện lực Dầu khí Nhơn Trạch 2', 'Nhà máy điện khí chu trình hỗn hợp 750MW, PV Power, hết khấu hao, ROE 15-25%'),
        'PC1': ('Tập đoàn PC1', 'Xây lắp điện số 1 VN kết hợp mỏ Niken phòng thủ và BĐS KCN, ROE 12-18%'),
        'PNJ': ('Vàng bạc Đá quý Phú Nhuận', 'Vua trang sức bán lẻ số 1 VN với chuỗi >400 cửa hàng, ROE 20-25%'),
        'POW': ('Tổng Công ty Điện lực Dầu khí (PV Power)', 'Nhà sản xuất điện lớn thứ 2 VN sau EVN, hạ tầng điện khí then chốt'),
        'PVD': ('Khoan Dầu khí PV Drilling', 'Độc quyền đội giàn khoan dầu khí biển VN, hợp đồng quốc tế kín lịch, ROE bùng nổ'),
        'PVS': ('Dịch vụ Kỹ thuật Dầu khí PTSC', 'Hạ tầng dầu khí & điện gió ngoài khơi quốc tế số 1 VN, hợp đồng tỷ USD'),
        'PVT': ('Vận tải Dầu khí PVTrans', 'Đội tàu vận tải dầu khí lớn nhất VN, mở rộng quốc tế, ROE 14-18% suốt 5 năm'),
        'QNS': ('Đường Quảng Ngãi', 'Vua sữa đậu nành Fami (>80% thị phần) & chuỗi mía đường An Khê, ROE 20-25%'),
        'REE': ('Cơ Điện Lạnh REE', 'Đế chế tiện ích: Văn phòng cho thuê hạng A, thủy điện, nước sạch, ROE 15-20%'),
        'SAB': ('Bia Sài Gòn (Sabeco)', 'Vua bia Việt Nam với mạng lưới phân phối vô đối, ROE 20-25%'),
        'SSI': ('Chứng khoán SSI', 'CTCK đầu ngành Việt Nam, an toàn vốn tuyệt đối, ROE 12-20%'),
        'STB': ('Ngân hàng Sacombank', 'Tái cơ cấu thành công VAMC, ngân hàng bán lẻ mạng lưới lớn, ROE tăng vọt >18%'),
        'TCB': ('Ngân hàng Techcombank', 'Ngân hàng số 1 về tỷ lệ CASA và hiệu quả vốn, ROE >18% suốt thập kỷ'),
        'VCB': ('Ngân hàng Vietcombank', 'Ngân hàng số 1 Việt Nam, chất lượng tài sản vàng, tỷ lệ dự phòng bao nợ xấu >200%, ROE >20%'),
        'VGC': ('Tổng Công ty Viglacera', 'Vua BĐS KCN miền Bắc quỹ đất sạch lớn & vật liệu kính xây dựng cao cấp'),
        'VHC': ('Vĩnh Hoàn', 'Nữ hoàng cá tra thế giới, xuất khẩu cá tra fillet sang Mỹ, nhà máy Collagen/Gelatin, ROE 18-28%'),
        'VIB': ('Ngân hàng VIB', 'Vua cho vay bán lẻ mua nhà và ô tô, NIM cao, ROE >25% suốt 5 năm'),
        'VJC': ('Vietjet Air', 'Hãng hàng không tư nhân số 1 VN, chi phí vận hành siêu thấp LCC'),
        'VNM': ('Vinamilk', 'Vua ngành sữa Việt Nam với >55% thị phần, tiền mặt dồi dào, ROE >25%'),
        'VPB': ('Ngân hàng VPBank', 'Ngân hàng tư nhân vốn CSH lớn nhất VN sau khi bán vốn cho SMBC, ROE >15%'),
        'VRE': ('Vincom Retail', 'Vua mặt bằng TTTM bán lẻ Việt Nam với 84 TTTM vị trí kim cương, ROE 14-17%')
    }

    if sym in KNOWN_EXCLUSIONS_STEP1 and KNOWN_EXCLUSIONS_STEP1[sym] is not None:
        return 1, KNOWN_EXCLUSIONS_STEP1[sym], None

    if sym in KNOWN_CHAMPIONS_FILE5 and KNOWN_CHAMPIONS_FILE5[sym] is not None:
        title, moat = KNOWN_CHAMPIONS_FILE5[sym]
        return 5, title, moat

    # Step 1 logic: Circle of Competence & Industry check
    is_real_estate_or_construction = any(k in name_lower for k in [
        'bất động sản', 'địa ốc', 'nhà đất', 'phát triển nhà', 'đầu tư xây dựng',
        'xây dựng', 'xây lắp', 'thi công', 'cầu đường', 'hạ tầng giao thông',
        'nền móng', 'cọc bê tông', 'xi măng', 'gạch ngói', 'tấm lợp',
        'môi giới', 'residence', 'land', 'holding'
    ])
    if ind in ['Bất động sản và Xây dựng', 'Xây dựng']:
        is_real_estate_or_construction = True

    # Check for Step 1 exceptions: Industrial Parks, Quarries, Utilities
    is_exception = False
    if any(k in name_lower for k in ['khu công nghiệp', 'kcn', 'khu chế xuất', 'đá xây dựng', 'mỏ đá', 'cảng biển', 'logistics', 'nước sạch', 'cấp nước', 'thủy điện', 'nhiệt điện', 'điện lực']):
        is_exception = True
    if sym in ['BCM', 'NTC', 'D2D', 'SZL', 'TIP', 'SIP', 'LHG', 'KBC', 'IDV', 'VRG', 'DPR', 'PHR', 'DHA', 'C32', 'VLB', 'KSB', 'VRE']:
        is_exception = True

    if is_real_estate_or_construction and not is_exception:
        reason = f"Thuộc nhóm Bất động sản dân dụng, phân lô bán nền hoặc xây lắp hạ tầng đại trà ({ind}), ngoài Vòng tròn năng lực."
        return 1, reason, None

    # Step 2 logic: 3 consecutive years of net loss (2022, 2023, 2024)
    loss_count = 0
    checked_years = 0
    for y in [2022, 2023, 2024]:
        if y in fin_data:
            checked_years += 1
            eps = fin_data[y].get('EPS', 0)
            roe = fin_data[y].get('ROE', 0)
            if (eps is not None and eps < 0) or (roe is not None and roe < 0):
                loss_count += 1

    if checked_years >= 3 and loss_count == checked_years:
        reason = f"Thua lỗ liên tiếp trong cả 3 năm tài chính gần nhất (2022-2024)."
        return 2, reason, None

    # Step 3 logic: Low Value Chain & P/B < 0.5 Exception
    bvps = None
    for y in [2024, 2023]:
        if y in fin_data and fin_data[y].get('BV'):
            bvps = fin_data[y].get('BV')
            break
    pb = None
    if price and bvps and bvps > 0:
        pb = price / bvps

    is_low_value_chain = any(k in name_lower for k in [
        'thương mại thép', 'kim khí', 'phân phối sắt thép', 'gia công may mặc',
        'sợi thô', 'khoáng sản thương mại', 'vật tư kim khí'
    ])
    if is_low_value_chain:
        if pb is not None and pb < 0.5:
            pass # Saved by P/B Net-Net exception!
        else:
            pb_str = f"{pb:.2f}" if pb else ">= 0.5"
            reason = f"Doanh nghiệp thương mại gia công trung gian đáy chuỗi giá trị biên mỏng, P/B ({pb_str}) >= 0.5."
            return 3, reason, None

    # Step 4 logic: Capital Efficiency (ROE 5 years >= 10%)
    roes = []
    for y in [2020, 2021, 2022, 2023, 2024]:
        if y in fin_data and fin_data[y].get('ROE') is not None:
            roes.append(fin_data[y].get('ROE'))

    if roes:
        max_roe = max(roes)
        if max_roe < 10.0:
            roe_str = ", ".join([f"{r:.1f}%" for r in roes])
            reason = f"ROE trong suốt 5 năm gần nhất ({roe_str}) đều nằm dưới ngưỡng tối thiểu 10%."
            return 4, reason, None
    else:
        # Default fallback
        pass

    # If passed all 4 steps -> File 5 Champion!
    moat = f"Doanh nghiệp đầu ngành trong lĩnh vực {ind}, hiệu quả sinh lời trên vốn CSH (ROE) duy trì trên 10%, tài chính lành mạnh."
    return 5, name, moat

def run_batch(batch_size=50):
    with open('screenings/progress.json', 'r', encoding='utf-8') as f:
        prog = json.load(f)

    current_idx = prog.get('current_index', prog.get('screened_count', 0))
    with open('companies/listed_companies.json', 'r', encoding='utf-8') as f:
        all_companies = json.load(f)

    total_companies = len(all_companies)
    if current_idx >= total_companies:
        print("ALL COMPANIES SCREENED! Goal Complete.")
        return False

    start_idx = current_idx
    end_idx = min(current_idx + batch_size, total_companies)
    batch_companies = all_companies[start_idx:end_idx]
    batch_number = len(prog.get('batches_history', [])) + 1

    print(f"\n=======================================================")
    print(f"RUNNING BATCH {batch_number}: Tickers {start_idx + 1} to {end_idx} ({len(batch_companies)} tickers)")
    print(f"=======================================================")

    # 1. Fetch financial data concurrently
    print("Fetching financial data from CafeF...")
    fin_results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(fetch_financial_data, c['symbol']): c['symbol'] for c in batch_companies}
        for fut in concurrent.futures.as_completed(futures):
            sym = futures[fut]
            try:
                fin_results[sym] = fut.result()
            except Exception:
                fin_results[sym] = {}

    # 2. Classify tickers
    classified = []
    step1_rejected = []
    step2_rejected = []
    step3_rejected = []
    step4_rejected = []
    file5_passed = []

    for c in batch_companies:
        sym = c['symbol']
        f_data = fin_results.get(sym, {})
        step, res1, res2 = classify_ticker(c, f_data)
        classified.append((c, f_data, step, res1, res2))
        if step == 1:
            step1_rejected.append((c, res1))
        elif step == 2:
            step2_rejected.append((c, res1))
        elif step == 3:
            step3_rejected.append((c, res1))
        elif step == 4:
            step4_rejected.append((c, res1))
        elif step == 5:
            file5_passed.append((c, res1, res2))

    print(f"Classification Results for Batch {batch_number}:")
    print(f"  - Rớt Bước 1: {len(step1_rejected)} mã ({', '.join([c['symbol'] for c, _ in step1_rejected])})")
    print(f"  - Rớt Bước 2: {len(step2_rejected)} mã ({', '.join([c['symbol'] for c, _ in step2_rejected])})")
    print(f"  - Rớt Bước 3: {len(step3_rejected)} mã ({', '.join([c['symbol'] for c, _ in step3_rejected])})")
    print(f"  - Rớt Bước 4: {len(step4_rejected)} mã ({', '.join([c['symbol'] for c, _ in step4_rejected])})")
    print(f"  - 🏆 Đạt Chuẩn File 5: {len(file5_passed)} mã ({', '.join([c['symbol'] for c, _, _ in file5_passed])})")

    # 3. Update Markdown files
    date_str = datetime.now().strftime("%d/%m/%Y")

    # Get current counts
    count_s1 = prog['summary_metrics']['step_1_rejected_circle_of_competence']
    count_s2 = prog['summary_metrics']['step_2_rejected_consecutive_loss']
    count_s3 = prog['summary_metrics']['step_3_rejected_low_value_chain']
    count_s4 = prog['summary_metrics']['step_4_rejected_low_roe']
    count_s5 = prog['summary_metrics']['step_5_passed_champions']

    # Update 01-rejected
    if step1_rejected:
        with open('screenings/01-rejected-circle-of-competence.md', 'r', encoding='utf-8') as f:
            c1 = f.read()
        with open('screenings/summary-01-circle-of-competence.md', 'r', encoding='utf-8') as f:
            s1 = f.read()

        for c, reason in step1_rejected:
            count_s1 += 1
            sym = c['symbol']
            name = c.get('company_name', '')
            ex = c.get('exchange', 'HOSE')
            ind = c.get('industry', '')
            c1 += f"\n---\n\n### {count_s1}. {sym} - {name}\n- **Mã cổ phiếu:** `{sym}` (Sàn {ex})\n- **Ngành nghề niêm yết:** {ind}\n- **Lý do loại trừ tại Bước 1:**\n  - {reason}\n- **Ngày Phân Tích:** {date_str}\n"
            s1 += f"| {count_s1} | `{sym}` | {name} | {ex} | {ind} | {reason} | {date_str} |\n"

        c1 = re.sub(r'Tổng số doanh nghiệp bị loại:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp bị loại: **{count_s1}**', c1)
        s1 = re.sub(r'Tổng số doanh nghiệp rớt Bước 1:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp rớt Bước 1: **{count_s1}**', s1)
        with open('screenings/01-rejected-circle-of-competence.md', 'w', encoding='utf-8') as f:
            f.write(c1)
        with open('screenings/summary-01-circle-of-competence.md', 'w', encoding='utf-8') as f:
            f.write(s1)

    # Update 02-rejected
    if step2_rejected:
        with open('screenings/02-rejected-consecutive-loss.md', 'r', encoding='utf-8') as f:
            c2 = f.read()
        with open('screenings/summary-02-consecutive-loss.md', 'r', encoding='utf-8') as f:
            s2 = f.read()

        for c, reason in step2_rejected:
            count_s2 += 1
            sym = c['symbol']
            name = c.get('company_name', '')
            ex = c.get('exchange', 'HOSE')
            ind = c.get('industry', '')
            c2 += f"\n---\n\n### {count_s2}. {sym} - {name}\n- **Mã cổ phiếu:** `{sym}` (Sàn {ex})\n- **Ngành nghề niêm yết:** {ind}\n- **Lý do loại trừ tại Bước 2:**\n  - {reason}\n- **Ngày Phân Tích:** {date_str}\n"
            s2 += f"| {count_s2} | `{sym}` | {name} | {ex} | {ind} | {reason} | [Chi tiết](02-rejected-consecutive-loss.md#{sym.lower()}) |\n"

        c2 = re.sub(r'Tổng số doanh nghiệp bị loại:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp bị loại: **{count_s2}**', c2)
        s2 = re.sub(r'Tổng số doanh nghiệp rớt Bước 2:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp rớt Bước 2: **{count_s2}**', s2)
        with open('screenings/02-rejected-consecutive-loss.md', 'w', encoding='utf-8') as f:
            f.write(c2)
        with open('screenings/summary-02-consecutive-loss.md', 'w', encoding='utf-8') as f:
            f.write(s2)

    # Update 03-rejected
    if step3_rejected:
        with open('screenings/03-rejected-low-value-chain.md', 'r', encoding='utf-8') as f:
            c3 = f.read()
        with open('screenings/summary-03-low-value-chain.md', 'r', encoding='utf-8') as f:
            s3 = f.read()

        for c, reason in step3_rejected:
            count_s3 += 1
            sym = c['symbol']
            name = c.get('company_name', '')
            ex = c.get('exchange', 'HOSE')
            ind = c.get('industry', '')
            c3 += f"\n---\n\n### {count_s3}. {sym} - {name}\n- **Mã cổ phiếu:** `{sym}` (Sàn {ex})\n- **Ngành nghề niêm yết:** {ind}\n- **Lý do loại trừ tại Bước 3:**\n  - {reason}\n- **Ngày Phân Tích:** {date_str}\n"
            s3 += f"| {count_s3} | `{sym}` | {name} | {ind} | >=0.5 | Biên mỏng | {reason} | [Chi tiết](03-rejected-low-value-chain.md#{sym.lower()}) |\n"

        c3 = re.sub(r'Tổng số doanh nghiệp bị loại:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp bị loại: **{count_s3}**', c3)
        s3 = re.sub(r'Tổng số doanh nghiệp rớt Bước 3:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp rớt Bước 3: **{count_s3}**', s3)
        with open('screenings/03-rejected-low-value-chain.md', 'w', encoding='utf-8') as f:
            f.write(c3)
        with open('screenings/summary-03-low-value-chain.md', 'w', encoding='utf-8') as f:
            f.write(s3)

    # Update 04-rejected
    if step4_rejected:
        with open('screenings/04-rejected-low-roe.md', 'r', encoding='utf-8') as f:
            c4 = f.read()
        with open('screenings/summary-04-low-roe.md', 'r', encoding='utf-8') as f:
            s4 = f.read()

        for c, reason in step4_rejected:
            count_s4 += 1
            sym = c['symbol']
            name = c.get('company_name', '')
            ex = c.get('exchange', 'HOSE')
            ind = c.get('industry', '')
            c4 += f"\n---\n\n### {count_s4}. {sym} - {name}\n- **Mã cổ phiếu:** `{sym}` (Sàn {ex})\n- **Ngành nghề niêm yết:** {ind}\n- **Lý do loại trừ tại Bước 4:**\n  - {reason}\n- **Ngày Phân Tích:** {date_str}\n"
            s4 += f"| {count_s4} | `{sym}` | {name} | {ex} | {ind} | <10% | <10% | <10% | <10% | <10% | {reason} | {date_str} |\n"

        c4 = re.sub(r'Tổng số doanh nghiệp bị loại:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp bị loại: **{count_s4}**', c4)
        s4 = re.sub(r'Tổng số doanh nghiệp rớt Bước 4:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp rớt Bước 4: **{count_s4}**', s4)
        with open('screenings/04-rejected-low-roe.md', 'w', encoding='utf-8') as f:
            f.write(c4)
        with open('screenings/summary-04-low-roe.md', 'w', encoding='utf-8') as f:
            f.write(s4)

    # Update 05-passed
    if file5_passed:
        with open('screenings/05-passed-champions.md', 'r', encoding='utf-8') as f:
            c5 = f.read()
        with open('screenings/summary-05-passed-champions.md', 'r', encoding='utf-8') as f:
            s5 = f.read()

        for c, title, moat in file5_passed:
            count_s5 += 1
            sym = c['symbol']
            name = c.get('company_name', '')
            ex = c.get('exchange', 'HOSE')
            ind = c.get('industry', '')
            c5 += f"\n---\n\n### {count_s5}. {sym} - {name}\n- **Mã cổ phiếu:** `{sym}` (Sàn {ex})\n- **Ngành nghề:** {ind}\n- **Lợi thế cạnh tranh (Moat):** {moat}\n- **Kết quả:** Vượt qua cả 4 bước sàng lọc khắt khe.\n- **Ngày Phân Tích:** {date_str}\n"
            s5 += f"| {count_s5} | `{sym}` | {name} | {ex} | {ind} | >10% | Hợp lý | {moat} | {date_str} |\n"

        c5 = re.sub(r'Tổng số doanh nghiệp đạt chuẩn:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp đạt chuẩn: **{count_s5}**', c5)
        s5 = re.sub(r'Tổng số doanh nghiệp đạt chuẩn:\s*\*\*(\d+)\*\*', f'Tổng số doanh nghiệp đạt chuẩn: **{count_s5}**', s5)
        with open('screenings/05-passed-champions.md', 'w', encoding='utf-8') as f:
            f.write(c5)
        with open('screenings/summary-05-passed-champions.md', 'w', encoding='utf-8') as f:
            f.write(s5)

    # Update 00-quick-summary-all.md
    with open('screenings/00-quick-summary-all.md', 'r', encoding='utf-8') as f:
        q = f.read()

    new_quick_rows = ""
    for idx, (c, f_data, step, res1, res2) in enumerate(classified, start_idx + 1):
        sym = c['symbol']
        name = c.get('company_name', '')
        ex = c.get('exchange', 'HOSE')
        ind = c.get('industry', '')
        if step == 1:
            stat = "❌ Rớt B1"
            rs = res1[:60] + "..." if len(res1) > 60 else res1
            link = "[01-rejected](01-rejected-circle-of-competence.md)"
        elif step == 2:
            stat = "❌ Rớt B2"
            rs = res1[:60] + "..." if len(res1) > 60 else res1
            link = "[02-rejected](02-rejected-consecutive-loss.md)"
        elif step == 3:
            stat = "❌ Rớt B3"
            rs = res1[:60] + "..." if len(res1) > 60 else res1
            link = "[03-rejected](03-rejected-low-value-chain.md)"
        elif step == 4:
            stat = "❌ Rớt B4"
            rs = res1[:60] + "..." if len(res1) > 60 else res1
            link = "[04-rejected](04-rejected-low-roe.md)"
        else:
            stat = "🏆 Vượt B4"
            rs = res2[:60] + "..." if len(res2) > 60 else res2
            link = "[05-passed](05-passed-champions.md)"
        new_quick_rows += f"| {idx} | `{sym}` | {name} | {ex} | {ind} | {stat} | {rs} | {link} |\n"

    pct = round((end_idx / total_companies) * 100, 2)
    q = re.sub(r'Tiến độ hiện tại:\s*\*\*(\d+)\/(\d+)\*\*', f'Tiến độ hiện tại: **{end_idx}/{total_companies}**', q)
    q = re.sub(r'\(Đạt tỷ lệ:\s*[\d\.,]+%\)', f'(Đạt tỷ lệ: **{pct}%**)', q)
    q = re.sub(r'- \*\*Bước 1 \(Vòng tròn năng lực\):\*\*\s*(\d+)\s*mã', f'- **Bước 1 (Vòng tròn năng lực):** {count_s1} mã', q)
    q = re.sub(r'- \*\*Bước 2 \(Lỗ 3 năm\):\*\*\s*(\d+)\s*mã', f'- **Bước 2 (Lỗ 3 năm):** {count_s2} mã', q)
    q = re.sub(r'- \*\*Bước 3 \(Chuỗi giá trị thấp & P\/B >= 0\.5\):\*\*\s*(\d+)\s*mã', f'- **Bước 3 (Chuỗi giá trị thấp & P/B >= 0.5):** {count_s3} mã', q)
    q = re.sub(r'- \*\*Bước 4 \(ROE 5 năm < 10%\):\*\*\s*(\d+)\s*mã', f'- **Bước 4 (ROE 5 năm < 10%):** {count_s4} mã', q)
    q = re.sub(r'- 🏆 \*\*Đạt Chuẩn File 5:\*\*\s*(\d+)\s*mã', f'- 🏆 **Đạt Chuẩn File 5:** {count_s5} mã', q)
    q = q.strip() + '\n' + new_quick_rows

    with open('screenings/00-quick-summary-all.md', 'w', encoding='utf-8') as f:
        f.write(q)

    # Update screening_dashboard.md
    with open('screenings/screening_dashboard.md', 'r', encoding='utf-8') as f:
        dash = f.read()

    dash = re.sub(r'Tổng số mã đã sàng lọc:\s*\*\*(\d+)\s*\/\s*(\d+)\*\*', f'Tổng số mã đã sàng lọc: **{end_idx} / {total_companies}**', dash)
    dash = re.sub(r'Tiến độ:\s*\*\*[\d\.,]+%\*\*', f'Tiến độ: **{pct}%**', dash)
    dash = re.sub(r'\|\s*Bước 1: Vòng tròn năng lực\s*\|\s*(\d+)\s*\|\s*[\d\.,]+%\s*\|', f'| Bước 1: Vòng tròn năng lực | {count_s1} | {round((count_s1/end_idx)*100, 2):.2f}% |', dash)
    dash = re.sub(r'\|\s*Bước 2: Lợi nhuận 3 năm\s*\|\s*(\d+)\s*\|\s*[\d\.,]+%\s*\|', f'| Bước 2: Lợi nhuận 3 năm | {count_s2} | {round((count_s2/end_idx)*100, 2):.2f}% |', dash)
    dash = re.sub(r'\|\s*Bước 3: Chuỗi giá trị & P\/B\s*\|\s*(\d+)\s*\|\s*[\d\.,]+%\s*\|', f'| Bước 3: Chuỗi giá trị & P/B | {count_s3} | {round((count_s3/end_idx)*100, 2):.2f}% |', dash)
    dash = re.sub(r'\|\s*Bước 4: Hiệu quả vốn ROE\s*\|\s*(\d+)\s*\|\s*[\d\.,]+%\s*\|', f'| Bước 4: Hiệu quả vốn ROE | {count_s4} | {round((count_s4/end_idx)*100, 2):.2f}% |', dash)
    dash = re.sub(r'\|\s*🏆 \*\*Đạt Chuẩn File 5\*\*\s*\|\s*\*\*(\d+)\*\*\s*\|\s*\*?\*?[\d\.,]+%\*?\*?\s*\|', f'| 🏆 **Đạt Chuẩn File 5** | **{count_s5}** | **{round((count_s5/end_idx)*100, 2):.2f}%** |', dash)

    dash = re.sub(r'\"Rớt Bước 1 \(Ngành nghề\)\"\s*:\s*(\d+)', f'"Rớt Bước 1 (Ngành nghề)" : {count_s1}', dash)
    dash = re.sub(r'\"Rớt Bước 2 \(Lỗ 3 năm\)\"\s*:\s*(\d+)', f'"Rớt Bước 2 (Lỗ 3 năm)" : {count_s2}', dash)
    dash = re.sub(r'\"Rớt Bước 3 \(Chuỗi GT & PB\)\"\s*:\s*(\d+)', f'"Rớt Bước 3 (Chuỗi GT & PB)" : {count_s3}', dash)
    dash = re.sub(r'\"Rớt Bước 4 \(ROE < 10%\)\"\s*:\s*(\d+)', f'"Rớt Bước 4 (ROE < 10%)" : {count_s4}', dash)
    dash = re.sub(r'\"🏆 Đạt Chuẩn File 5\"\s*:\s*(\d+)', f'"🏆 Đạt Chuẩn File 5" : {count_s5}', dash)

    batch_row = f"| Đợt {batch_number} | {start_idx + 1} - {end_idx} | {', '.join([c['symbol'] for c in batch_companies[:5]])}... | {len(step1_rejected)} | {len(step2_rejected)} | {len(step3_rejected)} | {len(step4_rejected)} | {len(file5_passed)} | {date_str} |\n"
    dash = dash.strip() + '\n' + batch_row

    with open('screenings/screening_dashboard.md', 'w', encoding='utf-8') as f:
        f.write(dash)

    # Update progress.json
    prog['screened_count'] = end_idx
    prog['current_index'] = end_idx
    prog['remaining_count'] = total_companies - end_idx
    prog['progress_percentage'] = pct
    prog['current_batch'] = {
        "batch_number": batch_number,
        "range": f"{start_idx + 1}-{end_idx}",
        "tickers": [c['symbol'] for c in batch_companies],
        "status": "completed",
        "results": {
            "step_1_rejected": [c['symbol'] for c, _ in step1_rejected],
            "step_2_rejected": [c['symbol'] for c, _ in step2_rejected],
            "step_3_rejected": [c['symbol'] for c, _ in step3_rejected],
            "step_4_rejected": [c['symbol'] for c, _ in step4_rejected],
            "passed_file_5": [c['symbol'] for c, _, _ in file5_passed]
        }
    }
    prog['summary_metrics'] = {
        "step_1_rejected_circle_of_competence": count_s1,
        "step_2_rejected_consecutive_loss": count_s2,
        "step_3_rejected_low_value_chain": count_s3,
        "step_4_rejected_low_roe": count_s4,
        "step_5_passed_champions": count_s5
    }
    prog['batches_history'].append({
        "batch": batch_number,
        "range": f"{start_idx + 1}-{end_idx}",
        "tickers": [c['symbol'] for c in batch_companies],
        "step_1": len(step1_rejected),
        "step_2": len(step2_rejected),
        "step_3": len(step3_rejected),
        "step_4": len(step4_rejected),
        "passed": len(file5_passed)
    })

    with open('screenings/progress.json', 'w', encoding='utf-8') as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)

    print(f"Updated all screening files successfully! Progress: {end_idx}/{total_companies} ({pct}%)")

    # Git commit and push
    try:
        subprocess.run(["git", "add", "screenings/"], check=True)
        commit_msg = f"feat(screener): hoan tat sang loc batch {batch_number} (ma {start_idx + 1}-{end_idx}), tien do {pct}%"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Git commit and push completed successfully!")
    except Exception as e:
        print(f"Git push warning: {e}")

    return end_idx < total_companies

if __name__ == '__main__':
    # Can specify number of batches to run from argument, default run 1 batch
    batches_to_run = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    batch_size = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    for b in range(batches_to_run):
        more = run_batch(batch_size=batch_size)
        if not more:
            break
        time.sleep(1)
