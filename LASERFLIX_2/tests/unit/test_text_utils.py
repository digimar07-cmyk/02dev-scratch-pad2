"""
tests/unit/test_text_utils.py — Testes reais das funcoes de text_utils.

Metodologia Akita:
- Funcoes puras: sem IO, sem mocks, sem fixtures especiais
- Cada teste valida uma regra documentada no docstring da funcao
"""
import pytest
from utils.text_utils import remove_accents, normalize_project_name


class TestRemoveAccents:

    def test_remove_acento_agudo(self):
        """Acentos agudos devem ser removidos."""
        assert remove_accents("Jose") == "Jose"
        assert remove_accents("Luminária") == "Luminaria"

    def test_remove_cedilha(self):
        """Cedilha deve ser removida."""
        assert remove_accents("Cançao") == "Cancao"

    def test_string_sem_acento_inalterada(self):
        """String sem acento nao deve ser alterada."""
        assert remove_accents("natal") == "natal"

    def test_string_vazia(self):
        """String vazia deve retornar string vazia."""
        assert remove_accents("") == ""

    def test_preserva_numeros_e_simbolos(self):
        """Numeros e simbolos nao devem ser afetados."""
        result = remove_accents("Proj 123 !@#")
        assert "123" in result
        assert "!@#" in result


class TestNormalizeProjectName:

    def test_lowercase(self):
        """Resultado deve ser sempre lowercase."""
        result = normalize_project_name("NATAL ARVORE")
        assert result == result.lower()

    def test_remove_extensao_zip(self):
        """Extensao .zip deve ser removida."""
        result = normalize_project_name("produto.zip")
        assert ".zip" not in result

    def test_remove_extensao_svg(self):
        """Extensao .svg deve ser removida."""
        result = normalize_project_name("vetor.svg")
        assert ".svg" not in result

    def test_substitui_traco_por_espaco(self):
        """Tracos devem ser convertidos para espaco."""
        result = normalize_project_name("meu-produto")
        assert "-" not in result
        assert "meu produto" == result

    def test_substitui_underscore_por_espaco(self):
        """Underscores devem ser convertidos para espaco."""
        result = normalize_project_name("meu_produto")
        assert "_" not in result

    def test_remove_codigo_numerico_longo(self):
        """Codigos numericos com 5+ digitos devem ser removidos."""
        result = normalize_project_name("produto-12345")
        assert "12345" not in result

    def test_preserva_ano_4_digitos(self):
        """Anos (4 digitos) NAO devem ser removidos — so IDs com 5+ digitos sao."""
        result = normalize_project_name("natal-2024")
        assert "2024" in result

    def test_remove_acento(self):
        """Acentos devem ser removidos na normalizacao."""
        result = normalize_project_name("Árvore de Natal")
        assert "á" not in result.lower()
        assert "arvore" in result

    def test_normaliza_espacos_multiplos(self):
        """Espacos multiplos devem colapsar para um unico espaco."""
        result = normalize_project_name("natal   arvore")
        assert "  " not in result

    def test_string_vazia(self):
        """String vazia deve retornar string vazia sem explodir."""
        assert normalize_project_name("") == ""

    def test_exemplo_do_docstring(self):
        """Exemplo exato do docstring: anos (4 digitos) sao preservados, IDs (5+) removidos."""
        result = normalize_project_name("Natal_2024_Arvore-12345.zip")
        assert result == "natal 2024 arvore"
