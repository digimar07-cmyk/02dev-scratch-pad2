@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py "%SCRIPT_DIR%13_detect_duplication.py" > "QA\reports\06_duplication.txt" 2>&1
set "ERR=%ERRORLEVEL%"

popd
exit /b %ERR%
