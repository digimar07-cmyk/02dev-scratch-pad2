@echo off
echo ============================================
echo  LASERFLIX QA - TYPE CHECK (basedpyright)
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

basedpyright ai/ config/ core/ utils/ ui/ main.py > QA\reports\types_report.txt 2>&1
set TYPES_EXIT=%ERRORLEVEL%

echo Type check exit code: %TYPES_EXIT%
type QA\reports\types_report.txt

echo types_exit=%TYPES_EXIT% > QA\reports\types_exit_codes.txt

if %TYPES_EXIT% neq 0 (
    echo [AVISO] basedpyright reportou erros de tipo. Ver QA\reports\types_report.txt
    exit /b 1
)
echo [TYPES] OK.
exit /b 0
