"""
Testes unitarios de core/database.py.
"""
import sys
import os
import importlib
import inspect
import pytest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("core.database")


def test_importable():
    assert mod is not None


def test_has_class():
    classes = [
        n for n in dir(mod)
        if not n.startswith("_") and isinstance(getattr(mod, n), type)
    ]
    assert classes, "core/database.py nao expoe classe publica."


def test_no_tkinter_in_database():
    content = (Path(ROOT) / "core" / "database.py").read_text(encoding="utf-8")
    assert "import tkinter" not in content, (
        "core/database.py importa tkinter \u2014 VIOLACAO CRITICA."
    )
    assert "from tkinter" not in content, (
        "core/database.py importa tkinter \u2014 VIOLACAO CRITICA."
    )


def test_text_generator_importable():
    """ai/text_generator.py com 21KB deve ser importavel e ter conteudo."""
    mod2 = importlib.import_module("ai.text_generator")
    assert mod2 is not None
    classes = [
        n for n in dir(mod2)
        if not n.startswith("_") and isinstance(getattr(mod2, n), type)
    ]
    funcs = [
        n for n in dir(mod2)
        if not n.startswith("_") and callable(getattr(mod2, n)) and not isinstance(getattr(mod2, n), type)
    ]
    assert classes or funcs, (
        "ai/text_generator.py com 21KB sem conteudo publico \u2014 import quebrado."
    )
