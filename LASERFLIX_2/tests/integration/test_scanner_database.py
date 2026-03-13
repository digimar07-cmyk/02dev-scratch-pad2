"""
tests/integration/test_scanner_database.py

Testes de INTEGRAÇÃO: RecursiveScanner → DatabaseManager pipeline.

Metodologia Akita:
- Testa o fluxo completo: escanear pasta → salvar no DB → consultar.
- Usa tmp_scan_tree (fixture) para simular estrutura real de disco.
- Sem disco de produção.
"""
import os
import sys
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from utils.recursive_scanner import RecursiveScanner
from core.database import DatabaseManager


class TestScannerDatabasePipeline:

    def test_dado_scan_hybrid_quando_resultado_salvo_no_db_entao_db_tem_projetos(
            self, tmp_scan_tree, tmp_db_file, tmp_config_file):
        # Arrange
        scanner = RecursiveScanner()
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)

        # Act
        products = scanner.scan_folders_hybrid(tmp_scan_tree)
        for product in products:
            db.set_project(product["path"], {"name": product["name"]})

        # Assert
        assert db.project_count() == len(products)
        assert db.project_count() > 0

    def test_dado_scan_pure_quando_resultado_salvo_no_db_entao_apenas_com_folder_jpg(
            self, tmp_scan_tree, tmp_db_file, tmp_config_file):
        # Arrange
        scanner = RecursiveScanner()
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)

        # Act
        products = scanner.scan_folders_pure(tmp_scan_tree)
        for product in products:
            db.set_project(product["path"], {"name": product["name"]})

        # Assert — modo pure só detecta pasta com folder.jpg
        paths_in_db = db.all_paths()
        for path in paths_in_db:
            assert os.path.exists(os.path.join(path, "folder.jpg"))

    def test_dado_db_populado_pelo_scanner_quando_save_e_load_entao_dados_intactos(
            self, tmp_scan_tree, tmp_db_file, tmp_config_file):
        # Arrange
        scanner = RecursiveScanner()
        db = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        products = scanner.scan_folders_hybrid(tmp_scan_tree)
        for product in products:
            db.set_project(product["path"], {"name": product["name"]})
        original_count = db.project_count()

        # Act — salva e recarrega
        db.save_database()
        db2 = DatabaseManager(db_file=tmp_db_file, config_file=tmp_config_file)
        db2.load_database()

        # Assert
        assert db2.project_count() == original_count
