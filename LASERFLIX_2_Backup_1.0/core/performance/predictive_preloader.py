"""
core/performance/predictive_preloader.py — Preload preditivo de páginas.
"""
import threading
from typing import List, Tuple, Callable
from core.thumbnail_preloader import ThumbnailPreloader
from utils.logging_setup import LOGGER


class PredictivePreloader:
    """Preload preditivo de thumbnails das próximas páginas."""

    def __init__(self, thumbnail_preloader: ThumbnailPreloader, prefetch_pages: int = 1):
        self.thumb_preloader = thumbnail_preloader
        self.prefetch_pages = prefetch_pages
        self.current_page = 1
        self.preloaded_pages: set = set()
        self.active_preload_thread = None
        self.cancel_flag = threading.Event()
        self.logger = LOGGER
        self.logger.debug(f"🔮 PredictivePreloader: prefetch={prefetch_pages} pages")

    def prefetch_next_page(
        self,
        current_page: int,
        total_pages: int,
        get_page_items_fn: Callable[[int], List[Tuple[str, dict]]],
    ) -> None:
        if current_page != self.current_page:
            self.current_page = current_page
            self.preloaded_pages.discard(current_page)
        pages_to_prefetch = [
            current_page + offset
            for offset in range(1, self.prefetch_pages + 1)
            if (current_page + offset) <= total_pages
            and (current_page + offset) not in self.preloaded_pages
        ]
        if not pages_to_prefetch:
            return
        self._cancel_active_preload()
        self.cancel_flag.clear()
        self.active_preload_thread = threading.Thread(
            target=self._preload_pages_background,
            args=(pages_to_prefetch, get_page_items_fn),
            daemon=True,
            name="PredictivePreloader",
        )
        self.active_preload_thread.start()
        self.logger.debug(f"🔮 Prefetching pages: {pages_to_prefetch} (current={current_page}, total={total_pages})")

    def _preload_pages_background(
        self,
        pages: List[int],
        get_page_items_fn: Callable[[int], List[Tuple[str, dict]]],
    ) -> None:
        for page_num in pages:
            if self.cancel_flag.is_set():
                self.logger.debug("❌ Preload cancelado")
                return
            try:
                items = get_page_items_fn(page_num)
                project_paths = [path for path, _ in items]
                if not project_paths:
                    continue
                self.thumb_preloader.preload_batch(project_paths=project_paths, callback=None)
                self.preloaded_pages.add(page_num)
                self.logger.info(f"✅ Prefetch complete: page {page_num} ({len(project_paths)} thumbnails)")
            except Exception as e:
                self.logger.warning(f"Erro ao precarregar página {page_num}: {e}")

    def _cancel_active_preload(self) -> None:
        if self.active_preload_thread and self.active_preload_thread.is_alive():
            self.cancel_flag.set()
            self.active_preload_thread.join(timeout=0.5)
            self.logger.debug("❌ Preload anterior cancelado")

    def on_filter_changed(self) -> None:
        self._cancel_active_preload()
        self.preloaded_pages.clear()
        self.logger.debug("🔄 Filtro mudou - preload invalidado")

    def on_scroll_progress(self, progress_pct: float) -> None:
        if progress_pct >= 80:
            pass

    def clear(self) -> None:
        self._cancel_active_preload()
        self.preloaded_pages.clear()
        self.current_page = 1

    def get_stats(self) -> dict:
        return {
            "current_page": self.current_page,
            "preloaded_pages": sorted(self.preloaded_pages),
            "preloaded_count": len(self.preloaded_pages),
            "is_preloading": (
                self.active_preload_thread is not None
                and self.active_preload_thread.is_alive()
            ),
        }
