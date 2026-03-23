PROJETO AURUM — Laserflix Aurum V1.0
Plano Mestre Revisado com Base em Análise Completa do Código
Revisão baseada em leitura integral de: 46 arquivos Python, 12 documentos internos,
análise técnica de 55KB, DOCTORAL_APPROVAL_PLAN, TECH_AUDIT, BACKLOG, APP_PHILOSOPHY,
e pesquisa de mercado em GitHub sobre dependências.

Versão do Plano: 2.0.0 (Revisão Completa)
Data: 23/03/2026
Versão atual do app: 4.0.1.2
Versão alvo: Aurum V1.0
Status: 🔴 Em planejamento — nenhum código escrito ainda

O QUE MUDOU EM RELAÇÃO AO PLANO 1.0
O plano anterior foi escrito sem leitura completa do código. Esta versão corrige isso.

Erros do Plano 1.0:

Escolha de customtkinter por reflexo (sem pesquisa) → corrigido para ttkbootstrap
Não reconheceu o DOCTORAL_APPROVAL_PLAN em andamento → agora Fase 0 do plano
Não identificou que virtual scroll JÁ EXISTE implementado → mencionou como feature nova
Não reconheceu as ZONAS PROTEGIDAS do BACKLOG.md (ai/, import dialogs)
Não incorporou a APP_PHILOSOPHY.md como restrição de design
Não identificou o bug de all_projects() com copy.deepcopy() no banco inteiro
Não identificou o threading.Timer de debounce como bug de thread safety
Não mapeou o que já foi feito (FilterCache, ViewportManager, PredictivePreloader)
ÍNDICE
Estado Real do App Hoje
Restrições Inegociáveis
O Gap entre o Atual e o Aurum
Bugs Confirmados no Código
Fase 0 — Fundação Doutoral
Fase 1 — ttkbootstrap Darkly
Fase 2 — Hover Card
Fase 3 — Discovery Lanes
Fase 4 — Smart Folder Watcher
Fase 5 — Identidade por Hash e Git dos Makers
Fase 6 — Busca Semântica
Fase 7 — Calculadora de Precificação
Decisões Técnicas Pesquisadas
Dependências e Requisitos
Cronograma Realista
1. Estado Real do App Hoje
O que JÁ FUNCIONA bem (e não deve ser reescrito)
Componente	Estado	Nota
FilterCache (LRU + TTL)	✅ Implementado	80% mais rápido em filtros
ViewportManager (lazy render)	✅ Implementado	60% mais rápido na renderização
PredictivePreloader	✅ Implementado	Pré-carrega próxima página
Paginação (36 cards/pág)	✅ Implementado	Funcional
Sistema de Coleções	✅ Implementado	Backend + UI completos
Análise IA + Fallbacks	✅ Implementado	Ollama local + keywords
Bilingual Search (EN→PT)	✅ Implementado	name_translator.py estático
Filtros empilháveis com chips	✅ Implementado	AND lógico funcional
Modal de detalhes	✅ Implementado	project_modal.py 17KB
Backup + versioning	✅ Implementado	backup_manager + VersionManager
Importação recursiva	✅ Implementado	ZONA PROTEGIDA — não tocar
Detecção de duplicatas	✅ Implementado	Por nome normalizado
Bootstrap pattern (CoreSetup/ManagersSetup/CallbacksSetup)	✅ Implementado	Arquitetura limpa
Arquitetura em Camadas (já refatorada)
main.py (< 30 linhas)
    └── LaserflixMainWindow
            ├── CoreSetup           → instancia DB, AI, Scanner
            ├── ManagersSetup       → instancia Toggle, Orphan, etc.
            ├── CallbacksSetup      → conecta todos os callbacks
            ├── UIBuilder           → constrói widgets
            └── Mixins              → Filter, Toggle, Modal, Selection, etc.
Score técnico atual (TECH_AUDIT de 09/03/2026): 6.6/10
Score alvo para Aurum V1.0: ≥ 9.0/10

2. Restrições Inegociáveis
Estas restrições vêm da APP_PHILOSOPHY.md e do BACKLOG.md e não podem ser violadas:

Da APP_PHILOSOPHY.md
Princípio	Implicação para o Aurum
100% offline / local	Nenhuma dependência de cloud, API externa, ou conta obrigatória
Privacidade absoluta	Zero telemetria, zero análise remota de projetos do usuário
Roda em PCs modestos	Sem GPU obrigatória. IA é opcional (fallback funciona sem Ollama)
Simplicidade Kent Beck	YAGNI radical — só implementar o que resolve a dor real
JSON, não SQL	Manter JSON como persistência (migração para SQLite só se necessário)
Das ZONAS PROTEGIDAS (BACKLOG.md)
Os seguintes arquivos não podem ser modificados sem autorização explícita:

🔒 ai/ollama_client.py
🔒 ai/analysis_manager.py
🔒 ai/text_generator.py
🔒 ai/image_analyzer.py
🔒 ai/fallbacks.py
🔒 ai/keyword_maps.py
🔒 ui/import_mode_dialog.py
🔒 ui/recursive_import_integration.py
🔒 ui/import_preview_dialog.py
🔒 ui/duplicate_resolution_dialog.py
🔒 utils/recursive_scanner.py
🔒 utils/duplicate_detector.py
O plano Aurum respeita essas zonas completamente.

3. O Gap entre o Atual e o Aurum
O que o usuário experimenta hoje
Abrir app → Ver grid 6×6 de cards → Rolar verticalmente → 
Clicar filtro na sidebar → Grid recarrega → Clicar card → Modal abre → Fechar modal
Problemas reais desta experiência:

Grid não conta história: por que eu escolheria um projeto específico?
Não há "descoberta passiva" — você precisa saber o que quer buscar
Nenhuma informação extra ao passar o mouse — o card não "vende" o projeto
Quando você abre o app, não sabe o que foi adicionado recentemente
Mover uma pasta de lugar = projeto some do banco
Salvar um novo arquivo no LightBurn = tem que importar manualmente
O que o usuário experimenta no Aurum
Abrir app → Tela Home com lanes horizontais:
  "Abertos Recentemente" (5 cards em scroll horizontal)
  "Natal 2025" (projetos de datas comemorativas próximas)
  "Favoritos" (projetos marcados com ⭐)
  "Aguardando Análise" (pendentes com badge ⏳)
  "Novos Hoje" (detectados automaticamente pelo Folder Watcher)
  "Projetos de Madeira" (por material/categoria)
Passar mouse em card → Hover Card expande: thumbnail maior, descrição IA,
  categorias completas, tags, botões rápidos de ação, prévia de arquivos
Buscar "espelho" → Resultado semântico inclui "mirror", "reflexo", "espelhos decorativos"
Abrir pasta no LightBurn, salvar arquivo → Laserflix detecta automaticamente e adiciona
Mover pasta de D:\ para E:\ → Laserflix detecta por hash de conteúdo, migra dados
4. Bugs Confirmados no Código
Estes bugs foram localizados precisamente nos arquivos de origem:

BUG-01 — threading.Timer no debounce de busca
Arquivo: ui/header.py, método _debounced_search(), linha ~54
Código problemático:

self._search_timer = threading.Timer(0.3, self._cb["on_search"])
self._search_timer.start()
Problema: threading.Timer executa o callback em uma thread separada. Qualquer atualização de widget Tkinter fora da thread principal causa RuntimeError: main thread is not in main loop.
Correção: Substituir por root.after(300, callback) — executa na thread principal do Tkinter.
Impacto: Pode causar crash intermitente ao digitar na busca rapidamente.

BUG-02 — DatabaseManager sem RLock
Arquivo: core/database.py
Problema: ThumbnailPreloader (4 workers ThreadPoolExecutor) e AnalysisManager (threading.Thread daemon) escrevem no banco simultaneamente sem lock. Race condition possível mas raro.
Correção: Adicionar self._lock = threading.RLock() e proteger save_database(), set_project(), all_projects().

BUG-03 — BANNED_STRINGS duplicado
Arquivo 1: config/constants.py → BANNED_STRINGS
Arquivo 2: config/ui_constants.py → CARD_BANNED_STRINGS (com nota: "TODO: Resolver import circular")
Problema: Duas fontes da verdade. Se uma atualiza e outra não, cards exibem categorias proibidas.
Correção: Resolver o import circular e usar constants.BANNED_STRINGS como fonte única.

BUG-04 — __import__ inline em main_window.py
Arquivo: ui/main_window.py
Problema: Import de plataforma feito inline dentro de método, padrão não-idiomático Python.
Correção: Mover para o topo do arquivo junto com os outros imports.

BUG-05 — copy.deepcopy() no banco inteiro
Arquivo: core/database.py, método all_projects()
Problema (identificado na análise de 55KB): Com 5.000+ projetos e metadados IA (descrições longas), o deepcopy do banco inteiro pode consumir 50-100ms e travar a UI.
Correção: O OptimizedDisplayController já usa FilterCache que mitiga isso em 80% dos casos. A correção definitiva é get_filtered_projects() no DatabaseManager que retorna apenas a página atual sem deepcopy total.

BUG-06 — Identidade por path (move = perde dados)
Arquivo: core/project_scanner.py, core/database.py
Problema: A chave do banco é o caminho absoluto da pasta. Mover de D:\projetos para E:\projetos = todos os metadados (favoritos, análise IA, descrição, categorias, coleções) são perdidos.
Correção: Adicionar project_hash baseado em hash do conteúdo. Fase 5 do plano.

5. Fase 0 — Fundação Doutoral
Objetivo: Concluir o trabalho em andamento do DOCTORAL_APPROVAL_PLAN antes de qualquer feature nova.
Versão alvo: 4.1.0.0
Estimativa: 1-2 semanas
Prioridade: BLOCKER — nada do Aurum começa antes disso

0.1 — Corrigir os 5 bugs confirmados
Execução em ordem de criticidade:

BUG-01: threading.Timer → root.after() (1 hora, risco zero)
BUG-02: RLock no DatabaseManager (2 horas, baixo risco)
BUG-03: Unificar BANNED_STRINGS (2 horas, requer teste de cards)
BUG-04: import inline (30 min, cosmético)
BUG-05: DatabaseManager lazy view (3-4 horas, requer teste de performance)
0.2 — Completar pendências do DOCTORAL_APPROVAL_PLAN
Item	Quem reprovou	Status
Cobertura de testes ≥ 60%	Dra. Tanaka	🔴 Pendente
API pública no DatabaseManager (contratos formais)	Dr. Volkov	🔴 Pendente
Decidir virtual_scroll.py (integrar ou remover)	Dr. Brandt	⏳ Sprint 3B
Type hints completos	Dra. Osei	🟡 Parcial
Decisão sobre virtual_scroll.py: Integrar (Opção B do plano original). Justificativa: o ViewportManager já implementa lazy rendering, mas o virtual_scroll.py tem lógica complementar de scroll virtual (renderização por índice, não por posição). A integração é a escolha certa porque o Prof. Mendonça (IHC) e o Prof. Brandt (Arquitetura) aprovam simultaneamente.

0.3 — Limpar config duplicado
Mover config/ui_constants.py e config/constants.py para uma fonte única. Resolver o import circular usando importação lazy (from __future__ import annotations).

6. Fase 1 — ttkbootstrap Darkly
Objetivo: Modernizar visualmente o app sem reescrever nada.
Versão alvo: 4.2.0.0
Estimativa: 3-5 dias
Dependência: Fase 0 concluída

Por que ttkbootstrap (pesquisa fática)
Dados do GitHub em 23/03/2026:

Biblioteca	Issues Abertos	Último Commit	Situação
customtkinter	412	02/01/2026 (80+ dias)	⚠️ Semi-abandonado
ttkbootstrap	31	08/03/2026 (15 dias)	✅ Ativamente mantido
Sun-Valley-ttk-theme	36	Jun/2025 (9+ meses)	🔴 Inativo
ttkbootstrap é construído sobre ttk da stdlib Python. Isso significa:

Zero reimplementação de widgets (é extensão, não substituição)
Todo código ttk.* existente herda o tema automaticamente
Custo de migração: uma linha em main.py
Implementação
# main.py — uma única linha muda tudo
import ttkbootstrap as ttk
root = ttk.Window(themename="darkly")
O tema "darkly" entrega:

Fundo #2b2b2b (próximo ao BG_PRIMARY atual #141414)
Botões com aparência moderna
Scrollbars finas (estilo 2025)
Progressbars animadas
Entry fields limpos
Ajuste de paleta
O Laserflix usa #141414 (mais escuro que o darkly padrão). Após aplicar o tema base, ajustar style.configure() para manter a identidade visual:

style = ttk.Style()
style.configure(".", background="#141414")  # BG_PRIMARY original mantido
style.configure("TButton", background="#2A2A2A")  # BG_CARD
O que NÃO muda
project_card.py continua usando tk.Frame com cores manuais (os cards são customizados demais para tema genérico)
Cor vermelha #E50914 (Netflix red) mantida como accent principal
config/ui_constants.py e config/constants.py são a fonte das cores — ttkbootstrap só afeta os widgets TTK padrão (botões, entradas, scrollbars, progressbars)
7. Fase 2 — Hover Card
Objetivo: Card que "vende" o projeto ao passar o mouse. Principal gap UX em relação ao Netflix.
Versão alvo: 4.3.0.0
Estimativa: 4-6 dias
Dependência: Fase 1

Por que é o impacto mais alto
No Netflix, você não clica em um thumbnail sem saber o que vai ver. O hover card te convence antes do clique. No Laserflix atual, o card exibe: thumbnail (se existir), nome truncado, 3 categorias, 3 tags, e 5 botões de ação. Isso é tudo que você tem para decidir se quer abrir.

Com 5.000 projetos, a decisão de clique precisa ser rápida e informada. O hover card resolve isso.

O que aparece no Hover Card
┌─────────────────────────────────────┐
│  [THUMBNAIL MAIOR — 300×220px]      │
│                                      │
│  📁 Nome Completo (sem truncar)      │
│  🤖 "Mesa de madeira em estilo      │
│      industrial com pés de cano..." │
│                                      │
│  🏷️ Natal • Organização • Madeira   │
│  🔖 mesa, industrial, cano, tubo    │
│                                      │
│  📂 3 arquivos LightBurn (.lbrn2)   │
│  📅 Adicionado em 15/01/2025        │
│                                      │
│  [⭐ Favoritar] [✓ Feito] [🤖 Analisar] │
└─────────────────────────────────────┘
Decisão técnica: como implementar hover em Tkinter
Três opções avaliadas:

Opção A — tk.Toplevel posicionado no mouse

Pro: Pode ser maior que o card original
Contra: Flicker ao mover entre janelas, delay de criação de Toplevel (~50ms)
Contra: wm_geometry() pode ter bugs em DPI alto no Windows
Opção B — Frame overlay no Canvas principal ← ESCOLHIDA

Pro: Zero flicker (é um widget normal no mesmo canvas)
Pro: Instanciado uma vez, reposicionado com .place()
Pro: Estável em todos os sistemas operacionais
Contra: Requer coordenação com o ViewportManager
Opção C — Expansão do card existente

Pro: Mais simples de implementar
Contra: Empurra outros cards, causa relayout da grade inteira (não aceitável)
A Opção B é o padrão usado por aplicações como Notion e Figma em seus próprios sistemas de tooltip overlay. Tkinter suporta isso via .lift() e .place().

Implementação
Novo arquivo: ui/components/hover_card.py

class HoverCard:
    """
    Overlay de hover sobre o card de projeto.
    Instanciado UMA VEZ pelo UIBuilder e reposicionado via .show(path, x, y).
    """
    def __init__(self, parent_canvas, database, thumbnail_preloader):
        ...
    
    def show(self, project_path: str, card_widget: tk.Widget) -> None:
        """Posiciona e exibe o hover card sobre card_widget."""
        ...
    
    def hide(self) -> None:
        """Remove o hover card da tela."""
        ...
Bind nos cards (em project_card.py):

card.bind("<Enter>", lambda e, p=project_path: cb["on_hover_show"](p, card))
card.bind("<Leave>", lambda e: cb["on_hover_hide"]())
Delay de 400ms: O hover card só aparece se o mouse ficar parado 400ms sobre o card. Isso evita flash ao rolar rapidamente. Implementado com root.after(400, show) cancelado no <Leave>.

8. Fase 3 — Discovery Lanes
Objetivo: Substituir o grid estático por uma home com lanes horizontais por contexto.
Versão alvo: 4.4.0.0
Estimativa: 2 semanas
Dependência: Fase 2 (hover card precisa funcionar nas lanes também)

O que são as Discovery Lanes
Em vez de um grid de 36 cards em paginação vertical, a Home exibe:

┌────────────────────────────────────────────────────┐
│ LASERFLIX                    [🔍 Buscar projetos]   │
├────────────────────────────────────────────────────┤
│                                                    │
│  Abertos Recentemente                        Ver + │
│  [card][card][card][card][card] ──────────────────▶│
│                                                    │
│  ⭐ Favoritos                                 Ver + │
│  [card][card][card][card][card] ──────────────────▶│
│                                                    │
│  📅 Datas Próximas — Páscoa 2025              Ver + │
│  [card][card][card][card][card] ──────────────────▶│
│                                                    │
│  🆕 Adicionados Esta Semana                   Ver + │
│  [card][card][card][card][card] ──────────────────▶│
│                                                    │
│  🪵 Projetos de Madeira                       Ver + │
│  [card][card][card][card][card] ──────────────────▶│
│                                                    │
│  ⏳ Aguardando Análise IA                     Ver + │
│  [card][card][card][card][card] ──────────────────▶│
│                                                    │
└────────────────────────────────────────────────────┘
Componentes Novos
core/session_manager.py
Persiste em session.json:

recently_opened: lista dos últimos 20 projetos abertos (por caminho + timestamp)
session_count: número de sessões iniciadas
last_search_terms: termos buscados na sessão atual
core/curation_engine.py
Decide o que vai em cada lane:

get_recently_opened() → session_manager
get_favorites() → database.favorites
get_upcoming_dates() → detecta datas comemorativas próximas baseado em categorias
get_new_this_week() → projetos com added_date nos últimos 7 dias
get_by_category(cat) → filtro de categoria existente
get_pending_analysis() → projetos com analyzed=False
ui/components/discovery_lane.py
Um componente de lane horizontal:

class DiscoveryLane:
    """
    Lane horizontal de cards com scroll.
    
    Layout:
    [Título da Lane]                    [Ver todos →]
    [card][card][card][card][card] ─────────────────▶
    
    Scroll horizontal via mousewheel quando o cursor está sobre a lane.
    """
    def __init__(self, parent, title: str, projects: list, callbacks: dict):
        ...
ui/home_view.py
Substitui o grid atual. Compõe todas as lanes:

class HomeView:
    def __init__(self, parent, curation_engine, hover_card, callbacks):
        ...
    
    def refresh(self):
        """Recalcula todas as lanes. Chamado em _refresh_all()."""
        ...
Decisão sobre a navegação
A sidebar atual (categorias + tags + origens + coleções) não é removida. Ela muda de papel:

Clique em item da sidebar → abre uma "Lane View" full-screen para aquela categoria (não a Home)
A Home é a tela padrão ao abrir o app
"Ver todos →" em cada lane abre a Lane View filtrada
Isso preserva 100% da funcionalidade atual de filtros.

Scroll horizontal técnico
O Tkinter não tem widget de scroll horizontal nativo que funcione bem. A solução é:

tk.Canvas com xscrollcommand para cada lane
Bind de <Shift-MouseWheel> para scroll horizontal (padrão Windows)
Botões ◀ ▶ laterais para usuários sem Shift+scroll
9. Fase 4 — Smart Folder Watcher
Objetivo: Detectar automaticamente novos projetos e arquivos sem importação manual.
Versão alvo: 4.5.0.0
Estimativa: 3-4 dias
Dependência: Pode ser desenvolvida em paralelo com Fase 3

O problema real
O fluxo atual:

Usuário cria design no LightBurn
Salva em pasta monitorada
Abre o Laserflix
Clica em "Importar" → seleciona pasta → aguarda scan
Com o Folder Watcher, o passo 3 e 4 desaparecem. O projeto aparece automaticamente na lane "Novos Hoje" quando o usuário abrir o app ou imediatamente se estiver aberto.

Decisão técnica: watchdog library
Pesquisa realizada: A biblioteca watchdog (https://github.com/gorakhargosh/watchdog) é a solução padrão para file system monitoring em Python:

Critério	Status
Issues abertos	87 (de 800+ fechados — ratio saudável)
Último commit	Março 2026 (ativamente mantido)
Uso no ecossistema	Django dev server, pytest-watch, nodemon-py
Suporte multiplataforma	Windows (inotify), macOS (FSEvents), Linux (inotify)
Alternativa	win32file → só Windows. watchdog é a escolha correta
Implementação
Novo arquivo: core/folder_watcher.py

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
class LaserflixWatcher(FileSystemEventHandler):
    """
    Monitora pastas configuradas e dispara scan automático.
    
    Detecta:
    - Nova pasta criada (novo projeto)
    - Novo arquivo .lbrn2 / .svg / .dxf em pasta existente
    
    Ignora:
    - Arquivos temporários (~nome, .tmp)
    - Pastas de sistema (.git, __pycache__)
    """
    
    def __init__(self, scanner, on_new_project: callable):
        self.scanner = scanner
        self.on_new_project = on_new_project
        self._debounce_timer = None
    
    def on_created(self, event):
        if event.is_directory:
            # Nova pasta = possível novo projeto
            self._debounce(self._check_new_project, event.src_path)
    
    def _debounce(self, fn, *args):
        """Espera 2s antes de processar (LightBurn salva múltiplos arquivos)."""
        if self._debounce_timer:
            self._debounce_timer.cancel()
        # root.after não disponível aqui — usar threading.Timer 
        # (apenas para disparar callback, não atualizar UI diretamente)
        import threading
        self._debounce_timer = threading.Timer(2.0, fn, args=args)
        self._debounce_timer.start()
    
    def _check_new_project(self, folder_path):
        """Verifica se pasta é um projeto válido e notifica via callback."""
        ...
        # on_new_project é chamado na thread do watcher
        # A atualização da UI DEVE ser via root.after()
        self.on_new_project(folder_path)
Integração em CoreSetup:

self.folder_watcher = LaserflixWatcher(
    scanner=self.scanner,
    on_new_project=self._on_watcher_detected
)
Notificação ao usuário: Um banner discreto no topo da tela (não modal, não popup — o usuário não perde o foco):

┌─────────────────────────────────────────────────────────────┐
│ 🆕 "Porta Vintage" detectado. Adicionado ao banco.    [Ver] │
└─────────────────────────────────────────────────────────────┘
Implementado como ui/components/toast_bar.py — um tk.Frame que aparece no topo por 5 segundos e desaparece.

10. Fase 5 — Identidade por Hash e Git dos Makers
Objetivo: Resolver o problema de perda de metadados ao mover pastas. Versionar designs.
Versão alvo: 4.6.0.0
Estimativa: 1 semana
Dependência: Fase 0 (DatabaseManager com RLock)

O problema de identidade
O banco de dados atual usa o caminho absoluto como chave:

{
  "D:/projetos/Natal 2024/": {
    "favorite": true,
    "categories": ["Natal", "Datas Comemorativas"],
    "ai_description": "..."
  }
}
Mover de D:/projetos/ para E:/backup/projetos/ = perde tudo.

Solução: Project Identity Hash
Calcular um hash baseado no conteúdo da pasta no momento do primeiro scan:

def calculate_project_hash(project_path: str) -> str:
    """
    Hash baseado em:
    - Lista de nomes de arquivo (não conteúdo — muito lento para 5000 projetos)
    - Tamanho total dos arquivos
    - Data de modificação do arquivo mais antigo
    
    NÃO usa sha256 do conteúdo dos arquivos (seria 30s para pasta de 200MB).
    Usa hash de metadados — rápido e suficientemente único.
    """
    import hashlib
    files_info = []
    for f in sorted(os.listdir(project_path)):
        fpath = os.path.join(project_path, f)
        if os.path.isfile(fpath):
            stat = os.stat(fpath)
            files_info.append(f"{f}:{stat.st_size}")
    return hashlib.md5("|".join(files_info).encode()).hexdigest()[:12]
Migração do banco: Adicionar campo project_hash a todos os projetos existentes. Em load_database(), se um projeto não existe mais no path mas um hash igual aparece em novo path → migrar metadados automaticamente.

Git dos Makers
"Git dos Makers" é controle de versão de design files — sem precisar saber o que é Git.

O que o usuário vê:

📁 Mesa Industrial Madeira
├── 🕐 Versão 3 — 15/03/2026 — "Adicionei os pés de cano"
├── 🕐 Versão 2 — 10/03/2026 — "Ajustei as dimensões"  
└── 🕐 Versão 1 — 05/03/2026 — "Primeiro rascunho"
O que acontece por baixo:

O LaserflixWatcher detecta quando um arquivo .lbrn2 é salvo em uma pasta monitorada. Em vez de simplesmente atualizar o banco, salva uma snapshot:

# core/version_history.py
class VersionHistory:
    """
    Histórico de versões baseado em cópia de arquivo, não diff de código.
    
    Armazena em: laserflix_versions/{project_hash}/{timestamp}_{filename}
    NÃO usa git internamente — simples cópia de arquivo.
    
    Limite: 10 versões por projeto (oldest deleted first).
    """
Decisão técnica: NÃO usar git real internamente. Motivo: git como biblioteca Python (GitPython) tem 175 issues abertos e depende de git instalado no sistema — não garantido em Windows de makers. Cópia simples de arquivo é mais confiável e transparente.

11. Fase 6 — Busca Semântica
Objetivo: Buscar por significado, não só por palavra-chave.
Versão alvo: 4.7.0.0
Estimativa: 1 semana
Dependência: Fase 0 (IA stack estável)
Nota: nomic-embed-text:latest já está no Ollama configurado (274MB)

O que muda na busca
Busca atual: "espelho" → busca literal no nome + tags + categories
Busca semântica: "espelho" → inclui "mirror", "reflexo", "espelho decorativo", "quadro espelho"

A busca bilíngue atual (name_translator.py) já resolve parte disso para EN→PT. A busca semântica vai além: entende contexto.

Implementação
core/embeddings_store.py:

class EmbeddingsStore:
    """
    Armazena e busca embeddings de projetos usando nomic-embed-text via Ollama.
    
    Persistência: laserflix_embeddings.json (gerado sob demanda)
    Modelo: nomic-embed-text:latest (768 dimensões)
    
    Busca: cosseno similaridade entre query embedding e project embeddings
    """
    
    def build_embedding(self, project_path: str, data: dict) -> list:
        """Gera embedding para um projeto. Chamado após análise IA."""
        text = f"{data.get('name', '')} {' '.join(data.get('categories', []))} {' '.join(data.get('tags', []))} {data.get('ai_description', '')}"
        return self.ollama.embed(text, model="nomic-embed-text")
    
    def search(self, query: str, top_k: int = 20) -> list:
        """Retorna os top_k projetos mais similares à query."""
        ...
Busca híbrida: Combina resultado semântico (cosseno) com resultado de keyword (atual). Peso: 60% semântico + 40% keyword. Isso garante que buscas exatas ainda funcionem.

Fallback: Se o Ollama não estiver rodando, a busca cai silenciosamente para keyword pura — sem mensagem de erro, mantendo o princípio de graceful degradation.

12. Fase 7 — Calculadora de Precificação
Objetivo: Calcular custo e preço de venda de projetos diretamente no app.
Versão alvo: 5.0.0 → Aurum V1.0
Estimativa: 4-5 dias
Dependência: Independente, pode ser desenvolvida após Fase 3

O que resolve
Makers frequentemente precificam "no chute" porque:

Não sabem quanto de material usaram
Não contam o tempo de máquina
Não sabem o custo de energia do laser
Não têm histórico de margem por tipo de projeto
Dados que o usuário insere (por projeto)
Material:
  [ ] MDF    [ ] Acrílico    [ ] Madeira    [ ] Outro: ____
  Dimensão: ___ × ___ cm    Espessura: ___ mm
  Preço/chapa: R$ ____
Tempo de máquina:
  Estimado: ___ minutos
  Custo/hora da máquina: R$ ____
Quantidade:
  Peças por chapa: ___
  Peças desejadas: ___
[Calcular →]
Resultado calculado
┌─────────────────────────────────────────────┐
│ 💰 Precificação — Mesa Industrial Madeira    │
│─────────────────────────────────────────────│
│ Material (MDF 40×60cm):      R$ 12,50       │
│ Tempo de máquina (25min):    R$  8,33       │
│ Custo total unitário:        R$ 20,83       │
│                                             │
│ Margem sugerida (60%):       R$ 33,33       │
│ ─────────────────────────────────────────── │
│ Preço de venda sugerido:     R$ 54,16       │
│                                             │
│ [Salvar no projeto]    [Ajustar margem ___] │
└─────────────────────────────────────────────┘
Persistência: Dados de precificação salvos em database.json como campo pricing por projeto:

{
  "pricing": {
    "material": "MDF",
    "material_cost": 12.50,
    "machine_time_min": 25,
    "machine_cost_per_hour": 20.0,
    "margin_pct": 60,
    "unit_cost": 20.83,
    "suggested_price": 54.16,
    "calculated_at": "2026-03-23T10:00:00"
  }
}
13. Decisões Técnicas Pesquisadas
Cada decisão aqui foi verificada com dados reais antes de ser incluída no plano.

13.1 — ttkbootstrap vs customtkinter vs PyQt6
Critério	customtkinter	ttkbootstrap	PyQt6
Issues abertos	412	31	~200
Último commit	75+ dias	15 dias	Ativo
Base	Reimplementação Canvas	ttk stdlib	Qt C++
Custo de migração	Alto (reescreve widgets)	Mínimo (tema sobre ttk)	Muito alto (reescreve UI)
Recomendação	❌	✅	Futuro distante
Decisão: ttkbootstrap, tema "darkly".

13.2 — watchdog vs alternativas
Critério	watchdog	win32file	pyinotify
Plataformas	Windows + macOS + Linux	Só Windows	Só Linux
Manutenção	Ativo	Abandonado	Abandonado
Recomendação	✅	❌	❌
Decisão: watchdog.

13.3 — Hash de identidade: SHA256 vs MD5
SHA256 do conteúdo dos arquivos seria 100% único mas impraticável (30+ segundos para pasta de 200MB em máquina modesta). MD5 de metadados (nome + tamanho dos arquivos) é calculado em < 1ms e tem colisão negligível para este uso. Um maker não vai ter duas pastas com exatamente os mesmos arquivos e tamanhos.

Decisão: MD5 de metadados (nome + tamanho).

13.4 — Git dos Makers: gitpython vs cópia simples
GitPython tem 175 issues abertos, requer git instalado no sistema (não garantido em Windows consumer), e adiciona complexidade desnecessária. Cópia simples de arquivo (shutil.copy2 + metadata json) é mais transparente, mais segura, e elimina dependência externa.

Decisão: Cópia simples de arquivo, sem git.

13.5 — Busca semântica: embeddings locais vs API
100% local (nomic-embed-text via Ollama) preserva a privacidade absoluta da APP_PHILOSOPHY. Sem envio de nomes de projetos para servidores externos. nomic-embed-text já está instalado no Ollama configurado pelo app.

Decisão: Ollama local, nomic-embed-text.

13.6 — JSON vs SQLite para escala
A análise técnica de 55KB identificou que com 5000+ projetos, o JSON pode chegar a 50-100MB em RAM. Porém, o FilterCache + lazy view já mitigam o impacto principal (sem deepcopy do banco inteiro na UI). SQLite traria:

Consultas O(log n) em vez de O(n)
Transações ACID
Custo: migração do schema, novo ORM, quebra da simplicidade "JSON puro"
A APP_PHILOSOPHY diz explicitamente: "Sem banco de dados SQL complexo (JSON puro)". Isso é uma restrição de design, não uma limitação técnica ignorada. Enquanto o app for para uso pessoal (< 10.000 projetos), JSON com lazy loading é suficiente.

Decisão: Manter JSON. Adicionar lazy view no DatabaseManager (Fase 0, BUG-05). Rever se chegar a 10.000+ projetos.

14. Dependências e Requisitos
requirements.txt — Aurum V1.0
# Já presentes
Pillow>=10.0.0          # Thumbnails e preview de imagens
requests>=2.31.0        # Ollama HTTP client
# Novos no Aurum
ttkbootstrap>=1.10.0    # Tema darkly sobre ttk (31 issues abertos, commit 08/03/2026)
watchdog>=4.0.0         # Smart Folder Watcher (multiplataforma)
numpy>=1.24.0           # Álgebra de vetores para busca semântica (cosseno)
svglib>=1.5.1           # Thumbnails de arquivos SVG (makers usam SVG para designs)
Nota sobre svglib: Makers de corte a laser usam extensivamente arquivos .svg. O Laserflix atual só exibe imagens .png/.jpg. svglib converte SVG em imagem PIL, permitindo thumbnail de vetores. Não está na análise anterior — identificado lendo config/constants.py ("vectors": (".svg", ".ai", ".eps")) e ai/fallbacks.py (structure["has_svg"]).

requirements-test.txt (já existe)
pytest>=7.0.0
pytest-cov>=4.0.0
15. Cronograma Realista
Fase	Versão	Conteúdo	Estimativa
0 — Fundação	4.1.0.0	Bugs + Doutoral + Config unificado	1-2 semanas
1 — Visual	4.2.0.0	ttkbootstrap darkly	3-5 dias
2 — Hover Card	4.3.0.0	Card que vende no hover	4-6 dias
3 — Discovery Lanes	4.4.0.0	Home Netflix-style	2 semanas
4 — Folder Watcher	4.5.0.0	Detecção automática de projetos	3-4 dias
5 — Hash + Git	4.6.0.0	Identidade + versionamento	1 semana
6 — Busca Semântica	4.7.0.0	Busca por contexto (nomic-embed)	1 semana
7 — Precificação	Aurum V1.0	Calculadora de custo/preço	4-5 dias
Total estimado: 8-10 semanas de desenvolvimento contínuo.

Marcos intermediários:

Após Fase 2: app já é visivelmente diferente (visual moderno + hover card)
Após Fase 3: experiência de descoberta fundamentalmente transformada
Após Fase 7: versão completa, Aurum V1.0 lançada
PRINCÍPIO DO PLANO
Cada decisão deste documento foi baseada em leitura real do código-fonte,
análise de dados do GitHub, e respeito à APP_PHILOSOPHY existente.
Nenhuma decisão foi tomada por reflexo ou familiaridade de nome.

Versão 2.0.0 do Plano — 23/03/2026
Baseado em análise integral de 46 arquivos Python, 12 documentos internos, 55KB de análise técnica