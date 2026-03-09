"""
conftest.py — Fixtures compartilhadas entre todos os testes
"""
import pytest
import os
import json
import tempfile
from pathlib import Path


@pytest.fixture
def temp_db_file():
    """
    Cria arquivo temporário para testar DatabaseManager.
    
    Uso:
        def test_save(temp_db_file):
            db = DatabaseManager(db_file=temp_db_file)
            db.save_database()
    """
    fd, path = tempfile.mkstemp(suffix=".json")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.unlink(path)


@pytest.fixture
def sample_database():
    """
    Database mock com 3 projetos para testes.
    
    IMPORTANTE: Usa schema LEGADO com 'category' (string) para testar migração.
    DatabaseManager deve converter automaticamente para 'categories' (lista) ao carregar.
    
    Returns:
        dict: Database válido com projetos de teste
    """
    return {
        "/path/to/project1": {
            "name": "Project 1",
            "path": "/path/to/project1",
            "category": "Engraving",  # SCHEMA LEGADO (string)
            "tags": ["test", "sample"],
            "favorite": True,
            "done": False,
            "good": False,
            "bad": False,
            "analyzed": True,
            "origin": "/path/to",
        },
        "/path/to/project2": {
            "name": "Project 2",
            "path": "/path/to/project2",
            "category": "Cutting",  # SCHEMA LEGADO (string)
            "tags": ["test"],
            "favorite": False,
            "done": True,
            "good": True,
            "bad": False,
            "analyzed": True,
            "origin": "/path/to",
        },
        "/other/project3": {
            "name": "Project 3",
            "path": "/other/project3",
            "category": "Engraving",  # SCHEMA LEGADO (string)
            "tags": [],
            "favorite": False,
            "done": False,
            "good": False,
            "bad": True,
            "analyzed": False,
            "origin": "/other",
        },
    }


@pytest.fixture
def sample_database_new_schema():
    """
    Database mock usando SCHEMA NOVO com 'categories' (lista).
    
    Use esta fixture para testar comportamento com dados já migrados.
    
    Returns:
        dict: Database com schema novo
    """
    return {
        "/path/to/project1": {
            "name": "Project 1",
            "path": "/path/to/project1",
            "categories": ["Engraving"],  # SCHEMA NOVO (lista)
            "tags": ["test", "sample"],
            "favorite": True,
            "done": False,
            "good": False,
            "bad": False,
            "analyzed": True,
            "origin": "/path/to",
        },
        "/path/to/project2": {
            "name": "Project 2",
            "path": "/path/to/project2",
            "categories": ["Cutting"],  # SCHEMA NOVO (lista)
            "tags": ["test"],
            "favorite": False,
            "done": True,
            "good": True,
            "bad": False,
            "analyzed": True,
            "origin": "/path/to",
        },
    }


@pytest.fixture
def sample_collections():
    """
    Collections mock para testes.
    
    Returns:
        dict: Collections válidas
    """
    return {
        "Favorites": {
            "projects": ["/path/to/project1"],
            "created_at": "2026-01-01",
        },
        "Done": {
            "projects": ["/path/to/project2"],
            "created_at": "2026-01-02",
        },
    }


@pytest.fixture
def mock_canvas():
    """
    Mock de tk.Canvas para testes de controllers.
    """
    class MockCanvas:
        def yview_scroll(self, *args): pass
        def yview_moveto(self, *args): pass
    
    return MockCanvas()


@pytest.fixture
def mock_frame():
    """
    Mock de tk.Frame para testes de controllers.
    """
    class MockFrame:
        def winfo_children(self): return []
    
    return MockFrame()
