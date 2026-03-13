"""
LASERFLIX QA - Gerador de Relatório Consolidado
Agrega todos os relatórios em um único arquivo auditável.
NAO altera thresholds. NAO filtra resultados.
"""
import os
import re
import datetime
from pathlib import Path

REPORTS_DIR = Path(__file__).parent / "reports"
OUTPUT_FILE = REPORTS_DIR / "CONSOLIDATED_REPORT.txt"

REPORT_FILES = {
    "LINT - RUFF": "ruff_report.txt",
    "LINT - PYLINT": "pylint_report.txt",
    "TYPE CHECK - BASEDPYRIGHT": "types_report.txt",
    "COMPLEXITY - CC": "complexity_cc_report.txt",
    "COMPLEXITY - MI": "complexity_mi_report.txt",
    "DEAD CODE - VULTURE": "dead_code_report.txt",
    "DUPLICATION - PYLINT": "duplication_report.txt",
    "TESTS UNIT": "pytest_unit.xml",
    "TESTS INTEGRATION": "pytest_integration.xml",
    "TESTS SMOKE": "pytest_smoke.xml",
}

EXIT_FILES = [
    "lint_exit_codes.txt",
    "types_exit_codes.txt",
    "complexity_exit_codes.txt",
    "dead_code_exit_codes.txt",
    "duplication_exit_codes.txt",
    "unit_exit_codes.txt",
    "integration_exit_codes.txt",
    "smoke_exit_codes.txt",
]


def read_exit_codes() -> dict:
    codes = {}
    for ef in EXIT_FILES:
        path = REPORTS_DIR / ef
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if "=" in line:
                    k, v = line.split("=", 1)
                    codes[k.strip()] = v.strip()
    return codes


def count_xml_failures(xml_path: Path) -> tuple:
    """Retorna (total_tests, failures+errors) sem suprimir erros."""
    if not xml_path.exists():
        return 0, -1  # -1 = arquivo nao encontrado = falha critica
    content = xml_path.read_text(encoding="utf-8", errors="replace")
    tests_m = re.search(r'tests="(\d+)"', content)
    fail_m = re.search(r'failures="(\d+)"', content)
    err_m = re.search(r'errors="(\d+)"', content)
    tests = int(tests_m.group(1)) if tests_m else 0
    failures = int(fail_m.group(1)) if fail_m else 0
    errors = int(err_m.group(1)) if err_m else 0
    return tests, failures + errors


def build_report():
    lines = []
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines.append("=" * 70)
    lines.append("  LASERFLIX QA \u2014 RELAT\u00d3RIO CONSOLIDADO")
    lines.append(f"  Gerado em: {now}")
    lines.append("=" * 70)
    lines.append("")

    exit_codes = read_exit_codes()
    lines.append("## EXIT CODES POR CATEGORIA")
    lines.append("-" * 40)
    for k, v in exit_codes.items():
        status = "OK" if v == "0" else "FALHOU"
        lines.append(f"  {k:40s} => {v}  [{status}]")
    lines.append("")

    lines.append("## RESULTADO DOS TESTES")
    lines.append("-" * 40)
    for label, filename in REPORT_FILES.items():
        if filename.endswith(".xml"):
            xml_path = REPORTS_DIR / filename
            total, failures = count_xml_failures(xml_path)
            if failures == -1:
                lines.append(f"  {label}: ARQUIVO NAO ENCONTRADO \u2014 CR\u00cdTICO")
            elif failures > 0:
                lines.append(f"  {label}: {failures}/{total} FALHOU")
            else:
                lines.append(f"  {label}: {total} testes OK")
    lines.append("")

    lines.append("## CONTE\u00daTO DOS RELAT\u00d3RIOS")
    lines.append("=" * 70)
    for label, filename in REPORT_FILES.items():
        if filename.endswith(".xml"):
            continue
        path = REPORTS_DIR / filename
        lines.append(f"\n### {label}")
        lines.append("-" * 40)
        if path.exists():
            content = path.read_text(encoding="utf-8", errors="replace")
            if content.strip():
                lines.append(content)
            else:
                lines.append("(arquivo vazio \u2014 poss\u00edvel aus\u00eancia de problemas ou erro de execu\u00e7\u00e3o)")
        else:
            lines.append("ARQUIVO NAO ENCONTRADO \u2014 Esta etapa nao foi executada.")

    lines.append("")
    lines.append("=" * 70)
    lines.append("  FIM DO RELAT\u00d3RIO CONSOLIDADO")
    lines.append("=" * 70)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Relat\u00f3rio consolidado salvo em: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_report()
