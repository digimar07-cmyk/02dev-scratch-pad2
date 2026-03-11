import importlib
from pathlib import Path

def package_modules(root: str) -> list[str]:
    base = Path(root)
    mods = []
    if not base.exists():
        return mods
    for path in base.rglob("*.py"):
        if path.name == "__init__.py":
            continue
        mods.append(".".join(path.with_suffix("").parts))
    return mods

def test_import_core_modules() -> None:
    failures = []
    for mod in package_modules("core"):
        try:
            importlib.import_module(mod)
        except Exception as exc:
            failures.append(f"{mod}: {exc}")
    assert not failures, "\n".join(failures)

def test_import_config_modules() -> None:
    failures = []
    for mod in package_modules("config"):
        try:
            importlib.import_module(mod)
        except Exception as exc:
            failures.append(f"{mod}: {exc}")
    assert not failures, "\n".join(failures)
