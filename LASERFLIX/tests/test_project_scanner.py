"""
test_project_scanner.py — Testes do ProjectScanner (Fase 2)

Testa:
  - scan_projects(): escaneia pastas e adiciona ao database
  - get_origin_from_path(): detecta origem pelo caminho
  - analyze_project_structure(): analisa arquivos e pastas
  - extract_tags_from_name(): extrai tags do nome do projeto

Todos os testes usam tmp_path do pytest para isolar o filesystem.
"""
import pytest
import os
from core.project_scanner import ProjectScanner


# ===========================================================
# Fixtures
# ===========================================================

@pytest.fixture
def scanner():
    """Scanner com database vazio em memória."""
    database = {}
    return ProjectScanner(database)


@pytest.fixture
def project_tree(tmp_path):
    """
    Cria estrutura de pastas real no disco para testes:

    tmp_path/
      Creative Fabrica/
        Rose Bundle/
          rose.svg
          rose.pdf
        Butterfly Pack/
          butterfly.svg
          butterfly.dxf
          thumb/         (subpasta)
      Etsy/
        Cat Design/
          cat.ai
          cat.png
    """
    root_cf = tmp_path / "Creative Fabrica"
    root_etsy = tmp_path / "Etsy"

    rose = root_cf / "Rose Bundle"
    butterfly = root_cf / "Butterfly Pack"
    cat = root_etsy / "Cat Design"

    for folder in [rose, butterfly, cat]:
        folder.mkdir(parents=True)

    (rose / "rose.svg").write_text("<svg/>")
    (rose / "rose.pdf").write_bytes(b"%PDF")
    (butterfly / "butterfly.svg").write_text("<svg/>")
    (butterfly / "butterfly.dxf").write_text("DXF")
    (butterfly / "thumb").mkdir()
    (cat / "cat.ai").write_bytes(b"%AI")
    (cat / "cat.png").write_bytes(b"\x89PNG")

    return {"root_cf": str(root_cf), "root_etsy": str(root_etsy), "tmp": tmp_path}


# ===========================================================
# TestScanProjects
# ===========================================================

class TestScanProjects:
    """Testes de scan_projects()."""

    def test_scan_finds_subdirectories(self, scanner, project_tree):
        """SCAN: Detecta subpastas como projetos."""
        count = scanner.scan_projects([project_tree["root_cf"]])

        assert count == 2
        paths = list(scanner.database.keys())
        names = [os.path.basename(p) for p in paths]
        assert "Rose Bundle" in names
        assert "Butterfly Pack" in names

    def test_scan_creates_correct_fields(self, scanner, project_tree):
        """SCAN: Projeto criado com todos os campos obrigatórios."""
        scanner.scan_projects([project_tree["root_cf"]])
        project = list(scanner.database.values())[0]

        required_fields = [
            "name", "origin", "favorite", "done", "good", "bad",
            "categories", "tags", "analyzed", "ai_description", "added_date"
        ]
        for field in required_fields:
            assert field in project, f"Campo ausente: {field}"

    def test_scan_default_values(self, scanner, project_tree):
        """SCAN: Campos booleanos começam como False."""
        scanner.scan_projects([project_tree["root_cf"]])
        project = list(scanner.database.values())[0]

        assert project["favorite"] is False
        assert project["done"] is False
        assert project["good"] is False
        assert project["bad"] is False
        assert project["analyzed"] is False
        assert project["categories"] == []
        assert project["tags"] == []
        assert project["ai_description"] == ""

    def test_scan_skips_existing_projects(self, scanner, project_tree):
        """SCAN: Não duplica projetos já existentes."""
        scanner.scan_projects([project_tree["root_cf"]])
        first_count = len(scanner.database)

        # Escaneia a mesma pasta novamente
        count = scanner.scan_projects([project_tree["root_cf"]])

        assert count == 0
        assert len(scanner.database) == first_count

    def test_scan_skips_files_only_dirs(self, scanner, tmp_path):
        """SCAN: Ignora arquivos soltos, só leva diretórios."""
        (tmp_path / "readme.txt").write_text("not a project")
        (tmp_path / "image.png").write_bytes(b"PNG")
        (tmp_path / "ProjectFolder").mkdir()

        count = scanner.scan_projects([str(tmp_path)])

        assert count == 1

    def test_scan_nonexistent_folder(self, scanner):
        """SCAN: Pasta inexistente não causa crash, retorna 0."""
        count = scanner.scan_projects(["/does/not/exist/at/all"])

        assert count == 0
        assert len(scanner.database) == 0

    def test_scan_multiple_folders(self, scanner, project_tree):
        """SCAN: Escaneia múltiplas pastas de uma vez."""
        count = scanner.scan_projects([
            project_tree["root_cf"],
            project_tree["root_etsy"]
        ])

        assert count == 3  # Rose Bundle + Butterfly Pack + Cat Design

    def test_scan_empty_folder(self, scanner, tmp_path):
        """SCAN: Pasta vazia retorna 0."""
        empty = tmp_path / "Empty Root"
        empty.mkdir()

        count = scanner.scan_projects([str(empty)])

        assert count == 0


# ===========================================================
# TestGetOriginFromPath
# ===========================================================

class TestGetOriginFromPath:
    """Testes de get_origin_from_path()."""

    def test_origin_creative_fabrica(self, scanner, tmp_path):
        """ORIGIN: Pasta com 'Creative' detecta Creative Fabrica."""
        path = str(tmp_path / "Creative Fabrica" / "My Project")
        assert scanner.get_origin_from_path(path) == "Creative Fabrica"

    def test_origin_fabrica_keyword(self, scanner, tmp_path):
        """ORIGIN: Pasta com 'Fabrica' detecta Creative Fabrica."""
        path = str(tmp_path / "Fabrica" / "My Project")
        assert scanner.get_origin_from_path(path) == "Creative Fabrica"

    def test_origin_etsy(self, scanner, tmp_path):
        """ORIGIN: Pasta com 'Etsy' detecta Etsy."""
        path = str(tmp_path / "Etsy" / "My Project")
        assert scanner.get_origin_from_path(path) == "Etsy"

    def test_origin_etsy_case_insensitive(self, scanner, tmp_path):
        """ORIGIN: Detecção de Etsy é case-insensitive."""
        path = str(tmp_path / "etsy_downloads" / "My Project")
        assert scanner.get_origin_from_path(path) == "Etsy"

    def test_origin_fallback_to_parent_name(self, scanner, tmp_path):
        """ORIGIN: Pasta desconhecida usa nome da pasta pai."""
        path = str(tmp_path / "MyStore" / "My Project")
        assert scanner.get_origin_from_path(path) == "MyStore"


# ===========================================================
# TestAnalyzeProjectStructure
# ===========================================================

class TestAnalyzeProjectStructure:
    """Testes de analyze_project_structure()."""

    def test_analyze_counts_files(self, scanner, project_tree):
        """ANALYZE: Conta total de arquivos corretamente."""
        rose_path = os.path.join(project_tree["root_cf"], "Rose Bundle")
        structure = scanner.analyze_project_structure(rose_path)

        assert structure["total_files"] == 2  # rose.svg + rose.pdf

    def test_analyze_detects_svg_flag(self, scanner, project_tree):
        """ANALYZE: Detecta has_svg=True quando existe .svg."""
        rose_path = os.path.join(project_tree["root_cf"], "Rose Bundle")
        structure = scanner.analyze_project_structure(rose_path)

        assert structure["has_svg"] is True

    def test_analyze_detects_pdf_flag(self, scanner, project_tree):
        """ANALYZE: Detecta has_pdf=True quando existe .pdf."""
        rose_path = os.path.join(project_tree["root_cf"], "Rose Bundle")
        structure = scanner.analyze_project_structure(rose_path)

        assert structure["has_pdf"] is True

    def test_analyze_detects_dxf_flag(self, scanner, project_tree):
        """ANALYZE: Detecta has_dxf=True quando existe .dxf."""
        butterfly_path = os.path.join(project_tree["root_cf"], "Butterfly Pack")
        structure = scanner.analyze_project_structure(butterfly_path)

        assert structure["has_dxf"] is True

    def test_analyze_detects_ai_flag(self, scanner, project_tree):
        """ANALYZE: Detecta has_ai=True quando existe .ai."""
        cat_path = os.path.join(project_tree["root_etsy"], "Cat Design")
        structure = scanner.analyze_project_structure(cat_path)

        assert structure["has_ai"] is True

    def test_analyze_counts_subfolders(self, scanner, project_tree):
        """ANALYZE: Conta subpastas do nível raiz."""
        butterfly_path = os.path.join(project_tree["root_cf"], "Butterfly Pack")
        structure = scanner.analyze_project_structure(butterfly_path)

        assert structure["total_subfolders"] == 1  # thumb/
        assert "thumb" in structure["subfolders"]

    def test_analyze_file_types_dict(self, scanner, project_tree):
        """ANALYZE: Dict de file_types conta extenções."""
        rose_path = os.path.join(project_tree["root_cf"], "Rose Bundle")
        structure = scanner.analyze_project_structure(rose_path)

        assert structure["file_types"][".svg"] == 1
        assert structure["file_types"][".pdf"] == 1

    def test_analyze_nonexistent_path(self, scanner):
        """ANALYZE: Caminho inexistente retorna estrutura vazia sem crash."""
        structure = scanner.analyze_project_structure("/does/not/exist")

        assert structure["total_files"] == 0
        assert structure["has_svg"] is False


# ===========================================================
# TestExtractTagsFromName
# ===========================================================

class TestExtractTagsFromName:
    """Testes de extract_tags_from_name()."""

    def test_extract_basic_tags(self, scanner):
        """TAGS: Extrai palavras relevantes do nome."""
        tags = scanner.extract_tags_from_name("Rose Flower Mandala")

        assert len(tags) > 0
        # Verifica que alguma palavra aparece nas tags
        all_tags_lower = " ".join(tags).lower()
        assert "rose" in all_tags_lower or "flower" in all_tags_lower

    def test_extract_removes_stopwords(self, scanner):
        """TAGS: Remove stopwords genéricas."""
        tags = scanner.extract_tags_from_name("Bundle Pack Collection SVG Files")
        all_tags_lower = " ".join(tags).lower()

        for stopword in ["bundle", "pack", "collection", "svg", "files", "file"]:
            assert stopword not in all_tags_lower.split()

    def test_extract_removes_extensions(self, scanner):
        """TAGS: Remove extensões de arquivo."""
        tags = scanner.extract_tags_from_name("Butterfly.svg")
        all_tags = " ".join(tags).lower()

        assert ".svg" not in all_tags

    def test_extract_removes_sku_codes(self, scanner):
        """TAGS: Remove códigos SKU numéricos longos."""
        tags = scanner.extract_tags_from_name("Cat Design-123456")
        all_tags = " ".join(tags)

        assert "123456" not in all_tags

    def test_extract_max_five_tags(self, scanner):
        """TAGS: Retorna no máximo 5 tags."""
        tags = scanner.extract_tags_from_name(
            "Rose Flower Garden Spring Nature Beautiful Elegant"
        )

        assert len(tags) <= 5

    def test_extract_empty_name(self, scanner):
        """TAGS: Nome vazio retorna lista vazia ou pequena."""
        tags = scanner.extract_tags_from_name("")

        assert isinstance(tags, list)
        assert len(tags) == 0

    def test_extract_no_duplicates(self, scanner):
        """TAGS: Sem tags duplicadas."""
        tags = scanner.extract_tags_from_name("Cat Cat Cat")
        tags_lower = [t.lower() for t in tags]

        assert len(tags_lower) == len(set(tags_lower))

    def test_extract_phrase_tag(self, scanner):
        """TAGS: Primeira tag é frase com múltiplas palavras."""
        tags = scanner.extract_tags_from_name("Floral Garden Art")

        # Primeira tag deve conter espaço (frase composta)
        assert " " in tags[0]
