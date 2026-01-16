"""
Step 2 - 초기 샘플/수집 데이터 품질 체크

입력(기본): data/step2_raw_text_sample.csv
출력:
- out/step2_quality_report.json
- out/step2_quality_report.md

체크 항목(전처리규정_v1.md 기반):
- 필수 컬럼 존재/결측
- 중복(원문, dedup_key 기준)
- 텍스트 길이(원문/정규화 후), 너무 짧은 텍스트
- PII 패턴(URL/이메일/전화번호) 포함 여부(건수 + 샘플)
- provider_type/source_type 분포
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

from step2_label_standards import ALLOWED_SENTIMENT, ALLOWED_TOPIC, autofill_labels, is_missing

RAW_DEFAULT = Path("data/step2_raw_text_sample.csv")
PRE_DEFAULT = Path("out/step2_preprocessed.csv")
OUT_DIR = Path("out")
REPORT_JSON = OUT_DIR / "step2_quality_report.json"
REPORT_MD = OUT_DIR / "step2_quality_report.md"

REQUIRED_COLS = ["text_id", "source_type", "provider_type", "provider_name", "text"]
DEDUP_ON = ["provider_type", "source_type", "text_normalized"]
MIN_TEXT_LEN = 8

LABEL_TOP_N = 10

_RE_URL = re.compile(r"(https?://\S+|www\.\S+)", flags=re.IGNORECASE)
_RE_EMAIL = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", flags=re.IGNORECASE)
_RE_PHONE = re.compile(r"(?<!\d)\d{8,}(?!\d)")


def normalize_text(s: str) -> str:
    s = str(s).strip().lower()
    s = _RE_URL.sub("<URL>", s)
    s = _RE_EMAIL.sub("<EMAIL>", s)
    s = _RE_PHONE.sub("<PHONE>", s)
    s = re.sub(r"[^0-9a-z가-힣\s<>/_-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _is_blank_series(s: pd.Series) -> pd.Series:
    s2 = s.astype("string")
    return s2.isna() | (s2.str.strip() == "")


def _stable_text_id(row: pd.Series) -> str:
    base = "|".join(
        [
            str(row.get("provider_type", "")).strip(),
            str(row.get("source_type", "")).strip(),
            str(row.get("provider_name", "")).strip(),
            str(row.get("text_effective", "")).strip(),
            str(row.get("dedup_key", "")).strip(),
        ]
    )
    h = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
    return f"gen_{h}"


def _rows_with_null_or_blank_required(df: pd.DataFrame, required: list[str]) -> int | None:
    missing_required_cols = [c for c in required if c not in df.columns]
    if missing_required_cols:
        return None
    masks = []
    for c in required:
        masks.append(_is_blank_series(df[c]))
    any_bad = masks[0]
    for m in masks[1:]:
        any_bad = any_bad | m
    return int(any_bad.sum())


def _pii_counts(texts: pd.Series) -> dict:
    url_hits = texts.astype(str).str.contains(_RE_URL, regex=True, na=False)
    email_hits = texts.astype(str).str.contains(_RE_EMAIL, regex=True, na=False)
    phone_hits = texts.astype(str).str.contains(_RE_PHONE, regex=True, na=False)
    return {
        "url": int(url_hits.sum()),
        "email": int(email_hits.sum()),
        "phone": int(phone_hits.sum()),
    }


def _sample_ids(df: pd.DataFrame, mask: pd.Series, max_n: int = 10) -> list[str]:
    if "text_id" not in df.columns:
        return []
    return df.loc[mask, "text_id"].astype(str).head(max_n).tolist()


def _label_stats(df: pd.DataFrame, col: str, allowed: list[str]) -> dict:
    """
    결측률/허용값 위반/Top 분포를 계산한다.
    - 결측: NaN 또는 공백 문자열
    - 위반: allowed에 없는 값(대소문자 무시하여 비교)
    """
    if col not in df.columns:
        return {"exists": False}

    s = df[col]
    # 결측 정의: NaN 또는 공백
    s_str = s.astype("string")
    missing_mask = s_str.isna() | (s_str.str.strip() == "")
    missing_count = int(missing_mask.sum())
    total = int(len(df))

    # 허용값 위반
    allowed_set = {a.lower() for a in allowed}
    non_missing = s_str[~missing_mask].fillna("").str.strip()
    invalid_mask = ~non_missing.str.lower().isin(list(allowed_set))
    invalid_count = int(invalid_mask.sum())
    invalid_values = non_missing[invalid_mask].value_counts().head(LABEL_TOP_N).to_dict()

    # Top 분포(결측 제외)
    top_dist = non_missing.value_counts().head(LABEL_TOP_N).to_dict()

    return {
        "exists": True,
        "total": total,
        "missing_count": missing_count,
        "missing_rate": float(missing_count / total) if total else 0.0,
        "invalid_count": invalid_count,
        "invalid_top_values": invalid_values,
        "top_distribution": top_dist,
        "allowed_values": allowed,
    }


def _markdown_report(payload: dict) -> str:
    def jpath(*keys, default=None):
        cur = payload
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur

    lines = []
    lines.append("# Step 2 품질 체크 리포트")
    lines.append("")
    lines.append(f"- 입력: `{jpath('input', 'raw_path')}`")
    pre = jpath("input", "preprocessed_path")
    if pre:
        lines.append(f"- 전처리 파일(참고): `{pre}`")
    lines.append("")

    lines.append("## 요약")
    lines.append(f"- rows: **{jpath('raw', 'rows', default=0)}**")
    lines.append(f"- 필수 컬럼 누락: **{len(jpath('raw', 'missing_required_cols', default=[]))}**")
    lines.append(f"- 필수 컬럼 결측/공백 행(원본 기준): **{jpath('raw', 'rows_with_null_required', default=0)}**")
    filled = jpath("raw", "rows_with_null_required_after_fill")
    if filled is not None:
        lines.append(f"- 필수 컬럼 결측/공백 행(text/raw_text 보정 후): **{filled}**")
    lines.append(f"- (원문 text) 중복 후보: **{jpath('raw', 'dup_raw_text', default=0)}**")
    lines.append(f"- (dedup_key) 중복 후보: **{jpath('raw', 'dedup_key_duplicates', default=0)}**")
    lines.append(f"- PII(URL/EMAIL/PHONE) 포함: **{jpath('raw', 'pii', 'url', default=0)}/{jpath('raw', 'pii', 'email', default=0)}/{jpath('raw', 'pii', 'phone', default=0)}**")
    lines.append("")
    lines.append("중복 정의(참고):")
    lines.append("- **원문 중복**: `text` 컬럼이 완전히 동일한 경우(공백/기호 차이 포함)")
    lines.append("- **dedup_key 중복**: `provider_type + source_type + text_normalized`가 동일한 경우(정규화 후 의미 중복 후보)")
    lines.append("")

    lines.append("## 분포")
    pt = jpath("raw", "provider_type_distribution", default={}) or {}
    st = jpath("raw", "source_type_distribution", default={}) or {}
    lines.append("- 도메인(provider_type)")
    for k, v in pt.items():
        lines.append(f"  - {k}: {v}")
    lines.append("- source_type")
    for k, v in st.items():
        lines.append(f"  - {k}: {v}")
    lines.append("")

    # 라벨 품질
    label = jpath("raw", "label_quality", default={}) or {}
    if label:
        lines.append("## 라벨 품질")
        sent = label.get("sentiment_label", {})
        topic = label.get("topic_label", {})

        def _fmt_rate(v):
            try:
                return f"{float(v) * 100:.1f}%"
            except Exception:
                return "N/A"

        if sent.get("exists"):
            lines.append(f"- sentiment_label 결측률: **{_fmt_rate(sent.get('missing_rate'))}** (missing={sent.get('missing_count')}/{sent.get('total')})")
            lines.append(f"- sentiment_label 허용값 위반: **{sent.get('invalid_count')}**")
            if sent.get("top_distribution"):
                lines.append(f"- sentiment_label Top 분포(Top {LABEL_TOP_N}):")
                for k, v in list(sent["top_distribution"].items())[:LABEL_TOP_N]:
                    lines.append(f"  - {k}: {v}")
            if sent.get("invalid_top_values"):
                lines.append("- sentiment_label 위반 Top 값:")
                for k, v in list(sent["invalid_top_values"].items())[:LABEL_TOP_N]:
                    lines.append(f"  - {k}: {v}")
        else:
            lines.append("- sentiment_label: (컬럼 없음)")

        if topic.get("exists"):
            lines.append(f"- topic_label 결측률: **{_fmt_rate(topic.get('missing_rate'))}** (missing={topic.get('missing_count')}/{topic.get('total')})")
            lines.append(f"- topic_label 허용값 위반: **{topic.get('invalid_count')}**")
            if topic.get("top_distribution"):
                lines.append(f"- topic_label Top 분포(Top {LABEL_TOP_N}):")
                for k, v in list(topic["top_distribution"].items())[:LABEL_TOP_N]:
                    lines.append(f"  - {k}: {v}")
            if topic.get("invalid_top_values"):
                lines.append("- topic_label 위반 Top 값:")
                for k, v in list(topic["invalid_top_values"].items())[:LABEL_TOP_N]:
                    lines.append(f"  - {k}: {v}")
        else:
            lines.append("- topic_label: (컬럼 없음)")
        lines.append("")

    # (선택) 자동 라벨 보완 결과
    autofill = jpath("raw", "label_autofill", default=None)
    if isinstance(autofill, dict) and autofill.get("enabled"):
        lines.append("## (선택) 룰 기반 자동 라벨 보완(임시)")
        lines.append(f"- 적용 여부: **{autofill.get('enabled')}**")
        lines.append(f"- sentiment_label 보완 건수: **{autofill.get('filled_sentiment')}**")
        lines.append(f"- topic_label 보완 건수: **{autofill.get('filled_topic')}**")
        miss_after = autofill.get("missing_after")
        if isinstance(miss_after, dict):
            lines.append(f"- 보완 후 sentiment_label 결측률: **{miss_after.get('sentiment_missing_rate')}** (missing={miss_after.get('sentiment_missing_count')}/{miss_after.get('total')})")
            lines.append(f"- 보완 후 topic_label 결측률: **{miss_after.get('topic_missing_rate')}** (missing={miss_after.get('topic_missing_count')}/{miss_after.get('total')})")
        lines.append("")

    lines.append("## 권장 확인")
    lines.append("- 스크래핑 데이터는 `source_url`, `fetched_at` 컬럼 포함을 권장합니다.")
    lines.append("- PII 탐지된 경우, 전처리(`scripts/step2_preprocess_text.py`)로 마스킹 후 저장하세요.")
    lines.append("- 라벨 표준/허용값은 `라벨링가이드_v1.md`를 기준으로 관리합니다.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", default=str(RAW_DEFAULT), help="raw csv path")
    p.add_argument("--pre", default=str(PRE_DEFAULT), help="preprocessed csv path (optional)")
    p.add_argument("--out_json", default=str(REPORT_JSON), help="output json path")
    p.add_argument("--out_md", default=str(REPORT_MD), help="output md path")
    p.add_argument("--autofill_labels", action="store_true", help="룰 기반으로 결측 라벨을 임시 보완하고 보완 건수를 리포트에 명시")
    args = p.parse_args()

    raw_path = Path(args.raw)
    pre_path = Path(args.pre)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(raw_path)

    missing_required_cols = [c for c in REQUIRED_COLS if c not in df.columns]

    # 원본 기준 결측/공백(보수적으로 체크)
    rows_with_null_required = _rows_with_null_or_blank_required(df, REQUIRED_COLS)

    # text/raw_text 호환 보정 + text_id 생성(확장 데이터의 일부 호환)
    df_work = df.copy()
    filled_text_from_raw_text = 0
    generated_text_id = 0

    if "text" not in df_work.columns and "raw_text" in df_work.columns:
        df_work["text"] = df_work["raw_text"]

    if "text" in df_work.columns and "raw_text" in df_work.columns:
        text_blank = _is_blank_series(df_work["text"])
        raw_nonblank = ~_is_blank_series(df_work["raw_text"])
        fill_mask = text_blank & raw_nonblank
        if int(fill_mask.sum()):
            df_work.loc[fill_mask, "text"] = df_work.loc[fill_mask, "raw_text"]
            filled_text_from_raw_text = int(fill_mask.sum())

    if "text_id" not in df_work.columns:
        df_work["text_id"] = ""

    # text_effective: 후속 계산(중복/길이/PII)에서 사용
    df_work["text_effective"] = df_work["text"] if "text" in df_work.columns else ""
    tid_blank = _is_blank_series(df_work["text_id"])
    if int(tid_blank.sum()):
        df_work.loc[tid_blank, "text_id"] = df_work.loc[tid_blank].apply(_stable_text_id, axis=1)
        generated_text_id = int(tid_blank.sum())

    rows_with_null_required_after_fill = _rows_with_null_or_blank_required(df_work, REQUIRED_COLS)

    # 텍스트 기반 지표
    text_series = df_work["text_effective"] if "text_effective" in df_work.columns else pd.Series([], dtype=str)
    df_work["_text_normalized"] = text_series.astype(str).map(normalize_text) if len(text_series) else ""
    df_work["_len_raw"] = text_series.astype(str).str.len() if len(text_series) else 0
    df_work["_len_norm"] = df_work["_text_normalized"].astype(str).str.len() if len(text_series) else 0

    too_short_norm = int((df_work["_len_norm"] < MIN_TEXT_LEN).sum()) if len(df_work) else 0

    # 중복
    dup_raw_text = int(text_series.astype(str).duplicated().sum()) if len(text_series) else 0
    dedup_key_duplicates = None
    if len(df_work) and all(c in df_work.columns for c in ["provider_type", "source_type"]):
        dedup_key_duplicates = int(
            df_work[["provider_type", "source_type"]]
            .astype(str)
            .assign(text_normalized=df_work["_text_normalized"])
            .duplicated()
            .sum()
        )

    pii = _pii_counts(text_series) if len(text_series) else {"url": 0, "email": 0, "phone": 0}
    url_mask = text_series.astype(str).str.contains(_RE_URL, regex=True, na=False) if len(text_series) else pd.Series([], dtype=bool)
    email_mask = text_series.astype(str).str.contains(_RE_EMAIL, regex=True, na=False) if len(text_series) else pd.Series([], dtype=bool)
    phone_mask = text_series.astype(str).str.contains(_RE_PHONE, regex=True, na=False) if len(text_series) else pd.Series([], dtype=bool)

    provider_type_dist = df_work["provider_type"].astype(str).value_counts().to_dict() if "provider_type" in df_work.columns else {}
    source_type_dist = df_work["source_type"].astype(str).value_counts().to_dict() if "source_type" in df_work.columns else {}

    label_quality = {
        "sentiment_label": _label_stats(df_work, "sentiment_label", ALLOWED_SENTIMENT),
        "topic_label": _label_stats(df_work, "topic_label", ALLOWED_TOPIC),
    }

    label_autofill = {"enabled": bool(args.autofill_labels)}
    if args.autofill_labels:
        df_label = df_work.copy()
        res = autofill_labels(df_label, text_col="text_effective")
        label_autofill.update(res)
        # 보완 후 결측률(공백/NaN)
        total = int(len(df_label))
        sent_miss = int(is_missing(df_label["sentiment_label"]).sum()) if "sentiment_label" in df_label.columns else None
        topic_miss = int(is_missing(df_label["topic_label"]).sum()) if "topic_label" in df_label.columns else None
        label_autofill["missing_after"] = {
            "total": total,
            "sentiment_missing_count": sent_miss,
            "sentiment_missing_rate": (float(sent_miss / total) if total and sent_miss is not None else None),
            "topic_missing_count": topic_miss,
            "topic_missing_rate": (float(topic_miss / total) if total and topic_miss is not None else None),
        }
        label_autofill["label_quality_after_autofill"] = {
            "sentiment_label": _label_stats(df_label, "sentiment_label", ALLOWED_SENTIMENT),
            "topic_label": _label_stats(df_label, "topic_label", ALLOWED_TOPIC),
        }

    payload = {
        "input": {
            "raw_path": str(raw_path).replace("\\", "/"),
            "preprocessed_path": str(pre_path).replace("\\", "/") if pre_path.exists() else None,
        },
        "raw": {
            "rows": int(len(df_work)),
            "missing_required_cols": missing_required_cols,
            "rows_with_null_required": rows_with_null_required,
            "rows_with_null_required_after_fill": rows_with_null_required_after_fill,
            "filled_text_from_raw_text": filled_text_from_raw_text,
            "generated_text_id": generated_text_id,
            "dup_raw_text": dup_raw_text,
            "dedup_key_duplicates": dedup_key_duplicates,
            "too_short_after_normalize(<8)": too_short_norm,
            "text_len_raw": {
                "min": int(df_work["_len_raw"].min()) if len(df_work) else 0,
                "max": int(df_work["_len_raw"].max()) if len(df_work) else 0,
                "mean": float(df_work["_len_raw"].mean()) if len(df_work) else 0.0,
            },
            "text_len_normalized": {
                "min": int(df_work["_len_norm"].min()) if len(df_work) else 0,
                "max": int(df_work["_len_norm"].max()) if len(df_work) else 0,
                "mean": float(df_work["_len_norm"].mean()) if len(df_work) else 0.0,
            },
            "pii": {
                **pii,
                "sample_text_ids": {
                    "url": _sample_ids(df_work, url_mask),
                    "email": _sample_ids(df_work, email_mask),
                    "phone": _sample_ids(df_work, phone_mask),
                },
            },
            "label_quality": label_quality,
            "label_autofill": label_autofill,
            "provider_type_distribution": provider_type_dist,
            "source_type_distribution": source_type_dist,
        },
    }

    out_json = Path(args.out_json)
    out_md = Path(args.out_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_md.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_markdown_report(payload), encoding="utf-8")

    print("saved:")
    print(f"- {out_json}")
    print(f"- {out_md}")


if __name__ == "__main__":
    main()


