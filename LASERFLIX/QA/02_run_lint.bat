@echo off
echo ============================================
echo  LASERFLIX QA - LINT (ruff + pylint)
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

echo.
echo [RUFF] Executando analise de lint...
python -m ruff check ai/ config/ core/ utils/ ui/ main.py --output-format=full > QA\reports\ruff_report.txt 2>&1
set RUFF_EXIT=%ERRORLEVEL%
echo Ruff exit code: %RUFF_EXIT%
type QA\reports\ruff_report.txt

echo.
echo [PYLINT] Executando analise semantica...
python -m pylint ai/ config/ core/ utils/ ui/ main.py ^
  --rcfile=QA\pylintrc ^
  --output-format=text ^
  --reports=yes ^
  --score=yes > QA\reports\pylint_report.txt 2>&1
set PYLINT_EXIT=%ERRORLEVEL%
echo Pylint exit code: %PYLINT_EXIT%
type QA\reports\pylint_report.txt

echo.
echo Relatorios salvos em QA\reports\
echo ruff_exit=%RUFF_EXIT% > QA\reports\lint_exit_codes.txt
echo pylint_exit=%PYLINT_EXIT% >> QA\reports\lint_exit_codes.txt

if %RUFF_EXIT% neq 0 (
    echo [REPROVADO] Ruff encontrou erros.
    exit /b 1
)
echo [LINT] Ruff OK. Verifique pylint manualmente para smells.
exit /b 0
