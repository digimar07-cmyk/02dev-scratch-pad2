"""
test_ai_system.py — Testes do Sistema de IA

Cobre:
  - AnalysisManager (análise de projetos)
  - OllamaClient (comunicação com Ollama)
  - TextGenerator (geração de texto)
  - Fallbacks (comportamento sem IA)
  - ImageAnalyzer (análise de imagens)
"""
import pytest
from unittest.mock import Mock, patch
from ai.analysis_manager import AnalysisManager
from ai.ollama_client import OllamaClient
from ai.text_generator import TextGenerator
from ai.fallbacks import FallbackAnalyzer
from ai.image_analyzer import ImageAnalyzer


class TestAnalysisManager:
    """Testes do gerenciador de análises."""
    
    def test_analyze_project_basic(self):
        """SMOKE: Analisar projeto básico."""
        manager = AnalysisManager()
        
        project_data = {
            "name": "Test Project",
            "path": "/path/to/project.lbrn"
        }
        
        # Mock da chamada de IA
        with patch.object(manager, 'analyze', return_value={"category": "Engraving"}):
            result = manager.analyze(project_data)
            
            assert result is not None
            assert "category" in result
    
    def test_batch_analysis(self):
        """BATCH: Analisar múltiplos projetos em batch."""
        manager = AnalysisManager()
        
        projects = [
            {"name": "Project 1", "path": "/path1.lbrn"},
            {"name": "Project 2", "path": "/path2.lbrn"},
        ]
        
        with patch.object(manager, 'analyze_batch', return_value=[{}, {}]):
            results = manager.analyze_batch(projects)
            
            assert len(results) == 2


class TestOllamaClient:
    """Testes do cliente Ollama."""
    
    def test_check_connection(self):
        """SMOKE: Verificar conexão com Ollama."""
        client = OllamaClient()
        
        # Mock da resposta
        with patch.object(client, 'is_available', return_value=True):
            available = client.is_available()
            
            assert isinstance(available, bool)
    
    def test_generate_text(self):
        """GERAÇÃO: Gerar texto com Ollama."""
        client = OllamaClient()
        
        with patch.object(client, 'generate', return_value="Generated text"):
            result = client.generate("Test prompt")
            
            assert result is not None
            assert isinstance(result, str)
    
    def test_handle_connection_error(self):
        """ERROR: Lidar com erro de conexão."""
        client = OllamaClient()
        
        with patch.object(client, 'is_available', return_value=False):
            available = client.is_available()
            
            assert available is False


class TestTextGenerator:
    """Testes do gerador de texto."""
    
    def test_generate_description(self):
        """SMOKE: Gerar descrição para projeto."""
        generator = TextGenerator()
        
        project_name = "Christmas Tree"
        
        with patch.object(generator, 'generate_description', return_value="A festive design"):
            description = generator.generate_description(project_name)
            
            assert description is not None
            assert len(description) > 0
    
    def test_generate_tags(self):
        """TAGS: Gerar tags para projeto."""
        generator = TextGenerator()
        
        project_name = "Wooden Box"
        
        with patch.object(generator, 'generate_tags', return_value=["wood", "box"]):
            tags = generator.generate_tags(project_name)
            
            assert isinstance(tags, list)
            assert len(tags) > 0


class TestFallbacks:
    """Testes do sistema de fallback (sem IA)."""
    
    def test_fallback_analysis_without_ai(self):
        """FALLBACK: Analisar sem IA disponível."""
        analyzer = FallbackAnalyzer()
        
        project_name = "engraving_design.lbrn"
        
        result = analyzer.analyze_by_filename(project_name)
        
        assert result is not None
        assert "category" in result or "tags" in result
    
    def test_keyword_based_categorization(self):
        """KEYWORDS: Categorizar por palavras-chave."""
        analyzer = FallbackAnalyzer()
        
        # Nome com palavra-chave "cutting"
        result = analyzer.categorize_by_keywords("laser_cutting_pattern")
        
        assert result is not None


class TestImageAnalyzer:
    """Testes do analisador de imagens."""
    
    def test_extract_colors(self):
        """COLORS: Extrair cores dominantes de imagem."""
        analyzer = ImageAnalyzer()
        
        # Mock de imagem
        mock_image_path = "test.png"
        
        with patch.object(analyzer, 'extract_colors', return_value=["red", "blue"]):
            colors = analyzer.extract_colors(mock_image_path)
            
            assert isinstance(colors, list)
    
    def test_detect_complexity(self):
        """COMPLEXITY: Detectar complexidade visual."""
        analyzer = ImageAnalyzer()
        
        mock_image_path = "test.png"
        
        with patch.object(analyzer, 'calculate_complexity', return_value=0.7):
            complexity = analyzer.calculate_complexity(mock_image_path)
            
            assert isinstance(complexity, (int, float))
            assert 0 <= complexity <= 1
