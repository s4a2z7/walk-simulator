"""
Raw 텍스트 샘플 생성기(선택)

목적:
- Step 2에서 Raw 100~500건을 빠르게 만들기 위한 보조 스크립트
- 실제 수집이 어려운 경우 데모/EDA/전처리 파이프라인 검증에 사용
"""

from __future__ import annotations

import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd


PROVIDERS = [
    ("HOSPITAL", "A내과(강남점)"),
    ("HOSPITAL", "B이비인후과(강남역점)"),
    ("HOSPITAL", "C의원(홍대점)"),
    ("PHARMACY", "A약국(강남점)"),
    ("PHARMACY", "B약국(홍대점)"),
    ("CHECKUP_CENTER", "A검진센터(강남점)"),
    ("CHECKUP_CENTER", "B검진센터(여의도점)"),
]

TOPICS = ["wait", "staff", "explain", "price", "clean", "process", "reservation", "policy", "prep", "location", "pickup"]
SENTIMENTS = ["positive", "neutral", "negative"]

TEMPLATES = [
    ("review", "positive", "staff", "직원들이 친절해서 좋았어요."),
    ("review", "negative", "wait", "대기 시간이 길어서 아쉬웠습니다."),
    ("review", "neutral", "process", "전체적으로 무난했어요."),
    ("inquiry", "neutral", "reservation", "예약 가능한 시간대가 있나요?"),
    ("inquiry", "neutral", "policy", "예약 변경/취소 규정을 알려주세요."),
    ("inquiry", "neutral", "prep", "방문 전에 준비물이 있나요?"),
]


def main() -> None:
    random.seed(42)
    n = 200
    start = date(2025, 12, 18)

    rows = []
    for i in range(1, n + 1):
        provider_type, provider_name = random.choice(PROVIDERS)
        source_type, sentiment, topic, text = random.choice(TEMPLATES)
        created_at = (start + timedelta(days=random.randint(0, 13))).isoformat()
        rating = random.choice([1, 2, 3, 4, 5]) if source_type == "review" else ""

        rows.append(
            {
                "text_id": f"T{i:04d}",
                "source_type": source_type,
                "provider_type": provider_type,
                "provider_name": provider_name,
                "created_at": created_at,
                "rating": rating,
                "sentiment_label": sentiment if source_type == "review" else "neutral",
                "topic_label": topic if topic in TOPICS else random.choice(TOPICS),
                "text": text,
            }
        )

    df = pd.DataFrame(rows)
    out = Path("data/generated_raw_text_sample.csv")
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"saved: {out} rows={len(df)}")


if __name__ == "__main__":
    main()


