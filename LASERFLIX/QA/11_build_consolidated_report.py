from pathlib import Path

REPORTS = Path("QA/reports")
OUT = REPORTS / "11_consolidated_report.md"

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        return f"[ERRO AO LER {path}: {exc}]"

REPORTS.mkdir(parents=True, exist_ok=True)

parts = [
    "# Relatório consolidado",
    "",
    "Este relatório consolida as saídas brutas da suíte de QA.",
    "",
]

targets = sorted(p for p in REPORTS.glob("*") if p.name != OUT.name)
if not targets:
    parts.append("Nenhum relatório encontrado.")
else:
    for path in targets:
        parts.append(f"## {path.name}")
        parts.append("```text")
        parts.append(read_text(path)[:30000])
        parts.append("```")
        parts.append("")

OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"Consolidated report written to: {OUT}")
