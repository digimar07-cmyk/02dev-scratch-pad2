# TECH AUDIT — Laserflix v4.0.0.9

> **Documento gerado em:** 09/03/2026  
> **Versão auditada:** 4.0.0.9  
> **Tipo:** Análise Técnica Sênior + Veredito de Banca Examinadora de Doutorado  
> **Ferramenta de análise:** Perplexity AI (Claude Sonnet 4.6)  
> **Status do documento:** ✅ Registrado e versionado

---

## Índice

1. [Visão Geral da Arquitetura](#1-visão-geral-da-arquitetura)
2. [Mapa de Arquivos por Camada](#2-mapa-de-arquivos-por-camada)
3. [Análise Individual dos Arquivos Críticos](#3-análise-individual-dos-arquivos-críticos)
4. [Correlações entre Componentes](#4-correlações-entre-componentes)
5. [Problemas por Severidade](#5-problemas-por-severidade)
6. [Scorecard Técnico — Ranking por Categoria](#6-scorecard-técnico--ranking-por-categoria)
7. [Banca Examinadora — Veredito Doutoral](#7-banca-examinadora--veredito-doutoral)
8. [Condições Obrigatórias para Aprovação](#8-condições-obrigatórias-para-aprovação)
9. [Plano de Ação Pós-Banca](#9-plano-de-ação-pós-banca)

---

## 1. Visão Geral da Arquitetura

O Laserflix é uma aplicação desktop Python/Tkinter de gerenciamento de projetos de produção gráfica com análise por IA local (Ollama). O projeto passou por refatoração progressiva significativa — de um monolito de 868 linhas num único arquivo para uma arquitetura em camadas com **46 arquivos distribuídos em 8 camadas lógicas**, totalizando ~240 KB de código-fonte.

A filosofia de design documentada segue **Kent Beck "Tidy First"** — micro-refactorings incrementais com zero quebra de funcionalidade a cada passo.

### Stack Tecnológico

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.10+ |
| Interface Gráfica | Tkinter (stdlib) |
| Persistência | JSON com escrita atômica |
| IA Local | Ollama + qwen3.5:4b (3.4 GB) |
| Embeddings | nomic-embed-text:latest (274 MB) |
| Imagens | Pillow (PIL) |
| Versionamento | Git + GitHub |

---

## 2. Mapa de Arquivos por Camada

```
┌──────────────────────────────────────────────────────────────┐
│  ENTRY          main.py (502 bytes)                          │
├──────────────────────────────────────────────────────────────┤
│  CONFIG         settings.py · card_layout.py · ui_constants  │
├──────────────────────────────────────────────────────────────┤
│  CORE           database.py (13.2 KB)                        │
│                 collections_manager.py (13.4 KB)             │
│                 thumbnail_preloader.py · project_scanner.py  │
├──────────────────────────────────────────────────────────────┤
│  AI             ollama_client.py · image_analyzer.py         │
│                 text_generator.py · fallbacks.py             │
│                 analysis_manager.py                          │
├──────────────────────────────────────────────────────────────┤
│  UI/Controllers  optimized_display_controller.py (14.2 KB)   │
│                  ⚠️  display_controller.py (14.6 KB) LEGADO  │
│                  selection_controller.py (5.0 KB)            │
│                  analysis_controller.py (11.5 KB)            │
│                  collection_controller.py (2.8 KB)           │
│                  ⚠️  project_management_controller.py MORTO  │
│                  ⚠️  modal_manager.py (PASTA ERRADA)         │
├──────────────────────────────────────────────────────────────┤
│  UI/Managers    dialog_manager.py (6.0 KB)                   │
│                 toggle_manager.py (3.2 KB)                   │
│                 orphan_manager.py (2.8 KB)                   │
│                 collection_dialog_manager.py (2.2 KB)        │
│                 modal_generator.py (2.7 KB)                  │
│                 progress_ui_manager.py (857 bytes)           │
├──────────────────────────────────────────────────────────────┤
│  UI/Builders    ui_builder.py · header_builder.py            │
│                 cards_grid_builder.py · navigation_builder   │
├──────────────────────────────────────────────────────────────┤
│  UI/Components  selection_bar.py · chips_bar.py              │
│                 pagination_controls.py                       │
├──────────────────────────────────────────────────────────────┤
│  UI/Views       main_window.py (26.9 KB) ← ORQUESTRADOR      │
│                 sidebar.py (11.9 KB)                         │
│                 header.py (13.2 KB)                          │
│                 project_card.py (15.6 KB)                    │
│                 project_modal.py (17.9 KB)                   │
│                 collections_dialog.py (14.1 KB)              │
│                 recursive_import_integration.py (20.4 KB)    │
│                 edit_modal.py (5.1 KB)                       │
│                 ⚠️  virtual_scroll.py (9.0 KB) NÃO INTEGRADO │
└──────────────────────────────────────────────────────────────┘
```

### Inventário de Arquivos por Camada

| Camada | Arquivos | Tamanho Total | Status |
|---|:---:|---:|---|
| Entry | 1 | 502 B | ✅ Limpo |
| Config | 3 | 3.7 KB | ✅ Limpo |
| Core | 4 | 26.6 KB | ⚠️ API incompleta |
| AI | 5 | n/d | ✅ Limpo |
| UI/Controllers | 7 | 56.1 KB | 🔴 3 arquivos problema |
| UI/Managers | 6 | 17.7 KB | ✅ Limpo |
| UI/Builders | 4 | n/d | ✅ Limpo |
| UI/Components | 3 | n/d | ✅ Limpo |
| UI/Views | 9 | 133.9 KB | ⚠️ 1 arquivo não integrado |
| Utils | 2 | n/d | ✅ Limpo |
| **TOTAL** | **~46** | **~240 KB** | |

---

## 3. Análise Individual dos Arquivos Críticos

### `main_window.py` — Orquestrador Central (26.863 bytes)

**Padrão aplicado:** Orchestrator / Mediator  
**Risco de edição no Git:** 🔴 ALTO — qualquer mudança exige entender toda a cadeia de callbacks

- É o único arquivo que conhece todos os outros
- Inicializa controllers, conecta callbacks e delega tudo
- Após refatoração: ~600 linhas (era 868)
- `__init__` ainda tem ~280 linhas de setup sequencial — limite aceitável para Mediator, mas no limite
- Imports locais dentro de `display_projects()` para evitar circular import → sintoma de acoplamento estrutural não resolvido
- **Ação requerida:** Decompor `__init__` em métodos `_setup_core()`, `_setup_controllers()`, `_build_ui()`, `_setup_callbacks()`

---

### `database.py` — Repositório Principal (13.220 bytes)

**Padrão aplicado:** Repository + Atomic Write  
**Risco de edição no Git:** 🟢 BAIXO — bem encapsulado

- Escrita atômica via `tmp + os.replace()` ✅
- Tratamento de `UnicodeDecodeError`, `JSONDecodeError` ✅
- Fallback para `.bak` automático ✅
- **Problema crítico:** expõe `self.database` como dict público
- `main_window` usa `self.database = self.db_manager.database` — referência direta ao dict interno que pode ficar stale silenciosamente
- **Ação requerida:** Adicionar API pública (`get_project()`, `remove_project()`, `all_paths()`, `project_count()`)

```python
# SOLUÇÃO — adicionar ao DatabaseManager:
def get_project(self, path: str) -> dict | None:
    return self.database.get(path)

def remove_project(self, path: str) -> bool:
    if path not in self.database: return False
    del self.database[path]
    return True

def all_paths(self) -> list[str]:
    return list(self.database.keys())

def project_count(self) -> int:
    return len(self.database)
```

---

### `collections_manager.py` — Repositório de Coleções (13.409 bytes)

**Padrão aplicado:** Repository com CRUD completo  
**Risco de edição no Git:** 🟢 BAIXO

- API clara e previsível ✅
- `clean_orphan_projects()` e `get_stats()` implementados ✅
- `add_collection()` como alias de `create_collection()` — boa prática de retrocompatibilidade ✅
- Um dos módulos mais estáveis e bem implementados do projeto

---

### `selection_controller.py` — Controller de Seleção (5.001 bytes)

**Padrão aplicado:** MVC Controller  
**Risco de edição no Git:** 🟢 BAIXO — sem dependência de Tkinter

- Comunicação 100% via callbacks ✅
- Sem dependência de widgets Tkinter — testável em isolamento ✅
- **BUG CRÍTICO CORRIGIDO em 09/03/2026:** `db_manager.save()` não existia → corrigido para `db_manager.save_database()`
- **BUG CRÍTICO CORRIGIDO em 09/03/2026:** `on_refresh_needed` não incluía `sidebar.refresh()` → corrigido para apontar para `_refresh_all()`
- Este bug existiu desde a criação do controller e só foi descoberto em uso real por ausência de testes
- **Ação requerida:** Criar `tests/test_selection_controller.py`

```python
# TESTE MÍNIMO QUE TERIA CAPTURADO O BUG:
def test_remove_selected_persists_to_disk(tmp_path):
    db_file = tmp_path / "test.json"
    db_manager = DatabaseManager(db_file)
    db_manager.database = {"/proj/a": {"name": "A"}, "/proj/b": {"name": "B"}}
    ctrl = SelectionController(db_manager.database, db_manager, CollectionsManager())
    ctrl.selection_mode = True
    ctrl.selected_paths = {"/proj/a"}
    ctrl.remove_selected(parent_window=None)
    assert "/proj/a" not in db_manager.database
    reloaded = DatabaseManager(db_file)
    reloaded.load_database()
    assert "/proj/a" not in reloaded.database
```

---

### `optimized_display_controller.py` — Controller de Display Ativo (14.184 bytes)

**Padrão aplicado:** MVC Controller com cache de filtros  
**Risco de edição no Git:** 🟡 MÉDIO

- Gerencia filtros empilháveis, ordenação, paginação e cache invalidation ✅
- O arquivo mais complexo da camada de controllers
- **Problema:** coexiste com `display_controller.py` legado (14.617 bytes) que não foi removido
- **Ação requerida:** Remover `display_controller.py` imediatamente

---

### `recursive_import_integration.py` — Workflow de Importação (20.365 bytes)

**Padrão aplicado:** Workflow / Facade  
**Risco de edição no Git:** 🔴 ALTO — maior arquivo da camada de UI

- Gerencia fluxo completo de importação recursiva com análise IA em thread separada ✅
- É o maior arquivo da camada UI/View — indica acúmulo de responsabilidades
- **Ação requerida:** Avaliar extração de responsabilidades secundárias para classes auxiliares

---

### `project_card.py` — Widget do Card (15.595 bytes)

**Padrão aplicado:** Composite Widget  
**Risco de edição no Git:** 🟡 MÉDIO

- Aceita callbacks via dict `cb={}` — interface limpa que desacopla widget do controller ✅
- Integra thumbnail async, toggles e modo seleção ✅
- Bem implementado para o escopo

---

### `virtual_scroll.py` — Scroll Virtual (8.960 bytes)

**Padrão aplicado:** Widget customizado  
**Status:** ⚠️ NÃO INTEGRADO

- Implementação existe e está completa
- `main_window` usa paginação simples em vez de scroll virtual
- **Ação requerida:** Integrar OU remover. Manter no repositório sem uso é débito técnico

```python
# COMO INTEGRAR (solução):
from ui.virtual_scroll import VirtualScroll

# No _setup_core() do main_window:
self.virtual_scroll = VirtualScroll(
    canvas=self.content_canvas,
    item_height=220,
    render_callback=self._render_card_at_index
)
```

---

## 4. Correlações entre Componentes

```
main_window.py (Mediator/Orquestrador)
  │
  ├── SelectionController
  │     ├── .database (dict — referência direta ⚠️)
  │     ├── db_manager.save_database()        ✅ (corrigido 09/03/2026)
  │     ├── collections_manager.save()        ✅
  │     ├── on_mode_changed → hide SelectionBar
  │     ├── on_projects_removed → _on_projects_removed()
  │     └── on_refresh_needed → _refresh_all()  ✅ (corrigido 09/03/2026)
  │
  ├── OptimizedDisplayController
  │     ├── FilterCache (interno)
  │     ├── .database (dict — referência direta ⚠️)
  │     └── on_display_updated → main_window callbacks
  │
  ├── AnalysisController
  │     └── AnalysisManager
  │           └── TextGenerator / ImageAnalyzer
  │                 └── OllamaClient
  │                       └── [fallbacks.py se offline]
  │
  ├── Sidebar
  │     └── sidebar.refresh(database, collections_manager)
  │           └── chamado por _refresh_all() ← PONTO CRÍTICO
  │
  ├── CollectionController
  │     └── CollectionsManager.save()
  │
  └── DialogManager / ModalGenerator
        └── Delega abertura de todos os diálogos
```

### Pontos de Falha Conhecidos e Status

| Ponto de Falha | Status | Data do Fix |
|---|---|---|
| `save()` inexistente no `SelectionController` | ✅ Corrigido | 09/03/2026 |
| `on_refresh_needed` sem sidebar.refresh | ✅ Corrigido | 09/03/2026 |
| Referência direta ao dict interno do DB | ⚠️ Em aberto | — |
| Imports circulares via import local | ⚠️ Em aberto | — |

---

## 5. Problemas por Severidade

### 🔴 Críticos — Dívida Técnica Imediata

| # | Arquivo | Problema | Solução |
|---|---|---|---|
| 1 | `display_controller.py` | Controller LEGADO não removido — dois controllers para a mesma função | `git rm ui/controllers/display_controller.py` |
| 2 | `project_management_controller.py` | Não importado em lugar algum — código morto | `git rm ui/controllers/project_management_controller.py` |
| 3 | `virtual_scroll.py` | Implementação completa não integrada | Integrar com VirtualScroll ou `git rm` |
| 4 | `main_window_pre_selectionctrl.py` | Arquivo de backup (100 bytes) no repositório de produção | `git rm ui/main_window_pre_selectionctrl.py` |
| 5 | `modal_manager.py` em `/controllers/` | Está na pasta errada — é um Manager, não um Controller | Mover para `/managers/` |

```bash
# COMANDO PARA LIMPAR TODOS DE UMA VEZ:
git rm laserflix_v4.0.0.8_Stable/ui/controllers/display_controller.py
git rm laserflix_v4.0.0.8_Stable/ui/controllers/project_management_controller.py
git rm laserflix_v4.0.0.8_Stable/ui/virtual_scroll.py
git rm laserflix_v4.0.0.8_Stable/ui/main_window_pre_selectionctrl.py
git rm "laserflix_v4.0.0.8_Stable/Novo(a) Text Document.txt"
git commit -m "chore: remove dead code — 5 arquivos não utilizados ou legados"
```

---

### 🟡 Médios — Risco Operacional

| # | Problema | Impacto | Solução |
|---|---|---|---|
| 1 | Referência direta ao dict interno do DB via `self.database` | Violação de DIP; stale reference silenciosa se DB recriar o dict | Adicionar API pública ao `DatabaseManager` |
| 2 | Ausência de type hints | Sem suporte a `mypy`/`pyright`; refactoring inseguro | Adicionar type hints em `core/` e `ui/controllers/` |
| 3 | Zero testes unitários | Bugs críticos só detectados em uso real (como o de hoje) | Criar `tests/` com `pytest`, mínimo 60% coverage em core/ e controllers/ |
| 4 | Callbacks sem contrato formal | Assinatura esperada desconhecida para IDE e revisores | Usar `typing.Protocol` ou `Callable` com assinatura explícita |
| 5 | Imports locais dentro de métodos | Sintoma de acoplamento circular; imports locais mascaram o problema | Resolver o ciclo com injeção de dependência |
| 6 | `__init__` do `main_window` com ~280 linhas | Constructor Overload Syndrome — testabilidade reduzida | Decompor em métodos `_setup_*` |

---

### 🟢 Baixos — Limpeza de Repositório

| # | Arquivo | Problema |
|---|---|---|
| 1 | `Novo(a) Text Document.txt` | Arquivo vazio — lixo de desenvolvimento |
| 2 | `PERSONA_MASTER_CODER.md` | Prompt de instrução de IA dentro do repositório de código-fonte |

---

## 6. Scorecard Técnico — Ranking por Categoria

> Avaliação conforme padrões ISO/IEC 25010 (SQuaRE — Software Quality Requirements and Evaluation)

| Categoria de Avaliação | Score | Justificativa |
|---|:---:|---|
| **Arquitetura / Separação de Camadas** | 7.5/10 | MVC bem definido; 3 arquivos problemáticos na camada Controller contaminam a estrutura |
| **Coesão dos Módulos (SRP)** | 7.0/10 | Maioria tem responsabilidade única; `main_window.__init__` ainda é denso |
| **Acoplamento (DIP / IoC)** | 6.5/10 | Callbacks desacoplam bem; referência direta ao dict interno viola DIP |
| **Qualidade de Código** | 6.0/10 | Ausência de type hints e docstrings inconsistentes reduzem a nota |
| **Segurança de Dados (Persistência)** | 8.5/10 | Escrita atômica + `.bak` + auto-backup com limite são práticas de produção |
| **Performance** | 7.5/10 | Cache de filtros, thumbnail preloader async e paginação funcionam; virtual scroll não integrado |
| **Testabilidade** | 2.0/10 | Zero testes. Controllers sem Tkinter são testáveis — mas nenhum foi testado |
| **Manutenibilidade (Modificar no Git)** | 6.0/10 | Camada de Controller segura; mudanças em `main_window.py` são de alto risco |
| **Documentação Interna** | 7.0/10 | CHANGELOG, README, REFACTORING_STATUS detalhados; docstrings nos métodos principais |
| **Limpeza do Repositório** | 4.5/10 | 5 arquivos mortos/legados em produção |
| **Resiliência a Falhas (IA offline)** | 9.0/10 | Sistema de fallbacks robusto — app funciona sem Ollama |
| **Versionamento** | 8.0/10 | VERSION + settings.py + CHANGELOG sincronizados; commits semânticos |
| **Score Geral Ponderado** | **6.6/10** | Competente com dívida técnica acumulada não resolvida |

---

## 7. Banca Examinadora — Veredito Doutoral

> Sessão pública realizada em 09/03/2026.
> Banca composta por 5 doutores em Engenharia de Software.
> Os pareceres abaixo são integrais e irrecorríveis.

---

### Prof. Dr. Heinrich Brandt — Arquitetura de Software (TU Berlin)

**Pontos Positivos:**
- Separação em camadas é reconhecível e não trivial para desenvolvimento solo
- Padrão Mediator no `main_window.py` com comunicação via callbacks é válido e bem executado
- Escrita atômica no `DatabaseManager` demonstra conhecimento de concorrência de I/O

**Pontos Negativos:**
- Dois controllers para a mesma função coexistem no mesmo diretório — isso é abandono, não refatoração
- `modal_manager.py` na pasta `/controllers/` — falta de disciplina para respeitar a estrutura criada
- Múltiplos arquivos legados sem remoção após substituição

**Veredicto:** **REPROVADO neste critério.** Corrija e reapresente.

---

### Profa. Dra. Yuki Tanaka — Qualidade e Engenharia de Confiabilidade (Universidade de Tóquio)

**Pontos Positivos:**
- Sistema de fallback para Ollama offline é robusto e demonstra pensamento defensivo
- Backup atômico com `.bak` e auto-backup com limite de arquivos são práticas de produção reais

**Pontos Negativos:**
- Zero arquivos de teste no repositório
- Bug crítico (`save()` inexistente) existiu desde a criação do controller e foi descoberto apenas em uso real
- Um teste de 8 linhas com `pytest` teria capturado esse bug no momento em que foi escrito
- Um software sem testes não é um software de doutorado — é um protótipo

**Veredicto:** **REPROVADO neste critério.** Exige cobertura mínima de 60% em `core/` e `ui/controllers/`.

---

### Prof. Dr. Aleksandr Volkov — Padrões de Projeto e OO (Universidade Estatal de Moscou)

**Pontos Positivos:**
- Padrão Strategy no sistema de fallbacks de IA é correto e bem executado
- Padrão Builder na camada `ui/builders/` aplicado de forma consistente
- Padrão Observer nos managers de progresso está bem isolado

**Pontos Negativos:**
- `self.database = self.db_manager.database` viola o Princípio de Demeter e o DIP simultaneamente
- Callbacks sem contrato formal (`Protocol`/`ABC`) — ninguém sabe a assinatura esperada
- Se amanhã precisar migrar de JSON para SQLite, terá que reescrever cinco arquivos em vez de um

**Veredicto:** **REPROVADO parcialmente.** Refatoração da API do `DatabaseManager` é condição para aprovação.

---

### Profa. Dra. Amara Osei — Manutenibilidade e Evolução de Software (Universidade de Acra / MIT)

**Pontos Positivos:**
- `CHANGELOG.md` com causa raiz, fluxo de execução documentado e commits semânticos é excelente
- Versionamento com `VERSION + settings.py + CHANGELOG` sincronizados demonstra maturidade de processo
- Documentação de refatoração no `REFACTORING_STATUS.md` é prática rara e valiosa

**Pontos Negativos:**
- Zero type hints em 2026 é inaceitável — `mypy` teria capturado o bug `save()` automaticamente
- `__init__` com 280 linhas é Constructor Overload Syndrome — um programa dentro de um programa
- Imports locais dentro de métodos mascaram acoplamento circular que deveria ser resolvido na raiz

**Veredicto:** **APROVADO com restrições.** Type hints e decomposição do `__init__` são condições para aprovação plena.

---

### Prof. Dr. Carlos Mendonça — IHC e Sistemas de Produção (USP)

**Pontos Positivos:**
- O produto tem valor real de uso — gerenciamento completo com IA local é ambicioso e foi executado
- Escolha do `qwen3.5:4b` multimodal (84.7% menos espaço) é inteligente tecnicamente
- Ollama local garante privacidade dos dados do usuário — escolha correta para app de produção gráfica

**Pontos Negativos:**
- Bug de feedback falso: cards sumiam da tela mas voltavam ao reiniciar — violação das heurísticas de Nielsen (Visibilidade do Status do Sistema)
- `virtual_scroll.py` construído e não integrado — desperdício técnico e de experiência do usuário
- `recursive_import_integration.py` com 20 KB é o maior arquivo de UI — acúmulo de responsabilidades indevidas

**Veredicto:** **APROVADO como produto. REPROVADO como tese.** Valor de uso ≠ prova de escolhas corretas.

---

## 8. Condições Obrigatórias para Aprovação

> **Resultado final da banca:** REPROVADO — COM DIREITO A REAPRESENTAÇÃO EM 90 DIAS

A banca reconhece que o trabalho demonstra competência técnica prática acima da média para desenvolvimento solo. A arquitetura em camadas, a qualidade da persistência, o sistema de fallback de IA e a documentação de processo são contribuições reais.

**Entretanto, os seguintes pontos são inaceitáveis para aprovação em nível de doutorado:**

| # | Condição Obrigatória | Avaliador | Prazo |
|---|---|---|---|
| 1 | Remover os 5 arquivos mortos/legados do repositório | Prof. Brandt | Sprint 1 |
| 2 | Cobertura mínima 60% em `core/` e `ui/controllers/` com `pytest` | Profa. Tanaka | Sprint 2 |
| 3 | API pública no `DatabaseManager` — eliminar acesso direto ao dict interno | Prof. Volkov | Sprint 2 |
| 4 | Type hints completos em todos os arquivos de `core/` e `ui/controllers/` | Profa. Osei | Sprint 2 |
| 5 | Decomposição do `__init__` de `main_window.py` em métodos `_setup_*` | Profa. Osei | Sprint 3 |
| 6 | Integração do `virtual_scroll.py` OU remoção definitiva | Prof. Mendonça | Sprint 1 |
| 7 | Mover `modal_manager.py` de `/controllers/` para `/managers/` | Prof. Brandt | Sprint 1 |

> *"O código que não pode ser testado por outro engenheiro não é código de engenharia — é artesanato."*
> — Banca Examinadora, 09/03/2026

---

## 9. Plano de Ação Pós-Banca

### Sprint 1 — Limpeza (sem risco, alto impacto)

```bash
# 1. Remover arquivos mortos
git rm laserflix_v4.0.0.8_Stable/ui/controllers/display_controller.py
git rm laserflix_v4.0.0.8_Stable/ui/controllers/project_management_controller.py
git rm laserflix_v4.0.0.8_Stable/ui/virtual_scroll.py          # ou integrar
git rm laserflix_v4.0.0.8_Stable/ui/main_window_pre_selectionctrl.py
git rm "laserflix_v4.0.0.8_Stable/Novo(a) Text Document.txt"

# 2. Mover modal_manager para pasta correta
git mv laserflix_v4.0.0.8_Stable/ui/controllers/modal_manager.py \
        laserflix_v4.0.0.8_Stable/ui/managers/modal_manager.py

git commit -m "chore: remove dead code + move modal_manager to /managers/"
```

### Sprint 2 — Qualidade de Código

```python
# 1. Type hints — exemplo para selection_controller.py
from typing import Optional, Callable
import tkinter as tk

class SelectionController:
    def __init__(
        self,
        database: dict,
        db_manager: "DatabaseManager",
        collections_manager: "CollectionsManager",
    ) -> None:
        self.on_refresh_needed: Optional[Callable[[], None]] = None
        self.on_mode_changed: Optional[Callable[[bool], None]] = None
        self.on_projects_removed: Optional[Callable[[int], None]] = None

    def remove_selected(self, parent_window: tk.Misc | None) -> None:
        ...

# 2. API pública no DatabaseManager
class DatabaseManager:
    def get_project(self, path: str) -> dict | None:
        return self.database.get(path)

    def remove_project(self, path: str) -> bool:
        if path not in self.database: return False
        del self.database[path]
        return True

    def all_paths(self) -> list[str]:
        return list(self.database.keys())

    def project_count(self) -> int:
        return len(self.database)
```

```bash
# 3. Estrutura de testes
mkdir -p tests
touch tests/__init__.py
touch tests/test_database.py
touch tests/test_selection_controller.py
touch tests/test_collections_manager.py
pip install pytest pytest-cov
pytest --cov=core --cov=ui/controllers --cov-report=term-missing
```

### Sprint 3 — Refatoração Estrutural

```python
# Decomposição do __init__ do main_window.py
class LaserflixMainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self._setup_core()
        self._setup_controllers()
        self._build_ui()
        self._setup_callbacks()
        self._setup_managers()
        self._startup()

    def _setup_core(self) -> None:
        """Inicializa DatabaseManager, CollectionsManager, AI stack."""
        ...

    def _setup_controllers(self) -> None:
        """Instancia todos os controllers."""
        ...

    def _build_ui(self) -> None:
        """Constrói todos os widgets via builders."""
        ...

    def _setup_callbacks(self) -> None:
        """Conecta todos os callbacks dos controllers."""
        ...

    def _setup_managers(self) -> None:
        """Inicializa managers de dialog, toggle, etc."""
        ...

    def _startup(self) -> None:
        """Carrega dados iniciais e exibe primeira tela."""
        ...
```

---

## Histórico deste Documento

| Versão | Data | Evento |
|---|---|---|
| 1.0.0 | 09/03/2026 | Criação — análise técnica sênior + veredito da banca doutoral |

---

> *Documento gerado por análise automatizada de código-fonte via Perplexity AI (Claude Sonnet 4.6)*  
> *Banca simulada com base nos critérios reais de avaliação de doutorado em Engenharia de Software*  
> *Todos os problemas e soluções apontados foram verificados diretamente no código-fonte do repositório*
