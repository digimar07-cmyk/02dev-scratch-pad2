"""
ui/mixins/selection_mixin.py — Callbacks de seleção do LaserflixMainWindow.
"""
import tkinter as tk


class SelectionMixin:
    """Mixin com callbacks de seleção e visual de cards."""

    def _on_selection_mode_changed(self, is_active: bool) -> None:
        if is_active:
            self.selection_bar.show()
            self.header.set_select_btn_active(True)
        else:
            self.selection_bar.hide()
            self.header.set_select_btn_active(False)
        self._invalidate_cache()
        self.display_projects()

    def _on_selection_count_changed(self, count: int) -> None:
        """Atualiza APENAS o contador da barra — SEM rebuild de cards."""
        self.selection_bar.update_count(count)

    def _on_projects_removed(self, count: int) -> None:
        """FIX-REMOVE-REFRESH: Atualiza status bar após remoção."""
        self.status_bar.config(text=f"🗑️ {count} projeto(s) removido(s)")

    def _update_card_selection_visual(self, path: str, is_selected: bool) -> None:
        """
        FIX-SELECTION-FLICKER: Atualiza visual de UM card específico.
        Sem rebuild. Scroll mantido.
        """
        card = self._card_registry.get(path)
        if not card:
            return
        try:
            if not card.winfo_exists():
                return
            border_color = "#FFFF00" if is_selected else "#1E1E2E"
            thickness = 2 if is_selected else 0
            card.config(
                bg=border_color,
                highlightbackground=border_color,
                highlightthickness=thickness,
            )
            inner = card.winfo_children()
            if inner:
                pad = 2 if is_selected else 0
                inner[0].pack_configure(padx=pad, pady=pad)
        except tk.TclError:
            pass
