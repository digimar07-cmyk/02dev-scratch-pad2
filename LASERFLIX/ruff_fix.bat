@echo off
REM ╔══════════════════════════════════════════════════════════════════╗
REM ║  RUFF FIX — Auto-correção de Code Smells                        ║
REM ║  Uso: clique duplo ou execute no terminal                        ║
REM ║  Projeto: LASERFLIX                                              ║
REM ╚══════════════════════════════════════════════════════════════════╝

cd /d "%~dp0"

echo.
echo ════════════════════════════════════════════════════════════
echo   RUFF CHECK + FIX — LASERFLIX
echo ════════════════════════════════════════════════════════════
echo.

REM ── Verifica se ruff está instalado ─────────────────────────────────
python -m ruff --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] ruff nao encontrado. Instalando...
    python -m pip install ruff -q
)

echo [1/3] Verificando problemas ANTES do fix...
echo.
python -m ruff check core/ ui/controllers/ --statistics
echo.

echo ────────────────────────────────────────────────────────────
echo [2/3] Aplicando auto-correcoes (--fix)...
echo ────────────────────────────────────────────────────────────
echo.
python -m ruff check core/ ui/controllers/ --fix
echo.

echo ────────────────────────────────────────────────────────────
echo [3/3] Verificando problemas APOS o fix (os que restaram)...
echo ────────────────────────────────────────────────────────────
echo.
python -m ruff check core/ ui/controllers/ --statistics
echo.

echo ════════════════════════════════════════════════════════════
echo   CONCLUIDO! Os erros sem [*] precisam de correcao manual.
echo ════════════════════════════════════════════════════════════
echo.
pause
