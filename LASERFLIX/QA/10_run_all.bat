@echo off
setlocal
set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%\.."

if not exist "QA\reports" mkdir "QA\reports"

call "%SCRIPT_DIR%02_run_lint.bat"
set "LINT_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%03_run_types.bat"
set "TYPES_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%04_run_complexity.bat"
set "COMPLEXITY_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%05_run_dead_code.bat"
set "DEADCODE_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%06_run_duplication.bat"
set "DUP_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%07_run_unit_tests.bat"
set "UNIT_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%08_run_integration_tests.bat"
set "INT_ERR=%ERRORLEVEL%"

call "%SCRIPT_DIR%09_run_smoke_tests.bat"
set "SMOKE_ERR=%ERRORLEVEL%"

py "%SCRIPT_DIR%11_build_consolidated_report.py"
set "REPORT_ERR=%ERRORLEVEL%"

py "%SCRIPT_DIR%12_enforce_quality_gate.py"
set "GATE_ERR=%ERRORLEVEL%"

echo.
echo Lint exit code: %LINT_ERR%
echo Types exit code: %TYPES_ERR%
echo Complexity exit code: %COMPLEXITY_ERR%
echo Dead code exit code: %DEADCODE_ERR%
echo Duplication exit code: %DUP_ERR%
echo Unit exit code: %UNIT_ERR%
echo Integration exit code: %INT_ERR%
echo Smoke exit code: %SMOKE_ERR%
echo Report exit code: %REPORT_ERR%
echo Quality gate exit code: %GATE_ERR%

popd
pause
exit /b %GATE_ERR%
