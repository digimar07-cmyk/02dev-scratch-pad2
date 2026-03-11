@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py -m vulture main.py ai config core ui utils --min-confidence 70 > "QA\reports\05_vulture.txt" 2>&1
set "ERR=%ERRORLEVEL%"

popd
exit /b %ERR%
