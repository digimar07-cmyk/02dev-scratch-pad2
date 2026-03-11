"""
ui/mixins/dialog_mixin.py — Wrappers de dialogs do LaserflixMainWindow.
"""
from ui.managers.dialog_manager import DialogManager


class DialogMixin:
    """Mixin com todos os métodos de dialogs externos."""

    def open_import_dialog(self) -> None:
        self.import_manager.database = self.database
        self.import_manager.start_import()

    def open_prepare_folders(self) -> None:
        DialogManager.open_prepare_folders(self)

    def open_model_settings(self) -> None:
        DialogManager.open_model_settings(self)

    def open_categories_picker(self) -> None:
        DialogManager.open_categories_picker(self)

    def export_database(self) -> None:
        DialogManager.export_database(self)

    def import_database(self) -> None:
        DialogManager.import_database(self)

    def manual_backup(self) -> None:
        DialogManager.manual_backup(self)
