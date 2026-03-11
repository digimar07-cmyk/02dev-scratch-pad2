"""
Verifica contratos de fronteira arquitetural:
- utils/ nao importa de ui/ nem de core/ nem de ai/
- config/ nao importa de ui/ nem de core/ nem de ai/
- ai/ nao importa de ui/
"""
import ast
import pytest
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent


def get_imports(filepath: Path) -> list:
    try:
        tree = ast.parse(filepath.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError as e:
        pytest.fail(f"SyntaxError em {filepath}: {e}")
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                result.append(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                result.append(node.module)
    return result


BOUNDARY_RULES = [
    ("utils", ["ui", "core", "ai"]),
    ("config", ["ui", "core", "ai"]),
    ("ai", ["ui"]),
]


def parametrize_violations():
    cases = []
    for module_dir, forbidden_prefixes in BOUNDARY_RULES:
        dir_path = ROOT / module_dir
        if dir_path.exists():
            for py_file in dir_path.rglob("*.py"):
                for forbidden in forbidden_prefixes:
                    cases.append((py_file, module_dir, forbidden))
    return cases


@pytest.mark.parametrize("py_file,module_dir,forbidden_prefix", parametrize_violations())
def test_module_boundary(py_file, module_dir, forbidden_prefix):
    """Verifica que modulos nao violam fronteiras arquiteturais."""
    imports = get_imports(py_file)
    violations = [
        i for i in imports
        if i == forbidden_prefix or i.startswith(forbidden_prefix + ".")
    ]
    rel = py_file.relative_to(ROOT)
    assert not violations, (
        f"VIOLACAO DE FRONTEIRA em {rel}:\n"
        f"  {module_dir}/ nao deveria importar de {forbidden_prefix}/\n"
        f"  Imports encontrados: {violations}"
    )
