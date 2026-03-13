"""
tests/unit/test_virtual_scroll_manager.py

Testes unitários para core/virtual_scroll_manager.py → VirtualScrollManager.

Metodologia Akita:
- VirtualScrollManager depende de canvas/frame do Tkinter.
- Usamos MagicMock para simular os widgets sem iniciar Tkinter.
- Testamos APENAS a lógica pura (cálculos, reciclagem, stats).
  A renderização real pertence a testes de integração com Tkinter (futuro).
"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.virtual_scroll_manager import VirtualScrollManager


def make_manager(data=None, cols=3):
    """Factory: cria VirtualScrollManager com canvas/frame mockados."""
    canvas = MagicMock()
    canvas.winfo_height.return_value = 1080
    canvas.yview.return_value = (0.0, 1.0)
    frame = MagicMock()
    renderer = MagicMock(return_value=MagicMock())
    if data is None:
        data = []
    return VirtualScrollManager(
        canvas=canvas,
        scrollable_frame=frame,
        data=data,
        card_renderer=renderer,
        cols=cols,
        card_width=280,
        card_height=410,
        card_pad=8,
    )


class TestVirtualScrollManagerStats:

    def test_dado_data_vazia_quando_get_stats_entao_total_items_zero(self):
        vsm = make_manager(data=[])
        assert vsm.get_stats()["total_items"] == 0

    def test_dado_data_com_itens_quando_get_stats_entao_total_items_correto(self):
        data = [(f"/proj/{i}", {}) for i in range(10)]
        vsm = make_manager(data=data)
        assert vsm.get_stats()["total_items"] == 10

    def test_dado_manager_criado_quando_get_stats_entao_contem_chaves_obrigatorias(self):
        vsm = make_manager()
        stats = vsm.get_stats()
        for key in ["total_items", "active_widgets", "pool_size", "visible_range",
                    "viewport_size", "buffer_size", "max_pool"]:
            assert key in stats, f"Chave ausente: {key}"


class TestVirtualScrollManagerClear:

    def test_dado_manager_com_widgets_quando_clear_entao_active_widgets_zero(self):
        vsm = make_manager()
        # Injeta widgets fictícios
        vsm.active_widgets = {0: MagicMock(), 1: MagicMock()}
        vsm.clear()
        assert len(vsm.active_widgets) == 0

    def test_dado_manager_com_pool_quando_clear_entao_pool_vazio(self):
        vsm = make_manager()
        vsm.widget_pool = [MagicMock(), MagicMock()]
        vsm.clear()
        assert len(vsm.widget_pool) == 0

    def test_dado_manager_limpo_quando_clear_entao_visible_range_zero(self):
        vsm = make_manager()
        vsm.clear()
        assert vsm.visible_range == (0, 0)


class TestVirtualScrollManagerRefreshData:

    def test_dado_novos_dados_quando_refresh_data_entao_data_atualizado(self):
        vsm = make_manager(data=[])
        new_data = [("/proj/a", {}), ("/proj/b", {})]
        vsm.refresh_data(new_data)
        assert vsm.get_stats()["total_items"] == 2

    def test_dado_refresh_quando_visible_range_resetado(self):
        vsm = make_manager(data=[])
        vsm.visible_range = (5, 10)  # estado sujo
        vsm.refresh_data([])
        assert vsm.visible_range == (0, 0)


class TestVirtualScrollManagerRecycle:

    def test_dado_widget_fora_do_range_quando_recycle_entao_move_para_pool(self):
        vsm = make_manager()
        widget_mock = MagicMock()
        vsm.active_widgets[0] = widget_mock  # idx 0 fora do range (5, 10)
        vsm._recycle_widgets(start_idx=5, end_idx=10)
        assert 0 not in vsm.active_widgets
        assert widget_mock in vsm.widget_pool

    def test_dado_widget_dentro_do_range_quando_recycle_entao_permanece_ativo(self):
        vsm = make_manager()
        widget_mock = MagicMock()
        vsm.active_widgets[7] = widget_mock  # idx 7 dentro do range (5, 10)
        vsm._recycle_widgets(start_idx=5, end_idx=10)
        assert 7 in vsm.active_widgets
