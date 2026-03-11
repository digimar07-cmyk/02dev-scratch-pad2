@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py -m pytest tests\smoke -q > "QA\reports\09_smoke_pytest.txt" 2>&1
set "ERR=%ERRORLEVEL%"

popd
exit /b %ERR%
