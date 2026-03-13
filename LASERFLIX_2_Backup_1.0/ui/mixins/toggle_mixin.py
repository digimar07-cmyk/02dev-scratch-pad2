"""
ui/mixins/toggle_mixin.py — Métodos de toggle e remoção do LaserflixMainWindow.
"""


class ToggleMixin:
    """Mixin com toggle de favorito, done, good, bad e remoção."""

    def toggle_favorite(self, path, btn=None) -> None:
        self.toggle_mgr.toggle_favorite(path, btn)
        self._invalidate_cache()

    def toggle_done(self, path, btn=None) -> None:
        self.toggle_mgr.toggle_done(path, btn)
        self._invalidate_cache()

    def toggle_good(self, path, btn=None) -> None:
        self.toggle_mgr.toggle_good(path, btn)
        self._invalidate_cache()

    def toggle_bad(self, path, btn=None) -> None:
        self.toggle_mgr.toggle_bad(path, btn)
        self._invalidate_cache()

    def remove_project(self, path: str) -> None:
        if path in self.database:
            name = self.database[path].get("name", path)
            self.database.pop(path)
            self.db_manager.save_database()
            self._invalidate_cache()
            self.collections_manager.clean_orphan_projects(set(self.database.keys()))
            self.sidebar.refresh(self.database, self.collections_manager)
            self.display_projects()
            self.status_bar.config(text=f"🗑️ '{name}' removido do banco.")

    def clean_orphans(self) -> None:
        self.orphan_mgr.clean_orphans()
