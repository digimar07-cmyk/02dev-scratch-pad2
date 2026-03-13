"""
tests/unit/test_collections_manager_extended.py

Cobre linhas ainda não testadas de core/collections_manager.py:
  68-80   load() com JSON corrompido e Exception genérica
  95-104  save() com erro de I/O
  110     add_collection() alias
  217-218 clean_orphan_projects() com removções
  221-222 clean_orphan_projects() sem remoções (count == 0)
  234     get_stats() total_entries
  238     get_stats() unique_projects

Regra: NUNCA alterar testes. Bugs são no app.
"""
import os
import sys
import json
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.collections_manager import CollectionsManager


def make_cm(tmp_path):
    return CollectionsManager(file_path=str(tmp_path / "collections.json"))


# ═ load() caminhos de erro ═══════════════════════════════════════════

class TestCollectionsManagerLoadErrors:

    def test_dado_json_corrompido_quando_load_entao_collections_vazio(self, tmp_path):
        path = tmp_path / "collections.json"
        path.write_text("{ INVALIDO JSON !!!", encoding="utf-8")
        cm = CollectionsManager(file_path=str(path))
        assert cm.collections == {}

    def test_dado_json_corrompido_quando_load_entao_nao_levanta_excecao(self, tmp_path):
        path = tmp_path / "collections.json"
        path.write_text("QUEBRADO", encoding="utf-8")
        try:
            cm = CollectionsManager(file_path=str(path))
        except Exception as e:
            pytest.fail(f"load() não deve explodir: {e}")

    def test_dado_excecao_generica_quando_load_entao_collections_vazio(self, tmp_path):
        path = tmp_path / "collections.json"
        path.write_text(json.dumps({"col": []}), encoding="utf-8")
        with patch("builtins.open", side_effect=PermissionError("sem permissão")):
            cm = CollectionsManager.__new__(CollectionsManager)
            cm.file_path = str(path)
            cm.collections = {}
            cm.logger = MagicMock()
            cm.load()
        assert cm.collections == {}


# ═ save() caminho de erro ═════════════════════════════════════════════

class TestCollectionsManagerSaveErrors:

    def test_dado_erro_de_io_quando_save_entao_nao_levanta_excecao(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("teste")
        with patch("builtins.open", side_effect=OSError("disco cheio")):
            try:
                cm.save()
            except Exception as e:
                pytest.fail(f"save() não deve explodir: {e}")


# ═ add_collection() alias ══════════════════════════════════════════

class TestCollectionsManagerAddCollectionAlias:

    def test_dado_nome_valido_quando_add_collection_entao_retorna_true(self, tmp_path):
        cm = make_cm(tmp_path)
        result = cm.add_collection("Nova Coleção")
        assert result is True

    def test_dado_add_collection_quando_chamado_entao_colecao_existe(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.add_collection("Alias Test")
        assert "Alias Test" in cm.get_all_collections()

    def test_dado_nome_duplicado_quando_add_collection_entao_retorna_false(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.add_collection("Dup")
        result = cm.add_collection("Dup")
        assert result is False


# ═ clean_orphan_projects() ═══════════════════════════════════════════

class TestCollectionsManagerCleanOrphans:

    def test_dado_projeto_invalido_quando_clean_entao_remove_orfao(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        cm.add_project("col", "/proj/valido")
        cm.add_project("col", "/proj/orfao")
        removed = cm.clean_orphan_projects({"/proj/valido"})
        assert removed == 1
        assert "/proj/orfao" not in cm.get_projects("col")

    def test_dado_todos_projetos_validos_quando_clean_entao_retorna_zero(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        cm.add_project("col", "/proj/a")
        cm.add_project("col", "/proj/b")
        removed = cm.clean_orphan_projects({"/proj/a", "/proj/b"})
        assert removed == 0

    def test_dado_colecao_vazia_quando_clean_entao_retorna_zero(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("vazia")
        removed = cm.clean_orphan_projects({"/proj/qualquer"})
        assert removed == 0

    def test_dado_dois_orfaos_em_duas_colecoes_quando_clean_entao_remove_ambos(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("a")
        cm.create_collection("b")
        cm.add_project("a", "/proj/orfao1")
        cm.add_project("b", "/proj/orfao2")
        removed = cm.clean_orphan_projects(set())
        assert removed == 2


# ═ get_stats() ════════════════════════════════════════════════════════

class TestCollectionsManagerGetStats:

    def test_dado_colecoes_vazias_quando_get_stats_entao_zeros(self, tmp_path):
        cm = make_cm(tmp_path)
        stats = cm.get_stats()
        assert stats["total_collections"] == 0
        assert stats["total_entries"] == 0
        assert stats["unique_projects"] == 0

    def test_dado_projeto_em_duas_colecoes_quando_get_stats_entao_unique_correto(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("a")
        cm.create_collection("b")
        cm.add_project("a", "/proj/x")
        cm.add_project("b", "/proj/x")  # mesmo projeto em 2 coleções
        stats = cm.get_stats()
        assert stats["total_entries"] == 2
        assert stats["unique_projects"] == 1

    def test_dado_tres_projetos_distintos_quando_get_stats_entao_unique_tres(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        cm.add_project("col", "/proj/a")
        cm.add_project("col", "/proj/b")
        cm.add_project("col", "/proj/c")
        stats = cm.get_stats()
        assert stats["total_entries"] == 3
        assert stats["unique_projects"] == 3
