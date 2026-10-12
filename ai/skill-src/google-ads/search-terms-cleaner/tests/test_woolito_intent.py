import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import woolito_intent_diagnostic as d


class IntentTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / 'assets/woolito-synthetic/manifest.json').read_text())
        self.tables = {k: d.load_csv(ROOT / f'assets/woolito-synthetic/{k}.csv', k) for k in d.SCHEMAS}

    def classify(self, query, **updates):
        row = dict(self.tables['search_terms'][0], query=query, **updates)
        return d.classify(row, self.tables, self.manifest)

    def test_required_keep_and_review(self):
        for q in ['動畫製作公司','商業動畫報價','產品介紹動畫','品牌動畫製作',
                  '企業教育訓練動畫','互動賀卡製作','教育訓練動畫製作','商業角色設計',
                  '動畫製作免費估價','企業形象動畫','企業節慶動畫','產品 介紹 動畫']:
            with self.subTest(q=q):
                self.assertEqual(self.classify(q)['decision'], 'KEEP_B2B')
        for q in ['動畫角色設計','動畫教學','3D 動畫','新動畫片名','免費動畫製作報價','動畫']:
            with self.subTest(q=q):
                self.assertEqual(self.classify(q, cost=99999)['decision'], 'REVIEW')

    def test_exact_candidates_only(self):
        for q in ['鬼滅之刃動畫','動漫線上看','動畫免費下載','動畫工作招聘']:
            r = self.classify(q)
            self.assertEqual(r['decision'], 'NEGATIVE_EXACT_CANDIDATE')
            self.assertEqual(r['proposed_negative'], q)
            self.assertEqual(r['proposed_negative_match'], 'EXACT')
            self.assertEqual(r['review_status'], 'MANUAL_REVIEW_REQUIRED')
        for q in ['免費','教學','設計','動畫','鬼滅之刃動畫製作報價','動畫工作招聘商業角色設計']:
            self.assertNotEqual(self.classify(q)['decision'], 'NEGATIVE_EXACT_CANDIDATE')

    def test_historical_and_positive_conflicts(self):
        q = '動畫免費下載'
        self.tables['historical_conversions'].append(dict(query=q, conversions=1))
        self.assertEqual(self.classify(q)['decision'], 'REVIEW')
        self.tables['historical_conversions'] = []
        self.assertEqual(self.classify(q, conversions=0.5)['decision'], 'REVIEW')
        self.tables['positives'][0]['keyword'] = q
        self.assertEqual(self.classify(q)['decision'], 'REVIEW')

    def test_cross_row_conversion_protection(self):
        q = '動漫線上看'
        self.tables['search_terms'].append(dict(self.tables['search_terms'][7],
            date='2026-08-02', campaign_id='synthetic-c2', conversions=1))
        self.tables['campaign_totals'] = None
        result = d.diagnose(self.tables, self.manifest)
        matches = [r for r in result['rows'] if r['query'] == q]
        self.assertTrue(all(r['decision'] == 'REVIEW' for r in matches))

    def test_missing_checks_fail_closed(self):
        for kind in ['search_terms','positives','negatives','historical_conversions']:
            with self.subTest(kind=kind):
                manifest = copy.deepcopy(self.manifest)
                manifest['complete'][kind] = False
                r = d.classify(dict(self.tables['search_terms'][0], query='動漫線上看'), self.tables, manifest)
                self.assertEqual(r['decision'], 'REVIEW')
                self.assertIn('DATA_INCOMPLETE', r['conflict_check'])
        self.tables['positives'] = None
        self.assertEqual(self.classify('動漫線上看')['decision'], 'REVIEW')

    def test_negative_scopes_and_unconfirmed_semantics(self):
        n = dict(scope='SHARED',campaign_id='synthetic-c1',ad_group_id='',list_id='synthetic-list',keyword='動漫線上看',match_type='EXACT')
        self.tables['negatives'] = [n]
        self.assertEqual(self.classify('動漫線上看')['reason_code'], 'ALREADY_NEGATIVE_EXACT')
        n['campaign_id'] = 'another'
        self.assertEqual(self.classify('動漫線上看')['decision'], 'NEGATIVE_EXACT_CANDIDATE')
        n.update(scope='ACCOUNT',match_type='PHRASE')
        self.assertEqual(self.classify('動漫線上看')['decision'], 'REVIEW')

    def test_coverage_and_synthetic_block(self):
        r = d.diagnose(self.tables, self.manifest)
        self.assertEqual(r['account_conclusion'], 'BLOCKED_ON_ACCOUNT_DATA')
        self.assertIsNone(r['product_decision'])
        self.assertEqual(r['coverage_status'], 'CONFIRMED')
        self.assertAlmostEqual(r['coverage'][0]['cost_coverage'], 2310/4000)
        self.assertAlmostEqual(r['coverage'][0]['click_coverage'], 105/200)
        self.tables['campaign_totals'].pop()
        self.assertEqual(d.diagnose(self.tables, self.manifest)['coverage_status'], 'PARTIAL')
        self.tables['campaign_totals'] = None
        self.assertEqual(d.diagnose(self.tables, self.manifest)['coverage'], [])

    def test_reject_grain_and_window_errors(self):
        self.tables['campaign_totals'].append(self.tables['campaign_totals'][0])
        with self.assertRaises(ValueError): d.diagnose(self.tables, self.manifest)
        self.setUp()
        self.tables['search_terms'].append(self.tables['search_terms'][0])
        with self.assertRaises(ValueError): d.diagnose(self.tables, self.manifest)
        self.setUp()
        self.tables['campaign_totals'][18]['cost'] = 0
        with self.assertRaises(ValueError): d.diagnose(self.tables, self.manifest)
        self.setUp()
        self.manifest['end'] = '2026-10-12'
        with self.assertRaises(ValueError): d.diagnose(self.tables, self.manifest)

    def test_strict_csv_and_numbers(self):
        for value in ['--','','NaN','inf','-1','garbage']:
            with self.assertRaises(ValueError): d.number(value)
        self.assertEqual(d.number('NT$1,234.50'), 1234.5)
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory)/'input.csv'
            p.write_text('query,cost\n動畫,100\n')
            with self.assertRaises(ValueError): d.load_csv(p, 'search_terms')
            raw = (ROOT/'assets/woolito-synthetic/search_terms.csv').read_text()
            p.write_text(raw.replace('2026-08-01','2026-10-12'))
            with self.assertRaises(ValueError): d.load_csv(p, 'search_terms')
            p.write_text(raw.replace(',100,0,0',',--,0,0',1))
            with self.assertRaises(ValueError): d.load_csv(p, 'search_terms')


if __name__ == '__main__': unittest.main()
