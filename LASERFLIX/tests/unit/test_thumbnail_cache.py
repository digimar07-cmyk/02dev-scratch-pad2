"""
Testes unitarios de core/thumbnail_cache.py.
Verifica logica de cache sem depender de UI.
"""
import sys
import os
import importlib
import pytest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("core.thumbnail_cache")


def test_thumbnail_cache_importable():
    assert mod is not None


def test_cache_has_public_class():
    classes = [
        n for n in dir(mod)
        if not n.startswith("_") and isinstance(getattr(mod, n), type)
    ]
    assert classes, "core/thumbnail_cache.py nao expoe classe publica."


def test_cache_does_not_import_tkinter():
    content = (Path(ROOT) / "core" / "thumbnail_cache.py").read_text(encoding="utf-8")
    assert "import tkinter" not in content, (
        "core/thumbnail_cache.py importa tkinter. "
        "Cache de thumbnails e logica de core \u2014 nao deve depender de UI."
    )
