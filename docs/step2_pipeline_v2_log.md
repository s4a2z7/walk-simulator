# Step2 파이프라인 기준선 고정 로그 — step2_pipeline_v2

- **고정 시각(UTC)**: 2026-01-07T12:22:08.644828+00:00
- **Raw 기준 파일**: `data/step2_raw_text_expanded_mg_700_300.csv`
- **Raw 기준 복사본**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/data/baselines/step2_pipeline_v2_raw.csv`
- **Raw SHA256**: `d1f7476808b4608efd5a10e41a429ecdd3e36af360e45d37f5f9dd688c1e0839`

## 1) 기준선 요약
- **Raw rows**: 1000
- **dup_text(원문 중복 후보)**: 515
- **dedup_key 중복 후보**: 431
- **After preprocess rows**: 566
- **dedup 제거 건수(preprocess)**: 424

## 2) 분포(기준선)

### 2.1 provider_type 분포(Raw)
- HOSPITAL: 380
- CHECKUP_CENTER: 320
- PHARMACY: 300

### 2.2 source_type 분포(Raw)
- inquiry: 302
- review: 301
- faq: 200
- dataset: 100
- notice: 97

## 3) 스냅샷(out/) 산출물 및 해시

- **스냅샷 폴더**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/out/step2_pipeline_v2`
- **Manifest**: `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/out/step2_pipeline_v2/manifest.json`

| 파일 | sha256 |
|---|---|
| `eda_length_hist.png` | `4a3e8d3becd679874a5695356aa0a75bfea71d74981a167946f222f16378b8e9` |
| `eda_sentiment_distribution.png` | `251752f979b7fd76761ccfd595d2425f6566fd5ead8ce32e39a5a13ec31256cb` |
| `eda_top_keywords.csv` | `f249dd4cc954dba7d78c683ba83db020dd6f0ed1dc8d201e1c9f1e6a63d2ca1a` |
| `eda_topic_distribution.png` | `f4371dd6a2b7363decdd4eb8b5b6d6fd2dfd2b67fa30301a1f1e40e195b5ed91` |
| `step2_eda_report.md` | `86a90427bd816312116d1e371217603ee79072713698ad95f2bc9effea48606f` |
| `step2_preprocess_summary.json` | `aad9c54c39f80571350a69913bf4bd4b3fe4400efde8a0e4102ee8eafe915ee1` |
| `step2_preprocessed.csv` | `6ff1d654b11d3b8616e514d0720052c708ba1758bdcbc7d5bbe18e6d90ac8819` |
| `step2_quality_report.json` | `a62a1560d43b958cf7e9467b2268daf70557981252d22ca590a8d0aab0e4d421` |
| `step2_quality_report.md` | `7b5a21126f8cb91724110cf550a488da3ef8d12026cee60e94e68789ffcee7cc` |

## 4) 기준선 고정 선언

- 본 실행 결과를 **step2_pipeline_v2 기준선**으로 간주합니다.
- 이후 수치 변경(행 수/중복/분포 등)이 발생하면, 본 문서의 SHA256 및 `C:/Users/cutep/OneDrive/바탕 화면/yurim251202/VibeCoding/CareLog AI/out/step2_pipeline_v2/manifest.json`과 비교하여 변경 여부를 확인합니다.
- 기준선 변경이 필요한 경우, **새 태그(step2_pipeline_v2 등)** 로 별도 스냅샷/로그를 생성합니다(기존 v1은 유지).
