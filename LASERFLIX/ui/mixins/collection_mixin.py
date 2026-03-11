"""
ui/mixins/collection_mixin.py — Wrappers de coleção do LaserflixMainWindow.
"""


class CollectionMixin:
    """Mixin com wrappers de coleção e dialog de coleções."""

    def _on_add_to_collection(self, project_path: str, collection_name: str) -> None:
        self.collection_dialog_mgr.add_to_collection(project_path, collection_name)

    def _on_remove_from_collection(
        self, project_path: str, collection_name: str
    ) -> None:
        self.collection_dialog_mgr.remove_from_collection(
            project_path, collection_name
        )

    def _on_new_collection_with(self, project_path: str) -> None:
        self.collection_dialog_mgr.new_collection_with(project_path)

    def open_collections_dialog(self) -> None:
        self.collection_dialog_mgr.open_collections_dialog()
