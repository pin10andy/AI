#!/usr/bin/env python3
"""
search_terms_analyzer.py — Google Ads 搜尋字詞 CSV 量化預篩工具

用法：
  python3 search_terms_analyzer.py report.csv
  python3 search_terms_analyzer.py report.csv --format json
  python3 search_terms_analyzer.py report.csv --cost-threshold 300 --min-clicks 5
  python3 search_terms_analyzer.py                     # demo 模式（內建範例資料）
"""

import argparse
import csv
import json
import sys
from io import StringIO
from collections import defaultdict


# ---------------------------------------------------------------------------
# 欄位名稱對照（繁體中文 ↔ 英文，Google Ads 匯出格式）
# ---------------------------------------------------------------------------

COLUMN_MAP = {
    # 搜尋字詞
    '搜尋字詞': 'term',
    'Search term': 'term',
    'search term': 'term',
    # 比對類型
    '比對類型': 'match_type',
    'Match type': 'match_type',
    # 已新增/已排除
    '已新增/已排除': 'added_excluded',
    'Added/Excluded': 'added_excluded',
    # 廣告活動
    '廣告活動': 'campaign',
    'Campaign': 'campaign',
    # 廣告群組
    '廣告群組': 'ad_group',
    'Ad group': 'ad_group',
    # 廣告活動類型
    '廣告活動類型': 'campaign_type',
    'Campaign type': 'campaign_type',
    # 點擊次數（傳統格式）
    '點擊次數': 'clicks',
    'Clicks': 'clicks',
    # 互動（PMax / 新版格式）
    '互動': 'clicks',
    'Interactions': 'clicks',
    # 曝光次數（傳統格式）
    '曝光次數': 'impressions',
    'Impressions': 'impressions',
    # 曝光（新版格式，無「次數」）
    '曝光': 'impressions',
    # 點閱率（傳統格式）
    '點閱率': 'ctr_raw',
    'CTR': 'ctr_raw',
    # 互動率（新版格式）
    '互動率': 'ctr_raw',
    'Interaction rate': 'ctr_raw',
    # 平均單次點擊出價（傳統格式）
    '平均單次點擊出價': 'avg_cpc',
    '平均每次點擊出價': 'avg_cpc',
    'Avg. CPC': 'avg_cpc',
    # 平均費用（新版格式，PMax 使用）
    '平均費用': 'avg_cpc',
    'Avg. cost': 'avg_cpc',
    # 費用
    '費用': 'cost',
    'Cost': 'cost',
    # 轉換次數（傳統格式）
    '轉換次數': 'conversions',
    'Conversions': 'conversions',
    # 轉換（新版格式，無「次數」）
    '轉換': 'conversions',
    # 費用／轉換次數
    '費用/轉換次數': 'cost_per_conv',
    'Cost / conv.': 'cost_per_conv',
    'Cost/conv.': 'cost_per_conv',
    # 單次轉換費用（新版格式）
    '單次轉換費用': 'cost_per_conv',
    'Cost per conversion': 'cost_per_conv',
    # 轉換率
    '轉換率': 'conv_rate_raw',
    'Conv. rate': 'conv_rate_raw',
    # 所有轉換次數
    '所有轉換次數': 'all_conv',
    'All conv.': 'all_conv',
    # 貨幣代碼（忽略，但需辨識）
    '貨幣代碼': 'currency',
    'Currency code': 'currency',
    # 平均千次曝光出價（忽略）
    '平均千次曝光出價': 'avg_cpm',
    'Avg. CPM': 'avg_cpm',
}


# ---------------------------------------------------------------------------
# Demo 資料（無 CSV 時使用）
# ---------------------------------------------------------------------------

DEMO_CSV = """搜尋字詞,廣告活動,廣告群組,點擊次數,曝光次數,點閱率,平均單次點擊出價,費用,轉換次數,費用/轉換次數,轉換率
床墊推薦,品牌_床墊,硬式床墊,120,1500,8.00%,NT$25,NT$3000,18,NT$167,15.00%
床墊哪個牌子好,品牌_床墊,硬式床墊,85,900,9.44%,NT$22,NT$1870,10,NT$187,11.76%
獨立筒床墊,品牌_床墊,獨立筒,200,2200,9.09%,NT$28,NT$5600,22,NT$255,11.00%
枕頭推薦,品牌_枕頭,頸椎枕,95,1100,8.64%,NT$18,NT$1710,12,NT$143,12.63%
撐腰枕頭,品牌_枕頭,腰枕,60,700,8.57%,NT$20,NT$1200,8,NT$150,13.33%
免費床墊,品牌_床墊,硬式床墊,15,800,1.88%,NT$12,NT$180,0,--,0.00%
床墊修理,品牌_床墊,硬式床墊,8,400,2.00%,NT$15,NT$120,0,--,0.00%
二手床墊,品牌_床墊,硬式床墊,12,600,2.00%,NT$10,NT$120,0,--,0.00%
床墊工廠招募,品牌_床墊,獨立筒,5,300,1.67%,NT$8,NT$40,0,--,0.00%
什麼是獨立筒,品牌_床墊,獨立筒,35,1200,2.92%,NT$15,NT$525,0,--,0.00%
床墊自己做 DIY,品牌_床墊,硬式床墊,10,500,2.00%,NT$10,NT$100,0,--,0.00%
宜家家居床墊,品牌_床墊,硬式床墊,18,700,2.57%,NT$20,NT$360,0,--,0.00%
記憶床墊評價,品牌_床墊,記憶棉,45,600,7.50%,NT$22,NT$990,6,NT$165,13.33%
乳膠床墊推薦,品牌_床墊,乳膠床墊,38,480,7.92%,NT$24,NT$912,5,NT$182,13.16%
腰痛床墊,品牌_床墊,護腰床墊,28,380,7.37%,NT$26,NT$728,4,NT$182,14.29%
低背痛床墊,品牌_床墊,護腰床墊,15,200,7.50%,NT$25,NT$375,2,NT$188,13.33%
頸椎枕頭推薦,品牌_枕頭,頸椎枕,42,550,7.64%,NT$19,NT$798,7,NT$114,16.67%
天然乳膠枕,品牌_枕頭,乳膠枕,30,420,7.14%,NT$22,NT$660,4,NT$165,13.33%
枕頭多高合適,品牌_枕頭,頸椎枕,22,800,2.75%,NT$16,NT$352,1,NT$352,4.55%
孕婦枕推薦,品牌_枕頭,特殊枕,18,350,5.14%,NT$18,NT$324,0,--,0.00%
床墊多少錢,品牌_床墊,硬式床墊,55,900,6.11%,NT$20,NT$1100,5,NT$220,9.09%
大島床墊,品牌_床墊,品牌字,90,1000,9.00%,NT$15,NT$1350,15,NT$90,16.67%
LOVEFU床墊,品牌_床墊,品牌字,75,850,8.82%,NT$14,NT$1050,14,NT$75,18.67%
床架推薦,品牌_床墊,硬式床墊,20,600,3.33%,NT$18,NT$360,1,NT$360,5.00%
寢具品牌,品牌_床墊,硬式床墊,25,700,3.57%,NT$16,NT$400,1,NT$400,4.00%
"""


# ---------------------------------------------------------------------------
# 數值解析
# ---------------------------------------------------------------------------

def parse_number(value: str) -> float:
    """將 Google Ads CSV 的數值字串轉為 float。處理 NT$、%、-- 等格式。"""
    if not value or value.strip() in ('--', '-', ''):
        return 0.0
    cleaned = value.strip().replace('NT$', '').replace('$', '').replace('%', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_ctr(value: str) -> float:
    """CTR 字串 → 小數（8.00% → 0.08）"""
    pct = parse_number(value)
    return pct / 100.0 if pct > 1.0 else pct


# ---------------------------------------------------------------------------
# CSV 解析
# ---------------------------------------------------------------------------

def detect_header_row(rows: list) -> int:
    """跳過 Google Ads 報表的前置說明列，找出實際標題列的索引。"""
    known_terms = set(COLUMN_MAP.keys())
    for i, row in enumerate(rows):
        for cell in row:
            if cell.strip() in known_terms:
                return i
    return 0


def load_csv(filepath: str) -> list:
    """讀取 CSV 並回傳正規化的 dict 列表。"""
    try:
        with open(filepath, encoding='utf-8-sig') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"[錯誤] 找不到檔案：{filepath}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        try:
            with open(filepath, encoding='big5') as f:
                content = f.read()
        except Exception as e:
            print(f"[錯誤] 無法讀取檔案（嘗試 UTF-8 和 Big5）：{e}", file=sys.stderr)
            sys.exit(1)

    return parse_csv_content(content)


def parse_csv_content(content: str) -> list:
    """解析 CSV 字串，回傳正規化的 dict 列表。"""
    reader = csv.reader(StringIO(content))
    rows = list(reader)
    if not rows:
        return []

    # 找標題列
    header_idx = detect_header_row(rows)
    header = rows[header_idx]

    # 建立欄位索引（對應到內部名稱）
    col_idx = {}
    for i, col_name in enumerate(header):
        internal = COLUMN_MAP.get(col_name.strip())
        if internal:
            col_idx[internal] = i

    if 'term' not in col_idx:
        print("[錯誤] 找不到「搜尋字詞」欄位，請確認 CSV 格式正確。", file=sys.stderr)
        sys.exit(1)

    records = []
    for row in rows[header_idx + 1:]:
        if not row or not any(row):
            continue
        term_raw = row[col_idx['term']].strip() if 'term' in col_idx and col_idx['term'] < len(row) else ''
        if not term_raw:
            continue
        # 跳過小計/總計行（可能是 "總計"、"合計" 或 "總計：xxx" 開頭的摘要列）
        if term_raw in ('總計', 'Total', '合計') or term_raw.startswith('總計：') or term_raw.startswith('合計：'):
            continue
        # Google Ads 有時在中文字之間插入空格（如 "乳膠 墊 如何 清洗"），統一移除
        term_val = term_raw.replace(' ', '')

        def get(key):
            idx = col_idx.get(key)
            return row[idx].strip() if idx is not None and idx < len(row) else ''

        clicks = int(parse_number(get('clicks')))
        impressions = int(parse_number(get('impressions')))
        cost = parse_number(get('cost'))
        conversions = parse_number(get('conversions'))
        ctr = parse_ctr(get('ctr_raw')) if get('ctr_raw') else (clicks / impressions if impressions > 0 else 0.0)
        conv_rate = parse_ctr(get('conv_rate_raw')) if get('conv_rate_raw') else (conversions / clicks if clicks > 0 else 0.0)
        avg_cpc = parse_number(get('avg_cpc')) if get('avg_cpc') else (cost / clicks if clicks > 0 else 0.0)
        cost_per_conv = parse_number(get('cost_per_conv')) if get('cost_per_conv') else (cost / conversions if conversions > 0 else 0.0)

        records.append({
            'term': term_val,
            'term_raw': term_raw,        # 保留原始格式（含空格）
            'match_type': get('match_type'),
            'campaign': get('campaign'),
            'ad_group': get('ad_group'),
            'campaign_type': get('campaign_type'),   # 最高成效 / 搜尋 / 多媒體
            'clicks': clicks,
            'impressions': impressions,
            'ctr': round(ctr, 4),
            'avg_cpc': round(avg_cpc, 1),
            'cost': round(cost, 1),
            'conversions': round(conversions, 2),
            'conv_rate': round(conv_rate, 4),
            'cost_per_conv': round(cost_per_conv, 1),
        })

    return records


# ---------------------------------------------------------------------------
# 分析核心
# ---------------------------------------------------------------------------

def analyze(records: list, cost_threshold: float = 300.0, min_clicks: int = 5,
            min_impressions: int = 100) -> dict:
    """對字詞清單做量化分類，回傳結構化結果。"""
    if not records:
        return {'error': '沒有可分析的資料'}

    total_cost = sum(r['cost'] for r in records)
    total_clicks = sum(r['clicks'] for r in records)
    total_conv = sum(r['conversions'] for r in records)
    avg_conv_rate = total_conv / total_clicks if total_clicks > 0 else 0
    avg_cpc = total_cost / total_clicks if total_clicks > 0 else 0

    negative_candidates = []
    new_group_candidates = []
    monitor = []
    wasted = []

    # 統計各字詞在哪些 ad group 出現
    term_groups = defaultdict(set)
    for r in records:
        term_groups[r['term']].add(r['ad_group'])

    for r in records:
        term = r['term']
        cost = r['cost']
        clicks = r['clicks']
        impressions = r['impressions']
        conversions = r['conversions']
        ctr = r['ctr']
        conv_rate = r['conv_rate']

        flags = []

        # --- 否定字候選 ---
        # 條件：花費超過閾值 且 轉換 = 0
        if cost >= cost_threshold and conversions == 0:
            flags.append('negative_high_cost')

        # --- 浪費字詞 ---
        # 條件：有花費 + 有點擊 + 轉換 = 0 + CTR < 2%（明確低效）
        if cost > 0 and clicks > 0 and conversions == 0 and ctr < 0.02:
            flags.append('wasted')

        # --- 低 CTR 但高曝光 ---
        if impressions >= min_impressions and ctr < 0.005:
            flags.append('low_ctr')

        # --- 新 ad group 候選 ---
        # 條件：點擊 > 門檻 + 轉換率高於均值 + 字詞出現在多個 ad group
        if clicks >= min_clicks and conv_rate > avg_conv_rate * 1.2 and len(term_groups[term]) >= 1:
            flags.append('new_group_candidate')

        # --- 監控 ---
        # 條件：有花費無轉換但曝光不足，暫時觀察
        if cost > 0 and conversions == 0 and impressions < min_impressions and 'negative_high_cost' not in flags:
            flags.append('monitor_insufficient_data')

        # 分配到各類別
        if 'negative_high_cost' in flags:
            negative_candidates.append({**r, 'flags': flags, 'suggested_level': _suggest_level(r)})
        elif 'wasted' in flags:
            wasted.append({**r, 'flags': flags})
        elif 'new_group_candidate' in flags:
            new_group_candidates.append({**r, 'flags': flags})
        elif 'monitor_insufficient_data' in flags or 'low_ctr' in flags:
            monitor.append({**r, 'flags': flags})

    wasted_total = sum(r['cost'] for r in wasted) + sum(r['cost'] for r in negative_candidates)

    return {
        'summary': {
            'total_terms': len(records),
            'total_cost': round(total_cost, 1),
            'total_clicks': total_clicks,
            'total_conversions': round(total_conv, 2),
            'avg_cpc': round(avg_cpc, 1),
            'avg_conv_rate_pct': round(avg_conv_rate * 100, 2),
            'wasted_cost': round(wasted_total, 1),
            'wasted_pct': round(wasted_total / total_cost * 100, 1) if total_cost > 0 else 0,
        },
        'negative_candidates': sorted(negative_candidates, key=lambda x: x['cost'], reverse=True),
        'new_group_candidates': sorted(new_group_candidates, key=lambda x: x['conv_rate'], reverse=True),
        'monitor': sorted(monitor, key=lambda x: x['cost'], reverse=True),
        'wasted': sorted(wasted, key=lambda x: x['cost'], reverse=True),
        'config': {
            'cost_threshold': cost_threshold,
            'min_clicks': min_clicks,
            'min_impressions': min_impressions,
        },
    }


def _suggest_level(r: dict) -> str:
    """依字詞特徵建議否定字應加入的層級。"""
    term = r['term'].lower()
    # 明確不相關：帳戶層級
    irrelevant_signals = ['免費', 'free', 'diy', '自己做', '招募', '徵才', '二手', '工廠', '修理', '維修']
    if any(s in term for s in irrelevant_signals):
        return '帳戶層級'
    # 資訊型：廣告活動層級
    info_signals = ['什麼是', '怎麼', '如何', '教學', '原理', '是什麼']
    if any(s in term for s in info_signals):
        return '廣告活動層級'
    # 預設：廣告群組層級
    return '廣告群組層級'


# ---------------------------------------------------------------------------
# 輸出格式
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    """產出人類易讀的文字報告。"""
    lines = []
    s = result['summary']
    cfg = result['config']

    lines.append('=' * 60)
    lines.append('搜尋字詞分析報告')
    lines.append(f'閾值設定：花費 NT${cfg["cost_threshold"]} | 最低點擊 {cfg["min_clicks"]}')
    lines.append('=' * 60)

    lines.append('\n【執行摘要】')
    lines.append(f'  分析字詞數：{s["total_terms"]}')
    lines.append(f'  總花費：    NT${s["total_cost"]:,.0f}')
    lines.append(f'  總轉換：    {s["total_conversions"]}')
    lines.append(f'  平均 CPC：  NT${s["avg_cpc"]}')
    lines.append(f'  平均轉換率：{s["avg_conv_rate_pct"]}%')
    lines.append(f'  ⚠ 浪費花費：NT${s["wasted_cost"]:,.0f}（佔 {s["wasted_pct"]}%）')

    # 否定字候選
    negs = result['negative_candidates']
    lines.append(f'\n【否定關鍵字候選】{len(negs)} 個（花費超過 NT${cfg["cost_threshold"]} 且零轉換）')
    if negs:
        lines.append(f'  {"搜尋字詞":<22} {"廣告群組":<20} {"花費":>8} {"點擊":>6} {"類型":<6} {"建議層級"}')
        lines.append('  ' + '-' * 82)
        for r in negs:
            ctype = r.get('campaign_type', '')[:4]
            lines.append(f'  {r["term"]:<22} {r["ad_group"]:<20} NT${r["cost"]:>6,.0f} {r["clicks"]:>5}  {ctype:<6} {r["suggested_level"]}')

    # 新 ad group 候選
    news = result['new_group_candidates']
    lines.append(f'\n【建議獨立廣告群組】{len(news)} 個（轉換率高於均值）')
    if news:
        lines.append(f'  {"搜尋字詞":<20} {"廣告群組":<20} {"點擊":>6} {"轉換率":>8}')
        lines.append('  ' + '-' * 60)
        for r in news:
            lines.append(f'  {r["term"]:<20} {r["ad_group"]:<20} {r["clicks"]:>5}  {r["conv_rate"]*100:.1f}%')

    # 浪費字詞
    wasted = result['wasted']
    wasted_total = sum(r['cost'] for r in wasted)
    lines.append(f'\n【浪費預算字詞】{len(wasted)} 個（有花費 + 低 CTR + 零轉換）')
    lines.append(f'  小計：NT${wasted_total:,.0f}')
    if wasted:
        lines.append(f'  {"搜尋字詞":<20} {"廣告群組":<20} {"花費":>8} {"CTR":>7}')
        lines.append('  ' + '-' * 60)
        for r in wasted[:10]:  # 最多顯示前 10 筆
            lines.append(f'  {r["term"]:<20} {r["ad_group"]:<20} NT${r["cost"]:>6,.0f} {r["ctr"]*100:>5.1f}%')
        if len(wasted) > 10:
            lines.append(f'  ... 另有 {len(wasted)-10} 筆（--format json 取得完整清單）')

    # 監控
    mon = result['monitor']
    lines.append(f'\n【持續監控】{len(mon)} 個（數據不足，暫不處理）')
    if mon:
        for r in mon[:5]:
            lines.append(f'  - {r["term"]}（NT${r["cost"]:.0f} 花費，{r["impressions"]} 曝光）')
        if len(mon) > 5:
            lines.append(f'  ... 另有 {len(mon)-5} 筆')

    lines.append('\n' + '=' * 60)
    lines.append('⚡ 下一步：將此結果提供給 Claude，做意圖分類與策略判斷')
    lines.append('=' * 60)

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Google Ads 搜尋字詞 CSV 量化預篩工具'
    )
    parser.add_argument('csv', nargs='?', help='搜尋字詞報表 CSV 路徑（省略則使用 demo 資料）')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='輸出格式（預設 text）')
    parser.add_argument('--cost-threshold', type=float, default=300.0,
                        help='花費閾值（NT$，預設 300）：超過此值且零轉換才列為否定候選')
    parser.add_argument('--min-clicks', type=int, default=5,
                        help='最低點擊門檻（預設 5）：新 ad group 候選需超過此值')
    parser.add_argument('--min-impressions', type=int, default=100,
                        help='最低曝光門檻（預設 100）：用於 CTR 計算的最低樣本數')
    args = parser.parse_args()

    # 載入資料
    if args.csv:
        records = load_csv(args.csv)
    else:
        print('[demo 模式] 使用內建範例資料\n', file=sys.stderr)
        records = parse_csv_content(DEMO_CSV)

    if not records:
        print('[錯誤] CSV 沒有可解析的資料列', file=sys.stderr)
        sys.exit(1)

    # 分析
    result = analyze(
        records,
        cost_threshold=args.cost_threshold,
        min_clicks=args.min_clicks,
        min_impressions=args.min_impressions,
    )

    # 輸出
    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))


if __name__ == '__main__':
    main()
