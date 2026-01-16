# 2026-01-12 Step3 실행/평가 로그(오늘)

## 실행 요약
- 실행 커맨드
  - `py -3 scripts\step3_prompt_test.py --n 5`
  - `py -3 scripts\step3_prompt_pipeline.py --n 8 --enable_classification`
- 실행 결과: **결제/쿼터 정상화 후 live 응답 생성 성공**
  - 모델: `gpt-4o-mini`
  - 결과물은 `out/`에 저장됨(아래 참고)

## 산출물(out/)
- `out/step3_prompt_test_samples.md`
- `out/step3_prompt_test_results.jsonl`
- `out/step3_pipeline_samples.md`
- `out/step3_pipeline_results.jsonl`

## 채점(루브릭 기반) — 완료(샘플 3~5개)
- 채점 문서: `docs/step3_prompt_score_sheet.md`

### 1) 리뷰 요약(review_summary) (샘플 1~5)
| 샘플ID | 정확도 | 간결성 | 감정근거 | 형식(JSON) | 합계 | 코멘트 |
|---|---:|---:|---:|---:|---:|---|
| 1 | 2 | 2 | 2 | 2 | 8 | OK |
| 2 | 2 | 1 | 2 | 2 | 7 | key_points 1개로 부족 |
| 3 | 1 | 2 | 1 | 2 | 6 | 입력 근거 약한 추정 포함 |
| 4 | 2 | 2 | 2 | 2 | 8 | OK |
| 5 | 2 | 2 | 2 | 2 | 8 | OK |

### 2) 대화 요약(dialog_summary) (샘플 1~3)
| 샘플ID | 요약품질 | intent | response | next_actions | 형식(JSON) | 합계 | 코멘트 |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 2 | 2 | 2 | 1 | 2 | 9 | next_actions 근거를 더 명시하면 좋음 |
| 2 | 2 | 2 | 2 | 1 | 2 | 9 | next_actions 일반적 |
| 3 | 2 | 2 | 2 | 1 | 2 | 9 | next_actions 근거 문구 추가 권장 |

### 3) 키워드 추출(keyword_extraction) (샘플 1~3)
| 샘플ID | 관련성 | 중복/일반어제거 | 커버리지 | 형식(JSON) | 합계 | 코멘트 |
|---|---:|---:|---:|---:|---:|---|
| 1 | 2 | 2 | 1 | 2 | 7 | 5~10개 요구사항 미달(3개) |
| 2 | 2 | 2 | 1 | 2 | 7 | 5~10개 요구사항 미달 |
| 3 | 2 | 2 | 1 | 2 | 7 | 5~10개 요구사항 미달 |

### 4) 텍스트 분류(text_classification) (샘플 1~3)
| 샘플ID | source_type | provider_type | sentiment | topic | 형식(JSON) | 합계 | 코멘트 |
|---|---:|---:|---:|---:|---:|---:|---|
| 1 | 2 | 0 | 2 | 2 | 2 | 8 | provider_type는 입력 힌트 부족으로 unknown |
| 2 | 2 | 0 | 1 | 2 | 2 | 7 | inquiry는 감정/기관유형 근거 약함 |
| 3 | 2 | 0 | 2 | 2 | 2 | 8 | provider_type는 입력 힌트 부족으로 unknown |

