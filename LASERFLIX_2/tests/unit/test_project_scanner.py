"""
tests/unit/test_project_scanner.py

Testes unitários para core/project_scanner.py → ProjectScanner.

Metodologia Akita:
- ProjectScanner recebe `database` como dict injetado (sem DB real de produção).
- Usa tmp_path para criar estrutura de pastas real.
- ZOMBIES: Z (pastas vazias), O (um projeto), M (múltiplos), E (pasta não existe).
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.project_scanner import ProjectScanner


# ════════════════════════════════════════════════════════
# scan_projects
# ════════════════════════════════════════════════════════

class TestProjectScannerScanProjects:

    def test_dado_lista_vazia_quando_scan_projects_entao_retorna_zero(self, tmp_path):
        db = {}
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([])
        assert result == 0

    def test_dado_pasta_inexistente_quando_scan_projects_entao_retorna_zero(self, tmp_path):
        db = {}
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([str(tmp_path / "nao_existe")])
        assert result == 0

    def test_dado_pasta_vazia_quando_scan_projects_entao_retorna_zero(self, tmp_path):
        base = tmp_path / "base"
        base.mkdir()
        db = {}
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([str(base)])
        assert result == 0

    def test_dado_uma_subpasta_quando_scan_projects_entao_retorna_um(self, tmp_path):
        base = tmp_path / "base"
        base.mkdir()
        (base / "produto_natal").mkdir()
        db = {}
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([str(base)])
        assert result == 1

    def test_dado_uma_subpasta_quando_scan_projects_entao_db_contem_path(self, tmp_path):
        base = tmp_path / "base"
        base.mkdir()
        p = base / "produto_natal"
        p.mkdir()
        db = {}
        scanner = ProjectScanner(database=db)
        scanner.scan_projects([str(base)])
        assert str(p) in db

    def test_dado_tres_subpastas_quando_scan_projects_entao_retorna_tres(self, tmp_path):
        base = tmp_path / "base"
        base.mkdir()
        for i in range(3):
            (base / f"produto_{i}").mkdir()
        db = {}
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([str(base)])
        assert result == 3

    def test_dado_projeto_ja_no_db_quando_scan_projects_entao_nao_duplica(self, tmp_path):
        base = tmp_path / "base"
        base.mkdir()
        p = base / "produto_natal"
        p.mkdir()
        db = {str(p): {"name": "produto_natal"}}  # já existe
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([str(base)])
        assert result == 0  # não adiciona duplicata

    def test_dado_arquivo_na_pasta_quando_scan_projects_entao_ignora_arquivo(self, tmp_path):
        """Apenas diretórios são projetos, arquivos são ignorados."""
        base = tmp_path / "base"
        base.mkdir()
        (base / "arquivo.txt").write_text("conteudo")
        db = {}
        scanner = ProjectScanner(database=db)
        result = scanner.scan_projects([str(base)])
        assert result == 0

    def test_dado_scan_quando_projeto_adicionado_tem_campos_obrigatorios(self, tmp_path):
        base = tmp_path / "base"
        base.mkdir()
        p = base / "produto_natal"
        p.mkdir()
        db = {}
        scanner = ProjectScanner(database=db)
        scanner.scan_projects([str(base)])
        projeto = db[str(p)]
        for campo in ["name", "origin", "favorite", "done", "categories", "tags", "analyzed"]:
            assert campo in projeto, f"Campo ausente: {campo}"


# ════════════════════════════════════════════════════════
# get_origin_from_path
# ════════════════════════════════════════════════════════

class TestProjectScannerOrigin:

    @pytest.mark.parametrize("path, expected_origin", [
        ("/projetos/Creative Fabrica/natal",  "Creative Fabrica"),
        ("/projetos/CREATIVE/natal",          "Creative Fabrica"),
        ("/projetos/FABRICA/natal",           "Creative Fabrica"),
        ("/projetos/Etsy/natal",              "Etsy"),
        ("/projetos/ETSY/natal",              "Etsy"),
        ("/projetos/Diversos/natal",          "Diversos"),
    ])
    def test_get_origin_from_path(self, path, expected_origin):
        scanner = ProjectScanner(database={})
        result = scanner.get_origin_from_path(path)
        assert result == expected_origin


# ════════════════════════════════════════════════════════
# analyze_project_structure
# ════════════════════════════════════════════════════════

class TestProjectScannerAnalyzeStructure:

    def test_dado_pasta_com_svg_quando_analyze_entao_has_svg_true(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        (p / "arte.svg").write_bytes(b"<svg/>")
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        assert result["has_svg"] is True

    def test_dado_pasta_com_pdf_quando_analyze_entao_has_pdf_true(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        (p / "manual.pdf").write_bytes(b"%PDF")
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        assert result["has_pdf"] is True

    def test_dado_pasta_vazia_quando_analyze_entao_total_files_zero(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        assert result["total_files"] == 0

    def test_dado_pasta_com_dois_arquivos_quando_analyze_entao_total_files_dois(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        (p / "a.svg").write_bytes(b"<svg/>")
        (p / "b.pdf").write_bytes(b"%PDF")
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        assert result["total_files"] == 2

    def test_dado_pasta_sem_formatos_especiais_quando_analyze_entao_flags_false(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        (p / "readme.txt").write_text("texto")
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        assert result["has_svg"] is False
        assert result["has_pdf"] is False
        assert result["has_dxf"] is False
        assert result["has_ai"] is False

    def test_dado_pasta_com_subpasta_quando_analyze_entao_total_subfolders_um(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        (p / "subpasta").mkdir()
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        assert result["total_subfolders"] == 1

    def test_dado_analyze_quando_retorna_chaves_obrigatorias(self, tmp_path):
        p = tmp_path / "produto"
        p.mkdir()
        scanner = ProjectScanner(database={})
        result = scanner.analyze_project_structure(str(p))
        for chave in ["total_files", "total_subfolders", "file_types",
                      "subfolders", "images", "documents",
                      "has_svg", "has_pdf", "has_dxf", "has_ai"]:
            assert chave in result, f"Chave ausente: {chave}"


# ════════════════════════════════════════════════════════
# extract_tags_from_name
# ════════════════════════════════════════════════════════

class TestProjectScannerExtractTags:

    def test_dado_nome_vazio_quando_extract_tags_entao_lista_vazia(self):
        scanner = ProjectScanner(database={})
        result = scanner.extract_tags_from_name("")
        assert result == []

    def test_dado_nome_simples_quando_extract_tags_entao_retorna_tags(self):
        scanner = ProjectScanner(database={})
        result = scanner.extract_tags_from_name("Natal Arvore")
        assert len(result) > 0

    def test_dado_nome_com_stopwords_quando_extract_tags_entao_stopwords_removidas(self):
        scanner = ProjectScanner(database={})
        result = scanner.extract_tags_from_name("laser cut svg bundle")
        tags_lower = [t.lower() for t in result]
        # Stopwords não devem aparecer como tag individual
        for stopword in ["laser", "cut", "svg", "bundle"]:
            assert stopword not in tags_lower

    def test_dado_nome_com_sku_quando_extract_tags_entao_sku_removido(self):
        scanner = ProjectScanner(database={})
        result = scanner.extract_tags_from_name("Natal-12345")
        for tag in result:
            assert "12345" not in tag

    def test_dado_nome_com_extensao_quando_extract_tags_entao_extensao_removida(self):
        scanner = ProjectScanner(database={})
        result = scanner.extract_tags_from_name("Natal.svg")
        for tag in result:
            assert ".svg" not in tag

    def test_dado_nome_longo_quando_extract_tags_entao_max_cinco_tags(self):
        scanner = ProjectScanner(database={})
        result = scanner.extract_tags_from_name("aa bb cc dd ee ff gg hh")
        assert len(result) <= 5
