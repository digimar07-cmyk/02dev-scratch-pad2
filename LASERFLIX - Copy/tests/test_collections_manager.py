"""
tests/test_collections_manager.py — TANAKA-05

Cobre: CollectionsManager (create, rename, delete, add_project,
       remove_project, clean_orphans, get_stats, persistência)

Nota: CollectionsManager usa nome-como-chave (não UUID).
Todos os métodos foram calibrados para a API real do arquivo.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.collections_manager import CollectionsManager


@pytest.fixture
def col(tmp_path, monkeypatch):
    """CollectionsManager com arquivo temporário, sem depender de DB_FILE."""
    col_file = str(tmp_path / "collections.json")
    # Override do COLLECTIONS_FILE global para apontar ao tmp
    import core.collections_manager as cm_module
    monkeypatch.setattr(cm_module, "COLLECTIONS_FILE", col_file)
    manager = CollectionsManager()
    return manager


# ── Criar Coleções ─────────────────────────────────────────────────────

class TestCreateCollection:
    def test_create_retorna_true(self, col):
        assert col.create_collection("Logos") is True

    def test_create_aparece_na_lista(self, col):
        col.create_collection("Natal")
        assert "Natal" in col.get_all_collections()

    def test_create_duplicada_retorna_false(self, col):
        col.create_collection("Logos")
        assert col.create_collection("Logos") is False

    def test_create_nome_vazio_retorna_false(self, col):
        assert col.create_collection("") is False

    def test_add_collection_alias(self, col):
        assert col.add_collection("Via Alias") is True
        assert "Via Alias" in col.get_all_collections()


# ── Renomear / Deletar ─────────────────────────────────────────────────

class TestRenameDeleteCollection:
    def test_rename_funciona(self, col):
        col.create_collection("Old")
        assert col.rename_collection("Old", "New") is True
        assert "New" in col.get_all_collections()
        assert "Old" not in col.get_all_collections()

    def test_rename_preserva_projetos(self, col):
        col.create_collection("Old")
        col.add_project("Old", "/proj/x")
        col.rename_collection("Old", "New")
        assert "/proj/x" in col.get_projects("New")

    def test_delete_remove_colecao(self, col):
        col.create_collection("Para Deletar")
        assert col.delete_collection("Para Deletar") is True
        assert "Para Deletar" not in col.get_all_collections()

    def test_delete_inexistente_retorna_false(self, col):
        assert col.delete_collection("Fantasma") is False


# ── Projetos em Coleções ───────────────────────────────────────────────

class TestProjectsInCollection:
    def test_add_projeto_a_colecao(self, col):
        col.create_collection("Favoritos")
        assert col.add_project("Favoritos", "/proj/x") is True
        assert "/proj/x" in col.get_projects("Favoritos")

    def test_add_projeto_duplicado_retorna_false(self, col):
        col.create_collection("Favoritos")
        col.add_project("Favoritos", "/proj/x")
        assert col.add_project("Favoritos", "/proj/x") is False

    def test_remove_projeto_da_colecao(self, col):
        col.create_collection("Favoritos")
        col.add_project("Favoritos", "/proj/x")
        assert col.remove_project("Favoritos", "/proj/x") is True
        assert "/proj/x" not in col.get_projects("Favoritos")

    def test_projeto_em_multiplas_colecoes(self, col):
        col.create_collection("A")
        col.create_collection("B")
        col.add_project("A", "/proj/x")
        col.add_project("B", "/proj/x")
        colecoes = col.get_project_collections("/proj/x")
        assert set(colecoes) == {"A", "B"}

    def test_is_project_in_collection(self, col):
        col.create_collection("Test")
        col.add_project("Test", "/proj/x")
        assert col.is_project_in_collection("Test", "/proj/x") is True
        assert col.is_project_in_collection("Test", "/proj/y") is False


# ── Utiliários ────────────────────────────────────────────────────────────

class TestUtilities:
    def test_clean_orphans_remove_paths_invalidos(self, col):
        col.create_collection("Test")
        col.add_project("Test", "/proj/ghost")
        col.add_project("Test", "/proj/real")
        removed = col.clean_orphan_projects({"/proj/real"})
        assert removed == 1
        assert "/proj/ghost" not in col.get_projects("Test")
        assert "/proj/real" in col.get_projects("Test")

    def test_clean_orphans_sem_fantasmas_retorna_zero(self, col):
        col.create_collection("Test")
        col.add_project("Test", "/proj/real")
        removed = col.clean_orphan_projects({"/proj/real"})
        assert removed == 0

    def test_get_stats(self, col):
        col.create_collection("A")
        col.create_collection("B")
        col.add_project("A", "/proj/x")
        col.add_project("B", "/proj/x")  # mesmo proj em 2 coleções
        col.add_project("B", "/proj/y")
        stats = col.get_stats()
        assert stats["total_collections"] == 2
        assert stats["total_entries"] == 3
        assert stats["unique_projects"] == 2

    def test_persistencia_reload(self, col, tmp_path, monkeypatch):
        col.create_collection("Persistida")
        col.add_project("Persistida", "/proj/z")

        import core.collections_manager as cm_module
        col_file = cm_module.COLLECTIONS_FILE
        manager2 = CollectionsManager()
        assert "Persistida" in manager2.get_all_collections()
        assert "/proj/z" in manager2.get_projects("Persistida")
