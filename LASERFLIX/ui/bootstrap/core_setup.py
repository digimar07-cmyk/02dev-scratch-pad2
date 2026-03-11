"""
ui/bootstrap/core_setup.py — Instancia objetos core/ e ai/.

Isola todos os imports de core/ e ai/ do main_window.py.
O main_window.py nunca importa core/ diretamente.
"""
from core.database import DatabaseManager
from core.collections_manager import CollectionsManager
from core.thumbnail_preloader import ThumbnailPreloader
from core.project_scanner import ProjectScanner

from ai.ollama_client import OllamaClient
from ai.image_analyzer import ImageAnalyzer
from ai.text_generator import TextGenerator
from ai.fallbacks import FallbackGenerator
from ai.analysis_manager import AnalysisManager


class CoreSetup:
    """
    Responsável por instanciar e expor todos os objetos core/ e ai/.
    Injetado no LaserflixMainWindow via composição.
    """

    def __init__(self):
        self.db_manager = DatabaseManager()
        self.db_manager.load_config()
        self.db_manager.load_database()

        self.collections_manager = CollectionsManager()
        self.thumbnail_preloader = ThumbnailPreloader(max_workers=4)
        self.scanner = ProjectScanner(self.db_manager.database)

        self.ollama = OllamaClient(self.db_manager.config.get("models"))
        self.image_analyzer = ImageAnalyzer(self.ollama)
        self.fallback_generator = FallbackGenerator(self.scanner)
        self.text_generator = TextGenerator(
            self.ollama, self.image_analyzer, self.scanner, self.fallback_generator
        )
        self.analysis_manager = AnalysisManager(
            self.text_generator, self.db_manager, self.ollama
        )

        self.database = self.db_manager.database
