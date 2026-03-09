"""
test_infrastructure.py — Smoke Tests (Fase 1)

Verifica que a estrutura básica do projeto está funcional:
  - Importação de todos os módulos
  - Configuração (settings.py) carrega
  - Estrutura de pastas existe
  - Fixtures do pytest funcionam
"""
import pytest
import os
import sys
from pathlib import Path


class TestImports:
    """Smoke tests: Verifica que todos os módulos podem ser importados."""
    
    def test_import_core_database(self):
        """SMOKE: Importar core.database sem erro."""
        from core import database
        assert hasattr(database, 'DatabaseManager')
    
    def test_import_core_collections(self):
        """SMOKE: Importar core.collections_manager sem erro."""
        from core import collections_manager
        assert hasattr(collections_manager, 'CollectionsManager')
    
    def test_import_core_scanner(self):
        """SMOKE: Importar core.project_scanner sem erro."""
        from core import project_scanner
        assert hasattr(project_scanner, 'ProjectScanner')
    
    def test_import_core_thumbnail_cache(self):
        """SMOKE: Importar core.thumbnail_cache sem erro."""
        from core import thumbnail_cache
        assert hasattr(thumbnail_cache, 'ThumbnailCache')
    
    def test_import_ui_selection_controller(self):
        """SMOKE: Importar ui.controllers.selection_controller sem erro."""
        from ui.controllers import selection_controller
        assert hasattr(selection_controller, 'SelectionController')
    
    def test_import_utils_duplicate_detector(self):
        """SMOKE: Importar utils.duplicate_detector sem erro."""
        from utils import duplicate_detector
        assert hasattr(duplicate_detector, 'DuplicateDetector')
    
    def test_import_utils_name_translator(self):
        """SMOKE: Importar utils.name_translator sem erro."""
        from utils import name_translator
        # name_translator tem funções, não classe
        assert hasattr(name_translator, 'translate_to_pt')
        assert hasattr(name_translator, 'translate_to_en')
        assert hasattr(name_translator, 'search_bilingual')
    
    def test_import_ai_analysis_manager(self):
        """SMOKE: Importar ai.analysis_manager sem erro."""
        from ai import analysis_manager
        assert hasattr(analysis_manager, 'AnalysisManager')
    
    def test_import_ai_fallbacks(self):
        """SMOKE: Importar ai.fallbacks sem erro."""
        from ai import fallbacks
        assert hasattr(fallbacks, 'FallbackGenerator')


class TestConfiguration:
    """Testes de configuração do projeto."""
    
    def test_settings_file_exists(self):
        """ESTRUTURA: config/settings.py deve existir."""
        from config import settings
        assert hasattr(settings, 'DB_FILE')
    
    def test_db_file_path_defined(self):
        """CONFIG: DB_FILE deve estar definido."""
        from config.settings import DB_FILE
        assert DB_FILE is not None
        assert isinstance(DB_FILE, str)
        assert len(DB_FILE) > 0
    
    def test_logging_setup_works(self):
        """CONFIG: logging_setup deve criar LOGGER."""
        from utils.logging_setup import LOGGER
        assert LOGGER is not None
        assert hasattr(LOGGER, 'info')
        assert hasattr(LOGGER, 'error')
        assert hasattr(LOGGER, 'warning')


class TestProjectStructure:
    """Testes de estrutura de pastas do projeto."""
    
    def test_core_directory_exists(self):
        """ESTRUTURA: Pasta core/ deve existir."""
        assert os.path.isdir('core')
    
    def test_ui_directory_exists(self):
        """ESTRUTURA: Pasta ui/ deve existir."""
        assert os.path.isdir('ui')
    
    def test_utils_directory_exists(self):
        """ESTRUTURA: Pasta utils/ deve existir."""
        assert os.path.isdir('utils')
    
    def test_ai_directory_exists(self):
        """ESTRUTURA: Pasta ai/ deve existir."""
        assert os.path.isdir('ai')
    
    def test_tests_directory_exists(self):
        """ESTRUTURA: Pasta tests/ deve existir."""
        assert os.path.isdir('tests')
    
    def test_config_directory_exists(self):
        """ESTRUTURA: Pasta config/ deve existir."""
        assert os.path.isdir('config')


class TestPytestSetup:
    """Testes da configuração do pytest."""
    
    def test_conftest_exists(self):
        """ESTRUTURA: tests/conftest.py deve existir."""
        assert os.path.isfile('tests/conftest.py')
    
    def test_fixtures_available(self, temp_db_file, sample_database):
        """FIXTURES: Fixtures do conftest.py devem funcionar."""
        # temp_db_file fixture
        assert temp_db_file is not None
        assert isinstance(temp_db_file, str)
        assert temp_db_file.endswith('.json')
        
        # sample_database fixture
        assert sample_database is not None
        assert isinstance(sample_database, dict)
        assert len(sample_database) > 0
    
    def test_mock_fixtures_available(self, mock_canvas, mock_frame):
        """FIXTURES: Mock fixtures devem funcionar."""
        assert mock_canvas is not None
        assert mock_frame is not None
        assert hasattr(mock_canvas, 'yview_scroll')
        assert hasattr(mock_frame, 'winfo_children')


class TestPythonEnvironment:
    """Testes do ambiente Python."""
    
    def test_python_version(self):
        """AMBIENTE: Python 3.8+ deve estar instalado."""
        assert sys.version_info >= (3, 8)
    
    def test_required_packages_importable(self):
        """AMBIENTE: Pacotes essenciais devem estar instalados."""
        try:
            import pytest
            import PIL
            assert True
        except ImportError as e:
            pytest.fail(f"Pacote obrigatório não encontrado: {e}")
