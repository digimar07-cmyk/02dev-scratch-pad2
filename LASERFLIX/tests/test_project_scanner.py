"""
test_project_scanner.py — Testes agressivos no ProjectScanner.

Estratégia: pastas inexistentes, permissões negadas, nomes Unicode,
muito volume, comportamentos silenciosos.
"""
import os
import pytest
from core.project_scanner import ProjectScanner


# ══════════════════════════════════════════════════════════════
# FIXTURES
# ══════════════════════════════════════════════════════════════

@pytest.fixture
def scanner(tmp_path):
    database = {}
    return ProjectScanner(database=database), database


# ══════════════════════════════════════════════════════════════
# SCAN — o motor central do app
# ══════════════════════════════════════════════════════════════

class TestScanProjects:

    def test_scan_pasta_inexistente_nao_trava(self, scanner):
        """Pasta que não existe mais não pode travar o scan."""
        sc, db = scanner
        try:
            count = sc.scan_projects(["/pasta/que/nao/existe/jamais"])
            assert count == 0
        except Exception as e:
            pytest.fail(f"BUG: scan de pasta inexistente lança exceção: {e}")

    def test_scan_com_folders_none_nao_trava(self, scanner):
        """scan_projects(None) não pode travar com TypeError."""
        sc, db = scanner
        try:
            count = sc.scan_projects(None)
            assert count == 0
        except TypeError as e:
            pytest.fail(f"BUG: scan_projects(None) lança TypeError: {e}")

    def test_scan_com_folders_lista_vazia(self, scanner):
        """scan_projects([]) deve retornar 0 e não alterar o banco."""
        sc, db = scanner
        count = sc.scan_projects([])
        assert count == 0
        assert len(db) == 0

    def test_scan_com_pasta_que_virou_arquivo(self, tmp_path, scanner):
        """Se um path que era pasta agora é um arquivo, não pode travar."""
        sc, db = scanner
        arquivo = tmp_path / "virou_arquivo.txt"
        arquivo.write_text("conteúdo")
        try:
            count = sc.scan_projects([str(arquivo)])  # é arquivo, não pasta
        except Exception as e:
            pytest.fail(f"BUG: scan de arquivo (não pasta) lança exceção: {e}")

    def test_scan_adiciona_apenas_diretorios_nao_arquivos(self, tmp_path, scanner):
        """Arquivos soltos na pasta raiz não devem ser adicionados como projetos."""
        sc, db = scanner
        (tmp_path / "arquivo_solto.svg").write_text("svg")
        (tmp_path / "arquivo_solto.pdf").write_text("pdf")
        (tmp_path / "projeto_real").mkdir()
        count = sc.scan_projects([str(tmp_path)])
        assert count == 1, f"BUG: {count} itens adicionados — arquivos soltos não devem virar projetos"
        assert str(tmp_path / "arquivo_solto.svg") not in db
        assert str(tmp_path / "projeto_real") in db

    def test_scan_nao_readiciona_projetos_existentes(self, tmp_path, scanner):
        """Re-scan na mesma pasta não deve duplicar projetos no banco."""
        sc, db = scanner
        (tmp_path / "projeto_a").mkdir()
        sc.scan_projects([str(tmp_path)])
        sc.scan_projects([str(tmp_path)])  # segundo scan
        assert len(db) == 1, f"BUG: segundo scan duplicou projetos. db tem {len(db)} itens."

    def test_scan_projeto_com_nome_unicode(self, tmp_path, scanner):
        """Pasta com nome em unicode (acentos, japonês) deve ser adicionada corretamente."""
        sc, db = scanner
        (tmp_path / "Projeto São João 日本語").mkdir()
        count = sc.scan_projects([str(tmp_path)])
        assert count == 1, "BUG: projeto com nome unicode não foi adicionado"

    def test_scan_preenche_todos_os_campos_obrigatorios(self, tmp_path, scanner):
        """Cada projeto deve ter todos os campos obrigatórios preenchidos."""
        sc, db = scanner
        (tmp_path / "Projeto Alpha").mkdir()
        sc.scan_projects([str(tmp_path)])
        campos = ["name", "origin", "favorite", "done", "good", "bad",
                  "categories", "tags", "analyzed", "ai_description", "added_date"]
        path = str(tmp_path / "Projeto Alpha")
        for campo in campos:
            assert campo in db[path], f"BUG: campo '{campo}' ausente no projeto escaneado"

    def test_scan_1000_projetos_performance(self, tmp_path, scanner):
        """1000 projetos devem ser escaneados sem travar (< 10s)."""
        import time
        sc, db = scanner
        for i in range(1000):
            (tmp_path / f"projeto_{i:04d}").mkdir()
        inicio = time.time()
        count = sc.scan_projects([str(tmp_path)])
        duracao = time.time() - inicio
        assert count == 1000
        assert duracao < 10.0, f"BUG: scan de 1000 projetos levou {duracao:.1f}s — muito lento para produção"


# ══════════════════════════════════════════════════════════════
# EXTRACT TAGS — processamento de nomes
# ══════════════════════════════════════════════════════════════

class TestExtractTags:

    def test_nome_vazio_retorna_lista_vazia(self, scanner):
        """Nome vazio não pode travar nem retornar None."""
        sc, _ = scanner
        result = sc.extract_tags_from_name("")
        assert result == [], f"BUG: extract_tags('') retornou {result!r} em vez de []"

    def test_nome_none_nao_trava(self, scanner):
        """Nome None não pode travar com AttributeError."""
        sc, _ = scanner
        try:
            result = sc.extract_tags_from_name(None)
        except AttributeError as e:
            pytest.fail(f"BUG: extract_tags_from_name(None) lança AttributeError: {e}")

    def test_nome_so_numeros_retorna_lista_vazia(self, scanner):
        """Nome composto só de números não deve gerar tags."""
        sc, _ = scanner
        result = sc.extract_tags_from_name("12345-67890-11111")
        assert all(not t.isdigit() for t in result), (
            f"BUG: extract_tags gerou tags numéricas: {result}"
        )

    def test_nome_com_stopwords_puras_retorna_lista_vazia(self, scanner):
        """Nome composto só de stopwords deve retornar lista vazia."""
        sc, _ = scanner
        result = sc.extract_tags_from_name("laser cut svg pdf bundle pack set")
        assert result == [], (
            f"BUG: extract_tags retornou {result!r} para nome composto só de stopwords."
        )

    def test_tags_nao_duplicadas(self, scanner):
        """Tags retornadas não devem ter duplicatas."""
        sc, _ = scanner
        result = sc.extract_tags_from_name("Rose Rose Rose Floral")
        lower_tags = [t.lower() for t in result]
        assert len(lower_tags) == len(set(lower_tags)), (
            f"BUG: extract_tags retornou duplicatas: {result}"
        )

    def test_maximo_5_tags_retornadas(self, scanner):
        """Nunca mais de 5 tags por projeto."""
        sc, _ = scanner
        nome_longo = "Alpha Beta Gamma Delta Epsilon Zeta Eta Theta"
        result = sc.extract_tags_from_name(nome_longo)
        assert len(result) <= 5, (
            f"BUG: extract_tags retornou {len(result)} tags (máx deveria ser 5): {result}"
        )


# ══════════════════════════════════════════════════════════════
# ANALYZE STRUCTURE — análise de arquivos do projeto
# ══════════════════════════════════════════════════════════════

class TestAnalyzeStructure:

    def test_analyze_pasta_inexistente_retorna_estrutura_vazia(self, scanner):
        """Analisar pasta que não existe mais retorna estrutura, não lança exceção."""
        sc, _ = scanner
        try:
            result = sc.analyze_project_structure("/pasta/inexistente")
            assert isinstance(result, dict)
            assert result["total_files"] == 0
        except Exception as e:
            pytest.fail(f"BUG: analyze_project_structure de pasta inexistente lança: {e}")

    def test_analyze_conta_arquivos_corretamente(self, tmp_path, scanner):
        """Contagem de arquivos deve ser exata."""
        sc, _ = scanner
        proj = tmp_path / "MeuProjeto"
        proj.mkdir()
        (proj / "arquivo1.svg").write_text("a")
        (proj / "arquivo2.pdf").write_text("b")
        (proj / "arquivo3.dxf").write_text("c")
        result = sc.analyze_project_structure(str(proj))
        assert result["total_files"] == 3, (
            f"BUG: analyze contou {result['total_files']} arquivos, esperado 3"
        )
        assert result["has_svg"] is True
        assert result["has_pdf"] is True
        assert result["has_dxf"] is True

    def test_analyze_projeto_vazio(self, tmp_path, scanner):
        """Projeto vazio (sem arquivos) deve retornar zeros, não None ou exceção."""
        sc, _ = scanner
        proj = tmp_path / "Vazio"
        proj.mkdir()
        result = sc.analyze_project_structure(str(proj))
        assert result["total_files"] == 0
        assert result["has_svg"] is False
        assert result["images"] == []
