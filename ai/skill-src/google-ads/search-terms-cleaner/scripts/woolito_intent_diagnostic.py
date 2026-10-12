#!/usr/bin/env python3
"""Read-only Woolito v0.1. Strict normalized CSV; never calls Ads APIs.
Reuse legacy header aliases only, NOT its lossy parser or cost-based decisions.
"""
import argparse
import csv
import json
import math
import re
import unicodedata
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from search_terms_analyzer import COLUMN_MAP

START, END = date(2026, 7, 14), date(2026, 10, 11)
SCHEMAS = {
    'search_terms': ('date', 'query', 'campaign_id', 'ad_group_id', 'trigger_keyword',
                     'positive_match_type', 'impressions', 'clicks', 'cost', 'conversions'),
    'positives': ('campaign_id', 'ad_group_id', 'keyword', 'match_type', 'status'),
    'negatives': ('scope', 'campaign_id', 'ad_group_id', 'list_id', 'keyword', 'match_type'),
    'campaign_totals': ('date', 'campaign_id', 'clicks', 'cost', 'conversions'),
    'historical_conversions': ('query', 'conversions'),
}
ALIASES = {k: {'term': 'query', 'match_type': 'positive_match_type'}.get(v, v)
           for k, v in COLUMN_MAP.items()}
ALIASES.update({'日期': 'date', 'Date': 'date', 'Campaign ID': 'campaign_id',
                '廣告活動 ID': 'campaign_id', 'Ad group ID': 'ad_group_id',
                '廣告群組 ID': 'ad_group_id', 'Keyword': 'trigger_keyword',
                '關鍵字': 'trigger_keyword', 'Keyword match type': 'positive_match_type'})
NUMBERS = {'impressions', 'clicks', 'cost', 'conversions', 'conversion_value'}
# Full-query patterns and complete service phrases, not single-word negatives.
PROTECTED = ('動畫製作公司', '商業動畫報價', '企業形象動畫', '產品介紹動畫',
             '品牌動畫製作', '商業動畫製作報價', '企業教育訓練動畫', '企業訓練動畫',
             '教育訓練動畫製作', '互動賀卡製作', '企業節慶動畫', '商業角色設計',
             '動畫製作免費估價')
NONCOMMERCIAL = {
    'ENTERTAINMENT': r'(?:鬼滅之刃動畫|動漫線上看|動畫線上看)',
    'DOWNLOAD': r'動畫免費下載',
    'RECRUITMENT': r'動畫工作招聘',
    'STUDENT_ASSIGNMENT': r'動畫學生作業',
}


def norm(value):
    """Comparison normalization only; retain raw query for exact proposal.

    Spaces between Han characters are joined for context recognition. Do not
    remove spaces between Latin words or emulate Google's matching engine.
    """
    value = unicodedata.normalize('NFKC', value).casefold().strip()
    value = re.sub(r'\s+', ' ', value)
    return re.sub(r'(?<=[\u3400-\u9fff]) +(?=[\u3400-\u9fff])', '', value)


def number(value):
    if value is None or not value.strip() or value.strip() in ('--', '-'):
        raise ValueError('missing metric (never coerced to zero)')
    value = value.replace('NT$', '').replace('$', '').replace(',', '').strip()
    result = float(value)
    if not math.isfinite(result) or result < 0:
        raise ValueError('metric must be finite and nonnegative')
    return result


def load_csv(path, kind):
    # Contract is one header, no report preamble/totals; explicit normalization.
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        canonical = [ALIASES.get(h.strip(), h.strip()) if kind == 'search_terms'
                     else h.strip() for h in headers]
        if len(set(canonical)) != len(canonical):
            raise ValueError(f'{kind}: duplicate/aliased headers')
        if not set(SCHEMAS[kind]) <= set(canonical):
            raise ValueError(f'{kind}: missing required columns')
        records = []
        for line, raw in enumerate(reader, 2):
            if None in raw or any(v is None for v in raw.values()):
                raise ValueError(f'{kind}:{line}: ragged row')
            row = {c: raw[h].strip() for h, c in zip(headers, canonical)}
            if any(not row[k] for k in SCHEMAS[kind]
                   if k not in ('campaign_id', 'ad_group_id', 'list_id')):
                raise ValueError(f'{kind}:{line}: blank required field')
            for key in NUMBERS & row.keys():
                row[key] = number(row[key])
            if 'date' in row and not START <= date.fromisoformat(row['date']) <= END:
                raise ValueError(f'{kind}:{line}: date outside 90-day window')
            if kind in ('search_terms', 'positives', 'campaign_totals'):
                if not row['campaign_id'] or (kind != 'campaign_totals' and not row['ad_group_id']):
                    raise ValueError(f'{kind}:{line}: missing IDs')
            match = row.get('positive_match_type', row.get('match_type'))
            if match and match not in ('EXACT', 'PHRASE', 'BROAD'):
                raise ValueError(f'{kind}:{line}: unsupported match type')
            if kind == 'positives' and row['status'] != 'ENABLED':
                raise ValueError('positives must be filtered to ENABLED')
            if kind == 'negatives':
                scope = row['scope']
                if scope not in ('ACCOUNT', 'SHARED', 'CAMPAIGN', 'AD_GROUP'):
                    raise ValueError('invalid negative scope')
                if scope != 'ACCOUNT' and not row['campaign_id']:
                    raise ValueError('negative requires campaign/list binding')
                if scope == 'AD_GROUP' and not row['ad_group_id']:
                    raise ValueError('negative requires ad group')
                if scope == 'SHARED' and not row['list_id']:
                    raise ValueError('shared negative requires list_id')
            records.append(row)
        return records


def applies(row, term):
    return (row.get('scope') == 'ACCOUNT' or
            (row['campaign_id'] == term['campaign_id'] and
             (row.get('scope') != 'AD_GROUP' or row['ad_group_id'] == term['ad_group_id'])))


def classify(row, tables, manifest):
    q = norm(row['query'])
    protected = PROTECTED + tuple(manifest.get('protected_phrases', []))
    decision, reason = 'REVIEW', 'AMBIGUOUS_CONTEXT'
    if any(norm(p) in q for p in protected if p.strip()):
        decision, reason = 'KEEP_B2B', 'PROTECTED_SERVICE_CONTEXT'
    else:
        for category, pattern in NONCOMMERCIAL.items():
            if re.fullmatch(pattern, q):
                decision, reason = 'NEGATIVE_EXACT_CANDIDATE', category
                break
    conflicts = []
    history = tables.get('historical_conversions')
    if row['conversions'] > 0 or any(h['conversions'] > 0 and norm(h['query']) == q
                                     for h in (history or [])):
        conflicts.append('HISTORICAL_CONVERSION')
    for p in tables.get('positives') or []:
        if p['campaign_id'] == row['campaign_id'] and p['ad_group_id'] == row['ad_group_id']:
            if norm(p['keyword']) == q:
                conflicts.append('ENABLED_POSITIVE_TEXT_CONFLICT')
    for n in tables.get('negatives') or []:
        if applies(n, row):
            if norm(n['keyword']) == q and n['match_type'] == 'EXACT':
                conflicts.append('ALREADY_NEGATIVE_EXACT')
            elif n['match_type'] != 'EXACT':
                conflicts.append('EXISTING_NEGATIVE_SEMANTICS_UNCONFIRMED')
    required = ('search_terms', 'positives', 'negatives', 'historical_conversions')
    missing = [k for k in required if tables.get(k) is None or
               manifest.get('complete', {}).get(k) is not True]
    if missing:
        conflicts.append('DATA_INCOMPLETE:' + ','.join(missing))
    if decision == 'NEGATIVE_EXACT_CANDIDATE' and conflicts:
        decision, reason = 'REVIEW', conflicts[0]
    # Positive expansion is deliberately not simulated; clean text check is
    # still only a bounded conflict check, never an approval to exclude.
    return {**row, 'decision': decision, 'reason_code': reason,
            'confidence': 'RULE_BOUND_ONLY', 'evidence': f'v0.1 full-context rule: {reason}',
            'proposed_negative_match': 'EXACT' if decision == 'NEGATIVE_EXACT_CANDIDATE' else '',
            'proposed_negative': row['query'] if decision == 'NEGATIVE_EXACT_CANDIDATE' else '',
            'proposed_level': 'AD_GROUP',
            'conflict_check': ';'.join(conflicts) or 'TEXT_CHECK_CLEAR_SEMANTICS_UNCONFIRMED',
            'review_status': 'MANUAL_REVIEW_REQUIRED'}


def diagnose(tables, manifest):
    if manifest.get('start') != START.isoformat() or manifest.get('end') != END.isoformat():
        raise ValueError('manifest window mismatch')
    if manifest.get('source_kind') not in ('synthetic', 'account'):
        raise ValueError('source_kind must be synthetic or account')
    for key in ('currency', 'account_timezone', 'exported_at', 'conversion_lag_days'):
        if key not in manifest:
            raise ValueError(f'missing manifest {key}')
    lag = manifest['conversion_lag_days']
    if not isinstance(lag, int) or isinstance(lag, bool) or lag < 0:
        raise ValueError('conversion_lag_days must be a nonnegative integer')
    rows = tables.get('search_terms')
    if not rows:
        raise ValueError('search terms empty/missing')
    keys = [(r['date'], r['campaign_id'], r['ad_group_id'], r['query'],
             r['trigger_keyword'], r['positive_match_type']) for r in rows]
    if len(keys) != len(set(keys)):
        raise ValueError('duplicate search grain: do not concatenate overlapping exports')
    # Cross-row history: a converting visible query elsewhere also protects it.
    checks = dict(tables)
    if tables.get('historical_conversions') is not None:
        checks['historical_conversions'] = tables['historical_conversions'] + [r for r in rows if r['conversions'] > 0]
    classified = [classify(r, checks, manifest) for r in rows]
    totals = tables.get('campaign_totals')
    visible = defaultdict(lambda: dict(cost=0., clicks=0., conversions=0.))
    for r in rows:
        for metric in ('cost', 'clicks', 'conversions'):
            visible[r['date'], r['campaign_id']][metric] += r[metric]
    coverage, coverage_status = [], 'UNCONFIRMED'
    if totals is not None:
        keyed = {(r['date'], r['campaign_id']): r for r in totals}
        if len(keyed) != len(totals):
            raise ValueError('duplicate campaign/date total')
        campaigns = set(manifest.get('campaign_ids', []))
        expected = {( (START + timedelta(days=d)).isoformat(), c)
                    for d in range(90) for c in campaigns}
        complete = bool(expected) and set(keyed) == expected and set(visible) <= expected
        if not set(visible) <= set(keyed):
            raise ValueError('visible rows missing corresponding totals')
        for key, values in visible.items():
            if any(values[m] > keyed[key][m] + 1e-6 for m in ('cost', 'clicks', 'conversions')):
                raise ValueError('visible metrics exceed campaign totals: grain/filter mismatch')
        coverage_status = 'CONFIRMED' if complete and manifest.get('complete', {}).get('campaign_totals') is True else 'PARTIAL'
        for campaign in sorted({r['campaign_id'] for r in totals}):
            total = {m: sum(r[m] for r in totals if r['campaign_id'] == campaign)
                     for m in ('cost', 'clicks', 'conversions')}
            vis = {m: sum(r[m] for r in rows if r['campaign_id'] == campaign) for m in total}
            coverage.append({'campaign_id': campaign, 'visible': vis, 'campaign_total': total,
                             'cost_coverage': vis['cost'] / total['cost'] if total['cost'] else None,
                             'click_coverage': vis['clicks'] / total['clicks'] if total['clicks'] else None})
    groups = defaultdict(lambda: dict(cost=0., clicks=0., conversions=0., rows=0))
    for r in classified:
        key = (r['campaign_id'], r['trigger_keyword'], r['positive_match_type'], r['decision'], r['reason_code'])
        for m in ('cost', 'clicks', 'conversions'):
            groups[key][m] += r[m]
        groups[key]['rows'] += 1
    missing = [k for k in SCHEMAS if tables.get(k) is None or manifest.get('complete', {}).get(k) is not True]
    synthetic = manifest['source_kind'] == 'synthetic'
    return {'source_kind': manifest['source_kind'], 'window': [START.isoformat(), END.isoformat()],
            'account_conclusion': 'BLOCKED_ON_ACCOUNT_DATA' if synthetic or missing or coverage_status != 'CONFIRMED' else 'MANUAL_DIAGNOSIS_REQUIRED',
            'product_decision': None, 'live_write_go': 'NO_GO', 'data_gaps': missing,
            'coverage_status': coverage_status, 'coverage': coverage,
            'limitations': ['Synthetic metrics are not Woolito spend.' if synthetic else 'Visible search terms only.',
                            'Hidden queries cannot be classified or extrapolated.',
                            'Positive close variants/intent expansion and Chinese negative tokenization are not simulated.',
                            'Zero conversion does not imply wasted cost; candidate spend is not recoverable savings.',
                            f'Last {lag} days in window may have conversion lag; rerun after maturity.'],
            'top_visible_sources': sorted([{'campaign_id': k[0], 'trigger_keyword': k[1],
                  'positive_match_type': k[2], 'decision': k[3], 'reason_code': k[4], **v}
                 for k, v in groups.items()], key=lambda r: r['cost'], reverse=True),
            'rows': sorted(classified, key=lambda r: r['cost'], reverse=True)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input_dir', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True, help='private local directory for account data')
    args = parser.parse_args()
    try:
        manifest = json.loads((args.input_dir / 'manifest.json').read_text(encoding='utf-8'))
        tables = {k: load_csv(args.input_dir / f'{k}.csv', k)
                  if (args.input_dir / f'{k}.csv').exists() else None for k in SCHEMAS}
        result = diagnose(tables, manifest)
    except (ValueError, OSError, KeyError) as error:
        parser.exit(2, f'Input rejected: {error}\n')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / 'diagnostic.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    fields = ['query', 'date', 'campaign_id', 'ad_group_id', 'trigger_keyword', 'positive_match_type',
              'cost', 'conversions', 'decision', 'reason_code', 'confidence', 'evidence',
              'proposed_negative_match', 'proposed_negative', 'proposed_level', 'conflict_check', 'review_status']
    with (args.output_dir / 'candidates.csv').open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(result['rows'])
    print(json.dumps({k: result[k] for k in ('source_kind', 'account_conclusion', 'coverage_status', 'live_write_go')}, ensure_ascii=False))


if __name__ == '__main__':
    main()
