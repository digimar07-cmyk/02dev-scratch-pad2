"""
Testes de integracao: verifica isolamento real da camada core.
core/ deve funcionar sem tkinter no path.
Usa subprocesso isolado para evitar contaminar o processo de testes.
"""
import sys
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


def test_core_database_works_without_ui():
    """core.database deve funcionar sem nenhum import de UI."""
    code = f"""
import sys
sys.path.insert(0, r'{ROOT}')
from core.database import *
print("OK")
"""
    rc, out, err = run_in_subprocess(code)
    assert rc == 0, f"core.database falhou sem UI:\n{err}"
    assert "OK" in out


def test_core_collections_manager_works_without_ui():
    code = f"""
import sys
sys.path.insert(0, r'{ROOT}')
from core.collections_manager import *
print("OK")
"""
    rc, out, err = run_in_subprocess(code)
    assert rc == 0, f"core.collections_manager falhou:\n{err}"


def test_utils_independent():
    """utils/ deve funcionar sem core/, ui/ e ai/."""
    code = f"""
import sys
sys.path.insert(0, r'{ROOT}')
from utils.text_utils import *
from utils.platform_utils import *
from utils.logging_setup import LOGGER
print("OK")
"""
    rc, out, err = run_in_subprocess(code)
    assert rc == 0, f"utils falhou:\n{err}"


def test_config_no_side_effects_on_import():
    """config/ nao deve ter side effects ao ser importado."""
    code = f"""
import sys
import os
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
