"""
AI Hub 스타일 샘플 데이터 생성(테스트용)

실제 AI Hub 다운로드 전, 변환 파이프라인을 검증하기 위한 샘플 생성기
"""

from __future__ import annotations

import json
import random
from pathlib import Path


OUT_DIR = Path("data/aihub_download")
OUT_PATH = OUT_DIR / "medical_conversation_sample.json"

# AI Hub 스타일 의료/상담 텍스트 템플릿(150건 생성 목표)
TEMPLATES = {
    "hospital": [
        "내과 진료 예약하고 싶은데 오늘 가능한가요?",
        "진료 예약을 변경하고 싶어요. 어떻게 하나요?",
        "예약 없이 당일 접수 가능한가요?",
        "진료비는 어떻게 결제하나요?",
        "건강보험 적용되나요?",
        "진료 시간이 어떻게 되시나요?",
        "주차 가능한가요?",
        "병원 위치가 어디인가요?",
        "진료 과목은 어떤 게 있나요?",
        "예약 취소는 언제까지 가능한가요?",
        "진료 대기 시간이 얼마나 걸리나요?",
        "MRI 검사 예약하고 싶어요.",
        "초음파 검사는 어떻게 예약하나요?",
        "혈액 검사 결과는 언제 나오나요?",
        "입원 상담은 어디서 하나요?",
        "응급실 운영 시간이 어떻게 되나요?",
        "감기 증상인데 어느 과에 가야 하나요?",
        "복통이 심한데 바로 진료 가능한가요?",
        "두통약 처방받고 싶어요.",
        "진료 기록 발급 받으려면 어떻게 하나요?",
    ],
    "pharmacy": [
        "처방전 없이도 약 구매 가능한가요?",
        "처방약 조제 시간이 얼마나 걸리나요?",
        "조제 완료되면 알림 받을 수 있나요?",
        "약국 운영 시간이 어떻게 되나요?",
        "일요일에도 영업하나요?",
        "약 배달 서비스가 있나요?",
        "약 복용 방법 상담 가능한가요?",
        "감기약 추천해주세요.",
        "소화제는 어떤 게 좋나요?",
        "진통제 부작용이 있나요?",
        "항생제 복용 중인데 술 마셔도 되나요?",
        "약 가격이 얼마인가요?",
        "건강보험 적용 약인가요?",
        "처방전 유효기간이 어떻게 되나요?",
        "약 반납은 어떻게 하나요?",
    ],
    "checkup": [
        "건강검진 예약하고 싶어요.",
        "검진 전 금식이 필요한가요?",
        "검진 전날 물은 마셔도 되나요?",
        "검진 당일 커피 마셔도 되나요?",
        "검진 소요 시간이 얼마나 걸리나요?",
        "검진 결과는 언제 나오나요?",
        "검진 예약 변경하려면 어떻게 하나요?",
        "검진 예약 취소 수수료가 있나요?",
        "국가건강검진 대상자인지 확인하고 싶어요.",
        "종합검진 비용이 얼마인가요?",
        "위내시경 검진 예약 가능한가요?",
        "대장내시경은 어떻게 준비하나요?",
        "유방암 검진은 포함되나요?",
        "자궁경부암 검진도 같이 받을 수 있나요?",
        "검진 전 복용 중인 약은 어떻게 하나요?",
        "검진 당일 준비물이 있나요?",
        "신분증 꼭 가져가야 하나요?",
        "검진 결과 상담은 어떻게 받나요?",
        "재검사가 필요하다고 나왔는데 어떻게 하나요?",
        "검진센터 위치가 어디인가요?",
    ],
}


def main() -> None:
    random.seed(42)
    
    # 150건 생성(병원 70, 약국 45, 검진센터 35)
    records = []
    
    # 병원(70건)
    for i in range(70):
        text = random.choice(TEMPLATES["hospital"])
        records.append({
            "id": f"MED_{i+1:04d}",
            "category": "hospital",
            "text": text,
        })
    
    # 약국(45건)
    for i in range(45):
        text = random.choice(TEMPLATES["pharmacy"])
        records.append({
            "id": f"PHARM_{i+1:04d}",
            "category": "pharmacy",
            "text": text,
        })
    
    # 검진센터(35건)
    for i in range(35):
        text = random.choice(TEMPLATES["checkup"])
        records.append({
            "id": f"CHK_{i+1:04d}",
            "category": "checkup",
            "text": text,
        })
    
    # JSON 저장(AI Hub 스타일)
    output = {
        "dataset_name": "medical_conversation_sample",
        "version": "1.0",
        "total_count": len(records),
        "data": records,
    }
    
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"AI Hub style sample data generated:")
    print(f"- Output: {OUT_PATH}")
    print(f"- Records: {len(records)}")
    print(f"  - Hospital: 70")
    print(f"  - Pharmacy: 45")
    print(f"  - Checkup Center: 35")
    print(f"\nNext step: Convert to project CSV schema")
    print(f"  py -3 .\\scripts\\step2_convert_aihub_to_csv.py --input {OUT_PATH} --output data\\aihub_converted.csv --format json")


if __name__ == "__main__":
    main()

