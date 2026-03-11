@echo off
echo ============================================
echo  LASERFLIX QA - INSTALANDO FERRAMENTAS DEV
echo ============================================
echo.

cd /d "%~dp0.."

echo [1/6] Instalando ruff...
pip install ruff --quiet
if %ERRORLEVEL% neq 0 ( echo ERRO: ruff falhou & exit /b 1 )

echo [2/6] Instalando pylint...
pip install pylint --quiet
if %ERRORLEVEL% neq 0 ( echo ERRO: pylint falhou & exit /b 1 )

echo [3/6] Instalando basedpyright...
pip install basedpyright --quiet
if %ERRORLEVEL% neq 0 ( echo ERRO: basedpyright falhou & exit /b 1 )

echo [4/6] Instalando radon...
pip install radon --quiet
if %ERRORLEVEL% neq 0 ( echo ERRO: radon falhou & exit /b 1 )

echo [5/6] Instalando vulture...
pip install vulture --quiet
if %ERRORLEVEL% neq 0 ( echo ERRO: vulture falhou & exit /b 1 )

echo [6/6] Instalando pytest e plugins...
pip install pytest pytest-cov pytest-timeout --quiet
if %ERRORLEVEL% neq 0 ( echo ERRO: pytest falhou & exit /b 1 )

echo.
echo ============================================
echo  INSTALACAO CONCLUIDA
echo ============================================
pip show ruff pylint basedpyright radon vulture pytest
