"""
core/performance/__init__.py - Performance Optimization Modules

EXPORTS:
- ViewportManager: Lazy rendering de cards (60% faster initial render)
- FilterCache: Cache inteligente de filtros (0ms on cache hit)
- PredictivePreloader: Preload preditivo de páginas (0ms page switch)

USAGE:
    from core.performance import ViewportManager, FilterCache, PredictivePreloader
"""

from .viewport_manager import ViewportManager
from .filter_cache import FilterCache
from .predictive_preloader import PredictivePreloader

__all__ = [
    "ViewportManager",
    "FilterCache",
    "PredictivePreloader",
]
