@echo off
:: Verifica se o script possui privilegios de administrador
net session >nul 2>&1
if %errorLevel% == 0 (
    goto :executar
) else (
    :: Reabre o proprio arquivo solicitando elevacao de privilegios (UAC)
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:executar
G:
cd "G:\GitHub\02dev-scratch-pad2\LASERFLIX"
pytest tests/ -v
pause