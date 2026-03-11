from pathlib import Path
import py_compile

def test_ui_tree_compiles() -> None:
    failures = []
    ui = Path("ui")
    if not ui.exists():
        raise AssertionError("Diretorio ui nao encontrado")
    for path in ui.rglob("*.py"):
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            failures.append(f"{path}: {exc}")
    assert not failures, "\n".join(failures)
