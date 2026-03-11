@echo off
echo ============================================
echo  LASERFLIX QA - COMPLEXIDADE (radon)
echo ============================================
cd /d "%~dp0.."

if not exist "QA\reports" mkdir "QA\reports"

echo [RADON CC] Complexidade ciclomatica por funcao...
radon cc ai/ config/ core/ utils/ ui/ main.py -s -a -n C > QA\reports\complexity_cc_report.txt 2>&1
set CC_EXIT=%ERRORLEVEL%
type QA\reports\complexity_cc_report.txt

echo.
echo [RADON MI] Indice de manutenibilidade por arquivo...
radon mi ai/ config/ core/ utils/ ui/ main.py -s > QA\reports\complexity_mi_report.txt 2>&1
type QA\reports\complexity_mi_report.txt

echo.
echo [RADON HAL] Metricas de Halstead...
radon hal ai/ config/ core/ utils/ ui/ main.py > QA\reports\complexity_hal_report.txt 2>&1

echo cc_exit=%CC_EXIT% > QA\reports\complexity_exit_codes.txt

echo Relatorios salvos em QA\reports\
echo [NOTA] Funcoes com CC >= C (score 10+) devem ser refatoradas.
exit /b 0
