# 2026-01-07 (수) — Step2 pipeline v1 기준선 고정

- 작성시각: 2026-01-07 (수)

## 해결하고자 한 문제
- Step2 파이프라인을 **기준선(v1)** 으로 고정하기 위해, 현재 Raw(약 1000건)를 기준으로 **quality_check → preprocess → EDA**를 재실행하고 `out/` 산출물이 모두 최신 상태인지 검증한다.
- 중복 제거 수치, 전처리 후 row 수, 도메인(provider_type)/source_type 분포가 리포트에 명확히 반영되었는지 점검한다.
- 이후 수치 변경 여부를 추적할 수 있도록 **스냅샷 + 해시 기반 로그**를 남긴다.

## 오늘까지 해결된 것(완료)
- **파이프라인 재실행(현재 Raw=1000 기준)**
  - 실행 입력 Raw: `data/step2_raw_text_expanded.csv` (1000 rows)
  - 실행 단계:
    - `scripts/step2_quality_check.py --raw data/step2_raw_text_expanded.csv`
    - `scripts/step2_preprocess_text.py --raw data/step2_raw_text_expanded.csv`
    - `scripts/step2_eda_text.py`
    - `scripts/step2_generate_eda_report.py`

- **리포트 수치 반영 점검(요구사항 3)**
  - 중복 후보(quality): **513(원문)/427(dedup_key)**
  - 전처리 후 rows: **570**
  - 전처리 dedup 제거 건수: **420**
  - 분포(quality/EDA 공통):
    - 도메인(provider_type): HOSPITAL 375 / CHECKUP_CENTER 317 / PHARMACY 308
    - source_type: review 300 / inquiry 300 / faq 200 / dataset 100 / notice 100

- **Raw 스키마 호환 보정(확장 데이터 일부가 `raw_text`에만 값이 있고 `text`, `text_id`가 비어있는 문제)**
  - 품질 체크에서:
    - `text` 공백을 `raw_text`로 보정 후 필수 컬럼 결측/공백 행: **0**
    - 보정 수치: `filled_text_from_raw_text=588`, `generated_text_id=588`
  - 전처리에서:
    - `text`/`raw_text` coalesce 및 `text_id` 결정론적 생성(`sha1` 기반) 적용 후 진행

- **산출물 최신성 확인(요구사항 2)**
  - `out/step2_quality_report.md`, `out/step2_quality_report.json`
  - `out/step2_preprocess_summary.json`
  - `out/step2_eda_report.md`

- **Step2 기준선(v1) 스냅샷/로그 고정(요구사항 4)**
  - 실행: `py -3 scripts/step2_freeze_pipeline_v1.py --tag step2_pipeline_v1 --raw data/step2_raw_text_expanded.csv`
  - 생성/갱신:
    - Raw 복사본: `data/baselines/step2_pipeline_v1_raw.csv`
    - 스냅샷 폴더: `out/step2_pipeline_v1/`
    - manifest: `out/step2_pipeline_v1/manifest.json`
    - 고정 로그: `docs/step2_pipeline_v1_log.md`
  - 기존(350건 기준) 로그는 보존용으로 복사:
    - `docs/step2_pipeline_v1_log_legacy_350_20260107.md`

## 아직 해결되지 않은 것(미완료/리스크)
- **입력 Raw 자체(`data/step2_raw_text_expanded.csv`)에는 일부 행에서 `text`/`text_id`가 비어 있고 `raw_text`에만 내용이 존재**한다.
  - 현재 v1 파이프라인은 이를 자동 보정하도록 수정했으나, 향후 Raw를 재생성/교체할 경우 동일 규칙을 유지해야 수치가 변하지 않는다.

## 향후 개발을 위한 컨텍스트(메모)
- v1 기준선 검증은 아래 2개를 비교하면 된다.
  - `docs/step2_pipeline_v1_log.md` (요약 수치 + 파일 해시)
  - `out/step2_pipeline_v1/manifest.json` (산출물별 SHA256)
- 기준선 변경이 필요하면 **기존 v1은 유지**하고 `step2_pipeline_v2` 같은 새 태그로 스냅샷을 생성한다.


