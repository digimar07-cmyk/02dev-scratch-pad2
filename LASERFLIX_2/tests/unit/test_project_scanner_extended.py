"""
tests/unit/test_project_scanner_extended.py

Cobre linhas ainda não testadas de core/project_scanner.py:
  60-61   scan_projects() except ao escanear pasta
  83-84   get_origin_from_path() except → retorna "Diversos"
  125     analyze_project_structure() flag has_dxf
  127     analyze_project_structure() flag has_ai
  135-136 analyze_project_structure() classificação images[] e documents[]

Regra: NUNCA alterar testes. Bugs são no app.
"""
import os
import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.project_scanner import ProjectScanner


def make_scanner():
    db = {}
    return ProjectScanner(database=db), db


class TestProjectScannerScanError:

    def test_dado_listdir_levanta_excecao_quando_scan_entao_nao_explode(self, tmp_path):
        scanner, db = make_scanner()
        pasta = str(tmp_path / "pasta")
        os.makedirs(pasta)
        with patch("os.listdir", side_effect=PermissionError("sem permissão")):
            try:
                result = scanner.scan_projects([pasta])
            except Exception as e:
                pytest.fail(f"scan_projects não deve explodir: {e}")

    def test_dado_listdir_levanta_excecao_quando_scan_entao_retorna_zero(self, tmp_path):
        scanner, db = make_scanner()
        pasta = str(tmp_path / "pasta")
        os.makedirs(pasta)
        with patch("os.listdir", side_effect=PermissionError("sem permissão")):
            result = scanner.scan_projects([pasta])
        assert result == 0


class TestProjectScannerOriginError:

    def test_dado_excecao_em_basename_quando_get_origin_entao_retorna_diversos(self):
        scanner, _ = make_scanner()
        with patch("os.path.dirname", side_effect=Exception("erro inesperado")):
            result = scanner.get_origin_from_path("/qualquer/caminho")
        assert result == "Diversos"


class TestProjectScannerAnalyzeStructureFlags:

    def test_dado_arquivo_dxf_quando_analyze_entao_has_dxf_true(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "arquivo.dxf").write_text("dxf")
        result = scanner.analyze_project_structure(str(pasta))
        assert result["has_dxf"] is True

    def test_dado_arquivo_ai_quando_analyze_entao_has_ai_true(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "arquivo.ai").write_text("ai")
        result = scanner.analyze_project_structure(str(pasta))
        assert result["has_ai"] is True

    def test_dado_arquivo_sem_dxf_ai_quando_analyze_entao_flags_false(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "arquivo.txt").write_text("txt")
        result = scanner.analyze_project_structure(str(pasta))
        assert result["has_dxf"] is False
        assert result["has_ai"] is False


class TestProjectScannerAnalyzeDocuments:

    def test_dado_arquivo_pdf_quando_analyze_entao_classificado_em_documents(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "manual.pdf").write_text("pdf")
        result = scanner.analyze_project_structure(str(pasta))
        assert "manual.pdf" in result["documents"]

    def test_dado_arquivo_sem_extensao_de_documento_quando_analyze_entao_documents_vazio(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "imagem.svg").write_text("svg")
        result = scanner.analyze_project_structure(str(pasta))
        assert result["documents"] == []


class TestProjectScannerAnalyzeImages:

    def test_dado_arquivo_png_quando_analyze_entao_classificado_em_images(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "foto.png").write_text("png")
        result = scanner.analyze_project_structure(str(pasta))
        assert "foto.png" in result["images"]

    def test_dado_arquivo_jpg_quando_analyze_entao_classificado_em_images(self, tmp_path):
        scanner, _ = make_scanner()
        pasta = tmp_path / "projeto"
        pasta.mkdir()
        (pasta / "foto.jpg").write_text("jpg")
        result = scanner.analyze_project_structure(str(pasta))
        assert "foto.jpg" in result["images"]


class TestVirtualScrollViewportLine50:
    """Cobre linha 50 de virtual_scroll_manager.py:
    o caminho do except quando winfo_height levanta Exception
    mas não no __init__ (depois de já instanciado).
    """

    def test_dado_canvas_falha_em_segunda_chamada_quando_calculate_entao_usa_padrao(self):
        from core.virtual_scroll_manager import VirtualScrollManager
        canvas = MagicMock()
        # Primeira chamada no __init__ ok, segunda falha
        canvas.winfo_height.side_effect = [800, Exception("falha na segunda")]
        canvas.bind = MagicMock()
        vsm = VirtualScrollManager(
            canvas=canvas,
            scrollable_frame=MagicMock(),
            data=[],
            card_renderer=lambda f, p, d, r, c: MagicMock(),
        )
        # Chama novamente para cair no except
        vsm._calculate_viewport()
        assert vsm.viewport_size == 18
        assert vsm.buffer_size == 12
        assert vsm.max_pool_size == 30
