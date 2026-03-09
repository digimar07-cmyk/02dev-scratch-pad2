"""
conftest.py — Fixtures compartilhadas para todos os testes

Fornece:
  - temp_db_file: Banco de dados temporário (auto-cleanup)
  - sample_database: Dados de exemplo para testes
  - mock_canvas: Mock de tk.Canvas
  - mock_frame: Mock de tk.Frame
"""
import pytest
import tempfile
import os
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_db_file():
    """
    Cria arquivo temporário para database de testes.
    Cleanup automático após cada teste.
    """
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    yield path
    
    # Cleanup
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


@pytest.fixture
def sample_database():
    """
    Retorna dicionário de exemplo para testes de database.
    Simula estrutura de projetos do LASERFLIX.
    """
    return {
        "/path/to/project1": {
            "name": "Christmas Tree",
            "origin": "Etsy",
            "favorite": False,
            "done": False,
            "good": False,
            "bad": False,
            "categories": ["Natal", "Decoração", "Sala"],
            "tags": ["christmas", "tree", "decoration"],
            "analyzed": True,
            "ai_description": "Uma árvore de Natal decorativa.",
            "added_date": "2024-01-15T10:30:00",
        },
        "/path/to/project2": {
            "name": "Wooden Box",
            "origin": "Creative Fabrica",
            "favorite": True,
            "done": False,
            "good": True,
            "bad": False,
            "categories": ["Caixa", "Organizador", "Escritório"],
            "tags": ["box", "wood", "storage"],
            "analyzed": True,
            "ai_description": "Uma caixa organizadora de madeira.",
            "added_date": "2024-02-20T14:45:00",
        },
        "/path/to/project3": {
            "name": "Baby Mirror",
            "origin": "Etsy",
            "favorite": False,
            "done": True,
            "good": False,
            "bad": False,
            "categories": ["Bebê", "Espelho", "Quarto Infantil"],
            "tags": ["baby", "mirror", "nursery"],
            "analyzed": False,
            "ai_description": "",
            "added_date": "2024-03-10T09:15:00",
        }
    }


@pytest.fixture
def mock_canvas():
    """
    Mock de tk.Canvas para testes de UI.
    Simula métodos essenciais sem inicializar Tkinter.
    """
    canvas = MagicMock()
    canvas.winfo_height.return_value = 1080
    canvas.winfo_width.return_value = 1920
    canvas.yview.return_value = (0.0, 0.5)
    canvas.yview_moveto = Mock()
    canvas.yview_scroll = Mock()
    canvas.bind = Mock()
    return canvas


@pytest.fixture
def mock_frame():
    """
    Mock de tk.Frame para testes de UI.
    Simula widgets filhos e métodos de layout.
    """
    frame = MagicMock()
    frame.winfo_children.return_value = []
    frame.grid = Mock()
    frame.pack = Mock()
    frame.grid_forget = Mock()
    frame.destroy = Mock()
    return frame


@pytest.fixture
def sample_collections():
    """
    Retorna dicionário de exemplo para testes de coleções.
    """
    return {
        "Natal 2024": ["/path/to/project1"],
        "Favoritos": ["/path/to/project2"],
        "Para Revisar": ["/path/to/project3"],
    }
