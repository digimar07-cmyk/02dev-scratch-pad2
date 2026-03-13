# Plano de Desenvolvimento Laserflix v4.0

> Criado em: 2026-03-13
> Metodologia: Akita/XP (ver AKITA_METODOLOGIA.md)
> Status atual: **PRÉ-FASE 0 — Base Limpa concluída**

---

## Status de Execução

```
✅ PRÉ-FASE 0   — Limpeza e arquivamento (2026-03-13)
⏳ FASE 0       — Fundação de Segurança            ← PRÓXIMA
○  FASE 1       — Críticos Imediatos
○  FASE 2       — Infraestrutura de Testes
○  FASE 3       — Migração SQLite
○  FASE 4       — Refatoração de Módulos
○  FASE 5       — Qualidade de Código
○  FASE 6       — Melhorias Pós-Estabilização
```

**Legenda:** ✅ Concluído | ⏳ Em andamento | ○ Aguardando

---

## PRÉ-FASE 0 — Base Limpa ✅

**Executado em:** 2026-03-13

### O que foi feito:
- [x] Análise técnica completa do projeto (parecer: 7.2/10)
- [x] Testes antigos movidos para `tests/_archived/` (não deletados)
- [x] Docs obsoletos movidos para `docs/archive/`
- [x] Nova estrutura de testes criada (vazia, limpa)
- [x] `conftest.py` reescrito do zero
- [x] `pytest.ini` criado com configuração correta
- [x] `.gitignore` atualizado
- [x] 3 documentos de referência criados
- [x] Arquivo `C` (erro de commit) identificado para remoção

### Problemas identificados na análise:
1. **CRÍTICO**: Banco JSON não escala (→ Fase 3)
2. **CRÍTICO**: Cobertura de testes ~15-20% (→ Fase 2)
3. **CRÍTICO**: `recursive_import_integration.py` 20KB responsabilidade dupla (→ Fase 4)
4. **CRÍTICO**: Imports circulares dentro de método (→ Fase 1)
5. **CRÍTICO**: `__del__` não-determinístico para cleanup (→ Fase 1)
6. **MÉDIO**: Logging com f-strings em vez de `%s` (→ Fase 1)
7. **MÉDIO**: `get_card_callbacks()` retorna dict com 17 entradas sem tipo (→ Fase 4)
8. **MÉDIO**: Collections e DB sem transação atômica (→ Fase 3)

---

## FASE 0 — Fundação de Segurança ⏳

**Duração estimada:** 1-2 dias  
**Pré-requisito:** Base Limpa concluída ✅

### Tarefas:

#### 0.1 — Verificar que a nova estrutura de testes funciona
- [ ] Fazer `git pull` da base limpa
- [ ] Rodar `cd LASERFLIX_2 && python -m pytest` → deve mostrar **0 tests collected** ou apenas smoke
- [ ] Confirmar que não há erros de import no `conftest.py`
- [ ] Reportar resultado ao AI para prosseguir

#### 0.2 — Smoke Test de Imports (AI executa)
- [ ] Criar `tests/smoke/test_startup.py` com testes de import dos módulos principais
- [ ] Criar `tests/smoke/test_database_init.py` com teste de inicialização do DatabaseManager
- [ ] Rodar: todos devem passar (GREEN)

#### 0.3 — Baseline de Cobertura (AI executa)
- [ ] Rodar `pytest --cov=. --cov-report=term-missing`
- [ ] Documentar resultado em `QA/BASELINE_COVERAGE.md`
- [ ] Este número é o baseline — nunca pode DIMINUIR após qualquer fase

#### 0.4 — Remover arquivo `C` da raiz (AI executa)
- [ ] Deletar `LASERFLIX_2/C` (erro de commit confirmado)
- [ ] Verificar `.gitignore` — adicionar entradas faltantes

**Critério de conclusão da Fase 0:**
- pytest roda sem erros de configuração
- Smoke tests passando (GREEN)
- Baseline documentado
- Arquivo `C` removido

---

## FASE 1 — Críticos Imediatos ○

**Duração estimada:** 2-3 dias  
**Pré-requisito:** Fase 0 concluída

### Tarefas:

#### 1.1 — Corrigir `__del__` → `_on_close()` (TDD)
- [ ] Escrever `tests/unit/test_main_window_lifecycle.py` (RED)
- [ ] Implementar `_on_close()` + `WM_DELETE_WINDOW` em `main_window.py` (GREEN)
- [ ] Remover `__del__` (REFACTOR)
- [ ] Todos os testes passando

#### 1.2 — Corrigir imports circulares em `display_projects()`
- [ ] Mover imports para o topo do arquivo
- [ ] Se import circular: documentar cadeia e resolver com injeção
- [ ] Smoke tests continuam passando

#### 1.3 — Corrigir logging f-strings (todos os arquivos)
- [ ] Script de localização: `grep -rn 'logger.*f"' . --include="*.py"`
- [ ] Substituir todos por `logger.X("%s", var)` lazy
- [ ] Commit por módulo

---

## FASE 2 — Infraestrutura de Testes ○

**Duração estimada:** 3-5 dias  
**Pré-requisito:** Fase 1 concluída  
**Meta:** Cobertura 0% → 70%+

### Módulos a cobrir (em ordem de prioridade):

1. `core/database.py` → 95%+ (crítico, já tem API documentada)
2. `core/collections_manager.py` → 85%+
3. `utils/` (todos os módulos) → 85%+
4. `ai/fallback_generator.py` → 75%+
5. `ai/ollama_client.py` → 70%+
6. `ui/main_window.py` → 50%+ (smoke de lifecycle)

### Tipos de teste a criar:

```
tests/unit/test_database_full.py         — API pública, persistência, migração, backup
tests/unit/test_collections_manager.py   — CRUD de coleções
tests/unit/test_fallback_generator.py    — contratos de AI fallback
tests/integration/test_import_pipeline.py — scan→dedup→db
tests/structural/test_file_sizes.py      — guardião de tamanho
tests/structural/test_layer_isolation.py — core/ não importa ui/
```

---

## FASE 3 — Migração SQLite ○

**Duração estimada:** 5-7 dias  
**Pré-requisito:** Fase 2 concluída (testes de database passando)
**Estratégia:** Strangler Fig — API idêntica, troca por feature flag

### Tarefas:
1. Definir e aprovar schema SQL (ver proposta em AKITA_METODOLOGIA.md)
2. Criar `core/database_sqlite.py` com API idêntica (TDD primeiro)
3. Criar script `utils/migrate_json_to_sqlite.py`
4. Implementar feature flag `USE_SQLITE` em `config/settings.py`
5. Criar factory `core/get_database_manager()`
6. Migrar `CollectionsManager` para usar mesmo DB
7. Teste de integração do pipeline completo com SQLite

---

## FASE 4 — Refatoração de Módulos ○

**Duração estimada:** 3-4 dias  
**Pré-requisito:** Fase 2 concluída

### Tarefas:
1. Quebrar `recursive_import_integration.py` (20KB) em:
   - `core/recursive_scanner.py` (lógica pura, sem tkinter)
   - `ui/recursive_import_dialog.py` (só UI)
2. Criar `ui/card_callbacks.py` com `CardCallbacks` dataclass tipado
3. Atualizar `core/protocols.py` com `DatabaseProtocol` runtime-checkable
4. Teste estrutural: `core/` não importa `tkinter`

---

## FASE 5 — Qualidade de Código ○

**Duração estimada:** 2-3 dias  
**Pré-requisito:** Fases 1-4 concluídas

### Tarefas:
1. Type hints completos em `core/`, `utils/`, `ai/`
2. `mypy --strict` passando em `core/` e `utils/`
3. `conftest.py` com fixtures globais reutilizáveis
4. Relatório final de cobertura em `QA/COVERAGE_REPORT_v4.md`

### Meta de cobertura final:
```
core/database.py            → 95%+
core/collections_manager.py → 85%+
utils/                      → 85%+
ai/                         → 75%+
ui/main_window.py           → 50%+
TOTAL                       → 70%+
```

---

## FASE 6 — Melhorias Pós-Estabilização ○

**Início:** somente após CI 100% verde nas Fases 0-5

### Itens candidatos (priorizar com usuário):
1. Virtual Scroll Real ativado para 500+ itens
2. Search semântico com embeddings (sqlite-vec ou Ollama)
3. Export/Import de banco como `.db` portável
4. Paginação definitiva (virtual scroll vs. paginação clássica — decidir)
5. UI: dark mode configurável
6. Performance: lazy loading de thumbnails otimizado

---

## Regras de Ouro (Nunca Violar)

1. **CI sempre verde** — `pytest` passa antes de qualquer commit
2. **TDD obrigatório** — teste antes do código para features novas
3. **Commits atômicos** — nunca `git add .` com múltiplas responsabilidades
4. **Aprovação do usuário** — cada fase concluída requer `git pull` + teste + feedback
5. **Nunca diminuir cobertura** — baseline é o piso, nunca o teto
6. **Tidy First** — refatoração e feature são commits separados

---

## Como Atualizar Este Documento

Após cada tarefa concluída:
1. Marcar `[ ]` como `[x]`
2. Atualizar o **Status de Execução** no topo
3. Adicionar data de conclusão
4. Commit: `docs: atualiza status PLANO_DESENVOLVIMENTO_V4 — fase X.Y concluída`
