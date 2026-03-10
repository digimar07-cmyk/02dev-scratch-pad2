"""
tests/test_database.py — TANAKA-03

Cobre: DatabaseManager.load_database, save_database, API pública (VOLKOV-01)
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from core.database import DatabaseManager


# ── Load ───────────────────────────────────────────────────────────────

class TestDatabaseLoad:
    def test_load_inexistente_retorna_vazio(self, tmp_db):
        tmp_db.load_database()
        assert tmp_db.database == {}

    def test_load_dados_existentes(self, tmp_db_with_data):
        assert "/proj/alpha" in tmp_db_with_data.database
        assert "/proj/beta" in tmp_db_with_data.database
        assert "/proj/gamma" in tmp_db_with_data.database

    def test_load_json_corrompido_retorna_vazio(self, tmp_path):
        db_file = str(tmp_path / "bad.json")
        Path(db_file).write_text("{INVALID JSON", encoding="utf-8")
        db = DatabaseManager(db_file=db_file)
        db.load_database()
        assert db.database == {}

    def test_load_usa_bak_quando_principal_corrompido(self, tmp_path):
        db_file = str(tmp_path / "db.json")
        bak_file = db_file + ".bak"
        Path(db_file).write_text("{INVALID", encoding="utf-8")
        Path(bak_file).write_text(
            json.dumps({"/proj/from_bak": {"name": "FromBak"}}),
            encoding="utf-8"
        )
        db = DatabaseManager(db_file=db_file)
        db.load_database()
        assert "/proj/from_bak" in db.database

    def test_load_migra_category_para_categories(self, tmp_path):
        db_file = str(tmp_path / "db.json")
        Path(db_file).write_text(
            json.dumps({"/proj/old": {"name": "Old", "category": "Motion"}}),
            encoding="utf-8"
        )
        db = DatabaseManager(db_file=db_file)
        db.load_database()
        assert "categories" in db.database["/proj/old"]
        assert "category" not in db.database["/proj/old"]
        assert db.database["/proj/old"]["categories"] == ["Motion"]


# ── Save ───────────────────────────────────────────────────────────────

class TestDatabaseSave:
    def test_save_persiste_em_disco(self, tmp_db_with_data, tmp_path):
        content = json.loads(Path(tmp_path / "test_db.json").read_text(encoding="utf-8"))
        assert "/proj/alpha" in content

    def test_save_cria_bak_na_segunda_gravacao(self, tmp_db_with_data, tmp_path):
        tmp_db_with_data.save_database()  # segunda vez — deve gerar .bak
        bak = tmp_path / "test_db.json.bak"
        assert bak.exists()

    def test_escrita_atomica_sem_arquivo_tmp(self, tmp_db_with_data, tmp_path):
        tmp_db_with_data.save_database()
        tmp_files = list(tmp_path.glob("*.tmp"))
        assert len(tmp_files) == 0

    def test_reload_apos_save_preserva_dados(self, tmp_db_with_data, tmp_path):
        db2 = DatabaseManager(db_file=str(tmp_path / "test_db.json"))
        db2.load_database()
        assert set(db2.database.keys()) == {"/proj/alpha", "/proj/beta", "/proj/gamma"}


# ── API Pública (VOLKOV-01) ───────────────────────────────────────────────

class TestDatabaseAPI:
    def test_get_project_existente(self, tmp_db_with_data):
        data = tmp_db_with_data.get_project("/proj/alpha")
        assert data is not None
        assert data["name"] == "Alpha"

    def test_get_project_inexistente_retorna_none(self, tmp_db_with_data):
        assert tmp_db_with_data.get_project("/proj/nao_existe") is None

    def test_set_project_insere(self, tmp_db):
        tmp_db.set_project("/proj/new", {"name": "New"})
        assert tmp_db.has_project("/proj/new")

    def test_set_project_atualiza(self, tmp_db_with_data):
        tmp_db_with_data.set_project("/proj/alpha", {"name": "Alpha Updated"})
        assert tmp_db_with_data.get_project("/proj/alpha")["name"] == "Alpha Updated"

    def test_remove_project_existente_retorna_true(self, tmp_db_with_data):
        result = tmp_db_with_data.remove_project("/proj/alpha")
        assert result is True
        assert not tmp_db_with_data.has_project("/proj/alpha")

    def test_remove_project_inexistente_retorna_false(self, tmp_db_with_data):
        result = tmp_db_with_data.remove_project("/proj/fantasma")
        assert result is False

    def test_has_project_true(self, tmp_db_with_data):
        assert tmp_db_with_data.has_project("/proj/beta") is True

    def test_has_project_false(self, tmp_db_with_data):
        assert tmp_db_with_data.has_project("/proj/nao_existe") is False

    def test_all_paths_retorna_todos(self, tmp_db_with_data):
        paths = tmp_db_with_data.all_paths()
        assert set(paths) == {"/proj/alpha", "/proj/beta", "/proj/gamma"}

    def test_all_projects_retorna_copia(self, tmp_db_with_data):
        copy = tmp_db_with_data.all_projects()
        copy["/proj/intruso"] = {}
        assert not tmp_db_with_data.has_project("/proj/intruso")

    def test_project_count(self, tmp_db_with_data):
        assert tmp_db_with_data.project_count() == 3

    def test_iter_projects(self, tmp_db_with_data):
        paths = [p for p, _ in tmp_db_with_data.iter_projects()]
        assert set(paths) == {"/proj/alpha", "/proj/beta", "/proj/gamma"}
