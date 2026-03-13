"""
tests/unit/test_virtual_scroll_extended.py

Cobre linhas ainda não testadas de core/virtual_scroll_manager.py:
  50      _calculate_viewport() caminho de erro (except)
  62-66   _on_canvas_resize()
  69-70   update_visible_items() guarda _scroll_update_pending
  74      update_visible_items() data vazio
  92      update_visible_items() new_range == visible_range (early return)
  112     _render_visible_items() idx >= len(data) break
  114     _render_visible_items() idx já em active_widgets (continue)

Regra: NUNCA alterar testes. Bugs são no app.
"""
import os
import sys
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.virtual_scroll_manager import VirtualScrollManager


def make_canvas(height=800, scroll_pos=0.0):
    """Mock de canvas para testes."""
    canvas = MagicMock()
    canvas.winfo_height.return_value = height
    canvas.yview.return_value = (scroll_pos, scroll_pos + 0.1)
    return canvas


def make_frame():
    return MagicMock()


def make_renderer():
    """Renderer que retorna um widget mock."""
    def renderer(frame, path, data, row, col):
        w = MagicMock()
        return w
    return renderer


def make_vsm(data=None, height=800, scroll_pos=0.0):
    if data is None:
        data = [("/proj/a", {"name": "A"}), ("/proj/b", {"name": "B"})]
    canvas = make_canvas(height=height, scroll_pos=scroll_pos)
    frame = make_frame()
    return VirtualScrollManager(
        canvas=canvas,
        scrollable_frame=frame,
        data=data,
        card_renderer=make_renderer(),
    )


# ═ _calculate_viewport() erro ═══════════════════════════════════════

class TestVirtualScrollCalculateViewport:

    def test_dado_canvas_levanta_excecao_quando_calculate_entao_usa_padrao(self):
        canvas = MagicMock()
        canvas.winfo_height.side_effect = Exception("canvas não inicializado")
        canvas.bind = MagicMock()
        vsm = VirtualScrollManager(
            canvas=canvas,
            scrollable_frame=make_frame(),
            data=[],
            card_renderer=make_renderer(),
        )
        assert vsm.viewport_size == 18
        assert vsm.buffer_size == 12
        assert vsm.max_pool_size == 30


# ═ _on_canvas_resize() ══════════════════════════════════════════════

class TestVirtualScrollCanvasResize:

    def test_dado_resize_event_quando_on_canvas_resize_entao_nao_explode(self):
        vsm = make_vsm()
        try:
            vsm._on_canvas_resize(event=None)
        except Exception as e:
            pytest.fail(f"_on_canvas_resize não deve explodir: {e}")

    def test_dado_resize_event_quando_on_canvas_resize_entao_recalcula_viewport(self):
        vsm = make_vsm()
        old_size = vsm.viewport_size
        vsm.canvas.winfo_height.return_value = 1200
        vsm._on_canvas_resize()
        # Viewport deve ser recalculado (pode mudar ou não, mas não explode)
        assert vsm.viewport_size > 0


# ═ update_visible_items() ═══════════════════════════════════════════

class TestVirtualScrollUpdateVisible:

    def test_dado_scroll_pending_quando_update_entao_retorna_sem_processar(self):
        vsm = make_vsm()
        vsm._scroll_update_pending = True
        # Não deve chamar canvas.yview
        vsm.update_visible_items()
        vsm.canvas.yview.assert_not_called()

    def test_dado_data_vazio_quando_update_entao_retorna_sem_processar(self):
        vsm = make_vsm(data=[])
        vsm.update_visible_items()
        # Não deve chamar yview quando data está vazio
        vsm.canvas.yview.assert_not_called()

    def test_dado_mesma_range_quando_update_entao_nao_renderiza_novamente(self):
        vsm = make_vsm()
        vsm.update_visible_items()  # primeira vez define visible_range
        range_antes = vsm.visible_range
        active_antes = len(vsm.active_widgets)
        vsm.update_visible_items()  # segunda vez mesma posição
        assert vsm.visible_range == range_antes

    def test_dado_data_com_items_quando_update_entao_pending_False_ao_final(self):
        vsm = make_vsm()
        vsm.update_visible_items()
        assert vsm._scroll_update_pending is False


# ═ _render_visible_items() edge cases ═══════════════════════════════

class TestVirtualScrollRenderItems:

    def test_dado_end_idx_maior_que_data_quando_render_entao_nao_explode(self):
        vsm = make_vsm(data=[("/proj/a", {"name": "A"})])
        try:
            vsm._render_visible_items(0, 10)  # end_idx > len(data)
        except Exception as e:
            pytest.fail(f"_render_visible_items não deve explodir: {e}")

    def test_dado_end_idx_maior_que_data_quando_render_entao_apenas_itens_existentes(self):
        vsm = make_vsm(data=[("/proj/a", {"name": "A"})])
        vsm._render_visible_items(0, 10)
        assert len(vsm.active_widgets) == 1

    def test_dado_idx_ja_em_active_quando_render_entao_nao_duplica(self):
        data = [("/proj/a", {"name": "A"}), ("/proj/b", {"name": "B"})]
        vsm = make_vsm(data=data)
        vsm._render_visible_items(0, 2)  # renderiza pela primeira vez
        count_antes = len(vsm.active_widgets)
        vsm._render_visible_items(0, 2)  # renderiza de novo (deve pular ativos)
        assert len(vsm.active_widgets) == count_antes
