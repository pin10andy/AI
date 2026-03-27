#!/usr/bin/env python3
"""
ad_copy_validator.py — Google Ads RSA/PMax 文案格式驗證工具

用法：
  python3 ad_copy_validator.py --headlines "標題1|標題2|標題3" --descriptions "說明1|說明2"
  python3 ad_copy_validator.py --file copy.json
  python3 ad_copy_validator.py --format json --headlines "..."
  python3 ad_copy_validator.py                     # demo 模式
"""

import argparse
import json
import sys
import unicodedata


# ---------------------------------------------------------------------------
# 字元限制
# ---------------------------------------------------------------------------

RSA_HEADLINE_MAX = 30       # 標題字元上限
RSA_DESC_MAX = 90           # 說明字元上限
RSA_HEADLINE_MIN_COUNT = 3  # 最少標題數
RSA_HEADLINE_GOOD_COUNT = 12  # 達到 Good Ad Strength 的建議標題數
RSA_DESC_MIN_COUNT = 2
RSA_DESC_GOOD_COUNT = 4
SEARCH_RSA_EXACT_HEADLINE_COUNT = 15
SEARCH_RSA_EXACT_DESC_COUNT = 4
PMAX_EXACT_SHORT_HEADLINE_COUNT = 15
PMAX_EXACT_LONG_HEADLINE_COUNT = 5
PMAX_EXACT_DESC_COUNT = 5

PMAX_SHORT_HEADLINE_MAX = 30
PMAX_LONG_HEADLINE_MAX = 90
PMAX_DESC_MAX = 90
PMAX_DESC_SHORT_MAX = 60    # 至少 1 個說明需 ≤ 60 字元

# 禁用詞（從 master-brand.yaml voice.do_not 提取）
BRAND_FORBIDDEN_PATTERNS = [
    '免費', '最低價', '最便宜', '打折', '搶購', '限時瘋搶',
    '超便宜', '跳樓大拍賣', '史上最低',
]


# ---------------------------------------------------------------------------
# 字元計算（中文算 1，英文算 1）
# ---------------------------------------------------------------------------

def char_len(text: str) -> int:
    """計算文字長度，與 Google Ads 計算方式一致（中英文各算 1）。"""
    return sum(1 for c in text if unicodedata.east_asian_width(c) not in ('W', 'F'))  + \
           sum(1 for c in text if unicodedata.east_asian_width(c) in ('W', 'F'))


# 簡化版：直接計算字元數（Google Ads 對中文算全形寬度）
def google_char_len(text: str) -> int:
    """模擬 Google Ads 字元計數（全形中文字元算 1 個字元，與顯示寬度有別）。"""
    return len(text)


# ---------------------------------------------------------------------------
# 多樣性檢查
# ---------------------------------------------------------------------------

def diversity_score(texts: list) -> dict:
    """檢查標題間的語意多樣性（基於詞彙重疊率）。"""
    if len(texts) < 2:
        return {'score': 1.0, 'duplicates': []}

    duplicates = []
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            a, b = set(texts[i]), set(texts[j])
            overlap = len(a & b) / max(len(a), len(b), 1)
            if overlap > 0.6:
                duplicates.append({'pair': [texts[i], texts[j]], 'overlap_pct': round(overlap * 100)})

    return {
        'score': round(1 - len(duplicates) / max(len(texts), 1), 2),
        'duplicates': duplicates,
    }


def extract_texts(items: list) -> list:
    """Support string arrays, object arrays, and mixed legacy payloads."""
    texts = []
    for item in items or []:
        if isinstance(item, str):
            texts.append(item)
        elif isinstance(item, dict):
            text = item.get('text')
            if isinstance(text, str):
                texts.append(text)
    return texts


# ---------------------------------------------------------------------------
# 驗證核心
# ---------------------------------------------------------------------------

def validate_rsa(headlines: list, descriptions: list, exact_output: bool = False) -> dict:
    issues = []
    warnings = []

    # 標題數量
    if exact_output:
        if len(headlines) != SEARCH_RSA_EXACT_HEADLINE_COUNT:
            issues.append(
                f'Search RSA output 必須有 {SEARCH_RSA_EXACT_HEADLINE_COUNT} 個標題，目前為 {len(headlines)} 個'
            )
    else:
        if len(headlines) < RSA_HEADLINE_MIN_COUNT:
            issues.append(f'標題數量 {len(headlines)} 個，最少需要 {RSA_HEADLINE_MIN_COUNT} 個')
        elif len(headlines) < RSA_HEADLINE_GOOD_COUNT:
            warnings.append(f'標題數量 {len(headlines)} 個，建議 {RSA_HEADLINE_GOOD_COUNT} 個以達到 Good Ad Strength')

    # 說明數量
    if exact_output:
        if len(descriptions) != SEARCH_RSA_EXACT_DESC_COUNT:
            issues.append(
                f'Search RSA output 必須有 {SEARCH_RSA_EXACT_DESC_COUNT} 個說明，目前為 {len(descriptions)} 個'
            )
    else:
        if len(descriptions) < RSA_DESC_MIN_COUNT:
            issues.append(f'說明數量 {len(descriptions)} 個，最少需要 {RSA_DESC_MIN_COUNT} 個')
        elif len(descriptions) < RSA_DESC_GOOD_COUNT:
            warnings.append(f'說明數量 {len(descriptions)} 個，建議 {RSA_DESC_GOOD_COUNT} 個')

    # 標題字元限制
    headline_results = []
    for h in headlines:
        length = google_char_len(h)
        status = 'ok' if length <= RSA_HEADLINE_MAX else 'error'
        if status == 'error':
            issues.append(f'標題超出 {RSA_HEADLINE_MAX} 字元限制：「{h}」（{length} 字元）')
        # 禁用詞
        forbidden = [w for w in BRAND_FORBIDDEN_PATTERNS if w in h]
        if forbidden:
            issues.append(f'標題含品牌禁用詞「{forbidden[0]}」：「{h}」')
        headline_results.append({'text': h, 'length': length, 'status': status})

    # 說明字元限制
    desc_results = []
    for d in descriptions:
        length = google_char_len(d)
        status = 'ok' if length <= RSA_DESC_MAX else 'error'
        if status == 'error':
            issues.append(f'說明超出 {RSA_DESC_MAX} 字元限制：「{d[:20]}...」（{length} 字元）')
        desc_results.append({'text': d, 'length': length, 'status': status})

    # 多樣性
    div = diversity_score(headlines)
    if div['duplicates']:
        for dup in div['duplicates']:
            warnings.append(f'標題語意重疊 {dup["overlap_pct"]}%：「{dup["pair"][0]}」vs「{dup["pair"][1]}」')

    # Ad Strength 預估
    ad_strength = _estimate_ad_strength(len(headlines), len(descriptions), div['score'], len(issues))

    return {
        'type': 'RSA',
        'headlines': headline_results,
        'descriptions': desc_results,
        'issues': issues,
        'warnings': warnings,
        'diversity': div,
        'ad_strength_estimate': ad_strength,
        'passed': len(issues) == 0,
    }


def validate_pmax(short_headlines: list, long_headlines: list,
                  descriptions: list, exact_output: bool = False) -> dict:
    issues = []
    warnings = []

    if exact_output:
        if len(short_headlines) != PMAX_EXACT_SHORT_HEADLINE_COUNT:
            issues.append(
                f'PMax output 必須有 {PMAX_EXACT_SHORT_HEADLINE_COUNT} 個短標題，目前為 {len(short_headlines)} 個'
            )
        if len(long_headlines) != PMAX_EXACT_LONG_HEADLINE_COUNT:
            issues.append(
                f'PMax output 必須有 {PMAX_EXACT_LONG_HEADLINE_COUNT} 個長標題，目前為 {len(long_headlines)} 個'
            )
        if len(descriptions) != PMAX_EXACT_DESC_COUNT:
            issues.append(
                f'PMax output 必須有 {PMAX_EXACT_DESC_COUNT} 個說明，目前為 {len(descriptions)} 個'
            )

    for h in short_headlines:
        if google_char_len(h) > PMAX_SHORT_HEADLINE_MAX:
            issues.append(f'短標題超限：「{h}」（{google_char_len(h)} 字元）')

    for h in long_headlines:
        if google_char_len(h) > PMAX_LONG_HEADLINE_MAX:
            issues.append(f'長標題超限：「{h}」（{google_char_len(h)} 字元）')

    has_short_desc = any(google_char_len(d) <= PMAX_DESC_SHORT_MAX for d in descriptions)
    if not has_short_desc and descriptions:
        warnings.append(f'沒有 ≤ {PMAX_DESC_SHORT_MAX} 字元的說明（PMax 需要至少 1 個短說明）')

    for d in descriptions:
        if google_char_len(d) > PMAX_DESC_MAX:
            issues.append(f'說明超限：「{d[:20]}...」（{google_char_len(d)} 字元）')

    return {
        'type': 'PMax',
        'short_headlines': [{'text': h, 'length': google_char_len(h), 'status': 'ok' if google_char_len(h) <= PMAX_SHORT_HEADLINE_MAX else 'error'} for h in short_headlines],
        'long_headlines': [{'text': h, 'length': google_char_len(h), 'status': 'ok' if google_char_len(h) <= PMAX_LONG_HEADLINE_MAX else 'error'} for h in long_headlines],
        'descriptions': [{'text': d, 'length': google_char_len(d), 'status': 'ok' if google_char_len(d) <= PMAX_DESC_MAX else 'error'} for d in descriptions],
        'issues': issues,
        'warnings': warnings,
        'passed': len(issues) == 0,
    }


def _estimate_ad_strength(headline_count: int, desc_count: int,
                           diversity: float, issue_count: int) -> str:
    if issue_count > 0:
        return 'Poor（有格式問題，需先修正）'
    score = 0
    score += min(headline_count / RSA_HEADLINE_GOOD_COUNT, 1.0) * 40
    score += min(desc_count / RSA_DESC_GOOD_COUNT, 1.0) * 20
    score += diversity * 30
    score += 10  # 基礎分
    if score >= 85:
        return 'Excellent'
    elif score >= 65:
        return 'Good'
    elif score >= 45:
        return 'Average'
    else:
        return 'Poor'


# ---------------------------------------------------------------------------
# Demo 資料
# ---------------------------------------------------------------------------

DEMO_HEADLINES = [
    '大島樂眠 獨立筒床墊', '告別腰痛 從床墊開始', '量脖子找對枕頭',
    '睡眠顧問 免費諮詢', '乳膠床墊推薦首選', '台灣寢具品牌',
    '硬式床墊 護腰首選', '免費試躺 安心選購', '記憶棉床墊特價',
    '枕頭推薦 頸椎適配', '睡好覺 從選對床開始', '台北門市 預約試躺',
]

DEMO_DESCRIPTIONS = [
    '大島樂眠提供專業睡眠顧問服務，依你的脖圍、睡姿推薦最適合的枕頭與床墊，讓你一覺到天亮。',
    '獨立筒、乳膠、記憶棉多款床墊可試躺，安心計畫讓你買得放心睡得安心，現在預約享專屬服務。',
    '久坐腰背緊？我們有專為久坐族設計的護腰床墊，讓身體先被接住，再慢慢進入放鬆睡眠。',
    '台北門市歡迎預約試躺，專業睡眠顧問陪你一起找到最適合你的寢具組合。',
]


# ---------------------------------------------------------------------------
# 輸出
# ---------------------------------------------------------------------------

def format_text(result: dict) -> str:
    lines = []
    t = result.get('type', 'RSA')
    lines.append('=' * 60)
    lines.append(f'廣告文案驗證報告 — {t}')
    lines.append('=' * 60)

    status = '✅ 通過' if result.get('passed') else '❌ 有問題需修正'
    lines.append(f'\n驗證結果：{status}')

    if t == 'RSA':
        ad_strength = result.get('ad_strength_estimate', 'N/A')
        lines.append(f'Ad Strength 預估：{ad_strength}')

        lines.append(f'\n【標題】{len(result["headlines"])} 個（建議 {RSA_HEADLINE_GOOD_COUNT} 個）')
        for h in result['headlines']:
            mark = '✅' if h['status'] == 'ok' else '❌'
            lines.append(f'  {mark} [{h["length"]:>2}/{RSA_HEADLINE_MAX}] {h["text"]}')

        lines.append(f'\n【說明】{len(result["descriptions"])} 個（建議 {RSA_DESC_GOOD_COUNT} 個）')
        for d in result['descriptions']:
            mark = '✅' if d['status'] == 'ok' else '❌'
            lines.append(f'  {mark} [{d["length"]:>2}/{RSA_DESC_MAX}] {d["text"][:40]}{"..." if len(d["text"]) > 40 else ""}')

    if t == 'PMax':
        lines.append(f'\n【短標題】{len(result.get("short_headlines", []))} 個')
        for h in result.get('short_headlines', []):
            mark = '✅' if h['status'] == 'ok' else '❌'
            lines.append(f'  {mark} [{h["length"]:>2}/{PMAX_SHORT_HEADLINE_MAX}] {h["text"]}')

        lines.append(f'\n【長標題】{len(result.get("long_headlines", []))} 個')
        for h in result.get('long_headlines', []):
            mark = '✅' if h['status'] == 'ok' else '❌'
            lines.append(f'  {mark} [{h["length"]:>2}/{PMAX_LONG_HEADLINE_MAX}] {h["text"][:40]}{"..." if len(h["text"]) > 40 else ""}')

        lines.append(f'\n【說明】{len(result.get("descriptions", []))} 個')
        for d in result.get('descriptions', []):
            mark = '✅' if d['status'] == 'ok' else '❌'
            lines.append(f'  {mark} [{d["length"]:>2}/{PMAX_DESC_MAX}] {d["text"][:40]}{"..." if len(d["text"]) > 40 else ""}')

    if result.get('issues'):
        lines.append('\n【需修正的問題】')
        for issue in result['issues']:
            lines.append(f'  ❌ {issue}')

    if result.get('warnings'):
        lines.append('\n【建議改善】')
        for w in result['warnings']:
            lines.append(f'  ⚠ {w}')

    if not result.get('issues') and not result.get('warnings'):
        lines.append('\n  ✅ 格式完全符合規範')

    lines.append('\n' + '=' * 60)
    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description='Google Ads 文案格式驗證')
    parser.add_argument('--headlines', help='標題，以 | 分隔')
    parser.add_argument('--descriptions', help='說明，以 | 分隔')
    parser.add_argument('--type', choices=['rsa', 'pmax'], default='rsa')
    parser.add_argument('--file', help='JSON 格式的文案檔案')
    parser.add_argument('--exact-search-output', action='store_true',
                        help='強制檢查 Search RSA MVP 的 15 headlines / 4 descriptions 契約')
    parser.add_argument('--exact-pmax-output', action='store_true',
                        help='強制檢查 PMax 文案輸出的 15 short / 5 long / 5 descriptions 契約')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    args = parser.parse_args()
    exact_search_output = args.exact_search_output
    exact_pmax_output = args.exact_pmax_output

    if args.file:
        with open(args.file) as f:
            data = json.load(f)
        if isinstance(data, dict) and data.get('campaign_type') == 'search_rsa':
            exact_search_output = True
        if isinstance(data, dict) and data.get('campaign_type') == 'pmax':
            exact_pmax_output = True
            short_headlines = extract_texts(data.get('short_headlines', []))
            long_headlines = extract_texts(data.get('long_headlines', []))
            headlines = short_headlines + long_headlines
            descriptions = extract_texts(data.get('descriptions', []))
        elif isinstance(data, dict) and 'assets' in data:
            headlines = extract_texts(data.get('assets', {}).get('headlines', []))
            descriptions = extract_texts(data.get('assets', {}).get('descriptions', []))
            short_headlines = headlines[:5]
            long_headlines = headlines[5:]
        else:
            headlines = extract_texts(data.get('headlines', []))
            descriptions = extract_texts(data.get('descriptions', []))
            short_headlines = []
            long_headlines = []
    elif args.headlines:
        headlines = [h.strip() for h in args.headlines.split('|') if h.strip()]
        descriptions = [d.strip() for d in args.descriptions.split('|') if d.strip()] if args.descriptions else []
        short_headlines = headlines[:PMAX_EXACT_SHORT_HEADLINE_COUNT]
        long_headlines = headlines[PMAX_EXACT_SHORT_HEADLINE_COUNT:]
    else:
        print('[demo 模式] 使用內建範例\n', file=sys.stderr)
        headlines = DEMO_HEADLINES
        descriptions = DEMO_DESCRIPTIONS
        short_headlines = headlines[:PMAX_EXACT_SHORT_HEADLINE_COUNT]
        long_headlines = headlines[PMAX_EXACT_SHORT_HEADLINE_COUNT:]

    if args.type == 'pmax' or exact_pmax_output:
        if not short_headlines and not long_headlines:
            short_headlines = headlines[:PMAX_EXACT_SHORT_HEADLINE_COUNT]
            long_headlines = headlines[PMAX_EXACT_SHORT_HEADLINE_COUNT:]
        result = validate_pmax(short_headlines, long_headlines, descriptions,
                               exact_output=exact_pmax_output)
    else:
        result = validate_rsa(headlines, descriptions, exact_output=exact_search_output)

    if args.format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_text(result))


if __name__ == '__main__':
    main()
