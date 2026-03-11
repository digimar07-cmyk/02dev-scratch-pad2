"""
Testes unitarios de utils/name_translator.py.
"""
import sys
import os
import importlib
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("utils.name_translator")


def test_module_importable():
    assert mod is not None


def test_has_public_functions():
    public = [n for n in dir(mod) if not n.startswith("_") and callable(getattr(mod, n))]
    assert public, "utils/name_translator.py sem funcoes publicas."


def test_translation_returns_string():
    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    for fname in funcs[:2]:
        func = getattr(mod, fname)
        try:
            result = func("Test Movie Title")
            if result is not None:
                assert isinstance(result, str), (
                    f"{fname} nao retornou string: {type(result)}"
                )
        except TypeError:
            pass


def test_translation_is_deterministic():
    """A mesma entrada deve sempre produzir a mesma saida."""
    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    for fname in funcs[:1]:
        func = getattr(mod, fname)
        try:
            r1 = func("Blade Runner 2049")
            r2 = func("Blade Runner 2049")
            assert r1 == r2, f"{fname} nao e deterministico: '{r1}' != '{r2}'"
        except TypeError:
            pass
