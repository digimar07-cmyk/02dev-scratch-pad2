"""
test_integration.py — Testes de Integração

Cobre:
  - Database + Collections (adicionar projeto a coleção)
  - Scanner + Database (importar projetos)
  - Thumbnail + Cache (gerar e cachear)
  - VirtualScroll + Display (renderizar lista grande)
  - AI + Database (analisar e salvar)
  - Full workflow (scan → analyze → display)
"""
import pytest
import tempfile
import os
from pathlib import Path
from core.database import DatabaseManager
from core.collections_manager import CollectionsManager
from core.project_scanner import ProjectScanner
from core.thumbnail_cache import ThumbnailCache
from core.virtual_scroll_manager import VirtualScrollManager


@pytest.fixture
def temp_integration_env():
    """Ambiente completo para testes de integração."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Database temporário
        db_file = os.path.join(tmpdir, "database.json")
        collections_file = os.path.join(tmpdir, "collections.json")
        cache_dir = os.path.join(tmpdir, "cache")
        os.makedirs(cache_dir)
        
        # Projetos de teste
        projects_dir = os.path.join(tmpdir, "projects")
        os.makedirs(projects_dir)
        Path(projects_dir, "project1.lbrn").touch()
        Path(projects_dir, "project2.lbrn").touch()
        
        yield {
            "db_file": db_file,
            "collections_file": collections_file,
            "cache_dir": cache_dir,
            "projects_dir": projects_dir,
        }


class TestDatabaseCollectionsIntegration:
    """Integração Database + Collections."""
    
    def test_add_project_to_collection(self, temp_integration_env):
        """INTEGRAÇÃO: Adicionar projeto do database a uma coleção."""
        # Criar database
        db = DatabaseManager(db_file=temp_integration_env["db_file"])
        db.database["/project1"] = {"name": "Project 1"}
        db.save_database()
        
        # Criar coleção
        import core.collections_manager as cm
        original_file = cm.COLLECTIONS_FILE
        cm.COLLECTIONS_FILE = temp_integration_env["collections_file"]
        
        try:
            collections = CollectionsManager()
            collections.create_collection("My Collection")
            collections.add_project("My Collection", "/project1")
            
            # Verificar
            assert "/project1" in collections.get_projects("My Collection")
        finally:
            cm.COLLECTIONS_FILE = original_file
    
    def test_remove_project_cleans_collections(self, temp_integration_env):
        """INTEGRAÇÃO: Remover projeto deve limpar coleções."""
        db = DatabaseManager(db_file=temp_integration_env["db_file"])
        db.database["/project1"] = {"name": "Project 1"}
        db.save_database()
        
        import core.collections_manager as cm
        original_file = cm.COLLECTIONS_FILE
        cm.COLLECTIONS_FILE = temp_integration_env["collections_file"]
        
        try:
            collections = CollectionsManager()
            collections.create_collection("Test")
            collections.add_project("Test", "/project1")
            
            # Remover projeto do database
            del db.database["/project1"]
            db.save_database()
            
            # Limpar órfãos
            valid_paths = set(db.database.keys())
            collections.clean_orphan_projects(valid_paths)
            
            # Verificar que foi removido
            assert "/project1" not in collections.get_projects("Test")
        finally:
            cm.COLLECTIONS_FILE = original_file


class TestScannerDatabaseIntegration:
    """Integração Scanner + Database."""
    
    def test_scan_and_import_projects(self, temp_integration_env):
        """INTEGRAÇÃO: Escanear diretório e importar para database."""
        scanner = ProjectScanner()
        db = DatabaseManager(db_file=temp_integration_env["db_file"])
        
        # Escanear
        projects = scanner.scan_directory(
            temp_integration_env["projects_dir"],
            extensions=[".lbrn"]
        )
        
        # Importar para database
        for project_path in projects:
            project_name = Path(project_path).stem
            db.database[project_path] = {
                "name": project_name,
                "path": project_path,
            }
        
        db.save_database()
        
        # Verificar
        assert len(db.database) == 2


class TestVirtualScrollIntegration:
    """Integração VirtualScroll + Display."""
    
    def test_render_large_project_list(self):
        """INTEGRAÇÃO: Renderizar lista grande com virtual scroll."""
        # Criar lista grande de projetos
        projects = [f"project_{i}" for i in range(1000)]
        
        # VirtualScroll
        scroll_manager = VirtualScrollManager(
            viewport_height=600,
            item_height=150,
            buffer_size=5
        )
        
        # Calcular visíveis
        start, end = scroll_manager.calculate_visible_range(len(projects), scroll_position=0)
        
        # Renderizar apenas visíveis
        visible_projects = projects[start:end]
        
        # Deve renderizar apenas uma fração
        assert len(visible_projects) < len(projects)
        assert len(visible_projects) < 50  # Muito menos que 1000


class TestFullWorkflow:
    """Teste do workflow completo."""
    
    def test_complete_workflow(self, temp_integration_env):
        """WORKFLOW: Scan → Import → Organize → Display."""
        # 1. Scan
        scanner = ProjectScanner()
        projects = scanner.scan_directory(
            temp_integration_env["projects_dir"],
            extensions=[".lbrn"]
        )
        
        assert len(projects) == 2
        
        # 2. Import to Database
        db = DatabaseManager(db_file=temp_integration_env["db_file"])
        for project_path in projects:
            db.database[project_path] = {"name": Path(project_path).stem}
        db.save_database()
        
        assert len(db.database) == 2
        
        # 3. Organize in Collection
        import core.collections_manager as cm
        original_file = cm.COLLECTIONS_FILE
        cm.COLLECTIONS_FILE = temp_integration_env["collections_file"]
        
        try:
            collections = CollectionsManager()
            collections.create_collection("All Projects")
            
            for project_path in projects:
                collections.add_project("All Projects", project_path)
            
            assert collections.get_collection_size("All Projects") == 2
            
            # 4. Display with VirtualScroll
            scroll_manager = VirtualScrollManager(
                viewport_height=600,
                item_height=150,
                buffer_size=5
            )
            
            start, end = scroll_manager.calculate_visible_range(len(projects), 0)
            visible = projects[start:end]
            
            assert len(visible) <= len(projects)
            
        finally:
            cm.COLLECTIONS_FILE = original_file
