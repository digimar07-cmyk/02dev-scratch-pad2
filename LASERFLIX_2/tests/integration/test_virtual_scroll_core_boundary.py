"""
tests/integration/test_virtual_scroll_core_boundary.py

Testa a fronteira arquitetural e a logica pura do VirtualScrollManager.
Dois tipos:
  1. Arquitetural (AST): garante ausencia de tkinter/ui em core/
  2. Comportamental: logica de indexacao, stats e reciclagem sem Tkinter

Metodologia Akita: usa canvas fake (duck typing) para testar calculo
de viewport e reciclagem sem instanciar nenhum widget real.
"""
import ast
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


# ── Teste Arquitetural ────────────────────────────────────────────────────────

def test_virtual_scroll_manager_architecture():
    """core/virtual_scroll_manager.py NAO pode importar tkinter nem ui/."""
    vsm = ROOT / "core" / "virtual_scroll_manager.py"
    content = vsm.read_text(encoding="utf-8")
    tree = ast.parse(content)

    tk_imports = []
    ui_imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                if "tkinter" in a.name or "customtkinter" in a.name:
                    tk_imports.append(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                if "tkinter" in node.module:
                    tk_imports.append(node.module)
                if node.module.startswith("ui"):
                    ui_imports.append(node.module)

    violations = []
    if tk_imports:
        violations.append(f"Importa tkinter: {tk_imports}")
    if ui_imports:
        violations.append(f"Importa ui/: {ui_imports}")

    assert not violations, (
        "core/virtual_scroll_manager.py VIOLA FRONTEIRA ARQUITETURAL:\n"
        + "\n".join(violations)
    )


# ── Canvas/Frame Fakes (duck typing) ───────────────────────────────────────

class FakeCanvas:
    """Duck type de Canvas para testar VirtualScrollManager sem Tkinter."""
    def __init__(self, height=1080):
        self._height = height
        self._bindings = {}

    def winfo_height(self):
        return self._height

    def yview(self):
        return (0.0, 1.0)

    def yview_moveto(self, pos):
        pass

    def bind(self, event, callback):
        self._bindings[event] = callback


class FakeFrame:
    """Duck type de Frame para testar VirtualScrollManager sem Tkinter."""
    pass


class FakeWidget:
    """Duck type de widget filho para testar reciclagem."""
    def __init__(self):
        self._grid_forgotten = False
        self._destroyed = False

    def grid_forget(self):
        self._grid_forgotten = True

    def grid(self, row, column, padx=0, pady=0, sticky=""):
        self._grid_forgotten = False

    def destroy(self):
        self._destroyed = True


def make_renderer():
    """Retorna um card_renderer fake que cria FakeWidgets."""
    widgets_created = []
    def renderer(frame, path, data, row, col):
        w = FakeWidget()
        widgets_created.append(w)
        return w
    renderer.widgets_created = widgets_created
    return renderer


# ── Testes Comportamentais ─────────────────────────────────────────────────────

class TestViewportCalculo:

    def test_viewport_calculado_na_inicializacao(self):
        """viewport_size e buffer_size devem ser calculados no __init__."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(height=1080),
            scrollable_frame=FakeFrame(),
            data=[],
            card_renderer=make_renderer(),
        )
        assert vsm.viewport_size > 0
        assert vsm.buffer_size > 0
        assert vsm.max_pool_size > 0

    def test_viewport_menor_em_canvas_menor(self):
        """Canvas com altura menor deve resultar em viewport_size menor."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm_grande = VirtualScrollManager(
            canvas=FakeCanvas(height=2160),
            scrollable_frame=FakeFrame(),
            data=[],
            card_renderer=make_renderer(),
        )
        vsm_pequeno = VirtualScrollManager(
            canvas=FakeCanvas(height=540),
            scrollable_frame=FakeFrame(),
            data=[],
            card_renderer=make_renderer(),
        )
        assert vsm_grande.viewport_size > vsm_pequeno.viewport_size

    def test_canvas_altura_zero_usa_fallback(self):
        """Canvas com altura 0 ou 1 deve usar fallback sem explodir."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(height=0),
            scrollable_frame=FakeFrame(),
            data=[],
            card_renderer=make_renderer(),
        )
        assert vsm.viewport_size > 0


class TestStatsEEstado:

    def test_get_stats_estrutura(self):
        """get_stats deve retornar dict com chaves obrigatorias."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(),
            scrollable_frame=FakeFrame(),
            data=[(f"/p/{i}", {}) for i in range(10)],
            card_renderer=make_renderer(),
        )
        stats = vsm.get_stats()
        for key in ["total_items", "active_widgets", "pool_size", "visible_range",
                    "viewport_size", "buffer_size", "max_pool"]:
            assert key in stats

    def test_get_stats_total_items(self):
        """get_stats.total_items deve refletir len(data) exato."""
        from core.virtual_scroll_manager import VirtualScrollManager
        data = [(f"/p/{i}", {}) for i in range(25)]
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(),
            scrollable_frame=FakeFrame(),
            data=data,
            card_renderer=make_renderer(),
        )
        assert vsm.get_stats()["total_items"] == 25

    def test_clear_zera_widgets_ativos(self):
        """clear() deve zerar active_widgets e widget_pool."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(),
            scrollable_frame=FakeFrame(),
            data=[(f"/p/{i}", {}) for i in range(5)],
            card_renderer=make_renderer(),
        )
        # Insere widget fake manualmente
        vsm.active_widgets[0] = FakeWidget()
        vsm.widget_pool.append(FakeWidget())
        vsm.clear()
        assert len(vsm.active_widgets) == 0
        assert len(vsm.widget_pool) == 0

    def test_refresh_data_substitui_dataset(self):
        """refresh_data deve substituir self.data pelo novo dataset."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(),
            scrollable_frame=FakeFrame(),
            data=[(f"/a/{i}", {}) for i in range(5)],
            card_renderer=make_renderer(),
        )
        novo_data = [(f"/b/{i}", {}) for i in range(12)]
        vsm.refresh_data(novo_data)
        assert vsm.get_stats()["total_items"] == 12


class TestReciclagem:

    def test_recycle_widgets_move_para_pool(self):
        """_recycle_widgets deve mover widgets fora da range para widget_pool."""
        from core.virtual_scroll_manager import VirtualScrollManager
        vsm = VirtualScrollManager(
            canvas=FakeCanvas(),
            scrollable_frame=FakeFrame(),
            data=[],
            card_renderer=make_renderer(),
        )
        # Insere 5 widgets como ativos nos indices 0-4
        for i in range(5):
            vsm.active_widgets[i] = FakeWidget()

        # Recicla: apenas indices 2-4 ficam visiveis
        vsm._recycle_widgets(start_idx=2, end_idx=5)

        # Indices 0 e 1 devem ter ido para o pool
        assert len(vsm.widget_pool) == 2
        assert 0 not in vsm.active_widgets
        assert 1 not in vsm.active_widgets
        assert 2 in vsm.active_widgets
