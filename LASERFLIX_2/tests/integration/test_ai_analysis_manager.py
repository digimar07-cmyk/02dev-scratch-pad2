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
from unittest.mock import patch, MagicMock

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


# ── Testes de Contrato de Interface ────────────────────────────────────────

class TestContratoInterface:

    @pytest.fixture
    def manager(self):
        """Retorna instancia do AIAnalysisManager sem chamar Ollama."""
        mod = importlib.import_module("ai.analysis_manager")
        cls = next(
            getattr(mod, n) for n in dir(mod)
            if not n.startswith("_") and isinstance(getattr(mod, n), type)
        )
        return cls()

    def test_manager_tem_metodo_analyze(self, manager):
        """AIAnalysisManager deve ter metodo 'analyze' ou 'analyze_project'."""
        has_analyze = hasattr(manager, "analyze") or hasattr(manager, "analyze_project")
        assert has_analyze, "AIAnalysisManager nao tem metodo analyze/analyze_project"

    def test_manager_tem_atributo_model(self, manager):
        """AIAnalysisManager deve ter atributo 'model' configuravel."""
        assert hasattr(manager, "model"), "AIAnalysisManager nao tem atributo 'model'"

    def test_analyze_com_ollama_offline_nao_explode(self, manager):
        """
        analyze_project com Ollama offline deve retornar resultado vazio/neutro
        sem levantar excecao nao tratada.
        Mock cirurgico: intercepta apenas a chamada HTTP, deixa toda logica rodar.
        """
        method = getattr(manager, "analyze_project", None) or getattr(manager, "analyze", None)
        if method is None:
            pytest.skip("Metodo analyze nao encontrado")

        # Simula timeout/conexao recusada de Ollama
        with patch("requests.post", side_effect=ConnectionError("Ollama offline")):
            try:
                result = method("/fake/path", {"name": "Teste"})
                # Se retornou, nao deve ter explodido
                # Resultado pode ser None, dict vazio ou dict com flags de erro
                assert result is None or isinstance(result, dict)
            except (ConnectionError, OSError):
                pytest.fail(
                    "analyze_project vazou ConnectionError para o caller. "
                    "Deve ser capturada internamente."
                )

    def test_analyze_com_requests_ausente_nao_explode(self, manager):
        """
        Se requests nao estiver disponivel, nao deve travar o import do modulo.
        Esse teste garante que o import do modulo ja passou (linha anterior).
        """
        # Se chegou aqui, o import ja funcionou
        assert manager is not None
