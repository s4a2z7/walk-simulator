"""
Step 2 - 인코딩 깨짐(모지바케) 텍스트 정정 유틸

배경:
- 일부 레코드(text)에 "(異붽? ?뺣낫 ?쒓났)" 같은 깨진 문자열이 섞일 수 있음
- 전처리/EDA에서 잡음 토큰(예: "뺣낫", "쒓났")을 유발

기능:
- 지정 입력 CSV의 text 컬럼에서 알려진 모지바케 패턴을 제거/치환
- 출력 CSV로 저장(원본 보존)
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


# 알려진 깨짐 패턴(이번 프로젝트에서 관측된 형태)
_RE_BAD_PAREN = re.compile(r"\(\s*異붽\?\s*\?뺣낫\s*\?쒓났\s*\)")
_RE_BAD_TOKENS = re.compile(r"(異붽\?|\?뺣낫|\?쒓났)")


def clean_text(s: str) -> str:
    s = str(s)
    # 1) 괄호 덩어리 통째로 제거
    s = _RE_BAD_PAREN.sub("", s)
    # 2) 남아 있는 토큰 조각 제거
    s = _RE_BAD_TOKENS.sub("", s)
    # 3) 공백 정리
    s = re.sub(r"\s+", " ", s).strip()
    return s


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True, help="input csv path")
    p.add_argument("--out", dest="out_path", required=True, help="output csv path")
    args = p.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(in_path)
    if "text" not in df.columns:
        raise ValueError("missing column: text")

    before_bad = int(df["text"].astype(str).str.contains("異붽|뺣낫|쒓났", regex=True, na=False).sum())
    df["text"] = df["text"].map(clean_text)
    after_bad = int(df["text"].astype(str).str.contains("異붽|뺣낫|쒓났", regex=True, na=False).sum())

    df.to_csv(out_path, index=False, encoding="utf-8")

    print("saved:")
    print(f"- {out_path}")
    print(f"bad_rows: {before_bad} -> {after_bad}")


if __name__ == "__main__":
    main()


