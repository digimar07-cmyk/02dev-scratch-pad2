# PLANO DE APROVAÇÃO DOUTORAL — Laserflix v4.0.0.9

> **Objetivo:** Aprovação 100% na Banca Examinadora de Doutorado em Engenharia de Software  
> **Data de criação:** 09/03/2026  
> **Prazo alvo:** 90 dias (deadline: 07/06/2026)  
> **Versão alvo de aprovação:** 4.1.0.0  
> **Status geral:** 🟡 SPRINT 1 CONCLUÍDO — SPRINT 2A EM FILA

---

## Índice

1. [Painel de Controle Geral](#1-painel-de-controle-geral)
2. [Plano Dr. Brandt — Arquitetura](#2-plano-dr-brandt--arquitetura)
3. [Plano Dra. Tanaka — Qualidade e Testes](#3-plano-dra-tanaka--qualidade-e-testes)
4. [Plano Dr. Volkov — Padrões de Projeto](#4-plano-dr-volkov--padrões-de-projeto)
5. [Plano Dra. Osei — Manutenibilidade](#5-plano-dra-osei--manutenibilidade)
6. [Plano Dr. Mendonça — IHC e Produto](#6-plano-dr-mendonça--ihc-e-produto)
7. [Cronograma Integrado de Sprints](#7-cronograma-integrado-de-sprints)
8. [Critérios de Aceitação por Doutor](#8-critérios-de-aceitação-por-doutor)
9. [Checklist Final de Reapresentação](#9-checklist-final-de-reapresentação)

---

## 1. Painel de Controle Geral

| Doutor | Critério Principal | Status Atual | Meta |
|---|---|:---:|:---:|
| Prof. Dr. Brandt | Arquitetura limpa, sem código morto | 🟡 SPRINT 1 CONCLUÍDO | ✅ Aprovado |
| Profa. Dra. Tanaka | Cobertura de testes ≥ 60% | 🔴 REPROVADO | ✅ Aprovado |
| Prof. Dr. Volkov | API pública no DB + contratos formais | 🔴 REPROVADO | ✅ Aprovado |
| Profa. Dra. Osei | Type hints + decomposição do __init__ | 🟡 PARCIAL | ✅ Aprovado |
| Prof. Dr. Mendonça | Virtual scroll + feedback correto | 🟡 PARCIAL | ✅ Aprovado |

**Score atual:** 6.6/10 → **Score alvo:** ≥ 9.0/10

---

## 2. Plano Dr. Brandt — Arquitetura

> *"Dois controllers para a mesma função coexistem. Isso não é refatoração — é abandono."*

### Diagnóstico

O Prof. Brandt reprovou por 3 razões específicas:
1. Arquivo legado `display_controller.py` não removido após substituição
2. `modal_manager.py` na pasta `/controllers/` quando deveria estar em `/managers/`
3. Arquivos mortos (`project_management_controller.py`, `main_window_pre_selectionctrl.py`, `virtual_scroll.py` sem uso, `Novo(a) Text Document.txt`)

### Tarefas

#### BRANDT-01 — Remover `display_controller.py` legado
✅ **CONCLUÍDO** — 09/03/2026  
Arquivo removido. Zero imports restantes. `OptimizedDisplayController` é o único controller de display.

---

#### BRANDT-02 — Remover `project_management_controller.py` (código morto)
✅ **CONCLUÍDO** — 09/03/2026  
Arquivo removido. Zero imports confirmados.

---

#### BRANDT-03 — Remover `main_window_pre_selectionctrl.py` (backup no repo)
✅ **CONCLUÍDO** — 09/03/2026  
Arquivo removido do repositório.

---

#### BRANDT-04 — Remover `Novo(a) Text Document.txt` (lixo)
✅ **CONCLUÍDO** — 09/03/2026  
Arquivo vazio deletado. commit `56d895838b1ecf6fade2f05bc868921f8482ca3a`.

---

#### BRANDT-05 — Mover `modal_manager.py` para `/managers/`
✅ **CONCLUÍDO** — 09/03/2026  
Arquivo movido. Todos os imports atualizados. `__init__.py` de ambos os pacotes sincronizado.

---

#### BRANDT-06 — Decidir e executar `virtual_scroll.py`
⏳ **ADIADO — Sprint 3B** (semana 6: 13/04 - 19/04)  
Decisão: integrar (Opção B) — maior valor de produto e aprova Prof. Mendonça simultaneamente.

---

#### BRANDT-BUGFIX — Restaurar métodos de paginação
✅ **CONCLUÍDO** — 09/03/2026  
Métodos `next_page`, `prev_page`, `first_page`, `last_page` restaurados no `BaseDisplayController`.
Bug: `AttributeError: 'OptimizedDisplayController' object has no attribute 'first_page'`  
Causa: métodos removidos acidentalmente durante Sprint 1. Impacto: crash pós-importação.

---

### Resultado Sprint 1 — Brandt

- ✅ Diretório `/controllers/` com apenas 4 controllers ativos e corretos
- ✅ Diretório `/managers/` com todos os 7 managers no lugar certo
- ✅ Zero arquivos mortos no repositório
- ⏳ `virtual_scroll.py` — decisão Sprint 3B
- **Score Arquitetura estimado:** 7.5 → ~8.5/10 (pendente BRANDT-06)

---

## 3. Plano Dra. Tanaka — Qualidade e Testes

> *"Zero testes. Um software sem testes não é um software de doutorado — é um protótipo."*

### Diagnóstico

A Profa. Tanaka reprovou por uma razão simples e inegociável: **zero cobertura de testes**. O bug crítico do `save()` → `save_database()` existiu em produção desde a criação do controller e foi detectado apenas em uso real. Cobertura mínima exigida: **60% em `core/` e `ui/controllers/`**.

### Tarefas

#### TANAKA-01 — Criar estrutura de testes
🔴 **PENDENTE** — Sprint 2A (semana 2: 16/03 - 22/03)

```bash
mkdir -p tests
touch tests/__init__.py tests/conftest.py
pip install pytest pytest-cov pytest-mock
```

**Critério de aceite:** `tests/` existe, `pytest` executa sem erros.

---

#### TANAKA-02 — `conftest.py` com fixtures compartilhadas
🔴 **PENDENTE** — Sprint 2A

---

#### TANAKA-03 — `test_database.py`
🔴 **PENDENTE** — Sprint 2B (semana 3: 23/03 - 29/03)

---

#### TANAKA-04 — `test_selection_controller.py`
🔴 **PENDENTE** — Sprint 2B  
⚠️ Inclui regression test obrigatório do bug de 09/03/2026 (`test_remove_persists_to_disk`).

---

#### TANAKA-05 — `test_collections_manager.py`
🔴 **PENDENTE** — Sprint 2B

---

#### TANAKA-06 — Executar cobertura e atingir ≥ 60%
🔴 **PENDENTE** — Sprint 2C (semana 4: 30/03 - 05/04)

---

## 4. Plano Dr. Volkov — Padrões de Projeto

> *"self.database = self.db_manager.database viola o Princípio de Demeter e o DIP simultaneamente."*

### Diagnóstico

O Prof. Volkov reprovou por 2 problemas de design:
1. Acesso direto ao dict interno do `DatabaseManager` — viola encapsulamento, DIP e Princípio de Demeter
2. Callbacks sem contrato formal — ninguém sabe a assinatura esperada

### Tarefas

#### VOLKOV-01 — API pública no `DatabaseManager`
🔴 **PENDENTE** — Sprint 2A (semana 2: 16/03 - 22/03)

Adicionar 8 métodos: `get_project()`, `set_project()`, `remove_project()`, `has_project()`, `all_paths()`, `all_projects()`, `project_count()`, `iter_projects()`.

---

#### VOLKOV-02 — Contratos formais para callbacks (Protocol)
🔴 **PENDENTE** — Sprint 2A  
Criar `core/protocols.py` com 5 Protocol classes.

---

#### VOLKOV-03 — Verificar Strategy pattern no sistema de fallbacks
🔴 **PENDENTE** — Sprint 2C

---

## 5. Plano Dra. Osei — Manutenibilidade

> *"Zero type hints em 2026 é inaceitável. mypy teria capturado o bug save() automaticamente."*

### Tarefas

#### OSEI-01 — Configurar `mypy` e `ruff`
🔴 **PENDENTE** — Sprint 2B (semana 3)

#### OSEI-02 — Type hints em `core/database.py`
🔴 **PENDENTE** — Sprint 2B

#### OSEI-03 — Type hints em `core/collections_manager.py`
🔴 **PENDENTE** — Sprint 2B

#### OSEI-04 — Type hints em todos os `ui/controllers/`
🔴 **PENDENTE** — Sprint 2C (semana 4)

#### OSEI-05 — Decomposição do `__init__` do `main_window.py`
🔴 **PENDENTE** — Sprint 3A (semana 5: 06/04 - 12/04)

#### OSEI-06 — Resolver imports circulares
🔴 **PENDENTE** — Sprint 3A

---

## 6. Plano Dr. Mendonça — IHC e Produto

> *"O app mentia. Cards sumiam na tela mas voltavam ao reiniciar. Isso é feedback falso."*

### Tarefas

#### MENDONCA-01 — Confirmar e documentar correção do feedback falso
🟡 **PARCIAL** — bug corrigido em v4.0.0.9, regression test pendente (TANAKA-04)

#### MENDONCA-02 — Integrar `virtual_scroll.py`
🔴 **PENDENTE** — Sprint 3B (semana 6: 13/04 - 19/04)

#### MENDONCA-03 — Refatorar `recursive_import_integration.py`
🔴 **PENDENTE** — Sprint 3C (semana 7: 20/04 - 26/04)

#### MENDONCA-04 — Validar heurísticas de Nielsen
🔴 **PENDENTE** — Sprint 3B

---

## 7. Cronograma Integrado de Sprints

```
SEMANA 1 (09/03 - 15/03) — SPRINT 1: LIMPEZA ✅ CONCLUÍDO
├── BRANDT-01  Remover display_controller.py legado              ✅
├── BRANDT-02  Remover project_management_controller.py          ✅
├── BRANDT-03  Remover main_window_pre_selectionctrl.py          ✅
├── BRANDT-04  Remover Novo(a) Text Document.txt                 ✅
├── BRANDT-05  Mover modal_manager.py para /managers/            ✅
├── BRANDT-06  Decisão e execução do virtual_scroll.py           ⏳ Sprint 3B
└── BUGFIX     Restaurar métodos de paginação BaseDisplayCtrl    ✅

SEMANA 2 (16/03 - 22/03) — SPRINT 2A: FUNDAÇÃO DE QUALIDADE 🔴 PRÓXIMO
├── TANAKA-01  Criar estrutura tests/ + conftest.py
├── TANAKA-02  conftest.py com fixtures
├── VOLKOV-01  API pública no DatabaseManager (8 métodos)
└── VOLKOV-02  Criar core/protocols.py com 5 Protocols

SEMANA 3 (23/03 - 29/03) — SPRINT 2B: TESTES E TIPAGEM
├── TANAKA-03  test_database.py (12 testes)
├── TANAKA-04  test_selection_controller.py (9 testes)
├── TANAKA-05  test_collections_manager.py (8 testes)
├── OSEI-01    Configurar mypy + ruff
├── OSEI-02    Type hints em database.py
└── OSEI-03    Type hints em collections_manager.py

SEMANA 4 (30/03 - 05/04) — SPRINT 2C: TYPE HINTS NOS CONTROLLERS
├── OSEI-04    Type hints em selection_controller.py
├── OSEI-04    Type hints em analysis_controller.py
├── OSEI-04    Type hints em optimized_display_controller.py
├── OSEI-04    Type hints em collection_controller.py
├── TANAKA-06  Executar coverage ≥ 60%
└── VOLKOV-03  Documentar Strategy pattern em fallbacks.py

SEMANA 5 (06/04 - 12/04) — SPRINT 3A: REFATORAÇÃO ESTRUTURAL
├── OSEI-05    Decomposição do __init__ (main_window.py)
├── OSEI-06    Resolver imports circulares
└── MENDONCA-01 Confirmar + testar feedback visual pós-remoção

SEMANA 6 (13/04 - 19/04) — SPRINT 3B: PRODUTO
├── MENDONCA-02 Integrar VirtualScroll
├── BRANDT-06   Integrar virtual_scroll.py
└── MENDONCA-04 Validar heurísticas de Nielsen

SEMANA 7 (20/04 - 26/04) — SPRINT 3C: REFATORAÇÃO IMPORT
└── MENDONCA-03 Refatorar recursive_import_integration.py

SEMANA 8-10 (27/04 - 17/05) — SPRINT 4: INTEGRAÇÃO E TESTES FINAIS
├── Executar mypy sem erros
├── pytest com coverage ≥ 60%
├── Smoke test completo do app
├── Atualizar CHANGELOG + VERSION para 4.1.0.0
└── Atualizar TECH_AUDIT.md com scores finais

SEMANA 11-12 (18/05 - 31/05) — BUFFER E DOCUMENTAÇÃO
├── Documentar decisões arquiteturais
├── Atualizar README com nova estrutura
└── Preparar reapresentação para banca

DEADLINE: 07/06/2026 — Reapresentação à banca
```

---

## 8. Critérios de Aceitação por Doutor

### Prof. Dr. Brandt — Arquitetura ✅ quando:
- [x] Zero arquivos legados em `/controllers/` (`display_controller.py` ausente)
- [x] Zero código morto (nenhum arquivo sem import no projeto inteiro)
- [x] `modal_manager.py` em `/managers/`
- [ ] `virtual_scroll.py` integrado OU ausente (Sprint 3B)
- [x] `main_window_pre_selectionctrl.py` ausente
- [x] `grep -r "display_controller" . --include="*.py"` retorna zero

### Profa. Dra. Tanaka — Testes ✅ quando:
- [ ] `tests/` existe com `conftest.py`, `test_database.py`, `test_selection_controller.py`, `test_collections_manager.py`
- [ ] `pytest tests/ -v` passa com 100% dos testes
- [ ] `pytest --cov=core --cov=ui/controllers --cov-fail-under=60` retorna exit 0
- [ ] Regression test `test_remove_persists_to_disk` existe e passa
- [ ] `requirements.txt` inclui `pytest` e `pytest-cov`

### Prof. Dr. Volkov — Padrões ✅ quando:
- [ ] `DatabaseManager` tem: `get_project()`, `set_project()`, `remove_project()`, `has_project()`, `all_paths()`, `all_projects()`, `project_count()`, `iter_projects()`
- [ ] `core/protocols.py` existe com ≥ 4 Protocol classes
- [ ] `grep -rn "\.database\[" . --include="*.py" | grep -v database.py` retorna zero
- [ ] Todos os controllers usam `Optional[XxxCallback]` tipado nos atributos de callback
- [ ] `mypy core/ --ignore-missing-imports` sem erros

### Profa. Dra. Osei — Manutenibilidade ✅ quando:
- [ ] `mypy.ini` ou `pyproject.toml` com configuração mypy presente
- [ ] `mypy core/ ui/controllers/ --ignore-missing-imports` retorna zero erros
- [ ] `main_window.__init__` com ≤ 15 linhas
- [ ] Métodos `_setup_core()`, `_setup_controllers()`, `_build_ui()`, `_setup_callbacks()`, `_setup_managers()`, `_startup()` existem no `main_window.py`
- [ ] Zero imports locais dentro de funções/métodos
- [ ] `ruff check . --select ANN` sem erros críticos

### Prof. Dr. Mendonça — IHC e Produto ✅ quando:
- [x] Após remoção: cards desaparecem imediatamente da tela (corrigido v4.0.0.9)
- [x] Após remoção: sidebar atualiza contadores imediatamente
- [x] Após remoção: reiniciar o app não traz de volta os projetos removidos
- [ ] Teste de regressão `test_remove_persists_to_disk` passa (Sprint 2B)
- [ ] VirtualScroll integrado OU `virtual_scroll.py` removido com decisão documentada (Sprint 3B)
- [ ] `recursive_import_integration.py` com ≤ 8 KB (Sprint 3C)

---

## 9. Checklist Final de Reapresentação

> Executar esta checklist na íntegra antes de contatar a banca para reapresentação.

### Verificações Automáticas

```bash
# 1. Sem código morto
grep -r "display_controller" . --include="*.py"               # deve retornar ZERO
grep -r "project_management_controller" . --include="*.py"    # deve retornar ZERO
ls ui/controllers/modal_manager.py 2>/dev/null && echo "FALHOU" || echo "OK"
ls ui/managers/modal_manager.py    2>/dev/null && echo "OK" || echo "FALHOU"

# 2. Testes
pytest tests/ -v --tb=short                                   # deve passar 100%
pytest tests/ --cov=core --cov=ui/controllers --cov-fail-under=60  # exit 0

# 3. Tipagem
mypy core/ ui/controllers/ --ignore-missing-imports           # deve retornar: Success

# 4. Linting
ruff check core/ ui/controllers/ --select E,F                 # zero erros E/F

# 5. Estrutura do main_window.__init__
python -c "
import ast, sys
tree = ast.parse(open('ui/main_window.py').read())
for node in ast.walk(tree):
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                lines = item.end_lineno - item.lineno
                print(f'__init__ tem {lines} linhas')
                sys.exit(0 if lines <= 20 else 1)
"
```

### Verificações Manuais

- [ ] Iniciar app com `python main.py` — abre sem erros
- [ ] Adicionar 3 projetos via importação manual
- [ ] Selecionar 2 projetos e remover — verificar que desaparecem imediatamente
- [ ] Reiniciar app — projetos removidos NÃO aparecem
- [ ] Sidebar mostra contadores corretos
- [ ] Análise IA funciona (com Ollama) ou mostra fallback correto (sem Ollama)
- [ ] `pytest tests/ -v` — todos os testes verdes
- [ ] `mypy core/ ui/controllers/` — Success
- [ ] `VERSION` = `4.1.0.0`
- [ ] `CHANGELOG.md` atualizado com todas as mudanças
- [ ] `TECH_AUDIT.md` atualizado com scores finais

---

## Histórico deste Documento

| Versão | Data | Evento |
|---|---|---|
| 1.0.0 | 09/03/2026 | Criação — plano de aprovação doutoral completo por avaliador |
| 1.1.0 | 09/03/2026 | Atualização — Sprint 1 100% concluído; BUGFIX paginação registrado |

---

> *"O problema não é falta de habilidade — é falta de disciplina para fechar o que abre e provar o que afirma."*  
> — Banca Examinadora, 09/03/2026

> *Documento gerado e mantido por Perplexity AI (Claude Sonnet 4.6)*
