"""
tests/unit/test_text_utils.py

Testes unitários para utils/text_utils.py.
Funções puras — sem fixtures de disco, sem estado externo.

Metodologia Akita:
- Funções puras são o tipo MAIS FÁCIL de testar.
- Cada teste = uma transformação de entrada → saída.
- Tabular: múltiplos casos via @pytest.mark.parametrize.
- ZOMBIES: todos os casos cobertos por parametrize.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.text_utils import remove_accents, normalize_project_name


# ════════════════════════════════════════════════════════
# remove_accents
# ════════════════════════════════════════════════════════

class TestRemoveAccents:

    @pytest.mark.parametrize("entrada, esperado", [
        ("José",       "Jose"),
        ("Natal",      "Natal"),        # sem acentos — inalterado
        ("Páscoa",     "Pascoa"),
        ("coração",    "coracao"),
        ("ação",       "acao"),
        ("Ñoño",       "Nono"),
        ("",           ""),              # ZERO — string vazia
        ("   ",        "   "),           # apenas espaços
    ])
    def test_remove_accents(self, entrada, esperado):
        assert remove_accents(entrada) == esperado


# ════════════════════════════════════════════════════════
# normalize_project_name
# ════════════════════════════════════════════════════════

class TestNormalizeProjectName:

    @pytest.mark.parametrize("entrada, esperado", [
        # Caso básico
        ("Natal_2024",                          "natal 2024"),
        # Remove extensões
        ("arvore.svg",                           "arvore"),
        ("design.pdf",                           "design"),
        ("pack.zip",                             "pack"),
        ("vetor.cdr",                            "vetor"),
        # Substitui separadores
        ("natal-arvore",                         "natal arvore"),
        ("natal_arvore",                         "natal arvore"),
        # Remove acentos
        ("Páscoa_2024",                          "pascoa 2024"),
        ("Ação",                                 "acao"),
        # Remove APENAS códigos com 5+ dígitos (IDs de produto)
        ("Natal_12345",                          "natal"),
        ("Natal_123456789",                      "natal"),
        # Preserva números curtos (anos)
        ("Natal_2024_Arvore-12345.zip",          "natal 2024 arvore"),
        ("Pack_2023",                            "pack 2023"),
        # Normaliza espaços múltiplos
        ("natal   arvore",                       "natal arvore"),
        # ZERO — string vazia
        ("",                                     ""),
        # Apenas separadores
        ("---",                                  ""),
        ("___",                                  ""),
    ])
    def test_normalize_project_name(self, entrada, esperado):
        assert normalize_project_name(entrada) == esperado

    def test_dado_nome_com_multiplas_extensoes_entao_todas_removidas(self):
        """Garante que múltiplas extensões na string são removidas."""
        resultado = normalize_project_name("design.svg.pdf")
        assert ".svg" not in resultado
        assert ".pdf" not in resultado

    def test_dado_nome_maiusculo_entao_retorna_minusculo(self):
        assert normalize_project_name("NATAL") == "natal"
