# CareLog AI — 의료 서비스 NLP 파이프라인

**프로젝트 기간**: 2025-12-29 ~ 2026-01-16  
**버전**: 1.0  
**최종 업데이트**: 2026-01-16

---

## 📋 프로젝트 개요

의료 서비스(병원/검진센터/약국) 관련 텍스트를 자동으로 분석하고, 사용자와 대화하는 AI 챗봇 시스템

### 주요 기능
1. ✅ **텍스트 분류**: 리뷰/문의/FAQ/공지 자동 분류 (4가지 축)
2. ✅ **요약 생성**: 리뷰 요약, 대화 요약
3. ✅ **키워드 추출**: 핵심 키워드 5~10개 자동 추출 (후처리 포함)
4. ✅ **챗봇**: 예약/안내 중심 대화형 AI (Streamlit)

---

## 🚀 빠른 시작

### 1. 설치
```bash
# 프로젝트 클론
git clone <repository_url>
cd "CareLog AI"

# 의존성 설치
pip install -r requirements.txt
pip install -r requirements-demo.txt
```

### 2. OpenAI API 키 설정
`.env` 파일 생성:
```
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 3. 챗봇 데모 실행
```bash
py -3 -m streamlit run demo\streamlit_app.py --server.headless=true
```

접속: `http://localhost:8501/`

---

## 📁 프로젝트 구조

```
CareLog AI/
├── data/                      # 원본 데이터
│   ├── crawling/             # 크롤링 데이터 (리뷰)
│   └── aihub/                # Aihub 데이터셋 (대화)
├── out/                       # 전처리 결과 및 테스트 출력
│   ├── step2_pipeline_v2/    # Step 2 전처리 결과 (1,000행)
│   ├── step3_prompt_test_samples.md
│   ├── step3_pipeline_samples.md
│   └── step3_pipeline_results.jsonl
├── prompts/                   # 프롬프트 정의
│   ├── step3_text_classification.md
│   ├── step3_review_summary.md
│   ├── step3_dialog_summary.md
│   ├── step3_keyword_extraction.md
│   └── step4_chatbot.md
├── scripts/                   # 실행 스크립트
│   ├── step2_expand_to_1000.py
│   ├── step3_prompt_test.py
│   └── step3_prompt_pipeline.py
├── demo/                      # 데모 UI
│   ├── streamlit_app.py      # ✅ Streamlit 챗봇 (최종)
│   └── gradio_app.py         # (호환 이슈로 미사용)
├── docs/                      # 문서
│   ├── step4_완료보고.md
│   ├── step4_user_guide.md
│   ├── step4_project_report.md
│   ├── step4_demo_test_cases.md
│   └── 2026-01-16_멘토피드백_기록.md
├── requirements.txt           # 기본 의존성
├── requirements-demo.txt      # 데모 전용 (Streamlit)
└── .env                       # OpenAI API 키 (커밋 금지)
```

---

## 📊 데이터셋

### 전처리 완료 데이터
- **파일**: `out/step2_pipeline_v2/step2_preprocessed.csv`
- **크기**: 1,000행
- **구성**:
  - 크롤링 리뷰: 200개
  - Aihub 대화: 400개
  - GPT-4o-mini 증강: 400개

### 라벨
- `source_type`: review, inquiry, faq, dataset, notice
- `provider_type`: HOSPITAL, CHECKUP_CENTER, PHARMACY
- `sentiment_label`: positive, neutral, negative
- `topic_label`: reservation, prep, explain, wait, staff, ...

---

## 🛠️ 기술 스택

| 구분 | 기술 | 버전 |
|------|------|------|
| **언어** | Python | 3.11 |
| **UI** | Streamlit | 1.53.0 |
| **LLM API** | OpenAI | 1.59.7 (gpt-4o-mini) |
| **데이터** | pandas, BeautifulSoup4 | 2.2.3, 4.12.3 |
| **환경** | python-dotenv | 1.0.1 |

---

## 📈 개발 단계

### Step 1: 프로젝트 기획 (2025-12-29 ~ 2026-01-04)
- ✅ 목표 정의 및 데이터 소스 조사
- ✅ Python 환경 구축

### Step 2: 데이터 수집 및 전처리 (2026-01-06 ~ 2026-01-11)
- ✅ 네이버 플레이스 크롤링 (200개)
- ✅ Aihub 데이터셋 활용 (400개)
- ✅ GPT-4o-mini 기반 증강 (400개)
- ✅ 전처리 파이프라인 구축

### Step 3: 프롬프트 엔지니어링 (2026-01-12 ~ 2026-01-15)
- ✅ 프롬프트 4종 설계 (분류, 리뷰 요약, 대화 요약, 키워드)
- ✅ v0 → v1 개선 (평가 기반)
- ✅ 자동화 파이프라인 + 후처리

### Step 4: 데모 제작 및 마무리 (2026-01-16)
- ✅ Streamlit 챗봇 UI 구현
- ✅ OpenAI API 통합
- ✅ 문서화 (가이드, 보고서, 테스트 케이스)

---

## 💡 주요 성과

### 정량적 성과
- 전처리 데이터: **1,000개**
- 프롬프트 개발: **5종**
- 프롬프트 개선: **v0 → v1**
- 문서화: **10개 이상**

### 정성적 성과
- 프롬프트 엔지니어링 경험 축적
- 전처리 → 프롬프트 → 데모 전 과정 경험
- 기술적 문제 해결 (Gradio → Streamlit 전환)

---

## 🎯 사용 방법

### 챗봇 데모
```bash
# 실행
py -3 -m streamlit run demo\streamlit_app.py --server.headless=true

# 접속
http://localhost:8501/
```

### 분석 스크립트
```bash
# 개별 프롬프트 테스트 (5개 샘플)
py -3 scripts\step3_prompt_test.py --n 5

# 통합 파이프라인 (8개 샘플, 분류 포함)
py -3 scripts\step3_prompt_pipeline.py --n 8 --enable_classification
```

---

## ⚠️ 주의사항

### 개인정보 보호
- 주민번호, 계좌번호 등 민감한 개인정보 입력 금지
- 대화 내용은 OpenAI API 서버로 전송됨

### 의료적 조언 제한
- 본 챗봇은 **안내 목적**
- 의료적 진단/처방은 반드시 전문가 상담
- 응급 상황 시 119 또는 응급실 즉시 연락

### API 사용량
- OpenAI API는 유료 (사용량 주의)
- 쿼터 초과 시 서비스 제한

---

## 📚 문서

- **사용자 가이드**: `docs/step4_user_guide.md`
- **프로젝트 보고서**: `docs/step4_project_report.md`
- **완료 보고**: `docs/step4_완료보고.md`
- **테스트 케이스**: `docs/step4_demo_test_cases.md`

---

## 🔮 향후 계획

### 단기 (1~2개월)
- [ ] 챗봇에 분석 기능 통합
- [ ] RAG 기반 지식베이스 연동
- [ ] Docker 컨테이너화
- [ ] Streamlit Cloud 배포

### 중기 (3~6개월)
- [ ] 다국어 지원 (영어/일본어)
- [ ] 음성 인터페이스 (STT/TTS)
- [ ] 다중 에이전트 시스템

### 장기 (6개월 이상)
- [ ] 실제 의료 기관 파일럿 테스트
- [ ] 예약 시스템 API 연동
- [ ] 모바일 앱 개발

---

## 🤝 기여

본 프로젝트는 학습 목적으로 개발되었습니다.  
이슈 및 피드백은 GitHub Issues를 이용해 주세요.

---

## 📝 라이선스

MIT License (또는 프로젝트 정책에 따라 변경)

---

## 👥 팀

**CareLog AI 프로젝트팀**

- 개발: (이름)
- 멘토: (이름)
- 감사: OpenAI, Aihub

---

**최종 업데이트**: 2026-01-16 21:20 KST
