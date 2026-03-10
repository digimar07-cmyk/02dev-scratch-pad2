@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  05 - CODE SMELL  |  ruff + radon + vulture + score geral       ║
REM ║  Gera: QA/reports/smell_report_TIMESTAMP.txt (auto)             ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

python -m pip install radon vulture -q >nul 2>&1

echo.
echo ================================================================
echo   05 - CODE SMELL CHECK - LASERFLIX
echo ================================================================
echo.

python QA/05_code_smell_check.py

echo.
echo   Relatorio gerado em QA/reports/
echo.
pause
