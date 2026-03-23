LASERFLIX AURUM V1.0 — GUIA COMPLETO DE DESENVOLVIMENTO
Documento para Continuação em Qualquer IA de Codificação
Para a IA que vai implementar: Este documento contém tudo que você precisa.
Leia do início ao fim antes de tocar em qualquer arquivo.
Código-fonte em: https://github.com/digimar07-cmyk/02dev-scratch-pad2/tree/main/LASERFLIX_2

ÍNDICE RÁPIDO
Contexto Completo do App
Arquitetura Atual — Mapa de Arquivos
Modelo de Dados (JSON)
Regras Absolutas — Não Violar
FASE 0 — Correção de Bugs e Fundação
FASE 1 — ttkbootstrap Darkly
FASE 2 — Hover Card
FASE 3 — Discovery Lanes
FASE 4 — Smart Folder Watcher
FASE 5 — Hash de Identidade e Git dos Makers
FASE 6 — Busca Semântica
FASE 7 — Calculadora de Precificação
Dependências Novas e requirements.txt Final
Sequência de Commits Recomendada
1. CONTEXTO COMPLETO DO APP
O que é o Laserflix
Organizador visual desktop de projetos de corte a laser. Metáfora: "Netflix de projetos". Grid de thumbnails navegável, busca em tempo real, filtros, coleções/playlists, e análise por IA local via Ollama.

Usuário-alvo: Maker artesão criativo, não programador. Usa LightBurn para criar designs. Tem 500-5000 projetos em pastas no Windows.

Stack:

Python 3.9+
Tkinter (stdlib) + ttk
JSON (persistência — SEM SQL)
Ollama local: qwen3.5:4b (análise IA) + nomic-embed-text (embeddings)
Pillow (thumbnails)
requests (HTTP para Ollama)
Entry point: main.py (< 30 linhas) → instancia LaserflixMainWindow

O que já funciona (NÃO REESCREVER)
FilterCache LRU com TTL (80% mais rápido em filtros)
ViewportManager — lazy rendering (60% mais rápido)
PredictivePreloader — pré-carrega próxima página
Sistema de coleções completo (backend + UI)
Análise IA com fallbacks por keyword
Busca bilíngue EN→PT (name_translator.py estático)
Filtros empilháveis com chips visuais
Modal de detalhes do projeto
Importação recursiva de pastas
Detecção de duplicatas por nome normalizado
Backup automático + versionamento semântico
2. ARQUITETURA ATUAL — MAPA DE ARQUIVOS
LASERFLIX_2/
├── main.py                        # Entry point — instancia LaserflixMainWindow
├── VERSION                        # "4.0.1.2"
├── requirements.txt               # Pillow, requests
│
├── config/
│   ├── settings.py                # VERSION, paths de arquivos de dados
│   ├── constants.py               # Cores, fontes, BANNED_STRINGS, extensões
│   ├── ui_constants.py            # Cores UI, limites de card, CARD_BANNED_STRINGS (DUPLICATA)
│   └── card_layout.py             # COLS=6, CARD_W=260, CARD_H=410, COVER_H=180, CARD_PAD=3
│
├── core/
│   ├── database.py                # DatabaseManager — load/save JSON, config
│   ├── collections_manager.py     # Coleções/playlists de projetos
│   ├── thumbnail_preloader.py     # ThreadPoolExecutor 4 workers, cache PIL
│   ├── project_scanner.py         # Scan de pastas, extração de tags de nome
│   └── performance/
│       ├── filter_cache.py        # LRU cache TTL para resultados filtrados
│       ├── viewport_manager.py    # Lazy rendering baseado em viewport
│       └── predictive_preloader.py # Prefetch de páginas
│
├── ai/
│   ├── ollama_client.py           # HTTP client para Ollama API  ← ZONA PROTEGIDA
│   ├── analysis_manager.py        # Coordena análise batch         ← ZONA PROTEGIDA
│   ├── text_generator.py          # Gera categorias + descrições   ← ZONA PROTEGIDA
│   ├── image_analyzer.py          # Análise visual de capa (Moondream) ← ZONA PROTEGIDA
│   ├── fallbacks.py               # Análise por keyword sem IA     ← ZONA PROTEGIDA
│   └── keyword_maps.py            # Dicionários de categorias      ← ZONA PROTEGIDA
│
├── ui/
│   ├── main_window.py             # Orquestrador principal (LaserflixMainWindow)
│   ├── project_card.py            # Factory de card individual
│   ├── project_modal.py           # Modal de detalhes (tela cheia)
│   ├── header.py                  # HeaderBar — logo, busca, menu
│   ├── sidebar.py                 # SidebarPanel — filtros categorizados
│   ├── edit_modal.py              # EditModal — editar categorias/tags
│   ├── theme.py                   # Constantes de tema (ACCENT_BLUE etc)
│   ├── import_mode_dialog.py      ← ZONA PROTEGIDA
│   ├── recursive_import_integration.py ← ZONA PROTEGIDA
│   ├── import_preview_dialog.py   ← ZONA PROTEGIDA
│   ├── duplicate_resolution_dialog.py  ← ZONA PROTEGIDA
│   │
│   ├── controllers/
│   │   ├── optimized_display_controller.py  # ÚNICO controller de display
│   │   ├── analysis_controller.py           # Análise IA + progress UI
│   │   ├── selection_controller.py          # Modo seleção múltipla
│   │   └── collection_controller.py         # CRUD de coleções
│   │
│   ├── managers/
│   │   ├── dialog_manager.py               # Abre todos os diálogos
│   │   ├── toggle_manager.py               # Toggle favorite/done/good/bad
│   │   ├── orphan_manager.py               # Limpeza de projetos órfãos
│   │   ├── modal_manager.py                # Coordena abertura de modais
│   │   ├── modal_generator.py              # Gera descrição no modal
│   │   ├── collection_dialog_manager.py    # Dialog de coleções
│   │   └── progress_ui_manager.py          # show/hide/update progress bar
│   │
│   ├── builders/
│   │   ├── ui_builder.py          # Constrói toda a UI (chamado em __init__)
│   │   ├── header_builder.py      # Header dinâmico com título e paginação
│   │   ├── cards_grid_builder.py  # Renderiza grid de cards
│   │   └── navigation_builder.py  # Paginação ⏮◀▶⏭
│   │
│   ├── bootstrap/
│   │   ├── core_setup.py          # Instancia DatabaseManager, OllamaClient, etc.
│   │   ├── managers_setup.py      # Instancia ToggleManager, OrphanManager, etc.
│   │   └── callbacks_setup.py     # Conecta todos os callbacks
│   │
│   ├── mixins/
│   │   ├── filter_mixin.py        # set_filter, _on_search, _apply_filter
│   │   ├── toggle_mixin.py        # toggle_favorite, toggle_done, remove_project
│   │   ├── modal_mixin.py         # open_project_modal, open_edit_mode
│   │   ├── selection_mixin.py     # Modo seleção múltipla
│   │   ├── collection_mixin.py    # open_collections_dialog
│   │   ├── dialog_mixin.py        # open_prepare_folders, open_model_settings
│   │   └── analysis_mixin.py      # analyze_single_project, analyze_only_new
│   │
│   └── components/
│       ├── chips_bar.py           # Barra de chips de filtros ativos
│       ├── selection_bar.py       # Barra de seleção múltipla
│       ├── status_bar.py          # Barra de status inferior
│       └── pagination_controls.py # Controles de paginação (cancelado, não usado)
│
├── utils/
│   ├── logging_setup.py           # Logger global LOGGER
│   ├── name_translator.py         # Dict estático EN→PT (busca bilíngue)
│   ├── text_utils.py              # normalize_project_name, remove_accents
│   ├── platform_utils.py          # open_file, open_folder (multiplataforma)
│   ├── duplicate_detector.py      ← ZONA PROTEGIDA
│   └── recursive_scanner.py       ← ZONA PROTEGIDA
│
└── tests/
    ├── conftest.py                # Fixtures pytest
    └── unit/                      # 14+ arquivos de teste
3. MODELO DE DADOS (JSON)
database.json — cada projeto é uma chave
{
  "C:/projetos/Natal 2024/": {
    "name": "Natal 2024",
    "origin": "Creative Fabrica",
    "favorite": true,
    "done": false,
    "good": true,
    "bad": false,
    "categories": ["Natal", "Datas Comemorativas", "Decoração"],
    "tags": ["arvore", "enfeite", "natal", "madeira"],
    "analyzed": true,
    "analyzed_model": "qwen3.5:4b",
    "ai_description": "Kit de decoração natalina com árvore estilizada...",
    "added_date": "2025-01-15T10:30:00",
    "name_pt": "Natal 2024"
  }
}
Chave: caminho absoluto da pasta (PROBLEMA — será corrigido na Fase 5)

config.json
{
  "scan_folders": ["C:/projetos", "D:/laser_designs"],
  "models": {
    "analysis": "qwen3.5:4b",
    "description": "qwen3.5:4b",
    "vision": "moondream",
    "embedding": "nomic-embed-text"
  },
  "ollama_url": "http://localhost:11434"
}
collections.json
{
  "Melhores de 2024": ["C:/projetos/Natal 2024/", "C:/projetos/Pascoa/"],
  "Para Vender": ["C:/projetos/Mesa Industrial/"]
}
4. REGRAS ABSOLUTAS — NÃO VIOLAR
4.1 — Zonas Protegidas (não tocar sem autorização explícita)
ai/ollama_client.py
ai/analysis_manager.py
ai/text_generator.py
ai/image_analyzer.py
ai/fallbacks.py
ai/keyword_maps.py
ui/import_mode_dialog.py
ui/recursive_import_integration.py
ui/import_preview_dialog.py
ui/duplicate_resolution_dialog.py
utils/recursive_scanner.py
utils/duplicate_detector.py
4.2 — Princípios da APP_PHILOSOPHY.md
100% offline: Zero cloud, zero API externa, sem conta obrigatória
Privacidade absoluta: Zero telemetria, projetos do usuário não saem da máquina
Roda em PCs modestos: IA é opcional. Sem IA, o app funciona com fallbacks por keyword
JSON, não SQL: Não migrar para SQLite sem autorização explícita do usuário
YAGNI radical: Não implementar nada que não esteja neste plano
4.3 — Regras de threading
NUNCA chamar widget.config() de dentro de uma thread daemon
Toda atualização de UI de dentro de thread → usar root.after(0, callback)
Exemplos corretos:
# ERRADO (causa RuntimeError aleatório):
threading.Thread(target=lambda: label.config(text="ok")).start()
# CORRETO:
def _update():
    label.config(text="ok")
root.after(0, _update)
4.4 — Padrão de importação
Sem imports circulares
Imports de core/ e ai/ → apenas via ui/bootstrap/core_setup.py
main_window.py não importa core/ diretamente
5. FASE 0 — CORREÇÃO DE BUGS E FUNDAÇÃO
Meta: Versão 4.1.0.0
Prioridade: BLOCKER — implementar antes de qualquer outra fase
Estimativa: 5-8 dias

BUG-01 — threading.Timer no debounce de busca
Arquivo: ui/header.py
Localização: método _debounced_search() (aproximadamente linha 54-60)
Código atual problemático:

def _debounced_search(self) -> None:
    if self._search_timer:
        self._search_timer.cancel()
    self._search_timer = threading.Timer(0.3, self._cb["on_search"])
    self._search_timer.start()
Problema: threading.Timer executa o callback em uma nova thread. on_search chama métodos Tkinter que só podem rodar na thread principal. Causa RuntimeError: main thread is not in main loop intermitente ao digitar rápido.

Correção — substituir completamente o método:

def _debounced_search(self) -> None:
    """Debounce 300ms usando root.after() — thread-safe."""
    if self._search_timer:
        # Cancela o after() agendado anteriormente
        self._root.after_cancel(self._search_timer)
    # Agenda na thread principal do Tkinter
    self._search_timer = self._root.after(300, self._cb["on_search"])
Ajuste necessário em __init__ de HeaderBar:
Adicionar self._root = parent (ou passar root como parâmetro adicional).
Alternativa mais simples: self._root = parent.winfo_toplevel() — obtém a janela raiz a partir de qualquer widget filho.

Como integrar winfo_toplevel():

def __init__(self, parent: tk.Widget, cb: dict):
    self._cb = cb
    self._select_btn = None
    self.search_var = tk.StringVar()
    self._search_timer = None
    self._root = None  # Será definido em _build()
    self.filter_btns = {}
    self._build(parent)
def _build(self, parent: tk.Widget) -> None:
    hdr = tk.Frame(parent, bg="#000000", height=70)
    hdr.pack(fill="x", side="top")
    hdr.pack_propagate(False)
    self._root = hdr.winfo_toplevel()  # ← ADICIONAR ESTA LINHA
    # ... resto do _build() sem alteração
BUG-02 — DatabaseManager sem RLock
Arquivo: core/database.py
Problema: ThumbnailPreloader (4 workers ThreadPoolExecutor) e AnalysisManager (threading.Thread daemon) escrevem no banco simultaneamente. Race condition possível.

Adicionar no __init__ de DatabaseManager:

import threading
import copy
class DatabaseManager:
    def __init__(self):
        # ... código existente ...
        self._lock = threading.RLock()  # ADICIONAR — RLock (reentrante)
Proteger os métodos críticos (sem mudar assinatura):

def save_database(self) -> None:
    """Salva database com lock."""
    with self._lock:
        snapshot = dict(self.database)  # Cópia rasa é suficiente aqui
    self._atomic_save(self.db_file, snapshot)  # Fora do lock (I/O não bloqueia DB)
def set_project(self, path: str, data: dict) -> None:
    """Define/atualiza um projeto."""
    with self._lock:
        self.database[path] = data
def get_project(self, path: str) -> dict:
    """Retorna cópia segura de um projeto."""
    with self._lock:
        return copy.copy(self.database.get(path, {}))
def all_projects(self) -> dict:
    """Retorna snapshot do banco (deepcopy protegido por lock)."""
    with self._lock:
        return copy.deepcopy(self.database)
Adicionar método de lazy view (resolve BUG-05 simultaneamente):

def get_page(self, paths: list, page: int, per_page: int) -> list:
    """
    Retorna apenas os projetos da página atual — sem deepcopy do banco inteiro.
    
    Args:
        paths: Lista de paths já filtrados e ordenados
        page: Página atual (1-indexed)
        per_page: Itens por página (padrão: 36)
    
    Returns:
        Lista de tuplas (path, data_copy) para a página
    """
    start = (page - 1) * per_page
    end = start + per_page
    page_paths = paths[start:end]
    with self._lock:
        return [(p, copy.copy(self.database[p])) for p in page_paths if p in self.database]
BUG-03 — BANNED_STRINGS duplicado
Arquivo 1: config/constants.py
Contém: BANNED_STRINGS = {"diversos", "data especial", ...}

Arquivo 2: config/ui_constants.py
Contém: CARD_BANNED_STRINGS = {"diversos", "data especial", ...} (com TODO comentado)

Correção em config/ui_constants.py:
Encontrar a seção CARD_BANNED_STRINGS (no final do arquivo) e substituir:

# ANTES (remover):
# NOTA: Duplicado de config.constants.BANNED_STRINGS para evitar import circular
# TODO: Resolver import circular e usar fonte única
CARD_BANNED_STRINGS = {
    "diversos",
    "data especial",
    "ambiente doméstico",
    "ambiente domestico",
    "sem categoria",
    "general",
    "miscellaneous",
    "uncategorized",
}
# DEPOIS (substituir por):
# Import lazy para evitar circular (constants não importa ui_constants)
def _get_banned_strings():
    from config.constants import BANNED_STRINGS
    return BANNED_STRINGS
CARD_BANNED_STRINGS = _get_banned_strings()
Verificar que ai/fallbacks.py importa de config.constants (correto) e ui/project_card.py importa CARD_BANNED_STRINGS de config.ui_constants (agora resolve para a mesma fonte).

BUG-04 — __import__ inline em main_window.py
Arquivo: ui/main_window.py
Problema: Algum método contém from utils.platform_utils import open_folder inline dentro de uma função. Padrão não-idiomático.

Correção: Mover o import para o topo do arquivo, junto dos outros imports:

# No topo de main_window.py, adicionar (se não existir):
from utils.platform_utils import open_file, open_folder
FASE 0.2 — Completar DOCTORAL_APPROVAL_PLAN
Test Coverage ≥ 60% (Dra. Tanaka)
Os arquivos de teste JÁ EXISTEM em tests/unit/. A infraestrutura está pronta (conftest.py com fixtures). O problema é que muitos testes provavelmente falham porque o código do app tem bugs.

Sequência:

Rodar pytest tests/ -v --cov=. --cov-report=term-missing para ver cobertura atual
Para cada teste que falha, corrigir o BUG no código do APP (nunca no teste)
Meta: ≥ 60% de cobertura nos módulos core/ e utils/
Arquivos de teste existentes (não modificar, só corrigir o app):

tests/unit/test_database.py
tests/unit/test_collections_manager.py
tests/unit/test_text_utils.py
tests/unit/test_duplicate_detector.py
tests/unit/test_recursive_scanner.py
tests/unit/test_virtual_scroll_manager.py
tests/unit/test_project_scanner.py
tests/unit/test_project_scanner_extended.py
tests/unit/test_name_translator.py
tests/unit/test_database_controller.py
tests/unit/test_database_extended.py
tests/unit/test_collections_manager_extended.py
tests/unit/test_collections_manager_extended2.py
tests/unit/test_virtual_scroll_extended.py
API Pública no DatabaseManager (Dr. Volkov)
Adicionar type hints completos e docstrings formais em core/database.py:

from typing import Dict, List, Optional, Tuple
import threading
import copy
class DatabaseManager:
    """
    Gerenciador do banco de dados de projetos.
    
    API Pública:
        load_config() -> None
        load_database() -> None
        save_database() -> None
        set_project(path: str, data: dict) -> None
        get_project(path: str) -> dict
        all_projects() -> dict
        get_page(paths: list, page: int, per_page: int) -> list
        remove_project(path: str) -> None
    
    Thread Safety: Todos os métodos de escrita são protegidos por RLock.
    """
    
    def load_config(self) -> None: ...
    def load_database(self) -> None: ...
    def save_database(self) -> None: ...
    def set_project(self, path: str, data: dict) -> None: ...
    def get_project(self, path: str) -> dict: ...
    def all_projects(self) -> Dict[str, dict]: ...
    def get_page(self, paths: List[str], page: int, per_page: int) -> List[Tuple[str, dict]]: ...
    def remove_project(self, path: str) -> None: ...
Decisão sobre virtual_scroll.py (Dr. Brandt)
Ação: Integrar virtual_scroll.py com o ViewportManager existente, ou remover se redundante.

Para verificar: grep -r "virtual_scroll" LASERFLIX_2/ --include="*.py" — se zero imports, remover o arquivo e registrar no DOCTORAL_APPROVAL_PLAN como "BRANDT-06: REMOVIDO — funcionalidade coberta por ViewportManager".

FASE 0.3 — Limpar estrutura de configuração
Mover version_manager.py e refactor_monitor.py da raiz para scripts/:

mkdir scripts/
mv version_manager.py scripts/
mv refactor_monitor.py scripts/
Atualizar referências: grep -r "version_manager\|refactor_monitor" . --include="*.py" e ajustar imports.

6. FASE 1 — ttkbootstrap Darkly
Meta: Versão 4.2.0.0
Estimativa: 3-5 dias
Dependência: Fase 0 completa

6.1 — Instalação
pip install ttkbootstrap>=1.10.0
Adicionar em requirements.txt:

ttkbootstrap>=1.10.0
6.2 — Integração em main.py
Arquivo: main.py
Alteração: Substituir tk.Tk() por ttk.Window:

# ANTES (código atual de main.py):
import tkinter as tk
from ui.main_window import LaserflixMainWindow
def main():
    root = tk.Tk()
    root.title("Laserflix")
    # ... configurações ...
    app = LaserflixMainWindow(root)
    root.mainloop()
if __name__ == "__main__":
    main()
# DEPOIS:
import ttkbootstrap as ttk
from ui.main_window import LaserflixMainWindow
def main():
    root = ttk.Window(themename="darkly")
    root.title("Laserflix")
    # ... mesmas configurações ...
    app = LaserflixMainWindow(root)
    root.mainloop()
if __name__ == "__main__":
    main()
6.3 — Ajuste de paleta
O tema "darkly" usa #2b2b2b como fundo, mas o Laserflix usa #141414 (BG_PRIMARY). Após criar o root, ajustar:

def main():
    root = ttk.Window(themename="darkly")
    
    # Sobrescrever paleta do tema para manter identidade do Laserflix
    style = ttk.Style()
    style.configure(".", background="#141414", foreground="#FFFFFF")
    style.configure("TFrame", background="#141414")
    style.configure("TLabel", background="#141414", foreground="#FFFFFF")
    style.configure("TButton", 
                    background="#2A2A2A", 
                    foreground="#FFFFFF",
                    borderwidth=0,
                    focuscolor="none")
    style.configure("TScrollbar", background="#333333", troughcolor="#1A1A1A")
    style.configure("Horizontal.TProgressbar",
                    background="#E50914",  # Netflix red
                    troughcolor="#2A2A2A")
    
    root.title("Laserflix")
    app = LaserflixMainWindow(root)
    root.mainloop()
6.4 — Atualizar widgets TTK existentes
Verificar em ui/builders/ui_builder.py e ui/sidebar.py:

# ANTES — ttk.Scrollbar explícito com orientação
scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=window.content_canvas.yview)
# DEPOIS — já funciona com o tema, mas adicionar style para scrollbar fina:
scrollbar = ttk.Scrollbar(content_frame, orient="vertical", 
                           command=window.content_canvas.yview,
                           style="Vertical.TScrollbar")
Nota: project_card.py usa tk.Frame e tk.Label com cores hardcoded — NÃO mudar. Os cards têm design próprio que não deve herdar o tema TTK.

6.5 — Verificação visual
Após implementar, verificar:

 Header preto com logo vermelho visível
 Sidebar escura com botões legíveis
 Scrollbars finas e discretas
 Progress bar vermelha (#E50914)
 Cards com BG_CARD (#2A2A2A) — sem herdar tema TTK
 Modal com fundo #0F0F0F
7. FASE 2 — HOVER CARD
Meta: Versão 4.3.0.0
Estimativa: 4-6 dias
Dependência: Fase 1 completa

7.1 — Criar ui/components/hover_card.py
Arquivo novo: ui/components/hover_card.py

"""
ui/components/hover_card.py — Overlay de informação ao passar o mouse no card.
Design: Frame overlay fixo no Canvas principal.
Instanciado UMA VEZ pelo UIBuilder. Reposicionado via show(path, widget).
Delay: 400ms antes de exibir (evita flash ao rolar).
Dimensão: 320×420px fixo.
Posição: À direita do card se há espaço, senão à esquerda.
"""
import os
import tkinter as tk
from tkinter import ttk
from typing import Optional
from config.ui_constants import (
    BG_CARD, BG_SECONDARY, FG_PRIMARY, FG_SECONDARY, FG_TERTIARY,
    ACCENT_RED, ACCENT_GOLD, ACCENT_GREEN
)
class HoverCard:
    """
    Overlay de hover que aparece 400ms após o mouse entrar em um card.
    
    Uso pelo UIBuilder:
        hover_card = HoverCard(parent=content_canvas, database=database,
                               thumbnail_preloader=thumb_preloader)
    
    Bind nos project_cards (via callback):
        card.bind("<Enter>", lambda e, p=path: hover_card.schedule_show(p, card))
        card.bind("<Leave>", lambda e: hover_card.cancel_and_hide())
    """
    
    WIDTH = 320
    HEIGHT = 420
    DELAY_MS = 400   # ms antes de exibir
    
    def __init__(self, parent: tk.Widget, database: dict, thumbnail_preloader):
        self.parent = parent
        self.database = database
        self.thumb = thumbnail_preloader
        
        self._timer: Optional[str] = None          # ID do root.after()
        self._current_path: Optional[str] = None
        self._frame: Optional[tk.Frame] = None
        self._root = parent.winfo_toplevel()
        
        self._build_frame()
    
    def _build_frame(self) -> None:
        """Constrói o frame overlay (invisível até show() ser chamado)."""
        self._frame = tk.Frame(
            self._root,                # Pai = janela raiz (flutua sobre tudo)
            bg="#1A1A1A",
            relief="flat",
            bd=1,
            highlightbackground="#444444",
            highlightthickness=1,
            width=self.WIDTH,
            height=self.HEIGHT,
        )
        self._frame.pack_propagate(False)
        
        # Thumbnail grande
        self._cover_label = tk.Label(self._frame, bg="#0A0A0A")
        self._cover_label.pack(fill="x", padx=10, pady=(10, 0))
        self._cover_label.config(width=self.WIDTH - 20, height=200)
        
        # Scroll interno para conteúdo
        self._info_canvas = tk.Canvas(self._frame, bg="#1A1A1A",
                                       highlightthickness=0, height=200)
        self._info_canvas.pack(fill="both", expand=True, padx=10, pady=5)
        
        self._info_frame = tk.Frame(self._info_canvas, bg="#1A1A1A")
        self._info_canvas.create_window((0, 0), window=self._info_frame, anchor="nw")
        self._info_frame.bind("<Configure>", lambda e: self._info_canvas.configure(
            scrollregion=self._info_canvas.bbox("all")))
    
    def schedule_show(self, project_path: str, card_widget: tk.Widget) -> None:
        """Agenda exibição após DELAY_MS. Cancela agendamento anterior."""
        self.cancel_and_hide()
        self._current_path = project_path
        self._timer = self._root.after(
            self.DELAY_MS,
            lambda: self._show_now(project_path, card_widget)
        )
    
    def cancel_and_hide(self) -> None:
        """Cancela agendamento pendente e esconde o overlay."""
        if self._timer:
            self._root.after_cancel(self._timer)
            self._timer = None
        self._frame.place_forget()
        self._current_path = None
    
    def _show_now(self, project_path: str, card_widget: tk.Widget) -> None:
        """Posiciona e exibe o hover card. Chamado pelo root.after()."""
        if not project_path or project_path not in self.database:
            return
        
        data = self.database[project_path]
        
        # Calcular posição
        try:
            cx = card_widget.winfo_rootx() - self._root.winfo_rootx()
            cy = card_widget.winfo_rooty() - self._root.winfo_rooty()
            cw = card_widget.winfo_width()
            rw = self._root.winfo_width()
        except tk.TclError:
            return  # Widget destruído durante o delay
        
        # Posicionar à direita do card se cabe, senão à esquerda
        if cx + cw + self.WIDTH + 10 < rw:
            x = cx + cw + 8
        else:
            x = cx - self.WIDTH - 8
        y = max(10, cy - 50)
        
        # Popular conteúdo
        self._populate(project_path, data)
        
        # Exibir
        self._frame.place(x=x, y=y, width=self.WIDTH, height=self.HEIGHT)
        self._frame.lift()  # Sempre acima de outros widgets
    
    def _populate(self, project_path: str, data: dict) -> None:
        """Preenche o hover card com dados do projeto."""
        # Limpar conteúdo anterior
        for w in self._info_frame.winfo_children():
            w.destroy()
        self._cover_label.config(image="", text="")
        
        # Thumbnail
        img = self.thumb.get_cached(project_path)
        if img:
            self._cover_label.config(image=img)
            self._cover_label.image = img  # Evitar GC
        else:
            self._cover_label.config(text="📁", font=("Arial", 48), fg="#555555")
        
        pad = {"padx": 8, "pady": 2, "anchor": "w"}
        
        # Nome completo (sem truncar)
        name = data.get("name_pt") or data.get("name", os.path.basename(project_path))
        tk.Label(self._info_frame, text=name,
                 font=("Arial", 11, "bold"), bg="#1A1A1A", fg=FG_PRIMARY,
                 wraplength=self.WIDTH - 20, justify="left").pack(**pad)
        
        # Descrição IA (se existir)
        desc = data.get("ai_description", "")
        if desc:
            preview = desc[:120] + "..." if len(desc) > 120 else desc
            tk.Label(self._info_frame, text=preview,
                     font=("Arial", 9), bg="#1A1A1A", fg=FG_SECONDARY,
                     wraplength=self.WIDTH - 20, justify="left").pack(**pad)
        
        # Separador
        tk.Frame(self._info_frame, bg="#333333", height=1).pack(fill="x", pady=4)
        
        # Categorias
        cats = data.get("categories", [])
        if cats:
            cat_text = "  •  ".join(cats[:5])
            tk.Label(self._info_frame, text=f"📂 {cat_text}",
                     font=("Arial", 9), bg="#1A1A1A", fg="#4ECDC4",
                     wraplength=self.WIDTH - 20, justify="left").pack(**pad)
        
        # Tags
        tags = data.get("tags", [])
        if tags:
            tag_text = "  #".join([""] + tags[:6]).strip()
            tk.Label(self._info_frame, text=tag_text,
                     font=("Arial", 9), bg="#1A1A1A", fg="#FFD700",
                     wraplength=self.WIDTH - 20, justify="left").pack(**pad)
        
        # Data de adição
        added = data.get("added_date", "")
        if added:
            try:
                from datetime import datetime
                dt = datetime.fromisoformat(added)
                date_str = dt.strftime("%d/%m/%Y")
                tk.Label(self._info_frame, text=f"📅 Adicionado em {date_str}",
                         font=("Arial", 9), bg="#1A1A1A", fg=FG_TERTIARY).pack(**pad)
            except Exception:
                pass
        
        # Status badges (linha)
        status_frame = tk.Frame(self._info_frame, bg="#1A1A1A")
        status_frame.pack(fill="x", padx=8, pady=4)
        
        if data.get("favorite"):
            tk.Label(status_frame, text="⭐", bg="#1A1A1A", font=("Arial", 14)).pack(side="left")
        if data.get("done"):
            tk.Label(status_frame, text="✓", bg="#1A1A1A", fg="#1DB954",
                     font=("Arial", 14, "bold")).pack(side="left")
        if data.get("good"):
            tk.Label(status_frame, text="👍", bg="#1A1A1A", font=("Arial", 14)).pack(side="left")
        
        # Arquivos do projeto
        try:
            files = [f for f in os.listdir(project_path)
                     if f.endswith((".lbrn2", ".svg", ".dxf", ".ai"))]
            if files:
                n = len(files)
                tk.Label(self._info_frame, text=f"📄 {n} arquivo(s) de design",
                         font=("Arial", 9), bg="#1A1A1A", fg=FG_TERTIARY).pack(**pad)
        except (PermissionError, FileNotFoundError):
            pass
7.2 — Integrar HoverCard no UIBuilder
Arquivo: ui/builders/ui_builder.py
Método: build(window)

Adicionar após a construção do canvas:

@staticmethod
def build(window) -> None:
    UIBuilder._build_header(window)
    UIBuilder._build_main_container(window)
    UIBuilder._build_status_bar(window)
    UIBuilder._build_hover_card(window)  # ← ADICIONAR
    UIBuilder._bind_keyboard_shortcuts(window)
@staticmethod
def _build_hover_card(window) -> None:
    """Instancia o HoverCard overlay (singleton por janela)."""
    from ui.components.hover_card import HoverCard
    window.hover_card = HoverCard(
        parent=window.content_canvas,
        database=window.database,
        thumbnail_preloader=window.thumbnail_preloader,
    )
7.3 — Adicionar callbacks de hover em project_card.py
Arquivo: ui/project_card.py
Função: build_card()

O cb dict já é passado para build_card. Adicionar duas entradas novas no cb:

cb["on_hover_show"] → lambda path, widget: hover_card.schedule_show(path, widget)
cb["on_hover_hide"] → lambda: hover_card.cancel_and_hide()
Em project_card.py, no final da função build_card(), antes do return:

# Hover card bindings (após criar todos os widgets)
if cb.get("on_hover_show") and cb.get("on_hover_hide"):
    def _bind_hover(widget, path=project_path):
        widget.bind("<Enter>", lambda e: cb["on_hover_show"](path, card))
        widget.bind("<Leave>", lambda e: cb["on_hover_hide"]())
        for child in widget.winfo_children():
            _bind_hover(child)
    _bind_hover(card)
7.4 — Conectar callbacks no cards_grid_builder.py
Arquivo: ui/builders/cards_grid_builder.py
Método: onde o cb dict é montado para build_card()

Adicionar:

cb = {
    # ... callbacks existentes ...
    "on_hover_show": lambda p, w: window.hover_card.schedule_show(p, w),
    "on_hover_hide": lambda: window.hover_card.cancel_and_hide(),
}
7.5 — Adicionar método get_cached no ThumbnailPreloader
Arquivo: core/thumbnail_preloader.py
Verificar se já existe método get_cached(project_path). Se não existir, adicionar:

def get_cached(self, project_path: str) -> Optional[ImageTk.PhotoImage]:
    """Retorna thumbnail cacheado ou None se não disponível."""
    return self._cache.get(project_path)
8. FASE 3 — DISCOVERY LANES
Meta: Versão 4.4.0.0
Estimativa: 2 semanas
Dependência: Fase 2 completa (hover card deve funcionar nas lanes)

8.1 — Criar core/session_manager.py
Arquivo novo: core/session_manager.py

"""
core/session_manager.py — Gerencia estado de sessão do usuário.
Persiste em: laserflix_session.json (mesmo diretório do database.json)
Dados salvos: projetos abertos recentemente, contagem de sessões.
"""
import json
import os
from datetime import datetime
from typing import List
from utils.logging_setup import LOGGER
class SessionManager:
    """
    Rastreia atividade do usuário para personalização das discovery lanes.
    
    API Pública:
        record_opened(path: str) -> None
        get_recently_opened(limit: int = 20) -> List[str]
        increment_session() -> None
        get_session_count() -> int
        save() -> None
        load() -> None
    """
    
    SESSION_FILE = "laserflix_session.json"
    MAX_RECENT = 30  # Máximo de projetos no histórico
    
    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Diretório onde ficam os arquivos JSON do app
        """
        self.session_file = os.path.join(data_dir, self.SESSION_FILE)
        self.logger = LOGGER
        
        self._recently_opened: List[dict] = []  # [{path, opened_at}]
        self._session_count: int = 0
        
        self.load()
    
    def record_opened(self, path: str) -> None:
        """Registra que um projeto foi aberto."""
        # Remove entrada anterior do mesmo projeto (se existir)
        self._recently_opened = [
            r for r in self._recently_opened if r["path"] != path
        ]
        # Adiciona no início
        self._recently_opened.insert(0, {
            "path": path,
            "opened_at": datetime.now().isoformat()
        })
        # Limita tamanho
        self._recently_opened = self._recently_opened[:self.MAX_RECENT]
        self.save()
    
    def get_recently_opened(self, limit: int = 20) -> List[str]:
        """Retorna lista de paths abertos recentemente (mais recente primeiro)."""
        return [r["path"] for r in self._recently_opened[:limit]]
    
    def increment_session(self) -> None:
        """Chamado ao iniciar o app. Incrementa contador de sessões."""
        self._session_count += 1
        self.save()
    
    def get_session_count(self) -> int:
        return self._session_count
    
    def save(self) -> None:
        data = {
            "recently_opened": self._recently_opened,
            "session_count": self._session_count,
            "version": 1,
        }
        try:
            tmp = self.session_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp, self.session_file)
        except Exception as e:
            self.logger.warning("Erro ao salvar session: %s", e)
    
    def load(self) -> None:
        if not os.path.exists(self.session_file):
            return
        try:
            with open(self.session_file, encoding="utf-8") as f:
                data = json.load(f)
            self._recently_opened = data.get("recently_opened", [])
            self._session_count = data.get("session_count", 0)
        except Exception as e:
            self.logger.warning("Erro ao carregar session: %s", e)
8.2 — Criar core/curation_engine.py
Arquivo novo: core/curation_engine.py

"""
core/curation_engine.py — Motor de curadoria das discovery lanes.
Decide o conteúdo de cada lane baseado em:
- Sessão do usuário (recentemente abertos)
- Estado do banco (favoritos, data de adição, categorias)
- Calendário (datas comemorativas próximas)
"""
import os
from datetime import datetime, timedelta
from typing import List, Dict
from utils.logging_setup import LOGGER
# Mapa de datas comemorativas (mês, dia): [categorias associadas]
UPCOMING_DATES_MAP = {
    (12, 25): ["Natal", "Noel", "Natalino"],
    (10, 31): ["Halloween", "Bruxa", "Abóbora"],
    (6, 12):  ["Dia dos Namorados", "Amor"],
    (5, 12):  ["Dia das Mães", "Mãe"],
    (8, 12):  ["Dia dos Pais", "Pai"],
    (4, 20):  ["Páscoa", "Coelho", "Ovo"],  # Data variável — aproximação
    (1, 1):   ["Ano Novo", "Réveillon"],
    (6, 24):  ["Festa Junina", "São João"],
    (9, 7):   ["7 de Setembro", "Brasil", "Independência"],
    (11, 2):  ["Dia de Finados", "Cemitério"],
}
UPCOMING_WINDOW_DAYS = 45  # Mostrar datas até X dias antes
class CurationEngine:
    """
    Seleciona projetos para cada discovery lane.
    
    Uso em HomeView:
        engine = CurationEngine(database, session_manager)
        lanes = engine.build_lanes()
        # lanes: [{"title": "...", "icon": "...", "projects": [...]}]
    """
    
    def __init__(self, database: dict, session_manager):
        self.database = database
        self.session = session_manager
        self.logger = LOGGER
    
    def build_lanes(self) -> List[Dict]:
        """
        Constrói todas as lanes disponíveis.
        Retorna lista de dicts com title, icon, projects (list de paths).
        Lanes vazias são omitidas.
        """
        lanes = []
        
        # 1. Recentemente abertos
        recent = self._get_recently_opened()
        if recent:
            lanes.append({"title": "Abertos Recentemente", "icon": "🕐",
                          "projects": recent, "filter_type": "recent"})
        
        # 2. Favoritos
        favorites = self._get_favorites()
        if favorites:
            lanes.append({"title": "Favoritos", "icon": "⭐",
                          "projects": favorites, "filter_type": "favorites"})
        
        # 3. Datas próximas (seasonal)
        seasonal = self._get_seasonal()
        lanes.extend(seasonal)
        
        # 4. Adicionados esta semana
        new_week = self._get_new_this_week()
        if new_week:
            lanes.append({"title": "Adicionados Esta Semana", "icon": "🆕",
                          "projects": new_week, "filter_type": "new_week"})
        
        # 5. Por categoria — top 5 categorias mais populares
        cat_lanes = self._get_category_lanes(max_lanes=5)
        lanes.extend(cat_lanes)
        
        # 6. Aguardando análise IA
        pending = self._get_pending_analysis()
        if pending:
            lanes.append({"title": "Aguardando Análise IA", "icon": "⏳",
                          "projects": pending, "filter_type": "pending"})
        
        return lanes
    
    def _get_recently_opened(self, limit: int = 15) -> List[str]:
        paths = self.session.get_recently_opened(limit=limit)
        # Filtra paths que ainda existem no banco E no disco
        return [p for p in paths if p in self.database and os.path.isdir(p)]
    
    def _get_favorites(self, limit: int = 20) -> List[str]:
        favs = [p for p, d in self.database.items()
                if d.get("favorite") and os.path.isdir(p)]
        # Ordenar por data de adição (mais recente primeiro)
        return sorted(favs,
                      key=lambda p: self.database[p].get("added_date", ""),
                      reverse=True)[:limit]
    
    def _get_seasonal(self) -> List[Dict]:
        """Retorna lanes de datas comemorativas próximas."""
        today = datetime.now()
        result = []
        
        for (month, day), keywords in UPCOMING_DATES_MAP.items():
            try:
                event_date = datetime(today.year, month, day)
                if event_date < today:
                    event_date = datetime(today.year + 1, month, day)
                
                days_until = (event_date - today).days
                if days_until > UPCOMING_WINDOW_DAYS:
                    continue
                
                # Buscar projetos com categorias/tags relacionadas
                projects = self._find_by_keywords(keywords, limit=15)
                if not projects:
                    continue
                
                title = keywords[0]  # Nome principal da data
                result.append({
                    "title": f"📅 {title} — daqui a {days_until} dias",
                    "icon": "📅",
                    "projects": projects,
                    "filter_type": "seasonal",
                })
            except ValueError:
                continue  # Data inválida (ex: 29/02 em ano não-bissexto)
        
        return result
    
    def _get_new_this_week(self, limit: int = 15) -> List[str]:
        cutoff = (datetime.now() - timedelta(days=7)).isoformat()
        new = [
            p for p, d in self.database.items()
            if d.get("added_date", "") >= cutoff and os.path.isdir(p)
        ]
        return sorted(new, key=lambda p: self.database[p].get("added_date", ""),
                       reverse=True)[:limit]
    
    def _get_category_lanes(self, max_lanes: int = 5) -> List[Dict]:
        """Retorna lanes das categorias mais populares."""
        # Contar frequência de categorias
        cat_count: Dict[str, int] = {}
        for data in self.database.values():
            for cat in data.get("categories", []):
                cat_count[cat] = cat_count.get(cat, 0) + 1
        
        # Top N categorias
        top_cats = sorted(cat_count.items(), key=lambda x: x[1], reverse=True)
        top_cats = [c for c, n in top_cats if n >= 3][:max_lanes]  # Mínimo 3 projetos
        
        lanes = []
        for cat in top_cats:
            projects = [
                p for p, d in self.database.items()
                if cat in d.get("categories", []) and os.path.isdir(p)
            ][:20]
            if projects:
                lanes.append({
                    "title": cat,
                    "icon": "🗂️",
                    "projects": projects,
                    "filter_type": "category",
                    "filter_value": cat,
                })
        return lanes
    
    def _get_pending_analysis(self, limit: int = 15) -> List[str]:
        pending = [p for p, d in self.database.items()
                   if not d.get("analyzed") and os.path.isdir(p)]
        return pending[:limit]
    
    def _find_by_keywords(self, keywords: List[str], limit: int = 15) -> List[str]:
        """Encontra projetos que contêm qualquer keyword em categorias ou tags."""
        kw_lower = [k.lower() for k in keywords]
        matches = []
        for path, data in self.database.items():
            if not os.path.isdir(path):
                continue
            all_text = " ".join(
                data.get("categories", []) + data.get("tags", [])
            ).lower()
            if any(kw in all_text for kw in kw_lower):
                matches.append(path)
        return matches[:limit]
8.3 — Criar ui/components/discovery_lane.py
Arquivo novo: ui/components/discovery_lane.py

"""
ui/components/discovery_lane.py — Lane horizontal de cards estilo Netflix.
Layout:
  [🕐 Título da Lane]              [Ver todos →]
  [card][card][card][card][card] ─────────────▶
Scroll horizontal via Shift+MouseWheel ou botões ◀ ▶.
"""
import tkinter as tk
from typing import List, Callable, Optional
from config.ui_constants import BG_PRIMARY, BG_SECONDARY, FG_PRIMARY, FG_SECONDARY, ACCENT_RED
from config.card_layout import CARD_W, CARD_H, CARD_PAD
class DiscoveryLane:
    """
    Uma lane horizontal de cards.
    
    Args:
        parent: Frame pai (a HomeView)
        title: Título da lane (ex: "Favoritos")
        icon: Emoji de ícone (ex: "⭐")
        project_paths: Lista de caminhos de projeto para exibir
        card_builder_fn: Função que cria um card — mesma assinatura de build_card()
        on_see_all: Callback quando "Ver todos →" é clicado — on_see_all(filter_type, filter_value)
        filter_type: "favorites", "recent", "category", etc.
        filter_value: Valor do filtro para on_see_all (ex: nome da categoria)
    """
    
    def __init__(self, parent: tk.Frame, title: str, icon: str,
                 project_paths: List[str], card_builder_fn: Callable,
                 on_see_all: Optional[Callable] = None,
                 filter_type: str = "all", filter_value: str = ""):
        
        self.parent = parent
        self.title = title
        self.icon = icon
        self.project_paths = project_paths
        self.card_builder_fn = card_builder_fn
        self.on_see_all = on_see_all
        self.filter_type = filter_type
        self.filter_value = filter_value
        
        self._frame: Optional[tk.Frame] = None
        self._canvas: Optional[tk.Canvas] = None
        self._cards_frame: Optional[tk.Frame] = None
        
        self._build()
    
    def _build(self) -> None:
        """Constrói a lane completa."""
        # Frame externo da lane
        self._frame = tk.Frame(self.parent, bg=BG_PRIMARY)
        self._frame.pack(fill="x", pady=(0, 20))
        
        # Header da lane: [ícone + título] [Ver todos →]
        header = tk.Frame(self._frame, bg=BG_PRIMARY)
        header.pack(fill="x", padx=20, pady=(0, 8))
        
        tk.Label(header, text=f"{self.icon}  {self.title}",
                 font=("Arial", 14, "bold"), bg=BG_PRIMARY, fg=FG_PRIMARY
                 ).pack(side="left")
        
        if self.on_see_all:
            see_all_btn = tk.Label(header, text="Ver todos →",
                                   font=("Arial", 10), bg=BG_PRIMARY, fg=ACCENT_RED,
                                   cursor="hand2")
            see_all_btn.pack(side="right")
            see_all_btn.bind("<Button-1>", lambda e: self.on_see_all(
                self.filter_type, self.filter_value))
        
        # Container do scroll horizontal
        scroll_container = tk.Frame(self._frame, bg=BG_PRIMARY)
        scroll_container.pack(fill="x", padx=20)
        
        # Canvas para scroll horizontal
        self._canvas = tk.Canvas(scroll_container, bg=BG_PRIMARY,
                                  highlightthickness=0,
                                  height=CARD_H + 10)
        self._canvas.pack(fill="x", expand=True)
        
        # Frame interno com os cards (dentro do canvas)
        self._cards_frame = tk.Frame(self._canvas, bg=BG_PRIMARY)
        canvas_window = self._canvas.create_window(
            (0, 0), window=self._cards_frame, anchor="nw"
        )
        
        # Atualizar scrollregion quando cards são adicionados
        self._cards_frame.bind("<Configure>", lambda e: self._canvas.configure(
            scrollregion=self._canvas.bbox("all")))
        
        # Bind Shift+MouseWheel para scroll horizontal
        self._canvas.bind("<Shift-MouseWheel>", self._on_horizontal_scroll)
        self._cards_frame.bind("<Shift-MouseWheel>", self._on_horizontal_scroll)
        
        # Renderizar cards
        self._render_cards()
        
        # Botões ◀ ▶ de navegação lateral
        self._add_nav_buttons(scroll_container)
    
    def _render_cards(self) -> None:
        """Renderiza os cards em linha horizontal."""
        for i, path in enumerate(self.project_paths):
            col_frame = tk.Frame(self._cards_frame, bg=BG_PRIMARY,
                                  width=CARD_W + CARD_PAD * 2)
            col_frame.pack(side="left", padx=CARD_PAD)
            col_frame.pack_propagate(False)
            
            try:
                card = self.card_builder_fn(col_frame, path, row=0, col=i)
                if card:
                    card.pack()
            except Exception as e:
                # Card com erro — mostrar placeholder
                tk.Label(col_frame, text="⚠️", bg="#2A2A2A",
                         font=("Arial", 24)).pack(expand=True)
    
    def _on_horizontal_scroll(self, event) -> None:
        """Scroll horizontal via Shift+MouseWheel."""
        self._canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def _add_nav_buttons(self, parent: tk.Frame) -> None:
        """Adiciona botões ◀ ▶ sobrepostos nas laterais (aparece no hover)."""
        # Implementação simples: botões sempre visíveis nas extremidades
        # Pode ser refinado para aparecer apenas no hover do container
        
        # Botão ◀ à esquerda
        left_btn = tk.Button(parent, text="◀", bg="#222222", fg=FG_PRIMARY,
                              font=("Arial", 12), relief="flat", cursor="hand2",
                              command=lambda: self._canvas.xview_scroll(-3, "units"))
        left_btn.place(x=0, rely=0.5, anchor="w", width=30, height=CARD_H)
        
        # Botão ▶ à direita
        right_btn = tk.Button(parent, text="▶", bg="#222222", fg=FG_PRIMARY,
                               font=("Arial", 12), relief="flat", cursor="hand2",
                               command=lambda: self._canvas.xview_scroll(3, "units"))
        right_btn.place(relx=1.0, rely=0.5, anchor="e", width=30, height=CARD_H)
    
    def destroy(self) -> None:
        """Remove a lane da tela."""
        if self._frame:
            self._frame.destroy()
8.4 — Criar ui/home_view.py
Arquivo novo: ui/home_view.py

"""
ui/home_view.py — Tela Home com discovery lanes estilo Netflix.
Substitui o grid paginado como tela padrão ao abrir o app.
Grid paginado continua disponível via "Ver todos →" em cada lane.
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable
from config.ui_constants import BG_PRIMARY, SCROLL_SPEED
from ui.components.discovery_lane import DiscoveryLane
class HomeView:
    """
    Tela Home com múltiplas discovery lanes em scroll vertical.
    
    Uso em UIBuilder:
        window.home_view = HomeView(
            parent=content_frame,
            curation_engine=window.curation_engine,
            card_builder_fn=window._build_card_for_lane,
            on_see_all=window._on_lane_see_all,
            hover_card=window.hover_card,
        )
    
    Ciclo de vida:
        home_view.show()    # Exibe a home (esconde grid paginado)
        home_view.hide()    # Esconde a home (exibe grid paginado)
        home_view.refresh() # Reconstrói lanes (chamar após _refresh_all)
    """
    
    def __init__(self, parent: tk.Frame, curation_engine, card_builder_fn: Callable,
                 on_see_all: Callable, hover_card=None):
        self.parent = parent
        self.curation_engine = curation_engine
        self.card_builder_fn = card_builder_fn
        self.on_see_all = on_see_all
        self.hover_card = hover_card
        
        self._lanes: list = []  # Instâncias de DiscoveryLane ativas
        self._visible = False
        
        # Canvas principal com scroll vertical
        self._canvas = tk.Canvas(parent, bg=BG_PRIMARY, highlightthickness=0)
        self._scrollbar = ttk.Scrollbar(parent, orient="vertical",
                                         command=self._canvas.yview)
        self._inner_frame = tk.Frame(self._canvas, bg=BG_PRIMARY)
        
        self._inner_frame.bind("<Configure>", lambda e: self._canvas.configure(
            scrollregion=self._canvas.bbox("all")))
        
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._inner_frame, anchor="nw")
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        
        # Bind scroll e resize
        self._canvas.bind("<MouseWheel>", self._on_scroll)
        self._canvas.bind("<Configure>", self._on_canvas_resize)
        self._inner_frame.bind("<MouseWheel>", self._on_scroll)
    
    def _on_scroll(self, event) -> None:
        self._canvas.yview_scroll(int(-1 * (event.delta / SCROLL_SPEED)), "units")
    
    def _on_canvas_resize(self, event) -> None:
        self._canvas.itemconfig(self._canvas_window, width=event.width)
    
    def show(self) -> None:
        """Exibe a HomeView."""
        self._canvas.pack(side="left", fill="both", expand=True)
        self._scrollbar.pack(side="right", fill="y")
        self._visible = True
        if not self._lanes:
            self.refresh()
    
    def hide(self) -> None:
        """Esconde a HomeView."""
        self._canvas.pack_forget()
        self._scrollbar.pack_forget()
        self._visible = False
    
    def refresh(self) -> None:
        """Reconstrói todas as lanes. Chamar após mudança no banco."""
        # Destruir lanes antigas
        for lane in self._lanes:
            lane.destroy()
        self._lanes.clear()
        
        # Reconstruir com dados atuais
        lanes_data = self.curation_engine.build_lanes()
        
        for lane_info in lanes_data:
            lane = DiscoveryLane(
                parent=self._inner_frame,
                title=lane_info["title"],
                icon=lane_info["icon"],
                project_paths=lane_info["projects"],
                card_builder_fn=self.card_builder_fn,
                on_see_all=self.on_see_all,
                filter_type=lane_info.get("filter_type", "all"),
                filter_value=lane_info.get("filter_value", ""),
            )
            self._lanes.append(lane)
    
    def is_visible(self) -> bool:
        return self._visible
8.5 — Integrar no main_window.py
Em ui/bootstrap/core_setup.py, adicionar:

from core.session_manager import SessionManager
from core.curation_engine import CurationEngine
class CoreSetup:
    def __init__(self):
        # ... código existente ...
        self.session_manager = SessionManager(data_dir=os.path.dirname(self.db_manager.db_file))
        self.session_manager.increment_session()
        self.curation_engine = CurationEngine(self.database, self.session_manager)
Em ui/modal_mixin.py, no método open_project_modal, adicionar ao início:

def open_project_modal(self, project_path: str) -> None:
    self.session_manager.record_opened(project_path)  # ← ADICIONAR
    if self.selection_ctrl.selection_mode:
        ...
Em ui/builders/ui_builder.py, método build(), adicionar:

UIBuilder._build_home_view(window)
@staticmethod
def _build_home_view(window) -> None:
    """Instancia a HomeView."""
    from ui.home_view import HomeView
    window.home_view = HomeView(
        parent=window.content_frame,  # Frame do content_frame existente
        curation_engine=window.curation_engine,
        card_builder_fn=window._build_card_for_lane,
        on_see_all=window._on_lane_see_all,
        hover_card=window.hover_card,
    )
    window.home_view.show()  # Home é a tela padrão
Adicionar métodos em main_window.py (via mixin ou diretamente):

def _build_card_for_lane(self, parent, project_path, row=0, col=0):
    """Constrói um card para uso nas discovery lanes."""
    from ui.project_card import build_card
    return build_card(
        parent=parent,
        project_path=project_path,
        data=self.database.get(project_path, {}),
        row=row, col=col,
        cb=self._get_card_callbacks(),  # Método que monta o cb dict
        thumbnail_preloader=self.thumbnail_preloader,
        collections_manager=self.collections_manager,
    )
def _on_lane_see_all(self, filter_type: str, filter_value: str) -> None:
    """Ao clicar em 'Ver todos →' em uma lane — vai para grid filtrado."""
    self.home_view.hide()
    # Aplicar filtro correspondente
    if filter_type == "favorites":
        self.set_filter("favorites")
    elif filter_type == "category" and filter_value:
        self._on_category_filter([filter_value])
    elif filter_type == "recent":
        self.set_filter("recent")  # Adicionar esse filtro no display_controller
    # O grid paginado já está configurado, basta exibir
    self.display_projects()
9. FASE 4 — SMART FOLDER WATCHER
Meta: Versão 4.5.0.0
Estimativa: 3-4 dias
Dependência: Pode ser desenvolvida em paralelo com Fase 3

9.1 — Instalação
pip install watchdog>=4.0.0
Adicionar em requirements.txt: watchdog>=4.0.0

9.2 — Criar core/folder_watcher.py
Arquivo novo: core/folder_watcher.py

"""
core/folder_watcher.py — Monitoramento automático de pastas de projetos.
Usa watchdog para detectar novos projetos quando o usuário salva no LightBurn.
Debounce de 2s (LightBurn salva múltiplos arquivos em sequência).
Notifica via callback thread-safe (root.after).
"""
import os
import threading
from typing import Callable, List, Optional
from utils.logging_setup import LOGGER
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileCreatedEvent, DirCreatedEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    LOGGER.warning("watchdog não instalado — Smart Folder Watcher desabilitado")
class _LaserflixEventHandler(FileSystemEventHandler if WATCHDOG_AVAILABLE else object):
    """Handler de eventos do watchdog."""
    
    # Extensões que indicam um arquivo de design relevante
    DESIGN_EXTENSIONS = {".lbrn2", ".lbrn", ".svg", ".dxf", ".ai", ".eps"}
    # Pastas técnicas a ignorar
    IGNORED_FOLDERS = {"__pycache__", ".git", "node_modules", ".tmp", "Thumbs.db"}
    
    def __init__(self, on_new_project: Callable, on_new_file: Callable,
                 database: dict, root_tk=None):
        if WATCHDOG_AVAILABLE:
            super().__init__()
        self.on_new_project = on_new_project
        self.on_new_file = on_new_file
        self.database = database
        self.root_tk = root_tk
        self._timers: dict = {}  # {path: threading.Timer}
        self.logger = LOGGER
    
    def on_created(self, event):
        path = event.src_path
        
        # Ignorar pastas técnicas
        if any(ig in path for ig in self.IGNORED_FOLDERS):
            return
        
        if event.is_directory:
            self._debounce_check(path, self._check_new_project)
        elif os.path.splitext(path)[1].lower() in self.DESIGN_EXTENSIONS:
            # Novo arquivo de design em pasta existente
            folder = os.path.dirname(path)
            if folder in self.database:
                self._debounce_check(folder, lambda p: self._notify_new_file(path, p))
    
    def _debounce_check(self, path: str, fn: Callable, delay: float = 2.0) -> None:
        """Cancela timer anterior e agenda novo."""
        if path in self._timers:
            self._timers[path].cancel()
        timer = threading.Timer(delay, fn, args=(path,))
        timer.daemon = True
        timer.start()
        self._timers[path] = timer
    
    def _check_new_project(self, folder_path: str) -> None:
        """Verifica se a nova pasta é um projeto válido."""
        if not os.path.isdir(folder_path):
            return
        if folder_path in self.database:
            return  # Já existe no banco
        
        # Verificar se tem pelo menos um arquivo de design
        try:
            files = os.listdir(folder_path)
            has_design = any(
                os.path.splitext(f)[1].lower() in self.DESIGN_EXTENSIONS
                for f in files
            )
        except (PermissionError, FileNotFoundError):
            return
        
        if has_design:
            self.logger.info("Watcher: novo projeto detectado: %s", folder_path)
            if self.root_tk:
                self.root_tk.after(0, lambda: self.on_new_project(folder_path))
    
    def _notify_new_file(self, file_path: str, folder_path: str) -> None:
        """Notifica que novo arquivo foi adicionado em projeto existente."""
        self.logger.info("Watcher: novo arquivo em projeto: %s", file_path)
        if self.root_tk:
            self.root_tk.after(0, lambda: self.on_new_file(file_path, folder_path))
class FolderWatcher:
    """
    Monitora pastas configuradas para detectar novos projetos.
    
    Uso em CoreSetup:
        watcher = FolderWatcher(
            database=db_manager.database,
            on_new_project=lambda path: ...,  # Callback na thread principal
            on_new_file=lambda file, folder: ...,
        )
        watcher.start(folders=config["scan_folders"], root_tk=root)
        # No teardown:
        watcher.stop()
    """
    
    def __init__(self, database: dict, on_new_project: Callable, on_new_file: Callable):
        self.database = database
        self.on_new_project = on_new_project
        self.on_new_file = on_new_file
        self.logger = LOGGER
        self._observer: Optional[object] = None
        self._running = False
    
    def start(self, folders: List[str], root_tk=None) -> bool:
        """
        Inicia monitoramento das pastas.
        
        Returns:
            True se iniciado com sucesso, False se watchdog não disponível
        """
        if not WATCHDOG_AVAILABLE:
            self.logger.warning("watchdog não instalado — Folder Watcher inativo")
            return False
        
        handler = _LaserflixEventHandler(
            on_new_project=self.on_new_project,
            on_new_file=self.on_new_file,
            database=self.database,
            root_tk=root_tk,
        )
        
        self._observer = Observer()
        for folder in folders:
            if os.path.isdir(folder):
                self._observer.schedule(handler, folder, recursive=False)
                self.logger.info("Watcher: monitorando %s", folder)
        
        self._observer.start()
        self._running = True
        self.logger.info("Smart Folder Watcher iniciado (%d pastas)", len(folders))
        return True
    
    def stop(self) -> None:
        """Para o monitoramento."""
        if self._observer and self._running:
            self._observer.stop()
            self._observer.join(timeout=3.0)
            self._running = False
            self.logger.info("Smart Folder Watcher parado")
    
    def is_running(self) -> bool:
        return self._running
9.3 — Criar ui/components/toast_bar.py
Arquivo novo: ui/components/toast_bar.py

"""
ui/components/toast_bar.py — Banner de notificação não-intrusivo.
Aparece no topo por AUTO_HIDE_MS ms e desaparece automaticamente.
Não bloqueia o usuário (não é modal).
"""
import tkinter as tk
from typing import Optional, Callable
from config.ui_constants import BG_SECONDARY, FG_PRIMARY, ACCENT_GREEN, ACCENT_RED
class ToastBar:
    """
    Barra de notificação que aparece no topo da janela.
    
    Uso:
        toast = ToastBar(root)
        toast.show("🆕 Projeto detectado: Mesa Industrial", 
                   action_text="Ver", action_cb=lambda: ...)
    """
    
    AUTO_HIDE_MS = 6000  # 6 segundos
    HEIGHT = 40
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self._timer: Optional[str] = None
        self._frame: Optional[tk.Frame] = None
        self._build()
    
    def _build(self) -> None:
        self._frame = tk.Frame(self.root, bg="#1A3A1A", height=self.HEIGHT,
                                relief="flat", bd=0)
        # Não faz pack aqui — só quando show() for chamado
        
        self._msg_label = tk.Label(self._frame, text="", bg="#1A3A1A",
                                    fg=FG_PRIMARY, font=("Arial", 10))
        self._msg_label.pack(side="left", padx=15, pady=8)
        
        self._action_btn = tk.Label(self._frame, text="", bg="#1A3A1A",
                                     fg=ACCENT_GREEN, font=("Arial", 10, "bold"),
                                     cursor="hand2")
        self._action_btn.pack(side="left", padx=5)
        
        close_btn = tk.Label(self._frame, text="✕", bg="#1A3A1A",
                              fg="#888888", font=("Arial", 10), cursor="hand2")
        close_btn.pack(side="right", padx=10)
        close_btn.bind("<Button-1>", lambda e: self.hide())
    
    def show(self, message: str, action_text: str = "", 
             action_cb: Optional[Callable] = None,
             color: str = "#1A3A1A") -> None:
        """
        Exibe a toast com mensagem.
        
        Args:
            message: Texto da notificação
            action_text: Texto do botão de ação (opcional)
            action_cb: Callback ao clicar no botão de ação
            color: Cor de fundo ("#1A3A1A" verde, "#3A1A1A" vermelho)
        """
        if self._timer:
            self.root.after_cancel(self._timer)
        
        self._frame.config(bg=color)
        self._msg_label.config(text=message, bg=color)
        
        if action_text and action_cb:
            self._action_btn.config(text=action_text)
            self._action_btn.bind("<Button-1>", lambda e: action_cb())
        else:
            self._action_btn.config(text="")
            self._action_btn.unbind("<Button-1>")
        
        # Exibir no topo (antes do header)
        self._frame.pack(side="top", fill="x", before=self.root.winfo_children()[0])
        
        # Auto-hide
        self._timer = self.root.after(self.AUTO_HIDE_MS, self.hide)
    
    def hide(self) -> None:
        if self._timer:
            self.root.after_cancel(self._timer)
            self._timer = None
        self._frame.pack_forget()
9.4 — Integrar Watcher em CoreSetup e main_window.py
Em ui/bootstrap/core_setup.py:

from core.folder_watcher import FolderWatcher
class CoreSetup:
    def __init__(self):
        # ... código existente ...
        self.folder_watcher = FolderWatcher(
            database=self.database,
            on_new_project=None,   # Será definido pelo main_window
            on_new_file=None,       # Será definido pelo main_window
        )
Em main_window.py, no método de inicialização (após UIBuilder.build):

# Iniciar Folder Watcher com callbacks conectados
scan_folders = self.db_manager.config.get("scan_folders", [])
self.folder_watcher.on_new_project = self._on_watcher_new_project
self.folder_watcher.on_new_file = self._on_watcher_new_file
self.folder_watcher.start(folders=scan_folders, root_tk=self.root)
# Parar no fechamento
self.root.protocol("WM_DELETE_WINDOW", self._on_close)
def _on_close(self) -> None:
    self.folder_watcher.stop()
    self.db_manager.save_database()
    self.root.destroy()
def _on_watcher_new_project(self, folder_path: str) -> None:
    """Chamado na thread principal quando novo projeto é detectado."""
    # Adicionar ao banco via scanner
    added = self.scanner.scan_projects([os.path.dirname(folder_path)])
    if added > 0:
        self._refresh_all()
        name = os.path.basename(folder_path)
        self.toast_bar.show(
            f"🆕 '{name}' detectado automaticamente",
            action_text="Ver",
            action_cb=lambda: self.open_project_modal(folder_path)
        )
def _on_watcher_new_file(self, file_path: str, folder_path: str) -> None:
    """Chamado quando novo arquivo de design é adicionado a projeto existente."""
    name = os.path.basename(file_path)
    project_name = os.path.basename(folder_path)
    self.toast_bar.show(f"📄 '{name}' adicionado a '{project_name}'")
10. FASE 5 — HASH DE IDENTIDADE E GIT DOS MAKERS
Meta: Versão 4.6.0.0
Estimativa: 1 semana
Dependência: Fase 0 (DatabaseManager com RLock)

10.1 — Adicionar project_hash ao ProjectScanner
Arquivo: core/project_scanner.py

Adicionar método:

import hashlib
def calculate_project_hash(self, project_path: str) -> str:
    """
    Calcula hash de identidade baseado em metadados dos arquivos.
    
    Usa: lista de nomes + tamanhos de arquivo (não conteúdo — rápido).
    Formato: MD5 hex dos primeiros 12 chars.
    
    NÃO usa conteúdo de arquivo (seria 30+ segundos para pastas grandes).
    MD5 de metadados é suficientemente único para este uso.
    """
    try:
        files_info = []
        for f in sorted(os.listdir(project_path)):
            fpath = os.path.join(project_path, f)
            if os.path.isfile(fpath):
                try:
                    size = os.path.getsize(fpath)
                    files_info.append(f"{f}:{size}")
                except OSError:
                    continue
        
        if not files_info:
            # Pasta vazia — hash do nome da pasta
            files_info = [os.path.basename(project_path)]
        
        content = "|".join(files_info)
        return hashlib.md5(content.encode("utf-8")).hexdigest()[:12]
    except Exception as e:
        self.logger.warning("Erro ao calcular hash de %s: %s", project_path, e)
        return ""
Modificar scan_projects() para adicionar hash ao criar novo projeto:

def scan_projects(self, folders):
    ...
    self.database[project_path] = {
        "name": item,
        "project_hash": self.calculate_project_hash(project_path),  # ← ADICIONAR
        "origin": self.get_origin_from_path(project_path),
        "favorite": False,
        # ... restante dos campos ...
    }
10.2 — Detecção de pasta movida em DatabaseManager
Arquivo: core/database.py

Adicionar em load_database(), após carregar o JSON:

def load_database(self) -> None:
    """Carrega banco e tenta recuperar projetos movidos por hash."""
    # ... código existente de carregamento ...
    
    # Detecção de projetos movidos (Fase 5 — Hash Identity)
    self._resolve_moved_projects()
def _resolve_moved_projects(self) -> None:
    """
    Detecta projetos que foram movidos de pasta e migra metadados.
    
    Lógica:
    1. Identifica paths no banco que não existem mais no disco
    2. Para cada path "morto", busca hash correspondente em paths que existem
    3. Se hash bater → migra metadados do path morto para o novo path
    """
    from core.project_scanner import ProjectScanner
    
    dead_paths = [p for p in self.database if not os.path.isdir(p)]
    if not dead_paths:
        return
    
    # Construir índice de hashes dos projetos mortos
    dead_by_hash = {}
    for path in dead_paths:
        h = self.database[path].get("project_hash", "")
        if h:
            dead_by_hash[h] = path
    
    if not dead_by_hash:
        return
    
    # Scanner temporário para calcular hashes de paths novos
    scanner = ProjectScanner(self.database)
    
    # Buscar candidatos em pastas configuradas
    config = self._load_config_silent()
    for folder in config.get("scan_folders", []):
        if not os.path.isdir(folder):
            continue
        try:
            for item in os.listdir(folder):
                new_path = os.path.join(folder, item)
                if not os.path.isdir(new_path) or new_path in self.database:
                    continue
                
                new_hash = scanner.calculate_project_hash(new_path)
                if new_hash and new_hash in dead_by_hash:
                    old_path = dead_by_hash[new_hash]
                    # Migrar metadados
                    self.database[new_path] = self.database.pop(old_path)
                    self.database[new_path]["project_hash"] = new_hash
                    self.logger.info(
                        "Projeto movido detectado: %s → %s", old_path, new_path)
        except PermissionError:
            continue
    
    # Salvar se houve migração
    if dead_paths != [p for p in self.database if not os.path.isdir(p)]:
        self.save_database()
10.3 — Criar core/version_history.py
Arquivo novo: core/version_history.py

"""
core/version_history.py — Histórico de versões de arquivos de design.
"Git dos Makers" — versionamento simples por cópia de arquivo.
NÃO usa git real (GitPython tem 175 issues abertos e requer git instalado).
Armazena em: laserflix_versions/{project_hash}/{timestamp}_{filename}
Limite: MAX_VERSIONS por projeto (oldest deletado primeiro).
"""
import os
import shutil
import json
from datetime import datetime
from typing import List, Dict, Optional
from utils.logging_setup import LOGGER
class VersionHistory:
    """
    Gerencia histórico de versões de arquivos de design.
    
    Uso no FolderWatcher (ao detectar modificação em arquivo existente):
        history = VersionHistory(versions_dir="laserflix_versions")
        history.save_version(
            project_path="/projetos/Mesa/",
            file_path="/projetos/Mesa/mesa.lbrn2",
            project_hash="abc123def456",
            comment="Auto-detectado pelo Folder Watcher",
        )
    
    Listar versões (no ProjectModal):
        versions = history.list_versions(project_hash="abc123def456",
                                          filename="mesa.lbrn2")
    """
    
    MAX_VERSIONS = 10
    VERSIONS_DIR_NAME = "laserflix_versions"
    DESIGN_EXTENSIONS = {".lbrn2", ".lbrn", ".svg", ".dxf"}
    
    def __init__(self, base_dir: str):
        """
        Args:
            base_dir: Diretório pai onde criar laserflix_versions/
        """
        self.versions_dir = os.path.join(base_dir, self.VERSIONS_DIR_NAME)
        os.makedirs(self.versions_dir, exist_ok=True)
        self.logger = LOGGER
    
    def save_version(self, project_path: str, file_path: str,
                     project_hash: str, comment: str = "") -> Optional[str]:
        """
        Salva uma nova versão do arquivo.
        
        Returns:
            Caminho do arquivo de versão salvo, ou None se erro
        """
        if not os.path.isfile(file_path):
            return None
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in self.DESIGN_EXTENSIONS:
            return None
        
        # Diretório da versão: versions_dir/project_hash/
        project_version_dir = os.path.join(self.versions_dir, project_hash)
        os.makedirs(project_version_dir, exist_ok=True)
        
        # Nome do arquivo de versão: {timestamp}_{filename}
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        version_filename = f"{timestamp}_{filename}"
        dest_path = os.path.join(project_version_dir, version_filename)
        
        try:
            shutil.copy2(file_path, dest_path)
        except (PermissionError, OSError) as e:
            self.logger.warning("Erro ao salvar versão: %s", e)
            return None
        
        # Salvar metadata
        meta = {
            "original_path": file_path,
            "saved_at": datetime.now().isoformat(),
            "comment": comment,
            "size_bytes": os.path.getsize(dest_path),
        }
        meta_path = dest_path + ".meta.json"
        try:
            with open(meta_path, "w", encoding="utf-8") as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
        except OSError:
            pass
        
        # Limpar versões antigas se exceder MAX_VERSIONS
        self._prune_old_versions(project_version_dir, filename)
        
        self.logger.info("Versão salva: %s", version_filename)
        return dest_path
    
    def list_versions(self, project_hash: str, filename: str) -> List[Dict]:
        """
        Lista versões salvas de um arquivo.
        
        Returns:
            Lista de dicts com: version_path, original_path, saved_at, comment, size_bytes
            Ordenado: mais recente primeiro
        """
        project_version_dir = os.path.join(self.versions_dir, project_hash)
        if not os.path.isdir(project_version_dir):
            return []
        
        versions = []
        for f in os.listdir(project_version_dir):
            if not f.endswith(filename) or f.endswith(".meta.json"):
                continue
            
            version_path = os.path.join(project_version_dir, f)
            meta_path = version_path + ".meta.json"
            
            meta = {}
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, encoding="utf-8") as mf:
                        meta = json.load(mf)
                except Exception:
                    pass
            
            versions.append({
                "version_path": version_path,
                "version_filename": f,
                "saved_at": meta.get("saved_at", ""),
                "comment": meta.get("comment", ""),
                "size_bytes": meta.get("size_bytes", 0),
            })
        
        return sorted(versions, key=lambda v: v["saved_at"], reverse=True)
    
    def restore_version(self, version_path: str, target_path: str) -> bool:
        """
        Restaura uma versão para o arquivo original.
        
        Args:
            version_path: Caminho do arquivo de versão
            target_path: Onde restaurar (geralmente o arquivo original)
        
        Returns:
            True se sucesso
        """
        try:
            # Backup do arquivo atual antes de restaurar
            if os.path.exists(target_path):
                backup = target_path + ".backup_before_restore"
                shutil.copy2(target_path, backup)
            shutil.copy2(version_path, target_path)
            return True
        except (PermissionError, OSError) as e:
            self.logger.error("Erro ao restaurar versão: %s", e)
            return False
    
    def _prune_old_versions(self, version_dir: str, filename: str) -> None:
        """Remove versões antigas além do limite MAX_VERSIONS."""
        all_versions = sorted([
            f for f in os.listdir(version_dir)
            if f.endswith(filename) and not f.endswith(".meta.json")
        ])
        while len(all_versions) > self.MAX_VERSIONS:
            oldest = all_versions.pop(0)
            oldest_path = os.path.join(version_dir, oldest)
            try:
                os.remove(oldest_path)
                meta = oldest_path + ".meta.json"
                if os.path.exists(meta):
                    os.remove(meta)
            except OSError:
                pass
11. FASE 6 — BUSCA SEMÂNTICA
Meta: Versão 4.7.0.0
Estimativa: 1 semana
Dependência: Fase 0 (IA stack estável)

11.1 — Instalação
pip install numpy>=1.24.0
nomic-embed-text já está disponível no Ollama configurado pelo app (274MB).

11.2 — Criar core/embeddings_store.py
Arquivo novo: core/embeddings_store.py

"""
core/embeddings_store.py — Armazena e busca embeddings semânticos de projetos.
Modelo: nomic-embed-text:latest (768 dimensões) via Ollama local.
Persistência: laserflix_embeddings.json
Busca: similaridade por cosseno (numpy).
Fallback: se Ollama offline, retorna resultados vazios silenciosamente.
"""
import json
import os
import copy
from typing import List, Optional, Tuple
from utils.logging_setup import LOGGER
try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    LOGGER.warning("numpy não instalado — busca semântica desabilitada")
class EmbeddingsStore:
    """
    Gerencia embeddings vetoriais para busca semântica.
    
    Uso:
        store = EmbeddingsStore(ollama_client, data_dir)
        
        # Gerar embedding para projeto (após análise IA)
        store.build_embedding(project_path, project_data)
        
        # Buscar projetos semanticamente similares
        results = store.search("espelho decorativo", top_k=20)
        # results: lista de (project_path, similarity_score)
    """
    
    EMBEDDINGS_FILE = "laserflix_embeddings.json"
    EMBEDDING_MODEL = "nomic-embed-text"
    
    def __init__(self, ollama_client, data_dir: str):
        self.ollama = ollama_client
        self.embeddings_file = os.path.join(data_dir, self.EMBEDDINGS_FILE)
        self.logger = LOGGER
        
        # {project_path: [float, ...]}
        self._embeddings: dict = {}
        self._load()
    
    def build_embedding(self, project_path: str, data: dict) -> bool:
        """
        Gera e armazena embedding para um projeto.
        Chamado após análise IA (em AnalysisController._on_analysis_done).
        
        Returns:
            True se gerado com sucesso
        """
        if not NUMPY_AVAILABLE:
            return False
        
        # Construir texto representativo do projeto
        parts = [
            data.get("name", ""),
            data.get("name_pt", ""),
            " ".join(data.get("categories", [])),
            " ".join(data.get("tags", [])),
            data.get("ai_description", "")[:300],  # Limitar para performance
        ]
        text = " ".join(p for p in parts if p).strip()
        
        if not text:
            return False
        
        try:
            embedding = self._get_embedding(text)
            if embedding:
                self._embeddings[project_path] = embedding
                self._save()
                return True
        except Exception as e:
            self.logger.warning("Erro ao gerar embedding para %s: %s", project_path, e)
        return False
    
    def search(self, query: str, top_k: int = 20,
               database_paths: Optional[List[str]] = None) -> List[Tuple[str, float]]:
        """
        Busca projetos semanticamente similares à query.
        
        Args:
            query: Texto de busca
            top_k: Número máximo de resultados
            database_paths: Se fornecido, só busca nestes paths (filtro prévio)
        
        Returns:
            Lista de (project_path, similarity_score) ordenada por similaridade
            Retorna lista vazia se numpy/ollama não disponível
        """
        if not NUMPY_AVAILABLE or not self._embeddings:
            return []
        
        query_embedding = self._get_embedding(query)
        if not query_embedding:
            return []
        
        # Paths a considerar
        candidate_paths = database_paths or list(self._embeddings.keys())
        candidates = [
            (p, self._embeddings[p])
            for p in candidate_paths
            if p in self._embeddings
        ]
        
        if not candidates:
            return []
        
        try:
            q_vec = np.array(query_embedding, dtype=np.float32)
            q_norm = np.linalg.norm(q_vec)
            if q_norm == 0:
                return []
            q_vec = q_vec / q_norm
            
            results = []
            for path, emb in candidates:
                try:
                    p_vec = np.array(emb, dtype=np.float32)
                    p_norm = np.linalg.norm(p_vec)
                    if p_norm == 0:
                        continue
                    p_vec = p_vec / p_norm
                    similarity = float(np.dot(q_vec, p_vec))
                    results.append((path, similarity))
                except Exception:
                    continue
            
            results.sort(key=lambda x: x[1], reverse=True)
            return results[:top_k]
        except Exception as e:
            self.logger.error("Erro na busca semântica: %s", e)
            return []
    
    def remove_project(self, project_path: str) -> None:
        """Remove embedding de projeto deletado."""
        if project_path in self._embeddings:
            del self._embeddings[project_path]
            self._save()
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """Obtém embedding do Ollama. Retorna None se offline."""
        try:
            # O OllamaClient deve ter método embed() — verificar API do ollama_client.py
            # Se não existir, adicionar:
            response = self.ollama.embed(text, model=self.EMBEDDING_MODEL)
            return response  # Lista de floats
        except Exception as e:
            self.logger.debug("Ollama offline para embeddings: %s", e)
            return None
    
    def _load(self) -> None:
        if not os.path.exists(self.embeddings_file):
            return
        try:
            with open(self.embeddings_file, encoding="utf-8") as f:
                self._embeddings = json.load(f)
            self.logger.info("Embeddings carregados: %d projetos", len(self._embeddings))
        except Exception as e:
            self.logger.warning("Erro ao carregar embeddings: %s", e)
    
    def _save(self) -> None:
        try:
            tmp = self.embeddings_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self._embeddings, f)
            os.replace(tmp, self.embeddings_file)
        except Exception as e:
            self.logger.warning("Erro ao salvar embeddings: %s", e)
11.3 — Verificar API de embed no OllamaClient
Arquivo: ai/ollama_client.py ← ZONA PROTEGIDA (só verificar, não modificar sem autorização)

Verificar se existe método embed(text, model). Se não existir, adicionar APENAS se autorizado:

def embed(self, text: str, model: str = "nomic-embed-text") -> Optional[List[float]]:
    """Gera embedding vetorial via Ollama."""
    try:
        resp = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": model, "prompt": text},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json().get("embedding")
    except Exception as e:
        self.logger.debug("Erro embed: %s", e)
        return None
11.4 — Integrar busca semântica no DisplayController
Arquivo: ui/controllers/optimized_display_controller.py

Em BaseDisplayController.get_filtered_projects(), adicionar busca semântica:

def get_filtered_projects(self) -> list:
    """Filtra projetos. Se busca semântica disponível, usa busca híbrida."""
    paths = super().get_filtered_projects() if hasattr(super(), 'get_filtered_projects') else []
    
    if self.search_query and self._embeddings_store:
        # Busca semântica nos candidatos já filtrados
        semantic_results = self._embeddings_store.search(
            query=self.search_query,
            top_k=100,
            database_paths=list(self.database.keys())
        )
        
        if semantic_results:
            # Busca híbrida: 60% semântico + 40% keyword
            semantic_paths = [p for p, score in semantic_results if score > 0.5]
            
            # Keyword (resultado atual da busca por texto)
            keyword_paths = [p for p in paths]
            
            # Combinar (semânticos primeiro, depois keyword-only)
            combined = list(dict.fromkeys(semantic_paths + keyword_paths))
            return [p for p in combined if p in self.database]
    
    return paths
12. FASE 7 — CALCULADORA DE PRECIFICAÇÃO
Meta: Versão Aurum V1.0
Estimativa: 4-5 dias
Dependência: Independente (pode ser desenvolvida após Fase 3)

12.1 — Criar ui/pricing_dialog.py
Arquivo novo: ui/pricing_dialog.py

"""
ui/pricing_dialog.py — Calculadora de precificação para projetos de laser.
Acessível via: botão no ProjectModal + menu contextual no card.
Dados salvos em: database[path]["pricing"]
"""
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import Optional
from config.ui_constants import (
    BG_SECONDARY, BG_CARD, FG_PRIMARY, FG_SECONDARY,
    ACCENT_RED, ACCENT_GREEN
)
MATERIALS = [
    "MDF 3mm", "MDF 6mm", "MDF 9mm", "MDF 12mm",
    "Acrílico 3mm", "Acrílico 5mm", "Acrílico 8mm",
    "Madeira Pinus", "Madeira Cedar", "Madeira OSB",
    "Compensado 3mm", "Compensado 6mm",
    "Couro", "Tecido", "Outro"
]
class PricingDialog:
    """
    Dialog de calculadora de precificação.
    
    Uso no ProjectModal:
        PricingDialog(root, project_path, database, on_save=callback).open()
    
    Campos calculados:
        - Custo de material (baseado em dimensão e preço/chapa)
        - Custo de máquina (tempo × custo/hora)
        - Custo total unitário
        - Preço de venda com margem configurável
    """
    
    BG = "#181818"
    
    def __init__(self, root: tk.Tk, project_path: str, 
                 database: dict, on_save: Optional[callable] = None):
        self.root = root
        self.path = project_path
        self.database = database
        self.on_save = on_save
        self._win: Optional[tk.Toplevel] = None
    
    def open(self) -> None:
        data = self.database.get(self.path, {})
        existing = data.get("pricing", {})
        
        self._win = tk.Toplevel(self.root)
        self._win.title("💰 Calculadora de Precificação")
        self._win.configure(bg=self.BG)
        self._win.geometry("600x700")
        self._win.transient(self.root)
        self._win.grab_set()
        self._win.bind("<Escape>", lambda e: self._win.destroy())
        
        project_name = data.get("name", "Projeto")
        
        # Título
        tk.Label(self._win, text=f"💰 {project_name}",
                 font=("Arial", 16, "bold"), bg=self.BG, fg=FG_PRIMARY
                 ).pack(pady=(20, 5))
        tk.Label(self._win, text="Calculadora de Precificação",
                 font=("Arial", 11), bg=self.BG, fg=FG_SECONDARY
                 ).pack(pady=(0, 15))
        
        # Frame de formulário
        form = tk.Frame(self._win, bg=self.BG)
        form.pack(fill="both", expand=True, padx=30)
        
        # ── MATERIAL ──
        self._section_label(form, "📦 Material")
        
        # Tipo de material
        self._field_label(form, "Tipo de material:")
        self._material_var = tk.StringVar(value=existing.get("material", "MDF 3mm"))
        mat_combo = ttk.Combobox(form, textvariable=self._material_var,
                                  values=MATERIALS, state="readonly", width=30)
        mat_combo.pack(anchor="w", pady=(0, 8))
        
        # Dimensão da chapa
        dim_frame = tk.Frame(form, bg=self.BG)
        dim_frame.pack(anchor="w", pady=(0, 8))
        self._field_label_inline(dim_frame, "Dimensão da chapa:")
        self._mat_w = self._entry_small(dim_frame, existing.get("sheet_w_cm", "60"))
        tk.Label(dim_frame, text="×", bg=self.BG, fg=FG_PRIMARY).pack(side="left", padx=3)
        self._mat_h = self._entry_small(dim_frame, existing.get("sheet_h_cm", "40"))
        tk.Label(dim_frame, text="cm", bg=self.BG, fg=FG_SECONDARY,
                 font=("Arial", 9)).pack(side="left", padx=3)
        
        # Preço por chapa
        price_frame = tk.Frame(form, bg=self.BG)
        price_frame.pack(anchor="w", pady=(0, 8))
        self._field_label_inline(price_frame, "Preço da chapa: R$")
        self._sheet_price = self._entry_small(price_frame, existing.get("sheet_price", "15.00"))
        
        # Uso da chapa
        usage_frame = tk.Frame(form, bg=self.BG)
        usage_frame.pack(anchor="w", pady=(0, 15))
        self._field_label_inline(usage_frame, "% da chapa usada:")
        self._sheet_usage = self._entry_small(usage_frame, existing.get("sheet_usage_pct", "30"), w=5)
        tk.Label(usage_frame, text="%", bg=self.BG, fg=FG_SECONDARY).pack(side="left")
        
        # ── MÁQUINA ──
        self._section_label(form, "⚡ Tempo de Máquina")
        
        machine_frame = tk.Frame(form, bg=self.BG)
        machine_frame.pack(anchor="w", pady=(0, 8))
        self._field_label_inline(machine_frame, "Tempo estimado:")
        self._machine_min = self._entry_small(machine_frame, existing.get("machine_min", "30"), w=6)
        tk.Label(machine_frame, text="minutos", bg=self.BG, fg=FG_SECONDARY).pack(side="left", padx=3)
        
        cost_frame = tk.Frame(form, bg=self.BG)
        cost_frame.pack(anchor="w", pady=(0, 15))
        self._field_label_inline(cost_frame, "Custo da máquina: R$")
        self._machine_cost_h = self._entry_small(cost_frame, existing.get("machine_cost_h", "20.00"))
        tk.Label(cost_frame, text="/hora", bg=self.BG, fg=FG_SECONDARY).pack(side="left", padx=3)
        
        # ── QUANTIDADE ──
        self._section_label(form, "📦 Quantidade")
        
        qty_frame = tk.Frame(form, bg=self.BG)
        qty_frame.pack(anchor="w", pady=(0, 15))
        self._field_label_inline(qty_frame, "Peças desejadas:")
        self._qty = self._entry_small(qty_frame, existing.get("qty", "1"), w=6)
        
        # ── MARGEM ──
        self._section_label(form, "📈 Margem de Lucro")
        
        margin_frame = tk.Frame(form, bg=self.BG)
        margin_frame.pack(anchor="w", pady=(0, 15))
        self._field_label_inline(margin_frame, "Margem desejada:")
        self._margin = self._entry_small(margin_frame, existing.get("margin_pct", "60"), w=5)
        tk.Label(margin_frame, text="%", bg=self.BG, fg=FG_SECONDARY).pack(side="left")
        
        # Botão Calcular
        tk.Button(form, text="💰 Calcular Preço",
                  command=self._calculate,
                  bg=ACCENT_RED, fg=FG_PRIMARY, font=("Arial", 12, "bold"),
                  relief="flat", cursor="hand2", padx=20, pady=10
                  ).pack(pady=10)
        
        # ── RESULTADO ──
        self._result_frame = tk.Frame(form, bg="#0A2A0A", relief="flat", bd=1)
        # Só aparece após calcular
        
        self._result_labels = {}
        
        # Se já tem dados salvos, mostrar resultado anterior
        if existing.get("unit_cost"):
            self._show_result(existing)
    
    def _calculate(self) -> None:
        """Executa o cálculo de precificação."""
        try:
            sheet_price = float(self._sheet_price.get().replace(",", "."))
            sheet_usage = float(self._sheet_usage.get()) / 100
            machine_min = float(self._machine_min.get().replace(",", "."))
            machine_cost_h = float(self._machine_cost_h.get().replace(",", "."))
            qty = max(1, int(self._qty.get()))
            margin_pct = float(self._margin.get())
            
            # Cálculos
            material_cost = sheet_price * sheet_usage
            machine_cost = (machine_min / 60) * machine_cost_h
            unit_cost = (material_cost + machine_cost) / qty
            margin_factor = 1 + (margin_pct / 100)
            suggested_price = unit_cost * margin_factor
            
            result = {
                "material": self._material_var.get(),
                "sheet_price": sheet_price,
                "sheet_usage_pct": int(sheet_usage * 100),
                "sheet_w_cm": self._mat_w.get(),
                "sheet_h_cm": self._mat_h.get(),
                "machine_min": machine_min,
                "machine_cost_h": machine_cost_h,
                "qty": qty,
                "margin_pct": margin_pct,
                "material_cost": round(material_cost, 2),
                "machine_cost": round(machine_cost, 2),
                "unit_cost": round(unit_cost, 2),
                "suggested_price": round(suggested_price, 2),
                "calculated_at": datetime.now().isoformat(),
            }
            
            self._show_result(result)
            
            # Salvar no banco
            if self.path in self.database:
                self.database[self.path]["pricing"] = result
                if self.on_save:
                    self.on_save()
                    
        except (ValueError, ZeroDivisionError) as e:
            tk.messagebox.showerror("Erro", f"Valores inválidos: {e}", parent=self._win)
    
    def _show_result(self, result: dict) -> None:
        """Exibe o resultado do cálculo."""
        for w in self._result_frame.winfo_children():
            w.destroy()
        
        self._result_frame.pack(fill="x", pady=10)
        
        rows = [
            ("Material", f"R$ {result.get('material_cost', 0):.2f}"),
            ("Tempo de máquina", f"R$ {result.get('machine_cost', 0):.2f}"),
            ("── Custo unitário ──", f"R$ {result.get('unit_cost', 0):.2f}"),
            (f"Margem ({result.get('margin_pct', 0):.0f}%)", 
             f"R$ {result.get('unit_cost', 0) * result.get('margin_pct', 0) / 100:.2f}"),
            ("═══ Preço sugerido ═══", f"R$ {result.get('suggested_price', 0):.2f}"),
        ]
        
        for label, value in rows:
            row = tk.Frame(self._result_frame, bg="#0A2A0A")
            row.pack(fill="x", padx=15, pady=2)
            bold = "═══" in label or "──" in label
            font = ("Arial", 11, "bold") if bold else ("Arial", 10)
            fg_val = ACCENT_GREEN if "Preço sugerido" in label else FG_PRIMARY
            
            tk.Label(row, text=label, bg="#0A2A0A", fg=FG_SECONDARY, font=font,
                     anchor="w").pack(side="left", fill="x", expand=True)
            tk.Label(row, text=value, bg="#0A2A0A", fg=fg_val, font=font
                     ).pack(side="right")
    
    # ── Helpers de UI ──
    
    def _section_label(self, parent, text: str) -> None:
        tk.Label(parent, text=text, font=("Arial", 12, "bold"),
                 bg=self.BG, fg=FG_PRIMARY).pack(anchor="w", pady=(10, 4))
        tk.Frame(parent, bg="#333333", height=1).pack(fill="x", pady=(0, 8))
    
    def _field_label(self, parent, text: str) -> None:
        tk.Label(parent, text=text, font=("Arial", 10), bg=self.BG,
                 fg=FG_SECONDARY).pack(anchor="w", pady=(0, 3))
    
    def _field_label_inline(self, parent, text: str) -> None:
        tk.Label(parent, text=text, font=("Arial", 10), bg=self.BG,
                 fg=FG_SECONDARY).pack(side="left", padx=(0, 5))
    
    def _entry_small(self, parent, default: str, w: int = 10) -> tk.Entry:
        e = tk.Entry(parent, width=w, bg=BG_CARD, fg=FG_PRIMARY,
                     font=("Arial", 11), relief="flat", insertbackground=FG_PRIMARY)
        e.insert(0, str(default))
        e.pack(side="left")
        return e
12.2 — Adicionar botão de precificação no ProjectModal
Arquivo: ui/project_modal.py
Nos botões de ação do modal, adicionar:

tk.Button(..., text="💰 Precificar",
          command=lambda: PricingDialog(
              self._root, self._path, self._database,
              on_save=self._cb.get("on_save")
          ).open(),
          ...).pack(...)
13. DEPENDÊNCIAS E requirements.txt FINAL
# requirements.txt — Laserflix Aurum V1.0
# Já presentes
Pillow>=10.0.0          # Thumbnails e preview de imagens
requests>=2.31.0        # Ollama HTTP client
# Novos no Aurum V1.0
ttkbootstrap>=1.10.0    # Tema darkly sobre ttk stdlib
                        # (31 issues vs 412 do customtkinter — decisão por dados)
watchdog>=4.0.0         # Smart Folder Watcher (multiplataforma Windows/macOS/Linux)
numpy>=1.24.0           # Álgebra de vetores para busca semântica (cosseno)
svglib>=1.5.1           # Thumbnails de arquivos .svg (makers usam SVG extensivamente)
# requirements-test.txt (já existe, manter)
pytest>=7.0.0
pytest-cov>=4.0.0
Ollama — modelos necessários (já instalados conforme config.json)
qwen3.5:4b          — análise de categorias e descrições (3.4 GB)
moondream           — análise visual de capa de projeto
nomic-embed-text    — embeddings para busca semântica (274 MB)
14. SEQUÊNCIA DE COMMITS RECOMENDADA
feat(bug): replace threading.Timer with root.after() in header debounce
feat(bug): add threading.RLock to DatabaseManager
feat(bug): unify BANNED_STRINGS from single source in constants.py
feat(bug): move inline import to top of main_window.py
feat(bug): add lazy get_page() to DatabaseManager (avoid full deepcopy)
feat(test): fix failing unit tests to reach 60% coverage
feat(arch): integrate virtual_scroll.py or remove if redundant
feat(visual): add ttkbootstrap darkly theme to main.py
feat(visual): adjust palette overrides for Laserflix identity
feat(hover): create ui/components/hover_card.py
feat(hover): add hover callbacks to project_card.py and cards_grid_builder.py
feat(session): create core/session_manager.py
feat(curation): create core/curation_engine.py
feat(lanes): create ui/components/discovery_lane.py
feat(home): create ui/home_view.py
feat(home): integrate HomeView in UIBuilder and main_window.py
feat(watcher): create core/folder_watcher.py (watchdog)
feat(toast): create ui/components/toast_bar.py
feat(watcher): integrate FolderWatcher and ToastBar in main_window.py
feat(hash): add calculate_project_hash to ProjectScanner
feat(hash): add _resolve_moved_projects to DatabaseManager.load_database()
feat(versions): create core/version_history.py
feat(embed): create core/embeddings_store.py
feat(search): integrate hybrid search in OptimizedDisplayController
feat(pricing): create ui/pricing_dialog.py
feat(pricing): add pricing button to ProjectModal
chore(release): bump version to Aurum V1.0
APÊNDICE — CHECKLIST DE VALIDAÇÃO POR FASE
Fase 0 ✓
 pytest tests/ -v roda sem crash
 pytest --cov=core --cov=utils mostra ≥60%
 Digitar rápido no campo de busca não causa RuntimeError
 Banco salva corretamente com múltiplos threads ativos
 CARD_BANNED_STRINGS e BANNED_STRINGS retornam os mesmos valores
Fase 1 ✓
 App abre sem erro com import ttkbootstrap
 Scrollbars mais finas e modernas
 Botões TTK (header, sidebar) com aparência atualizada
 Cards (project_card.py) com visual inalterado (não herdam tema TTK)
 Progress bar vermelha (#E50914)
Fase 2 ✓
 Hover card aparece após 400ms sobre qualquer card
 Hover card desaparece ao sair do card
 Hover card não aparece em scroll rápido
 Thumbnail maior visível no hover
 Posicionamento correto em cards nas bordas da tela
Fase 3 ✓
 Home abre com pelo menos 3 lanes
 Scroll horizontal funciona com Shift+MouseWheel
 "Ver todos →" abre o grid filtrado corretamente
 Hover card funciona dentro das lanes
 Abertura de projeto registra na sessão
Fase 4 ✓
 Salvar arquivo no LightBurn em pasta monitorada → toast aparece em ≤ 5s
 App fecha sem erro (watcher.stop() chamado)
 Pasta já no banco não é duplicada pelo watcher
 Toast desaparece após 6s automaticamente
Fase 5 ✓
 Mover pasta e reabrir o app → metadados recuperados automaticamente
 Hash calculado em < 50ms para pastas com até 500 arquivos
 VersionHistory salva até 10 versões por arquivo
 Versões antigas além do limite são removidas
Fase 6 ✓
 Buscar "espelho" retorna projetos com "mirror" nas tags
 Se Ollama offline, busca cai para keyword sem erro visível
 Embeddings persistem entre sessões (laserflix_embeddings.json)
 Busca híbrida mistura resultado semântico com keyword
Fase 7 ✓
 Calculadora abre do botão no ProjectModal
 Cálculo correto: material + máquina + margem
 Resultado salvo no database.json em "pricing"
 Valores anteriores carregados ao reabrir o dialog
Documento gerado em 23/03/2026
Baseado em leitura integral de 46 arquivos Python, 12 documentos internos do repositório
Repositório: https://github.com/digimar07-cmyk/02dev-scratch-pad2/tree/main/LASERFLIX_2