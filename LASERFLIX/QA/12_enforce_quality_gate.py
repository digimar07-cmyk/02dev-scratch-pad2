from pathlib import Path
import sys

reports = Path("QA/reports")
out = reports / "12_quality_gate_summary.md"

def text(name: str) -> str:
    p = reports / name
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""

failures = []

smoke = text("09_smoke_pytest.txt")
unit = text("07_unit_pytest.txt")
integ = text("08_integration_pytest.txt")
mypy = text("03_mypy.txt")
ruff = text("02_ruff.txt")
pylint = text("02_pylint.txt")
dup = text("06_duplication.txt")

if "failed" in smoke.lower() or "error" in smoke.lower():
    failures.append("Smoke tests com falhas.")
if "failed" in unit.lower() or "error" in unit.lower():
    failures.append("Unit tests com falhas.")
if "failed" in integ.lower() or "error" in integ.lower():
    failures.append("Integration tests com falhas.")
if "error:" in mypy.lower() or "found " in mypy.lower():
    failures.append("Type checking com achados relevantes.")
if "DUPLICATION_GROUP" in dup:
    failures.append("Duplicação relevante detectada.")
if "F" in ruff or "E" in ruff:
    failures.append("Ruff apontou problemas.")
if "fatal" in pylint.lower() or "error" in pylint.lower() or "syntax-error" in pylint.lower():
    failures.append("Pylint apontou problemas relevantes.")

status = "APROVADO" if not failures else "REPROVADO"

lines = [
    "# Quality Gate",
    "",
    f"**Status geral:** {status}",
    "",
]

if failures:
    lines.append("## Motivos")
    for item in failures:
        lines.append(f"- {item}")
else:
    lines.append("Nenhuma falha crítica detectada.")

out.write_text("\n".join(lines), encoding="utf-8")
print(f"Quality gate summary written to: {out}")

sys.exit(1 if failures else 0)
