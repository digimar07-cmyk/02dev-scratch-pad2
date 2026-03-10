"""
╔══════════════════════════════════════════════════════════════════╗
║           CODE SMELL DETECTOR — LASERFLIX                        ║
║  Ferramentas: ruff + radon + vulture                              ║
║  Uso: python code_smell_check.py                                  ║
║  Gera: smell_report_YYYYMMDD_HHMMSS.txt na raiz                   ║
╚══════════════════════════════════════════════════════════════════╝
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


# ── Configuração ──────────────────────────────────────────────────────────────────────────────────

TARGET_DIRS = ["core", "ui", "config", "utils"]

# Thresholds de complexidade ciclomática
CC_THRESHOLD_WARN  = 5   # Amarelo
CC_THRESHOLD_ALERT = 10  # Vermelho — refatorar urgente

# Maintainability Index (0–100, maior = melhor)
MI_THRESHOLD = 20

# Confiança mínima do vulture (0–100)
VULTURE_MIN_CONFIDENCE = 60

REPORT_FILE = f"smell_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"


# ── Cores terminal ─────────────────────────────────────────────────────────────────────────────

class C:
    RED    = "\033[91m"
    YELLOW = "\033[93m"
    GREEN  = "\033[92m"
    CYAN   = "\033[96m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"
    DIM    = "\033[2m"

def red(t):    return f"{C.RED}{t}{C.RESET}"
def yellow(t): return f"{C.YELLOW}{t}{C.RESET}"
def green(t):  return f"{C.GREEN}{t}{C.RESET}"
def cyan(t):   return f"{C.CYAN}{t}{C.RESET}"
def bold(t):   return f"{C.BOLD}{t}{C.RESET}"
def dim(t):    return f"{C.DIM}{t}{C.RESET}"


# ── Helpers ──────────────────────────────────────────────────────────────────────────────────

def run(cmd: list[str]) -> tuple[int, str, str]:
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode, result.stdout, result.stderr


def check_tool(name: str) -> bool:
    code, _, _ = run([sys.executable, "-m", name, "--version"])
    return code == 0


def install_tool(name: str) -> None:
    print(f"  📦 Instalando {name}...")
    run([sys.executable, "-m", "pip", "install", name, "-q"])


def separator(title: str = "") -> str:
    width = 68
    if title:
        pad = (width - len(title) - 2) // 2
        return f"\n{'\u2550' * pad} {bold(title)} {'\u2550' * pad}\n"
    return f"\n{'\u2500' * width}\n"


# ── Dataclass de resultado ──────────────────────────────────────────────────────────────────

@dataclass
class SmellSummary:
    ruff_errors:     int = 0
    ruff_fixable:    int = 0
    cc_warnings:     int = 0
    cc_critical:     int = 0
    mi_bad:          int = 0
    dead_code:       int = 0
    worst_functions: list = field(default_factory=list)
    dead_items:      list = field(default_factory=list)


# ── Etapa 1: RUFF ─────────────────────────────────────────────────────────────────────────────

def run_ruff(targets: list[str], summary: SmellSummary) -> str:
    print(cyan("\n🔍 [1/3] RUFF — Smells de estilo, imports e lógica"))

    cmd = [sys.executable, "-m", "ruff", "check"] + targets + ["--output-format", "json"]
    _, stdout, _ = run(cmd)

    output_lines: list[str] = []
    category_count: dict[str, int] = {}

    try:
        issues = json.loads(stdout) if stdout.strip() else []
    except json.JSONDecodeError:
        issues = []
        output_lines.append(dim("  (saída JSON não disponível)"))

    fixable = 0
    for issue in issues:
        code = issue.get("code", "???")
        prefix = code[:2]
        category_count[prefix] = category_count.get(prefix, 0) + 1
        if issue.get("fix"):
            fixable += 1

    summary.ruff_errors  = len(issues)
    summary.ruff_fixable = fixable

    smell_map: dict[str, tuple[str, object]] = {
        "W" : ("⚠️  Whitespace/Style",        yellow),
        "UP": ("📦 Modernização Python",      yellow),
        "F" : ("🔴 Erros reais (imports/vars)", red),
        "B" : ("🐛 Bugs potenciais",           red),
        "E" : ("📐 Formatação",              yellow),
        "SI": ("🔄 Simplificação de código",  yellow),
        "I" : ("📋 Ordem de imports",         dim),
        "C" : ("🧩 Convenções",              dim),
    }

    for prefix, count in sorted(category_count.items(), key=lambda x: -x[1]):
        entry = smell_map.get(prefix, (f"[{prefix}]", dim))
        label, color_fn = entry
        output_lines.append(f"  {color_fn(label)}: {bold(str(count))} ocorrências")

    output_lines.append("")
    output_lines.append(f"  Total  : {bold(red(str(len(issues))))} issues")
    output_lines.append(f"  Fixável : {green(str(fixable))} (ruff check --fix)")

    result_text = "\n".join(output_lines)
    print(result_text)
    return result_text


# ── Etapa 2: RADON ────────────────────────────────────────────────────────────────────────────

def run_radon(targets: list[str], summary: SmellSummary) -> str:
    print(cyan("\n🧠 [2/3] RADON — Complexidade Ciclomática & Maintainability Index"))

    output_lines: list[str] = []

    # ── CC ──
    print(dim("  Calculando complexidade ciclomática..."))
    cmd_cc = [sys.executable, "-m", "radon", "cc"] + targets + [
        "--min", "B",
        "--show-complexity",
        "--average",
        "--json",
    ]
    _, stdout_cc, _ = run(cmd_cc)

    worst: list[tuple] = []

    try:
        cc_data = json.loads(stdout_cc) if stdout_cc.strip() else {}
        for filepath, blocks in cc_data.items():
            for block in blocks:
                cc     = block.get("complexity", 0)
                name   = block.get("name", "?")
                lineno = block.get("lineno", 0)
                letter = block.get("rank", "?")

                if cc >= CC_THRESHOLD_ALERT:
                    summary.cc_critical += 1
                    worst.append((filepath, name, cc, lineno, letter))
                    output_lines.append(
                        f"  {red('🔴 CRÍTICO')}  CC={bold(str(cc))} [{letter}]  "
                        f"{filepath}:{lineno} → {bold(name)}()"
                    )
                elif cc >= CC_THRESHOLD_WARN:
                    summary.cc_warnings += 1
                    worst.append((filepath, name, cc, lineno, letter))
                    output_lines.append(
                        f"  {yellow('🟡 ATENÇÃO')}  CC={bold(str(cc))} [{letter}]  "
                        f"{filepath}:{lineno} → {bold(name)}()"
                    )
    except (json.JSONDecodeError, TypeError):
        output_lines.append(dim("  (dados CC não disponíveis)"))

    summary.worst_functions = sorted(worst, key=lambda x: -x[2])[:10]

    if not output_lines:
        output_lines.append(green("  ✅ Nenhuma função com complexidade alta (CC < 5)"))

    # ── MI ──
    print(dim("  Calculando Maintainability Index..."))
    cmd_mi = [sys.executable, "-m", "radon", "mi"] + targets + ["--json"]
    _, stdout_mi, _ = run(cmd_mi)

    output_lines.append("")
    output_lines.append(bold("  📊 Maintainability Index (MI):"))

    try:
        mi_data = json.loads(stdout_mi) if stdout_mi.strip() else {}
        bad_files: list[tuple] = []
        for filepath, mi_info in mi_data.items():
            mi_val = mi_info.get("mi", 100)
            rank   = mi_info.get("rank", "?")
            if mi_val < MI_THRESHOLD:
                summary.mi_bad += 1
                bad_files.append((filepath, mi_val, rank))

        if bad_files:
            for fp, val, rank in sorted(bad_files, key=lambda x: x[1]):
                output_lines.append(
                    f"  {red('⚠️')} MI={bold(f'{val:.1f}')} [{rank}]  {fp}"
                )
        else:
            output_lines.append(green(f"  ✅ Todos os arquivos com MI >= {MI_THRESHOLD}"))

    except (json.JSONDecodeError, TypeError):
        output_lines.append(dim("  (dados MI não disponíveis)"))

    result_text = "\n".join(output_lines)
    print(result_text)
    return result_text


# ── Etapa 3: VULTURE ─────────────────────────────────────────────────────────────────────────

def run_vulture(targets: list[str], summary: SmellSummary) -> str:
    print(cyan("\n💀 [3/3] VULTURE — Dead Code (código morto/não utilizado)"))

    cmd = [
        sys.executable, "-m", "vulture",
        "--min-confidence", str(VULTURE_MIN_CONFIDENCE),
    ] + targets

    _, stdout, _ = run(cmd)

    output_lines: list[str] = []
    items: list[str] = []

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        items.append(line)

        low = line.lower()
        if "unused variable" in low:
            output_lines.append(f"  {dim('📦 var morta')}    {line}")
        elif "unused import" in low:
            output_lines.append(f"  {yellow('📥 import')}      {line}")
        elif "unused function" in low:
            output_lines.append(f"  {red('🔴 função')}      {line}")
        elif "unused class" in low:
            output_lines.append(f"  {red('🔴 classe')}      {line}")
        elif "unused attribute" in low:
            output_lines.append(f"  {yellow('🟡 atributo')}    {line}")
        else:
            output_lines.append(f"  {dim('❓')} {line}")

    summary.dead_code  = len(items)
    summary.dead_items = items[:20]

    if not output_lines:
        output_lines.append(green("  ✅ Nenhum dead code encontrado!"))
    else:
        output_lines.append(
            f"\n  Total dead code: {bold(red(str(len(items))))}  "
            f"(confiança >= {VULTURE_MIN_CONFIDENCE}%)"
        )

    result_text = "\n".join(output_lines)
    print(result_text)
    return result_text


# ── Score Final ─────────────────────────────────────────────────────────────────────────────

def calc_score(s: SmellSummary) -> tuple[int, str, str]:
    penalty  = min(s.ruff_errors  * 0.3,  20)
    penalty += min(s.cc_warnings  * 2,    15)
    penalty += min(s.cc_critical  * 5,    25)
    penalty += min(s.mi_bad       * 3,    20)
    penalty += min(s.dead_code    * 0.5,  20)
    score = max(0, int(100 - penalty))

    if score >= 80:
        return score, "A", green(f"✅ SAUDÁVEL ({score}/100)")
    if score >= 60:
        return score, "B", yellow(f"⚠️  ATENÇÃO ({score}/100)")
    if score >= 40:
        return score, "C", yellow(f"🔶 PROBLEMÁTICO ({score}/100)")
    return score, "D", red(f"🔴 CRÍTICO ({score}/100)")


def print_summary(s: SmellSummary, report_sections: list[str]) -> None:
    score, grade, label = calc_score(s)

    print(separator("📋 RESUMO FINAL"))

    rows = [
        ("Ruff issues",              str(s.ruff_errors),  red    if s.ruff_errors > 20 else yellow),
        ("  └ auto-fixáveis",        str(s.ruff_fixable), green),
        ("CC warnings  (CC 5–9)",    str(s.cc_warnings),  yellow if s.cc_warnings > 0 else green),
        ("CC críticos  (CC ≥ 10)",  str(s.cc_critical),  red    if s.cc_critical > 0 else green),
        ("MI baixo     (< 20)",       str(s.mi_bad),       red    if s.mi_bad > 0      else green),
        ("Dead code",                 str(s.dead_code),    yellow if s.dead_code > 5   else green),
    ]

    for lbl, val, color_fn in rows:
        print(f"  {lbl:<30} {color_fn(val)}")

    print(f"\n  {'Score de Saúde':<30} {label}")

    if s.worst_functions:
        print(bold("\n  🏆 TOP funções mais complexas:"))
        for fp, fn, cc, ln, lt in s.worst_functions[:5]:
            bar   = "█" * min(cc, 20)
            color = red if cc >= CC_THRESHOLD_ALERT else yellow
            print(f"    CC={color(str(cc))} {bar:<20} {fn}()  ({os.path.basename(fp)}:{ln})")

    print(bold("\n  💡 Próximos passos recomendados:"))
    if s.ruff_fixable > 0:
        print(f"    1. ruff check {' '.join(TARGET_DIRS)} --fix   ({s.ruff_fixable} auto-correções)")
    if s.cc_critical > 0:
        print(f"    2. Refatorar {s.cc_critical} função(oes) com CC ≥ 10 (extrair métodos)")
    if s.dead_code > 10:
        print(f"    3. Revisar dead code ({s.dead_code} itens) com vulture")
    if s.mi_bad > 0:
        print(f"    4. Melhorar legibilidade dos {s.mi_bad} arquivo(s) com MI baixo")
    if score >= 80:
        print(green("    ✅ Código em boa forma! Continue com os testes unitários."))

    _save_report(s, report_sections, score, grade)


def _save_report(s: SmellSummary, sections: list[str], score: int, grade: str) -> None:
    clean_sections = []
    for sec in sections:
        clean_sec = ""
        for ch in sec:
            if ord(ch) > 127:
                try:
                    ch.encode("utf-8")
                    clean_sec += ch
                except UnicodeEncodeError:
                    clean_sec += "?"
            else:
                clean_sec += ch
        clean_sections.append(clean_sec)

    lines = [
        "=" * 68,
        "  CODE SMELL REPORT — LASERFLIX",
        f"  Data : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"  Score: {score}/100  [Grau {grade}]",
        "=" * 68,
        "",
    ] + clean_sections + [
        "",
        "=" * 68,
        f"  RESUMO: ruff={s.ruff_errors} | CC_warn={s.cc_warnings} | "
        f"CC_crit={s.cc_critical} | MI_bad={s.mi_bad} | dead={s.dead_code}",
        "=" * 68,
    ]

    Path(REPORT_FILE).write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  📄 Relatório salvo: {bold(REPORT_FILE)}")


# ── Main ──────────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print(separator("🔬 CODE SMELL DETECTOR — LASERFLIX"))
    print(f"  Data    : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"  Targets : {', '.join(TARGET_DIRS)}")

    existing = [d for d in TARGET_DIRS if Path(d).exists()]
    if not existing:
        print(red("\n❌ Nenhuma pasta encontrada! Execute na raiz do projeto."))
        print(dim(f"   Esperado: {', '.join(TARGET_DIRS)}"))
        sys.exit(1)

    print(f"  Pastas  : {green(str(len(existing)))} encontradas de {len(TARGET_DIRS)}")

    print(bold("\n  🛠️  Verificando ferramentas..."))
    for tool in ["ruff", "radon", "vulture"]:
        if check_tool(tool):
            print(f"    {green('✅')} {tool}")
        else:
            print(f"    {yellow('⚠️')} {tool} não encontrado")
            install_tool(tool)

    summary = SmellSummary()
    sections: list[str] = []

    sections.append(run_ruff(existing, summary))
    sections.append(run_radon(existing, summary))
    sections.append(run_vulture(existing, summary))

    print_summary(summary, sections)


if __name__ == "__main__":
    main()
