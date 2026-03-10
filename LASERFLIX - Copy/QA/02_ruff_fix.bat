@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  02 - RUFF FIX  |  Auto-corrige erros fixáveis                  ║
REM ║  Gera: QA/reports/02_ruff_fix_REPORT.txt                        ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

set REPORT=QA\reports\02_ruff_fix_REPORT.txt
set TS=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

echo. > "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   02 - RUFF FIX REPORT - LASERFLIX >> "%REPORT%"
echo   Data: %TS% >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo. >> "%REPORT%"

python -m ruff --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Instalando ruff...
    python -m pip install ruff -q
)

echo --- ESTADO ANTES DO FIX --- >> "%REPORT%"
echo [1/3] Contando erros ANTES do fix...
python -m ruff check core/ ui/ config/ utils/ --statistics 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo --- APLICANDO AUTO-FIX --- >> "%REPORT%"
echo [2/3] Aplicando --fix...
python -m ruff check core/ ui/ config/ utils/ --fix 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo --- ESTADO APÓS O FIX (erros que restaram) --- >> "%REPORT%"
echo [3/3] Verificando o que restou...
python -m ruff check core/ ui/ config/ utils/ --statistics 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   FIM DO RELATÓRIO >> "%REPORT%"
echo ================================================================ >> "%REPORT%"

echo.
echo ================================================================
echo   CONCLUIDO! Relatorio salvo em: %REPORT%
echo   Os erros sem [*] precisam de correcao manual.
echo ================================================================
echo.
pause
