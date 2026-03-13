"""
Testa a fronteira arquitetural de core/virtual_scroll_manager.py.
Se este arquivo importa tkinter, esta na camada errada.
Falha aqui = violacao arquitetural real.
"""
import ast
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def test_virtual_scroll_manager_architecture():
    vsm = ROOT / "core" / "virtual_scroll_manager.py"
    content = vsm.read_text(encoding="utf-8")
    tree = ast.parse(content)

    tk_imports = []
    ui_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if "tkinter" in a.name or "customtkinter" in a.name:
                    tk_imports.append(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                if "tkinter" in node.module:
                    tk_imports.append(node.module)
                if node.module.startswith("ui"):
                    ui_imports.append(node.module)

    violations = []
    if tk_imports:
        violations.append(f"Importa tkinter: {tk_imports}")
    if ui_imports:
        violations.append(f"Importa ui/: {ui_imports}")

    assert not violations, (
        f"core/virtual_scroll_manager.py VIOLA FRONTEIRA ARQUITETURAL:\n"
        + "\n".join(violations)
        + "\nVirtualScroll com dependencia de UI pertence a ui/, nao a core/."
    )
