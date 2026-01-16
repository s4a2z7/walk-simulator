"""
Step 2 - Raw 텍스트 CSV 병합 유틸

목적:
- 웹 수집 결과(data/step2_web_text_raw.csv), 샘플(data/step2_raw_text_sample.csv),
  (선택) 외부 다운로드 데이터 등을 하나의 Raw CSV로 합쳐 전처리 파이프라인에 투입한다.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


DEFAULT_OUT = Path("data/step2_raw_text_combined.csv")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", default=str(DEFAULT_OUT), help="output csv path")
    p.add_argument(
        "inputs",
        nargs="+",
        help="input csv paths (예: data/step2_raw_text_sample.csv data/step2_web_text_raw.csv)",
    )
    args = p.parse_args()

    dfs = []
    for ip in args.inputs:
        path = Path(ip)
        df = pd.read_csv(path)
        df["__source_file"] = str(path).replace("\\", "/")
        dfs.append(df)

    out = pd.concat(dfs, ignore_index=True, sort=False)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(out_path, index=False, encoding="utf-8")

    print("saved:")
    print(f"- {out_path} rows={len(out)} files={len(dfs)}")


if __name__ == "__main__":
    main()


