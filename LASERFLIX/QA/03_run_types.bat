@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py -m mypy main.py ai config core ui utils --config-file "mypy.ini" > "QA\reports\03_mypy.txt" 2>&1
set "ERR=%ERRORLEVEL%"

popd
exit /b %ERR%
