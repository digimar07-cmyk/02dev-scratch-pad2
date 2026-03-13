"""
tests/unit/test_database_controller.py

Testes unitários para core/database_controller.py → DatabaseController.

Metodologia Akita:
- DatabaseController usa callbacks de UI injetados (DI pura).
- Isolamento total: callbacks são MagicMock — sem Tkinter, sem disco real.
- Testamos O QUE o controller faz: chama callbacks corretos, retorna valores corretos.
- ZOMBIES: Z (sem callbacks), O (uma operação), E (arquivo não existe, exceção).
"""
import os
import sys
import json
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.database_controller import DatabaseController
from core.database import DatabaseManager


def make_controller(tmp_path):
    """Factory: DatabaseController com DB real (tmp_path) e callbacks mockados."""
    db_file = str(tmp_path / "database.json")
    config_file = str(tmp_path / "config.json")
    db_manager = DatabaseManager(db_file=db_file, config_file=config_file)
    # database_ref espelha o dict interno do db_manager
    ctrl = DatabaseController(
        db_manager=db_manager,
        database_ref=db_manager.database,
    )
    # Injeta callbacks mockados
    ctrl.on_show_info = MagicMock()
    ctrl.on_show_error = MagicMock()
    ctrl.on_status_message = MagicMock()
    ctrl.on_database_changed = MagicMock()
    ctrl.on_request_save_path = MagicMock()
    ctrl.on_request_open_path = MagicMock()
    return ctrl, db_manager


# ════════════════════════════════════════════════════════
# manual_backup
# ════════════════════════════════════════════════════════

class TestDatabaseControllerManualBackup:

    def test_dado_db_existente_quando_manual_backup_entao_retorna_true(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        # Garante que o arquivo db existe
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        # Redireciona diretório de backup para tmp_path
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy") as mock_copy:
                result = ctrl.manual_backup()
        assert result is True

    def test_dado_manual_backup_bem_sucedido_quando_show_info_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy"):
                ctrl.manual_backup()
        ctrl.on_show_info.assert_called_once()

    def test_dado_manual_backup_bem_sucedido_quando_status_message_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy"):
                ctrl.manual_backup()
        ctrl.on_status_message.assert_called_once()

    def test_dado_erro_no_copy_quando_manual_backup_entao_retorna_false(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy", side_effect=OSError("disco cheio")):
                result = ctrl.manual_backup()
        assert result is False

    def test_dado_erro_no_copy_quando_manual_backup_entao_show_error_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy", side_effect=OSError("disco cheio")):
                ctrl.manual_backup()
        ctrl.on_show_error.assert_called_once()


# ════════════════════════════════════════════════════════
# import_from_file
# ════════════════════════════════════════════════════════

class TestDatabaseControllerImport:

    def test_dado_arquivo_inexistente_quando_import_entao_retorna_false(self, tmp_path):
        ctrl, _ = make_controller(tmp_path)
        result = ctrl.import_from_file("/nao/existe.json")
        assert result is False

    def test_dado_arquivo_inexistente_quando_import_entao_show_error_chamado(self, tmp_path):
        ctrl, _ = make_controller(tmp_path)
        ctrl.import_from_file("/nao/existe.json")
        ctrl.on_show_error.assert_called_once()

    def test_dado_arquivo_valido_quando_import_entao_retorna_true(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        # Cria arquivo válido para importar
        import_file = tmp_path / "import.json"
        import_file.write_text(
            json.dumps({"/proj/a": {"name": "A"}}),
            encoding="utf-8"
        )
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy"):
                result = ctrl.import_from_file(str(import_file))
        assert result is True

    def test_dado_arquivo_valido_quando_import_entao_on_database_changed_chamado(self, tmp_path):
        ctrl, _ = make_controller(tmp_path)
        import_file = tmp_path / "import.json"
        import_file.write_text(
            json.dumps({"/proj/a": {"name": "A"}}),
            encoding="utf-8"
        )
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy"):
                ctrl.import_from_file(str(import_file))
        ctrl.on_database_changed.assert_called_once()


# ════════════════════════════════════════════════════════
# export
# ════════════════════════════════════════════════════════

class TestDatabaseControllerExport:

    def test_dado_sem_callback_save_path_quando_export_entao_nao_faz_nada(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        ctrl.on_request_save_path = None  # sem callback
        # Não deve levantar exceção
        ctrl.export()
        ctrl.on_show_info.assert_not_called()

    def test_dado_usuario_cancela_dialogo_quando_export_entao_nao_exporta(self, tmp_path):
        ctrl, _ = make_controller(tmp_path)
        ctrl.on_request_save_path.return_value = None  # usuário cancelou
        ctrl.export()
        ctrl.on_show_info.assert_not_called()

    def test_dado_path_valido_quando_export_entao_show_info_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        export_dest = str(tmp_path / "export_dest.json")
        ctrl.on_request_save_path.return_value = export_dest
        # Usa shutil real (arquivos estão em tmp_path)
        ctrl.export()
        ctrl.on_show_info.assert_called_once()

    def test_dado_path_valido_quando_export_entao_arquivo_criado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        export_dest = str(tmp_path / "export_dest.json")
        ctrl.on_request_save_path.return_value = export_dest
        ctrl.export()
        assert os.path.exists(export_dest)


# ════════════════════════════════════════════════════════
# callbacks sem injection (ZERO)
# ════════════════════════════════════════════════════════

class TestDatabaseControllerCallbacksNone:
    """ZERO: callbacks None não devem causar exceção."""

    def test_dado_todos_callbacks_none_quando_manual_backup_entao_nao_explode(self, tmp_path):
        db_file = str(tmp_path / "database.json")
        config_file = str(tmp_path / "config.json")
        db_manager = DatabaseManager(db_file=db_file, config_file=config_file)
        db_manager.set_project("/proj/a", {})
        db_manager.save_database()
        ctrl = DatabaseController(db_manager=db_manager, database_ref=db_manager.database)
        # Todos callbacks são None por padrão
        with patch("core.database_controller.os.makedirs"):
            with patch("core.database_controller.shutil.copy"):
                try:
                    ctrl.manual_backup()
                except Exception as e:
                    pytest.fail(f"manual_backup não deve explodir sem callbacks: {e}")
