@echo off
REM Step2 전체 파이프라인 자동 실행 (Windows)
echo ========================================
echo Step2 전체 파이프라인 실행
echo ========================================

py -3 scripts\run_full_pipeline.py %*

if %ERRORLEVEL% neq 0 (
    echo.
    echo 파이프라인 실행 중 오류가 발생했습니다.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 파이프라인 실행이 완료되었습니다!
echo out\ 폴더에서 결과를 확인하세요.
pause

