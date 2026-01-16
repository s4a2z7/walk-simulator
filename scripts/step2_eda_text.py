"""
Step 2 - 텍스트 EDA 코드(예시)

입력: out/step2_preprocessed.csv (없으면 data/step2_raw_text_sample.csv로부터 간단 전처리 후 사용)
출력:
- out/eda_length_hist.png
- out/eda_top_keywords.csv
- out/eda_topic_distribution.png (topic_label이 있으면)
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import re
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


RAW_PATH = Path("data/step2_raw_text_sample.csv")
PRE_PATH = Path("out/step2_preprocessed.csv")
OUT_DIR = Path("out")


def ensure_preprocessed() -> pd.DataFrame:
    if PRE_PATH.exists():
        return pd.read_csv(PRE_PATH)
    # 전처리 파일이 없으면 최소 컬럼만으로 간단 처리
    df = pd.read_csv(RAW_PATH).dropna(subset=["text"])
    df["text_normalized"] = df["text"].astype(str).str.lower()
    df["text_len"] = df["text_normalized"].str.len()
    return df


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid")

    df = ensure_preprocessed()
    if "text_normalized" not in df.columns:
        df["text_normalized"] = df["text"].astype(str)

    # 1) 텍스트 길이 분포
    df["text_len"] = df["text_normalized"].astype(str).str.len()
    plt.figure(figsize=(8, 4))
    sns.histplot(df["text_len"], bins=20, kde=False)
    plt.title("Text Length Distribution")
    plt.xlabel("length")
    plt.ylabel("count")
    length_path = OUT_DIR / "eda_length_hist.png"
    plt.tight_layout()
    plt.savefig(length_path, dpi=160)
    plt.close()

    # 2) 빈도 키워드(공백 토큰 기준)
    tokens = []
    if "tokens" in df.columns:
        # tokens 컬럼이 문자열로 저장되었을 수 있음 -> 간단 파싱(대괄호/콤마 형태)
        for v in df["tokens"].astype(str).tolist():
            v = v.strip()
            if v.startswith("[") and v.endswith("]"):
                # 매우 단순한 파싱(데모용)
                v = v[1:-1].replace("'", "").replace('"', "")
                parts = [p.strip() for p in v.split(",") if p.strip()]
                tokens.extend(parts)
            else:
                tokens.extend([t for t in v.split() if t])
    else:
        for s in df["text_normalized"].astype(str).tolist():
            tokens.extend([t for t in s.split() if t])

    # 아주 짧은 토큰 제거 + 인코딩 깨짐/잡음 토큰 필터링
    # (정규화 규정상 허용 문자만 남는 게 이상적이지만, tokens 문자열 파싱 과정에서 노이즈가 섞일 수 있어 2차 방어)
    _re_ok = re.compile(r"^[0-9a-z가-힣<>/_-]{2,}$", flags=re.IGNORECASE)
    tokens = [t for t in tokens if _re_ok.match(t)]
    top = Counter(tokens).most_common(30)
    top_df = pd.DataFrame(top, columns=["token", "count"])
    top_path = OUT_DIR / "eda_top_keywords.csv"
    top_df.to_csv(top_path, index=False, encoding="utf-8")

    # 3) 데이터 유형별 분포(긍정/부정, 카테고리 등)
    if "sentiment_label" in df.columns:
        plt.figure(figsize=(6, 4))
        sns.countplot(data=df, x="sentiment_label", order=sorted(df["sentiment_label"].dropna().unique()))
        plt.title("Sentiment Label Distribution")
        plt.xlabel("sentiment_label")
        plt.ylabel("count")
        p = OUT_DIR / "eda_sentiment_distribution.png"
        plt.tight_layout()
        plt.savefig(p, dpi=160)
        plt.close()

    if "topic_label" in df.columns:
        plt.figure(figsize=(8, 4))
        order = df["topic_label"].value_counts().index.tolist()
        sns.countplot(data=df, x="topic_label", order=order)
        plt.title("Topic Label Distribution")
        plt.xlabel("topic_label")
        plt.ylabel("count")
        plt.xticks(rotation=30, ha="right")
        p = OUT_DIR / "eda_topic_distribution.png"
        plt.tight_layout()
        plt.savefig(p, dpi=160)
        plt.close()

    print("saved:")
    print(f"- {length_path}")
    print(f"- {top_path}")
    if (OUT_DIR / "eda_sentiment_distribution.png").exists():
        print("- out/eda_sentiment_distribution.png")
    if (OUT_DIR / "eda_topic_distribution.png").exists():
        print("- out/eda_topic_distribution.png")


if __name__ == "__main__":
    main()


