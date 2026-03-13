"""
core/database_controller.py — Controla operações de alto nível do database.

FASE 7F.2: Centraliza operações de database
Redução estimada: -30 linhas no main_window.py

NOTA ARQUITETURAL:
  core/ não pode depender de frameworks de UI (fronteira ui/core).
  Dialogs (file open/save, messageboxes) são responsabilidade da UI.
  Este controller usa callbacks para notificar a UI sobre
  sucesso/erro, mantendo a lógica de negócio pura em core/.

  CALLBACKS ESPERADOS (injetados pela camada ui/ após instanciar):
    on_request_save_path(title, default_ext, filetypes) -> str | None
    on_request_open_path(title, filetypes) -> str | None
    on_show_info(title, message)
    on_show_error(title, message)
    on_status_message(message)
    on_database_changed()
"""
import os
import shutil
from datetime import datetime
from typing import Callable, Optional


class DatabaseController:
    """
    Controla operações de alto nível do database.

    Responsabilidades:
    - Export de database
    - Backup manual
    - Import de database

    A UI injeta callbacks para dialogs e notificações.
    """

    def __init__(self, db_manager, database_ref, parent=None):
        self.db_manager = db_manager
        self.database = database_ref
        self.parent = parent  # mantido por compatibilidade, não usado internamente

        # Callbacks de negócio
        self.on_database_changed: Optional[Callable] = None
        self.on_status_message: Optional[Callable[[str], None]] = None

        # Callbacks de UI (injetados pela camada ui/ após instanciar)
        self.on_request_save_path: Optional[Callable] = None
        self.on_request_open_path: Optional[Callable] = None
        self.on_show_info: Optional[Callable[[str, str], None]] = None
        self.on_show_error: Optional[Callable[[str, str], None]] = None

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def export(self) -> None:
        """Exporta database para arquivo escolhido pela UI."""
        if not self.on_request_save_path:
            return

        filename = self.on_request_save_path(
            title="Exportar Database",
            default_ext=".json",
            filetypes=[("JSON files", "*.json")],
        )

        if not filename:
            return

        try:
            shutil.copy(self.db_manager.db_file, filename)  # FIX: db_path → db_file
            self._show_info(
                "✅ Export concluído",
                f"Database exportado para:\n{filename}",
            )
            self._notify_status(f"Database exportado: {os.path.basename(filename)}")
        except Exception as e:
            self._show_error("❌ Erro no export", f"Não foi possível exportar:\n{e}")

    def manual_backup(self) -> bool:
        """Cria backup manual do database. Retorna True se bem-sucedido."""
        try:
            backup_dir = "backups"
            os.makedirs(backup_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.json")

            shutil.copy(self.db_manager.db_file, backup_file)  # FIX: db_path → db_file

            self._show_info(
                "✅ Backup criado",
                f"Backup salvo em:\n{backup_file}",
            )
            self._notify_status(f"Backup criado: {os.path.basename(backup_file)}")
            return True
        except Exception as e:
            self._show_error("❌ Erro no backup", f"Não foi possível criar backup:\n{e}")
            return False

    def import_from_file(self, filepath: str) -> bool:
        """Importa database de arquivo. Retorna True se bem-sucedido."""
        if not os.path.exists(filepath):
            self._show_error(
                "❌ Arquivo não encontrado",
                f"Arquivo não existe:\n{filepath}",
            )
            return False

        try:
            self.manual_backup()

            shutil.copy(filepath, self.db_manager.db_file)  # FIX: db_path → db_file
            self.db_manager.load_database()

            self._show_info(
                "✅ Import concluído",
                f"Database importado de:\n{filepath}",
            )
            self._notify_status(f"Database importado: {os.path.basename(filepath)}")
            self._notify_changed()
            return True

        except Exception as e:
            self._show_error("❌ Erro no import", f"Não foi possível importar:\n{e}")
            return False

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------

    def _notify_status(self, message: str) -> None:
        if self.on_status_message:
            self.on_status_message(message)

    def _notify_changed(self) -> None:
        if self.on_database_changed:
            self.on_database_changed()

    def _show_info(self, title: str, message: str) -> None:
        if self.on_show_info:
            self.on_show_info(title, message)

    def _show_error(self, title: str, message: str) -> None:
        if self.on_show_error:
            self.on_show_error(title, message)
