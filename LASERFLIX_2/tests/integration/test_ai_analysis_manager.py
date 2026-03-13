"""
Testa contratos basicos do ai/analysis_manager.py sem chamar Ollama real.
"""
import sys
import ast
import pytest
import importlib
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


def test_analysis_manager_importable():
    from ai import analysis_manager
    assert analysis_manager is not None


def test_analysis_manager_has_public_class():
    mod = importlib.import_module("ai.analysis_manager")
    classes = [
        n for n in dir(mod)
        if not n.startswith("_") and isinstance(getattr(mod, n), type)
    ]
    assert classes, "ai/analysis_manager.py nao expoe classe publica."


def test_analysis_manager_does_not_import_ui():
    """AI layer nao pode depender de UI."""
    path = ROOT / "ai" / "analysis_manager.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    ui_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("ui"):
                ui_imports.append(node.module)
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.startswith("ui"):
                    ui_imports.append(a.name)
    assert not ui_imports, (
        f"ai/analysis_manager.py importa ui/: {ui_imports}\n"
        "AI layer nao pode depender de UI."
    )
