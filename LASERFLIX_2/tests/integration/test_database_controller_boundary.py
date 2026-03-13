"""
tests/integration/test_database_controller_boundary.py

Testa contratos e fronteira arquitetural do DatabaseController.
Dois tipos:
  1. Arquiteturais: verifica que core/ nao importa tkinter
  2. Comportamentais: contratos de callback, import, export, boundary UI/core

Metodologia Akita: DatabaseController nao pode ter Tkinter.
Callbacks sao injetados para simular a UI sem instanciar janelas.
"""
import os
import json
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


# ── Testes Arquiteturais ──────────────────────────────────────────────────────

class TestArquitetura:

    def test_database_controller_has_no_tkinter(self):
        """database_controller em core/ nao pode ter tkinter."""
        path = ROOT / "core" / "database_controller.py"
        content = path.read_text(encoding="utf-8")
        assert "import tkinter" not in content
        assert "from tkinter" not in content
        assert "import customtkinter" not in content

    def test_database_controller_public_interface(self):
        """database_controller.py deve expor ao menos uma classe publica."""
        import importlib
        mod = importlib.import_module("core.database_controller")
        classes = [
            name for name in dir(mod)
            if not name.startswith("_") and isinstance(getattr(mod, name), type)
        ]
        assert classes, "core.database_controller nao expoe classe publica."

    def test_core_database_has_public_class(self):
        """core.database deve ter ao menos uma classe instanciavel."""
        import importlib
        mod = importlib.import_module("core.database")
        classes = [
            name for name in dir(mod)
            if not name.startswith("_") and isinstance(getattr(mod, name), type)
        ]
        assert classes, "Nenhuma classe publica em core.database"


# ── Fixture helpers ───────────────────────────────────────────────────────────

@pytest.fixture
def db_com_dados(tmp_path):
    """DatabaseManager com db_file real e um projeto pre-inserido."""
    from core.database import DatabaseManager
    db_file = str(tmp_path / "db.json")
    db = DatabaseManager(
        db_file=db_file,
        config_file=str(tmp_path / "cfg.json")
    )
    db.set_project("/fake/proj", {"name": "Teste"})
    db.save_database()
    # Expoe db_path para compatibilidade com DatabaseController
    db.db_path = db_file
    return db


@pytest.fixture
def controller(db_com_dados):
    """DatabaseController pronto para uso com callbacks capturados."""
    from core.database_controller import DatabaseController
    ctrl = DatabaseController(
        db_manager=db_com_dados,
        database_ref=db_com_dados.database
    )
    # Captura mensagens sem precisar de UI
    ctrl._info_calls = []
    ctrl._error_calls = []
    ctrl._status_calls = []
    ctrl._changed_calls = []
    ctrl.on_show_info = lambda t, m: ctrl._info_calls.append((t, m))
    ctrl.on_show_error = lambda t, m: ctrl._error_calls.append((t, m))
    ctrl.on_status_message = lambda m: ctrl._status_calls.append(m)
    ctrl.on_database_changed = lambda: ctrl._changed_calls.append(True)
    return ctrl


# ── Testes Comportamentais ───────────────────────────────────────────────────

class TestImportFromFile:

    def test_import_arquivo_valido_retorna_true(self, controller, tmp_path):
        """Importar JSON valido deve retornar True e disparar on_database_changed."""
        # Cria arquivo fonte
        src = tmp_path / "fonte.json"
        src.write_text(json.dumps({"/outro/proj": {"name": "Importado"}}))

        result = controller.import_from_file(str(src))
        assert result is True
        assert len(controller._changed_calls) == 1

    def test_import_arquivo_inexistente_retorna_false(self, controller, tmp_path):
        """Importar arquivo que nao existe deve retornar False e disparar on_show_error."""
        result = controller.import_from_file(str(tmp_path / "nao_existe.json"))
        assert result is False
        assert len(controller._error_calls) == 1

    def test_import_dispara_status_message(self, controller, tmp_path):
        """Import bem-sucedido deve disparar on_status_message."""
        src = tmp_path / "db_source.json"
        src.write_text(json.dumps({"/proj": {"name": "X"}}))
        controller.import_from_file(str(src))
        assert len(controller._status_calls) >= 1

    def test_import_nao_dispara_changed_em_falha(self, controller, tmp_path):
        """Import falhado nao deve disparar on_database_changed."""
        controller.import_from_file(str(tmp_path / "fantasma.json"))
        assert len(controller._changed_calls) == 0


class TestManualBackup:

    def test_manual_backup_retorna_true(self, controller):
        """manual_backup com db_file existente deve retornar True."""
        result = controller.manual_backup()
        assert result is True

    def test_manual_backup_dispara_info(self, controller):
        """manual_backup deve disparar on_show_info."""
        controller.manual_backup()
        assert len(controller._info_calls) == 1

    def test_manual_backup_dispara_status(self, controller):
        """manual_backup deve disparar on_status_message."""
        controller.manual_backup()
        assert len(controller._status_calls) == 1


class TestExport:

    def test_export_sem_callback_nao_explode(self, controller):
        """export() sem on_request_save_path nao deve explodir."""
        controller.on_request_save_path = None
        controller.export()  # Deve retornar silenciosamente

    def test_export_com_callback_none_nao_exporta(self, controller):
        """Se callback retornar None (usuario cancelou), nao deve exportar nem disparar info."""
        controller.on_request_save_path = lambda **kw: None
        controller.export()
        assert len(controller._info_calls) == 0
