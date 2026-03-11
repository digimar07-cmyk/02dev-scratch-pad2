@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

py -m pip install --upgrade pip
py -m pip install pytest pytest-cov ruff mypy pylint radon vulture

popd
echo.
echo Dependencias de QA instaladas.
pause
