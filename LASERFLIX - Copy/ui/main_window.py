"""
ui/main_window.py — Orquestrador puro do Laserflix.

Responsabilidade única: orquestrar bootstrap, controllers e display.
Todo código de domínio está nos mixins e bootstrap.
"""
import tkinter as tk
from functools import partial

from config.settings import VERSION
from config.card_layout import COLS
from config.ui_constants import (
    BG_PRIMARY, SCROLL_SPEED, FG_TERTIARY,
)

from ui.bootstrap.core_setup import CoreSetup
from ui.bootstrap.managers_setup import ManagersSetup
from ui.bootstrap.callbacks_setup import CallbacksSetup

from ui.controllers.optimized_display_controller import OptimizedDisplayController
from ui.controllers.analysis_controller import AnalysisController
from ui.controllers.selection_controller import SelectionController
from ui.controllers.collection_controller import CollectionController
from ui.builders.ui_builder import UIBuilder
from ui.components.selection_bar import SelectionBar

from ui.mixins.filter_mixin import FilterMixin
from ui.mixins.toggle_mixin import ToggleMixin
from ui.mixins.analysis_mixin import AnalysisMixin
from ui.mixins.modal_mixin import ModalMixin
from ui.mixins.collection_mixin import CollectionMixin
from ui.mixins.dialog_mixin import DialogMixin
from ui.mixins.selection_mixin import SelectionMixin

from utils.logging_setup import LOGGER


class LaserflixMainWindow(
    FilterMixin,
    ToggleMixin,
    AnalysisMixin,
    ModalMixin,
    CollectionMixin,
    DialogMixin,
    SelectionMixin,
):
    def __init__(self, root: tk.Tk):
        self.root = root
        self.logger = LOGGER

        # ── 1. CORE SETUP (sem imports de core/ aqui) ──────────────────
        _core = CoreSetup()
        self.db_manager           = _core.db_manager
        self.collections_manager  = _core.collections_manager
        self.thumbnail_preloader  = _core.thumbnail_preloader
        self.scanner              = _core.scanner
        self.ollama               = _core.ollama
        self.image_analyzer       = _core.image_analyzer
        self.fallback_generator   = _core.fallback_generator
        self.text_generator       = _core.text_generator
        self.analysis_manager     = _core.analysis_manager
        self.database             = _core.database

        # ── 2. CONTROLLERS ─────────────────────────────────────────────
        self.selection_ctrl = SelectionController(
            database=self.database,
            db_manager=self.db_manager,
            collections_manager=self.collections_manager,
        )
        self.collection_ctrl = CollectionController(
            collections_manager=self.collections_manager,
            database=self.database,
        )

        # ── 3. ESTADO INTERNO ──────────────────────────────────────────
        self._last_display_state  = None
        self._force_rebuild       = False
        self._visible_range       = (0, 36)
        self._scroll_update_pending = False
        self._card_registry       = {}

        # ── 4. BUILD UI ────────────────────────────────────────────────
        self.root.title(f"LASERFLIX {VERSION}")
        self.root.state("zoomed")
        self.root.configure(bg=BG_PRIMARY)
        UIBuilder.build(self)

        # ── 5. SELECTION BAR ───────────────────────────────────────────
        self.selection_bar = SelectionBar(self.root)

        # ── 6. CONTROLLERS PÓS-UI ──────────────────────────────────────
        self.display_ctrl = OptimizedDisplayController(
            database=self.database,
            canvas=self.content_canvas,
            scrollable_frame=self.scrollable_frame,
            thumbnail_preloader=self.thumbnail_preloader,
            collections_manager=self.collections_manager,
            items_per_page=36,
        )
        self.display_ctrl.on_display_update = self.display_projects

        self.analysis_ctrl = AnalysisController(
            analysis_manager=self.analysis_manager,
            text_generator=self.text_generator,
            db_manager=self.db_manager,
            ollama_client=self.ollama,
        )

        # ── 7. MANAGERS ────────────────────────────────────────────────
        _mgr = ManagersSetup(self)
        self.import_manager       = _mgr.import_manager
        self.toggle_mgr           = _mgr.toggle_mgr
        self.collection_dialog_mgr = _mgr.collection_dialog_mgr
        self.progress_ui          = _mgr.progress_ui
        self.orphan_mgr           = _mgr.orphan_mgr
        self.modal_gen            = _mgr.modal_gen

        # ── 8. CALLBACKS WIRING ────────────────────────────────────────
        CallbacksSetup(self)

        # ── 9. STARTUP ─────────────────────────────────────────────────
        self.display_projects()
        self.logger.info("✨ Laserflix v%s iniciado (PERFORMANCE ENABLED)", VERSION)

    def __del__(self):
        if hasattr(self, 'thumbnail_preloader'):
            self.thumbnail_preloader.shutdown()

    # ── SCROLL ─────────────────────────────────────────────────────────
    def _on_scroll(self, event):
        self.content_canvas.yview_scroll(
            int(-1 * (event.delta / SCROLL_SPEED)), "units"
        )
        self._schedule_viewport_update()

    def _schedule_viewport_update(self):
        if self._scroll_update_pending:
            return
        self._scroll_update_pending = True
        self.root.after(100, self._update_visible_cards)

    def _update_visible_cards(self):
        self._scroll_update_pending = False

    # ── CACHE / REBUILD ────────────────────────────────────────────────
    def _should_rebuild(self) -> bool:
        if self._force_rebuild:
            self._force_rebuild = False
            return True
        current_state = self.display_ctrl.get_display_state()
        current_state["selection_mode"] = self.selection_ctrl.selection_mode
        current_state["db_hash"] = (
            len(self.database),
            sum(1 for d in self.database.values() if d.get("favorite")),
            sum(1 for d in self.database.values() if d.get("done")),
        )
        if self._last_display_state is None:
            self._last_display_state = current_state
            return True
        if current_state == self._last_display_state:
            return False
        self._last_display_state = current_state
        return True

    def _invalidate_cache(self) -> None:
        self._force_rebuild = True
        if hasattr(self.display_ctrl, 'invalidate_cache'):
            self.display_ctrl.invalidate_cache()

    def _refresh_all(self) -> None:
        self._invalidate_cache()
        self.display_projects()
        self.sidebar.refresh(self.database, self.collections_manager)

    # ── DISPLAY ────────────────────────────────────────────────────────
    def display_projects(self) -> None:
        if not self._should_rebuild():
            return
        for w in self.scrollable_frame.winfo_children():
            w.destroy()
        filtered_paths = self.display_ctrl.get_filtered_projects()
        all_filtered = [
            (p, self.database[p]) for p in filtered_paths if p in self.database
        ]
        all_filtered = self.display_ctrl.apply_sorting(all_filtered)
        total_count = len(all_filtered)
        page_info   = self.display_ctrl.get_page_info(total_count)
        page_items  = all_filtered[page_info["start_idx"]:page_info["end_idx"]]

        from ui.builders.header_builder import HeaderBuilder
        HeaderBuilder.build(
            self.scrollable_frame, self.display_ctrl,
            total_count=total_count, showing_count=len(page_items),
        )
        if not all_filtered:
            self._build_empty_state()
            return
        from ui.builders.cards_grid_builder import CardsGridBuilder
        self._card_registry = CardsGridBuilder.build(
            self.scrollable_frame, page_items, self._get_card_callbacks()
        )
        self.content_canvas.yview_moveto(0)

    def _get_card_callbacks(self) -> dict:
        return {
            "on_open_modal":           self.open_project_modal,
            "on_toggle_favorite":      self.toggle_favorite,
            "on_toggle_done":          self.toggle_done,
            "on_toggle_good":          self.toggle_good,
            "on_toggle_bad":           self.toggle_bad,
            "on_analyze_single":       self.analyze_single_project,
            "on_open_folder":          __import__('utils.platform_utils', fromlist=['open_folder']).open_folder,
            "on_set_category":         partial(self._add_filter_chip, "category"),
            "on_set_tag":              partial(self._add_filter_chip, "tag"),
            "on_set_origin":           partial(self._add_filter_chip, "origin"),
            "on_set_collection":       partial(self._add_filter_chip, "collection"),
            "get_cover_image_async":   self._get_thumbnail_async,
            "selection_mode":          self.selection_ctrl.selection_mode,
            "selected_paths":          self.selection_ctrl.selected_paths,
            "on_toggle_select":        self.selection_ctrl.toggle_project,
            "on_add_to_collection":    self._on_add_to_collection,
            "on_remove_from_collection": self._on_remove_from_collection,
            "on_new_collection_with":  self._on_new_collection_with,
            "get_collections":         lambda: list(self.collections_manager.collections.keys()),
            "get_project_collections": lambda p: self.collections_manager.get_project_collections(p),
        }

    def _build_empty_state(self) -> None:
        tk.Label(
            self.scrollable_frame,
            text="Nenhum projeto.\nClique em 'Importar Pastas' para adicionar.",
            font=("Arial", 14), bg=BG_PRIMARY, fg=FG_TERTIARY, justify="center",
        ).grid(row=2, column=0, columnspan=COLS, pady=80)

    def _get_thumbnail_async(self, project_path, callback, widget):
        def _ui_safe_callback(path, photo):
            try:
                if widget and widget.winfo_exists():
                    self.root.after(0, lambda: callback(path, photo))
            except Exception as e:
                self.logger.debug(f"Widget destruído: {e}")
        self.thumbnail_preloader.preload_single(project_path, _ui_safe_callback)

    def _on_import_complete(self) -> None:
        self.database = self.db_manager.database
        self.import_manager.database = self.database
        self.db_manager.save_database()
        self._invalidate_cache()
        self.sidebar.refresh(self.database, self.collections_manager)
        self.display_ctrl.current_page = 1
        self.display_projects()
        self.status_bar.config(text="✅ Importação concluída!")
