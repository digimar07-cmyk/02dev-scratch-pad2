"""
tests/unit/test_database_extended.py

Testes para as linhas não cobertas de core/database.py:
  - load_config / save_config
  - auto_backup / manual_backup (do DatabaseManager)
  - _save_json_atomic
  - _try_restore_from_backup

Metodologia Akita:
  NUNCA alterar testes. Testes revelam bugs no app.
  ZOMBIES: Z (arquivo inexistente), O (uma operação), E (corrompido/permissão).
"""
import os
import sys
import json
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.database import DatabaseManager


def make_db(tmp_path):
    """Factory: DatabaseManager isolado em tmp_path."""
    db_file = str(tmp_path / "database.json")
    config_file = str(tmp_path / "config.json")
    return DatabaseManager(db_file=db_file, config_file=config_file)


# ════════════════════════════════════════════════════════
# load_config
# ════════════════════════════════════════════════════════

class TestDatabaseManagerLoadConfig:

    def test_dado_config_inexistente_quando_load_config_entao_config_padrao_mantido(self, tmp_path):
        db = make_db(tmp_path)
        db.load_config()  # arquivo não existe
        assert db.config == {"folders": [], "models": {}}

    def test_dado_config_valido_quando_load_config_entao_dados_carregados(self, tmp_path):
        db = make_db(tmp_path)
        config_data = {"folders": ["/pasta/a", "/pasta/b"], "models": {"ollama": "llama3"}}
        with open(db.config_file, "w", encoding="utf-8") as f:
            json.dump(config_data, f)
        db.load_config()
        assert db.config["folders"] == ["/pasta/a", "/pasta/b"]
        assert db.config["models"] == {"ollama": "llama3"}

    def test_dado_config_corrompido_quando_load_config_entao_nao_levanta_excecao(self, tmp_path):
        db = make_db(tmp_path)
        with open(db.config_file, "w", encoding="utf-8") as f:
            f.write("{ INVALIDO JSON !!!")
        try:
            db.load_config()
        except Exception as e:
            pytest.fail(f"load_config não deve levantar exceção: {e}")

    def test_dado_config_corrompido_com_bak_quando_load_config_entao_tenta_restaurar(self, tmp_path):
        db = make_db(tmp_path)
        # Cria .bak válido
        bak_data = {"folders": ["/bak/pasta"], "models": {}}
        with open(db.config_file + ".bak", "w", encoding="utf-8") as f:
            json.dump(bak_data, f)
        # Cria config corrompido
        with open(db.config_file, "w", encoding="utf-8") as f:
            f.write("INVALIDO")
        db.load_config()
        # Após restaurar do .bak, config deve ter os dados do backup
        assert db.config["folders"] == ["/bak/pasta"]


# ════════════════════════════════════════════════════════
# save_config
# ════════════════════════════════════════════════════════

class TestDatabaseManagerSaveConfig:

    def test_dado_config_populado_quando_save_config_entao_arquivo_criado(self, tmp_path):
        db = make_db(tmp_path)
        db.config = {"folders": ["/pasta/x"], "models": {}}
        db.save_config()
        assert os.path.exists(db.config_file)

    def test_dado_config_salvo_quando_load_config_entao_dados_preservados(self, tmp_path):
        db = make_db(tmp_path)
        db.config = {"folders": ["/pasta/x", "/pasta/y"], "models": {"a": "b"}}
        db.save_config()
        db2 = make_db(tmp_path)
        db2.load_config()
        assert db2.config["folders"] == ["/pasta/x", "/pasta/y"]
        assert db2.config["models"] == {"a": "b"}

    def test_dado_config_salvo_quando_arquivo_e_json_valido(self, tmp_path):
        db = make_db(tmp_path)
        db.config = {"folders": ["/pasta/z"], "models": {}}
        db.save_config()
        with open(db.config_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["folders"] == ["/pasta/z"]


# ════════════════════════════════════════════════════════
# manual_backup (DatabaseManager)
# ════════════════════════════════════════════════════════

class TestDatabaseManagerManualBackup:

    def test_dado_db_inexistente_quando_manual_backup_entao_retorna_none(self, tmp_path):
        db = make_db(tmp_path)
        result = db.manual_backup()
        assert result is None

    def test_dado_db_existente_quando_manual_backup_entao_retorna_path(self, tmp_path):
        db = make_db(tmp_path)
        db.set_project("/proj/a", {"name": "A"})
        db.save_database()
        result = db.manual_backup()
        assert result is not None
        assert "manual_backup_" in result

    def test_dado_db_existente_quando_manual_backup_entao_arquivo_criado(self, tmp_path):
        db = make_db(tmp_path)
        db.set_project("/proj/a", {"name": "A"})
        db.save_database()
        result = db.manual_backup()
        assert os.path.exists(result)

    def test_dado_db_existente_quando_manual_backup_entao_conteudo_identico(self, tmp_path):
        db = make_db(tmp_path)
        db.set_project("/proj/a", {"name": "A"})
        db.save_database()
        result = db.manual_backup()
        with open(result, "r", encoding="utf-8") as f:
            backup_data = json.load(f)
        assert "/proj/a" in backup_data


# ════════════════════════════════════════════════════════
# auto_backup
# ════════════════════════════════════════════════════════

class TestDatabaseManagerAutoBackup:

    def test_dado_db_inexistente_quando_auto_backup_entao_nao_levanta_excecao(self, tmp_path):
        db = make_db(tmp_path)
        try:
            db.auto_backup()
        except Exception as e:
            pytest.fail(f"auto_backup não deve explodir sem db: {e}")

    def test_dado_db_existente_quando_auto_backup_entao_arquivo_criado(self, tmp_path):
        db = make_db(tmp_path)
        db.set_project("/proj/a", {"name": "A"})
        db.save_database()
        db.auto_backup()
        from config.settings import BACKUP_FOLDER
        backups = [f for f in os.listdir(BACKUP_FOLDER) if f.startswith("auto_backup_")]
        assert len(backups) >= 1

    def test_dado_multiplos_auto_backups_quando_limite_excedido_entao_antigos_removidos(self, tmp_path):
        from config.settings import BACKUP_FOLDER, MAX_AUTO_BACKUPS
        import time
        db = make_db(tmp_path)
        db.set_project("/proj/a", {"name": "A"})
        db.save_database()
        # Cria MAX_AUTO_BACKUPS + 2 backups
        for _ in range(MAX_AUTO_BACKUPS + 2):
            db.auto_backup()
            time.sleep(0.01)  # garante timestamps diferentes
        backups = sorted([f for f in os.listdir(BACKUP_FOLDER) if f.startswith("auto_backup_")])
        assert len(backups) <= MAX_AUTO_BACKUPS


# ════════════════════════════════════════════════════════
# _try_restore_from_backup
# ════════════════════════════════════════════════════════

class TestDatabaseManagerRestoreBackup:

    def test_dado_sem_bak_quando_restore_entao_retorna_false(self, tmp_path):
        db = make_db(tmp_path)
        result = db._try_restore_from_backup(db.db_file)
        assert result is False

    def test_dado_bak_existente_quando_restore_db_entao_retorna_true(self, tmp_path):
        db = make_db(tmp_path)
        bak_data = {"/proj/bak": {"name": "bak"}}
        with open(db.db_file + ".bak", "w", encoding="utf-8") as f:
            json.dump(bak_data, f)
        result = db._try_restore_from_backup(db.db_file)
        assert result is True

    def test_dado_bak_existente_quando_restore_db_entao_database_carregado(self, tmp_path):
        db = make_db(tmp_path)
        bak_data = {"/proj/bak": {"name": "bak"}}
        with open(db.db_file + ".bak", "w", encoding="utf-8") as f:
            json.dump(bak_data, f)
        db._try_restore_from_backup(db.db_file)
        assert db.has_project("/proj/bak")

    def test_dado_bak_de_config_quando_restore_entao_config_carregado(self, tmp_path):
        db = make_db(tmp_path)
        bak_data = {"folders": ["/bak/pasta"], "models": {}}
        with open(db.config_file + ".bak", "w", encoding="utf-8") as f:
            json.dump(bak_data, f)
        db._try_restore_from_backup(db.config_file)
        assert db.config["folders"] == ["/bak/pasta"]


# ════════════════════════════════════════════════════════
# _save_json_atomic
# ════════════════════════════════════════════════════════

class TestDatabaseManagerSaveJsonAtomic:

    def test_dado_dados_validos_quando_save_atomic_entao_arquivo_criado(self, tmp_path):
        db = make_db(tmp_path)
        target = str(tmp_path / "output.json")
        db._save_json_atomic(target, {"chave": "valor"}, make_backup=False)
        assert os.path.exists(target)

    def test_dado_dados_validos_quando_save_atomic_entao_conteudo_correto(self, tmp_path):
        db = make_db(tmp_path)
        target = str(tmp_path / "output.json")
        db._save_json_atomic(target, {"x": 42}, make_backup=False)
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["x"] == 42

    def test_dado_arquivo_existente_quando_save_atomic_com_backup_entao_bak_criado(self, tmp_path):
        db = make_db(tmp_path)
        target = str(tmp_path / "output.json")
        # Cria arquivo original
        with open(target, "w", encoding="utf-8") as f:
            json.dump({"original": True}, f)
        db._save_json_atomic(target, {"novo": True}, make_backup=True)
        assert os.path.exists(target + ".bak")

    def test_dado_dados_nao_serializaveis_quando_save_atomic_entao_levanta_excecao(self, tmp_path):
        db = make_db(tmp_path)
        target = str(tmp_path / "output.json")
        with pytest.raises(TypeError):
            db._save_json_atomic(target, {"obj": object()}, make_backup=False)

    def test_dado_arquivo_existente_quando_save_atomic_entao_tmp_nao_sobra(self, tmp_path):
        """Após save bem-sucedido, o arquivo .tmp não deve existir."""
        db = make_db(tmp_path)
        target = str(tmp_path / "output.json")
        db._save_json_atomic(target, {"ok": True}, make_backup=False)
        assert not os.path.exists(target + ".tmp")
