"""
tests/unit/test_collections_manager_extended2.py

Cobre linhas ainda não testadas de core/collections_manager.py:
  101-104  save() bloco except OSError ao tentar remover .tmp
  217-218  clean_orphan_projects() save() após remoções (branch removed_count > 0)
  221-222  logger.info após remoção de órfãos
  238      get_stats() set comprehension unique_projects linha exata

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


class TestCollectionsManagerSaveExceptOsRemove:
    """Cobre linhas 101-104: save() falha ao abrir arquivo, tenta remover .tmp mas .tmp não existe."""

    def test_dado_erro_open_e_tmp_nao_existe_quando_save_entao_nao_explode(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        # Simula OSError no open do .tmp, e .tmp não existe (os.path.exists retorna False)
        with patch("builtins.open", side_effect=OSError("disco cheio")):
            with patch("os.path.exists", return_value=False):
                try:
                    cm.save()
                except Exception as e:
                    pytest.fail(f"save() não deve explodir: {e}")

    def test_dado_erro_open_e_tmp_existe_mas_remove_falha_quando_save_entao_nao_explode(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        # Simula OSError no open, .tmp existe mas os.remove também falha
        with patch("builtins.open", side_effect=OSError("disco cheio")):
            with patch("os.path.exists", return_value=True):
                with patch("os.remove", side_effect=OSError("não pode remover")):
                    try:
                        cm.save()
                    except Exception as e:
                        pytest.fail(f"save() não deve explodir mesmo com remove falhando: {e}")


class TestCollectionsManagerCleanOrphansExtended:
    """Cobre linhas 217-222: save() e logger.info após remoção de órfãos."""

    def test_dado_orfao_removido_quando_clean_entao_salva_em_disco(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        cm.add_project("col", "/proj/orfao")
        cm.clean_orphan_projects(set())  # remove o órfão
        # Recarrega do disco para confirmar que save() foi chamado
        cm2 = CollectionsManager(file_path=str(tmp_path / "collections.json"))
        assert "/proj/orfao" not in cm2.get_projects("col")

    def test_dado_orfao_removido_quando_clean_entao_logger_info_chamado(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("col")
        cm.add_project("col", "/proj/orfao")
        cm.logger = MagicMock()
        cm.clean_orphan_projects(set())
        cm.logger.info.assert_called()


class TestCollectionsManagerGetStatsUnique:
    """Cobre linha 238: set comprehension para unique_projects."""

    def test_dado_mesmo_projeto_em_tres_colecoes_quando_get_stats_entao_unique_um(self, tmp_path):
        cm = make_cm(tmp_path)
        for nome in ["a", "b", "c"]:
            cm.create_collection(nome)
            cm.add_project(nome, "/proj/compartilhado")
        stats = cm.get_stats()
        assert stats["total_entries"] == 3
        assert stats["unique_projects"] == 1

    def test_dado_projetos_distintos_em_colecoes_distintas_quando_get_stats_entao_unique_correto(self, tmp_path):
        cm = make_cm(tmp_path)
        cm.create_collection("x")
        cm.create_collection("y")
        cm.add_project("x", "/proj/1")
        cm.add_project("x", "/proj/2")
        cm.add_project("y", "/proj/3")
        stats = cm.get_stats()
        assert stats["total_entries"] == 3
        assert stats["unique_projects"] == 3
