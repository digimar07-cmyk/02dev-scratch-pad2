\
        @echo off
        setlocal EnableExtensions EnableDelayedExpansion

        title LASERFLIX - Diagnostico do Ambiente

        set "REPORT_DIR=QA\reports"
        if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"

        for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set "TS=%%i"
        set "REPORT_FILE=%REPORT_DIR%\environment_diagnostic_%TS%.txt"

        echo =============================================================== > "%REPORT_FILE%"
        echo LASERFLIX - DIAGNOSTICO DO AMBIENTE >> "%REPORT_FILE%"
        echo =============================================================== >> "%REPORT_FILE%"
        echo Data/Hora: %date% %time% >> "%REPORT_FILE%"
        echo Pasta atual inicial: %cd% >> "%REPORT_FILE%"
        echo. >> "%REPORT_FILE%"

        call :section "1) PYTHON E PIP"
        call :run "python --version" python --version
        call :run "py --version" py --version
        call :run "pip --version" pip --version
        call :run "py -m pip --version" py -m pip --version
        call :run "where python" where python
        call :run "where py" where py

        call :section "2) SISTEMA E ARQUITETURA"
        call :run "ver" ver
        call :run "systeminfo resumido" cmd /c systeminfo ^| findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"
        call :run "wmic cpu get name" wmic cpu get name
        call :run "wmic os get osarchitecture" wmic os get osarchitecture
        call :run "echo %%PROCESSOR_ARCHITECTURE%%" cmd /c echo %%PROCESSOR_ARCHITECTURE%%

        call :section "3) GIT"
        call :run "git --version" git --version
        call :run "where git" where git

        call :section "4) PASTA DO PROJETO"
        call :run "cd" cd
        call :run "dir" dir

        call :section "5) VENV"
        call :run "if exist .venv" cmd /c if exist .venv (echo .venv EXISTE) else (echo .venv NAO_EXISTE)
        call :run "if exist venv" cmd /c if exist venv (echo venv EXISTE) else (echo venv NAO_EXISTE)

        call :section "6) LISTA DE PACOTES PYTHON"
        call :run "py -m pip list" py -m pip list

        call :section "7) IMPORTACOES DAS FERRAMENTAS DE QA"
        call :run "import pytest" py -c "import pytest; print('pytest OK')"
        call :run "import ruff" py -c "import ruff; print('ruff OK')"
        call :run "import mypy" py -c "import mypy; print('mypy OK')"
        call :run "import pylint" py -c "import pylint; print('pylint OK')"
        call :run "import radon" py -c "import radon; print('radon OK')"
        call :run "import vulture" py -c "import vulture; print('vulture OK')"

        call :section "8) EXECUTAVEIS DAS FERRAMENTAS"
        call :run "where pytest" where pytest
        call :run "where ruff" where ruff
        call :run "where mypy" where mypy
        call :run "where pylint" where pylint
        call :run "where radon" where radon
        call :run "where vulture" where vulture

        call :section "9) ESTRUTURA DE QA"
        call :run "dir QA" dir QA
        call :run "dir tests" dir tests
        call :run "dir QA\reports" dir QA\reports

        call :section "10) CONTEUDO DOS SCRIPTS BAT"
        call :run "type QA\01_install_dev_tools.bat" type QA\01_install_dev_tools.bat
        call :run "type QA\10_run_all.bat" type QA\10_run_all.bat

        call :section "11) PYTEST"
        call :run "py -m pytest --version" py -m pytest --version
        call :run "py -m pytest -q" py -m pytest -q

        call :section "12) RELATORIOS"
        call :run "dir QA\reports /s" dir QA\reports /s

        call :section "13) ARQUIVO SUSPEITO"
        call :run "type ui\components\chips_bar.py" type ui\components\chips_bar.py

        call :section "14) COMPILACAO BASICA"
        call :run "py -m compileall ." py -m compileall .

        call :section "15) GIT STATUS"
        call :run "git status" git status
        call :run "git branch" git branch

        echo. >> "%REPORT_FILE%"
        echo =============================================================== >> "%REPORT_FILE%"
        echo FIM DO DIAGNOSTICO >> "%REPORT_FILE%"
        echo Relatorio salvo em: %REPORT_FILE% >> "%REPORT_FILE%"
        echo =============================================================== >> "%REPORT_FILE%"

        echo.
        echo ===============================================================
        echo Diagnostico concluido.
        echo Relatorio salvo em:
        echo %REPORT_FILE%
        echo ===============================================================
        echo.
        pause
        exit /b 0

        :section
        echo.>> "%REPORT_FILE%"
        echo =============================================================== >> "%REPORT_FILE%"
        echo %~1 >> "%REPORT_FILE%"
        echo =============================================================== >> "%REPORT_FILE%"
        exit /b 0

        :run
        echo.>> "%REPORT_FILE%"
        echo [COMANDO] %~1 >> "%REPORT_FILE%"
        echo --------------------------------------------------------------- >> "%REPORT_FILE%"
        shift
        call %* >> "%REPORT_FILE%" 2>&1
        set "ERR=%ERRORLEVEL%"
        echo --------------------------------------------------------------- >> "%REPORT_FILE%"
        echo [EXIT CODE] !ERR! >> "%REPORT_FILE%"
        exit /b 0
