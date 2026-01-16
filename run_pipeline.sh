#!/bin/bash
# Step2 전체 파이프라인 자동 실행 (Unix/Mac)

echo "========================================"
echo "Step2 전체 파이프라인 실행"
echo "========================================"

python3 scripts/run_full_pipeline.py "$@"

if [ $? -ne 0 ]; then
    echo ""
    echo "파이프라인 실행 중 오류가 발생했습니다."
    exit 1
fi

echo ""
echo "파이프라인 실행이 완료되었습니다!"
echo "out/ 폴더에서 결과를 확인하세요."

