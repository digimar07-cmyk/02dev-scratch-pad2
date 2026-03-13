"""
Smoke test do bootstrap da aplicacao.
Testa inicializacao controlada sem abrir janela visivel.
USa Tk() com withdraw() para evitar abertura real.
NAO captura toda excecao para 'passar'.
"""
import sys
import os
import pytest
import inspect

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)


def test_laserflixmainwindow_class_exists():
    """LaserflixMainWindow deve ser importavel e ser uma classe."""
    from ui.main_window import LaserflixMainWindow
    assert isinstance(LaserflixMainWindow, type), (
        "LaserflixMainWindow nao e uma classe. "
        "Possivel problema de definicao ou import circular."
    )


def test_laserflixmainwindow_init_signature():
    """LaserflixMainWindow deve aceitar um argumento root no __init__."""
    from ui.main_window import LaserflixMainWindow
    sig = inspect.signature(LaserflixMainWindow.__init__)
    params = list(sig.parameters.keys())
    assert "root" in params or len(params) >= 2, (
        f"LaserflixMainWindow.__init__ nao tem parametro 'root': {params}\n"
        "main.py chama LaserflixMainWindow(root) \u2014 interface quebrada."
    )


@pytest.mark.timeout(10)
def test_tk_root_creation_does_not_crash():
    """
    Cria um Tk root com withdraw() e verifica que nao crasha.
    Nao testa a aplicacao completa \u2014 apenas que Tk esta funcional.
    """
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()
        assert root.winfo_exists(), "Tk root nao foi criado corretamente"
        root.destroy()
    except Exception as e:
        pytest.fail(f"Criacao de Tk root falhou: {e}")


@pytest.mark.timeout(20)
def test_laserflixmainwindow_instantiation():
    """
    Tenta instanciar LaserflixMainWindow com Tk real (hidden).
    Se falhar, reporta o erro REAL \u2014 sem suprimir.
    Falha aqui = erro REAL de bootstrap da aplicacao.
    """
    import tkinter as tk
    from ui.main_window import LaserflixMainWindow
    root = tk.Tk()
    root.withdraw()
    try:
        app = LaserflixMainWindow(root)
        assert app is not None, "LaserflixMainWindow retornou None"
        assert hasattr(app, '__class__'), "Objeto criado nao tem __class__"
    except Exception as e:
        root.destroy()
        pytest.fail(
            f"LaserflixMainWindow falhou ao instanciar:\n"
            f"{type(e).__name__}: {e}\n"
            "Este e um erro REAL de bootstrap da aplicacao."
        )
    else:
        try:
            root.destroy()
        except Exception:
            pass
