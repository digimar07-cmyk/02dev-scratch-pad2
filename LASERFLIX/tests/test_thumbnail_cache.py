"""
test_thumbnail_cache.py — Testes do ThumbnailCache (Fase 2)

ESTRATEGIA:
  - Testa métodos puros (sem Tkinter/PIL) diretamente
  - Mocka ImageTk.PhotoImage para isolar de display
  - Testa: cache LRU, find_first_image, get_all_project_images,
           get/set/clear, get_stats, stop do worker

NAO TESTA:
  - load_thumbnail() real (exige display Tkinter)
  - get_cover_image_async() com callback real (exige widget Tk)
"""
import pytest
import os
import time
from collections import OrderedDict
from unittest.mock import patch, MagicMock
from core.thumbnail_cache import ThumbnailCache


# ===========================================================
# Fixture
# ===========================================================

@pytest.fixture
def cache():
    """ThumbnailCache com limite pequeno para testar LRU."""
    tc = ThumbnailCache(limit=3)
    yield tc
    tc.stop()  # Para o worker thread após cada teste


@pytest.fixture
def image_tree(tmp_path):
    """
    Estrutura de pastas com imagens reais (1x1px PNG).

    tmp_path/
      project_a/
        cover.png
        extra.jpg
        readme.txt
      project_b/
        sub/
          nested.png
      project_empty/
    """
    import struct, zlib

    def make_tiny_png(path):
        """Cria PNG válido de 1x1px branco."""
        def chunk(name, data):
            c = struct.pack('>I', len(data)) + name + data
            return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)

        png  = b'\x89PNG\r\n\x1a\n'
        png += chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
        raw  = b'\x00\xff\xff\xff'  # filtro 0 + branco RGB
        png += chunk(b'IDAT', zlib.compress(raw))
        png += chunk(b'IEND', b'')
        path.write_bytes(png)

    proj_a = tmp_path / "project_a"
    proj_b = tmp_path / "project_b"
    proj_empty = tmp_path / "project_empty"
    sub = proj_b / "sub"

    for d in [proj_a, proj_b, sub, proj_empty]:
        d.mkdir(parents=True)

    make_tiny_png(proj_a / "cover.png")
    make_tiny_png(proj_a / "extra.jpg")
    (proj_a / "readme.txt").write_text("not an image")
    make_tiny_png(sub / "nested.png")

    return {
        "proj_a": str(proj_a),
        "proj_b": str(proj_b),
        "proj_empty": str(proj_empty),
        "cover": str(proj_a / "cover.png"),
        "extra": str(proj_a / "extra.jpg"),
    }


# ===========================================================
# TestCacheLRU
# ===========================================================

class TestCacheLRU:
    """Testes do comportamento LRU do cache (get/set)."""

    def test_set_and_get_returns_same_object(self, cache, image_tree):
        """LRU: set() e get() retornam o mesmo objeto."""
        fake_photo = MagicMock(name="PhotoImage")
        path = image_tree["cover"]

        cache.set(path, fake_photo)
        result = cache.get(path)

        assert result is fake_photo

    def test_get_nonexistent_returns_none(self, cache):
        """LRU: get() de caminho não cacheado retorna None."""
        result = cache.get("/path/does/not/exist.png")
        assert result is None

    def test_get_invalid_path_returns_none(self, cache):
        """LRU: get() de caminho inválido retorna None."""
        assert cache.get("") is None
        assert cache.get(None) is None

    def test_lru_evicts_oldest_when_full(self, cache, image_tree, tmp_path):
        """LRU: Quando cheio (limit=3), remove o mais antigo."""
        # Cria 4 arquivos PNG mínimos
        paths = []
        import struct, zlib

        def make_tiny_png(p):
            def chunk(name, data):
                c = struct.pack('>I', len(data)) + name + data
                return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
            png  = b'\x89PNG\r\n\x1a\n'
            png += chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            raw  = b'\x00\xff\xff\xff'
            png += chunk(b'IDAT', zlib.compress(raw))
            png += chunk(b'IEND', b'')
            p.write_bytes(png)

        for i in range(4):
            p = tmp_path / f"img{i}.png"
            make_tiny_png(p)
            paths.append(str(p))

        photos = [MagicMock(name=f"photo{i}") for i in range(4)]

        # Adiciona 3 (limit)
        for i in range(3):
            cache.set(paths[i], photos[i])

        assert len(cache.cache) == 3

        # Adiciona o 4o - deve ejetar o primeiro
        cache.set(paths[3], photos[3])

        assert len(cache.cache) == 3
        assert cache.get(paths[0]) is None   # Mais antigo foi removido
        assert cache.get(paths[3]) is not None  # Mais novo ainda está

    def test_get_moves_to_end_lru(self, cache, image_tree, tmp_path):
        """LRU: get() de item existente move para o fim (mais recente)."""
        import struct, zlib

        def make_png(p):
            def chunk(name, data):
                c = struct.pack('>I', len(data)) + name + data
                return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
            png  = b'\x89PNG\r\n\x1a\n'
            png += chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            raw  = b'\x00\xff\xff\xff'
            png += chunk(b'IDAT', zlib.compress(raw))
            png += chunk(b'IEND', b'')
            p.write_bytes(png)

        paths = []
        for i in range(3):
            p = tmp_path / f"lru{i}.png"
            make_png(p)
            paths.append(str(p))

        photos = [MagicMock() for _ in range(3)]
        for i in range(3):
            cache.set(paths[i], photos[i])

        # Acessa o primeiro (move para o fim)
        cache.get(paths[0])

        # Adiciona novo item - deve ejetar paths[1] (agora o mais antigo)
        p_new = tmp_path / "lru_new.png"
        make_png(p_new)
        cache.set(str(p_new), MagicMock())

        assert cache.get(paths[0]) is not None   # Sobreviveu
        assert cache.get(paths[1]) is None       # Ejeitado

    def test_clear_empties_cache(self, cache, image_tree):
        """CLEAR: clear() esvazia o cache completamente."""
        cache.set(image_tree["cover"], MagicMock())
        cache.set(image_tree["extra"], MagicMock())

        cache.clear()

        assert len(cache.cache) == 0


# ===========================================================
# TestFindFirstImage
# ===========================================================

class TestFindFirstImage:
    """Testes de find_first_image()."""

    def test_finds_first_image_in_folder(self, cache, image_tree):
        """FIND: Retorna caminho da primeira imagem (ordem alfabética)."""
        result = cache.find_first_image(image_tree["proj_a"])

        assert result is not None
        assert result.endswith(("cover.png", "extra.jpg"))

    def test_returns_none_for_empty_folder(self, cache, image_tree):
        """FIND: Pasta sem imagens retorna None."""
        result = cache.find_first_image(image_tree["proj_empty"])

        assert result is None

    def test_returns_none_for_nonexistent_folder(self, cache):
        """FIND: Pasta inexistente retorna None sem crash."""
        result = cache.find_first_image("/does/not/exist")

        assert result is None

    def test_ignores_non_image_files(self, cache, image_tree):
        """FIND: Ignora arquivos .txt e outros não-imagem."""
        result = cache.find_first_image(image_tree["proj_a"])

        assert result is not None
        assert not result.endswith(".txt")


# ===========================================================
# TestGetAllProjectImages
# ===========================================================

class TestGetAllProjectImages:
    """Testes de get_all_project_images()."""

    def test_finds_images_recursively(self, cache, image_tree):
        """IMAGES: Busca imagens recursivamente em subpastas."""
        # proj_b tem imagem apenas na subpasta
        result = cache.get_all_project_images(image_tree["proj_b"])

        assert len(result) == 1
        assert result[0].endswith("nested.png")

    def test_finds_all_images_in_flat_folder(self, cache, image_tree):
        """IMAGES: Encontra todas as imagens em pasta plana."""
        result = cache.get_all_project_images(image_tree["proj_a"])

        assert len(result) == 2

    def test_empty_folder_returns_empty_list(self, cache, image_tree):
        """IMAGES: Pasta vazia retorna lista vazia."""
        result = cache.get_all_project_images(image_tree["proj_empty"])

        assert result == []

    def test_max_images_limit(self, cache, tmp_path):
        """IMAGES: Respeita limite max_images."""
        import struct, zlib

        def make_png(p):
            def chunk(name, data):
                c = struct.pack('>I', len(data)) + name + data
                return c + struct.pack('>I', zlib.crc32(name + data) & 0xffffffff)
            png  = b'\x89PNG\r\n\x1a\n'
            png += chunk(b'IHDR', struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0))
            raw  = b'\x00\xff\xff\xff'
            png += chunk(b'IDAT', zlib.compress(raw))
            png += chunk(b'IEND', b'')
            p.write_bytes(png)

        folder = tmp_path / "many_images"
        folder.mkdir()
        for i in range(10):
            make_png(folder / f"img{i:02d}.png")

        result = cache.get_all_project_images(str(folder), max_images=3)

        assert len(result) == 3

    def test_returns_absolute_paths(self, cache, image_tree):
        """IMAGES: Retorna caminhos absolutos."""
        result = cache.get_all_project_images(image_tree["proj_a"])

        for path in result:
            assert os.path.isabs(path)


# ===========================================================
# TestGetStats
# ===========================================================

class TestGetStats:
    """Testes de get_stats()."""

    def test_stats_empty_cache(self, cache):
        """STATS: Cache vazio tem size=0."""
        stats = cache.get_stats()

        assert stats["size"] == 0
        assert stats["limit"] == 3
        assert stats["usage_pct"] == 0.0

    def test_stats_with_items(self, cache, image_tree):
        """STATS: Estatísticas corretas após adicionar itens."""
        cache.set(image_tree["cover"], MagicMock())
        cache.set(image_tree["extra"], MagicMock())

        stats = cache.get_stats()

        assert stats["size"] == 2
        assert stats["usage_pct"] == pytest.approx(66.67, rel=0.01)

    def test_stats_has_queue_size_key(self, cache):
        """STATS: stats contém chave queue_size."""
        stats = cache.get_stats()

        assert "queue_size" in stats
        assert isinstance(stats["queue_size"], int)


# ===========================================================
# TestWorkerThread
# ===========================================================

class TestWorkerThread:
    """Testes do worker thread assíncrono."""

    def test_worker_thread_starts(self, cache):
        """WORKER: Thread worker inicia ao criar o cache."""
        assert cache.worker_thread is not None
        assert cache.worker_thread.is_alive()

    def test_stop_terminates_worker(self, cache):
        """WORKER: stop() para o worker thread."""
        cache.stop()

        # Dá tempo para o join finalizar
        cache.worker_thread.join(timeout=3)

        assert not cache.worker_thread.is_alive()
