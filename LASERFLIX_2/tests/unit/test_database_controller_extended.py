"""
tests/unit/test_database_controller_extended.py

Cobre linhas ainda não testadas de core/database_controller.py:
  79-80   export() caminho de erro (shutil.copy levanta Exception)
  126-128 import_from_file() caminho de erro (shutil.copy levanta Exception após arquivo existir)

Regra: NUNCA alterar testes. Bugs são no app.
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
    db_file = str(tmp_path / "database.json")
    config_file = str(tmp_path / "config.json")
    db_manager = DatabaseManager(db_file=db_file, config_file=config_file)
    ctrl = DatabaseController(db_manager=db_manager, database_ref=db_manager.database)
    ctrl.on_show_info = MagicMock()
    ctrl.on_show_error = MagicMock()
    ctrl.on_status_message = MagicMock()
    ctrl.on_database_changed = MagicMock()
    ctrl.on_request_save_path = MagicMock()
    ctrl.on_request_open_path = MagicMock()
    return ctrl, db_manager


class TestDatabaseControllerExportError:

    def test_dado_shutil_copy_falha_quando_export_entao_show_error_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        export_dest = str(tmp_path / "export_dest.json")
        ctrl.on_request_save_path.return_value = export_dest
        with patch("core.database_controller.shutil.copy", side_effect=OSError("disco cheio")):
            ctrl.export()
        ctrl.on_show_error.assert_called_once()

    def test_dado_shutil_copy_falha_quando_export_entao_show_info_nao_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        db_manager.set_project("/proj/a", {"name": "A"})
        db_manager.save_database()
        export_dest = str(tmp_path / "export_dest.json")
        ctrl.on_request_save_path.return_value = export_dest
        with patch("core.database_controller.shutil.copy", side_effect=OSError("disco cheio")):
            ctrl.export()
        ctrl.on_show_info.assert_not_called()


class TestDatabaseControllerImportError:

    def test_dado_shutil_copy_falha_quando_import_entao_show_error_chamado(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        # Cria o arquivo de origem válido
        import_file = tmp_path / "import.json"
        import_file.write_text(json.dumps({"/proj/a": {"name": "A"}}), encoding="utf-8")
        # Garante que db existe para manual_backup não falhar
        db_manager.set_project("/proj/x", {"name": "X"})
        db_manager.save_database()
        with patch("core.database_controller.shutil.copy", side_effect=OSError("permissão negada")):
            result = ctrl.import_from_file(str(import_file))
        assert result is False
        ctrl.on_show_error.assert_called()

    def test_dado_shutil_copy_falha_quando_import_entao_retorna_false(self, tmp_path):
        ctrl, db_manager = make_controller(tmp_path)
        import_file = tmp_path / "import.json"
        import_file.write_text(json.dumps({"/proj/a": {"name": "A"}}), encoding="utf-8")
        db_manager.set_project("/proj/x", {"name": "X"})
        db_manager.save_database()
        with patch("core.database_controller.shutil.copy", side_effect=OSError("erro")):
            result = ctrl.import_from_file(str(import_file))
        assert result is False
