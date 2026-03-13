@echo off
echo ============================================
echo  LASERFLIX QA - CODIGO MORTO (vulture)
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

echo Executando vulture com min-confidence 80...
vulture ai/ config/ core/ utils/ ui/ main.py ^
  --min-confidence 80 > QA\reports\dead_code_report.txt 2>&1
set VULTURE_EXIT=%ERRORLEVEL%

echo Vulture exit code: %VULTURE_EXIT%
type QA\reports\dead_code_report.txt

echo vulture_exit=%VULTURE_EXIT% > QA\reports\dead_code_exit_codes.txt
echo Relatorio salvo em QA\reports\dead_code_report.txt
exit /b 0
