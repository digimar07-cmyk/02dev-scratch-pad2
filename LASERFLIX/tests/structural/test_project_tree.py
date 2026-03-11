"""
Validacao estrutural da arvore do projeto.
Falha se arquivos essenciais estiverem ausentes.
Falha se artefatos proibidos estiverem no source tree.
"""
import os
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


REQUIRED_FILES = [
    "main.py",
    "ai/__init__.py",
    "config/__init__.py",
    "core/__init__.py",
    "utils/__init__.py",
    "ui/__init__.py",
    "config/constants.py",
    "config/settings.py",
    "core/database.py",
    "core/collections_manager.py",
    "ui/main_window.py",
    "utils/logging_setup.py",
]


@pytest.mark.parametrize("relative_path", REQUIRED_FILES)
def test_required_file_exists(relative_path):
    """Todo arquivo essencial do projeto deve existir."""
    full_path = ROOT / relative_path
    assert full_path.exists(), f"Arquivo essencial ausente: {relative_path}"
    assert full_path.stat().st_size > 0, f"Arquivo essencial esta vazio: {relative_path}"


def test_no_backup_files_in_source():
    """
    Arquivos .backup commitados contaminam analise.
    Devem ser removidos do source tree.
    EXCECAO: diretorio laserflix_backups intencional.
    """
    violations = []
    for path in ROOT.rglob("*"):
        name = path.name.lower()
        if ".backup" in name or name.endswith(".bak") or name.endswith(".orig"):
            if "laserflix_backups" not in str(path):
                violations.append(str(path.relative_to(ROOT)))
    assert not violations, (
        f"Arquivos .backup encontrados no source tree (contaminacao de analise):\n"
        + "\n".join(violations)
    )


def test_managers_has_init():
    """ui/managers/ deve ter __init__.py para garantir resolucao de imports."""
    init_path = ROOT / "ui" / "managers" / "__init__.py"
    assert init_path.exists(), (
        "ui/managers/__init__.py esta ausente. "
        "Imports do tipo 'from ui.managers.X import Y' podem falhar silenciosamente."
    )


def test_no_pycache_in_git():
    """__pycache__ nao deve ser rastreado pelo git."""
    gitignore = ROOT / ".gitignore"
    if not gitignore.exists():
        pytest.fail(".gitignore ausente. __pycache__ pode estar sendo commitado.")
    content = gitignore.read_text(encoding="utf-8")
    assert "__pycache__" in content, ".gitignore nao exclui __pycache__"
    assert "*.pyc" in content, ".gitignore nao exclui *.pyc"


def test_loose_py_files_in_root_are_documented():
    """
    Arquivos .py soltos na raiz (fora dos modulos) devem ser justificados.
    main.py e aceitavel. backup_manager, version_manager, refactor_monitor sao suspeitos
    mas documentados. Qualquer outro e violacao.
    """
    accepted_root_py = {"main.py", "backup_manager.py", "version_manager.py", "refactor_monitor.py"}
    root_py_files = {f.name for f in ROOT.glob("*.py")}
    undocumented = root_py_files - accepted_root_py
    assert not undocumented, (
        f"Arquivos .py na raiz nao catalogados: {undocumented}. "
        "Adicionar ao set accepted_root_py com justificativa OU mover para modulo correto."
    )
