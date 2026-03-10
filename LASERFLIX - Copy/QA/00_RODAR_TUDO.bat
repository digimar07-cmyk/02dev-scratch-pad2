@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  00 - RODAR TUDO  |  Executa toda a suite QA em sequência       ║
REM ║  Todos os relatórios ficam em QA/reports/                        ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

set TS=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%
set SUMMARY=QA\reports\00_SUITE_SUMMARY_%TS%.txt

echo. > "%SUMMARY%"
echo ================================================================ >> "%SUMMARY%"
echo   00 - QA SUITE COMPLETA - LASERFLIX >> "%SUMMARY%"
echo   Data: %TS% >> "%SUMMARY%"
echo ================================================================ >> "%SUMMARY%"
echo. >> "%SUMMARY%"

echo.
echo ================================================================
echo   LASERFLIX QA SUITE — INICIANDO
echo ================================================================
echo.

REM ── 01 Ruff Check ────────────────────────────────────────────────
echo [1/5] Ruff Check...
python -m ruff check core/ ui/ config/ utils/ --statistics > QA\reports\01_ruff_check_REPORT.txt 2>&1
echo   [OK] Relatorio: QA/reports/01_ruff_check_REPORT.txt
echo [1/5] Ruff Check - CONCLUIDO >> "%SUMMARY%"

REM ── 02 MyPy ───────────────────────────────────────────────────────
echo [2/5] MyPy Check...
python -m mypy core/ ui/ --config-file mypy.ini > QA\reports\03_mypy_check_REPORT.txt 2>&1
echo   [OK] Relatorio: QA/reports/03_mypy_check_REPORT.txt
echo [2/5] MyPy Check - CONCLUIDO >> "%SUMMARY%"

REM ── 03 Pylint ─────────────────────────────────────────────────────
echo [3/5] Pylint Check...
python -m pylint core/ ui/ utils/ config/ --output-format=text --score=yes > QA\reports\04_pylint_check_REPORT.txt 2>&1
echo   [OK] Relatorio: QA/reports/04_pylint_check_REPORT.txt
echo [3/5] Pylint Check - CONCLUIDO >> "%SUMMARY%"

REM ── 04 Code Smell ─────────────────────────────────────────────────
echo [4/5] Code Smell Check...
python QA/05_code_smell_check.py > QA\reports\05_smell_stdout.txt 2>&1
echo   [OK] Relatorio: QA/reports/05_smell_report_*.txt
echo [4/5] Code Smell - CONCLUIDO >> "%SUMMARY%"

REM ── 05 PyTest ─────────────────────────────────────────────────────
echo [5/5] PyTest...
python -m pytest tests/ -v --tb=short --no-header > QA\reports\06_pytest_REPORT.txt 2>&1
echo   [OK] Relatorio: QA/reports/06_pytest_REPORT.txt
echo [5/5] PyTest - CONCLUIDO >> "%SUMMARY%"

echo. >> "%SUMMARY%"
echo ================================================================ >> "%SUMMARY%"
echo   TODOS OS RELATÓRIOS GERADOS EM QA/reports/ >> "%SUMMARY%"
echo ================================================================ >> "%SUMMARY%"

echo.
echo ================================================================
echo   SUITE COMPLETA! Relatórios em: QA/reports/
echo   Arquivos gerados:
echo     01_ruff_check_REPORT.txt
echo     03_mypy_check_REPORT.txt
echo     04_pylint_check_REPORT.txt
echo     05_smell_report_*.txt
echo     06_pytest_REPORT.txt
echo     00_SUITE_SUMMARY_*.txt
echo ================================================================
echo.
pause
