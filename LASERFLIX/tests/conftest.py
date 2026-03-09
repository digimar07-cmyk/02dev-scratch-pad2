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
            db = DatabaseManager()
            db.db_file = temp_db_file
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
    
    Returns:
        dict: Database válido com projetos de teste
    """
    return {
        "/path/to/project1": {
            "name": "Project 1",
            "path": "/path/to/project1",
            "category": "Engraving",
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
            "category": "Cutting",
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
            "category": "Engraving",
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
