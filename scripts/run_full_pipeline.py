#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step2 전체 파이프라인 자동 실행 스크립트

데이터 확장 → 품질체크 → 전처리 → EDA → 리포트 생성까지 한 번에 실행
"""
import subprocess
import sys
from pathlib import Path
import argparse

def run_command(cmd_list, description):
    """명령 실행 및 에러 핸들링"""
    print(f"\n{'='*60}")
    print(f"[Step] {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd_list)}")
    print()
    
    result = subprocess.run(cmd_list, capture_output=False, text=True)
    
    if result.returncode != 0:
        print(f"\n[ERROR] {description} 실행 중 오류 발생 (exit code: {result.returncode})")
        sys.exit(1)
    
    print(f"\n[OK] {description} 완료")
    return result

def main():
    parser = argparse.ArgumentParser(description="Step2 전체 파이프라인 자동 실행")
    parser.add_argument("--skip_expansion", action="store_true", help="데이터 확장 단계 건너뛰기")
    parser.add_argument("--target", type=int, default=1000, help="목표 데이터 건수")
    parser.add_argument("--autofill_labels", action="store_true", help="룰 기반으로 결측 라벨을 임시 보완(리포트/EDA에 반영)")
    parser.add_argument(
        "--raw",
        default=None,
        help="입력 raw csv 경로(기본: data/step2_raw_text_sample.csv). skip_expansion과 함께 쓰면 해당 파일을 그대로 사용",
    )
    args = parser.parse_args()
    
    # 프로젝트 루트 탐색
    root = Path(__file__).parent.parent
    scripts_dir = root / "scripts"
    data_dir = root / "data"
    
    print(f"프로젝트 루트: {root}")
    print(f"목표 데이터 건수: {args.target}")
    
    # Python 실행 명령 (Windows에서는 py -3, Unix에서는 python3)
    if sys.platform == "win32":
        python_cmd = "py"
        python_args = ["-3"]
    else:
        python_cmd = "python3"
        python_args = []
    
    # 입출력 파일 경로
    if args.raw:
        raw_input = Path(args.raw)
        if not raw_input.is_absolute():
            raw_input = root / raw_input
    else:
        raw_input = data_dir / "step2_raw_text_sample.csv"
    raw_expanded = data_dir / "step2_raw_text_expanded.csv"
    raw_for_pipeline = raw_input
    
    # Step 1: 데이터 확장 (optional)
    if not args.skip_expansion:
        run_command(
            [python_cmd] + python_args + [
                str(scripts_dir / "step2_expand_to_1000.py"),
                "--current", str(raw_input),
                "--out", str(raw_expanded),
                "--target", str(args.target),
            ],
            f"1. 데이터 {args.target}건 확장"
        )
        raw_for_pipeline = raw_expanded
    else:
        print("\n데이터 확장 단계를 건너뜁니다.")
    
    # Step 2: 품질 체크
    run_command(
        [python_cmd] + python_args + [
            str(scripts_dir / "step2_quality_check.py"),
            "--raw", str(raw_for_pipeline),
            *(["--autofill_labels"] if args.autofill_labels else []),
        ],
        "2. 데이터 품질 체크"
    )
    
    # Step 3: 전처리
    run_command(
        [python_cmd] + python_args + [
            str(scripts_dir / "step2_preprocess_text.py"),
            "--raw", str(raw_for_pipeline),
            *(["--autofill_labels"] if args.autofill_labels else []),
        ],
        "3. 데이터 전처리"
    )
    
    # Step 4: EDA
    run_command(
        [python_cmd] + python_args + [
            str(scripts_dir / "step2_eda_text.py"),
        ],
        "4. 탐색적 데이터 분석(EDA)"
    )
    
    # Step 5: EDA 리포트 생성
    run_command(
        [python_cmd] + python_args + [
            str(scripts_dir / "step2_generate_eda_report.py"),
        ],
        "5. EDA 리포트 생성"
    )
    
    print(f"\n{'='*60}")
    print("[완료] 전체 파이프라인 실행 완료!")
    print(f"{'='*60}")
    print("\n[산출물] 생성된 파일:")
    print("- out/step2_quality_report.md")
    print("- out/step2_quality_report.json")
    print("- out/step2_preprocessed.csv")
    print("- out/step2_preprocess_summary.json")
    print("- out/eda_length_hist.png")
    print("- out/eda_top_keywords.csv")
    print("- out/eda_sentiment_distribution.png")
    print("- out/eda_topic_distribution.png")
    print("- out/step2_eda_report.md")
    if not args.skip_expansion:
        print("- out/step2_expansion_to_1000_comparison.json")
    print()

if __name__ == "__main__":
    main()

