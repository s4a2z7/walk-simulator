# Step2 라벨 표준(허용값) — sentiment_label / topic_label

본 문서는 Step2 데이터(`review / inquiry / faq / notice / dataset`)의 라벨 컬럼 표준 허용값을 정의합니다.  
상세 정의/예시는 `라벨링가이드_v1.md`를 따르며, **코드의 품질체크(quality_check) 허용값 검증 기준**으로도 사용합니다.

---

## 1) sentiment_label (감정 라벨)

### 1.1 허용값(표준)
- `positive`
- `neutral`
- `negative`

### 1.2 비고(운영 규칙)
- 결측/공백은 품질 체크에서 결측으로 집계합니다.
- 허용값 집합 외 값은 “허용값 위반”으로 집계합니다.

---

## 2) topic_label (주제 라벨)

### 2.1 허용값(표준)
- `reservation`
- `policy`
- `location`
- `opening_hours`
- `prep`
- `pickup`
- `wait`
- `staff`
- `price`
- `explain`
- `process`
- `clean`
- `speed`
- `other`

### 2.2 비고(운영 규칙)
- 결측/공백은 품질 체크에서 결측으로 집계합니다.
- 허용값 집합 외 값은 “허용값 위반”으로 집계합니다.
- `other`는 최후 수단(가능하면 상위 카테고리로 매핑)입니다.

---

## 3) (선택) 룰 기반 자동 라벨링(임시 보완)

목적: 라벨 결측을 임시로 채워 EDA/모델링의 공백을 줄이기 위함(정답 라벨 보증 아님)

- **적용 범위(권장)**: `sentiment_label`/`topic_label`이 결측/공백인 경우에만 채움
- **리포트 표기(필수)**: 자동 보완 건수(`filled_*`)는 리포트에 반드시 명시

참고 구현:
- `scripts/step2_autolabel_rules.py`
- `scripts/step2_label_standards.py` (공용 규칙/허용값)


