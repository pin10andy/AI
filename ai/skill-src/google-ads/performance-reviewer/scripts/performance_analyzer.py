#!/usr/bin/env python3
"""
performance_analyzer.py — Google Ads 成效報表量化分析工具

用法：
  python3 performance_analyzer.py report.csv
  python3 performance_analyzer.py report.csv --level adgroup --format json
  python3 performance_analyzer.py report.csv --target-roas 2.5 --target-cpa 400
  python3 performance_analyzer.py                     # demo 模式
"""

import argparse
import csv
import json
import sys
from io import StringIO


# ---------------------------------------------------------------------------
# 欄位對照
# ---------------------------------------------------------------------------

COLUMN_MAP = {
    # 名稱
    '廣告活動': 'name', 'Campaign': 'name',
    '廣告群組': 'name', 'Ad group': 'name',
    '廣告': 'name', 'Ad': 'name',
    # 狀態
    '狀態': 'status', 'Status': 'status',
    # 點擊
    '點擊次數': 'clicks', 'Clicks': 'clicks',
    # 曝光
    '曝光次數': 'impressions', 'Impressions': 'impressions',
    # CTR
    '點閱率': 'ctr_raw', 'CTR': 'ctr_raw',
    # CPC
    '平均單次點擊出價': 'avg_cpc', '平均每次點擊出價': 'avg_cpc', 'Avg. CPC': 'avg_cpc',
    # 費用
    '費用': 'cost', 'Cost': 'cost',
    # 轉換
    '轉換次數': 'conversions', 'Conversions': 'conversions',
    # CPA
    '費用/轉換次數': 'cost_per_conv', 'Cost / conv.': 'cost_per_conv', 'Cost/conv.': 'cost_per_conv',
    # 轉換率
    '轉換率': 'conv_rate_raw', 'Conv. rate': 'conv_rate_raw',
    # 轉換值
    '所有轉換值': 'conv_value', 'All conv. value': 'conv_value',
    # ROAS
    '廣告投資報酬率': 'roas', 'ROAS': 'roas',
    # 曝光率
    '搜尋曝光佔有率': 'impression_share_raw', 'Search Impr. share': 'impression_share_raw',
}

DEMO_CSV = """廣告活動,廣告群組,點擊次數,曝光次數,點閱率,平均單次點擊出價,費用,轉換次數,費用/轉換次數,轉換率,所有轉換值
品牌_床墊,獨立筒,450,5200,8.65%,NT$26,NT$11700,55,NT$213,12.22%,NT$275000
品牌_床墊,記憶棉,280,3800,7.37%,NT$24,NT$6720,28,NT$240,10.00%,NT$140000
品牌_床墊,乳膠床墊,190,2600,7.31%,NT$25,NT$4750,18,NT$264,9.47%,NT$90000
品牌_床墊,護腰床墊,320,4100,7.80%,NT$27,NT$8640,42,NT$206,13.13%,NT$210000
品牌_床墊,品牌字,380,4200,9.05%,NT$15,NT$5700,58,NT$98,15.26%,NT$290000
品牌_枕頭,頸椎枕,210,2800,7.50%,NT$19,NT$3990,28,NT$143,13.33%,NT$112000
品牌_枕頭,乳膠枕,150,2100,7.14%,NT$20,NT$3000,18,NT$167,12.00%,NT$72000
品牌_枕頭,腰枕,95,1400,6.79%,NT$21,NT$1995,10,NT$200,10.53%,NT$40000
競品_搶量,競品A,85,3200,2.66%,NT$18,NT$1530,3,NT$510,3.53%,NT$9000
競品_搶量,競品B,62,2800,2.21%,NT$16,NT$992,2,NT$496,3.23%,NT$6000
再行銷,網站訪客,180,8500,2.12%,NT$12,NT$2160,22,NT$98,12.22%,NT$88000
再行銷,加購未結帳,95,4200,2.26%,NT$10,NT$950,18,NT$53,18.95%,NT$72000
"""


def parse_number(value: str) -> float:
    if not value or value.strip() in ('--', '-', ''):
        return 0.0
    cleaned = value.strip().replace('NT$', '').replace('$', '').replace('%', '').replace(',', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_pct(value: str) -> float:
    pct = parse_number(value)
    return pct / 100.0 if pct > 1.0 else pct


def parse_csv_content(content: str) -> list:
    reader = csv.reader(StringIO(content))
    rows = list(reader)
    if not rows:
        return []

    # 找標題列
    known = set(COLUMN_MAP.keys())
    header_idx = 0
    for i, row in enumerate(rows):
        if any(c.strip() in known for c in row):
            header_idx = i
            break

    header = rows[header_idx]
    col_idx = {}
    for i, col in enumerate(header):
        internal = COLUMN_MAP.get(col.strip())
        if internal and internal not in col_idx:
            col_idx[internal] = i

    if 'name' not in col_idx:
        print("[錯誤] 找不到名稱欄位（廣告活動/廣告群組）", file=sys.stderr)
        sys.exit(1)

    records = []
    for row in rows[header_idx + 1:]:
        if not row or not any(row):
            continue

        def get(key):
            idx = col_idx.get(key)
            return row[idx].strip() if idx is not None and idx < len(row) else ''

        name = get('name')
        if not name or name in ('總計', 'Total', '合計'):
            continue

        clicks = int(parse_number(get('clicks')))
        impressions = int(parse_number(get('impressions')))
        cost = parse_number(get('cost'))
        conversions = parse_number(get('conversions'))
        conv_value = parse_number(get('conv_value'))
        ctr = parse_pct(get('ctr_raw')) if get('ctr_raw') else (clicks / impressions if impressions > 0 else 0)
        conv_rate = parse_pct(get('conv_rate_raw')) if get('conv_rate_raw') else (conversions / clicks if clicks > 0 else 0)
        avg_cpc = parse_number(get('avg_cpc')) if get('avg_cpc') else (cost / clicks if clicks > 0 else 0)
        cost_per_conv = parse_number(get('cost_per_conv')) if get('cost_per_conv') else (cost / conversions if conversions > 0 else 0)
        roas = parse_number(get('roas')) if get('roas') else (conv_value / cost if cost > 0 else 0)

        records.append({
            'name': name,
            'status': get('status'),
            'clicks': clicks,
            'impressions': impressions,
            'ctr': round(ctr, 4),
            'avg_cpc': round(avg_cpc, 1),
            'cost': round(cost, 1),
            'conversions': round(conversions, 2),
            'conv_rate': round(conv_rate, 4),
            'cost_per_conv': round(cost_per_conv, 1),
            'conv_value': round(conv_value, 1),
            'roas': round(roas, 2),
        })

    return records


def analyze(records: list, target_roas: float = 0, target_cpa: float = 0,
            min_clicks: int = 30) -> dict:
    if not records:
        return {'error': '沒有可分析的資料'}

    total_cost = sum(r['cost'] for r in records)
    total_conv = sum(r['conversions'] for r in records)
    total_value = sum(r['conv_value'] for r in records)
    total_clicks = sum(r['clicks'] for r in records)

    overall_roas = total_value / total_cost if total_cost > 0 else 0
    overall_cpa = total_cost / total_conv if total_conv > 0 else 0
    overall_conv_rate = total_conv / total_clicks if total_clicks > 0 else 0

    # 如果沒設目標，用整體均值推估
    if target_roas <= 0:
        target_roas = overall_roas * 0.8  # 比均值低 20% 才算不達標
    if target_cpa <= 0:
        target_cpa = overall_cpa * 1.3   # 比均值高 30% 才算不達標

    keep = []
    pause = []
    scale = []
    test = []

    for r in records:
        verdict = _classify(r, target_roas, target_cpa, overall_conv_rate, min_clicks)
        entry = {**r, 'verdict': verdict['action'], 'reason': verdict['reason']}
        if verdict['action'] == '保留':
            keep.append(entry)
        elif verdict['action'] == '停用':
            pause.append(entry)
        elif verdict['action'] == '擴量':
            scale.append(entry)
        else:
            test.append(entry)

    return {
        'summary': {
            'total_items': len(records),
            'total_cost': round(total_cost, 1),
            'total_conversions': round(total_conv, 2),
            'overall_roas': round(overall_roas, 2),
            'overall_cpa': round(overall_cpa, 1),
            'overall_conv_rate_pct': round(overall_conv_rate * 100, 2),
        },
        'targets': {
            'roas': round(target_roas, 2),
            'cpa': round(target_cpa, 1),
        },
        'keep': sorted(keep, key=lambda x: x['roas'], reverse=True),
        'pause': sorted(pause, key=lambda x: x['cost'], reverse=True),
        'scale': sorted(scale, key=lambda x: x['roas'], reverse=True),
        'test': test,
        'counts': {
            'keep': len(keep),
            'pause': len(pause),
            'scale': len(scale),
            'test': len(test),
        },
    }


def _classify(r: dict, target_roas: float, target_cpa: float,
              avg_conv_rate: float, min_clicks: int) -> dict:
    clicks = r['clicks']
    cost = r['cost']
    conversions = r['conversions']
    roas = r['roas']
    cpa = r['cost_per_conv']
    conv_rate = r['conv_rate']

    # 資料不足 → 測試
    if clicks < min_clicks:
        return {'action': '測試', 'reason': f'點擊數僅 {clicks}，低於 {min_clicks} 的最低樣本門檻，暫不判斷'}

    # 零轉換 + 有花費 → 停用候選
    if conversions == 0 and cost > 0:
        return {'action': '停用', 'reason': f'花費 NT${cost:,.0f} 但轉換為 0，建議先檢查追蹤再考慮停用'}

    # 擴量：ROAS 高於目標 1.5x 且轉換率佳
    if roas > 0 and target_roas > 0 and roas >= target_roas * 1.5 and conv_rate >= avg_conv_rate:
        return {'action': '擴量', 'reason': f'ROAS {roas:.1f}x 達目標 {target_roas:.1f}x 的 {roas/target_roas:.1f} 倍，轉換率 {conv_rate*100:.1f}% 高於均值，建議增加預算'}

    # 停用：ROAS 低於目標且 CPA 過高
    if roas > 0 and target_roas > 0 and roas < target_roas * 0.6:
        return {'action': '停用', 'reason': f'ROAS {roas:.1f}x 僅達目標 {target_roas:.1f}x 的 {roas/target_roas*100:.0f}%，嚴重不達標'}

    if target_cpa > 0 and cpa > target_cpa * 1.5 and conversions > 3:
        return {'action': '停用', 'reason': f'CPA NT${cpa:,.0f} 超出目標 NT${target_cpa:,.0f} 的 {cpa/target_cpa:.1f} 倍'}

    # 保留：基本達標
    if roas > 0 and target_roas > 0 and roas >= target_roas:
        return {'action': '保留', 'reason': f'ROAS {roas:.1f}x 達標（目標 {target_roas:.1f}x），成效穩定'}

    if target_cpa > 0 and 0 < cpa <= target_cpa:
        return {'action': '保留', 'reason': f'CPA NT${cpa:,.0f} 達標（目標 NT${target_cpa:,.0f}），成效穩定'}

    # 預設：測試（數據模糊）
    return {'action': '測試', 'reason': f'ROAS {roas:.1f}x 接近目標 {target_roas:.1f}x，需更多數據確認趨勢'}


def format_text(result: dict) -> str:
    lines = []
    s = result['summary']
    t = result['targets']

    lines.append('=' * 65)
    lines.append('成效分析報告')
    lines.append(f'目標 ROAS：{t["roas"]:.1f}x  |  目標 CPA：NT${t["cpa"]:,.0f}')
    lines.append('=' * 65)

    lines.append('\n【整體摘要】')
    lines.append(f'  分析項目：{s["total_items"]} 個')
    lines.append(f'  總花費：  NT${s["total_cost"]:,.0f}')
    lines.append(f'  總轉換：  {s["total_conversions"]}')
    lines.append(f'  整體 ROAS：{s["overall_roas"]:.2f}x')
    lines.append(f'  整體 CPA： NT${s["overall_cpa"]:,.0f}')
    lines.append(f'  整體轉換率：{s["overall_conv_rate_pct"]}%')

    c = result['counts']
    lines.append(f'\n【判斷結果】保留 {c["keep"]} / 停用 {c["pause"]} / 擴量 {c["scale"]} / 測試 {c["test"]}')

    def table(items, title):
        if not items:
            return
        lines.append(f'\n▶ {title}（{len(items)} 個）')
        lines.append(f'  {"名稱":<24} {"費用":>8} {"轉換":>6} {"ROAS":>6}  原因')
        lines.append('  ' + '-' * 80)
        for r in items:
            lines.append(f'  {r["name"]:<24} NT${r["cost"]:>6,.0f} {r["conversions"]:>5}  {r["roas"]:>5.1f}x  {r["reason"]}')

    table(result['scale'], '🚀 擴量')
    table(result['keep'], '✅ 保留')
    table(result['test'], '🔬 測試')
    table(result['pause'], '⏸ 停用')

    lines.append('\n' + '=' * 65)
    lines.append('⚡ 下一步：將此結果提供給 Claude，做原因假設與下週優先事項')
    lines.append('=' * 65)
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Google Ads 成效報表量化分析工具')
    parser.add_argument('csv', nargs='?', help='成效報表 CSV 路徑（省略則 demo）')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--level', choices=['campaign', 'adgroup', 'ad'], default='adgroup')
    parser.add_argument('--target-roas', type=float, default=0)
    parser.add_argument('--target-cpa', type=float, default=0)
    parser.add_argument('--min-clicks', type=int, default=30)
    args = parser.parse_args()

    if args.csv:
        try:
            with open(args.csv, encoding='utf-8-sig') as f:
                content = f.read()
        except FileNotFoundError:
            print(f'[錯誤] 找不到檔案：{args.csv}', file=sys.stderr)
            sys.exit(1)
    else:
        print('[demo 模式] 使用內建範例資料\n', file=sys.stderr)
        content = DEMO_CSV

    records = parse_csv_content(content)
    if not records:
        print('[錯誤] CSV 沒有可解析的資料列', file=sys.stderr)
        sys.exit(1)

    result = analyze(records, target_roas=args.target_roas,
                     target_cpa=args.target_cpa, min_clicks=args.min_clicks)

    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))


if __name__ == '__main__':
    main()
