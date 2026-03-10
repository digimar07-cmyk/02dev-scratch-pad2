"""
╔══════════════════════════════════════════════════════════════════╗
║  05 - CODE SMELL DETECTOR — LASERFLIX                            ║
║  Ferramentas: ruff + radon + vulture                             ║
║  Gera: QA/reports/05_smell_report_YYYYMMDD_HHMMSS.txt           ║
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

# ── Configuracao ──────────────────────────────────────────────────
TARGET_DIRS     = ["core", "ui", "config", "utils"]
REPORTS_DIR     = Path("QA/reports")
CC_WARN         = 5
CC_ALERT        = 10
MI_THRESHOLD    = 20
VULTURE_CONF    = 60
REPORT_FILE     = REPORTS_DIR / f"05_smell_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"


# ── Cores ─────────────────────────────────────────────────────────────────
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


# ── Helpers ────────────────────────────────────────────────────────────────
def run(cmd: list[str]) -> tuple[int, str, str]:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout, r.stderr

def check_tool(name: str) -> bool:
    code, _, _ = run([sys.executable, "-m", name, "--version"])
    return code == 0

def install_tool(name: str) -> None:
    print(f"  Instalando {name}...")
    run([sys.executable, "-m", "pip", "install", name, "-q"])

def sep(title: str = "") -> str:
    w = 68
    if title:
        p = (w - len(title) - 2) // 2
        return f"\n{'=' * p} {bold(title)} {'=' * p}\n"
    return f"\n{'-' * w}\n"


# ── Dataclass ─────────────────────────────────────────────────────────────────
@dataclass
class Summary:
    ruff_errors:     int  = 0
    ruff_fixable:    int  = 0
    cc_warnings:     int  = 0
    cc_critical:     int  = 0
    mi_bad:          int  = 0
    dead_code:       int  = 0
    worst_functions: list = field(default_factory=list)
    dead_items:      list = field(default_factory=list)


# ── Ruff ───────────────────────────────────────────────────────────────────
def run_ruff(targets: list[str], s: Summary) -> str:
    print(cyan("\n[1/3] RUFF"))
    cmd = [sys.executable, "-m", "ruff", "check"] + targets + ["--output-format", "json"]
    _, stdout, _ = run(cmd)
    lines: list[str] = []
    cat: dict[str, int] = {}
    try:
        issues = json.loads(stdout) if stdout.strip() else []
    except json.JSONDecodeError:
        issues = []
    fixable = 0
    for issue in issues:
        code = issue.get("code", "??")[:2]
        cat[code] = cat.get(code, 0) + 1
        if issue.get("fix"):
            fixable += 1
    s.ruff_errors  = len(issues)
    s.ruff_fixable = fixable
    smell_map = {
        "W" : ("[W]  Whitespace/Style",         yellow),
        "UP": ("[UP] Modernizacao Python",        yellow),
        "F" : ("[F]  Erros reais",                red),
        "B" : ("[B]  Bugs potenciais",            red),
        "E" : ("[E]  Formatacao",                 yellow),
        "SI": ("[SI] Simplificacao",              yellow),
        "I" : ("[I]  Ordem imports",              dim),
    }
    for prefix, count in sorted(cat.items(), key=lambda x: -x[1]):
        lbl, fn = smell_map.get(prefix, (f"[{prefix}]", dim))
        lines.append(f"  {fn(lbl)}: {bold(str(count))}")
    lines += ["", f"  Total   : {bold(red(str(len(issues))))}", f"  Fixavel : {green(str(fixable))}"]
    out = "\n".join(lines)
    print(out)
    return out


# ── Radon ──────────────────────────────────────────────────────────────────
def run_radon(targets: list[str], s: Summary) -> str:
    print(cyan("\n[2/3] RADON - Complexidade + Maintainability"))
    lines: list[str] = []
    worst: list[tuple] = []
    _, out_cc, _ = run([sys.executable, "-m", "radon", "cc"] + targets + ["--min", "B", "--show-complexity", "--json"])
    try:
        for fp, blocks in (json.loads(out_cc) if out_cc.strip() else {}).items():
            for b in blocks:
                cc, name, ln, rank = b.get("complexity",0), b.get("name","?"), b.get("lineno",0), b.get("rank","?")
                if cc >= CC_ALERT:
                    s.cc_critical += 1
                    worst.append((fp, name, cc, ln, rank))
                    lines.append(f"  {red('CRITICO')}  CC={bold(str(cc))} [{rank}]  {fp}:{ln} -> {bold(name)}()")
                elif cc >= CC_WARN:
                    s.cc_warnings += 1
                    worst.append((fp, name, cc, ln, rank))
                    lines.append(f"  {yellow('ATENCAO')}  CC={bold(str(cc))} [{rank}]  {fp}:{ln} -> {bold(name)}()")
    except (json.JSONDecodeError, TypeError):
        lines.append(dim("  (CC indisponivel)"))
    s.worst_functions = sorted(worst, key=lambda x: -x[2])[:10]
    if not lines:
        lines.append(green("  OK Nenhuma funcao com CC alto"))
    _, out_mi, _ = run([sys.executable, "-m", "radon", "mi"] + targets + ["--json"])
    lines += ["", bold("  Maintainability Index:")]
    try:
        bad: list[tuple] = []
        for fp, mi in (json.loads(out_mi) if out_mi.strip() else {}).items():
            v, r = mi.get("mi", 100), mi.get("rank", "?")
            if v < MI_THRESHOLD:
                s.mi_bad += 1
                bad.append((fp, v, r))
        if bad:
            for fp, v, r in sorted(bad, key=lambda x: x[1]):
                lines.append(f"  {red('AVISO')} MI={bold(f'{v:.1f}')} [{r}]  {fp}")
        else:
            lines.append(green(f"  OK Todos MI >= {MI_THRESHOLD}"))
    except (json.JSONDecodeError, TypeError):
        lines.append(dim("  (MI indisponivel)"))
    out = "\n".join(lines)
    print(out)
    return out


# ── Vulture ─────────────────────────────────────────────────────────────────
def run_vulture(targets: list[str], s: Summary) -> str:
    print(cyan("\n[3/3] VULTURE - Dead Code"))
    _, stdout, _ = run([sys.executable, "-m", "vulture", "--min-confidence", str(VULTURE_CONF)] + targets)
    lines: list[str] = []
    items: list[str] = []
    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        items.append(line)
        low = line.lower()
        if "unused function" in low:   lines.append(f"  {red('funcao')}     {line}")
        elif "unused class" in low:    lines.append(f"  {red('classe')}     {line}")
        elif "unused import" in low:   lines.append(f"  {yellow('import')}     {line}")
        elif "unused attribute" in low:lines.append(f"  {yellow('atributo')}   {line}")
        else:                           lines.append(f"  {dim('?')} {line}")
    s.dead_code  = len(items)
    s.dead_items = items[:20]
    if not lines:
        lines.append(green("  OK Nenhum dead code!"))
    else:
        lines.append(f"\n  Total: {bold(red(str(len(items))))} itens (confianca >= {VULTURE_CONF}%)")
    out = "\n".join(lines)
    print(out)
    return out


# ── Score ──────────────────────────────────────────────────────────────────
def calc_score(s: Summary) -> tuple[int, str, str]:
    p  = min(s.ruff_errors * 0.3, 20)
    p += min(s.cc_warnings * 2,   15)
    p += min(s.cc_critical * 5,   25)
    p += min(s.mi_bad      * 3,   20)
    p += min(s.dead_code   * 0.5, 20)
    score = max(0, int(100 - p))
    if score >= 80: return score, "A", green(f"OK SAUDAVEL ({score}/100)")
    if score >= 60: return score, "B", yellow(f"ATENCAO ({score}/100)")
    if score >= 40: return score, "C", yellow(f"PROBLEMATICO ({score}/100)")
    return score, "D", red(f"CRITICO ({score}/100)")


# ── Resumo + Salva ───────────────────────────────────────────────────────────────
def save_and_print_summary(s: Summary, sections: list[str]) -> None:
    score, grade, label = calc_score(s)
    print(sep("RESUMO FINAL"))
    rows = [
        ("Ruff issues",             str(s.ruff_errors),  red    if s.ruff_errors > 20 else yellow),
        ("  auto-fixaveis",         str(s.ruff_fixable), green),
        ("CC warnings  (CC 5-9)",   str(s.cc_warnings),  yellow if s.cc_warnings > 0 else green),
        ("CC criticos  (CC >= 10)", str(s.cc_critical),  red    if s.cc_critical > 0 else green),
        ("MI baixo     (< 20)",     str(s.mi_bad),       red    if s.mi_bad > 0      else green),
        ("Dead code",               str(s.dead_code),    yellow if s.dead_code > 5   else green),
    ]
    for lbl, val, fn in rows:
        print(f"  {lbl:<30} {fn(val)}")
    print(f"\n  {'Score de Saude':<30} {label}")
    if s.worst_functions:
        print(bold("\n  TOP funcoes mais complexas:"))
        for fp, fn_name, cc, ln, _ in s.worst_functions[:5]:
            bar   = "#" * min(cc, 20)
            color = red if cc >= CC_ALERT else yellow
            print(f"    CC={color(str(cc))} {bar:<20} {fn_name}()  ({os.path.basename(fp)}:{ln})")
    print(bold("\n  Proximos passos:"))
    if s.ruff_fixable > 0: print(f"    1. Execute 02_ruff_fix.bat ({s.ruff_fixable} auto-correcoes)")
    if s.cc_critical  > 0: print(f"    2. Refatorar {s.cc_critical} funcao(oes) CC >= 10")
    if s.dead_code    > 10:print(f"    3. Remover dead code ({s.dead_code} itens)")
    if s.mi_bad       > 0: print(f"    4. Melhorar {s.mi_bad} arquivo(s) com MI baixo")
    if score          >= 80:print(green("    OK Codigo saudavel!"))
    # Salva
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    clean = []
    for sec in sections:
        clean.append("".join(c if ord(c) < 128 else "?" for c in sec))
    lines = [
        "=" * 68,
        "  05 - CODE SMELL REPORT - LASERFLIX",
        f"  Data : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
        f"  Score: {score}/100  [Grau {grade}]",
        "=" * 68, "",
    ] + clean + [
        "", "=" * 68,
        f"  RESUMO: ruff={s.ruff_errors} | CC_warn={s.cc_warnings} | CC_crit={s.cc_critical} | MI_bad={s.mi_bad} | dead={s.dead_code}",
        "=" * 68,
    ]
    REPORT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Relatorio: {bold(str(REPORT_FILE))}")


# ── Main ───────────────────────────────────────────────────────────────────
def main() -> None:
    # Fix encoding para terminais Windows com cp1252 (evita crash com caracteres especiais)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print(sep("CODE SMELL DETECTOR - LASERFLIX"))
    print(f"  Data    : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    existing = [d for d in TARGET_DIRS if Path(d).exists()]
    if not existing:
        print(red("\nERRO: Execute na raiz do projeto LASERFLIX!"))
        sys.exit(1)
    print(f"  Pastas  : {green(str(len(existing)))} encontradas")
    print(bold("\n  Verificando ferramentas..."))
    for tool in ["ruff", "radon", "vulture"]:
        if check_tool(tool):
            print(f"    OK {tool}")
        else:
            print(f"    AVISO {tool} nao encontrado")
            install_tool(tool)
    s = Summary()
    secs: list[str] = []
    secs.append(run_ruff(existing, s))
    secs.append(run_radon(existing, s))
    secs.append(run_vulture(existing, s))
    save_and_print_summary(s, secs)

if __name__ == "__main__":
    main()
