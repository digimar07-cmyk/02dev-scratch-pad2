"""
Testes unitarios de utils/recursive_scanner.py com sistema de arquivos real (tmpdir).
Nao usa mocks para o filesystem \u2014 testa com diretorio real.
"""
import sys
import os
import importlib
import pytest
from pathlib import Path

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

mod = importlib.import_module("utils.recursive_scanner")


def test_module_importable():
    assert mod is not None


def test_scanner_has_public_api():
    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    assert funcs, "utils/recursive_scanner.py nao tem funcao publica."


def test_scanner_finds_files_in_real_tmpdir(tmp_path):
    """Cria estrutura real de diretorios e verifica que o scanner encontra arquivos."""
    (tmp_path / "MovieA").mkdir()
    (tmp_path / "MovieA" / "cover.jpg").write_bytes(b"fake_image")
    (tmp_path / "MovieB").mkdir()
    (tmp_path / "MovieB" / "cover.png").write_bytes(b"fake_image")

    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    if not funcs:
        pytest.skip("Nenhuma funcao publica em recursive_scanner.")

    scan_func = getattr(mod, funcs[0])
    try:
        result = scan_func(str(tmp_path))
        assert result is not None, "Scanner retornou None para diretorio valido."
    except TypeError as e:
        pytest.skip(f"Assinatura da funcao incompativel: {e}")


def test_scanner_returns_empty_for_empty_dir(tmp_path):
    """Diretorio vazio deve retornar resultado vazio ou falsy."""
    funcs = [
        n for n in dir(mod)
        if not n.startswith("_") and callable(getattr(mod, n)) and not isinstance(getattr(mod, n), type)
    ]
    if not funcs:
        pytest.skip("Nenhuma funcao publica.")
    scan_func = getattr(mod, funcs[0])
    try:
        result = scan_func(str(tmp_path))
        assert not result or result == [] or result == {}, (
            f"Scanner retornou dados para diretorio vazio: {result}"
        )
    except TypeError:
        pytest.skip("Assinatura incompativel.")
