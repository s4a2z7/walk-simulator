"""
Step 2 - EDA 리포트(시각화 포함) 자동 생성기

입력(out/):
- out/step2_quality_report.json
- out/step2_preprocess_summary.json
- out/eda_top_keywords.csv
- out/eda_length_hist.png
- out/eda_sentiment_distribution.png (있으면)
- out/eda_topic_distribution.png (있으면)

출력:
- out/step2_eda_report.md
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


OUT_DIR = Path("out")
QUALITY_JSON = OUT_DIR / "step2_quality_report.json"
PRE_SUMMARY_JSON = OUT_DIR / "step2_preprocess_summary.json"
TOP_KEYWORDS_CSV = OUT_DIR / "eda_top_keywords.csv"
REPORT_MD = OUT_DIR / "step2_eda_report.md"
STYLE_COMPARE_JSON = OUT_DIR / "source_type_balance_comparison.json"


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _exists(name: str) -> bool:
    return (OUT_DIR / name).exists()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    quality = _read_json(QUALITY_JSON) if QUALITY_JSON.exists() else {}
    pre = _read_json(PRE_SUMMARY_JSON) if PRE_SUMMARY_JSON.exists() else {}
    top = pd.read_csv(TOP_KEYWORDS_CSV) if TOP_KEYWORDS_CSV.exists() else pd.DataFrame(columns=["token", "count"])

    raw = quality.get("raw", {})
    raw_rows = raw.get("rows")
    missing_cols = raw.get("missing_required_cols", [])
    null_required = raw.get("rows_with_null_required")
    null_required_filled = raw.get("rows_with_null_required_after_fill")
    filled_text_from_raw_text = raw.get("filled_text_from_raw_text")
    generated_text_id = raw.get("generated_text_id")
    pii = raw.get("pii", {}) or {}

    provider_dist = raw.get("provider_type_distribution", {}) or {}
    source_dist = raw.get("source_type_distribution", {}) or {}

    pre_before = (pre.get("before") or {}) if isinstance(pre, dict) else {}
    pre_after = (pre.get("after") or {}) if isinstance(pre, dict) else {}
    pre_label_autofill = (pre.get("label_autofill") or {}) if isinstance(pre, dict) else {}
    style_compare = _read_json(STYLE_COMPARE_JSON) if STYLE_COMPARE_JSON.exists() else None

    # Top 10 키워드 표
    top10 = top.head(10).fillna("")
    top10_rows = []
    for i, r in enumerate(top10.itertuples(index=False), start=1):
        tok = getattr(r, "token", "")
        cnt = getattr(r, "count", "")
        top10_rows.append(f"| {i} | {tok} | {cnt} |")

    lines: list[str] = []
    lines.append("# Step 2 — 탐색적 데이터 분석(EDA) 리포트")
    lines.append("")
    lines.append("## 데이터 개요 및 품질 요약")
    lines.append(f"- **Raw rows**: {raw_rows}")
    lines.append(f"- **필수 컬럼 누락**: {len(missing_cols)} ({', '.join(missing_cols) if missing_cols else '없음'})")
    lines.append(f"- **필수 컬럼 결측/공백 행(원본 기준)**: {null_required}")
    if null_required_filled is not None:
        lines.append(f"- **필수 컬럼 결측/공백 행(text/raw_text 보정 후)**: {null_required_filled}")
    if filled_text_from_raw_text is not None:
        lines.append(f"- **text 공백을 raw_text로 보정한 행 수**: {filled_text_from_raw_text}")
    if generated_text_id is not None:
        lines.append(f"- **text_id 결측을 생성으로 보정한 행 수**: {generated_text_id}")
    # 중복(원문 / dedup_key)도 요약에 노출(기준선 고정 점검용)
    dup_raw_text = (quality.get("raw") or {}).get("dup_raw_text")
    dedup_key_dups = (quality.get("raw") or {}).get("dedup_key_duplicates")
    if dup_raw_text is not None or dedup_key_dups is not None:
        lines.append(f"- **중복 후보(원문/dedup_key)**: {dup_raw_text}/{dedup_key_dups}")
    lines.append(f"- **PII(URL/EMAIL/PHONE)**: {pii.get('url', 0)}/{pii.get('email', 0)}/{pii.get('phone', 0)}")
    lines.append("")
    lines.append("### 분포")
    lines.append("- **도메인(provider_type)**")
    for k, v in provider_dist.items():
        lines.append(f"  - {k}: {v}")
    lines.append("- **source_type**")
    for k, v in source_dist.items():
        lines.append(f"  - {k}: {v}")
    lines.append("")
    lines.append("## 전처리 요약(전처리규정 v1)")
    lines.append(f"- **before rows**: {pre_before.get('rows')}")
    lines.append(f"- **after rows**: {pre_after.get('rows')}")
    if pre_after.get("dedup_removed") is not None:
        lines.append(f"- **dedup 제거 건수**: {pre_after.get('dedup_removed')}")
    if isinstance(pre_label_autofill, dict) and pre_label_autofill.get("enabled"):
        lines.append(f"- **(임시) 룰 기반 라벨 보완 적용**: {pre_label_autofill.get('enabled')}")
        lines.append(f"- **(임시) 라벨 보완 건수(sentiment/topic)**: {pre_label_autofill.get('filled_sentiment')}/{pre_label_autofill.get('filled_topic')}")
    lines.append(f"- **정규화 텍스트 길이(min/max)**: {pre_after.get('min_len')}/{pre_after.get('max_len')}")
    lines.append(f"- **평균 토큰 수**: {pre_after.get('avg_token_count')}")
    lines.append("")
    lines.append("## 1) 텍스트 길이 분포")
    if _exists("eda_length_hist.png"):
        lines.append("")
        lines.append("![텍스트 길이 분포](eda_length_hist.png)")
    else:
        lines.append("- (산출물 없음) `out/eda_length_hist.png`")
    lines.append("")
    lines.append("## 2) 빈도 키워드 분석")
    lines.append("")
    lines.append("### Top 10 키워드")
    lines.append("")
    lines.append("| 순위 | 키워드 | 빈도 |")
    lines.append("|---:|---|---:|")
    lines.extend(top10_rows if top10_rows else ["| 1 | (없음) | 0 |"])
    lines.append("")
    lines.append("## 3) 데이터 유형별 분포(시각화)")
    if _exists("eda_sentiment_distribution.png"):
        lines.append("")
        lines.append("### 3.1 sentiment_label 분포")
        lines.append("")
        lines.append("![감정 레이블 분포](eda_sentiment_distribution.png)")
    else:
        lines.append("- (산출물 없음) `out/eda_sentiment_distribution.png`")
    if _exists("eda_topic_distribution.png"):
        lines.append("")
        lines.append("### 3.2 topic_label 분포")
        lines.append("")
        lines.append("![주제 레이블 분포](eda_topic_distribution.png)")
    else:
        lines.append("- (산출물 없음) `out/eda_topic_distribution.png`")
    lines.append("")
    
    # 1000건 확장 리포트(현재 Raw가 확장 결과와 일치할 때만 표시)
    expansion_path = OUT_DIR / "step2_expansion_to_1000_comparison.json"
    if expansion_path.exists():
        expansion_data = json.loads(expansion_path.read_text(encoding="utf-8"))
        target_total = expansion_data.get("target_total", 1000)
        after_total = (expansion_data.get("after") or {}).get("total")
        # 현재 리포트의 Raw rows가 확장 결과(보통 1000)와 일치할 때만 섹션 표시
        is_current_expansion_run = (raw_rows == target_total) and (after_total == raw_rows)
    else:
        expansion_data = None
        is_current_expansion_run = False

    if is_current_expansion_run and expansion_data:
        lines.append("## 4) 데이터 1000건 확장 요약")
        lines.append("")
        target_dist = expansion_data.get("target_distribution", {})
        before_data = expansion_data.get("before", {})
        after_data = expansion_data.get("after", {})
        added_data = expansion_data.get("added", {})
        
        lines.append(f"- **목표 총 건수**: {target_total}건")
        dist_str = ", ".join([f"{k}={int(v*100)}%" for k, v in target_dist.items()])
        lines.append(f"- **목표 분배율**: {dist_str}")
        lines.append(f"- **확장 전**: {before_data.get('total', 0)}건")
        lines.append(f"- **확장 후**: {after_data.get('total', 0)}건")
        lines.append(f"- **추가 생성**: {added_data.get('total', 0)}건")
        lines.append("")
        
        # 전후 비교 테이블
        lines.append(f"### source_type 분포 비교 ({before_data.get('total', 0)}건 → {after_data.get('total', 0)}건)")
        lines.append("")
        lines.append("| source_type | 확장 전 | 확장 후 | 증가 |")
        lines.append("|---|---:|---:|---:|")
        before_counts = before_data.get("distribution", {})
        after_counts = after_data.get("distribution", {})
        all_types = sorted(set(before_counts.keys()) | set(after_counts.keys()))
        for st in all_types:
            b = before_counts.get(st, 0)
            a = after_counts.get(st, 0)
            diff = a - b
            lines.append(f"| {st} | {b} | {a} | +{diff} |")
        lines.append("")
    
    elif style_compare and ((style_compare.get("after") or {}).get("rows") == raw_rows):
        # 문체 편중 완화 리포트: 현재 Raw가 보강 후 데이터와 일치할 때만 표시
        lines.append("## 4) source_type 분포 보강(전/후 비교)")
        lines.append("")
        lines.append("아래는 문체 편중 완화를 위해 `inquiry/review` 보강을 수행한 경우에만 표시됩니다.")
        lines.append("")
        tgt = style_compare.get("target_min", {})
        before_sc = (style_compare.get("before") or {}).get("source_type_counts", {}) or {}
        after_sc = (style_compare.get("after") or {}).get("source_type_counts", {}) or {}
        added = style_compare.get("added", {}) or {}
        lines.append(f"- 목표(최소 비율): {tgt}")
        lines.append(f"- 추가 생성(계획): {added.get('planned')}, 실제 추가 rows: {added.get('actual_rows')}")
        lines.append("")
        lines.append("| source_type | before | after |")
        lines.append("|---|---:|---:|")
        keys = sorted(set(before_sc.keys()) | set(after_sc.keys()))
        for k in keys:
            lines.append(f"| {k} | {before_sc.get(k, 0)} | {after_sc.get(k, 0)} |")
        lines.append("")

    lines.append("## 5) 산출물 목록(out/)")
    lines.append("")
    lines.append("- `out/step2_quality_report.md`, `out/step2_quality_report.json`")
    lines.append("- `out/step2_preprocessed.csv`, `out/step2_preprocess_summary.json`")
    lines.append("- `out/eda_length_hist.png`, `out/eda_top_keywords.csv`")
    lines.append("- `out/eda_sentiment_distribution.png`, `out/eda_topic_distribution.png`")
    lines.append("")

    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("saved:")
    print(f"- {REPORT_MD}")


if __name__ == "__main__":
    main()


