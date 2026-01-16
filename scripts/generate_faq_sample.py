"""
공식 FAQ 스타일 텍스트 샘플 생성(200건 목표)

목적:
- 실제 웹 수집이 어려운 경우, FAQ/안내 페이지 스타일의 텍스트를 생성해
  전처리/EDA 파이프라인 검증에 사용
- robots.txt 제한이 있거나 대량 수집이 부담스러운 경우 대안
"""

from __future__ import annotations

import random
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


OUT_PATH = Path("data/step2_faq_style_sample.csv")

# 도메인별 FAQ/안내 텍스트 템플릿(실제 공식 사이트 FAQ 스타일)
FAQ_TEMPLATES = {
    "HOSPITAL": [
        # 예약 관련
        "진료 예약은 전화, 홈페이지, 모바일 앱을 통해 가능합니다.",
        "예약 변경은 진료 시작 1시간 전까지 가능하며, 홈페이지에서 직접 변경하실 수 있습니다.",
        "예약 취소는 진료 당일 오전 9시 이전까지 가능합니다.",
        "초진 환자는 전화 예약 후 방문 30분 전 도착을 권장합니다.",
        "재진 환자는 이전 진료 기록을 바탕으로 빠른 접수가 가능합니다.",
        "당일 예약은 오전 9시부터 선착순으로 접수됩니다.",
        "진료 대기 시간은 예약 시간 기준 평균 15~30분입니다.",
        
        # 진료 안내
        "진료과는 내과, 외과, 정형외과, 이비인후과, 소아청소년과 등이 있습니다.",
        "야간 진료는 평일 오후 6시부터 9시까지 운영됩니다.",
        "응급실은 24시간 운영되며, 중증 환자 우선 진료 원칙을 따릅니다.",
        "진료 시 신분증과 건강보험증을 지참해 주시기 바랍니다.",
        "건강보험 적용 여부는 진료과 및 치료 내용에 따라 다릅니다.",
        "비급여 항목은 수납 전 안내드리며, 사전 문의도 가능합니다.",
        
        # 검사 관련
        "혈액 검사 결과는 당일 오후 또는 익일 오전 확인 가능합니다.",
        "MRI 검사는 예약제로 운영되며, 평균 대기 기간은 3~5일입니다.",
        "초음파 검사는 당일 예약 가능하며, 검사 전 4시간 금식이 필요합니다.",
        "X-ray 검사는 예약 없이 접수 가능하며, 촬영 후 10~20분 내 결과 확인이 가능합니다.",
        
        # 수납/비용
        "진료비는 수납 창구 또는 자동수납기에서 결제 가능합니다.",
        "카드 결제, 현금, 계좌이체 모두 가능하며, 영수증은 자동 발급됩니다.",
        "진료비 세부 내역은 홈페이지에서 조회 가능합니다.",
        
        # 편의시설
        "주차장은 지하 1~3층에 위치하며, 진료 환자는 2시간 무료 주차가 가능합니다.",
        "병원 내 약국은 1층에 위치하며, 평일 오전 9시부터 오후 6시까지 운영됩니다.",
        "편의점과 카페는 본관 1층에 있으며, 오전 7시부터 오후 8시까지 이용 가능합니다.",
        "휠체어 및 유모차 대여는 안내 데스크에서 신분증 맡기시면 무료로 이용하실 수 있습니다.",
        
        # 기타
        "환자 보호자는 1인까지 병실 출입이 가능합니다.",
        "면회 시간은 평일 오후 6시부터 8시까지이며, 주말은 오전 10시부터 오후 6시까지입니다.",
        "진단서 발급은 진료과에서 신청 후 원무과에서 수령 가능합니다.",
        "의료 기록 열람 및 사본 발급은 환자 본인 또는 법정 대리인만 가능합니다.",
    ],
    
    "PHARMACY": [
        # 조제 관련
        "처방전 조제는 접수 후 평균 10~15분 소요됩니다.",
        "처방전 유효기간은 발행일로부터 3일이며, 기간 내 조제하셔야 합니다.",
        "처방전 없이 구매 가능한 일반의약품도 다수 구비되어 있습니다.",
        "복약 상담은 약사가 직접 진행하며, 복용 방법과 주의사항을 안내해 드립니다.",
        
        # 약 수령
        "조제 완료 시 문자 알림 서비스를 제공합니다(사전 신청 필요).",
        "조제된 약은 3일 이내 수령해 주시기 바랍니다.",
        "약 배달 서비스는 거동이 불편한 환자에 한해 제공됩니다(사전 문의 필수).",
        
        # 운영 시간
        "평일 운영 시간은 오전 9시부터 오후 7시까지입니다.",
        "토요일은 오전 9시부터 오후 1시까지 운영됩니다.",
        "일요일 및 공휴일은 휴무입니다.",
        "점심 시간(오후 12시 30분~1시 30분)에도 운영됩니다.",
        
        # 복약 안내
        "항생제는 처방된 기간 동안 빠짐없이 복용해야 합니다.",
        "식전 복용 약은 식사 30분 전, 식후 복용 약은 식사 30분 후 복용하세요.",
        "어지럼증이나 졸음이 올 수 있는 약은 운전 전 복용을 피해 주세요.",
        "약 복용 중 이상 반응이 나타나면 즉시 복용을 중단하고 약사 또는 의사와 상담하세요.",
        
        # 비용/보험
        "처방약은 건강보험이 적용되며, 본인 부담금만 납부하시면 됩니다.",
        "일반의약품은 건강보험 적용 대상이 아닙니다.",
        "카드 결제와 현금 결제 모두 가능합니다.",
        
        # 기타
        "남은 약 또는 유효기간이 지난 약은 약국에 반납해 주세요.",
        "약국 내 혈압 측정기와 체온계를 무료로 이용하실 수 있습니다.",
        "건강 상담은 약사에게 언제든지 문의 가능합니다.",
    ],
    
    "CHECKUP_CENTER": [
        # 예약 관련
        "건강검진 예약은 전화 또는 홈페이지를 통해 가능합니다.",
        "예약 변경은 검진 3일 전까지 가능하며, 그 이후에는 수수료가 발생할 수 있습니다.",
        "예약 취소는 검진 7일 전까지 무료이며, 이후에는 취소 수수료가 부과됩니다.",
        "국가건강검진 대상자는 공단에서 발송된 검진표를 지참해 주세요.",
        
        # 검진 준비
        "검진 전날 저녁 9시 이후에는 금식해 주세요(물 포함).",
        "검진 당일 아침 식사, 물, 커피, 담배, 껌 모두 금지입니다.",
        "검진 전 복용 중인 약은 담당 의사와 상담 후 결정하세요.",
        "혈압약은 소량의 물과 함께 복용 가능합니다(사전 문의 권장).",
        "검진 전날 과식이나 음주는 피해 주시기 바랍니다.",
        
        # 검진 당일
        "검진 소요 시간은 기본 검진 기준 2~3시간입니다.",
        "검진 당일 신분증을 반드시 지참해 주세요.",
        "여성 검진 대상자는 생리 기간을 피해서 예약해 주세요.",
        "임신 중이거나 임신 가능성이 있는 경우 사전에 알려주세요(X-ray 제외 조치).",
        "검진 전 탈의가 필요하므로 편한 복장으로 방문해 주세요.",
        
        # 검진 항목
        "기본 검진 항목은 신장, 체중, 혈압, 시력, 청력, 혈액검사, 소변검사, 흉부 X-ray를 포함합니다.",
        "위내시경 검진은 수면 또는 비수면 중 선택 가능합니다(수면 시 보호자 동반 필수).",
        "대장내시경은 전날 장 정결제 복용이 필요합니다.",
        "유방암 검진(유방촬영 또는 초음파)은 만 40세 이상 여성에게 권장됩니다.",
        "자궁경부암 검진은 만 20세 이상 여성에게 권장됩니다.",
        
        # 결과 안내
        "검진 결과는 검진 후 7~10일 이내에 우편 또는 이메일로 발송됩니다.",
        "결과 상담은 예약 후 전문의와 1:1 상담이 가능합니다.",
        "재검사가 필요한 경우 안내 전화를 드립니다.",
        "과거 검진 결과는 홈페이지에서 조회 가능합니다.",
        
        # 비용
        "국가건강검진은 공단 부담으로 본인 부담금이 없습니다.",
        "추가 검진 항목은 별도 비용이 발생하며, 수납 전 안내해 드립니다.",
        "검진 비용은 현금, 카드, 계좌이체로 결제 가능합니다.",
        
        # 편의시설
        "주차는 건물 지하 주차장을 이용하시면 되며, 검진 환자는 무료 주차가 가능합니다.",
        "검진 후 간단한 식사(죽, 샌드위치)가 제공됩니다.",
        "수면 내시경 검진 시 회복실에서 충분히 휴식 후 귀가하시기 바랍니다.",
    ]
}


def main() -> None:
    random.seed(43)  # 이전 샘플과 다른 시드 사용
    
    rows = []
    created_at = datetime.now(timezone.utc).isoformat()
    
    # 병원 FAQ: 90건
    hospital_texts = random.choices(FAQ_TEMPLATES["HOSPITAL"], k=90)
    for i, text in enumerate(hospital_texts, start=1):
        rows.append({
            "text_id": f"FAQ_HOSP_{i:04d}",
            "provider_type": "HOSPITAL",
            "source_type": "faq",
            "provider_name": random.choice([
                "서울대학교병원", "서울아산병원", "연세세브란스병원", "삼성서울병원",
                "고려대안암병원", "가톨릭대서울성모병원", "경희대학교병원", "이대목동병원"
            ]),
            "text": text,
            "source_url": "https://example.com/hospital/faq",
            "created_at": created_at,
        })
    
    # 약국 안내: 60건
    pharmacy_texts = random.choices(FAQ_TEMPLATES["PHARMACY"], k=60)
    for i, text in enumerate(pharmacy_texts, start=1):
        rows.append({
            "text_id": f"FAQ_PHARM_{i:04d}",
            "provider_type": "PHARMACY",
            "source_type": "notice",
            "provider_name": random.choice([
                "서울약국", "강남약국", "연세약국", "건강약국",
                "메디팜약국", "케어약국", "참약국", "온약국"
            ]),
            "text": text,
            "source_url": "https://example.com/pharmacy/guide",
            "created_at": created_at,
        })
    
    # 검진센터 FAQ: 50건
    checkup_texts = random.choices(FAQ_TEMPLATES["CHECKUP_CENTER"], k=50)
    for i, text in enumerate(checkup_texts, start=1):
        rows.append({
            "text_id": f"FAQ_CHK_{i:04d}",
            "provider_type": "CHECKUP_CENTER",
            "source_type": "faq",
            "provider_name": random.choice([
                "강남세브란스건강증진센터", "서울아산병원건강증진센터",
                "삼성서울병원건강의학센터", "서울대병원건강증진센터"
            ]),
            "text": text,
            "source_url": "https://example.com/checkup/faq",
            "created_at": created_at,
        })
    
    df = pd.DataFrame(rows)
    
    # 중복 제거(text 기준)
    before = len(df)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    after = len(df)
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PATH, index=False, encoding="utf-8")
    
    print(f"FAQ style sample data generated:")
    print(f"- Output: {OUT_PATH}")
    print(f"- Records: {before} → {after} (removed {before - after} duplicates)")
    print(f"- Distribution:")
    for ptype, count in df["provider_type"].value_counts().items():
        print(f"  - {ptype}: {count}")
    print(f"\nNext step: Merge with existing data")
    print(f"  py -3 .\\scripts\\step2_merge_raw_text.py --out data\\step2_raw_text_merged.csv " +
          f"data\\step2_raw_text_sample.csv data\\aihub_converted.csv {OUT_PATH}")


if __name__ == "__main__":
    main()

