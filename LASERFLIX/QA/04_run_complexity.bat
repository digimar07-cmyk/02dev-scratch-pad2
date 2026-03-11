@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

py -m radon cc main.py ai config core ui utils -s -a > "QA\reports\04_radon_cc.txt" 2>&1
set "ERR1=%ERRORLEVEL%"

py -m radon raw main.py ai config core ui utils > "QA\reports\04_radon_raw.txt" 2>&1
set "ERR2=%ERRORLEVEL%"

popd

if not "%ERR1%"=="0" exit /b %ERR1%
exit /b %ERR2%
