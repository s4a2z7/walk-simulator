# Step 3 — 통합 파이프라인 실행 결과(샘플)

- generated_at(UTC): `2026-01-16T10:33:24.401975+00:00`
- input: `C:/VibeCoding/CareLog AI/out/step2_preprocessed.csv`
- model: `gpt-4o-mini`
- temperature: `0.2`
- mode: `live`
- enable_classification: `True`

## 샘플 1 — `T0001`

- source_type(gt): `review` / provider_type(gt): `HOSPITAL`

입력(text):

- 접수부터 안내까지 친절해서 좋았어요.

### 출력(text_classification) raw

```json
{
  "source_type": "review",
  "provider_type": "unknown",
  "sentiment_label": "positive",
  "topic_label": "staff"
}
```

### 출력(review_summary) raw

```json
{
  "summary": "접수와 안내 서비스가 친절했다.",
  "key_points": ["접수 서비스가 친절함", "안내 서비스가 좋음"],
  "sentiment_guess": "positive"
}
```

### 출력(keyword_extraction) raw

```json
{
  "keywords": ["접수", "안내", "친절", "접수 안내", "친절한 안내"]
}
```

### keyword_extraction 최종 키워드(postprocessed)

```json
{"keywords": ["접수", "안내", "친절", "접수 안내", "친절한 안내"]}
```

## 샘플 2 — `T0007`

- source_type(gt): `inquiry` / provider_type(gt): `HOSPITAL`

입력(text):

- 오늘 진료 예약 가능한 시간대가 있나요?

### 출력(text_classification) raw

```json
{
  "source_type": "inquiry",
  "provider_type": "unknown",
  "sentiment_label": "unknown",
  "topic_label": "reservation"
}
```

### 출력(dialog_summary) raw

```json
{
  "summary": "사용자가 오늘 진료 예약 가능한 시간대를 문의했습니다. 상담원이 관련 정책과 가능한 시간대를 확인 후 답변하겠다고 했습니다.",
  "user_intent": "오늘 진료 예약 가능한 시간대 확인",
  "assistant_response": "안내드립니다. 관련 정책/가능 시간대를 확인 후 답변드릴게요.",
  "next_actions": ["가능한 시간대 확인"]
}
```

### 출력(keyword_extraction) raw

```json
{
  "keywords": ["진료", "예약", "시간대", "가능한 시간대", "진료 예약"]
}
```

### keyword_extraction 최종 키워드(postprocessed)

```json
{"keywords": ["진료", "예약", "시간대", "가능한 시간대", "진료 예약"]}
```

## 샘플 3 — `FAQ_HOSP_0001`

- source_type(gt): `faq` / provider_type(gt): `HOSPITAL`

입력(text):

- 예약 변경은 진료 시작 1시간 전까지 가능하며, 홈페이지에서 직접 변경하실 수 있습니다.

### 출력(text_classification) raw

```json
{
  "source_type": "faq",
  "provider_type": "unknown",
  "sentiment_label": "neutral",
  "topic_label": "reservation"
}
```

### 출력(keyword_extraction) raw

```json
{
  "keywords": ["예약 변경", "진료 시작", "1시간 전", "홈페이지", "직접 변경"]
}
```

### keyword_extraction 최종 키워드(postprocessed)

```json
{"keywords": ["예약 변경", "진료 시작", "1시간 전", "홈페이지", "직접 변경"]}
```

## 샘플 4 — `FAQ_PHARM_0001`

- source_type(gt): `notice` / provider_type(gt): `PHARMACY`

입력(text):

- 일반의약품은 건강보험 적용 대상이 아닙니다.

### 출력(text_classification) raw

```json
{
  "source_type": "faq",
  "provider_type": "unknown",
  "sentiment_label": "neutral",
  "topic_label": "other"
}
```

### 출력(keyword_extraction) raw

```json
{
  "keywords": ["일반의약품", "건강보험", "적용", "대상", "건강보험 적용"]
}
```

### keyword_extraction 최종 키워드(postprocessed)

```json
{"keywords": ["일반의약품", "건강보험", "적용", "건강보험 적용", "아닙니다"]}
```

## 샘플 5 — `AIHUB_00001_475bf980`

- source_type(gt): `dataset` / provider_type(gt): `HOSPITAL`

입력(text):

- 진료비는 어떻게 결제하나요?

### 출력(text_classification) raw

```json
{
  "source_type": "inquiry",
  "provider_type": "unknown",
  "sentiment_label": "unknown",
  "topic_label": "price"
}
```

### 출력(keyword_extraction) raw

```json
{
  "keywords": ["진료비", "결제", "결제 방법", "진료비 결제", "어떻게 결제하나요"]
}
```

### keyword_extraction 최종 키워드(postprocessed)

```json
{"keywords": ["진료비", "결제", "결제 방법", "진료비 결제", "어떻게 결제하나요"]}
```
