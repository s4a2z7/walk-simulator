"""
Step 2 - 문체 편중 완화(소스 비율 보강 + inquiry/review 다양성 생성)

기능:
1) Raw CSV의 source_type 분포를 계산
2) 목표 최소 비율(target_min) 기준으로 부족한 source_type(inquiry/review)을 추가 생성
3) 병합 CSV 생성 + 전/후 분포 비교 JSON(out/) 저장

기본 정책(권장):
- inquiry 최소 25%, review 최소 25%를 만족하도록 "추가 생성"만 수행(기존 데이터 삭제/다운샘플링 없음)
- provider_type/provider_name은 기존 데이터 분포를 최대한 따라 샘플링
"""

from __future__ import annotations

import argparse
import json
import random
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


DEFAULT_RAW = Path("data/step2_raw_text_sample.csv")
DEFAULT_OUT = Path("data/step2_raw_text_balanced.csv")
DEFAULT_ADDED = Path("data/step2_style_added.csv")
OUT_COMPARE = Path("out/source_type_balance_comparison.json")


TARGET_MIN = {
    # 최소 비율(필요 시 조정)
    "inquiry": 0.25,
    "review": 0.25,
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _count_dist(series: pd.Series) -> dict[str, int]:
    return series.astype(str).value_counts().to_dict()


def _compute_needed_additions(counts: dict[str, int], target_min: dict[str, float]) -> dict[str, int]:
    """
    기존 데이터를 삭제하지 않고, 특정 source_type의 최소 비율을 만족하기 위해
    필요한 추가 행 수(최소)를 계산.
    - 수학적으로: (c_i + x_i) / (N + sum x) >= p_i
    - 보강 대상은 target_min에 있는 타입만으로 가정(여기서는 inquiry/review)

    단순 해법:
    - 각 i에 대해 x_i만 추가한다고 가정한 하한을 계산 후,
      가장 큰 하한을 만족하도록 해당 타입을 우선 보강
    - 이후 전체 합을 기준으로 다른 타입도 조건을 만족하는지 재검증, 부족분 추가
    """
    n0 = int(sum(counts.values()))
    added = {k: 0 for k in target_min.keys()}

    def share(t: str) -> float:
        return (counts.get(t, 0) + added.get(t, 0)) / (n0 + sum(added.values()))

    # 반복 보강(최대 몇 번이면 수렴; 여기서는 소수 타입 2개라 충분)
    for _ in range(10_000):
        violated = [t for t, p in target_min.items() if share(t) + 1e-12 < p]
        if not violated:
            break
        # 가장 부족한 타입에 1개씩 추가
        worst = min(violated, key=lambda t: share(t) - target_min[t])
        added[worst] += 1
    return added


# ===== 다양성 생성 유틸 =====

_RE_MULTI_SPACE = re.compile(r"\s+")


def _variant_spacing(s: str, rng: random.Random) -> str:
    # 띄어쓰기/구두점 변형(과도한 노이즈는 금지)
    s = s.replace("?", " ?") if rng.random() < 0.2 else s
    s = s.replace(".", "") if rng.random() < 0.15 else s
    s = _RE_MULTI_SPACE.sub(" ", s).strip()
    return s


def _variant_colloquial(s: str, rng: random.Random) -> str:
    # 구어체 종결/축약(안전한 범위)
    replacements = [
        ("가능한가요", "가능해요"),
        ("알려주세요", "알려주실래요"),
        ("어떻게 하나요", "어케 해요"),
        ("있나요", "있어요"),
        ("됩니다", "돼요"),
    ]
    for a, b in replacements:
        if a in s and rng.random() < 0.35:
            s = s.replace(a, b)
    return s


def _variant_typo(s: str, rng: random.Random) -> str:
    # 아주 가벼운 오타/축약(지나친 훼손 금지)
    if rng.random() < 0.15:
        s = s.replace("예약", rng.choice(["예약", "예악", "예약 "])).strip()
    if rng.random() < 0.10:
        s = s.replace("가능", rng.choice(["가능", "가눙"]))
    return s


INQUIRY_BASE = [
    "오늘 {time} 예약 가능한가요?",
    "예약 변경은 언제까지 가능해요?",
    "예약 취소하면 수수료 있나요?",
    "검진 전 금식은 몇 시간 해야 하나요?",
    "복용 중인 약은 검진 전에 어떻게 하나요?",
    "주차 가능한가요? 무료인가요?",
    "영업시간이 어떻게 되나요?",
    "처방약 조제 얼마나 걸려요?",
    "처방약 수령 예약할 수 있나요?",
    "당일 접수도 가능한지 궁금해요.",
]

REVIEW_BASE = [
    "직원 응대가 {adj}했어요.",
    "대기 시간이 {adj}어요.",
    "설명이 {adj}해서 이해하기 쉬웠어요.",
    "시설이 {adj}했어요.",
    "전체 진행이 {adj}했어요.",
    "가격 안내가 {adj}했어요.",
]


def gen_inquiry(rng: random.Random) -> str:
    t = rng.choice(INQUIRY_BASE)
    t = t.format(time=rng.choice(["오전", "오후", "저녁", "내일 오전", "이번 주"]))
    t = _variant_colloquial(t, rng)
    t = _variant_typo(t, rng)
    t = _variant_spacing(t, rng)
    return t


def gen_review(rng: random.Random) -> str:
    adj_pos = rng.choice(["친절", "깔끔", "빠른", "만족스러", "좋"])
    adj_neg = rng.choice(["길", "불친절", "아쉬", "복잡", "별로"])
    t = rng.choice(REVIEW_BASE).format(adj=rng.choice([adj_pos, adj_neg]))
    # 감정 표현 약간(이모지는 사용하지 않음)
    if rng.random() < 0.2:
        t = t + rng.choice(["", " ㅠ", " ㅜ", " ..."])
    t = _variant_typo(t, rng)
    t = _variant_spacing(t, rng)
    return t


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--raw", default=str(DEFAULT_RAW), help="input raw csv path")
    p.add_argument("--out", default=str(DEFAULT_OUT), help="output merged csv path")
    p.add_argument("--added_out", default=str(DEFAULT_ADDED), help="output added rows csv path")
    p.add_argument("--seed", type=int, default=20260107, help="random seed")
    args = p.parse_args()

    rng = random.Random(args.seed)
    raw_path = Path(args.raw)
    out_path = Path(args.out)
    added_path = Path(args.added_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    added_path.parent.mkdir(parents=True, exist_ok=True)
    OUT_COMPARE.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(raw_path)
    if "source_type" not in df.columns or "text" not in df.columns:
        raise ValueError("raw must contain source_type and text")

    before_counts = _count_dist(df["source_type"])
    needed = _compute_needed_additions(before_counts, TARGET_MIN)

    # provider_type/provider_name 풀
    provider_pool = None
    if "provider_type" in df.columns and "provider_name" in df.columns:
        provider_pool = (
            df[["provider_type", "provider_name"]]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .to_dict("records")
        )

    def pick_provider() -> tuple[str, str]:
        if provider_pool:
            r = rng.choice(provider_pool)
            return r.get("provider_type", "HOSPITAL"), r.get("provider_name", "")
        return "HOSPITAL", ""

    rows = []
    created_at = _now_iso()
    base_id = 1

    for stype, k in needed.items():
        for _ in range(int(k)):
            provider_type, provider_name = pick_provider()
            text = gen_inquiry(rng) if stype == "inquiry" else gen_review(rng)
            rows.append(
                {
                    "text_id": f"AUG_{stype.upper()}_{base_id:05d}",
                    "source_type": stype,
                    "provider_type": provider_type,
                    "provider_name": provider_name,
                    "created_at": created_at,
                    "text": text,
                }
            )
            base_id += 1

    added_df = pd.DataFrame(rows)
    if len(added_df):
        # 원문 중복(기존 text와 동일) 최소화
        existing_texts = set(df["text"].astype(str).tolist())
        added_df = added_df[~added_df["text"].astype(str).isin(existing_texts)].copy()

    merged = pd.concat([df, added_df], ignore_index=True, sort=False)
    after_counts = _count_dist(merged["source_type"])

    added_df.to_csv(added_path, index=False, encoding="utf-8")
    merged.to_csv(out_path, index=False, encoding="utf-8")

    payload = {
        "target_min": TARGET_MIN,
        "before": {"rows": int(len(df)), "source_type_counts": before_counts},
        "added": {"planned": needed, "actual_rows": int(len(added_df))},
        "after": {"rows": int(len(merged)), "source_type_counts": after_counts},
    }
    OUT_COMPARE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print("saved:")
    print(f"- {added_path} rows={len(added_df)}")
    print(f"- {out_path} rows={len(merged)}")
    print(f"- {OUT_COMPARE}")
    print("planned additions:", needed)


if __name__ == "__main__":
    main()


