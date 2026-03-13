"""
ui/mixins/modal_mixin.py — Métodos de modais do LaserflixMainWindow.
"""
import os
from functools import partial

from ui.edit_modal import EditModal
from ui.project_modal import ProjectModal


class ModalMixin:
    """Mixin com abertura de modais, edit e callbacks internos."""

    def open_project_modal(self, project_path: str) -> None:
        if self.selection_ctrl.selection_mode:
            self.selection_ctrl.toggle_project(project_path)
            return
        ProjectModal(
            root=self.root,
            project_path=project_path,
            database=self.database,
            cb={
                "get_all_paths": lambda: [
                    p for p in self.database if os.path.isdir(p)
                ],
                "on_navigate": self.open_project_modal,
                "on_toggle": self._modal_toggle,
                "on_generate_desc": self._modal_generate_desc,
                "on_open_edit": self.open_edit_mode,
                "on_reanalize": self.analyze_single_project,
                "on_set_tag": partial(self._add_filter_chip, "tag"),
                "on_remove": self.remove_project,
                "get_project_collections": (
                    lambda p: self.collections_manager.get_project_collections(p)
                ),
            },
            cache=self.thumbnail_preloader,
            scanner=self.scanner,
        ).open()

    def _modal_toggle(self, path, key, value) -> None:
        if path in self.database:
            self.database[path][key] = value
            self.db_manager.save_database()
            self._invalidate_cache()
            self.display_projects()

    def _modal_generate_desc(self, path, desc_lbl, gen_btn, modal) -> None:
        self.modal_gen.generate_description(
            path, desc_lbl, gen_btn, modal, self.open_project_modal
        )

    def open_edit_mode(self, project_path: str) -> None:
        EditModal(
            self.root, project_path,
            self.database.get(project_path, {}),
            self._on_edit_save
        )

    def _on_edit_save(self, path, new_cats, new_tags) -> None:
        if path in self.database:
            if new_cats:
                self.database[path]["categories"] = new_cats
            self.database[path]["tags"] = new_tags
            self.database[path]["analyzed"] = True
            self.db_manager.save_database()
            self._invalidate_cache()
            self.sidebar.refresh(self.database, self.collections_manager)
            self.display_projects()
            self.status_bar.config(text="✓ Atualizado!")
