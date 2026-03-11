from __future__ import annotations

import subprocess


def test_no_pyc_tracked_by_git() -> None:
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        check=True,
    )

    tracked_files = [line.strip() for line in result.stdout.splitlines() if line.strip()]

    offenders = [
        path
        for path in tracked_files
        if path.endswith(".pyc") or "__pycache__/" in path or "__pycache__\\" in path
    ]

    assert not offenders, (
        "Arquivos de runtime versionados no repositório: " + ", ".join(offenders[:50])
    )