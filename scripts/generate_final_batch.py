"""
최종 배치 생성(63건) → 350건 목표 달성
"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


OUT_PATH = Path("data/step2_final_batch.csv")

FINAL_TEMPLATES = {
    "HOSPITAL": [
        "외래 진료는 평일 오전 9시부터 오후 5시까지 운영됩니다.",
        "토요일은 오전 진료만 운영되며, 일부 진료과는 휴진입니다.",
        "예약 환자 우선 진료 원칙을 따르며, 당일 접수는 대기 시간이 길 수 있습니다.",
        "진료 접수는 진료 시작 30분 전부터 가능합니다.",
        "초진 환자는 진료 전 문진표 작성이 필요합니다.",
        "재진 환자는 이전 진료 기록을 확인한 후 진료가 진행됩니다.",
        "진료 후 약 처방은 원내 약국 또는 원외 약국에서 받으실 수 있습니다.",
        "CT 검사는 예약제로 운영되며, 조영제 사용 여부에 따라 준비사항이 다릅니다.",
        "내시경 검사는 전날 저녁부터 금식이 필요합니다.",
        "물리치료는 의사 처방 후 재활의학과에서 받으실 수 있습니다.",
        "입원 환자 식사는 영양과에서 관리하며, 치료식이 제공됩니다.",
        "퇴원 시 퇴원 약과 진료 예약을 안내해 드립니다.",
        "응급실 이용 시 중증도에 따라 진료 순서가 결정됩니다.",
        "외국인 환자는 여권과 체류 증명서를 지참해 주세요.",
        "장애인 편의시설은 각 층에 마련되어 있습니다.",
        "환자 이송 서비스는 원무과에 문의하시면 안내받으실 수 있습니다.",
        "건강보험 미가입자는 전액 본인 부담으로 진료받으실 수 있습니다.",
        "의료급여 수급권자는 의료급여증을 지참해 주세요.",
        "진료비 할부 결제는 신용카드로만 가능합니다.",
        "진료비 영수증은 홈페이지에서 재발급 가능합니다.",
    ],
    "PHARMACY": [
        "처방전은 발행일로부터 3일 이내 조제해야 합니다.",
        "만성질환자 처방전은 최대 90일분까지 조제 가능합니다.",
        "약 복용 시간은 처방전에 표기된 대로 정확히 지켜주세요.",
        "약 보관은 직사광선을 피하고 서늘한 곳에 하세요.",
        "어린이 손이 닿지 않는 곳에 보관하세요.",
        "약 봉지에 표기된 복용 방법을 반드시 확인하세요.",
        "약 복용 중 부작용이 나타나면 즉시 약사에게 문의하세요.",
        "여러 약을 함께 복용할 때는 약사와 상담하세요.",
        "건강기능식품도 약과 상호작용할 수 있으니 주의하세요.",
        "약 알레르기가 있는 경우 반드시 약사에게 알려주세요.",
        "임신 중이거나 수유 중인 경우 약 복용 전 상담하세요.",
        "노인 환자는 약물 대사가 느려 용량 조절이 필요할 수 있습니다.",
        "약국에서는 혈압, 혈당 측정 서비스를 제공합니다.",
        "약 복용 상담은 언제든지 약사에게 문의하세요.",
        "처방약 외에도 일반의약품 상담이 가능합니다.",
    ],
    "CHECKUP_CENTER": [
        "건강검진은 예약제로 운영되며, 최소 1주일 전 예약을 권장합니다.",
        "검진 전날 저녁 9시 이후 금식해 주세요.",
        "검진 당일 물, 커피, 담배는 금지입니다.",
        "검진 당일 신분증을 반드시 지참하세요.",
        "검진 소요 시간은 2~3시간이며, 내시경 포함 시 3~4시간입니다.",
        "검진 결과는 7~10일 후 우편 또는 이메일로 발송됩니다.",
        "검진 결과 상담은 예약 후 전문의와 진행됩니다.",
        "재검사가 필요한 경우 안내 전화를 드립니다.",
        "위내시경은 수면 또는 비수면 중 선택 가능합니다.",
        "수면 내시경 후에는 운전이 불가능합니다.",
        "대장내시경은 전날 장 정결제 복용이 필요합니다.",
        "여성 검진 대상자는 생리 기간을 피해 예약하세요.",
        "임신 가능성이 있는 경우 X-ray 검사가 제외됩니다.",
        "검진 후 간단한 식사가 제공됩니다.",
        "검진 비용은 현금, 카드, 계좌이체로 결제 가능합니다.",
        "국가건강검진 대상자는 본인 부담금이 없습니다.",
        "추가 검진 항목은 별도 비용이 발생합니다.",
        "검진 예약 변경은 3일 전까지 가능합니다.",
        "검진 취소는 7일 전까지 무료이며, 이후에는 수수료가 부과됩니다.",
        "검진센터 주차는 무료로 제공됩니다.",
    ]
}


def main() -> None:
    random.seed(45)
    
    rows = []
    created_at = datetime.now(timezone.utc).isoformat()
    
    # 병원: 25건, 약국: 20건, 검진: 20건 = 65건 생성
    for i, text in enumerate(random.choices(FINAL_TEMPLATES["HOSPITAL"], k=25), start=1):
        rows.append({
            "text_id": f"FINAL_HOSP_{i:04d}",
            "provider_type": "HOSPITAL",
            "source_type": "faq",
            "provider_name": "종합병원",
            "text": text,
            "source_url": "https://example.com/hospital/faq/final",
            "created_at": created_at,
        })
    
    for i, text in enumerate(random.choices(FINAL_TEMPLATES["PHARMACY"], k=20), start=1):
        rows.append({
            "text_id": f"FINAL_PHARM_{i:04d}",
            "provider_type": "PHARMACY",
            "source_type": "notice",
            "provider_name": "종합약국",
            "text": text,
            "source_url": "https://example.com/pharmacy/guide/final",
            "created_at": created_at,
        })
    
    for i, text in enumerate(random.choices(FINAL_TEMPLATES["CHECKUP_CENTER"], k=20), start=1):
        rows.append({
            "text_id": f"FINAL_CHK_{i:04d}",
            "provider_type": "CHECKUP_CENTER",
            "source_type": "faq",
            "provider_name": "건강검진센터",
            "text": text,
            "source_url": "https://example.com/checkup/faq/final",
            "created_at": created_at,
        })
    
    df = pd.DataFrame(rows)
    
    before = len(df)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    after = len(df)
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    
    print(f"Final batch generated:")
    print(f"- Output: {OUT_PATH}")
    print(f"- Records: {before} → {after} (removed {before - after} duplicates)")
    print(f"- Distribution:")
    for ptype, count in df["provider_type"].value_counts().items():
        print(f"  - {ptype}: {count}")


if __name__ == "__main__":
    main()

