"""
Testes unitarios de core/collections_manager.py.
"""
import sys
import os
import importlib
import pytest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("core.collections_manager")


def test_importable():
    assert mod is not None


def test_has_class():
    classes = [
        n for n in dir(mod)
        if not n.startswith("_") and isinstance(getattr(mod, n), type)
    ]
    assert classes, "core/collections_manager.py nao tem classe publica."


def test_no_tkinter():
    content = (Path(ROOT) / "core" / "collections_manager.py").read_text(encoding="utf-8")
    assert "import tkinter" not in content, (
        "core/collections_manager importa tkinter \u2014 VIOLACAO ARQUITETURAL."
    )
    assert "from tkinter" not in content, (
        "core/collections_manager importa tkinter \u2014 VIOLACAO ARQUITETURAL."
    )
