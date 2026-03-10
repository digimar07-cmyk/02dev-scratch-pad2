@echo off
REM ╔══════════════════════════════════════════════════════════════╗
REM ║  RUFF CHECK — Somente leitura, SEM modificar o código       ║
REM ║  Projeto: LASERFLIX                                          ║
REM ║  Uso: clique duplo ou execute no terminal                    ║
REM ╚══════════════════════════════════════════════════════════════╝

cd /d "%~dp0"

echo.
echo ══════════════════════════════════════════════════════════════
echo   RUFF CHECK — LASERFLIX  (somente leitura, sem --fix)
echo ══════════════════════════════════════════════════════════════
echo.

REM ── Verifica se ruff está instalado ──────────────────────────
python -m ruff --version >nul 2>&1
if errorlevel 1 (
    echo [AVISO] ruff nao encontrado. Instalando...
    python -m pip install ruff -q
)

echo [1/2] Verificando: core/ ui/controllers/
echo ──────────────────────────────────────────────────────────────
echo.
python -m ruff check core/ ui/controllers/
echo.

echo ──────────────────────────────────────────────────────────────
echo [2/2] Resumo por categoria (--statistics)
echo ──────────────────────────────────────────────────────────────
echo.
python -m ruff check core/ ui/controllers/ --statistics
echo.

echo ══════════════════════════════════════════════════════════════
echo   CONCLUIDO! Nenhum arquivo foi modificado.
echo   Para auto-corrigir, rode: ruff_fix.bat
echo ══════════════════════════════════════════════════════════════
echo.
pause
