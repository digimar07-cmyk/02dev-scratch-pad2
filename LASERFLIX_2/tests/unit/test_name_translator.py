"""
tests/unit/test_name_translator.py

Testes unitarios de utils/name_translator.py.
Modulo 100% puro (sem IO, sem rede, sem Tkinter) — sem mocks necessarios.

Cobre:
  - translate_to_pt: traducao EN->PT palavra a palavra
  - translate_to_en: traducao PT->EN via REVERSE_TRANSLATIONS
  - search_bilingual: busca em qualquer idioma
  - Consistencia dos dicionarios TRANSLATIONS / REVERSE_TRANSLATIONS

Metodologia Akita: funcoes puras = testadas com inputs/outputs reais.
"""
import sys
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from utils.name_translator import (
    translate_to_pt,
    translate_to_en,
    search_bilingual,
    TRANSLATIONS,
    REVERSE_TRANSLATIONS,
)


# ── translate_to_pt ────────────────────────────────────────────────────────────

class TestTranslateToPt:

    def test_palavra_simples_conhecida(self):
        assert translate_to_pt("dog") == "cachorro"

    def test_palavra_simples_maiuscula(self):
        """Deve ser case-insensitive."""
        assert translate_to_pt("Dog") == "cachorro"

    def test_frase_multiplas_palavras(self):
        result = translate_to_pt("Nursery Mirror")
        assert "infantil" in result
        assert "espelho" in result

    def test_palavra_desconhecida_preservada(self):
        """Palavra sem traducao deve ser mantida como esta."""
        result = translate_to_pt("laserflix")
        assert "laserflix" in result

    def test_frase_mista_conhecida_e_desconhecida(self):
        result = translate_to_pt("beautiful laserflix")
        assert "bonito" in result
        assert "laserflix" in result

    def test_string_vazia_retorna_vazia(self):
        assert translate_to_pt("") == ""

    def test_pontuacao_removida_antes_de_traduzir(self):
        """Palavra com pontuacao deve ser traduzida corretamente."""
        result = translate_to_pt("dog,")
        assert "cachorro" in result

    def test_palavra_christmas(self):
        assert translate_to_pt("christmas") == "natal"

    def test_palavra_wood(self):
        assert translate_to_pt("wood") == "madeira"

    def test_palavra_heart(self):
        assert translate_to_pt("heart") == "coração"

    def test_frase_completa_laser_cut(self):
        """Simula um nome de produto tipico do Laserflix."""
        result = translate_to_pt("Christmas Tree Ornament")
        assert "natal" in result
        assert "árvore" in result
        assert "ornamento" in result

    def test_retorno_eh_string(self):
        result = translate_to_pt("cat")
        assert isinstance(result, str)


# ── translate_to_en ────────────────────────────────────────────────────────────

class TestTranslateToEn:

    def test_palavra_conhecida_pt_para_en(self):
        result = translate_to_en("cachorro")
        assert "dog" in result

    def test_string_vazia_retorna_vazia(self):
        assert translate_to_en("") == ""

    def test_palavra_desconhecida_preservada(self):
        result = translate_to_en("laserflix")
        assert "laserflix" in result

    def test_frase_pt_para_en(self):
        result = translate_to_en("espelho infantil")
        assert "mirror" in result
        assert "nursery" in result

    def test_palavra_natal(self):
        result = translate_to_en("natal")
        assert "christmas" in result

    def test_retorno_eh_string(self):
        result = translate_to_en("gato")
        assert isinstance(result, str)


# ── search_bilingual ────────────────────────────────────────────────────────────

class TestSearchBilingual:

    # Busca direta EN no texto EN
    def test_busca_direta_en_encontra(self):
        assert search_bilingual("mirror", "Nursery Mirror") is True

    def test_busca_direta_en_case_insensitive(self):
        assert search_bilingual("MIRROR", "Nursery Mirror") is True

    def test_busca_direta_en_nao_encontra(self):
        assert search_bilingual("dragon", "Nursery Mirror") is False

    # Busca PT -> encontra no texto EN via traducao reversa
    def test_busca_pt_encontra_em_texto_en(self):
        """Query 'espelho' deve encontrar 'Mirror' no texto EN."""
        assert search_bilingual("espelho", "Nursery Mirror") is True

    def test_busca_pt_tema_natal(self):
        """Query 'natal' deve encontrar 'Christmas' no texto EN."""
        assert search_bilingual("natal", "Christmas Tree Ornament") is True

    def test_busca_pt_palavra_desconhecida_nao_encontra(self):
        """Query PT sem traducao conhecida nao deve dar match falso."""
        assert search_bilingual("laserflix", "Nursery Mirror") is False

    # Casos extremos
    def test_query_vazia_retorna_false(self):
        assert search_bilingual("", "Nursery Mirror") is False

    def test_texto_vazio_retorna_false(self):
        assert search_bilingual("mirror", "") is False

    def test_ambos_vazios_retorna_false(self):
        assert search_bilingual("", "") is False

    def test_retorno_eh_bool(self):
        result = search_bilingual("dog", "Dog Box")
        assert isinstance(result, bool)

    # Exemplos literais do docstring
    def test_docstring_exemplo_mirror_en(self):
        assert search_bilingual("mirror", "Nursery Mirror") is True

    def test_docstring_exemplo_espelho_pt(self):
        assert search_bilingual("espelho", "Nursery Mirror") is True

    def test_docstring_exemplo_infantil_pt(self):
        assert search_bilingual("infantil", "Nursery Mirror") is True


# ── Consistencia dos dicionarios ───────────────────────────────────────────────

class TestDicionarios:

    def test_translations_nao_vazio(self):
        assert len(TRANSLATIONS) > 50

    def test_reverse_translations_nao_vazio(self):
        assert len(REVERSE_TRANSLATIONS) > 0

    def test_todas_chaves_sao_lowercase(self):
        """Todas as chaves do TRANSLATIONS devem ser lowercase (padrao de lookup)."""
        for key in TRANSLATIONS:
            assert key == key.lower(), f"Chave nao-lowercase: '{key}'"

    def test_dog_roundtrip(self):
        """dog -> cachorro -> dog (roundtrip)."""
        pt = translate_to_pt("dog")
        en = translate_to_en(pt)
        assert "dog" in en

    def test_christmas_roundtrip(self):
        pt = translate_to_pt("christmas")
        en = translate_to_en(pt)
        assert "christmas" in en

    def test_heart_roundtrip(self):
        pt = translate_to_pt("heart")
        en = translate_to_en(pt)
        assert "heart" in en
