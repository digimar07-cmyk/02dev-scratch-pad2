"""
LASERFLIX QA \u2014 Quality Gate
Le os resultados reais dos relatorios e declara APROVADO ou REPROVADO.
NAO modifica thresholds em runtime.
NAO altera testes apos ver resultados.
Qualquer falha critica = REPROVADO imediato.

ATENCAO: Thresholds definidos ANTES de qualquer execucao.
Alterar esses valores apos ver resultados = MAQUIAGEM.
"""
import sys
import re
import datetime
from pathlib import Path

REPORTS_DIR = Path(__file__).parent / "reports"
GATE_OUTPUT = REPORTS_DIR / "QUALITY_GATE.txt"

# THRESHOLDS FIXADOS PRE-EXECUCAO
THRESHOLDS = {
    "ruff_errors_max": 0,
    "type_errors_max": 0,
    "unit_test_failures_max": 0,
    "integration_test_failures_max": 0,
    "smoke_test_failures_max": 0,
    "max_complexity_cc": 10,
    "max_duplicate_blocks": 20,
    "vulture_critical_min_confidence": 80,
}

CRITICAL_FAILURES = []
WARNINGS = []


def check_exit_code(filename: str, label: str, critical: bool = True):
    path = REPORTS_DIR / filename
    if not path.exists():
        msg = f"[CR\u00cdTICO] Arquivo de exit code nao encontrado: {filename} \u2014 etapa nao executada."
        CRITICAL_FAILURES.append(msg)
        return
    content = path.read_text(encoding="utf-8")
    for line in content.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            v = v.strip()
            if v != "0":
                msg = f"[FALHA] {label}: exit code {v}"
                if critical:
                    CRITICAL_FAILURES.append(msg)
                else:
                    WARNINGS.append(msg)


def check_xml_failures(filename: str, label: str):
    path = REPORTS_DIR / filename
    if not path.exists():
        CRITICAL_FAILURES.append(
            f"[CR\u00cdTICO] Relatorio XML nao encontrado: {filename} \u2014 testes nao foram executados."
        )
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    fail_m = re.search(r'failures="(\d+)"', content)
    err_m = re.search(r'errors="(\d+)"', content)
    failures = int(fail_m.group(1)) if fail_m else 0
    errors = int(err_m.group(1)) if err_m else 0
    total_fail = failures + errors
    if total_fail > 0:
        CRITICAL_FAILURES.append(
            f"[FALHA CR\u00cdTICA] {label}: {total_fail} teste(s) falharam."
        )


def check_complexity():
    path = REPORTS_DIR / "complexity_cc_report.txt"
    if not path.exists():
        WARNINGS.append("[AVISO] Relatorio de complexidade CC nao encontrado.")
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    violations = []
    for line in content.splitlines():
        match = re.search(r'- ([A-F]) \((\d+)\)', line)
        if match:
            score = int(match.group(2))
            if score > THRESHOLDS["max_complexity_cc"]:
                violations.append(f"  CC={score}: {line.strip()}")
    if violations:
        CRITICAL_FAILURES.append(
            f"[COMPLEXIDADE] {len(violations)} funcao(oes) excedem CC={THRESHOLDS['max_complexity_cc']}:\n"
            + "\n".join(violations[:20])
        )


def check_dead_code():
    path = REPORTS_DIR / "dead_code_report.txt"
    if not path.exists():
        WARNINGS.append("[AVISO] Relatorio de codigo morto nao encontrado.")
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    count = len([l for l in content.splitlines() if l.strip() and not l.startswith("#")])
    if count > 0:
        WARNINGS.append(
            f"[CODIGO MORTO] Vulture identificou {count} item(ns) potencialmente nao usados. Revisar."
        )


def check_duplication():
    path = REPORTS_DIR / "duplication_report.txt"
    if not path.exists():
        WARNINGS.append("[AVISO] Relatorio de duplicacao nao encontrado.")
        return
    content = path.read_text(encoding="utf-8", errors="replace")
    blocks = content.count("Similar lines in")
    if blocks > THRESHOLDS["max_duplicate_blocks"]:
        CRITICAL_FAILURES.append(
            f"[DUPLICACAO] {blocks} blocos similares detectados. Threshold: {THRESHOLDS['max_duplicate_blocks']}."
        )
    elif blocks > 0:
        WARNINGS.append(
            f"[DUPLICACAO] {blocks} bloco(s) similar(es) encontrado(s). Abaixo do threshold critico."
        )


def enforce():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    check_exit_code("lint_exit_codes.txt", "LINT (ruff)", critical=True)
    check_exit_code("types_exit_codes.txt", "TYPE CHECK (basedpyright)", critical=True)
    check_xml_failures("pytest_unit.xml", "TESTES UNIT\u00c1RIOS")
    check_xml_failures("pytest_integration.xml", "TESTES DE INTEGRA\u00c7\u00c3O")
    check_xml_failures("pytest_smoke.xml", "SMOKE + ESTRUTURAIS")
    check_complexity()
    check_dead_code()
    check_duplication()

    result = "REPROVADO" if CRITICAL_FAILURES else "APROVADO"

    lines = [
        "=" * 70,
        "  LASERFLIX QA \u2014 QUALITY GATE",
        f"  Executado em: {now}",
        f"  RESULTADO: *** {result} ***",
        "=" * 70,
        "",
    ]

    if CRITICAL_FAILURES:
        lines.append("## FALHAS CR\u00cdTICAS")
        lines.append("-" * 40)
        for f in CRITICAL_FAILURES:
            lines.append(f)
        lines.append("")

    if WARNINGS:
        lines.append("## AVISOS (nao reprovam, mas requerem revisao)")
        lines.append("-" * 40)
        for w in WARNINGS:
            lines.append(w)
        lines.append("")

    lines.append(f"Thresholds aplicados: {THRESHOLDS}")
    lines.append("AVISO: Qualquer alteracao de thresholds apos execucao = MAQUIAGEM.")

    GATE_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    report_text = "\n".join(lines)
    GATE_OUTPUT.write_text(report_text, encoding="utf-8")

    print(report_text)

    if CRITICAL_FAILURES:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    enforce()
