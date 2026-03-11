from __future__ import annotations

import shutil
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parent

FILES: dict[str, str] = {
    "QA/00_README_QA.md": dedent("""\
        # QA do LASERFLIX

        Esta estrutura foi reconstruída do zero para atuar como auditor independente do código.

        ## Princípios
        - testes existem para encontrar defeitos reais;
        - verde falso é fracasso;
        - a base de testes não deve ser alterada para esconder defeitos;
        - o projeto deve reprovar se houver falhas críticas.

        ## Ordem de execução
        1. `QA\\01_install_dev_tools.bat`
        2. `QA\\10_run_all.bat`

        ## Execução por etapa
        - `QA\\02_run_lint.bat`
        - `QA\\03_run_types.bat`
        - `QA\\04_run_complexity.bat`
        - `QA\\05_run_dead_code.bat`
        - `QA\\06_run_duplication.bat`
        - `QA\\07_run_unit_tests.bat`
        - `QA\\08_run_integration_tests.bat`
        - `QA\\09_run_smoke_tests.bat`

        ## Saídas
        Relatórios ficam em `QA\\reports\\`.
    """),
    "QA/00A_PHASE1_CLEANUP_REPORT.md": dedent("""\
        # Fase 1 — Invalidação da base antiga

        Esta fase assume que qualquer estrutura anterior de QA/testes/checks pode estar contaminada, enviesada ou maquiada.

        ## Regras aplicadas
        - não herdar automaticamente configs antigas de QA;
        - não confiar em relatórios antigos;
        - não confiar em testes antigos sem revalidação;
        - não usar thresholds herdados por conveniência.

        ## Diretórios recriados nesta fase
        - `QA/`
        - `tests/unit/`
        - `tests/integration/`
        - `tests/smoke/`

        ## Observação
        O código-fonte do app não é modificado por esta reconstrução.
    """),
    "QA/00B_PHASE2_REBUILD_MANIFEST.md": dedent("""\
        # Fase 2 — Reconstrução total da suíte

        ## Ferramentas centrais
        - pytest
        - ruff
        - pylint
        - mypy
        - radon
        - vulture

        ## Objetivos
        - lint real
        - type checking
        - complexidade
        - código morto
        - duplicação
        - unit tests
        - integration tests
        - smoke tests
        - relatório consolidado
        - quality gate
    """),
    "QA/00C_PHASE3_GOLDEN_RULE.md": dedent("""\
        # Fase 3 — Regra de Ouro

        ## Absolutos
        1. Não alterar a base de testes para fazer o app passar.
        2. Não enfraquecer asserts.
        3. Não adicionar skip/xfail para esconder defeitos.
        4. Não excluir arquivos do escopo sem justificativa técnica explícita.
        5. Não reduzir thresholds depois de ver falhas.
        6. Corrigir o código do app, não o termômetro.
        7. Se o erro persistir, admitir que a correção falhou.
    """),
    "QA/00D_TOOL_CLASSIFICATION.md": dedent("""\
        # Classificação das ferramentas

        ## Framework de testes
        - PyTest
        - Unittest
        - Robot
        - DocTest

        ## Linter
        - Ruff
        - Pylint

        ## Type checker
        - Pyright
        - Basedpyright
        - MyPy

        ## Smells / complexidade / duplicação
        - Ruff (parcial)
        - Pylint (parcial)
        - Radon
        - Vulture

        ## Ferramentas de editor / LSP
        - JEDI
        - PyLSP / Python LSP Server
        - Helix

        ## Não prioritário aqui
        - Testify
    """),
    "QA/00E_THRESHOLDS_AND_SCOPE.md": dedent("""\
        # Thresholds e escopo

        ## Escopo
        Inclui:
        - `main.py`
        - `ai/`
        - `config/`
        - `core/`
        - `ui/`
        - `utils/`

        Exclui apenas artefatos operacionais:
        - `__pycache__/`
        - `*.pyc`
        - `.coverage`
        - `*.log`
        - `*.backup*`
        - `laserflix_backups/`

        ## Thresholds iniciais
        - Radon CC: alerta acima de B, reprovação a partir de D relevante
        - Duplicação: qualquer grupo >= 20 linhas iguais deve ser relatado
        - Smoke test: qualquer falha estrutural reprova
        - Type errors relevantes: reprovam
        - Falhas de importação: reprovam
    """),
    "QA/ruff.toml": dedent("""\
        target-version = "py311"
        line-length = 100

        exclude = [
          "__pycache__",
          ".venv",
          "venv",
          "laserflix_backups",
        ]

        [lint]
        select = ["E", "F", "I", "B", "UP"]
        ignore = []
    """),
    "pytest.ini": dedent("""\
        [pytest]
        testpaths = tests
        python_files = test_*.py
        python_functions = test_*
        addopts = -ra
    """),
    "mypy.ini": dedent("""\
        [mypy]
        python_version = 3.11
        ignore_missing_imports = True
        warn_unused_configs = True
        warn_redundant_casts = True
        warn_unused_ignores = True
        warn_return_any = True
        no_implicit_optional = True
        pretty = True

        [mypy-tests.*]
        disallow_untyped_defs = False
    """),
    ".pylintrc": dedent("""\
        [MASTER]
        ignore=__pycache__,.venv,venv,laserflix_backups

        [MESSAGES CONTROL]
        disable=
            missing-module-docstring,
            missing-function-docstring,
            missing-class-docstring,
            too-few-public-methods

        [FORMAT]
        max-line-length=100
    """),
    "QA/01_install_dev_tools.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        py -m pip install --upgrade pip
        py -m pip install pytest pytest-cov ruff mypy pylint radon vulture

        popd
        echo.
        echo Dependencias de QA instaladas.
        pause
    """),
    "QA/02_run_lint.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m ruff check . --config "QA\\ruff.toml" > "QA\\reports\\02_ruff.txt" 2>&1
        set "RUFF_ERR=%ERRORLEVEL%"

        py -m pylint main.py ai config core ui utils --rcfile=".pylintrc" > "QA\\reports\\02_pylint.txt" 2>&1
        set "PYLINT_ERR=%ERRORLEVEL%"

        popd

        if not "%RUFF_ERR%"=="0" exit /b %RUFF_ERR%
        exit /b %PYLINT_ERR%
    """),
    "QA/03_run_types.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m mypy main.py ai config core ui utils --config-file "mypy.ini" > "QA\\reports\\03_mypy.txt" 2>&1
        set "ERR=%ERRORLEVEL%"

        popd
        exit /b %ERR%
    """),
    "QA/04_run_complexity.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m radon cc main.py ai config core ui utils -s -a > "QA\\reports\\04_radon_cc.txt" 2>&1
        set "ERR1=%ERRORLEVEL%"

        py -m radon raw main.py ai config core ui utils > "QA\\reports\\04_radon_raw.txt" 2>&1
        set "ERR2=%ERRORLEVEL%"

        popd

        if not "%ERR1%"=="0" exit /b %ERR1%
        exit /b %ERR2%
    """),
    "QA/05_run_dead_code.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m vulture main.py ai config core ui utils --min-confidence 70 > "QA\\reports\\05_vulture.txt" 2>&1
        set "ERR=%ERRORLEVEL%"

        popd
        exit /b %ERR%
    """),
    "QA/06_run_duplication.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py "%SCRIPT_DIR%13_detect_duplication.py" > "QA\\reports\\06_duplication.txt" 2>&1
        set "ERR=%ERRORLEVEL%"

        popd
        exit /b %ERR%
    """),
    "QA/07_run_unit_tests.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m pytest tests\\unit -q > "QA\\reports\\07_unit_pytest.txt" 2>&1
        set "ERR=%ERRORLEVEL%"

        popd
        exit /b %ERR%
    """),
    "QA/08_run_integration_tests.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m pytest tests\\integration -q > "QA\\reports\\08_integration_pytest.txt" 2>&1
        set "ERR=%ERRORLEVEL%"

        popd
        exit /b %ERR%
    """),
    "QA/09_run_smoke_tests.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

        py -m pytest tests\\smoke -q > "QA\\reports\\09_smoke_pytest.txt" 2>&1
        set "ERR=%ERRORLEVEL%"

        popd
        exit /b %ERR%
    """),
    "QA/10_run_all.bat": dedent("""\
        @echo off
        setlocal
        set "SCRIPT_DIR=%~dp0"
        pushd "%SCRIPT_DIR%\\.."

        if not exist "QA\\reports" mkdir "QA\\reports"

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
    """),
    "QA/11_build_consolidated_report.py": dedent("""\
        from pathlib import Path

        REPORTS = Path("QA/reports")
        OUT = REPORTS / "11_consolidated_report.md"

        def read_text(path: Path) -> str:
            try:
                return path.read_text(encoding="utf-8", errors="replace")
            except Exception as exc:
                return f"[ERRO AO LER {path}: {exc}]"

        REPORTS.mkdir(parents=True, exist_ok=True)

        parts = [
            "# Relatório consolidado",
            "",
            "Este relatório consolida as saídas brutas da suíte de QA.",
            "",
        ]

        targets = sorted(p for p in REPORTS.glob("*") if p.name != OUT.name)
        if not targets:
            parts.append("Nenhum relatório encontrado.")
        else:
            for path in targets:
                parts.append(f"## {path.name}")
                parts.append("```text")
                parts.append(read_text(path)[:30000])
                parts.append("```")
                parts.append("")

        OUT.write_text("\\n".join(parts), encoding="utf-8")
        print(f"Consolidated report written to: {OUT}")
    """),
    "QA/12_enforce_quality_gate.py": dedent("""\
        from pathlib import Path
        import sys

        reports = Path("QA/reports")
        out = reports / "12_quality_gate_summary.md"

        def text(name: str) -> str:
            p = reports / name
            return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

        failures = []

        smoke = text("09_smoke_pytest.txt")
        unit = text("07_unit_pytest.txt")
        integ = text("08_integration_pytest.txt")
        mypy = text("03_mypy.txt")
        ruff = text("02_ruff.txt")
        pylint = text("02_pylint.txt")
        dup = text("06_duplication.txt")

        if "failed" in smoke.lower() or "error" in smoke.lower():
            failures.append("Smoke tests com falhas.")
        if "failed" in unit.lower() or "error" in unit.lower():
            failures.append("Unit tests com falhas.")
        if "failed" in integ.lower() or "error" in integ.lower():
            failures.append("Integration tests com falhas.")
        if "error:" in mypy.lower() or "found " in mypy.lower():
            failures.append("Type checking com achados relevantes.")
        if "DUPLICATION_GROUP" in dup:
            failures.append("Duplicação relevante detectada.")
        if "F" in ruff or "E" in ruff:
            failures.append("Ruff apontou problemas.")
        if "fatal" in pylint.lower() or "error" in pylint.lower() or "syntax-error" in pylint.lower():
            failures.append("Pylint apontou problemas relevantes.")

        status = "APROVADO" if not failures else "REPROVADO"

        lines = [
            "# Quality Gate",
            "",
            f"**Status geral:** {status}",
            "",
        ]

        if failures:
            lines.append("## Motivos")
            for item in failures:
                lines.append(f"- {item}")
        else:
            lines.append("Nenhuma falha crítica detectada.")

        out.write_text("\\n".join(lines), encoding="utf-8")
        print(f"Quality gate summary written to: {out}")

        sys.exit(1 if failures else 0)
    """),
    "QA/13_detect_duplication.py": dedent("""\
        from __future__ import annotations

        from collections import defaultdict
        from pathlib import Path
        import hashlib

        ROOTS = ["ai", "config", "core", "ui", "utils"]
        MIN_LINES = 20

        def normalize(lines: list[str]) -> list[str]:
            out = []
            for line in lines:
                s = line.strip()
                if not s:
                    continue
                if s.startswith("#"):
                    continue
                out.append(s)
            return out

        def py_files() -> list[Path]:
            files: list[Path] = []
            for root in ROOTS:
                p = Path(root)
                if p.exists():
                    files.extend(p.rglob("*.py"))
            main = Path("main.py")
            if main.exists():
                files.append(main)
            return sorted(set(files))

        def main() -> None:
            blocks: dict[str, list[tuple[Path, int, int]]] = defaultdict(list)

            for path in py_files():
                text = path.read_text(encoding="utf-8", errors="replace").splitlines()
                cleaned = normalize(text)
                for i in range(0, max(0, len(cleaned) - MIN_LINES + 1)):
                    block = cleaned[i:i + MIN_LINES]
                    digest = hashlib.sha1("\\n".join(block).encode("utf-8")).hexdigest()
                    blocks[digest].append((path, i + 1, i + MIN_LINES))

            found = 0
            for _, refs in blocks.items():
                uniq = {(str(p), a, b) for p, a, b in refs}
                if len(uniq) > 1:
                    found += 1
                    print(f"DUPLICATION_GROUP {found}")
                    for p, a, b in sorted(uniq):
                        print(f"  - {p}:{a}-{b}")
                    print()

            if found == 0:
                print("Nenhuma duplicação literal relevante encontrada.")
            else:
                print(f"Total duplication groups: {found}")

        if __name__ == "__main__":
            main()
    """),
    "tests/conftest.py": dedent("""\
        from pathlib import Path
        import sys

        ROOT = Path(__file__).resolve().parents[1]
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))
    """),
    "tests/unit/test_project_structure.py": dedent("""\
        from pathlib import Path

        def test_main_exists() -> None:
            assert Path("main.py").exists(), "main.py deve existir na raiz"

        def test_expected_dirs_exist() -> None:
            for name in ["ai", "config", "core", "ui", "utils"]:
                assert Path(name).exists(), f"{name} deve existir"

        def test_qa_folder_exists() -> None:
            assert Path("QA").exists(), "QA deve existir"
    """),
    "tests/unit/test_python_files_compile.py": dedent("""\
        from pathlib import Path
        import py_compile

        def iter_py_files():
            for root in ["ai", "config", "core", "ui", "utils"]:
                p = Path(root)
                if p.exists():
                    yield from p.rglob("*.py")
            main = Path("main.py")
            if main.exists():
                yield main

        def test_python_files_compile_individually() -> None:
            failures = []
            for path in iter_py_files():
                try:
                    py_compile.compile(str(path), doraise=True)
                except Exception as exc:
                    failures.append(f"{path}: {exc}")
            assert not failures, "\\n".join(failures)
    """),
    "tests/unit/test_no_runtime_artifacts_committed.py": dedent("""\
        from pathlib import Path

        def test_no_pyc_committed_in_source_tree() -> None:
            offenders = [str(p) for p in Path(".").rglob("*.pyc") if ".venv" not in str(p)]
            assert not offenders, "Arquivos .pyc presentes na arvore: " + ", ".join(offenders[:50])
    """),
    "tests/integration/test_import_layers.py": dedent("""\
        import importlib
        from pathlib import Path

        def package_modules(root: str) -> list[str]:
            base = Path(root)
            mods = []
            if not base.exists():
                return mods
            for path in base.rglob("*.py"):
                if path.name == "__init__.py":
                    continue
                mods.append(".".join(path.with_suffix("").parts))
            return mods

        def test_import_core_modules() -> None:
            failures = []
            for mod in package_modules("core"):
                try:
                    importlib.import_module(mod)
                except Exception as exc:
                    failures.append(f"{mod}: {exc}")
            assert not failures, "\\n".join(failures)

        def test_import_config_modules() -> None:
            failures = []
            for mod in package_modules("config"):
                try:
                    importlib.import_module(mod)
                except Exception as exc:
                    failures.append(f"{mod}: {exc}")
            assert not failures, "\\n".join(failures)
    """),
    "tests/integration/test_main_import.py": dedent("""\
        import importlib.util
        from pathlib import Path

        def test_main_file_can_be_parsed() -> None:
            path = Path("main.py")
            assert path.exists()
            spec = importlib.util.spec_from_file_location("laserflix_main", path)
            assert spec is not None
            assert spec.loader is not None
    """),
    "tests/smoke/test_smoke_compile_ui.py": dedent("""\
        from pathlib import Path
        import py_compile

        def test_ui_tree_compiles() -> None:
            failures = []
            ui = Path("ui")
            if not ui.exists():
                raise AssertionError("Diretorio ui nao encontrado")
            for path in ui.rglob("*.py"):
                try:
                    py_compile.compile(str(path), doraise=True)
                except Exception as exc:
                    failures.append(f"{path}: {exc}")
            assert not failures, "\\n".join(failures)
    """),
    "diagnostico_laserflix_ambiente.bat": dedent(r"""\
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
    """),
}

SUSPECT_DIRS = ["QA", "tests"]
SUSPECT_FILES = ["pytest.ini", "mypy.ini", ".pylintrc", "diagnostico_laserflix_ambiente.bat"]

def remove_old_suspects() -> None:
    for rel in SUSPECT_DIRS:
        path = ROOT / rel
        if path.exists():
            shutil.rmtree(path)
    for rel in SUSPECT_FILES:
        path = ROOT / rel
        if path.exists():
            path.unlink()

def write_files() -> None:
    for rel, content in FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")

def main() -> None:
    print(f"Rebuilding strict QA structure in: {ROOT}")
    remove_old_suspects()
    write_files()
    (ROOT / "QA" / "reports").mkdir(parents=True, exist_ok=True)
    print("Done.")
    print()
    print("Rode exatamente estes comandos na raiz do projeto:")
    print(r"py rebuild_strict_qa.py")
    print(r"QA\01_install_dev_tools.bat")
    print(r"QA\10_run_all.bat")

if __name__ == "__main__":
    main()