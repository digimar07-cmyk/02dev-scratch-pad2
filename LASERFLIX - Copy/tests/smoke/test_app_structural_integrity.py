"""
Smoke test de integridade estrutural da aplicacao.
Verifica contratos minimos entre camadas sem subir a janela grafica.
"""
import sys
import os
import ast
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


def test_main_window_direct_core_imports():
    """
    ui/main_window.py importar core/ diretamente e acoplamento perigoso.
    Controllers devem intermediar o acesso.
    """
    mw_path = ROOT / "ui" / "main_window.py"
    assert mw_path.exists(), "ui/main_window.py nao encontrado"
    tree = ast.parse(mw_path.read_text(encoding="utf-8"))
    direct_core_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.module.startswith("core."):
                direct_core_imports.append(node.module)
    assert not direct_core_imports, (
        f"ui/main_window.py importa core/ diretamente: {direct_core_imports}\n"
        "Risco: UI acoplada diretamente a camada de dados. Deveria usar controllers."
    )


def test_virtual_scroll_manager_not_tkinter():
    """
    core/virtual_scroll_manager.py: se importar tkinter, esta na camada errada.
    VirtualScroll com dependencia de UI pertence a ui/, nao a core/.
    """
    vsm_path = ROOT / "core" / "virtual_scroll_manager.py"
    assert vsm_path.exists(), "core/virtual_scroll_manager.py nao encontrado"
    content = vsm_path.read_text(encoding="utf-8")
    tree = ast.parse(content)
    tk_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if "tkinter" in a.name:
                    tk_imports.append(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module and "tkinter" in node.module:
                tk_imports.append(node.module)
    assert not tk_imports, (
        f"core/virtual_scroll_manager.py importa tkinter: {tk_imports}\n"
        "VIOLACAO: core/ nao pode depender de UI. Mover para ui/ ou refatorar."
    )


def test_database_controller_no_tkinter():
    """
    core/database_controller.py nao deve importar tkinter.
    Se importar, esta na camada errada.
    """
    dbc_path = ROOT / "core" / "database_controller.py"
    assert dbc_path.exists(), "core/database_controller.py nao encontrado"
    content = dbc_path.read_text(encoding="utf-8")
    assert "tkinter" not in content, (
        "core/database_controller.py contem referencia a tkinter.\n"
        "VIOLACAO ARQUITETURAL: controllers de UI nao pertencem a core/."
    )


def test_keyword_maps_line_count():
    """
    ai/keyword_maps.py tem ~54KB. Verifica se e dado puro ou logica.
    Arquivo de logica com 54KB e smell critico.
    Se > 2000 linhas e tiver funcoes, deve ser decomposto.
    """
    km_path = ROOT / "ai" / "keyword_maps.py"
    assert km_path.exists()
    content = km_path.read_text(encoding="utf-8")
    tree = ast.parse(content)
    functions = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]
    line_count = len(content.splitlines())
    assert not (line_count > 2000 and len(functions) > 10), (
        f"ai/keyword_maps.py tem {line_count} linhas e {len(functions)} funcoes.\n"
        "Se contem logica, deve ser decomposto. Se sao dados, mover para JSON/CSV."
    )


def test_main_window_file_size():
    """ui/main_window.py nao deve exceder 300 linhas (FILE_SIZE_LIMIT_RULE)."""
    mw_path = ROOT / "ui" / "main_window.py"
    content = mw_path.read_text(encoding="utf-8")
    line_count = len(content.splitlines())
    assert line_count <= 300, (
        f"ui/main_window.py tem {line_count} linhas. Limite: 300.\n"
        "Arquivo monolitico de UI. Decomponha em componentes menores."
    )
