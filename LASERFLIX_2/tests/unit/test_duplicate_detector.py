"""
tests/unit/test_duplicate_detector.py

Testes unitários para utils/duplicate_detector.py → DuplicateDetector.

Metodologia Akita:
- Sem disco: DuplicateDetector recebe dict na memória.
- ZOMBIES: Z/O/M/B/E cobertos.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.duplicate_detector import DuplicateDetector


class TestDuplicateDetectorNormalize:
    """normalize_folder_name: transformações puras."""

    @pytest.mark.parametrize("entrada, esperado", [
        ("Natal_2024",    "natal 2024"),
        ("natal-2024",    "natal 2024"),
        ("NATAL_2024",    "natal 2024"),
        ("natal  2024",   "natal 2024"),
        ("",              ""),
    ])
    def test_normalize_folder_name(self, entrada, esperado):
        detector = DuplicateDetector()
        assert detector.normalize_folder_name(entrada) == esperado


class TestDuplicateDetectorFindDuplicates:

    def test_dado_db_vazio_quando_find_duplicates_entao_retorna_dict_vazio(self):
        detector = DuplicateDetector()
        result = detector.find_duplicates({})
        assert result == {}

    def test_dado_dois_paths_nome_identico_quando_find_duplicates_entao_detecta_grupo(self):
        # Arrange
        db = {
            "/disco1/natal_2024": {},
            "/disco2/natal_2024": {},
        }
        detector = DuplicateDetector()

        # Act
        result = detector.find_duplicates(db)

        # Assert — deve ter exatamente 1 grupo de duplicata
        assert len(result) == 1
        grupo = list(result.values())[0]
        assert len(grupo) == 2

    def test_dado_paths_nomes_diferentes_quando_find_duplicates_entao_nao_ha_duplicatas(self):
        db = {
            "/proj/natal_2024": {},
            "/proj/pascoa_2023": {},
        }
        detector = DuplicateDetector()
        assert detector.find_duplicates(db) == {}

    def test_dado_nomes_com_separadores_diferentes_quando_find_duplicates_entao_detecta_como_iguais(self):
        """natal_2024 e natal-2024 devem ser tratados como duplicata."""
        db = {
            "/proj/natal_2024": {},
            "/proj/natal-2024": {},
        }
        detector = DuplicateDetector()
        result = detector.find_duplicates(db)
        assert len(result) == 1

    def test_dado_tres_paths_dois_iguais_quando_find_duplicates_entao_um_grupo_dois_paths(self):
        db = {
            "/a/natal_2024": {},
            "/b/natal_2024": {},
            "/c/pascoa": {},
        }
        detector = DuplicateDetector()
        result = detector.find_duplicates(db)
        assert len(result) == 1
        grupo = list(result.values())[0]
        assert len(grupo) == 2


class TestDuplicateDetectorIsDuplicate:

    def test_dado_dois_paths_mesmo_basename_quando_is_duplicate_entao_true(self):
        detector = DuplicateDetector()
        assert detector.is_duplicate("/a/natal_2024", "/b/natal_2024") is True

    def test_dado_dois_paths_basenames_diferentes_quando_is_duplicate_entao_false(self):
        detector = DuplicateDetector()
        assert detector.is_duplicate("/a/natal_2024", "/b/pascoa_2023") is False

    def test_dado_variantes_separador_quando_is_duplicate_entao_true(self):
        detector = DuplicateDetector()
        assert detector.is_duplicate("/a/natal_2024", "/b/natal-2024") is True


class TestDuplicateDetectorSummary:

    def test_dado_db_vazio_quando_get_duplicate_summary_entao_zeros(self):
        detector = DuplicateDetector()
        summary = detector.get_duplicate_summary({})
        assert summary["total_projects"] == 0
        assert summary["duplicate_groups"] == 0
        assert summary["duplicate_count"] == 0

    def test_dado_db_com_duplicatas_quando_get_duplicate_summary_entao_count_correto(self):
        db = {
            "/a/natal_2024": {},
            "/b/natal_2024": {},
            "/c/pascoa": {},
        }
        detector = DuplicateDetector()
        summary = detector.get_duplicate_summary(db)
        assert summary["total_projects"] == 3
        assert summary["duplicate_groups"] == 1
        assert summary["duplicate_count"] == 2
