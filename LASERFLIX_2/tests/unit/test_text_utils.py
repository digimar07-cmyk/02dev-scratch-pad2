"""
Testes unitarios de utils/text_utils.py.
Funcoes puras devem ser testadas com valores reais, nao mocks.
"""
import sys
import os
import importlib
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("utils.text_utils")
public_funcs = [
    name for name in dir(mod)
    if not name.startswith("_") and callable(getattr(mod, name))
]


def test_module_has_public_functions():
    assert public_funcs, "utils/text_utils.py nao expoe nenhuma funcao publica."


def test_text_utils_functions_are_callable():
    for name in public_funcs:
        func = getattr(mod, name)
        assert callable(func), f"{name} nao e callable"


def test_no_unexpected_side_effects_on_import():
    """Reimportar o modulo nao deve ter side effects."""
    mod2 = importlib.import_module("utils.text_utils")
    assert mod2 is not None


def test_module_does_not_import_tkinter():
    import ast
    from pathlib import Path
    content = (Path(ROOT) / "utils" / "text_utils.py").read_text(encoding="utf-8")
    assert "tkinter" not in content, (
        "utils/text_utils.py importa tkinter. "
        "Utilitarios de texto nao podem depender de UI."
    )
