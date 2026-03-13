"""
Testa que database_controller.py esta na camada certa
e que seus contratos de interface sao mantidos.
"""
import sys
import ast
import pytest
import importlib
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


def test_database_controller_has_no_tkinter():
    """database_controller em core/ nao pode ter tkinter."""
    path = ROOT / "core" / "database_controller.py"
    content = path.read_text(encoding="utf-8")
    assert "import tkinter" not in content
    assert "from tkinter" not in content
    assert "import customtkinter" not in content


def test_database_controller_public_interface():
    """database_controller.py deve expor ao menos uma classe ou funcao publica."""
    mod = importlib.import_module("core.database_controller")
    public = [name for name in dir(mod) if not name.startswith("_")]
    assert public, "core.database_controller nao expoe nada publico. Modulo vazio ou quebrado."


def test_core_database_has_public_class():
    """core.database deve ter ao menos uma classe instanciavel."""
    mod = importlib.import_module("core.database")
    classes = [
        name for name in dir(mod)
        if not name.startswith("_") and isinstance(getattr(mod, name), type)
    ]
    assert classes, "Nenhuma classe publica em core.database"
