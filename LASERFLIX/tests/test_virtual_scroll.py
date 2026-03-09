"""
test_virtual_scroll.py — Testes do VirtualScrollManager

Cobre:
  - Cálculo de visible range
  - Batch rendering
  - Memory management
  - Performance de scroll
"""
import pytest
from core.virtual_scroll_manager import VirtualScrollManager


@pytest.fixture
def scroll_manager():
    """VirtualScrollManager configurado para testes."""
    return VirtualScrollManager(
        viewport_height=600,
        item_height=150,
        buffer_size=5
    )


class TestVisibleRangeCalculation:
    """Testes de cálculo do range visível."""
    
    def test_calculate_visible_range(self, scroll_manager):
        """SMOKE: Calcular range de itens visíveis."""
        total_items = 100
        scroll_position = 0
        
        start, end = scroll_manager.calculate_visible_range(total_items, scroll_position)
        
        assert start >= 0
        assert end <= total_items
        assert end > start
    
    def test_visible_range_at_start(self, scroll_manager):
        """EDGE: Range no início da lista."""
        total_items = 100
        scroll_position = 0
        
        start, end = scroll_manager.calculate_visible_range(total_items, scroll_position)
        
        assert start == 0
    
    def test_visible_range_at_end(self, scroll_manager):
        """EDGE: Range no final da lista."""
        total_items = 100
        scroll_position = 10000  # Muito além do fim
        
        start, end = scroll_manager.calculate_visible_range(total_items, scroll_position)
        
        assert end == total_items
    
    def test_buffer_zone(self, scroll_manager):
        """BUFFER: Range deve incluir buffer para scroll suave."""
        total_items = 100
        scroll_position = 600  # Middle
        
        start, end = scroll_manager.calculate_visible_range(total_items, scroll_position)
        
        # Range deve ser maior que apenas visíveis (inclui buffer)
        visible_count = scroll_manager.viewport_height // scroll_manager.item_height
        assert (end - start) > visible_count


class TestBatchRendering:
    """Testes de renderização em batch."""
    
    def test_render_batch(self, scroll_manager):
        """SMOKE: Renderizar batch de itens."""
        items = [f"item_{i}" for i in range(100)]
        visible_range = (0, 10)
        
        batch = scroll_manager.get_batch(items, visible_range)
        
        assert len(batch) == 10
        assert batch[0] == "item_0"
        assert batch[-1] == "item_9"
    
    def test_batch_size_limit(self, scroll_manager):
        """PERFORMANCE: Batch não deve exceder tamanho máximo."""
        items = [f"item_{i}" for i in range(100)]
        visible_range = (0, 50)  # Solicitar 50 itens
        
        batch = scroll_manager.get_batch(items, visible_range, max_batch_size=20)
        
        # Deve limitar a 20
        assert len(batch) <= 20


class TestMemoryManagement:
    """Testes de gestão de memória."""
    
    def test_cleanup_offscreen_items(self, scroll_manager):
        """MEMORY: Limpar itens fora da tela."""
        rendered_items = {i: f"widget_{i}" for i in range(50)}
        visible_range = (10, 20)
        
        # Items fora do range devem ser marcados para limpeza
        to_cleanup = scroll_manager.get_items_to_cleanup(rendered_items, visible_range)
        
        assert 0 in to_cleanup  # Item 0 está fora do range
        assert 10 not in to_cleanup  # Item 10 está visível
        assert 49 in to_cleanup  # Item 49 está fora do range
    
    def test_memory_limit(self, scroll_manager):
        """MEMORY: Não deve manter mais que X itens na memória."""
        max_cached_items = 30
        rendered_items = {i: f"widget_{i}" for i in range(100)}
        
        # Aplicar limite
        to_keep = scroll_manager.apply_memory_limit(rendered_items, max_cached_items)
        
        assert len(to_keep) <= max_cached_items
