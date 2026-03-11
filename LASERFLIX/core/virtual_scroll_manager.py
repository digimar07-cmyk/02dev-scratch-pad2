"""
core/virtual_scroll_manager.py - Virtual Scroll Engine

NOTA ARQUITETURAL:
  core/ não pode depender de tkinter (fronteira ui/core).
  Os objetos canvas/frame reais são injetados pelo caller em ui/.
  Type hints usam Any para manter compatibilidade sem import de UI.
"""
from typing import Any, List, Callable, Tuple
from utils.logging_setup import LOGGER


class VirtualScrollManager:
    """Gerenciador de scroll virtual para grandes datasets."""

    def __init__(
        self,
        canvas: Any,
        scrollable_frame: Any,
        data: List,
        card_renderer: Callable,
        cols: int = 6,
        card_width: int = 280,
        card_height: int = 410,
        card_pad: int = 8,
        buffer_multiplier: float = 1.5,
    ):
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        self.data = data
        self.card_renderer = card_renderer
        self.cols = cols
        self.card_width = card_width
        self.card_height = card_height
        self.card_pad = card_pad
        self.buffer_multiplier = buffer_multiplier
        self.widget_pool: List[Any] = []
        self.active_widgets: dict = {}
        self.visible_range: Tuple[int, int] = (0, 0)
        self.last_scroll_pos: float = 0.0
        self._scroll_update_pending = False
        self.logger = LOGGER
        self._calculate_viewport()
        self.canvas.bind("<Configure>", self._on_canvas_resize)

    def _calculate_viewport(self) -> None:
        try:
            viewport_height = self.canvas.winfo_height()
            if viewport_height <= 1:
                viewport_height = 1080
            row_height = self.card_height + (self.card_pad * 2)
            visible_rows = max(1, int(viewport_height / row_height))
            visible_cards = visible_rows * self.cols
            buffer_cards = int(visible_cards * self.buffer_multiplier)
            self.viewport_size = visible_cards
            self.buffer_size = buffer_cards
            self.max_pool_size = visible_cards + buffer_cards
            self.logger.info(
                f"📐 Viewport calculado: {visible_rows} linhas × {self.cols} cols = "
                f"{visible_cards} visíveis + {buffer_cards} buffer = {self.max_pool_size} total"
            )
        except Exception as e:
            self.logger.warning(f"Erro ao calcular viewport: {e}, usando padrão")
            self.viewport_size = 18
            self.buffer_size = 12
            self.max_pool_size = 30

    def _on_canvas_resize(self, event=None) -> None:
        self._calculate_viewport()
        self.update_visible_items()

    def update_visible_items(self) -> None:
        if self._scroll_update_pending:
            return
        if not self.data:
            return
        self._scroll_update_pending = True
        try:
            scroll_pos = self.canvas.yview()[0]
            total_items = len(self.data)
            total_rows = (total_items + self.cols - 1) // self.cols
            row_height = self.card_height + (self.card_pad * 2)
            total_height = total_rows * row_height
            scroll_pixels = scroll_pos * total_height
            first_visible_row = max(0, int(scroll_pixels / row_height) - 1)
            visible_rows = (self.viewport_size // self.cols) + 2
            last_visible_row = min(total_rows, first_visible_row + visible_rows)
            start_idx = first_visible_row * self.cols
            end_idx = min(total_items, last_visible_row * self.cols)
            new_range = (start_idx, end_idx)
            if new_range == self.visible_range:
                return
            self.visible_range = new_range
            self._recycle_widgets(start_idx, end_idx)
            self._render_visible_items(start_idx, end_idx)
        finally:
            self._scroll_update_pending = False

    def _recycle_widgets(self, start_idx: int, end_idx: int) -> None:
        to_remove = []
        for idx, widget in self.active_widgets.items():
            if idx < start_idx or idx >= end_idx:
                widget.grid_forget()
                self.widget_pool.append(widget)
                to_remove.append(idx)
        for idx in to_remove:
            del self.active_widgets[idx]

    def _render_visible_items(self, start_idx: int, end_idx: int) -> None:
        for idx in range(start_idx, end_idx):
            if idx >= len(self.data):
                break
            if idx in self.active_widgets:
                continue
            row = (idx // self.cols) + 2
            col = idx % self.cols
            project_path, project_data = self.data[idx]
            widget = self.card_renderer(self.scrollable_frame, project_path, project_data, row, col)
            self.active_widgets[idx] = widget

    def refresh_data(self, new_data: List) -> None:
        self.clear()
        self.data = new_data
        self.visible_range = (0, 0)
        self.update_visible_items()
        self.canvas.yview_moveto(0)

    def clear(self) -> None:
        for widget in self.active_widgets.values():
            widget.destroy()
        for widget in self.widget_pool:
            widget.destroy()
        self.active_widgets.clear()
        self.widget_pool.clear()
        self.visible_range = (0, 0)

    def get_stats(self) -> dict:
        return {
            "total_items": len(self.data),
            "active_widgets": len(self.active_widgets),
            "pool_size": len(self.widget_pool),
            "visible_range": self.visible_range,
            "viewport_size": self.viewport_size,
            "buffer_size": self.buffer_size,
            "max_pool": self.max_pool_size,
        }
