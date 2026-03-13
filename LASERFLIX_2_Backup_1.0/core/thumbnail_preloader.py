"""
core/thumbnail_preloader.py - Thumbnail Batch Preloader
"""
import os
import threading
from concurrent.futures import ThreadPoolExecutor
from collections import OrderedDict
from typing import List, Callable, Optional, Tuple
from PIL import Image, ImageTk

from config.settings import THUMBNAIL_CACHE_LIMIT, THUMBNAIL_SIZE
from config.constants import FILE_EXTENSIONS
from utils.logging_setup import LOGGER


class ThumbnailPreloader:
    """Carregador paralelo de thumbnails com cache LRU."""

    def __init__(
        self,
        max_workers: int = 4,
        cache_limit: int = THUMBNAIL_CACHE_LIMIT,
        thumbnail_size: Tuple[int, int] = THUMBNAIL_SIZE,
    ):
        self.max_workers = max_workers
        self.cache_limit = cache_limit
        self.thumbnail_size = thumbnail_size
        self.executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix="ThumbLoader")
        self.cache: OrderedDict = OrderedDict()
        self.cache_lock = threading.Lock()
        self.logger = LOGGER
        self.logger.info(f"📷 Thumbnail Preloader iniciado: {max_workers} threads, cache {cache_limit} images")

    def preload_batch(
        self,
        project_paths: List[str],
        callback: Optional[Callable[[str, ImageTk.PhotoImage], None]] = None,
    ) -> dict:
        if not project_paths:
            return {}
        results = {}
        futures = []
        for path in project_paths:
            cached = self._get_from_cache(path)
            if cached:
                results[path] = cached
                if callback:
                    callback(path, cached)
                continue
            future = self.executor.submit(self._load_thumbnail, path)
            futures.append((path, future))
        for path, future in futures:
            try:
                photo = future.result(timeout=2.0)
                if photo:
                    results[path] = photo
                    self._add_to_cache(path, photo)
                    if callback:
                        callback(path, photo)
            except Exception as e:
                self.logger.warning(f"Erro ao carregar thumb de {path}: {e}")
        return results

    def preload_single(
        self,
        project_path: str,
        callback: Optional[Callable[[str, ImageTk.PhotoImage], None]] = None,
    ) -> Optional[ImageTk.PhotoImage]:
        cached = self._get_from_cache(project_path)
        if cached:
            if callback:
                callback(project_path, cached)
            return cached

        def _async_load():
            photo = self._load_thumbnail(project_path)
            if photo:
                self._add_to_cache(project_path, photo)
                if callback:
                    callback(project_path, photo)

        self.executor.submit(_async_load)
        return None

    def _load_thumbnail(self, project_path: str) -> Optional[ImageTk.PhotoImage]:
        try:
            img_path = self.find_first_image(project_path)
            if not img_path:
                return None
            img = Image.open(img_path)
            img.thumbnail(self.thumbnail_size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            self.logger.debug(f"Erro ao carregar thumb de {project_path}: {e}")
            return None

    def find_first_image(self, project_path: str) -> Optional[str]:
        valid_extensions = FILE_EXTENSIONS["images"]
        try:
            for item in sorted(os.listdir(project_path)):
                if item.lower().endswith(valid_extensions):
                    full_path = os.path.join(project_path, item)
                    if os.path.isfile(full_path):
                        return full_path
        except Exception:
            pass
        return None

    def _get_from_cache(self, project_path: str) -> Optional[ImageTk.PhotoImage]:
        with self.cache_lock:
            img_path = self.find_first_image(project_path)
            if not img_path:
                return None
            cached = self.cache.get(img_path)
            if cached:
                self.cache.move_to_end(img_path)
                return cached
        return None

    def _add_to_cache(self, project_path: str, photo: ImageTk.PhotoImage) -> None:
        img_path = self.find_first_image(project_path)
        if not img_path:
            return
        with self.cache_lock:
            self.cache[img_path] = photo
            self.cache.move_to_end(img_path)
            while len(self.cache) > self.cache_limit:
                oldest_key, _ = self.cache.popitem(last=False)
                self.logger.debug(f"🗑️ Cache LRU: evicted {oldest_key}")

    def clear_cache(self) -> None:
        with self.cache_lock:
            self.cache.clear()
        self.logger.info("🗑️ Cache de thumbnails limpo")

    def shutdown(self) -> None:
        self.executor.shutdown(wait=True, cancel_futures=True)
        self.logger.info("📷 Thumbnail Preloader parado")

    def get_stats(self) -> dict:
        with self.cache_lock:
            cache_size = len(self.cache)
        return {
            "cache_size": cache_size,
            "cache_limit": self.cache_limit,
            "cache_usage_pct": (cache_size / self.cache_limit * 100) if self.cache_limit > 0 else 0,
            "max_workers": self.max_workers,
        }
