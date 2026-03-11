"""
Detecta dependencias circulares entre modulos.
Estrategia: tenta importar cada modulo em processo isolado com subprocess.
Falha real = circular import, import quebrado, ou dependencia de UI sem display.
"""
import subprocess
import sys
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent

MODULES_TO_CHECK = [
    "config.constants",
    "config.settings",
    "config.ui_constants",
    "config.card_layout",
    "utils.logging_setup",
    "utils.text_utils",
    "utils.platform_utils",
    "utils.recursive_scanner",
    "utils.duplicate_detector",
    "utils.name_translator",
    "core.database",
    "core.collections_manager",
    "core.project_scanner",
    "core.protocols",
    "core.thumbnail_cache",
    "ai.ollama_client",
    "ai.image_analyzer",
    "ai.analysis_manager",
]


def attempt_import(module: str):
    """Tenta importar modulo em subprocesso isolado para detectar circular imports."""
    result = subprocess.run(
        [sys.executable, "-c", f"import sys; sys.path.insert(0, r'{ROOT}'); import {module}"],
        capture_output=True,
        text=True,
        timeout=15,
        cwd=str(ROOT),
    )
    if result.returncode != 0:
        return False, result.stderr.strip()
    return True, ""


@pytest.mark.parametrize("module", MODULES_TO_CHECK)
def test_module_importable_without_circular_dependency(module):
    """
    Cada modulo core/utils/config/ai deve ser importavel sem circular import.
    Falha indica: circular import, dependencia quebrada, ou import de tkinter sem display.
    """
    success, error = attempt_import(module)
    assert success, (
        f"Modulo '{module}' falhou ao importar:\n{error}\n"
        "Pode indicar: circular import, dependencia quebrada, ou import de tkinter sem display."
    )
