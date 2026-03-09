"""
tests/conftest.py — Fixtures compartilhadas (TANAKA-02)

Fixtures disponíveis para todos os testes:
    tmp_db              DatabaseManager vazio em pasta temporária
    tmp_db_with_data    DatabaseManager com 3 projetos pré-carregados
    tmp_collections     CollectionsManager em pasta temporária
                        (usa monkeypatch no COLLECTIONS_FILE global
                         pois CollectionsManager não aceita path no __init__)
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

# Garante root do projeto no sys.path para imports absolutos
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture
def tmp_db(tmp_path):
    """DatabaseManager com banco de dados temporário vazio."""
    from core.database import DatabaseManager
    return DatabaseManager(db_file=str(tmp_path / "test_db.json"))


@pytest.fixture
def tmp_db_with_data(tmp_path):
    """DatabaseManager com 3 projetos pré-carregados e persistidos."""
    from core.database import DatabaseManager
    db = DatabaseManager(db_file=str(tmp_path / "test_db.json"))
    db.database = {
        "/proj/alpha": {"name": "Alpha", "categories": ["Motion"], "tags": [], "favorite": False},
        "/proj/beta":  {"name": "Beta",  "categories": ["Print"],  "tags": ["logo"], "favorite": False},
        "/proj/gamma": {"name": "Gamma", "categories": ["Motion"], "tags": [], "favorite": True},
    }
    db.save_database()
    return db


@pytest.fixture
def tmp_collections(tmp_path, monkeypatch):
    """
    CollectionsManager apontando para arquivo temporário.

    CollectionsManager usa COLLECTIONS_FILE como global — não aceita path
    no __init__. Usamos monkeypatch para redirecionar antes de instanciar.
    """
    import core.collections_manager as cm_module
    col_file = str(tmp_path / "collections.json")
    monkeypatch.setattr(cm_module, "COLLECTIONS_FILE", col_file)
    from core.collections_manager import CollectionsManager
    return CollectionsManager()
