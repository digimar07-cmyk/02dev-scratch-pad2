"""
conftest.py — Fixtures globais do Laserflix v4.0

Regras:
- Cada fixture tem responsabilidade unica
- Nenhum mock automatico global
- Nenhuma inicializacao de Tkinter aqui
- Fixtures com 'tmp_path' garantem isolamento total entre testes

Disponivel para todos os testes automaticamente (sem import).
"""
import sys
import os
import pytest

# Garante que o projeto esta no path independente de onde pytest eh executado
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ── Fixtures de Path ────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def project_root():
    """Caminho absoluto da raiz do projeto LASERFLIX_2/"""
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def source_modules():
    """Modulos-fonte do projeto. Usado em testes estruturais."""
    return ["ai", "config", "core", "utils", "ui"]


# ── Fixtures de Dados ────────────────────────────────────────────────────────

@pytest.fixture
def sample_project():
    """
    Projeto de exemplo com todos os campos obrigatorios.
    Usado como base para testes de database, UI e AI.
    """
    return {
        "name": "Projeto Teste",
        "categories": ["Acao", "Drama"],
        "tags": ["hd", "dublado"],
        "analyzed": True,
        "analyzed_model": "llama3",
        "favorite": False,
        "done": False,
        "good": False,
        "bad": False,
        "origin": "Pasta Local",
        "description": "Descricao de teste para o projeto"
    }


@pytest.fixture
def sample_project_unanalyzed():
    """Projeto sem analise de IA. Para testar estado inicial."""
    return {
        "name": "Projeto Sem Analise",
        "categories": [],
        "tags": [],
        "analyzed": False,
        "analyzed_model": None,
        "favorite": False,
        "done": False,
        "good": False,
        "bad": False,
        "origin": "Desconhecido",
        "description": ""
    }


# ── Fixtures de Database ─────────────────────────────────────────────────────

@pytest.fixture
def tmp_db(tmp_path):
    """
    DatabaseManager isolado em diretorio temporario.
    Cada teste recebe seu proprio banco vazio.
    Nao contamina o banco real do projeto.
    """
    from core.database import DatabaseManager
    return DatabaseManager(
        db_file=str(tmp_path / "test_database.json"),
        config_file=str(tmp_path / "test_config.json")
    )


@pytest.fixture
def populated_db(tmp_db, sample_project):
    """
    DatabaseManager com 10 projetos pre-carregados.
    Para testes que precisam de dados existentes.
    """
    for i in range(10):
        path = f"/fake/path/projeto_{i}"
        data = {**sample_project, "name": f"Projeto {i}"}
        if i % 3 == 0:
            data["favorite"] = True
        if i % 4 == 0:
            data["analyzed"] = False
        tmp_db.set_project(path, data)
    return tmp_db


@pytest.fixture
def tmp_collections(tmp_path, tmp_db):
    """
    CollectionsManager isolado em diretorio temporario.
    Depende de tmp_db para consistencia.
    """
    from core.collections_manager import CollectionsManager
    return CollectionsManager(
        db_manager=tmp_db,
        collections_file=str(tmp_path / "test_collections.json")
    )
