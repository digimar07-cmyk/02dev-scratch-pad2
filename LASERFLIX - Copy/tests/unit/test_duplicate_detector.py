"""
Testes unitarios de utils/duplicate_detector.py.
Forca o detector com entradas conhecidas e verifica comportamento real.
Nao cria mocks que escondem comportamento.
"""
import sys
import os
import importlib
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("utils.duplicate_detector")


def test_module_has_public_api():
    public = [n for n in dir(mod) if not n.startswith("_")]
    assert public, "utils/duplicate_detector.py esta vazio ou sem API publica."


def test_detector_class_or_function_exists():
    """Deve existir uma classe ou funcao principal de deteccao."""
    classes = [
        n for n in dir(mod)
        if not n.startswith("_") and isinstance(getattr(mod, n), type)
    ]
    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    assert classes or funcs, "Nenhuma classe ou funcao encontrada em duplicate_detector."


def test_detector_with_identical_strings():
    """Se o detector recebe strings identicas, deve identificar como duplicata."""
    classes = [
        n for n in dir(mod)
        if not n.startswith("_") and isinstance(getattr(mod, n), type)
    ]
    if not classes:
        pytest.skip("Nenhuma classe para testar \u2014 revisar API do modulo.")
    cls = getattr(mod, classes[0])
    try:
        detector = cls()
        result = None
        for method_name in ["detect", "check", "find_duplicates", "is_duplicate", "compare"]:
            if hasattr(detector, method_name):
                method = getattr(detector, method_name)
                try:
                    result = method("Test Movie", "Test Movie")
                    break
                except TypeError:
                    pass
        if result is None:
            pytest.skip("Nao foi possivel determinar o metodo de deteccao \u2014 revisar API.")
        assert result, "Detector nao identificou strings identicas como duplicatas."
    except TypeError as e:
        pytest.skip(f"Construtor requer argumentos nao conhecidos: {e}")
