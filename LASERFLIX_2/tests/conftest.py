"""
conftest.py — Fixtures compartilhadas entre todos os testes.

Metodologia Akita:
- Testes são especificações de comportamento, não scripts de validação.
- Cada fixture é mínima, autocontida e não depende de estado externo.
- Isolamento total: nenhum teste usa disco real; usa tmp_path do pytest.
- Nomenclatura: given_<estado> / when_<ação> / then_<resultado esperado>.

REGRA ABSOLUTA:
  Os arquivos de teste NUNCA são modificados após criação.
  O que se corrige é o código do app, não os testes.
"""
import json
import os
import pytest


# ─────────────────────────────────────────────────────────
# Fixtures de sistema de arquivos (isolamento em tmp_path)
# ─────────────────────────────────────────────────────────

@pytest.fixture
def tmp_db_file(tmp_path):
    """Arquivo database.json vazio em diretório temporário."""
    return str(tmp_path / "database.json")


@pytest.fixture
def tmp_config_file(tmp_path):
    """Arquivo config.json vazio em diretório temporário."""
    return str(tmp_path / "config.json")


@pytest.fixture
def tmp_collections_file(tmp_path):
    """Arquivo collections.json vazio em diretório temporário."""
    return str(tmp_path / "collections.json")


@pytest.fixture
def tmp_db_with_data(tmp_path):
    """
    database.json pré-populado com 3 projetos realistas.
    Usado para testes que exigem estado inicial não-vazio.
    """
    db = {
        "/projetos/natal_2024": {
            "name": "Natal 2024",
            "categories": ["Natal", "Datas Comemorativas"],
            "tags": ["arvore", "enfeite"],
            "description": "Artes de natal",
        },
        "/projetos/pascoa_2023": {
            "name": "Páscoa 2023",
            "categories": ["Páscoa"],
            "tags": ["coelho", "ovo"],
            "description": "Artes de páscoa",
        },
        "/projetos/dia_das_maes": {
            "name": "Dia das Mães",
            "categories": ["Datas Comemorativas"],
            "tags": ["flor", "presente"],
            "description": "Artes dia das mães",
        },
    }
    db_file = tmp_path / "database.json"
    db_file.write_text(json.dumps(db, ensure_ascii=False), encoding="utf-8")
    return str(db_file)


@pytest.fixture
def tmp_db_legacy(tmp_path):
    """
    database.json com schema LEGADO: campo 'category' (string) em vez de
    'categories' (lista). Verifica migração automática.
    """
    db = {
        "/projetos/natal_legacy": {
            "name": "Natal Legacy",
            "category": "Natal",
        },
        "/projetos/sem_cat": {
            "name": "Sem Categoria Legacy",
            "category": "Sem Categoria",
        },
    }
    db_file = tmp_path / "database.json"
    db_file.write_text(json.dumps(db, ensure_ascii=False), encoding="utf-8")
    return str(db_file)


@pytest.fixture
def tmp_db_corrupted(tmp_path):
    """database.json com JSON inválido (corrompido)."""
    db_file = tmp_path / "database.json"
    db_file.write_text("{invalid json{{{", encoding="utf-8")
    return str(db_file)


@pytest.fixture
def tmp_scan_tree(tmp_path):
    """
    Árvore de pastas simulando estrutura real de produtos.
    Inclui pastas com folder.jpg, pastas com arquivos válidos,
    pastas técnicas (a serem ignoradas) e pastas vazias.

    Estrutura:
        base/
          produto_natal/         ← tem folder.jpg  → detectado
            folder.jpg
            arte.svg
          produto_pascoa/        ← só .svg (sem folder.jpg) → detectado (hybrid)
            coelho.svg
          svg/                   ← pasta técnica → ignorada
            algo.svg
          vazio/                 ← sem arquivos válidos → ignorada
    """
    base = tmp_path / "base"

    # produto com folder.jpg
    p1 = base / "produto_natal"
    p1.mkdir(parents=True)
    (p1 / "folder.jpg").write_bytes(b"fake-jpg")
    (p1 / "arte.svg").write_bytes(b"<svg/>")

    # produto sem folder.jpg mas com arquivo válido
    p2 = base / "produto_pascoa"
    p2.mkdir(parents=True)
    (p2 / "coelho.svg").write_bytes(b"<svg/>")

    # pasta técnica — deve ser ignorada
    tech = base / "svg"
    tech.mkdir(parents=True)
    (tech / "algo.svg").write_bytes(b"<svg/>")

    # pasta vazia — deve ser ignorada
    empty = base / "vazio"
    empty.mkdir(parents=True)

    return str(base)


@pytest.fixture
def tmp_collections_with_data(tmp_path):
    """
    collections.json pré-populado com 2 coleções.
    """
    data = {
        "Favoritos": ["/projetos/natal_2024", "/projetos/pascoa_2023"],
        "Arquivados": ["/projetos/dia_das_maes"],
    }
    f = tmp_path / "collections.json"
    f.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return str(f)
