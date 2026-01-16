"""
Step2 라벨 표준(허용값) + 룰 기반 자동 라벨링(임시 보완)

- 표준 허용값 문서: docs/step2_label_standards.md
- 상세 가이드: 라벨링가이드_v1.md
"""

from __future__ import annotations

import re
from typing import Any

import pandas as pd


ALLOWED_SENTIMENT = ["positive", "neutral", "negative"]
ALLOWED_TOPIC = [
    "reservation",
    "policy",
    "location",
    "opening_hours",
    "prep",
    "pickup",
    "wait",
    "staff",
    "price",
    "explain",
    "process",
    "clean",
    "speed",
    "other",
]


POS_KW = re.compile(r"(친절|만족|좋|추천|빠르|쾌적|깔끔|도움)", re.IGNORECASE)
NEG_KW = re.compile(r"(불친절|불편|별로|나쁘|늦|지연|길었|아쉬|비싸|혼잡|문제)", re.IGNORECASE)

TOPIC_RULES: list[tuple[str, re.Pattern[str]]] = [
    ("reservation", re.compile(r"(예약|접수|시간대|당일\s*예약|예약하고|예약 가능)", re.IGNORECASE)),
    ("policy", re.compile(r"(변경|취소|수수료|규정|불이익|기한|환불)", re.IGNORECASE)),
    ("location", re.compile(r"(주소|위치|오시는|주차|교통|도보)", re.IGNORECASE)),
    ("opening_hours", re.compile(r"(영업|운영\s*시간|진료\s*시간|휴무|일요일|토요일|점심시간)", re.IGNORECASE)),
    ("prep", re.compile(r"(준비물|금식|전날|검진\s*전|신분증|복용\s*약|커피|물\s*마셔)", re.IGNORECASE)),
    ("pickup", re.compile(r"(조제|수령|처방|픽업|완료\s*알림|문자\s*알림)", re.IGNORECASE)),
    ("wait", re.compile(r"(대기|줄|혼잡|지연|기다)", re.IGNORECASE)),
    ("staff", re.compile(r"(직원|간호사|약사|응대|친절|불친절)", re.IGNORECASE)),
    ("price", re.compile(r"(가격|비용|보험|비급여|결제|수납)", re.IGNORECASE)),
    ("explain", re.compile(r"(설명|안내|상담|자세히|이해)", re.IGNORECASE)),
    ("process", re.compile(r"(절차|동선|접수-검진-수납|흐름|과정)", re.IGNORECASE)),
    ("clean", re.compile(r"(청결|깨끗|시설|위생|환경)", re.IGNORECASE)),
    ("speed", re.compile(r"(빠르|신속|금방|바로)", re.IGNORECASE)),
]


def is_missing(series: pd.Series) -> pd.Series:
    s = series.astype("string")
    return s.isna() | (s.str.strip() == "")


def infer_sentiment(text: Any) -> str:
    t = str(text)
    if NEG_KW.search(t):
        return "negative"
    if POS_KW.search(t):
        return "positive"
    return "neutral"


def infer_topic(text: Any) -> str:
    t = str(text)
    for label, rx in TOPIC_RULES:
        if rx.search(t):
            return label
    return "other"


def autofill_labels(
    df: pd.DataFrame,
    *,
    text_col: str = "text",
    sentiment_col: str = "sentiment_label",
    topic_col: str = "topic_label",
) -> dict:
    """
    결측/공백 라벨을 규칙 기반으로 채운다(임시).
    - 원본 df를 **in-place로 수정**한다.
    - 반환: 채운 건수 및 플래그 컬럼명
    """
    if text_col not in df.columns:
        raise ValueError(f"missing text column: {text_col}")

    if sentiment_col not in df.columns:
        df[sentiment_col] = ""
    if topic_col not in df.columns:
        df[topic_col] = ""

    sent_missing = is_missing(df[sentiment_col])
    topic_missing = is_missing(df[topic_col])

    df["sentiment_auto"] = False
    df["topic_auto"] = False

    if int(sent_missing.sum()):
        df.loc[sent_missing, sentiment_col] = df.loc[sent_missing, text_col].map(infer_sentiment)
        df.loc[sent_missing, "sentiment_auto"] = True

    if int(topic_missing.sum()):
        df.loc[topic_missing, topic_col] = df.loc[topic_missing, text_col].map(infer_topic)
        df.loc[topic_missing, "topic_auto"] = True

    return {
        "filled_sentiment": int(sent_missing.sum()),
        "filled_topic": int(topic_missing.sum()),
        "sentiment_flag_col": "sentiment_auto",
        "topic_flag_col": "topic_auto",
    }


