#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step2: MEDICAL/GENERAL 비율을 맞춘 Raw 생성기(v2용)

정의(기본):
- MEDICAL: provider_type in {HOSPITAL, CHECKUP_CENTER}
- GENERAL: provider_type in {PHARMACY}

동작:
- 입력 raw를 읽어 `text/raw_text` 호환 보정 후 domain(MEDICAL/GENERAL) 컬럼을 부여한다.
- 목표 비율이 입력과 다르면:
  - MEDICAL 부족분은 소량(보통 몇 건) 룰 기반 템플릿으로 생성
  - GENERAL 과잉분은 랜덤/결정론적(seed)으로 제거하여 총합을 맞춘다.

주의:
- v1 기준선은 유지하고, 이 스크립트 산출물은 **v2용 raw**로만 사용한다.
"""

from __future__ import annotations

import argparse
import hashlib
import random
from datetime import datetime
from pathlib import Path

import pandas as pd


MEDICAL_PROVIDER_TYPES = ["HOSPITAL", "CHECKUP_CENTER"]
GENERAL_PROVIDER_TYPES = ["PHARMACY"]


INQUIRY_TEMPLATES = [
    "주말에도 예약 가능한가요?",
    "당일 예약이 가능한지 알고 싶습니다.",
    "예약 취소는 어떻게 하나요?",
    "온라인 예약이 되나요?",
    "예약 변경은 어떻게 하나요?",
    "대기 시간이 얼마나 걸리나요?",
    "진료 시간이 어떻게 되나요?",
    "주차는 가능한가요?",
    "보험 적용이 되나요?",
    "검진 결과는 언제 나오나요?",
    "검진 전 준비사항이 있나요?",
]

REVIEW_TEMPLATES = [
    "친절하고 빠른 진료 감사합니다.",
    "대기 시간이 좀 길었지만 전반적으로 만족했어요.",
    "설명을 자세히 해주셔서 좋았습니다.",
    "시설이 깨끗하고 안내가 잘 되어 있어요.",
    "예약하고 가니 접수가 빨랐어요.",
]

FAQ_TEMPLATES = [
    "예약은 전화 또는 온라인으로 가능합니다.",
    "진료 시간은 평일 9시부터 18시까지입니다.",
    "주차는 건물 지하 주차장을 이용하실 수 있습니다.",
    "검진 전 8시간 금식이 필요합니다.",
    "예약 취소는 최소 하루 전까지 가능합니다.",
]


def _is_blank_series(s: pd.Series) -> pd.Series:
    s2 = s.astype("string")
    return s2.isna() | (s2.str.strip() == "")


def coalesce_text(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "text" not in df.columns and "raw_text" in df.columns:
        df["text"] = df["raw_text"]
    elif "text" in df.columns and "raw_text" in df.columns:
        m = _is_blank_series(df["text"]) & (~_is_blank_series(df["raw_text"]))
        if int(m.sum()):
            df.loc[m, "text"] = df.loc[m, "raw_text"]
    return df


def add_domain(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "provider_type" not in df.columns:
        df["domain"] = "UNKNOWN"
        return df
    pt = df["provider_type"].astype("string").fillna("").str.strip()
    df["domain"] = "UNKNOWN"
    df.loc[pt.isin(MEDICAL_PROVIDER_TYPES), "domain"] = "MEDICAL"
    df.loc[pt.isin(GENERAL_PROVIDER_TYPES), "domain"] = "GENERAL"
    return df


def _make_ids(provider_name: str, source_type: str, text: str) -> tuple[str, str]:
    # dedup_key(짧게)
    dedup_raw = f"{provider_name}|{source_type}|{text}"
    dedup_key = hashlib.md5(dedup_raw.encode("utf-8")).hexdigest()[:16]
    # text_id(결정론적으로)
    tid_raw = f"{provider_name}|{source_type}|{text}|{dedup_key}"
    text_id = "mg_" + hashlib.sha1(tid_raw.encode("utf-8")).hexdigest()[:12]
    return text_id, dedup_key


def generate_medical_rows(n: int, *, seed: int = 42) -> pd.DataFrame:
    rnd = random.Random(seed)
    rows = []
    provider_names = {
        "HOSPITAL": ["서울병원", "강남병원", "부산병원", "대전병원", "광주병원"],
        "CHECKUP_CENTER": ["서울검진센터", "강남검진센터", "부산검진센터", "대전검진센터", "광주검진센터"],
    }
    source_types = ["inquiry", "review", "faq"]
    templates = {"inquiry": INQUIRY_TEMPLATES, "review": REVIEW_TEMPLATES, "faq": FAQ_TEMPLATES}
    created_at = datetime.now().strftime("%Y-%m-%d")

    for _ in range(n):
        provider_type = rnd.choice(MEDICAL_PROVIDER_TYPES)
        provider_name = rnd.choice(provider_names[provider_type])
        source_type = rnd.choice(source_types)
        text = rnd.choice(templates[source_type])
        text_id, dedup_key = _make_ids(provider_name, source_type, text)
        rows.append(
            {
                "text_id": text_id,
                "source_type": source_type,
                "provider_type": provider_type,
                "provider_name": provider_name,
                "created_at": created_at,
                "rating": None,
                "sentiment_label": "",
                "topic_label": "",
                "text": text,
                "raw_text": text,
                "dedup_key": dedup_key,
                "collected_at": created_at,
                "domain": "MEDICAL",
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="in_path", required=True, help="input raw csv path")
    p.add_argument("--out", dest="out_path", required=True, help="output raw csv path")
    p.add_argument("--target_total", type=int, default=1000)
    p.add_argument("--target_medical", type=int, default=700)
    p.add_argument("--target_general", type=int, default=300)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    in_path = Path(args.in_path)
    out_path = Path(args.out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(in_path)
    df = coalesce_text(df)
    df = add_domain(df)

    # 현재 분포
    cur_total = int(len(df))
    cur_med = int((df["domain"] == "MEDICAL").sum()) if "domain" in df.columns else 0
    cur_gen = int((df["domain"] == "GENERAL").sum()) if "domain" in df.columns else 0

    # 목표 검증(합)
    if args.target_medical + args.target_general != args.target_total:
        raise ValueError("target_medical + target_general must equal target_total")

    # 총합을 target_total로 맞추기 위해 먼저 샘플링(필요 시)
    rnd = random.Random(args.seed)
    if cur_total > args.target_total:
        keep_idx = rnd.sample(list(df.index), k=args.target_total)
        df = df.loc[keep_idx].copy()
        df = add_domain(df)

    # MEDICAL 부족분 생성 + GENERAL 과잉분 제거(총합 유지)
    cur_total = int(len(df))
    cur_med = int((df["domain"] == "MEDICAL").sum())
    cur_gen = int((df["domain"] == "GENERAL").sum())

    need_med = max(0, args.target_medical - cur_med)
    need_gen = max(0, args.target_general - cur_gen)

    if need_med and need_gen:
        # 동시에 부족한 경우는 정의상 거의 불가(UNKNOWN이 많을 때). 여기선 UNKNOWN을 재분류/제거하지 않고 그대로 둔다.
        pass

    if need_med:
        # 부족한 만큼 MEDICAL 생성 → 총합 초과분만큼 GENERAL(또는 UNKNOWN)에서 제거
        gen_df = generate_medical_rows(need_med, seed=args.seed)
        # 입력 컬럼을 최대한 유지: input에 없는 컬럼은 채우고, extra는 포함
        df = pd.concat([df, gen_df], ignore_index=True)
        df = add_domain(df)

        excess = int(len(df) - args.target_total)
        if excess > 0:
            # 우선 GENERAL에서 제거, 부족하면 UNKNOWN에서 제거
            drop_pool = df.index[df["domain"].isin(["GENERAL", "UNKNOWN"])].tolist()
            if len(drop_pool) < excess:
                drop_pool = df.index.tolist()
            drop_idx = rnd.sample(drop_pool, k=excess)
            df = df.drop(index=drop_idx).reset_index(drop=True)

    # GENERAL이 부족한 경우는(현 데이터 기준 거의 없음) 생성 로직을 생략하고 UNKNOWN에서 전환하지 않는다.

    # 최종 분포 확인
    df = add_domain(df)
    out_path.write_text(df.to_csv(index=False, encoding="utf-8"), encoding="utf-8")

    med = int((df["domain"] == "MEDICAL").sum())
    gen = int((df["domain"] == "GENERAL").sum())
    print("saved:")
    print(f"- {out_path}")
    print(f"total={len(df)}, MEDICAL={med}, GENERAL={gen}")


if __name__ == "__main__":
    main()


