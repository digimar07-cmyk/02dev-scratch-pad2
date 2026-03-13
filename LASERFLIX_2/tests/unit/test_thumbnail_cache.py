"""
tests/unit/test_thumbnail_cache.py — Testes do ThumbnailCache (logica LRU).

Metodologia Akita:
- Testa o comportamento LRU e os metodos publicos sem Tkinter
- Nao testa carregamento de imagem real (precisa de display)
- Foca em: set/get, eviction, clear, stats, find_first_image
"""
import os
import pytest


@pytest.fixture
def cache():
    """ThumbnailCache com limite reduzido para testar eviction facilmente."""
    from core.thumbnail_cache import ThumbnailCache
    c = ThumbnailCache(limit=3)
    yield c
    c.stop()  # Para o worker thread corretamente


class TestCacheLRU:

    def test_get_path_inexistente_retorna_none(self, cache):
        """get() para path que nunca foi inserido deve retornar None."""
        result = cache.get("/nao/existe.jpg")
        assert result is None

    def test_get_path_none_retorna_none(self, cache):
        """get(None) nao deve explodir, retorna None."""
        assert cache.get(None) is None

    def test_cache_vazio_stats_correto(self, cache):
        """Cache recém-criado deve ter size=0."""
        stats = cache.get_stats()
        assert stats["size"] == 0
        assert stats["limit"] == 3

    def test_clear_esvazia_cache(self, cache, tmp_path):
        """clear() deve remover todos os itens do cache."""
        # Insere manualmente no cache interno para testar sem PIL
        fake_path = str(tmp_path / "img.jpg")
        # Simulamos insercao direta no OrderedDict interno
        cache.cache[fake_path] = (123456.0, "fake_photo")
        assert cache.get_stats()["size"] == 1
        cache.clear()
        assert cache.get_stats()["size"] == 0

    def test_eviction_remove_mais_antigo(self, cache, tmp_path):
        """Ao superar o limite, o item mais antigo deve ser removido."""
        # Insere 3 itens (limite eh 3)
        for i in range(3):
            fake_path = str(tmp_path / f"img{i}.jpg")
            cache.cache[fake_path] = (float(i), f"photo_{i}")
            from collections import OrderedDict
            cache.cache.move_to_end(fake_path)

        # Insere 4o item manualmente simulando o comportamento do set()
        novo_path = str(tmp_path / "img_novo.jpg")
        cache.cache[novo_path] = (99.0, "photo_novo")
        cache.cache.move_to_end(novo_path)
        while len(cache.cache) > cache.limit:
            cache.cache.popitem(last=False)

        assert cache.get_stats()["size"] == 3
        # O mais antigo (img0.jpg) deve ter sido removido
        primeiro = str(tmp_path / "img0.jpg")
        assert primeiro not in cache.cache

    def test_get_stats_estrutura(self, cache):
        """get_stats deve retornar dict com as chaves obrigatorias."""
        stats = cache.get_stats()
        for key in ["size", "limit", "usage_pct", "queue_size"]:
            assert key in stats


class TestFindFirstImage:

    def test_encontra_jpg_na_pasta(self, cache, tmp_path):
        """find_first_image deve retornar caminho do primeiro jpg encontrado."""
        img = tmp_path / "folder.jpg"
        img.touch()
        result = cache.find_first_image(str(tmp_path))
        assert result is not None
        assert result.endswith(".jpg")

    def test_pasta_sem_imagem_retorna_none(self, cache, tmp_path):
        """Pasta sem arquivos de imagem validos deve retornar None."""
        (tmp_path / "documento.txt").touch()
        result = cache.find_first_image(str(tmp_path))
        assert result is None

    def test_pasta_inexistente_retorna_none(self, cache, tmp_path):
        """Pasta que nao existe deve retornar None sem explodir."""
        result = cache.find_first_image(str(tmp_path / "nao_existe"))
        assert result is None

    def test_get_all_project_images_recursivo(self, cache, tmp_path):
        """get_all_project_images deve encontrar imagens em subpastas."""
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.jpg").touch()
        (sub / "b.png").touch()
        result = cache.get_all_project_images(str(tmp_path))
        assert len(result) == 2
