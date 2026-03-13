"""
tests/unit/test_collections_manager.py

Testes unitários para core/collections_manager.py → CollectionsManager.

Metodologia Akita:
- Isolamento: file_path injetado via __init__ aponta para tmp_path.
- Nomenclatura: test_dado_<estado>_quando_<acao>_entao_<resultado>
- Estrutura AAA.
- ZOMBIES: Z/O/M/B/I/E/S cobertos por classe.
"""
import os
import sys
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.collections_manager import CollectionsManager


# ════════════════════════════════════════════════════════
# ZERO — gerenciador recém criado
# ════════════════════════════════════════════════════════

class TestCollectionsManagerZero:

    def test_dado_colecoes_vazias_quando_get_all_collections_entao_lista_vazia(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        assert cm.get_all_collections() == []

    def test_dado_colecoes_vazias_quando_get_stats_entao_zeros(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        stats = cm.get_stats()
        assert stats["total_collections"] == 0
        assert stats["total_entries"] == 0
        assert stats["unique_projects"] == 0


# ════════════════════════════════════════════════════════
# ONE — uma coleção
# ════════════════════════════════════════════════════════

class TestCollectionsManagerOne:

    def test_dado_nome_valido_quando_create_collection_entao_retorna_true(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        assert cm.create_collection("Favoritos") is True

    def test_dado_nome_valido_quando_create_collection_entao_aparece_em_get_all(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        assert "Favoritos" in cm.get_all_collections()

    def test_dado_colecao_existente_quando_create_novamente_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        assert cm.create_collection("Favoritos") is False

    def test_dado_nome_vazio_quando_create_collection_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        assert cm.create_collection("") is False

    def test_dado_nome_com_espacos_quando_create_collection_entao_strip_aplicado(self, tmp_collections_file):
        """Nome com espaços externos deve ser normalizado via strip()."""
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("  Favoritos  ")
        assert "Favoritos" in cm.get_all_collections()

    def test_dado_colecao_criada_quando_delete_collection_entao_retorna_true(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        assert cm.delete_collection("Favoritos") is True

    def test_dado_colecao_deletada_quando_get_all_entao_nao_contem(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.delete_collection("Favoritos")
        assert "Favoritos" not in cm.get_all_collections()

    def test_dado_colecao_inexistente_quando_delete_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        assert cm.delete_collection("NaoExiste") is False


# ════════════════════════════════════════════════════════
# RENAME — renomear coleção
# ════════════════════════════════════════════════════════

class TestCollectionsManagerRename:

    def test_dado_colecao_existente_quando_rename_entao_retorna_true(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Antigo")
        assert cm.rename_collection("Antigo", "Novo") is True

    def test_dado_rename_quando_novo_nome_aparece_em_get_all(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Antigo")
        cm.rename_collection("Antigo", "Novo")
        assert "Novo" in cm.get_all_collections()

    def test_dado_rename_quando_nome_antigo_sumiu_de_get_all(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Antigo")
        cm.rename_collection("Antigo", "Novo")
        assert "Antigo" not in cm.get_all_collections()

    def test_dado_rename_para_nome_existente_quando_rename_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("A")
        cm.create_collection("B")
        assert cm.rename_collection("A", "B") is False

    def test_dado_colecao_inexistente_quando_rename_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        assert cm.rename_collection("NaoExiste", "Novo") is False

    def test_dado_novo_nome_vazio_quando_rename_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("A")
        assert cm.rename_collection("A", "") is False


# ════════════════════════════════════════════════════════
# PROJETOS — add / remove / query
# ════════════════════════════════════════════════════════

class TestCollectionsManagerProjects:

    def test_dado_colecao_vazia_quando_add_project_entao_retorna_true(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        assert cm.add_project("Favoritos", "/proj/natal") is True

    def test_dado_projeto_adicionado_quando_is_project_in_collection_entao_true(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/proj/natal")
        assert cm.is_project_in_collection("Favoritos", "/proj/natal") is True

    def test_dado_projeto_adicionado_duplicado_quando_add_project_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/proj/natal")
        assert cm.add_project("Favoritos", "/proj/natal") is False

    def test_dado_colecao_inexistente_quando_add_project_entao_retorna_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        assert cm.add_project("NaoExiste", "/proj/natal") is False

    def test_dado_projeto_adicionado_quando_remove_project_entao_retorna_true(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/proj/natal")
        assert cm.remove_project("Favoritos", "/proj/natal") is True

    def test_dado_projeto_removido_quando_is_project_in_collection_entao_false(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/proj/natal")
        cm.remove_project("Favoritos", "/proj/natal")
        assert cm.is_project_in_collection("Favoritos", "/proj/natal") is False

    def test_dado_projeto_em_duas_colecoes_quando_get_project_collections_entao_retorna_ambas(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("A")
        cm.create_collection("B")
        cm.add_project("A", "/proj/natal")
        cm.add_project("B", "/proj/natal")
        cols = cm.get_project_collections("/proj/natal")
        assert "A" in cols
        assert "B" in cols

    def test_dado_colecao_com_projetos_quando_get_collection_size_entao_retorna_count_correto(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/proj/a")
        cm.add_project("Favoritos", "/proj/b")
        assert cm.get_collection_size("Favoritos") == 2


# ════════════════════════════════════════════════════════
# CLEANUP — clean_orphan_projects
# ════════════════════════════════════════════════════════

class TestCollectionsManagerCleanup:

    def test_dado_orphan_quando_clean_orphan_projects_entao_remove_invalidos(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("A")
        cm.add_project("A", "/proj/valido")
        cm.add_project("A", "/proj/orphan")
        valid_paths = {"/proj/valido"}

        removed = cm.clean_orphan_projects(valid_paths)

        assert removed == 1
        assert cm.is_project_in_collection("A", "/proj/orphan") is False
        assert cm.is_project_in_collection("A", "/proj/valido") is True

    def test_dado_sem_orphans_quando_clean_orphan_projects_entao_retorna_zero(self, tmp_collections_file):
        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("A")
        cm.add_project("A", "/proj/valido")
        valid_paths = {"/proj/valido"}

        removed = cm.clean_orphan_projects(valid_paths)

        assert removed == 0


# ════════════════════════════════════════════════════════
# PERSISTENCE — persistência em disco
# ════════════════════════════════════════════════════════

class TestCollectionsManagerPersistence:

    def test_dado_colecoes_salvas_quando_nova_instancia_carrega_entao_dados_persistidos(self, tmp_collections_file):
        # Arrange — escreve
        cm1 = CollectionsManager(file_path=tmp_collections_file)
        cm1.create_collection("Favoritos")
        cm1.add_project("Favoritos", "/proj/natal")

        # Act — nova instância lê
        cm2 = CollectionsManager(file_path=tmp_collections_file)

        # Assert
        assert "Favoritos" in cm2.get_all_collections()
        assert cm2.is_project_in_collection("Favoritos", "/proj/natal")

    def test_dado_collections_pre_populado_quando_instancia_criada_entao_carrega_corretamente(
            self, tmp_collections_with_data):
        cm = CollectionsManager(file_path=tmp_collections_with_data)
        assert "Favoritos" in cm.get_all_collections()
        assert "Arquivados" in cm.get_all_collections()
        assert cm.get_collection_size("Favoritos") == 2
