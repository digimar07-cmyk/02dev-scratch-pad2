@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  04 - PYLINT CHECK  |  Análise profunda de qualidade            ║
REM ║  Gera: QA/reports/04_pylint_check_REPORT.txt                    ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

set REPORT=QA\reports\04_pylint_check_REPORT.txt
set TS=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

echo. > "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   04 - PYLINT CHECK REPORT - LASERFLIX >> "%REPORT%"
echo   Data: %TS% >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo. >> "%REPORT%"

python -m pylint --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Instalando pylint...
    python -m pip install pylint -q
)

echo [1/3] Analisando core/ ...
echo --- CORE --- >> "%REPORT%"
python -m pylint core/ --output-format=text --reports=yes --score=yes 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo [2/3] Analisando ui/ ...
echo --- UI --- >> "%REPORT%"
python -m pylint ui/ --output-format=text --reports=yes --score=yes 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo [3/3] Analisando utils/ e config/ ...
echo --- UTILS + CONFIG --- >> "%REPORT%"
python -m pylint utils/ config/ --output-format=text --reports=yes --score=yes 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   FIM DO RELATÓRIO >> "%REPORT%"
echo ================================================================ >> "%REPORT%"

echo.
echo ================================================================
echo   CONCLUIDO! Relatorio salvo em: %REPORT%
echo   Score pylint: ideal acima de 8.0/10
echo ================================================================
echo.
pause
