"""
추가 FAQ/안내 텍스트 생성(115건 목표 → 350건 달성)

목적: 350건 목표 달성을 위한 추가 고품질 텍스트 생성
"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


OUT_PATH = Path("data/step2_additional_faq.csv")

# 추가 FAQ 템플릿(더 다양한 시나리오)
ADDITIONAL_TEMPLATES = {
    "HOSPITAL": [
        # 전문 진료
        "심장내과는 부정맥, 협심증, 심근경색 등 심혈관 질환을 전문으로 진료합니다.",
        "신경과에서는 두통, 어지럼증, 손발 저림, 치매 등을 진단하고 치료합니다.",
        "피부과는 아토피, 여드름, 탈모, 피부암 등을 전문으로 다룹니다.",
        "정신건강의학과는 우울증, 불안장애, 수면장애 등을 상담하고 치료합니다.",
        "재활의학과에서는 물리치료, 작업치료, 통증 치료를 제공합니다.",
        
        # 응급/특수 상황
        "응급 상황 시 119에 먼저 연락하시고, 가까운 응급실로 이동하세요.",
        "야간 응급 진료는 내과, 외과, 소아과에서 제공됩니다.",
        "외국인 환자를 위한 통역 서비스가 제공됩니다(사전 신청 필요).",
        "장애인 환자를 위한 편의시설과 전용 주차 공간이 마련되어 있습니다.",
        
        # 입원/수술
        "입원 수속은 원무과에서 진행하며, 신분증과 보험증이 필요합니다.",
        "수술 전 검사는 수술 3~7일 전에 시행됩니다.",
        "수술 당일 보호자 동반이 필수이며, 수술 동의서를 작성해야 합니다.",
        "입원 중 면회는 지정된 시간에만 가능하며, 중환자실은 제한적입니다.",
        
        # 예방접종/건강관리
        "독감 예방접종은 매년 10월부터 시작되며, 예약 없이 접수 가능합니다.",
        "영유아 예방접종은 소아청소년과에서 국가 예방접종 일정에 따라 시행됩니다.",
        "건강검진 결과 상담은 가정의학과에서 예약 후 받으실 수 있습니다.",
        
        # 증명서/서류
        "진단서는 진료 당일 또는 익일 발급 가능하며, 수수료가 부과됩니다.",
        "소견서, 진료확인서는 원무과에서 즉시 발급 가능합니다.",
        "영문 진단서는 발급까지 3~5일 소요됩니다.",
        "보험 청구용 서류는 진료과에서 안내받으신 후 원무과에서 발급받으세요.",
    ],
    
    "PHARMACY": [
        # 약 종류별 안내
        "해열제는 체온이 38.5도 이상일 때 복용하며, 4~6시간 간격으로 복용 가능합니다.",
        "소화제는 식후 불편감이 있을 때 복용하며, 장기 복용 시 의사와 상담하세요.",
        "진통제는 통증이 심할 때 복용하되, 하루 최대 용량을 초과하지 마세요.",
        "알레르기약은 졸음이 올 수 있으니 운전 전 복용을 피하세요.",
        
        # 특수 상황
        "임신 중이거나 수유 중인 경우 반드시 약사에게 알려주세요.",
        "어린이 약은 체중과 나이에 따라 용량이 다르므로 정확한 복용이 중요합니다.",
        "노인 환자는 약물 대사가 느려 용량 조절이 필요할 수 있습니다.",
        
        # 보관/폐기
        "약은 직사광선을 피하고 서늘하고 건조한 곳에 보관하세요.",
        "냉장 보관이 필요한 약은 약봉지에 표시되어 있습니다.",
        "유효기간이 지난 약은 약국이나 보건소에 반납해 주세요.",
        
        # 상호작용
        "여러 약을 함께 복용할 때는 약사에게 상호작용 여부를 확인하세요.",
        "건강기능식품도 약과 상호작용할 수 있으니 복용 중인 약을 알려주세요.",
        "자몽주스는 일부 약물의 효과를 변화시킬 수 있으니 주의하세요.",
        
        # 복약 지도
        "캡슐약은 물과 함께 삼키고, 씹거나 쪼개지 마세요.",
        "가루약은 물에 타서 복용하거나 그대로 입에 넣고 물로 삼키세요.",
        "물약은 흔들어서 복용하고, 계량컵이나 스포이트를 사용하세요.",
        "패치제는 깨끗하고 건조한 피부에 부착하고, 매일 다른 부위에 붙이세요.",
    ],
    
    "CHECKUP_CENTER": [
        # 검진 종류
        "일반 건강검진은 만 20세 이상 성인에게 2년마다 제공됩니다.",
        "암 검진은 위암, 대장암, 간암, 유방암, 자궁경부암을 대상으로 합니다.",
        "영유아 건강검진은 생후 4개월부터 71개월까지 총 8회 시행됩니다.",
        "학생 건강검진은 초·중·고등학교에서 매년 시행됩니다.",
        
        # 검진 항목 상세
        "혈액검사는 빈혈, 혈당, 콜레스테롤, 간 기능, 신장 기능 등을 확인합니다.",
        "소변검사는 신장 질환, 당뇨, 요로감염 등을 조기 발견하는 데 도움이 됩니다.",
        "흉부 X-ray는 폐렴, 결핵, 폐암 등 폐 질환을 확인합니다.",
        "심전도 검사는 부정맥, 협심증 등 심장 질환을 조기 발견합니다.",
        
        # 내시경 검진
        "위내시경은 위암, 위염, 위궤양 등을 조기 발견할 수 있습니다.",
        "수면 내시경은 진정제를 사용해 검사 중 불편감을 최소화합니다.",
        "수면 내시경 후에는 운전이 불가능하므로 대중교통을 이용하세요.",
        "대장내시경은 대장암, 용종 등을 조기 발견하고 제거할 수 있습니다.",
        
        # 여성 검진
        "유방촬영은 유방암 조기 발견에 가장 효과적인 검사입니다.",
        "유방 초음파는 치밀 유방에서 유방촬영을 보완하는 검사입니다.",
        "자궁경부암 검사는 세포 검사로 간단하게 시행됩니다.",
        "난소 초음파는 난소 종양, 낭종 등을 확인합니다.",
        
        # 특수 검진
        "골밀도 검사는 골다공증 위험을 평가하며, 폐경 여성에게 권장됩니다.",
        "갑상선 초음파는 갑상선 결절, 갑상선암을 조기 발견합니다.",
        "복부 초음파는 간, 담낭, 췌장, 신장, 비장 등을 확인합니다.",
        "심장 초음파는 심장 구조와 기능을 평가합니다.",
        
        # 검진 후 관리
        "정상 판정을 받아도 정기적인 건강검진이 필요합니다.",
        "유소견 판정 시 추가 검사나 치료가 필요할 수 있습니다.",
        "생활습관 개선이 필요한 경우 영양 상담과 운동 처방을 받을 수 있습니다.",
    ]
}


def main() -> None:
    random.seed(44)
    
    rows = []
    created_at = datetime.now(timezone.utc).isoformat()
    
    # 병원: 50건
    for i, text in enumerate(random.choices(ADDITIONAL_TEMPLATES["HOSPITAL"], k=50), start=1):
        rows.append({
            "text_id": f"ADD_HOSP_{i:04d}",
            "provider_type": "HOSPITAL",
            "source_type": "faq",
            "provider_name": random.choice([
                "서울대병원", "아산병원", "세브란스병원", "삼성병원",
                "고대안암병원", "서울성모병원", "분당서울대병원", "강남세브란스병원"
            ]),
            "text": text,
            "source_url": "https://example.com/hospital/faq/additional",
            "created_at": created_at,
        })
    
    # 약국: 35건
    for i, text in enumerate(random.choices(ADDITIONAL_TEMPLATES["PHARMACY"], k=35), start=1):
        rows.append({
            "text_id": f"ADD_PHARM_{i:04d}",
            "provider_type": "PHARMACY",
            "source_type": "notice",
            "provider_name": random.choice([
                "중앙약국", "서울약국", "강남약국", "건강약국",
                "온누리약국", "참약국", "행복약국", "메디팜약국"
            ]),
            "text": text,
            "source_url": "https://example.com/pharmacy/guide/additional",
            "created_at": created_at,
        })
    
    # 검진센터: 35건
    for i, text in enumerate(random.choices(ADDITIONAL_TEMPLATES["CHECKUP_CENTER"], k=35), start=1):
        rows.append({
            "text_id": f"ADD_CHK_{i:04d}",
            "provider_type": "CHECKUP_CENTER",
            "source_type": "faq",
            "provider_name": random.choice([
                "서울대병원건강증진센터", "아산병원건강증진센터",
                "세브란스건강증진센터", "삼성서울병원건강의학센터"
            ]),
            "text": text,
            "source_url": "https://example.com/checkup/faq/additional",
            "created_at": created_at,
        })
    
    df = pd.DataFrame(rows)
    
    # 중복 제거
    before = len(df)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    after = len(df)
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    
    print(f"Additional FAQ data generated:")
    print(f"- Output: {OUT_PATH}")
    print(f"- Records: {before} → {after} (removed {before - after} duplicates)")
    print(f"- Distribution:")
    for ptype, count in df["provider_type"].value_counts().items():
        print(f"  - {ptype}: {count}")
    print(f"\nNext step: Final merge to reach 350+ records")


if __name__ == "__main__":
    main()

