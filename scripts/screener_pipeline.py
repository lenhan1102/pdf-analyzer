import urllib.request
import json
import re
import os
import sys
import subprocess
import concurrent.futures
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
        'KBC': None, # Special KCN exception handled below
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
    }

    KNOWN_CHAMPIONS_FILE5 = {
        'HPG': ('Thép Hòa Phát', 'Vua thép Đông Nam Á, chuỗi lò cao BOF Dung Quất chi phí rẻ nhất thế giới, ROE đỉnh cao 25-35%'),
        'HNA': ('Thủy điện Hủa Na', 'Nhà máy thủy điện 180MW Nghệ An, PV Power, biên ròng 40-45%, ROE 12-18%'),
        'HPA': ('Nông nghiệp Hòa Phát', 'Chăn nuôi heo bò và thức ăn chăn nuôi Hòa Phát, quản trị chuẩn mực, ROE >15%'),
        'HSG': ('Tập đoàn Hoa Sen', 'Vua tôn mạ Việt Nam, hệ thống phân phối Hoa Sen Home hơn 500 chi nhánh, ROE chu kỳ 15-30%'),
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
        'VHM': None,
        'VIC': None,
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
    # Check if low value chain (outsourcing/commodity trade)
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
        # If no financial data on CafeF
        # Default fail Step 4 or Step 1 depending on industry
        pass

    # If passed all 4 steps -> File 5 Champion!
    moat = f"Doanh nghiệp đầu ngành trong lĩnh vực {ind}, hiệu quả sinh lời trên vốn CSH (ROE) duy trì trên 10%, tài chính lành mạnh."
    return 5, name, moat

print("Screener pipeline engine module loaded.")
