@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  03 - MYPY CHECK  |  Verificação de tipos estáticos             ║
REM ║  Gera: QA/reports/03_mypy_check_REPORT.txt                      ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

set REPORT=QA\reports\03_mypy_check_REPORT.txt
set TS=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

echo. > "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   03 - MYPY CHECK REPORT - LASERFLIX >> "%REPORT%"
echo   Data: %TS% >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo. >> "%REPORT%"

python -m mypy --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Instalando mypy...
    python -m pip install mypy -q
)

echo [1/2] Verificando tipos em core/ ...
echo --- CORE --- >> "%REPORT%"
python -m mypy core/ --config-file mypy.ini 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo [2/2] Verificando tipos em ui/ ...
echo --- UI --- >> "%REPORT%"
python -m mypy ui/ --config-file mypy.ini 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   FIM DO RELATÓRIO >> "%REPORT%"
echo ================================================================ >> "%REPORT%"

echo.
echo ================================================================
echo   CONCLUIDO! Relatorio salvo em: %REPORT%
echo   Erros de tipo = funcoes recebendo dados do tipo errado.
echo ================================================================
echo.
pause
