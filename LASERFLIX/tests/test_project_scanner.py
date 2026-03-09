"""
test_project_scanner.py — Testes do ProjectScanner

Cobre:
  - Detecção de projetos LightBurn (.lbrn, .lbrn2)
  - Extração de metadados (nome, tamanho, data)
  - Filtragem por extensão
  - Scan recursivo de diretórios
"""
import pytest
import os
import tempfile
from pathlib import Path
from core.project_scanner import ProjectScanner


@pytest.fixture
def temp_project_dir():
    """Cria diretório temporário com projetos de teste."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Criar arquivos de teste
        Path(tmpdir, "project1.lbrn").touch()
        Path(tmpdir, "project2.lbrn2").touch()
        Path(tmpdir, "image.png").touch()
        Path(tmpdir, "document.txt").touch()
        
        # Subdiretório
        subdir = Path(tmpdir, "subfolder")
        subdir.mkdir()
        Path(subdir, "project3.lbrn").touch()
        
        yield tmpdir


class TestProjectDetection:
    """Testes de detecção de projetos."""
    
    def test_detect_lbrn_files(self, temp_project_dir):
        """SMOKE: Detectar arquivos .lbrn."""
        scanner = ProjectScanner()
        projects = scanner.scan_directory(temp_project_dir, extensions=[".lbrn"])
        
        # Deve encontrar project1.lbrn
        assert len([p for p in projects if p.endswith(".lbrn")]) >= 1
    
    def test_detect_lbrn2_files(self, temp_project_dir):
        """SMOKE: Detectar arquivos .lbrn2."""
        scanner = ProjectScanner()
        projects = scanner.scan_directory(temp_project_dir, extensions=[".lbrn2"])
        
        # Deve encontrar project2.lbrn2
        assert len([p for p in projects if p.endswith(".lbrn2")]) >= 1
    
    def test_ignore_non_project_files(self, temp_project_dir):
        """FILTRO: Não deve detectar arquivos não-projeto (.png, .txt)."""
        scanner = ProjectScanner()
        projects = scanner.scan_directory(temp_project_dir, extensions=[".lbrn", ".lbrn2"])
        
        # Não deve conter .png ou .txt
        for project in projects:
            assert not project.endswith(".png")
            assert not project.endswith(".txt")
    
    def test_recursive_scan(self, temp_project_dir):
        """RECURSIVO: Deve encontrar projetos em subdiretórios."""
        scanner = ProjectScanner()
        projects = scanner.scan_directory(temp_project_dir, extensions=[".lbrn"], recursive=True)
        
        # Deve encontrar project3.lbrn no subfolder
        subfolder_projects = [p for p in projects if "subfolder" in p]
        assert len(subfolder_projects) >= 1


class TestMetadataExtraction:
    """Testes de extração de metadados."""
    
    def test_extract_file_size(self, temp_project_dir):
        """METADADOS: Extrair tamanho do arquivo."""
        scanner = ProjectScanner()
        test_file = Path(temp_project_dir, "project1.lbrn")
        
        # Escrever conteúdo para ter tamanho
        test_file.write_text("test content")
        
        size = scanner.get_file_size(str(test_file))
        assert size > 0
    
    def test_extract_modification_date(self, temp_project_dir):
        """METADADOS: Extrair data de modificação."""
        scanner = ProjectScanner()
        test_file = Path(temp_project_dir, "project1.lbrn")
        
        mod_time = scanner.get_modification_date(str(test_file))
        assert mod_time is not None
    
    def test_extract_project_name(self, temp_project_dir):
        """METADADOS: Extrair nome do projeto do arquivo."""
        scanner = ProjectScanner()
        test_file = Path(temp_project_dir, "my_project.lbrn")
        test_file.touch()
        
        name = scanner.get_project_name(str(test_file))
        assert name == "my_project"


class TestEdgeCases:
    """Testes de casos extremos."""
    
    def test_empty_directory(self):
        """EDGE: Diretório vazio não deve causar erro."""
        with tempfile.TemporaryDirectory() as tmpdir:
            scanner = ProjectScanner()
            projects = scanner.scan_directory(tmpdir)
            assert projects == []
    
    def test_nonexistent_directory(self):
        """EDGE: Diretório inexistente deve retornar vazio ou erro tratado."""
        scanner = ProjectScanner()
        projects = scanner.scan_directory("/path/that/does/not/exist")
        # Deve retornar lista vazia ou lançar exceção tratada
        assert isinstance(projects, list)
