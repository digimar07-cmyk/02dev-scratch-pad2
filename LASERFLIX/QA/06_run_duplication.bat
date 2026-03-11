@echo off
echo ============================================
echo  LASERFLIX QA - DUPLICACAO DE CODIGO
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

echo [PYLINT DUPLICATE] Detectando blocos duplicados...
pylint ai/ config/ core/ utils/ ui/ main.py ^
  --disable=all ^
  --enable=duplicate-code ^
  --min-similarity-lines=6 > QA\reports\duplication_report.txt 2>&1
set DUP_EXIT=%ERRORLEVEL%

echo Duplication exit code: %DUP_EXIT%
type QA\reports\duplication_report.txt

echo dup_exit=%DUP_EXIT% > QA\reports\duplication_exit_codes.txt
echo Relatorio salvo em QA\reports\duplication_report.txt
exit /b 0
