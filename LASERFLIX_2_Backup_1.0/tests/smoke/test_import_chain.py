"""
Smoke test da cadeia de imports criticos.
Nao e 'importou sem crash = passou'.
Valida que imports especificos funcionam E retornam os tipos esperados.
"""
import sys
import os
import pytest
import importlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)


def test_import_config_constants():
    from config import constants
    assert hasattr(constants, '__file__'), "constants nao e modulo real"


def test_import_config_settings():
    from config import settings
    assert hasattr(settings, '__file__')


def test_import_utils_logging():
    from utils.logging_setup import LOGGER
    import logging
    assert isinstance(LOGGER, logging.Logger), (
        f"LOGGER nao e Logger. E: {type(LOGGER)}"
    )


def test_import_core_database():
    """core.database deve ser importavel e expor ao menos uma classe publica."""
    mod = importlib.import_module("core.database")
    public_classes = [
        name for name in dir(mod)
        if not name.startswith("_") and isinstance(getattr(mod, name), type)
    ]
    assert public_classes, (
        "core/database.py nao expoe nenhuma classe publica. "
        "Ou esta vazio, ou tudo e privado, ou falhou ao definir classes."
    )


def test_import_core_collections_manager():
    mod = importlib.import_module("core.collections_manager")
    public_classes = [
        name for name in dir(mod)
        if not name.startswith("_") and isinstance(getattr(mod, name), type)
    ]
    assert public_classes, "core/collections_manager.py nao expoe nenhuma classe publica."


def test_import_utils_duplicate_detector():
    mod = importlib.import_module("utils.duplicate_detector")
    assert mod is not None
    public = [n for n in dir(mod) if not n.startswith("_")]
    assert public, "utils/duplicate_detector.py nao expoe nada publico."


def test_import_ai_ollama_client():
    mod = importlib.import_module("ai.ollama_client")
    assert mod is not None
    public = [n for n in dir(mod) if not n.startswith("_")]
    assert public, "ai/ollama_client.py nao expoe nada publico."


def test_import_ai_analysis_manager():
    mod = importlib.import_module("ai.analysis_manager")
    assert mod is not None
    public = [n for n in dir(mod) if not n.startswith("_")]
    assert public, "ai/analysis_manager.py nao expoe nada publico."


def test_main_py_has_guard():
    """
    main.py nao deve ter side effects ao ser importado.
    Verifica que a funcao main() existe E que ha guard if __name__.
    NAO executa o modulo.
    """
    main_path = os.path.join(ROOT, "main.py")
    assert os.path.exists(main_path), "main.py nao encontrado na raiz do projeto."
    source = open(main_path, encoding="utf-8").read()
    assert "def main():" in source or "def main(" in source, (
        "main.py nao contem funcao main() isolada. "
        "Codigo de inicializacao solto no modulo cria side effects ao importar."
    )
    assert 'if __name__ == "__main__"' in source or "if __name__ == '__main__'" in source, (
        "main.py nao protege execucao com guard if __name__. "
        "Importar o modulo pode subir a janela grafica."
    )
