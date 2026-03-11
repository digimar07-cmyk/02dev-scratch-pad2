@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py -m ruff check . --config "QA\ruff.toml" > "QA\reports\02_ruff.txt" 2>&1
set "RUFF_ERR=%ERRORLEVEL%"

py -m pylint main.py ai config core ui utils --rcfile=".pylintrc" > "QA\reports\02_pylint.txt" 2>&1
set "PYLINT_ERR=%ERRORLEVEL%"

popd

if not "%RUFF_ERR%"=="0" exit /b %RUFF_ERR%
exit /b %PYLINT_ERR%
