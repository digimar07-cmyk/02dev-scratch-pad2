@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  01 - RUFF CHECK  |  Análise estática — SEM modificar código    ║
REM ║  Gera: QA/reports/01_ruff_check_REPORT.txt                      ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

set REPORT=QA\reports\01_ruff_check_REPORT.txt
set TS=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

echo. > "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   01 - RUFF CHECK REPORT - LASERFLIX >> "%REPORT%"
echo   Data: %TS% >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo. >> "%REPORT%"

python -m ruff --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Instalando ruff...
    python -m pip install ruff -q
)

echo [1/2] Erros detalhados...
echo --- ERROS DETALHADOS --- >> "%REPORT%"
python -m ruff check core/ ui/ config/ utils/ 2>&1 | tee -a "%REPORT%"

echo. >> "%REPORT%"
echo --- RESUMO POR CATEGORIA --- >> "%REPORT%"
echo [2/2] Resumo por categoria...
python -m ruff check core/ ui/ config/ utils/ --statistics 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   FIM DO RELATÓRIO >> "%REPORT%"
echo ================================================================ >> "%REPORT%"

echo.
echo ================================================================
echo   CONCLUIDO! Relatorio salvo em: %REPORT%
echo   Para corrigir automaticamente, rode: 02_ruff_fix.bat
echo ================================================================
echo.
pause
