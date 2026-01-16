"""
Step 2 - 룰 기반 자동 라벨링(임시 보완용)

목적:
- sentiment_label / topic_label 결측을 규칙 기반으로 임시 채운다.
- 결과를 별도 CSV로 저장하고, 어떤 값이 자동으로 채워졌는지 플래그를 남긴다.

주의:
- 정답 라벨을 보장하지 않음(품질 확보를 위해 샘플링 수동 검증 권장)
- 표준 허용값은 `라벨링가이드_v1.md` 기준
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from step2_label_standards import autofill_labels, is_missing

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", default="data/step2_raw_text_sample.csv", help="input csv path")
    p.add_argument("--out", dest="out_path", default="data/step2_raw_text_autolabeled.csv", help="output csv path")
    args = p.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(in_path)
    if "text" not in df.columns:
        raise ValueError("missing column: text")

    if "sentiment_label" not in df.columns:
        df["sentiment_label"] = ""
    if "topic_label" not in df.columns:
        df["topic_label"] = ""

    sent_missing = is_missing(df["sentiment_label"])
    topic_missing = is_missing(df["topic_label"])
    result = autofill_labels(df, text_col="text")

    df["autolabeled_at"] = datetime.now(timezone.utc).isoformat()
    df.to_csv(out_path, index=False, encoding="utf-8")

    print("saved:")
    print(f"- {out_path}")
    print(f"filled sentiment_label: {result['filled_sentiment']}")
    print(f"filled topic_label: {result['filled_topic']}")


if __name__ == "__main__":
    main()


