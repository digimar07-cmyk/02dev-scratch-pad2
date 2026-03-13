"""
tests/unit/test_duplicate_detector.py — Testes reais do DuplicateDetector.

Metodologia Akita:
- Testa a logica de normalizacao e deteccao usando dados reais
- Sem mocks: DuplicateDetector nao tem dependencia de IO
"""
import pytest
from utils.duplicate_detector import DuplicateDetector


@pytest.fixture
def detector():
    return DuplicateDetector()


class TestNormalizacao:

    def test_lowercase(self, detector):
        """Normalizacao deve converter para lowercase."""
        assert detector.normalize_folder_name("NATAL") == "natal"

    def test_traco_vira_espaco(self, detector):
        """Traco deve ser convertido para espaco."""
        assert detector.normalize_folder_name("meu-projeto") == "meu projeto"

    def test_underscore_vira_espaco(self, detector):
        """Underscore deve ser convertido para espaco."""
        assert detector.normalize_folder_name("meu_projeto") == "meu projeto"

    def test_espacos_multiplos_normalizados(self, detector):
        """Espacos multiplos devem ser colapsados para um unico espaco."""
        result = detector.normalize_folder_name("meu   projeto  aqui")
        assert "  " not in result

    def test_strip_espacos_borda(self, detector):
        """Espacos nas bordas devem ser removidos."""
        assert detector.normalize_folder_name("  natal  ") == "natal"


class TestDeteccaoDuplicatas:

    def test_sem_duplicatas(self, detector):
        """Database sem nomes similares nao deve ter duplicatas."""
        db = {
            "/pastas/luminaria-natal": {},
            "/pastas/porta-retrato": {},
            "/pastas/mandala-geometrica": {},
        }
        result = detector.find_duplicates(db)
        assert len(result) == 0

    def test_detecta_duplicata_traco_vs_underscore(self, detector):
        """Pastas com traco e underscore no mesmo nome devem ser duplicatas."""
        db = {
            "/a/meu-projeto": {},
            "/b/meu_projeto": {},
        }
        result = detector.find_duplicates(db)
        assert len(result) == 1

    def test_detecta_duplicata_case_diferente(self, detector):
        """Pastas com case diferente devem ser consideradas duplicatas."""
        db = {
            "/a/Natal Arvore": {},
            "/b/natal arvore": {},
        }
        result = detector.find_duplicates(db)
        assert len(result) == 1

    def test_database_vazio_sem_duplicatas(self, detector):
        """Database vazio nao deve ter duplicatas."""
        result = detector.find_duplicates({})
        assert result == {}

    def test_is_duplicate_true(self, detector):
        """is_duplicate retorna True para caminhos com nomes normalizados iguais."""
        assert detector.is_duplicate("/a/meu-projeto", "/b/meu_projeto") is True

    def test_is_duplicate_false(self, detector):
        """is_duplicate retorna False para nomes diferentes."""
        assert detector.is_duplicate("/a/natal", "/b/pascoa") is False

    def test_get_duplicate_summary_estrutura(self, detector):
        """get_duplicate_summary deve retornar dict com chaves obrigatorias."""
        db = {"/a/proj": {}, "/b/proj": {}}
        summary = detector.get_duplicate_summary(db)
        for key in ["total_projects", "duplicate_groups", "duplicate_count", "examples"]:
            assert key in summary
