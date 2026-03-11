import importlib.util
from pathlib import Path

def test_main_file_can_be_parsed() -> None:
    path = Path("main.py")
    assert path.exists()
    spec = importlib.util.spec_from_file_location("laserflix_main", path)
    assert spec is not None
    assert spec.loader is not None
