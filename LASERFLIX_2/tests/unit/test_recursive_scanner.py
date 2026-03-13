"""
tests/unit/test_recursive_scanner.py

Testes unitários para utils/recursive_scanner.py → RecursiveScanner.

Metodologia Akita:
- Usa tmp_scan_tree (fixture de conftest) que cria estrutura real no tmp_path.
- Sem disco de produção, sem side-effects.
- Cobre detecção por folder.jpg (pure), fallback (hybrid), pastas técnicas ignoradas.
- ZOMBIES: Z (base vazia), O (um produto), M (múltiplos), B (pastas técnicas), E (path inválido).
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.recursive_scanner import RecursiveScanner


class TestRecursiveScannerPure:
    """scan_folders_pure: detecta APENAS pastas com folder.jpg."""

    def test_dado_base_vazia_quando_scan_pure_entao_retorna_lista_vazia(self, tmp_path):
        base = str(tmp_path / "vazia")
        os.makedirs(base)
        scanner = RecursiveScanner()
        result = scanner.scan_folders_pure(base)
        assert result == []

    def test_dado_produto_com_folder_jpg_quando_scan_pure_entao_detectado(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_pure(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "produto_natal" in names

    def test_dado_produto_sem_folder_jpg_quando_scan_pure_entao_nao_detectado(self, tmp_scan_tree):
        """produto_pascoa não tem folder.jpg — NÃO deve ser detectado no modo pure."""
        scanner = RecursiveScanner()
        result = scanner.scan_folders_pure(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "produto_pascoa" not in names

    def test_dado_pasta_tecnica_quando_scan_pure_entao_ignorada(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_pure(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "svg" not in names

    def test_dado_path_invalido_quando_scan_pure_entao_retorna_lista_vazia(self, tmp_path):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_pure(str(tmp_path / "nao_existe"))
        assert result == []


class TestRecursiveScannerHybrid:
    """scan_folders_hybrid: detecta folder.jpg E fallback (arquivos válidos)."""

    def test_dado_produto_com_folder_jpg_quando_scan_hybrid_entao_detectado(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_hybrid(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "produto_natal" in names

    def test_dado_produto_sem_folder_jpg_mas_com_svg_quando_scan_hybrid_entao_detectado(self, tmp_scan_tree):
        """produto_pascoa tem coelho.svg — deve ser detectado via fallback em hybrid."""
        scanner = RecursiveScanner()
        result = scanner.scan_folders_hybrid(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "produto_pascoa" in names

    def test_dado_pasta_tecnica_quando_scan_hybrid_entao_ignorada(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_hybrid(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "svg" not in names

    def test_dado_pasta_vazia_quando_scan_hybrid_entao_ignorada(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_hybrid(tmp_scan_tree)
        names = [p["name"] for p in result]
        assert "vazio" not in names


class TestRecursiveScannerStats:

    def test_dado_scan_realizado_quando_get_stats_entao_retorna_dict_com_chaves(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        scanner.scan_folders_hybrid(tmp_scan_tree)
        stats = scanner.get_stats()
        assert "total_scanned" in stats
        assert "products_found" in stats
        assert "technical_skipped" in stats

    def test_dado_scan_realizado_quando_products_found_coincide_com_len_result(self, tmp_scan_tree):
        scanner = RecursiveScanner()
        result = scanner.scan_folders_hybrid(tmp_scan_tree)
        stats = scanner.get_stats()
        assert stats["products_found"] == len(result)


class TestRecursiveScannerUniqueId:

    def test_dado_dois_paths_diferentes_quando_generate_unique_id_entao_ids_diferentes(self, tmp_path):
        scanner = RecursiveScanner()
        id1 = scanner.generate_unique_id("/base/prod_a", "/base")
        id2 = scanner.generate_unique_id("/base/prod_b", "/base")
        assert id1 != id2

    def test_dado_mesmo_path_quando_generate_unique_id_entao_ids_identicos(self, tmp_path):
        scanner = RecursiveScanner()
        id1 = scanner.generate_unique_id("/base/prod_a", "/base")
        id2 = scanner.generate_unique_id("/base/prod_a", "/base")
        assert id1 == id2
