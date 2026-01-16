#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step2 데이터 1000건 확장 스크립트

목표 분배표 기준으로 부족분을 계산하고, 다양성 있는 데이터를 생성해 병합
"""
import argparse
import pandas as pd
import random
from pathlib import Path
from datetime import datetime
import hashlib
import json

# 목표 분배표 (1000건 기준)
TARGET_DISTRIBUTION = {
    "inquiry": 0.30,  # 30% = 300건
    "review": 0.30,   # 30% = 300건
    "faq": 0.20,      # 20% = 200건
    "dataset": 0.10,  # 10% = 100건
    "notice": 0.10    # 10% = 100건
}

TARGET_TOTAL = 1000

# provider_type 균등 분배
PROVIDER_TYPES = ["HOSPITAL", "PHARMACY", "CHECKUP_CENTER"]

# 다양성 증대를 위한 텍스트 변형 함수들
def add_colloquial_variation(text):
    """구어체 변형"""
    variations = [
        (r"어떻게", ["어케", "어떻게"]),
        (r"무엇", ["뭐", "무엇"]),
        (r"가능한가요", ["가능한가요", "가능해요", "될까요"]),
        (r"합니까", ["해요", "합니까"]),
        (r"있습니까", ["있어요", "있나요", "있습니까"]),
    ]
    for pattern, replacements in variations:
        if pattern in text:
            text = text.replace(pattern, random.choice(replacements))
    return text

def add_typo_variation(text):
    """가벼운 오타 추가 (과도하지 않게)"""
    typo_map = {
        "예약": ["예약", "예악"],
        "가능": ["가능", "가눙"],
        "진료": ["진료", "진료"],
        "검진": ["검진", "검진"],
    }
    for original, variants in typo_map.items():
        if original in text and random.random() < 0.15:  # 15% 확률
            text = text.replace(original, random.choice(variants), 1)
    return text

def add_spacing_variation(text):
    """공백/구두점 변형"""
    if random.random() < 0.3:
        if not text.endswith(("?", ".", "!")):
            text += random.choice(["", "?", "."])
    return text

def add_emotion_expression(text):
    """감정 표현 추가 (텍스트 기반, 이모지 제외)"""
    emotions = ["ㅠㅠ", "ㅜㅜ", "...", "!!", ""]
    if random.random() < 0.2:
        text = text.rstrip() + " " + random.choice(emotions)
    return text.strip()

def apply_style_diversity(text, source_type):
    """source_type에 따라 적절한 다양성 적용"""
    if source_type in ["inquiry", "review"]:
        if random.random() < 0.4:
            text = add_colloquial_variation(text)
        if random.random() < 0.15:
            text = add_typo_variation(text)
        text = add_spacing_variation(text)
        if source_type == "review":
            text = add_emotion_expression(text)
    return text

# 템플릿 풀 (더 다양한 텍스트)
INQUIRY_TEMPLATES = [
    "주말에도 예약 가능한가요?",
    "당일 예약이 가능한지 알고 싶습니다",
    "예약 취소는 어떻게 하나요?",
    "온라인 예약이 되나요?",
    "전화 예약만 가능한가요?",
    "예약 없이 방문 가능한가요?",
    "예약 변경은 어떻게 하나요?",
    "대기 시간이 얼마나 걸리나요?",
    "진료 시간이 어떻게 되나요?",
    "주차는 가능한가요?",
    "보험 적용이 되나요?",
    "비용이 얼마나 드나요?",
    "검진 결과는 언제 나오나요?",
    "검진 전 준비사항이 있나요?",
    "약 복용 방법을 알려주세요",
    "부작용이 있을까요?",
    "처방전 없이도 구매 가능한가요?",
    "배송도 되나요?",
    "영업 시간이 어떻게 되나요?",
    "휴무일은 언제인가요?",
]

REVIEW_TEMPLATES = [
    "친절하고 빠른 진료 감사합니다",
    "대기 시간이 좀 길었지만 만족스러웠어요",
    "설명을 자세히 해주셔서 좋았습니다",
    "시설이 깨끗하고 좋네요",
    "주차가 편리해서 좋았습니다",
    "예약 시스템이 편리해요",
    "직원분들이 친절하셨습니다",
    "가격이 합리적이에요",
    "검진이 꼼꼼하게 진행되었습니다",
    "결과 설명이 명확했어요",
    "약 효과가 좋았습니다",
    "복용 방법을 자세히 알려주셨어요",
    "배송이 빨라서 좋았어요",
    "재방문 의사 있습니다",
    "추천할 만한 곳이에요",
    "아쉬운 점이 있었지만 전반적으로 괜찮았습니다",
    "다음에도 이용할게요",
    "처음 방문인데 만족스럽습니다",
    "예약 없이 갔는데도 대기 시간이 짧았어요",
    "전문적인 상담 감사합니다",
]

FAQ_TEMPLATES = [
    "예약은 전화 또는 온라인으로 가능합니다",
    "영업 시간은 평일 9시부터 18시까지입니다",
    "주차는 건물 지하 주차장을 이용하실 수 있습니다",
    "보험 적용 여부는 사전에 문의해주시기 바랍니다",
    "검진 결과는 일주일 이내에 확인 가능합니다",
    "검진 전 8시간 금식이 필요합니다",
    "약은 처방전이 있어야 구매 가능합니다",
    "배송은 영업일 기준 2-3일 소요됩니다",
    "휴무일은 일요일과 공휴일입니다",
    "예약 취소는 최소 하루 전까지 가능합니다",
    "당일 예약은 전화로만 가능합니다",
    "대기 시간은 평균 30분 정도입니다",
    "진료 비용은 항목에 따라 다릅니다",
    "주말 진료는 토요일 오전만 가능합니다",
    "초진은 예약 필수입니다",
]

DATASET_TEMPLATES = [
    "고혈압 약 복용 시 주의사항을 알려드립니다",
    "당뇨 환자의 식이요법에 대해 설명드립니다",
    "정기 검진의 중요성에 대해 안내드립니다",
    "감기약 복용 방법을 안내드립니다",
    "건강검진 항목별 의미를 설명드립니다",
]

NOTICE_TEMPLATES = [
    "설날 연휴 휴무 안내드립니다",
    "예약 시스템 점검 안내",
    "신규 검진 프로그램 도입 안내",
    "주차장 공사로 인한 불편 안내",
    "영업 시간 변경 안내드립니다",
]

def generate_text_by_type(source_type, provider_type):
    """source_type과 provider_type에 맞는 텍스트 생성"""
    if source_type == "inquiry":
        base_text = random.choice(INQUIRY_TEMPLATES)
    elif source_type == "review":
        base_text = random.choice(REVIEW_TEMPLATES)
    elif source_type == "faq":
        base_text = random.choice(FAQ_TEMPLATES)
    elif source_type == "dataset":
        base_text = random.choice(DATASET_TEMPLATES)
    elif source_type == "notice":
        base_text = random.choice(NOTICE_TEMPLATES)
    else:
        base_text = "기본 텍스트입니다"
    
    # 다양성 적용
    text = apply_style_diversity(base_text, source_type)
    return text

def generate_row(source_type, provider_type, text_id_base=1000):
    """단일 행 생성 (기존 스키마와 완전 일치)"""
    text = generate_text_by_type(source_type, provider_type)
    
    # provider_name 생성
    provider_names = {
        "HOSPITAL": ["서울병원", "강남병원", "부산병원", "대전병원", "광주병원"],
        "PHARMACY": ["서울약국", "강남약국", "부산약국", "대전약국", "광주약국"],
        "CHECKUP_CENTER": ["서울검진센터", "강남검진센터", "부산검진센터", "대전검진센터", "광주검진센터"],
    }
    provider_name = random.choice(provider_names[provider_type])
    
    # dedup_key 생성
    dedup_raw = f"{provider_name}_{text}_{source_type}"
    dedup_key = hashlib.md5(dedup_raw.encode("utf-8")).hexdigest()[:16]
    
    # text_id 생성
    text_id = f"{provider_type[:4].lower()}_{text_id_base}_{random.randint(1000,9999)}"
    
    # 라벨 생성 (간단한 룰 기반)
    sentiment_label = "neutral"
    if source_type == "review":
        if any(word in text for word in ["좋", "감사", "만족", "친절", "편리"]):
            sentiment_label = "positive"
        elif any(word in text for word in ["아쉬", "불편", "길었"]):
            sentiment_label = "negative"
    
    topic_label = "other"
    if "예약" in text:
        topic_label = "reservation"
    elif "검진" in text:
        topic_label = "prep"
    elif "약" in text or "복용" in text:
        topic_label = "explain"
    elif "주차" in text or "위치" in text:
        topic_label = "location"
    elif "비용" in text or "가격" in text:
        topic_label = "price"
    elif "시간" in text or "대기" in text:
        topic_label = "wait"
    elif "친절" in text or "직원" in text:
        topic_label = "staff"
    
    # 기존 스키마의 모든 컬럼 포함
    created_at = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "text_id": text_id,
        "source_type": source_type,
        "provider_type": provider_type,
        "provider_name": provider_name,
        "created_at": created_at,
        "rating": None,  # 선택 컬럼
        "sentiment_label": sentiment_label,
        "topic_label": topic_label,
        "text": text,  # raw_text 대신 text 사용
        "__source_file": None,
        "source_url": None,
        "raw_text": text,  # 호환성 유지
        "dedup_key": dedup_key,
        "collected_at": created_at,
    }

def main():
    parser = argparse.ArgumentParser(description="1000건 데이터 확장")
    parser.add_argument("--current", type=str, required=True, help="현재 raw CSV 경로")
    parser.add_argument("--out", type=str, required=True, help="확장된 1000건 CSV 출력 경로")
    parser.add_argument("--added_out", type=str, default="data/step2_expanded_added.csv", help="추가된 데이터만 저장할 경로")
    parser.add_argument("--target", type=int, default=1000, help="목표 총 건수")
    args = parser.parse_args()
    
    # 현재 데이터 로드
    current_df = pd.read_csv(args.current)
    current_total = len(current_df)
    
    print(f"현재 데이터: {current_total}건")
    print(f"목표 데이터: {args.target}건")
    
    # 현재 source_type 분포
    current_dist = current_df["source_type"].value_counts().to_dict()
    print(f"현재 분포: {current_dist}")
    
    # 목표 분포 계산
    target_dist = {k: int(args.target * v) for k, v in TARGET_DISTRIBUTION.items()}
    print(f"목표 분포: {target_dist}")
    
    # 부족분 계산
    needed = {}
    for source_type, target_count in target_dist.items():
        current_count = current_dist.get(source_type, 0)
        if target_count > current_count:
            needed[source_type] = target_count - current_count
    
    print(f"추가 필요: {needed}")
    total_needed = sum(needed.values())
    print(f"총 추가 필요: {total_needed}건")
    
    if total_needed == 0:
        print("이미 목표를 달성했습니다!")
        current_df.to_csv(args.out, index=False, encoding="utf-8-sig")
        return
    
    # 추가 데이터 생성
    added_rows = []
    text_id_counter = 1000
    for source_type, count in needed.items():
        for i in range(count):
            provider_type = random.choice(PROVIDER_TYPES)
            row = generate_row(source_type, provider_type, text_id_base=text_id_counter)
            added_rows.append(row)
            text_id_counter += 1
    
    added_df = pd.DataFrame(added_rows)
    print(f"생성된 추가 데이터: {len(added_df)}건")
    
    # 병합
    expanded_df = pd.concat([current_df, added_df], ignore_index=True)
    
    # 저장
    expanded_df.to_csv(args.out, index=False, encoding="utf-8-sig")
    added_df.to_csv(args.added_out, index=False, encoding="utf-8-sig")
    
    print(f"saved:")
    print(f"- {args.out} (총 {len(expanded_df)}건)")
    print(f"- {args.added_out} (추가 {len(added_df)}건)")
    
    # 최종 분포 확인
    final_dist = expanded_df["source_type"].value_counts().to_dict()
    print(f"최종 분포: {final_dist}")
    
    # 비교 JSON 저장
    comparison = {
        "target_total": args.target,
        "target_distribution": TARGET_DISTRIBUTION,
        "before": {
            "total": current_total,
            "distribution": current_dist,
        },
        "added": {
            "total": len(added_df),
            "needed": needed,
        },
        "after": {
            "total": len(expanded_df),
            "distribution": final_dist,
        },
    }
    
    comparison_path = Path("out") / "step2_expansion_to_1000_comparison.json"
    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    with open(comparison_path, "w", encoding="utf-8") as f:
        json.dump(comparison, f, ensure_ascii=False, indent=2)
    print(f"- {comparison_path}")

if __name__ == "__main__":
    main()

