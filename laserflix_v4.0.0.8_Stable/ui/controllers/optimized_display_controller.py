"""
ui/controllers/optimized_display_controller.py — DisplayController Otimizado

Controller de display com filtros, ordenação, paginação e cache.

🔥 REFATORADO em 09/03/2026:
   - Removida herança de DisplayController (arquivo legado deletado)
   - Agora é um controller standalone com todos os métodos próprios
   - Assinatura do __init__ restaurada para compatibilidade com main_window.py
"""

import tkinter as tk
from typing import Callable, Optional, List, Tuple, Any
from utils.logging_setup import LOGGER


class OptimizedDisplayController:
    """
    Controller de display com filtros, ordenação, paginação e cache.
    
    Responsabilidades:
    - Filtrar projetos (categoria, tag, origem, busca, favoritos, etc)
    - Ordenar projetos (nome, data, tipo)
    - Paginar resultados
    - Cache de filtros para performance
    
    Padrão: MVC Controller + Cache Strategy
    """
    
    def __init__(
        self,
        database: dict,
        canvas: Optional[tk.Canvas] = None,
        scrollable_frame: Optional[tk.Frame] = None,
        thumbnail_preloader=None,
        collections_manager=None,
        items_per_page: int = 36,
    ):
        """
        Args:
            database: Database de projetos
            canvas: Canvas com scroll (opcional, para retrocompatibilidade)
            scrollable_frame: Frame interno scrollable (opcional)
            thumbnail_preloader: Instância do ThumbnailPreloader (opcional)
            collections_manager: Gerenciador de coleções
            items_per_page: Cards por página
        """
        self.database = database
        self.canvas = canvas
        self.scrollable_frame = scrollable_frame
        self.thumbnail_preloader = thumbnail_preloader
        self.collections_manager = collections_manager
        self.items_per_page = items_per_page
        self.logger = LOGGER
        
        # Estado de filtros
        self.current_filter: str = "all"
        self.current_origin: Optional[str] = None
        self.current_categories: set = set()
        self.current_tag: Optional[str] = None
        self.current_collection: Optional[str] = None
        self.search_query: str = ""
        self.active_filters: List[dict] = []
        
        # Estado de ordenação
        self.current_sort: str = "name"
        
        # Estado de paginação
        self.current_page: int = 1
        self.total_pages: int = 1
        
        # Cache simples de filtros
        self._filter_cache: dict = {}
        self._cache_enabled: bool = True
        
        # Callback para atualização da UI
        self.on_display_update: Optional[Callable[[], None]] = None
    
    # ═══════════════════════════════════════════════════════════════
    # FILTROS
    # ═══════════════════════════════════════════════════════════════
    
    def set_filter(self, filter_type: str) -> None:
        """Define filtro principal (all, favorites, done, etc)."""
        self.current_filter = filter_type
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def set_origin_filter(self, origin: Optional[str]) -> None:
        """Define filtro de origem (pasta raiz)."""
        self.current_origin = origin
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def set_category_filter(self, categories) -> None:
        """Define filtro de categorias."""
        if isinstance(categories, str):
            self.current_categories = {categories}
        elif isinstance(categories, (list, set)):
            self.current_categories = set(categories)
        else:
            self.current_categories = set()
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def set_tag_filter(self, tag: Optional[str]) -> None:
        """Define filtro de tag."""
        self.current_tag = tag
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def set_collection_filter(self, collection: Optional[str]) -> None:
        """Define filtro de coleção."""
        self.current_collection = collection
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def set_search_query(self, query: str) -> None:
        """Define busca textual."""
        self.search_query = query.lower().strip()
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def add_filter_chip(self, filter_type: str, value: str) -> None:
        """Adiciona chip de filtro empilhável."""
        if not any(f["type"] == filter_type and f["value"] == value for f in self.active_filters):
            self.active_filters.append({"type": filter_type, "value": value})
            self.current_page = 1
            self._invalidate_cache()
            if self.on_display_update:
                self.on_display_update()
    
    def remove_filter_chip(self, filt: dict) -> None:
        """Remove chip de filtro."""
        if filt in self.active_filters:
            self.active_filters.remove(filt)
            self.current_page = 1
            self._invalidate_cache()
            if self.on_display_update:
                self.on_display_update()
    
    def clear_all_filters(self) -> None:
        """Limpa todos os filtros."""
        self.current_filter = "all"
        self.current_origin = None
        self.current_categories.clear()
        self.current_tag = None
        self.current_collection = None
        self.search_query = ""
        self.active_filters.clear()
        self.current_page = 1
        self._invalidate_cache()
        if self.on_display_update:
            self.on_display_update()
    
    def get_filtered_projects(self) -> List[str]:
        """
        Retorna lista de paths filtrados (com cache).
        
        Returns:
            Lista de paths que passam por todos os filtros ativos
        """
        # Gerar cache key
        cache_key = (
            self.current_filter,
            self.current_origin,
            tuple(sorted(self.current_categories)),
            self.current_tag,
            self.current_collection,
            self.search_query,
            tuple((f["type"], f["value"]) for f in self.active_filters),
        )
        
        # Verificar cache
        if self._cache_enabled and cache_key in self._filter_cache:
            return self._filter_cache[cache_key]
        
        # Aplicar filtros
        filtered_paths = []
        for path, data in self.database.items():
            if self._passes_all_filters(path, data):
                filtered_paths.append(path)
        
        # Guardar no cache
        if self._cache_enabled:
            self._filter_cache[cache_key] = filtered_paths
        
        return filtered_paths
    
    def _passes_all_filters(self, path: str, data: dict) -> bool:
        """
        Verifica se um projeto passa por todos os filtros ativos.
        """
        # Filtro principal
        if self.current_filter == "favorites" and not data.get("favorite"):
            return False
        elif self.current_filter == "done" and not data.get("done"):
            return False
        elif self.current_filter == "good" and not data.get("good"):
            return False
        elif self.current_filter == "bad" and not data.get("bad"):
            return False
        
        # Filtro de origem
        if self.current_origin:
            origin = data.get("origin", "")
            if origin != self.current_origin:
                return False
        
        # Filtro de categorias
        if self.current_categories:
            project_cat = data.get("category", "")
            if project_cat not in self.current_categories:
                return False
        
        # Filtro de tag
        if self.current_tag:
            project_tags = data.get("tags", [])
            if self.current_tag not in project_tags:
                return False
        
        # Filtro de coleção
        if self.current_collection and self.collections_manager:
            collection_paths = self.collections_manager.get_collection_projects(self.current_collection)
            if path not in collection_paths:
                return False
        
        # Busca textual
        if self.search_query:
            name = data.get("name", "").lower()
            if self.search_query not in name:
                return False
        
        # Filtros de chips adicionais
        for filt in self.active_filters:
            filt_type = filt["type"]
            filt_value = filt["value"]
            
            if filt_type == "category":
                if data.get("category") != filt_value:
                    return False
            elif filt_type == "tag":
                if filt_value not in data.get("tags", []):
                    return False
            elif filt_type == "origin":
                if data.get("origin") != filt_value:
                    return False
            elif filt_type == "collection" and self.collections_manager:
                collection_paths = self.collections_manager.get_collection_projects(filt_value)
                if path not in collection_paths:
                    return False
        
        return True
    
    def get_display_state(self) -> dict:
        """Retorna estado atual do display para detecção de mudanças."""
        return {
            "filter": self.current_filter,
            "origin": self.current_origin,
            "categories": tuple(sorted(self.current_categories)),
            "tag": self.current_tag,
            "collection": self.current_collection,
            "search": self.search_query,
            "active_filters": tuple((f["type"], f["value"]) for f in self.active_filters),
            "sort": self.current_sort,
            "page": self.current_page,
        }
    
    # ═══════════════════════════════════════════════════════════════
    # ORDENAÇÃO
    # ═══════════════════════════════════════════════════════════════
    
    def set_sort(self, sort_type: str) -> None:
        """Define tipo de ordenação."""
        self.current_sort = sort_type
        if self.on_display_update:
            self.on_display_update()
    
    def apply_sorting(self, projects: List[Tuple[str, dict]]) -> List[Tuple[str, dict]]:
        """
        Ordena lista de projetos.
        """
        if self.current_sort == "name":
            return sorted(projects, key=lambda x: x[1].get("name", "").lower())
        elif self.current_sort == "date":
            return sorted(projects, key=lambda x: x[1].get("created_at", ""), reverse=True)
        elif self.current_sort == "type":
            return sorted(projects, key=lambda x: x[1].get("category", ""))
        else:
            return projects
    
    # ═══════════════════════════════════════════════════════════════
    # PAGINAÇÃO
    # ═══════════════════════════════════════════════════════════════
    
    def next_page(self) -> None:
        """Avança para próxima página."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            if self.on_display_update:
                self.on_display_update()
    
    def prev_page(self) -> None:
        """Volta para página anterior."""
        if self.current_page > 1:
            self.current_page -= 1
            if self.on_display_update:
                self.on_display_update()
    
    def goto_page(self, page: int) -> None:
        """Vai para página específica."""
        if 1 <= page <= self.total_pages:
            self.current_page = page
            if self.on_display_update:
                self.on_display_update()
    
    def get_page_info(self, total_items: int) -> dict:
        """
        Calcula informações de paginação.
        """
        self.total_pages = max(1, (total_items + self.items_per_page - 1) // self.items_per_page)
        
        # Ajustar current_page se necessário
        if self.current_page > self.total_pages:
            self.current_page = self.total_pages
        
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, total_items)
        
        return {
            "start_idx": start_idx,
            "end_idx": end_idx,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
        }
    
    # ═══════════════════════════════════════════════════════════════
    # CACHE
    # ═══════════════════════════════════════════════════════════════
    
    def _invalidate_cache(self) -> None:
        """Invalida cache de filtros."""
        self._filter_cache.clear()
    
    def invalidate_cache(self) -> None:
        """
        Invalida cache (chamar ao modificar dados).
        
        IMPORTANTE: Chamar ao:
        - Adicionar/remover projeto
        - Toggle favorite/done/good/bad
        - Modificar categorias/tags
        """
        self._invalidate_cache()
        self.logger.debug("🗑️ Cache invalidado")
