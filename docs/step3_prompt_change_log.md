# Step 3 — 프롬프트 변경 로그(템플릿)

## 목적/원칙
- “왜 바꿨는지, 무엇이 좋아졌는지”를 **루브릭 점수/실패 케이스**로 증명한다.
- 프롬프트 수정은 한 번에 1~2개 포인트만(원인-결과 추적 가능하게).

---

## 변경 기록

### 2026-01-12
- **대상 프롬프트**
  - [ ] `prompts/step3_review_summary.md`
  - [ ] `prompts/step3_dialog_summary.md`
  - [ ] `prompts/step3_keyword_extraction.md`
  - [ ] `prompts/step3_text_classification.md`
- **변경 요약(한 줄)**
  - (오늘) OpenAI 결제 후 live 평가 완료(프롬프트 내용 변경 없음)
- **변경 상세**
  - 무엇을 바꿈:
    - 프롬프트 자체는 변경하지 않음
  - 바꾼 이유(관측된 실패):
    - (초기) 모델 호출이 429(insufficient_quota)로 실패했으나, 결제 후 재실행하여 출력(JSON) 확보
  - 기대 효과:
    - (다음 실행 가능 시) 루브릭/스코어 시트 기반으로 정상 평가 및 반복 개선 진행
- **테스트 조건**
  - 입력 샘플: (예: `out/step2_preprocessed.csv` 중 5개)
  - 모델/파라미터: (예: gpt-4o-mini, temp=0.2)
- **결과(스코어 시트 요약)**
  - 변경 전 점수:
  - 변경 후 점수:
  - 실패 케이스/잔존 이슈:
    - 키워드 추출이 5~10개 요구사항을 자주 만족하지 못함(개수 제약 강화 필요)
    - 분류(provider_type)는 입력 힌트가 없으면 unknown으로 나옴(정책상 타당)

---

### 2026-01-16
- **대상**
  - [x] `prompts/step3_keyword_extraction.md`
  - [x] `prompts/step3_review_summary.md`
  - [x] `prompts/step3_dialog_summary.md`
  - [x] `scripts/step3_prompt_pipeline.py` (키워드 후처리)
- **변경 요약(한 줄)**
  - 키워드/리뷰/대화 프롬프트 제약 강화 + 통합 파이프라인에서 **키워드 자동 정제(일반어 제거/최소 5개 보장)** 추가
- **변경 상세**
  - 무엇을 바꿈:
    - 키워드: 5~10개 강제, 일반어 제외 규칙 강화
    - 리뷰: `key_points` 최소 2개 강제
    - 대화: 근거 없는 사실 추가 금지, next_actions 근거 기반 강화
    - 파이프라인: keyword_extraction 결과에 대해 `postprocess`/`final_keywords` 산출(일반어 제거 + 부족분 입력 기반 보충)
  - 바꾼 이유(관측된 실패):
    - 키워드가 3개만 나오거나, `가능` 같은 일반어가 섞이는 케이스
    - 리뷰 요약에서 key_points 1개로 떨어지는 케이스
    - 대화요약에서 입력에 없는 사실을 요약에 섞는 케이스
  - 기대 효과:
    - 자동화 파이프라인 출력이 “항상 5~10개 키워드”를 만족하고, 일반어/중복이 줄어듦
- **테스트 조건**
  - 실행:
    - `py -3 scripts\\step3_prompt_test.py --n 5`
    - `py -3 scripts\\step3_prompt_pipeline.py --n 8 --enable_classification`
- **결과(스코어 시트 요약)**
  - 문서: `docs/2026-01-16_step3_prompt_score_sheet_v1.md`
  - 잔존 이슈:
    - 키워드 내 의미 중복(예: “길다/너무 길다/대기/시간”)은 추가 개선 여지
