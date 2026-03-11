from pathlib import Path

def test_main_exists() -> None:
    assert Path("main.py").exists(), "main.py deve existir na raiz"

def test_expected_dirs_exist() -> None:
    for name in ["ai", "config", "core", "ui", "utils"]:
        assert Path(name).exists(), f"{name} deve existir"

def test_qa_folder_exists() -> None:
    assert Path("QA").exists(), "QA deve existir"
