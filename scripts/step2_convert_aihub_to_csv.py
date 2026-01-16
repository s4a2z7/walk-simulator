"""
Step 2 - AI Hub 다운로드 데이터를 프로젝트 CSV 스키마로 변환

입력:
- data/aihub_download/*.json (AI Hub JSON 데이터)
- data/aihub_download/*.xlsx (AI Hub Excel 데이터)
- data/aihub_download/*.csv (AI Hub CSV 데이터)

출력:
- data/aihub_converted.csv (프로젝트 스키마에 맞춘 CSV)

필수 컬럼(프로젝트 스키마):
- text_id, provider_type, source_type, provider_name, text, source_url, created_at
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd


OUT_DIR = Path("data")
DEFAULT_OUT = OUT_DIR / "aihub_converted.csv"

# AI Hub 데이터는 "dataset" 고정
SOURCE_TYPE = "dataset"
PROVIDER_NAME = "AI Hub"

# 키워드 기반 provider_type 추론
_KW_HOSPITAL = re.compile(r"(병원|의원|내과|외과|이비인후과|정형외과|진료|의사|진찰)", re.IGNORECASE)
_KW_PHARMACY = re.compile(r"(약국|처방|조제|복약|약사)", re.IGNORECASE)
_KW_CHECKUP = re.compile(r"(검진|건강검진|검사|금식|준비사항)", re.IGNORECASE)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_text_id(text: str, idx: int) -> str:
    """AI Hub 데이터용 text_id 생성"""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]
    return f"AIHUB_{idx:05d}_{h}"


def _infer_provider_type(text: str) -> str:
    """텍스트 내용으로 provider_type 추론"""
    if _KW_HOSPITAL.search(text):
        return "HOSPITAL"
    if _KW_PHARMACY.search(text):
        return "PHARMACY"
    if _KW_CHECKUP.search(text):
        return "CHECKUP_CENTER"
    # 기본값(가장 많은 카테고리)
    return "HOSPITAL"


def convert_json(input_path: Path, source_url: str = "") -> pd.DataFrame:
    """
    AI Hub JSON 데이터를 프로젝트 스키마로 변환
    
    가정:
    - JSON 구조: [{"text": "...", ...}, ...] 또는 {"data": [{"text": "..."}, ...]}
    - "text", "question", "answer", "utterance" 등의 필드에서 텍스트 추출
    """
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # JSON 구조 자동 탐지
    if isinstance(data, dict):
        # {"data": [...]} 형태
        if "data" in data and isinstance(data["data"], list):
            records = data["data"]
        else:
            # 단일 레코드를 리스트로 감싸기
            records = [data]
    elif isinstance(data, list):
        records = data
    else:
        raise ValueError(f"Unsupported JSON structure in {input_path}")
    
    rows = []
    created_at = _now_iso()
    
    for idx, rec in enumerate(records, start=1):
        # 텍스트 추출(다양한 필드명 지원)
        text = None
        for field in ["text", "question", "answer", "utterance", "content", "sentence"]:
            if field in rec and rec[field]:
                text = str(rec[field]).strip()
                break
        
        if not text or len(text) < 3:
            continue
        
        # provider_type 추론
        provider_type = _infer_provider_type(text)
        
        rows.append({
            "text_id": _stable_text_id(text, idx),
            "provider_type": provider_type,
            "source_type": SOURCE_TYPE,
            "provider_name": PROVIDER_NAME,
            "text": text,
            "source_url": source_url if source_url else f"https://aihub.or.kr/dataset/{input_path.stem}",
            "created_at": created_at,
        })
    
    return pd.DataFrame(rows)


def convert_excel(input_path: Path, source_url: str = "", sheet_name: str | int = 0) -> pd.DataFrame:
    """
    AI Hub Excel 데이터를 프로젝트 스키마로 변환
    
    가정:
    - 첫 번째 시트(또는 지정 시트)에 데이터가 있음
    - "text", "question", "answer" 등의 컬럼 존재
    """
    df = pd.read_excel(input_path, sheet_name=sheet_name)
    
    # 텍스트 컬럼 자동 탐지
    text_col = None
    for col in ["text", "question", "answer", "utterance", "content", "sentence"]:
        if col in df.columns:
            text_col = col
            break
    
    if not text_col:
        raise ValueError(f"Cannot find text column in {input_path}. Available columns: {list(df.columns)}")
    
    rows = []
    created_at = _now_iso()
    
    for idx, row in df.iterrows():
        text = str(row[text_col]).strip()
        if not text or text == "nan" or len(text) < 3:
            continue
        
        provider_type = _infer_provider_type(text)
        
        rows.append({
            "text_id": _stable_text_id(text, idx + 1),
            "provider_type": provider_type,
            "source_type": SOURCE_TYPE,
            "provider_name": PROVIDER_NAME,
            "text": text,
            "source_url": source_url if source_url else f"https://aihub.or.kr/dataset/{input_path.stem}",
            "created_at": created_at,
        })
    
    return pd.DataFrame(rows)


def convert_csv_format(input_path: Path, source_url: str = "") -> pd.DataFrame:
    """
    AI Hub CSV 데이터를 프로젝트 스키마로 변환
    
    가정:
    - "text", "question", "answer" 등의 컬럼 존재
    """
    df = pd.read_csv(input_path)
    
    # 텍스트 컬럼 자동 탐지
    text_col = None
    for col in ["text", "question", "answer", "utterance", "content", "sentence"]:
        if col in df.columns:
            text_col = col
            break
    
    if not text_col:
        raise ValueError(f"Cannot find text column in {input_path}. Available columns: {list(df.columns)}")
    
    rows = []
    created_at = _now_iso()
    
    for idx, row in df.iterrows():
        text = str(row[text_col]).strip()
        if not text or text == "nan" or len(text) < 3:
            continue
        
        provider_type = _infer_provider_type(text)
        
        rows.append({
            "text_id": _stable_text_id(text, idx + 1),
            "provider_type": provider_type,
            "source_type": SOURCE_TYPE,
            "provider_name": PROVIDER_NAME,
            "text": text,
            "source_url": source_url if source_url else f"https://aihub.or.kr/dataset/{input_path.stem}",
            "created_at": created_at,
        })
    
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert AI Hub data to project CSV schema")
    parser.add_argument("--input", type=str, required=True, help="Input file path (JSON/Excel/CSV)")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUT), help="Output CSV path")
    parser.add_argument("--format", type=str, choices=["json", "excel", "csv"], required=True, help="Input format")
    parser.add_argument("--source_url", type=str, default="", help="AI Hub dataset URL (optional)")
    parser.add_argument("--sheet_name", type=str, default="0", help="Excel sheet name or index (default: 0)")
    args = parser.parse_args()
    
    input_path = Path(args.input)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    print(f"Converting {input_path} ({args.format}) to project CSV schema...")
    
    if args.format == "json":
        df = convert_json(input_path, args.source_url)
    elif args.format == "excel":
        sheet = int(args.sheet_name) if args.sheet_name.isdigit() else args.sheet_name
        df = convert_excel(input_path, args.source_url, sheet)
    elif args.format == "csv":
        df = convert_csv_format(input_path, args.source_url)
    else:
        raise ValueError(f"Unsupported format: {args.format}")
    
    if len(df) == 0:
        print("Warning: No records converted. Check input file structure.")
        return
    
    # 중복 제거(text 기준)
    before = len(df)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    after = len(df)
    
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")
    
    print(f"\nConversion complete!")
    print(f"- Input: {input_path}")
    print(f"- Output: {out_path}")
    print(f"- Records: {before} → {after} (removed {before - after} duplicates)")
    print(f"- Provider type distribution:")
    for ptype, count in df["provider_type"].value_counts().items():
        print(f"  - {ptype}: {count}")


if __name__ == "__main__":
    main()

