"""
Step 2 파이프라인 v1(기준선) 고정 도구

목적:
- 현재 Raw(약 350건) + out/ 산출물을 스냅샷으로 보관
- 파일 해시(SHA256)와 핵심 지표를 로그로 남겨 이후 수치 변경 여부를 추적

사용 예:
  py -3 scripts/step2_freeze_pipeline_v1.py --tag step2_pipeline_v1
  py -3 scripts/step2_freeze_pipeline_v1.py --tag step2_pipeline_v2 --raw data/step2_raw_text_expanded_mg_700_300.csv
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW = ROOT / "data" / "step2_raw_text_sample.csv"
DEFAULT_BASELINE_DIR = ROOT / "data" / "baselines"


OUT_FILES = [
    "step2_quality_report.json",
    "step2_quality_report.md",
    "step2_preprocess_summary.json",
    "step2_preprocessed.csv",
    "eda_length_hist.png",
    "eda_top_keywords.csv",
    "eda_sentiment_distribution.png",
    "eda_topic_distribution.png",
    "step2_eda_report.md",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--tag", default="step2_pipeline_v1", help="snapshot tag")
    p.add_argument("--raw", default=str(DEFAULT_RAW), help="raw csv path")
    p.add_argument("--out_dir", default=None, help="snapshot output dir (default: out/{tag})")
    p.add_argument("--baseline_dir", default=str(DEFAULT_BASELINE_DIR), help="baseline raw storage dir (under data/)")
    p.add_argument("--log_md", default=None, help="log markdown path (default: docs/{tag}_log.md)")
    args = p.parse_args()

    tag = args.tag
    raw_path = Path(args.raw)
    out_dir = Path(args.out_dir) if args.out_dir else (ROOT / "out" / tag)
    baseline_dir = Path(args.baseline_dir)
    log_md = Path(args.log_md) if args.log_md else (ROOT / "docs" / f"{tag}_log.md")

    out_dir.mkdir(parents=True, exist_ok=True)
    baseline_dir.mkdir(parents=True, exist_ok=True)
    log_md.parent.mkdir(parents=True, exist_ok=True)

    # 1) Raw baseline copy
    baseline_raw = baseline_dir / f"{tag}_raw.csv"
    baseline_raw.write_bytes(raw_path.read_bytes())

    # 2) out/ snapshot copy
    manifest = {
        "tag": tag,
        "generated_at": now_iso(),
        "raw": {},
        "out": {},
    }

    manifest["raw"] = {
        "path": str(raw_path.as_posix()),
        "baseline_copy": str(baseline_raw.as_posix()),
        "sha256": sha256_file(baseline_raw),
        "bytes": baseline_raw.stat().st_size,
    }

    for name in OUT_FILES:
        src = ROOT / "out" / name
        if not src.exists():
            continue
        dst = out_dir / name
        dst.write_bytes(src.read_bytes())
        manifest["out"][name] = {
            "sha256": sha256_file(dst),
            "bytes": dst.stat().st_size,
        }

    (out_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 3) 핵심 지표 요약(리포트 JSON에서 읽기)
    quality_path = ROOT / "out" / "step2_quality_report.json"
    pre_sum_path = ROOT / "out" / "step2_preprocess_summary.json"

    quality = read_json(quality_path) if quality_path.exists() else {}
    pre_sum = read_json(pre_sum_path) if pre_sum_path.exists() else {}

    raw = quality.get("raw", {}) if isinstance(quality, dict) else {}
    provider_dist = raw.get("provider_type_distribution", {}) or {}
    source_dist = raw.get("source_type_distribution", {}) or {}

    pre_before = (pre_sum.get("before") or {}) if isinstance(pre_sum, dict) else {}
    pre_after = (pre_sum.get("after") or {}) if isinstance(pre_sum, dict) else {}

    # 4) Markdown 로그 작성
    md = []
    md.append(f"# Step2 파이프라인 기준선 고정 로그 — {tag}")
    md.append("")
    md.append(f"- **고정 시각(UTC)**: {manifest['generated_at']}")
    md.append(f"- **Raw 기준 파일**: `{raw_path.as_posix()}`")
    md.append(f"- **Raw 기준 복사본**: `{baseline_raw.as_posix()}`")
    md.append(f"- **Raw SHA256**: `{manifest['raw']['sha256']}`")
    md.append("")
    md.append("## 1) 기준선 요약")
    md.append(f"- **Raw rows**: {raw.get('rows')}")
    md.append(f"- **dup_text(원문 중복 후보)**: {raw.get('dup_raw_text')}")
    md.append(f"- **dedup_key 중복 후보**: {raw.get('dedup_key_duplicates')}")
    md.append(f"- **After preprocess rows**: {pre_after.get('rows')}")
    md.append(f"- **dedup 제거 건수(preprocess)**: {pre_after.get('dedup_removed')}")
    md.append("")
    md.append("## 2) 분포(기준선)")
    md.append("")
    md.append("### 2.1 provider_type 분포(Raw)")
    for k, v in provider_dist.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("### 2.2 source_type 분포(Raw)")
    for k, v in source_dist.items():
        md.append(f"- {k}: {v}")
    md.append("")
    md.append("## 3) 스냅샷(out/) 산출물 및 해시")
    md.append("")
    md.append(f"- **스냅샷 폴더**: `{out_dir.as_posix()}`")
    md.append(f"- **Manifest**: `{(out_dir / 'manifest.json').as_posix()}`")
    md.append("")
    md.append("| 파일 | sha256 |")
    md.append("|---|---|")
    for name, meta in sorted(manifest["out"].items()):
        md.append(f"| `{name}` | `{meta['sha256']}` |")
    md.append("")
    md.append("## 4) 기준선 고정 선언")
    md.append("")
    md.append(f"- 본 실행 결과를 **{tag} 기준선**으로 간주합니다.")
    md.append(f"- 이후 수치 변경(행 수/중복/분포 등)이 발생하면, 본 문서의 SHA256 및 `{(out_dir / 'manifest.json').as_posix()}`과 비교하여 변경 여부를 확인합니다.")
    md.append("- 기준선 변경이 필요한 경우, **새 태그(step2_pipeline_v2 등)** 로 별도 스냅샷/로그를 생성합니다(기존 v1은 유지).")
    md.append("")

    log_md.write_text("\n".join(md), encoding="utf-8")

    print("saved:")
    print(f"- {baseline_raw}")
    print(f"- {out_dir / 'manifest.json'}")
    print(f"- {log_md}")


if __name__ == "__main__":
    main()


