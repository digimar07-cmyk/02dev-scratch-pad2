"""
test_database.py — Testes agressivos para encontrar bugs reais no DatabaseManager.

Estratégia: bordas, dados podres, corrupção, comportamento inesperado.
Não testamos o caminho feliz — testamos onde o app PODE QUEBRAR.
"""
import json
import os
import pytest
from core.database import DatabaseManager


# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def db(tmp_path):
    db_file = str(tmp_path / "database.json")
    cfg_file = str(tmp_path / "config.json")
    return DatabaseManager(db_file=db_file, config_file=cfg_file)


# ══════════════════════════════════════════════════════════════
# INTEGRIDADE DOS DADOS — o que entra tem que sair igual
# ══════════════════════════════════════════════════════════════

class TestIntegridade:

    def test_set_project_retorna_referencia_real_nao_copia(self, db):
        """Bug: set_project guarda referência mutável — modificar depois altera o banco."""
        data = {"name": "Projeto A", "tags": ["laser"]}
        db.set_project("/path/a", data)
        data["tags"].append("INVASÃO")
        # Se get_project retornar a mesma referência, o banco foi corrompido
        tags_no_banco = db.get_project("/path/a")["tags"]
        assert "INVASÃO" not in tags_no_banco, (
            "BUG: set_project guarda referência mutável. "
            "Modificar o dict original corrompe o banco em memória."
        )

    def test_get_project_retorna_referencia_real_nao_copia(self, db):
        """Bug: get_project retorna referência interna — modificar fora corrompe o banco."""
        db.set_project("/path/a", {"name": "Projeto A", "tags": []})
        proj = db.get_project("/path/a")
        proj["tags"].append("INVASÃO")
        tags_no_banco = db.get_project("/path/a")["tags"]
        assert "INVASÃO" not in tags_no_banco, (
            "BUG: get_project retorna referência interna. "
            "Modificar o retorno corrompe o banco."
        )

    def test_all_projects_retorna_copia_profunda(self, db):
        """Bug: all_projects() faz dict() superficial — listas internas ainda são referências."""
        db.set_project("/path/a", {"name": "A", "tags": ["original"]})
        todos = db.all_projects()
        todos["/path/a"]["tags"].append("INVASÃO")
        tags_no_banco = db.get_project("/path/a")["tags"]
        assert "INVASÃO" not in tags_no_banco, (
            "BUG: all_projects() retorna cópia rasa. "
            "Listas internas dos projetos ainda são a mesma referência."
        )

    def test_save_load_preserva_todos_os_campos(self, db):
        """Campos especiais (unicode, booleanos, listas vazias) devem sobreviver ao save/load."""
        original = {
            "name": "Projeto São João 日本語",
            "favorite": True,
            "done": False,
            "categories": [],
            "tags": ["a", "b", "c"],
            "ai_description": "Descrição com \n quebra de linha e \t tab",
        }
        db.set_project("/path/unicode", original)
        db.save_database()
        db.database.clear()
        db.load_database()
        recarregado = db.get_project("/path/unicode")
        assert recarregado is not None, "Projeto sumiu após save/load"
        assert recarregado["name"] == original["name"], "Nome unicode corrompido"
        assert recarregado["favorite"] is True
        assert recarregado["done"] is False
        assert recarregado["categories"] == []
        assert recarregado["tags"] == ["a", "b", "c"]


# ══════════════════════════════════════════════════════════════
# CORRUPÇÃO E RECUPERAÇÃO — o que acontece quando o arquivo está podre
# ══════════════════════════════════════════════════════════════

class TestCorrupcao:

    def test_database_json_truncado_nao_trava(self, tmp_path):
        """Arquivo cortado no meio (ex: disco cheio) não pode travar o app."""
        db_file = str(tmp_path / "database.json")
        with open(db_file, "w") as f:
            f.write('{"path/a": {"name": "incomplete')
        cfg_file = str(tmp_path / "config.json")
        db = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db.load_database()
        assert isinstance(db.database, dict), "database deve ser dict mesmo após corrupção"
        assert len(db.database) == 0, "database corrompido deve resultar em banco vazio"

    def test_database_json_e_bak_ambos_corrompidos(self, tmp_path):
        """Se principal E backup estiverem corrompidos, não pode entrar em loop nem travar."""
        db_file = str(tmp_path / "database.json")
        bak_file = db_file + ".bak"
        with open(db_file, "w") as f:
            f.write("LIXO PURO")
        with open(bak_file, "w") as f:
            f.write("MAIS LIXO")
        cfg_file = str(tmp_path / "config.json")
        db = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db.load_database()  # não pode travar, não pode loop infinito
        assert isinstance(db.database, dict)

    def test_database_json_vazio_nao_e_dict(self, tmp_path):
        """Arquivo database.json com conteúdo '[]' (lista) em vez de '{}' (dict)."""
        db_file = str(tmp_path / "database.json")
        with open(db_file, "w") as f:
            f.write("[]")  # lista, não dict — formato errado
        cfg_file = str(tmp_path / "config.json")
        db = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db.load_database()
        # Não pode travar. database deve ser dict.
        assert isinstance(db.database, dict), (
            "BUG: database.json com '[]' (lista) causa db.database virar lista. "
            "Isso quebra TUDO que faz db.database.get() ou 'in db.database'."
        )

    def test_config_sem_chave_folders_nao_quebra_app(self, tmp_path):
        """Config restaurado de backup pode não ter a chave 'folders' — app não pode travar."""
        db_file = str(tmp_path / "database.json")
        cfg_file = str(tmp_path / "config.json")
        with open(cfg_file, "w") as f:
            json.dump({"models": {}}, f)  # sem 'folders'
        db = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db.load_config()
        folders = db.config.get("folders", None)
        assert folders is not None, (
            "BUG: config sem chave 'folders' — acesso a db.config['folders'] vai "
            "lançar KeyError no app em produção."
        )
        assert isinstance(folders, list), "'folders' deve ser lista"


# ══════════════════════════════════════════════════════════════
# OPERAÇÕES COM DADOS INVÁLIDOS — o que o usuário pode causar
# ══════════════════════════════════════════════════════════════

class TestDadosInvalidos:

    def test_set_project_com_path_vazio(self, db):
        """Path vazio como chave do banco — não deve ser aceito silenciosamente."""
        db.set_project("", {"name": "Fantasma"})
        assert db.has_project("") is False, (
            "BUG: set_project aceita path vazio. "
            "Projeto invisível no banco — nunca aparece na UI mas ocupa memória."
        )

    def test_set_project_com_data_none(self, db):
        """Salvar None como dados do projeto não pode silenciosamente aceitar."""
        db.set_project("/path/a", None)
        projeto = db.get_project("/path/a")
        assert projeto is not None, (
            "BUG: set_project aceita None como dados. "
            "get_project retorna None e o app não sabe se o projeto existe ou não."
        )

    def test_set_project_com_data_nao_serializavel(self, db, tmp_path):
        """Dados com objeto não-serializável deve falhar no save, não silenciosamente."""
        import datetime
        db.set_project("/path/a", {"name": "A", "obj": object()})  # object() não é JSON
        with pytest.raises(Exception):
            db.save_database()  # deve lançar exceção, não engolir silenciosamente

    def test_remove_project_com_path_none(self, db):
        """remove_project(None) não pode travar com AttributeError."""
        try:
            resultado = db.remove_project(None)
            assert resultado is False
        except (AttributeError, TypeError) as e:
            pytest.fail(f"BUG: remove_project(None) lança exceção: {e}")

    def test_has_project_com_path_none(self, db):
        """has_project(None) não pode travar."""
        try:
            resultado = db.has_project(None)
            assert resultado is False
        except (AttributeError, TypeError) as e:
            pytest.fail(f"BUG: has_project(None) lança exceção: {e}")

    def test_2000_projetos_save_load_integro(self, db):
        """Simula uso real: 2000 projetos. Save/load deve preservar todos."""
        for i in range(2000):
            db.set_project(f"/pasta/projeto_{i:04d}", {
                "name": f"Projeto {i}",
                "favorite": i % 2 == 0,
                "tags": [f"tag{i}", f"cat{i % 10}"],
                "categories": ["Laser"] if i % 3 == 0 else [],
            })
        db.save_database()
        db.database.clear()
        db.load_database()
        assert db.project_count() == 2000, (
            f"BUG: Após save/load de 2000 projetos, "
            f"só {db.project_count()} foram recuperados."
        )


# ══════════════════════════════════════════════════════════════
# BACKUP — o mecanismo de segurança tem que funcionar
# ══════════════════════════════════════════════════════════════

class TestBackup:

    def test_restore_backup_corrompido_nao_entra_em_loop(self, tmp_path):
        """Se .bak também for inválido, _try_restore_from_backup não pode loopar."""
        db_file = str(tmp_path / "database.json")
        bak_file = db_file + ".bak"
        cfg_file = str(tmp_path / "config.json")
        with open(db_file, "w") as f:
            f.write("CORROMPIDO")
        with open(bak_file, "w") as f:
            f.write("CORROMPIDO TAMBEM")
        db = DatabaseManager(db_file=db_file, config_file=cfg_file)
        # Não pode travar, não pode RecursionError
        db.load_database()
        assert isinstance(db.database, dict)

    def test_auto_backup_limita_quantidade(self, tmp_path, monkeypatch):
        """auto_backup deve deletar backups antigos ao passar do limite MAX_AUTO_BACKUPS."""
        import config.settings as settings
        monkeypatch.setattr(settings, "MAX_AUTO_BACKUPS", 3)
        monkeypatch.setattr(settings, "BACKUP_FOLDER", str(tmp_path / "backups"))
        os.makedirs(str(tmp_path / "backups"), exist_ok=True)

        db_file = str(tmp_path / "database.json")
        cfg_file = str(tmp_path / "config.json")
        db = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db.set_project("/p", {"name": "p"})
        db.save_database()

        for _ in range(6):  # cria 6 backups — deve manter só 3
            db.auto_backup()

        backups = [f for f in os.listdir(str(tmp_path / "backups")) if f.startswith("auto_backup_")]
        assert len(backups) <= 3, (
            f"BUG: auto_backup criou {len(backups)} arquivos, limite é 3. "
            "Pasta de backup vai encher o disco em produção."
        )
