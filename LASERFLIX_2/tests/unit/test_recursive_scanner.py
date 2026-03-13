"""
tests/unit/test_recursive_scanner.py — Testes reais do RecursiveScanner.

Metodologia Akita:
- Usa tmp_path do pytest para criar estrutura real de pastas no disco
- Sem mocks de filesystem: testa comportamento real
- Cada modo (pure/hybrid) testado separadamente
"""
import os
import pytest
from utils.recursive_scanner import RecursiveScanner


@pytest.fixture
def scanner():
    return RecursiveScanner()


def criar_produto_folder_jpg(pasta_base, nome):
    """Cria pasta com folder.jpg (deteccao pure mode)."""
    p = pasta_base / nome
    p.mkdir()
    (p / "folder.jpg").touch()
    return p


def criar_produto_com_svg(pasta_base, nome):
    """Cria pasta com arquivo .svg (deteccao hybrid mode fallback)."""
    p = pasta_base / nome
    p.mkdir()
    (p / "arquivo.svg").touch()
    return p


class TestScanPure:

    def test_encontra_pasta_com_folder_jpg(self, scanner, tmp_path):
        """Modo pure deve encontrar pasta que tem folder.jpg."""
        criar_produto_folder_jpg(tmp_path, "Luminaria Natal")
        result = scanner.scan_folders_pure(str(tmp_path))
        assert len(result) == 1
        assert result[0]["name"] == "Luminaria Natal"

    def test_ignora_pasta_sem_folder_jpg(self, scanner, tmp_path):
        """Modo pure deve ignorar pasta sem folder.jpg mesmo com outros arquivos."""
        p = tmp_path / "Produto Sem Capa"
        p.mkdir()
        (p / "arquivo.svg").touch()
        result = scanner.scan_folders_pure(str(tmp_path))
        assert len(result) == 0

    def test_encontra_multiplos_produtos(self, scanner, tmp_path):
        """Modo pure deve encontrar todos os produtos com folder.jpg."""
        for nome in ["Produto A", "Produto B", "Produto C"]:
            criar_produto_folder_jpg(tmp_path, nome)
        result = scanner.scan_folders_pure(str(tmp_path))
        assert len(result) == 3

    def test_pasta_base_inexistente_retorna_vazio(self, scanner, tmp_path):
        """Caminho inexistente deve retornar lista vazia sem explodir."""
        result = scanner.scan_folders_pure(str(tmp_path / "nao_existe"))
        assert result == []

    def test_pasta_base_vazia_retorna_vazio(self, scanner, tmp_path):
        """Pasta base sem nenhum conteudo deve retornar lista vazia."""
        result = scanner.scan_folders_pure(str(tmp_path))
        assert result == []

    def test_ignora_subpastas_tecnicas(self, scanner, tmp_path):
        """Pastas tecnicas como 'svg', 'backup', 'cache' devem ser ignoradas."""
        for nome in ["svg", "backup", "cache", ".git", "__pycache__"]:
            p = tmp_path / nome
            p.mkdir()
            (p / "folder.jpg").touch()  # Tem folder.jpg mas e pasta tecnica
        result = scanner.scan_folders_pure(str(tmp_path))
        assert len(result) == 0

    def test_detection_method_pure(self, scanner, tmp_path):
        """Produto encontrado em modo pure deve ter detection_method='folder_jpg'."""
        criar_produto_folder_jpg(tmp_path, "Produto X")
        result = scanner.scan_folders_pure(str(tmp_path))
        assert result[0]["detection_method"] == "folder_jpg"
        assert result[0]["has_folder_jpg"] is True


class TestScanHybrid:

    def test_encontra_produto_via_fallback_svg(self, scanner, tmp_path):
        """Modo hybrid deve encontrar pasta com .svg mesmo sem folder.jpg."""
        criar_produto_com_svg(tmp_path, "Produto SVG")
        result = scanner.scan_folders_hybrid(str(tmp_path))
        assert len(result) == 1
        assert result[0]["detection_method"] == "fallback"

    def test_stats_atualizado_apos_scan(self, scanner, tmp_path):
        """Stats devem refletir o numero real de produtos encontrados."""
        for i in range(3):
            criar_produto_folder_jpg(tmp_path, f"Prod {i}")
        scanner.scan_folders_pure(str(tmp_path))
        stats = scanner.get_stats()
        assert stats["products_found"] == 3

    def test_unique_id_gerado_para_cada_produto(self, scanner, tmp_path):
        """Cada produto deve ter unique_id diferente."""
        for nome in ["A", "B", "C"]:
            criar_produto_folder_jpg(tmp_path, nome)
        result = scanner.scan_folders_pure(str(tmp_path))
        ids = [r["unique_id"] for r in result]
        assert len(ids) == len(set(ids))  # Todos unicos
