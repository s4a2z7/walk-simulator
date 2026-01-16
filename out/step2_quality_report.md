# Step 2 품질 체크 리포트

- 입력: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/data/step2_raw_text_expanded_mg_700_300.csv`
- 전처리 파일(참고): `out/step2_preprocessed.csv`

## 요약
- rows: **1000**
- 필수 컬럼 누락: **0**
- 필수 컬럼 결측/공백 행(원본 기준): **584**
- 필수 컬럼 결측/공백 행(text/raw_text 보정 후): **0**
- (원문 text) 중복 후보: **515**
- (dedup_key) 중복 후보: **431**
- PII(URL/EMAIL/PHONE) 포함: **0/0/0**

중복 정의(참고):
- **원문 중복**: `text` 컬럼이 완전히 동일한 경우(공백/기호 차이 포함)
- **dedup_key 중복**: `provider_type + source_type + text_normalized`가 동일한 경우(정규화 후 의미 중복 후보)

## 분포
- 도메인(provider_type)
  - HOSPITAL: 380
  - CHECKUP_CENTER: 320
  - PHARMACY: 300
- source_type
  - inquiry: 302
  - review: 301
  - faq: 200
  - dataset: 100
  - notice: 97

## 라벨 품질
- sentiment_label 결측률: **27.3%** (missing=273/1000)
- sentiment_label 허용값 위반: **0**
- sentiment_label Top 분포(Top 10):
  - neutral: 527
  - positive: 166
  - negative: 34
- topic_label 결측률: **27.3%** (missing=273/1000)
- topic_label 허용값 위반: **0**
- topic_label Top 분포(Top 10):
  - other: 186
  - reservation: 164
  - prep: 76
  - wait: 71
  - explain: 68
  - location: 39
  - staff: 37
  - price: 34
  - policy: 11
  - speed: 10

## (선택) 룰 기반 자동 라벨 보완(임시)
- 적용 여부: **True**
- sentiment_label 보완 건수: **273**
- topic_label 보완 건수: **273**
- 보완 후 sentiment_label 결측률: **0.0** (missing=0/1000)
- 보완 후 topic_label 결측률: **0.0** (missing=0/1000)

## 권장 확인
- 스크래핑 데이터는 `source_url`, `fetched_at` 컬럼 포함을 권장합니다.
- PII 탐지된 경우, 전처리(`scripts/step2_preprocess_text.py`)로 마스킹 후 저장하세요.
- 라벨 표준/허용값은 `라벨링가이드_v1.md`를 기준으로 관리합니다.
