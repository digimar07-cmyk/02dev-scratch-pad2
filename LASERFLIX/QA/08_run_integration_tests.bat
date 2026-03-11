@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py -m pytest tests\integration -q > "QA\reports\08_integration_pytest.txt" 2>&1
set "ERR=%ERRORLEVEL%"

popd
exit /b %ERR%
