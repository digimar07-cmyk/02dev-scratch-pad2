"""
tests/unit/test_database.py

Testes unitários para core/database.py → DatabaseManager.

Metodologia Akita:
- Cada teste = um comportamento isolado.
- Nomenclatura: test_dado_<estado>_quando_<acao>_entao_<resultado>
- Estrutura AAA: Arrange / Act / Assert.
- Isolamento: nenhum teste escreve no disco real.
  O DatabaseManager aceita db_file e config_file injetados no __init__.
- ZOMBIES cobertos:
    Z → Zero (banco vazio)
    O → One (um projeto)
    M → Many (múltiplos projetos)
    B → Boundary (limites: nome vazio, path vazio)
    I → Interface (API pública documentada em VOLKOV-01)
    E → Exception (JSON corrompido, arquivo não existente)
    S → Simple (operações básicas CRUD)
"""
import json
import os
import sys
import pytest

# Garante que a raiz do app está no path para imports funcionarem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.database import DatabaseManager


# ════════════════════════════════════════════════════════
# ZERO — banco vazio
# ════════════════════════════════════════════════════════

class TestDatabaseManagerZero:
    """Comportamentos quando o banco está vazio ou não existe."""

    def test_dado_db_vazio_quando_get_project_entao_retorna_none(self, tmp_db_file, tmp_config_file):
        # Arrange
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)

        # Act
        result = db.get_project("/qualquer/caminho")

        # Assert
        assert result is None

    def test_dado_db_vazio_quando_project_count_entao_retorna_zero(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        assert db.project_count() == 0

    def test_dado_db_vazio_quando_all_paths_entao_retorna_lista_vazia(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        assert db.all_paths() == []

    def test_dado_db_vazio_quando_all_projects_entao_retorna_dict_vazio(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        assert db.all_projects() == {}

    def test_dado_db_vazio_quando_has_project_entao_retorna_false(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        assert db.has_project("/nao/existe") is False

    def test_dado_db_vazio_quando_remove_project_entao_retorna_false(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        assert db.remove_project("/nao/existe") is False

    def test_dado_db_vazio_quando_iter_projects_entao_itera_zero_vezes(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        items = list(db.iter_projects())
        assert len(items) == 0


# ════════════════════════════════════════════════════════
# ONE — um projeto
# ════════════════════════════════════════════════════════

class TestDatabaseManagerOne:
    """Comportamentos com exatamente um projeto."""

    def test_dado_projeto_inserido_quando_get_project_entao_retorna_dados(self, tmp_db_file, tmp_config_file):
        # Arrange
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        path = "/projetos/natal"
        data = {"name": "Natal", "categories": ["Natal"]}

        # Act
        db.set_project(path, data)
        result = db.get_project(path)

        # Assert
        assert result == data

    def test_dado_projeto_inserido_quando_has_project_entao_retorna_true(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/projetos/natal", {"name": "Natal"})
        assert db.has_project("/projetos/natal") is True

    def test_dado_projeto_inserido_quando_project_count_entao_retorna_um(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/projetos/natal", {"name": "Natal"})
        assert db.project_count() == 1

    def test_dado_projeto_inserido_quando_remove_project_entao_retorna_true(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/projetos/natal", {"name": "Natal"})
        assert db.remove_project("/projetos/natal") is True

    def test_dado_projeto_removido_quando_has_project_entao_retorna_false(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/projetos/natal", {"name": "Natal"})
        db.remove_project("/projetos/natal")
        assert db.has_project("/projetos/natal") is False

    def test_dado_projeto_inserido_quando_all_paths_entao_contem_path(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/projetos/natal", {"name": "Natal"})
        assert "/projetos/natal" in db.all_paths()

    def test_dado_projeto_inserido_quando_set_novamente_entao_atualiza_dados(self, tmp_db_file, tmp_config_file):
        """set_project deve ATUALIZAR se path já existe."""
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/projetos/natal", {"name": "Natal v1"})
        db.set_project("/projetos/natal", {"name": "Natal v2"})
        assert db.get_project("/projetos/natal")["name"] == "Natal v2"


# ════════════════════════════════════════════════════════
# MANY — múltiplos projetos
# ════════════════════════════════════════════════════════

class TestDatabaseManagerMany:
    """Comportamentos com múltiplos projetos."""

    def test_dado_tres_projetos_quando_project_count_entao_retorna_tres(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        for i in range(3):
            db.set_project(f"/projetos/p{i}", {"name": f"Projeto {i}"})
        assert db.project_count() == 3

    def test_dado_tres_projetos_quando_all_paths_entao_contem_todos(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        paths = ["/proj/a", "/proj/b", "/proj/c"]
        for p in paths:
            db.set_project(p, {})
        assert set(db.all_paths()) == set(paths)

    def test_dado_tres_projetos_quando_all_projects_entao_retorna_copia_profunda(self, tmp_db_file, tmp_config_file):
        """Modificar o retorno de all_projects() NÃO deve afetar o banco interno."""
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/proj/a", {"name": "A"})
        copia = db.all_projects()
        copia["/proj/a"]["name"] = "MODIFICADO"
        # O banco interno não deve ter sido alterado
        assert db.get_project("/proj/a")["name"] == "A"

    def test_dado_tres_projetos_quando_iter_projects_entao_itera_todos(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        for i in range(3):
            db.set_project(f"/proj/{i}", {"name": f"{i}"})
        items = list(db.iter_projects())
        assert len(items) == 3


# ════════════════════════════════════════════════════════
# PERSISTENCE — save / load do disco
# ════════════════════════════════════════════════════════

class TestDatabaseManagerPersistence:
    """Comportamentos de persistência (save/load) em disco isolado."""

    def test_dado_projetos_quando_save_e_load_entao_dados_preservados(self, tmp_db_file, tmp_config_file):
        # Arrange
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/proj/natal", {"name": "Natal", "categories": ["Natal"]})

        # Act — salva e carrega em nova instância
        db.save_database()
        db2 = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db2.load_database()

        # Assert
        assert db2.get_project("/proj/natal") == {"name": "Natal", "categories": ["Natal"]}

    def test_dado_db_existente_quando_load_database_entao_popula_banco(self, tmp_db_with_data, tmp_config_file, tmp_path):
        # Arrange — tmp_db_with_data já tem 3 projetos pré-escritos
        db = DatabaseManager(db_file=tmp_db_with_data, config_file=tmp_config_file)

        # Act
        db.load_database()

        # Assert
        assert db.project_count() == 3

    def test_dado_db_inexistente_quando_load_database_entao_inicia_vazio(self, tmp_db_file, tmp_config_file):
        """Arquivo não existe → banco inicia vazio, sem exceção."""
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.load_database()  # arquivo não existe ainda
        assert db.project_count() == 0

    def test_dado_db_corrompido_quando_load_database_entao_nao_levanta_excecao(self, tmp_db_corrupted, tmp_config_file):
        """JSON corrompido não deve derrubar a app. Apenas loga e continua."""
        db = DatabaseManager(db_file=tmp_db_corrupted, config_file=tmp_config_file)
        try:
            db.load_database()  # não deve explodir
        except Exception as e:
            pytest.fail(f"load_database não deveria levantar exceção: {e}")

    def test_dado_db_salvo_quando_arquivo_existe_entao_conteudo_e_json_valido(self, tmp_db_file, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db.set_project("/proj/test", {"name": "Test"})
        db.save_database()
        with open(tmp_db_file, encoding="utf-8") as f:
            loaded = json.load(f)
        assert "/proj/test" in loaded


# ════════════════════════════════════════════════════════
# MIGRAÇÃO — schema legado (category → categories)
# ════════════════════════════════════════════════════════

class TestDatabaseManagerMigration:
    """Migração automática de campo 'category' para 'categories'."""

    def test_dado_schema_legado_quando_load_database_entao_category_vira_lista(self, tmp_db_legacy, tmp_config_file):
        # Arrange
        db = DatabaseManager(db_file=tmp_db_legacy, config_file=tmp_config_file)

        # Act
        db.load_database()

        # Assert — campo 'category' deve virar lista em 'categories'
        projeto = db.get_project("/projetos/natal_legacy")
        assert "categories" in projeto
        assert isinstance(projeto["categories"], list)
        assert "Natal" in projeto["categories"]

    def test_dado_schema_legado_quando_load_database_entao_campo_category_removido(self, tmp_db_legacy, tmp_config_file):
        db = DatabaseManager(db_file=tmp_db_legacy, config_file=tmp_config_file)
        db.load_database()
        projeto = db.get_project("/projetos/natal_legacy")
        assert "category" not in projeto

    def test_dado_schema_legado_sem_categoria_quando_load_entao_categories_lista_vazia(self, tmp_db_legacy, tmp_config_file):
        """'Sem Categoria' deve virar lista vazia, não lista com string 'Sem Categoria'."""
        db = DatabaseManager(db_file=tmp_db_legacy, config_file=tmp_config_file)
        db.load_database()
        projeto = db.get_project("/projetos/sem_cat")
        assert projeto["categories"] == []
