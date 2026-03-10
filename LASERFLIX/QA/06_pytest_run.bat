@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  06 - PYTEST  |  Roda todos os testes unitários                 ║
REM ║  Gera: QA/reports/06_pytest_REPORT.txt                          ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0\.."

if not exist "QA\reports" mkdir "QA\reports"

set REPORT=QA\reports\06_pytest_REPORT.txt
set TS=%date:~6,4%-%date:~3,2%-%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

echo. > "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   06 - PYTEST REPORT - LASERFLIX >> "%REPORT%"
echo   Data: %TS% >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo. >> "%REPORT%"

python -m pytest --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] Instalando pytest...
    python -m pip install pytest pytest-cov -q
)

echo [1/1] Rodando todos os testes em tests/ ...
echo --- RESULTADO DOS TESTES --- >> "%REPORT%"
python -m pytest tests/ -v --tb=short --no-header 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo --- COBERTURA DE CODIGO --- >> "%REPORT%"
python -m pytest tests/ --cov=core --cov=ui --cov=utils --cov=config --cov-report=term-missing --no-header -q 2>&1 >> "%REPORT%"

echo. >> "%REPORT%"
echo ================================================================ >> "%REPORT%"
echo   FIM DO RELATÓRIO >> "%REPORT%"
echo ================================================================ >> "%REPORT%"

echo.
echo ================================================================
echo   CONCLUIDO! Relatorio salvo em: %REPORT%
echo   PASSED = verde, FAILED = problema encontrado!
echo ================================================================
echo.
pause
