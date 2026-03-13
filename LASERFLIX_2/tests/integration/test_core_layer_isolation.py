"""
tests/integration/test_core_layer_isolation.py

Testes de isolamento e integracao da camada core/.
Dois tipos de testes aqui:
  1. Arquiteturais (AST/subprocess): garantem que fronteiras de camada nao sao violadas
  2. Comportamentais integrados: scan + database + collections trabalhando juntos

Metodologia Akita: sem mocks, usa filesystem real via tmp_path.
"""
import sys
import ast
import pytest
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def run_in_subprocess(code: str):
    """Executa codigo em subprocesso sem DISPLAY."""
    env = dict(__import__("os").environ)
    env.pop("DISPLAY", None)
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=20,
        cwd=str(ROOT),
        env=env,
    )
    return result.returncode, result.stdout, result.stderr


# ── Testes Arquiteturais (subprocess/AST) ──────────────────────────────────

class TestIsolamentoCamadas:

    def test_core_database_works_without_ui(self):
        """core.database deve funcionar sem nenhum import de UI."""
        code = f"""
import sys
sys.path.insert(0, r'{ROOT}')
from core.database import DatabaseManager
db = DatabaseManager()
db.set_project('/test', {{"name": "ok"}})
assert db.get_project('/test')["name"] == "ok"
print("OK")
"""
        rc, out, err = run_in_subprocess(code)
        assert rc == 0, f"core.database falhou sem UI:\n{err}"
        assert "OK" in out

    def test_core_collections_manager_works_without_ui(self):
        """core.collections_manager deve funcionar sem nenhum import de UI."""
        code = f"""
import sys, tempfile, os
sys.path.insert(0, r'{ROOT}')
from core.collections_manager import CollectionsManager
with tempfile.TemporaryDirectory() as tmp:
    cm = CollectionsManager(file_path=os.path.join(tmp, 'col.json'))
    cm.create_collection("Teste")
    assert "Teste" in cm.get_all_collections()
    print("OK")
"""
        rc, out, err = run_in_subprocess(code)
        assert rc == 0, f"core.collections_manager falhou:\n{err}"
        assert "OK" in out

    def test_utils_independent(self):
        """utils/ deve funcionar sem core/, ui/ e ai/."""
        code = f"""
import sys
sys.path.insert(0, r'{ROOT}')
from utils.text_utils import remove_accents, normalize_project_name
from utils.logging_setup import LOGGER
assert remove_accents("Natal") == "Natal"
print("OK")
"""
        rc, out, err = run_in_subprocess(code)
        assert rc == 0, f"utils falhou:\n{err}"
        assert "OK" in out

    def test_config_no_side_effects_on_import(self):
        """config/ nao deve criar arquivos ao ser importado."""
        code = f"""
import sys, os
sys.path.insert(0, r'{ROOT}')
before = set(os.listdir(r'{ROOT}'))
from config import constants, settings
after = set(os.listdir(r'{ROOT}'))
new_files = after - before
if new_files:
    print(f"SIDE_EFFECT: {{new_files}}")
    sys.exit(1)
print("OK")
"""
        rc, out, err = run_in_subprocess(code)
        assert rc == 0, f"config/ tem side effects ao importar:\n{out}\n{err}"


# ── Testes de Integracao Comportamental ───────────────────────────────────

class TestScanToDatabase:
    """
    Testa o fluxo completo: ProjectScanner + DatabaseManager trabalhando juntos.
    Cria pastas reais no disco, escaneia e verifica persistencia.
    """

    def test_scan_popula_database(self, tmp_path):
        """Scan de pasta real deve inserir projetos no DatabaseManager."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner

        # Cria 3 pastas de projeto no disco
        for nome in ["Luminaria Natal", "Porta Retrato", "Mandala Geometrica"]:
            (tmp_path / nome).mkdir()

        db = DatabaseManager(
            db_file=str(tmp_path / "db.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        scanner = ProjectScanner(db.database)
        count = scanner.scan_projects([str(tmp_path)])

        assert count == 3
        assert db.project_count() == 3

    def test_scan_nao_duplica_existentes(self, tmp_path):
        """Segundo scan na mesma pasta nao deve adicionar projetos ja presentes."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner

        (tmp_path / "Produto A").mkdir()
        (tmp_path / "Produto B").mkdir()

        db = DatabaseManager(
            db_file=str(tmp_path / "db.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        scanner = ProjectScanner(db.database)
        count1 = scanner.scan_projects([str(tmp_path)])
        count2 = scanner.scan_projects([str(tmp_path)])  # segundo scan

        assert count1 == 2
        assert count2 == 0  # nada novo
        assert db.project_count() == 2

    def test_scan_pasta_inexistente_nao_explode(self, tmp_path):
        """Scan de pasta que nao existe nao deve levantar excecao."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner

        db = DatabaseManager(
            db_file=str(tmp_path / "db.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        scanner = ProjectScanner(db.database)
        count = scanner.scan_projects([str(tmp_path / "nao_existe")])
        assert count == 0

    def test_scan_define_campos_obrigatorios(self, tmp_path):
        """Projeto inserido pelo scanner deve ter todos os campos obrigatorios."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner

        (tmp_path / "Meu Projeto").mkdir()

        db = DatabaseManager(
            db_file=str(tmp_path / "db.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        scanner = ProjectScanner(db.database)
        scanner.scan_projects([str(tmp_path)])

        path = str(tmp_path / "Meu Projeto")
        data = db.get_project(path)
        for campo in ["name", "categories", "tags", "analyzed", "favorite", "done", "added_date"]:
            assert campo in data, f"Campo obrigatorio ausente: {campo}"

    def test_scan_e_save_reload_roundtrip(self, tmp_path):
        """Projetos escaneados devem ser recuperados apos save/reload."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner

        for nome in ["Arvore", "Natal"]:
            (tmp_path / nome).mkdir()

        db_file = str(tmp_path / "db.json")
        cfg_file = str(tmp_path / "cfg.json")

        db1 = DatabaseManager(db_file=db_file, config_file=cfg_file)
        scanner = ProjectScanner(db1.database)
        scanner.scan_projects([str(tmp_path)])
        db1.save_database()

        db2 = DatabaseManager(db_file=db_file, config_file=cfg_file)
        db2.load_database()
        assert db2.project_count() == 2


class TestScanPlusCollections:
    """
    Testa integracao entre scan, database e collections.
    Scanner insere projetos; collections organiza os mesmos paths.
    """

    def test_path_escaneado_pode_ser_adicionado_a_colecao(self, tmp_path):
        """Path inserido pelo scanner deve ser reconhecido pelo CollectionsManager."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner
        from core.collections_manager import CollectionsManager

        (tmp_path / "Produto X").mkdir()

        db = DatabaseManager(
            db_file=str(tmp_path / "db.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        scanner = ProjectScanner(db.database)
        scanner.scan_projects([str(tmp_path)])

        cm = CollectionsManager(file_path=str(tmp_path / "col.json"))
        cm.create_collection("Favoritos")

        path = str(tmp_path / "Produto X")
        result = cm.add_project("Favoritos", path)
        assert result is True
        assert path in cm.get_projects("Favoritos")

    def test_orphan_cleanup_apos_remocao_do_disco(self, tmp_path):
        """Apos remover pasta do disco, clean_orphan_projects deve eliminar a referencia."""
        from core.database import DatabaseManager
        from core.project_scanner import ProjectScanner
        from core.collections_manager import CollectionsManager
        import shutil

        (tmp_path / "Projeto Permanente").mkdir()
        (tmp_path / "Projeto Temporario").mkdir()

        db = DatabaseManager(
            db_file=str(tmp_path / "db.json"),
            config_file=str(tmp_path / "cfg.json")
        )
        scanner = ProjectScanner(db.database)
        scanner.scan_projects([str(tmp_path)])

        cm = CollectionsManager(file_path=str(tmp_path / "col.json"))
        cm.create_collection("Tudo")
        for path in db.all_paths():
            cm.add_project("Tudo", path)

        assert cm.get_collection_size("Tudo") == 2

        # Remove uma pasta do disco
        shutil.rmtree(str(tmp_path / "Projeto Temporario"))

        # Simula o que o app faz: valid_paths = paths que ainda existem no disco
        import os
        valid_paths = {p for p in db.all_paths() if os.path.exists(p)}
        removed = cm.clean_orphan_projects(valid_paths)

        assert removed == 1
        assert cm.get_collection_size("Tudo") == 1
