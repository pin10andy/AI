#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo


TZ = ZoneInfo("Asia/Taipei")
NOW = datetime.now(TZ).replace(microsecond=0)

PACK_GROUP_TO_ASSET_TYPE = {
    "short_headlines": "short_headline",
    "long_headlines": "long_headline",
    "headlines": "headline",
    "descriptions": "description",
}

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

DEFAULT_REQUIRED_TOKENS = [
    "山丘樂眠床",
    "LOVEFU",
    "飄雲專利",
]

DEFAULT_PROTECTED_PHRASES = [
    "100天安心睡",
]

HIGH_RISK_PATTERNS = [
    "不再背痛失眠",
    "腰椎不再酸痛",
    "專為腰痛患者設計",
    "幫助緩解腰痛",
    "告別腰痛困擾",
    "舒緩腰痛",
]

MEDIUM_RISK_PATTERNS = [
    "改善睡眠品質",
    "一覺到天明",
    "無壓睡感",
    "壓力少一點",
    "負擔少一點",
]

PRODUCT_SPECIFIC_PATTERNS = [
    "山丘",
    "山丘樂眠床",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def compact_text(text: str) -> str:
    return re.sub(r"\s+", "", text)


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value and value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def find_risk_patterns(text: str, patterns: list[str]) -> list[str]:
    return [pattern for pattern in patterns if pattern in text]


def classify_policy_risk(text: str) -> str:
    if find_risk_patterns(text, HIGH_RISK_PATTERNS):
        return "high"
    if find_risk_patterns(text, MEDIUM_RISK_PATTERNS):
        return "medium"
    return "low"


def infer_lane_context(source_path: Path) -> dict[str, Any] | None:
    parts = list(source_path.parts)
    if "google-ads" not in parts:
        return None
    index = parts.index("google-ads")
    if len(parts) <= index + 4:
        return None
    lane_id = parts[index + 3]
    lane_parts = lane_id.split("-")
    message_scope = lane_parts[0] if lane_parts else lane_id
    goal = lane_parts[1] if len(lane_parts) > 1 else ""
    return {
        "lane_id": lane_id,
        "message_scope": message_scope,
        "goal": goal,
        "platform": "google_ads",
    }


def build_char_index(packager_output: dict[str, Any]) -> dict[str, dict[str, Any]]:
    rows = packager_output.get("character_audit", {}).get("results", [])
    return {row["asset_id"]: row for row in rows}


def normalize_asset(
    asset: dict[str, Any],
    asset_type: str,
    bucket: str,
    char_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    char_row = char_index.get(asset["asset_id"], {})
    normalized = {
        "asset_id": asset["asset_id"],
        "text": asset["text"],
        "asset_type": char_row.get("asset_type", asset_type),
        "bucket": bucket,
        "source": asset.get("source", "unknown"),
        "angle_key": asset.get("angle_key", "unknown"),
        "decision_confidence": asset.get("decision_confidence", "directional"),
        "char_count": char_row.get("char_count", asset.get("char_count", len(asset["text"]))),
    }

    risk_level = asset.get("risk_level") or classify_policy_risk(asset["text"])
    if risk_level in {"low", "medium", "high"}:
        normalized["risk_level"] = risk_level

    if asset.get("rewrite_mode"):
        normalized["rewrite_mode"] = asset["rewrite_mode"]

    coverage_tags = asset.get("coverage_tags") or {}
    normalized_tags = {}
    for key in ("protected_phrases", "must_include_tokens", "reusable_motifs"):
        values = coverage_tags.get(key) or []
        if values:
            normalized_tags[key] = values
    if normalized_tags:
        normalized["coverage_tags"] = normalized_tags

    if asset.get("status_note"):
        normalized["notes"] = asset["status_note"]

    return normalized


def flatten_assets(packager_output: dict[str, Any]) -> list[dict[str, Any]]:
    char_index = build_char_index(packager_output)
    assets: list[dict[str, Any]] = []
    for pack_key, bucket in (("primary_pack", "primary"), ("test_pack", "test")):
        asset_groups = packager_output["upload_ready_assets"].get(pack_key, {})
        for group_name, grouped_assets in asset_groups.items():
            asset_type = PACK_GROUP_TO_ASSET_TYPE.get(group_name, "headline")
            for asset in grouped_assets:
                assets.append(normalize_asset(asset, asset_type, bucket, char_index))
    return assets


def collect_required_tokens(assets: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []
    compact_assets = [compact_text(asset["text"]) for asset in assets]
    for asset in assets:
        tags = asset.get("coverage_tags") or {}
        found.extend(tags.get("must_include_tokens") or [])
    for token in DEFAULT_REQUIRED_TOKENS:
        compact_token = compact_text(token)
        if any(compact_token in text for text in compact_assets):
            found.append(token)
    return dedupe(found)


def collect_protected_phrases(assets: list[dict[str, Any]]) -> list[str]:
    found: list[str] = []
    compact_assets = [compact_text(asset["text"]) for asset in assets]
    for asset in assets:
        tags = asset.get("coverage_tags") or {}
        found.extend(tags.get("protected_phrases") or [])
    for phrase in DEFAULT_PROTECTED_PHRASES:
        compact_phrase = compact_text(phrase)
        if any(compact_phrase in text for text in compact_assets):
            found.append(phrase)
    return dedupe(found)


def build_angle_status(
    packager_output: dict[str, Any],
    assets: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    counts = Counter(asset["angle_key"] for asset in assets)
    primary_counts = Counter(
        asset["angle_key"] for asset in assets if asset["bucket"] == "primary"
    )
    test_counts = Counter(
        asset["angle_key"] for asset in assets if asset["bucket"] == "test"
    )

    main_angles = {
        note["angle_key"] for note in packager_output["strategic_notes"]["main_angles"]
    }
    test_angles = {
        note["angle_key"] for note in packager_output["strategic_notes"]["test_angles"]
    }
    hold_angles = {
        note["angle_key"] for note in packager_output["strategic_notes"]["do_not_expand_angles"]
    }

    results: list[dict[str, Any]] = []
    for angle_key in packager_output["angle_taxonomy"]["keys"]:
        total = counts.get(angle_key, 0)
        primary_total = primary_counts.get(angle_key, 0)
        test_total = test_counts.get(angle_key, 0)

        if total == 0:
            status = "gap"
        elif angle_key in hold_angles and total >= 2:
            status = "overbuilt"
        elif angle_key in main_angles:
            status = "core"
        elif angle_key in test_angles and primary_total == 0 and test_total > 0:
            status = "test_only"
        elif angle_key in test_angles:
            status = "supporting"
        elif total == 1:
            status = "thin"
        else:
            status = "supporting"

        results.append(
            {
                "angle_key": angle_key,
                "label": ANGLE_LABELS.get(angle_key, angle_key),
                "status": status,
                "total_count": total,
            }
        )
    return results


def build_history_signals(packager_output: dict[str, Any]) -> dict[str, Any] | None:
    warnings = packager_output.get("redundancy_warnings") or []
    if not warnings:
        return None
    clusters = []
    for index, warning in enumerate(warnings, start=1):
        clusters.append(
            {
                "cluster_id": f"redundancy-cluster-{index}",
                "asset_ids": [warning["asset_a_id"], warning["asset_b_id"]],
                "reason": warning["similarity_reason"],
            }
        )
    return {
        "window_days": 0,
        "observed_fatigue_signals": [],
        "asset_reuse_clusters": clusters,
    }


def build_compliance_context(
    packager_output: dict[str, Any],
    assets: list[dict[str, Any]],
) -> dict[str, Any]:
    watch_terms: list[str] = []
    must_avoid: list[str] = []

    for asset in assets:
        watch_terms.extend(find_risk_patterns(asset["text"], HIGH_RISK_PATTERNS))
        watch_terms.extend(find_risk_patterns(asset["text"], MEDIUM_RISK_PATTERNS))

    for item in packager_output["strategic_notes"]["safer_rewrite_watchlist"]:
        source_text = item["source_text"]
        must_avoid.extend(find_risk_patterns(source_text, HIGH_RISK_PATTERNS))
        watch_terms.extend(find_risk_patterns(source_text, HIGH_RISK_PATTERNS))
        watch_terms.extend(find_risk_patterns(source_text, MEDIUM_RISK_PATTERNS))

    return {
        "policy_watch_terms": dedupe(watch_terms),
        "must_avoid": dedupe(must_avoid),
    }


def adapt_packager_output(
    packager_output: dict[str, Any],
    source_path: Path,
) -> dict[str, Any]:
    assets = flatten_assets(packager_output)
    lane_context = infer_lane_context(source_path)
    history_signals = build_history_signals(packager_output)
    adapted = {
        "audit_id": f"{packager_output['package_id']}-creative-audit",
        "brand_name": packager_output["brand_name"],
        "product_name": packager_output["product_name"],
        "campaign_type": packager_output["campaign_type"],
        "generated_from": "packager_sidecar",
        "data_source": {
            "type": "packager_output",
            "mode": "read_only",
            "provider": "local_file",
            "evidence_level": "pack_only",
            "notes": "Derived from upload-packager output only; no export-backed or live snapshot data attached.",
            "artifact_refs": [str(source_path)],
        },
        "creative_inventory": {
            "primary_assets": [asset for asset in assets if asset["bucket"] == "primary"],
            "test_assets": [asset for asset in assets if asset["bucket"] == "test"],
        },
        "coverage_context": {
            "required_tokens": collect_required_tokens(assets),
            "protected_phrases": collect_protected_phrases(assets),
            "angle_status": build_angle_status(packager_output, assets),
        },
        "delivery_context": {
            "sign_off_status": packager_output["delivery_metadata"]["sign_off_status"],
            "manual_review_required": packager_output["compliance_notes"]["manual_review_required"],
        },
        "compliance_context": build_compliance_context(packager_output, assets),
    }
    if lane_context:
        adapted["lane_context"] = lane_context
    if history_signals:
        adapted["history_signals"] = history_signals
    return adapted


def summarize_counts(audit_input: dict[str, Any]) -> dict[str, int]:
    assets = (
        audit_input["creative_inventory"]["primary_assets"]
        + audit_input["creative_inventory"]["test_assets"]
    )
    headlines = sum(
        1
        for asset in assets
        if asset["asset_type"] in {"headline", "short_headline", "long_headline"}
    )
    descriptions = sum(1 for asset in assets if asset["asset_type"] == "description")
    non_text = sum(
        1 for asset in assets if asset["asset_type"] in {"image", "video", "logo"}
    )
    return {
        "total": len(assets),
        "headlines": headlines,
        "descriptions": descriptions,
        "non_text": non_text,
    }


def current_policy_risk_assets(audit_input: dict[str, Any]) -> tuple[list[str], list[str]]:
    medium_assets: list[str] = []
    high_assets: list[str] = []
    assets = (
        audit_input["creative_inventory"]["primary_assets"]
        + audit_input["creative_inventory"]["test_assets"]
    )
    for asset in assets:
        text = asset["text"]
        if find_risk_patterns(text, HIGH_RISK_PATTERNS):
            high_assets.append(asset["asset_id"])
        elif find_risk_patterns(text, MEDIUM_RISK_PATTERNS):
            medium_assets.append(asset["asset_id"])
    return medium_assets, high_assets


def product_specificity_stats(audit_input: dict[str, Any]) -> tuple[int, int]:
    assets = (
        audit_input["creative_inventory"]["primary_assets"]
        + audit_input["creative_inventory"]["test_assets"]
    )
    product_specific = 0
    for asset in assets:
        if any(pattern in asset["text"] for pattern in PRODUCT_SPECIFIC_PATTERNS):
            product_specific += 1
    return product_specific, len(assets)


def dimension_entry(score: int, verdict: str, rationale: str) -> dict[str, Any]:
    return {
        "score": score,
        "verdict": verdict,
        "rationale": rationale,
    }


def build_audit_output(
    packager_output: dict[str, Any],
    audit_input: dict[str, Any],
) -> dict[str, Any]:
    campaign_type = audit_input["campaign_type"]
    lane_context = audit_input.get("lane_context") or {}
    lane_id = lane_context.get("lane_id", "")
    counts = summarize_counts(audit_input)
    angle_status = audit_input["coverage_context"]["angle_status"]
    unique_angles = [item for item in angle_status if item["total_count"] > 0]
    gap_angles = [item for item in angle_status if item["status"] == "gap"]
    redundancy_count = len(packager_output.get("redundancy_warnings") or [])
    product_specific_count, total_assets = product_specificity_stats(audit_input)
    product_ratio = product_specific_count / total_assets if total_assets else 0.0
    medium_assets, high_assets = current_policy_risk_assets(audit_input)
    all_char_pass = packager_output["character_audit"]["all_pass"]

    if campaign_type == "search_rsa":
        primary_assets = audit_input["creative_inventory"]["primary_assets"]
        test_assets = audit_input["creative_inventory"]["test_assets"]
        if (
            counts["headlines"] >= 15
            and counts["descriptions"] >= 4
            and primary_assets
            and test_assets
        ):
            sufficiency_score = 5
            sufficiency_verdict = "pass"
            sufficiency_rationale = (
                "headline / description 數量達到 RSA 常用水位，且 primary / test 兩個 bucket 都存在。"
            )
        elif counts["headlines"] >= 12 and counts["descriptions"] >= 3:
            sufficiency_score = 3
            sufficiency_verdict = "warn"
            sufficiency_rationale = (
                "RSA headline / description 接近可用，但測試容量仍偏緊。"
            )
        else:
            sufficiency_score = 1
            sufficiency_verdict = "fail"
            sufficiency_rationale = (
                "RSA headline 或 description 明顯不足，會直接限制素材組合與學習。"
            )
    else:
        if counts["headlines"] >= 15 and counts["descriptions"] >= 4:
            sufficiency_score = 4 if counts["non_text"] == 0 else 5
            sufficiency_verdict = "warn" if counts["non_text"] == 0 else "pass"
            sufficiency_rationale = (
                "文字 headline / description 數量達到 PMax 常用下限，但目前只驗證文字素材，未驗證 image / video / logo completeness。"
                if counts["non_text"] == 0
                else "文字與非文字素材都已達可審核水位。"
            )
        elif counts["headlines"] >= 12 and counts["descriptions"] >= 3:
            sufficiency_score = 3
            sufficiency_verdict = "warn"
            sufficiency_rationale = "文字素材接近可用，但 headline 或 description 數量仍偏緊。"
        else:
            sufficiency_score = 1
            sufficiency_verdict = "fail"
            sufficiency_rationale = "文字素材數量不足，會直接限制 PMax 測試與 serving。"

    if len(unique_angles) >= 8 and redundancy_count <= 2:
        diversity_score = 4
        diversity_verdict = "warn" if redundancy_count else "pass"
        diversity_rationale = (
            f"目前覆蓋 {len(unique_angles)}/10 個 angle，只有 {redundancy_count} 組近義重複警示，整體多樣性可用但仍需控制相近變體。"
        )
    elif len(unique_angles) >= 6:
        diversity_score = 3
        diversity_verdict = "warn"
        diversity_rationale = "angle coverage 勉強可用，但重複語意或角度偏斜仍明顯。"
    else:
        diversity_score = 1
        diversity_verdict = "fail"
        diversity_rationale = "angle coverage 過窄，主力與測試素材難以形成有效對照。"

    if product_ratio >= 0.7:
        product_score = 5
        product_verdict = "pass"
        product_rationale = "大多數素材已清楚對焦山丘樂眠床。"
    elif product_ratio >= 0.45:
        product_score = 3
        product_verdict = "warn"
        product_rationale = (
            f"共有 {product_specific_count}/{total_assets} 則素材明確提到山丘，仍有一批 generic LOVEFU / 飄雲語言稀釋 hillbed 焦點。"
        )
    else:
        product_score = 2
        product_verdict = "fail"
        product_rationale = "產品聚焦仍偏弱，generic brand copy 比例過高。"

    if high_assets:
        policy_score = 1
        policy_verdict = "fail"
        policy_rationale = "高風險結果承諾仍存在於目前素材池。"
    elif medium_assets:
        policy_score = 3
        policy_verdict = "warn"
        policy_rationale = (
            f"高風險醫療式語句已被 safer rewrite 移除，但目前仍有 {len(medium_assets)} 則素材保留睡眠結果或舒壓效果語氣。"
        )
    else:
        policy_score = 4
        policy_verdict = "pass"
        policy_rationale = "目前未見明確高風險句，僅需一般人工審核。"

    if campaign_type == "search_rsa":
        if all_char_pass and counts["headlines"] >= 15 and counts["descriptions"] >= 4:
            platform_score = 4
            platform_verdict = "warn" if lane_id.endswith("pmax") else "pass"
            platform_rationale = (
                "RSA headline / description 已通過 char audit，且數量可上稿；但目前 artifact path 與 payload campaign_type 不一致，需先清掉流程漂移。"
                if lane_id.endswith("pmax")
                else "RSA headline / description 已通過 char audit，且數量可上稿。"
            )
        elif all_char_pass:
            platform_score = 3
            platform_verdict = "warn"
            platform_rationale = "char audit 通過，但素材總量仍偏緊。"
        else:
            platform_score = 2
            platform_verdict = "fail"
            platform_rationale = "部分素材未通過 char audit，會影響實際上稿。"
    else:
        if all_char_pass and counts["headlines"] >= 15 and counts["descriptions"] >= 4:
            platform_score = 3 if counts["non_text"] == 0 else 4
            platform_verdict = "warn" if counts["non_text"] == 0 else "pass"
            platform_rationale = (
                "文字素材已通過 char audit，但這份 evidence 不包含 PMax 非文字素材，因此平台適配只可做中低信心判斷。"
                if counts["non_text"] == 0
                else "char audit 通過，且資產型別完整。"
            )
        elif all_char_pass:
            platform_score = 3
            platform_verdict = "warn"
            platform_rationale = "char audit 通過，但素材總量或型別仍不足。"
        else:
            platform_score = 2
            platform_verdict = "fail"
            platform_rationale = "部分素材未通過 char audit，會影響實際上稿。"

    dimension_scores = {
        "asset_sufficiency": dimension_entry(
            sufficiency_score, sufficiency_verdict, sufficiency_rationale
        ),
        "creative_diversity": dimension_entry(
            diversity_score, diversity_verdict, diversity_rationale
        ),
        "product_specificity": dimension_entry(
            product_score, product_verdict, product_rationale
        ),
        "policy_risk": dimension_entry(policy_score, policy_verdict, policy_rationale),
        "platform_fit": dimension_entry(
            platform_score, platform_verdict, platform_rationale
        ),
    }

    findings: list[dict[str, Any]] = []
    generic_assets = [
        asset["asset_id"]
        for asset in (
            audit_input["creative_inventory"]["primary_assets"]
            + audit_input["creative_inventory"]["test_assets"]
        )
        if not any(pattern in asset["text"] for pattern in PRODUCT_SPECIFIC_PATTERNS)
    ]
    if product_ratio < 0.6:
        findings.append(
            {
                "finding_id": "finding-product-drift",
                "severity": "high",
                "category": "product_drift",
                "title": "Generic LOVEFU / 飄雲 language still dilutes hillbed focus",
                "summary": "目前 final pack 雖已補進 hillbed-specific candidate，但 generic 品牌與系列語言仍佔顯著比例。",
                "evidence": [
                    f"只有 {product_specific_count}/{total_assets} 則素材明確提到山丘或山丘樂眠床。",
                    "packager strategic notes 已將 brand_trust 列為 do_not_expand，代表 generic trust copy 已接近過量。",
                ],
                "blocking": False,
                "affected_assets": generic_assets[:8],
            }
        )

    if gap_angles:
        findings.append(
            {
                "finding_id": "finding-angle-gap",
                "severity": "medium",
                "category": "coverage_gap",
                "title": "Angle coverage still has an unfilled gap",
                "summary": "目前 angle taxonomy 仍未完全覆蓋，代表 builder / packager 的最終 pack 仍有策略空洞。",
                "evidence": [
                    "gap angles: " + ", ".join(item["angle_key"] for item in gap_angles),
                    "packager warnings 已明示本輪 final pack 未承接 entry_value angle。",
                ],
                "blocking": False,
                "affected_assets": [],
            }
        )

    if medium_assets or high_assets:
        findings.append(
            {
                "finding_id": "finding-policy-watch",
                "severity": "medium" if not high_assets else "blocker",
                "category": "policy_risk",
                "title": "Policy-sensitive outcome language still needs manual QA",
                "summary": "高風險醫療式舊句已被替換，但目前 pack 仍保留需要人工把關的效果語氣。",
                "evidence": [
                    "current medium-risk assets: " + ", ".join(medium_assets) if medium_assets else "current high-risk assets: " + ", ".join(high_assets),
                    "safer rewrite watchlist 已證明此 lane 對結果承諾敏感，不能只因 schema pass 就放行。",
                ],
                "blocking": bool(high_assets),
                "affected_assets": high_assets or medium_assets,
            }
        )

    if counts["non_text"] == 0 and campaign_type == "pmax":
        findings.append(
            {
                "finding_id": "finding-pmax-nontext",
                "severity": "medium",
                "category": "platform_fit",
                "title": "PMax non-text completeness is not verified by current evidence",
                "summary": "這份 preflight 只能確認文字 pack，還不能確認 image / video / logo 是否足以支撐實際 PMax serving。",
                "evidence": [
                    "character_audit.all_pass=true，但 upload_ready_assets 僅包含 headlines / descriptions。",
                    "creative-auditor input evidence_level=pack_only，platform-fit 只可做低至中信心判斷。",
                ],
                "blocking": False,
                "affected_assets": [],
            }
        )

    if lane_id.endswith("pmax") and campaign_type != "pmax":
        findings.append(
            {
                "finding_id": "finding-path-payload-drift",
                "severity": "medium",
                "category": "platform_fit",
                "title": "Artifact path and payload campaign_type are inconsistent",
                "summary": "同一份 packager artifact 的 storage lane 與 payload campaign_type 不一致，代表 workflow metadata 還有漂移。",
                "evidence": [
                    f"lane_context.lane_id={lane_id}",
                    f"payload campaign_type={campaign_type}",
                ],
                "blocking": False,
                "affected_assets": [],
            }
        )

    if any(finding["blocking"] for finding in findings):
        upload_status = "blocked_for_upload"
        rationale = "目前仍有 blocker 級問題，不應直接進入 ready_to_upload。"
    elif audit_input["delivery_context"]["manual_review_required"] or packager_output["delivery_metadata"]["sign_off_status"] != "ready_to_upload":
        upload_status = "needs_manual_review"
        if campaign_type == "search_rsa":
            rationale = (
                "RSA 素材量已達可審核水位，但 evidence 仍是 pack_only，且產品聚焦、angle gap、政策語氣與 path/payload drift 仍需人工確認。"
            )
        else:
            rationale = (
                "文字素材已達可審核水位，但 evidence 仍是 pack_only，且產品聚焦、angle gap、PMax 非文字 completeness 仍需人工確認。"
            )
    else:
        upload_status = "clear_to_review"
        rationale = "未發現 blocker，且整體 creative health 可進入人工審核。"

    overall = round(
        (
            sufficiency_score
            + diversity_score
            + product_score
            + policy_score
            + platform_score
        )
        / 5
        * 20
    )
    if overall >= 85:
        grade = "A"
    elif overall >= 70:
        grade = "B"
    elif overall >= 55:
        grade = "C"
    elif overall >= 40:
        grade = "D"
    else:
        grade = "F"

    recommended_actions = [
        {
            "priority": "P1",
            "owner": "copy_runner",
            "action": "Replace 1-2 generic LOVEFU / 飄雲 lines with hillbed-specific support or pain-relief framing that stays policy-safe.",
            "reason": "目前 generic 語言仍佔顯著比例，會稀釋 hillbed product focus。",
        },
        {
            "priority": "P1",
            "owner": "human_reviewer",
            "action": "Manually QA `hl-06` and `desc-02` for sleep-outcome wording before changing sign_off_status.",
            "reason": "目前仍保留中度敏感的結果語氣，不能只依賴 safer rewrite watchlist 就放行。",
        },
        {
            "priority": "P1",
            "owner": "pm",
            "action": "Decide whether `entry_value` should be intentionally absent or explicitly reintroduced as a low-risk test angle.",
            "reason": "目前 taxonomy gap 還在，會影響後續 builder / packager 的 coverage discipline。",
        },
        {
            "priority": "P2",
            "owner": "copy_runner",
            "action": "Resolve the path / payload campaign_type drift before promoting this audit handoff into a formal gate.",
            "reason": "目前 artifact 被放在 pmax lane，但 payload 是 search_rsa，會讓 downstream review 誤判格式要求。",
        },
    ]

    source_notes = [
        "Input is derived from upload-packager output only; no export-backed click, impression, placement, or duration layers are attached.",
        "Fatigue and platform-fit remain directional because evidence_level is pack_only.",
        (
            "This audit uses text assets only; serving behavior still needs live or export-backed evidence."
            if campaign_type == "search_rsa"
            else "This audit only verifies text assets for a PMax lane; image, video, and logo completeness are not verified here."
        ),
    ]
    if lane_id.endswith("pmax") and campaign_type != "pmax":
        source_notes.append(
            f"Artifact path suggests `{lane_id}` while payload declares `{campaign_type}`; payload is treated as the authoritative contract."
        )
    source_notes.extend(packager_output["compliance_notes"].get("inherited_caveats", [])[:2])

    return {
        "audit_id": audit_input["audit_id"],
        "brand_name": audit_input["brand_name"],
        "product_name": audit_input["product_name"],
        "campaign_type": audit_input["campaign_type"],
        "generated_by": "codex",
        "generated_at": NOW.isoformat(),
        "source_data_assessment": {
            "evidence_level": audit_input["data_source"]["evidence_level"],
            "fatigue_confidence": "low",
            "platform_fit_confidence": "low" if counts["non_text"] == 0 else "medium",
            "notes": dedupe(source_notes),
        },
        "health_score": {
            "overall": overall,
            "grade": grade,
        },
        "dimension_scores": dimension_scores,
        "findings": findings,
        "upload_decision": {
            "status": upload_status,
            "rationale": rationale,
        },
        "recommended_actions": recommended_actions,
        "integration_handoff": {
            "packager_blockers": [
                finding["summary"] for finding in findings if finding["blocking"]
            ],
            "upstream_constraints": [
                "Introduce a hillbed-specificity floor or generic-brand ratio cap before final pack assembly.",
                "Carry accepted angle gaps as explicit metadata instead of leaving them as silent omissions.",
                "Promote policy watch terms from safer rewrite watchlist into a structured packager handoff field.",
            ],
            "challenger_notes": [
                "Packager already improved safer rewrite discipline; the remaining issue is product focus, not raw policy triage.",
                "Because this run is pack-only, fatigue conclusions should not be upgraded beyond directional.",
                "Use this audit as a preflight gate before PM / media buyer sign-off, not as a replacement for packager output.",
            ],
        },
        "limitations": [
            "No live or export-backed delivery data was available for fatigue analysis.",
            (
                "No image / video / logo assets were present in the current evidence bundle."
                if campaign_type == "pmax"
                else "This sample still does not validate live serving behavior or real post-upload delivery splits."
            ),
            (
                f"Artifact path uses lane `{lane_id}` while payload campaign_type is `{campaign_type}`."
                if lane_id.endswith("pmax") and campaign_type != "pmax"
                else "No path / payload contract drift was observed in the source artifact."
            ),
            "This sample audit is derived from the 2026-03-15 v1.2 UAT packager artifact only.",
        ],
    }


def render_report(audit_output: dict[str, Any]) -> str:
    lines = [
        "# Google Ads Creative Audit Report",
        "",
        f"- audit_id: {audit_output['audit_id']}",
        f"- generated_by: {audit_output['generated_by']}",
        f"- generated_at: {audit_output['generated_at']}",
        "",
        "## Executive Summary",
        "",
        f"- Evidence level: `{audit_output['source_data_assessment']['evidence_level']}`",
        f"- Health score: **{audit_output['health_score']['overall']} / 100 ({audit_output['health_score']['grade']})**",
        f"- Upload decision: **{audit_output['upload_decision']['status']}**",
        f"- Verdict: {audit_output['upload_decision']['rationale']}",
        "",
        "## Source Data Assessment",
        "",
        f"- Fatigue confidence: `{audit_output['source_data_assessment']['fatigue_confidence']}`",
        f"- Platform-fit confidence: `{audit_output['source_data_assessment']['platform_fit_confidence']}`",
        "- Notes:",
    ]
    for note in audit_output["source_data_assessment"]["notes"]:
        lines.append(f"  - {note}")

    lines.extend(
        [
            "",
            "## Dimension Scores",
            "",
            "| Dimension | Score | Verdict | Rationale |",
            "|---|---:|---|---|",
        ]
    )
    for label, key in (
        ("Asset Sufficiency", "asset_sufficiency"),
        ("Creative Diversity", "creative_diversity"),
        ("Product Specificity", "product_specificity"),
        ("Policy Risk", "policy_risk"),
        ("Platform Fit", "platform_fit"),
    ):
        item = audit_output["dimension_scores"][key]
        lines.append(
            f"| {label} | {item['score']} | {item['verdict']} | {item['rationale']} |"
        )

    lines.extend(
        [
            "",
            "## Findings",
            "",
            "| Severity | Category | Title | Evidence | Affected Assets | Blocking |",
            "|---|---|---|---|---|---|",
        ]
    )
    for finding in audit_output["findings"]:
        evidence = "<br>".join(finding["evidence"])
        affected = ", ".join(finding["affected_assets"]) or "-"
        blocking = "yes" if finding["blocking"] else "no"
        lines.append(
            f"| {finding['severity']} | {finding['category']} | {finding['title']} | {evidence} | {affected} | {blocking} |"
        )

    lines.extend(["", "## Recommended Actions", ""])
    for action in audit_output["recommended_actions"]:
        lines.append(
            f"- `{action['priority']}` `{action['owner']}`: {action['action']} Reason: {action['reason']}"
        )

    lines.extend(["", "## Integration Handoff", "", "### Packager Blockers", ""])
    blockers = audit_output["integration_handoff"]["packager_blockers"] or ["none"]
    for blocker in blockers:
        lines.append(f"- {blocker}")

    lines.extend(["", "### Upstream Constraints", ""])
    for item in audit_output["integration_handoff"]["upstream_constraints"]:
        lines.append(f"- {item}")

    lines.extend(["", "### Challenger Notes", ""])
    for item in audit_output["integration_handoff"]["challenger_notes"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Limitations", ""])
    for item in audit_output["limitations"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Adapt upload-packager output into creative-auditor input or produce a deterministic sample audit."
    )
    parser.add_argument("packager_path", help="Path to upload-packager JSON output")
    parser.add_argument(
        "--mode",
        choices=("audit-input", "audit-output"),
        default="audit-output",
        help="Emit normalized creative-audit input or a deterministic sample audit output",
    )
    parser.add_argument(
        "--report-path",
        help="Optional markdown report path. Only used with --mode audit-output.",
    )
    args = parser.parse_args()

    packager_path = Path(args.packager_path)
    packager_output = load_json(packager_path)
    audit_input = adapt_packager_output(packager_output, packager_path)

    if args.mode == "audit-input":
        print(json.dumps(audit_input, ensure_ascii=False, indent=2))
        return

    audit_output = build_audit_output(packager_output, audit_input)
    if args.report_path:
        Path(args.report_path).write_text(render_report(audit_output))
    print(json.dumps(audit_output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
