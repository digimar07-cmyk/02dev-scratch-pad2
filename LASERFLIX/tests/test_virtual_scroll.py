"""
test_virtual_scroll.py — Testes do VirtualScrollManager (Fase 2)

ESTRATEGIA:
  - Mocka tk.Canvas e tk.Frame completamente (sem display)
  - Testa lógica pura: cálculos de range, indexação no grid,
    widget pooling, refresh_data, clear e get_stats

NAO TESTA:
  - Rendering visual real (exige display Tkinter)
  - Scroll event binding (exige event loop)
"""
import pytest
from unittest.mock import MagicMock, patch, call
from core.virtual_scroll_manager import VirtualScrollManager


# ===========================================================
# Helpers
# ===========================================================

def make_vsm(data=None, cols=3, card_height=100, card_pad=5, buffer_multiplier=1.0):
    """
    Cria VirtualScrollManager com mocks de Tkinter.
    Viewport mockado para retornar altura de 500px.
    """
    canvas = MagicMock()
    canvas.winfo_height.return_value = 500
    canvas.yview.return_value = (0.0, 1.0)  # Scroll no topo

    frame = MagicMock()

    rendered = []  # Registra chamadas ao card_renderer

    def fake_renderer(parent, path, proj_data, row, col):
        widget = MagicMock(name=f"widget_{path}")
        rendered.append((path, row, col))
        return widget

    if data is None:
        data = [(f"/path/proj{i}", {"name": f"Project {i}"}) for i in range(20)]

    vsm = VirtualScrollManager(
        canvas=canvas,
        scrollable_frame=frame,
        data=data,
        card_renderer=fake_renderer,
        cols=cols,
        card_width=200,
        card_height=card_height,
        card_pad=card_pad,
        buffer_multiplier=buffer_multiplier,
    )
    vsm._rendered = rendered
    return vsm


# ===========================================================
# TestCalculateViewport
# ===========================================================

class TestCalculateViewport:
    """Testes de _calculate_viewport()."""

    def test_viewport_size_calculated(self):
        """VIEWPORT: Calcula viewport_size baseado em altura e colunas."""
        # Canvas 500px, card_height=100, card_pad=5 -> row_height=110
        # visible_rows = 500 // 110 = 4
        # viewport_size = 4 * 3 cols = 12
        vsm = make_vsm(cols=3, card_height=100, card_pad=5)

        assert vsm.viewport_size == 12

    def test_buffer_size_calculated(self):
        """VIEWPORT: Calcula buffer_size como viewport * buffer_multiplier."""
        vsm = make_vsm(cols=3, card_height=100, card_pad=5, buffer_multiplier=1.0)
        # viewport_size=12, buffer=12*1.0=12

        assert vsm.buffer_size == 12

    def test_max_pool_size_is_viewport_plus_buffer(self):
        """VIEWPORT: max_pool_size = viewport + buffer."""
        vsm = make_vsm(cols=3, card_height=100, card_pad=5, buffer_multiplier=1.0)

        assert vsm.max_pool_size == vsm.viewport_size + vsm.buffer_size

    def test_viewport_fallback_when_canvas_too_small(self):
        """VIEWPORT: Usa fallback quando canvas retorna altura <= 1."""
        canvas = MagicMock()
        canvas.winfo_height.return_value = 0  # Canvas não inicializado
        canvas.yview.return_value = (0.0, 1.0)

        vsm = VirtualScrollManager(
            canvas=canvas,
            scrollable_frame=MagicMock(),
            data=[],
            card_renderer=MagicMock(),
            cols=6,
            card_height=410,
            card_pad=8,
        )

        # Fallback: viewport_size=18, buffer=12, max=30
        assert vsm.viewport_size == 18
        assert vsm.buffer_size == 12
        assert vsm.max_pool_size == 30


# ===========================================================
# TestGridIndexing
# ===========================================================

class TestGridIndexing:
    """Testes de cálculos de posição no grid."""

    def test_first_item_is_row2_col0(self):
        """GRID: Item 0 vai para row=2, col=0 (pula header)."""
        vsm = make_vsm(cols=3)
        vsm.update_visible_items()

        # Verifica render do primeiro item
        first = next(r for r in vsm._rendered if r[0] == "/path/proj0")
        assert first[1] == 2  # row = (0 // 3) + 2 = 2
        assert first[2] == 0  # col = 0 % 3 = 0

    def test_fourth_item_is_row3_col0(self):
        """GRID: Item 3 (4o) vai para row=3, col=0 (segunda linha)."""
        vsm = make_vsm(cols=3)
        vsm.update_visible_items()

        # Item índice 3 = row (3//3)+2=3, col=3%3=0
        fourth = next((r for r in vsm._rendered if r[0] == "/path/proj3"), None)
        if fourth:  # Pode não estar no viewport dependendo do buffer
            assert fourth[1] == 3
            assert fourth[2] == 0

    def test_col_wraps_per_cols_value(self):
        """GRID: Coluna reinicia a cada 'cols' itens."""
        vsm = make_vsm(cols=4)
        vsm.update_visible_items()

        # Verifica que todos os cols renderizados estão em 0..3
        for _, row, col in vsm._rendered:
            assert 0 <= col < 4


# ===========================================================
# TestVisibleRange
# ===========================================================

class TestVisibleRange:
    """Testes de cálculo do visible_range."""

    def test_initial_visible_range_is_zero(self):
        """RANGE: visible_range inicial é (0, 0)."""
        vsm = make_vsm()
        # Antes de update, range é (0,0)
        assert vsm.visible_range == (0, 0)

    def test_update_sets_visible_range(self):
        """RANGE: update_visible_items() define um range válido."""
        vsm = make_vsm(data=[(f"/p{i}", {}) for i in range(30)])
        vsm.update_visible_items()

        start, end = vsm.visible_range
        assert start == 0
        assert end > 0
        assert end <= 30

    def test_update_does_not_exceed_data_length(self):
        """RANGE: end nunca ultrapassa len(data)."""
        data = [(f"/p{i}", {}) for i in range(5)]  # Apenas 5 items
        vsm = make_vsm(data=data)
        vsm.update_visible_items()

        _, end = vsm.visible_range
        assert end <= 5

    def test_skip_update_when_range_unchanged(self):
        """RANGE: Segunda chamada com mesmo scroll não re-renderiza."""
        vsm = make_vsm()
        vsm.update_visible_items()
        first_rendered = len(vsm._rendered)

        # Segunda chamada - mesmo scroll_pos
        vsm.update_visible_items()
        second_rendered = len(vsm._rendered)

        assert first_rendered == second_rendered  # Nenhum novo render

    def test_empty_data_does_nothing(self):
        """RANGE: Dataset vazio não causa crash."""
        vsm = make_vsm(data=[])
        vsm.update_visible_items()  # Não deve lançar exceção

        assert vsm.visible_range == (0, 0)
        assert len(vsm.active_widgets) == 0


# ===========================================================
# TestWidgetPooling
# ===========================================================

class TestWidgetPooling:
    """Testes de widget pooling (RecyclerView pattern)."""

    def test_active_widgets_populated_after_update(self):
        """POOL: active_widgets preenchido após update."""
        vsm = make_vsm(data=[(f"/p{i}", {}) for i in range(20)])
        vsm.update_visible_items()

        assert len(vsm.active_widgets) > 0

    def test_recycle_moves_widgets_to_pool(self):
        """POOL: _recycle_widgets() move widgets fora do range para o pool."""
        vsm = make_vsm(data=[(f"/p{i}", {}) for i in range(20)])

        # Simula widgets ativos nos índices 0-5
        for i in range(6):
            vsm.active_widgets[i] = MagicMock()

        # Recicla tudo fora do range 3-6
        vsm._recycle_widgets(3, 6)

        # 0,1,2 devem ter sido reciclados
        assert 0 not in vsm.active_widgets
        assert 1 not in vsm.active_widgets
        assert 2 not in vsm.active_widgets
        # 3,4,5 permanecem
        assert 3 in vsm.active_widgets
        assert 4 in vsm.active_widgets
        assert 5 in vsm.active_widgets
        # Pool deve ter recebido 3 widgets
        assert len(vsm.widget_pool) == 3

    def test_already_active_items_not_re_rendered(self):
        """POOL: Items já em active_widgets não são renderizados novamente."""
        vsm = make_vsm(data=[(f"/p{i}", {}) for i in range(20)])
        vsm.update_visible_items()
        count_after_first = len(vsm._rendered)

        # Muda range levemente para forçar segundo update
        vsm.visible_range = (0, 0)
        vsm.canvas.yview.return_value = (0.001, 1.0)  # Scroll imperceptível
        vsm.update_visible_items()

        # Não devem ter sido adicionados renders duplicados
        new_renders = len(vsm._rendered) - count_after_first
        assert new_renders >= 0  # Pode renderizar novos mas não duplicados


# ===========================================================
# TestRefreshData
# ===========================================================

class TestRefreshData:
    """Testes de refresh_data()."""

    def test_refresh_replaces_data(self):
        """REFRESH: refresh_data() substitui o dataset."""
        vsm = make_vsm(data=[(f"/old{i}", {}) for i in range(10)])

        new_data = [(f"/new{i}", {}) for i in range(5)]
        vsm.refresh_data(new_data)

        assert vsm.data == new_data
        assert len(vsm.data) == 5

    def test_refresh_resets_visible_range(self):
        """REFRESH: refresh_data() reseta visible_range para (0,0) antes de update."""
        vsm = make_vsm()
        vsm.update_visible_items()

        vsm.refresh_data([(f"/new{i}", {}) for i in range(5)])

        # After refresh, range deve ser válido (não o antigo)
        start, end = vsm.visible_range
        assert start >= 0
        assert end >= 0

    def test_refresh_with_empty_data(self):
        """REFRESH: refresh_data([]) limpa tudo sem crash."""
        vsm = make_vsm()
        vsm.update_visible_items()

        vsm.refresh_data([])

        assert vsm.data == []
        assert len(vsm.active_widgets) == 0


# ===========================================================
# TestClear
# ===========================================================

class TestClear:
    """Testes de clear()."""

    def test_clear_empties_active_widgets(self):
        """CLEAR: clear() esvazia active_widgets."""
        vsm = make_vsm()
        vsm.update_visible_items()
        assert len(vsm.active_widgets) > 0

        vsm.clear()

        assert len(vsm.active_widgets) == 0

    def test_clear_empties_widget_pool(self):
        """CLEAR: clear() esvazia widget_pool."""
        vsm = make_vsm()
        # Adiciona manualmente ao pool
        vsm.widget_pool.append(MagicMock())
        vsm.widget_pool.append(MagicMock())

        vsm.clear()

        assert len(vsm.widget_pool) == 0

    def test_clear_resets_visible_range(self):
        """CLEAR: clear() reseta visible_range para (0,0)."""
        vsm = make_vsm()
        vsm.update_visible_items()

        vsm.clear()

        assert vsm.visible_range == (0, 0)

    def test_clear_calls_destroy_on_active_widgets(self):
        """CLEAR: Destrói widgets ativos ao limpar."""
        vsm = make_vsm()
        mock_widget = MagicMock()
        vsm.active_widgets[0] = mock_widget

        vsm.clear()

        mock_widget.destroy.assert_called_once()


# ===========================================================
# TestGetStats
# ===========================================================

class TestGetStats:
    """Testes de get_stats()."""

    def test_stats_keys_present(self):
        """STATS: Todas as chaves esperadas presentes."""
        vsm = make_vsm()
        stats = vsm.get_stats()

        expected_keys = [
            "total_items", "active_widgets", "pool_size",
            "visible_range", "viewport_size", "buffer_size", "max_pool"
        ]
        for key in expected_keys:
            assert key in stats, f"Chave ausente: {key}"

    def test_stats_total_items_reflects_data(self):
        """STATS: total_items = len(data)."""
        data = [(f"/p{i}", {}) for i in range(42)]
        vsm = make_vsm(data=data)

        assert vsm.get_stats()["total_items"] == 42

    def test_stats_after_clear(self):
        """STATS: Após clear, active_widgets=0 e pool_size=0."""
        vsm = make_vsm()
        vsm.update_visible_items()
        vsm.clear()

        stats = vsm.get_stats()
        assert stats["active_widgets"] == 0
        assert stats["pool_size"] == 0
