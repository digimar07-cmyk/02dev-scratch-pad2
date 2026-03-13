"""
tests/integration/test_database_collections.py

Testes de INTEGRAÇÃO: DatabaseManager + CollectionsManager.

Metodologia Akita:
- Integração ≠ Unit: aqui testamos DOIS componentes trabalhando juntos.
- Ainda isolado: usa tmp_path, sem disco de produção.
- Objetivo: garantir que o contrato entre DB e Collections funciona.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.database import DatabaseManager
from core.collections_manager import CollectionsManager


class TestDatabaseCollectionsIntegration:

    def test_dado_projeto_no_db_quando_adicionado_a_colecao_entao_associacao_funciona(
            self, tmp_db_file, tmp_config_file, tmp_collections_file):
        # Arrange
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/proj/natal", {"name": "Natal"})

        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")

        # Act
        cm.add_project("Favoritos", "/proj/natal")

        # Assert
        assert cm.is_project_in_collection("Favoritos", "/proj/natal")
        assert db.has_project("/proj/natal")  # DB não foi afetado

    def test_dado_projeto_removido_do_db_quando_clean_orphans_entao_colecao_atualizada(
            self, tmp_db_file, tmp_config_file, tmp_collections_file):
        # Arrange
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/proj/natal", {"name": "Natal"})
        db.set_project("/proj/pascoa", {"name": "Páscoa"})

        cm = CollectionsManager(file_path=tmp_collections_file)
        cm.create_collection("Favoritos")
        cm.add_project("Favoritos", "/proj/natal")
        cm.add_project("Favoritos", "/proj/pascoa")

        # Act — simula remoção de projeto do DB
        db.remove_project("/proj/pascoa")
        valid_paths = set(db.all_paths())
        removed = cm.clean_orphan_projects(valid_paths)

        # Assert
        assert removed == 1
        assert cm.is_project_in_collection("Favoritos", "/proj/natal")
        assert not cm.is_project_in_collection("Favoritos", "/proj/pascoa")

    def test_dado_db_salvo_e_collections_salvas_quando_novas_instancias_criadas_entao_tudo_persiste(
            self, tmp_db_file, tmp_config_file, tmp_collections_file):
        # Arrange — escreve
        db1 = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db1.set_project("/proj/natal", {"name": "Natal"})
        db1.save_database()

        cm1 = CollectionsManager(file_path=tmp_collections_file)
        cm1.create_collection("Favoritos")
        cm1.add_project("Favoritos", "/proj/natal")

        # Act — lê com novas instâncias
        db2 = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db2.load_database()
        cm2 = CollectionsManager(file_path=tmp_collections_file)

        # Assert
        assert db2.has_project("/proj/natal")
        assert cm2.is_project_in_collection("Favoritos", "/proj/natal")
