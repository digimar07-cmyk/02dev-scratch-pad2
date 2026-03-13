@echo off
echo ============================================
echo  LASERFLIX QA - SMOKE TESTS + ESTRUTURAIS
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

pytest tests/smoke/ tests/structural/ ^
  -v ^
  --tb=long ^
  --timeout=30 ^
  --junitxml=QA\reports\pytest_smoke.xml ^
  -p no:cacheprovider
set SMOKE_EXIT=%ERRORLEVEL%

echo smoke_exit=%SMOKE_EXIT% > QA\reports\smoke_exit_codes.txt

if %SMOKE_EXIT% neq 0 (
    echo [REPROVADO] Smoke/structural tests falharam.
    exit /b 1
)
echo [SMOKE] Passou.
exit /b 0
