# Step 2 — AI Hub 의료/상담 데이터셋 다운로드 및 변환 가이드

**목표**: AI Hub에서 의료/상담/QnA 데이터셋 **150건 이상** 확보 후 프로젝트 CSV 스키마로 변환

---

## 1. AI Hub 접속 및 회원가입

### 1.1 AI Hub 접속
- URL: [https://aihub.or.kr/](https://aihub.or.kr/)
- 회원가입 → 로그인

### 1.2 데이터셋 이용 약관 확인
- AI Hub 데이터는 **비상업적 연구/교육 목적으로 제공**됩니다.
- 출처 표기(`source_type=dataset`, `provider_name=AI Hub`) 필수

---

## 2. 추천 데이터셋(의료/상담/헬스케어)

### 2.1 한국어 대화(공공/민원)
- **키워드**: "한국어 대화", "공공 민원", "상담"
- **규모**: 50만 건 이상
- **내용**: 소상공인 및 공공 민원 10개 분야 대화
- **형식**: JSON/Excel
- **추천 이유**: 예약/문의 유형 텍스트 포함

### 2.2 의료 AI 데이터
- **키워드**: "의료", "병원", "건강", "진료"
- **내용**: 의료 상담/진료 기록/FAQ
- **주의**: 개인정보 비식별화 확인 필수

### 2.3 헬스케어 QnA
- **키워드**: "헬스케어", "건강 상담", "의료 질의응답"
- **내용**: 건강/의료 관련 질문-답변 쌍
- **형식**: JSON/CSV

---

## 3. 다운로드 절차

### 3.1 데이터셋 검색
1. AI Hub 로그인 후 상단 검색창 클릭
2. 키워드 입력: "의료", "상담", "QnA", "헬스케어", "공공 민원"
3. 검색 결과에서 적합한 데이터셋 선택

### 3.2 데이터셋 신청
1. 데이터셋 상세 페이지 → "데이터 신청" 버튼 클릭
2. 이용 목적: "AI 챗봇 연구/교육용"
3. 승인 대기(일반적으로 **즉시~1일 이내** 승인)

### 3.3 다운로드
1. 승인 후 "다운로드" 버튼 활성화
2. 파일 형식: JSON/Excel/CSV 중 선택
3. 다운로드 위치: `data/aihub_download/` (프로젝트 내 신규 폴더)

**권장 다운로드 구조**:
```
data/
├─ aihub_download/
│  ├─ conversation_data.json      (한국어 대화 데이터)
│  ├─ medical_qna.xlsx            (의료 QnA 데이터)
│  └─ healthcare_faq.csv          (헬스케어 FAQ)
```

---

## 4. 프로젝트 CSV 스키마로 변환

### 4.1 변환 스크립트 실행
다운로드 받은 AI Hub 데이터를 프로젝트 스키마로 변환:

```powershell
# JSON 파일 변환
py -3 .\scripts\step2_convert_aihub_to_csv.py --input data\aihub_download\conversation_data.json --output data\aihub_converted.csv --format json

# Excel 파일 변환
py -3 .\scripts\step2_convert_aihub_to_csv.py --input data\aihub_download\medical_qna.xlsx --output data\aihub_converted.csv --format excel
```

### 4.2 프로젝트 스키마 확인
변환 스크립트는 아래 필수 컬럼을 자동 생성합니다:

| 컬럼 | 예시 값 | 설명 |
|---|---|---|
| `text_id` | `AIHUB_T0001` | AI Hub 데이터 ID |
| `provider_type` | `HOSPITAL` | 추론 또는 기본값 |
| `source_type` | `dataset` | AI Hub는 `dataset` 고정 |
| `provider_name` | `AI Hub` | 고정값 |
| `source_url` | `https://aihub.or.kr/...` | 데이터셋 URL |
| `created_at` | `2025-01-05T10:00:00Z` | 변환 시각 |
| `text` | `예약 가능한 시간대가...` | 실제 텍스트 |

---

## 5. 병합 및 품질 체크

### 5.1 Raw 데이터 병합
```powershell
# AI Hub 데이터 + 웹 수집 + 기존 샘플 병합
py -3 .\scripts\step2_merge_raw_text.py
```

출력: `data/step2_raw_text_merged.csv`

### 5.2 품질 체크
```powershell
py -3 .\scripts\step2_quality_check.py --raw .\data\step2_raw_text_merged.csv
```

출력:
- `out/step2_quality_report.json`
- `out/step2_quality_report.md`

**체크 항목**:
- ✅ 필수 컬럼 누락
- ✅ 결측/중복
- ✅ PII 탐지(AI Hub는 비식별화 완료되어 있어야 함)
- ✅ 텍스트 길이/분포

---

## 6. 목표 건수 달성 확인

### 6.1 목표 분배(350건)
| 소스 | 목표 건수 | 비고 |
|---|---:|---|
| AI Hub 데이터셋 | 150 | 이번 단계 |
| 웹 수집(FAQ/안내) | 200 | 다음 단계 |
| 합계 | **350** | |

### 6.2 도메인 분포 확인
품질 리포트(`step2_quality_report.md`)에서 도메인 분포 확인:
- HOSPITAL: 45% (158건)
- PHARMACY: 35% (123건)
- CHECKUP_CENTER: 20% (69건)

---

## 7. 주의사항 및 리스크

### 7.1 라이선스/출처 표기
- AI Hub 데이터는 **출처 표기 필수**
- `provider_name=AI Hub`, `source_type=dataset` 자동 삽입됨

### 7.2 개인정보 보호
- AI Hub는 "비식별화 완료" 데이터를 제공하지만, **재확인 권장**
- 품질 체크에서 PII 탐지 시 전처리 단계에서 마스킹

### 7.3 데이터 품질
- AI Hub 데이터는 **검증된 고품질 데이터**이지만, 프로젝트 도메인(병원/약국/검진센터)과 불일치 시 `provider_type` 수동 보정 필요
- 변환 스크립트는 텍스트 내 키워드(병원/약국/검진)로 `provider_type` 추론

---

## 8. 트러블슈팅

### 8.1 다운로드 승인이 안 될 때
- 이용 목적을 "연구/교육용 AI 챗봇 개발"로 명확히 기재
- 1~2일 대기 후 재시도

### 8.2 변환 스크립트 에러
- JSON 구조가 예상과 다를 경우: `scripts/step2_convert_aihub_to_csv.py` 열어서 매핑 수동 조정
- Excel 시트명 확인: `--sheet_name` 파라미터 추가

### 8.3 텍스트가 너무 긴 경우
- AI Hub 데이터는 대화형이 많아 텍스트가 긴 경우 있음
- 전처리 단계(`step2_preprocess_text.py`)에서 자동으로 문장 단위 분리 또는 최대 길이 제한 가능

---

## 9. 체크리스트

- [ ] AI Hub 회원가입 완료
- [ ] 의료/상담 데이터셋 검색("한국어 대화", "의료 QnA" 등)
- [ ] 데이터셋 신청 및 승인
- [ ] 데이터 다운로드(`data/aihub_download/`)
- [ ] 변환 스크립트 실행(`step2_convert_aihub_to_csv.py`)
- [ ] 변환 결과 확인(`data/aihub_converted.csv`)
- [ ] 병합 스크립트 실행(`step2_merge_raw_text.py`)
- [ ] 품질 체크 실행(`step2_quality_check.py`)
- [ ] 품질 리포트 확인(150건 이상 확보 여부)
- [ ] 전처리 → EDA 파이프라인 실행

---

**다음 단계**: 150건 확보 후 **웹 수집(200건)** 진행 → 최종 350건 달성

