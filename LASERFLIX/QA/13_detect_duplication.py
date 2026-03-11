from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import hashlib

ROOTS = ["ai", "config", "core", "ui", "utils"]
MIN_LINES = 20

def normalize(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#"):
            continue
        out.append(s)
    return out

def py_files() -> list[Path]:
    files: list[Path] = []
    for root in ROOTS:
        p = Path(root)
        if p.exists():
            files.extend(p.rglob("*.py"))
    main = Path("main.py")
    if main.exists():
        files.append(main)
    return sorted(set(files))

def main() -> None:
    blocks: dict[str, list[tuple[Path, int, int]]] = defaultdict(list)

    for path in py_files():
        text = path.read_text(encoding="utf-8", errors="replace").splitlines()
        cleaned = normalize(text)
        for i in range(0, max(0, len(cleaned) - MIN_LINES + 1)):
            block = cleaned[i:i + MIN_LINES]
            digest = hashlib.sha1("\n".join(block).encode("utf-8")).hexdigest()
            blocks[digest].append((path, i + 1, i + MIN_LINES))

    found = 0
    for _, refs in blocks.items():
        uniq = {(str(p), a, b) for p, a, b in refs}
        if len(uniq) > 1:
            found += 1
            print(f"DUPLICATION_GROUP {found}")
            for p, a, b in sorted(uniq):
                print(f"  - {p}:{a}-{b}")
            print()

    if found == 0:
        print("Nenhuma duplicação literal relevante encontrada.")
    else:
        print(f"Total duplication groups: {found}")

if __name__ == "__main__":
    main()
