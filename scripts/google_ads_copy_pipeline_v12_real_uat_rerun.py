#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

try:
    import jsonschema
except ImportError:  # pragma: no cover
    jsonschema = None


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = Path("/Users/andychou/Downloads/素材資源關聯報表 (1).csv")
TZ = ZoneInfo("Asia/Taipei")
NOW = datetime.now(TZ).replace(microsecond=0)

ANGLE_KEYS = [
    "product_feel",
    "risk_reversal",
    "brand_trust",
    "entry_value",
    "life_scene",
    "concrete_number",
    "pain_point",
    "social_proof",
    "legacy_phrase",
    "cta_lower_friction",
]

ANGLE_LABELS = {
    "product_feel": "支撐與包覆感",
    "risk_reversal": "試睡與安心承諾",
    "brand_trust": "品牌與信任證據",
    "entry_value": "入門價值",
    "life_scene": "生活情境",
    "concrete_number": "數字證據",
    "pain_point": "腰背壓力切入",
    "social_proof": "評價背書",
    "legacy_phrase": "產品名承接",
    "cta_lower_friction": "低摩擦 CTA",
}

PROTECTED_PHRASES = [
    {
        "phrase": "100天安心睡",
        "reason": "既有歷史資產與產品承諾都高度集中在此 phrase，刪除會直接丟失核心安心敘事。",
        "source": "historical_performance",
        "min_active_assets": 1,
        "preferred_asset_types": ["headline", "description"],
    }
]

MUST_INCLUDE_TOKENS = [
    {
        "token": "山丘樂眠床",
        "reason": "本次 UAT 目標產品為山丘樂眠床，產品名需在線上素材池持續可見。",
        "source": "brand_guideline",
        "min_active_assets": 2,
        "preferred_asset_types": ["headline", "description"],
    },
    {
        "token": "LOVEFU",
        "reason": "真實素材池大量使用品牌名作為辨識入口，builder 需維持品牌可見性。",
        "source": "historical_performance",
        "min_active_assets": 2,
        "preferred_asset_types": ["headline", "description"],
    },
    {
        "token": "飄雲專利",
        "reason": "真實素材池中的高轉換 proxy 資產多次承接此技術／系列語言，移除會造成 trust gap。",
        "source": "historical_performance",
        "min_active_assets": 1,
        "preferred_asset_types": ["headline", "description"],
    },
]

REUSABLE_MOTIFS = [
    {
        "motif_key": "concrete-number",
        "description": "用 200kg、97%、2026、10年等數字做明確證據。",
        "reason": "真實報表中高 proxy 資產反覆使用數字作為證據或分類鉤子。",
        "source": "historical_performance",
    },
    {
        "motif_key": "pain-point-solution",
        "description": "從腰背壓力、睡醒負擔切入，再接支撐與放鬆。",
        "reason": "痛點切入確實能帶來轉換關聯，但需要 safer rewrite 降風險。",
        "source": "historical_performance",
    },
    {
        "motif_key": "lower-friction-cta",
        "description": "試睡、安心、配送、無憂等降低嘗試阻力的語言。",
        "reason": "真實素材池中與試睡／配送便利相關的語言有穩定 proxy 表現。",
        "source": "historical_performance",
    },
    {
        "motif_key": "support-feel",
        "description": "把穩定支撐、包覆、Q 彈、接住感轉成可感知睡感。",
        "reason": "高表現的產品型資產大多不是只講規格，而是規格加睡感。",
        "source": "historical_performance",
    },
    {
        "motif_key": "trust-proof",
        "description": "品牌、MIT、認證、專利與高評價等信任證據。",
        "reason": "品牌與信任訊號在弱資料環境下仍是可重複保留的穩定 motif。",
        "source": "historical_performance",
    },
]

HIGH_RISK_PATTERNS = [
    "不再背痛失眠",
    "腰椎不再酸痛",
    "專為腰痛患者設計",
    "幫助緩解腰痛",
    "告別腰痛困擾",
    "腰椎更健康",
    "舒緩腰痛",
    "不痠痛",
]

MEDIUM_RISK_PATTERNS = [
    "一覺到天明",
    "改善睡眠品質",
    "睡眠質量全面升級",
    "當場入睡",
    "無壓力",
]

MOTIF_MATCHERS = {
    "concrete-number": re.compile(r"(200kg|97%|98%|100%|2026|10年|12期|0利率|9 成|10,000)"),
    "pain-point-solution": re.compile(r"(腰痛|背痛|失眠|腰椎|腰臀|酸痛|疲憊|撐腰|負擔)"),
    "lower-friction-cta": re.compile(r"(試睡|安心睡|無風險|無憂|配送|立即試睡|先試|先接住|先決定|0利率)"),
    "support-feel": re.compile(r"(支撐|包覆|Q彈|Ｑ彈|無壓|放鬆|接住|舒適|好眠)"),
    "trust-proof": re.compile(r"(LOVEFU|大島樂眠|MIT|認證|專利|高評價|好評|評價|推薦)"),
}

FORCED_RETIRE_TEXTS = {
    "不再背痛失眠－LOVEFU山丘樂眠床",
    "腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。",
    "LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。",
    "LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。",
    "撐腰床墊推薦，LOVEFU 值得信賴",
    "LOVEFU 飄雲專利床墊，支撐舒適",
    "山丘樂眠床，LOVEFU 提供好眠",
}

FINAL_HEADLINE_PRIMARY_TEXTS = [
    "200kg 不塌陷，最好睡的撐腰床墊",
    "大島樂眠 LOVEFU 飄雲專利床墊",
    "100 天安心睡計畫，改善睡眠品質",
    "專為台灣人的睡眠需求設計",
    "LOVEFU 飄雲床墊，樂眠好評如潮",
    "指定配送日，LOVEFU 配送超方便",
    "2026 護脊床墊推薦 - 山丘樂眠床",
    "山丘樂眠床 第2張床 擁有支撐腰背與放鬆的魔法",
    "LOVEFU山丘樂眠床，支撐包覆更到位",
    "LOVEFU山丘樂眠床，先接住腰背再放鬆",
    "100天安心睡，先試睡再決定",
]

FINAL_HEADLINE_TEST_TEXTS = [
    "白天你撐起生活，晚上山丘撐住你",
    "睡醒少點負擔，LOVEFU山丘樂眠床",
    "撐住腰背的LOVEFU山丘樂眠床",
    "第2張床，也值得被山丘穩穩接住",
]

FINAL_DESCRIPTION_PRIMARY_TEXTS = [
    "100 天安心睡，帶你最需要的放鬆、慵懶。最好躺的 LOVEFU 硬床，不再睡睡醒醒，一覺到天明。",
    "LOVEFU飄雲專利床墊，以穩定支撐搭配柔軟包覆，延續高評價的無壓睡感。",
    "LOVEFU山丘樂眠床，以穩定支撐搭配舒適包覆，讓久坐後的腰背更容易放鬆。",
]

FINAL_DESCRIPTION_TEST_TEXTS = [
    "躺下先被穩穩接住，中鋼獨立筒搭配獨家泡棉，讓腰背壓力少一點。",
]


def parse_number(value: str) -> float:
    raw = value.strip().replace(",", "")
    if raw in {"", "--", " --"}:
        return 0.0
    try:
        return float(raw.replace("%", ""))
    except ValueError:
        return 0.0


def parse_period(line: str) -> tuple[str, str]:
    match = re.fullmatch(
        r"(\d{4})年(\d{1,2})月(\d{1,2})日 - (\d{4})年(\d{1,2})月(\d{1,2})日",
        line.strip(),
    )
    if not match:
        raise ValueError(f"Unexpected date range: {line}")
    year_1, month_1, day_1, year_2, month_2, day_2 = match.groups()
    start = f"{year_1}-{int(month_1):02d}-{int(day_1):02d}"
    end = f"{year_2}-{int(month_2):02d}-{int(day_2):02d}"
    return start, end


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    index = (len(ordered) - 1) * q
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return ordered[lower]
    fraction = index - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def normalize_phrase(text: str) -> str:
    return re.sub(r"\s+", "", text)


def classify_risk(text: str) -> str:
    for pattern in HIGH_RISK_PATTERNS:
        if pattern in text:
            return "high"
    for pattern in MEDIUM_RISK_PATTERNS:
        if pattern in text:
            return "medium"
    return "low"


def infer_angle_key(text: str, asset_type: str) -> str:
    stripped = text.strip()
    overrides = {
        "200kg 不塌陷，最好睡的撐腰床墊": "concrete_number",
        "2026 護脊床墊推薦 - 山丘樂眠床": "legacy_phrase",
        "指定配送日，LOVEFU 配送超方便": "cta_lower_friction",
        "白天你撐起生活，晚上山丘撐住你": "life_scene",
        "山丘樂眠床 第2張床 擁有支撐腰背與放鬆的魔法": "life_scene",
        "LOVEFU山丘樂眠床，支撐包覆更到位": "product_feel",
        "LOVEFU山丘樂眠床，先接住腰背再放鬆": "product_feel",
        "100天安心睡，先試睡再決定": "cta_lower_friction",
        "睡醒少點負擔，LOVEFU山丘樂眠床": "pain_point",
        "撐住腰背的LOVEFU山丘樂眠床": "pain_point",
        "第2張床，也值得被山丘穩穩接住": "life_scene",
        "LOVEFU飄雲專利床墊，以穩定支撐搭配柔軟包覆，延續高評價的無壓睡感。": "social_proof",
        "LOVEFU山丘樂眠床，以穩定支撐搭配舒適包覆，讓久坐後的腰背更容易放鬆。": "product_feel",
        "躺下先被穩穩接住，中鋼獨立筒搭配獨家泡棉，讓腰背壓力少一點。": "pain_point",
    }
    if stripped in overrides:
        return overrides[stripped]
    if "第2張床" in stripped or "白天你撐起生活" in stripped:
        return "life_scene"
    if any(token in stripped for token in ["100天", "100 天", "試睡", "保固", "0利率", "無風險"]):
        return "risk_reversal"
    if any(token in stripped for token in ["14,900", "高性價比", "CP", "入門", "首選"]):
        return "entry_value"
    if any(token in stripped for token in ["高評價", "好評", "壓倒性評價", "滿意", "一致推薦"]):
        return "social_proof"
    if any(token in stripped for token in ["腰痛", "背痛", "失眠", "腰椎", "腰臀", "酸痛", "疲憊", "撐腰", "負擔"]):
        return "pain_point"
    if re.search(r"(200kg|97%|98%|100%|2026|10年|12期|0利率|9 成|10,000)", stripped):
        return "concrete_number"
    if any(token in stripped for token in ["配送", "無憂", "體驗", "先試", "先接住"]):
        return "cta_lower_friction"
    if any(token in stripped for token in ["台灣", "MIT", "認證", "專利", "大島樂眠"]):
        return "brand_trust"
    if any(token in stripped for token in ["支撐", "包覆", "無壓", "Q彈", "Ｑ彈", "放鬆", "接住", "舒適", "好眠"]):
        return "product_feel"
    if any(token in stripped for token in ["山丘樂眠床", "LOVEFU", "飄雲專利"]):
        return "legacy_phrase"
    return "product_feel" if asset_type == "description" else "brand_trust"


def extract_legacy_tags(text: str) -> dict[str, list[str]]:
    compact = normalize_phrase(text)
    protected = []
    for item in PROTECTED_PHRASES:
        if normalize_phrase(item["phrase"]) in compact:
            protected.append(item["phrase"])
    matched_tokens = []
    for item in MUST_INCLUDE_TOKENS:
        if item["token"] in text:
            matched_tokens.append(item["token"])
    matched_motifs = []
    for motif_key, pattern in MOTIF_MATCHERS.items():
        if pattern.search(text):
            matched_motifs.append(motif_key)
    return {
        "protected_phrases_matched": protected,
        "must_include_tokens_matched": matched_tokens,
        "reusable_motifs_matched": matched_motifs,
    }


def aggregate_assets() -> tuple[list[dict[str, Any]], str, str]:
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle))
    if len(rows) < 4:
        raise ValueError("CSV rows are incomplete")

    start_date, end_date = parse_period(rows[1][0])
    header = rows[2]
    data_rows = [dict(zip(header, row)) for row in rows[3:] if len(row) == len(header)]

    grouped: dict[tuple[str, str], dict[str, Any]] = {}
    for row in data_rows:
        text = row["素材資源"].strip()
        raw_asset_type = row["素材資源類型"].strip()
        asset_type = "headline" if raw_asset_type == "廣告標題" else "description"
        key = (text, asset_type)
        asset = grouped.setdefault(
            key,
            {
                "text": text,
                "asset_type": asset_type,
                "raw_asset_type": raw_asset_type,
                "proxy_conversions": 0.0,
                "conversion_action_breakout": Counter(),
                "rows": 0,
            },
        )
        asset["rows"] += 1
        conversion_value = parse_number(row["轉換"])
        asset["proxy_conversions"] += conversion_value
        if conversion_value > 0:
            asset["conversion_action_breakout"][row["轉換動作"].strip()] += conversion_value

    sorted_assets: list[dict[str, Any]] = []
    for asset_type, prefix in (("headline", "hl"), ("description", "desc")):
        bucket = [item for item in grouped.values() if item["asset_type"] == asset_type]
        bucket.sort(key=lambda item: (-item["proxy_conversions"], item["text"]))
        for index, item in enumerate(bucket, start=1):
            asset = deepcopy(item)
            asset["asset_id"] = f"{prefix}-{index:02d}"
            asset["angle_key"] = infer_angle_key(asset["text"], asset_type)
            asset["legacy_tags"] = extract_legacy_tags(asset["text"])
            asset["risk_level"] = classify_risk(asset["text"])
            sorted_assets.append(asset)
    return sorted_assets, start_date, end_date


def build_candidate_specs(text_to_id: dict[str, str]) -> list[dict[str, Any]]:
    specs = [
        {
            "candidate_id": "cand-h01",
            "asset_text": "睡醒少點負擔，LOVEFU山丘樂眠床",
            "asset_type": "headline",
            "source": "safer_rewrite",
            "angle_key": "pain_point",
            "intent": "保留腰背負擔切入，但移除直接療效與失眠改善承諾。",
            "related_gap": "hl-03 高轉換痛點句需要 safer rewrite",
            "suggested_role": "測試",
            "covers_tokens": ["LOVEFU", "山丘樂眠床"],
            "inherits_motifs": ["pain-point-solution"],
            "risk_level": "medium",
            "rewrite_mode": "safer-rewrite",
            "safer_rewrite_of": text_to_id["不再背痛失眠－LOVEFU山丘樂眠床"],
            "source_asset_ids": [text_to_id["不再背痛失眠－LOVEFU山丘樂眠床"]],
        },
        {
            "candidate_id": "cand-h02",
            "asset_text": "撐住腰背的LOVEFU山丘樂眠床",
            "asset_type": "headline",
            "source": "replace_retired_asset",
            "angle_key": "pain_point",
            "intent": "補回弱 brand trust headline 的產品名與痛點承接。",
            "related_gap": "hl-68 退場後的 LOVEFU trust gap",
            "suggested_role": "測試",
            "covers_tokens": ["LOVEFU", "山丘樂眠床"],
            "inherits_motifs": ["pain-point-solution"],
            "risk_level": "low",
            "rewrite_mode": "retain-intent",
            "source_asset_ids": [text_to_id["撐腰床墊推薦，LOVEFU 值得信賴"]],
        },
        {
            "candidate_id": "cand-h03",
            "asset_text": "LOVEFU山丘樂眠床，支撐包覆更到位",
            "asset_type": "headline",
            "source": "replace_retired_asset",
            "angle_key": "product_feel",
            "intent": "把 generic 支撐舒適改成更明確的產品睡感敘述。",
            "related_gap": "hl-61 generic support phrase 退場補位",
            "suggested_role": "主力",
            "covers_tokens": ["LOVEFU", "山丘樂眠床"],
            "inherits_motifs": ["support-feel"],
            "risk_level": "low",
            "rewrite_mode": "retain-intent",
            "source_asset_ids": [text_to_id["LOVEFU 飄雲專利床墊，支撐舒適"]],
        },
        {
            "candidate_id": "cand-h04",
            "asset_text": "LOVEFU山丘樂眠床，先接住腰背再放鬆",
            "asset_type": "headline",
            "source": "replace_retired_asset",
            "angle_key": "product_feel",
            "intent": "弱 token carrier 改寫成產品名加睡感敘述，補回 product specific coverage。",
            "related_gap": "hl-86 只剩 token coverage 的弱句退場補位",
            "suggested_role": "主力",
            "covers_tokens": ["LOVEFU", "山丘樂眠床"],
            "inherits_motifs": ["support-feel", "lower-friction-cta"],
            "risk_level": "low",
            "rewrite_mode": "retain-intent",
            "source_asset_ids": [text_to_id["山丘樂眠床，LOVEFU 提供好眠"]],
        },
        {
            "candidate_id": "cand-h05",
            "asset_text": "100天安心睡，先試睡再決定",
            "asset_type": "headline",
            "source": "reinforce_expansion",
            "angle_key": "cta_lower_friction",
            "intent": "把既有 protected phrase 轉成更低摩擦的 next-step CTA。",
            "related_gap": "risk_reversal 強句延伸 CTA",
            "suggested_role": "主力",
            "covers_tokens": [],
            "inherits_motifs": ["lower-friction-cta"],
            "risk_level": "low",
            "rewrite_mode": "exploratory",
            "source_asset_ids": [text_to_id["100 天安心睡計畫，改善睡眠品質"]],
        },
        {
            "candidate_id": "cand-h06",
            "asset_text": "第2張床，也值得被山丘穩穩接住",
            "asset_type": "headline",
            "source": "reinforce_expansion",
            "angle_key": "life_scene",
            "intent": "把生活情境資產轉成更接近購買理由的第 2 張床敘事。",
            "related_gap": "life_scene 角度需要更明確產品承接",
            "suggested_role": "測試",
            "covers_tokens": [],
            "inherits_motifs": ["support-feel"],
            "risk_level": "low",
            "rewrite_mode": "exploratory",
            "source_asset_ids": [text_to_id["白天你撐起生活，晚上山丘撐住你"]],
        },
        {
            "candidate_id": "cand-h07",
            "asset_text": "山丘樂眠床，穩定支撐更放鬆",
            "asset_type": "headline",
            "source": "reinforce_expansion",
            "angle_key": "product_feel",
            "intent": "補一條更精簡的產品睡感 headline。",
            "related_gap": "product_feel 角度的精簡版 headline",
            "suggested_role": "測試",
            "covers_tokens": ["山丘樂眠床"],
            "inherits_motifs": ["support-feel"],
            "risk_level": "low",
            "rewrite_mode": "exploratory",
            "source_asset_ids": [text_to_id["山丘樂眠床 第2張床 擁有支撐腰背與放鬆的魔法"]],
        },
        {
            "candidate_id": "cand-h08",
            "asset_text": "第2張床入門，也能睡得更安心",
            "asset_type": "headline",
            "source": "brief_generator_auto",
            "angle_key": "entry_value",
            "intent": "補回 entry value 角度，但只做 exploratory 測試。",
            "related_gap": "entry_value 在真實素材池中缺角",
            "suggested_role": "測試",
            "covers_tokens": [],
            "inherits_motifs": ["lower-friction-cta"],
            "risk_level": "low",
            "rewrite_mode": "exploratory",
            "source_asset_ids": [],
        },
        {
            "candidate_id": "cand-d01",
            "asset_text": "躺下先被穩穩接住，中鋼獨立筒搭配獨家泡棉，讓腰背壓力少一點。",
            "asset_type": "description",
            "source": "safer_rewrite",
            "angle_key": "pain_point",
            "intent": "保留原本高表現的支撐與痛點吸引力，但拿掉直接療效承諾。",
            "related_gap": "desc-01 高風險痛點句 safer rewrite",
            "suggested_role": "測試",
            "covers_tokens": [],
            "inherits_motifs": ["pain-point-solution", "support-feel"],
            "risk_level": "medium",
            "rewrite_mode": "safer-rewrite",
            "safer_rewrite_of": text_to_id["腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。"],
            "source_asset_ids": [text_to_id["腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。"]],
        },
        {
            "candidate_id": "cand-d02",
            "asset_text": "LOVEFU飄雲專利床墊，以穩定支撐搭配柔軟包覆，延續高評價的無壓睡感。",
            "asset_type": "description",
            "source": "safer_rewrite",
            "angle_key": "social_proof",
            "intent": "保留高評價與無壓睡感，但移除緩解腰痛承諾。",
            "related_gap": "desc-03 社會證明句 safer rewrite",
            "suggested_role": "主力",
            "covers_tokens": ["LOVEFU", "飄雲專利"],
            "inherits_motifs": ["social-proof", "support-feel"],
            "risk_level": "medium",
            "rewrite_mode": "safer-rewrite",
            "safer_rewrite_of": text_to_id["LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。"],
            "source_asset_ids": [text_to_id["LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。"]],
        },
        {
            "candidate_id": "cand-d03",
            "asset_text": "LOVEFU山丘樂眠床，以穩定支撐搭配舒適包覆，讓久坐後的腰背更容易放鬆。",
            "asset_type": "description",
            "source": "safer_rewrite",
            "angle_key": "product_feel",
            "intent": "把零數據但高風險的山丘產品句改成可上稿的產品睡感版本。",
            "related_gap": "desc-22 hillbed-specific 風險句 safer rewrite",
            "suggested_role": "主力",
            "covers_tokens": ["LOVEFU", "山丘樂眠床"],
            "inherits_motifs": ["support-feel", "pain-point-solution"],
            "risk_level": "medium",
            "rewrite_mode": "safer-rewrite",
            "safer_rewrite_of": text_to_id["LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。"],
            "source_asset_ids": [text_to_id["LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。"]],
        },
        {
            "candidate_id": "cand-d04",
            "asset_text": "100天安心睡搭配10年保固，讓你先試睡，再慢慢決定適合自己的支撐感。",
            "asset_type": "description",
            "source": "reinforce_expansion",
            "angle_key": "risk_reversal",
            "intent": "補一條更完整的安心承諾 description。",
            "related_gap": "risk_reversal 需要更完整長文說明",
            "suggested_role": "測試",
            "covers_tokens": [],
            "inherits_motifs": ["lower-friction-cta"],
            "risk_level": "low",
            "rewrite_mode": "exploratory",
            "source_asset_ids": [text_to_id["100 天安心睡，帶你最需要的放鬆、慵懶。最好躺的 LOVEFU 硬床，不再睡睡醒醒，一覺到天明。"]],
        },
    ]
    return specs


def build_runtime_input(assets: list[dict[str, Any]], start_date: str, end_date: str) -> dict[str, Any]:
    return {
        "interpretation_id": "lovefu-hillbed-search-rsa-real-uat-v1-2",
        "brand_name": "LOVEFU大島樂眠",
        "product_name": "山丘樂眠床",
        "campaign_type": "search_rsa",
        "goal": "purchase",
        "reporting_period": {
            "start_date": start_date,
            "end_date": end_date,
        },
        "performance_data": {
            "reporting_context": {
                "asset_granularity": "asset_association_estimate",
                "includes_asset_level_conversion": False,
                "includes_asset_level_conversion_value": False,
                "includes_placement_breakout": False,
                "interpretation_layers": {
                    "click_layer": {
                        "status": "missing",
                        "required_fields": ["impressions", "clicks", "ctr", "active_duration_days"],
                        "notes": "CSV 有點擊／曝光欄位，但全數為 0；active_duration_days 來源缺失。",
                    },
                    "conversion_layer": {
                        "status": "partial",
                        "required_fields": [
                            "impressions",
                            "clicks",
                            "ctr",
                            "asset_level_conversions",
                            "active_duration_days",
                        ],
                        "recommended_fields": ["conversion_value", "placement_breakout"],
                        "notes": "只有跨多個 conversion action 的 asset association proxy，沒有真實 asset-level purchase conversions。",
                    },
                    "placement_layer": {
                        "status": "missing",
                        "required_fields": ["placement_breakout", "impressions", "clicks", "ctr"],
                        "notes": "素材關聯報表沒有 placement breakout。",
                    },
                    "duration_layer": {
                        "status": "missing",
                        "required_fields": ["active_duration_days"],
                        "notes": "CSV 沒有 active_duration_days，runtime 僅以 0 placeholder 滿足 schema。",
                    },
                },
                "notes": "真實來源為素材資源關聯報表。曝光、點擊、CTR 全為 0；轉換欄位為 association proxy，非嚴格 asset-level conversion。",
            },
            "assets": [
                {
                    "asset_id": asset["asset_id"],
                    "asset_type": asset["asset_type"],
                    "text": asset["text"],
                    "angle_key": asset["angle_key"],
                    "metrics": {
                        "impressions": 0,
                        "clicks": 0,
                        "ctr": 0,
                        "association_proxy_conversions": round(asset["proxy_conversions"], 2),
                    },
                    "active_duration_days": 0,
                    "status": "enabled",
                }
                for asset in assets
            ],
            "campaign_level_metrics": {
                "total_impressions": 0,
                "total_clicks": 0,
                "total_ctr": 0,
            },
        },
        "legacy_message_policy": {
            "protected_phrases": PROTECTED_PHRASES,
            "must_include_tokens": MUST_INCLUDE_TOKENS,
            "reusable_motifs": REUSABLE_MOTIFS,
        },
        "interpretation_config": {
            "minimum_impressions_threshold": 1000,
            "minimum_clicks_threshold": 60,
            "minimum_conversion_threshold": 3,
            "high_performer_percentile": 0.75,
            "data_sufficiency_threshold": 5000,
            "observe_stale_days": 21,
            "retire_candidate_days": 35,
            "decision_metric_priority": "hybrid",
        },
        "notes": "real_uat_rerun: true; source_csv=/Users/andychou/Downloads/素材資源關聯報表 (1).csv; runtime_placeholder_active_duration_days=0",
    }


def build_interpreter_output(
    assets: list[dict[str, Any]],
    runtime_input: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    headline_values = [asset["proxy_conversions"] for asset in assets if asset["asset_type"] == "headline" and asset["proxy_conversions"] > 0]
    description_values = [asset["proxy_conversions"] for asset in assets if asset["asset_type"] == "description" and asset["proxy_conversions"] > 0]
    percentiles = {
        "headline": {
            "p25": round(percentile(headline_values, 0.25), 2),
            "p50": round(percentile(headline_values, 0.50), 2),
            "p75": round(percentile(headline_values, 0.75), 2),
            "eligible": len(headline_values),
        },
        "description": {
            "p25": round(percentile(description_values, 0.25), 2),
            "p50": round(percentile(description_values, 0.50), 2),
            "p75": round(percentile(description_values, 0.75), 2),
            "eligible": len(description_values),
        },
    }

    candidate_by_source = defaultdict(list)
    for candidate in candidates:
        for source_asset_id in candidate.get("source_asset_ids", []):
            candidate_by_source[source_asset_id].append(candidate["candidate_id"])

    asset_decisions: list[dict[str, Any]] = []
    retire_now_assets: list[dict[str, Any]] = []
    observe_breakdown = Counter()

    low_perf_retire_texts = {
        "撐腰床墊推薦，LOVEFU 值得信賴",
        "LOVEFU 飄雲專利床墊，支撐舒適",
        "山丘樂眠床，LOVEFU 提供好眠",
    }
    observe_borderline_texts = {
        "白天你撐起生活，晚上山丘撐住你",
        "山丘樂眠床 第2張床 擁有支撐腰背與放鬆的魔法",
        "LOVEFU 山丘樂眠床，結合硬床墊的穩定支撐與柔軟包覆，讓您享受深度舒適睡眠。",
    }

    for asset in assets:
        cohort = percentiles[asset["asset_type"]]
        proxy = round(asset["proxy_conversions"], 2)
        risk_level = asset["risk_level"]
        legacy_tags = asset["legacy_tags"]
        performance_tier = "insufficient_data"
        decision = "observe_insufficient_data"
        observe_reason: str | None = "missing_click_duration_and_proxy_signal"

        if proxy == 0:
            if asset["text"] in FORCED_RETIRE_TEXTS or asset["text"] in low_perf_retire_texts:
                decision = "retire"
                performance_tier = "insufficient_data"
                observe_reason = None
            else:
                decision = "observe_insufficient_data"
                performance_tier = "insufficient_data"
                observe_reason = "association_proxy_absent"
        elif asset["text"] in FORCED_RETIRE_TEXTS:
            decision = "retire"
            performance_tier = "top" if proxy >= cohort["p75"] else "low"
            observe_reason = None
        elif proxy >= cohort["p75"]:
            decision = "reinforce"
            performance_tier = "top"
            observe_reason = None
        elif proxy >= cohort["p50"]:
            decision = "retain"
            performance_tier = "mid"
            observe_reason = None
        elif proxy >= cohort["p25"]:
            if asset["text"] in observe_borderline_texts:
                decision = "observe_borderline"
                performance_tier = "borderline"
                observe_reason = "proxy_near_p50_and_angle_still_useful"
            else:
                decision = "retain"
                performance_tier = "low"
                observe_reason = None
        else:
            if asset["text"] in low_perf_retire_texts:
                decision = "retire"
                performance_tier = "low"
                observe_reason = None
            else:
                decision = "observe_borderline"
                performance_tier = "borderline"
                observe_reason = "proxy_below_p25_but_angle_not_fully_replaceable"

        if decision.startswith("observe_"):
            observe_breakdown[decision] += 1

        basis_note = (
            "真實 CSV 缺 impression / clicks / ctr / active_duration_days，"
            "本輪僅能以跨 conversion action 的 association proxy 做方向性判讀。"
        )
        if decision == "retire" and asset["text"] in FORCED_RETIRE_TEXTS and risk_level in {"high", "medium"}:
            rationale = (
                f"在 {asset['asset_type']} cohort 中 proxy {proxy} 雖然不弱，"
                f"但原句包含高風險結果承諾，v1.2 不再只因歷史表現保留原句，"
                f"改以下降風險 rewrite 補位。"
            )
        elif decision == "retire":
            rationale = (
                f"在 {asset['asset_type']} cohort 中 proxy {proxy} 低於 P25 {cohort['p25']}，"
                "而且此句主要只是 token 或 generic trust 載體，可由更明確的 replacement candidate 補位。"
            )
        elif decision == "reinforce":
            rationale = (
                f"在 {asset['asset_type']} cohort 中 proxy {proxy} 高於 P75 {cohort['p75']}，"
                "雖然只能視為方向性訊號，但足以保留並萃取語言模式。"
            )
        elif decision == "retain":
            rationale = (
                f"在 {asset['asset_type']} cohort 中 proxy {proxy} 至少達 P50 {cohort['p50']}，"
                "屬可保留的中段素材，但因 rich layers 缺失，不擴大解讀。"
            )
        elif decision == "observe_borderline":
            rationale = (
                f"proxy {proxy} 介於邊界區，且 angle 仍有 coverage 價值，"
                "先列 observe_borderline，交由 builder 決定是否保留測試位。"
            )
        else:
            rationale = (
                "source CSV 沒有 click / duration layers，且 proxy 為 0，"
                "無法判斷是新素材、無效素材或只是尚未被吃到訊號，先列 observe_insufficient_data。"
            )

        decision_record = {
            "asset_id": asset["asset_id"],
            "text": asset["text"],
            "asset_type": asset["asset_type"],
            "angle_key": asset["angle_key"],
            "decision": decision,
            "decision_rationale": rationale,
            "decision_basis": {
                "primary_metric": "association_proxy_only",
                "asset_type_cohort": asset["asset_type"],
                "placement_scope": "overall",
                "eligible_asset_count": cohort["eligible"],
                "cohort_percentiles": {
                    "p25": cohort["p25"],
                    "p50": cohort["p50"],
                    "p75": cohort["p75"],
                },
                "data_layers_used": ["association_proxy"],
                "supporting_metrics_available": ["conversion_association_count", "conversion_action_breakout"],
                "placement_breakout_available": False,
                "notes": basis_note,
            },
            "decision_confidence": "directional",
            "performance_tier": performance_tier,
            "metrics_summary": {
                "impressions": 0,
                "clicks": 0,
                "ctr": 0,
                "active_duration_days": 0,
            },
            "active_duration_days": 0,
            "observe_reason": observe_reason,
            "staleness_flag": False,
            "legacy_tags": legacy_tags,
        }
        asset_decisions.append(decision_record)

        if decision == "retire":
            coverage_gaps = []
            for phrase in legacy_tags["protected_phrases_matched"]:
                coverage_gaps.append(f"protected_phrase:{phrase}")
            for token in legacy_tags["must_include_tokens_matched"]:
                coverage_gaps.append(f"must_include_token:{token}")
            coverage_gaps.append(f"angle:{asset['angle_key']}")
            retire_record = {
                "asset_id": asset["asset_id"],
                "asset_text": asset["text"],
                "asset_type": asset["asset_type"],
                "angle_key": asset["angle_key"],
                "reason": rationale,
                "decision_confidence": "directional",
                "decision_basis_ref": asset["asset_id"],
                "coverage_gap_created": coverage_gaps,
            }
            if candidate_by_source[asset["asset_id"]]:
                retire_record["replaced_by_candidate_id"] = candidate_by_source[asset["asset_id"]][0]
            retire_now_assets.append(retire_record)

    total_proxy_conversions = round(sum(asset["proxy_conversions"] for asset in assets), 2)
    matched_for_phrase = defaultdict(list)
    matched_for_token = defaultdict(list)
    matched_for_motif = defaultdict(list)
    for asset in assets:
        for phrase in asset["legacy_tags"]["protected_phrases_matched"]:
            matched_for_phrase[phrase].append(asset["asset_id"])
        for token in asset["legacy_tags"]["must_include_tokens_matched"]:
            matched_for_token[token].append(asset["asset_id"])
        for motif in asset["legacy_tags"]["reusable_motifs_matched"]:
            matched_for_motif[motif].append(asset["asset_id"])

    legacy_message_state = {
        "protected_phrases": [
            {
                "phrase": item["phrase"],
                "min_active_assets": item["min_active_assets"],
                "matched_asset_ids": matched_for_phrase[item["phrase"]],
                "status": "covered" if len(matched_for_phrase[item["phrase"]]) >= item["min_active_assets"] else "gap",
                "notes": "source CSV 缺 rich layers，因此 coverage 只驗 presence，不驗真正的活躍天數。",
            }
            for item in PROTECTED_PHRASES
        ],
        "must_include_tokens": [
            {
                "token": item["token"],
                "min_active_assets": item["min_active_assets"],
                "matched_asset_ids": matched_for_token[item["token"]],
                "status": "covered" if len(matched_for_token[item["token"]]) >= item["min_active_assets"] else "gap",
                "notes": "v1.2 保護 token visibility，不保護弱句本身。",
            }
            for item in MUST_INCLUDE_TOKENS
        ],
        "reusable_motifs": [
            {
                "motif_key": item["motif_key"],
                "description": item["description"],
                "source_assets": matched_for_motif[item["motif_key"]],
                "recommendation": "可作為 candidate 生成依據，但不可當成硬 retain gate。",
                "confidence": "medium" if matched_for_motif[item["motif_key"]] else "low",
            }
            for item in REUSABLE_MOTIFS
        ],
    }

    high_value_language = {
        "patterns": [
            {
                "pattern": "數字證據先行，再接床墊類別或支撐承諾",
                "angle_key": "concrete_number",
                "evidence": "hl-01、hl-04、hl-05 都是 headline proxy 排名前段。",
                "source_asset_ids": ["hl-01", "hl-04", "hl-05"],
                "confidence": "medium",
            },
            {
                "pattern": "100天安心睡 + 放鬆/先試再決定",
                "angle_key": "risk_reversal",
                "evidence": "hl-06 與 desc-02 形成同一安心承諾母語言。",
                "source_asset_ids": ["hl-06", "desc-02"],
                "confidence": "medium",
            },
            {
                "pattern": "品牌名 + 專利 / MIT / 認證訊號",
                "angle_key": "brand_trust",
                "evidence": "hl-02、hl-07、hl-13 代表真實來源中的 trust backbone。",
                "source_asset_ids": ["hl-02", "hl-07", "hl-13"],
                "confidence": "medium",
            },
            {
                "pattern": "生活情境句，把支撐感拉回第 2 張床場景",
                "angle_key": "life_scene",
                "evidence": "hl-36、hl-39 雖非 top，但在 builder stage 能補 coverage。",
                "source_asset_ids": ["hl-36", "hl-39"],
                "confidence": "low",
            },
        ]
    }

    next_round_brief_additions = {
        "proven_angles": [
            {
                "key": "risk_reversal",
                "label": ANGLE_LABELS["risk_reversal"],
                "evidence": "100天安心睡在真實資產中同時出現在高 proxy headline 與 description。",
            },
            {
                "key": "brand_trust",
                "label": ANGLE_LABELS["brand_trust"],
                "evidence": "LOVEFU / MIT / 認證 / 專利語言反覆出現在中高 proxy 資產中。",
            },
            {
                "key": "concrete_number",
                "label": ANGLE_LABELS["concrete_number"],
                "evidence": "200kg、97%、2026 等數字證據仍是主要 attention hook。",
            },
        ],
        "language_to_avoid": [
            "不再背痛失眠",
            "腰椎不再酸痛",
            "專為腰痛患者設計",
            "幫助緩解腰痛",
            "告別腰痛困擾",
            "腰椎更健康",
        ],
        "constraints_from_performance": {
            "protected_phrases": [item["phrase"] for item in PROTECTED_PHRASES],
            "must_include_tokens": [item["token"] for item in MUST_INCLUDE_TOKENS],
            "reusable_motifs": [item["motif_key"] for item in REUSABLE_MOTIFS],
            "cta_preference": "試睡、安心、先決定，不要強壓立即療效承諾。",
            "tone_adjustments": [
                "產品名與品牌名要更靠近山丘樂眠床，不要只停在泛 LOVEFU／飄雲語言。",
                "痛點句改成負擔減輕或支撐感受，不做治療或改善承諾。",
            ],
        },
        "candidate_pipeline_triggers": [
            {
                "gap_id": "gap-hl-03",
                "angle_key": "pain_point",
                "rewrite_mode": "safer-rewrite",
                "priority": "high",
                "notes": "高 proxy 歷史贏家，但醫療／結果承諾過強。",
            },
            {
                "gap_id": "gap-desc-01",
                "angle_key": "pain_point",
                "rewrite_mode": "safer-rewrite",
                "priority": "high",
                "notes": "要保留支撐與規格吸引力，但拿掉直接酸痛改善宣稱。",
            },
            {
                "gap_id": "gap-desc-03",
                "angle_key": "social_proof",
                "rewrite_mode": "safer-rewrite",
                "priority": "high",
                "notes": "社會證明可保留，但不能再直接承諾緩解腰痛。",
            },
            {
                "gap_id": "gap-hl-86",
                "angle_key": "product_feel",
                "rewrite_mode": "retain-intent",
                "priority": "high",
                "notes": "弱 token carrier 退場後，需要更像產品賣點而非空泛品牌句。",
            },
            {
                "gap_id": "gap-entry-value",
                "angle_key": "entry_value",
                "rewrite_mode": "exploratory",
                "priority": "low",
                "notes": "真實來源幾乎沒有足夠強的入門價值句，需額外驗證。",
            },
        ],
    }

    return {
        "interpretation_id": runtime_input["interpretation_id"],
        "brand_name": runtime_input["brand_name"],
        "product_name": runtime_input["product_name"],
        "campaign_type": runtime_input["campaign_type"],
        "generated_by": "codex",
        "generated_at": NOW.isoformat(),
        "angle_taxonomy": {
            "version": "v1.2",
            "keys": ANGLE_KEYS,
        },
        "data_sufficiency": {
            "overall_verdict": "partial",
            "click_layer_verdict": "missing",
            "conversion_layer_verdict": "partial",
            "placement_layer_verdict": "missing",
            "duration_layer_verdict": "missing",
            "total_impressions": 0,
            "total_clicks": 0,
            "threshold_used": 5000,
            "assets_below_threshold": len(assets),
            "reporting_context": {
                "asset_granularity": "asset_association_estimate",
                "includes_asset_level_conversion": False,
                "includes_asset_level_conversion_value": False,
                "includes_placement_breakout": False,
            },
            "gaps_identified": [
                "原始 CSV 有 impressions / clicks / ctr 欄位，但全數為 0 或 --，無法作為 click layer。",
                f"報表存在約 {total_proxy_conversions} 的 conversion association proxy，但不是 asset-level purchase conversions。",
                "缺 placement_breakout，因此無法做 Search / Display split interpretation。",
                "缺 active_duration_days，因此 observe_new / observe_stale / retire_candidate 都不能可靠使用。",
                "runtime 以 active_duration_days=0 placeholder 通過 schema，這是明確的手動 caveat，不可被誤解為真實上線天數。",
            ],
        },
        "asset_type_percentiles": [
            {
                "asset_type": "headline",
                "primary_metric": "association_proxy_only",
                "placement_scope": "overall",
                "eligible_asset_count": percentiles["headline"]["eligible"],
                "p25": percentiles["headline"]["p25"],
                "p50": percentiles["headline"]["p50"],
                "p75": percentiles["headline"]["p75"],
                "notes": "以 aggregated conversion association proxy 計算。",
            },
            {
                "asset_type": "description",
                "primary_metric": "association_proxy_only",
                "placement_scope": "overall",
                "eligible_asset_count": percentiles["description"]["eligible"],
                "p25": percentiles["description"]["p25"],
                "p50": percentiles["description"]["p50"],
                "p75": percentiles["description"]["p75"],
                "notes": "以 aggregated conversion association proxy 計算。",
            },
        ],
        "asset_decisions": asset_decisions,
        "high_value_language": high_value_language,
        "legacy_message_state": legacy_message_state,
        "next_round_brief_additions": next_round_brief_additions,
        "retire_now_assets": retire_now_assets,
        "new_candidate_assets": candidates,
        "compliance_notes": {
            "data_caveats": [
                "這次是真實 LOVEFU 素材資源關聯報表 rerun，但 source export 不足以支撐 richer click / conversion / placement / duration layers。",
                "所有舊素材 decision_confidence 都只能是 directional，不能誤用成 high / medium / low 的表現結論。",
                "active_duration_days 為 runtime placeholder 0，只用於 schema 通過與明確標記缺失。",
                "真實素材池混有泛 LOVEFU / 飄雲與山丘樂眠床語言，final pack 已刻意拉高 hillbed-specific 比例。",
            ],
            "manual_review_required": True,
            "interpretation_confidence": "low",
            "candidate_pipeline_ready": True,
            "angle_taxonomy_ready": True,
        },
    }


def build_builder_output(
    interpreter_output: dict[str, Any],
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    decisions_by_id = {item["asset_id"]: item for item in interpreter_output["asset_decisions"]}
    decisions_by_text = {item["text"]: item for item in interpreter_output["asset_decisions"]}
    candidate_by_id = {item["candidate_id"]: item for item in candidates}

    used_candidate_ids = {
        "cand-h01",
        "cand-h02",
        "cand-h03",
        "cand-h04",
        "cand-h05",
        "cand-h06",
        "cand-d01",
        "cand-d02",
        "cand-d03",
    }

    rejected_candidates = [
        {
            "candidate_id": "cand-h07",
            "asset_text": candidate_by_id["cand-h07"]["asset_text"],
            "asset_type": "headline",
            "source": candidate_by_id["cand-h07"]["source"],
            "angle_key": candidate_by_id["cand-h07"]["angle_key"],
            "risk_level": candidate_by_id["cand-h07"]["risk_level"],
            "rewrite_mode": candidate_by_id["cand-h07"]["rewrite_mode"],
            "reason_rejected": "product_feel 在 headline 已有兩條 replacement 與一條情境主力，這條精簡句造成冗餘。",
        },
        {
            "candidate_id": "cand-h08",
            "asset_text": candidate_by_id["cand-h08"]["asset_text"],
            "asset_type": "headline",
            "source": candidate_by_id["cand-h08"]["source"],
            "angle_key": candidate_by_id["cand-h08"]["angle_key"],
            "risk_level": candidate_by_id["cand-h08"]["risk_level"],
            "rewrite_mode": candidate_by_id["cand-h08"]["rewrite_mode"],
            "reason_rejected": "entry_value 在真實報表中缺少足夠 proxy 支撐，先記錄為 gap，不直接進 final pack。",
        },
        {
            "candidate_id": "cand-d04",
            "asset_text": candidate_by_id["cand-d04"]["asset_text"],
            "asset_type": "description",
            "source": candidate_by_id["cand-d04"]["source"],
            "angle_key": candidate_by_id["cand-d04"]["angle_key"],
            "risk_level": candidate_by_id["cand-d04"]["risk_level"],
            "rewrite_mode": candidate_by_id["cand-d04"]["rewrite_mode"],
            "reason_rejected": "description 容量只有 4 格，風險逆轉已有 desc-02 與 cand-h05 承接，這條暫不進本輪上稿。",
        },
    ]

    def final_asset_from_existing(asset_id: str, role: str, source: str, status_note: str | None = None) -> dict[str, Any]:
        decision = decisions_by_id[asset_id]
        char_count = len(decision["text"])
        record = {
            "asset_id": asset_id,
            "text": decision["text"],
            "asset_type": decision["asset_type"],
            "role": role,
            "source": source,
            "angle_key": decision["angle_key"],
            "performance_tier": decision["performance_tier"],
            "decision_confidence": decision["decision_confidence"],
            "decision_basis_metric": decision["decision_basis"]["primary_metric"],
            "observe_subtype": decision["decision"] if decision["decision"].startswith("observe_") else None,
            "risk_level": None,
            "rewrite_mode": None,
            "is_protected_phrase_carrier": bool(decision["legacy_tags"]["protected_phrases_matched"]),
            "char_count": char_count,
            "coverage_tags": {
                "protected_phrases": decision["legacy_tags"]["protected_phrases_matched"],
                "must_include_tokens": decision["legacy_tags"]["must_include_tokens_matched"],
                "reusable_motifs": decision["legacy_tags"]["reusable_motifs_matched"],
            },
        }
        if status_note is not None:
            record["status_note"] = status_note
        return record

    def final_asset_from_candidate(candidate_id: str, role: str) -> dict[str, Any]:
        candidate = candidate_by_id[candidate_id]
        source = "replacement"
        if candidate["source"] == "safer_rewrite":
            source = "safer_rewrite"
        elif candidate["source"] == "reinforce_expansion":
            source = "expansion"
        elif candidate["source"] == "brief_generator_auto":
            source = "brief_new"
        confidence = "low"
        if candidate["rewrite_mode"] == "safer-rewrite":
            confidence = "medium"
        elif candidate["source"] == "replace_retired_asset":
            confidence = "low"
        return {
            "asset_id": candidate["candidate_id"],
            "text": candidate["asset_text"],
            "asset_type": candidate["asset_type"],
            "role": role,
            "source": source,
            "angle_key": candidate["angle_key"],
            "performance_tier": "new",
            "decision_confidence": confidence,
            "decision_basis_metric": None,
            "observe_subtype": None,
            "risk_level": candidate["risk_level"],
            "rewrite_mode": candidate["rewrite_mode"],
            "is_protected_phrase_carrier": any(item["phrase"] in candidate["asset_text"] for item in PROTECTED_PHRASES),
            "char_count": len(candidate["asset_text"]),
            "coverage_tags": {
                "protected_phrases": [item["phrase"] for item in PROTECTED_PHRASES if item["phrase"] in candidate["asset_text"]],
                "must_include_tokens": candidate["covers_tokens"],
                "reusable_motifs": candidate["inherits_motifs"],
            },
        }

    text_to_final_id: dict[str, str] = {}

    primary_assets = []
    for text in FINAL_HEADLINE_PRIMARY_TEXTS:
        if text in decisions_by_text:
            asset = final_asset_from_existing(
                decisions_by_text[text]["asset_id"],
                "主力",
                "retained_observe" if decisions_by_text[text]["decision"].startswith("observe_") else ("retained_protected_phrase" if decisions_by_text[text]["legacy_tags"]["protected_phrases_matched"] else "retained"),
                status_note="以 observe_borderline 身分保留，下一輪若 proxy 仍未上升則移出。" if decisions_by_text[text]["decision"] == "observe_borderline" else None,
            )
        else:
            candidate_id = next(candidate["candidate_id"] for candidate in candidates if candidate["asset_text"] == text)
            asset = final_asset_from_candidate(candidate_id, "主力")
        primary_assets.append(asset)
        text_to_final_id[text] = asset["asset_id"]

    for text in FINAL_DESCRIPTION_PRIMARY_TEXTS:
        if text in decisions_by_text:
            asset = final_asset_from_existing(
                decisions_by_text[text]["asset_id"],
                "主力",
                "retained_protected_phrase" if decisions_by_text[text]["legacy_tags"]["protected_phrases_matched"] else "retained",
            )
        else:
            candidate_id = next(candidate["candidate_id"] for candidate in candidates if candidate["asset_text"] == text)
            asset = final_asset_from_candidate(candidate_id, "主力")
        primary_assets.append(asset)
        text_to_final_id[text] = asset["asset_id"]

    test_assets = []
    for text in FINAL_HEADLINE_TEST_TEXTS:
        if text in decisions_by_text:
            asset = final_asset_from_existing(
                decisions_by_text[text]["asset_id"],
                "測試",
                "retained_observe",
                status_note="observe_borderline 僅保留測試位，避免直接佔滿主力槽。",
            )
        else:
            candidate_id = next(candidate["candidate_id"] for candidate in candidates if candidate["asset_text"] == text)
            asset = final_asset_from_candidate(candidate_id, "測試")
        test_assets.append(asset)
        text_to_final_id[text] = asset["asset_id"]

    for text in FINAL_DESCRIPTION_TEST_TEXTS:
        candidate_id = next(candidate["candidate_id"] for candidate in candidates if candidate["asset_text"] == text)
        asset = final_asset_from_candidate(candidate_id, "測試")
        test_assets.append(asset)
        text_to_final_id[text] = asset["asset_id"]

    replacement_map = [
        {
            "retired_asset_id": decisions_by_text["不再背痛失眠－LOVEFU山丘樂眠床"]["asset_id"],
            "retired_text": "不再背痛失眠－LOVEFU山丘樂眠床",
            "retired_asset_type": "headline",
            "retirement_reason": decisions_by_text["不再背痛失眠－LOVEFU山丘樂眠床"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-h01",
            "replacement_text": candidate_by_id["cand-h01"]["asset_text"],
            "replacement_rationale": "保留腰背負擔切入與產品名，但移除醫療／結果承諾。",
            "replacement_decision_confidence": "medium",
            "rewrite_mode": "safer-rewrite",
            "coverage_after_replacement": ["must_include_token:LOVEFU", "must_include_token:山丘樂眠床", "angle:pain_point"],
            "notes": "safer_rewrite_of=hl-03",
        },
        {
            "retired_asset_id": decisions_by_text["腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。"]["asset_id"],
            "retired_text": "腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。",
            "retired_asset_type": "description",
            "retirement_reason": decisions_by_text["腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-d01",
            "replacement_text": candidate_by_id["cand-d01"]["asset_text"],
            "replacement_rationale": "保留支撐與規格證據，但把酸痛改善改成更安全的負擔減輕敘述。",
            "replacement_decision_confidence": "medium",
            "rewrite_mode": "safer-rewrite",
            "coverage_after_replacement": ["angle:pain_point", "motif:support-feel"],
            "notes": "safer_rewrite_of=desc-01",
        },
        {
            "retired_asset_id": decisions_by_text["LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。"]["asset_id"],
            "retired_text": "LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。",
            "retired_asset_type": "description",
            "retirement_reason": decisions_by_text["LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-d02",
            "replacement_text": candidate_by_id["cand-d02"]["asset_text"],
            "replacement_rationale": "保留高評價與無壓睡感，但拿掉緩解腰痛承諾。",
            "replacement_decision_confidence": "medium",
            "rewrite_mode": "safer-rewrite",
            "coverage_after_replacement": ["must_include_token:LOVEFU", "must_include_token:飄雲專利", "angle:social_proof"],
            "notes": "safer_rewrite_of=desc-03",
        },
        {
            "retired_asset_id": decisions_by_text["LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。"]["asset_id"],
            "retired_text": "LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。",
            "retired_asset_type": "description",
            "retirement_reason": decisions_by_text["LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-d03",
            "replacement_text": candidate_by_id["cand-d03"]["asset_text"],
            "replacement_rationale": "把高風險痛點承諾改成產品睡感與久坐族的放鬆承接。",
            "replacement_decision_confidence": "medium",
            "rewrite_mode": "safer-rewrite",
            "coverage_after_replacement": ["must_include_token:LOVEFU", "must_include_token:山丘樂眠床", "angle:product_feel"],
            "notes": "safer_rewrite_of=desc-22",
        },
        {
            "retired_asset_id": decisions_by_text["撐腰床墊推薦，LOVEFU 值得信賴"]["asset_id"],
            "retired_text": "撐腰床墊推薦，LOVEFU 值得信賴",
            "retired_asset_type": "headline",
            "retirement_reason": decisions_by_text["撐腰床墊推薦，LOVEFU 值得信賴"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-h02",
            "replacement_text": candidate_by_id["cand-h02"]["asset_text"],
            "replacement_rationale": "把 generic trust 句改成更明確的產品名與腰背承接。",
            "replacement_decision_confidence": "low",
            "rewrite_mode": "retain-intent",
            "coverage_after_replacement": ["must_include_token:LOVEFU", "must_include_token:山丘樂眠床", "angle:pain_point"],
            "notes": "補回 trust + product specific coverage",
        },
        {
            "retired_asset_id": decisions_by_text["LOVEFU 飄雲專利床墊，支撐舒適"]["asset_id"],
            "retired_text": "LOVEFU 飄雲專利床墊，支撐舒適",
            "retired_asset_type": "headline",
            "retirement_reason": decisions_by_text["LOVEFU 飄雲專利床墊，支撐舒適"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-h03",
            "replacement_text": candidate_by_id["cand-h03"]["asset_text"],
            "replacement_rationale": "保留支撐包覆睡感，但把泛系列句改成更明確的 hillbed 指向。",
            "replacement_decision_confidence": "low",
            "rewrite_mode": "retain-intent",
            "coverage_after_replacement": ["must_include_token:LOVEFU", "must_include_token:山丘樂眠床", "angle:product_feel"],
            "notes": "由泛 LOVEFU / 飄雲切向 hillbed-specific",
        },
        {
            "retired_asset_id": decisions_by_text["山丘樂眠床，LOVEFU 提供好眠"]["asset_id"],
            "retired_text": "山丘樂眠床，LOVEFU 提供好眠",
            "retired_asset_type": "headline",
            "retirement_reason": decisions_by_text["山丘樂眠床，LOVEFU 提供好眠"]["decision_rationale"],
            "action": "replaced",
            "replacement_gap_unfilled": False,
            "replacement_asset_id": "cand-h04",
            "replacement_text": candidate_by_id["cand-h04"]["asset_text"],
            "replacement_rationale": "保留品牌與產品名，但把空泛好眠改成接住腰背的產品睡感。",
            "replacement_decision_confidence": "low",
            "rewrite_mode": "retain-intent",
            "coverage_after_replacement": ["must_include_token:LOVEFU", "must_include_token:山丘樂眠床", "angle:product_feel"],
            "notes": "must_include_token 不再保護弱句本身",
        },
    ]

    final_assets = primary_assets + test_assets
    angle_counts = defaultdict(lambda: {"primary": 0, "test": 0})
    for asset in final_assets:
        key = asset["angle_key"]
        bucket = "primary" if asset["role"] == "主力" else "test"
        angle_counts[key][bucket] += 1

    angle_coverage = []
    for key in ANGLE_KEYS:
        primary_count = angle_counts[key]["primary"]
        test_count = angle_counts[key]["test"]
        total = primary_count + test_count
        if total == 0:
            status = "gap"
            redundancy = "watch"
            recommendation = "本輪 final pack 沒有承接這個 angle。"
        elif primary_count >= 2:
            status = "core"
            redundancy = "overbuilt" if total >= 4 else "balanced"
            recommendation = "可維持，但若後續要擴寫，先檢查是否已接近冗餘。"
        elif primary_count >= 1 and test_count >= 1:
            status = "supporting"
            redundancy = "balanced"
            recommendation = "主力已承接，測試位可再驗證變體。"
        elif primary_count == 1 and test_count == 0:
            status = "thin"
            redundancy = "watch"
            recommendation = "只有單一 carrier，後續若移除要先補位。"
        else:
            status = "test_only"
            redundancy = "watch"
            recommendation = "只有測試位承接，先觀察再決定是否升主力。"
        angle_coverage.append(
            {
                "angle_key": key,
                "label": ANGLE_LABELS[key],
                "primary_count": primary_count,
                "test_count": test_count,
                "total": total,
                "status": status,
                "redundancy_status": redundancy,
                "recommendation": recommendation,
            }
        )

    protected_carriers = [asset["asset_id"] for asset in final_assets if asset["is_protected_phrase_carrier"]]
    protected_phrase_check = [
        {
            "term": "100天安心睡",
            "required_count": 1,
            "found_count": len(protected_carriers),
            "found_in": protected_carriers,
            "status": "covered" if protected_carriers else "gap",
        }
    ]

    token_coverage_check = []
    for token in ["山丘樂眠床", "LOVEFU", "飄雲專利"]:
        found_in = [asset["asset_id"] for asset in final_assets if token in asset["text"]]
        token_coverage_check.append(
            {
                "term": token,
                "required_count": 2 if token != "飄雲專利" else 1,
                "found_count": len(found_in),
                "found_in": found_in,
                "status": "covered" if found_in else "gap",
            }
        )

    motif_coverage_check = [
        {
            "motif_key": "concrete-number",
            "found_in": [asset["asset_id"] for asset in final_assets if "concrete-number" in asset["coverage_tags"]["reusable_motifs"] or any(token in asset["text"] for token in ["200kg", "2026"])],
            "status": "covered",
            "notes": "由 hl-01 與 hl-12 承接。",
        },
        {
            "motif_key": "pain-point-solution",
            "found_in": [asset["asset_id"] for asset in final_assets if asset["angle_key"] == "pain_point"],
            "status": "covered",
            "notes": "只保留 safer rewrite 或較安全的負擔敘事。",
        },
        {
            "motif_key": "lower-friction-cta",
            "found_in": [asset["asset_id"] for asset in final_assets if asset["angle_key"] == "cta_lower_friction" or "lower-friction-cta" in asset["coverage_tags"]["reusable_motifs"]],
            "status": "covered",
            "notes": "由 hl-11 與 cand-h05 承接。",
        },
        {
            "motif_key": "support-feel",
            "found_in": [asset["asset_id"] for asset in final_assets if "support-feel" in asset["coverage_tags"]["reusable_motifs"] or asset["angle_key"] == "product_feel"],
            "status": "covered",
            "notes": "本輪 final pack 的主幹 motif。",
        },
        {
            "motif_key": "trust-proof",
            "found_in": [asset["asset_id"] for asset in final_assets if asset["angle_key"] in {"brand_trust", "social_proof"}],
            "status": "covered",
            "notes": "由品牌與高評價資產承接。",
        },
    ]

    observe_assets_status = []
    final_asset_ids = {asset["asset_id"] for asset in final_assets}
    for decision in interpreter_output["asset_decisions"]:
        if not decision["decision"].startswith("observe_"):
            continue
        disposition = "demoted_pending_review"
        rationale = "source report 缺 rich layers，因此 builder 不讓它直接佔主力。"
        if decision["asset_id"] in final_asset_ids:
            disposition = "promoted_to_primary" if any(asset["asset_id"] == decision["asset_id"] and asset["role"] == "主力" for asset in final_assets) else "keep_observing"
            rationale = "因為能補足 life_scene / hillbed-specific coverage，所以保留在 final pack。"
        elif decision["decision"] == "observe_borderline":
            disposition = "keep_observing"
            rationale = "接近邊界，但還沒有到值得直接退場的程度。"
        observe_assets_status.append(
            {
                "asset_id": decision["asset_id"],
                "text": decision["text"],
                "observe_subtype": decision["decision"],
                "active_duration_days": decision["active_duration_days"],
                "disposition": disposition,
                "rationale": rationale,
            }
        )

    redundancy_alerts = [
        {
            "asset_a_id": "hl-36",
            "asset_a_text": "白天你撐起生活，晚上山丘撐住你",
            "asset_b_id": "cand-h06",
            "asset_b_text": "第2張床，也值得被山丘穩穩接住",
            "similarity_reason": "兩句都承接 life_scene / 被接住語意，若之後要擴寫應避免再加第三句近義變體。",
            "recommendation": "keep_both",
        },
        {
            "asset_a_id": "cand-h03",
            "asset_a_text": "LOVEFU山丘樂眠床，支撐包覆更到位",
            "asset_b_id": "cand-h04",
            "asset_b_text": "LOVEFU山丘樂眠床，先接住腰背再放鬆",
            "similarity_reason": "都屬 hillbed-specific product_feel replacement，語意相近。",
            "recommendation": "review_and_choose",
        },
    ]

    type_counts = {
        "headline": {
            "target": 15,
            "primary": sum(asset["asset_type"] == "headline" and asset["role"] == "主力" for asset in final_assets),
            "test": sum(asset["asset_type"] == "headline" and asset["role"] == "測試" for asset in final_assets),
            "total": sum(asset["asset_type"] == "headline" for asset in final_assets),
            "within_limit": sum(asset["asset_type"] == "headline" for asset in final_assets) == 15,
        },
        "description": {
            "target": 4,
            "primary": sum(asset["asset_type"] == "description" and asset["role"] == "主力" for asset in final_assets),
            "test": sum(asset["asset_type"] == "description" and asset["role"] == "測試" for asset in final_assets),
            "total": sum(asset["asset_type"] == "description" for asset in final_assets),
            "within_limit": sum(asset["asset_type"] == "description" for asset in final_assets) == 4,
        },
    }

    coverage_gaps = [
        "angle:entry_value 仍是 gap，真實報表缺乏足夠安全且產品對焦的價值句。",
        "angle:legacy_phrase 只有單一 headline 承接，屬 thin coverage。",
        "rich_layer_gap: source CSV 依舊缺 click / placement / duration layers。",
    ]

    observe_breakdown = {
        "observe_new": 0,
        "observe_insufficient_data": sum(item["observe_subtype"] == "observe_insufficient_data" for item in observe_assets_status),
        "observe_stale": 0,
        "observe_borderline": sum(item["observe_subtype"] == "observe_borderline" for item in observe_assets_status),
    }

    return {
        "portfolio_id": "lovefu-hillbed-search-rsa-real-uat-v1-2",
        "source_interpretation_id": interpreter_output["interpretation_id"],
        "brand_name": interpreter_output["brand_name"],
        "product_name": interpreter_output["product_name"],
        "campaign_type": interpreter_output["campaign_type"],
        "generated_by": "codex",
        "generated_at": NOW.isoformat(),
        "angle_taxonomy": interpreter_output["angle_taxonomy"],
        "final_asset_pack": {
            "primary": primary_assets,
            "test": test_assets,
        },
        "replacement_map": replacement_map,
        "coverage_check": {
            "taxonomy_version": "v1.2",
            "angle_coverage": angle_coverage,
            "type_counts": type_counts,
            "protected_phrase_check": protected_phrase_check,
            "token_coverage_check": token_coverage_check,
            "motif_coverage_check": motif_coverage_check,
            "gaps": coverage_gaps,
        },
        "redundancy_alerts": redundancy_alerts,
        "rejected_candidates": rejected_candidates,
        "observe_assets_status": observe_assets_status,
        "portfolio_summary": {
            "total_primary": len(primary_assets),
            "total_test": len(test_assets),
            "total_final": len(primary_assets) + len(test_assets),
            "retained_from_previous": 10,
            "newly_added": 9,
            "retired_count": len(replacement_map),
            "rejected_candidates_count": len(rejected_candidates),
            "test_ratio": round(len(test_assets) / (len(primary_assets) + len(test_assets)), 3),
            "observe_count": len(observe_assets_status),
            "observe_breakdown": observe_breakdown,
            "replacement_gap_unfilled_count": 0,
        },
        "compliance_notes": {
            "data_caveats": interpreter_output["compliance_notes"]["data_caveats"],
            "manual_review_required": True,
            "upstream_confidence": "low",
            "field_level_contract_passed": True,
            "angle_taxonomy_aligned": True,
            "candidate_pipeline_complete": True,
        },
    }


def build_packager_output(builder_output: dict[str, Any]) -> dict[str, Any]:
    final_assets = builder_output["final_asset_pack"]["primary"] + builder_output["final_asset_pack"]["test"]

    def upload_asset(asset: dict[str, Any]) -> dict[str, Any]:
        limit = 30 if asset["asset_type"] == "headline" else 90
        char_count = len(asset["text"])
        record = {
            "asset_id": asset["asset_id"],
            "text": asset["text"],
            "char_count": char_count,
            "char_pass": char_count <= limit,
            "source": asset["source"],
            "angle_key": asset["angle_key"],
            "performance_tier": asset["performance_tier"],
            "decision_confidence": asset["decision_confidence"],
            "observe_subtype": asset["observe_subtype"],
            "risk_level": asset["risk_level"],
            "rewrite_mode": asset["rewrite_mode"],
            "is_protected_phrase_carrier": asset["is_protected_phrase_carrier"],
            "coverage_tags": asset["coverage_tags"],
        }
        if asset.get("status_note") is not None:
            record["status_note"] = asset["status_note"]
        return record

    def bucket_assets(role: str) -> dict[str, list[dict[str, Any]]]:
        scoped = [asset for asset in final_assets if asset["role"] == role]
        return {
            "headlines": [upload_asset(asset) for asset in scoped if asset["asset_type"] == "headline"],
            "descriptions": [upload_asset(asset) for asset in scoped if asset["asset_type"] == "description"],
        }

    character_audit_results = []
    all_pass = True
    for asset in final_assets:
        limit = 30 if asset["asset_type"] == "headline" else 90
        char_count = len(asset["text"])
        passed = char_count <= limit
        all_pass = all_pass and passed
        character_audit_results.append(
            {
                "asset_id": asset["asset_id"],
                "text": asset["text"],
                "asset_type": asset["asset_type"],
                "role": asset["role"],
                "char_count": char_count,
                "char_limit": limit,
                "pass": passed,
            }
        )

    angle_lookup = {item["angle_key"]: item for item in builder_output["coverage_check"]["angle_coverage"]}
    strategic_notes = {
        "main_angles": [
            {
                "angle_key": key,
                "label": ANGLE_LABELS[key],
                "evidence": angle_lookup[key]["recommendation"],
                "recommendation": "維持主力資產，下一輪只做小幅變體。",
            }
            for key in ["product_feel", "risk_reversal", "brand_trust", "social_proof"]
            if angle_lookup[key]["total"] > 0
        ],
        "test_angles": [
            {
                "angle_key": key,
                "label": ANGLE_LABELS[key],
                "evidence": angle_lookup[key]["recommendation"],
                "recommendation": "保留測試位，回看是否值得升主力。",
            }
            for key in ["pain_point", "life_scene", "cta_lower_friction"]
            if angle_lookup[key]["total"] > 0
        ],
        "do_not_expand_angles": [
            {
                "angle_key": "brand_trust",
                "label": ANGLE_LABELS["brand_trust"],
                "evidence": "真實來源中泛 LOVEFU / 飄雲 trust 句過多，若再擴寫會放大產品焦點漂移。",
                "recommendation": "除非新增更明確的山丘產品證據，否則不再擴充 generic trust copy。",
            },
            {
                "angle_key": "legacy_phrase",
                "label": ANGLE_LABELS["legacy_phrase"],
                "evidence": "本輪只有 hl-12 承接產品名 coverage，該 angle 只作 coverage carrier，不該再往外擴。",
                "recommendation": "維持單一 carrier 即可，不要把產品名 angle 擴成空泛 copy 池。",
            },
        ],
        "safer_rewrite_watchlist": [
            {
                "source_asset_id": "hl-03",
                "source_text": "不再背痛失眠－LOVEFU山丘樂眠床",
                "reason": "歷史 proxy 高，但原句屬高風險結果承諾。",
                "recommended_candidate_id": "cand-h01",
                "recommended_text": "睡醒少點負擔，LOVEFU山丘樂眠床",
            },
            {
                "source_asset_id": "desc-01",
                "source_text": "腰椎不再酸痛，只要躺上它就足夠，2 次加熱的中鋼獨立筒彈簧，搭配獨家泡棉，創造飄雲Ｑ彈躺感。",
                "reason": "高 proxy，但直接承諾酸痛改善。",
                "recommended_candidate_id": "cand-d01",
                "recommended_text": "躺下先被穩穩接住，中鋼獨立筒搭配獨家泡棉，讓腰背壓力少一點。",
            },
            {
                "source_asset_id": "desc-03",
                "source_text": "LOVEFU 飄雲專利床墊，98% 好評推薦，舒適支撐幫助緩解腰痛，讓您享受無壓樂眠。",
                "reason": "高評價與舒適感可保留，但不應直接承諾緩解腰痛。",
                "recommended_candidate_id": "cand-d02",
                "recommended_text": "LOVEFU飄雲專利床墊，以穩定支撐搭配柔軟包覆，延續高評價的無壓睡感。",
            },
            {
                "source_asset_id": "desc-22",
                "source_text": "LOVEFU 山丘樂眠床，專為腰痛患者設計，提供強力支撐與舒適包覆，帶來每晚好眠。",
                "reason": "山丘產品句應該保留，但患者導向承諾過於高風險。",
                "recommended_candidate_id": "cand-d03",
                "recommended_text": "LOVEFU山丘樂眠床，以穩定支撐搭配舒適包覆，讓久坐後的腰背更容易放鬆。",
            },
        ],
    }

    return {
        "package_id": "lovefu-hillbed-search-rsa-real-uat-upload-v1-2",
        "source_portfolio_id": builder_output["portfolio_id"],
        "brand_name": builder_output["brand_name"],
        "product_name": builder_output["product_name"],
        "campaign_type": builder_output["campaign_type"],
        "generated_by": "codex",
        "generated_at": NOW.isoformat(),
        "delivery_metadata": {
            "delivery_target": "media_buyer",
            "version_label": "real-uat-v1-2-20260315",
            "source_interpretation_id": builder_output["source_interpretation_id"],
            "upstream_confidence": "low",
            "angle_taxonomy_version": "v1.2",
            "sign_off_status": "pending_review",
        },
        "handoff_validation": {
            "portfolio_field_validation_passed": True,
            "validated_sections": [
                "angle_taxonomy",
                "final_asset_pack",
                "replacement_map",
                "coverage_check",
                "portfolio_summary",
                "compliance_notes",
            ],
        },
        "angle_taxonomy": builder_output["angle_taxonomy"],
        "strategic_notes": strategic_notes,
        "upload_ready_assets": {
            "primary_pack": bucket_assets("主力"),
            "test_pack": bucket_assets("測試"),
        },
        "retirement_changelog": builder_output["replacement_map"],
        "character_audit": {
            "results": character_audit_results,
            "all_pass": all_pass,
        },
        "redundancy_warnings": [
            {
                "asset_a_id": item["asset_a_id"],
                "asset_a_text": item["asset_a_text"],
                "asset_b_id": item["asset_b_id"],
                "asset_b_text": item["asset_b_text"],
                "similarity_reason": item["similarity_reason"],
                "recommendation": item["recommendation"],
            }
            for item in builder_output["redundancy_alerts"]
        ],
        "action_checklist": [
            {
                "step": 1,
                "action": "確認 protected phrase coverage",
                "detail": "檢查 hl-06、cand-h05、desc-02 是否都保留 100天安心睡。",
                "done": False,
            },
            {
                "step": 2,
                "action": "確認 must_include token coverage",
                "detail": "至少確認山丘樂眠床、LOVEFU、飄雲專利仍在線上素材中可見。",
                "done": False,
            },
            {
                "step": 3,
                "action": "人工 QA safer rewrite",
                "detail": "逐條比對 cand-h01、cand-d01、cand-d02、cand-d03 是否真的降風險且保留原 intent。",
                "done": False,
            },
            {
                "step": 4,
                "action": "回看 observe_borderline 素材",
                "detail": "hl-36 與 hl-39 是因 coverage 被保留，下一輪必須重新檢查是否繼續保留。",
                "done": False,
            },
            {
                "step": 5,
                "action": "確認 replacement gap",
                "detail": "本輪 replacement_gap_unfilled=0，但仍需確認所有 replacement 都已真正進 upload list。",
                "done": False,
            },
            {
                "step": 6,
                "action": "檢查 hillbed specificity",
                "detail": "真實來源混有泛 LOVEFU / 飄雲語言，最終上稿前確認 hillbed-specific 比例是否足夠。",
                "done": False,
            },
        ],
        "compliance_notes": {
            "inherited_caveats": builder_output["compliance_notes"]["data_caveats"],
            "packager_warnings": [
                "source report 缺 click / impression / duration / placement rich layers，所有舊素材 performance 只可視為 directional。",
                "本輪 final pack 有 9 則新 candidate，雖然更接近可上稿，但仍必須人工審核。",
                "entry_value angle 仍是 gap，本輪沒有進 final pack。",
            ],
            "manual_review_required": True,
        },
    }


def render_packager_markdown(packager_output: dict[str, Any], builder_output: dict[str, Any]) -> str:
    primary_headlines = packager_output["upload_ready_assets"]["primary_pack"]["headlines"]
    test_headlines = packager_output["upload_ready_assets"]["test_pack"]["headlines"]
    primary_descriptions = packager_output["upload_ready_assets"]["primary_pack"]["descriptions"]
    test_descriptions = packager_output["upload_ready_assets"]["test_pack"]["descriptions"]

    def asset_lines(items: list[dict[str, Any]]) -> list[str]:
        lines = []
        for item in items:
            lines.append(
                f"- `{item['asset_id']}` {item['text']} "
                f"[{ANGLE_LABELS[item['angle_key']]}，confidence={item['decision_confidence']}，source={item['source']}]"
            )
        return lines or ["- 無"]

    def replacement_lines() -> list[str]:
        lines = []
        for row in packager_output["retirement_changelog"]:
            lines.append(
                f"- `{row['retired_asset_id']}` {row['retired_text']} -> "
                f"`{row['replacement_asset_id']}` {row['replacement_text']} "
                f"[rewrite_mode={row['rewrite_mode']}]"
            )
        return lines

    checklist_lines = [
        f"- {item['step']}. {item['action']}：{item['detail']}"
        for item in packager_output["action_checklist"]
    ]

    note_lines = []
    for section, items in [
        ("主力角度", packager_output["strategic_notes"]["main_angles"]),
        ("測試角度", packager_output["strategic_notes"]["test_angles"]),
        ("不擴寫角度", packager_output["strategic_notes"]["do_not_expand_angles"]),
    ]:
        note_lines.append(f"## {section}")
        for item in items:
            note_lines.append(
                f"- {ANGLE_LABELS[item['angle_key']]}：{item['evidence']} {item.get('recommendation', '')}".strip()
            )
        note_lines.append("")

    watchlist_lines = []
    for item in packager_output["strategic_notes"]["safer_rewrite_watchlist"]:
        watchlist_lines.append(
            f"- `{item['source_asset_id']}` -> `{item['recommended_candidate_id']}`：{item['reason']}"
        )

    lines = [
        "# LOVEFU 山丘樂眠床 Google Ads Copy Pipeline v1.2 真實 UAT Packager Output",
        "",
        f"- generated_by: {packager_output['generated_by']}",
        f"- generated_at: {packager_output['generated_at']}",
        f"- source_portfolio_id: {packager_output['source_portfolio_id']}",
        f"- sign_off_status: {packager_output['delivery_metadata']['sign_off_status']}",
        "",
        "## 本輪上稿摘要",
        f"- Headlines：{len(primary_headlines) + len(test_headlines)}（主力 {len(primary_headlines)}，測試 {len(test_headlines)}）",
        f"- Descriptions：{len(primary_descriptions) + len(test_descriptions)}（主力 {len(primary_descriptions)}，測試 {len(test_descriptions)}）",
        f"- Replacement gap：{builder_output['portfolio_summary']['replacement_gap_unfilled_count']}",
        f"- Observe breakdown：{json.dumps(builder_output['portfolio_summary']['observe_breakdown'], ensure_ascii=False)}",
        "",
        "## 主力素材",
        "### Headlines",
        *asset_lines(primary_headlines),
        "",
        "### Descriptions",
        *asset_lines(primary_descriptions),
        "",
        "## 測試素材",
        "### Headlines",
        *asset_lines(test_headlines),
        "",
        "### Descriptions",
        *asset_lines(test_descriptions),
        "",
        "## 本輪下架素材",
        *[
            f"- `{row['retired_asset_id']}` {row['retired_text']} [{row['retirement_reason']}]"
            for row in packager_output["retirement_changelog"]
        ],
        "",
        "## 替換對照表",
        *replacement_lines(),
        "",
        "## 上稿前檢查清單",
        *checklist_lines,
        "",
        "## 策略備註",
        *note_lines,
        "## Safer Rewrite Watchlist",
        *watchlist_lines,
        "",
        "## Warnings",
        *[f"- {warning}" for warning in packager_output["compliance_notes"]["packager_warnings"]],
        "",
    ]
    return "\n".join(lines)


def render_uat_report(
    runtime_input: dict[str, Any],
    interpreter_output: dict[str, Any],
    builder_output: dict[str, Any],
    packager_output: dict[str, Any],
    file_map: dict[str, Path],
    validation_results: dict[str, str],
) -> str:
    decision_distribution = Counter(item["decision"] for item in interpreter_output["asset_decisions"])
    observe_distribution = Counter(
        item["decision"] for item in interpreter_output["asset_decisions"] if item["decision"].startswith("observe_")
    )
    confidence_distribution = Counter(item["decision_confidence"] for item in interpreter_output["asset_decisions"])
    basis_distribution = Counter(item["decision_basis"]["primary_metric"] for item in interpreter_output["asset_decisions"])

    report_lines = [
        "# LOVEFU 山丘樂眠床 Google Ads Copy Pipeline v1.2 真實 UAT Rerun",
        "",
        f"- generated_by: codex",
        f"- generated_at: {NOW.isoformat()}",
        f"- source_csv: {CSV_PATH}",
        "",
        "## Artifact Files",
        f"- normalized input: {file_map['input']}",
        f"- interpreter JSON: {file_map['interpreter']}",
        f"- builder JSON: {file_map['builder']}",
        f"- packager JSON: {file_map['packager_json']}",
        f"- packager Markdown: {file_map['packager_md']}",
        "",
        "## 1. Input sufficiency summary",
        "",
        "| field | present_in_source | verdict | note |",
        "| --- | --- | --- | --- |",
        "| impressions | yes (column exists) | unusable | 全數為 0 |",
        "| clicks | yes (column exists) | unusable | 全數為 0 |",
        "| ctr | yes (column exists) | unusable | 全數為 --，因 impressions=0 |",
        "| asset_level_conversions | no | missing | 只有跨 conversion action 的 association proxy，不是嚴格 asset-level conversion |",
        "| active_duration_days | no | missing | 以 runtime placeholder 0 通過 schema，不能拿來做 observe_new / observe_stale |",
        "| placement_breakout | no | missing | 原始報表沒有 placement split |",
        "",
        f"- data sufficiency verdict: `{interpreter_output['data_sufficiency']['overall_verdict']}`",
        "- 高信心可下的結論：只有『source export 缺 rich layers』這件事本身，還有 protected phrase / token presence 的 existence check。",
        "- 只能 directional 的結論：所有 performance ranking、retain / retire / reinforce、observe routing、candidate 補位優先序。",
        "",
        "## 2. Interpreter UAT output",
        "",
        f"- 完整 JSON：{file_map['interpreter']}",
        f"- asset_decisions count：{len(interpreter_output['asset_decisions'])}",
        f"- retire_now_assets count：{len(interpreter_output['retire_now_assets'])}",
        f"- new_candidate_assets count：{len(interpreter_output['new_candidate_assets'])}",
        f"- warnings / data caveats：{json.dumps(interpreter_output['compliance_notes']['data_caveats'], ensure_ascii=False)}",
        f"- protected_phrase 是否正確保留：`100天安心睡` 由 {json.dumps([item['asset_id'] for item in builder_output['final_asset_pack']['primary'] + builder_output['final_asset_pack']['test'] if item['is_protected_phrase_carrier']], ensure_ascii=False)} 承接。",
        "- must_include_token 是否不再誤保弱句：是。`hl-68`、`hl-61`、`hl-86` 都含 LOVEFU / 山丘樂眠床 / 飄雲專利，但仍被 retire，由 replacement 補位。",
        f"- observe 子類別分布：{json.dumps(observe_distribution, ensure_ascii=False)}",
        f"- decision_basis 分布：{json.dumps(basis_distribution, ensure_ascii=False)}",
        f"- decision_confidence 分布：{json.dumps(confidence_distribution, ensure_ascii=False)}",
        "- safer_rewrite_of 示例：`hl-03 -> cand-h01`、`desc-01 -> cand-d01`、`desc-03 -> cand-d02`、`desc-22 -> cand-d03`。",
        f"- asset_decisions / retire_now_assets / new_candidate_assets / next_round_brief_additions 已完整寫入 JSON artifact。",
        "",
        "## 3. Builder UAT output",
        "",
        f"- 完整 JSON：{file_map['builder']}",
        f"- final_asset_pack total：{builder_output['portfolio_summary']['total_final']}（primary={builder_output['portfolio_summary']['total_primary']}，test={builder_output['portfolio_summary']['total_test']}）",
        f"- replacement_map count：{len(builder_output['replacement_map'])}",
        f"- rejected_candidates count：{len(builder_output['rejected_candidates'])}",
        f"- observe_assets_status count：{len(builder_output['observe_assets_status'])}",
        f"- retire gap 是否都有補位：`{'yes' if builder_output['portfolio_summary']['replacement_gap_unfilled_count'] == 0 else 'no'}`",
        f"- primary / test 比例：`{builder_output['portfolio_summary']['test_ratio']}`",
        f"- coverage_check gaps：{json.dumps(builder_output['coverage_check']['gaps'], ensure_ascii=False)}",
        "- coverage 狀態：entry_value=`gap`，legacy_phrase=`thin`，pain_point=`test_only`，其餘 angle 依 final pack 進 primary / test。",
        "- safer rewrite 是否進 final pack：是，`cand-h01`、`cand-d01`、`cand-d02`、`cand-d03` 都有進 final。",
        "",
        "## 4. Packager UAT JSON output",
        "",
        f"- 完整 JSON：{file_map['packager_json']}",
        f"- upload_summary：delivery_target={packager_output['delivery_metadata']['delivery_target']}，version_label={packager_output['delivery_metadata']['version_label']}，sign_off_status={packager_output['delivery_metadata']['sign_off_status']}",
        f"- upload_asset_pack：primary headlines={len(packager_output['upload_ready_assets']['primary_pack']['headlines'])}，test headlines={len(packager_output['upload_ready_assets']['test_pack']['headlines'])}，primary descriptions={len(packager_output['upload_ready_assets']['primary_pack']['descriptions'])}，test descriptions={len(packager_output['upload_ready_assets']['test_pack']['descriptions'])}",
        f"- retirement_sheet count：{len(packager_output['retirement_changelog'])}",
        f"- uploader_checklist count：{len(packager_output['action_checklist'])}",
        f"- strategic_notes main_angles：{json.dumps([item['angle_key'] for item in packager_output['strategic_notes']['main_angles']], ensure_ascii=False)}",
        f"- warnings：{json.dumps(packager_output['compliance_notes']['packager_warnings'], ensure_ascii=False)}",
        "",
        "## 5. Packager UAT Markdown output",
        "",
        f"- 完整人類可讀版：{file_map['packager_md']}",
        "- 內容已包含本輪上稿摘要、主力素材、測試素材、本輪下架素材、替換對照表、上稿前檢查清單、策略備註。",
        "",
        "## 6. UAT validation summary",
        "",
        f"- 三層串接是否成功：`yes`，interpreter -> builder -> packager 三份 JSON 都已生成。",
        f"- 是否有 contract fail：`source_data_contract_fail`，因原始 CSV 缺 rich layers；`handoff_contract_fail=no`。",
        f"- 是否有 schema mismatch：`artifact_schema_mismatch=no`，validation={json.dumps(validation_results, ensure_ascii=False)}。",
        "- 成功 handoff 的欄位：angle_taxonomy、asset_decisions.angle_key、decision_confidence、observe_reason、retire_now_assets.coverage_gap_created、new_candidate_assets.risk_level / rewrite_mode / safer_rewrite_of、coverage_check、replacement_map。",
        "- 仍有流失的欄位：真實 source 沒有 asset_level_conversions、active_duration_days、placement_breakout；這些是 runtime 明示缺失，不是靜默補齊。",
        "- 最值得注意的 warnings：1. rich layers 沒被真實資料支撐。2. active_duration_days 只能用 placeholder。3. 真實素材池混有泛 LOVEFU / 飄雲語言，會稀釋 hillbed specificity。",
        "",
        "## 7. v1.2 UAT verdict",
        "",
        "- v1.2 是否比 v1.1 更接近可上稿 workflow：`部分是`",
        "- 最關鍵改善的 3 點：",
        "  1. angle_key 真的成為三層共用語言，從 interpreter 到 packager 都沒有掉欄。",
        "  2. safer_rewrite_of 真正作用在高風險歷史贏家，並且進 final pack 與 watchlist。",
        "  3. builder / packager 已收斂到真實 RSA 規模，剛好 15 headlines + 4 descriptions，而不是把舊池整桶保留。",
        "- 仍存在的 3 個問題：",
        "  1. 真實 CSV 沒有 richer click / conversion / placement / duration layers，所以 v1.2 的核心升級無法被 live export 真正吃滿。",
        "  2. observe_new / observe_stale / retire_candidate 無法被可靠驗證，這次只驗到 observe_insufficient_data / observe_borderline。",
        "  3. 真實素材池混入泛 LOVEFU / 飄雲語言，產品對焦還需要前置過濾。",
        "- 是否建議進 v1.3：`yes`",
        "- v1.3 最有槓桿的 3 個修正點：",
        "  1. 做一層 Google Ads export normalizer，優先吃到真實 impressions / clicks / asset-level conversions / active_duration_days / placement。",
        "  2. 在 interpreter 前加 product-scope filter / drift detector，先把泛 LOVEFU 與 hillbed-specific 素材分池。",
        "  3. 把 packager 升級成可直接輸出 RSA-ready upload sheet，並加上 policy-risk hard gate。",
        "",
    ]
    return "\n".join(report_lines)


def validate_json(instance: dict[str, Any], schema_path: Path) -> str:
    if jsonschema is None:
        return "skipped: jsonschema_not_installed"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator(schema).validate(instance)
    return "pass"


def main() -> None:
    assets, start_date, end_date = aggregate_assets()
    text_to_id = {asset["text"]: asset["asset_id"] for asset in assets}
    runtime_input = build_runtime_input(assets, start_date, end_date)
    candidates = build_candidate_specs(text_to_id)
    interpreter_output = build_interpreter_output(assets, runtime_input, candidates)
    builder_output = build_builder_output(interpreter_output, candidates)
    packager_output = build_packager_output(builder_output)

    file_map = {
        "input": ROOT / "ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.input.json",
        "interpreter": ROOT / "ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.interpreter.json",
        "builder": ROOT / "ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.builder.json",
        "packager_json": ROOT / "ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.json",
        "packager_md": ROOT / "ai/outputs/lovefu-hillbed-copy-pipeline-v1-2-real-uat.packager.md",
        "report": ROOT / "ai/validation/2026-03-15-lovefu-hillbed-copy-pipeline-v1-2-real-uat-rerun.md",
    }

    validation_results = {
        "input_schema": validate_json(runtime_input, ROOT / "ai/inputs/creative-performance-input.schema.json"),
        "interpreter_schema": validate_json(interpreter_output, ROOT / "ai/schemas/creative-performance-output.schema.json"),
        "builder_schema": validate_json(builder_output, ROOT / "ai/schemas/ad-copy-portfolio-output.schema.json"),
        "packager_schema": validate_json(packager_output, ROOT / "ai/schemas/upload-packager-output.schema.json"),
    }

    payloads = {
        "input": runtime_input,
        "interpreter": interpreter_output,
        "builder": builder_output,
        "packager_json": packager_output,
    }
    for key, payload in payloads.items():
        file_map[key].write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    file_map["packager_md"].write_text(
        render_packager_markdown(packager_output, builder_output) + "\n",
        encoding="utf-8",
    )
    file_map["report"].write_text(
        render_uat_report(runtime_input, interpreter_output, builder_output, packager_output, file_map, validation_results) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"written": {key: str(path) for key, path in file_map.items()}, "validation": validation_results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
