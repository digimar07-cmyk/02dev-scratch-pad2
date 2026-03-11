from pathlib import Path
import py_compile

def iter_py_files():
    for root in ["ai", "config", "core", "ui", "utils"]:
        p = Path(root)
        if p.exists():
            yield from p.rglob("*.py")
    main = Path("main.py")
    if main.exists():
        yield main

def test_python_files_compile_individually() -> None:
    failures = []
    for path in iter_py_files():
        try:
            py_compile.compile(str(path), doraise=True)
        except Exception as exc:
            failures.append(f"{path}: {exc}")
    assert not failures, "\n".join(failures)
