"""
core/performance/predictive_preloader.py — Preload preditivo de páginas.

PERFORMANCE OPTIMIZATION 3/3: Predictive Page Preloading

INSPIRAÇÃO:
- YouTube (pre-buffers next video)
- Spotify (preloads next 3 tracks)
- Chrome (prefetch de links)

CONCEITO:
┌────────────────────────────────┐
│ USER VIEWING Page 1             │
├────────────────────────────────┤
│ 👁️ Page 1: [rendered]            │
│ ⏳ Page 2: [preloading in bg...] │ ← Background
│ 💤 Page 3: [not loaded]          │
└────────────────────────────────┘

USER CLICKS "Next" → Page 2 INSTANT! (0ms wait)

GANHO:
- Antes: Clica Next → Espera 1080ms → Thumbs carregam
- Depois: Clica Next → 0ms espera → Thumbs já prontos!
"""

import threading
from typing import List, Tuple, Callable, Optional
from core.thumbnail_preloader import ThumbnailPreloader
from utils.logging_setup import LOGGER


class PredictivePreloader:
    """
    Preload preditivo de thumbnails das próximas páginas.
    
    Responsabilidades:
    - Detectar quando usuário está perto do fim da página
    - Preload de thumbnails da página seguinte em background
    - Adaptive prefetching (preload +1 ou +2 páginas)
    - Cancelar preload se usuário mudar de filtro
    """
    
    def __init__(
        self,
        thumbnail_preloader: ThumbnailPreloader,
        prefetch_pages: int = 1,
    ):
        """
        Args:
            thumbnail_preloader: Instância do ThumbnailPreloader
            prefetch_pages: Número de páginas a precarregar (1 = next page only)
        """
        self.thumb_preloader = thumbnail_preloader
        self.prefetch_pages = prefetch_pages
        
        # Estado
        self.current_page = 1
        self.preloaded_pages = set()  # Páginas já precarregadas
        self.active_preload_thread = None
        self.cancel_flag = threading.Event()
        
        self.logger = LOGGER
        self.logger.debug(
            f"🔮 PredictivePreloader: prefetch={prefetch_pages} pages"
        )
    
    def prefetch_next_page(
        self,
        current_page: int,
        total_pages: int,
        get_page_items_fn: Callable[[int], List[Tuple[str, dict]]],
    ) -> None:
        """
        Inicia preload da próxima página (se necessário).
        
        Args:
            current_page: Página atual (1-indexed)
            total_pages: Total de páginas
            get_page_items_fn: Função(page) -> List[(path, data)]
        
        Example:
            preloader.prefetch_next_page(
                current_page=1,
                total_pages=10,
                get_page_items_fn=lambda p: db.get_page(p)
            )
        """
        # Atualizar página atual
        if current_page != self.current_page:
            self.current_page = current_page
            self.preloaded_pages.discard(current_page)  # Remove da lista
        
        # Calcular páginas para preload
        pages_to_prefetch = []
        for offset in range(1, self.prefetch_pages + 1):
            next_page = current_page + offset
            if next_page <= total_pages and next_page not in self.preloaded_pages:
                pages_to_prefetch.append(next_page)
        
        if not pages_to_prefetch:
            return  # Nada para precarregar
        
        # Cancelar preload anterior (se existir)
        self._cancel_active_preload()
        
        # Iniciar novo preload em background
        self.cancel_flag.clear()
        self.active_preload_thread = threading.Thread(
            target=self._preload_pages_background,
            args=(pages_to_prefetch, get_page_items_fn),
            daemon=True,
            name="PredictivePreloader"
        )
        self.active_preload_thread.start()
        
        self.logger.debug(
            f"🔮 Prefetching pages: {pages_to_prefetch} "
            f"(current={current_page}, total={total_pages})"
        )
    
    def _preload_pages_background(
        self,
        pages: List[int],
        get_page_items_fn: Callable[[int], List[Tuple[str, dict]]],
    ) -> None:
        """
        Preload de páginas em background thread.
        
        Args:
            pages: Lista de números de página para preload
            get_page_items_fn: Função para obter items da página
        """
        for page_num in pages:
            if self.cancel_flag.is_set():
                self.logger.debug("❌ Preload cancelado")
                return  # Cancelado
            
            try:
                # 1. Obter items da página
                items = get_page_items_fn(page_num)
                project_paths = [path for path, _ in items]
                
                if not project_paths:
                    continue
                
                # 2. Preload thumbnails
                self.thumb_preloader.preload_batch(
                    project_paths=project_paths,
                    callback=None  # Sem callback (background)
                )
                
                # 3. Marcar como precarregado
                self.preloaded_pages.add(page_num)
                
                self.logger.info(
                    f"✅ Prefetch complete: page {page_num} "
                    f"({len(project_paths)} thumbnails)"
                )
            
            except Exception as e:
                self.logger.warning(f"Erro ao precarregar página {page_num}: {e}")
    
    def _cancel_active_preload(self) -> None:
        """
        Cancela preload ativo (se houver).
        """
        if self.active_preload_thread and self.active_preload_thread.is_alive():
            self.cancel_flag.set()  # Sinaliza cancelamento
            self.active_preload_thread.join(timeout=0.5)  # Espera até 500ms
            self.logger.debug("❌ Preload anterior cancelado")
    
    def on_filter_changed(self) -> None:
        """
        Callback quando filtro muda (invalida preload).
        """
        self._cancel_active_preload()
        self.preloaded_pages.clear()
        self.logger.debug("🔄 Filtro mudou - preload invalidado")
    
    def on_scroll_progress(self, progress_pct: float) -> None:
        """
        Callback quando usuário scrolla (0-100%).
        
        Inicia preload quando > 80%.
        
        Args:
            progress_pct: Porcentagem de scroll (0-100)
        """
        if progress_pct >= 80:
            # Usuário perto do fim - iniciar preload
            # (requer current_page, total_pages, get_page_items_fn)
            # Implementar no DisplayController
            pass
    
    def clear(self) -> None:
        """
        Limpa estado do preloader.
        """
        self._cancel_active_preload()
        self.preloaded_pages.clear()
        self.current_page = 1
    
    def get_stats(self) -> dict:
        """
        Estatísticas de preload.
        """
        return {
            "current_page": self.current_page,
            "preloaded_pages": sorted(self.preloaded_pages),
            "preloaded_count": len(self.preloaded_pages),
            "is_preloading": (
                self.active_preload_thread is not None
                and self.active_preload_thread.is_alive()
            ),
        }
