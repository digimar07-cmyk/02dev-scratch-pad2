@echo off
echo ============================================
echo  LASERFLIX QA - TESTES UNITARIOS
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

pytest tests/unit/ ^
  -v ^
  --tb=short ^
  --timeout=30 ^
  --junitxml=QA\reports\pytest_unit.xml ^
  --cov=ai --cov=core --cov=utils ^
  --cov-report=term-missing ^
  --cov-report=html:QA\reports\coverage_html ^
  --cov-fail-under=40 ^
  -p no:cacheprovider
set UNIT_EXIT=%ERRORLEVEL%

echo unit_exit=%UNIT_EXIT% > QA\reports\unit_exit_codes.txt

if %UNIT_EXIT% neq 0 (
    echo [REPROVADO] Testes unitarios falharam.
    exit /b 1
)
echo [UNIT] Passou.
exit /b 0
