"""
tests/unit/test_database.py — Testes de comportamento real do DatabaseManager.

Metodologia Akita:
- Cada teste verifica UMA regra de negocio especifica
- Sem mocks: usa DatabaseManager real com tmp_path
- Falhar = encontrou um bug real
- Fixtures do conftest.py: tmp_db, populated_db, sample_project
"""
import json
import os
import pytest


# ── CRUD basico ──────────────────────────────────────────────────────────────

class TestCRUDBasico:

    def test_set_e_get_projeto(self, tmp_db):
        """Inserir e recuperar dados deve retornar exatamente o que foi inserido."""
        tmp_db.set_project("/path/a", {"name": "Luminaria Natal"})
        result = tmp_db.get_project("/path/a")
        assert result == {"name": "Luminaria Natal"}

    def test_get_inexistente_retorna_none(self, tmp_db):
        """Buscar path que nao existe deve retornar None, nunca explodir."""
        assert tmp_db.get_project("/nao/existe") is None

    def test_remove_existente_retorna_true(self, tmp_db):
        """Remover projeto existente deve retornar True."""
        tmp_db.set_project("/path/x", {"name": "X"})
        assert tmp_db.remove_project("/path/x") is True

    def test_remove_existente_apaga_dado(self, tmp_db):
        """Apos remover, get_project deve retornar None."""
        tmp_db.set_project("/path/x", {"name": "X"})
        tmp_db.remove_project("/path/x")
        assert tmp_db.get_project("/path/x") is None

    def test_remove_inexistente_retorna_false(self, tmp_db):
        """Remover path que nao existe deve retornar False sem explodir."""
        assert tmp_db.remove_project("/nao/existe") is False

    def test_has_project_true(self, tmp_db):
        """has_project retorna True para path inserido."""
        tmp_db.set_project("/existe", {})
        assert tmp_db.has_project("/existe") is True

    def test_has_project_false(self, tmp_db):
        """has_project retorna False para path nao inserido."""
        assert tmp_db.has_project("/nao/existe") is False

    def test_update_projeto_sobrescreve(self, tmp_db):
        """set_project com mesmo path deve sobrescrever dados anteriores."""
        tmp_db.set_project("/path", {"name": "Original"})
        tmp_db.set_project("/path", {"name": "Atualizado"})
        assert tmp_db.get_project("/path")["name"] == "Atualizado"


# ── Consultas e contagem ─────────────────────────────────────────────────────

class TestConsultas:

    def test_all_paths_retorna_todos(self, tmp_db):
        """all_paths deve conter exatamente os paths inseridos."""
        paths = ["/a", "/b", "/c"]
        for p in paths:
            tmp_db.set_project(p, {})
        result = tmp_db.all_paths()
        assert sorted(result) == sorted(paths)

    def test_project_count_vazio(self, tmp_db):
        """Banco vazio deve ter contagem zero."""
        assert tmp_db.project_count() == 0

    def test_project_count_apos_insercoes(self, tmp_db):
        """Contagem deve refletir exatamente o numero de insercoes."""
        for i in range(5):
            tmp_db.set_project(f"/path/{i}", {})
        assert tmp_db.project_count() == 5

    def test_project_count_apos_remocao(self, tmp_db):
        """Contagem deve diminuir apos remocao."""
        tmp_db.set_project("/a", {})
        tmp_db.set_project("/b", {})
        tmp_db.remove_project("/a")
        assert tmp_db.project_count() == 1

    def test_all_projects_retorna_copia(self, tmp_db):
        """Modificar o dict retornado por all_projects nao deve alterar o banco."""
        tmp_db.set_project("/p", {"name": "Original"})
        copia = tmp_db.all_projects()
        copia["/p"]["name"] = "Alterado externamente"
        # O banco interno nao deve ter sido afetado
        assert tmp_db.get_project("/p")["name"] == "Original"

    def test_iter_projects_percorre_tudo(self, tmp_db):
        """iter_projects deve gerar todos os pares (path, data) inseridos."""
        dados = {f"/path/{i}": {"idx": i} for i in range(4)}
        for path, data in dados.items():
            tmp_db.set_project(path, data)
        iterado = dict(tmp_db.iter_projects())
        assert len(iterado) == 4
        for path in dados:
            assert path in iterado


# ── Persistencia (save/load) ─────────────────────────────────────────────────

class TestPersistencia:

    def test_save_e_reload_roundtrip(self, tmp_path, sample_project):
        """Dados salvos devem ser identicos apos recarregar em nova instancia."""
        from core.database import DatabaseManager
        db_file = str(tmp_path / "db.json")
        cfg_file = str(tmp_path / "cfg.json")

        db1 = DatabaseManager(db_file=db_file, config_file=cfg_file)
        for i in range(3):
            db1.set_project(f"/path/{i}", {**sample_project, "name": f"Proj {i}"})
        db1.save_database()

        db2 = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db2.load_database()
        assert db2.project_count() == 3
        assert db2.get_project("/path/0")["name"] == "Proj 0"

    def test_load_arquivo_inexistente_inicia_vazio(self, tmp_path):
        """load_database com arquivo inexistente nao deve explodir e inicia vazio."""
        from core.database import DatabaseManager
        db = DatabaseManager(
            db_file=str(tmp_path / "naoexiste.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        db.load_database()
        assert db.project_count() == 0

    def test_load_json_corrompido_nao_explode(self, tmp_path):
        """load_database com JSON invalido nao deve lancar excecao."""
        from core.database import DatabaseManager
        db_file = tmp_path / "db.json"
        db_file.write_text("{ isso nao eh json valido !!!")
        db = DatabaseManager(
            db_file=str(db_file),
            config_file=str(tmp_path / "cfg.json")
        )
        # Nao deve explodir
        db.load_database()

    def test_save_atomico_sem_arquivo_tmp(self, tmp_path, sample_project):
        """Apos save_database() bem-sucedido, arquivo .tmp nao deve existir."""
        from core.database import DatabaseManager
        db_file = str(tmp_path / "db.json")
        db = DatabaseManager(db_file=db_file, config_file=str(tmp_path / "cfg.json"))
        db.set_project("/p", sample_project)
        db.save_database()
        assert not os.path.exists(db_file + ".tmp")

    def test_migracao_category_para_categories(self, tmp_path):
        """Banco com campo 'category' antigo deve ser migrado para 'categories' como lista."""
        from core.database import DatabaseManager
        db_file = tmp_path / "db.json"
        db_file.write_text(
            json.dumps({"/path/proj": {"name": "Teste", "category": "Luminaria"}})
        )
        db = DatabaseManager(
            db_file=str(db_file),
            config_file=str(tmp_path / "cfg.json")
        )
        db.load_database()
        data = db.get_project("/path/proj")
        assert "category" not in data
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert "Luminaria" in data["categories"]


# ── Backup ───────────────────────────────────────────────────────────────────

class TestBackup:

    def test_save_cria_arquivo_bak(self, tmp_path):
        """Segundo save deve criar arquivo .bak do save anterior."""
        from core.database import DatabaseManager
        db_file = str(tmp_path / "db.json")
        db = DatabaseManager(db_file=db_file, config_file=str(tmp_path / "cfg.json"))
        db.set_project("/p", {"name": "A"})
        db.save_database()  # primeira escrita
        db.set_project("/q", {"name": "B"})
        db.save_database()  # segunda escrita deve criar .bak
        assert os.path.exists(db_file + ".bak")

    def test_manual_backup_retorna_path_valido(self, tmp_path):
        """manual_backup deve retornar o caminho do backup criado."""
        from core.database import DatabaseManager
        db_file = str(tmp_path / "db.json")
        db = DatabaseManager(db_file=db_file, config_file=str(tmp_path / "cfg.json"))
        db.set_project("/p", {"name": "X"})
        db.save_database()
        backup_path = db.manual_backup()
        assert backup_path is not None
        assert os.path.exists(backup_path)

    def test_manual_backup_sem_db_retorna_none(self, tmp_path):
        """manual_backup sem db_file existente deve retornar None sem explodir."""
        from core.database import DatabaseManager
        db = DatabaseManager(
            db_file=str(tmp_path / "naoexiste.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        result = db.manual_backup()
        assert result is None
