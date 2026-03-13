"""
Testa que core/ NAO importa tkinter nem modulos de ui/.
Esta e a violacao arquitetural mais critica do projeto.
Se core/ depende de UI, a camada de dados nao pode ser testada sem janela grafica.
"""
import ast
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
CORE_DIR = ROOT / "core"

UI_FORBIDDEN_IMPORTS = [
    "tkinter",
    "customtkinter",
    "ui",
]


def get_imports_from_file(filepath: Path) -> list:
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as e:
        pytest.fail(f"SyntaxError em {filepath}: {e}")
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)
    return imports


def get_core_py_files():
    return list(CORE_DIR.rglob("*.py"))


@pytest.mark.parametrize("py_file", get_core_py_files())
def test_core_file_has_no_ui_imports(py_file):
    """Nenhum arquivo em core/ pode importar tkinter ou modulos de ui/."""
    imports = get_imports_from_file(py_file)
    violations = []
    for imp in imports:
        for forbidden in UI_FORBIDDEN_IMPORTS:
            if imp == forbidden or imp.startswith(forbidden + "."):
                violations.append(f"Import proibido: '{imp}'")
    rel = py_file.relative_to(ROOT)
    assert not violations, (
        f"VIOLACAO ARQUITETURAL em {rel}:\n"
        + "\n".join(violations)
        + "\ncore/ nao pode depender de ui/ ou tkinter."
    )
