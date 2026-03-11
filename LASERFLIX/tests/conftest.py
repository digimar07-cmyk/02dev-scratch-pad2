"""
conftest.py \u2014 Configuracao global dos testes LASERFLIX.
NAO contem mocks automaticos.
NAO suprime excecoes.
NAO inicializa Tkinter globalmente.
Cada teste e responsavel pelo seu proprio setup.
"""
import sys
import os
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="session")
def project_root():
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def source_modules():
    """Retorna os modulos-fonte esperados do projeto."""
    return ["ai", "config", "core", "utils", "ui"]
