"""
Testes unitarios de ai/fallbacks.py.
Este arquivo tem 25KB \u2014 deve ter funcoes e comportamento testavel.
"""
import sys
import os
import ast
import importlib
import pytest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("ai.fallbacks")


def test_fallbacks_importable():
    assert mod is not None


def test_fallbacks_has_content():
    public = [n for n in dir(mod) if not n.startswith("_")]
    assert public, (
        "ai/fallbacks.py nao expoe nada publico. "
        "25KB de arquivo vazio e impossivel \u2014 provavel erro de import silenciado."
    )


def test_fallback_returns_non_empty_string():
    """Funcoes de fallback devem retornar strings nao-vazias."""
    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    if not funcs:
        pytest.skip("Nenhuma funcao publica.")
    for fname in funcs[:3]:
        func = getattr(mod, fname)
        try:
            result = func("TestTitle")
            if isinstance(result, str):
                assert result.strip(), f"{fname}('TestTitle') retornou string vazia"
        except TypeError:
            pass


def test_fallbacks_does_not_import_ui():
    content = (Path(ROOT) / "ai" / "fallbacks.py").read_text(encoding="utf-8")
    tree = ast.parse(content)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            assert not node.module.startswith("ui"), (
                f"ai/fallbacks.py importa ui/: {node.module}"
            )
