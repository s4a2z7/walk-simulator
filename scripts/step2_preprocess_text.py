"""
Step 2 - 텍스트 전처리 코드(예시)

입력(기본): data/step2_raw_text_sample.csv
출력:
- out/step2_preprocessed.csv  (정규화/필터링/토큰 컬럼 포함)
- out/step2_preprocess_summary.json (전후 통계)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import pandas as pd

from step2_label_standards import autofill_labels, is_missing


RAW_PATH = Path("data/step2_raw_text_sample.csv")
OUT_DIR = Path("out")
OUT_PATH = OUT_DIR / "step2_preprocessed.csv"
SUMMARY_PATH = OUT_DIR / "step2_preprocess_summary.json"

# ===== 전처리 규정(v1) — 필요 시 여기만 수정 =====
REQUIRED_COLS = ["text_id", "source_type", "provider_type", "provider_name", "text"]
MIN_TEXT_LEN = 8  # 정규화 후 최소 길이

MASK_URL = True
MASK_EMAIL = True
MASK_PHONE = True

DEDUP_ON = ["provider_type", "source_type", "text_normalized"]
# =============================================


_RE_URL = re.compile(r"(https?://\S+|www\.\S+)", flags=re.IGNORECASE)
_RE_EMAIL = re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b", flags=re.IGNORECASE)
# 매우 느슨한 전화/숫자열 패턴(연속 숫자 8자리 이상)
_RE_PHONE = re.compile(r"(?<!\d)\d{8,}(?!\d)")


def normalize_text(s: str) -> str:
    """
    텍스트 정규화(요구사항 반영):
    - 소문자 변환(영문)
    - 특수문자 제거(의미 보존을 위해 일부 기호는 공백으로 치환)
    - 다중 공백 축소
    """
    s = s.strip()
    s = s.lower()
    if MASK_URL:
        s = _RE_URL.sub("<URL>", s)
    if MASK_EMAIL:
        s = _RE_EMAIL.sub("<EMAIL>", s)
    if MASK_PHONE:
        s = _RE_PHONE.sub("<PHONE>", s)
    # 한글/영문/숫자/공백만 남기고 나머지는 공백으로 치환
    s = re.sub(r"[^0-9a-z가-힣\s<>/_-]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def simple_tokenize(s: str) -> list[str]:
    # 형태소 분석기 없이 데모용: 공백 토큰화
    if not s:
        return []
    return [tok for tok in s.split(" ") if tok]


def _is_blank_series(s: pd.Series) -> pd.Series:
    s2 = s.astype("string")
    return s2.isna() | (s2.str.strip() == "")


def _stable_text_id(row: pd.Series) -> str:
    """
    Raw에 text_id가 없는 케이스(확장 데이터의 일부)를 대비해,
    입력 값 기반으로 **결정론적** text_id를 생성한다.
    """
    base = "|".join(
        [
            str(row.get("provider_type", "")).strip(),
            str(row.get("source_type", "")).strip(),
            str(row.get("provider_name", "")).strip(),
            str(row.get("text", "")).strip(),
            str(row.get("dedup_key", "")).strip(),
        ]
    )
    h = hashlib.sha1(base.encode("utf-8")).hexdigest()[:12]
    return f"gen_{h}"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", default=str(RAW_PATH), help="input raw csv path")
    p.add_argument("--out_csv", default=str(OUT_PATH), help="output preprocessed csv path")
    p.add_argument("--out_summary", default=str(SUMMARY_PATH), help="output preprocess summary json path")
    p.add_argument("--autofill_labels", action="store_true", help="룰 기반으로 결측 라벨을 임시 보완하고 플래그 컬럼을 추가")
    args = p.parse_args()

    raw_path = Path(args.raw)
    out_csv = Path(args.out_csv)
    out_summary = Path(args.out_summary)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_summary.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path)

    # 0) text / raw_text 호환 처리:
    # - 확장 데이터의 일부는 text가 비어 있고 raw_text에만 값이 들어가 있음
    if "text" not in df.columns and "raw_text" in df.columns:
        df["text"] = df["raw_text"]
    elif "text" in df.columns and "raw_text" in df.columns:
        text_blank = _is_blank_series(df["text"])
        df.loc[text_blank, "text"] = df.loc[text_blank, "raw_text"]

    # 0-1) text_id 호환 처리: 비어 있으면 결정론적으로 생성
    if "text_id" not in df.columns:
        df["text_id"] = ""
    tid_blank = _is_blank_series(df["text_id"])
    if tid_blank.any():
        df.loc[tid_blank, "text_id"] = df.loc[tid_blank].apply(_stable_text_id, axis=1)

    # 0-2) (선택) 결측 라벨 임시 보완
    label_autofill = {"enabled": bool(args.autofill_labels)}
    if args.autofill_labels:
        result = autofill_labels(df, text_col="text")
        label_autofill.update(result)
        # 잔여 결측(보완 후)
        label_autofill["remaining_missing_sentiment"] = int(is_missing(df.get("sentiment_label", pd.Series([], dtype="string"))).sum()) if "sentiment_label" in df.columns else None
        label_autofill["remaining_missing_topic"] = int(is_missing(df.get("topic_label", pd.Series([], dtype="string"))).sum()) if "topic_label" in df.columns else None

    before = {
        "rows": int(len(df)),
        "null_or_blank_text": int(_is_blank_series(df["text"]).sum()) if "text" in df.columns else None,
        "null_or_blank_text_id": int(_is_blank_series(df["text_id"]).sum()) if "text_id" in df.columns else None,
        "dup_text": int(df["text"].astype(str).duplicated().sum()) if "text" in df.columns else None,
    }

    # 1) 결측치 제거(필수 컬럼 기준)
    for c in REQUIRED_COLS:
        if c not in df.columns:
            raise ValueError(f"missing required column: {c}")
    df = df.dropna(subset=REQUIRED_COLS)

    # 2) 불필요 데이터 필터링(너무 짧은 텍스트 제거)
    df["text"] = df["text"].astype(str)
    df = df[df["text"].str.len() >= 1].copy()

    # 3) 텍스트 정규화
    df["text_normalized"] = df["text"].map(normalize_text)

    # 4) 토큰화 및 형식 통일
    df["tokens"] = df["text_normalized"].map(simple_tokenize)
    df["token_count"] = df["tokens"].map(len)

    # 5) 길이 필터(정규화 후)
    df = df[df["text_normalized"].str.len() >= MIN_TEXT_LEN].copy()

    # 6) 중복 제거(정규화 텍스트 + 도메인/출처 기준)
    before_dedup_rows = int(len(df))
    df = df.drop_duplicates(subset=DEDUP_ON).copy()
    after_dedup_rows = int(len(df))
    dedup_removed = int(before_dedup_rows - after_dedup_rows)

    after = {
        "rows": int(len(df)),
        "min_len": int(df["text_normalized"].str.len().min()) if len(df) else 0,
        "max_len": int(df["text_normalized"].str.len().max()) if len(df) else 0,
        "avg_token_count": float(df["token_count"].mean()) if len(df) else 0.0,
        "dedup_removed": dedup_removed,
        "dedup_before_rows": before_dedup_rows,
        "dedup_after_rows": after_dedup_rows,
    }

    df.to_csv(out_csv, index=False, encoding="utf-8")
    out_summary.write_text(
        json.dumps(
            {
                "input": {"raw_path": str(raw_path).replace("\\", "/")},
                "before": before,
                "after": after,
                "label_autofill": label_autofill,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print("saved:")
    print(f"- {out_csv}")
    print(f"- {out_summary}")


if __name__ == "__main__":
    main()


