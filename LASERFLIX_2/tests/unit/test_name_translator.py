"""
tests/unit/test_name_translator.py

Testes unitários para utils/name_translator.py.

Metodologia Akita:
- Funções puras — sem estado, sem disco, sem Tkinter.
- Tabular via @pytest.mark.parametrize.
- ZOMBIES: Z (string vazia), O (uma palavra), M (múltiplas), B (pontuação), E (palavra desconhecida).
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.name_translator import translate_to_pt, translate_to_en, search_bilingual, TRANSLATIONS


# ════════════════════════════════════════════════════════
# translate_to_pt
# ════════════════════════════════════════════════════════

class TestTranslateToPt:

    def test_dado_string_vazia_quando_translate_to_pt_entao_retorna_vazia(self):
        assert translate_to_pt("") == ""

    @pytest.mark.parametrize("entrada, esperado", [
        ("dog",              "cachorro"),
        ("cat",              "gato"),
        ("christmas",        "natal"),
        ("heart",            "coração"),
        ("flower",           "flor"),
        ("star",             "estrela"),
        ("mirror",           "espelho"),
        ("wood",             "madeira"),
    ])
    def test_dado_palavra_conhecida_quando_translate_to_pt_entao_retorna_pt(self, entrada, esperado):
        assert translate_to_pt(entrada) == esperado

    def test_dado_palavra_desconhecida_quando_translate_to_pt_entao_mantém_original(self):
        # palavra não está no dicionário — deve ser preservada
        assert translate_to_pt("xyzabc") == "xyzabc"

    def test_dado_frase_mista_quando_translate_to_pt_entao_traduz_palavras_conhecidas(self):
        # "Nursery Mirror" → "infantil espelho"
        resultado = translate_to_pt("Nursery Mirror")
        assert "infantil" in resultado
        assert "espelho" in resultado

    def test_dado_palavra_com_pontuacao_quando_translate_to_pt_entao_pontuacao_removida_antes(self):
        # "dog," deve ser traduzido como "cachorro" (a vírgula é stripped)
        resultado = translate_to_pt("dog,")
        assert resultado == "cachorro"

    def test_dado_entrada_maiuscula_quando_translate_to_pt_entao_case_insensitivo(self):
        assert translate_to_pt("DOG") == "cachorro"
        assert translate_to_pt("Dog") == "cachorro"

    def test_dado_multiplas_palavras_quando_translate_to_pt_entao_todas_traduzidas(self):
        resultado = translate_to_pt("dog cat bird")
        assert resultado == "cachorro gato pássaro"


# ════════════════════════════════════════════════════════
# translate_to_en
# ════════════════════════════════════════════════════════

class TestTranslateToEn:

    def test_dado_string_vazia_quando_translate_to_en_entao_retorna_vazia(self):
        assert translate_to_en("") == ""

    @pytest.mark.parametrize("entrada, esperado", [
        ("cachorro",     "dog"),
        ("gato",         "cat"),
        ("natal",        "christmas"),
        ("flor",         "flower"),
        ("estrela",      "star"),
        ("espelho",      "mirror"),
        ("madeira",      "wood"),
    ])
    def test_dado_palavra_pt_conhecida_quando_translate_to_en_entao_retorna_en(self, entrada, esperado):
        assert translate_to_en(entrada) == esperado

    def test_dado_palavra_desconhecida_quando_translate_to_en_entao_mantém_original(self):
        assert translate_to_en("xyzabc") == "xyzabc"

    def test_dado_entrada_maiuscula_quando_translate_to_en_entao_case_insensitivo(self):
        assert translate_to_en("CACHORRO") == "dog"


# ════════════════════════════════════════════════════════
# search_bilingual
# ════════════════════════════════════════════════════════

class TestSearchBilingual:

    # ZERO — entradas vazias
    def test_dado_query_vazia_quando_search_bilingual_entao_false(self):
        assert search_bilingual("", "Nursery Mirror") is False

    def test_dado_texto_vazio_quando_search_bilingual_entao_false(self):
        assert search_bilingual("mirror", "") is False

    def test_dado_ambos_vazios_quando_search_bilingual_entao_false(self):
        assert search_bilingual("", "") is False

    # Busca direta EN
    def test_dado_query_en_quando_texto_en_contem_entao_true(self):
        assert search_bilingual("mirror", "Nursery Mirror") is True

    # Busca via tradução PT → EN
    def test_dado_query_pt_quando_texto_en_tem_equivalente_entao_true(self):
        assert search_bilingual("espelho", "Nursery Mirror") is True

    def test_dado_query_pt_tema_quando_texto_en_tem_equivalente_entao_true(self):
        assert search_bilingual("natal", "Christmas Tree Design") is True

    # Busca não encontrada
    def test_dado_query_sem_relacao_quando_search_bilingual_entao_false(self):
        assert search_bilingual("tubarão", "Nursery Mirror") is False

    # Case insensitive
    def test_dado_query_maiuscula_quando_search_bilingual_entao_case_insensitivo(self):
        assert search_bilingual("MIRROR", "Nursery Mirror") is True

    # Integridade do dicionário
    def test_dado_dicionario_quando_todas_chaves_sao_strings_minusculas(self):
        for key in TRANSLATIONS:
            assert key == key.lower(), f"Chave não está em lowercase: '{key}'"

    def test_dado_dicionario_quando_todos_valores_sao_strings_nao_vazias(self):
        for key, value in TRANSLATIONS.items():
            assert isinstance(value, str), f"Valor não é string: '{key}'"
            assert len(value) > 0, f"Valor vazio para chave: '{key}'"
