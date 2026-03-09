"""
test_utils.py — Testes dos Utilitários

Cobre:
  - DuplicateDetector (hash, comparação)
  - NameTranslator (normalização, limpeza)
  - TextUtils (truncate, sanitize)
  - PlatformUtils (OS detection)
"""
import pytest
import tempfile
from pathlib import Path
from utils.duplicate_detector import DuplicateDetector
from utils import name_translator
from utils.text_utils import truncate_text, sanitize_filename
from utils.platform_utils import get_platform, is_windows


class TestDuplicateDetector:
    """Testes do detector de duplicatas."""
    
    def test_calculate_file_hash(self):
        """SMOKE: Calcular hash de arquivo."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
            tmp.write("test content")
            tmp_path = tmp.name
        
        try:
            detector = DuplicateDetector()
            hash1 = detector.calculate_hash(tmp_path)
            
            assert hash1 is not None
            assert len(hash1) > 0
        finally:
            Path(tmp_path).unlink()
    
    def test_identical_files_same_hash(self):
        """DUPLICATA: Arquivos idênticos devem ter mesmo hash."""
        content = "identical content"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp1:
            tmp1.write(content)
            path1 = tmp1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp2:
            tmp2.write(content)
            path2 = tmp2.name
        
        try:
            detector = DuplicateDetector()
            hash1 = detector.calculate_hash(path1)
            hash2 = detector.calculate_hash(path2)
            
            assert hash1 == hash2
        finally:
            Path(path1).unlink()
            Path(path2).unlink()
    
    def test_different_files_different_hash(self):
        """DUPLICATA: Arquivos diferentes devem ter hashes diferentes."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp1:
            tmp1.write("content A")
            path1 = tmp1.name
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp2:
            tmp2.write("content B")
            path2 = tmp2.name
        
        try:
            detector = DuplicateDetector()
            hash1 = detector.calculate_hash(path1)
            hash2 = detector.calculate_hash(path2)
            
            assert hash1 != hash2
        finally:
            Path(path1).unlink()
            Path(path2).unlink()


class TestNameTranslator:
    """Testes do tradutor de nomes."""
    
    def test_translate_to_pt(self):
        """SMOKE: Traduzir termos EN → PT."""
        result = name_translator.translate_to_pt("dog mirror")
        
        assert result is not None
        assert len(result) > 0
        # Deve conter traduções
        assert "cachorro" in result or "espelho" in result
    
    def test_translate_to_en(self):
        """TRADUÇÃO: Traduzir termos PT → EN."""
        result = name_translator.translate_to_en("cachorro espelho")
        
        assert result is not None
        assert len(result) > 0
        # Deve conter traduções
        assert "dog" in result or "mirror" in result
    
    def test_bilingual_search(self):
        """BUSCA: Busca bilíngue deve funcionar."""
        # Buscar "espelho" em texto inglês "mirror"
        found = name_translator.search_bilingual("espelho", "Nursery Mirror")
        
        assert found is True


class TestTextUtils:
    """Testes de utilitários de texto."""
    
    def test_truncate_long_text(self):
        """TRUNCATE: Truncar texto longo."""
        long_text = "A" * 100
        
        truncated = truncate_text(long_text, max_length=50)
        
        assert len(truncated) <= 53  # 50 + "..."
    
    def test_sanitize_filename(self):
        """SANITIZE: Limpar nome de arquivo."""
        unsafe_name = "file<>:\"/|?*name.txt"
        
        safe_name = sanitize_filename(unsafe_name)
        
        # Não deve conter caracteres inválidos
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            assert char not in safe_name


class TestPlatformUtils:
    """Testes de utilitários de plataforma."""
    
    def test_get_platform(self):
        """SMOKE: Detectar plataforma do sistema."""
        platform = get_platform()
        
        assert platform in ['Windows', 'Linux', 'Darwin', 'Unknown']
    
    def test_is_windows(self):
        """PLATFORM: Detectar se é Windows."""
        result = is_windows()
        
        assert isinstance(result, bool)
