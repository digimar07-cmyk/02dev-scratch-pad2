"""
core/performance/filter_cache.py — Cache inteligente de resultados filtrados.

PERFORMANCE OPTIMIZATION 2/3: Smart Filter Cache

INSPIRAÇÃO:
- Redis (in-memory cache)
- Memcached (LRU eviction)
- React Query (stale-while-revalidate)

CONCEITO:
┌──────────────────────────────┐
│ CACHE KEY                       │
│ (filter_type, value, search)   │
├──────────────────────────────┤
│ (“favorites”, True, “”)        │ ← HIT! (0ms)
│ (“done”, True, “”)             │ ← HIT! (0ms)
│ (“category”, “games”, “pixel”) │ ← MISS (compute)
└──────────────────────────────┘

GANHO:
- Antes: 5000 projects × 5ms = 25ms por filtro
- Cache HIT: 0ms (instant!)
- 3 cliques em ⭐: 25ms + 25ms + 25ms = 75ms → 25ms + 0ms + 0ms = 25ms
"""

import time
import threading
from typing import Any, Callable, Optional, Tuple, List
from collections import OrderedDict
from utils.logging_setup import LOGGER


class FilterCache:
    """
    Cache LRU para resultados de filtros.
    
    Features:
    - Cache baseado em (filter_type, filter_value, search_query)
    - LRU eviction (max 50 entradas)
    - TTL expiration (5 minutos)
    - Thread-safe (lock)
    - Auto invalidation (on data change)
    """
    
    def __init__(
        self,
        max_size: int = 50,
        ttl_seconds: int = 300,  # 5 min
    ):
        """
        Args:
            max_size: Máximo de entradas em cache
            ttl_seconds: Tempo de vida do cache (300s = 5min)
        """
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        
        # Cache: {key: (result, timestamp)}
        self.cache = OrderedDict()
        self.lock = threading.Lock()
        
        # Stats
        self.hits = 0
        self.misses = 0
        
        self.logger = LOGGER
        self.logger.debug(
            f"📦 FilterCache: max_size={max_size}, ttl={ttl_seconds}s"
        )
    
    def get_or_compute(
        self,
        key: Tuple[str, Any, str],
        compute_fn: Callable[[], List[Any]],
    ) -> List[Any]:
        """
        Busca no cache ou computa resultado.
        
        Args:
            key: (filter_type, filter_value, search_query)
            compute_fn: Função que computa resultado se cache miss
        
        Returns:
            Lista de resultados filtrados
        
        Example:
            result = cache.get_or_compute(
                key=("favorites", True, ""),
                compute_fn=lambda: db.filter_projects(favorites=True)
            )
        """
        with self.lock:
            # 1. CHECK CACHE
            cached = self.cache.get(key)
            
            if cached:
                result, timestamp = cached
                age = time.time() - timestamp
                
                # Check TTL
                if age < self.ttl_seconds:
                    # CACHE HIT!
                    self.hits += 1
                    self.cache.move_to_end(key)  # LRU: mark as recently used
                    
                    self.logger.debug(
                        f"✅ Cache HIT: {key} (age={age:.1f}s, hits={self.hits})"
                    )
                    return result
                else:
                    # Expired - remove
                    del self.cache[key]
                    self.logger.debug(f"⌛ Expired: {key} (age={age:.1f}s)")
        
        # 2. CACHE MISS - COMPUTE
        self.misses += 1
        result = compute_fn()
        
        with self.lock:
            # 3. STORE IN CACHE
            self.cache[key] = (result, time.time())
            self.cache.move_to_end(key)
            
            # 4. LRU EVICTION
            while len(self.cache) > self.max_size:
                evicted_key, _ = self.cache.popitem(last=False)
                self.logger.debug(f"🗑️ Evicted: {evicted_key}")
            
            self.logger.debug(
                f"❌ Cache MISS: {key} (computed, misses={self.misses})"
            )
        
        return result
    
    def invalidate(self, pattern: Optional[str] = None) -> int:
        """
        Invalida cache (completo ou por padrão).
        
        Args:
            pattern: Se None, limpa tudo. Senão, limpa keys que contêm pattern
        
        Returns:
            Número de entradas removidas
        
        Example:
            cache.invalidate()  # Limpa tudo
            cache.invalidate("favorites")  # Limpa apenas filtros de favoritos
        """
        with self.lock:
            if pattern is None:
                # CLEAR ALL
                count = len(self.cache)
                self.cache.clear()
                self.logger.info(f"🗑️ Cache CLEARED: {count} entries")
                return count
            
            # PARTIAL CLEAR (by pattern)
            keys_to_remove = [
                key for key in self.cache.keys()
                if pattern in str(key)
            ]
            
            for key in keys_to_remove:
                del self.cache[key]
            
            self.logger.info(
                f"🗑️ Cache INVALIDATED: {len(keys_to_remove)} entries "
                f"matching '{pattern}'"
            )
            return len(keys_to_remove)
    
    def invalidate_all(self) -> int:
        """
        Atalho para invalidar tudo.
        """
        return self.invalidate(pattern=None)
    
    def get_stats(self) -> dict:
        """
        Estatísticas do cache.
        """
        with self.lock:
            total_requests = self.hits + self.misses
            hit_rate = (
                (self.hits / total_requests * 100)
                if total_requests > 0 else 0
            )
            
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate_pct": round(hit_rate, 1),
                "cache_size": len(self.cache),
                "max_size": self.max_size,
            }
    
    def reset_stats(self) -> None:
        """
        Reseta contadores de hit/miss.
        """
        self.hits = 0
        self.misses = 0
