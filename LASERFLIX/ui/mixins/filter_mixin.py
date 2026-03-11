"""
ui/mixins/filter_mixin.py — Métodos de filtro do LaserflixMainWindow.
"""


class FilterMixin:
    """Mixin com todos os métodos de filtro e busca."""

    def set_filter(self, filter_type: str) -> None:
        self.display_ctrl.set_filter(filter_type)
        self.sidebar.set_active_btn(None)
        self.header.set_active_filter(filter_type)

    def _on_search(self) -> None:
        self.display_ctrl.set_search_query(self.search_var.get())

    def _apply_filter(self, filter_type: str, value, btn=None, show_count=False):
        filter_methods = {
            "origin": self.display_ctrl.set_origin_filter,
            "category": self.display_ctrl.set_category_filter,
            "tag": self.display_ctrl.set_tag_filter,
            "collection": self.display_ctrl.set_collection_filter,
        }
        if filter_type in filter_methods:
            filter_methods[filter_type](value)
        self.sidebar.set_active_btn(btn)
        if show_count:
            if filter_type == "origin":
                count = sum(
                    1 for d in self.database.values() if d.get("origin") == value
                )
                self.status_bar.config(text=f"Origem: {value} ({count} projetos)")
            elif filter_type == "collection":
                count = self.collections_manager.get_collection_size(value)
                self.status_bar.config(
                    text=f"📁 Coleção: {value} ({count} projetos)"
                )

    def _add_filter_chip(self, filter_type: str, value) -> None:
        self.display_ctrl.add_filter_chip(filter_type, value)

    def _on_origin_filter(self, origin, btn=None) -> None:
        self._apply_filter("origin", origin, btn, show_count=True)

    def _on_category_filter(self, cats, btn=None) -> None:
        self._apply_filter("category", cats, btn)

    def _on_tag_filter(self, tag, btn=None) -> None:
        self._apply_filter("tag", tag, btn)

    def _on_collection_filter(self, collection_name: str, btn=None) -> None:
        self._apply_filter("collection", collection_name, btn, show_count=True)
