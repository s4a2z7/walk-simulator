# Step 2 데이터셋 마스터 현황 (Master Status)

- **프로젝트명**: CareLog AI — Step 2 외부 데이터셋 구축
- **문서 목적**: Step 2 데이터셋의 **기준선/분포/라벨/리스크/다음 단계 조건**을 한 문서에서 관리(제출용)
- **작성일**: YYYY-MM-DD
- **작성자/담당**: TBD
- **버전**: vX.Y (예: v1.0)
- **기준 리포트(참조)**: `out/step2_quality_report.*`, `out/step2_preprocess_summary.json`, `out/step2_eda_report.md`

---

## 1) 기준선 요약 (Raw / After preprocess / Dedup)

### 1.1 데이터 기준선(행 수)

| 구분 | rows | 비고 |
|---|---:|---|
| Raw (수집/병합 직후) | TBD | 입력: `data/step2_raw_text_sample.csv` 또는 통합 Raw |
| After preprocess (전처리 후) | TBD | 출력: `out/step2_preprocessed.csv` |

### 1.2 Dedup 요약

| 항목 | 값 | 정의/비고 |
|---|---:|---|
| 원문(text) 중복 후보 | TBD | `text` 완전 동일 기준 |
| dedup_key 중복 후보 | TBD | `provider_type + source_type + text_normalized` 동일 기준 |
| 전처리 단계에서 dedup 제거 건수 | TBD | `dedup_removed` |
| dedup 전 rows | TBD | `dedup_before_rows` |
| dedup 후 rows | TBD | `dedup_after_rows` |

### 1.3 전처리 주요 지표(요약)

| 항목 | 값 | 비고 |
|---|---:|---|
| 정규화 텍스트 길이 min | TBD | chars |
| 정규화 텍스트 길이 max | TBD | chars |
| 평균 토큰 수 | TBD | whitespace token 기준 |
| PII 탐지(원본) | TBD | URL/EMAIL/PHONE 각 건수 |
| PII 마스킹(전처리) | TBD | 적용 여부 및 결과 요약 |

---

## 2) 도메인 분포

> 도메인 정의 예시: provider_type (HOSPITAL / PHARMACY / CHECKUP_CENTER 등) 또는 서비스 도메인(진료/약국/검진).

### 2.1 provider_type 분포 (Raw 기준)

| provider_type | rows | 비율(%) |
|---|---:|---:|
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| **합계** | TBD | 100 |

### 2.2 provider_type 분포 (After preprocess 기준)

| provider_type | rows | 비율(%) |
|---|---:|---:|
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| **합계** | TBD | 100 |

### 2.3 도메인 편향 점검(서술)

- **관찰 요약**: TBD  
- **편향 여부**: (예) 높음 / 보통 / 낮음  
- **근거**: (예) 특정 provider_type 과다 편중, 특정 주제/라벨 집중 등  
- **개선 액션**: TBD  

---

## 3) source_type 분포

> source_type 정의 예시: review / inquiry / faq / dataset / notice 등.

### 3.1 목표 분배(정책)

- **목표(정책) 요약**: TBD  
- **source_type 목표 비율(%)**:
  - review: TBD%
  - inquiry: TBD%
  - faq: TBD%
  - dataset: TBD%
  - notice: TBD%

### 3.2 현재 분포 비교 (Raw vs After preprocess)

| source_type | Raw rows | Raw 비율(%) | After preprocess rows | After preprocess 비율(%) |
|---|---:|---:|---:|---:|
| review | TBD | TBD | TBD | TBD |
| inquiry | TBD | TBD | TBD | TBD |
| faq | TBD | TBD | TBD | TBD |
| dataset | TBD | TBD | TBD | TBD |
| notice | TBD | TBD | TBD | TBD |
| **합계** | TBD | 100 | TBD | 100 |

### 3.3 문체 편중/다양성 점검(서술)

- **문체 편중 여부**: TBD  
- **근거**: (예) FAQ 문장 패턴 반복, 동일 템플릿 반복 등  
- **대응 현황**: TBD (예: inquiry/review 보강, 외부 수집 확대 등)  

---

## 4) 라벨 상태 요약

> 라벨 표준/허용값은 `라벨링가이드_v1.md` 기준으로 관리합니다.

### 4.1 sentiment_label

- **허용값(Allowed Values)**: TBD (예: positive / neutral / negative)
- **결측률(%)**: TBD
- **허용값 위반 건수**: TBD

#### Top 분포

| sentiment_label | rows | 비율(%) |
|---|---:|---:|
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| **합계** | TBD | 100 |

### 4.2 topic_label

- **허용값(Allowed Values)**: TBD (예: reservation / price / wait / other …)
- **결측률(%)**: TBD
- **허용값 위반 건수**: TBD

#### Top 분포

| topic_label | rows | 비율(%) |
|---|---:|---:|
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| TBD | TBD | TBD |
| **합계** | TBD | 100 |

### 4.3 라벨 품질 코멘트(서술)

- **이슈 요약**: TBD (예: 결측률 높음, 분류 기준 모호, 특정 라벨 과다 등)  
- **대응**: TBD (예: 가이드 강화, 샘플링 수동 검수, 룰 보완, 재라벨링 등)  

---

## 5) 리스크 및 대응 현황 표

| 리스크 | 영향 | 지표/탐지 방법 | 현재 상태 | 대응/완화 전략 | 오너 | 다음 액션 | 목표 일자 |
|---|---|---|---|---|---|---|---|
| 도메인 편향(특정 도메인 과다) | TBD | provider_type 분포/EDA | TBD | 일반 대화/다양 도메인 소스 추가 | TBD | TBD | YYYY-MM-DD |
| 중복 증가로 품질 저하 | TBD | dup_text / dedup_key | TBD | dedup 강화, 템플릿 다양화 | TBD | TBD | YYYY-MM-DD |
| 문체 편중(FAQ 중심, 자연어 다양성 부족) | TBD | 반복 패턴/키워드 편향 | TBD | inquiry/review 보강, 수집 소스 다변화 | TBD | TBD | YYYY-MM-DD |
| 라벨 품질/일관성 부족 | TBD | 결측률/위반/분포 | TBD | 라벨링 가이드/검수 프로세스 | TBD | TBD | YYYY-MM-DD |
| 데이터 볼륨 부족(학습/일반화 한계) | TBD | rows/분포 | TBD | 1k→2k+ 확장 계획 | TBD | TBD | YYYY-MM-DD |
| 크롤링 컴플라이언스/법적 리스크 | TBD | robots.txt, 약관 점검 | TBD | 공식/허용 소스만 수집, 최소수집 | TBD | TBD | YYYY-MM-DD |

---

## 6) 다음 단계 진입 조건 체크리스트

> 다음 단계 예시: (Step 3) 학습 데이터셋 확정/모델 학습 준비, 또는 라벨링/정제 고도화.

### 6.1 데이터 품질(필수)

- [ ] **필수 컬럼 누락 = 0** (컬럼 스키마 충족)
- [ ] **필수 컬럼 결측 행 = 0** 또는 허용 범위 내(TBD)
- [ ] **PII(전화/이메일/URL) 탐지 = 0** 또는 마스킹 완료(TBD)
- [ ] **중복(dup_text / dedup_key) 관리 기준 충족**(TBD)

### 6.2 분포(필수)

- [ ] **provider_type 분포 편향 기준 충족**(TBD)
- [ ] **source_type 목표 분배 기준 충족**(TBD)
- [ ] **문체 다양성 기준 충족**(TBD: 구어체/오타/축약/감정표현 포함 비율 등)

### 6.3 라벨(필수/선택)

- [ ] **sentiment_label 결측률 ≤ TBD%**
- [ ] **topic_label 결측률 ≤ TBD%**
- [ ] **허용값 위반 = 0**
- [ ] (선택) **샘플링 수동 검수 N건 완료**(TBD) 및 오류율 기록

### 6.4 재현성(필수)

- [ ] `run_pipeline.bat` 또는 `scripts/run_full_pipeline.py`로 **전체 파이프라인 재실행 가능**
- [ ] `out/step2_quality_report.*`, `out/step2_preprocess_summary.json`, `out/step2_eda_report.md`가 **최신 상태로 자동 생성**

---

## 부록) 참조 파일(링크/경로)

- 데이터(입력): `data/step2_raw_text_sample.csv` (또는 통합 Raw)
- 품질 리포트: `out/step2_quality_report.md`, `out/step2_quality_report.json`
- 전처리 산출물: `out/step2_preprocessed.csv`, `out/step2_preprocess_summary.json`
- EDA 산출물: `out/eda_length_hist.png`, `out/eda_top_keywords.csv`, `out/eda_sentiment_distribution.png`, `out/eda_topic_distribution.png`
- 통합 EDA 리포트: `out/step2_eda_report.md`
- 라벨 가이드: `라벨링가이드_v1.md`


