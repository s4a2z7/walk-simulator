# Step2 파이프라인 기준선(v1) 고정 로그 — step2_pipeline_v1

- **고정 시각(UTC)**: 2026-01-07T11:39:23.129242+00:00
- **Raw 기준 파일**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/data/step2_raw_text_sample.csv`
- **Raw 기준 복사본**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/data/baselines/step2_pipeline_v1_raw.csv`
- **Raw SHA256**: `8a2da48abaecc2e8f16acd9da9aeb316c10a6a57b7e0149d021356333c8fa499`

## 1) 기준선 요약
- **Raw rows**: 350
- **dup_text(원문 중복 후보)**: 29
- **dedup_key 중복 후보**: 27
- **After preprocess rows**: 323
- **dedup 제거 건수(preprocess)**: 27

## 2) 분포(기준선)

### 2.1 provider_type 분포(Raw)
- HOSPITAL: 150
- CHECKUP_CENTER: 107
- PHARMACY: 93

### 2.2 source_type 분포(Raw)
- faq: 111
- review: 87
- inquiry: 57
- dataset: 51
- notice: 44

## 3) 스냅샷(out/) 산출물 및 해시

- **스냅샷 폴더**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/out/step2_pipeline_v1`
- **Manifest**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/out/step2_pipeline_v1/manifest.json`

| 파일 | sha256 |
|---|---|
| `eda_length_hist.png` | `d7ce1e42a602ab13668cd167ccb405eb8c363c7d6169187e0301ee276e10cad1` |
| `eda_sentiment_distribution.png` | `b7dc519d6715ea05fb5c2dfa4457751738306e4f93221abe5a13e67dc4c676c2` |
| `eda_top_keywords.csv` | `362cac97f110ac89ac45e44c38cce586fb8c045f6a5cf8ec5e4cc0e3a694ec36` |
| `eda_topic_distribution.png` | `8c1f52dcc1781e59857ecdcf05372c29e4b204569200ad2e1f76418a5bc767d9` |
| `step2_eda_report.md` | `d87f9c22bd71a0c03efd7a5c607856d14d4dce188b48f38e5eec2a72f57c2e1f` |
| `step2_preprocess_summary.json` | `ab9c5b1a32c0cc0c353eb7a832fc38834a4c40aa168dd5b82b2c0474383b5f8c` |
| `step2_preprocessed.csv` | `bba074fc81659ee7eb1414116589eb6ca7649c432697448138742aca13385121` |
| `step2_quality_report.json` | `477993ddc4a1f5bca9f2fcee623545c0deb16d8bf205a2c7e014f69eef5a1ee6` |
| `step2_quality_report.md` | `505e10b2c26ddd0270852ea55d7891b73510ae6054258272596298b79a1c74b4` |

## 4) 기준선(v1) 고정 선언

- 본 실행 결과를 **Step2 기준선(v1)** 으로 간주합니다.
- 이후 수치 변경(행 수/중복/분포 등)이 발생하면, 본 문서의 SHA256 및 `out/step2_pipeline_v1/manifest.json`과 비교하여 변경 여부를 확인합니다.
- 기준선 변경이 필요한 경우, **새 태그(step2_pipeline_v2 등)** 로 별도 스냅샷/로그를 생성합니다(기존 v1은 유지).
