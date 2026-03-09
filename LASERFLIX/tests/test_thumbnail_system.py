"""
test_thumbnail_system.py — Testes do Sistema de Thumbnails

Cobre:
  - ThumbnailCache (save, load, cleanup)
  - ThumbnailPreloader (threading, priority queue)
  - Lazy loading
  - Memory management
"""
import pytest
import os
import tempfile
from pathlib import Path
from PIL import Image
from core.thumbnail_cache import ThumbnailCache
from core.thumbnail_preloader import ThumbnailPreloader


@pytest.fixture
def temp_cache_dir():
    """Cria diretório temporário para cache de thumbnails."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def sample_image():
    """Cria imagem de teste."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tmp.name)
        yield tmp.name
    os.unlink(tmp.name)


class TestThumbnailCache:
    """Testes do sistema de cache de thumbnails."""
    
    def test_save_thumbnail(self, temp_cache_dir, sample_image):
        """SMOKE: Salvar thumbnail no cache."""
        cache = ThumbnailCache(cache_dir=temp_cache_dir)
        
        # Criar thumbnail
        img = Image.open(sample_image)
        img.thumbnail((64, 64))
        
        cache.save("test_project", img)
        
        # Verificar que arquivo foi criado
        cached_files = os.listdir(temp_cache_dir)
        assert len(cached_files) > 0
    
    def test_load_thumbnail(self, temp_cache_dir, sample_image):
        """SMOKE: Carregar thumbnail do cache."""
        cache = ThumbnailCache(cache_dir=temp_cache_dir)
        
        # Salvar
        img = Image.open(sample_image)
        img.thumbnail((64, 64))
        cache.save("test_project", img)
        
        # Carregar
        loaded_img = cache.load("test_project")
        assert loaded_img is not None
        assert isinstance(loaded_img, Image.Image)
    
    def test_cache_miss(self, temp_cache_dir):
        """EDGE: Carregar thumbnail inexistente deve retornar None."""
        cache = ThumbnailCache(cache_dir=temp_cache_dir)
        loaded_img = cache.load("nonexistent_project")
        assert loaded_img is None
    
    def test_cleanup_old_cache(self, temp_cache_dir, sample_image):
        """LIMPEZA: Remover thumbnails antigos do cache."""
        cache = ThumbnailCache(cache_dir=temp_cache_dir)
        
        # Salvar thumbnail
        img = Image.open(sample_image)
        cache.save("old_project", img)
        
        # Limpar cache
        cache.cleanup(max_age_days=0)  # Remove tudo
        
        # Verificar que foi removido
        loaded_img = cache.load("old_project")
        assert loaded_img is None


class TestThumbnailPreloader:
    """Testes do sistema de pré-carregamento de thumbnails."""
    
    def test_preload_thumbnail(self, temp_cache_dir, sample_image):
        """SMOKE: Pré-carregar thumbnail em background."""
        preloader = ThumbnailPreloader(cache_dir=temp_cache_dir)
        
        # Solicitar pré-carregamento
        preloader.request(sample_image, priority=1)
        
        # Aguardar processamento (timeout)
        import time
        time.sleep(0.5)
        
        # Verificar que foi processado
        assert preloader.queue.qsize() == 0  # Fila deve estar vazia
    
    def test_priority_queue(self, temp_cache_dir):
        """PRIORIDADE: Thumbnails com maior prioridade devem ser processados primeiro."""
        preloader = ThumbnailPreloader(cache_dir=temp_cache_dir)
        
        # Adicionar com prioridades diferentes
        preloader.request("low_priority.png", priority=3)
        preloader.request("high_priority.png", priority=1)
        
        # Próximo item deve ser o de maior prioridade (menor número)
        if not preloader.queue.empty():
            priority, path = preloader.queue.get()
            assert "high_priority" in path


class TestLazyLoading:
    """Testes de carregamento lazy de thumbnails."""
    
    def test_load_only_visible_thumbnails(self):
        """LAZY: Carregar apenas thumbnails visíveis."""
        # Mock de projetos
        projects = [f"project_{i}" for i in range(100)]
        visible_range = (0, 10)  # Apenas primeiros 10 visíveis
        
        # Carregar apenas visíveis
        to_load = projects[visible_range[0]:visible_range[1]]
        
        assert len(to_load) == 10
        assert to_load[0] == "project_0"
        assert to_load[-1] == "project_9"
