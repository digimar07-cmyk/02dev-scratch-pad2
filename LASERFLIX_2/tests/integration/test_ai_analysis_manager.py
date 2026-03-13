"""
tests/integration/test_ai_analysis_manager.py

Testa contratos do ai/analysis_manager.py sem chamar Ollama real.
Dois tipos:
  1. Arquiteturais: isolamento de camada (sem UI, sem tkinter)
  2. Comportamentais: interface publica, contrato de retorno, fallback

Metodologia Akita:
- AI layer eh completamente testavel sem rede
- Testa o contrato de interface, nao a resposta da IA
- Usa mocks CIRURGICOS apenas onde a chamada de rede eh inevitavel
"""
import sys
import ast
import pytest
import importlib
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))


# ── Testes Arquiteturais ──────────────────────────────────────────────────────

class TestArquitetura:

    def test_analysis_manager_importable(self):
        """ai.analysis_manager deve ser importavel sem erros."""
        from ai import analysis_manager
        assert analysis_manager is not None

    def test_analysis_manager_has_public_class(self):
        """ai.analysis_manager deve expor ao menos uma classe publica."""
        mod = importlib.import_module("ai.analysis_manager")
        classes = [
            n for n in dir(mod)
            if not n.startswith("_") and isinstance(getattr(mod, n), type)
        ]
        assert classes, "ai/analysis_manager.py nao expoe classe publica."

    def test_analysis_manager_does_not_import_ui(self):
        """AI layer NAO pode depender de UI."""
        path = ROOT / "ai" / "analysis_manager.py"
        tree = ast.parse(path.read_text(encoding="utf-8"))
        ui_imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith("ui"):
                    ui_imports.append(node.module)
            elif isinstance(node, ast.Import):
                for a in node.names:
                    if a.name.startswith("ui"):
                        ui_imports.append(a.name)
        assert not ui_imports, (
            f"ai/analysis_manager.py importa ui/: {ui_imports}\n"
            "AI layer nao pode depender de UI."
        )

    def test_analysis_manager_does_not_import_tkinter(self):
        """AI layer NAO pode importar tkinter diretamente."""
        path = ROOT / "ai" / "analysis_manager.py"
        content = path.read_text(encoding="utf-8")
        assert "import tkinter" not in content
        assert "from tkinter" not in content
        assert "import customtkinter" not in content


# ── Helpers para dependencias fakes ──────────────────────────────────────────────

def _make_fake_ollama():
    """Cria fake ollama_client com os atributos acessados por AnalysisManager."""
    fake = MagicMock()
    fake.stop_flag = False
    fake.active_models = {"text_quality": "llava:fake", "text_fast": "llava:fast"}
    return fake


def _make_fake_text_generator():
    """Cria fake text_generator que retorna cats/tags vazios sem chamar Ollama."""
    fake = MagicMock()
    fake.analyze_project.return_value = ([], [])
    return fake


def _make_fake_db_manager(tmp_path=None):
    """Cria fake db_manager com save_database como no-op."""
    fake = MagicMock()
    fake.save_database.return_value = None
    return fake


# ── Testes de Contrato de Interface ────────────────────────────────────────

class TestContratoInterface:
    """
    Testa o contrato publico de AnalysisManager.
    Injeta fakes para as 3 dependencias obrigatorias:
      - text_generator: retorna ([], []) sem chamar Ollama
      - db_manager: save_database() e' no-op
      - ollama_client: stop_flag + active_models configurados
    """

    @pytest.fixture
    def manager(self):
        """Instancia AnalysisManager com dependencias fake — sem rede, sem Ollama."""
        from ai.analysis_manager import AnalysisManager
        return AnalysisManager(
            text_generator=_make_fake_text_generator(),
            db_manager=_make_fake_db_manager(),
            ollama_client=_make_fake_ollama(),
        )

    def test_manager_instancia_sem_erros(self, manager):
        """AnalysisManager deve instanciar sem erros com dependencias fakes."""
        assert manager is not None

    def test_manager_tem_metodo_analyze_single(self, manager):
        """AnalysisManager deve ter metodo analyze_single."""
        assert hasattr(manager, "analyze_single"), (
            "AnalysisManager nao tem metodo analyze_single"
        )

    def test_manager_tem_metodo_analyze_batch(self, manager):
        """AnalysisManager deve ter metodo analyze_batch."""
        assert hasattr(manager, "analyze_batch"), (
            "AnalysisManager nao tem metodo analyze_batch"
        )

    def test_manager_tem_metodo_stop(self, manager):
        """AnalysisManager deve ter metodo stop()."""
        assert hasattr(manager, "stop")

    def test_manager_tem_callbacks_de_progresso(self, manager):
        """AnalysisManager deve expor os 4 callbacks de progresso."""
        for cb in ["on_progress", "on_start", "on_complete", "on_error"]:
            assert hasattr(manager, cb), f"Callback ausente: {cb}"

    def test_manager_estado_inicial_nao_analisando(self, manager):
        """Estado inicial deve ser is_analyzing=False e should_stop=False."""
        assert manager.is_analyzing is False
        assert manager.should_stop is False

    def test_stop_quando_idle_nao_explode(self, manager):
        """Chamar stop() quando nao ha analise em andamento nao deve explodir."""
        manager.stop()  # Nao deve levantar excecao
        assert manager.should_stop is True

    def test_get_unanalyzed_projects_vazio(self, manager):
        """get_unanalyzed_projects em database vazio retorna lista vazia."""
        result = manager.get_unanalyzed_projects({})
        assert result == []

    def test_get_all_projects_vazio(self, manager):
        """get_all_projects em database vazio retorna lista vazia."""
        result = manager.get_all_projects({})
        assert result == []

    def test_callbacks_aceitam_injecao(self, manager):
        """Callbacks devem aceitar funcoes injetadas externamente."""
        log = []
        manager.on_progress = lambda done, total, name: log.append((done, total, name))
        manager.on_error = lambda msg: log.append(msg)
        # Nao deve explodir ao atribuir
        assert manager.on_progress is not None
        assert manager.on_error is not None

    def test_analyze_batch_vazio_dispara_on_error(self, manager):
        """
        analyze_batch com lista vazia deve disparar on_error sem explodir.
        Verifica o contrato: nao ha projetos -> on_error e' chamado.
        """
        erros = []
        manager.on_error = lambda msg: erros.append(msg)
        manager.analyze_batch([], {})
        # on_error deve ter sido chamado
        assert len(erros) == 1
        assert "Nenhum projeto" in erros[0] or len(erros[0]) > 0
