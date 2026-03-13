@echo off
echo ============================================
echo  LASERFLIX QA - TESTES DE INTEGRACAO
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

pytest tests/integration/ ^
  -v ^
  --tb=short ^
  --timeout=60 ^
  --junitxml=QA\reports\pytest_integration.xml ^
  -p no:cacheprovider
set INT_EXIT=%ERRORLEVEL%

echo integration_exit=%INT_EXIT% > QA\reports\integration_exit_codes.txt

if %INT_EXIT% neq 0 (
    echo [REPROVADO] Testes de integracao falharam.
    exit /b 1
)
echo [INTEGRATION] Passou.
exit /b 0
