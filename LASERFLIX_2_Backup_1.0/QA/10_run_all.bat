@echo off
echo ============================================
echo  LASERFLIX QA - SUITE COMPLETA
echo ============================================
cd /d "%~dp0"

set FAILED=0

call 02_run_lint.bat
if %ERRORLEVEL% neq 0 set FAILED=1

call 03_run_types.bat
if %ERRORLEVEL% neq 0 set FAILED=1

call 04_run_complexity.bat

call 05_run_dead_code.bat

call 06_run_duplication.bat

call 07_run_unit_tests.bat
if %ERRORLEVEL% neq 0 set FAILED=1

call 08_run_integration_tests.bat
if %ERRORLEVEL% neq 0 set FAILED=1

call 09_run_smoke_tests.bat
if %ERRORLEVEL% neq 0 set FAILED=1

echo.
echo Gerando relatorio consolidado...
python 11_build_consolidated_report.py

echo.
echo Executando quality gate...
python 12_enforce_quality_gate.py
if %ERRORLEVEL% neq 0 set FAILED=1

echo.
if %FAILED% neq 0 (
    echo ============================================
    echo  RESULTADO FINAL: *** REPROVADO ***
    echo ============================================
    exit /b 1
) else (
    echo ============================================
    echo  RESULTADO FINAL: APROVADO
    echo ============================================
    exit /b 0
)
